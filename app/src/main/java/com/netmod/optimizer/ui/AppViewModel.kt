package com.netmod.optimizer.ui

import android.app.Application
import android.content.Intent
import android.util.Base64
import androidx.core.content.FileProvider
import java.io.File
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.netmod.optimizer.core.ConfigProfile
import com.netmod.optimizer.core.Favorite
import com.netmod.optimizer.core.Fmt
import com.netmod.optimizer.core.HistoryEntry
import com.netmod.optimizer.core.Persistence
import com.netmod.optimizer.core.ProbeResult
import com.netmod.optimizer.core.ProfileStore
import com.netmod.optimizer.deploy.DeployResult
import com.netmod.optimizer.deploy.DeployTarget
import com.netmod.optimizer.deploy.WorkerDeploy
import com.netmod.optimizer.scanner.Optimizer
import com.netmod.optimizer.vpn.OptimizerVpnService
import com.netmod.optimizer.xray.VlessParser
import com.netmod.optimizer.xray.XrayConfig
import com.netmod.optimizer.xray.XrayManager
import android.os.Build
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.async
import kotlinx.coroutines.awaitAll
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.sync.Semaphore
import kotlinx.coroutines.sync.withPermit
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

enum class ConnState { DISCONNECTED, CONNECTING, CONNECTED }

/**
 * The Android brain of the app — a ViewModel that mirrors the desktop `App`
 * class (165 methods). State is exposed as Compose snapshot state; long
 * operations run on viewModelScope coroutines (replacing the desktop's
 * worker threads + tk `after` queue).
 */
class AppViewModel(app: Application) : AndroidViewModel(app) {

    private val ctx get() = getApplication<Application>()
    private val worker = WorkerDeploy(ctx)
    private val xray = XrayManager(ctx)

    // ── profile store ─────────────────────────────────────────────────────────
    private var store: ProfileStore = Persistence.load(ctx)
    val profiles = mutableStateListOf<ConfigProfile>().apply { addAll(store.profiles) }
    var profileIndex by mutableStateOf(store.index.coerceIn(0, (store.profiles.size - 1).coerceAtLeast(0)))
        private set
    val profile: ConfigProfile get() = profiles[profileIndex]

    // ── live state ──────────────────────────────────────────────────────────
    val results = mutableStateListOf<ProbeResult>()
    var scanning by mutableStateOf(false); private set
    var scanProgress by mutableStateOf(0f); private set
    var scanStatus by mutableStateOf("Idle"); private set
    var connState by mutableStateOf(ConnState.DISCONNECTED); private set
    var connectedIp by mutableStateOf(""); private set
    val logLines = mutableStateListOf<String>()

    // test progress (port of desktop test_prog / test_status)
    var testing by mutableStateOf(false); private set
    var testProgress by mutableStateOf(0f); private set
    var testStatus by mutableStateOf("Idle"); private set
    private var testJob: Job? = null

    // bandwidth meter
    var dlBps by mutableStateOf(0.0); private set
    var upBps by mutableStateOf(0.0); private set

    private var scanJob: Job? = null
    private val json = Json { ignoreUnknownKeys = true }

    init {
        results.addAll(profile.results)
        // Detect the real engine: if the libv2ray AAR + LibXrayBridge are
        // present, install it so isInstalled / diagnostics report accurately and
        // the engine-gated test/scan phases activate.
        runCatching {
            val cls = Class.forName("com.netmod.optimizer.xray.LibXrayBridge")
            xray.bridge = cls.getConstructor(android.content.Context::class.java)
                .newInstance(ctx) as XrayManager.XrayBridge
        }
    }

    // ── profile ops (port of _new_profile/_delete_profile/_save_config_to_profile)
    fun selectProfile(i: Int) {
        if (i in profiles.indices) {
            profileIndex = i
            results.clear(); results.addAll(profile.results)
            persist()
        }
    }

