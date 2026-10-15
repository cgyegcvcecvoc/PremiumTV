package com.premiumtv.app.data

import android.app.Application
import android.content.Context
import android.os.Build
import android.util.Log
import com.premiumtv.app.BuildConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock
import kotlinx.coroutines.withContext
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.io.FileNotFoundException
import java.io.FilterInputStream
import java.io.IOException
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

/**
 * Owns the channel list and the guide.
 *
 * Two sources, one shape:
 *  - the bundle shipped inside the APK (android/app/src/main/assets/bundle),
 *    produced by android/tools/build_bundle.py from this repository;
 *  - a cache in the app's private files, written by [refresh].
 *
 * The cache wins when it exists, so automatic and manual refreshes survive a
 * restart - but only while it was written by this same build. A cache records
 * the version and library scope of the bundle it replaced; when those differ
 * from this APK's bundle (a 1.0.x USA refresh still on the device after the
 * global preview is installed over it), the cache is discarded on load,
 * because it would otherwise hide everything the new APK ships, the cable
 * guide included. Resetting in Settings deletes it and falls back to what the
 * APK shipped with. All load/write operations share one mutex: a background
 * worker can never replace files while the foreground UI is reading them.
 */
class TvRepository(private val app: Application) {

    private companion object {
        const val TAG = "PremiumTV"

        const val PREFS = "premiumtv_refresh"
        const val KEY_LAST_ATTEMPT = "last_attempt_ms"
        const val KEY_LAST_SUCCESS = "last_success_ms"
        const val KEY_LAST_TRIGGER = "last_trigger"
        const val KEY_LAST_MESSAGE = "last_message"
        const val KEY_NEXT_AUTOMATIC = "next_automatic_ms"

        const val PLAYLIST_VALIDATOR = "playlist"
        const val GUIDE_VALIDATOR = "guide"

        const val MAX_PLAYLIST_BYTES = 32L * 1024L * 1024L
        // The global preview's merged guide is ~38 MB of XML. It is parsed
        // straight off the connection, so this only bounds the download.
        const val MAX_GUIDE_BYTES = 160L * 1024L * 1024L
    }

    private val operations = Mutex()
    private val preferences = app.getSharedPreferences(PREFS, Context.MODE_PRIVATE)

    private val _state = MutableStateFlow<LoadState>(LoadState.Loading)
    val state: StateFlow<LoadState> = _state

    private val _status = MutableStateFlow("")
    val status: StateFlow<String> = _status

    private val _refreshInfo = MutableStateFlow(readRefreshInfo())
    val refreshInfo: StateFlow<RefreshInfo> = _refreshInfo

    /**
     * The metadata of the bundle inside this APK: its version, library scope
     * and preview features. It decides which UI the build shows, whatever a
     * downloaded copy says.
     */
    private val bundledMeta: BundleMeta by lazy {
        try {
            app.assets.open("bundle/meta.json").use { parseMeta(it) }
        } catch (e: Exception) {
            Log.w(TAG, "The APK's bundle metadata is unreadable", e)
            BundleMeta.EMPTY
        }
    }

    private val cacheDir: File get() = File(app.filesDir, "bundle")
    private val stagingCacheDir: File get() = File(app.filesDir, "bundle-staging")
    private val backupCacheDir: File get() = File(app.filesDir, "bundle-backup")

    suspend fun load() = withContext(Dispatchers.IO) {
        operations.withLock { loadLocked() }
    }

    /**
     * Refreshes both app data sources.
     *
     * A manual refresh deliberately downloads both files even when their HTTP
     * validators are unchanged: this is the Settings screen's "force" action.
     * Automatic checks send ETag/Last-Modified validators, so matching the
     * repository's frequent publishing windows normally costs only two tiny
     * HTTP 304 responses.
     */
    suspend fun refresh(trigger: RefreshTrigger): RefreshOutcome = withContext(Dispatchers.IO) {
        operations.withLock { refreshLocked(trigger) }
    }

