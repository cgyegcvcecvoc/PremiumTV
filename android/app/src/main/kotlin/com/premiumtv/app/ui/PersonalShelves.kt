package com.premiumtv.app.ui

import android.content.Context
import com.premiumtv.app.data.Channel

/**
 * Recently watched + Favorites (1.0.6), the viewer's own shelves.
 *
 * Pure list logic first (unit-testable on the JVM): a channel is keyed by its
 * stream URL — backup feeds share an EPG id, but the URL is the identity every
 * feed actually has. Opening a channel moves it to the front of Recents;
 * Favorites toggle. Both persist in SharedPreferences as newline-joined keys
 * (stream URLs never contain a newline).
 */
internal const val MAX_RECENTS = 30

internal fun recordRecentChannel(keys: List<String>, key: String, limit: Int = MAX_RECENTS): List<String> {
    if (key.isBlank()) return keys
    return (listOf(key) + keys.filter { it != key }).take(limit)
}

internal fun toggleFavoriteChannel(keys: List<String>, key: String): List<String> {
    if (key.isBlank()) return keys
    return if (key in keys) keys.filter { it != key } else listOf(key) + keys
}

/** Keys -> channels in key order; channels that left the playlist drop out. */
internal fun resolveShelf(keys: List<String>, channels: List<Channel>): List<Channel> {
    val byUrl = channels.associateBy { it.url }
    return keys.mapNotNull { byUrl[it] }
}

/** Manual server switching wraps around; auto-fallback only walks forward. */
internal fun nextServerIndex(current: Int, count: Int, delta: Int): Int {
    if (count < 1) return 0
    return ((current + delta) % count + count) % count
}

internal class PersonalShelves(context: Context) {
    private val prefs = context.getSharedPreferences("premiumtv_personal", Context.MODE_PRIVATE)

    fun recentKeys(): List<String> = read(RECENTS)
    fun favoriteKeys(): List<String> = read(FAVORITES)

    fun recordRecent(key: String) = write(RECENTS, recordRecentChannel(recentKeys(), key))
    fun toggleFavorite(key: String): List<String> {
        val next = toggleFavoriteChannel(favoriteKeys(), key)
        write(FAVORITES, next)
        return next
    }

    private fun read(name: String): List<String> =
        prefs.getString(name, "").orEmpty().split('\n').filter { it.isNotBlank() }

    private fun write(name: String, keys: List<String>) {
        prefs.edit().putString(name, keys.joinToString("\n")).apply()
    }

    private companion object {
        const val RECENTS = "recent_keys"
        const val FAVORITES = "favorite_keys"
    }
}
