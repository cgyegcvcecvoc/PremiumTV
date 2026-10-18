package com.premiumtv.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Icon
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.graphics.vector.path
import androidx.compose.ui.graphics.vector.rememberVectorPainter
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.premiumtv.app.data.Channel

/*
 * The logo a channel shows when it has none of its own.
 *
 * Before 1.0.5 a channel without a tvg-logo showed two initials, which read
 * as broken art on a TV screen. Now every logo-less channel gets a drawn
 * placeholder: the category decides the picture - a ball for Sports, a
 * smile for Comedy, a balloon for Kids - and the generic set is a television
 * outline, the app's own mark. The vectors are drawn here rather than added
 * as drawables so the whole fallback stays one testable mapping function.
 */

/** Which placeholder picture a category gets. Pure so it can be unit tested. */
internal fun iconKeyForGroup(group: String): String {
    val key = group.lowercase()
    return when {
        "sport" in key || "soccer" in key || "football" in key || "hockey" in key ||
            "basketball" in key || "baseball" in key || "ufc" in key || "mma" in key ||
            "boxing" in key || "wrestling" in key || "golf" in key || "tennis" in key ||
            "formula 1" in key || "nascar" in key || "cricket" in key || "rugby" in key -> "ball"
        "comed" in key -> "smile"
        "weather" in key -> "weather"
        "news" in key -> "news"
        "kid" in key || "cartoon" in key -> "balloon"
        "music" in key -> "music"
        "movie" in key -> "movie"
        "documentar" in key || "education" in key || "culture" in key -> "book"
        "business" in key -> "chart"
        "religious" in key -> "cross"
        "legislative" in key -> "law"
        "lifestyle" in key || "relax" in key || "family" in key -> "heart"
        "series" in key || "celebrit" in key || "entertainment" in key ||
            "game show" in key || "tv show" in key || "paranormal" in key -> "star"
        "international" in key || "global" in key || "online" in key -> "globe"
        else -> "tv"
    }
}

private const val VIEWPORT = 24f
private const val STROKE_WIDTH = 1.7f

private fun icon(name: String, block: androidx.compose.ui.graphics.vector.ImageVector.Builder.() -> Unit): ImageVector =
    ImageVector.Builder(
        name = name,
        defaultWidth = 24.dp,
        defaultHeight = 24.dp,
        viewportWidth = VIEWPORT,
        viewportHeight = VIEWPORT,
    ).apply(block).build()

private val Stroke = SolidColor(Color.White)

/** The generic set: a television outline with antennas - the app's own mark. */
private val TvIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Tv") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            // antennas
            moveTo(9f, 3.6f); lineTo(12f, 7f)
            moveTo(15f, 3.6f); lineTo(12f, 7f)
            // body
            moveTo(5f, 8f); horizontalLineTo(19f)
            arcTo(2f, 2f, 0f, false, true, 21f, 10f); verticalLineTo(18f)
            arcTo(2f, 2f, 0f, false, true, 19f, 20f); horizontalLineTo(5f)
            arcTo(2f, 2f, 0f, false, true, 3f, 18f); verticalLineTo(10f)
            arcTo(2f, 2f, 0f, false, true, 5f, 8f); close()
            // screen
            moveTo(6.4f, 11f); horizontalLineTo(13.6f); verticalLineTo(17f); horizontalLineTo(6.4f); close()
            // speaker
            moveTo(17.2f, 11.6f); verticalLineTo(16.4f)
            // feet
            moveTo(8f, 20f); lineTo(6.8f, 22.4f)
            moveTo(16f, 20f); lineTo(17.2f, 22.4f)
        }
    }
}

private val BallIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Ball") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(3f, 12f)
            arcTo(9f, 9f, 0f, true, true, 21f, 12f)
            arcTo(9f, 9f, 0f, true, true, 3f, 12f); close()
            moveTo(12f, 6.8f); lineTo(16.2f, 9.9f); lineTo(14.6f, 15f)
            lineTo(9.4f, 15f); lineTo(7.8f, 9.9f); close()
            moveTo(12f, 3.1f); verticalLineTo(6.8f)
            moveTo(20.6f, 9.4f); lineTo(16.2f, 9.9f)
            moveTo(18.9f, 19.2f); lineTo(14.6f, 15f)
            moveTo(5.1f, 19.2f); lineTo(9.4f, 15f)
            moveTo(3.4f, 9.4f); lineTo(7.8f, 9.9f)
        }
    }
}

