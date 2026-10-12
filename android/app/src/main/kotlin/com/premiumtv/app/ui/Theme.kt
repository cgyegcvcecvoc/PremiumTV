package com.premiumtv.app.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

/**
 * The Marquee look: cinema gold on midnight blue.
 *
 * New material (dark surfaces, soft strokes, generous radii) with a classic
 * playbill voice (warm gold, tight display lettering, red ON-AIR accents).
 * The colour names below are shared across the UI files; add new accents here
 * rather than inventing raw hex values in screens.
 */
val PremiumGold = Color(0xFFF3C24B)
val PremiumGoldDim = Color(0xFFB8892F)
val LiveRed = Color(0xFFE2483C)
val CardBackground = Color(0xFF121820)
val CardBackgroundFocused = Color(0xFF1C2530)
val MutedText = Color(0xFF9FB0C4)
val PanelStroke = Color(0x22FFFFFF)

private val TvColors = darkColorScheme(
    primary = PremiumGold,
    onPrimary = Color(0xFF12160B),
    primaryContainer = PremiumGoldDim,
    onPrimaryContainer = Color(0xFF12160B),
    secondary = PremiumGold,
    onSecondary = Color(0xFF12160B),
    background = Color(0xFF070A0F),
    onBackground = Color(0xFFF2F4F8),
    surface = Color(0xFF11171F),
    onSurface = Color(0xFFF2F4F8),
    surfaceVariant = Color(0xFF1A222D),
    onSurfaceVariant = Color(0xFFB9C3D0),
    outline = Color(0xFF3A4552),
    error = LiveRed,
)

private val TvTypography = Typography(
    headlineMedium = TextStyle(
        fontWeight = FontWeight.Bold,
        letterSpacing = (-0.2).sp,
    ),
    headlineSmall = TextStyle(
        fontWeight = FontWeight.Bold,
        letterSpacing = (-0.1).sp,
    ),
    titleLarge = TextStyle(
        fontWeight = FontWeight.Bold,
        letterSpacing = (-0.1).sp,
    ),
    titleMedium = TextStyle(
        fontWeight = FontWeight.SemiBold,
        letterSpacing = 0.1.sp,
    ),
    labelSmall = TextStyle(
        fontWeight = FontWeight.Medium,
        letterSpacing = 0.4.sp,
    ),
)

@Composable
fun PremiumTvTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = TvColors,
        typography = TvTypography,
        content = content,
    )
}
