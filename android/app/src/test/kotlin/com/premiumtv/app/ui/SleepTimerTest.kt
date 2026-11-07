package com.premiumtv.app.ui

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/** The 1.1.5 sleep timer's user-facing label, independent of Android. */
class SleepTimerTest {

    @Test
    fun `the label rounds up so a running timer never reads zero`() {
        assertEquals("under a minute", sleepTimerLabel(1L))
        assertEquals("under a minute", sleepTimerLabel(59_999L))
        assertEquals("1 min", sleepTimerLabel(60_000L))
        assertEquals("30 min", sleepTimerLabel(30L * 60_000L))
    }

    @Test
    fun `hours are spelled out and exact hours lose the minute part`() {
        assertEquals("1 hr", sleepTimerLabel(60L * 60_000L))
        assertEquals("1 hr 30 min", sleepTimerLabel(90L * 60_000L))
        assertEquals("2 hr", sleepTimerLabel(120L * 60_000L))
    }

    @Test
    fun `a deadline in the past is off`() {
        assertEquals("Off", sleepTimerLabel(0L))
        assertEquals("Off", sleepTimerLabel(-1_000L))
    }

    @Test
    fun `settings offers off plus three useful durations`() {
        assertEquals(listOf(0, 30, 60, 90), SLEEP_TIMER_CHOICES)
        assertTrue(0 in SLEEP_TIMER_CHOICES)
    }
}
