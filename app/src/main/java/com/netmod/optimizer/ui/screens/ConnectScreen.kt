package com.netmod.optimizer.ui.screens

import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.foundation.background
import android.net.VpnService
import com.netmod.optimizer.core.Fmt
import com.netmod.optimizer.ui.AppViewModel
import com.netmod.optimizer.ui.ConnState
import com.netmod.optimizer.ui.components.CardTitle
import com.netmod.optimizer.ui.components.Chip
import com.netmod.optimizer.ui.components.SectionCard
import com.netmod.optimizer.ui.theme.Theme

@Composable
fun ConnectScreen(vm: AppViewModel) {
    val p = Theme.palette
    val ctx = LocalContext.current
    var pending by androidx.compose.runtime.remember { androidx.compose.runtime.mutableStateOf<com.netmod.optimizer.core.ProbeResult?>(null) }

    // VpnService consent dialog (required before establishing the tunnel)
    val vpnLauncher = rememberLauncherForActivityResult(ActivityResultContracts.StartActivityForResult()) { res ->
        if (res.resultCode == android.app.Activity.RESULT_OK) pending?.let { vm.connect(it) }
        pending = null
    }

    fun requestConnect(r: com.netmod.optimizer.core.ProbeResult) {
        val intent = VpnService.prepare(ctx)
        if (intent != null) { pending = r; vpnLauncher.launch(intent) } else vm.connect(r)
    }

    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard(accent = when (vm.connState) {
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
                        modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = p.redC),
                    ) { Text("Disconnect") }
                }
            }
        }
        item {
            SectionCard {
                CardTitle("VPN mode (Android)", "Routes all device traffic through the VLESS edge via the system VpnService — no root needed.")
                if (!vm.profile.hasConfig) Text("⚠ Set UUID + host in Config first.", color = p.orange, fontSize = 12.sp, modifier = Modifier.padding(top = 6.dp))
                Button(
                    onClick = { vm.pickAutoBest()?.let { requestConnect(it) } ?: vm.log("No configs yet — run a scan first.") },
                    enabled = vm.connState == ConnState.DISCONNECTED && vm.profile.hasConfig,
                    modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = p.accent),
                ) { Text("⚡ Auto-Best Connect") }
                Text("Picks the config proven to carry real traffic (or best ping if none verified yet).",
                    color = p.fg3, fontSize = 11.sp, modifier = Modifier.padding(top = 4.dp))
            }
        }
        item { Text("Pick an edge to connect", color = p.fg2, fontSize = 14.sp, fontWeight = FontWeight.SemiBold) }
        items(vm.results.take(30)) { r ->
            SectionCard {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween, verticalAlignment = Alignment.CenterVertically) {
                    Column {
                        Text("${r.ip}:${r.port}", color = p.fg1, fontSize = 15.sp, fontWeight = FontWeight.Medium)
                        Text(Fmt.pingLabel(r.pingMs), color = Fmt.pingColor(r.pingMs, p), fontSize = 12.sp)
                    }
                    Button(
                        onClick = { requestConnect(r) },
                        enabled = vm.connState == ConnState.DISCONNECTED && vm.profile.hasConfig,
                        colors = ButtonDefaults.buttonColors(containerColor = p.accent),
                    ) { Text("Connect") }
                }
            }
        }
    }
}
