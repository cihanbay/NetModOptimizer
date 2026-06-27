package com.veo.optimizer.xray

import android.content.Context
import com.veo.optimizer.core.ConfigProfile
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import java.io.File
import java.net.HttpURLConnection
import java.net.InetSocketAddress
import java.net.Proxy
import java.net.URL

/**
 * Android port of XrayManager.
 *
 * On the desktop, this downloaded the xray-core binary and ran it as a
 * subprocess. Android cannot exec arbitrary binaries from app storage on
 * modern OS versions, so we drive xray-core through the Go-mobile bridge
 * (libXray / AndroidLibXrayLite AAR). The actual process lifecycle lives in
 * the VpnService; this manager builds configs and runs the latency/speed
 * tests that the desktop XrayManager exposed as static helpers.
 *
 * To enable real tunnelling: add the libXray AAR to app/libs, then implement
 * [XrayBridge] with calls to libv2ray.Libv2ray.* and set [bridge].
 */
class XrayManager(private val ctx: Context) {

    /** Pluggable xray-core engine. Default is a no-op so the app compiles
     *  without the native AAR; wire a real bridge to enable tunnelling. */
    interface XrayBridge {
        fun start(configJson: String, tunFd: Int)
        fun stop()
        fun queryStats(tag: String, direct: String): Long
        val isRunning: Boolean
    }

    object NoopBridge : XrayBridge {
        override fun start(configJson: String, tunFd: Int) {}
        override fun stop() {}
        override fun queryStats(tag: String, direct: String): Long = 0
        override val isRunning: Boolean = false
    }

    var bridge: XrayBridge = NoopBridge

    private val json = Json { prettyPrint = false }

    fun configFile(name: String, cfg: JsonObject): File {
        val f = File(ctx.cacheDir, name)
        f.writeText(json.encodeToString(JsonObject.serializer(), cfg))
        return f
    }

    val isInstalled: Boolean get() = bridge !is NoopBridge

    fun start(cfg: JsonObject, tunFd: Int) =
        bridge.start(json.encodeToString(JsonObject.serializer(), cfg), tunFd)

    fun stop() = bridge.stop()

    val isRunning: Boolean get() = bridge.isRunning

    // ── Network quality tests (port of latency/dl_speed/up_speed) ────────────
    companion object {
        /** Port of XrayManager.latency — HTTP latency through a local proxy. */
        suspend fun latency(socksPort: Int): Pair<Double?, String?> = withContext(Dispatchers.IO) {
            runCatching {
                val proxy = Proxy(Proxy.Type.SOCKS, InetSocketAddress("127.0.0.1", socksPort))
                val t0 = System.nanoTime()
                val c = URL("https://www.gstatic.com/generate_204").openConnection(proxy) as HttpURLConnection
                c.connectTimeout = 8000; c.readTimeout = 8000
                val code = c.responseCode
                c.disconnect()
                if (code in 200..399) ((System.nanoTime() - t0) / 1e6) to null
                else null to "http-$code"
            }.getOrElse { null to (it.message ?: "err") }
        }

        /** Port of XrayManager.dl_speed — download throughput in Mbps. */
        suspend fun dlSpeed(socksPort: Int): Pair<Double?, String?> = withContext(Dispatchers.IO) {
            runCatching {
                val proxy = Proxy(Proxy.Type.SOCKS, InetSocketAddress("127.0.0.1", socksPort))
                val url = URL("https://speed.cloudflare.com/__down?bytes=3000000")
                val t0 = System.nanoTime()
                val c = url.openConnection(proxy) as HttpURLConnection
                c.connectTimeout = 8000; c.readTimeout = 15000
                var total = 0L
                c.inputStream.use { ins ->
                    val buf = ByteArray(65536)
                    while (true) { val n = ins.read(buf); if (n < 0) break; total += n }
                }
                c.disconnect()
                val secs = (System.nanoTime() - t0) / 1e9
                (total * 8 / 1e6 / secs) to null
            }.getOrElse { null to (it.message ?: "err") }
        }

        /** Port of XrayManager.up_speed — upload throughput in Mbps. */
        suspend fun upSpeed(socksPort: Int, sizeBytes: Int = 1_000_000): Pair<Double?, String?> =
            withContext(Dispatchers.IO) {
                runCatching {
                    val proxy = Proxy(Proxy.Type.SOCKS, InetSocketAddress("127.0.0.1", socksPort))
                    val url = URL("https://speed.cloudflare.com/__up")
                    val payload = ByteArray(sizeBytes)
                    val t0 = System.nanoTime()
                    val c = url.openConnection(proxy) as HttpURLConnection
                    c.requestMethod = "POST"; c.doOutput = true
                    c.connectTimeout = 8000; c.readTimeout = 15000
                    c.outputStream.use { it.write(payload) }
                    c.responseCode
                    c.disconnect()
                    val secs = (System.nanoTime() - t0) / 1e9
                    (sizeBytes * 8 / 1e6 / secs) to null
                }.getOrElse { null to (it.message ?: "err") }
            }
    }
}
