package com.premiumtv.app.ui

import com.premiumtv.app.data.Channel
import org.json.JSONObject

/**
 * The on-demand catalogue the bundle ships as `bundle/vod-catalog.json`.
 *
 * `scripts/vod_catalog.py` resolves a curated set of public-domain films and
 * classic TV episodes from the Internet Archive, verifies each direct stream,
 * and publishes one document that `android/tools/build_bundle.py` bundles. An
 * entry plays exactly like a channel — [VodItem.asChannel] turns it into the
 * same Channel the player already understands — so Recently watched and the
 * dead-feed memory work without a second player or a parallel path.
 */
data class VodItem(
    val id: String,
    val title: String,
    val kind: String,
    val show: String,
    val season: Int,
    val episode: Int,
    val year: Int,
    val genre: String,
    val runtimeSeconds: Int,
    val summary: String,
    val stream: String,
    val poster: String,
    val license: String,
    val streams: List<String> = listOf(stream),
) {
    val isMovie: Boolean get() = kind == "movie"

    /** "Movie" or "S1 E5" — what the card says above the title. */
    val label: String
        get() = when {
            isMovie -> "FILM"
            season > 0 && episode > 0 -> "S${season} E${episode}"
            season > 0 -> "S$season"
            else -> "EPISODE"
        }

    /** "1968 · Horror · 97 min", dropping whatever the item does not have. */
    val detail: String
        get() = listOfNotNull(
            year.takeIf { it > 0 }?.toString(),
            genre.takeIf { it.isNotBlank() },
            runtimeSeconds.takeIf { it > 0 }?.let { "${it / 60} min" },
        ).joinToString(" · ")

    /** The player's input: primary direct stream, same shape as a channel. */
    fun asChannel(): Channel = asChannelForUrl(stream)

    /** Every direct derivative published for this title, primary first, for automatic fallback. */
    fun asChannels(): List<Channel> {
        val urls = streams.filter { it.isNotBlank() }.distinct().ifEmpty { listOf(stream) }
        return urls.map { asChannelForUrl(it) }
    }

    private fun asChannelForUrl(targetUrl: String): Channel = Channel(
        id = id,
        name = if (isMovie) title else "$show · $label",
        logo = poster,
        group = if (isMovie) "Movies" else "TV Shows",
        country = "US",
        chno = "",
        url = targetUrl,
        userAgent = "",
        referrer = "",
        origin = "",
    )
}

/** The bundled catalogue: its titles and whether the shelf is paused. */
data class VodCatalog(val items: List<VodItem>, val comingSoon: Boolean)

/** Parses the bundled catalogue; unusable entries are dropped, never faked. */
internal fun parseVodCatalogDocument(text: String?): VodCatalog {
    if (text.isNullOrBlank()) return VodCatalog(emptyList(), false)
    return try {
        val root = JSONObject(text)
        val comingSoon = root.optString("status") == "coming_soon"
        val array = root.optJSONArray("items") ?: return VodCatalog(emptyList(), comingSoon)
        val items = buildList {
            for (index in 0 until array.length()) {
                val item = array.optJSONObject(index) ?: continue
                val stream = item.optString("stream")
                val title = item.optString("title")
                val id = item.optString("id")
                if (stream.isBlank() || title.isBlank() || id.isBlank()) continue
                val rawStreams = item.optJSONArray("streams")
                val parsedStreams = buildList {
                    add(stream)
                    if (rawStreams != null) {
                        for (sIdx in 0 until rawStreams.length()) {
                            val candidate = rawStreams.optString(sIdx)
                            if (candidate.isNotBlank() && candidate !in this) add(candidate)
                        }
                    }
                }
                add(
                    VodItem(
                        id = id,
                        title = title,
                        kind = item.optString("kind", "movie"),
                        show = item.optString("show"),
                        season = item.optInt("season"),
                        episode = item.optInt("episode"),
                        year = item.optInt("year"),
                        genre = item.optString("genre"),
                        runtimeSeconds = item.optInt("runtime_seconds"),
                        summary = item.optString("summary"),
                        stream = stream,
                        poster = item.optString("poster"),
                        license = item.optString("license"),
                        streams = parsedStreams,
                    )
                )
            }
        }
        // A catalogue document that lists one title twice keeps its first
        // entry only: the list is played, resumed and counted by id.
        val unique = if (items.size < 2) {
            items
        } else {
            val seen = HashSet<String>(items.size * 2)
            items.filter { item -> seen.add(item.id) }
        }
        VodCatalog(unique, comingSoon)
    } catch (_: Exception) {
        VodCatalog(emptyList(), false)
    }
}

internal fun parseVodCatalog(text: String?): List<VodItem> = parseVodCatalogDocument(text).items
