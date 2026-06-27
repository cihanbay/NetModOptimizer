package com.veo.optimizer.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Checkbox
import androidx.compose.material3.CheckboxDefaults
import androidx.compose.material3.DropdownMenu
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.core.CF_PORTS
import com.veo.optimizer.core.Fmt
import com.veo.optimizer.core.PROVIDER_RANGES
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.components.CardTitle
import com.veo.optimizer.ui.components.Chip
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme

@OptIn(ExperimentalLayoutApi::class)
@Composable
fun ScanScreen(vm: AppViewModel) {
    val p = Theme.palette
    var range by remember { mutableStateOf(vm.profile.rangeRaw) }
    var mode by remember { mutableStateOf(vm.profile.mode) }
    var showProviders by remember { mutableStateOf(false) }
    var providerLabel by remember { mutableStateOf(vm.profile.rangeName) }
    val selectedPorts = remember { mutableStateListOf<Int>().apply { addAll(vm.profile.ports) } }

    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
                CardTitle("Scanner", "Probe Cloudflare edge IPs")
                OutlinedTextField(
                    value = range, onValueChange = { range = it; vm.updateProfile { rangeRaw = it } },
                    label = { Text("IP range") }, modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                    placeholder = { Text("104.16.0.0/13 or 1.1.1.1-1.1.1.50") },
                )
                // Provider range dropdown
                Row(Modifier.fillMaxWidth().padding(top = 8.dp)) {
                    Button(
                        onClick = { showProviders = true },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = p.bgHover, contentColor = p.fg2),
                    ) { Text("Range: $providerLabel  ▾") }
                }
                DropdownMenu(expanded = showProviders, onDismissRequest = { showProviders = false }) {
                    PROVIDER_RANGES.forEach { pr ->
                        DropdownMenuItem(
                            text = { Text(pr.label, fontSize = 13.sp) },
                            onClick = {
                                providerLabel = pr.label
                                showProviders = false
                                if (pr.ranges.isNotEmpty()) {
                                    val csv = pr.ranges.joinToString(",")
                                    range = csv
                                    vm.updateProfile { rangeRaw = csv; rangeName = pr.label }
                                }
                            },
                        )
                    }
                }
                // Port selection
                Text("Ports", color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
                FlowRow(Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                    CF_PORTS.forEach { port ->
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Checkbox(
                                checked = port in selectedPorts,
                                onCheckedChange = { checked ->
                                    if (checked) selectedPorts.add(port) else selectedPorts.remove(port)
                                    vm.updateProfile { ports = selectedPorts.toMutableList() }
                                },
                                colors = CheckboxDefaults.colors(checkedColor = p.accent),
                            )
                            Text("$port", color = p.fg2, fontSize = 12.sp)
                        }
                    }
                }
                // Scan mode buttons
                Text("Scan mode", color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
                FlowRow(Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                    listOf("auto" to "Config-Aware", "http" to "HTTP", "tls" to "TLS", "tcp" to "TCP").forEach { (m, label) ->
                        Button(
                            onClick = { mode = m; vm.updateProfile { this.mode = m } },
                            colors = ButtonDefaults.buttonColors(
                                containerColor = if (mode == m) p.accent else p.bgHover,
                                contentColor = if (mode == m) androidx.compose.ui.graphics.Color.White else p.fg2,
                            ),
                        ) { Text(label, fontSize = 12.sp) }
                    }
                }
                if (mode == "auto") {
                    Text("Config-Aware: 3-phase scan (TCP pre-filter → TLS+SNI verify → real proxy test)",
                        color = p.fg3, fontSize = 11.sp, modifier = Modifier.padding(top = 4.dp))
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
                            r.lossPct?.let { if (it > 0) append("loss ${it.toInt()}%  ") }
                            r.jitterMs?.let { if (it > 0) append("jit ${it.toInt()}ms  ") }
                            r.latMs?.let { append("proxy ${it.toInt()}ms") }
                        }, color = p.fg3, fontSize = 12.sp)
                    }
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp)) {
                        Chip(Fmt.pingLabel(r.pingMs), Fmt.pingColor(r.pingMs, p))
                        if (r.cfValid) Chip("CF", p.blue)
                        if (r.latMs != null) Chip("OK", p.green)
                    }
                }
            }
        }
    }
}
