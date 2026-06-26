package com.netmod.optimizer.scanner

import com.netmod.optimizer.core.CF_SNI_ROTATE
import com.netmod.optimizer.core.ProbeResult
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import kotlinx.coroutines.withContext
import kotlinx.coroutines.withTimeoutOrNull
import java.io.BufferedReader
import java.net.InetAddress
import java.net.InetSocketAddress
import java.net.Socket
import java.security.SecureRandom
import java.security.cert.X509Certificate
import java.util.Base64
import javax.net.ssl.SSLContext
import javax.net.ssl.SSLSocket
import javax.net.ssl.SSLSocketFactory
import javax.net.ssl.TrustManager
import javax.net.ssl.X509TrustManager

/**
 * Port of the `scanner` module (Optimizer).
 *
 * The desktop version used asyncio; here we use Kotlin coroutines + a
 * Semaphore for the same bounded-concurrency probing. TLS verification is
 * disabled exactly like the Python version (CERT_NONE) because we are
 * probing edge IPs by raw address, not by hostname.
 */
class Optimizer(
    concurrency: Int = 200,
    private val timeoutMs: Long = 5000,
    tries: Int = 4,
) {
    private val sem = Semaphore(concurrency.coerceAtLeast(1))
    private val tries = tries.coerceAtLeast(1)

    private val insecureFactory: SSLSocketFactory by lazy {
        val ctx = SSLContext.getInstance("TLS")
        val tm = arrayOf<TrustManager>(object : X509TrustManager {
            override fun checkClientTrusted(c: Array<X509Certificate>?, a: String?) {}
            override fun checkServerTrusted(c: Array<X509Certificate>?, a: String?) {}
            override fun getAcceptedIssuers(): Array<X509Certificate> = arrayOf()
        })
        ctx.init(null, tm, SecureRandom())
        ctx.socketFactory
    }

    companion object {
        /** Port of Optimizer.fix_range — expand CIDR / range / list / hostname. */
        fun fixRange(raw: String): List<String> {
            val s = raw.trim()
            if (s.isEmpty()) return emptyList()
            if (s.contains(",")) {
                val seen = LinkedHashSet<String>()
                s.split(",").forEach { part -> fixRange(part.trim()).forEach { seen.add(it) } }
                return seen.toList().take(65536)
            }
            if (s.any { it.isLetter() }) {
                return runCatching {
                    InetAddress.getAllByName(s).filter { it.address.size == 4 }
                        .map { it.hostAddress!! }.distinct().take(65536)
                }.getOrDefault(emptyList())
            }
            if (s.contains("-")) {
                val (a, b) = s.split("-", limit = 2)
                return runCatching {
                    var si = ipToLong(a.trim()); var ei = ipToLong(b.trim())
                    if (si > ei) { val t = si; si = ei; ei = t }
                    if (ei - si + 1 > 65536) ei = si + 65535
                    (si..ei).map { longToIp(it) }
                }.getOrDefault(emptyList())
            }
            return runCatching { expandCidr(s) }.getOrDefault(emptyList())
        }

        private fun ipToLong(ip: String): Long {
            val p = ip.split(".").map { it.toLong() }
            require(p.size == 4 && p.all { it in 0..255 })
            return (p[0] shl 24) or (p[1] shl 16) or (p[2] shl 8) or p[3]
        }

        private fun longToIp(v: Long): String =
            "${(v shr 24) and 0xff}.${(v shr 16) and 0xff}.${(v shr 8) and 0xff}.${v and 0xff}"

        private fun expandCidr(cidr: String): List<String> {
            if (!cidr.contains("/")) return listOf(cidr)
            val (base, bitsS) = cidr.split("/")
            val bits = bitsS.toInt()
            val baseLong = ipToLong(base)
            val mask = if (bits == 0) 0L else (-1L shl (32 - bits)) and 0xffffffffL
            val network = baseLong and mask
            val size = 1L shl (32 - bits)
            val hosts = if (size <= 2) listOf(network)
            else (network + 1 until network + size - 1).toList()
            return hosts.map { longToIp(it) }.take(65536)
        }
    }

    suspend fun probe(
        ip: String, port: Int, mode: String,
        sni: String, host: String, path: String,
    ): ProbeResult = sem.withPermit {
        val latencies = ArrayList<Double>()
        var lastError: String? = null

        for (attempt in 0 until tries) {
            val effSni = sni.ifEmpty { host.ifEmpty { CF_SNI_ROTATE[attempt % CF_SNI_ROTATE.size] } }
            val (ok, tcpMs) = tcp(ip, port)
            if (!ok) { lastError = "tcp-fail"; continue }
            when (mode) {
                "tcp" -> latencies.add(tcpMs)
                "tls" -> tlsRaw(ip, port, effSni)?.let { latencies.add(it) } ?: run { lastError = "tls-fail" }
                else -> httpRaw(ip, port, effSni, host, path.ifEmpty { "/" })
                    ?.let { latencies.add(it) } ?: run { lastError = "http-fail" }
            }
        }

        if (latencies.isEmpty())
            return@withPermit ProbeResult(ip, port, mode, null, lastError ?: "all-fail")

        val avg = latencies.average()
        val jitter = if (latencies.size > 1) latencies.max() - latencies.min() else 0.0
        val loss = (tries - latencies.size).toDouble() / tries * 100.0

        var colo = ""; var cfValid = false
        if (mode == "http") {
            val traceSni = sni.ifEmpty { host.ifEmpty { "speed.cloudflare.com" } }
            cfTrace(ip, port, traceSni).let { colo = it.first; cfValid = it.second }
        }
        ProbeResult(
            ip = ip, port = port, mode = mode, pingMs = avg, error = null,
            lossPct = loss, jitterMs = jitter, colo = colo, cfValid = cfValid,
        )
    }

    private suspend fun tcp(ip: String, port: Int): Pair<Boolean, Double> = withContext(Dispatchers.IO) {
        val t0 = System.nanoTime()
        runCatching {
            Socket().use { s ->
                s.connect(InetSocketAddress(ip, port), timeoutMs.toInt())
            }
            true to (System.nanoTime() - t0) / 1e6
        }.getOrElse { false to 0.0 }
    }

    private suspend fun tlsRaw(ip: String, port: Int, sni: String): Double? = withContext(Dispatchers.IO) {
        val t0 = System.nanoTime()
        runCatching {
            withTimeoutOrNull(timeoutMs) {
                val raw = Socket()
                raw.connect(InetSocketAddress(ip, port), timeoutMs.toInt())
                val ssl = insecureFactory.createSocket(raw, sni, port, true) as SSLSocket
                ssl.useClientMode = true
                ssl.startHandshake()
                ssl.close()
                (System.nanoTime() - t0) / 1e6
            }
        }.getOrNull()
    }

    private suspend fun httpRaw(ip: String, port: Int, sni: String, host: String, path: String): Double? =
        withContext(Dispatchers.IO) {
            val t0 = System.nanoTime()
            runCatching {
                withTimeoutOrNull(timeoutMs) {
                    val wsKey = Base64.getEncoder().encodeToString(ByteArray(16).also { SecureRandom().nextBytes(it) })
                    val reqHost = host.ifEmpty { sni.ifEmpty { ip } }
                    val raw = Socket()
                    raw.connect(InetSocketAddress(ip, port), timeoutMs.toInt())
                    val ssl = insecureFactory.createSocket(raw, sni, port, true) as SSLSocket
                    ssl.startHandshake()
                    val req = buildString {
                        append("GET $path HTTP/1.1\r\n")
                        append("Host: $reqHost\r\n")
                        append("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36\r\n")
                        append("Upgrade: websocket\r\n")
                        append("Connection: Upgrade\r\n")
                        append("Sec-WebSocket-Key: $wsKey\r\n")
                        append("Sec-WebSocket-Version: 13\r\n\r\n")
                    }
                    ssl.outputStream.write(req.toByteArray()); ssl.outputStream.flush()
                    val line = BufferedReader(ssl.inputStream.reader()).readLine() ?: ""
                    ssl.close()
                    val parts = line.split(" ")
                    if (parts.size < 2 || parts[1] != "101") null
                    else (System.nanoTime() - t0) / 1e6
                }
            }.getOrNull()
        }

    private suspend fun cfTrace(ip: String, port: Int, sni: String): Pair<String, Boolean> =
        withContext(Dispatchers.IO) {
            runCatching {
                withTimeoutOrNull(timeoutMs) {
                    val raw = Socket()
                    raw.connect(InetSocketAddress(ip, port), timeoutMs.toInt())
                    val ssl = insecureFactory.createSocket(raw, sni, port, true) as SSLSocket
                    ssl.startHandshake()
                    val req = "GET /cdn-cgi/trace HTTP/1.1\r\nHost: ${sni.ifEmpty { ip }}\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\n\r\n"
                    ssl.outputStream.write(req.toByteArray()); ssl.outputStream.flush()
                    val body = ssl.inputStream.readBytes().toString(Charsets.UTF_8)
                    ssl.close()
                    val colo = body.lineSequence().firstOrNull { it.startsWith("colo=") }
                        ?.substringAfter("=")?.trim().orEmpty()
                    colo to colo.isNotEmpty()
                } ?: ("" to false)
            }.getOrElse { "" to false }
        }
}
