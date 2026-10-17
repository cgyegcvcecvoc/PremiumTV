package com.premiumtv.app.update

import android.app.Application
import android.content.Context
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
import java.io.FileOutputStream
import java.io.IOException
import java.net.HttpURLConnection
import java.net.URL
import java.security.MessageDigest

/**
 * What Settings shows about app updates, and what the download button does.
 *
 * Update policy (shared with the Mac app and enforced by the release guard):
 *  - only a published *stable* GitHub release counts - drafts and pre-releases
 *    are ignored;
 *  - its version must be numerically above this APK's version;
 *  - its Android APK and checksum file must already be attached.
 *
 * The automatic check runs at most once a day and sends the last ETag, so a
 * normal launch usually costs one tiny `304 Not Modified` response.  Nothing
 * is downloaded in the background: the installer is fetched only when the
 * user presses the button in Settings, and an already-downloaded installer for
 * the same version is reused instead of downloaded again.
 */
class AppUpdateManager(private val app: Application) {

    companion object {
        private const val TAG = "PremiumTV"
        const val RELEASES_API =
            "https://api.github.com/repos/cgyegcvcecvoc/PremiumTV1/releases?per_page=30"
        const val CHECK_INTERVAL_MILLIS = 24L * 60L * 60L * 1000L
        private const val RETRY_INTERVAL_MILLIS = 60L * 60L * 1000L
        private const val MAX_API_BYTES = 2L * 1024L * 1024L
        private const val MAX_CHECKSUM_BYTES = 256L * 1024L

        private const val PREFS = "premiumtv_app_update"
        private const val KEY_APP_VERSION = "app_version"
        private const val KEY_ETAG = "etag"
        private const val KEY_LAST_CHECKED = "last_checked_ms"
        private const val KEY_NEXT_CHECK = "next_check_ms"
        private const val KEY_LATEST_STABLE = "latest_stable"
        private const val KEY_AVAILABLE = "available_version"
        private const val KEY_RELEASE_URL = "release_url"
        private const val KEY_APK_URL = "apk_url"
        private const val KEY_CHECKSUM_URL = "checksum_url"
        private const val KEY_APK_SIZE = "apk_size"
        private const val KEY_DOWNLOADED = "downloaded_version"
        private const val KEY_MESSAGE = "message"
    }

    private val preferences = app.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
    private val operations = Mutex()

    private val _state = MutableStateFlow(loadState())
    val state: StateFlow<AppUpdateState> = _state

    /** Called at startup; the 24-hour throttle keeps this off the network. */
    suspend fun checkIfDue() {
        check(force = false)
    }

    /** Settings → Check for updates. A manual check always asks GitHub. */
    suspend fun check(force: Boolean): AppUpdateState = withContext(Dispatchers.IO) {
        operations.withLock { checkLocked(force) }
    }

    /** Settings → Download update. Reuses a verified installer for this version. */
    suspend fun download(): AppUpdateState = withContext(Dispatchers.IO) {
        operations.withLock { downloadLocked() }
    }

    /**
     * Settings → Install update. Returns an error message, or null when
     * Android's package installer was opened.
     */
    fun installDownloaded(): String? {
        val version = _state.value.downloadedVersion
        if (version == null) {
            val message = "Download the update first."
            publish(_state.value.copy(message = message, error = message))
            return message
        }
        val file = installerFile(version)
        if (!file.isFile || file.length() <= 0L) {
            val message = "The downloaded installer is missing. Check for updates again."
            publish(_state.value.copy(downloadedVersion = null, message = message, error = message))
            return message
        }
        val error = UpdateInstaller.install(app, file)
        val message = error
            ?: "Android's package installer is open. Confirm the update, then reopen PremiumTV."
        publish(_state.value.copy(message = message, error = error))
        return error
    }

    // --------------------------------------------------------------- checking

