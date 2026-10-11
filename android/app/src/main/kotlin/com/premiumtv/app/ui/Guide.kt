package com.premiumtv.app.ui

import com.premiumtv.app.data.Programme
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/** The programme on air at [now], if the guide covers this channel. */
fun nowPlaying(programmes: List<Programme>, now: Long): Programme? =
    programmes.firstOrNull { now >= it.start && now < it.end }

/** The next programme starting at or after [now]. */
fun nextUp(programmes: List<Programme>, now: Long): Programme? =
    programmes.firstOrNull { it.start >= now }

/** How far through [programme] we are, 0..1. */
fun progressOf(programme: Programme, now: Long): Float {
    val span = programme.end - programme.start
    if (span <= 0L) return 0f
    return ((now - programme.start).toFloat() / span.toFloat()).coerceIn(0f, 1f)
}

// Only ever touched from the main thread, which is where every caller runs.
private val CLOCK = SimpleDateFormat("h:mm a", Locale.US)
private val DAY_CLOCK = SimpleDateFormat("EEE h:mm a", Locale.US)
private val REFRESH_INSTANT = SimpleDateFormat("MMM d, h:mm a z", Locale.US)

fun formatClock(epochSeconds: Long): String = CLOCK.format(Date(epochSeconds * 1000L))

fun formatRange(start: Long, end: Long): String =
    "${formatClock(start)} - ${formatClock(end)}"

fun formatDay(epochSeconds: Long): String = DAY_CLOCK.format(Date(epochSeconds * 1000L))

/** Device-local date/time for refresh history and the next WorkManager slot. */
fun formatRefreshInstant(epochMillis: Long): String = REFRESH_INSTANT.format(Date(epochMillis))
