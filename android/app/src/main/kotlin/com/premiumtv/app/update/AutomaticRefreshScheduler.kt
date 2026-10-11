package com.premiumtv.app.update

import android.content.Context
import androidx.work.BackoffPolicy
import androidx.work.Constraints
import androidx.work.ExistingWorkPolicy
import androidx.work.NetworkType
import androidx.work.OneTimeWorkRequestBuilder
import androidx.work.WorkManager
import androidx.work.workDataOf
import com.premiumtv.app.PremiumTvApplication
import java.util.Calendar
import java.util.TimeZone
import java.util.concurrent.TimeUnit

/**
 * Schedules app-side downloads shortly after the repository's publishing jobs.
 *
 * GitHub Actions uses America/New_York for its playlist, quick-update and EPG
 * cron jobs. WorkManager is intentionally inexact — Android may defer work
 * while a device sleeps — so each source slot is followed by a 45-minute
 * publishing grace period. After every run, the worker chains the next slot.
 * WorkManager persists that request across app exits and device reboots.
 */
object AutomaticRefreshScheduler {
    private const val WORK_NAME_PREFIX = "premiumtv-library-refresh"
    const val WORK_TAG = "premiumtv-automatic-refresh"
    const val INPUT_SCHEDULED_FOR = "scheduled_for_epoch_ms"

    internal const val PUBLISHING_GRACE_MINUTES = 45
    internal val REPOSITORY_TIME_ZONE: TimeZone = TimeZone.getTimeZone("America/New_York")

    // Keep this list in sync with scrape.yml, quick-update.yml and epg-build.yml.
    // tests/test_android_refresh.py guards that contract.
    internal val SOURCE_PUBLICATION_SLOTS = listOf(
        RefreshSlot(1, 19),
        RefreshSlot(3, 7),
        RefreshSlot(5, 47),
        RefreshSlot(6, 23),
        RefreshSlot(7, 31),
        RefreshSlot(9, 41),
        RefreshSlot(12, 53),
        RefreshSlot(13, 47),
        RefreshSlot(16, 41),
        RefreshSlot(17, 47),
        RefreshSlot(19, 23),
        RefreshSlot(20, 17),
        RefreshSlot(23, 29),
    )

    /** Enqueues the next connected-network check and returns its target time. */
    fun scheduleNext(context: Context, afterMillis: Long = System.currentTimeMillis()): Long {
        val nextRun = nextRunAfter(afterMillis)
        val delay = (nextRun - System.currentTimeMillis()).coerceAtLeast(0L)
        val constraints = Constraints.Builder()
            .setRequiredNetworkType(NetworkType.CONNECTED)
            .build()
        val request = OneTimeWorkRequestBuilder<LibraryRefreshWorker>()
            .setInitialDelay(delay, TimeUnit.MILLISECONDS)
            .setConstraints(constraints)
            .setBackoffCriteria(BackoffPolicy.EXPONENTIAL, 20, TimeUnit.MINUTES)
            .setInputData(workDataOf(INPUT_SCHEDULED_FOR to nextRun))
            .addTag(WORK_TAG)
            .build()

        WorkManager.getInstance(context.applicationContext).enqueueUniqueWork(
            "$WORK_NAME_PREFIX-$nextRun",
            ExistingWorkPolicy.KEEP,
            request,
        )
        (context.applicationContext as? PremiumTvApplication)
            ?.repository
            ?.noteNextAutomaticRefresh(nextRun)
        return nextRun
    }

    /** Absolute instant of the first repository slot plus grace after [afterMillis]. */
    internal fun nextRunAfter(afterMillis: Long): Long {
        val startOfDay = Calendar.getInstance(REPOSITORY_TIME_ZONE).apply {
            timeInMillis = afterMillis
            set(Calendar.HOUR_OF_DAY, 0)
            set(Calendar.MINUTE, 0)
            set(Calendar.SECOND, 0)
            set(Calendar.MILLISECOND, 0)
        }

        // Start with yesterday because the 23:29 publication plus its grace
        // lands just after midnight. Returning from a simple today-only loop
        // would otherwise skip that 00:14 check.
        var nearest = Long.MAX_VALUE
        for (dayOffset in -1..2) {
            val day = (startOfDay.clone() as Calendar).apply {
                add(Calendar.DAY_OF_YEAR, dayOffset)
            }
            for (slot in SOURCE_PUBLICATION_SLOTS) {
                val candidate = (day.clone() as Calendar).apply {
                    set(Calendar.HOUR_OF_DAY, slot.hour)
                    set(Calendar.MINUTE, slot.minute)
                    add(Calendar.MINUTE, PUBLISHING_GRACE_MINUTES)
                }.timeInMillis
                if (candidate > afterMillis && candidate < nearest) nearest = candidate
            }
        }
        if (nearest != Long.MAX_VALUE) return nearest
        error("No automatic refresh slot could be calculated")
    }
}

internal data class RefreshSlot(val hour: Int, val minute: Int)
