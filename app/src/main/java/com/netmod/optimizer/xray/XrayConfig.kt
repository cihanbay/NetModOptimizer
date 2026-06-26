package com.netmod.optimizer.xray

import com.netmod.optimizer.core.ConfigProfile
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.add
import kotlinx.serialization.json.addJsonObject
import kotlinx.serialization.json.buildJsonArray
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import kotlinx.serialization.json.putJsonArray
import kotlinx.serialization.json.putJsonObject

/**
 * Port of XrayManager's config builders (_stream_settings, build_test,
 * build_proxy, build_tun). Produces the exact JSON xray-core expects.
 *
 * On Android the TUN inbound is NOT created by xray; the system VpnService
 * supplies the tun fd. So the Android tunnel uses the SOCKS config and
 * libXray's tun2socks layer fed by the VpnService fd (see OptimizerVpnService).
 */
object XrayConfig {

    private const val DEFAULT_UID = "00000000-0000-0000-0000-000000000000"

    fun streamSettings(p: ConfigProfile, ip: String): JsonObject {
        val net = p.network.ifEmpty { "ws" }
        val sec = p.security.ifEmpty { "tls" }
        val host = p.host.ifEmpty { ip }
        val sni = p.sni.ifEmpty { host }
        val path = p.path.ifEmpty { "/" }
        val alpn = p.alpn.split(",").map { it.trim() }.filter { it.isNotEmpty() }

        return buildJsonObject {
            put("network", net)
            put("security", sec)
            if (sec == "tls") putJsonObject("tlsSettings") {
                put("serverName", sni)
                put("fingerprint", p.fp.ifEmpty { "chrome" })
                put("allowInsecure", p.allowInsecure)
                if (alpn.isNotEmpty()) putJsonArray("alpn") { alpn.forEach { add(it) } }
            }
            when (net) {
                "ws" -> putJsonObject("wsSettings") { put("path", path); put("host", host) }
                "grpc" -> putJsonObject("grpcSettings") { put("serviceName", p.grpcService.ifEmpty { "grpc" }) }
                "h2" -> putJsonObject("httpSettings") {
                    put("path", path); putJsonArray("host") { add(host) }
                }
            }
        }
    }

    private fun defaultStream(sni: String, host: String, path: String) = buildJsonObject {
        put("network", "ws"); put("security", "tls")
        putJsonObject("tlsSettings") {
            put("serverName", sni); put("fingerprint", "chrome"); put("allowInsecure", false)
        }
        putJsonObject("wsSettings") { put("path", path); put("host", host) }
    }

    private fun outboundProxy(ip: String, port: Int, uid: String, ss: JsonObject) = buildJsonObject {
        put("tag", "proxy"); put("protocol", "vless")
        putJsonObject("settings") {
            putJsonArray("vnext") {
                addJsonObject {
                    put("address", ip); put("port", port)
                    putJsonArray("users") { addJsonObject { put("id", uid); put("encryption", "none") } }
                }
            }
        }
        put("streamSettings", ss)
    }

    /** Port of build_test — single http inbound for latency probing. */
    fun buildTest(ip: String, port: Int, profile: ConfigProfile, lport: Int): JsonObject {
        val uid = profile.uid.ifEmpty { DEFAULT_UID }
        val ss = streamSettings(profile, ip)
        return buildJsonObject {
            putJsonObject("log") { put("loglevel", "warning") }
            putJsonArray("inbounds") {
                addJsonObject {
                    put("tag", "http"); put("protocol", "http")
                    put("listen", "127.0.0.1"); put("port", lport)
                    putJsonObject("settings") {}
                }
            }
            putJsonArray("outbounds") { add(outboundProxy(ip, port, uid, ss)) }
        }
    }