    /** Drops the downloaded copy and goes back to what the APK shipped with. */
    suspend fun resetToBundled() = withContext(Dispatchers.IO) {
        operations.withLock {
            cacheDir.deleteRecursively()
            stagingCacheDir.deleteRecursively()
            backupCacheDir.deleteRecursively()
            clearValidators()
            loadLocked()
            _status.value = "Using the channel list and guide bundled in this APK."
        }
    }

    /** Called by the WorkManager scheduler so Settings can show the next check. */
    fun noteNextAutomaticRefresh(epochMillis: Long) {
        preferences.edit().putLong(KEY_NEXT_AUTOMATIC, epochMillis).apply()
        _refreshInfo.value = _refreshInfo.value.copy(nextAutomaticAtMillis = epochMillis)
    }

    // -------------------------------------------------------------- operations

    private fun loadLocked() {
        recoverInterruptedCacheWrite()
        discardCacheFromAnotherBuild()
        _state.value = LoadState.Loading
        _status.value = "Loading channels…"

        // Publish the channel rows as soon as their small files are ready. The
        // larger guide can finish without holding Channels behind a full parse.
        val cached = readCache { partial ->
            _state.value = LoadState.Ready(partial)
            _status.value = if (partial.guideLoading) "Channels ready; loading guide…" else ""
        }
        if (cached != null) {
            _state.value = LoadState.Ready(cached)
            _status.value = when {
                cached.guideError != null -> "Channels loaded; the programme guide is unavailable."
                else -> "Showing the latest copy downloaded in the app."
            }
            return
        }

        _status.value = "Loading bundled channels…"
        try {
            val bundled = readBundled { partial ->
                _state.value = LoadState.Ready(partial)
                _status.value = if (partial.guideLoading) "Channels ready; loading guide…" else ""
            }
            _state.value = LoadState.Ready(bundled)
            _status.value = if (bundled.guideError != null) {
                "Channels loaded; the programme guide is unavailable."
            } else {
                ""
            }
        } catch (e: Exception) {
            Log.e(TAG, "The channel data bundled in this APK could not be read", e)
            _state.value = LoadState.Error(
                "The channel data inside this app could not be read.\n" +
                    "Install the latest PremiumTV release and retry.\n\n" +
                    "Detail: ${e.javaClass.simpleName}: ${e.message ?: "no message"}"
            )
        }
    }

