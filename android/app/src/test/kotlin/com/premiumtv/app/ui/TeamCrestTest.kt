package com.premiumtv.app.ui

import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/** The 1.0.8 Live Events additions: team names and the drawn team badges. */
class TeamCrestTest {

    @Test fun teamsOfSplitsTheMatchup() {
        assertEquals("Arsenal" to "Chelsea", teamsOf("Arsenal vs. Chelsea"))
        assertEquals("Ball State Cardinals" to "Bowling Green Falcons", teamsOf("Ball State Cardinals vs. Bowling Green Falcons"))
    }

    @Test fun teamsOfHandlesTheDotlessVersusToo() {
        assertEquals("Roma" to "Genoa", teamsOf("Roma vs Genoa"))
    }

    @Test fun teamsOfRejectsTitlesWithoutTwoTeams() {
        assertNull(teamsOf("Pregame Show"))
        assertNull(teamsOf(" vs. "))
    }

    @Test fun initialsComeFromTheFirstTwoWords() {
        assertEquals("BS", teamInitials("Ball State Cardinals"))
        assertEquals("AR", teamInitials("Arsenal"))
        assertEquals("AS", teamInitials("AS Roma"))
        assertEquals("?", teamInitials("   "))
    }

    @Test fun theSameTeamAlwaysGetsTheSameColors() {
        val first = teamColors("Boston Bruins")
        val second = teamColors("Boston Bruins")
        assertEquals(first, second)
        assertNotEquals(first, teamColors("Montreal Canadiens"))
    }

    @Test fun teamHueStaysOnTheColorWheel() {
        for (name in listOf("Roma", "Genoa", "Ball State", "", "Ø federally weird ñ name")) {
            val hue = teamHue(name)
            assertTrue("hue for $name out of range: $hue", hue >= 0f && hue < 360f)
        }
    }

    @Test fun differentTeamsGetDifferentInitialsMostOfTheTime() {
        assertFalse(teamInitials("Arsenal FC") == teamInitials("Chelsea FC"))
        assertTrue(teamInitials("Arsenal FC").length == 2)
    }
}
