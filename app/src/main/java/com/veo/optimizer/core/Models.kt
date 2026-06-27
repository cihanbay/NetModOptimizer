package com.veo.optimizer.core

import kotlinx.serialization.Serializable

/**
 * Port of the `models` module (ProbeResult, ConfigProfile dataclasses).
 * Kotlinx-serialization replaces the hand-rolled to_dict/from_dict.
 */

@Serializable
data class ProbeResult(
    var ip: String = "",
    var port: Int = 443,
    var mode: String = "http",
    var pingMs: Double? = null,
    var error: String? = null,
    var tcpMs: Double? = null,
    var icmpMs: Double? = null,
    var dlMbps: Double? = null,
    var upMbps: Double? = null,
    var latMs: Double? = null,
    var tested: Boolean = false,
    var lossPct: Double? = null,
    var jitterMs: Double? = null,
    var colo: String = "",
    var cfValid: Boolean = false,
) {
    val ok: Boolean get() = error == null && pingMs != null
}

@Serializable
data class ConfigProfile(
    var name: String = "Profile",
    var uid: String = "",
    var host: String = "",
    var sni: String = "",
    var path: String = "/",
    var cfgName: String = "Edge-Optimized",
    var network: String = "ws",
    var security: String = "tls",
    var fp: String = "chrome",
    var alpn: String = "http/1.1",
    var allowInsecure: Boolean = false,
    var grpcService: String = "",
    var rangeRaw: String = "",
    var rangeName: String = "Custom",
    var ports: MutableList<Int> = mutableListOf(443),
    var mode: String = "http",
    var threads: Int = 200,
    var timeout: Double = 5.0,
    var topN: Int = 20,
    var results: MutableList<ProbeResult> = mutableListOf(),
    var scanned: Int = 0,
    var scanTime: String = "",
    var builtConfigs: MutableList<String> = mutableListOf(),
    var scanHistory: MutableList<HistoryEntry> = mutableListOf(),
    var favorites: MutableList<Favorite> = mutableListOf(),
    var cfWorkers: MutableList<CfWorker> = mutableListOf(),
) {
    val hasConfig: Boolean get() = uid.trim().isNotEmpty() && host.trim().isNotEmpty()
}

@Serializable
data class HistoryEntry(
    val name: String = "",
    val time: String = "",
    val scanned: Int = 0,
    val rangeName: String = "",
    val results: MutableList<ProbeResult> = mutableListOf(),
)

@Serializable
data class Favorite(
    val name: String = "",
    val url: String = "",
    val note: String = "",
    val added: String = "",
)

/** A Cloudflare worker / BPB deploy target persisted per profile. */
@Serializable
data class CfWorker(
    var name: String = "",
    var workerHost: String = "",
    var email: String = "",
    var apiKey: String = "",
    var accountId: String = "",
    var subUrl: String = "",
    var deployed: Boolean = false,
    var healthy: Boolean? = null,
)

@Serializable
data class ProfileStore(
    val profiles: MutableList<ConfigProfile> = mutableListOf(),
    var index: Int = 0,
)