    private fun checkLocked(force: Boolean): AppUpdateState {
        val now = System.currentTimeMillis()
        val before = _state.value
        if (!force && now < before.nextCheckAtMillis) return before

        _state.value = before.copy(
            checking = true,
            error = null,
            message = "Checking GitHub for a new stable release…",
        )

        var connection: HttpURLConnection? = null
        return try {
            val opened = request(RELEASES_API)
            connection = opened
            val etag = preferences.getString(KEY_ETAG, null)
            if (!force && !etag.isNullOrBlank()) {
                opened.setRequestProperty("If-None-Match", etag)
            }
            when (val code = opened.responseCode) {
                HttpURLConnection.HTTP_NOT_MODIFIED -> {
                    val message = when {
                        before.updateAvailable ->
                            "PremiumTV ${before.availableVersion} is still the newest stable release."
                        else -> before.message.ifBlank { "PremiumTV is up to date." }
                    }
                    publish(
                        _state.value.copy(
                            checking = false,
                            lastCheckedAtMillis = now,
                            nextCheckAtMillis = now + CHECK_INTERVAL_MILLIS,
                            message = message,
                            error = null,
                        )
                    )
                }

                HttpURLConnection.HTTP_OK -> {
                    val body = readBody(opened, MAX_API_BYTES)
                    opened.getHeaderField("ETag")?.let {
                        preferences.edit().putString(KEY_ETAG, it).apply()
                    }
                    val selected = selectUpdate(body, before.currentVersion)
                    publish(
                        _state.value.copy(
                            checking = false,
                            lastCheckedAtMillis = now,
                            nextCheckAtMillis = now + CHECK_INTERVAL_MILLIS,
                            latestStableVersion = selected.latestStableVersion,
                            availableVersion = selected.availableVersion,
                            releaseUrl = selected.releaseUrl,
                            installerUrl = selected.installerUrl,
                            checksumUrl = selected.checksumUrl,
                            installerSize = selected.installerSize,
                            // A verified installer for this exact version survives
                            // a re-check; nothing needs downloading again.
                            downloadedVersion = _state.value.downloadedVersion
                                ?.takeIf { it == selected.availableVersion },
                            message = selected.message,
                            error = null,
                        )
                    )
                }

                else -> throw IOException("GitHub returned HTTP $code")
            }
        } catch (e: Exception) {
            Log.w(TAG, "The app update check failed", e)
            val message = "Could not check for updates: " +
                (e.message ?: e.javaClass.simpleName) +
                ". PremiumTV keeps working from the installed version."
            publish(
                _state.value.copy(
                    checking = false,
                    lastCheckedAtMillis = now,
                    nextCheckAtMillis = now + RETRY_INTERVAL_MILLIS,
                    message = message,
                    error = message,
                )
            )
        } finally {
            connection?.disconnect()
        }
    }

    private data class SelectedUpdate(
        val latestStableVersion: String?,
        val availableVersion: String? = null,
        val releaseUrl: String? = null,
        val installerUrl: String? = null,
        val checksumUrl: String? = null,
        val installerSize: Long = 0L,
        val message: String,
    )