    private fun refreshLocked(trigger: RefreshTrigger): RefreshOutcome {
        beginRefresh(trigger)
        val isManual = trigger == RefreshTrigger.Manual

        try {
            var current = (_state.value as? LoadState.Ready)?.library
            if (current == null) {
                loadLocked()
                current = (_state.value as? LoadState.Ready)?.library
            }
            if (current == null) {
                return finishRefresh(
                    trigger = trigger,
                    successful = false,
                    message = "Refresh could not start because the current channel data is unreadable.",
                    retryable = false,
                )
            }

            val meta = current.meta
            val playlistUrl = meta.playlistUrl.trim()
            if (playlistUrl.isBlank()) {
                return finishRefresh(
                    trigger = trigger,
                    successful = false,
                    message = "This build has no playlist update URL to fetch.",
                    retryable = false,
                )
            }

            // A bundled fallback must always perform a full fetch. Validators
            // are only safe when the downloaded cache they describe is active.
            val conditional = !isManual && current.refreshed
            _status.value = if (isManual) {
                "Force refresh: downloading the complete channel list…"
            } else {
                "Background refresh: checking the channel list…"
            }
            val playlistDownload = download(
                urlString = playlistUrl,
                validatorName = PLAYLIST_VALIDATOR,
                conditional = conditional,
                maxBytes = MAX_PLAYLIST_BYTES,
            ) { input -> input.bufferedReader(Charsets.UTF_8).readText() }

            val parsedPlaylist = playlistDownload.body?.let { M3uParser.parse(it) }
            val channels = parsedPlaylist?.first ?: current.channels
            if (channels.isEmpty()) throw IOException("the playlist contained no channels")

            // Prefer a guide URL advertised by a newly downloaded playlist. If
            // the playlist was unchanged, its URL in bundle metadata is enough.
            val headerGuideUrl = parsedPlaylist?.second.orEmpty().trim()
            val guideUrl = headerGuideUrl.ifBlank { meta.guideUrl.trim() }
            if (guideUrl.isBlank()) throw IOException("the playlist has no programme-guide URL")

            _status.value = if (isManual) {
                "Force refresh: downloading the complete programme guide…"
            } else {
                "Background refresh: checking the programme guide…"
            }
            // The guide is parsed as it downloads, keeping only listings for
            // channels in the playlist that have not finished more than six
            // hours ago. Reading the 38 MB global guide into one String first
            // needed ~200 MB of heap, enough to kill the refresh on a TV stick.
            val known = HashSet<String>(channels.size * 2).apply { channels.forEach { add(it.id) } }
            val keepAfter = System.currentTimeMillis() / 1000L - 6 * 3600L
            val readGuide: (InputStream) -> List<Programme> = { input ->
                XmlTvParser.parse(input) { channelId, end -> end > keepAfter && known.contains(channelId) }
            }
            var guideDownload = download(
                urlString = guideUrl,
                validatorName = GUIDE_VALIDATOR,
                conditional = conditional,
                maxBytes = MAX_GUIDE_BYTES,
                read = readGuide,
            )

            // When channel membership changed, re-read even an otherwise
            // unchanged guide. The previous parsed cache intentionally omitted
            // programmes for channels that did not exist at that time.
            if (playlistDownload.body != null && guideDownload.notModified) {
                guideDownload = download(
                    urlString = guideUrl,
                    validatorName = GUIDE_VALIDATOR,
                    conditional = false,
                    maxBytes = MAX_GUIDE_BYTES,
                    read = readGuide,
                )
            }

            if (playlistDownload.notModified && guideDownload.notModified) {
                saveValidator(PLAYLIST_VALIDATOR, playlistUrl, playlistDownload)
                saveValidator(GUIDE_VALIDATOR, guideUrl, guideDownload)
                val message = if (isManual) {
                    "All app data was checked; the channel list and guide are already current."
                } else {
                    "Background check complete; the channel list and guide are already current."
                }
                return finishRefresh(trigger, true, message, changed = false)
            }

            val programmes = guideDownload.body ?: current.programmes.values.flatten()
            // The refreshed copy describes this APK's build, so the next load
            // keeps it (see discardCacheFromAnotherBuild) and the UI it gates
            // stays the one this APK ships.
            val build = bundledMeta.takeIf { it !== BundleMeta.EMPTY } ?: meta
            val updatedMeta = meta.copy(
                playlistUrl = playlistUrl,
                guideUrl = guideUrl,
                version = build.version,
                libraryScope = build.libraryScope,
                previewFeatures = build.previewFeatures,
                publishedOrder = build.publishedOrder.ifEmpty { meta.publishedOrder },
            )
            val library = buildLibrary(channels, programmes, updatedMeta, refreshed = true)
            writeCache(library)
            saveValidator(PLAYLIST_VALIDATOR, playlistUrl, playlistDownload)
            saveValidator(GUIDE_VALIDATOR, guideUrl, guideDownload)
            _state.value = LoadState.Ready(library)

            val message = if (isManual) {
                "Force refresh complete: ${library.channels.size} channels and " +
                    "${library.meta.programmeCount} guide listings loaded."
            } else {
                "Background refresh complete: ${library.channels.size} channels and " +
                    "${library.meta.programmeCount} guide listings loaded."
            }
            return finishRefresh(trigger, true, message, changed = true)
        } catch (e: Exception) {
            Log.w(TAG, "${trigger.name} refresh failed; keeping the current app data", e)
            val retryable = isRetryable(e)
            return finishRefresh(
                trigger = trigger,
                successful = false,
                message = refreshFailureMessage(e),
                retryable = retryable,
            )
        } catch (e: OutOfMemoryError) {
            // The half-built lists are garbage once this frame unwinds; the
            // library on screen was never replaced.
            Log.e(TAG, "${trigger.name} refresh ran out of memory; keeping the current app data", e)
            return finishRefresh(
                trigger = trigger,
                successful = false,
                message = "Refresh needed more memory than this device allows; the current app data was kept.",
                retryable = false,
            )
        }
    }

