package com.veo.optimizer.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Switch
import androidx.compose.material3.SwitchDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.components.CardTitle
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme

@Composable
fun ConfigScreen(vm: AppViewModel) {
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

    fun save() = vm.updateProfile {
        this.uid = uid; this.host = host; this.sni = sni; this.path = path
        this.network = network; this.security = security; this.fp = fp
        this.alpn = alpn; this.allowInsecure = allowInsecure; this.grpcService = grpcService
    }

    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
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
            SectionCard {
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
                            contentColor = if (network == n) androidx.compose.ui.graphics.Color.White else p.fg2,
                        )) { Text(n) }
                    }
                }
                Text("Security", color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
                Row(Modifier.fillMaxWidth().padding(top = 4.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("tls", "reality", "none").forEach { s ->
                        Button({ security = s; save() }, colors = ButtonDefaults.buttonColors(
                            containerColor = if (security == s) p.accent else p.bgHover,
                            contentColor = if (security == s) androidx.compose.ui.graphics.Color.White else p.fg2,
                        )) { Text(s) }
                    }
                }
            }
        }
        item {
            SectionCard {
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
            SectionCard {
                CardTitle("Test Config", "Verify this config works before connecting")
                Button(
                    onClick = {
                        if (!vm.profile.hasConfig) { msg = "Fill UUID + Host first"; return@Button }
                        val best = vm.pickAutoBest()
                        if (best != null) {
                            vm.connect(best)
                            msg = "Testing connection to ${best.ip}…"
                        } else {
                            msg = "Run a scan first to find edge IPs"
                        }
                    },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = p.teal),
                ) { Text("Test Connection") }
                if (msg.isNotEmpty()) Text(msg, color = p.fg3, modifier = Modifier.padding(top = 6.dp))
            }
        }
    }
}
