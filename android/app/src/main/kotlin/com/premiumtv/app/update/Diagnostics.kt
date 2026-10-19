package com.premiumtv.app.update

import com.premiumtv.app.data.Library
import com.premiumtv.app.data.RefreshInfo
import com.premiumtv.app.data.RefreshTrigger

/** One line of the built-in bug check shown in Settings. */
data class DiagnosticCheck(
    val label: String,
    val status: DiagnosticStatus,
    val detail: String,
)

enum class DiagnosticStatus { Ok, Warning, Problem }

/** The result of one "Check for bugs" run. */
data class DiagnosticsReport(
    val checks: List<DiagnosticCheck>,
    val ranAtMillis: Long = System.currentTimeMillis(),
) {
    val okCount: Int get() = checks.count { it.status == DiagnosticStatus.Ok }
    val warningCount: Int get() = checks.count { it.status == DiagnosticStatus.Warning }
    val problemCount: Int get() = checks.count { it.status == DiagnosticStatus.Problem }

    val headline: String
        get() = when {
            problemCount > 0 -> "$problemCount bug${plural(problemCount)} found"
            warningCount > 0 -> "No blocking bugs · $warningCount warning${plural(warningCount)}"
            else -> "All ${checks.size} checks passed"
        }

    private fun plural(count: Int) = if (count == 1) "" else "s"
}

/**
 * The Settings → Check for bugs action.
 *
 * This is deliberately offline and read-only: it inspects the library the app
 * is actually showing, the last refresh result and the update checker's state,
 * then reports specific, actionable findings. It never downloads anything or
 * changes the cache, so pressing it on a TV cannot make a working install worse.
 */
object Diagnostics {