    private fun beginRefresh(trigger: RefreshTrigger) {
        val now = System.currentTimeMillis()
        preferences.edit()
            .putLong(KEY_LAST_ATTEMPT, now)
            .putString(KEY_LAST_TRIGGER, trigger.name)
            .apply()
        _refreshInfo.value = _refreshInfo.value.copy(
            inProgress = true,
            lastAttemptAtMillis = now,
            lastTrigger = trigger,
            lastMessage = if (trigger == RefreshTrigger.Manual) {
                "Force refresh is running."
            } else {
                "Automatic background refresh is running."
            },
        )
    }

    private fun finishRefresh(
        trigger: RefreshTrigger,
        successful: Boolean,
        message: String,
        changed: Boolean = false,
        retryable: Boolean = false,
    ): RefreshOutcome {
        val now = System.currentTimeMillis()
        val editor = preferences.edit()
            .putLong(KEY_LAST_ATTEMPT, now)
            .putString(KEY_LAST_TRIGGER, trigger.name)
            .putString(KEY_LAST_MESSAGE, message)
        if (successful) editor.putLong(KEY_LAST_SUCCESS, now)
        editor.apply()

        _refreshInfo.value = _refreshInfo.value.copy(
            inProgress = false,
            lastAttemptAtMillis = now,
            lastSuccessAtMillis = if (successful) now else _refreshInfo.value.lastSuccessAtMillis,
            lastTrigger = trigger,
            lastMessage = message,
        )
        _status.value = message
        return RefreshOutcome(
            successful = successful,
            changed = changed,
            retryable = retryable,
        )
    }

    private fun readRefreshInfo(): RefreshInfo {
        val trigger = preferences.getString(KEY_LAST_TRIGGER, null)?.let { saved ->
            RefreshTrigger.entries.firstOrNull { it.name == saved }
        }
        return RefreshInfo(
            lastAttemptAtMillis = preferences.getLong(KEY_LAST_ATTEMPT, 0L),
            lastSuccessAtMillis = preferences.getLong(KEY_LAST_SUCCESS, 0L),
            nextAutomaticAtMillis = preferences.getLong(KEY_NEXT_AUTOMATIC, 0L),
            lastTrigger = trigger,
            lastMessage = preferences.getString(KEY_LAST_MESSAGE, null)
                ?: "Automatic refresh has not run yet.",
        )
    }

    // ---------------------------------------------------------------- reading

    /** Reads the APK's bundle and publishes channels before parsing the guide. */
    private fun readBundled(onChannelsReady: (Library) -> Unit): Library =
        readLibrary(
            open = { name -> app.assets.open("bundle/$name") },
            refreshed = false,
            onChannelsReady = onChannelsReady,
        )

    /**
     * Drops a downloaded copy that another build wrote.
     *
     * Every cache records the version and library scope of the bundle it was
     * refreshed from. A copy whose version or scope differs from this APK's
     * bundle belongs to an earlier install - typically a 1.0.x USA refresh
     * after the global preview was installed over it, which kept showing the
     * old lineup and hid the preview's cable guide. Its validators go too, so
     * the next refresh downloads the new build's files in full.
     */
    private fun discardCacheFromAnotherBuild() {
        if (!cacheDir.isDirectory) return
        val bundle = bundledMeta
        if (bundle === BundleMeta.EMPTY) return
        val cached = try {
            File(cacheDir, "meta.json").takeIf { it.isFile }?.inputStream()?.use { parseMeta(it) }
        } catch (e: Exception) {
            null
        }
        if (cached != null && cached.version == bundle.version && cached.libraryScope == bundle.libraryScope) {
            return
        }
        Log.i(
            TAG,
            "Discarding the downloaded ${cached?.version ?: "unknown"}/${cached?.libraryScope ?: "unknown"} " +
                "copy; this APK ships ${bundle.version}/${bundle.libraryScope}",
        )
        cacheDir.deleteRecursively()
        clearValidators()
    }

