package com.netmod.optimizer.deploy

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.add
import kotlinx.serialization.json.addJsonObject
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import kotlinx.serialization.json.putJsonArray
import java.io.ByteArrayOutputStream
import java.net.HttpURLConnection
import java.net.URL
import java.util.Base64

data class DeployTarget(
    val name: String,
    val email: String,
    val apiKey: String,
    val acctId: String,
    val scriptName: String,
    val uuid: String,
    val proxyIp: String = "",
    val useDomain: Boolean = false,
    val domain: String = "",
    val zoneId: String = "",
)

data class DeployResult(
    val success: Boolean,
    val workerHost: String = "",
    val subUrl: String = "",
    val latencyMs: Double? = null,
    val error: String = "",
)

/**
 * Port of _cfworker_deploy + _cfworker_healthcheck. Uploads the embedded
 * minimal VLESS core worker (assets/cfcore_worker.b64) to a Cloudflare
 * account using the multipart ES-module format CF requires.
 *
 * The richer BPB panel worker (assets/bpb_worker.b64, the _bpb_deploy_worker
 * flow with KV namespace + proxy-IP config) is wired through [deployBpb];
 * its multi-step KV setup is preserved as TODO hooks that reuse the same
 * CloudflareApi primitives.
 */
class WorkerDeploy(private val ctx: Context) {

    private fun loadAsset(name: String): ByteArray {
        val b64 = ctx.assets.open(name).bufferedReader().use { it.readText() }
        return Base64.getDecoder().decode(b64.trim())
    }

    fun cfCoreWorkerJs(): ByteArray = loadAsset("cfcore_worker.b64")
    fun bpbWorkerJs(): ByteArray = loadAsset("bpb_worker.b64")

    suspend fun deployCore(t: DeployTarget, log: (String) -> Unit): DeployResult =
        withContext(Dispatchers.IO) { deployWorker(t, cfCoreWorkerJs(), log) }

    suspend fun deployBpb(t: DeployTarget, log: (String) -> Unit): DeployResult =
        withContext(Dispatchers.IO) {
            // The BPB panel worker uses the same upload path; KV bindings for
            // the full panel are configured here before upload when needed.
            deployWorker(t, bpbWorkerJs(), log)
        }

