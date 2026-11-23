package com.premiumtv.app.data

import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

/*
 * The Live Events clock.
 *
 * A kickoff is one instant, but "5:45 PM" only means something next to the
 * clock it is read on. This object is the single answer to "which clock are
 * this screen's kickoff times read in": the device's own zone unless the
 * viewer picked another one, and then the same zone for the clock, the cards
 * and the countdowns.
 *
 * Which zones are offered starts from the location the viewer already gave the
 * local-channels shelf: the saved market's longitude picks the band of zones to
 * suggest, the device's own zone always leads the list, and the pick is stored
 * on the device only. Nothing here reads a location - the caller passes the
 * longitude it already has (data/LocalChannels.kt).
 *
 * Kept free of Compose and of Android framework types so the zone rules can be
 * unit tested on the JVM, the same way LiveEvents.kt is.
 */

/** One zone the clock can show, with the label a viewer reads. */
data class ClockZone(
    /** IANA name, e.g. "America/New_York"; "" means "follow the device". */
    val zone: String,
    val label: String,
)

object LiveClock {
    /** Where the viewer's choice is stored, on the device only. */
    const val STORAGE_KEY = "premiumtv.live.clockZone"

    data class Band(
        val id: String,
        /** Heading for the picker, so a zone list reads as places, not paths. */
        val label: String,
        val min: Double,
        val max: Double,
        val zones: List<String>,
    )

    /**
     * Zones offered per band, nearest-used first. A viewer in that part of the
     * world is most likely to want one of these when travelling or following a
     * league abroad; the device's own zone always leads the list.
     */
    val BANDS: List<Band> = listOf(
        Band(
            "americas", "The Americas", -180.0, -30.0,
            listOf(
                "America/New_York", "America/Chicago", "America/Denver",
                "America/Los_Angeles", "America/Anchorage", "Pacific/Honolulu",
                "America/Toronto", "America/Mexico_City", "America/Sao_Paulo",
                "America/Argentina/Buenos_Aires",
            ),
        ),
        Band(
            "atlantic", "Europe, Africa & the Atlantic", -30.0, 40.0,
            listOf(
                // Ordered by how often a US or travelling viewer wants them,
                // because other bands are only previewed with their first few.
                "Europe/London", "Europe/Paris", "Europe/Berlin", "Europe/Madrid",
                "Europe/Rome", "Europe/Lisbon", "Europe/Dublin", "Europe/Amsterdam",
                "Europe/Stockholm", "Europe/Warsaw", "UTC", "Europe/Moscow",
                "Africa/Lagos", "Africa/Johannesburg",
            ),
        ),
        Band(
            "east", "South & East Asia", 40.0, 90.0,
            listOf(
                "Asia/Dubai", "Asia/Karachi", "Asia/Kolkata", "Asia/Dhaka",
                "Asia/Bangkok", "Asia/Jakarta", "Asia/Singapore", "Asia/Shanghai",
                "Asia/Hong_Kong", "Asia/Tokyo", "Asia/Seoul",
            ),
        ),
        Band(
            "pacific", "East Asia & the Pacific", 90.0, 180.0,
            listOf(
                "Asia/Shanghai", "Asia/Hong_Kong", "Asia/Manila", "Asia/Tokyo",
                "Asia/Seoul", "Australia/Perth", "Australia/Adelaide",
                "Australia/Sydney", "Pacific/Auckland",
            ),
        ),
    )

    /** The device's own zone, as an IANA name. */
    fun deviceZone(): String = TimeZone.getDefault().id ?: ""

    /** True when this runtime knows [zone]; a stale saved name must not crash. */
    fun isKnownZone(zone: String?): Boolean {
        val text = zone?.trim().orEmpty()
        if (text.isEmpty()) return false
        // UTC and GMT are always available to java.util.TimeZone.
        return try {
            TimeZone.getTimeZone(text).id == text || TimeZone.getAvailableIDs().contains(text)
        } catch (_: Exception) {
            false
        }
    }