    /** Reads the downloaded copy, or returns null so the caller uses the APK's bundle. */
    private fun readCache(onChannelsReady: (Library) -> Unit): Library? {
        if (!cacheDir.isDirectory) return null
        return try {
            readLibrary(
                open = { name ->
                    val file = File(cacheDir, name)
                    if (file.isFile) file.inputStream() else null
                },
                refreshed = true,
                onChannelsReady = onChannelsReady,
            )
        } catch (e: Exception) {
            Log.w(TAG, "Downloaded channels are unreadable; using the bundled data", e)
            cacheDir.deleteRecursively()
            clearValidators()
            null
        }
    }

    /**
     * Parses the required channel list first, then publishes it while the guide
     * is parsed. A missing or damaged guide is non-fatal: the channel browser
     * still opens and reports that listings are unavailable.
     */
    private fun readLibrary(
        open: (String) -> InputStream?,
        refreshed: Boolean,
        onChannelsReady: (Library) -> Unit,
    ): Library {
        fun stream(name: String): InputStream =
            open(name) ?: throw FileNotFoundException("$name is missing")

        val readMeta = try {
            open("meta.json")?.use { parseMeta(it) } ?: BundleMeta.EMPTY
        } catch (e: Exception) {
            Log.w(TAG, "Bundle metadata is unavailable; continuing with defaults", e)
            BundleMeta.EMPTY
        }
        // Which preview UI shows is a property of the APK, not of the data.
        val meta = if (refreshed && bundledMeta !== BundleMeta.EMPTY) {
            readMeta.copy(previewFeatures = bundledMeta.previewFeatures)
        } else {
            readMeta
        }
        val channels = readJsonLines(stream("channels.jsonl")) { parseChannel(it) }
        if (channels.isEmpty()) throw IOException("channels.jsonl holds no channels")

        val loadedGroups = try {
            open("groups.jsonl")?.use { input ->
                readJsonLines(input) { parseGroup(it) }
            }.orEmpty()
        } catch (e: Exception) {
            Log.w(TAG, "Category metadata is unreadable; deriving categories from channels", e)
            emptyList()
        }
        val groups = loadedGroups.ifEmpty { groupsFrom(channels, meta.publishedOrder) }

        val partial = Library(
            channels = channels,
            groups = groups,
            programmes = emptyMap(),
            meta = meta,
            refreshed = refreshed,
            guideLoading = true,
        )
        onChannelsReady(partial)

        return try {
            val programmes = readJsonLines(stream("epg.jsonl")) { parseProgramme(it) }
            val byChannel = groupProgrammes(programmes, HashSet(channels.map { it.id }))
            partial.copy(programmes = byChannel, guideLoading = false)
        } catch (e: Exception) {
            Log.w(TAG, "Programme guide is unreadable; keeping the channel list available", e)
            partial.copy(
                guideLoading = false,
                guideError = "Programme listings could not be loaded. Channels are still available.",
            )
        }
    }

    private fun parseMeta(stream: InputStream): BundleMeta {
        val json = JSONObject(stream.bufferedReader().readText())
        val features = json.optJSONArray("preview_features")
        val previewFeatures = buildSet {
            for (index in 0 until (features?.length() ?: 0)) {
                features?.optString(index)?.trim()?.takeIf { it.isNotEmpty() }?.let { add(it) }
            }
        }
        val order = json.optJSONArray("published_order")
        val publishedOrder = buildList {
            for (index in 0 until (order?.length() ?: 0)) {
                order?.optString(index)?.trim()?.takeIf { it.isNotEmpty() }?.let { add(it) }
            }
        }
        return BundleMeta(
            version = json.optString("version", "1.0.0"),
            generatedUtc = json.optString("generated_utc", ""),
            playlist = json.optString("playlist", ""),
            guide = json.optString("guide", ""),
            channelCount = json.optInt("channel_count", 0),
            groupCount = json.optInt("group_count", 0),
            programmeCount = json.optInt("programme_count", 0),
            guideChannels = json.optInt("guide_channels", 0),
            windowStart = json.optLong("window_start", 0L),
            windowEnd = json.optLong("window_end", 0L),
            playlistUrl = json.optString("playlist_url", ""),
            guideUrl = json.optString("guide_url", ""),
            rawBase = json.optString("raw_base", ""),
            libraryScope = json.optString("library_scope", "usa"),
            previewFeatures = previewFeatures,
            publishedOrder = publishedOrder,
        )
    }

