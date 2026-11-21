package com.premiumtv.app.update

/**
 * What the UI had to do on the main thread, measured rather than guessed
 * (1.1.17).
 *
 * The 1.1.16 report was "it lags, then sometimes it stops", with no crash
 * record because the app had never actually been asked to record a *slow*
 * frame - only a fatal error. Settings → Check for bugs now shows these
 * numbers, so a report can say "opening a channel planned its feeds in 240 ms
 * on the UI thread" instead of "it feels slow".
 *
 * It is a handful of longs behind one volatile reference: no allocation per
 * frame, no timer, nothing that runs on its own. The values describe the last
 * thing the app did, and are deliberately not persisted - a restart is exactly
 * when they stop being about the current build.
 */
data class UiWorkSnapshot(
    /** How long the last channel index took to build. */
    val indexBuildMs: Long = 0L,
    /** How many channels that index covered. */
    val indexChannelCount: Int = 0,
    /** True when the index had to be built on the UI thread (a fallback path). */
    val indexOnUiThread: Boolean = false,
    /** How long the last channel open spent choosing its feeds. */
    val lastChannelOpenMs: Long = 0L,
    /** True when that choice came from the prepared index rather than a scan. */
    val lastChannelOpenUsedIndex: Boolean = true,
    /** Why the last index build failed, or empty when it did not. */
    val indexFailure: String = "",
)

/** Process-wide holder for [UiWorkSnapshot]; written from the main thread. */
object PerfLog {

    @Volatile
    var snapshot: UiWorkSnapshot = UiWorkSnapshot()
        private set

    /** Records one index build; [onUiThread] flags the fallback path. */
    fun recordIndexBuild(durationMs: Long, channelCount: Int, onUiThread: Boolean = false) {
        snapshot = snapshot.copy(
            indexBuildMs = durationMs.coerceAtLeast(0L),
            indexChannelCount = channelCount,
            indexOnUiThread = onUiThread,
            indexFailure = "",
        )
    }

    /** Records a failed index build, so Settings can report it honestly. */
    fun recordIndexFailure(reason: String) {
        snapshot = snapshot.copy(indexFailure = reason)
    }

    /** Records how long one channel open spent planning its feed list. */
    fun recordChannelOpen(durationMs: Long, usedIndex: Boolean) {
        snapshot = snapshot.copy(
            lastChannelOpenMs = durationMs.coerceAtLeast(0L),
            lastChannelOpenUsedIndex = usedIndex,
        )
    }
}
