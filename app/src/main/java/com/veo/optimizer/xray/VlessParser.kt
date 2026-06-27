package com.veo.optimizer.xray

import com.veo.optimizer.core.ConfigProfile
import java.net.URLDecoder

/** Parsed vless:// link (port of App._parse_vless_url). */
data class VlessLink(
    val uid: String, val host: String, val sni: String, val path: String,
    val network: String, val security: String, val fp: String, val alpn: String,
    val grpcService: String, val allowInsecure: Boolean, val cfgName: String,
    val server: String, val port: Int,
) {
    /** Merge link values into a ConfigProfile (mirrors the desktop import flow). */
    fun applyTo(p: ConfigProfile) {
        p.uid = uid; p.host = host; p.sni = sni; p.path = path
        p.network = network; p.security = security; p.fp = fp; p.alpn = alpn
        p.grpcService = grpcService; p.allowInsecure = allowInsecure; p.cfgName = cfgName
    }
}

object VlessParser {
    private fun dec(s: String) = runCatching { URLDecoder.decode(s, "UTF-8") }.getOrDefault(s)

    fun parse(url: String): VlessLink? {
        val u = url.trim()
        if (!u.lowercase().startsWith("vless://")) return null
        return runCatching {
            var body = u.substring(8)

            var cfgName = ""
            if (body.contains("#")) {
                val idx = body.lastIndexOf("#")
                cfgName = dec(body.substring(idx + 1)).trim()
                body = body.substring(0, idx)
            }
            var query = ""
            if (body.contains("?")) {
                val idx = body.indexOf("?")
                query = body.substring(idx + 1); body = body.substring(0, idx)
            }
            var uid = ""
            val addr: String
            if (body.contains("@")) {
                val idx = body.lastIndexOf("@")
                uid = dec(body.substring(0, idx)).trim()
                addr = body.substring(idx + 1)
            } else addr = body

            val server: String; val portS: String
            when {
                addr.startsWith("[") -> {
                    val end = addr.indexOf("]")
                    server = addr.substring(1, end)
                    portS = if (addr.length > end + 2) addr.substring(end + 2) else "443"
                }
                addr.contains(":") -> {
                    val idx = addr.lastIndexOf(":")
                    server = addr.substring(0, idx); portS = addr.substring(idx + 1)
                }
                else -> { server = addr; portS = "443" }
            }
            val port = portS.toIntOrNull() ?: 443

            val params = HashMap<String, String>()
            query.split("&").forEach {
                if (it.contains("=")) {
                    val (k, v) = it.split("=", limit = 2)
                    params[k.lowercase()] = dec(v)
                }
            }
            fun p(k: String, d: String = "") = params[k] ?: d

            val cdnHost = p("host").ifEmpty { server }
            val sni = p("sni").ifEmpty { p("peer").ifEmpty { cdnHost } }
            val insecure = (p("allowinsecure").ifEmpty { p("insecure").ifEmpty { "0" } }).trim()

            VlessLink(
                uid = uid, host = cdnHost, sni = sni, path = p("path", "/").ifEmpty { "/" },
                network = p("type", "ws"), security = p("security", "tls"),
                fp = p("fp", "chrome"),
                alpn = p("alpn", "http/1.1").replace("%2C", ",").replace("%2c", ","),
                grpcService = p("servicename").ifEmpty { p("service-name") },
                allowInsecure = insecure in listOf("1", "true", "yes"),
                cfgName = cfgName.ifEmpty { "Imported" },
                server = server, port = port,
            )
        }.getOrNull()
    }

    /** Build a vless:// share link (port of App._vless). */
    fun build(p: ConfigProfile, ip: String, port: Int): String {
        val sb = StringBuilder("vless://${p.uid}@$ip:$port?")
        val q = buildList {
            add("type=${p.network}")
            add("security=${p.security}")
            add("encryption=none")
            if (p.host.isNotEmpty()) add("host=${enc(p.host)}")
            if (p.sni.isNotEmpty()) add("sni=${enc(p.sni)}")
            if (p.path.isNotEmpty()) add("path=${enc(p.path)}")
            if (p.fp.isNotEmpty()) add("fp=${p.fp}")
            if (p.alpn.isNotEmpty()) add("alpn=${enc(p.alpn)}")
            if (p.network == "grpc" && p.grpcService.isNotEmpty()) add("serviceName=${enc(p.grpcService)}")
            if (p.allowInsecure) add("allowInsecure=1")
        }.joinToString("&")
        sb.append(q).append("#").append(enc(p.cfgName.ifEmpty { "Edge-Optimized" }))
        return sb.toString()
    }

    private fun enc(s: String) = java.net.URLEncoder.encode(s, "UTF-8")
}