private val SmileIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Smile") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round) {
            moveTo(3f, 12f)
            arcTo(9f, 9f, 0f, true, true, 21f, 12f)
            arcTo(9f, 9f, 0f, true, true, 3f, 12f); close()
            moveTo(8f, 14.2f)
            arcTo(5.4f, 5.4f, 0f, false, false, 16f, 14.2f)
        }
        path(fill = Stroke) {
            moveTo(9f, 8.4f)
            arcTo(1.1f, 1.1f, 0f, true, true, 9.01f, 8.4f); close()
            moveTo(15f, 8.4f)
            arcTo(1.1f, 1.1f, 0f, true, true, 15.01f, 8.4f); close()
        }
    }
}

private val NewsIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("News") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(4f, 5f); horizontalLineTo(20f); verticalLineTo(19f); horizontalLineTo(4f); close()
            moveTo(7f, 9f); horizontalLineTo(17f)
            moveTo(7f, 12f); horizontalLineTo(17f)
            moveTo(7f, 15f); horizontalLineTo(13f)
        }
    }
}

private val BalloonIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Balloon") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(7.6f, 9.2f)
            arcTo(4.4f, 5.4f, 0f, true, true, 16.4f, 9.2f)
            arcTo(4.4f, 5.4f, 0f, true, true, 7.6f, 9.2f); close()
            moveTo(12f, 14.6f); verticalLineTo(16.2f)
            moveTo(12f, 16.2f); curveTo(14.2f, 17.8f, 10.2f, 19.2f, 12.4f, 21.4f)
        }
    }
}

private val MusicIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Music") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(5.6f, 17.8f)
            arcTo(2.4f, 2.2f, 0f, true, true, 10.4f, 17.8f)
            arcTo(2.4f, 2.2f, 0f, true, true, 5.6f, 17.8f); close()
            moveTo(10.4f, 17.8f); verticalLineTo(5.4f); lineTo(18.6f, 3.6f); verticalLineTo(13.6f)
            moveTo(13.8f, 13.6f)
            arcTo(2.4f, 2.2f, 0f, true, true, 18.6f, 13.6f)
            arcTo(2.4f, 2.2f, 0f, true, true, 13.8f, 13.6f); close()
        }
    }
}

private val MovieIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Movie") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(3f, 6f); horizontalLineTo(21f); verticalLineTo(18f); horizontalLineTo(3f); close()
            moveTo(7.2f, 6f); verticalLineTo(18f)
            moveTo(16.8f, 6f); verticalLineTo(18f)
            moveTo(10.4f, 9.4f); lineTo(14.2f, 12f); lineTo(10.4f, 14.6f); close()
        }
    }
}

private val WeatherIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Weather") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(5.6f, 8.4f)
            arcTo(2.8f, 2.8f, 0f, true, true, 11.2f, 8.4f)
            arcTo(2.8f, 2.8f, 0f, true, true, 5.6f, 8.4f); close()
            moveTo(8.4f, 2.4f); verticalLineTo(4f)
            moveTo(2.8f, 8.4f); horizontalLineTo(4.2f)
            moveTo(12.6f, 8.4f); horizontalLineTo(14f)
            moveTo(4.4f, 4.4f); lineTo(5.4f, 5.4f)
            moveTo(12.4f, 4.4f); lineTo(11.4f, 5.4f)
            moveTo(6.4f, 19.6f); horizontalLineTo(17.2f)
            arcTo(3f, 3f, 0f, false, false, 16.6f, 13.8f)
            arcTo(4.4f, 4.4f, 0f, false, false, 9.2f, 13.4f)
            arcTo(3.3f, 3.3f, 0f, false, false, 6.4f, 19.6f); close()
        }
    }
}

private val BookIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Book") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(4f, 5f)
            curveTo(8f, 3.8f, 16f, 3.8f, 20f, 5f)
            verticalLineTo(18.6f)
            curveTo(16f, 17.4f, 8f, 17.4f, 4f, 18.6f)
            close()
            moveTo(12f, 4.3f); verticalLineTo(17.9f)
        }
    }
}

private val ChartIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Chart") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(4f, 3.6f); verticalLineTo(20.4f); horizontalLineTo(21f)
            moveTo(8f, 20.4f); verticalLineTo(13.6f)
            moveTo(12.4f, 20.4f); verticalLineTo(8.8f)
            moveTo(16.8f, 20.4f); verticalLineTo(11.6f)
        }
    }
}