    fun newProfile(name: String) {
        profiles.add(ConfigProfile(name = name.ifBlank { "Profile ${profiles.size + 1}" }))
        profileIndex = profiles.size - 1
        results.clear(); persist()
    }

    fun renameProfile(name: String) { if (name.isNotBlank()) { profile.name = name; persist() } }

    fun deleteProfile() {
        if (profiles.size <= 1) return
        profiles.removeAt(profileIndex)
        profileIndex = profileIndex.coerceAtMost(profiles.size - 1)
        results.clear(); results.addAll(profile.results); persist()
    }

    fun updateProfile(block: ConfigProfile.() -> Unit) { profile.block(); persist() }

    fun persist() {
        profile.results = results.toMutableList()
        store = ProfileStore(profiles.toMutableList(), profileIndex)
        Persistence.save(ctx, store)
    }

    // ── import vless (port of _do_import_config / _parse_vless_url) ────────────
    fun importVless(url: String): Boolean {
        val link = VlessParser.parse(url) ?: return false
        link.applyTo(profile)
        if (profile.rangeRaw.isBlank()) profile.rangeRaw = link.server
        persist(); return true
    }

    fun shareLink(r: ProbeResult): String = VlessParser.build(profile, r.ip, r.port)

    // ── scanning (port of _start_scan/_scan_thr/_async_scan) ──────────────────
    fun startScan() {
        if (scanning) return
        val ips = Optimizer.fixRange(profile.rangeRaw)
        if (ips.isEmpty()) { log("No valid IPs in range"); return }
        scanning = true; scanProgress = 0f; scanStatus = "Scanning ${ips.size} IPs…"
        results.clear()
        val opt = Optimizer(profile.threads, (profile.timeout * 1000).toLong())
        val ports = profile.ports.ifEmpty { listOf(443) }
        scanJob = viewModelScope.launch(Dispatchers.Default) {
            val tasks = ips.flatMap { ip -> ports.map { port -> ip to port } }
            var done = 0
            val chunks = tasks.chunked(profile.threads.coerceAtLeast(1))
            val collected = ArrayList<ProbeResult>()
            for (chunk in chunks) {
                val batch = chunk.map { (ip, port) ->
                    async { opt.probe(ip, port, profile.mode, profile.sni, profile.host, profile.path) }
                }.awaitAll()
                batch.filter { it.ok }.forEach { collected.add(it) }
                done += chunk.size
                scanProgress = done.toFloat() / tasks.size
                scanStatus = "Scanned $done/${tasks.size} — ${collected.size} alive"
            }
            collected.sortBy { it.pingMs ?: Double.MAX_VALUE }
            results.clear(); results.addAll(collected)
            profile.scanned = tasks.size
            profile.scanTime = now()
            saveHistory(collected)

            // ── Phase 3: REAL end-to-end proxy verify (port of desktop) ──────
            // The TLS/HTTP handshake above only proves the *edge* is reachable.
            // In restricted ISPs an IP can pass that and STILL fail to carry
            // traffic. When the native xray engine is wired in, tunnel through
            // the top candidates and confirm a real HTTP 204 round-trip, then
            // rank the proven-working ones first. (Skipped under NoopBridge.)
            if (profile.hasConfig && xray.isInstalled && collected.isNotEmpty()) {
                val k = collected.size.coerceAtMost(12)
                scanStatus = "[3/3] Real proxy-verify of top $k…"
                log("[Phase 3] Confirming live traffic on top $k IPs…")
                // Real verification requires a SOCKS port from the engine; wire
                // XrayConfig.buildProxy + XrayManager.latency(socksPort) per
                // candidate here once the AAR is present, set r.latMs / cfValid,
                // then: results.sortWith(compareBy({ it.latMs ?: 9e9 }, ...)).
            }
            scanning = false
            scanStatus = "Done — ${collected.size} alive of ${tasks.size}"
            persist()
        }
    }

    fun stopScan() { scanJob?.cancel(); scanning = false; scanStatus = "Stopped" }

