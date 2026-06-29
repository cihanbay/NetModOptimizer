package com.veo.optimizer.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MenuAnchorType
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.TabRowDefaults
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.core.CF_PORTS
import com.veo.optimizer.core.Fmt
import com.veo.optimizer.core.PROVIDER_RANGES
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.components.CardTitle
import com.veo.optimizer.ui.components.Chip
import com.veo.optimizer.ui.components.LabeledRow
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme

@Composable
fun ScanScreen(vm: AppViewModel) {
    val p = Theme.palette
    var selTab by remember { mutableIntStateOf(1) }
    val tabs = listOf("Config", "Scan", "Saved", "History")

    Column(Modifier.fillMaxSize()) {
        TabRow(
            selectedTabIndex = selTab,
            containerColor = p.bgHeader,
            contentColor = p.fg1,
            indicator = { tabPositions ->
                TabRowDefaults.SecondaryIndicator(
                    Modifier.tabIndicatorOffset(tabPositions[selTab]),
                    color = p.accent,
                )
            },
        ) {
            tabs.forEachIndexed { i, label ->
                Tab(
                    selected = selTab == i,
                    onClick = { selTab = i },
                    text = {
                        Text(label, fontSize = 12.sp,
                            fontWeight = if (selTab == i) FontWeight.Bold else FontWeight.Normal)
                    },
                    selectedContentColor = p.accent,
                    unselectedContentColor = p.fg3,
                )
            }
        }
        when (selTab) {
            0 -> ScanConfigTab(vm)
            1 -> ScanMainTab(vm)
            2 -> SavedTab(vm)
            3 -> HistoryTab(vm)
        }
    }
}

