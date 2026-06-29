package com.veo.optimizer

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Icon
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.material3.TopAppBarDefaults
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import com.veo.optimizer.ui.AppViewModel
import com.veo.optimizer.ui.Dest
import com.veo.optimizer.ui.screens.*
import com.veo.optimizer.ui.theme.VEOTheme
import com.veo.optimizer.ui.theme.Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent { VEOTheme { AppRoot() } }
    }
}

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
                Dest.WIZARD -> WizardScreen(vm)
                Dest.SCAN -> ScanScreen(vm)
                Dest.CONNECT -> ConnectScreen(vm)
                Dest.SETTINGS -> SettingsScreen(vm)
            }
        }
    }
}
