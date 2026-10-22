package com.premiumtv.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/** 1.1.0: dead feeds are filtered, expire, and never hide a live backup. */
class ChannelHealthTest {

    private fun channel(name: String, url: String, id: String = "chan.one") = Channel(
        id = id, name = name, url = url, group = "News", country = "US",
        logo = "", chno = "", referrer = "", origin = "", userAgent = "",
    )

    @Test
    fun `a dead primary feed is hidden but its live backup still shows`() {
        val primary = channel("News One", "https://stream/one.m3u8")
        val backup = channel("News One (Backup 1)", "https://stream/one-backup.m3u8")
        val dead = setOf(primary.url)

        val visible = visibleChannels(listOf(primary, backup), dead)

        assertEquals(listOf(backup.url), visible.map { it.url })
        assertEquals(1, hiddenChannelCount(listOf(primary, backup), dead))
    }

    @Test
    fun `a healthy channel survives an unrelated failure`() {
        val channel = channel("News One", "https://stream/one.m3u8")
        val visible = visibleChannels(listOf(channel), setOf("https://stream/other.m3u8"))
        assertEquals(1, visible.size)
    }

    @Test
    fun `recordings expire so a returning feed gets another chance`() {
        val now = 1_000_000_000_000L
        val entries = listOf(
            DeadFeed("https://stream/old.m3u8", now - DEAD_FEED_TTL_MS - 1),
            DeadFeed("https://stream/recent.m3u8", now - 60_000L),
        )
        assertEquals(setOf("https://stream/recent.m3u8"), deadUrlSet(entries, now))
        assertEquals(1, pruneDeadFeeds(entries, now).size)
    }

    @Test
    fun `healthy servers are tried before the ones already seen failing`() {
        val a = channel("A", "https://stream/a.m3u8")
        val b = channel("B (Backup 1)", "https://stream/b.m3u8")
        val c = channel("C (Backup 2)", "https://stream/c.m3u8")

        val ordered = healthyServersFirst(listOf(a, b, c), setOf(a.url))

        assertEquals(listOf(b.url, c.url, a.url), ordered.map { it.url })
        assertFalse(ordered.first().url in setOf(a.url))
        assertTrue(ordered.last().url in setOf(a.url))
    }

    @Test
    fun `an empty dead set keeps the published server order`() {
        val servers = listOf(
            channel("A", "https://stream/a.m3u8"),
            channel("B (Backup 1)", "https://stream/b.m3u8"),
        )
        assertEquals(servers, healthyServersFirst(servers, emptySet()))
    }
}
