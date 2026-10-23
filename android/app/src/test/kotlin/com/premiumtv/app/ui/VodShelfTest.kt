package com.premiumtv.app.ui

import org.json.JSONArray
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

/** The Movies & Shows catalogue: parsing, labels and the player's input. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [28])
class VodShelfTest {

    private fun item(
        id: String,
        title: String,
        kind: String = "movie",
        show: String = "",
        season: Int = 0,
        episode: Int = 0,
        year: Int = 0,
        genre: String = "",
        runtime: Int = 0,
        stream: String = "https://archive.org/download/x/$id.mp4",
    ): JSONObject = JSONObject()
        .put("id", id)
        .put("title", title)
        .put("kind", kind)
        .put("show", show)
        .put("season", season)
        .put("episode", episode)
        .put("year", year)
        .put("genre", genre)
        .put("runtime_seconds", runtime)
        .put("summary", "A test entry.")
        .put("stream", stream)
        .put("poster", "https://archive.org/services/img/$id")
        .put("license", "https://creativecommons.org/publicdomain/mark/1.0/")

    private fun catalog(vararg items: JSONObject): String =
        JSONObject().put("schema", 1).put("items", JSONArray(items.toList())).toString()

    @Test
    fun `parses entries and drops ones a player cannot open`() {
        val text = catalog(
            item("vod-a", "A Film"),
            item("vod-b", "No Stream", stream = ""),
            item("", "No Id"),
        )
        val parsed = parseVodCatalog(text)
        assertEquals(1, parsed.size)
        assertEquals("vod-a", parsed[0].id)
    }

    @Test
    fun `blank or malformed catalogues are empty, never invented`() {
        assertTrue(parseVodCatalog(null).isEmpty())
        assertTrue(parseVodCatalog("").isEmpty())
        assertTrue(parseVodCatalog("{not json").isEmpty())
        assertTrue(parseVodCatalog("""{"schema":1}""").isEmpty())
    }

    @Test
    fun `a film becomes a Movies channel with the poster as its logo`() {
        val film = parseVodCatalog(
            catalog(item("vod-film", "Night of the Living Dead", year = 1968, genre = "Horror", runtime = 5796))
        ).single()
        assertEquals("FILM", film.label)
        assertEquals("1968 · Horror · 96 min", film.detail)
        val channel = film.asChannel()
        assertEquals("Night of the Living Dead", channel.name)
        assertEquals("Movies", channel.group)
        assertEquals("https://archive.org/download/x/vod-film.mp4", channel.url)
        assertEquals(film.poster, channel.logo)
    }

    @Test
    fun `an episode names its show and season and plays as one TV Shows entry`() {
        val episode = parseVodCatalog(
            catalog(
                item(
                    "vod-ep", "Jed Buys Stock", kind = "episode", show = "The Beverly Hillbillies",
                    season = 1, episode = 5, year = 1962, runtime = 1508,
                )
            )
        ).single()
        assertEquals("S1 E5", episode.label)
        assertEquals("The Beverly Hillbillies · S1 E5", episode.asChannel().name)
        assertEquals("TV Shows", episode.asChannel().group)
    }

    @Test
    fun `an episode without numbering still labels itself`() {
        val episode = parseVodCatalog(
            catalog(item("vod-ep", "The Big Ham", kind = "episode", show = "Dragnet"))
        ).single()
        assertEquals("EPISODE", episode.label)
        assertEquals("Dragnet · EPISODE", episode.asChannel().name)
    }
}
