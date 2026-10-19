package com.premiumtv.app.update

import org.json.JSONObject
import java.text.ParseException
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

/**
 * The remote "please update" notice, and the policy that decides who sees it.
 *
 * Why this file exists: an installed app cannot be given new code, so the only
 * way to reach a version that is already on somebody's TV is a message the app
 * was *already* built to fetch.  `app-update-notice.json` in the repository is
 * that message.  Every build from 1.0.5 on reads it during the same daily
 * GitHub check the updater already performs, which means the wording, the
 * targeted version range and the end-of-support date can all be changed later
 * without publishing another release.
 *
 * The policy is deliberately boring and total: anything unreadable, disabled or
 * out of range produces `null`, and a `null` notice never affects the app.  A
 * bad edit to the JSON can silence the popup; it can never break playback.
 *
 * Versions older than 1.0.5 have no notice code at all.  They are reached by
 * the sanctioned notice entry `scripts/legacy_sunset.py` publishes into the
 * playlist they refresh from - see docs/UPDATES.md.
 */
object UpdateNotice {

    /** The published notice, read from `main` during the daily update check. */
    const val NOTICE_URL =
        "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/app-update-notice.json"

    /** Fallback shown when the document does not name a releases page. */
    const val DEFAULT_RELEASES_URL =
        "https://github.com/cgyegcvcecvoc/PremiumTV1/releases/latest"

    /** The notice is tiny; a response above this is treated as unreadable. */
    const val MAX_NOTICE_BYTES = 64L * 1024L

    private const val SUPPORTED_SCHEMA = 1
    private const val PLATFORM_ANDROID = "android"

    private val UTC: TimeZone = TimeZone.getTimeZone("UTC")

    /**
     * Parse the published JSON and pick the message this build should show.
     *
     * @param body          the notice document, exactly as published.
     * @param appVersion    this APK's numeric version ("1.0.4").
     * @param newestVersion the newest stable release the updater found, if any.
     * @param nowMillis     the current time; the end-of-support date is compared to it.
     * @return the notice to show, or null when this build should not be nagged.
     */
    fun select(
        body: String?,
        appVersion: String,
        newestVersion: String?,
        nowMillis: Long = System.currentTimeMillis(),
    ): AppUpdateNotice? {
        val text = body?.trim().orEmpty()
        if (text.isEmpty()) return null
        val document = try {
            JSONObject(text)
        } catch (e: Exception) {
            return null
        }
        if (!document.optBoolean("enabled", false)) return null
        // A schema this build has never seen may mean a changed contract; show
        // nothing rather than guess at fields that moved.
        if (document.optInt("schema", 0) != SUPPORTED_SCHEMA) return null

        val supportEnds = parseInstant(document.optString("support_ends_utc"))
        val ended = supportEnds != null && nowMillis >= supportEnds
        val releasesUrl = document.optString("releases_url").trim()
            .takeIf { it.startsWith("https://") } ?: DEFAULT_RELEASES_URL
        val rules = document.optJSONArray("rules") ?: return null

        for (index in 0 until rules.length()) {
            val rule = rules.optJSONObject(index) ?: continue
            val notice = fromRule(rule, appVersion, newestVersion, supportEnds, ended, releasesUrl)
            if (notice != null) return notice
        }
        return null
    }

    private fun fromRule(
        rule: JSONObject,
        appVersion: String,
        newestVersion: String?,
        supportEndsMillis: Long?,
        ended: Boolean,
        releasesUrl: String,
    ): AppUpdateNotice? {
        if (!targetsPlatform(rule)) return null
        if (!targetsVersion(rule, appVersion)) return null

        // Once the published support window has closed the same rule escalates:
        // the wording switches from "a surprise is waiting" to "this build is
        // frozen".  Both texts ship in the JSON, so day 30 needs no new build
        // and no remote edit.
        val active = if (ended) rule.optJSONObject("after_support_ends") ?: rule else rule

        val level = when (active.optString("level", "warning")) {
            "end_of_support" -> NoticeLevel.EndOfSupport
            "blocked" -> NoticeLevel.Blocked
            "critical" -> NoticeLevel.Critical
            else -> NoticeLevel.Warning
        }
        val values = mapOf(
            "{version}" to appVersion,
            "{newest}" to (newestVersion?.takeIf { it.isNotBlank() } ?: "the newest release"),
            "{support_ends}" to (supportEndsMillis?.let { formatDay(it) } ?: "the published date"),
        )
        val title = substitute(active.optString("title"), values)
        val message = substitute(active.optString("message"), values)
        if (title.isBlank() && message.isBlank()) return null

        return AppUpdateNotice(
            id = rule.optString("id").ifBlank { "notice" },
            level = level,
            title = title.ifBlank { "A newer PremiumTV is available" },
            message = message,
            surprise = substitute(active.optString("surprise"), values),
            actionLabel = substitute(active.optString("action_label"), values)
                .ifBlank { "Update now" },
            dismissLabel = substitute(active.optString("dismiss_label"), values)
                .ifBlank { "Remind me next time" },
            releasesUrl = rule.optString("releases_url").trim()
                .takeIf { it.startsWith("https://") } ?: releasesUrl,
            supportEndsAtMillis = supportEndsMillis ?: 0L,
            supportEnded = ended,
        )
    }