private val StarIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Star") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineJoin = StrokeJoin.Round) {
            moveTo(12f, 3.4f); lineTo(14.7f, 9.2f); lineTo(20.9f, 9.9f)
            lineTo(16.3f, 14.2f); lineTo(17.6f, 20.4f); lineTo(12f, 17.2f)
            lineTo(6.4f, 20.4f); lineTo(7.7f, 14.2f); lineTo(3.1f, 9.9f)
            lineTo(9.3f, 9.2f); close()
        }
    }
}

private val HeartIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Heart") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(12f, 20.2f)
            curveTo(6.6f, 16f, 3.6f, 12.8f, 3.6f, 9.6f)
            arcTo(4.3f, 4.3f, 0f, true, true, 12f, 7.6f)
            arcTo(4.3f, 4.3f, 0f, true, true, 20.4f, 9.6f)
            curveTo(20.4f, 12.8f, 17.4f, 16f, 12f, 20.2f)
            close()
        }
    }
}

private val CrossIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Cross") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineJoin = StrokeJoin.Round) {
            moveTo(10f, 3f); horizontalLineTo(14f); verticalLineTo(9f)
            horizontalLineTo(20f); verticalLineTo(13f); horizontalLineTo(14f)
            verticalLineTo(21f); horizontalLineTo(10f); verticalLineTo(13f)
            horizontalLineTo(4f); verticalLineTo(9f); horizontalLineTo(10f)
            close()
        }
    }
}

private val LawIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Law") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(3f, 9f); lineTo(12f, 3.8f); lineTo(21f, 9f)
            moveTo(5.6f, 9f); verticalLineTo(18f)
            moveTo(9.9f, 9f); verticalLineTo(18f)
            moveTo(14.1f, 9f); verticalLineTo(18f)
            moveTo(18.4f, 9f); verticalLineTo(18f)
            moveTo(3f, 20.6f); horizontalLineTo(21f)
        }
    }
}

private val GlobeIcon: ImageVector by lazy(LazyThreadSafetyMode.NONE) {
    icon("Globe") {
        path(stroke = Stroke, strokeLineWidth = STROKE_WIDTH, strokeLineCap = StrokeCap.Round, strokeLineJoin = StrokeJoin.Round) {
            moveTo(3f, 12f)
            arcTo(9f, 9f, 0f, true, true, 21f, 12f)
            arcTo(9f, 9f, 0f, true, true, 3f, 12f); close()
            moveTo(3.2f, 12f); horizontalLineTo(20.8f)
            moveTo(12f, 3.1f)
            curveTo(8.6f, 6.6f, 8.6f, 17.4f, 12f, 20.9f)
            curveTo(15.4f, 17.4f, 15.4f, 6.6f, 12f, 3.1f)
        }
    }
}

/** The placeholder picture for a category; the television set is the default. */
internal fun placeholderIconFor(group: String): ImageVector = when (iconKeyForGroup(group)) {
    "ball" -> BallIcon
    "smile" -> SmileIcon
    "news" -> NewsIcon
    "balloon" -> BalloonIcon
    "music" -> MusicIcon
    "movie" -> MovieIcon
    "weather" -> WeatherIcon
    "book" -> BookIcon
    "chart" -> ChartIcon
    "star" -> StarIcon
    "heart" -> HeartIcon
    "cross" -> CrossIcon
    "law" -> LawIcon
    "globe" -> GlobeIcon
    else -> TvIcon
}

/**
 * A channel's logo with its category placeholder underneath: remote art while
 * it loads or when its URL is dead, the drawn icon when it has none at all.
 */
@Composable
fun ChannelLogoBox(channel: Channel, modifier: Modifier = Modifier) {
    val placeholder = remember(channel.group) { placeholderIconFor(channel.group) }
    val placeholderPainter = rememberVectorPainter(placeholder)
    if (channel.logo.isNotBlank()) {
        AsyncImage(
            model = channel.logo,
            contentDescription = channel.name,
            contentScale = ContentScale.Fit,
            error = placeholderPainter,
            placeholder = placeholderPainter,
            modifier = modifier,
        )
    } else {
        Box(
            modifier = modifier.background(Color(0x14FFFFFF), RoundedCornerShape(10.dp)),
            contentAlignment = Alignment.Center,
        ) {
            Icon(
                imageVector = placeholder,
                contentDescription = null,
                tint = PremiumGold,
                modifier = Modifier.fillMaxSize(0.78f),
            )
        }
    }
}
