package com.veo.optimizer.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalClipboardManager
import androidx.compose.ui.text.AnnotatedString
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.core.Fmt
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.components.CardTitle
import com.veo.optimizer.ui.components.LabeledRow
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme

@Composable
fun SettingsScreen(vm: AppViewModel) {
    val p = Theme.palette
    var threads by remember { mutableStateOf(vm.profile.threads.toString()) }
    var timeout by remember { mutableStateOf(vm.profile.timeout.toString()) }
    var topN by remember { mutableStateOf(vm.profile.topN.toString()) }
    var newName by remember { mutableStateOf("") }

    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
                CardTitle("Profiles")
                vm.profiles.forEachIndexed { i, pr ->
                    Row(Modifier.fillMaxWidth().padding(vertical = 4.dp), verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween) {
                        Text(pr.name, color = if (i == vm.profileIndex) p.accent else p.fg1, fontSize = 14.sp,
                            fontWeight = if (i == vm.profileIndex) FontWeight.Bold else FontWeight.Normal)
                        Button({ vm.selectProfile(i) }, colors = ButtonDefaults.buttonColors(
                            containerColor = if (i == vm.profileIndex) p.accent else p.bgHover,
                            contentColor = if (i == vm.profileIndex) androidx.compose.ui.graphics.Color.White else p.fg2,
                        )) { Text(if (i == vm.profileIndex) "Active" else "Use") }
                    }
                }
                Row(Modifier.fillMaxWidth().padding(top = 8.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(newName, { newName = it }, label = { Text("New profile") }, modifier = Modifier.weight(1f))
                    Button({ vm.newProfile(newName); newName = "" }, colors = ButtonDefaults.buttonColors(containerColor = p.accent)) { Text("Add") }
                }
                Button({ vm.deleteProfile() }, modifier = Modifier.padding(top = 8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = p.redC)) { Text("Delete current") }
            }
        }
        item {
            SectionCard {
                CardTitle("Scan parameters")
                OutlinedTextField(threads, { threads = it; vm.updateProfile { this.threads = it.toIntOrNull() ?: 200 } },
                    label = { Text("Concurrency") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(timeout, { timeout = it; vm.updateProfile { this.timeout = it.toDoubleOrNull() ?: 5.0 } },
                    label = { Text("Timeout (s)") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(topN, { topN = it; vm.updateProfile { this.topN = it.toIntOrNull() ?: 20 } },
                    label = { Text("Top N results") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
            }
        }
        item {
            SectionCard {
                CardTitle("Diagnostics")
                Button(
                    onClick = { vm.shareDiagnostics() },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = p.blue),
                ) { Text("Share Diagnostic Report") }
                Text("Tap above to generate a full system snapshot for troubleshooting.",
                    color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 6.dp))
            }
        }
    }
}

@Composable
fun HistoryScreen(vm: AppViewModel) {
    val p = Theme.palette
    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item { CardTitle("Scan history", "Past scans for ${vm.profile.name}") }
        items(vm.profile.scanHistory) { h ->
            SectionCard {
                Text(h.name, color = p.fg1, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                LabeledRow("Scanned", "${h.scanned}")
                LabeledRow("Alive", "${h.results.size}")
                LabeledRow("Best", Fmt.pingLabel(h.results.minOfOrNull { it.pingMs ?: Double.MAX_VALUE }))
            }
        }
        if (vm.profile.scanHistory.isEmpty()) item { Text("No history yet.", color = p.fg3, fontSize = 13.sp) }
    }
}

@Composable
fun FavoritesScreen(vm: AppViewModel) {
    val p = Theme.palette
    val clip = LocalClipboardManager.current
    var url by remember { mutableStateOf("") }
    var name by remember { mutableStateOf("") }
    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
                CardTitle("Add favorite")
                OutlinedTextField(name, { name = it }, label = { Text("Name") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(url, { url = it }, label = { Text("vless:// link") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Button({ if (url.isNotBlank()) { vm.addFavorite(url, name.ifBlank { "Fav" }); url = ""; name = "" } },
                    modifier = Modifier.padding(top = 8.dp), colors = ButtonDefaults.buttonColors(containerColor = p.accent)) { Text("Save") }
            }
        }
        items(vm.profile.favorites) { f ->
            SectionCard {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    androidx.compose.foundation.layout.Column(Modifier.weight(1f)) {
                        Text(f.name, color = p.fg1, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                        Text(f.url, color = p.fg3, fontSize = 11.sp, maxLines = 1)
                    }
                    Button({ clip.setText(AnnotatedString(f.url)) }, colors = ButtonDefaults.buttonColors(containerColor = p.bgHover, contentColor = p.fg2)) { Text("Copy") }
                }
            }
        }
        if (vm.profile.favorites.isEmpty()) item { Text("No favorites saved.", color = p.fg3, fontSize = 13.sp) }
    }
}