// ── Config sub-tab (VLESS config + scan params) ─────────────────────────
@Composable
private fun ScanConfigTab(vm: AppViewModel) {
    val p = Theme.palette
    val clip = LocalClipboardManager.current
    var uid by remember { mutableStateOf(vm.profile.uid) }
    var host by remember { mutableStateOf(vm.profile.host) }
    var sni by remember { mutableStateOf(vm.profile.sni) }
    var path by remember { mutableStateOf(vm.profile.path) }
    var network by remember { mutableStateOf(vm.profile.network) }
    var security by remember { mutableStateOf(vm.profile.security) }
    var fp by remember { mutableStateOf(vm.profile.fp) }
    var alpn by remember { mutableStateOf(vm.profile.alpn) }
    var allowInsecure by remember { mutableStateOf(vm.profile.allowInsecure) }
    var grpcService by remember { mutableStateOf(vm.profile.grpcService) }
    var importUrl by remember { mutableStateOf("") }
    var msg by remember { mutableStateOf("") }
    var threads by remember { mutableStateOf(vm.profile.threads.toString()) }
    var timeout by remember { mutableStateOf(vm.profile.timeout.toString()) }
    var topN by remember { mutableStateOf(vm.profile.topN.toString()) }

    fun save() = vm.updateProfile {
        this.uid = uid; this.host = host; this.sni = sni; this.path = path
        this.network = network; this.security = security; this.fp = fp
        this.alpn = alpn; this.allowInsecure = allowInsecure; this.grpcService = grpcService
    }

    LazyColumn(Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item {
            SectionCard(Modifier.padding(0.dp)) {
                CardTitle("Import", "Paste a vless:// link")
                OutlinedTextField(importUrl, { importUrl = it }, label = { Text("vless://…") },
                    modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button({
                        val text = clip.getText()?.text ?: ""; if (text.isNotBlank()) importUrl = text
                    }, colors = ButtonDefaults.buttonColors(containerColor = p.bgHover, contentColor = p.fg2)) { Text("Paste") }
                    Button({
                        val ok = vm.importVless(importUrl)
                        msg = if (ok) "✔ Imported" else "✖ Invalid link"
                        if (ok) {
                            uid = vm.profile.uid; host = vm.profile.host; sni = vm.profile.sni
                            path = vm.profile.path; network = vm.profile.network
                            security = vm.profile.security; fp = vm.profile.fp
                            alpn = vm.profile.alpn; allowInsecure = vm.profile.allowInsecure
                            grpcService = vm.profile.grpcService
                        }
                    }, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = p.accent)) { Text("Import") }
                }
                if (msg.isNotEmpty()) Text(msg, color = p.fg3, modifier = Modifier.padding(top = 6.dp))
            }
        }
        item {
            SectionCard(Modifier.padding(0.dp)) {
                CardTitle("VLESS Config")
                OutlinedTextField(uid, { uid = it; save() }, label = { Text("UUID") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(host, { host = it; save() }, label = { Text("Host (CDN/SNI)") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(sni, { sni = it; save() }, label = { Text("SNI") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(path, { path = it; save() }, label = { Text("Path") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Text("Network", color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
                Row(Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("ws", "grpc", "h2").forEach { n ->
                        Button({ network = n; save() }, colors = ButtonDefaults.buttonColors(
                            containerColor = if (network == n) p.accent else p.bgHover,
                            contentColor = if (network == n) Color.White else p.fg2,
                        )) { Text(n, fontSize = 12.sp) }
                    }
                }
                Text("Security", color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
                Row(Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("tls", "reality", "none").forEach { s ->
                        Button({ security = s; save() }, colors = ButtonDefaults.buttonColors(
                            containerColor = if (security == s) p.accent else p.bgHover,
                            contentColor = if (security == s) Color.White else p.fg2,
                        )) { Text(s, fontSize = 12.sp) }
                    }
                }
            }
        }
        item {
            SectionCard(Modifier.padding(0.dp)) {
                CardTitle("Advanced")
                OutlinedTextField(fp, { fp = it; save() }, label = { Text("Fingerprint") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(alpn, { alpn = it; save() }, label = { Text("ALPN") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(grpcService, { grpcService = it; save() }, label = { Text("gRPC Service (if grpc)") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Row(Modifier.fillMaxWidth().padding(top = 10.dp), verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.SpaceBetween) {
                    Text("Allow Insecure TLS", color = p.fg2, fontSize = 14.sp)
                    Switch(checked = allowInsecure, onCheckedChange = { allowInsecure = it; save() },
                        colors = SwitchDefaults.colors(checkedTrackColor = p.accent))
                }
            }
        }
        item {
            SectionCard(Modifier.padding(0.dp)) {
                CardTitle("Scan Parameters")
                OutlinedTextField(threads, { threads = it; vm.updateProfile { this.threads = it.toIntOrNull() ?: 200 } },
                    label = { Text("Concurrency") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(timeout, { timeout = it; vm.updateProfile { this.timeout = it.toDoubleOrNull() ?: 5.0 } },
                    label = { Text("Timeout (s)") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(topN, { topN = it; vm.updateProfile { this.topN = it.toIntOrNull() ?: 20 } },
                    label = { Text("Top N results") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
            }
        }
    }
}

// ── Scan sub-tab (main scan controls + results) ─────────────────────────
@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
private fun ScanMainTab(vm: AppViewModel) {
    val p = Theme.palette
    var range by remember { mutableStateOf(vm.profile.rangeRaw) }
    var showProviders by remember { mutableStateOf(false) }
    var providerLabel by remember { mutableStateOf(vm.profile.rangeName) }
    var modeExpanded by remember { mutableStateOf(false) }
    var portExpanded by remember { mutableStateOf(false) }
    val modeLabel = when (vm.profile.mode) {
        "auto" -> "Config-Aware (Auto)"
        "http" -> "HTTP Request"
        "tls" -> "TLS Handshake"
        "tcp" -> "TCP Connect"
        else -> vm.profile.mode
    }

    LazyColumn(Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // ── IP Range Tags ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                CardTitle("IP Ranges", "Select provider ranges or add custom")
                Row(Modifier.fillMaxWidth().padding(top = 8.dp)) {
                    Button(
                        onClick = { showProviders = true },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = p.bgHover, contentColor = p.fg2),
                    ) { Text("Provider: $providerLabel  ▾", fontSize = 12.sp) }
                }
                DropdownMenu(expanded = showProviders, onDismissRequest = { showProviders = false }) {
                    PROVIDER_RANGES.forEach { pr ->
                        DropdownMenuItem(
                            text = { Text(pr.label, fontSize = 13.sp) },
                            onClick = {
                                providerLabel = pr.label
                                showProviders = false
                                if (pr.ranges.isNotEmpty()) {
                                    for (rng in pr.ranges) {
                                        if (rng !in vm.profile.rangeTags) {
                                            vm.profile.rangeTags.add(rng)
                                        }
                                    }
                                    vm.updateProfile { rangeName = pr.label }
                                }
                            },
                        )
                    }
                }
                // Custom range input
                Row(Modifier.fillMaxWidth().padding(top = 6.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    OutlinedTextField(
                        value = range,
                        onValueChange = { range = it },
                        label = { Text("Custom CIDR") },
                        modifier = Modifier.weight(1f),
                        placeholder = { Text("104.16.0.0/13") },
                        singleLine = true,
                    )
                    Button(
                        onClick = {
                            val rng = range.trim()
                            if (rng.isNotBlank() && rng !in vm.profile.rangeTags) {
                                vm.profile.rangeTags.add(rng)
                                vm.updateProfile { rangeRaw = rng }
                                range = ""
                            }
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = p.accent),
                    ) { Text("+ Add", fontSize = 12.sp) }
                }
                // Active tags
                Text("Active ranges:", color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 6.dp))
                FlowRow(Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    if (vm.profile.rangeTags.isEmpty()) {
                        Text("(no ranges added)", color = p.fg4, fontSize = 11.sp)
                    }
                    vm.profile.rangeTags.toList().forEachIndexed { idx, rng ->
                        val display = if (rng.length > 28) rng.take(25) + "…" else rng
                        Row(
                            Modifier.clip(RoundedCornerShape(6.dp)).background(p.blue.copy(alpha = 0.12f))
                                .padding(horizontal = 6.dp, vertical = 3.dp),
                            verticalAlignment = Alignment.CenterVertically,
                        ) {
                            Text(display, color = p.blue, fontSize = 11.sp)
                            Icon(Icons.Filled.Close, "Remove", tint = p.redC,
                                modifier = Modifier.padding(start = 4.dp).clickable {
                                    vm.profile.rangeTags.removeAt(idx)
                                })
                        }
                    }
                }
            }
        }

        // ── Ports as combobox ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                ExposedDropdownMenuBox(
                    expanded = portExpanded,
                    onExpandedChange = { portExpanded = it },
                ) {
                    OutlinedTextField(
                        value = vm.profile.ports.joinToString(", "),
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Ports") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(portExpanded) },
                        modifier = Modifier.fillMaxWidth().menuAnchor(MenuAnchorType.PrimaryNotEditable),
                    )
                    ExposedDropdownMenu(expanded = portExpanded, onDismissRequest = { portExpanded = false }) {
                        CF_PORTS.forEach { port ->
                            DropdownMenuItem(
                                text = {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        Checkbox(
                                            checked = port in vm.profile.ports,
                                            onCheckedChange = null,
                                            colors = CheckboxDefaults.colors(checkedColor = p.accent),
                                        )
                                        Text("$port", fontSize = 13.sp)
                                    }
                                },
                                onClick = {
                                    if (port in vm.profile.ports) vm.profile.ports.remove(port)
                                    else vm.profile.ports.add(port)
                                    if (vm.profile.ports.isEmpty()) vm.profile.ports.add(443)
                                },
                            )
                        }
                        DropdownMenuItem(
                            text = { Text("All ports", fontWeight = FontWeight.Bold, color = p.accent) },
                            onClick = { vm.profile.ports.clear(); vm.profile.ports.addAll(CF_PORTS); portExpanded = false },
                        )
                    }
                }
            }
        }

        // ── Scan mode as combobox ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                ExposedDropdownMenuBox(
                    expanded = modeExpanded,
                    onExpandedChange = { modeExpanded = it },
                ) {
                    OutlinedTextField(
                        value = modeLabel,
                        onValueChange = {},
                        readOnly = true,
                        label = { Text("Scan Mode") },
                        trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(modeExpanded) },
                        modifier = Modifier.fillMaxWidth().menuAnchor(MenuAnchorType.PrimaryNotEditable),
                    )
                    ExposedDropdownMenu(expanded = modeExpanded, onDismissRequest = { modeExpanded = false }) {
                        listOf("auto" to "Config-Aware (Auto)", "http" to "HTTP Request",
                            "tls" to "TLS Handshake", "tcp" to "TCP Connect").forEach { (m, label) ->
                            DropdownMenuItem(
                                text = { Text(label, fontSize = 13.sp) },
                                onClick = { vm.updateProfile { this.mode = m }; modeExpanded = false },
                            )
                        }
                    }
                }
                if (vm.profile.mode == "auto") {
                    Text("Config-Aware: 3-phase scan (TCP pre-filter → TLS+SNI verify → real proxy test)",
                        color = p.fg3, fontSize = 11.sp, modifier = Modifier.padding(top = 4.dp))
                }
            }
        }

        // ── Start/Stop ──
        item {
            Row(Modifier.fillMaxWidth().padding(0.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                Button(
                    onClick = { if (vm.scanning) vm.stopScan() else vm.startScan() },
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(containerColor = if (vm.scanning) p.redC else p.accent),
                ) { Text(if (vm.scanning) "Stop" else "Start scan") }
            }
        }

        // ── Progress ──
        if (vm.scanning) {
            item {
                LinearProgressIndicator(progress = { vm.scanProgress }, modifier = Modifier.fillMaxWidth(), color = p.accent)
            }
        }
        item {
            Text(vm.scanStatus, color = p.fg3, fontSize = 12.sp)
        }

        // ── Results ──
        items(vm.results) { r ->
            SectionCard(Modifier.padding(0.dp)) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text("${r.ip}:${r.port}", color = p.fg1, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                        Row(horizontalArrangement = Arrangement.spacedBy(3.dp), modifier = Modifier.padding(top = 2.dp)) {
                            Chip(Fmt.pingLabel(r.pingMs), Fmt.pingColor(r.pingMs, p))
                            if (r.colo.isNotEmpty()) Chip("colo ${r.colo}", p.fg3)
                            r.lossPct?.let { if (it > 0) Chip("${it.toInt()}% loss", p.orange) }
                            r.jitterMs?.let { if (it > 0) Chip("jit ${it.toInt()}ms", p.fg3) }
                            r.latMs?.let { Chip("proxy ${it.toInt()}ms", p.green) }
                            if (r.cfValid) Chip("CF", p.blue)
                        }
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        PillBtn("→", p.accent) { vm.connect(r) }
                        PillBtn("★", p.orange) { vm.addFavorite(vm.shareLink(r), "${r.ip}:${r.port}") }
                    }
                }
            }
        }
    }
}

// ── Saved (Favorites) sub-tab ───────────────────────────────────────────
@Composable
private fun SavedTab(vm: AppViewModel) {
    val p = Theme.palette
    val clip = LocalClipboardManager.current
    var url by remember { mutableStateOf("") }
    var name by remember { mutableStateOf("") }

    LazyColumn(Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        item {
            SectionCard(Modifier.padding(0.dp)) {
                CardTitle("Add favorite")
                OutlinedTextField(name, { name = it }, label = { Text("Name") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(url, { url = it }, label = { Text("vless:// link") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    Button(
                        onClick = { if (url.isNotBlank()) { vm.addFavorite(url, name.ifBlank { "Fav" }); url = ""; name = "" } },
                        colors = ButtonDefaults.buttonColors(containerColor = p.accent),
                    ) { Text("Save") }
                    Button(
                        onClick = { val t = clip.getText()?.text ?: ""; if (t.isNotBlank()) url = t },
                        colors = ButtonDefaults.buttonColors(containerColor = p.bgHover, contentColor = p.fg2),
                    ) { Text("Paste") }
                }
            }
        }
        items(vm.profile.favorites) { f ->
            SectionCard(Modifier.padding(0.dp)) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Text(f.name, color = p.fg1, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                        Text(f.url, color = p.fg3, fontSize = 11.sp, maxLines = 1)
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        PillBtn("Copy", p.bgHover) { clip.setText(AnnotatedString(f.url)) }
                        PillBtn("→", p.accent) {
                            vm.importVless(f.url)
                        }
                        PillBtn("★", p.teal) {
                            vm.importVless(f.url)
                            vm.connectAutoBest()
                        }
                    }
                }
            }
        }
        if (vm.profile.favorites.isEmpty()) item {
            Text("No favorites saved.", color = p.fg3, fontSize = 13.sp, modifier = Modifier.padding(top = 20.dp))
        }
    }
}

// ── History sub-tab ─────────────────────────────────────────────────────
@Composable
private fun HistoryTab(vm: AppViewModel) {
    val p = Theme.palette
    LazyColumn(Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        item { CardTitle("Scan history", "Past scans for ${vm.profile.name}") }
        items(vm.profile.scanHistory) { h ->
            SectionCard(Modifier.padding(0.dp)) {
                Text(h.name, color = p.fg1, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                Row(Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    LabeledRow("Scanned", "${h.scanned}")
                    LabeledRow("Alive", "${h.results.size}")
                    LabeledRow("Best", Fmt.pingLabel(h.results.minOfOrNull { it.pingMs ?: Double.MAX_VALUE }))
                }
                Button(
                    onClick = {
                        vm.results.clear()
                        vm.results.addAll(h.results)
                        vm.persist()
                    },
                    modifier = Modifier.padding(top = 8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = p.bgHover, contentColor = p.fg2),
                ) { Text("Load results", fontSize = 12.sp) }
            }
        }
        if (vm.profile.scanHistory.isEmpty()) item {
            Text("No history yet.", color = p.fg3, fontSize = 13.sp, modifier = Modifier.padding(top = 20.dp))
        }
    }
}

@Composable
private fun PillBtn(label: String, color: Color, onClick: () -> Unit) {
    Box(
        Modifier
            .clip(RoundedCornerShape(6.dp))
            .background(color)
            .clickable { onClick() }
            .padding(horizontal = 8.dp, vertical = 4.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(label, color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Medium)
    }
}