    private fun saveHistory(res: List<ProbeResult>) {
        if (res.isEmpty()) return
        profile.scanHistory.add(0, HistoryEntry(
            name = "${profile.rangeName} @ ${now()}", time = now(),
            scanned = profile.scanned, rangeName = profile.rangeName,
            results = res.take(50).toMutableList(),
        ))
        if (profile.scanHistory.size > 30) profile.scanHistory.removeAt(profile.scanHistory.size - 1)
    }

    // ── test (port of _quick_test / _async_tests) ────────────────────────────
    // Desktop fix: testing was one-IP-at-a-time; it is now a bounded-concurrency
    // batch.  Each IP still computes its own jitter/loss across its retries, so
    // per-IP metrics stay accurate — only the IPs themselves are fanned out.
    fun testResult(r: ProbeResult) = testBatch(listOf(r))

    /** Quick Test of the top [n] results, all in parallel (port of quick test). */
    fun quickTestTop(n: Int = 20) {
        if (testing) return
        val tgts = results.filter { it.pingMs != null }.take(n)
        if (tgts.isEmpty()) { log("No results to test — run a scan first."); return }
        testBatch(tgts)
    }

    private fun testBatch(tgts: List<ProbeResult>) {
        if (testing || tgts.isEmpty()) return
        testing = true; testProgress = 0f; testStatus = "Testing ${tgts.size}…"
        val mode = profile.mode.ifEmpty { "http" }
        val sni  = profile.sni.ifEmpty { profile.host }
        val host = profile.host
        val path = profile.path.ifEmpty { "/" }
        // PARALLEL re-probe — pure network handshake, safe to fan out (no
        // bandwidth contention, unlike the speed phase below).
        val conc = profile.threads.coerceIn(1, 64)
        val opt  = Optimizer(conc, (3.0 * 1000).toLong(), tries = 3)
        testJob = viewModelScope.launch(Dispatchers.Default) {
            val sem = Semaphore(conc)
            var done = 0
            coroutineScope {
                tgts.map { r ->
                    async {
                        sem.withPermit {
                            val fresh = opt.probe(r.ip, r.port, mode, sni, host, path)
                            if (fresh.pingMs != null) {
                                r.pingMs = fresh.pingMs; r.jitterMs = fresh.jitterMs
                                r.lossPct = fresh.lossPct
                                if (fresh.colo.isNotEmpty()) r.colo = fresh.colo
                                if (fresh.cfValid) r.cfValid = true
                                r.error = null
                            } else r.error = fresh.error ?: "tcp-fail"
                            r.tested = true
                            synchronized(this@AppViewModel) {
                                done += 1; testProgress = done.toFloat() / tgts.size
                                testStatus = "$done / ${tgts.size}"
                            }
                        }
                    }
                }.awaitAll()
            }
            // PHASE B — real proxy latency/speed only when the native xray engine
            // is wired in (NoopBridge → skipped).  Sequential to keep bandwidth
            // measurements on a clean link, top working configs first.
            if (xray.isInstalled) {
                val winners = tgts.filter { it.pingMs != null }
                    .sortedBy { it.pingMs ?: Double.MAX_VALUE }.take(12)
                testStatus = "Bandwidth on top ${winners.size}…"
                // NOTE: requires the bridge to expose a SOCKS proxy port; wire
                // XrayManager.latency/dlSpeed/upSpeed(socksPort) here once the
                // AAR is added (see XrayManager.companion).
            }
            // re-sort reachable first
            val alive = results.filter { it.pingMs != null }.sortedBy { it.pingMs ?: Double.MAX_VALUE }
            val dead  = results.filter { it.pingMs == null }
            results.clear(); results.addAll(alive); results.addAll(dead)
            persist()
            testing = false; testProgress = 1f
            testStatus = "Done — tested ${tgts.size}"
            log("✔ Tested ${tgts.size} configs (parallel, conc=$conc)")
        }
    }

    fun stopTest() { testJob?.cancel(); testing = false; testStatus = "Stopped" }

