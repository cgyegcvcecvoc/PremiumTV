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
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.LaunchedEffect
import kotlinx.coroutines.delay
import androidx.compose.runtime.Composable
import androidx.compose.ui.composed
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.key.onKeyEvent
import android.view.KeyEvent as NativeKey
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.semantics.disabled
import androidx.compose.ui.semantics.LiveRegionMode
import androidx.compose.ui.semantics.liveRegion
import androidx.compose.ui.semantics.Role
import androidx.compose.ui.semantics.onClick as semanticsOnClick
import androidx.compose.ui.semantics.role
import androidx.compose.ui.semantics.semantics
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.premiumtv.app.data.Channel

/**
 * Makes a control operable by touch, accessibility actions and a TV remote.
 *
 * The handlers stay explicit so a remote's centre key is handled once, rather
 * than once by the key listener and again by a generic click detector. Keeping
 * the latest callback in state also avoids a stale lambda if a lazy-list item
 * is reused after its data changes.
 */
fun Modifier.tvClickable(onClick: () -> Unit): Modifier = composed {
    val currentOnClick = rememberUpdatedState(onClick)
    this
        .semantics(mergeDescendants = true) {
            role = Role.Button
            semanticsOnClick(label = null) {
                currentOnClick.value()
                true
            }
        }
        .focusable()
        .onKeyEvent { event ->
            val native = event.nativeKeyEvent
            val isSelectKey = native.keyCode == NativeKey.KEYCODE_DPAD_CENTER ||
                native.keyCode == NativeKey.KEYCODE_ENTER ||
                native.keyCode == NativeKey.KEYCODE_NUMPAD_ENTER
            if (native.action == NativeKey.ACTION_UP && isSelectKey) {
                currentOnClick.value()
                true
            } else {
                false
            }
        }
        .pointerInput(Unit) {
            detectTapGestures(onTap = { currentOnClick.value() })
        }
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

// The click handler is deliberately the last parameter: a trailing lambda
// binds to the last parameter, so putting the modifier last would make
// FocusButton("Refresh") { ... } hand the lambda to the modifier instead.
@Composable
fun FocusButton(label: String, modifier: Modifier = Modifier, enabled: Boolean = true, onClick: () -> Unit) {
    var focused by remember { mutableStateOf(false) }
    Surface(
        modifier = modifier
            .height(52.dp)
            .onFocusChanged { focused = it.isFocused }
            .then(if (enabled) Modifier.tvClickable(onClick) else Modifier)
            .semantics { if (!enabled) disabled() },
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
                color = if (!enabled) MutedText else if (focused) Color(0xFF12160B) else Color.White,
            )
        }
    }
}

@Composable
fun LoadingScreen(title: String, detail: String) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF070A0F)),
        contentAlignment = Alignment.Center,
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(14.dp),
        ) {
            CircularProgressIndicator(color = PremiumGold, strokeWidth = 3.dp)
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = Color.White,
            )
            LoadingTip()
            Text(
                text = detail,
                style = MaterialTheme.typography.bodySmall,
                color = MutedText,
                textAlign = TextAlign.Center,
            )
        }
    }
}

@Composable
fun LoadErrorScreen(message: String, onRetry: () -> Unit) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color(0xFF070A0F)),
        contentAlignment = Alignment.Center,
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(16.dp),
            modifier = Modifier.padding(horizontal = 64.dp),
        ) {
            Text(
                text = "Channels couldn't be loaded",
                style = MaterialTheme.typography.titleLarge,
                color = Color.White,
                textAlign = TextAlign.Center,
            )
            Text(
                text = message,
                style = MaterialTheme.typography.bodyMedium,
                color = MutedText,
                textAlign = TextAlign.Center,
            )
            FocusButton("Retry loading") { onRetry() }
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

/**
 * Two clean initials for a channel that has no logo, used by the channel cards
 * and by the cable-grid channel column. It lives here rather than in either
 * screen so both surfaces fall back to the same label.
 */
internal fun initialsOf(name: String): String {
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

/** Product-specific, offline tips: no network request or tracking while loading. */
private val loadingTips = listOf(
    "TIP · You can browse and watch channels while the guide loads.",
    "TIP · Settings → Force refresh downloads both the channel list and guide.",
    "FACT · XMLTV is the programme-listing format used by PremiumTV.",
    "TIP · Back from a show returns to your previous tab and guide position.",
    "FACT · The bundled library works even when a refresh cannot reach the network.",
    "TIP · A stream may be offline or region-restricted even after a successful check.",
)

@Composable
fun LoadingTip() {
    var index by remember { mutableStateOf(0) }
    LaunchedEffect(Unit) {
        while (true) { delay(8_000L); index = (index + 1) % loadingTips.size }
    }
    Text(loadingTips[index], color = MutedText, style = MaterialTheme.typography.bodySmall,
        textAlign = TextAlign.Center, modifier = Modifier.padding(horizontal = 24.dp))
}

/** Non-modal: do not steal remote focus or hide the last usable library. */
@Composable
fun LibraryActivity(active: Boolean, message: String, startedAt: Long) {
    var elapsed by remember(startedAt) { mutableStateOf(0L) }
    LaunchedEffect(active, startedAt) {
        while (active) {
            elapsed = ((System.currentTimeMillis() - startedAt) / 1000L).coerceAtLeast(0L)
            delay(1_000L)
        }
    }
    Column(
        Modifier.fillMaxWidth().background(CardBackground).padding(12.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        if (active) androidx.compose.material3.LinearProgressIndicator(
            modifier = Modifier.fillMaxWidth(), color = PremiumGold,
        )
        Text(
            text = message + if (active) " · ${elapsed}s" else "",
            color = PremiumGold, style = MaterialTheme.typography.bodySmall,
            modifier = Modifier.semantics { liveRegion = LiveRegionMode.Polite },
        )
        if (active) LoadingTip()
    }
}
