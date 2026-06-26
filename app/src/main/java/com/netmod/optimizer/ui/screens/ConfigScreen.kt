package com.netmod.optimizer.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.unit.dp
import com.netmod.optimizer.ui.AppViewModel
import com.netmod.optimizer.ui.components.CardTitle
import com.netmod.optimizer.ui.components.SectionCard
import com.netmod.optimizer.ui.theme.Theme

@Composable
fun ConfigScreen(vm: AppViewModel) {
    val p = Theme.palette
    val clip = LocalClipboardManager.current
    var uid by remember { mutableStateOf(vm.profile.uid) }
    var host by remember { mutableStateOf(vm.profile.host) }
    var sni by remember { mutableStateOf(vm.profile.sni) }
    var path by remember { mutableStateOf(vm.profile.path) }
    var network by remember { mutableStateOf(vm.profile.network) }
    var importUrl by remember { mutableStateOf("") }
    var msg by remember { mutableStateOf("") }

    fun save() = vm.updateProfile {
        this.uid = uid; this.host = host; this.sni = sni; this.path = path; this.network = network
    }

    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
                CardTitle("Import vless://", "Paste a config link to auto-fill")
                OutlinedTextField(importUrl, { importUrl = it }, label = { Text("vless://…") },
                    modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button({
                        val text = clip.getText()?.text ?: ""; if (text.isNotBlank()) importUrl = text
                    }, colors = ButtonDefaults.buttonColors(containerColor = p.bgHover, contentColor = p.fg2)) { Text("Paste") }
                    Button({
                        val ok = vm.importVless(importUrl)
                        msg = if (ok) "✔ Imported" else "✖ Invalid link"
                        if (ok) { uid = vm.profile.uid; host = vm.profile.host; sni = vm.profile.sni; path = vm.profile.path; network = vm.profile.network }
                    }, modifier = Modifier.weight(1f), colors = ButtonDefaults.buttonColors(containerColor = p.accent)) { Text("Import") }
                }
                if (msg.isNotEmpty()) Text(msg, color = p.fg3, modifier = Modifier.padding(top = 6.dp))
            }
        }
        item {
            SectionCard {
                CardTitle("VLESS config")
                OutlinedTextField(uid, { uid = it; save() }, label = { Text("UUID") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(host, { host = it; save() }, label = { Text("Host (SNI/CDN)") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(sni, { sni = it; save() }, label = { Text("SNI") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(path, { path = it; save() }, label = { Text("Path") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("ws", "grpc", "h2").forEach { n ->
                        Button({ network = n; save() }, colors = ButtonDefaults.buttonColors(
                            containerColor = if (network == n) p.accent else p.bgHover,
                            contentColor = if (network == n) androidx.compose.ui.graphics.Color.White else p.fg2,
                        )) { Text(n) }
                    }
                }
            }
        }
    }
}
