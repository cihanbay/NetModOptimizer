package com.veo.optimizer.ui

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
import com.veo.optimizer.core.CF_IP_RANGES
import com.veo.optimizer.core.CF_PORTS
import com.veo.optimizer.core.ConfigProfile
import com.veo.optimizer.core.Favorite
import com.veo.optimizer.core.Fmt
import com.veo.optimizer.core.HistoryEntry
import com.veo.optimizer.core.Persistence
import com.veo.optimizer.core.ProbeResult
import com.veo.optimizer.core.ProfileStore
import com.veo.optimizer.deploy.DeployResult
import com.veo.optimizer.deploy.DeployTarget
import com.veo.optimizer.deploy.WorkerDeploy
import com.veo.optimizer.scanner.Optimizer
import com.veo.optimizer.vpn.OptimizerVpnService
import com.veo.optimizer.xray.VlessParser
import com.veo.optimizer.xray.XrayConfig
import com.veo.optimizer.xray.XrayManager
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
import java.net.HttpURLConnection
import java.net.InetSocketAddress
import java.net.Proxy
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import kotlin.math.abs

enum class ConnState { DISCONNECTED, CONNECTING, CONNECTED }

class AppViewModel(app: Application) : AndroidViewModel(app) {

    private val ctx get() = getApplication<Application>()
    private val worker = WorkerDeploy(ctx)
    private val xray = XrayManager(ctx)

    private var store: ProfileStore = Persistence.load(ctx)
    val profiles = mutableStateListOf<ConfigProfile>().apply { addAll(store.profiles) }
    var profileIndex by mutableStateOf(store.index.coerceIn(0, (store.profiles.size - 1).coerceAtLeast(0)))
        private set
    val profile: ConfigProfile get() = profiles[profileIndex]

    val results = mutableStateListOf<ProbeResult>()
    var scanning by mutableStateOf(false); private set
    var scanProgress by mutableStateOf(0f); private set
    var scanStatus by mutableStateOf("Idle"); private set
    var connState by mutableStateOf(ConnState.DISCONNECTED); private set
    var connectedIp by mutableStateOf(""); private set
    val logLines = mutableStateListOf<String>()

    var testing by mutableStateOf(false); private set
    var testProgress by mutableStateOf(0f); private set
    var testStatus by mutableStateOf("Idle"); private set
    private var testJob: Job? = null

    var dlBps by mutableStateOf(0.0); private set
    var upBps by mutableStateOf(0.0); private set

    private var scanJob: Job? = null
    private val json = Json { ignoreUnknownKeys = true }

    init {
        results.addAll(profile.results)
        runCatching {
            val cls = Class.forName("com.veo.optimizer.xray.LibXrayBridge")
            xray.bridge = cls.getConstructor(android.content.Context::class.java)
                .newInstance(ctx) as XrayManager.XrayBridge
        }
    }

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

    fun importVless(url: String): Boolean {
        val link = VlessParser.parse(url) ?: return false
        link.applyTo(profile)
        if (profile.rangeRaw.isBlank()) profile.rangeRaw = link.server
        persist(); return true
    }

    fun shareLink(r: ProbeResult): String = VlessParser.build(profile, r.ip, r.port)

    // ── SCANNING ────────────────────────────────────────────────────────────
    fun startScan() {
        if (scanning) return
        val ips = Optimizer.fixRange(profile.rangeRaw)
        if (ips.isEmpty()) { log("No valid IPs in range"); return }
        scanning = true; scanProgress = 0f; scanStatus = "Scanning ${ips.size} IPs…"
        results.clear()
        val ports = profile.ports.ifEmpty { listOf(443) }
        scanJob = viewModelScope.launch(Dispatchers.Default) {
            val tasks = ips.flatMap { ip -> ports.map { port -> ip to port } }
            val mode = profile.mode

            if (mode == "auto") {
                // ── Config-Aware 3-phase scan (matching desktop app) ──────
                scanConfigAware(tasks)
            } else {
                // ── Single-phase scan (tcp/tls/http) ─────────────────────
                scanSinglePhase(tasks, mode)
            }
            scanning = false
            persist()
        }
    }

