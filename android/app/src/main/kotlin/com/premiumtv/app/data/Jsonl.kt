package com.premiumtv.app.data

import android.util.JsonReader
import java.io.BufferedReader
import java.io.InputStream
import java.io.InputStreamReader
import java.io.StringReader
import java.nio.charset.StandardCharsets

/**
 * Reads a JSON Lines file (one JSON object per line).
 *
 * The bundle is 2,217 channels and roughly 10,000 programmes, so it is streamed
 * one line at a time instead of being parsed into one giant JSONObject: a TV
 * stick has far less heap than a desktop and org.json holds every value twice.
 *
 * Each line gets its own [JsonReader]. Looping `while (reader.hasNext())` over
 * the whole file does not work: android.util.JsonReader.hasNext() is true at the
 * end of the document too (it only reports END_OBJECT / END_ARRAY as "no more"),
 * so the loop called beginObject() on END_DOCUMENT and threw on the last line.
 * That exception made every bundled load fail, and the app showed its
 * "bundled data is missing" message even though the data was in the APK.
 */
internal fun <T> readJsonLines(input: InputStream, parse: (JsonReader) -> T): List<T> {
    val out = ArrayList<T>()
    BufferedReader(InputStreamReader(input, StandardCharsets.UTF_8)).use { lines ->
        while (true) {
            val line = lines.readLine() ?: break
            if (line.isBlank()) continue
            JsonReader(StringReader(line)).use { json ->
                json.isLenient = true
                out.add(parse(json))
            }
        }
    }
    return out
}

/** Reads a string field, tolerating a null or a number where a string was expected. */
internal fun JsonReader.nextStringOrEmpty(): String {
    return try {
        nextString()
    } catch (ignored: Exception) {
        try {
            skipValue()
        } catch (ignored2: Exception) {
            // Nothing further to skip; the caller moves on to the next object.
        }
        ""
    }
}

internal fun JsonReader.nextLongOrZero(): Long {
    return try {
        nextLong()
    } catch (ignored: Exception) {
        try {
            skipValue()
        } catch (ignored2: Exception) {
            // As above.
        }
        0L
    }
}

internal fun JsonReader.nextIntOrZero(): Int {
    return try {
        nextInt()
    } catch (ignored: Exception) {
        try {
            skipValue()
        } catch (ignored2: Exception) {
            // As above.
        }
        0
    }
}

internal fun parseChannel(reader: JsonReader): Channel {
    var id = ""
    var name = ""
    var logo = ""
    var group = "Other"
    var country = ""
    var chno = ""
    var url = ""
    var ua = ""
    var referrer = ""
    var origin = ""
    reader.beginObject()
    while (reader.hasNext()) {
        when (reader.nextName()) {
            "id" -> id = reader.nextStringOrEmpty()
            "name" -> name = reader.nextStringOrEmpty()
            "logo" -> logo = reader.nextStringOrEmpty()
            "group" -> group = reader.nextStringOrEmpty()
            "country" -> country = reader.nextStringOrEmpty()
            "chno" -> chno = reader.nextStringOrEmpty()
            "url" -> url = reader.nextStringOrEmpty()
            "ua" -> ua = reader.nextStringOrEmpty()
            "referrer" -> referrer = reader.nextStringOrEmpty()
            "origin" -> origin = reader.nextStringOrEmpty()
            else -> reader.skipValue()
        }
    }
    reader.endObject()
    return Channel(
        id = id,
        name = name.ifBlank { url },
        logo = logo,
        group = group.ifBlank { "Other" },
        country = country,
        chno = chno,
        url = url,
        userAgent = ua,
        referrer = referrer,
        origin = origin,
    )
}

internal fun parseGroup(reader: JsonReader): CategoryGroup {
    var name = "Other"
    var count = 0
    reader.beginObject()
    while (reader.hasNext()) {
        when (reader.nextName()) {
            "name" -> name = reader.nextStringOrEmpty()
            "count" -> count = reader.nextIntOrZero()
            else -> reader.skipValue()
        }
    }
    reader.endObject()
    return CategoryGroup(name = name.ifBlank { "Other" }, count = count)
}

internal fun parseProgramme(reader: JsonReader): Programme {
    var channelId = ""
    var start = 0L
    var end = 0L
    var title = ""
    var desc = ""
    var category = ""
    var icon = ""
    var episode = ""
    reader.beginObject()
    while (reader.hasNext()) {
        when (reader.nextName()) {
            "c" -> channelId = reader.nextStringOrEmpty()
            "s" -> start = reader.nextLongOrZero()
            "e" -> end = reader.nextLongOrZero()
            "t" -> title = reader.nextStringOrEmpty()
            "d" -> desc = reader.nextStringOrEmpty()
            "g" -> category = reader.nextStringOrEmpty()
            "i" -> icon = reader.nextStringOrEmpty()
            "ep" -> episode = reader.nextStringOrEmpty()
            else -> reader.skipValue()
        }
    }
    reader.endObject()
    if (end <= start) end = start + 1800L
    return Programme(
        channelId = channelId,
        start = start,
        end = end,
        title = title.ifBlank { "(no title)" },
        desc = desc,
        category = category,
        icon = icon,
        episode = episode,
    )
}
