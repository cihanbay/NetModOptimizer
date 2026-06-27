package com.veo.optimizer.ui.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.staticCompositionLocalOf
import com.veo.optimizer.core.DarkPalette
import com.veo.optimizer.core.LightPalette
import com.veo.optimizer.core.Palette

/** Access the active ported palette anywhere: `Theme.palette`. */
val LocalPalette = staticCompositionLocalOf { LightPalette }

object Theme {
    val palette @Composable get() = LocalPalette.current
}

@Composable
fun VEOTheme(dark: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    val p: Palette = if (dark) DarkPalette else LightPalette
    val scheme = if (dark) darkColorScheme(
        primary = p.accent, onPrimary = androidx.compose.ui.graphics.Color.White,
        background = p.bg, onBackground = p.fg1,
        surface = p.bgCard, onSurface = p.fg1,
        surfaceVariant = p.bgHover, onSurfaceVariant = p.fg2,
        secondary = p.blue, error = p.redC, outline = p.border,
    ) else lightColorScheme(
        primary = p.accent, onPrimary = androidx.compose.ui.graphics.Color.White,
        background = p.bg, onBackground = p.fg1,
        surface = p.bgCard, onSurface = p.fg1,
        surfaceVariant = p.bgHover, onSurfaceVariant = p.fg2,
        secondary = p.blue, error = p.redC, outline = p.border,
    )
    CompositionLocalProvider(LocalPalette provides p) {
        MaterialTheme(colorScheme = scheme, typography = Typography(), content = content)
    }
}
