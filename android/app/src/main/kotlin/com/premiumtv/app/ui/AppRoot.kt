package com.premiumtv.app.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.lifecycle.viewmodel.compose.viewModel
import com.premiumtv.app.TvViewModel
import androidx.compose.ui.platform.LocalContext
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.LoadState
import kotlinx.coroutines.delay

@Composable
fun AppRoot(viewModel: TvViewModel = viewModel()) {
    val state by viewModel.state.collectAsState()
    val status by viewModel.status.collectAsState()
    val refreshInfo by viewModel.refreshInfo.collectAsState()
    val updateInfo by viewModel.updateInfo.collectAsState()
    val diagnostics by viewModel.diagnostics.collectAsState()
    val diagnosticsRunning by viewModel.diagnosticsRunning.collectAsState()

    // The guide's "now" has to move on its own; the listings are keyed to real
    // clock times, so a static value would leave yesterday's show on screen.
    var now by remember { mutableStateOf(System.currentTimeMillis() / 1000L) }
    LaunchedEffect(Unit) {
        while (true) {
            delay(60_000L)
            now = System.currentTimeMillis() / 1000L
        }
    }

    // The channel and its server list (backup feeds, or the other streams of
    // the same live game) - resolved when the viewer picks a channel.
    var playing by remember { mutableStateOf<Pair<Channel, List<Channel>>?>(null) }
    // Recently watched + Favorites (1.0.6), persisted per device.
    val appContext = LocalContext.current.applicationContext
    val shelves = remember { PersonalShelves(appContext) }
    var recentKeys by remember { mutableStateOf(shelves.recentKeys()) }
    var favoriteKeys by remember { mutableStateOf(shelves.favoriteKeys()) }
    val toggleFavorite: (Channel) -> Unit = { channel ->
        favoriteKeys = shelves.toggleFavorite(channel.url)
    }

    // Held here rather than in HomeScreen, which leaves the composition while a
    // channel plays: closing the player returns to the same tab and, in the
    // guide, to the same highlighted show.
    var tab by rememberSaveable { mutableStateOf(HomeTab.Channels) }
    val guideState = rememberCableGuideState()

    when (val current = state) {
        LoadState.Loading -> LoadingScreen(
            title = "Loading channels…",
            detail = "Getting your TV library ready.",
        )

        is LoadState.Error -> LoadErrorScreen(
            message = current.message,
            onRetry = { viewModel.load() },
        )

        is LoadState.Ready -> {
            val selection = playing
            if (selection != null) {
                val channel = selection.first
                PlayerScreen(
                    channel = channel,
                    servers = selection.second,
                    programmes = current.library.programmes[channel.id].orEmpty(),
                    now = now,
                    onClose = { playing = null },
                    isFavorite = channel.url in favoriteKeys,
                    onToggleFavorite = { toggleFavorite(channel) },
                )
            } else {
                HomeScreen(
                    library = current.library,
                    now = now,
                    status = status,
                    refreshInfo = refreshInfo,
                    updateInfo = updateInfo,
                    diagnostics = diagnostics,
                    diagnosticsRunning = diagnosticsRunning,
                    tab = tab,
                    onTabChange = { tab = it },
                    guideState = guideState,
                    recentChannels = resolveShelf(recentKeys, current.library.channels),
                    favoriteChannels = resolveShelf(favoriteKeys, current.library.channels),
                    favoriteUrls = favoriteKeys.toSet(),
                    onToggleFavorite = toggleFavorite,
                    onSelect = { channel ->
                        // Opening a channel files it under Recently watched.
                        shelves.recordRecent(channel.url)
                        recentKeys = shelves.recentKeys()
                        playing = channel to serversFor(channel, current.library.channels)
                    },
                    onForceRefresh = { viewModel.forceRefresh() },
                    onReset = { viewModel.resetToBundled() },
                    onCheckForUpdate = { viewModel.checkForUpdates() },
                    onDownloadUpdate = { viewModel.downloadUpdate() },
                    onInstallUpdate = { viewModel.installUpdate() },
                    onCheckForBugs = { viewModel.runDiagnostics() },
                )
            }
        }
    }

    // The update popup floats above every screen except the player: cutting
    // into a programme that is already playing is worse than waiting for the
    // viewer to come back to the browser.
    val notice = updateInfo.notice
    if (notice != null && updateInfo.noticeVisible && playing == null) {
        UpdateNoticeDialog(
            notice = notice,
            installedVersion = updateInfo.currentVersion,
            newestVersion = updateInfo.latestStableVersion ?: updateInfo.availableVersion,
            updateAvailable = updateInfo.updateAvailable,
            onUpdate = {
                viewModel.dismissUpdateNotice()
                tab = HomeTab.Settings
                // Rule 5 in docs/UPDATES.md still holds: no background
                // downloads. The popup opens the update centre and re-checks
                // GitHub; the installer downloads on the Settings button.
                viewModel.checkForUpdates()
            },
            onDismiss = { viewModel.dismissUpdateNotice() },
        )
    }
}