    fun run(
        library: Library,
        refresh: RefreshInfo,
        update: AppUpdateState,
        installedVersion: String,
    ): DiagnosticsReport {
        val checks = mutableListOf<DiagnosticCheck>()
        val meta = library.meta

        // ---------------------------------------------------------- channels
        val blankChannels = library.channels.count { it.name.isBlank() || it.url.isBlank() }
        val badSchemes = library.channels.count { !it.url.startsWith("https://") && !it.url.startsWith("http://") }
        val duplicateUrls = library.channels.groupingBy { it.url }.eachCount().count { it.value > 1 }
        val channelStatus = when {
            library.channels.isEmpty() -> DiagnosticStatus.Problem
            blankChannels > 0 || badSchemes > 0 -> DiagnosticStatus.Problem
            duplicateUrls > 0 -> DiagnosticStatus.Warning
            else -> DiagnosticStatus.Ok
        }
        checks += DiagnosticCheck(
            label = "Channel list",
            status = channelStatus,
            detail = when (channelStatus) {
                DiagnosticStatus.Problem -> when {
                    library.channels.isEmpty() -> "No channels were loaded."
                    blankChannels > 0 -> "$blankChannels channel(s) have no name or stream URL."
                    else -> "$badSchemes channel(s) have an unusable stream URL."
                }
                DiagnosticStatus.Warning -> "$duplicateUrls duplicate stream URL(s) in the library."
                else -> "${library.channels.size} channels, every entry playable in format."
            },
        )

        // -------------------------------------------------------- categories
        val groupNames = library.groups.map { it.name }.toSet()
        val ungrouped = library.channels.count { it.group.isNotBlank() && it.group !in groupNames }
        val categoryStatus = when {
            library.groups.isEmpty() -> DiagnosticStatus.Problem
            ungrouped > 0 -> DiagnosticStatus.Warning
            else -> DiagnosticStatus.Ok
        }
        checks += DiagnosticCheck(
            label = "Categories",
            status = categoryStatus,
            detail = when (categoryStatus) {
                DiagnosticStatus.Problem -> "No categories were published."
                DiagnosticStatus.Warning -> "$ungrouped channel(s) name a category that is not in the sidebar."
                else -> "${library.groups.size} categories, every channel grouped."
            },
        )

        // ------------------------------------------------------------ guide
        val guideStatus = when {
            library.guideError != null -> DiagnosticStatus.Warning
            library.guideLoading -> DiagnosticStatus.Warning
            library.programmes.isEmpty() -> DiagnosticStatus.Problem
            meta.guideChannels == 0 -> DiagnosticStatus.Warning
            else -> DiagnosticStatus.Ok
        }
        checks += DiagnosticCheck(
            label = "TV guide",
            status = guideStatus,
            detail = when {
                library.guideError != null -> "Guide unavailable: ${library.guideError}"
                library.guideLoading -> "The guide is still loading; channels remain usable."
                library.programmes.isEmpty() -> "No programme listings parsed."
                else -> "${library.programmes.values.sumOf { it.size }} listings across ${meta.guideChannels} channels."
            },
        )

        // ----------------------------------------------------- bundled data
        val sourceProblems = buildList {
            if (!meta.playlistUrl.startsWith("https://")) add("playlist URL")
            if (!meta.guideUrl.startsWith("https://")) add("guide URL")
            if (meta.version.isBlank()) add("bundle version")
        }
        val bundleStatus = when {
            sourceProblems.isNotEmpty() -> DiagnosticStatus.Problem
            meta.channelCount > 0 && meta.channelCount != library.channels.size && !library.refreshed ->
                DiagnosticStatus.Warning
            else -> DiagnosticStatus.Ok
        }
        checks += DiagnosticCheck(
            label = "Data bundle",
            status = bundleStatus,
            detail = when {
                sourceProblems.isNotEmpty() -> "Missing ${sourceProblems.joinToString()}."
                bundleStatus == DiagnosticStatus.Warning ->
                    "Bundle declares ${meta.channelCount} channels but ${library.channels.size} loaded."
                else -> "Built ${meta.generatedUtc.ifBlank { "unknown" }} · scope ${meta.libraryScope}."
            },
        )

        // ----------------------------------------------------------- refresh
        val refreshFailed = refresh.lastAttemptAtMillis > 0L &&
            refresh.lastSuccessAtMillis < refresh.lastAttemptAtMillis
        checks += DiagnosticCheck(
            label = "Refresh pipeline",
            status = when {
                refresh.inProgress -> DiagnosticStatus.Ok
                refreshFailed -> DiagnosticStatus.Warning
                else -> DiagnosticStatus.Ok
            },
            detail = when {
                refresh.inProgress -> "A refresh is running now."
                refreshFailed -> refresh.lastMessage.ifBlank { "The last refresh did not finish." }
                refresh.lastTrigger == null -> "No refresh yet; the bundled copy is in use."
                else -> "Last success and last attempt agree."
            },
        )

        // ------------------------------------------------------- app updates
        val downloadedMismatch = update.downloadedVersion != null &&
            update.downloadedVersion != update.availableVersion
        checks += DiagnosticCheck(
            label = "App updates",
            status = when {
                update.error != null -> DiagnosticStatus.Problem
                downloadedMismatch -> DiagnosticStatus.Warning
                else -> DiagnosticStatus.Ok
            },
            detail = when {
                update.error != null -> update.error
                downloadedMismatch ->
                    "Downloaded ${update.downloadedVersion} does not match offered ${update.availableVersion}."
                update.updateAvailable -> "PremiumTV ${update.availableVersion} is ready in App updates."
                update.latestStableVersion != null -> "Newest stable ${update.latestStableVersion}; this build is current."
                else -> "Not checked yet; press Check for updates."
            },
        )

        // ----------------------------------------------------------- version
        val installed = AppVersions.normalize(installedVersion) ?: installedVersion
        val reported = AppVersions.normalize(update.currentVersion) ?: update.currentVersion
        checks += DiagnosticCheck(
            label = "Version",
            status = if (installed == reported && meta.version.isNotBlank()) {
                DiagnosticStatus.Ok
            } else {
                DiagnosticStatus.Warning
            },
            detail = "Installed $installed · library built for ${meta.version.ifBlank { "unknown" }}.",
        )

        return DiagnosticsReport(checks)
    }
}
