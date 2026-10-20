package com.premiumtv.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Team badges for the Live Events tab (1.0.8).
 *
 * A game's name is the only identity the playlist gives a team, so the badge
 * is drawn from the name itself: the same team always wears the same two
 * colours and the same initials, on every tab and every launch, with no
 * network request and nothing to load in. The palette stays inside the app's
 * saturation/lightness band so every badge looks like it belongs next to the
 * gold-and-midnight UI.
 */

/** A stable hue in 0..360 for a team name; the same name always maps the same. */
internal fun teamHue(name: String): Float {
    var hash = 7
    for (character in name.lowercase().trim()) {
        hash = hash * 31 + character.code
    }
    return ((hash % 360f) + 360f) % 360f
}

/** Up to two initials for the badge: first letters of the first two words. */
internal fun teamInitials(name: String): String {
    val words = name.trim().split(Regex("\\s+")).filter { it.isNotBlank() }
    return when {
        words.isEmpty() -> "?"
        words.size == 1 -> words[0].take(2).uppercase()
        else -> (words[0].take(1) + words[1].take(1)).uppercase()
    }
}

/** The two badge colours for a team name, as a gradient pair. */
internal fun teamColors(name: String): Pair<Color, Color> {
    val hue = teamHue(name)
    return Color.hsl(hue, saturation = 0.58f, lightness = 0.44f) to
        Color.hsl((hue + 26f) % 360f, saturation = 0.52f, lightness = 0.28f)
}

/**
 * A team's round badge: the team's two colours split diagonally, its initials
 * centred, a hairline ring so light and dark badges both sit on the card.
 */
@Composable
fun TeamCrest(
    name: String,
    modifier: Modifier = Modifier,
    size: Dp = 34.dp,
) {
    val (start, end) = remember(name) { teamColors(name) }
    Box(
        modifier = modifier
            .size(size)
            .clip(CircleShape)
            .background(Brush.linearGradient(listOf(start, end)))
            .border(1.dp, Color(0x44FFFFFF), CircleShape),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text = teamInitials(name),
            style = MaterialTheme.typography.labelSmall,
            color = Color.White,
            fontWeight = FontWeight.Bold,
        )
    }
}
