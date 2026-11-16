package com.premiumtv.app.ui

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * 1.1.12 "resilient playback": the in-place retry rules that sit in front of
 * the backup-server walk. These are the rules that decide whether a one-second
 * CDN blip costs a viewer their channel, so they are pinned here.
 */
class PlaybackRetryTest {

    @Test
    fun `network and IO errors are treated as transient`() {
        // Media3 PlaybackException codes 2000-2008 are the IO family.
        for (code in 2000..2008) {
            assertEquals(
                "error code $code should be transient",
                PlaybackFault.Transient,
                classifyErrorCode(code),
            )
        }
    }

    @Test
    fun `decoder and renderer errors are treated as media faults`() {
        for (code in 4001..4006) {
            assertEquals(
                "error code $code should be a media fault",
                PlaybackFault.Media,
                classifyErrorCode(code),
            )
        }
    }

    @Test
    fun `bad HTTP status and unsupported formats never retry`() {
        // 2003 is an IO error; permanent ones are the parsing/format/DRM range
        // and the "unspecified" code. Waiting cannot fix these.
        for (code in listOf(1000, 1001, 1002, 3001, 3002, 3003, 3004, 5001, 5002, 5003, 6000, 6001)) {
            assertEquals(
                "error code $code should be permanent",
                PlaybackFault.Permanent,
                classifyErrorCode(code),
            )
        }
    }

    @Test
    fun `a transient fault retries in place twice and then gives up`() {
        val first = decideRetry(PlaybackFault.Transient, alreadyRetried = 0, attemptedServerSwitch = false)
        assertTrue(first.retryInPlace)
        assertTrue(first.notice.isNotBlank())

        val second = decideRetry(PlaybackFault.Transient, alreadyRetried = 1, attemptedServerSwitch = false)
        assertTrue(second.retryInPlace)

        val spent = decideRetry(PlaybackFault.Transient, alreadyRetried = 2, attemptedServerSwitch = false)
        assertFalse("the budget is bounded, not infinite", spent.retryInPlace)
        assertEquals("", spent.notice)
    }

    @Test
    fun `a media fault gets one decoder rebuild, not two`() {
        assertTrue(decideRetry(PlaybackFault.Media, alreadyRetried = 0, attemptedServerSwitch = false).retryInPlace)
        assertFalse(decideRetry(PlaybackFault.Media, alreadyRetried = 1, attemptedServerSwitch = false).retryInPlace)
        assertTrue(
            decideRetry(PlaybackFault.Media, alreadyRetried = 0, attemptedServerSwitch = false)
                .notice.contains("decoder"),
        )
    }

    @Test
    fun `a permanent fault goes straight to the backup server`() {
        val decision = decideRetry(PlaybackFault.Permanent, alreadyRetried = 0, attemptedServerSwitch = false)
        assertFalse(decision.retryInPlace)
        assertEquals("", decision.notice)
    }

    @Test
    fun `after a server switch no further in-place retry is allowed`() {
        // The viewer has already been moved once; piling retries on top would
        // leave them on a spinner instead of the honest error card.
        assertFalse(
            decideRetry(PlaybackFault.Transient, alreadyRetried = 0, attemptedServerSwitch = true).retryInPlace,
        )
        assertFalse(
            decideRetry(PlaybackFault.Media, alreadyRetried = 0, attemptedServerSwitch = true).retryInPlace,
        )
    }

    @Test
    fun `a published origin is reduced to the tuple an Origin header allows`() {
        assertEquals("https://embed.example", originHeaderValue("https://embed.example/watch/123?ad=1"))
        assertEquals("http://embed.example:8080", originHeaderValue("http://embed.example:8080/a/b"))
        assertEquals("https://embed.example", originHeaderValue("  https://embed.example  "))
        assertEquals("", originHeaderValue(""))
        assertEquals("", originHeaderValue("file:///etc/passwd"))
        assertEquals("", originHeaderValue("not a url"))
    }
}
