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
import androidx.compose.foundation.lazy.itemsIndexed
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
    val tested = sorted.count { it.tested }
    val builtN = poolN

    LazyColumn(
        Modifier.fillMaxWidth().padding(horizontal = 12.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        // ── Profile card ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                            Text(vm.profile.name, color = p.fg1, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                            val cfgOk = vm.profile.hasConfig
                            Text(
                                if (cfgOk) "✔ Config" else "⚠ No config",
                                color = if (cfgOk) p.green else p.orange,
                                fontSize = 11.sp,
                            )
                        }
                        if (vm.profile.scanTime.isNotEmpty()) {
                            Text("Last scan: ${vm.profile.scanTime}  ·  ${vm.profile.rangeName}", color = p.fg3, fontSize = 11.sp)
                        }
                    }
                }
            }
        }

        // ── Stat boxes ──
        item {
            Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                MetricBox("Scanned", "${vm.profile.scanned}", p.blue, Modifier.weight(1f), "")
                MetricBox("Pool", "$poolN", p.teal, Modifier.weight(1f), "")
                MetricBox("Best", Fmt.pingLabel(bestPing), Fmt.pingColor(bestPing, p), Modifier.weight(1f), "")
                MetricBox("DL", if (bestDl != null) "%.0fM".format(bestDl) else "—",
                    Fmt.speedColor(bestDl, p), Modifier.weight(1f), "")
                MetricBox("Tested", "$tested", p.orange, Modifier.weight(1f), "")
            }
        }

        // ── VPN status + quick actions ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    val tunStatus = when (vm.connState) {
                        ConnState.CONNECTED -> "Connected"
                        ConnState.CONNECTING -> "Connecting…"
                        else -> "Disconnected"
                    }
                    val tunColor = when (vm.connState) {
                        ConnState.CONNECTED -> p.green
                        ConnState.CONNECTING -> p.orange
                        else -> p.fg3
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Box(Modifier.padding(0.dp).clip(RoundedCornerShape(4.dp)).background(tunColor).padding(horizontal = 6.dp, vertical = 2.dp)) {
                            Text(tunStatus, color = Color.White, fontSize = 11.sp, fontWeight = FontWeight.Medium)
                        }
                        if (vm.connectedIp.isNotEmpty()) Text(vm.connectedIp, color = p.fg3, fontSize = 11.sp)
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(4.dp)) {
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
                if (vm.connState == ConnState.CONNECTED) {
                    Row(Modifier.fillMaxWidth().padding(top = 6.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Chip("↓ ${Fmt.speed(vm.dlBps)}", p.green)
                        Chip("↑ ${Fmt.speed(vm.upBps)}", p.blue)
                    }
                }
            }
        }

        // ── Top-5 toolbar ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Text("Top 5:", color = p.fg2, fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
                    PillButton("Sub Link", p.blue) { vm.shareHomeSubLink() }
                    PillButton("File", p.teal) { vm.shareHomeSubFile() }
                    PillButton("TXT", p.fg3) { vm.shareHomeTxt() }
                    Box(Modifier.weight(1f))
                    SortDropdown(vm)
                }
            }
        }

        if (top5.isEmpty()) {
            item { Text("No results — run a scan first.", color = p.fg3, fontSize = 13.sp, modifier = Modifier.padding(top = 8.dp)) }
        }

        // ── Top-5 config cards ──
        itemsIndexed(top5) { idx, r ->
            SectionCard(Modifier.padding(0.dp)) {
                Row(
                    Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Column(Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text("${idx + 1}.", color = p.accent, fontSize = 13.sp, fontWeight = FontWeight.Bold)
                            Text("${r.ip}:${r.port}", color = p.fg1, fontSize = 13.sp, fontWeight = FontWeight.Medium)
                            if (r.cfValid) Chip("CF", p.blue)
                        }
                        Row(horizontalArrangement = Arrangement.spacedBy(3.dp), modifier = Modifier.padding(top = 2.dp)) {
                            Chip(Fmt.pingLabel(r.pingMs), Fmt.pingColor(r.pingMs, p))
                            if (r.tcpMs != null) Chip("tcp ${r.tcpMs!!.toInt()}ms", Fmt.pingColor(r.tcpMs, p))
                            if (r.icmpMs != null) Chip("icmp ${r.icmpMs!!.toInt()}ms", Fmt.pingColor(r.icmpMs, p))
                            if (r.latMs != null) Chip("proxy ${r.latMs!!.toInt()}ms", p.green)
                            if (r.dlMbps != null) Chip("↓${"%.1f".format(r.dlMbps)}M", Fmt.speedColor(r.dlMbps, p))
                            if (r.upMbps != null) Chip("↑${"%.1f".format(r.upMbps)}M", Fmt.speedColor(r.upMbps, p))
                            r.lossPct?.let { if (it > 0) Chip("${it.toInt()}% loss", p.orange) }
                            r.jitterMs?.let { if (it > 0) Chip("jit ${it.toInt()}ms", Fmt.jitterColor(it, p)) }
                        }
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(3.dp)) {
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