    /**
     * Pick the newest complete stable release above [currentVersion].
     *
     * The release list can contain drafts, pre-releases and releases whose
     * build jobs are still uploading. All three are skipped: an update is
     * offered only when its exact APK name is already attached.
     */
    private fun selectUpdate(body: String, currentVersion: String): SelectedUpdate {
        val releases = try {
            JSONArray(body)
        } catch (e: Exception) {
            throw IOException("GitHub's release list was not valid JSON", e)
        }

        var newestStable: String? = null
        var bestVersion: String? = null
        var bestReleaseUrl: String? = null
        var bestApkUrl: String? = null
        var bestChecksumUrl: String? = null
        var bestSize = 0L

        for (index in 0 until releases.length()) {
            val release = releases.optJSONObject(index) ?: continue
            if (release.optBoolean("draft") || release.optBoolean("prerelease")) continue
            val version = AppVersions.normalize(release.optString("tag_name")) ?: continue
            if (newestStable == null || AppVersions.isNewer(version, newestStable)) {
                newestStable = version
            }
            if (!AppVersions.isNewer(version, currentVersion)) continue

            val assets = release.optJSONArray("assets") ?: continue
            val apk = findAsset(assets, "PremiumTV-$version-debug.apk") ?: continue
            val apkUrl = apk.optString("browser_download_url")
            if (!apkUrl.startsWith("https://")) continue
            val checksum = findAsset(assets, "SHA256SUMS-android.txt")
            val checksumUrl = checksum?.optString("browser_download_url")
                ?.takeIf { it.startsWith("https://") }

            if (bestVersion == null || AppVersions.isNewer(version, bestVersion)) {
                bestVersion = version
                bestReleaseUrl = release.optString("html_url").takeIf { it.startsWith("https://") }
                bestApkUrl = apkUrl
                bestChecksumUrl = checksumUrl
                bestSize = apk.optLong("size", 0L)
            }
        }

        val message = when {
            bestVersion != null ->
                "PremiumTV $bestVersion is available (installed: $currentVersion)."
            newestStable == null ->
                "No stable release was found on GitHub."
            AppVersions.isNewer(newestStable!!, currentVersion) ->
                "PremiumTV $newestStable is newer, but its Android APK has not finished uploading yet."
            AppVersions.isNewer(currentVersion, newestStable!!) ->
                "This build ($currentVersion) is a preview above the newest stable release ($newestStable)."
            else ->
                "PremiumTV $currentVersion is the newest stable release."
        }

        return SelectedUpdate(
            latestStableVersion = newestStable,
            availableVersion = bestVersion,
            releaseUrl = bestReleaseUrl,
            installerUrl = bestApkUrl,
            checksumUrl = bestChecksumUrl,
            installerSize = bestSize,
            message = message,
        )
    }

    private fun findAsset(assets: JSONArray, name: String): JSONObject? {
        for (index in 0 until assets.length()) {
            val asset = assets.optJSONObject(index) ?: continue
            if (asset.optString("name") == name) return asset
        }
        return null
    }

    // ------------------------------------------------------------- downloading

    private fun downloadLocked(): AppUpdateState {
        val before = _state.value
        val version = before.availableVersion
        if (version == null) {
            val message = "No newer stable release is available to download."
            return publish(before.copy(message = message, error = message))
        }

        val target = installerFile(version)
        if (before.downloadedVersion == version && target.isFile && target.length() > 0L) {
            return publish(
                before.copy(
                    downloading = false,
                    progressPercent = 100,
                    message = "PremiumTV $version is already downloaded and verified. " +
                        "Press Install update; it will not be downloaded again.",
                    error = null,
                )
            )
        }

        val apkUrl = before.installerUrl
        if (apkUrl.isNullOrBlank()) {
            val message = "The release has no Android APK to download."
            return publish(before.copy(message = message, error = message))
        }

        val directory = updatesDir().apply { mkdirs() }
        val part = File(directory, "${target.name}.part")
        part.delete()
        _state.value = before.copy(
            downloading = true,
            progressPercent = 0,
            error = null,
            message = "Downloading PremiumTV $version…",
        )

        var connection: HttpURLConnection? = null
        return try {
            val opened = request(apkUrl)
            connection = opened
            opened.setRequestProperty("Accept", "application/octet-stream")
            val code = opened.responseCode
            if (code != HttpURLConnection.HTTP_OK) throw IOException("GitHub returned HTTP $code")
            val total = opened.getHeaderField("Content-Length")?.toLongOrNull() ?: -1L
            var copied = 0L
            opened.inputStream.use { input ->
                FileOutputStream(part).use { output ->
                    val buffer = ByteArray(64 * 1024)
                    while (true) {
                        val read = input.read(buffer)
                        if (read < 0) break
                        output.write(buffer, 0, read)
                        copied += read
                        if (total > 0L) {
                            val percent = ((copied * 100L) / total).toInt().coerceIn(0, 99)
                            if (percent != _state.value.progressPercent) {
                                _state.value = _state.value.copy(
                                    progressPercent = percent,
                                    message = "Downloading PremiumTV $version… $percent%",
                                )
                            }
                        }
                    }
                }
            }
            if (part.length() <= 0L) throw IOException("the downloaded installer was empty")
            verifyChecksum(part, target.name)
            if (target.exists() && !target.delete()) {
                throw IOException("could not replace the previous installer")
            }
            if (!part.renameTo(target)) throw IOException("could not save the downloaded installer")

            // Keep exactly one installer; it is reused until it is installed.
            directory.listFiles()?.forEach { file ->
                if (file.name != target.name) file.delete()
            }

            publish(
                _state.value.copy(
                    downloading = false,
                    progressPercent = 100,
                    downloadedVersion = version,
                    message = "PremiumTV $version downloaded and verified. " +
                        "Press Install update to finish.",
                    error = null,
                )
            )
        } catch (e: Exception) {
            part.delete()
            Log.w(TAG, "The app update download failed", e)
            val message = "Update download failed: ${e.message ?: e.javaClass.simpleName}"
            publish(
                _state.value.copy(
                    downloading = false,
                    progressPercent = -1,
                    message = message,
                    error = message,
                )
            )
        } finally {
            connection?.disconnect()
        }
    }