    // ---------------------------------------------------------------- writing

    private fun buildLibrary(
        channels: List<Channel>,
        programmes: List<Programme>,
        base: BundleMeta,
        refreshed: Boolean,
    ): Library {
        val now = System.currentTimeMillis() / 1000L
        val known = HashSet(channels.map { it.id })
        val kept = programmes.filter { known.contains(it.channelId) && it.end > now - 6 * 3600L }
        val byChannel = groupProgrammes(kept, known)
        val groups = groupsFrom(channels, base.publishedOrder)
        val meta = base.copy(
            channelCount = channels.size,
            groupCount = groups.size,
            programmeCount = kept.size,
            guideChannels = byChannel.size,
            windowStart = kept.minOfOrNull { it.start } ?: now,
            windowEnd = kept.maxOfOrNull { it.end } ?: now,
            generatedUtc = stamp(),
        )
        return Library(
            channels = channels,
            groups = groups,
            programmes = byChannel,
            meta = meta,
            refreshed = refreshed,
        )
    }

    private fun groupProgrammes(
        programmes: List<Programme>,
        known: Set<String>,
    ): Map<String, List<Programme>> {
        val out = HashMap<String, ArrayList<Programme>>()
        for (programme in programmes) {
            if (!known.contains(programme.channelId)) continue
            out.getOrPut(programme.channelId) { ArrayList() }.add(programme)
        }
        for (list in out.values) list.sortBy { it.start }
        return out
    }

    /**
     * Categories in the published order (as android/tools/build_bundle.py
     * writes groups.jsonl), then any others by size. Without the order a
     * refresh used to re-sort the Channels tab and the guide by size.
     */
    private fun groupsFrom(channels: List<Channel>, publishedOrder: List<String> = emptyList()): List<CategoryGroup> {
        val counts = LinkedHashMap<String, Int>()
        for (channel in channels) {
            counts[channel.group] = (counts[channel.group] ?: 0) + 1
        }
        val published = publishedOrder.filter { counts.containsKey(it) }.distinct()
        val publishedSet = published.toHashSet()
        val rest = counts.entries
            .filter { it.key !in publishedSet }
            .sortedWith(compareByDescending<Map.Entry<String, Int>> { it.value }.thenBy { it.key.lowercase() })
            .map { it.key }
        return (published + rest).map { CategoryGroup(it, counts[it] ?: 0) }
    }

    /** Writes a complete staging directory, then swaps it into place atomically. */
    private fun writeCache(library: Library) {
        stagingCacheDir.deleteRecursively()
        backupCacheDir.deleteRecursively()
        if (!stagingCacheDir.mkdirs() && !stagingCacheDir.isDirectory) {
            throw IOException("could not create the refresh staging directory")
        }

        File(stagingCacheDir, "meta.json").writeText(metaToJson(library.meta))
        writeLines(File(stagingCacheDir, "channels.jsonl"), library.channels.asSequence().map { channelToJson(it) })
        writeLines(File(stagingCacheDir, "groups.jsonl"), library.groups.asSequence().map { groupToJson(it) })
        // One line at a time: the global guide is ~100k listings.
        writeLines(
            File(stagingCacheDir, "epg.jsonl"),
            library.programmes.values.asSequence().flatten().map { programmeToJson(it) },
        )

        var oldMoved = false
        if (cacheDir.exists()) {
            oldMoved = cacheDir.renameTo(backupCacheDir)
            if (!oldMoved) throw IOException("could not prepare the existing refresh cache")
        }
        if (!stagingCacheDir.renameTo(cacheDir)) {
            if (oldMoved) backupCacheDir.renameTo(cacheDir)
            throw IOException("could not publish the refreshed app data")
        }
        backupCacheDir.deleteRecursively()
    }

