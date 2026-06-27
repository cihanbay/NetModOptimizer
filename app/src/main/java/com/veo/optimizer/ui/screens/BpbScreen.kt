package com.veo.optimizer.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
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
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.deploy.DeployTarget
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.components.CardTitle
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme
import java.util.UUID

@Composable
fun BpbScreen(vm: AppViewModel) {
    val p = Theme.palette
    var email by remember { mutableStateOf("") }
    var apiKey by remember { mutableStateOf("") }
    var acctId by remember { mutableStateOf("") }
    var script by remember { mutableStateOf("bpb-panel") }
    var uuid by remember { mutableStateOf(vm.profile.uid.ifEmpty { UUID.randomUUID().toString() }) }

    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
                CardTitle("BPB Panel deploy", "Deploy the full BPB worker to your Cloudflare account")
                OutlinedTextField(email, { email = it }, label = { Text("CF email") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(apiKey, { apiKey = it }, label = { Text("Global API key") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(acctId, { acctId = it }, label = { Text("Account ID") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(script, { script = it }, label = { Text("Worker name") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                OutlinedTextField(uuid, { uuid = it }, label = { Text("UUID") }, modifier = Modifier.fillMaxWidth().padding(top = 8.dp))
                Button(
                    onClick = {
                        vm.deployWorker(DeployTarget(script, email, apiKey, acctId, script, uuid), bpb = true)
                    },
                    enabled = !vm.deploying,
                    modifier = Modifier.fillMaxWidth().padding(top = 10.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = p.accent),
                ) { Text(if (vm.deploying) "Deploying…" else "Deploy BPB worker") }
            }
        }
        item {
            SectionCard {
                CardTitle("Deploy log")
                Column(
                    Modifier.fillMaxWidth().heightIn(min = 80.dp, max = 280.dp)
                        .padding(top = 8.dp).clip(RoundedCornerShape(10.dp)).background(p.bgInput)
                        .padding(10.dp).verticalScroll(rememberScrollState()),
                ) {
                    if (vm.deployLog.isEmpty()) Text("No deploy yet.", color = p.fg3, fontSize = 12.sp)
                    vm.deployLog.forEach { Text(it, color = p.fg2, fontSize = 12.sp, fontFamily = FontFamily.Monospace) }
                }
                vm.lastDeploy?.let { r ->
                    if (r.success) Text("✔ ${r.workerHost}\nSub: ${r.subUrl}", color = p.green, fontSize = 12.sp, modifier = Modifier.padding(top = 8.dp))
                }
            }
        }
    }
}
