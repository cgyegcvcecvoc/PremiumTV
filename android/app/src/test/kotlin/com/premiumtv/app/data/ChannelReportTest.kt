package com.premiumtv.app.data

import java.net.URLDecoder
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

/** The report form names the channel, the feed and what the player saw. */
class ChannelReportTest {

    private fun decode(value: String): String = URLDecoder.decode(value, "UTF-8")

    @Test
    fun `a report names the channel and the server position`() {
        val url = ChannelReport.issueUrl(
            channelName = "BBC America",
            group = "Entertainment",
            streamUrl = "http://example.test/live/index.m3u8?token=abc",
            serverIndex = 1,
            serverCount = 3,
            error = "HTTP 403 from the media segment",
            appVersion = "PremiumTV Android 1.1.24",
            platform = "Android 14",
            reportedAt = "2026-11-25T00:00:00Z",
        )
        assertTrue(url.startsWith(ChannelReport.ISSUE_URL))
        assertTrue(url.contains("title="))
        assertTrue(url.contains("body="))
        val title = decode(url.substringAfter("title=").substringBefore("&body="))
        assertEquals("[Channel report] BBC America — server 2 of 3 will not play", title)
        val body = decode(url.substringAfter("&body="))
        assertTrue(body.contains("**Channel:** BBC America"))
        assertTrue(body.contains("**Category:** Entertainment"))
        assertTrue(body.contains("example.test/live"))
        assertTrue(body.contains("HTTP 403 from the media segment"))
        assertTrue(body.contains("**App:** PremiumTV Android 1.1.24"))
    }

    @Test
    fun `a report without optional context stays useful and bounded`() {
        val url = ChannelReport.issueUrl(
            channelName = "x".repeat(300),
            streamUrl = "https://example.test/" + "a".repeat(5000),
            error = "bad\u0000news",
            reportedAt = "2026-11-25T00:00:00Z",
        )
        val body = decode(url.substringAfter("&body="))
        assertTrue(body.length < 4300)
        assertTrue(!body.contains("\u0000"))
    }

    @Test
    fun `server positions are bounded and never report zero`() {
        assertEquals("unknown", ChannelReport.serverPosition(0, 0))
        assertEquals("1 of 1", ChannelReport.serverPosition(0, 1))
        assertEquals("1 of 2", ChannelReport.serverPosition(-4, 2))
        assertEquals("2 of 2", ChannelReport.serverPosition(9, 2))
    }
}
