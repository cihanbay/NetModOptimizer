package com.veo.optimizer.ui.screens

import android.net.VpnService
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.LinearProgressIndicator
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
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.core.Fmt
import com.veo.optimizer.core.ProbeResult
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.ConnState
import com.veo.optimizer.ui.components.CardTitle
import com.veo.optimizer.ui.components.Chip
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme

@Composable
fun ConnectScreen(vm: AppViewModel) {
    val p = Theme.palette
    val ctx = LocalContext.current
    var pending by remember { mutableStateOf<ProbeResult?>(null) }

    val vpnLauncher = rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) { res ->
        if (res.resultCode == android.app.Activity.RESULT_OK) pending?.let { vm.connect(it) }
        pending = null
    }

    fun requestConnect(r: ProbeResult) {
        val intent = VpnService.prepare(ctx)
        if (intent != null) { pending = r; vpnLauncher.launch(intent) } else vm.connect(r)
    }

    LazyColumn(Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // ── Connection status ──
        item {
            SectionCard(Modifier.padding(0.dp), accent = when (vm.connState) {
                ConnState.CONNECTED -> p.cardBg2; ConnState.CONNECTING -> p.cardBg3; else -> null
            }) {
                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                    Box(Modifier.size(14.dp).clip(CircleShape).background(
                        when (vm.connState) {
                            ConnState.CONNECTED -> p.connected
                            ConnState.CONNECTING -> p.connecting
                            else -> p.disconnected
                        }
                    ))
                    Column {
                        Text(when (vm.connState) {
                            ConnState.CONNECTED -> "Connected"
                            ConnState.CONNECTING -> "Connecting…"
                            else -> "Disconnected"
                        }, color = p.fg1, fontSize = 18.sp, fontWeight = FontWeight.Bold)
                        if (vm.connectedIp.isNotEmpty()) Text(vm.connectedIp, color = p.fg3, fontSize = 13.sp)
                    }
                }
                if (vm.connState == ConnState.CONNECTED) {
                    Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        Chip("↓ ${Fmt.speed(vm.dlBps)}", p.green)
                        Chip("↑ ${Fmt.speed(vm.upBps)}", p.blue)
                    }
                    Button(
                        onClick = { vm.disconnect() },
                        modifier = Modifier.fillMaxWidth().padding(top = 8.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = p.redC),
                    ) { Text("Disconnect") }
                }
            }
        }

        // ── Auto-Best Connect ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                if (!vm.profile.hasConfig) Text("⚠ Set UUID + host in Config tab first.", color = p.orange, fontSize = 12.sp)
                Button(
                    onClick = { vm.pickAutoBest()?.let { requestConnect(it) } ?: vm.log("No configs — run a scan first.") },
                    enabled = vm.connState == ConnState.DISCONNECTED && vm.profile.hasConfig,
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = p.accent),
                ) { Text("⚡ Auto-Best Connect") }
                Text("Picks proven-working config (or best ping).", color = p.fg3, fontSize = 11.sp, modifier = Modifier.padding(top = 4.dp))
            }
        }

        // ── Quick Test + Full Test buttons ──
        item {
            SectionCard(Modifier.padding(0.dp)) {
                CardTitle("Test", "Re-probe or full bandwidth test")
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = { if (vm.testing) vm.stopTest() else vm.quickTestTop(20) },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = if (vm.testing) p.redC else p.accent),
                    ) { Text(if (vm.testing) "Stop" else "Quick Test", fontSize = 12.sp) }
                    Button(
                        onClick = { if (vm.testing) vm.stopTest() else vm.fullTestTop(20) },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = if (vm.testing) p.redC else p.teal),
                    ) { Text(if (vm.testing) "Stop" else "Full Test", fontSize = 12.sp) }
                }
                if (vm.testing) {
                    LinearProgressIndicator(progress = { vm.testProgress }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp), color = p.accent)
                }
                Text(vm.testStatus, color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 4.dp))
            }
        }

        // ── Pick an edge to connect ──
        item {
            Text("Pick an edge", color = p.fg2, fontSize = 14.sp, fontWeight = FontWeight.SemiBold,
                modifier = Modifier.padding(top = 4.dp))
        }
        itemsIndexed(vm.results.take(30)) { idx, r ->
            SectionCard(Modifier.padding(0.dp)) {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column(Modifier.weight(1f)) {
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                            Text("${idx + 1}.", color = p.accent, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                            Text("${r.ip}:${r.port}", color = p.fg1, fontSize = 13.sp, fontWeight = FontWeight.Medium)
                            if (r.cfValid) Chip("CF", p.blue)
                        }
                        Row(horizontalArrangement = Arrangement.spacedBy(3.dp), modifier = Modifier.padding(top = 2.dp)) {
                            Chip("ping ${Fmt.pingLabel(r.pingMs)}", Fmt.pingColor(r.pingMs, p))
                            r.tcpMs?.let { Chip("tcp ${it.toInt()}ms", Fmt.pingColor(it, p)) }
                            r.icmpMs?.let { Chip("icmp ${it.toInt()}ms", Fmt.pingColor(it, p)) }
                            r.latMs?.let { Chip("proxy ${it.toInt()}ms", p.green) }
                            r.dlMbps?.let { Chip("↓${"%.1f".format(it)}M", Fmt.speedColor(it, p)) }
                            r.upMbps?.let { Chip("↑${"%.1f".format(it)}M", Fmt.speedColor(it, p)) }
                            r.lossPct?.let { if (it > 0) Chip("${it.toInt()}% loss", p.orange) }
                        }
                    }
                    Button(
                        onClick = { requestConnect(r) },
                        enabled = vm.connState == ConnState.DISCONNECTED && vm.profile.hasConfig,
                        colors = ButtonDefaults.buttonColors(containerColor = p.accent),
                    ) { Text("Connect", fontSize = 12.sp) }
                }
            }
        }
    }
}
