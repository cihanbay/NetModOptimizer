package com.veo.optimizer.ui.screens

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
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
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.components.CardTitle
import com.veo.optimizer.ui.components.SectionCard
import com.veo.optimizer.ui.theme.Theme

@Composable
fun SettingsScreen(vm: AppViewModel) {
    val p = Theme.palette
    var newName by remember { mutableStateOf("") }

    LazyColumn(Modifier.fillMaxSize().padding(12.dp), verticalArrangement = Arrangement.spacedBy(10.dp)) {
        item {
            SectionCard(Modifier.padding(0.dp)) {
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
            SectionCard(Modifier.padding(0.dp)) {
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
