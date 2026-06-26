package com.netmod.optimizer

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Row
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreHoriz
import androidx.compose.material3.FilterChip
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.netmod.optimizer.ui.AppViewModel
import com.netmod.optimizer.ui.Dest
import com.netmod.optimizer.ui.screens.*
import com.netmod.optimizer.ui.theme.NetModTheme
import com.netmod.optimizer.ui.theme.Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent { NetModTheme { AppRoot() } }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AppRoot() {
    val vm: AppViewModel = viewModel()
    val p = Theme.palette
    var dest by remember { mutableStateOf(Dest.HOME) }

    Scaffold(
        containerColor = p.bg,
        topBar = {
            TopAppBar(
                title = { Text(dest.label, color = p.fg1) },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = p.bgHeader),
                actions = {
                    // Secondary tabs as scrollable chips (Config/Test/Worker/Saved/History/About)
                    Row(Modifier.horizontalScroll(rememberScrollState()).padding(end = 8.dp)) {
                        listOf(Dest.CONFIG, Dest.TEST, Dest.CFWORKER, Dest.FAVORITES, Dest.HISTORY, Dest.ABOUT).forEach { d ->
                            FilterChip(
                                selected = dest == d, onClick = { dest = d },
                                label = { Text(d.label) }, modifier = Modifier.padding(horizontal = 3.dp),
                            )
                        }
                    }
                },
            )
        },
        bottomBar = {
            NavigationBar(containerColor = p.bgHeader) {
                Dest.primary.forEach { d ->
                    NavigationBarItem(
                        selected = dest == d,
                        onClick = { dest = d },
                        icon = { Icon(d.icon, d.label) },
                        label = { Text(d.label) },
                    )
                }
            }
        },
    ) { inner ->
        Box(Modifier.fillMaxSize().padding(inner)) {
            when (dest) {
                Dest.HOME -> HomeScreen(vm)
                Dest.CONFIG -> ConfigScreen(vm)
                Dest.SCAN -> ScanScreen(vm)
                Dest.TEST -> TestScreen(vm)
                Dest.CONNECT -> ConnectScreen(vm)
                Dest.BPB -> BpbScreen(vm)
                Dest.CFWORKER -> CfWorkerScreen(vm)
                Dest.FAVORITES -> FavoritesScreen(vm)
                Dest.HISTORY -> HistoryScreen(vm)
                Dest.SETTINGS -> SettingsScreen(vm)
                Dest.ABOUT -> AboutScreen(vm)
            }
        }
    }
}
