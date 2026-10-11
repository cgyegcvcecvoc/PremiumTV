package com.premiumtv.app.data

/** One playable stream as published by the repository's M3U playlists. */
data class Channel(
    val id: String,
    val name: String,
    val logo: String,
    val group: String,
    val country: String,
    val chno: String,
    val url: String,
    val userAgent: String,
    val referrer: String,
    val origin: String,
)

/** One XMLTV programme. [start] and [end] are epoch seconds (UTC). */
data class Programme(
    val channelId: String,
    val start: Long,
    val end: Long,
    val title: String,
    val desc: String,
    val category: String,
    val icon: String,
    val episode: String,
)

/** A category row, in the order the repository publishes. */
data class CategoryGroup(
    val name: String,
    val count: Int,
)

/** Provenance of the data the app is currently showing. */
data class BundleMeta(
    val version: String,
    val generatedUtc: String,
    val playlist: String,
    val guide: String,
    val channelCount: Int,
    val groupCount: Int,
    val programmeCount: Int,
    val guideChannels: Int,
    val windowStart: Long,
    val windowEnd: Long,
    val playlistUrl: String,
    val guideUrl: String,
    val rawBase: String,
) {
    companion object {
        val EMPTY = BundleMeta(
            version = "0",
            generatedUtc = "",
            playlist = "",
            guide = "",
            channelCount = 0,
            groupCount = 0,
            programmeCount = 0,
            guideChannels = 0,
            windowStart = 0L,
            windowEnd = 0L,
            playlistUrl = "",
            guideUrl = "",
            rawBase = "",
        )
    }
}

data class Library(
    val channels: List<Channel>,
    val groups: List<CategoryGroup>,
    val programmes: Map<String, List<Programme>>,
    val meta: BundleMeta,
    /** True when this data came from a network refresh instead of the APK. */
    val refreshed: Boolean,
    /** Channels can be shown before the larger programme guide finishes parsing. */
    val guideLoading: Boolean = false,
    /** Non-fatal guide problem; channels remain usable if the guide is unavailable. */
    val guideError: String? = null,
)

/** Why a network refresh was requested. */
enum class RefreshTrigger {
    Manual,
    Automatic,
}

/** Result consumed by the background worker to decide whether a short retry is useful. */
data class RefreshOutcome(
    val successful: Boolean,
    val changed: Boolean = false,
    val retryable: Boolean = false,
)

/** Persistent background-refresh information shown in Settings. */
data class RefreshInfo(
    val inProgress: Boolean = false,
    val lastAttemptAtMillis: Long = 0L,
    val lastSuccessAtMillis: Long = 0L,
    val nextAutomaticAtMillis: Long = 0L,
    val lastTrigger: RefreshTrigger? = null,
    val lastMessage: String = "Automatic refresh has not run yet.",
)

sealed interface LoadState {
    data object Loading : LoadState
    data class Ready(val library: Library) : LoadState
    data class Error(val message: String) : LoadState
}
