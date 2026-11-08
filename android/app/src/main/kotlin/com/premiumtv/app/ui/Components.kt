package com.premiumtv.app.ui

import androidx.compose.animation.core.FastOutSlowInEasing
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
import androidx.compose.runtime.Composable
import androidx.compose.ui.composed
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.graphicsLayer
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
import kotlinx.coroutines.Job
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

/** How long a held OK/centre key counts as a long press on a TV remote. */
private const val TV_LONG_PRESS_MS = 550L

/**
 * Makes a control operable by touch, accessibility actions and a TV remote.
 *
 * The handlers stay explicit so a remote's centre key is handled once, rather
 * than once by the key listener and again by a generic click detector. Keeping
 * the latest callback in state also avoids a stale lambda if a lazy-list item
 * is reused after its data changes.
 *
 * The centre key is consumed on ACTION_DOWN as well as ACTION_UP: a held press
 * is tracked for [onLongClick] and a release fires exactly one action. 1.1.5
 * uses that for "hold OK to favourite" on a channel card, which removes the
 * second focus stop (the little star) from every card's D-pad path.
 */
/** The common case: a tap/OK with no long-press action. */
fun Modifier.tvClickable(onClick: () -> Unit): Modifier =
    tvClickable(onClick = onClick, onLongClick = null)

fun Modifier.tvClickable(
    onClick: () -> Unit,
    onLongClick: (() -> Unit)?,
): Modifier = composed {
    val currentOnClick = rememberUpdatedState(onClick)
    val currentOnLongClick = rememberUpdatedState(onLongClick)
    val scope = rememberCoroutineScope()
    var pressJob by remember { mutableStateOf<Job?>(null) }
    var longPressHandled by remember { mutableStateOf(false) }

    fun cancelPress() {
        pressJob?.cancel()
        pressJob = null
    }

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
            if (!isSelectKey) return@onKeyEvent false
            when (native.action) {
                NativeKey.ACTION_DOWN -> {
                    if (currentOnLongClick.value != null && native.repeatCount == 0) {
                        longPressHandled = false
                        cancelPress()
                        pressJob = scope.launch {
                            delay(TV_LONG_PRESS_MS)
                            longPressHandled = true
                            currentOnLongClick.value?.invoke()
                        }
                    }
                    // Consume the press so a parent cannot act on it too.
                    true
                }
                NativeKey.ACTION_UP -> {
                    cancelPress()
                    if (!longPressHandled) currentOnClick.value()
                    longPressHandled = false
                    true
                }
                else -> false
            }
        }
        .onFocusChanged { state ->
            // A focus move mid-press must not leave a timer behind that fires
            // on whatever the viewer is looking at next.
            if (!state.isFocused) {
                cancelPress()
                longPressHandled = false
            }
        }
        .pointerInput(onLongClick != null) {
            if (onLongClick != null) {
                detectTapGestures(
                    onTap = { currentOnClick.value() },
                    onLongPress = { currentOnLongClick.value?.invoke() },
                )
            } else {
                detectTapGestures(onTap = { currentOnClick.value() })
            }
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
    // Both rings use the control's own shape, so a 22 dp tab pill no longer
    // gets a 15 dp-cornered outline that visibly cuts its corners. The dark
    // 5 dp under-stroke leaves 1 dp of contrast on each side of the amber
    // ring, which keeps it readable on the gold selected tab and on a card.
    return this
        .border(5.dp, Color(0xE605080C), shape)
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
    // 1.1.5 smoothness: the 3% lift is applied in the graphics layer and read
    // in the draw phase. `Modifier.scale(scale)` read the animated value during
    // composition, so every frame of every focus move recomposed the card and
    // its artwork — the largest avoidable cost in D-pad browsing on a TV.
    val scale = animateFloatAsState(
        targetValue = if (focused) 1.03f else 1f,
        animationSpec = tween(durationMillis = 110, easing = FastOutSlowInEasing),
        label = "channelCardScale",
    )
    Surface(
        modifier = modifier
            .width(168.dp)
            .height(134.dp)
            .graphicsLayer {
                scaleX = scale.value
                scaleY = scale.value
            }
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick, onLongClick = onToggleFavorite)
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
                    // Touch-only: the star is not a second focus stop any more,
                    // so ▼ on a card goes to the next row instead of stopping
                    // on every favourite glyph. A remote holds OK instead.
                    val currentToggle = rememberUpdatedState(onToggleFavorite)
                    Box(
                        modifier = Modifier
                            .size(28.dp)
                            .semantics {
                                role = Role.Button
                                semanticsOnClick(label = "Favorite") {
                                    currentToggle.value?.invoke()
                                    true
                                }
                            }
                            .pointerInput(Unit) {
                                detectTapGestures { currentToggle.value?.invoke() }
                            },
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
    // A focused tab always darkens, including the selected one: the amber
    // pointer ring used to sit on a gold fill with almost no contrast, so
    // "selected" and "you are here" looked the same. Selected-but-not-focused
    // keeps the gold plaque.
    val background = when {
        selected && !focused -> PremiumGold
        focused -> Color(0xFF1B2531)
        else -> Color(0xFF151C26)
    }
    val foreground = when {
        selected && !focused -> Color(0xFF12160B)
        selected -> PremiumGold
        else -> Color(0xFFE6ECF5)
    }
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
    // The determinate bar follows real loader stages. There is no background
    // shimmer ticker while the library is parsing on slower TV hardware.
    val rawTarget = (progress ?: 0.10f).coerceIn(0.06f, 1f)
    val fraction by animateFloatAsState(
        targetValue = rawTarget,
        animationSpec = tween(durationMillis = 220),
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
            verticalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier
                .align(Alignment.Center)
                .padding(horizontal = 48.dp),
        ) {
            BrandLogo(modifier = Modifier.size(92.dp))
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
            Spacer(modifier = Modifier.height(14.dp))
            // Determinate gold bar: the fill tracks the loader's real
            // stages and has no continuously invalidated decorative layer.
            Box(
                modifier = Modifier
                    .width(260.dp)
                    .height(5.dp)
                    .background(Color(0x24FFFFFF), RoundedCornerShape(999.dp)),
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .fillMaxWidth(fraction)
                        .background(PremiumGold, RoundedCornerShape(999.dp)),
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = title,
                style = MaterialTheme.typography.titleMedium,
                color = Color.White,
                fontWeight = FontWeight.SemiBold,
                textAlign = TextAlign.Center,
            )
            Text(
                text = detail,
                style = MaterialTheme.typography.bodySmall,
                color = MutedText,
                textAlign = TextAlign.Center,
            )
        }
        // One quiet credit line instead of two stacked slogans.
        Text(
            text = "Version ${BuildConfig.VERSION_NAME}  ·  TV build",
            style = MaterialTheme.typography.labelSmall,
            color = PremiumGold.copy(alpha = 0.85f),
            letterSpacing = 1.1.sp,
            modifier = Modifier
                .align(Alignment.BottomCenter)
                .padding(bottom = 24.dp),
        )
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
