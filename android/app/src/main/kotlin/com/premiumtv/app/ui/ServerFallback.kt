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
