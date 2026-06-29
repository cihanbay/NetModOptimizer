package com.veo.optimizer.ui.screens

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Tab
import androidx.compose.material3.TabRow
import androidx.compose.material3.TabRowDefaults
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.theme.Theme

@Composable
fun WizardScreen(vm: AppViewModel) {
    val p = Theme.palette
    val tabs = listOf("BPB Panel", "CF Worker")
    val selTab = vm.wizardTab

    Column(Modifier.fillMaxSize()) {
        TabRow(
            selectedTabIndex = selTab,
            containerColor = p.bgHeader,
            contentColor = p.fg1,
            indicator = { tabPositions ->
                TabRowDefaults.SecondaryIndicator(
                    Modifier.tabIndicatorOffset(tabPositions[selTab]),
                    color = p.accent,
                )
            },
        ) {
            tabs.forEachIndexed { i, label ->
                Tab(
                    selected = selTab == i,
                    onClick = { vm.wizardTab = i },
                    text = {
                        Text(label, fontSize = 13.sp,
                            fontWeight = if (selTab == i) FontWeight.Bold else FontWeight.Normal)
                    },
                    selectedContentColor = p.accent,
                    unselectedContentColor = p.fg3,
                )
            }
        }
        when (selTab) {
            0 -> BpbScreen(vm)
            1 -> CfWorkerScreen(vm)
        }
    }
}
