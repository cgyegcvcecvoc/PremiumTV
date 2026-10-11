package com.premiumtv.app.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.focusable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.key.Key
import androidx.compose.ui.input.key.KeyEventType
import androidx.compose.ui.input.key.onKeyEvent
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.premiumtv.app.data.Channel

/**
 * Makes anything remote-control and touch operable.
 *
 * Material's `clickable` is a pointer modifier: it does not make a composable a
 * D-pad focus target, and relying on it alone leaves channel cards that can be
 * focused but never opened with the OK button. So focus, the centre/enter keys
 * and taps are each wired up explicitly and exactly once, which also means the
 * action can never fire twice for one press.
 */
fun Modifier.tvClickable(onClick: () -> Unit): Modifier = this
    .focusable()
    .onKeyEvent { event ->
        if (event.type == KeyEventType.KeyUp &&
            (event.key == Key.DirectionCenter || event.key == Key.Enter || event.key == Key.NumPadEnter)
        ) {
            onClick()
            true
        } else {
            false
        }
    }
    .pointerInput(Unit) {
        detectTapGestures(onTap = { onClick() })
    }

@Composable
fun ChannelCard(
    channel: Channel,
    subtitle: String?,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    var focused by remember { mutableStateOf(false) }
    val scale by animateFloatAsState(
        targetValue = if (focused) 1.06f else 1f,
        label = "channelCardScale",
    )
    Surface(
        modifier = modifier
            .width(168.dp)
            .height(134.dp)
            .scale(scale)
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick)
            .border(
                width = if (focused) 3.dp else 1.dp,
                color = if (focused) PremiumGold else Color(0x22FFFFFF),
                shape = RoundedCornerShape(12.dp),
            ),
        shape = RoundedCornerShape(12.dp),
        color = if (focused) CardBackgroundFocused else CardBackground,
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(10.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth(),
                contentAlignment = Alignment.Center,
            ) {
                if (channel.logo.isNotBlank()) {
                    AsyncImage(
                        model = channel.logo,
                        contentDescription = channel.name,
                        contentScale = ContentScale.Fit,
                        modifier = Modifier.fillMaxSize(),
                    )
                } else {
                    Text(
                        text = initialsOf(channel.name),
                        style = MaterialTheme.typography.headlineSmall,
                        color = PremiumGold,
                        fontWeight = FontWeight.Bold,
                    )
                }
            }
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = channel.name,
                style = MaterialTheme.typography.bodySmall,
                color = Color.White,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth(),
            )
            if (!subtitle.isNullOrBlank()) {
                Text(
                    text = subtitle,
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.fillMaxWidth(),
                )
            }
        }
    }
}

@Composable
fun TabChip(label: String, selected: Boolean, onClick: () -> Unit) {
    var focused by remember { mutableStateOf(false) }
    val background = when {
        selected -> PremiumGold
        focused -> Color(0xFF243040)
        else -> Color(0xFF151C26)
    }
    val foreground = if (selected) Color(0xFF12160B) else Color(0xFFE6ECF5)
    Surface(
        modifier = Modifier
            .height(44.dp)
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick),
        shape = RoundedCornerShape(22.dp),
        color = background,
    ) {
        Box(
            modifier = Modifier
                .fillMaxHeight()
                .padding(horizontal = 24.dp),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.titleSmall,
                color = foreground,
                fontWeight = if (selected) FontWeight.Bold else FontWeight.Medium,
            )
        }
    }
}

@Composable
fun FocusButton(label: String, onClick: () -> Unit, modifier: Modifier = Modifier) {
    var focused by remember { mutableStateOf(false) }
    Surface(
        modifier = modifier
            .height(52.dp)
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick),
        shape = RoundedCornerShape(26.dp),
        color = if (focused) PremiumGold else Color(0xFF1D2733),
    ) {
        Box(
            modifier = Modifier
                .fillMaxHeight()
                .padding(horizontal = 28.dp),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = label,
                style = MaterialTheme.typography.titleSmall,
                color = if (focused) Color(0xFF12160B) else Color.White,
            )
        }
    }
}

@Composable
fun CenteredMessage(message: String) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF070A0F)),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text = message,
            style = MaterialTheme.typography.titleMedium,
            color = Color(0xFFE6ECF5),
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(horizontal = 64.dp),
        )
    }
}

@Composable
fun InfoRow(label: String, value: String) {
    Column(modifier = Modifier.padding(vertical = 6.dp)) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MutedText,
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            color = Color.White,
        )
    }
}

private fun initialsOf(name: String): String {
    val letters = name.filter { it.isLetterOrDigit() }
    return when {
        letters.length >= 2 -> letters.substring(0, 2).uppercase()
        letters.length == 1 -> letters.uppercase()
        else -> "TV"
    }
}

/** Used by the category rows so each row header lines up with the cards. */
val SCREEN_GUTTER = 48.dp

/** Spacing helper for a row of cards. */
val CARD_GAP = 16.dp

/** Vertical rhythm between category rows. */
val ROW_ARRANGEMENT: Arrangement.Vertical = Arrangement.spacedBy(4.dp)
