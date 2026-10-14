package com.premiumtv.app.data

import android.app.Application
import kotlinx.coroutines.runBlocking
import org.junit.Assert.*
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.RuntimeEnvironment
import org.robolectric.annotation.Config
import java.io.File

/** Exercises Android's real JsonReader and APK assets, not source-text checks. */
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [28], application = Application::class)
class TvRepositoryTest {
    private lateinit var app: Application

    @Before fun cleanCache() {
        app = RuntimeEnvironment.getApplication()
        for (name in listOf("bundle", "bundle-staging", "bundle-backup")) {
            File(app.filesDir, name).deleteRecursively()
        }
        app.getSharedPreferences("premiumtv_refresh", 0).edit().clear().commit()
    }

    private fun copyBundle(name: String = "bundle"): File {
        val dir = File(app.filesDir, name).apply { mkdirs() }
        for (file in listOf("meta.json", "channels.jsonl", "groups.jsonl", "epg.jsonl")) {
            app.assets.open("bundle/$file").use { input ->
                File(dir, file).outputStream().use { input.copyTo(it) }
            }
        }
        return dir
    }

    private fun ready(repository: TvRepository): Library {
        val state = repository.state.value
        assertTrue("Expected loaded channels, got $state", state is LoadState.Ready)
        return (state as LoadState.Ready).library
    }

    @Test fun coldLaunchLoadsTheActualBundledChannels() = runBlocking {
        val repository = TvRepository(app)
        repository.load()
        val library = ready(repository)
        assertTrue(library.channels.isNotEmpty())
        assertEquals(library.meta.channelCount, library.channels.size)
        assertEquals(library.channels.size, library.groups.sumOf { it.count })
        assertFalse(library.refreshed)
        assertFalse(library.guideLoading)
        assertTrue(library.channels.all { it.url.startsWith("http") })
    }

    @Test fun malformedCacheFallsBackToTheApk() = runBlocking {
        val cache = copyBundle()
        File(cache, "channels.jsonl").writeText("{broken\n")
        val repository = TvRepository(app)
        repository.load()
        assertFalse(ready(repository).refreshed)
        assertFalse(cache.exists())
    }

    @Test fun damagedGuideKeepsChannelsAvailable() = runBlocking {
        val cache = copyBundle()
        File(cache, "epg.jsonl").writeText("{broken\n")
        val repository = TvRepository(app)
        repository.load()
        val library = ready(repository)
        assertTrue(library.channels.isNotEmpty())
        assertNotNull(library.guideError)
        assertFalse(library.guideLoading)
    }

    @Test fun missingGroupsAreDerivedFromChannels() = runBlocking {
        File(copyBundle(), "groups.jsonl").delete()
        val repository = TvRepository(app)
        repository.load()
        val library = ready(repository)
        assertEquals(library.channels.size, library.groups.sumOf { it.count })
    }

    @Test fun interruptedSwapRestoresBackupAndResetUsesApk() = runBlocking {
        copyBundle("bundle-backup")
        File(app.filesDir, "bundle-staging").mkdirs()
        val repository = TvRepository(app)
        repository.load()
        assertTrue(ready(repository).refreshed)
        assertFalse(File(app.filesDir, "bundle-backup").exists())
        assertFalse(File(app.filesDir, "bundle-staging").exists())
        repository.resetToBundled()
        assertFalse(ready(repository).refreshed)
        assertTrue(ready(repository).channels.isNotEmpty())
    }

    @Test fun m3uParserKeepsCommasInChannelNamesAndQuotedAttributes() {
        val playlist = """#EXTM3U
#EXTINF:-1 tvg-id="news.local" group-title="News, Local",News, Local
https://example.org/news.m3u8"""
        val (channels, _) = M3uParser.parse(playlist)
        assertEquals(1, channels.size)
        assertEquals("News, Local", channels.single().name)
        assertEquals("News, Local", channels.single().group)
    }

    @Test fun xmltvParserRejectsInvalidDatesAndRepairsNonPositiveDurations() {
        val guide = """<tv>
<programme channel="demo" start="20261101010000 +0000" stop="20261101000000 +0000">
<title>Valid start</title></programme>
<programme channel="demo" start="20261131010000 +0000" stop="20261131020000 +0000">
<title>Invalid calendar date</title></programme>
<programme channel="demo" start="00000101000000 +0000" stop="00000101010000 +0000">
<title>Invalid year zero</title></programme>
</tv>"""
        val programmes = XmlTvParser.parse(guide)
        assertEquals(1, programmes.size)
        assertEquals("Valid start", programmes.single().title)
        assertEquals(1800L, programmes.single().end - programmes.single().start)
    }
}
