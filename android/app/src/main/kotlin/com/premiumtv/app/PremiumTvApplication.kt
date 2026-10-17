package com.premiumtv.app

import android.app.Application
import coil.ImageLoader
import coil.ImageLoaderFactory
import coil.disk.DiskCache
import com.premiumtv.app.data.TvRepository
import com.premiumtv.app.update.AppUpdateManager
import com.premiumtv.app.update.AutomaticRefreshScheduler
import java.io.File

/** Shared app services: one data repository, background updates and channel artwork. */
class PremiumTvApplication : Application(), ImageLoaderFactory {

    /** Foreground UI and WorkManager use the same mutex-protected repository. */
    val repository: TvRepository by lazy(LazyThreadSafetyMode.SYNCHRONIZED) {
        TvRepository(this)
    }

    /** One update checker for the whole process; Settings and startup share it. */
    val updateManager: AppUpdateManager by lazy(LazyThreadSafetyMode.SYNCHRONIZED) {
        AppUpdateManager(this)
    }

    override fun onCreate() {
        super.onCreate()
        // WorkManager persists this one-time request across process exits and
        // reboots. Each completed worker schedules the following GitHub slot.
        AutomaticRefreshScheduler.scheduleNext(this)
    }

    override fun newImageLoader(): ImageLoader =
        ImageLoader.Builder(this)
            // Logos are decorative; avoiding per-card fades keeps focus and
            // scrolling animation work low on inexpensive TV hardware.
            .crossfade(false)
            .diskCache {
                DiskCache.Builder()
                    .directory(File(cacheDir, "channel-logos"))
                    .maxSizeBytes(64L * 1024L * 1024L)
                    .build()
            }
            .build()
}
