package com.premiumtv.app.ui

import androidx.compose.animation.core.EaseInOutCubic
import androidx.compose.animation.core.RepeatMode
import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.rememberInfiniteTransition
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
import androidx.compose.material3.CircularProgressIndicator
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
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.alpha
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.geometry.CornerRadius
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.input.key.onKeyEvent
import android.view.KeyEvent as NativeKey
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.platform.LocalDensity
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
 * 1.0.8 V1 Patch loading screen: layered marquee animation that stays light
 * on TV hardware — a breathing logo, sweeping gold underline, pulsing spinner
 * orbit and shimmering title. The stream of tips still cycles every 8 s, but
 * now fades rather than cuts, and the version plaque shows the V patch name.
 */
@Composable
fun LoadingScreen(title: String, detail: String) {
    // Brush offsets are in pixels, and Dp.toPx() only exists inside a Density
    // receiver (a Canvas draw scope has one; this composable body does not).
    // Resolve the two animated widths once here instead of calling toPx() in
    // the Modifier chain below, which does not compile.
    val density = LocalDensity.current
    val underlineWidthPx = with(density) { 110.dp.toPx() }
    val barWidthPx = with(density) { 160.dp.toPx() }
    val infinite = rememberInfiniteTransition(label = "loading")
    val logoPulse by infinite.animateFloat(
        initialValue = 1f,
        targetValue = 1.06f,
        animationSpec = infiniteRepeatable(tween(1400, easing = EaseInOutCubic), RepeatMode.Reverse),
        label = "logoPulse",
    )
    val logoGlow by infinite.animateFloat(
        initialValue = 0.55f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(1400, easing = EaseInOutCubic), RepeatMode.Reverse),
        label = "logoGlow",
    )
    val shimmerShift by infinite.animateFloat(
        initialValue = 0f,
        targetValue = 1f,
        animationSpec = infiniteRepeatable(tween(2200, easing = EaseInOutCubic), RepeatMode.Restart),
        label = "shimmer",
    )
    val barProgress by infinite.animateFloat(
        initialValue = 0.08f,
        targetValue = 0.92f,
        animationSpec = infiniteRepeatable(tween(1600, easing = EaseInOutCubic), RepeatMode.Reverse),
        label = "bar",
    )
    // Animated ellipsis for the loading title.
    var dotCount by remember { mutableIntStateOf(0) }
    LaunchedEffect(Unit) {
        while (true) { delay(420L); dotCount = (dotCount + 1) % 4 }
    }
    val dots = ".".repeat(dotCount)

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFF070A0F), Color(0xFF0C1320), Color(0xFF070A0F)),
                ),
            ),
    ) {
        // Subtle drifting gold haze behind the logo — two soft circles that
        // breathe with the same pulse, cheap to draw on a TV GPU.
        Canvas(
            modifier = Modifier
                .align(Alignment.Center)
                .size(420.dp)
                .alpha(0.12f * logoGlow),
        ) {
            drawCircle(
                color = PremiumGold,
                radius = size.minDimension * 0.38f * logoPulse,
                center = Offset(size.width * 0.5f, size.height * 0.42f),
            )
            drawCircle(
                color = PremiumGoldDim,
                radius = size.minDimension * 0.22f * (1.04f - (logoPulse - 1f)),
                center = Offset(size.width * 0.5f, size.height * 0.44f),
            )
        }
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.spacedBy(10.dp),
            modifier = Modifier
                .align(Alignment.Center)
                .padding(horizontal = 48.dp),
        ) {
            Box(
                modifier = Modifier.size(112.dp),
                contentAlignment = Alignment.Center,
            ) {
                // Outer halo ring that breathes with the logo.
                Canvas(modifier = Modifier.fillMaxSize().alpha(0.18f * logoGlow)) {
                    drawCircle(
                        color = PremiumGold,
                        radius = size.minDimension * 0.48f * logoPulse,
                        center = center,
                        style = Stroke(width = 1.5.dp.toPx()),
                    )
                }
                BrandLogo(modifier = Modifier.size(104.dp).scale(logoPulse).alpha(0.85f + 0.15f * logoGlow))
            }
            Text(
                text = "PremiumTV",
                style = MaterialTheme.typography.headlineMedium,
                color = PremiumGold,
                fontWeight = FontWeight.Bold,
                letterSpacing = 4.sp,
            )
            // Shimmer underline — a thin gold gradient that sweeps endlessly.
            Box(
                modifier = Modifier
                    .width(110.dp)
                    .height(2.dp)
                    .background(
                        Brush.linearGradient(
                            colors = listOf(
                                Color.Transparent,
                                PremiumGold.copy(alpha = 0.9f),
                                Color.Transparent,
                            ),
                            start = Offset(x = underlineWidthPx * (shimmerShift - 1f), y = 0f),
                            end = Offset(x = underlineWidthPx * shimmerShift, y = 0f),
                        ),
                    ),
            )
            Text(
                text = "Every channel, one guide",
                style = MaterialTheme.typography.labelMedium,
                color = MutedText,
                letterSpacing = 2.sp,
            )
            Spacer(modifier = Modifier.height(6.dp))
            // Orbit spinner: gold arc with trailing dots around a dim track.
            Box(modifier = Modifier.size(38.dp), contentAlignment = Alignment.Center) {
                CircularProgressIndicator(
                    color = PremiumGold,
                    strokeWidth = 3.dp,
                    modifier = Modifier.size(38.dp),
                )
                Canvas(modifier = Modifier.size(8.dp).alpha(logoGlow)) {
                    drawCircle(color = PremiumGold, radius = size.minDimension / 2)
                }
            }
            // Thin shimmer loading bar.
            Box(
                modifier = Modifier
                    .width(160.dp)
                    .height(3.dp)
                    .background(Color(0x22FFFFFF), RoundedCornerShape(999.dp)),
            ) {
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .fillMaxWidth(barProgress)
                        .background(PremiumGold, RoundedCornerShape(999.dp)),
                )
                // Sweep highlight
                Box(
                    modifier = Modifier
                        .fillMaxHeight()
                        .fillMaxWidth(0.3f)
                        .background(
                            Brush.horizontalGradient(
                                listOf(Color.Transparent, Color.White.copy(alpha = 0.55f), Color.Transparent),
                                startX = barWidthPx * (shimmerShift - 0.5f),
                                endX = barWidthPx * (shimmerShift + 0.2f),
                            ),
                        ),
                )
            }
            // Title with animated ellipsis so the TV never looks frozen.
            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(4.dp)) {
                Text(
                    text = title + dots,
                    style = MaterialTheme.typography.titleMedium,
                    color = Color.White,
                    fontWeight = FontWeight.SemiBold,
                )
                // Tiny pulsing dot cluster beside the title.
                repeat(3) { index ->
                    val dotAlpha by infinite.animateFloat(
                        initialValue = 0.25f,
                        targetValue = 1f,
                        animationSpec = infiniteRepeatable(
                            tween(700, delayMillis = index * 160, easing = EaseInOutCubic),
                            RepeatMode.Reverse,
                        ),
                        label = "dot$index",
                    )
                    Canvas(modifier = Modifier.size(4.dp).alpha(dotAlpha)) {
                        drawCircle(color = PremiumGold, radius = size.minDimension / 2)
                    }
                }
            }
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
            val displayName = remember(BuildConfig.VERSION_NAME) {
                // Show V patch name when this is a V release (1.0.8.1 -> 1.0.8 V1).
                val raw = BuildConfig.VERSION_NAME
                val parts = raw.split(".")
                if (parts.size == 4 && parts[3].toIntOrNull() != null && parts[3] != "0") {
                    "${parts[0]}.${parts[1]}.${parts[2]} V${parts[3]} Patch"
                } else raw
            }
            Text(
                text = "Version $displayName",
                style = MaterialTheme.typography.labelSmall,
                color = PremiumGold.copy(alpha = 0.85f),
                letterSpacing = 1.4.sp,
                fontWeight = FontWeight.Medium,
            )
            Text(
                text = "${BuildConfig.VERSION_NAME} · TV build · patched",
                style = MaterialTheme.typography.labelSmall,
                color = MutedText.copy(alpha = 0.9f),
                letterSpacing = 0.8.sp,
                modifier = Modifier.alpha(0.9f),
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
