package com.premiumtv.app.data

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * The Live Events clock: which zone a kickoff is read in, and how it is said.
 *
 * The rule under test is the one a viewer feels: the clock above the cards and
 * the time on each card are always the same zone, an unknown saved zone falls
 * back to the device instead of crashing, and the zones offered follow the
 * market the viewer already saved.
 */
class LiveClockTest {

    @Test
    fun aKnownZoneIsAcceptedAndAnUnknownOneNeverWins() {
        assertTrue(LiveClock.isKnownZone("America/New_York"))
        assertTrue(LiveClock.isKnownZone("UTC"))
        assertFalse(LiveClock.isKnownZone("Mars/Olympus_Mons"))
        assertFalse(LiveClock.isKnownZone(""))
        assertFalse(LiveClock.isKnownZone(null))
        // A stale name saved by an older build resolves to the device's own.
        assertEquals("Europe/Berlin", LiveClock.resolveZone("Mars/Olympus_Mons", "Europe/Berlin"))
        assertEquals("America/Chicago", LiveClock.resolveZone("America/Chicago", "Europe/Berlin"))
        assertEquals("", LiveClock.resolveZone("Mars/Olympus_Mons", "Mars/Olympus_Mons"))
    }

    @Test
    fun theLabelIsTheCityNotThePath() {
        assertEquals("New York", LiveClock.zoneLabel("America/New_York"))
        assertEquals("Buenos Aires", LiveClock.zoneLabel("America/Argentina/Buenos_Aires"))
        assertEquals("UTC", LiveClock.zoneLabel("UTC"))
        assertEquals("Device time", LiveClock.zoneLabel(""))
    }

    @Test
    fun theBandFollowsTheLongitudeAndWrapsCleanly() {
        assertEquals("americas", LiveClock.bandForLongitude(-76.3)?.id)   // Pennsylvania
        assertEquals("atlantic", LiveClock.bandForLongitude(-0.1)?.id)    // London
        assertEquals("east", LiveClock.bandForLongitude(77.2)?.id)        // Delhi
        assertEquals("pacific", LiveClock.bandForLongitude(151.2)?.id)    // Sydney
        assertNull(LiveClock.bandForLongitude(null))
        assertNull(LiveClock.bandForLongitude(Double.NaN))
        // 190 is 170 degrees west: the same band as -170, not "beyond the end".
        assertEquals(LiveClock.bandForLongitude(-170.0)?.id, LiveClock.bandForLongitude(190.0)?.id)
    }

    @Test
    fun theZonesOfferedLeadWithTheDeviceThenTheMarket() {
        val zones = LiveClock.suggestZones("Europe/Berlin", -76.3).map { it.zone }
        assertEquals("Europe/Berlin", zones.first())
        assertTrue(zones.contains("UTC"))
        // The saved market is in Pennsylvania, so its zone is offered next.
        assertTrue(zones.contains("America/New_York"))
        assertEquals(zones.size, zones.toSet().size)
    }

    @Test
    fun withoutALocationTheClockStillOffersZones() {
        val zones = LiveClock.suggestZones("America/Los_Angeles", null).map { it.zone }
        assertEquals("America/Los_Angeles", zones.first())
        assertTrue(zones.size >= 3)
        assertTrue(LiveClock.suggestZones(null, null).isNotEmpty())
    }

    @Test
    fun theOffsetAndTheDeltaAreReadFromTheZoneItself() {
        // 2026-11-23 20:00 UTC (1795464000): New York is EST (GMT-5), Berlin GMT+1.
        val at = 1_795_464_000_000L
        assertEquals("GMT-5", LiveClock.offsetLabel(at, "America/New_York"))
        assertEquals("GMT+1", LiveClock.offsetLabel(at, "Europe/Berlin"))
        assertEquals("-6 h", LiveClock.deltaLabel(at, "America/New_York", "Europe/Berlin"))
        assertEquals("+6 h", LiveClock.deltaLabel(at, "Europe/Berlin", "America/New_York"))
        assertEquals("", LiveClock.deltaLabel(at, "Europe/Berlin", "Europe/Berlin"))
        // Half-hour zones keep their minutes.
        assertEquals("GMT+5:30", LiveClock.offsetLabel(at, "Asia/Kolkata"))
    }

    @Test
    fun aKickoffIsSaidInTheClockZoneItIsReadIn() {
        val at = 1_795_464_000_000L
        assertEquals("3:00 PM", LiveClock.kickoffText(at, "America/New_York"))
        assertEquals("9:00 PM", LiveClock.kickoffText(at, "Europe/Berlin"))
        assertTrue(LiveClock.kickoffStamp(at, "Europe/Berlin").endsWith("GMT+1"))
        assertTrue(LiveClock.clockLine(at, "America/New_York").contains("New York · GMT-5"))
    }

    @Test
    fun theNextKickoffSkipsWhateverHasAlreadyStarted() {
        val now = 1_795_464_000L
        val events = listOf<Pair<Long?, String>>(
            now - 600L to "Started already",
            null to "No known kickoff",
            now + 3600L to "Later",
            now + 1200L to "Sooner",
        )
        assertEquals(now + 1200L to "Sooner", LiveClock.nextKickoff(events, now))
        assertNull(LiveClock.nextKickoff(events.take(2), now))
    }

    @Test
    fun theSummaryNamesTheClockAndTheNextKickoff() {
        val now = 1_795_464_000L
        val device = "Europe/Berlin"
        val own = LiveClock.summary(now, "", device, emptyList())
        assertTrue(own.startsWith("Kickoff times are read in your clock, Berlin"))
        val away = LiveClock.summary(now, "America/New_York", device, emptyList())
        assertTrue(away.contains("not this device"))
        val withGame = LiveClock.summary(now, "America/New_York", device,
            listOf(now + 3600L to "Arsenal vs. Chelsea"))
        assertTrue(withGame.contains("Next kickoff in 1:00:00: Arsenal vs. Chelsea."))
    }

    @Test
    fun aCountdownUsesTheSameShapeAsTheLiveEventsTab() {
        assertEquals("09:05", LiveClock.countdownText(545))
        assertEquals("1:00:00", LiveClock.countdownText(3600))
        assertEquals("1d 0:00:00", LiveClock.countdownText(86400))
        assertEquals("00:00", LiveClock.countdownText(-5))
    }

    @Test
    fun aSavedChoiceIsOnlyHonouredWhenItStillNamesAZone() {
        assertEquals("Asia/Tokyo", LiveClock.loadChoice(" Asia/Tokyo "))
        assertEquals("", LiveClock.loadChoice("Mars/Olympus_Mons"))
        assertEquals("", LiveClock.loadChoice(null))
    }
}
