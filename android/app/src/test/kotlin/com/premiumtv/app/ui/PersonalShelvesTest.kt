package com.premiumtv.app.ui

import com.premiumtv.app.data.Channel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class PersonalShelvesTest {
    private fun channel(url: String) = Channel(
        id = url, name = url, url = url, group = "News", country = "US",
        logo = "", chno = "", referrer = "", origin = "", userAgent = "",
    )

    @Test
    fun `opening a channel files it under recents, newest first, capped`() {
        var keys = emptyList<String>()
        keys = recordRecentChannel(keys, "a")
        keys = recordRecentChannel(keys, "b")
        keys = recordRecentChannel(keys, "a")
        assertEquals(listOf("a", "b"), keys)
        repeat(40) { keys = recordRecentChannel(keys, "c$it") }
        assertEquals(MAX_RECENTS, keys.size)
        assertEquals("c39", resolveShelf(keys, listOf(channel("a"), channel("c39"))).first().url)
    }

    @Test
    fun `favorites toggle and shelves drop channels that left the playlist`() {
        var keys = toggleFavoriteChannel(emptyList(), "a")
        keys = toggleFavoriteChannel(keys, "b")
        assertEquals(listOf("b", "a"), keys)
        keys = toggleFavoriteChannel(keys, "a")
        assertEquals(listOf("b"), keys)
        assertEquals(listOf("b"), resolveShelf(keys, listOf(channel("b"))).map { it.url })
        assertTrue(resolveShelf(listOf("gone"), listOf(channel("b"))).isEmpty())
    }

    @Test
    fun `manual server switching wraps in both directions`() {
        assertEquals(1, nextServerIndex(0, 3, 1))
        assertEquals(0, nextServerIndex(2, 3, 1))
        assertEquals(2, nextServerIndex(0, 3, -1))
        assertEquals(0, nextServerIndex(0, 0, 1))
    }
}
