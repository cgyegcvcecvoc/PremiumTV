package com.premiumtv.app.ui

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Typography
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

val PremiumGold = Color(0xFFFFC24B)
val CardBackground = Color(0xFF121820)
val CardBackgroundFocused = Color(0xFF1C2530)
val MutedText = Color(0xFF9FB0C4)

private val TvColors = darkColorScheme(
    primary = PremiumGold,
    onPrimary = Color(0xFF12160B),
    secondary = PremiumGold,
    onSecondary = Color(0xFF12160B),
    background = Color(0xFF070A0F),
    onBackground = Color(0xFFF2F4F8),
    surface = Color(0xFF11171F),
    onSurface = Color(0xFFF2F4F8),
    surfaceVariant = Color(0xFF1A222D),
    onSurfaceVariant = Color(0xFFB9C3D0),
)

@Composable
fun PremiumTvTheme(content: @Composable () -> Unit) {
    MaterialTheme(
        colorScheme = TvColors,
        typography = Typography(),
        content = content,
    )
}
