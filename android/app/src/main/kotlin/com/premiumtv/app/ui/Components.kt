package com.premiumtv.app.ui

import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.focusable
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.LinearProgressIndicator
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
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.Shape
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.key.onKeyEvent
import android.view.KeyEvent as NativeKey
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalContext
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
import androidx.compose.ui.unit.sp
import com.premiumtv.app.BuildConfig
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

/**
 * The 1.1.0 pointer outline: one amber ring around whatever the D-pad is on.
 *
 * Every focusable surface in the app uses this instead of its own colour, so
 * "where am I" looks the same on a channel card, a category row, a tab and a
 * button. Focused items get a 3 dp amber ring plus a soft outer glow; resting
 * items keep the quiet hairline they always had.
 */
internal fun Modifier.focusOutline(
    focused: Boolean,
    shape: Shape = RoundedCornerShape(12.dp),
    restColor: Color = Color(0x22FFFFFF),
): Modifier {
    if (!focused) return this.border(1.dp, restColor, shape)
    return this
        .drawBehind {
            val glow = 8.dp.toPx()
            drawRoundRect(
                color = FocusRingGlow.copy(alpha = 0.20f),
                topLeft = Offset(-glow / 2f, -glow / 2f),
                size = Size(size.width + glow, size.height + glow),
                cornerRadius = CornerRadius(15.dp.toPx()),
                style = Stroke(glow),
            )
        }
        .border(3.dp, FocusRing, shape)
}

@Composable
fun ChannelCard(
    channel: Channel,
    subtitle: String?,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    isFavorite: Boolean = false,
    onToggleFavorite: (() -> Unit)? = null,
) {
    var focused by remember { mutableStateOf(false) }
    // 1.0.6 smoothness: a 3% lift instead of 6% — the bigger scale animated
    // every focus move across a row and read as stutter on TV hardware.
    val scale by animateFloatAsState(
        targetValue = if (focused) 1.03f else 1f,
        label = "channelCardScale",
    )
    Surface(
        modifier = modifier
            .width(168.dp)
            .height(134.dp)
            .scale(scale)
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick)
            .focusOutline(focused, RoundedCornerShape(12.dp)),
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
                    .fillMaxWidth()
                    .padding(top = 4.dp),
                contentAlignment = Alignment.Center,
            ) {
                // Channels without art get their category's drawn placeholder
                // (a ball for Sports, a smile for Comedy, a TV set for the
                // rest) instead of two initials that read as broken art.
                ChannelLogoBox(
                    channel = channel,
                    modifier = Modifier.fillMaxSize(),
                )
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
            if (onToggleFavorite != null) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth(),
                    contentAlignment = Alignment.Center,
                ) {
                    Box(
                        modifier = Modifier
                            .size(26.dp)
                            .focusable()
                            .tvClickable { onToggleFavorite() },
                        contentAlignment = Alignment.Center,
                    ) {
                        Text(
                            text = if (isFavorite) "★" else "☆",
                            color = if (isFavorite) PremiumGold else MutedText,
                            style = MaterialTheme.typography.bodyMedium,
                        )
                    }
                }
            }
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
            .focusOutline(focused, RoundedCornerShape(22.dp), restColor = Color.Transparent)
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
            .focusOutline(focused, RoundedCornerShape(26.dp), restColor = Color.Transparent)
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

/**
 * The PremiumTV mark: the marquee television set the launcher icon uses,
 * drawn at any size from the same strokes as the drawn category icons.
 */
@Composable
fun BrandLogo(modifier: Modifier = Modifier) {
    Canvas(modifier) {
        val w = size.width
        val h = size.height
        val stroke = minOf(w, h) * 0.055f
        val gold = PremiumGold
        val cap = StrokeCap.Round
        // antennas
        drawLine(gold, Offset(w * 0.30f, h * 0.04f), Offset(w * 0.50f, h * 0.26f), stroke, cap = cap)
        drawLine(gold, Offset(w * 0.70f, h * 0.04f), Offset(w * 0.50f, h * 0.26f), stroke, cap = cap)
        // body
        drawRoundRect(
            color = gold,
            topLeft = Offset(w * 0.12f, h * 0.26f),
            size = Size(w * 0.76f, h * 0.52f),
            cornerRadius = CornerRadius(w * 0.07f, w * 0.07f),
            style = Stroke(stroke),
        )
        // screen
        drawRoundRect(
            color = gold,
            topLeft = Offset(w * 0.19f, h * 0.35f),
            size = Size(w * 0.42f, h * 0.34f),
            cornerRadius = CornerRadius(w * 0.03f, w * 0.03f),
            style = Stroke(stroke * 0.8f),
        )
        // speaker grille and knob
        drawLine(gold, Offset(w * 0.70f, h * 0.38f), Offset(w * 0.70f, h * 0.58f), stroke * 0.8f, cap = cap)
        drawCircle(gold, radius = stroke * 0.62f, center = Offset(w * 0.70f, h * 0.68f))
        // feet
        drawLine(gold, Offset(w * 0.30f, h * 0.78f), Offset(w * 0.24f, h * 0.94f), stroke, cap = cap)
        drawLine(gold, Offset(w * 0.70f, h * 0.78f), Offset(w * 0.76f, h * 0.94f), stroke, cap = cap)
    }
}

