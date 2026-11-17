package com.premiumtv.app

import android.app.Application
import coil.ImageLoader
import coil.ImageLoaderFactory
import coil.disk.DiskCache
import coil.memory.MemoryCache
import coil.decode.SvgDecoder
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
        installCrashRecorder()
        // WorkManager persists this one-time request across process exits and
        // reboots. Each completed worker schedules the following GitHub slot.
        AutomaticRefreshScheduler.scheduleNext(this)
    }

    /**
     * Records why a build died instead of failing silently.
     *
     * 1.1.12: viewers reported rare crashes with nothing to send us. Android's
     * default handler kills the process, so the app now writes the last error
     * to its own files and rethrows - the OS still gets a real crash, and
     * Settings -> Check for bugs can say "the last run ended unexpectedly"
     * with the class and message. It never swallows the exception: hiding a
     * crash would only move the damage somewhere harder to find.
     */
    private fun installCrashRecorder() {
        val previous = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
            try {
                val file = java.io.File(filesDir, "last-crash.txt")
                val detail = buildString {
                    append("time=").append(java.util.Date().toString()).append('\n')
                    append("thread=").append(thread.name).append('\n')
                    append(throwable.javaClass.name).append(": ")
                    append(throwable.message ?: "(no message)").append('\n')
                    throwable.stackTrace.take(24).forEach { append("  at ").append(it).append('\n') }
                }
                file.writeText(detail)
            } catch (ignored: Throwable) {
                // Storage full or already dying: the real handler still runs.
            }
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
