package com.premiumtv.app

import android.app.Application
import coil.ImageLoader
import coil.ImageLoaderFactory
import coil.disk.DiskCache
import java.io.File

/** Shared image pipeline for channel artwork. */
class PremiumTvApplication : Application(), ImageLoaderFactory {
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