    private suspend fun scanConfigAware(tasks: List<Pair<String, Int>>) {
        val hasTls = profile.sni.isNotBlank() || profile.host.isNotBlank()
        val sni = profile.sni.ifEmpty { profile.host }
        val host = profile.host
        val path = profile.path.ifEmpty { "/" }
        val collected = ArrayList<ProbeResult>()

        // ── Phase 1: Fast TCP pre-filter ──────────────────────────────────
        val phase1Opt = Optimizer(
            concurrency = profile.threads.coerceAtLeast(1),
            timeoutMs = (minOf(profile.timeout, 3.0) * 1000).toLong(),
            tries = 1
        )
        var done = 0
        val chunks = tasks.chunked(profile.threads.coerceAtLeast(1))
        scanStatus = "[1/3] TCP pre-filter…"
        log("[Phase 1] TCP pre-filter on ${tasks.size} targets")

        for (chunk in chunks) {
            val batch = coroutineScope {
                chunk.map { (ip, port) ->
                    async { phase1Opt.probe(ip, port, "tcp", sni, host, path) }
                }.awaitAll()
            }
            batch.filter { it.ok }.forEach { collected.add(it) }
            done += chunk.size
            scanProgress = done.toFloat() / tasks.size * 0.33f
            scanStatus = "[1/3] TCP pre-filter $done/${tasks.size} — ${collected.size} alive"
        }

        if (collected.isEmpty()) {
            results.clear()
            scanStatus = "Done — 0 alive of ${tasks.size}"
            profile.scanned = tasks.size; profile.scanTime = now()
            return
        }

        // ── Phase 2: TLS+SNI+HTTP config-verify ──────────────────────────
        scanStatus = "[2/3] Config-verify on ${collected.size} survivors…"
        log("[Phase 2] TLS+SNI verify on ${collected.size} survivors")
        val phase2Mode = if (hasTls) "http" else "tcp"
        val phase2Opt = Optimizer(
            concurrency = minOf(profile.threads, 150),
            timeoutMs = (profile.timeout * 1000).toLong(),
            tries = 4
        )
        val verified = ArrayList<ProbeResult>()
        done = 0
        val chunks2 = collected.chunked(20)
        for (chunk in chunks2) {
            val batch = coroutineScope {
                chunk.map { r ->
                    async { phase2Opt.probe(r.ip, r.port, phase2Mode, sni, host, path) }
                }.awaitAll()
            }
            batch.filter { it.ok }.forEach { verified.add(it) }
            done += chunk.size
            scanProgress = 0.33f + done.toFloat() / collected.size * 0.33f
            scanStatus = "[2/3] Config-verify $done/${collected.size} — ${verified.size} pass"
        }

        // ── Phase 3: Real end-to-end proxy verify ─────────────────────────
        if (profile.hasConfig && xray.isInstalled && verified.isNotEmpty()) {
            val k = verified.size.coerceAtMost(12)
            scanStatus = "[3/3] Real proxy-verify of top $k…"
            log("[Phase 3] Confirming live traffic on top $k IPs…")
            val phase3Opt = Optimizer(concurrency = 3, timeoutMs = 10000, tries = 2)
            val socksBase = 10810

            for ((idx, r) in verified.take(k).withIndex()) {
                val socksPort = socksBase + idx
                val cfg = XrayConfig.buildProxy(r.ip, r.port, profile, socks = socksPort)
                val cfgJson = json.encodeToString(JsonObject.serializer(), cfg)

                runCatching {
                    xray.start(cfg, 0)
                    Thread.sleep(1500)
                    val (lat, _) = XrayManager.latency(socksPort)
                    xray.stop()
                    if (lat != null) {
                        r.cfValid = true
                        r.latMs = lat
                    }
                }
                scanProgress = 0.66f + (idx + 1).toFloat() / k * 0.34f
            }

            val working = verified.filter { it.latMs != null }.sortedBy { it.latMs }
            val rest = verified.filter { it.latMs == null }
            verified.clear(); verified.addAll(working); verified.addAll(rest)
        }

        // Combine with any TCP-only survivors not in verified
        val verifiedIps = verified.map { "${it.ip}:${it.port}" }.toSet()
        collected.filter { "${it.ip}:${it.port}" !in verifiedIps }.forEach { verified.add(it) }

        verified.sortBy {
            when {
                it.latMs != null -> it.latMs
                it.pingMs != null -> it.pingMs
                else -> Double.MAX_VALUE
            }
        }

        results.clear(); results.addAll(verified)
        profile.scanned = tasks.size; profile.scanTime = now()
        saveHistory(verified)
        scanStatus = "Done — ${verified.size} alive of ${tasks.size}"
        log("✔ Scan complete: ${verified.size} alive")
    }

