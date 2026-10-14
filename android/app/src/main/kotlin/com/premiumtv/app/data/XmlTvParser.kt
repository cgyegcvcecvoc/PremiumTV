package com.premiumtv.app.data

import android.util.Xml
import org.xmlpull.v1.XmlPullParser
import java.io.StringReader
import java.util.Calendar
import java.util.TimeZone

/**
 * XMLTV parser used by the in-app updater.
 *
 * Streams the document with the platform XmlPullParser instead of building a
 * DOM: a full guide is ~10 MB of XML and a TV device would not thank us for
 * holding that in memory alongside a video decoder.
 */
internal object XmlTvParser {

    fun parse(text: String): List<Programme> {
        val out = ArrayList<Programme>()
        val parser = Xml.newPullParser()
        parser.setFeature(XmlPullParser.FEATURE_PROCESS_NAMESPACES, false)
        parser.setInput(StringReader(text))
        var event = parser.eventType
        while (event != XmlPullParser.END_DOCUMENT) {
            if (event == XmlPullParser.START_TAG && parser.name == "programme") {
                val programme = readProgramme(parser)
                if (programme != null) out.add(programme)
            }
            event = parser.next()
        }
        return out.sortedWith(compareBy({ it.channelId }, { it.start }))
    }

    private fun readProgramme(parser: XmlPullParser): Programme? {
        val channelId = parser.getAttributeValue(null, "channel")?.trim().orEmpty()
        val start = parseTime(parser.getAttributeValue(null, "start"))
        if (channelId.isEmpty() || start == 0L) {
            skipToEnd(parser, "programme")
            return null
        }
        var end = parseTime(parser.getAttributeValue(null, "stop"))
        if (end <= start) end = start + 1800L

        var title = ""
        var desc = ""
        var episode = ""
        var icon = ""
        val categories = ArrayList<String>()

        var event = parser.next()
        while (event != XmlPullParser.END_DOCUMENT &&
            !(event == XmlPullParser.END_TAG && parser.name == "programme")
        ) {
            if (event == XmlPullParser.START_TAG) {
                when (parser.name) {
                    "title" -> title = readText(parser)
                    "desc" -> desc = readText(parser)
                    "sub-title" -> episode = readText(parser)
                    "category" -> {
                        val value = readText(parser)
                        if (value.isNotEmpty() && !categories.contains(value)) categories.add(value)
                    }
                    "icon" -> {
                        val src = parser.getAttributeValue(null, "src").orEmpty()
                        if (src.isNotEmpty()) icon = src
                        parser.next()
                    }
                    else -> parser.next()
                }
            }
            event = parser.next()
        }

        return Programme(
            channelId = channelId,
            start = start,
            end = end,
            title = title.ifBlank { "(no title)" },
            desc = desc,
            category = categories.joinToString("; "),
            icon = icon,
            episode = episode,
        )
    }

    private fun skipToEnd(parser: XmlPullParser, tag: String) {
        var event = parser.eventType
        while (event != XmlPullParser.END_DOCUMENT &&
            !(event == XmlPullParser.END_TAG && parser.name == tag)
        ) {
            event = parser.next()
        }
    }

    /** Reads the text of a simple element and consumes its end tag. */
    private fun readText(parser: XmlPullParser): String {
        val event = parser.next()
        if (event == XmlPullParser.TEXT) {
            val value = (parser.text ?: "").trim()
            parser.next()
            return collapse(value)
        }
        return ""
    }

    private fun collapse(value: String): String = value.replace(Regex("\\s+"), " ")

    /**
     * XMLTV timestamps look like `20261011043000 +0000`. They are converted to
     * epoch seconds in UTC so the app can compare them with the device clock.
     */
    private fun parseTime(raw: String?): Long {
        val value = raw?.trim().orEmpty()
        val match = Regex("^(\\d{14})(?:\\s*([+-])(\\d{2})(\\d{2}))?$").matchEntire(value)
            ?: return 0L
        val stamp = match.groupValues[1]
        val signText = match.groupValues[2]
        val year = stamp.substring(0, 4).toIntOrNull() ?: return 0L
        if (year < 1) return 0L
        val offsetHours = match.groupValues[3].toIntOrNull() ?: 0
        val offsetMinutes = match.groupValues[4].toIntOrNull() ?: 0
        if (offsetHours > 23 || offsetMinutes > 59) return 0L

        return try {
            val calendar = Calendar.getInstance(TimeZone.getTimeZone("UTC"))
            calendar.isLenient = false
            calendar.clear()
            calendar.set(
                stamp.substring(0, 4).toInt(),
                stamp.substring(4, 6).toInt() - 1,
                stamp.substring(6, 8).toInt(),
                stamp.substring(8, 10).toInt(),
                stamp.substring(10, 12).toInt(),
                stamp.substring(12, 14).toInt(),
            )
            var epoch = calendar.timeInMillis / 1000L
            if (signText.isNotEmpty()) {
                val sign = if (signText == "-") -1L else 1L
                epoch -= sign * (offsetHours * 3600L + offsetMinutes * 60L)
            }
            epoch
        } catch (ignored: Exception) {
            0L
        }
    }
}
