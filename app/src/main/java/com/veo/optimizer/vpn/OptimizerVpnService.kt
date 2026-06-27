package com.veo.optimizer.vpn

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.Intent
import android.net.VpnService
import android.os.Build
import android.os.ParcelFileDescriptor
import android.util.Log
import com.veo.optimizer.MainActivity
import com.veo.optimizer.R
import com.veo.optimizer.xray.XrayManager
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject

/**
 * Android replacement for the desktop `tun_manager` (TunManager) module.
 *
 * The desktop app installed Wintun, created a TUN adapter, set up routes and
 * the default gateway, then ran xray in tun mode. On Android the OS provides
 * all of that through VpnService:
 *   • Builder.establish() returns the tun fd (replaces Wintun adapter)
 *   • addRoute("0.0.0.0", 0) replaces setup_routes/_get_default_gateway
 *   • The system tears the interface down (replaces teardown_routes)
 *
 * The tun fd is handed to xray-core (via XrayManager.bridge) which runs its
 * tun2socks layer internally, so all device traffic flows through the VLESS
 * proxy outbound.
 */
class OptimizerVpnService : VpnService() {

    private var tunInterface: ParcelFileDescriptor? = null
    private val xray by lazy { XrayManager(this) }

    companion object {
        private const val TAG = "VpnService"
        const val ACTION_START = "com.veo.optimizer.START"
        const val ACTION_STOP = "com.veo.optimizer.STOP"
        const val EXTRA_CONFIG = "config_json"
        const val EXTRA_SERVER_IP = "server_ip"
        private const val CHANNEL_ID = "veo_vpn"
        private const val NOTIF_ID = 1001

        @Volatile var isActive: Boolean = false
            private set

        /** Shared bridge instance — AppViewModel uses this to query stats. */
        @Volatile var sharedBridge: XrayManager.XrayBridge? = null
            private set

        fun start(ctx: Context, configJson: String, serverIp: String) {
            val i = Intent(ctx, OptimizerVpnService::class.java).apply {
                action = ACTION_START
                putExtra(EXTRA_CONFIG, configJson)
                putExtra(EXTRA_SERVER_IP, serverIp)
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) ctx.startForegroundService(i)
            else ctx.startService(i)
        }

        fun stop(ctx: Context) {
            ctx.startService(Intent(ctx, OptimizerVpnService::class.java).apply { action = ACTION_STOP })
        }
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_STOP -> { teardown(); stopSelf(); return START_NOT_STICKY }
            ACTION_START -> {
                val cfg = intent.getStringExtra(EXTRA_CONFIG) ?: return START_NOT_STICKY
                val serverIp = intent.getStringExtra(EXTRA_SERVER_IP) ?: ""
                startTunnel(cfg, serverIp)
            }
        }
        return START_STICKY
    }

    /**
     * Auto-wire the real xray engine if it is present. We look up
     * `com.veo.optimizer.xray.LibXrayBridge` by reflection so the project
     * compiles and runs TODAY with the NoopBridge; the moment you add the
     * libXray AAR and rename LibXrayBridge.kt.example → LibXrayBridge.kt, this
     * picks it up automatically with no further code changes.
     */
    private fun wireBridgeIfAvailable() {
        if (xray.isInstalled) return
        runCatching {
            val cls = Class.forName("com.veo.optimizer.xray.LibXrayBridge")
            val ctor = cls.getConstructor(Context::class.java)
            xray.bridge = ctor.newInstance(this) as XrayManager.XrayBridge
            sharedBridge = xray.bridge
        }
    }

    private fun startTunnel(configJson: String, serverIp: String) {
        startForeground(NOTIF_ID, buildNotification())
        wireBridgeIfAvailable()

        // 1. Build the TUN interface — Android's equivalent of Wintun + routes.
        val builder = Builder()
            .setSession("VEO VLESS")
            .setMtu(1500)                      // matches XrayConfig.buildTun MTU
            .addAddress("198.18.0.1", 30)      // matches desktop tun_addr/prefix intent
            .addRoute("0.0.0.0", 0)            // route ALL ipv4 (replaces setup_routes)
            .addDnsServer("1.1.1.1")
            .addDnsServer("8.8.8.8")
            .setBlocking(true)

        // Keep our own app out of the tunnel so xray can reach the edge IP.
        runCatching { builder.addDisallowedApplication(packageName) }
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP_MR1)
            builder.setUnderlyingNetworks(null)

        val pfd = builder.establish() ?: run {
            Log.e(TAG, "VPN establish() returned null")
            teardown(); stopSelf(); return
        }
        tunInterface = pfd

        // 2. Hand the fd + config to xray-core (libXray bridge runs tun2socks).
        val cfg = runCatching { Json.decodeFromString(JsonObject.serializer(), configJson) }.getOrNull()
        if (cfg == null) {
            Log.e(TAG, "Failed to parse config JSON")
            teardown(); stopSelf(); return
        }

        runCatching {
            xray.start(cfg, pfd.fd)
        }.onFailure {
            Log.e(TAG, "xray.start() failed", it)
            teardown(); stopSelf(); return
        }

        // 3. Verify core actually started
        Thread.sleep(1500)
        if (!xray.isRunning) {
            Log.e(TAG, "xray-core did not start — isRunning=false after startLoop()")
            teardown(); stopSelf(); return
        }

        isActive = true
        sharedBridge = xray.bridge
        Log.i(TAG, "TUN active, xray-core running")
    }

    private fun teardown() {
        isActive = false
        sharedBridge = null
        runCatching { xray.stop() }
        runCatching { tunInterface?.close() }
        tunInterface = null
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.N) stopForeground(STOP_FOREGROUND_REMOVE)
        else @Suppress("DEPRECATION") stopForeground(true)
    }

    override fun onDestroy() { teardown(); super.onDestroy() }
    override fun onRevoke() { teardown(); stopSelf() }

    private fun buildNotification(): Notification {
        val nm = getSystemService(NotificationManager::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            nm.createNotificationChannel(
                NotificationChannel(CHANNEL_ID, getString(R.string.vpn_channel),
                    NotificationManager.IMPORTANCE_LOW)
            )
        }
        val pi = PendingIntent.getActivity(
            this, 0, Intent(this, MainActivity::class.java),
            PendingIntent.FLAG_IMMUTABLE or PendingIntent.FLAG_UPDATE_CURRENT
        )
        val b = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
            Notification.Builder(this, CHANNEL_ID) else @Suppress("DEPRECATION") Notification.Builder(this)
        return b.setContentTitle(getString(R.string.app_name))
            .setContentText(getString(R.string.vpn_running))
            .setSmallIcon(R.drawable.ic_launcher_foreground)
            .setContentIntent(pi)
            .setOngoing(true)
            .build()
    }
}