    private fun verifyChecksum(file: File, assetName: String) {
        val checksumUrl = _state.value.checksumUrl
        if (checksumUrl.isNullOrBlank()) {
            throw IOException("the release has no SHA-256 checksum file")
        }
        var connection: HttpURLConnection? = null
        val body = try {
            val opened = request(checksumUrl)
            connection = opened
            val code = opened.responseCode
            if (code != HttpURLConnection.HTTP_OK) {
                throw IOException("the checksum request returned HTTP $code")
            }
            readBody(opened, MAX_CHECKSUM_BYTES)
        } finally {
            connection?.disconnect()
        }

        val expected = body.lineSequence()
            .map { it.trim() }
            .filter { it.isNotEmpty() }
            .mapNotNull { line ->
                val parts = line.split(Regex("\\s+"), limit = 2)
                if (parts.size == 2) {
                    parts[1].trim().removePrefix("*") to parts[0].trim()
                } else {
                    null
                }
            }
            .firstOrNull { it.first == assetName }
            ?.second
        if (expected.isNullOrBlank()) {
            throw IOException("the checksum file has no entry for $assetName")
        }
        if (!sha256(file).equals(expected, ignoreCase = true)) {
            throw IOException("the downloaded APK failed its SHA-256 check")
        }
    }

    private fun sha256(file: File): String {
        val digest = MessageDigest.getInstance("SHA-256")
        file.inputStream().use { input ->
            val buffer = ByteArray(64 * 1024)
            while (true) {
                val read = input.read(buffer)
                if (read < 0) break
                digest.update(buffer, 0, read)
            }
        }
        return digest.digest().joinToString("") { byte ->
            java.lang.String.format(java.util.Locale.US, "%02x", byte.toInt() and 0xff)
        }
    }

    // ----------------------------------------------------------------- helpers

    private fun updatesDir(): File = File(app.filesDir, "updates")

    private fun installerFile(version: String): File =
        File(updatesDir(), "PremiumTV-$version-debug.apk")

    private fun request(url: String): HttpURLConnection {
        val connection = URL(url).openConnection() as HttpURLConnection
        connection.connectTimeout = 15_000
        connection.readTimeout = 25_000
        connection.instanceFollowRedirects = true
        connection.setRequestProperty(
            "User-Agent",
            "PremiumTV/${BuildConfig.VERSION_NAME} (Android TV)",
        )
        connection.setRequestProperty("Accept", "application/vnd.github+json")
        return connection
    }

    private fun readBody(connection: HttpURLConnection, maxBytes: Long): String {
        connection.inputStream.bufferedReader(Charsets.UTF_8).use { reader ->
            val builder = StringBuilder()
            val buffer = CharArray(8 * 1024)
            var total = 0L
            while (true) {
                val read = reader.read(buffer)
                if (read < 0) break
                total += read
                if (total > maxBytes) throw IOException("the response was larger than expected")
                builder.append(buffer, 0, read)
            }
            return builder.toString()
        }
    }

    private fun publish(next: AppUpdateState): AppUpdateState {
        persist(next)
        _state.value = next
        return next
    }