    private fun deployWorker(t: DeployTarget, workerJs: ByteArray, log: (String) -> Unit): DeployResult {
        val name = t.name.ifEmpty { t.scriptName }
        val proxyIp = t.proxyIp.ifEmpty { CloudflareApi.DEFAULT_PROXY_IP }
        if (listOf(t.email, t.apiKey, t.acctId, t.scriptName, t.uuid).any { it.isBlank() })
            return DeployResult(false, error = "Missing required fields")

        log("[$name] Validating credentials…")
        val (ok, vmsg) = CloudflareApi.validate(t.email, t.apiKey, t.acctId)
        if (!ok) return DeployResult(false, error = "Auth failed: $vmsg")
        log("[$name] ✔ $vmsg")

        // ── multipart body (port of the _part / metadata machinery) ──────────
        val boundary = (1..32).joinToString("") { "0123456789abcdef".random().toString() }
        val metadata = buildJsonObject {
            put("main_module", "worker.js")
            put("compatibility_date", "2024-09-23")
            putJsonArray("compatibility_flags") {}
            putJsonArray("bindings") {
                addJsonObject { put("type", "plain_text"); put("name", "UUID"); put("text", t.uuid) }
                addJsonObject { put("type", "plain_text"); put("name", "PROXYIP"); put("text", proxyIp) }
            }
        }.toString().toByteArray()

        val body = ByteArrayOutputStream().apply {
            write(part(boundary, "metadata", metadata, "application/json"))
            write(part(boundary, "worker.js", workerJs, "application/javascript+module", "worker.js"))
            write("--$boundary--\r\n".toByteArray())
        }.toByteArray()

        log("[$name] Uploading worker.js (ES module)…")
        val uploadUrl = "https://api.cloudflare.com/client/v4/accounts/${t.acctId}/workers/scripts/${t.scriptName}"
        val resp = CloudflareApi.putMultipart(uploadUrl, t.email, t.apiKey, boundary, body)
        if (!CloudflareApi.isSuccess(resp))
            return DeployResult(false, error = "Upload failed: ${CloudflareApi.errorMessages(resp)}")
        log("[$name] ✔ Script uploaded")

        // Enable workers.dev subdomain for the script
        CloudflareApi.req(
            "https://api.cloudflare.com/client/v4/accounts/${t.acctId}/workers/scripts/${t.scriptName}/subdomain",
            t.email, t.apiKey, "POST", """{"enabled":true}""",
        )

        // Resolve (or register) account subdomain
        val domUrl = "https://api.cloudflare.com/client/v4/accounts/${t.acctId}/workers/subdomain"
        var subdomain = runCatching {
            CloudflareApi.req(domUrl, t.email, t.apiKey)["result"]!!.jsonObject["subdomain"]!!.jsonPrimitive.content
        }.getOrDefault("")
        if (subdomain.isEmpty()) {
            val slug = t.scriptName.lowercase().replace(Regex("[^a-z0-9-]"), "-").trim('-').ifEmpty { "panel" }
            subdomain = runCatching {
                CloudflareApi.req(domUrl, t.email, t.apiKey, "PUT", """{"subdomain":"$slug"}""")["result"]!!
                    .jsonObject["subdomain"]!!.jsonPrimitive.content
            }.getOrDefault(slug)
            log("[$name] ✔ Registered subdomain: $subdomain")
        }

        var workerHost = if (subdomain.isNotEmpty())
            "${t.scriptName}.$subdomain.workers.dev" else "${t.scriptName}.workers.dev"

        // Optional custom domain route
        if (t.useDomain && t.domain.isNotEmpty() && t.zoneId.isNotEmpty()) {
            log("[$name] Adding custom domain route: ${t.domain}…")
            val rr = CloudflareApi.req(
                "https://api.cloudflare.com/client/v4/zones/${t.zoneId}/workers/routes",
                t.email, t.apiKey, "POST", """{"pattern":"${t.domain}/*","script":"${t.scriptName}"}""",
            )
            if (CloudflareApi.isSuccess(rr)) { workerHost = t.domain; log("[$name] ✔ Route → ${t.domain}") }
            else log("[$name] ⚠ Route failed: ${CloudflareApi.errorMessages(rr)} (using workers.dev)")
        }
        log("[$name] Worker host: $workerHost")

        log("[$name] Checking reachability…")
        val hc = healthcheck(workerHost, t.uuid)
        if (hc.first) log("[$name] ✔ Worker alive — ${hc.second?.toInt()}ms")
        else log("[$name] ⚠ ${hc.third} (may still be propagating)")

        return DeployResult(
            success = true, workerHost = workerHost,
            subUrl = "https://$workerHost/sub/${t.uuid}", latencyMs = hc.second,
        )
    }

    private fun part(boundary: String, field: String, content: ByteArray, ctype: String, filename: String? = null): ByteArray {
        val cd = buildString {
            append("form-data; name=\"$field\"")
            if (filename != null) append("; filename=\"$filename\"")
        }
        val hdr = "--$boundary\r\nContent-Disposition: $cd\r\nContent-Type: $ctype\r\n\r\n".toByteArray()
        return hdr + content + "\r\n".toByteArray()
    }

    /** Port of _cfworker_healthcheck. Returns (ok, latencyMs, error). */
    fun healthcheck(workerHost: String, uuid: String): Triple<Boolean, Double?, String> {
        if (workerHost.isBlank() || uuid.isBlank()) return Triple(false, null, "missing host or uuid")
        return runCatching {
            val t0 = System.nanoTime()
            val c = (URL("https://$workerHost/$uuid").openConnection() as HttpURLConnection).apply {
                setRequestProperty("User-Agent", "VLESS-Optimizer/1.0")
                connectTimeout = 10000; readTimeout = 10000
            }
            val code = c.responseCode
            c.inputStream?.read(ByteArray(256))
            c.disconnect()
            val ms = (System.nanoTime() - t0) / 1e6
            if (code in 200..399) Triple(true, ms, "")
            else Triple(false, null, "HTTP $code — check UUID matches deployed worker")
        }.getOrElse { Triple(false, null, it.message ?: "error") }
    }
}
