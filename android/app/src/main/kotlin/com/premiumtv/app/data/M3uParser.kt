package com.premiumtv.app.data

/**
 * M3U parser used by the in-app updater.
 *
 * It mirrors android/tools/build_bundle.py exactly, so a playlist refreshed
 * over the network produces the same channel records the APK shipped with:
 * tvg-* attributes, the display name after the first comma outside quotes,
 * and the #EXTVLCOPT / #KODIPROP headers some streams need (referrer, user-agent).
 */
internal object M3uParser {

    private val ATTR = Regex("([\\w-]+)=\"([^\"]*)\"")
    private val TVG_URL = Regex("x-tvg-url=\"([^\"]*)\"")
    private val WHITESPACE_RUN = Regex("\\s{2,}")
    private val NOISE = charArrayOf(' ', '\u2605', '\u2606', '\u2b50', '\u2728', '\u2022', '\u25b6', '-', '\u2013')

    fun parse(text: String): Pair<List<Channel>, String> {
        val channels = ArrayList<Channel>()
        var guideUrl = ""

        var id = ""
        var name = ""
        var logo = ""
        var group = "Other"
        var country = ""
        var chno = ""
        var ua = ""
        var referrer = ""
        var origin = ""
        var pending = false

        var optReferrer = ""
        var optUa = ""
        var optOrigin = ""

        for (rawLine in text.lineSequence()) {
            val line = rawLine.trim()
            if (line.isEmpty()) continue

            if (line.startsWith("#EXTM3U")) {
                val found = TVG_URL.find(line)
                if (found != null) {
                    guideUrl = found.groupValues[1].split(",").firstOrNull()?.trim().orEmpty()
                }
                continue
            }

            if (line.startsWith("#EXTINF")) {
                optReferrer = ""
                optUa = ""
                optOrigin = ""
                val attrs = attributes(line)
                id = attrs["tvg-id"].orEmpty().trim()
                logo = attrs["tvg-logo"].orEmpty().trim()
                group = attrs["group-title"].orEmpty().trim().ifBlank { "Other" }
                country = attrs["tvg-country"].orEmpty().trim().uppercase()
                chno = attrs["tvg-chno"].orEmpty().trim()
                ua = attrs["http-user-agent"].orEmpty().trim()
                referrer = attrs["http-referrer"].orEmpty().trim()
                name = extinfName(line, attrs)
                pending = true
                continue
            }

            val option = when {
                line.startsWith("#EXTVLCOPT:") -> line.removePrefix("#EXTVLCOPT:")
                line.startsWith("#KODIPROP:") -> line.removePrefix("#KODIPROP:")
                else -> null
            }
            if (option != null) {
                val split = option.indexOf('=')
                if (split > 0) {
                    val key = option.substring(0, split).trim().lowercase()
                    val value = option.substring(split + 1).trim()
                    when (key) {
                        "http-referrer", "referer" -> optReferrer = value
                        "http-user-agent", "user-agent" -> optUa = value
                        "http-origin", "origin" -> optOrigin = value
                    }
                }
                continue
            }

            if (line.startsWith("#")) continue

            // A URL line: it always closes the entry above it.
            val url = line
            if (!pending) {
                id = ""
                name = cleanName(url.substringAfterLast('/'))
                logo = ""
                group = "Other"
                country = ""
                chno = ""
                ua = ""
                referrer = ""
                origin = ""
            }
            val resolvedId = id.ifBlank { slug(name) }
            channels.add(
                Channel(
                    id = resolvedId,
                    name = cleanName(name).ifBlank { url.substringAfterLast('/') },
                    logo = logo,
                    group = group,
                    country = country,
                    chno = chno,
                    url = url,
                    userAgent = ua.ifBlank { optUa },
                    referrer = referrer.ifBlank { optReferrer },
                    origin = origin.ifBlank { optOrigin },
                )
            )
            pending = false
            optReferrer = ""
            optUa = ""
            optOrigin = ""
            id = ""
            name = ""
            logo = ""
            group = "Other"
            country = ""
            chno = ""
            ua = ""
            referrer = ""
            origin = ""
        }

        return channels to guideUrl
    }

    private fun attributes(line: String): Map<String, String> {
        val out = HashMap<String, String>()
        for (match in ATTR.findAll(line)) {
            out[match.groupValues[1]] = match.groupValues[2]
        }
        return out
    }

    private fun extinfName(line: String, attrs: Map<String, String>): String {
        var quoted = false
        for (index in line.indices) {
            when (line[index]) {
                '"' -> quoted = !quoted
                ',' -> if (!quoted) return line.substring(index + 1).trim()
            }
        }
        return attrs["tvg-name"].orEmpty().trim()
    }

    private fun cleanName(raw: String): String {
        val trimmed = raw.trimStart(*NOISE)
        val collapsed = WHITESPACE_RUN.replace(trimmed, " ")
        return collapsed.ifBlank { raw.trim() }
    }

    private fun slug(value: String): String {
        return value.lowercase()
            .map { ch -> if (ch.isLetterOrDigit()) ch else '.' }
            .joinToString("")
            .trim('.')
    }
}
