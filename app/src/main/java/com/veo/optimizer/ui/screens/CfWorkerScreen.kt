package com.veo.optimizer.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
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
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.deploy.DeployTarget
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.components.CardTitle
import com.veo.optimizer.ui.components.Chip
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme
import java.util.UUID

@Composable
fun CfWorkerScreen(vm: AppViewModel) {
    val p = Theme.palette
    var email by remember { mutableStateOf("") }
    var apiKey by remember { mutableStateOf("") }
    var acctId by remember { mutableStateOf("") }
    var script by remember { mutableStateOf("vless-core") }
    var uuid by remember { mutableStateOf(UUID.randomUUID().toString()) }

    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
                CardTitle("Minimal worker creator", "Deploy a lightweight VLESS core worker")
                OutlinedTextField(email, { email = it }, label = { Text("CF email") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(apiKey, { apiKey = it }, label = { Text("Global API key") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(acctId, { acctId = it }, label = { Text("Account ID") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(script, { script = it }, label = { Text("Worker name") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(uuid, { uuid = it }, label = { Text("UUID") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Button(
                    onClick = { vm.deployWorker(DeployTarget(script, email, apiKey, acctId, script, uuid), bpb = false) },
                    enabled = !vm.deploying,
                    modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = p.accent),
                ) { Text(if (vm.deploying) "Deploying…" else "Deploy core worker") }
            }
        }
        item { Text("Deployed workers", color = p.fg2, fontSize = 14.sp, fontWeight = FontWeight.SemiBold) }
        items(vm.profile.cfWorkers) { w ->
            SectionCard {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Column {
                        Text(w.name.ifEmpty { w.workerHost }, color = p.fg1, fontSize = 14.sp, fontWeight = FontWeight.Medium)
                        Text(w.workerHost, color = p.fg3, fontSize = 12.sp)
                    }
                    Chip(if (w.healthy == true) "healthy" else "check", if (w.healthy == true) p.green else p.orange)
                }
                Button({ vm.healthcheckWorker(w.workerHost, uuid) },
                    modifier = Modifier.padding(top = 8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = p.bgHover, contentColor = p.fg2)) { Text("Healthcheck") }
            }
        }
    }
}
