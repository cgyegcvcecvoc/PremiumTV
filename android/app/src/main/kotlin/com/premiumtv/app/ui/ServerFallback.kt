package com.premiumtv.app.ui

/**
 * Automatic server backup (1.1.0), kept as pure functions so the walking
 * rules can be unit-tested without an emulator.
 *
 * The player walks a channel's server list forward when a feed fails. It never
 * wraps around on its own: wrapping would retry the dead first server forever
 * and leave the viewer on a black screen instead of the honest error card.
 * Manual switching in the side player still wraps, because a person pressing
 * "Server ▶" expects to cycle.
 */

/** Why the player is moving on from the current feed. */
enum class ServerSwitchReason { Failed, Stalled, Manual }

/**
 * The next server the automatic backup walks to, or null when every feed for
 * this channel has already been tried.
 */
internal fun autoNextServerIndex(current: Int, count: Int): Int? {
    if (count < 1) return null
    val next = current + 1
    return if (next in 0 until count) next else null
}

/** True when the automatic backup still has somewhere to go. */
internal fun hasBackupServer(current: Int, count: Int): Boolean =
    autoNextServerIndex(current, count) != null

/**
 * The line the side player and the big screen show while a backup takes over.
 * "switching to server" is also what the emulator smoke gate looks for, so the
 * wording stays in step with android/tools/smoke_apk.py.
 */
internal fun serverSwitchNotice(
    reason: ServerSwitchReason,
    nextIndex: Int,
    count: Int,
): String {
    val target = "switching to server ${nextIndex + 1} of $count…"
    return when (reason) {
        ServerSwitchReason.Failed -> "This feed stopped responding — $target"
        ServerSwitchReason.Stalled -> "This feed is taking too long — $target"
        ServerSwitchReason.Manual -> "Server ${nextIndex + 1} of $count · selected by you"
    }
}

/** "Server 2 of 3 · automatic backup on" for the player's status line. */
internal fun serverStatusLine(index: Int, count: Int, backupAvailable: Boolean): String {
    val position = "Server ${index + 1} of $count"
    return if (backupAvailable) "$position · automatic backup on" else position
}

/**
 * What the player says when the walk is over. A channel with one feed does not
 * get the "all N servers" wording; it never had a backup to try.
 */
internal fun exhaustedServerMessage(count: Int): String =
    if (count > 1) {
        "All $count servers for this channel were tried."
    } else {
        "This channel has only one feed, and it is not answering."
    }

/**
 * What the player should do with a failed feed before it gives up on it.
 *
 * 1.1.12 (release "resilient playback"): a dropped segment, a slow CDN edge or
 * a decoder hiccup used to skip straight to the next server. On a channel with
 * one listed feed that meant the viewer saw the error card for a fault the
 * player could have survived. The rule is now:
 *
 *  - a transient/network fault gets a bounded number of in-place retries on the
 *    same feed, because the feed is usually fine a second later;
 *  - a media/decoder fault gets one decoder-level retry before the feed is
 *    considered failed, because ExoPlayer can rebuild a codec session;
 *  - a permanent fault (bad HTTP status, unsupported format, DRM, parse error)
 *    skips the retries: waiting cannot fix them.
 *
 * Pure so the walk is unit-tested without an emulator.
 */
internal enum class PlaybackFault { Transient, Media, Permanent }

internal data class RetryDecision(
    val fault: PlaybackFault,
    /** Retry the same feed in place instead of walking on. */
    val retryInPlace: Boolean,
    /** Told to the viewer while the retry runs; empty when nothing is shown. */
    val notice: String,
)

/** How many in-place retries each fault class is allowed. */
internal const val TRANSIENT_RETRY_LIMIT = 2
internal const val MEDIA_RETRY_LIMIT = 1

/**
 * Classifies a [androidx.media3.common.PlaybackException.errorCode] without
 * importing the player, so the test runs on any JVM.
 */
internal fun classifyErrorCode(errorCode: Int): PlaybackFault = when (errorCode) {
    // IO and network faults are the ones a retry actually helps.
    2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008 -> PlaybackFault.Transient
    // Decoder init/runtime, audio track, and rendering faults.
    4001, 4002, 4003, 4004, 4005, 4006 -> PlaybackFault.Media
    // Everything else - bad manifest, HTTP status, unsupported format, DRM -
    // is decided by the provider, not by timing.
    else -> PlaybackFault.Permanent
}

/**
 * @param alreadyRetried how many in-place retries this feed has already had
 * @param attemptedServerSwitch whether a server switch already happened for
 *   this channel, which caps the total work a viewer is put through
 */
internal fun decideRetry(
    fault: PlaybackFault,
    alreadyRetried: Int,
    attemptedServerSwitch: Boolean,
): RetryDecision = when (fault) {
    PlaybackFault.Permanent -> RetryDecision(
        fault = fault,
        retryInPlace = false,
        notice = "",
    )
    PlaybackFault.Transient -> {
        val allowed = alreadyRetried < TRANSIENT_RETRY_LIMIT && !attemptedServerSwitch
        RetryDecision(
            fault = fault,
            retryInPlace = allowed,
            notice = if (allowed) "Reconnecting to this feed…" else "",
        )
    }
    PlaybackFault.Media -> {
        val allowed = alreadyRetried < MEDIA_RETRY_LIMIT && !attemptedServerSwitch
        RetryDecision(
            fault = fault,
            retryInPlace = allowed,
            notice = if (allowed) "Rebuilding the decoder for this feed…" else "",
        )
    }
}
