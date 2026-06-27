package com.veo.optimizer.deploy

import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.jsonArray
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.add
import kotlinx.serialization.json.addJsonObject
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import kotlinx.serialization.json.putJsonArray
import java.io.DataOutputStream
import java.net.HttpURLConnection
import java.net.URL

/**
 * Port of the Cloudflare helpers (_cf_hdr, _cf_req, _cf_validate) plus the
 * shared multipart machinery used by worker deploys.
 */
object CloudflareApi {
    const val DEFAULT_PROXY_IP = "bpb.yousef.isegaro.com"
    private val json = Json { ignoreUnknownKeys = true }

    fun headers(email: String, apiKey: String) = mapOf(
        "X-Auth-Email" to email,
        "X-Auth-Key" to apiKey,
        "Content-Type" to "application/json",
        "User-Agent" to "BPB-Optimizer/4.2.2",
    )

    /** Port of _cf_req — JSON request returning a parsed object (errors included). */
    fun req(
        url: String, email: String, apiKey: String,
        method: String = "GET", body: String? = null,
        contentType: String = "application/json", timeout: Int = 30000,
    ): JsonObject {
        return runCatching {
            val c = (URL(url).openConnection() as HttpURLConnection).apply {
                requestMethod = method
                connectTimeout = timeout; readTimeout = timeout
                headers(email, apiKey).forEach { (k, v) -> setRequestProperty(k, v) }
                setRequestProperty("Content-Type", contentType)
                if (body != null) { doOutput = true; outputStream.use { it.write(body.toByteArray()) } }
            }
            val code = c.responseCode
            val text = (if (code in 200..299) c.inputStream else c.errorStream)
                ?.bufferedReader()?.use { it.readText() } ?: "{}"
            c.disconnect()
            json.parseToJsonElement(text).jsonObject
        }.getOrElse { errObj(it.message ?: "network error") }
    }

    /** PUT a multipart/form-data body (worker script upload). */
    fun putMultipart(
        url: String, email: String, apiKey: String,
        boundary: String, body: ByteArray, timeout: Int = 60000,
    ): JsonObject = runCatching {
        val c = (URL(url).openConnection() as HttpURLConnection).apply {
            requestMethod = "PUT"; doOutput = true
            connectTimeout = timeout; readTimeout = timeout
            setRequestProperty("X-Auth-Email", email)
            setRequestProperty("X-Auth-Key", apiKey)
            setRequestProperty("Content-Type", "multipart/form-data; boundary=$boundary")
            setRequestProperty("User-Agent", "VLESS-Optimizer/1.0")
        }
        DataOutputStream(c.outputStream).use { it.write(body) }
        val code = c.responseCode
        val text = (if (code in 200..299) c.inputStream else c.errorStream)
            ?.bufferedReader()?.use { it.readText() } ?: "{}"
        c.disconnect()
        json.parseToJsonElement(text).jsonObject
    }.getOrElse { errObj("HTTP error: ${it.message}") }

    /** Port of _cf_validate. */
    fun validate(email: String, apiKey: String, acctId: String): Pair<Boolean, String> {
        val r = req("https://api.cloudflare.com/client/v4/accounts/$acctId", email, apiKey)
        val success = r["success"]?.jsonPrimitive?.content == "true"
        return if (success) {
            val name = runCatching { r["result"]!!.jsonObject["name"]!!.jsonPrimitive.content }.getOrDefault("?")
            true to "Account '$name' verified"
        } else false to errorMessages(r)
    }

    fun isSuccess(r: JsonObject) = r["success"]?.jsonPrimitive?.content == "true"

    fun errorMessages(r: JsonObject): String = runCatching {
        r["errors"]!!.jsonArray.joinToString("; ") { it.jsonObject["message"]?.jsonPrimitive?.content ?: "?" }
    }.getOrDefault("unknown error")

    private fun errObj(msg: String): JsonObject = buildJsonObject {
        put("success", false)
        putJsonArray("errors") { addJsonObject { put("message", msg) } }
    }
}