    private fun targetsPlatform(rule: JSONObject): Boolean {
        val platforms = rule.optJSONArray("platforms") ?: return true
        if (platforms.length() == 0) return true
        for (index in 0 until platforms.length()) {
            if (platforms.optString(index).trim().lowercase(Locale.US) == PLATFORM_ANDROID) {
                return true
            }
        }
        return false
    }

    /**
     * True when [appVersion] is inside the rule's inclusive range.  A missing
     * or unreadable bound is open-ended, so a rule can target "everything up to
     * 1.0.4" without also having to spell out a floor.
     */
    private fun targetsVersion(rule: JSONObject, appVersion: String): Boolean {
        val current = AppVersions.normalize(appVersion) ?: return false
        val min = AppVersions.normalize(rule.optString("min_version"))
        val max = AppVersions.normalize(rule.optString("max_version"))
        if (min != null && current != min && !AppVersions.isNewer(current, min)) return false
        if (max != null && AppVersions.isNewer(current, max)) return false
        return true
    }

    private fun substitute(text: String?, values: Map<String, String>): String {
        val source: String = text?.trim().orEmpty()
        if (source.isEmpty()) return ""
        var result: String = source
        for ((token, value) in values) {
            result = result.replace(token, value)
        }
        return result.trim()
    }

    /**
     * Parses `2026-11-16T23:59:59Z` or `2026-11-16` into epoch millis (UTC).
     *
     * A formatter is built per call on purpose: `SimpleDateFormat` is not
     * thread-safe and `ThreadLocal.withInitial` needs API 24, while this app
     * supports API 23.  The notice is read once a day, so the allocation is
     * free in practice.
     */
    fun parseInstant(value: String?): Long? {
        val text = value?.trim().orEmpty()
        if (text.isEmpty()) return null
        val zoned = text.endsWith("Z")
        val body = text.removeSuffix("Z")
        val pattern = when {
            body.length == 10 -> "yyyy-MM-dd"
            body.contains('T') -> "yyyy-MM-dd'T'HH:mm:ss"
            else -> return null
        }
        return try {
            val formatter = SimpleDateFormat(pattern, Locale.US)
            formatter.timeZone = UTC
            formatter.isLenient = false
            formatter.parse(body)?.time?.let { millis ->
                // A bare date means "that whole day", so it ends at midnight of
                // the following day; a timestamp is used exactly as published.
                if (!zoned && pattern == "yyyy-MM-dd") millis + 86_400_000L - 1L else millis
            }
        } catch (e: ParseException) {
            null
        } catch (e: IllegalArgumentException) {
            null
        }
    }

    /** "Nov 16, 2026" in UTC, so the date reads the same on every device. */
    fun formatDay(epochMillis: Long): String {
        val formatter = SimpleDateFormat("MMM d, yyyy", Locale.US)
        formatter.timeZone = UTC
        return formatter.format(Date(epochMillis))
    }
}

/** How urgently the notice should read. Every level stays dismissible on a TV. */
enum class NoticeLevel {
    /** "A newer version is waiting." */
    Warning,

    /** Stronger wording, still dismissible. */
    Critical,

    /** The published support window has closed; this build is frozen. */
    EndOfSupport,

    /**
     * A retired preview that must not be used. It still runs and still
     * dismisses, but the popup names the stable replacement and the download
     * path, and the accent is the same alarm red as end-of-support.
     */
    Blocked,
}

/** One resolved notice, ready for the dialog to render. */
data class AppUpdateNotice(
    val id: String,
    val level: NoticeLevel,
    val title: String,
    val message: String,
    val surprise: String,
    val actionLabel: String,
    val dismissLabel: String,
    val releasesUrl: String,
    val supportEndsAtMillis: Long = 0L,
    val supportEnded: Boolean = false,
) {
    /** True once the support window closed: the copy is about a frozen build. */
    val isEndOfSupport: Boolean get() = level == NoticeLevel.EndOfSupport

    /** True for a retired preview that should be replaced immediately. */
    val isBlocked: Boolean get() = level == NoticeLevel.Blocked
}
