package com.premiumtv.app.data

import android.app.Application
import android.os.Build
import com.premiumtv.app.BuildConfig
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.io.File
import java.io.FileNotFoundException
import java.io.IOException
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Owns the channel list and the guide.
 *
 * Two sources, one shape:
 *  - the bundle shipped inside the APK (android/app/src/main/assets/bundle),
 *    produced by android/tools/build_bundle.py from this repository;
 *  - a cache in the app's private files, written by [refresh].
 *
 * The cache wins when it exists, so a refresh survives a restart. Resetting in
 * Settings deletes it and falls back to what the APK shipped with.
 */
class TvRepository(private val app: Application) {

    private val _state = MutableStateFlow<LoadState>(LoadState.Loading)
    val state: StateFlow<LoadState> = _state

    private val _status = MutableStateFlow("")
    val status: StateFlow<String> = _status

    private val cacheDir: File get() = File(app.filesDir, "bundle")

    suspend fun load() = withContext(Dispatchers.IO) {
        _state.value = LoadState.Loading
        val library = readCache() ?: readBundled()
        _state.value = if (library != null) {
            LoadState.Ready(library)
        } else {
            LoadState.Error(
                "The bundled channel data is missing from this build.\n" +
                    "Run: python android/tools/build_bundle.py"
            )
        }
        if (library != null && library.refreshed) {
            _status.value = "Showing the copy downloaded from GitHub."
        }
    }

    /** Downloads the playlist and guide the bundle points at, then reloads. */
    suspend fun refresh() = withContext(Dispatchers.IO) {
        val meta = (_state.value as? LoadState.Ready)?.library?.meta
        val playlistUrl = meta?.playlistUrl.orEmpty()
        val guideUrl = meta?.guideUrl.orEmpty()
        if (playlistUrl.isBlank()) {
            _status.value = "This build has no update URL to fetch."
            return@withContext
        }

        try {
            _status.value = "Downloading playlist…"
            val playlist = downloadText(playlistUrl)

            _status.value = "Reading channels…"
            val (channels, headerGuide) = M3uParser.parse(playlist)
            if (channels.isEmpty()) throw IOException("the playlist contained no channels")

            _status.value = "Downloading guide…"
            val guide = downloadText(guideUrl.ifBlank { headerGuide })
            val programmes = XmlTvParser.parse(guide)

            val library = buildLibrary(channels, programmes, meta ?: BundleMeta.EMPTY, true)
            writeCache(library)
            _state.value = LoadState.Ready(library)
            _status.value = "Updated from GitHub: ${library.channels.size} channels, " +
                "${library.programmes.size} with listings."
        } catch (e: FileNotFoundException) {
            _status.value = "Update failed: the file was not found (HTTP 404). " +
                "The repository is private, so a TV cannot read raw GitHub links " +
                "until it is public or mirrored."
        } catch (e: Exception) {
            _status.value = "Update failed: ${e.message ?: e.javaClass.simpleName}"
        }
    }

    /** Drops the downloaded copy and goes back to what the APK shipped with. */
    suspend fun resetToBundled() = withContext(Dispatchers.IO) {
        cacheDir.deleteRecursively()
        _status.value = "Downloaded copy removed."
        load()
    }

    // ---------------------------------------------------------------- reading

    private fun readBundled(): Library? = try {
        readLibrary({ name -> app.assets.open("bundle/$name") }, refreshed = false)
    } catch (e: Exception) {
        null
    }

    private fun readCache(): Library? = try {
        if (!cacheDir.isDirectory) return null
        readLibrary(
            { name ->
                val file = File(cacheDir, name)
                if (file.isFile) file.inputStream() else null
            },
            refreshed = true
        )
    } catch (e: Exception) {
        null
    }

    private fun readLibrary(open: (String) -> InputStream?, refreshed: Boolean): Library? {
        val metaStream = open("meta.json") ?: return null
        val meta = parseMeta(metaStream)
        val channels = readJsonLines(open("channels.jsonl") ?: return null) { parseChannel(it) }
        val groups = readJsonLines(open("groups.jsonl") ?: return null) { parseGroup(it) }
        val programmes = readJsonLines(open("epg.jsonl") ?: return null) { parseProgramme(it) }
        if (channels.isEmpty()) return null
        val byChannel = groupProgrammes(programmes, HashSet(channels.map { it.id }))
        return Library(
            channels = channels,
            groups = groups.ifEmpty { groupsFrom(channels) },
            programmes = byChannel,
            meta = meta,
            refreshed = refreshed,
        )
    }

    private fun parseMeta(stream: InputStream): BundleMeta {
        val json = JSONObject(stream.bufferedReader().readText())
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
        val meta = base.copy(
            channelCount = channels.size,
            groupCount = groupsFrom(channels).size,
            programmeCount = kept.size,
            guideChannels = byChannel.size,
            windowStart = kept.minOfOrNull { it.start } ?: now,
            windowEnd = kept.maxOfOrNull { it.end } ?: now,
            generatedUtc = stamp(),
        )
        return Library(
            channels = channels,
            groups = groupsFrom(channels),
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

    private fun groupsFrom(channels: List<Channel>): List<CategoryGroup> {
        val counts = LinkedHashMap<String, Int>()
        for (channel in channels) {
            counts[channel.group] = (counts[channel.group] ?: 0) + 1
        }
        return counts.entries
            .sortedWith(compareByDescending<Map.Entry<String, Int>> { it.value }.thenBy { it.key.lowercase() })
            .map { CategoryGroup(it.key, it.value) }
    }

    private fun writeCache(library: Library) {
        cacheDir.deleteRecursively()
        cacheDir.mkdirs()
        File(cacheDir, "meta.json").writeText(metaToJson(library.meta))
        writeLines(File(cacheDir, "channels.jsonl"), library.channels.map { channelToJson(it) })
        writeLines(File(cacheDir, "groups.jsonl"), library.groups.map { groupToJson(it) })
        writeLines(
            File(cacheDir, "epg.jsonl"),
            library.programmes.values.flatten().map { programmeToJson(it) }
        )
    }

    private fun writeLines(file: File, lines: List<String>) {
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
        return json.toString()
    }

    // --------------------------------------------------------------- downloading

    private fun downloadText(urlString: String): String {
        val connection = URL(urlString).openConnection() as HttpURLConnection
        return try {
            connection.connectTimeout = 20_000
            connection.readTimeout = 90_000
            connection.instanceFollowRedirects = true
            connection.setRequestProperty(
                "User-Agent",
                "PremiumTV/${BuildConfig.VERSION_NAME} (Android ${Build.VERSION.RELEASE})"
            )
            val code = connection.responseCode
            if (code !in 200..299) throw IOException("HTTP $code from $urlString")
            connection.inputStream.bufferedReader().readText()
        } finally {
            connection.disconnect()
        }
    }

    private fun stamp(): String {
        return SimpleDateFormat("yyyy-MM-dd HH:mm 'UTC'", Locale.US).format(Date())
    }
}
