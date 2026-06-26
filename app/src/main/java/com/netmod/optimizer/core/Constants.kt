package com.netmod.optimizer.core

import androidx.compose.ui.graphics.Color

/**
 * Port of the `constants` module. The desktop app mutated global color
 * variables; on Android the palette lives in immutable data objects and the
 * active one is chosen by Theme.kt based on the dark/light flag.
 *
 * Dark theme follows the original "Samsung One UI Eye Comfort" palette.
 */
object Dim {
    const val APP_W = 980
    const val APP_H = 660
    const val SIDEBAR_W = 64
}

/** SNI values rotated during probing (was _CF_SNI_ROTATE in the desktop app). */
val CF_SNI_ROTATE = listOf(
    "speed.cloudflare.com",
    "www.cloudflare.com",
    "cf.cloudflare.com",
    "cloudflare.com",
)

data class Palette(
    val bg: Color,
    val bgCard: Color,
    val bgSidebar: Color,
    val bgHover: Color,
    val bgInput: Color,
    val bgHeader: Color,
    val border: Color,
    val borderHover: Color,
    val borderFocus: Color,
    val accent: Color,
    val accd: Color,
    val green: Color,
    val greenDim: Color,
    val orange: Color,
    val orangeDim: Color,
    val redC: Color,
    val redDim: Color,
    val blue: Color,
    val teal: Color,
    val purple: Color,
    val cyan: Color,
    val fg1: Color,
    val fg2: Color,
    val fg3: Color,
    val fg4: Color,
    val statusBg: Color,
    val cardBg1: Color,
    val cardBg2: Color,
    val cardBg3: Color,
    val cardBg4: Color,
    val cardBg5: Color,
) {
    val connected get() = green
    val disconnected get() = fg3
    val connecting get() = orange
}

private fun c(hex: String) = Color(android.graphics.Color.parseColor(hex))

val LightPalette = Palette(
    bg = c("#f4f5f7"), bgCard = c("#ffffff"), bgSidebar = c("#1e1e2e"),
    bgHover = c("#eaeaea"), bgInput = c("#ffffff"), bgHeader = c("#ffffff"),
    border = c("#dde0e8"), borderHover = c("#ccd0d8"), borderFocus = c("#FA7567"),
    accent = c("#FA7567"), accd = c("#e06050"),
    green = c("#1db954"), greenDim = c("#16a34a"),
    orange = c("#f0960a"), orangeDim = c("#e08600"),
    redC = c("#e03030"), redDim = c("#c02020"),
    blue = c("#2979ff"), teal = c("#00b4ab"), purple = c("#7c4dff"), cyan = c("#00bcd4"),
    fg1 = c("#1a1a2e"), fg2 = c("#444466"), fg3 = c("#9999bb"), fg4 = c("#bbbbcc"),
    statusBg = c("#e8e8e8"),
    cardBg1 = c("#e3f2fd"), cardBg2 = c("#e8f5e9"), cardBg3 = c("#fff3e0"),
    cardBg4 = c("#fce4ec"), cardBg5 = c("#f3e5f5"),
)

val DarkPalette = Palette(
    bg = c("#17181c"), bgCard = c("#1e1f23"), bgSidebar = c("#121316"),
    bgHover = c("#26272c"), bgInput = c("#1a1b1f"), bgHeader = c("#1c1d22"),
    border = c("#2c2d33"), borderHover = c("#383940"), borderFocus = c("#5c7cba"),
    accent = c("#5c7cba"), accd = c("#4e6aa8"),
    green = c("#6aaa64"), greenDim = c("#5a9a54"),
    orange = c("#c89050"), orangeDim = c("#b88040"),
    redC = c("#c75050"), redDim = c("#b74040"),
    blue = c("#5c7cba"), teal = c("#5a9a8a"), purple = c("#9078b0"), cyan = c("#6090a0"),
    fg1 = c("#f0f0f0"), fg2 = c("#bcbcc4"), fg3 = c("#6e6e7a"), fg4 = c("#4a4a54"),
    statusBg = c("#121316"),
    cardBg1 = c("#1a2332"), cardBg2 = c("#1a2818"), cardBg3 = c("#2a2218"),
    cardBg4 = c("#2a1818"), cardBg5 = c("#221a2a"),
)
