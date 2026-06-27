package com.veo.optimizer.ui.screens

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
import com.veo.optimizer.core.Fmt
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.ConnState
import com.veo.optimizer.ui.components.Chip
import com.veo.optimizer.ui.components.MetricBox
import com.veo.optimizer.ui.components.QrDialog
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme

@Composable
fun HomeScreen(vm: AppViewModel) {
    val p = Theme.palette
    var qrText by remember { mutableStateOf<String?>(null) }
    qrText?.let { QrDialog(it, "Config QR", onDismiss = { qrText = null }) }
    val sorted = vm.homeSorted()
    val top5 = sorted.take(5)
    val bestPing = sorted.minByOrNull { it.pingMs ?: Double.MAX_VALUE }?.pingMs
    val bestDl = sorted.mapNotNull { it.dlMbps }.maxOrNull()
    val poolN = vm.results.size

    LazyColumn(
        Modifier.fillMaxWidth().padding(12.dp),
        verticalArrangement = Arrangement.spacedBy(8.dp),
    ) {
        // ── Header with quick actions ──
        item {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                Column {
                    Text("VEO", color = p.fg1, fontSize = 22.sp, fontWeight = FontWeight.Bold)
                    val cfg = if (vm.profile.hasConfig) "Ready" else "No config"
                    Text("${vm.profile.name} · $cfg", color = p.fg3, fontSize = 12.sp)
                }
                Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    PillButton("Scan", p.accent) { /* navigate to scan */ }
                    val connLabel = when (vm.connState) {
                        ConnState.CONNECTED -> "Disconnect"
                        ConnState.CONNECTING -> "Connecting…"
                        else -> "Connect"
                    }
                    PillButton(connLabel,
                        if (vm.connState == ConnState.CONNECTED) p.redC else p.teal
                    ) {
                        if (vm.connState == ConnState.CONNECTED) vm.disconnect()
                        else vm.connectAutoBest()
                    }
                }
            }
        }

        // ── Compact stat row ──
        item {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                MetricBox("Pool", "$poolN", p.blue, Modifier.weight(1f), "")
                MetricBox("Best", Fmt.pingLabel(bestPing), Fmt.pingColor(bestPing, p), Modifier.weight(1f), "⚡")
                MetricBox("DL", if (bestDl != null) "%.0fM".format(bestDl) else "—",
                    Fmt.speedColor(bestDl, p), Modifier.weight(1f), "↓")
                val tunStatus = when (vm.connState) {
                    ConnState.CONNECTED -> "ON"; ConnState.CONNECTING -> "…"; else -> "OFF"
                }
                MetricBox("VPN", tunStatus,
                    p.connected.takeIf { vm.connState == ConnState.CONNECTED } ?: p.fg3,
                    Modifier.weight(1f), "")
            }
        }

        // ── Share toolbar ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    PillButton("Sub Link", p.blue) { vm.shareHomeSubLink() }
                    PillButton("File", p.teal) { vm.shareHomeSubFile() }
                    PillButton("TXT", p.fg3) { vm.shareHomeTxt() }
                    Box(Modifier.weight(1f))
                    SortDropdown(vm)
                }
            }
        }

        if (top5.isEmpty()) {
            item { Text("No results — run a scan first.", color = p.fg3, fontSize = 13.sp) }
        }

        // ── Top-5 config cards (compact) ──
        items(top5) { r ->
            SectionCard(Modifier.padding(0.dp)) {
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column(Modifier.weight(1f)) {
                        Text("${r.ip}:${r.port}", color = p.fg1, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                        Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                            Chip(Fmt.pingLabel(r.pingMs), Fmt.pingColor(r.pingMs, p))
                            if (r.dlMbps != null) Chip("%.0fM".format(r.dlMbps), Fmt.speedColor(r.dlMbps, p))
                            if (r.cfValid) Chip("CF", p.blue)
                            r.lossPct?.let { if (it > 0) Chip("${it.toInt()}% loss", p.orange) }
                        }
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                        PillButton("→", p.accent) { vm.connect(r) }
                        PillButton("QR", p.teal) { qrText = vm.shareLink(r) }
                        PillButton("★", p.orange) {
                            vm.addFavorite(vm.shareLink(r), "${r.ip}:${r.port}")
                        }
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
            .clip(RoundedCornerShape(8.dp))
            .background(color)
            .clickable { onClick() }
            .padding(horizontal = 10.dp, vertical = 5.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(label, color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Medium)
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
                .clip(RoundedCornerShape(8.dp))
                .background(p.bgCard)
                .clickable { expanded = true }
                .padding(horizontal = 8.dp, vertical = 5.dp),
        ) {
            Text("${vm.homeSortKey} ▾", color = p.fg2, fontSize = 12.sp)
        }
        DropdownMenu(expanded = expanded, onDismissRequest = { expanded = false }) {
            options.forEach { opt ->
                DropdownMenuItem(
                    text = { Text(opt, fontSize = 13.sp) },
                    onClick = { vm.setHomeSort(opt); expanded = false },
                )
            }
        }
    }
}
