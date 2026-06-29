package com.veo.optimizer.ui

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.CloudUpload
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Radar
import androidx.compose.material.icons.filled.Settings
import androidx.compose.ui.graphics.vector.ImageVector

enum class Dest(val label: String, val icon: ImageVector) {
    HOME("Home", Icons.Filled.Home),
    WIZARD("Wizard", Icons.Filled.CloudUpload),
    SCAN("Scan", Icons.Filled.Radar),
    CONNECT("Connect", Icons.Filled.Bolt),
    SETTINGS("Settings", Icons.Filled.Settings);

    companion object {
        val primary = listOf(HOME, WIZARD, SCAN, CONNECT, SETTINGS)
    }
}