    /** A zone name as a person reads it: "America/New_York" -> "New York". */
    fun zoneLabel(zone: String?): String {
        val text = zone?.trim().orEmpty()
        if (text.isEmpty()) return "Device time"
        if (text == "UTC") return "UTC"
        return text.substringAfterLast('/').replace('_', ' ')
    }

    /**
     * The band a longitude falls in, or null when there is no location. Bands
     * deliberately meet at their edges rather than overlapping twice: east
     * Asia is readable from both its neighbours' lists anyway.
     */
    fun bandForLongitude(longitude: Double?): Band? {
        val value = longitude ?: return null
        if (value.isNaN() || value.isInfinite()) return null
        val bounded = ((value + 180.0) % 360.0 + 360.0) % 360.0 - 180.0
        return BANDS.firstOrNull { bounded >= it.min && bounded < it.max }
    }

    /**
     * The zones to offer: the device's own first, UTC next, then the saved
     * market's band, then two from each other band so a viewer who moved (or
     * follows a league elsewhere) still finds their zone without typing it.
     */
    fun suggestZones(deviceZone: String?, longitude: Double?, limit: Int = 24): List<ClockZone> {
        val out = LinkedHashMap<String, ClockZone>()
        fun add(zone: String?) {
            val text = zone?.trim().orEmpty()
            if (text.isEmpty() || out.size >= limit || !isKnownZone(text) || out.containsKey(text)) return
            out[text] = ClockZone(text, zoneLabel(text))
        }
        add(deviceZone)
        if (deviceZone?.trim() != "UTC") add("UTC")
        val band = bandForLongitude(longitude)
        band?.zones?.forEach { add(it) }
        for (other in BANDS) {
            if (band != null && other.id == band.id) continue
            other.zones.take(5).forEach { add(it) }
        }
        return out.values.toList()
    }

    /** The zone a choice resolves to, falling back to the device's own. */
    fun resolveZone(choice: String?, deviceZone: String? = deviceZone()): String {
        val wanted = choice?.trim().orEmpty()
        if (wanted.isNotEmpty() && isKnownZone(wanted)) return wanted
        val device = deviceZone?.trim().orEmpty()
        return if (device.isNotEmpty() && isKnownZone(device)) device else ""
    }

    /** A [SimpleDateFormat] for [pattern] in the resolved zone. */
    private fun formatter(pattern: String, zone: String): SimpleDateFormat {
        val formatter = SimpleDateFormat(pattern, Locale.getDefault())
        formatter.timeZone = if (zone.isEmpty()) TimeZone.getDefault() else TimeZone.getTimeZone(zone)
        return formatter
    }

    /** The time of day in the clock's zone, e.g. "7:42:05 PM". */
    fun clockText(nowMs: Long, zone: String): String =
        formatter("h:mm:ss a", zone).format(Date(nowMs))

    /** The date in the clock's zone, e.g. "Mon, Nov 23". */
    fun dateText(nowMs: Long, zone: String): String =
        formatter("EEE, MMM d", zone).format(Date(nowMs))

    /** A kickoff as a time of day in the clock's zone, e.g. "5:45 PM". */
    fun kickoffText(kickoffMs: Long, zone: String): String =
        formatter("h:mm a", zone).format(Date(kickoffMs))

    /**
     * The zone's offset right now, as "GMT-5" (or "GMT+5:30" where the hour is
     * not whole). Read from the zone itself, so it follows daylight saving.
     */
    fun offsetLabel(nowMs: Long, zone: String): String {
        val effective = if (zone.isEmpty()) TimeZone.getDefault() else TimeZone.getTimeZone(zone)
        val minutes = effective.getOffset(nowMs) / 60000
        val sign = if (minutes < 0) "-" else "+"
        val abs = kotlin.math.abs(minutes)
        val hours = abs / 60
        val mins = abs % 60
        return if (mins == 0) "GMT$sign$hours" else "GMT$sign$hours:" + mins.toString().padStart(2, '0')
    }