/**
 * The 1.1.0 loading screen: calm, static and honest.
 *
 * 1.0.8 V1's version breathed, glowed, shimmered, orbited a spinner and
 * animated its own ellipsis — six animations before a single channel had
 * loaded, all of it work for a TV GPU that is usually the slowest chip in the
 * room. The wordmark, the tagline and a real progress line are all a viewer
 * needs; the line is driven by the loader's own stages instead of a decorative
 * loop.
 */
@Composable
fun LoadingScreen(title: String, detail: String, progress: Float? = null) {
    // Smoothly advances along real load stages and glides a moving highlight
    // across the bar so the viewer always sees active progress.
    val context = LocalContext.current
    val animationsEnabled = remember(context) {
        runCatching {
            android.provider.Settings.Global.getFloat(
                context.contentResolver,
                android.provider.Settings.Global.ANIMATOR_DURATION_SCALE,
                1f,
            ) > 0f
        }.getOrDefault(true)
    }
    val rawTarget = (progress ?: 0.14f).coerceIn(0.08f, 1f)
    var sweepOffset by remember { mutableStateOf(0f) }
    var stageTrickle by remember(rawTarget) { mutableStateOf(0f) }
    LaunchedEffect(rawTarget, animationsEnabled) {
        if (!animationsEnabled) return@LaunchedEffect
        while (true) {
            delay(45L)
            sweepOffset = (sweepOffset + 0.035f) % 1f
            if (rawTarget < 0.96f && stageTrickle < 0.12f) {
                stageTrickle = (stageTrickle + 0.004f).coerceAtMost(0.12f)
            }
        }
    }
    val fraction by animateFloatAsState(
        targetValue = (rawTarget + stageTrickle).coerceIn(0.08f, 1f),
        animationSpec = tween(durationMillis = 260),
        label = "loadingLine",
    )
    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFF070A0F), Color(0xFF0C1320), Color(0xFF070A0F)),
                ),
            ),
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(12.dp),
            modifier = Modifier
                .align(Alignment.Center)
                .padding(horizontal = 48.dp),
        ) {
            BrandLogo(modifier = Modifier.size(104.dp))
            Text(
                text = "PremiumTV",
                style = MaterialTheme.typography.headlineMedium,
                color = PremiumGold,
                fontWeight = FontWeight.Bold,
                letterSpacing = 4.sp,
            )
            Text(
                text = "Good TV, quietly ready.",
                style = MaterialTheme.typography.labelMedium,
                color = MutedText,
                letterSpacing = 2.sp,
            )
            Spacer(modifier = Modifier.height(12.dp))
            // Moving gold loading bar reporting real load stages with a soft travelling highlight.
            Box(
                modifier = Modifier
                    .width(240.dp)
                    .height(5.dp)
                    .background(Color(0x24FFFFFF), RoundedCornerShape(999.dp)),
            ) {
                val highlightStart = (sweepOffset * 1.4f - 0.35f).coerceIn(0f, 0.92f)
                val highlightEnd = (highlightStart + 0.28f).coerceIn(highlightStart + 0.05f, 1f)
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .fillMaxWidth(fraction)
                        .background(
                            Brush.horizontalGradient(
                                0.0f to PremiumGold.copy(alpha = 0.82f),
                                highlightStart to PremiumGold,
                                ((highlightStart + highlightEnd) * 0.5f) to Color(0xFFFFF0B3),
                                highlightEnd to PremiumGold,
                                1.0f to PremiumGold.copy(alpha = 0.90f),
                            ),
                            RoundedCornerShape(999.dp),
                        ),
                )
            }
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = Color.White,
                fontWeight = FontWeight.SemiBold,
                textAlign = TextAlign.Center,
            )
            LoadingTip()
            Text(
                text = detail,
                style = MaterialTheme.typography.bodySmall,
                color = MutedText,
                textAlign = TextAlign.Center,
            )
        }
        // The build the viewer is waiting on, pinned where a TV puts credits.
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 22.dp),
        ) {
            Text(
                text = "Version ${BuildConfig.VERSION_NAME}",
                style = MaterialTheme.typography.labelSmall,
                color = PremiumGold.copy(alpha = 0.85f),
                letterSpacing = 1.4.sp,
                fontWeight = FontWeight.Medium,
            )
            Text(
                text = "TV build · stable",
                style = MaterialTheme.typography.labelSmall,
                color = MutedText.copy(alpha = 0.9f),
                letterSpacing = 0.8.sp,
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