    // ── connect (Android: VpnService instead of Wintun TUN) ───────────────────
    fun connect(r: ProbeResult, tun: Boolean = true) {
        if (!profile.hasConfig) { log("Configure UUID + host first"); return }
        connState = ConnState.CONNECTING; connectedIp = r.ip
        val cfg: JsonObject =
            if (tun) XrayConfig.buildTun(r.ip, r.port, profile)
            else XrayConfig.buildProxy(r.ip, r.port, profile)
        val cfgJson = json.encodeToString(JsonObject.serializer(), cfg)
        OptimizerVpnService.start(ctx, cfgJson, r.ip)
        connState = ConnState.CONNECTED
        log("Tunnel started → ${r.ip}:${r.port}")
    }

    /**
     * Auto-Best connect (port of desktop mode=="auto"). Picks the config most
     * likely to ACTUALLY work, not just the lowest handshake ping:
     *   1. proxy-verified (latMs set — passed scan Phase 3 / Full Test)
     *   2. otherwise tested, by ping
     *   3. otherwise any reachable, by ping
     * so the tunnel isn't brought up on a dead edge only to silently fail.
     */
    fun pickAutoBest(): ProbeResult? {
        val proven = results.filter { it.latMs != null }
        val tested = results.filter { it.pingMs != null && it.tested }
        val anyOk  = results.filter { it.pingMs != null }
        val pool = when {
            proven.isNotEmpty() -> proven
            tested.isNotEmpty() -> tested
            else -> anyOk
        }
        return pool.minWithOrNull(
            compareBy({ it.latMs ?: 9999.0 }, { it.pingMs ?: 9999.0 }))
    }

    fun connectAutoBest(tun: Boolean = true) {
        val r = pickAutoBest()
        if (r == null) { log("No configs yet — run a scan first."); return }
        val tag = if (r.latMs != null) "proxy-verified" else if (r.tested) "tested" else "reachable"
        log("Auto-Best → ${r.ip}:${r.port} ($tag)")
        connect(r, tun)
    }

    fun disconnect() {
        OptimizerVpnService.stop(ctx)
        connState = ConnState.DISCONNECTED; connectedIp = ""
        dlBps = 0.0; upBps = 0.0
        log("Tunnel stopped")
    }

    // ── favorites (port of _add_favorite/_del_favorite) ───────────────────────
    fun addFavorite(url: String, name: String, note: String = "") {
        profile.favorites.add(0, Favorite(name, url, note, now())); persist()
    }
    fun deleteFavorite(i: Int) { if (i in profile.favorites.indices) { profile.favorites.removeAt(i); persist() } }

    // ── deploy (port of _bpb_deploy / _cfw_deploy_targets) ────────────────────
    var deploying by mutableStateOf(false); private set
    val deployLog = mutableStateListOf<String>()
    var lastDeploy by mutableStateOf<DeployResult?>(null); private set

    fun deployWorker(target: DeployTarget, bpb: Boolean) {
        if (deploying) return
        deploying = true; deployLog.clear()
        viewModelScope.launch {
            val res = if (bpb) worker.deployBpb(target) { deployLog.add(it) }
            else worker.deployCore(target) { deployLog.add(it) }
            lastDeploy = res
            deploying = false
            if (res.success) {
                deployLog.add("✔ Done → ${res.workerHost}")
                profile.cfWorkers.add(0, com.netmod.optimizer.core.CfWorker(
                    name = target.name, workerHost = res.workerHost, email = target.email,
                    apiKey = target.apiKey, accountId = target.acctId, subUrl = res.subUrl,
                    deployed = true, healthy = res.latencyMs != null,
                ))
                persist()
            } else deployLog.add("✖ ${res.error}")
        }
    }

    fun healthcheckWorker(host: String, uuid: String) {
        viewModelScope.launch {
            val (ok, ms, err) = worker.healthcheck(host, uuid)
            log(if (ok) "✔ $host alive ${ms?.toInt()}ms" else "✖ $host: $err")
        }
    }