    /** Port of build_proxy — socks + http inbounds, optional stats api. */
    fun buildProxy(
        ip: String, port: Int, profile: ConfigProfile,
        socks: Int = 10808, httpP: Int = 10809,
        loglevel: String = "warning", statsPort: Int? = null,
    ): JsonObject {
        val uid = profile.uid.ifEmpty { DEFAULT_UID }
        val ss = streamSettings(profile, ip)
        return buildJsonObject {
            putJsonObject("log") { put("loglevel", loglevel); put("access", "none") }
            putJsonArray("inbounds") {
                addJsonObject {
                    put("tag", "socks"); put("protocol", "socks")
                    put("listen", "127.0.0.1"); put("port", socks)
                    putJsonObject("settings") { put("auth", "noauth"); put("udp", true) }
                }
                addJsonObject {
                    put("tag", "http"); put("protocol", "http")
                    put("listen", "127.0.0.1"); put("port", httpP)
                    putJsonObject("settings") {}
                }
                if (statsPort != null) addJsonObject {
                    put("tag", "api-in"); put("listen", "127.0.0.1"); put("port", statsPort)
                    put("protocol", "dokodemo-door")
                    putJsonObject("settings") { put("address", "127.0.0.1") }
                }
            }
            putJsonArray("outbounds") {
                add(outboundProxy(ip, port, uid, ss))
                addJsonObject { put("tag", "direct"); put("protocol", "freedom"); putJsonObject("settings") {} }
                addJsonObject { put("tag", "block"); put("protocol", "blackhole"); putJsonObject("settings") {} }
            }
            putJsonObject("routing") {
                put("domainStrategy", "IPIfNonMatch")
                putJsonArray("rules") {
                    if (statsPort != null) addJsonObject {
                        put("type", "field")
                        putJsonArray("inboundTag") { add("api-in") }
                        put("outboundTag", "api")
                    }
                }
            }
            if (statsPort != null) {
                putJsonObject("stats") {}
                putJsonObject("api") { put("tag", "api"); putJsonArray("services") { add("StatsService") } }
                putJsonObject("policy") {
                    putJsonObject("system") {
                        put("statsInboundUplink", true); put("statsInboundDownlink", true)
                        put("statsOutboundUplink", true); put("statsOutboundDownlink", true)
                    }
                }
            }
        }
    }

    /**
     * Android tunnel config. Unlike the desktop build_tun (which created a
     * "tun" inbound via xray), Android obtains the tun fd from VpnService and
     * routes it through the socks inbound. This builds that socks-based config
     * with full DNS + routing so all device traffic goes through the proxy.
     */
    /**
     * Android full-tunnel config using xray-core's NATIVE `tun` inbound
     * (XTLS/gVisor build in libv2ray.aar). `CoreController.startLoop()` exports
     * the VpnService file descriptor through the `xray.tun.fd` env var, so the
     * core reads L3 packets straight from the tun — no tun2socks needed. All
     * captured traffic flows to the default (first) outbound = the VLESS proxy.
     */
    fun buildTun(
        ip: String, port: Int, profile: ConfigProfile, mtu: Int = 1500,
    ): JsonObject {
        val uid = profile.uid.ifEmpty { DEFAULT_UID }
        val ss = streamSettings(profile, ip)
        return buildJsonObject {
            putJsonObject("log") { put("loglevel", "warning") }
            putJsonObject("dns") {
                putJsonArray("servers") { add("1.1.1.1"); add("8.8.8.8") }
            }
            putJsonArray("inbounds") {
                addJsonObject {
                    put("tag", "tun-in")
                    put("port", 0)                       // tun inbound never listens
                    put("protocol", "tun")
                    putJsonObject("settings") { put("name", "tun0"); put("MTU", mtu) }
                    putJsonObject("sniffing") {
                        put("enabled", true)
                        putJsonArray("destOverride") { add("http"); add("tls"); add("quic") }
                        put("routeOnly", false)
                    }
                }
            }
            putJsonArray("outbounds") {
                add(outboundProxy(ip, port, uid, ss))    // default outbound (first)
                addJsonObject { put("tag", "direct"); put("protocol", "freedom"); putJsonObject("settings") {} }
                addJsonObject { put("tag", "block"); put("protocol", "blackhole"); putJsonObject("settings") {} }
            }
            putJsonObject("routing") {
                put("domainStrategy", "AsIs")            // no DNS in routing → no loops
                putJsonArray("rules") {}                 // default outbound handles all
            }
            // Stats so OptimizerVpnService can read up/down via queryStats("proxy", …)
            putJsonObject("stats") {}
            putJsonObject("policy") {
                putJsonObject("system") {
                    put("statsOutboundUplink", true); put("statsOutboundDownlink", true)
                }
            }
        }
    }

    /** @deprecated kept for compatibility; use [buildTun]. */
    fun buildTunSocks(
        ip: String, port: Int, profile: ConfigProfile,
        socks: Int = 10808, statsPort: Int? = null,
    ): JsonObject = buildTun(ip, port, profile)
}