    private suspend fun scanSinglePhase(tasks: List<Pair<String, Int>>, mode: String) {
        val opt = Optimizer(profile.threads, (profile.timeout * 1000).toLong())
        var done = 0
        val chunks = tasks.chunked(profile.threads.coerceAtLeast(1))
        val collected = ArrayList<ProbeResult>()
        for (chunk in chunks) {
            val batch = coroutineScope {
                chunk.map { (ip, port) ->
                    async { opt.probe(ip, port, mode, profile.sni, profile.host, profile.path) }
                }.awaitAll()
            }
            batch.filter { it.ok }.forEach { collected.add(it) }
            done += chunk.size
            scanProgress = done.toFloat() / tasks.size
            scanStatus = "Scanned $done/${tasks.size} — ${collected.size} alive"
        }
        collected.sortBy { it.pingMs ?: Double.MAX_VALUE }
        results.clear(); results.addAll(collected)
        profile.scanned = tasks.size; profile.scanTime = now()
        saveHistory(collected)
        scanStatus = "Done — ${collected.size} alive of ${tasks.size}"
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

    // ── TESTING ─────────────────────────────────────────────────────────────
    fun testResult(r: ProbeResult) = quickTestBatch(listOf(r))

    fun quickTestTop(n: Int = 20) {
        if (testing) return
        val tgts = results.filter { it.pingMs != null }.take(n)
        if (tgts.isEmpty()) { log("No results to test — run a scan first."); return }
        quickTestBatch(tgts)
    }

    fun fullTestTop(n: Int = 20) {
        if (testing) return
        val tgts = results.filter { it.pingMs != null }.take(n)
        if (tgts.isEmpty()) { log("No results to test — run a scan first."); return }
        fullTestBatch(tgts)
    }

    private fun quickTestBatch(tgts: List<ProbeResult>) {
        if (testing || tgts.isEmpty()) return
        testing = true; testProgress = 0f; testStatus = "Quick-checking ${tgts.size}…"
        val mode = profile.mode.let { if (it == "auto") "http" else it }
        val sni = profile.sni.ifEmpty { profile.host }
        val host = profile.host
        val path = profile.path.ifEmpty { "/" }
        val conc = profile.threads.coerceIn(1, 64).coerceAtMost(tgts.size)
        val opt = Optimizer(conc, (3.0 * 1000).toLong(), tries = 3)
        log("[Quick Test] concurrency=$conc, ${tgts.size} targets")
        testJob = viewModelScope.launch(Dispatchers.Default) {
            var done = 0
            coroutineScope {
                tgts.map { r ->
                    async {
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
                            done += 1
                            testProgress = done.toFloat() / tgts.size
                            testStatus = "Checked $done / ${tgts.size}"
                        }
                    }
                }.awaitAll()
            }
            val alive = results.filter { it.pingMs != null }.sortedBy { it.pingMs ?: 9999.0 }
            val dead = results.filter { it.pingMs == null }
            results.clear(); results.addAll(alive); results.addAll(dead)
            persist()
            testing = false; testProgress = 1f
            testStatus = "Done — ${tgts.size} checked"
            log("✔ Quick Test done: ${tgts.size} IPs")
        }
    }

