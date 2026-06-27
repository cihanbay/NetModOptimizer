package com.veo.optimizer.core

import androidx.compose.ui.graphics.Color

object Dim {
    const val APP_W = 980
    const val APP_H = 660
    const val SIDEBAR_W = 64
}

val CF_SNI_ROTATE = listOf(
    "speed.cloudflare.com",
    "cloudflare.com",
    "www.cloudflare.com",
    "blog.cloudflare.com",
)

val CF_PORTS = listOf(443, 8443, 2053, 2083, 2087, 2096)

val CF_IP_RANGES = listOf(
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "198.41.128.0/17",
    "162.158.0.0/15",
    "104.16.0.0/13",
    "104.24.0.0/14",
    "172.64.0.0/13",
    "131.0.72.0/22",
)

val CF_IP_RANGES_SMALL = listOf(
    "173.245.48.0/20",
    "103.21.244.0/22",
    "103.22.200.0/22",
    "103.31.4.0/22",
    "141.101.64.0/18",
    "108.162.192.0/18",
    "190.93.240.0/20",
    "188.114.96.0/20",
    "197.234.240.0/22",
    "162.158.0.0/15",
    "198.41.128.0/17",
    "104.16.0.0/16",
    "104.17.0.0/16",
    "104.18.0.0/16",
    "104.19.0.0/16",
    "104.20.0.0/14",
    "104.24.0.0/14",
    "172.64.0.0/16",
    "172.65.0.0/16",
    "172.66.0.0/16",
    "172.67.0.0/16",
    "131.0.72.0/22",
)

val CF_IP_RANGES_104_172 = listOf(
    "104.16.0.0/16",
    "104.17.0.0/16",
    "104.18.0.0/16",
    "104.19.0.0/16",
    "104.20.0.0/14",
    "104.24.0.0/14",
    "172.64.0.0/16",
    "172.65.0.0/16",
    "172.66.0.0/16",
    "172.67.0.0/16",
)

val CF_SNI_LIST = listOf(
    "speed.cloudflare.com",
    "cloudflare.com",
    "www.cloudflare.com",
    "cf.cloudflare.com",
)

data class ProviderRange(val label: String, val ranges: List<String>)

val PROVIDER_RANGES = listOf(
    ProviderRange("Custom", emptyList()),
    ProviderRange("CF 173.245.48.0/20", listOf("173.245.48.0/20")),
    ProviderRange("CF 103.21.244.0/22", listOf("103.21.244.0/22")),
    ProviderRange("CF 141.101.64.0/18", listOf("141.101.64.0/18")),
    ProviderRange("CF 108.162.192.0/18", listOf("108.162.192.0/18")),
    ProviderRange("CF 190.93.240.0/20", listOf("190.93.240.0/20")),
    ProviderRange("CF 188.114.96.0/20", listOf("188.114.96.0/20")),
    ProviderRange("CF 197.234.240.0/22", listOf("197.234.240.0/22")),
    ProviderRange("CF 131.0.72.0/22", listOf("131.0.72.0/22")),
    ProviderRange("CF 103.31.4.0/22", listOf("103.31.4.0/22")),
    ProviderRange("CF 103.22.200.0/22", listOf("103.22.200.0/22")),
    ProviderRange("CF 162.158.0.0/15 (big)", listOf("162.158.0.0/15")),
    ProviderRange("CF 198.41.128.0/17 (big)", listOf("198.41.128.0/17")),
    ProviderRange("CF 104.16.0.0/16 (a)", listOf("104.16.0.0/16")),
    ProviderRange("CF 104.17.0.0/16 (b)", listOf("104.17.0.0/16")),
    ProviderRange("CF 104.18.0.0/16 (c)", listOf("104.18.0.0/16")),
    ProviderRange("CF 104.19.0.0/16 (d)", listOf("104.19.0.0/16")),
    ProviderRange("CF 104.20.0.0/14", listOf("104.20.0.0/14")),
    ProviderRange("CF 104.24.0.0/14", listOf("104.24.0.0/14")),
    ProviderRange("CF 172.64.0.0/16 (a)", listOf("172.64.0.0/16")),
    ProviderRange("CF 172.65.0.0/16 (b)", listOf("172.65.0.0/16")),
    ProviderRange("CF 172.66.0.0/16 (c)", listOf("172.66.0.0/16")),
    ProviderRange("CF 172.67.0.0/16 (d)", listOf("172.67.0.0/16")),
    ProviderRange("CF All (small ranges)", CF_IP_RANGES_SMALL),
    ProviderRange("CF All (104.16-19 + 172.64-67)", CF_IP_RANGES_104_172),
    ProviderRange("Vercel Edge (76.76.21/24)", listOf("76.76.21.0/24")),
    ProviderRange("Vercel Broad (76.76/16)", listOf("76.76.0.0/16")),
    ProviderRange("Fastly", listOf(
        "151.101.0.0/16", "157.52.64.0/18", "167.82.0.0/17",
        "185.31.16.0/22", "199.232.0.0/16", "103.245.222.0/24", "199.27.72.0/21",
    )),
    ProviderRange("Netlify", listOf("netlify.app")),
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
