package com.premiumtv.app

import android.app.Application
import coil.ImageLoader
import coil.ImageLoaderFactory
import coil.disk.DiskCache
import coil.memory.MemoryCache
import coil.decode.SvgDecoder
import com.premiumtv.app.data.TvRepository
import com.premiumtv.app.update.AppUpdateManager
import com.premiumtv.app.update.CrashLog
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
        installCrashRecorder()
        // WorkManager persists this one-time request across process exits and
        // reboots. Each completed worker schedules the following GitHub slot.
        AutomaticRefreshScheduler.scheduleNext(this)
    }

    /**
     * Records why a build died instead of failing silently.
     *
     * 1.1.12: viewers reported rare crashes with nothing to send us. Android's
     * default handler kills the process, so the app writes the last error to
     * its own files and rethrows - the OS still gets a real crash. It never
     * swallows the exception: hiding a crash would only move the damage
     * somewhere harder to find.
     *
     * 1.1.14: the record is now readable. 1.1.12 wrote the file but nothing
     * displayed it, and app-private storage is not reachable by a viewer, so
     * the report could still only say "it crashed". Settings now shows the
     * recorded class, message and stack and can clear it (CrashLog).
     */
    private fun installCrashRecorder() {
        val previous = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
            CrashLog.write(filesDir, thread, throwable)
            previous?.uncaughtException(thread, throwable)
        }
    }

    override fun newImageLoader(): ImageLoader {
        val app = this
        return ImageLoader.Builder(app)
            .components { add(SvgDecoder.Factory()) }
            // Logos are decorative; avoiding per-card fades keeps focus and
            // scrolling animation work low on inexpensive TV hardware.
            .crossfade(false)
            // A TV stick's heap is the scarce resource, and the default memory
            // cache scales with it (largeHeap made that worse). 10% is enough
            // to keep a grid of logos warm and leaves the guide and player room.
            .memoryCache {
                MemoryCache.Builder(app)
                    .maxSizePercent(0.10)
                    .build()
            }
            .diskCache {
                DiskCache.Builder()
                    .directory(File(app.cacheDir, "channel-logos"))
                    .maxSizeBytes(64L * 1024L * 1024L)
                    .build()
            }
            .build()
    }
}