    private fun fullTestBatch(tgts: List<ProbeResult>) {
        if (testing || tgts.isEmpty()) return
        testing = true; testProgress = 0f; testStatus = "Full testing ${tgts.size}…"
        log("[Full Test] Starting 2-phase test on ${tgts.size} configs")
        testJob = viewModelScope.launch(Dispatchers.Default) {
            val useXray = profile.hasConfig && xray.isInstalled

            // ── Phase A: Parallel latency (TCP + ICMP + xray proxy) ────────
            val phaseAConc = tgts.size.coerceIn(2, 6)
            log("[Phase A] Latency on ${tgts.size} configs (concurrency=$phaseAConc" +
                if (useXray) ", xray engine)" else ", tcp+icmp only)")
            var done = 0
            val sem = kotlinx.coroutines.sync.Semaphore(phaseAConc)

            coroutineScope {
                tgts.map { r ->
                    async {
                        sem.withPermit {
                            // TCP connect
                            runCatching {
                                val t0 = System.nanoTime()
                                java.net.Socket().use { s ->
                                    s.connect(java.net.InetSocketAddress(r.ip, r.port), 5000)
                                }
                                r.tcpMs = (System.nanoTime() - t0) / 1e6
                            }.getOrNull() ?: run { r.tcpMs = null }

                            // ICMP ping
                            r.icmpMs = icmpPing(r.ip)

                            // xray proxy latency
                            if (useXray) {
                                val socksPort = 10820 + tgts.indexOf(r)
                                val cfg = XrayConfig.buildProxy(r.ip, r.port, profile, socks = socksPort)
                                runCatching {
                                    xray.start(cfg, 0)
                                    Thread.sleep(1500)
                                    val (lat, _) = XrayManager.latency(socksPort)
                                    r.latMs = lat
                                    xray.stop()
                                }
                            }
                            r.tested = true
                            synchronized(this@AppViewModel) {
                                done += 1
                                testProgress = done.toFloat() / tgts.size * 0.4f
                                testStatus = "Phase A: $done / ${tgts.size}"
                            }
                        }
                    }
                }.awaitAll()
            }
            if (!coroutineContext.isActive) return@launch

            // ── Phase B: Sequential bandwidth on winners ─────────────────────
            if (useXray) {
                val winners = tgts.filter { it.latMs != null }
                    .sortedBy { it.latMs ?: 9999.0 }.take(12)
                if (winners.isNotEmpty()) {
                    log("[Phase B] Bandwidth on top ${winners.size} configs (sequential)")
                    testStatus = "Bandwidth on top ${winners.size}…"

                    for ((idx, r) in winners.withIndex()) {
                        if (!coroutineContext.isActive) break
                        val socksPort = 10830 + idx
                        val cfg = XrayConfig.buildProxy(r.ip, r.port, profile, socks = socksPort)

                        runCatching {
                            xray.start(cfg, 0)
                            Thread.sleep(1500)

                            val (dl, _) = XrayManager.dlSpeed(socksPort)
                            if (dl != null) r.dlMbps = dl

                            val (up, _) = XrayManager.upSpeed(socksPort, 1_000_000)
                            if (up != null) r.upMbps = up

                            xray.stop()
                        }

                        testProgress = 0.4f + (idx + 1).toFloat() / winners.size * 0.6f
                        testStatus = "Speed ${idx + 1}/${winners.size} — ${r.ip}"
                    }
                }
            }

            // Re-sort: proxy-verified first, then by ping
            val alive = results.filter { it.pingMs != null }.sortedWith(
                compareBy({ it.latMs ?: 9999.0 }, { it.pingMs ?: 9999.0 })
            )
            val dead = results.filter { it.pingMs == null }
            results.clear(); results.addAll(alive); results.addAll(dead)
            persist()
            testing = false; testProgress = 1f
            testStatus = "Done — ${tgts.size} tested"
            log("✔ Full Test done: ${tgts.size} configs (xray=$useXray)")
        }
    }

