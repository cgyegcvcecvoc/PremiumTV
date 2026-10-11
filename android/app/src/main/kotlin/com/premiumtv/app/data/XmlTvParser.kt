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
        if (value.length < 14) return 0L
        return try {
            val calendar = Calendar.getInstance(TimeZone.getTimeZone("UTC"))
            calendar.clear()
            calendar.set(
                value.substring(0, 4).toInt(),
                value.substring(4, 6).toInt() - 1,
                value.substring(6, 8).toInt(),
                value.substring(8, 10).toInt(),
                value.substring(10, 12).toInt(),
                value.substring(12, 14).toInt(),
            )
            var epoch = calendar.timeInMillis / 1000L
            val offset = value.substring(14).trim()
            if (offset.length >= 5 && (offset[0] == '+' || offset[0] == '-')) {
                val sign = if (offset[0] == '-') -1L else 1L
                val hours = offset.substring(1, 3).toLongOrNull() ?: 0L
                val minutes = offset.substring(3, 5).toLongOrNull() ?: 0L
                epoch -= sign * (hours * 3600L + minutes * 60L)
            }
            epoch
        } catch (ignored: Exception) {
            0L
        }
    }
}