    /** Restores the old complete cache if the process stopped midway through a swap. */
    private fun recoverInterruptedCacheWrite() {
        if (!cacheDir.exists() && backupCacheDir.isDirectory) {
            backupCacheDir.renameTo(cacheDir)
        }
        stagingCacheDir.deleteRecursively()
        if (cacheDir.exists()) backupCacheDir.deleteRecursively()
    }

    private fun writeLines(file: File, lines: Sequence<String>) {
        file.bufferedWriter().use { writer ->
            for (line in lines) {
                writer.write(line)
                writer.write("\n")
            }
        }
    }

    private fun channelToJson(channel: Channel): String {
        val json = JSONObject()
        json.put("id", channel.id)
        json.put("name", channel.name)
        json.put("logo", channel.logo)
        json.put("group", channel.group)
        json.put("country", channel.country)
        json.put("chno", channel.chno)
        json.put("url", channel.url)
        json.put("ua", channel.userAgent)
        json.put("referrer", channel.referrer)
        json.put("origin", channel.origin)
        return json.toString()
    }

    private fun groupToJson(group: CategoryGroup): String {
        val json = JSONObject()
        json.put("name", group.name)
        json.put("count", group.count)
        return json.toString()
    }

    private fun programmeToJson(programme: Programme): String {
        val json = JSONObject()
        json.put("c", programme.channelId)
        json.put("s", programme.start)
        json.put("e", programme.end)
        json.put("t", programme.title)
        json.put("d", programme.desc)
        json.put("g", programme.category)
        json.put("i", programme.icon)
        json.put("ep", programme.episode)
        return json.toString()
    }

    private fun metaToJson(meta: BundleMeta): String {
        val json = JSONObject()
        json.put("version", meta.version)
        json.put("generated_utc", meta.generatedUtc)
        json.put("playlist", meta.playlist)
        json.put("guide", meta.guide)
        json.put("channel_count", meta.channelCount)
        json.put("group_count", meta.groupCount)
        json.put("programme_count", meta.programmeCount)
        json.put("guide_channels", meta.guideChannels)
        json.put("window_start", meta.windowStart)
        json.put("window_end", meta.windowEnd)
        json.put("playlist_url", meta.playlistUrl)
        json.put("guide_url", meta.guideUrl)
        json.put("raw_base", meta.rawBase)
        json.put("library_scope", meta.libraryScope)
        json.put("preview_features", JSONArray(meta.previewFeatures.toList()))
        json.put("published_order", JSONArray(meta.publishedOrder))
        return json.toString()
    }

    // --------------------------------------------------------------- downloading

    private class Downloaded<T>(
        val body: T?,
        val etag: String,
        val lastModified: String,
        val notModified: Boolean,
    )

    private class HttpStatusException(
        val statusCode: Int,
        val sourceUrl: String,
    ) : IOException("HTTP $statusCode from $sourceUrl")

    /** Counts what it passes on and stops a download that outgrows [limit]. */
    private class LimitedInputStream(input: InputStream, private val limit: Long) : FilterInputStream(input) {
        private var count = 0L

        private fun advance(read: Long) {
            if (read > 0) {
                count += read
                if (count > limit) throw IOException("the downloaded file exceeds the app's safety limit")
            }
        }

        override fun read(): Int {
            val value = super.read()
            if (value >= 0) advance(1)
            return value
        }

        override fun read(buffer: ByteArray, offset: Int, length: Int): Int {
            val read = super.read(buffer, offset, length)
            advance(read.toLong())
            return read
        }

        override fun skip(n: Long): Long {
            val skipped = super.skip(n)
            advance(skipped)
            return skipped
        }
    }