    /** How far the clock's zone is from the device's: "+3 h", "-2 h 30 m". */
    fun deltaLabel(nowMs: Long, zone: String, deviceZone: String): String {
        val zoneMinutes = (if (zone.isEmpty()) TimeZone.getDefault() else TimeZone.getTimeZone(zone)).getOffset(nowMs) / 60000
        val deviceMinutes = (if (deviceZone.isEmpty()) TimeZone.getDefault() else TimeZone.getTimeZone(deviceZone)).getOffset(nowMs) / 60000
        val total = zoneMinutes - deviceMinutes
        if (total == 0) return ""
        val sign = if (total > 0) "+" else "-"
        val abs = kotlin.math.abs(total)
        val hours = abs / 60
        val mins = abs % 60
        if (hours == 0) return "$sign$mins min"
        return "$sign$hours h" + if (mins != 0) " $mins m" else ""
    }

    /** The clock's own one-line reading: "7:42:05 PM · New York · GMT-5". */
    fun clockLine(nowMs: Long, choice: String?, deviceZone: String = deviceZone()): String {
        val zone = resolveZone(choice, deviceZone)
        return listOf(clockText(nowMs, zone), zoneLabel(zone), offsetLabel(nowMs, zone))
            .filter { it.isNotEmpty() }
            .joinToString(" · ")
    }

    /** A kickoff plus the clock's offset: "5:45 PM · GMT-5". */
    fun kickoffStamp(kickoffMs: Long, choice: String?, deviceZone: String = deviceZone()): String {
        val zone = resolveZone(choice, deviceZone)
        val label = kickoffText(kickoffMs, zone)
        val offset = offsetLabel(System.currentTimeMillis(), zone)
        return if (offset.isEmpty()) label else "$label · $offset"
    }

    /**
     * The soonest kickoff still ahead - `(instant epoch seconds, title)` - or
     * null. Used for the header's "next kickoff" line, which is the one thing a
     * viewer wants from a clock on this screen.
     */
    fun nextKickoff(events: List<Pair<Long?, String>>, nowEpochSeconds: Long): Pair<Long, String>? {
        var best: Pair<Long, String>? = null
        for ((instant, title) in events) {
            if (instant == null || instant <= nowEpochSeconds) continue
            if (best == null || instant < best!!.first) best = instant to title
        }
        return best
    }

    /** Seconds remaining until kickoff, as "mm:ss", "h:mm:ss" or "dd hh:mm:ss". */
    fun countdownText(seconds: Long): String {
        val safe = seconds.coerceAtLeast(0)
        return when {
            safe < 3600 -> "%02d:%02d".format(safe / 60, safe % 60)
            safe < 86400 -> "%d:%02d:%02d".format(safe / 3600, (safe % 3600) / 60, safe % 60)
            else -> "%dd %d:%02d:%02d".format(
                safe / 86400, (safe % 86400) / 3600, (safe % 3600) / 60, safe % 60,
            )
        }
    }

    /**
     * The sentence under the clock: which clock the times are read in, and how
     * long until the next kickoff.
     */
    fun summary(
        nowEpochSeconds: Long,
        choice: String?,
        deviceZone: String,
        events: List<Pair<Long?, String>>,
    ): String {
        val zone = resolveZone(choice, deviceZone)
        val offset = offsetLabel(nowEpochSeconds * 1000L, zone)
        val where = zoneLabel(zone) + if (offset.isNotEmpty()) " ($offset)" else ""
        val custom = zone.isNotEmpty() && deviceZone.isNotEmpty() && zone != deviceZone
        var text = if (custom) {
            "Kickoff times are read in $where, not this device's clock."
        } else {
            "Kickoff times are read in your clock, $where."
        }
        val next = nextKickoff(events, nowEpochSeconds)
        if (next != null) {
            text += " Next kickoff in ${countdownText(next.first - nowEpochSeconds)}: ${next.second}."
        }
        return text
    }

    /** A saved choice, or "" when there is none or it is no longer a real zone. */
    fun loadChoice(raw: String?): String {
        val text = raw?.trim().orEmpty()
        return if (isKnownZone(text)) text else ""
    }
}
