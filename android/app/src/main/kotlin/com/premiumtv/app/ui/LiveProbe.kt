package com.premiumtv.app.ui

import com.premiumtv.app.data.Channel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.net.HttpURLConnection
import java.net.URL

/** Where one live game's feed check stands (1.0.8 Live Events revamp). */
enum class LiveFeedStatus {
    /** No check has finished for this game yet. */
    Checking,

    /** At least one of the game's feeds answered — the game is on air. */
    Answering,

    /** Every feed timed out or refused the connection — nothing is answering. */
    Silent,
}

/**
 * Asks one stream whether its server still answers at all.
 *
 * The Live Events refresh button (and opening the tab) probes each game's
 * feeds until one answers, so the tab can say which games are live and which
 * have gone quiet instead of trusting a scraper snapshot blindly. Any HTTP
 * answer counts — even 403/404, which a geo-blocked or half-closed edge still
 * returns — because the viewer's question is "is anything still answering on
 * this game". Only a timeout or a refused connection means Silent.
 *
 * The Range header keeps a cooperating server from sending a body; a server
 * that ignores it costs a few bytes either way, and the connection is closed
 * without reading.
 */
internal suspend fun feedAnswers(channel: Channel): Boolean = withContext(Dispatchers.IO) {
    try {
        val connection = URL(channel.url).openConnection() as HttpURLConnection
        try {
            connection.connectTimeout = 4_000
            connection.readTimeout = 4_000
            connection.instanceFollowRedirects = true
            connection.requestMethod = "GET"
            connection.setRequestProperty("Range", "bytes=0-1")
            if (channel.userAgent.isNotBlank()) {
                connection.setRequestProperty("User-Agent", channel.userAgent)
            }
            if (channel.referrer.isNotBlank()) {
                connection.setRequestProperty("Referer", channel.referrer)
            }
            if (channel.origin.isNotBlank()) {
                connection.setRequestProperty("Origin", channel.origin)
            }
            connection.responseCode > 0
        } finally {
            connection.disconnect()
        }
    } catch (ignored: Exception) {
        false
    }
}