    fun stopTest() { testJob?.cancel(); testing = false; testStatus = "Stopped" }

    private fun icmpPing(host: String): Double? = try {
        val proc = Runtime.getRuntime().exec(arrayOf("ping", "-c", "1", "-w", "3000", host))
        val output = proc.inputStream.bufferedReader().readText()
        val time = Regex("time[=<](\\d+\\.?\\d*)").find(output)?.groupValues?.get(1)?.toDoubleOrNull()
        proc.waitFor()
        time
    } catch (_: Exception) { null }

    // ── CONNECT ─────────────────────────────────────────────────────────────
    fun connect(r: ProbeResult, tun: Boolean = true) {
        if (!profile.hasConfig) { log("Configure UUID + host in Config first"); return }
        if (connState == ConnState.CONNECTED) { disconnect() }

        connState = ConnState.CONNECTING; connectedIp = r.ip
        log("Connecting to ${r.ip}:${r.port}…")

        viewModelScope.launch(Dispatchers.Default) {
            val cfg: JsonObject = if (tun) XrayConfig.buildTun(r.ip, r.port, profile)
            else XrayConfig.buildProxy(r.ip, r.port, profile)
            val cfgJson = json.encodeToString(JsonObject.serializer(), cfg)

            OptimizerVpnService.start(ctx, cfgJson, r.ip)

            // Wait for VPN service to start and verify core is running
            var retries = 0
            while (!OptimizerVpnService.isActive && retries < 10) {
                Thread.sleep(500)
                retries++
            }

            if (OptimizerVpnService.isActive) {
                connState = ConnState.CONNECTED
                log("Tunnel connected → ${r.ip}:${r.port}")

                // Start bandwidth monitoring using shared bridge from VPN service
                while (connState == ConnState.CONNECTED) {
                    runCatching {
                        val bridge = OptimizerVpnService.sharedBridge
                        if (bridge != null) {
                            val up = bridge.queryStats("proxy", "uplink")
                            val down = bridge.queryStats("proxy", "downlink")
                            dlBps = down.toDouble()
                            upBps = up.toDouble()
                        }
                    }
                    Thread.sleep(2000)
                }
            } else {
                connState = ConnState.DISCONNECTED
                connectedIp = ""
                log("VPN connection failed — xray-core may not be installed or config is invalid")
            }
        }
    }

