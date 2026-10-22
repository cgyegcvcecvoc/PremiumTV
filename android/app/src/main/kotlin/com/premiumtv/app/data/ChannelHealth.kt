package com.premiumtv.app.data

import android.content.Context

/**
 * Dead-feed memory (1.1.0): the app's own answer to a channel that has gone
 * dark between the repository's nightly link checks.
 *
 * A feed is only recorded after the player itself watched it fail on *every*
 * server for that channel, so a single geo-restricted attempt or a one-off
 * timeout cannot hide a working channel. Recordings expire, because an
 * upstream link can come back and the published playlist is refreshed often;
 * Settings also has a one-press restore.
 *
 * The pure functions live here so the filtering rules are unit-testable on the
 * JVM without an emulator.
 */
internal const val DEAD_FEED_TTL_MS = 7L * 24L * 60L * 60L * 1000L

/** One remembered failure: the feed URL and when the player last saw it fail. */
data class DeadFeed(
    val url: String,
    val markedAtMillis: Long,
)

/** Drops recordings older than [ttlMs]; a returning feed gets a fresh chance. */
internal fun pruneDeadFeeds(
    entries: List<DeadFeed>,
    nowMillis: Long,
    ttlMs: Long = DEAD_FEED_TTL_MS,
): List<DeadFeed> = entries.filter { entry ->
    entry.url.isNotBlank() && nowMillis - entry.markedAtMillis < ttlMs
}

/** The URLs that are still considered dead at [nowMillis]. */
internal fun deadUrlSet(
    entries: List<DeadFeed>,
    nowMillis: Long,
    ttlMs: Long = DEAD_FEED_TTL_MS,
): Set<String> = pruneDeadFeeds(entries, nowMillis, ttlMs).map { it.url }.toSet()

/**
 * The channel list the browser may show: dead feeds are filtered out, and a
 * channel only disappears once every one of its feeds is dead.
 *
 * [deadUrls] holds feed URLs, and every channel row is one feed, so a channel
 * whose primary link died still appears through its backups.
 */
internal fun visibleChannels(channels: List<Channel>, deadUrls: Set<String>): List<Channel> =
    if (deadUrls.isEmpty()) channels else channels.filter { it.url !in deadUrls }

/** How many channel rows the browser is hiding right now. */
internal fun hiddenChannelCount(channels: List<Channel>, deadUrls: Set<String>): Int =
    channels.count { it.url in deadUrls }

/**
 * Orders a channel's servers so the ones with no recorded failure are tried
 * first. The order inside each group is preserved, so the published primary
 * feed still leads when everything is healthy.
 */
internal fun healthyServersFirst(servers: List<Channel>, deadUrls: Set<String>): List<Channel> {
    if (deadUrls.isEmpty()) return servers
    val healthy = servers.filter { it.url !in deadUrls }
    val known = servers.filter { it.url in deadUrls }
    return healthy + known
}

/** SharedPreferences-backed store for [DeadFeed] recordings. */
internal class ChannelHealthStore(context: Context) {
    private val prefs = context.getSharedPreferences("premiumtv_health", Context.MODE_PRIVATE)

    fun deadFeeds(nowMillis: Long = System.currentTimeMillis()): List<DeadFeed> =
        pruneDeadFeeds(read(), nowMillis)

    fun deadUrls(nowMillis: Long = System.currentTimeMillis()): Set<String> =
        deadUrlSet(read(), nowMillis)

    /** Records one failed feed, keeping any earlier failure of the same URL. */
    fun recordDead(url: String, nowMillis: Long = System.currentTimeMillis()) {
        if (url.isBlank()) return
        val kept = pruneDeadFeeds(read(), nowMillis).filter { it.url != url }
        write(listOf(DeadFeed(url, nowMillis)) + kept)
    }

    /** Settings → Restore hidden channels: forget every recorded failure. */
    fun clear() = write(emptyList())

    private fun read(): List<DeadFeed> =
        prefs.getString(KEY_DEAD, "").orEmpty()
            .split('\n')
            .mapNotNull { line ->
                val separator = line.indexOf('\t')
                if (separator <= 0) return@mapNotNull null
                val whenMillis = line.substring(0, separator).toLongOrNull() ?: return@mapNotNull null
                val url = line.substring(separator + 1)
                if (url.isBlank()) null else DeadFeed(url, whenMillis)
            }

    private fun write(entries: List<DeadFeed>) {
        prefs.edit()
            .putString(KEY_DEAD, entries.joinToString("\n") { "${it.markedAtMillis}\t${it.url}" })
            .apply()
    }

    private companion object {
        const val KEY_DEAD = "dead_feeds"
    }
}