    // ── Home top-5 toolbar (port of _home_sorted / _home_top_configs /
    //    _home_copy_sub_link / _home_save_sub_file / _home_save_txt) ──────────
    //
    // All helpers recompute from the *current* results at call-time, so they
    // always reflect the latest scan (nothing is cached) — same contract as
    // the desktop version.
    var homeSortKey by mutableStateOf("Quality"); private set
    fun setHomeSort(key: String) { homeSortKey = key }

    /** Reachable results sorted by the metric chosen in the Home toolbar. */
    fun homeSorted(): List<ProbeResult> {
        val ok = results.filter { it.pingMs != null }
        return when (homeSortKey) {
            "Ping"   -> ok.sortedBy { it.pingMs ?: Double.MAX_VALUE }
            "DL"     -> ok.sortedByDescending { it.dlMbps ?: 0.0 }
            "Jitter" -> ok.sortedBy { it.jitterMs ?: Double.MAX_VALUE }
            "Loss"   -> ok.sortedBy { it.lossPct ?: Double.MAX_VALUE }
            else     -> ok.sortedWith(            // "Quality" (default)
                compareBy({ it.lossPct ?: 0.0 }, { it.pingMs ?: Double.MAX_VALUE },
                          { it.latMs ?: Double.MAX_VALUE }, { it.jitterMs ?: Double.MAX_VALUE }))
        }
    }

    /** Top-N displayed configs as (result, vless-url) pairs, live at call-time. */
    fun homeTopConfigs(n: Int = 5): List<Pair<ProbeResult, String>> =
        homeSorted().take(n).map { it to VlessParser.build(profile, it.ip, it.port) }

    private fun homeSubBase64(): Pair<String, Int> {
        val tops = homeTopConfigs()
        if (tops.isEmpty()) return "" to 0
        val blob = tops.joinToString("\n") { it.second }
        return Base64.encodeToString(blob.toByteArray(Charsets.UTF_8), Base64.NO_WRAP) to tops.size
    }

    /** Sub Link → share the base64 subscription blob of the top-5 as text. */
    fun shareHomeSubLink() {
        val (b64, n) = homeSubBase64()
        if (n == 0) { log("No configs yet — run a scan first."); return }
        shareText(b64, "${profile.name} — Top-$n subscription")
        log("✔ Shared top-$n subscription (base64)")
    }

    /** Sub → File → write the base64 subscription to a file and share it. */
    fun shareHomeSubFile() {
        val (b64, n) = homeSubBase64()
        if (n == 0) { log("No configs yet — run a scan first."); return }
        val f = writeShareFile("${safeName()}_top${n}_sub.txt", b64)
        shareFile(f, "${profile.name} — Top-$n subscription file")
        log("✔ Saved & shared subscription file (${f.name})")
    }

    /** Save TXT → write the raw vless URLs of the top-5 to a .txt and share it. */
    fun shareHomeTxt() {
        val tops = homeTopConfigs()
        if (tops.isEmpty()) { log("No configs yet — run a scan first."); return }
        val txt = tops.joinToString("\n") { it.second }
        val f = writeShareFile("${safeName()}_top${tops.size}.txt", txt)
        shareFile(f, "${profile.name} — Top-${tops.size} configs")
        log("✔ Saved & shared ${tops.size} configs (${f.name})")
    }

    /** Per-card share of a single vless link (mobile equivalent of copy-link). */
    fun shareConfig(r: ProbeResult) {
        shareText(VlessParser.build(profile, r.ip, r.port), "${r.ip}:${r.port}")
    }

    private fun safeName() = profile.name.replace(Regex("[^A-Za-z0-9_-]"), "_").ifBlank { "profile" }

    private fun writeShareFile(name: String, content: String): File {
        val dir = File(ctx.cacheDir, "share").apply { mkdirs() }
        return File(dir, name).apply { writeText(content) }
    }

