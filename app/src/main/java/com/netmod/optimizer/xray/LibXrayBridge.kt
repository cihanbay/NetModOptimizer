package com.netmod.optimizer.xray

import android.content.Context
import android.util.Log
import libv2ray.CoreCallbackHandler
import libv2ray.CoreController
import libv2ray.Libv2ray

/**
 * Real xray-core engine, backed by AndroidLibXrayLite v26.6.22 (libv2ray.aar).
 *
 * API verified directly against the AAR's classes:
 *   Libv2ray.initCoreEnv(envPath, key)              // asset/cert path + xudp key
 *   Libv2ray.newCoreController(handler): CoreController
 *   controller.startLoop(configJson, tunFd: Int)    // sets xray.tun.fd, starts core
 *   controller.stopLoop()
 *   controller.queryStats(tag, "uplink"|"downlink"): Long
 *   controller.isRunning: Boolean
 *   interface CoreCallbackHandler { startup(): Long; shutdown(): Long; onEmitStatus(Long, String): Long }
 *
 * This xray-core build (XTLS, gVisor) has a native `tun` inbound. The config
 * produced by [XrayConfig.buildTun] contains that inbound; startLoop() exports
 * the VpnService file descriptor via the `xray.tun.fd` env var, so the core
 * reads packets straight from the tun fd — NO external tun2socks is required.
 *
 * This class is auto-installed by reflection from
 * OptimizerVpnService.wireBridgeIfAvailable(); keep the package + name +
 * (Context) constructor exactly as-is.
 */
class LibXrayBridge(private val ctx: Context) : XrayManager.XrayBridge {

    private val handler = object : CoreCallbackHandler {
        override fun startup(): Long = 0L
        override fun shutdown(): Long = 0L
        override fun onEmitStatus(code: Long, message: String?): Long {
            Log.i(TAG, "core[$code] $message")
            return 0L
        }
    }

    private var controller: CoreController? = null

    init {
        // Point xray at a writable dir for geoip/geosite. If the .dat files are
        // not present there, the AAR transparently falls back to the geoip.dat /
        // geosite.dat bundled inside it (golang.org/x/mobile/asset), so this
        // works out of the box.
        runCatching { Libv2ray.initCoreEnv(ctx.filesDir.absolutePath, "") }
            .onFailure { Log.w(TAG, "initCoreEnv failed", it) }
    }

    override fun start(configJson: String, tunFd: Int) {
        val c = controller ?: Libv2ray.newCoreController(handler).also { controller = it }
        // startLoop throws on failure (Go error -> Java exception); let the
        // VpnService's runCatching handle/log it.
        c.startLoop(configJson, tunFd)
    }

    override fun stop() {
        runCatching { controller?.stopLoop() }
            .onFailure { Log.w(TAG, "stopLoop failed", it) }
    }

    /** direct must be "uplink" or "downlink"; tag is the outbound tag ("proxy"). */
    override fun queryStats(tag: String, direct: String): Long =
        runCatching { controller?.queryStats(tag, direct) ?: 0L }.getOrDefault(0L)

    override val isRunning: Boolean get() = runCatching { controller?.isRunning ?: false }.getOrDefault(false)

    private companion object { const val TAG = "LibXrayBridge" }
}