    /**
     * GETs [urlString] and hands the body stream to [read] while the connection
     * is open, so a large guide is parsed as it arrives instead of being held
     * as text first. A conditional request sends the saved validators and
     * returns [Downloaded.notModified] on HTTP 304.
     */
    private fun <T> download(
        urlString: String,
        validatorName: String,
        conditional: Boolean,
        maxBytes: Long,
        read: (InputStream) -> T,
    ): Downloaded<T> {
        val connection = URL(urlString).openConnection() as HttpURLConnection
        val savedUrl = preferences.getString("${validatorName}_url", "").orEmpty()
        val savedEtag = preferences.getString("${validatorName}_etag", "").orEmpty()
        val savedModified = preferences.getString("${validatorName}_modified", "").orEmpty()

        return try {
            connection.connectTimeout = 20_000
            connection.readTimeout = 90_000
            connection.instanceFollowRedirects = true
            connection.setRequestProperty(
                "User-Agent",
                "PremiumTV/${BuildConfig.VERSION_NAME} (Android ${Build.VERSION.RELEASE})",
            )
            if (conditional && savedUrl == urlString) {
                if (savedEtag.isNotBlank()) connection.setRequestProperty("If-None-Match", savedEtag)
                if (savedModified.isNotBlank()) {
                    connection.setRequestProperty("If-Modified-Since", savedModified)
                }
            }

            val code = connection.responseCode
            if (code == HttpURLConnection.HTTP_NOT_MODIFIED) {
                Downloaded(
                    body = null,
                    etag = connection.getHeaderField("ETag").orEmpty().ifBlank { savedEtag },
                    lastModified = connection.getHeaderField("Last-Modified").orEmpty()
                        .ifBlank { savedModified },
                    notModified = true,
                )
            } else {
                if (code !in 200..299) throw HttpStatusException(code, urlString)
                val announcedLength = connection.contentLengthLong
                if (announcedLength > maxBytes) {
                    throw IOException("the downloaded file is unexpectedly large")
                }
                val body = LimitedInputStream(connection.inputStream, maxBytes).buffered(64 * 1024).use { read(it) }
                Downloaded(
                    body = body,
                    etag = connection.getHeaderField("ETag").orEmpty(),
                    lastModified = connection.getHeaderField("Last-Modified").orEmpty(),
                    notModified = false,
                )
            }
        } finally {
            connection.disconnect()
        }
    }

    private fun saveValidator(name: String, url: String, result: Downloaded<*>) {
        preferences.edit()
            .putString("${name}_url", url)
            .putString("${name}_etag", result.etag)
            .putString("${name}_modified", result.lastModified)
            .apply()
    }

    private fun clearValidators() {
        preferences.edit()
            .remove("${PLAYLIST_VALIDATOR}_url")
            .remove("${PLAYLIST_VALIDATOR}_etag")
            .remove("${PLAYLIST_VALIDATOR}_modified")
            .remove("${GUIDE_VALIDATOR}_url")
            .remove("${GUIDE_VALIDATOR}_etag")
            .remove("${GUIDE_VALIDATOR}_modified")
            .apply()
    }

    private fun isRetryable(error: Exception): Boolean = when (error) {
        is HttpStatusException -> error.statusCode == 408 || error.statusCode == 425 ||
            error.statusCode == 429 || error.statusCode in 500..599
        is IOException -> true
        else -> false
    }

    private fun refreshFailureMessage(error: Exception): String = when (error) {
        is HttpStatusException -> when (error.statusCode) {
            401, 403, 404 -> "Refresh could not download ${error.sourceUrl} (HTTP ${error.statusCode}). " +
                "The current app data was kept."
            else -> "Refresh failed with HTTP ${error.statusCode}; the current app data was kept."
        }
        else -> "Refresh failed: ${error.message ?: error.javaClass.simpleName}. " +
            "The current app data was kept."
    }

    private fun stamp(): String {
        val formatter = SimpleDateFormat("yyyy-MM-dd HH:mm 'UTC'", Locale.US)
        formatter.timeZone = TimeZone.getTimeZone("UTC")
        return formatter.format(Date())
    }
}