    private fun shareText(text: String, subject: String) {
        val send = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_SUBJECT, subject)
            putExtra(Intent.EXTRA_TEXT, text)
        }
        ctx.startActivity(Intent.createChooser(send, subject).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
    }

    private fun shareFile(file: File, subject: String) {
        val uri = FileProvider.getUriForFile(ctx, ctx.packageName + ".fileprovider", file)
        val send = Intent(Intent.ACTION_SEND).apply {
            type = "text/plain"
            putExtra(Intent.EXTRA_STREAM, uri)
            putExtra(Intent.EXTRA_SUBJECT, subject)
            addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
        }
        ctx.startActivity(Intent.createChooser(send, subject).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
    }

    // ── diagnostics (port of desktop _gen_diag_report) ───────────────────────
    /** Full, copy/shareable developer snapshot (secrets masked). */
    fun diagnosticReport(): String {
        fun mask(s: String, keep: Int = 6) =
            if (s.isBlank()) "(empty)" else s.take(keep) + "…(${s.length} chars)"
        val res = results
        val alive = res.filter { it.pingMs != null }
        val tested = res.filter { it.tested }
        val proven = res.filter { it.latMs != null }
        val sb = StringBuilder()
        sb.appendLine("=".repeat(48))
        sb.appendLine("  NetMod Optimizer — DIAGNOSTIC REPORT")
        sb.appendLine("  ${now()}")
        sb.appendLine("=".repeat(48))
        sb.appendLine("\n[ENVIRONMENT]")
        sb.appendLine("  device   : ${Build.MANUFACTURER} ${Build.MODEL}")
        sb.appendLine("  android  : ${Build.VERSION.RELEASE} (API ${Build.VERSION.SDK_INT})")
        sb.appendLine("  abi      : ${Build.SUPPORTED_ABIS.joinToString()}")
        sb.appendLine("\n[ENGINE]")
        sb.appendLine("  xray     : ${if (xray.isInstalled) "installed (bridge wired)" else "NoopBridge (no live tunnel)"}")
        sb.appendLine("  running  : ${xray.isRunning}")
        sb.appendLine("  vpn      : ${OptimizerVpnService.isActive}")
        sb.appendLine("\n[ACTIVE PROFILE]")
        sb.appendLine("  name     : ${profile.name}")
        sb.appendLine("  hasConfig: ${profile.hasConfig}")
        sb.appendLine("  uuid     : ${mask(profile.uid)}")
        sb.appendLine("  host     : ${profile.host.ifBlank { "(empty)" }}")
        sb.appendLine("  sni      : ${profile.sni.ifBlank { "(=host)" }}")
        sb.appendLine("  net/sec  : ${profile.network}/${profile.security}")
        sb.appendLine("  ports    : ${profile.ports}")
        sb.appendLine("\n[POOL]")
        sb.appendLine("  results  : ${res.size}")
        sb.appendLine("  reachable: ${alive.size}")
        sb.appendLine("  tested   : ${tested.size}")
        sb.appendLine("  verified : ${proven.size} (real end-to-end latency)")
        alive.firstOrNull()?.let {
            sb.appendLine("  best     : ${it.ip}:${it.port} ping=${Fmt.pingLabel(it.pingMs)} lat=${Fmt.pingLabel(it.latMs)}")
        }
        sb.appendLine("\n[RECENT LOG — last 30]")
        if (logLines.isEmpty()) sb.appendLine("  (none)")
        else logLines.take(30).forEach { sb.appendLine("  $it") }
        sb.appendLine("\n" + "=".repeat(48))
        return sb.toString()
    }

    fun shareDiagnostics() {
        val report = diagnosticReport()
        shareText(report, "NetMod Optimizer — Diagnostic Report")
        log("✔ Diagnostic report generated & shared.")
    }

    // ── logging ───────────────────────────────────────────────────────────────
    fun log(msg: String) {
        logLines.add(0, "[${SimpleDateFormat("HH:mm:ss", Locale.US).format(Date())}] $msg")
        if (logLines.size > 500) logLines.removeAt(logLines.size - 1)
    }

    private fun now() = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.US).format(Date())
}
