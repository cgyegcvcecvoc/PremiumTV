package com.premiumtv.app.update

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.premiumtv.app.PremiumTvApplication
import com.premiumtv.app.data.RefreshTrigger

/** Downloads and atomically installs fresh channels/guide while the app is closed. */
class LibraryRefreshWorker(
    appContext: Context,
    workerParameters: WorkerParameters,
) : CoroutineWorker(appContext, workerParameters) {

    override suspend fun doWork(): Result {
        val app = applicationContext as? PremiumTvApplication ?: return Result.failure()
        val outcome = app.repository.refresh(RefreshTrigger.Automatic)

        // A disconnected network is already held by the WorkManager constraint.
        // Retry transient server/time-out failures twice, but do not hammer a
        // private raw URL that consistently answers 401/403/404.
        if (!outcome.successful && outcome.retryable && runAttemptCount < 2) {
            return Result.retry()
        }

        // Use a new slot-specific unique name rather than replacing this running
        // worker. Application.onCreate may already have queued the same next slot;
        // ExistingWorkPolicy.KEEP safely collapses the duplicate.
        AutomaticRefreshScheduler.scheduleNext(applicationContext)
        return Result.success()
    }
}
