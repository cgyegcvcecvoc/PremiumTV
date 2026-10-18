package com.premiumtv.app.ui

import com.premiumtv.app.data.Channel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Test

/** The live-game parsing and the multi-server grouping, on the plain JVM. */
class LiveEventsTest {

    private fun channel(
        id: String,
        name: String,
        url: String,
        group: String = "Sports",
    ) = Channel(id, name, "", group, "US", "", url, "", "", "")

    @Test fun parsesTheScrapersEventNames() {
        val event = parseLiveEvent(
            channel(
                "Football.Dummy.us",
                "[American Football] Ball State Cardinals vs. Bowling Green Falcons | English (STRMCNTR)",
                "https://edge.example/1.m3u8",
            ),
        )
        assertNotNull(event)
        assertEquals("American Football", event!!.sport)
        assertEquals("Ball State Cardinals vs. Bowling Green Falcons", event.title)
    }

    @Test fun theSoccerPlaceholderIdWinsOverTheFootballTag() {
        // The scraper tags soccer games "[Football]"; only the shared id says
        // which football it means.
        val event = parseLiveEvent(
            channel("Soccer.Dummy.us", "[Football] AS Roma vs. Genoa | English (STRMCNTR)", "https://s.example/2.m3u8"),
        )
        assertEquals("Soccer", event?.sport)
        assertEquals("AS Roma vs. Genoa", event?.title)
    }

    @Test fun collegeHockeyMmaAndLeagueTagsLandInTheirOwnSections() {
        assertEquals(
            "College Football",
            parseLiveEvent(channel("NCAA.Sports.Dummy.us", "[NCAAF] Ohio vs. Michigan | English", "https://c/1"))?.sport,
        )
        assertEquals(
            "NHL Hockey",
            parseLiveEvent(channel("NHL.Hockey.Dummy.us", "[NHL Hockey] Bruins vs. Rangers", "https://c/2"))?.sport,
        )
        assertEquals(
            "Soccer",
            parseLiveEvent(channel("doms9.example_17", "[Liga MX] America vs. Chivas", "https://c/3"))?.sport,
        )
        assertEquals(
            "UFC / MMA",
            parseLiveEvent(channel("doms9.example_18", "[UFC] Volkanovski vs. Lopes", "https://c/4"))?.sport,
        )
    }

    @Test fun ordinaryChannelsAndShowsWithoutAMatchupAreNotEvents() {
        assertNull(parseLiveEvent(channel("news.us", "NBC News Now", "https://n/1")))
        assertNull(parseLiveEvent(channel("Sports.Dummy.us", "[Sports] Pregame Show", "https://n/2")))
        assertNull(parseLiveEvent(channel("movies.us", "Casino (1995)", "https://n/3", group = "Movies")))
    }

    @Test fun gamesGroupIntoSportSectionsWithTheirServers() {
        val channels = listOf(
            channel("Football.Dummy.us", "[American Football] A Cats vs. B Dogs | English (STRMCNTR)", "https://e/1"),
            channel("Soccer.Dummy.us", "[Football] Roma vs. Genoa | English (STRMCNTR)", "https://e/2"),
            channel("Soccer.Dummy.us", "[Football] Roma vs. Genoa | Spanish (STRMCNTR)", "https://e/3"),
            channel("news.us", "Local News", "https://e/4", group = "News"),
        )
        val sections = groupLiveEvents(channels)
        assertEquals(listOf("Soccer", "American Football"), sections.map { it.sport })
        val soccer = sections[0].events.single()
        assertEquals("Roma vs. Genoa", soccer.title)
        assertEquals(listOf("https://e/2", "https://e/3"), soccer.servers.map { it.url })
    }

    @Test fun everyFeedOfAGameFallsBackToItsSiblings() {
        val english = channel("Soccer.Dummy.us", "[Football] Roma vs. Genoa | English (STRMCNTR)", "https://e/2")
        val spanish = channel("Soccer.Dummy.us", "[Football] Roma vs. Genoa | Spanish (STRMCNTR)", "https://e/3")
        val all = listOf(english, spanish, channel("news.us", "News", "https://e/4", group = "News"))
        assertEquals(listOf(english, spanish), serversFor(english, all))
        assertEquals(listOf(spanish, english), serversFor(spanish, all))
    }

    @Test fun backupsOfAChannelBecomeItsServers() {
        val main = channel("JustForLaughs.us@SD", "Just for Laughs Gags (1080p)", "https://j/1", group = "Comedy")
        val backup = channel("JustForLaughs.us@SD", "Just for Laughs Gags (Backup 1)", "https://j/2", group = "Comedy Backups")
        val sameIdOtherShow = channel("JustForLaughs.us@SD", "Comedy Block (720p)", "https://j/3", group = "Comedy")
        val all = listOf(main, backup, sameIdOtherShow)
        assertEquals(listOf(main, backup), serversFor(main, all))
        assertEquals(listOf(backup, main), serversFor(backup, all))
        // Sharing an id is not enough: another show on the id stays out.
        assertEquals(listOf(sameIdOtherShow), serversFor(sameIdOtherShow, all))
    }

    @Test fun theLiveIndexMapsEveryFeedToItsGame() {
        val a = channel("Soccer.Dummy.us", "[Football] Roma vs. Genoa | English (STRMCNTR)", "https://e/2")
        val b = channel("Soccer.Dummy.us", "[Football] Roma vs. Genoa | Spanish (STRMCNTR)", "https://e/3")
        val index = liveEventIndex(listOf(a, b, channel("news.us", "News", "https://e/4", group = "News")))
        assertEquals(2, index.size)
        assertEquals("Roma vs. Genoa", index["https://e/2"]?.title)
        assertEquals("Roma vs. Genoa", index["https://e/3"]?.title)
        assertNull(index["https://e/4"])
    }

    @Test fun baseNamesIgnoreQualityBackupAndCountryTags() {
        assertEquals("pluto tv kids", baseDisplayName("Pluto TV Kids (Spain) (720p)"))
        assertEquals("pluto tv kids", baseDisplayName("Pluto TV Kids (Backup 1)"))
        assertEquals("pluto tv kids", baseDisplayName("Pluto TV Kids"))
    }
}