    fun pickAutoBest(): ProbeResult? {
        val proven = results.filter { it.latMs != null }
        val tested = results.filter { it.pingMs != null && it.tested }
        val anyOk = results.filter { it.pingMs != null }
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

    // ── FAVORITES ───────────────────────────────────────────────────────────
    fun addFavorite(url: String, name: String, note: String = "") {
        profile.favorites.add(0, Favorite(name, url, note, now())); persist()
    }
    fun deleteFavorite(i: Int) { if (i in profile.favorites.indices) { profile.favorites.removeAt(i); persist() } }

    // ── DEPLOY ──────────────────────────────────────────────────────────────
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
                profile.cfWorkers.add(0, com.veo.optimizer.core.CfWorker(
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

    // ── HOME ────────────────────────────────────────────────────────────────
    var homeSortKey by mutableStateOf("Quality"); private set
    fun setHomeSort(key: String) { homeSortKey = key }

    fun homeSorted(): List<ProbeResult> {
        val ok = results.filter { it.pingMs != null }
        return when (homeSortKey) {
            "Ping" -> ok.sortedBy { it.pingMs ?: Double.MAX_VALUE }
            "DL" -> ok.sortedByDescending { it.dlMbps ?: 0.0 }
            "Jitter" -> ok.sortedBy { it.jitterMs ?: Double.MAX_VALUE }
            "Loss" -> ok.sortedBy { it.lossPct ?: Double.MAX_VALUE }
            else -> ok.sortedWith(
                compareBy({ it.lossPct ?: 0.0 }, { it.pingMs ?: Double.MAX_VALUE },
                    { it.latMs ?: Double.MAX_VALUE }, { it.jitterMs ?: Double.MAX_VALUE }))
        }
    }

    fun homeTopConfigs(n: Int = 5): List<Pair<ProbeResult, String>> =
        homeSorted().take(n).map { it to VlessParser.build(profile, it.ip, it.port) }

    private fun homeSubBase64(): Pair<String, Int> {
        val tops = homeTopConfigs()
        if (tops.isEmpty()) return "" to 0
        val blob = tops.joinToString("\n") { it.second }
        return Base64.encodeToString(blob.toByteArray(Charsets.UTF_8), Base64.NO_WRAP) to tops.size
    }

    fun shareHomeSubLink() {
        val (b64, n) = homeSubBase64()
        if (n == 0) { log("No configs yet — run a scan first."); return }
        shareText(b64, "${profile.name} — Top-$n subscription")
        log("✔ Shared top-$n subscription (base64)")
    }

    fun shareHomeSubFile() {
        val (b64, n) = homeSubBase64()
        if (n == 0) { log("No configs yet — run a scan first."); return }
        val f = writeShareFile("${safeName()}_top${n}_sub.txt", b64)
        shareFile(f, "${profile.name} — Top-$n subscription file")
    }

    fun shareHomeTxt() {
        val tops = homeTopConfigs()
        if (tops.isEmpty()) { log("No configs yet — run a scan first."); return }
        val txt = tops.joinToString("\n") { it.second }
        val f = writeShareFile("${safeName()}_top${tops.size}.txt", txt)
        shareFile(f, "${profile.name} — Top-${tops.size} configs")
    }

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

    // ── DIAGNOSTICS ─────────────────────────────────────────────────────────
    fun diagnosticReport(): String {
        fun mask(s: String, keep: Int = 6) =
            if (s.isBlank()) "(empty)" else s.take(keep) + "…(${s.length} chars)"
        val res = results
        val alive = res.filter { it.pingMs != null }
        val tested = res.filter { it.tested }
        val proven = res.filter { it.latMs != null }
        val sb = StringBuilder()
        sb.appendLine("=".repeat(48))
        sb.appendLine("  VEO — DIAGNOSTIC REPORT")
        sb.appendLine("  ${now()}")
        sb.appendLine("=".repeat(48))
        sb.appendLine("\n[ENVIRONMENT]")
        sb.appendLine("  device   : ${Build.MANUFACTURER} ${Build.MODEL}")
        sb.appendLine("  android  : ${Build.VERSION.RELEASE} (API ${Build.VERSION.SDK_INT})")
        sb.appendLine("  abi      : ${Build.SUPPORTED_ABIS.joinToString()}")
        sb.appendLine("\n[ENGINE]")
        sb.appendLine("  xray     : ${if (xray.isInstalled) "installed" else "NoopBridge"}")
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
        sb.appendLine("  verified : ${proven.size}")
        alive.firstOrNull()?.let {
            sb.appendLine("  best     : ${it.ip}:${it.port} ping=${Fmt.pingLabel(it.pingMs)}")
        }
        sb.appendLine("\n[RECENT LOG]")
        if (logLines.isEmpty()) sb.appendLine("  (none)")
        else logLines.take(30).forEach { sb.appendLine("  $it") }
        sb.appendLine("\n" + "=".repeat(48))
        return sb.toString()
    }

    fun shareDiagnostics() {
        val report = diagnosticReport()
        shareText(report, "VEO — Diagnostic Report")
        log("✔ Diagnostic report shared.")
    }

    // ── LOGGING ─────────────────────────────────────────────────────────────
    fun log(msg: String) {
        logLines.add(0, "[${SimpleDateFormat("HH:mm:ss", Locale.US).format(Date())}] $msg")
        if (logLines.size > 500) logLines.removeAt(logLines.size - 1)
    }

    private fun now() = SimpleDateFormat("yyyy-MM-dd HH:mm", Locale.US).format(Date())
}
