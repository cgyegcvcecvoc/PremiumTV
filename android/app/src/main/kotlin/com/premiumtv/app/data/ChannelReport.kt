package com.premiumtv.app.data

import java.net.URLEncoder
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

/**
 * A prefilled GitHub issue for a channel or server that will not play.
 *
 * PremiumTV has no report server and no account system, so a report is a
 * normal GitHub issue the viewer chooses to open. The app fills in what it
 * already knows and the viewer presses Submit; nothing is sent by the app.
 * The macOS and web players build the same URL from report.js.
 */
object ChannelReport {
    const val ISSUE_URL = "https://github.com/cgyegcvcecvoc/PremiumTV/issues/new"
    private const val MAX_BODY = 4200
    private const val MAX_URL = 1200

    private fun text(value: String?, limit: Int): String {
        val cleaned = (value ?: "")
            .replace(Regex("[\\u0000-\\u0008\\u000B\\u000C\\u000E-\\u001F]"), "")
            .trim()
        return if (cleaned.length > limit) cleaned.take(limit - 1) + "…" else cleaned
    }

    /** "2 of 3" for a valid position; "unknown" when the walk has no size. */
    fun serverPosition(index: Int, count: Int): String {
        if (count < 1) return "unknown"
        val current = index.coerceIn(0, count - 1) + 1
        return "$current of $count"
    }

    private fun encode(value: String): String = URLEncoder.encode(value, "UTF-8")

    private fun timestamp(): String {
        val format = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US)
        format.timeZone = TimeZone.getTimeZone("UTC")
        return format.format(Date())
    }

    /**
     * Build the issue URL. Only the channel name is required; every other
     * field is optional so a caller with less context still produces a useful
     * form.
     */
    fun issueUrl(
        channelName: String,
        group: String = "",
        streamUrl: String = "",
        serverIndex: Int = 0,
        serverCount: Int = 1,
        error: String = "",
        appVersion: String = "unknown build",
        platform: String = "Android",
        reportedAt: String = timestamp(),
    ): String {
        val channel = text(channelName, 90).ifBlank { "Unknown channel" }
        val category = text(group, 60)
        val stream = text(streamUrl, MAX_URL)
        val message = text(error, 900).ifBlank { "The feed did not play." }
        val version = text(appVersion, 90).ifBlank { "unknown build" }
        val device = text(platform, 220).ifBlank { "Android" }
        val server = serverPosition(serverIndex, serverCount)
        val title = "[Channel report] $channel — server $server will not play"

        val lines = mutableListOf(
            "### Channel report",
            "",
            "**Channel:** $channel",
        )
        if (category.isNotBlank()) lines += "**Category:** $category"
        lines += "**Server:** $server"
        if (stream.isNotBlank()) lines += "**Stream:** $stream"
        lines += listOf(
            "",
            "**What the player reported:**",
            "",
            "> " + message.replace("\n", "\n> "),
            "",
            "**App:** $version",
            "**Platform:** $device",
            "**Reported:** $reportedAt",
            "",
            "_Opened from PremiumTV. Please add anything else you saw, then press Submit._",
        )

        var body = lines.joinToString("\n")
        if (body.length > MAX_BODY) body = body.take(MAX_BODY - 40) + "\n\n_Report shortened._"
        return "$ISSUE_URL?title=${encode(title)}&body=${encode(body)}"
    }
}
