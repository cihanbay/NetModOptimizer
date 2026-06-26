package com.netmod.optimizer.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.netmod.optimizer.core.Fmt
import com.netmod.optimizer.ui.AppViewModel
import com.netmod.optimizer.ui.ConnState
import com.netmod.optimizer.ui.components.Chip
import com.netmod.optimizer.ui.components.MetricBox
import com.netmod.optimizer.ui.components.QrDialog
import com.netmod.optimizer.ui.components.SectionCard
import com.netmod.optimizer.ui.theme.Theme

@Composable
fun HomeScreen(vm: AppViewModel) {
    val p = Theme.palette
    var qrText by remember { mutableStateOf<String?>(null) }
    qrText?.let { QrDialog(it, "Config QR — scan to import", onDismiss = { qrText = null }) }
    val sorted = vm.homeSorted()
    val top5 = sorted.take(5)
    val bestPing = sorted.minByOrNull { it.pingMs ?: Double.MAX_VALUE }?.pingMs
    val bestDl = sorted.mapNotNull { it.dlMbps }.maxOrNull()
    val tested = sorted.count { it.tested }
    val poolN = vm.results.size
    val builtN = vm.profile.builtConfigs.size

    LazyColumn(
        Modifier.fillMaxWidth().padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        item {
            Text("NetMod Optimizer", color = p.fg1, fontSize = 24.sp, fontWeight = FontWeight.Bold)
            val cfg = if (vm.profile.hasConfig) "Connected" else "No config"
            Text("Profile: ${vm.profile.name}  ·  $cfg", color = p.fg3, fontSize = 13.sp)
        }

        // ── stat boxes (Verified box removed — Pool/Configs already shows it) ──
        item {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                MetricBox("Scanned", "${vm.profile.scanned}", p.blue, Modifier.weight(1f), "")
                MetricBox("Pool / Configs", "$poolN · $builtN", p.teal, Modifier.weight(1f), "")
                val status = when (vm.connState) {
                    ConnState.CONNECTED -> "ON"; ConnState.CONNECTING -> "…"; else -> "OFF"
                }
                MetricBox("Tunnel", status,
                    p.connected.takeIf { vm.connState == ConnState.CONNECTED } ?: p.fg3,
                    Modifier.weight(1f), "⇅")
            }
        }
        item {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                MetricBox("Best ping", Fmt.pingLabel(bestPing), Fmt.pingColor(bestPing, p), Modifier.weight(1f), "⚡")
                MetricBox("Best DL", if (bestDl != null) "%.1fM".format(bestDl) else "—",
                    Fmt.speedColor(bestDl, p), Modifier.weight(1f), "↓")
                MetricBox("Tested", "$tested", p.orange, Modifier.weight(1f), "")
            }
        }

        // ── Top-5 toolbar: Sub Link / Sub → File / Save TXT / Sort ────────────
        item {
            SectionCard {
                Text("Top 5 configs", color = p.fg1, fontSize = 15.sp, fontWeight = FontWeight.SemiBold)
                Row(
                    Modifier.fillMaxWidth().padding(top = 10.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    PillButton("Sub Link", p.blue) { vm.shareHomeSubLink() }
                    PillButton("Sub → File", p.teal) { vm.shareHomeSubFile() }
                    PillButton("Save TXT", p.fg3) { vm.shareHomeTxt() }
                }
                Row(
                    Modifier.fillMaxWidth().padding(top = 10.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text("Sort:", color = p.fg3, fontSize = 13.sp)
                    SortDropdown(vm)
                }
            }
        }

        if (top5.isEmpty()) {
            item { Text("No results yet — run a scan.", color = p.fg3, fontSize = 13.sp) }
        }

        items(top5) { r ->
            SectionCard {
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column(Modifier.weight(1f)) {
                        Text("${r.ip}:${r.port}", color = p.fg1, fontSize = 15.sp, fontWeight = FontWeight.Medium)
                        Text(
                            buildString {
                                append(if (r.colo.isNotEmpty()) "colo ${r.colo} · " else "")
                                append(r.mode)
                                r.lossPct?.let { append(" · loss ${it.toInt()}%") }
                                r.jitterMs?.let { append(" · jit ${it.toInt()}ms") }
                            },
                            color = p.fg3, fontSize = 12.sp,
                        )
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalAlignment = Alignment.CenterVertically) {
                        Chip(Fmt.pingLabel(r.pingMs), Fmt.pingColor(r.pingMs, p))
                        if (r.dlMbps != null) Chip("%.0fM".format(r.dlMbps), Fmt.speedColor(r.dlMbps, p))
                        if (r.cfValid) Chip("CF", p.blue)
                    }
                }
                Row(
                    Modifier.fillMaxWidth().padding(top = 10.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                ) {
                    PillButton("Connect", p.accent) { vm.connect(r) }
                    PillButton("QR", p.teal) { qrText = vm.shareLink(r) }
                    PillButton("Share", p.fg3) { vm.shareConfig(r) }
                    PillButton("★ Save", p.orange) {
                        vm.addFavorite(vm.shareLink(r), "${vm.profile.cfgName} ${r.ip}")
                    }
                }
            }
        }
    }
}

/** Small filled pill button matching the app palette. */
@Composable
private fun PillButton(label: String, color: Color, onClick: () -> Unit) {
    Box(
        Modifier
            .clip(RoundedCornerShape(10.dp))
            .background(color)
            .clickable { onClick() }
            .padding(horizontal = 12.dp, vertical = 7.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(label, color = Color.White, fontSize = 13.sp, fontWeight = FontWeight.Medium)
    }
}

/** Sort selector for the Home top-5 (Quality / Ping / DL / Jitter / Loss). */
@Composable
private fun SortDropdown(vm: AppViewModel) {
    val p = Theme.palette
    var expanded by remember { mutableStateOf(false) }
    val options = listOf("Quality", "Ping", "DL", "Jitter", "Loss")
    Box {
        Box(
            Modifier
                .clip(RoundedCornerShape(10.dp))
                .background(p.bgCard)
                .clickable { expanded = true }
                .padding(horizontal = 12.dp, vertical = 7.dp),
        ) {
            Text("${vm.homeSortKey}  ▾", color = p.fg1, fontSize = 13.sp, fontWeight = FontWeight.Medium)
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            options.forEach { opt ->
                DropdownMenuItem(
                    text = { Text(opt) },
                    onClick = { vm.setHomeSort(opt); expanded = false },
                )
            }
        }
    }
}
