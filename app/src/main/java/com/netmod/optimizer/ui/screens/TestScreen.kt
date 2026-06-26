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
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
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
fun TestScreen(vm: AppViewModel) {
    val p = Theme.palette
    LazyColumn(Modifier.fillMaxWidth().padding(16.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
        item {
            SectionCard {
                CardTitle("Real-world test", "Measure latency, download & upload through each edge")
                Text("Speed tests run through a temporary local proxy backed by xray-core. Add the libXray AAR to enable live throughput numbers.",
                    color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 6.dp))
                Row(Modifier.fillMaxWidth().padding(top = 10.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    Button(
                        onClick = { if (vm.testing) vm.stopTest() else vm.quickTestTop(20) },
                        modifier = Modifier.weight(1f),
                        colors = ButtonDefaults.buttonColors(containerColor = if (vm.testing) p.redC else p.accent),
                    ) { Text(if (vm.testing) "Stop" else "⚡ Quick Test (parallel)") }
                }
                if (vm.testing) {
                    LinearProgressIndicator(progress = { vm.testProgress }, modifier = Modifier.fillMaxWidth().padding(top = 10.dp), color = p.accent)
                }
                Text(vm.testStatus, color = p.fg3, fontSize = 12.sp, modifier = Modifier.padding(top = 6.dp))
            }
        }
        items(vm.results.take(40)) { r ->
            SectionCard {
                Row(Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                    Column {
                        Text("${r.ip}:${r.port}", color = p.fg1, fontSize = 15.sp, fontWeight = FontWeight.Medium)
                        Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.padding(top = 4.dp)) {
                            Chip("ping ${Fmt.pingLabel(r.pingMs)}", Fmt.pingColor(r.pingMs, p))
                            r.dlMbps?.let { Chip("↓${"%.0f".format(it)}M", Fmt.speedColor(it, p)) }
                            r.upMbps?.let { Chip("↑${"%.0f".format(it)}M", Fmt.speedColor(it, p)) }
                        }
                    }
                    Button({ vm.testResult(r) }, colors = ButtonDefaults.buttonColors(containerColor = p.accent)) { Text("Test") }
                }
            }
        }
    }
}
