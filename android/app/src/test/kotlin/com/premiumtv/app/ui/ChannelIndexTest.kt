package com.premiumtv.app.ui

import com.premiumtv.app.data.Channel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertSame
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * The prepared channel index (1.1.17) must answer exactly what the documented
 * rule answers - it is a cache, not a new rule.
 *
 * The library below has every shape the parser produces: one game under two
 * feeds, a channel with a backup, a same-named channel in another country, an
 * id reused by a different show, a feed with no EPG id. For each row the test
 * computes what the rule says from `groupLiveEvents` plus the base display name
 * (an independent expression of it) and compares that with the index, so a
 * drift between the two would fail here instead of silently changing a
 * viewer's backup feed.
 */
class ChannelIndexTest {

    private fun channel(
        id: String,
        name: String,
        url: String,
        group: String = "Sports",
        country: String = "US",
    ) = Channel(id, name, "", group, country, "", url, "", "", "")

    private val library = listOf(
        channel("Football.Dummy.us", "[American Football] Bills vs. Jets | English (STRMCNTR)", "https://edge/event-1.m3u8"),
        channel("Football.Dummy.us", "[American Football] Bills vs. Jets | Spanish", "https://edge/event-2.m3u8"),
        channel("Soccer.Dummy.us", "[Football] Roma vs. Genoa | English", "https://edge/event-3.m3u8"),
        channel("Pluto.TV.Kids.us@East", "Pluto TV Kids (East)", "https://edge/kids-east.m3u8"),
        channel("Pluto.TV.Kids.us@East", "Pluto TV Kids (Backup 1)", "https://edge/kids-backup.m3u8"),
        channel("Pluto.TV.Kids.us@West", "Pluto TV Kids (West)", "https://edge/kids-west.m3u8", country = "GB"),
        channel("Show.Reused.us", "A Show", "https://edge/show-a.m3u8", country = ""),
        channel("Show.Reused.us", "A Show", "https://edge/show-b.m3u8", country = ""),
        channel("", "Unidentified Feed", "https://edge/no-id.m3u8", group = "News"),
        channel("NBC.us@WGAL", "NBC (WGAL)", "https://edge/wgal.m3u8", group = "NBC"),
    )

    /** The documented rule, written out independently of the index. */
    private fun expectedServers(channel: Channel): List<Channel> {
        val games = groupLiveEvents(library).flatMap { section -> section.events }
        val game = games.firstOrNull { event -> event.servers.any { it.url == channel.url } }
        val pool = if (game != null) {
            game.servers
        } else {
            library.filter { candidate ->
                candidate.url != channel.url &&
                    baseDisplayName(candidate.name) == baseDisplayName(channel.name) &&
                    sameChannel(candidate, channel)
            }
        }
        val ordered = mutableListOf(channel)
        for (candidate in pool) {
            if (candidate.url != channel.url && ordered.none { it.url == candidate.url }) ordered += candidate
        }
        return ordered
    }

    private fun sameChannel(candidate: Channel, channel: Channel): Boolean =
        (candidate.id == channel.id && candidate.id.isNotBlank()) ||
            (candidate.country.isNotBlank() && candidate.country == channel.country)

    @Test
    fun theIndexAnswersWhatTheDocumentedRuleAnswers() {
        val index = buildChannelIndex(library)
        for (channel in library) {
            assertEquals(
                "servers for ${channel.name} (${channel.url})",
                expectedServers(channel),
                index.serversFor(channel),
            )
        }
    }

    @Test
    fun theFreeScanStillAnswersTheSameWay() {
        // Callers without an index (and the 1.1.16 tests) keep working: the free
        // function is now the index's answer.
        val index = buildChannelIndex(library)
        for (channel in library) {
            assertEquals(index.serversFor(channel), serversFor(channel, library))
        }
    }

    @Test
    fun anEventFeedFindsTheGamesOtherFeeds() {
        val index = buildChannelIndex(library)
        val english = library[0]
        val spanish = library[1]
        assertNotNull(index.eventFor(english))
        assertEquals(listOf(english, spanish), index.serversFor(english))
        assertEquals(listOf(spanish, english), index.serversFor(spanish))
    }

    @Test
    fun backupsSharingTheEpisodeIdAreServers() {
        val index = buildChannelIndex(library)
        val east = library[3]
        val backup = library[4]
        assertEquals(listOf(east, backup), index.serversFor(east))
        assertEquals(listOf(backup, east), index.serversFor(backup))
    }

    @Test
    fun theSameNameInAnotherCountryIsNotABackup() {
        val index = buildChannelIndex(library)
        val west = library[5]
        assertEquals(listOf(west), index.serversFor(west))
    }

    @Test
    fun aReusedIdOnANamelessCountryKeepsBothFeeds() {
        val index = buildChannelIndex(library)
        val showA = library[6]
        val showB = library[7]
        assertEquals(listOf(showA, showB), index.serversFor(showA))
        assertEquals(listOf(showB, showA), index.serversFor(showB))
    }

    @Test
    fun aFeedWithoutAnIdStillGetsOnlyItself() {
        val index = buildChannelIndex(library)
        val anonymous = library[8]
        assertNull(index.eventFor(anonymous))
        assertEquals(listOf(anonymous), index.serversFor(anonymous))
    }

    @Test
    fun theUrlIndexAndTheSectionsDescribeTheSameGames() {
        val index = buildChannelIndex(library)
        val feeds = index.sections.sumOf { section -> section.events.sumOf { it.servers.size } }
        assertEquals(feeds, index.byUrl.size)
        for (section in index.sections) {
            for (event in section.events) {
                for (server in event.servers) {
                    assertSame(event, index.byUrl[server.url])
                }
            }
        }
    }

    @Test
    fun theBundledScheduleReachesTheSections() {
        val schedule = mapOf("soccer|genoa|roma" to 1_795_000_000L)
        val index = buildChannelIndex(library, schedule)
        val soccer = index.sections.firstOrNull { it.sport == "Soccer" }
        assertNotNull(soccer)
        assertTrue(soccer!!.events.isNotEmpty())
        assertTrue(soccer.events.all { it.kickoffUtc == 1_795_000_000L })
    }

    @Test
    fun anEmptyLibraryIndexesToNothingInsteadOfThrowing() {
        val index = buildChannelIndex(emptyList())
        assertTrue(index.sections.isEmpty())
        assertTrue(index.byUrl.isEmpty())
        val lonely = channel("a.us", "A", "https://edge/a.m3u8")
        assertEquals(listOf(lonely), index.serversFor(lonely))
        assertTrue(ChannelIndex.EMPTY.sections.isEmpty())
        assertTrue(ChannelIndex.EMPTY.byUrl.isEmpty())
    }
}
