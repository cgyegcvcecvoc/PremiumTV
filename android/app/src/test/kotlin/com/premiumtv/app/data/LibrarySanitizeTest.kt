package com.premiumtv.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertSame
import org.junit.Test

/**
 * Row identity for the lazy lists (1.1.17).
 *
 * Compose throws when a lazy layout is given two identical keys, so the data
 * boundary has to guarantee uniqueness: a refreshed library is whatever
 * upstream published, and upstream is not obliged to publish unique rows.
 */
class LibrarySanitizeTest {

    private fun channel(id: String, name: String, url: String, group: String = "News") =
        Channel(id, name, "", group, "", "", url, "", "", "")

    private fun group(name: String, count: Int) = CategoryGroup(name, count)

    @Test
    fun aRepeatedChannelRowIsDropped() {
        val a = channel("a.us", "A", "https://e/a.m3u8")
        val duplicate = a.copy()
        val b = channel("b.us", "B", "https://e/b.m3u8")
        val deduped = dedupeChannels(listOf(a, duplicate, b))
        assertEquals(listOf(a, b), deduped)
    }

    @Test
    fun twoFeedsOfOneChannelSurvive() {
        // Same EPG id, different URL: these are a channel and its backup, not a
        // duplicate row, and dropping one would lose a fallback feed.
        val main = channel("c.us", "C (1080p)", "https://e/c1.m3u8")
        val backup = channel("c.us", "C (Backup 1)", "https://e/c2.m3u8")
        assertEquals(listOf(main, backup), dedupeChannels(listOf(main, backup)))
    }

    @Test
    fun anAlreadyUniqueLibraryIsReturnedUnchanged() {
        val channels = listOf(channel("a.us", "A", "https://e/a.m3u8"), channel("b.us", "B", "https://e/b.m3u8"))
        assertSame(channels, dedupeChannels(channels))
        val groups = listOf(group("News", 2), group("Sports", 3))
        assertSame(groups, dedupeGroups(groups))
    }

    @Test
    fun everyRowKeyIsUniqueAfterDeduplication() {
        val channels = listOf(
            channel("a.us", "A", "https://e/a.m3u8"),
            channel("a.us", "A", "https://e/a.m3u8"),
            channel("a.us", "A (Backup 1)", "https://e/a2.m3u8"),
            channel("", "No id", "https://e/none.m3u8"),
        )
        val keys = dedupeChannels(channels).map { channelRowKey(it) }
        assertEquals(keys.size, keys.toSet().size)
        assertEquals("a.us|https://e/a.m3u8", keys.first())
    }

    @Test
    fun aRepeatedGroupNameKeepsItsFirstRow() {
        val first = group("News", 3)
        val second = group("News", 9)
        val sports = group("Sports", 1)
        assertEquals(listOf(first, sports), dedupeGroups(listOf(first, second, sports)))
    }

    @Test
    fun shortListsAreNotAllocatedFor() {
        val one = listOf(channel("a.us", "A", "https://e/a.m3u8"))
        assertSame(one, dedupeChannels(one))
        assertSame(emptyList<Channel>(), dedupeChannels(emptyList()))
        assertSame(emptyList<CategoryGroup>(), dedupeGroups(emptyList()))
    }
}