    private fun persist(state: AppUpdateState) {
        preferences.edit()
            .putString(KEY_APP_VERSION, BuildConfig.VERSION_NAME)
            .putLong(KEY_LAST_CHECKED, state.lastCheckedAtMillis)
            .putLong(KEY_NEXT_CHECK, state.nextCheckAtMillis)
            .putString(KEY_LATEST_STABLE, state.latestStableVersion)
            .putString(KEY_AVAILABLE, state.availableVersion)
            .putString(KEY_RELEASE_URL, state.releaseUrl)
            .putString(KEY_APK_URL, state.installerUrl)
            .putString(KEY_CHECKSUM_URL, state.checksumUrl)
            .putLong(KEY_APK_SIZE, state.installerSize)
            .putString(KEY_DOWNLOADED, state.downloadedVersion)
            .putString(KEY_MESSAGE, state.message)
            .apply()
    }

    private fun loadState(): AppUpdateState {
        val current = AppVersions.normalize(BuildConfig.VERSION_NAME) ?: BuildConfig.VERSION_NAME
        if (preferences.getString(KEY_APP_VERSION, null) != BuildConfig.VERSION_NAME) {
            // A newly installed APK starts with a clean update memory. Any APK
            // downloaded for the previous version is obsolete.
            preferences.getString(KEY_DOWNLOADED, null)?.let { installerFile(it).delete() }
            preferences.edit()
                .clear()
                .putString(KEY_APP_VERSION, BuildConfig.VERSION_NAME)
                .apply()
        }

        var available = preferences.getString(KEY_AVAILABLE, null)
        if (available != null && !AppVersions.isNewer(available, current)) {
            available = null
        }
        var downloaded = preferences.getString(KEY_DOWNLOADED, null)
        if (downloaded != null && !installerFile(downloaded).isFile) {
            downloaded = null
        } else if (downloaded != null && downloaded != available) {
            // A completely downloaded newer installer is still useful if the
            // newest offer has not changed; otherwise it is stale.
            installerFile(downloaded).delete()
            downloaded = null
        }

        // Only one installer is kept, so an interrupted older attempt cannot
        // pile up multi-megabyte files on a TV stick.
        val keepName = downloaded?.let { installerFile(it).name }
        updatesDir().listFiles()?.forEach { file ->
            if (keepName == null || file.name != keepName) file.delete()
        }

        return AppUpdateState(
            currentVersion = current,
            latestStableVersion = preferences.getString(KEY_LATEST_STABLE, null),
            availableVersion = available,
            releaseUrl = preferences.getString(KEY_RELEASE_URL, null),
            installerUrl = preferences.getString(KEY_APK_URL, null),
            checksumUrl = preferences.getString(KEY_CHECKSUM_URL, null),
            installerSize = preferences.getLong(KEY_APK_SIZE, 0L),
            lastCheckedAtMillis = preferences.getLong(KEY_LAST_CHECKED, 0L),
            nextCheckAtMillis = preferences.getLong(KEY_NEXT_CHECK, 0L),
            downloadedVersion = downloaded,
            message = preferences.getString(KEY_MESSAGE, null)
                ?: "PremiumTV checks for a new stable release when the app starts, then once a day.",
        )
    }
}

/** Everything the Settings screen needs to describe an app update. */
data class AppUpdateState(
    val currentVersion: String,
    val latestStableVersion: String? = null,
    val availableVersion: String? = null,
    val releaseUrl: String? = null,
    val installerUrl: String? = null,
    val checksumUrl: String? = null,
    val installerSize: Long = 0L,
    val lastCheckedAtMillis: Long = 0L,
    val nextCheckAtMillis: Long = 0L,
    val checking: Boolean = false,
    val downloading: Boolean = false,
    val progressPercent: Int = -1,
    val downloadedVersion: String? = null,
    val message: String = "",
    val error: String? = null,
) {
    val updateAvailable: Boolean get() = availableVersion != null
    val installerReady: Boolean
        get() = downloadedVersion != null && downloadedVersion == availableVersion
    val busy: Boolean get() = checking || downloading
}
