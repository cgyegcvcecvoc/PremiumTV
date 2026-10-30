package com.premiumtv.app.ui

import androidx.media3.common.C
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/** 1.1.3: audio track fallback, secondary SAP filtering, and playback clock formatting. */
class AudioTrackSelectionTest {

    @Test
    fun `prefers supported primary audio track over unsupported and SAP tracks`() {
        val tracks = listOf(
            AudioTrackCandidate("Dolby 5.1", "EN", supported = false, selected = false, isSecondary = false),
            AudioTrackCandidate("SAP Spanish", "ES", supported = true, selected = false, isSecondary = true),
            AudioTrackCandidate("Main Stereo", "EN", supported = true, selected = false, isSecondary = false),
        )
        assertEquals(2, selectPreferredAudioTrackIndex(tracks))
    }

    @Test
    fun `falls back to supported secondary track when it is the only supported audio`() {
        val tracks = listOf(
            AudioTrackCandidate("AC-3", "EN", supported = false, selected = false, isSecondary = false),
            AudioTrackCandidate("SAP Audio", "EN", supported = true, selected = false, isSecondary = true),
        )
        assertEquals(1, selectPreferredAudioTrackIndex(tracks))
    }

    @Test
    fun `returns minus one when no audio track is supported`() {
        val tracks = listOf(
            AudioTrackCandidate("DTS", "EN", supported = false, selected = false, isSecondary = false),
        )
        assertEquals(-1, selectPreferredAudioTrackIndex(tracks))
    }

    @Test
    fun `detects secondary SAP and commentary labels and role flags`() {
        assertTrue(isSecondaryAudioLabel("English SAP", 0))
        assertTrue(isSecondaryAudioLabel("Director Commentary", 0))
        assertTrue(isSecondaryAudioLabel("Main", C.ROLE_FLAG_ALTERNATE))
        assertFalse(isSecondaryAudioLabel("Main English", 0))
    }

    @Test
    fun `formats playback clock for short clips and feature films`() {
        assertEquals("0:00", formatPlaybackClock(0L))
        assertEquals("1:05", formatPlaybackClock(65_000L))
        assertEquals("2:07:00", formatPlaybackClock(7_620_000L))
    }
}
