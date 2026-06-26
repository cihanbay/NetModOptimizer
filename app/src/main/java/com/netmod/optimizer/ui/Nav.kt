package com.netmod.optimizer.ui

import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Bolt
import androidx.compose.material.icons.filled.CloudUpload
import androidx.compose.material.icons.filled.Dns
import androidx.compose.material.icons.filled.Favorite
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Link
import androidx.compose.material.icons.filled.Radar
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.Speed
import androidx.compose.ui.graphics.vector.ImageVector

/** Navigation destinations — one per desktop tab. */
enum class Dest(val label: String, val icon: ImageVector) {
    HOME("Home", Icons.Filled.Home),
    CONFIG("Config", Icons.Filled.Dns),
    SCAN("Scan", Icons.Filled.Radar),
    TEST("Test", Icons.Filled.Speed),
    CONNECT("Connect", Icons.Filled.Bolt),
    BPB("BPB", Icons.Filled.CloudUpload),
    CFWORKER("Worker", Icons.Filled.Link),
    FAVORITES("Saved", Icons.Filled.Favorite),
    HISTORY("History", Icons.Filled.History),
    SETTINGS("Settings", Icons.Filled.Settings),
    ABOUT("About", Icons.Filled.Info);

    companion object {
        /** Primary tabs shown in the bottom bar; the rest live in the overflow drawer. */
        val primary = listOf(HOME, SCAN, CONNECT, BPB, SETTINGS)
    }
}
