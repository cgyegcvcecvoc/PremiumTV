package com.premiumtv.app.ui

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/** 1.1.0: the automatic server-backup walk, tested without a player. */
class ServerFallbackTest {

    @Test
    fun `automatic backup walks forward and stops at the last server`() {
        assertEquals(1, autoNextServerIndex(0, 3))
        assertEquals(2, autoNextServerIndex(1, 3))
        assertNull(autoNextServerIndex(2, 3))
        assertNull(autoNextServerIndex(0, 1))
        assertNull(autoNextServerIndex(0, 0))
    }

    @Test
    fun `backup availability is honest about a single-feed channel`() {
        assertTrue(hasBackupServer(0, 2))
        assertFalse(hasBackupServer(0, 1))
        assertFalse(hasBackupServer(2, 3))
    }

    @Test
    fun `switch notices name the server the viewer is landing on`() {
        val failed = serverSwitchNotice(ServerSwitchReason.Failed, 1, 3)
        val stalled = serverSwitchNotice(ServerSwitchReason.Stalled, 1, 3)
        val manual = serverSwitchNotice(ServerSwitchReason.Manual, 2, 3)

        assertTrue(failed.contains("switching to server 2 of 3"))
        assertTrue(stalled.contains("switching to server 2 of 3"))
        assertEquals("Server 3 of 3 · selected by you", manual)
    }

    @Test
    fun `status line advertises the backup only when one exists`() {
        assertEquals("Server 1 of 2 · automatic backup on", serverStatusLine(0, 2, true))
        assertEquals("Server 1 of 1", serverStatusLine(0, 1, false))
    }

    @Test
    fun `an exhausted walk explains itself without inventing servers`() {
        assertEquals(
            "All 3 servers for this channel were tried.",
            exhaustedServerMessage(3),
        )
        assertEquals(
            "This channel has only one feed, and it is not answering.",
            exhaustedServerMessage(1),
        )
    }
}
