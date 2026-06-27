package com.veo.optimizer.core

import androidx.compose.ui.graphics.Color
import kotlin.math.abs

/** Port of _fmt_bytes / _fmt_speed and the *_color / *_label helpers. */
object Fmt {
    fun bytes(b: Long): String {
        var v = b.toDouble()
        val units = listOf("B", "KB", "MB", "GB", "TB")
        var i = 0
        while (v >= 1024 && i < units.size - 1) { v /= 1024; i++ }
        return if (i == 0) "${b} B" else "%.1f %s".format(v, units[i])
    }

    fun speed(bps: Double): String {
        val bits = bps * 8
        return when {
            bits >= 1_000_000_000 -> "%.2f Gbps".format(bits / 1e9)
            bits >= 1_000_000 -> "%.1f Mbps".format(bits / 1e6)
            bits >= 1_000 -> "%.0f Kbps".format(bits / 1e3)
            else -> "%.0f bps".format(bits)
        }
    }

    fun speedShort(bps: Double): String {
        val bits = bps * 8
        return when {
            bits >= 1_000_000 -> "%.1fM".format(bits / 1e6)
            bits >= 1_000 -> "%.0fK".format(bits / 1e3)
            else -> "%.0f".format(bits)
        }
    }

    // ── color thresholds (port of _ping_color/_speed_color/_loss_color/_jitter_color)
    fun pingColor(ms: Double?, p: Palette): Color = when {
        ms == null -> p.fg3
        ms < 100 -> p.green
        ms < 200 -> p.orange
        else -> p.redC
    }

    fun pingLabel(ms: Double?, unit: String = "ms"): String =
        if (ms == null) "—" else "${ms.toInt()} $unit"

    fun speedColor(mbps: Double?, p: Palette): Color = when {
        mbps == null -> p.fg3
        mbps >= 20 -> p.green
        mbps >= 5 -> p.orange
        else -> p.redC
    }

    fun lossColor(pct: Double?, p: Palette): Color = when {
        pct == null -> p.fg3
        pct <= 0.0 -> p.green
        pct < 25 -> p.orange
        else -> p.redC
    }

    fun jitterColor(ms: Double?, p: Palette): Color = when {
        ms == null -> p.fg3
        abs(ms) < 30 -> p.green
        abs(ms) < 80 -> p.orange
        else -> p.redC
    }
}
