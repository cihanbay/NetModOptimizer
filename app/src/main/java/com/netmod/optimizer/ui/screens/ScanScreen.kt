package com.netmod.optimizer.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.netmod.optimizer.core.Fmt
import com.netmod.optimizer.ui.AppViewModel
import com.netmod.optimizer.ui.components.CardTitle
import com.netmod.optimizer.ui.components.Chip
import com.netmod.optimizer.ui.components.SectionCard
import com.netmod.optimizer.ui.theme.Theme

@Composable
fun ScanScreen(vm: AppViewModel) {
    val p = Theme.palette
    var range by remember { mutableStateOf(vm.profile.rangeRaw) }
    var mode by remember { mutableStateOf(vm.profile.mode) }

    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
                CardTitle("Scanner", "Probe Cloudflare edge IPs (CIDR / range / list)")
                OutlinedTextField(
                    value = range, onValueChange = { range = it; vm.updateProfile { rangeRaw = it } },
                    label = { Text("IP range") }, modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                    placeholder = { Text("104.16.0.0/13 or 1.1.1.1-1.1.1.50") },
                )
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("http", "tls", "tcp").forEach { m ->
                        Button(
                            onClick = { mode = m; vm.updateProfile { this.mode = m } },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = if (mode == m) p.accent else p.bgHover,
                                contentColor = if (mode == m) androidx.compose.ui.graphics.Color.White else p.fg2,
                            ),
                        ) { Text(m.uppercase()) }
                    }
                }
                Row(Modifier.fillMaxWidth().padding(top = 10.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = { if (vm.scanning) vm.stopScan() else vm.startScan() },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = if (vm.scanning) p.redC else p.accent),
                    ) { Text(if (vm.scanning) "Stop" else "Start scan") }
                }
                if (vm.scanning) {
                    LinearProgressIndicator(progress = { vm.scanProgress }, modifier = Modifier.fillMaxWidth().padding(top = 10.dp), color = p.accent)
                }
                Text(vm.scanStatus, color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 6.dp))
            }
        }
        items(vm.results) { r ->
            SectionCard {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Column {
                        Text("${r.ip}:${r.port}", color = p.fg1, fontSize = 15.sp, fontWeight = FontWeight.Medium)
                        Text(buildString {
                            if (r.colo.isNotEmpty()) append("colo ${r.colo}  ")
                            r.lossPct?.let { append("loss ${it.toInt()}%  ") }
                            r.jitterMs?.let { append("jit ${it.toInt()}ms") }
                        }, color = p.fg3, fontSize = 12.sp)
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Chip(Fmt.pingLabel(r.pingMs), Fmt.pingColor(r.pingMs, p))
                        if (r.cfValid) Chip("CF", p.blue)
                    }
                }
            }
        }
    }
}
