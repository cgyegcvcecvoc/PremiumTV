package com.premiumtv.app.ui

import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.width
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import com.premiumtv.app.TvViewModel
import com.premiumtv.app.data.CategoryGroup
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.ChannelHealthStore
import com.premiumtv.app.data.LoadState
import com.premiumtv.app.data.hiddenChannelCount
import com.premiumtv.app.data.visibleChannels
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.delay
import kotlinx.coroutines.withContext

@Composable
fun AppRoot(viewModel: TvViewModel = viewModel()) {
    val state by viewModel.state.collectAsState()
    val status by viewModel.status.collectAsState()
    val refreshInfo by viewModel.refreshInfo.collectAsState()
    val updateInfo by viewModel.updateInfo.collectAsState()
    val diagnostics by viewModel.diagnostics.collectAsState()
    val diagnosticsRunning by viewModel.diagnosticsRunning.collectAsState()
    val liveFeedStatus by viewModel.liveFeedStatus.collectAsState()
    val liveProbeRunning by viewModel.liveProbeRunning.collectAsState()
    val loadProgress by viewModel.loadProgress.collectAsState()

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
    // The side player: a channel keeps playing in the docked right-hand panel
    // while the category rail and channel list stay usable.
    var sidePlayer by rememberSaveable { mutableStateOf(false) }
    // Recently watched + Favorites (1.0.6), persisted per device.
    val appContext = LocalContext.current.applicationContext
    val shelves = remember { PersonalShelves(appContext) }
    var vodChannelsById by remember { mutableStateOf(emptyMap<String, List<Channel>>()) }
    LaunchedEffect(Unit) {
        vodChannelsById = withContext(Dispatchers.Default) {
            appContext.readVodCatalog().associate { it.id to it.asChannels() }
        }
    }
    var recentKeys by remember { mutableStateOf(shelves.recentKeys()) }
    var favoriteKeys by remember { mutableStateOf(shelves.favoriteKeys()) }
    val toggleFavorite: (Channel) -> Unit = { channel ->
        favoriteKeys = shelves.toggleFavorite(channel.url)
    }

    // 1.1.0 dead-feed memory: a feed the player watched fail is remembered, and
    // a channel whose every feed failed is filtered out of the browser until
    // the next refresh (or Settings → Restore hidden channels).
    val health = remember { ChannelHealthStore(appContext) }
    var deadUrls by remember { mutableStateOf(health.deadUrls()) }
    val recordFeedFailure: (Channel) -> Unit = { channel ->
        health.recordDead(channel.url)
        deadUrls = health.deadUrls()
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
            progress = loadProgress,
        )

        is LoadState.Error -> LoadErrorScreen(
            message = current.message,
            onRetry = { viewModel.load() },
        )

        is LoadState.Ready -> {
            val selection = playing
            // The library the browser is allowed to show: channels whose every
            // feed is known dead drop out, and a category with nothing left
            // drops out with them.
            val visibleLibrary = remember(current.library, deadUrls) {
                val channels = visibleChannels(current.library.channels, deadUrls)
                val groups = current.library.groups.mapNotNull { group ->
                    val count = channels.count { it.group == group.name }
                    if (count > 0) CategoryGroup(group.name, count) else null
                }
                current.library.copy(channels = channels, groups = groups)
            }
            val hiddenCount = remember(current.library, deadUrls) {
                hiddenChannelCount(current.library.channels, deadUrls)
            }

            BoxWithConstraints(modifier = Modifier.fillMaxSize()) {
                // The dock is a readable column on a TV and never more than
                // 42% of a narrow screen, so the browser keeps the majority of
                // the width - the point of watching in the corner. A phone-sized
                // window (a test emulator, a tablet in portrait) has no room for
                // two usable panes, so there the same panel floats over the
                // right edge instead of squeezing the browser to nothing.
                val narrow = maxWidth < 720.dp
                val dockWidth = if (narrow) {
                    (maxWidth * 0.62f).coerceIn(220.dp, 320.dp)
                } else {
                    (maxWidth * 0.40f).coerceIn(300.dp, 420.dp)
                }

                // Browser on the left, docked player on the right. The player
                // slot is reserved here and the player itself is the same call
                // site below, so flipping to full screen never rebuilds the
                // ExoPlayer or restarts the stream.
                Row(modifier = Modifier.fillMaxSize()) {
                    Box(
                        modifier = Modifier
                            .weight(1f)
                            .fillMaxHeight(),
                    ) {
                        if (selection == null || sidePlayer) {
                            HomeScreen(
                                library = visibleLibrary,
                                now = now,
                                status = status,
                                refreshInfo = refreshInfo,
                                updateInfo = updateInfo,
                                diagnostics = diagnostics,
                                diagnosticsRunning = diagnosticsRunning,
                                tab = tab,
                                onTabChange = { tab = it },
                                guideState = guideState,
                                recentChannels = resolveShelf(recentKeys, visibleLibrary.channels),
                                favoriteChannels = resolveShelf(favoriteKeys, visibleLibrary.channels),
                                favoriteUrls = favoriteKeys.toSet(),
                                onToggleFavorite = toggleFavorite,
                                hiddenChannelCount = hiddenCount,
                                onRestoreHiddenChannels = {
                                    health.clear()
                                    deadUrls = emptySet()
                                },
                                onSelect = { channel ->
                                    // Opening a channel files it under Recently watched.
                                    shelves.recordRecent(channel.url)
                                    recentKeys = shelves.recentKeys()
                                    val vodServers = vodChannelsById[channel.id]
                                    if (vodServers != null && vodServers.isNotEmpty()) {
                                        playing = vodServers.first() to vodServers
                                    } else {
                                        playing = channel to serversFor(channel, current.library.channels)
                                    }
                                    // 1.1.2: a channel opens in the docked side player first,
                                    // with the browser still usable beside it. One press on
                                    // the picture (or “⤢ Big screen”) grows the same player
                                    // to full screen; Back tucks it away again.
                                    sidePlayer = true
                                },
                                onForceRefresh = { viewModel.forceRefresh() },
                                onReset = { viewModel.resetToBundled() },
                                onCheckForUpdate = { viewModel.checkForUpdates() },
                                onDownloadUpdate = { viewModel.downloadUpdate() },
                                onInstallUpdate = { viewModel.installUpdate() },
                                onCheckForBugs = { viewModel.runDiagnostics() },
                                liveFeedStatus = liveFeedStatus,
                                liveProbeRunning = liveProbeRunning,
                                onProbeLiveEvents = { viewModel.refreshLiveEvents() },
                                // The docked panel owns Back while it is up: its
                                // own hint promises that, and without it the
                                // press fell through to the app and exited.
                                playerDocked = sidePlayer && selection != null,
                            )
                        }
                    }
                    if (selection != null && sidePlayer && !narrow) {
                        // Reserve the dock's width so the browser is never
                        // covered by the picture.
                        Spacer(modifier = Modifier.width(dockWidth).fillMaxHeight())
                    }
                }

                if (selection != null) {
                    val channel = selection.first
                    val playerModifier = if (sidePlayer) {
                        Modifier
                            .align(Alignment.CenterEnd)
                            .width(dockWidth)
                            .fillMaxHeight()
                    } else {
                        Modifier.fillMaxSize()
                    }
                    Box(modifier = playerModifier) {
                        PlayerScreen(
                            channel = channel,
                            servers = selection.second,
                            programmes = current.library.programmes[channel.id].orEmpty(),
                            now = now,
                            expanded = !sidePlayer,
                            onExpand = { sidePlayer = false },
                            onMinimize = { sidePlayer = true },
                            onClose = {
                                playing = null
                                sidePlayer = false
                            },
                            isFavorite = channel.url in favoriteKeys,
                            onToggleFavorite = { toggleFavorite(channel) },
                            deadUrls = deadUrls,
                            onFeedFailed = recordFeedFailure,
                            onChannelDead = recordFeedFailure,
                        )
                    }
                }
            }
        }
    }

    // The update popup floats above every screen except a player that is
    // actually up - full screen *or* docked. Cutting into a programme that is
    // already playing is worse than waiting for the viewer to come back, and a
    // dialog window takes the remote's focus and its Back key with it: with the
    // dock open, Back is promised to the dock ("Back to tuck, Back to close"),
    // so a popup arriving late over a docked channel would swallow the press
    // and leave the panel stuck open. The check is decided from the last cached
    // notice at startup, so a viewer with nothing playing still sees it on the
    // next launch.
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
