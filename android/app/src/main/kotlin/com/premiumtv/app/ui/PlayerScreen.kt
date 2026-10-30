package com.premiumtv.app.ui

import android.content.Context
import androidx.activity.compose.BackHandler
import androidx.annotation.OptIn
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxScope
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.LinearProgressIndicator
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.mutableLongStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.media3.common.AudioAttributes
import androidx.media3.common.C
import androidx.media3.common.MediaItem
import androidx.media3.common.PlaybackException
import androidx.media3.common.Player
import androidx.media3.common.TrackGroup
import androidx.media3.common.TrackSelectionOverride
import androidx.media3.common.Tracks
import androidx.media3.common.util.UnstableApi
import androidx.media3.datasource.DefaultDataSource
import androidx.media3.datasource.DefaultHttpDataSource
import androidx.media3.exoplayer.DefaultRenderersFactory
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.source.DefaultMediaSourceFactory
import androidx.media3.exoplayer.source.MediaSource
import androidx.media3.exoplayer.trackselection.DefaultTrackSelector
import androidx.media3.extractor.DefaultExtractorsFactory
import androidx.media3.extractor.ts.DefaultTsPayloadReaderFactory
import androidx.media3.ui.PlayerView
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.Programme
import com.premiumtv.app.data.healthyServersFirst
import java.util.Locale

internal data class AudioTrackCandidate(
    val label: String,
    val language: String,
    val supported: Boolean,
    val selected: Boolean,
    val isSecondary: Boolean,
)

private data class BoundAudioTrack(
    val trackGroup: TrackGroup,
    val trackIndex: Int,
    val candidate: AudioTrackCandidate,
)

/**
 * Picks the best supported audio track index when none is active yet, skipping
 * SAP / commentary / descriptive tracks if a primary supported track exists.
 */
internal fun selectPreferredAudioTrackIndex(candidates: List<AudioTrackCandidate>): Int {
    if (candidates.isEmpty()) return -1
    val primaryIdx = candidates.indexOfFirst { it.supported && !it.isSecondary }
    if (primaryIdx >= 0) return primaryIdx
    return candidates.indexOfFirst { it.supported }
}

internal fun isSecondaryAudioLabel(label: String?, roleFlags: Int = 0): Boolean {
    val secondaryRoles = C.ROLE_FLAG_ALTERNATE or C.ROLE_FLAG_COMMENTARY or C.ROLE_FLAG_DESCRIBES_VIDEO
    if ((roleFlags and secondaryRoles) != 0) return true
    val text = label?.lowercase(Locale.ROOT).orEmpty()
    return Regex("\\b(sap|descriptive|description|dvs|commentary|clean|karaoke)\\b").containsMatchIn(text)
}

internal fun formatPlaybackClock(ms: Long): String {
    if (ms <= 0L) return "0:00"
    val totalSec = ms / 1000L
    val hours = totalSec / 3600L
    val minutes = (totalSec % 3600L) / 60L
    val seconds = totalSec % 60L
    return if (hours > 0L) {
        String.format(Locale.US, "%d:%02d:%02d", hours, minutes, seconds)
    } else {
        String.format(Locale.US, "%d:%02d", minutes, seconds)
    }
}

private const val VOD_RESUME_PREFS = "premiumtv_vod_positions"

private fun loadSavedVodPositionMs(context: Context, id: String): Long {
    if (!id.startsWith("vod-")) return 0L
    return context.getSharedPreferences(VOD_RESUME_PREFS, Context.MODE_PRIVATE)
        .getLong(id, 0L)
}

private fun saveVodPositionMs(context: Context, id: String, posMs: Long, durMs: Long) {
    if (!id.startsWith("vod-") || posMs < 0L) return
    val prefs = context.getSharedPreferences(VOD_RESUME_PREFS, Context.MODE_PRIVATE)
    if (durMs > 20_000L && posMs >= durMs - 12_000L) {
        prefs.edit().remove(id).apply()
    } else if (posMs >= 5_000L) {
        prefs.edit().putLong(id, posMs).apply()
    }
}

/**
 * Playback with automatic multi-server backup (1.1.0) and software FFmpeg +
 * multi-track audio recovery (1.1.3).
 *
 * A channel's feeds are walked by ONE ExoPlayer: when a feed fails, stalls or
 * is already known to be dead, the player hands the same player instance the
 * next server's media source. The 1.0.9 crash fix holds here — no player is
 * rebuilt mid-screen and the PlayerView is never left pointing at a released
 * instance.
 *
 * 1.1.0 changes what the viewer sees. The side player is no longer a floating
 * card over the browser: it is a docked panel on the right (see [SidePanel]),
 * with the category rail and channel list filling the rest of the screen the
 * way IPTV Smarters Pro arranges them. The panel is small while you browse and
 * one press on the picture — or on "⤢ Big screen" — grows it to full screen.
 *
 * When every feed for a channel has failed, [onChannelDead] lets the app hide
 * that channel until the next refresh instead of leaving it in the list to be
 * tapped again.
 */
@OptIn(UnstableApi::class)
@Composable
fun PlayerScreen(
    channel: Channel,
    servers: List<Channel>,
    programmes: List<Programme>,
    now: Long,
    expanded: Boolean = true,
    onExpand: () -> Unit = {},
    onMinimize: () -> Unit = {},
    onClose: () -> Unit,
    isFavorite: Boolean = false,
    onToggleFavorite: () -> Unit = {},
    deadUrls: Set<String> = emptySet(),
    onFeedFailed: (Channel) -> Unit = {},
    onChannelDead: (Channel) -> Unit = {},
) {
    val context = LocalContext.current
    val isVodItem = channel.id.startsWith("vod-")

    // The feed list is frozen for the life of this channel: health updates
    // arrive while the viewer is already watching, and re-sorting the list
    // underneath them would move the index they are on. Known-dead feeds sink
    // to the back once, when the channel opens.
    val playlist = remember(channel.url) {
        val full = if (servers.any { it.url == channel.url }) servers else listOf(channel) + servers
        healthyServersFirst(full, deadUrls)
    }
    var serverIndex by remember(channel.url) {
        mutableStateOf(playlist.indexOfFirst { it.url == channel.url }.coerceAtLeast(0))
    }
    val current = playlist[serverIndex.coerceIn(0, playlist.lastIndex)]

    // Keyed by channel: opening another channel over the side player must not
    // inherit the last one's error card or its "switching servers" notice.
    var errorMessage by remember(channel.url) { mutableStateOf<String?>(null) }
    var switchNotice by remember(channel.url) { mutableStateOf<String?>(null) }
    var audioNotice by remember(channel.url) { mutableStateOf<String?>(null) }
    var buffering by remember(channel.url) { mutableStateOf(true) }
    var backupsUsed by remember(channel.url) { mutableIntStateOf(0) }
    var audioFallbackUsed by remember(channel.url) { mutableStateOf(false) }
    var vodResumeApplied by remember(channel.url) { mutableStateOf(false) }

    var isPlaying by remember { mutableStateOf(true) }
    var isMuted by remember { mutableStateOf(false) }
    var positionMs by remember(channel.url) { mutableLongStateOf(0L) }
    var durationMs by remember(channel.url) { mutableLongStateOf(0L) }
    var boundAudioTracks by remember(channel.url) { mutableStateOf<List<BoundAudioTrack>>(emptyList()) }

    // ONE ExoPlayer for the whole screen, configured with:
    // - EXTENSION_RENDERER_MODE_ON + decoder fallback so bundled FFmpeg decodes
    //   AC-3, E-AC-3, DTS, FLAC, ALAC, PCM and MP2/MP3/AAC when hardware lacks them.
    // - Mixed-MIME / sample-rate / channel-count audio adaptiveness for FAST ad pods.
    // - Explicit media AudioAttributes + audio focus.
    val player = remember {
        val renderersFactory = DefaultRenderersFactory(context)
            .setEnableDecoderFallback(true)
            .setExtensionRendererMode(DefaultRenderersFactory.EXTENSION_RENDERER_MODE_ON)
        val trackSelector = DefaultTrackSelector(context).apply {
            setParameters(
                buildUponParameters()
                    .setExceedAudioConstraintsIfNecessary(true)
                    .setExceedRendererCapabilitiesIfNecessary(true)
                    .setAllowAudioMixedMimeTypeAdaptiveness(true)
                    .setAllowAudioMixedSampleRateAdaptiveness(true)
                    .setAllowAudioMixedChannelCountAdaptiveness(true)
            )
        }
        val audioAttributes = AudioAttributes.Builder()
            .setUsage(C.USAGE_MEDIA)
            .setContentType(C.AUDIO_CONTENT_TYPE_MOVIE)
            .build()
        ExoPlayer.Builder(context)
            .setRenderersFactory(renderersFactory)
            .setTrackSelector(trackSelector)
            .setAudioAttributes(audioAttributes, /* handleAudioFocus = */ true)
            .build()
            .apply {
                playWhenReady = true
                volume = 1f
            }
    }

    LaunchedEffect(player, current) {
        buffering = true
        audioNotice = null
        boundAudioTracks = emptyList()
        player.trackSelectionParameters = player.trackSelectionParameters
            .buildUpon()
            .clearOverridesOfType(C.TRACK_TYPE_AUDIO)
            .setTrackTypeDisabled(C.TRACK_TYPE_AUDIO, false)
            .build()
        player.setMediaSource(mediaSourceFor(context, current))
        player.prepare()
    }

    // Poll playback clock for VOD transport controls and periodic resume persistence.
    LaunchedEffect(player, channel.id, isVodItem) {
        var ticks = 0
        while (true) {
            positionMs = player.currentPosition.coerceAtLeast(0L)
            val dur = player.duration
            durationMs = if (dur != C.TIME_UNSET && dur > 0L) dur else 0L
            ticks += 1
            if (isVodItem && durationMs > 0L && ticks % 10 == 0) {
                saveVodPositionMs(context, channel.id, positionMs, durationMs)
            }
            kotlinx.coroutines.delay(500L)
        }
    }

    // Buffering watchdog: a feed that never leaves buffering (stuck manifest,
    // geo-block timeout, dead HLS variant) advances after 25 s instead of
    // leaving the spinner forever. On the last server it says so.
    LaunchedEffect(buffering, serverIndex, playlist.size, errorMessage) {
        if (!buffering || errorMessage != null) return@LaunchedEffect
        kotlinx.coroutines.delay(25_000L)
        if (buffering && errorMessage == null) {
            val next = autoNextServerIndex(serverIndex, playlist.size)
            if (next != null) {
                backupsUsed += 1
                serverIndex = next
                switchNotice = serverSwitchNotice(ServerSwitchReason.Stalled, next, playlist.size)
            } else if (playlist.size > 1) {
                buffering = false
                errorMessage = "This feed never started playing, and it was the last server."
            }
        }
    }

    // Leaving the app pauses; coming back resumes only if the viewer had not
    // paused it themselves.
    val lifecycleOwner = LocalLifecycleOwner.current
    DisposableEffect(player, lifecycleOwner) {
        var resumeOnStart = false
        val observer = LifecycleEventObserver { _, event ->
            when (event) {
                Lifecycle.Event.ON_STOP -> {
                    if (isVodItem && durationMs > 0L) {
                        saveVodPositionMs(context, channel.id, player.currentPosition, durationMs)
                    }
                    resumeOnStart = player.playWhenReady
                    player.pause()
                }
                Lifecycle.Event.ON_START -> if (resumeOnStart) player.play()
                else -> Unit
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose {
            if (isVodItem && durationMs > 0L) {
                saveVodPositionMs(context, channel.id, player.currentPosition, durationMs)
            }
            lifecycleOwner.lifecycle.removeObserver(observer)
        }
    }

    DisposableEffect(player) {
        onDispose { player.release() }
    }

    // The listener reads serverIndex and playlist at call time, so the effect
    // can stay keyed to the player and the channel instead of being rebuilt on
    // every hop.
    val reportFailed = rememberUpdatedState(onFeedFailed)
    val reportDead = rememberUpdatedState(onChannelDead)
    DisposableEffect(player, channel.url) {
        val listener = object : Player.Listener {
            override fun onPlayerError(error: PlaybackException) {
                buffering = false
                val failed = playlist[serverIndex.coerceIn(0, playlist.lastIndex)]
                // Remember the dead feed so the next open (or the next
                // channel's server list) does not lead with it.
                reportFailed.value(failed)
                val next = autoNextServerIndex(serverIndex, playlist.size)
                if (next != null) {
                    backupsUsed += 1
                    serverIndex = next
                    switchNotice = serverSwitchNotice(ServerSwitchReason.Failed, next, playlist.size)
                } else {
                    switchNotice = null
                    errorMessage = error.message ?: "This stream could not be played."
                    // Every feed failed: hide the channel until the next
                    // refresh instead of offering it again.
                    reportDead.value(channel)
                }
            }

            override fun onPlaybackStateChanged(playbackState: Int) {
                buffering = playbackState == Player.STATE_BUFFERING
                if (playbackState == Player.STATE_READY) {
                    errorMessage = null
                    switchNotice = null
                    if (isVodItem && !vodResumeApplied) {
                        vodResumeApplied = true
                        val saved = loadSavedVodPositionMs(context, channel.id)
                        val dur = player.duration
                        if (saved >= 5_000L && dur != C.TIME_UNSET && saved < dur - 12_000L) {
                            player.seekTo(saved)
                        }
                    }
                } else if (playbackState == Player.STATE_ENDED && isVodItem) {
                    val dur = player.duration
                    if (dur != C.TIME_UNSET && dur > 0L) {
                        saveVodPositionMs(context, channel.id, dur, dur)
                    }
                }
            }

            override fun onIsPlayingChanged(playingNow: Boolean) {
                isPlaying = playingNow
            }

            override fun onTracksChanged(tracks: Tracks) {
                val audioGroups = tracks.groups.filter { it.type == C.TRACK_TYPE_AUDIO }
                if (audioGroups.isEmpty()) {
                    boundAudioTracks = emptyList()
                    return
                }
                val collected = mutableListOf<BoundAudioTrack>()
                var ordinal = 1
                for (group in audioGroups) {
                    for (tIdx in 0 until group.length) {
                        val format = group.getTrackFormat(tIdx)
                        val lang = format.language?.uppercase(Locale.ROOT).orEmpty()
                        val rawLabel = format.label?.trim().orEmpty()
                        val display = when {
                            rawLabel.isNotBlank() && lang.isNotBlank() &&
                                !rawLabel.uppercase(Locale.ROOT).contains(lang) -> "$rawLabel · $lang"
                            rawLabel.isNotBlank() -> rawLabel
                            lang.isNotBlank() -> lang
                            else -> "Track $ordinal"
                        }
                        ordinal += 1
                        collected += BoundAudioTrack(
                            trackGroup = group.mediaTrackGroup,
                            trackIndex = tIdx,
                            candidate = AudioTrackCandidate(
                                label = display,
                                language = lang,
                                supported = group.isTrackSupported(tIdx),
                                selected = group.isTrackSelected(tIdx),
                                isSecondary = isSecondaryAudioLabel(format.label, format.roleFlags),
                            ),
                        )
                    }
                }
                val supportedOnly = collected.filter { it.candidate.supported }
                boundAudioTracks = supportedOnly

                if (supportedOnly.isNotEmpty()) {
                    audioNotice = null
                    val anySelectedSupported = supportedOnly.any { it.candidate.selected }
                    if (!anySelectedSupported) {
                        val bestIdx = selectPreferredAudioTrackIndex(collected.map { it.candidate })
                        if (bestIdx >= 0) {
                            val chosen = collected[bestIdx]
                            player.trackSelectionParameters = player.trackSelectionParameters
                                .buildUpon()
                                .clearOverridesOfType(C.TRACK_TYPE_AUDIO)
                                .setTrackTypeDisabled(C.TRACK_TYPE_AUDIO, false)
                                .addOverride(TrackSelectionOverride(chosen.trackGroup, listOf(chosen.trackIndex)))
                                .build()
                        }
                    }
                } else if (!isVodItem && hasBackupServer(serverIndex, playlist.size) && !audioFallbackUsed) {
                    audioFallbackUsed = true
                    val next = nextServerIndex(serverIndex, playlist.size, 1)
                    serverIndex = next
                    switchNotice = "Unsupported audio codec on previous feed — trying Server ${next + 1} of ${playlist.size}…"
                } else {
                    audioNotice = "Audio codec on this feed is not supported on this device"
                }
            }
        }
        player.addListener(listener)
        onDispose { player.removeListener(listener) }
    }

    val togglePlayPause: () -> Unit = {
        if (player.isPlaying) player.pause() else player.play()
        isPlaying = player.isPlaying
    }
    val toggleMute: () -> Unit = {
        val nextMuted = !isMuted
        isMuted = nextMuted
        player.volume = if (nextMuted) 0f else 1f
    }
    val skipByMs: (Long) -> Unit = { delta ->
        val dur = player.duration
        val maxPos = if (dur != C.TIME_UNSET && dur > 0L) dur else Long.MAX_VALUE
        val target = (player.currentPosition + delta).coerceIn(0L, maxPos)
        player.seekTo(target)
        positionMs = target
    }
    val cycleAudioTrack: () -> Unit = {
        if (boundAudioTracks.size > 1) {
            val currentIdx = boundAudioTracks.indexOfFirst { it.candidate.selected }.coerceAtLeast(0)
            val next = boundAudioTracks[(currentIdx + 1) % boundAudioTracks.size]
            player.trackSelectionParameters = player.trackSelectionParameters
                .buildUpon()
                .clearOverridesOfType(C.TRACK_TYPE_AUDIO)
                .setTrackTypeDisabled(C.TRACK_TYPE_AUDIO, false)
                .addOverride(TrackSelectionOverride(next.trackGroup, listOf(next.trackIndex)))
                .build()
            audioNotice = "Audio · ${next.candidate.label}"
        }
    }

    // Manual server switching wraps (a person pressing the button expects to
    // cycle); the automatic walk does not.
    val hopServer: (Int) -> Unit = { delta ->
        errorMessage = null
        buffering = true
        val next = nextServerIndex(serverIndex, playlist.size, delta)
        serverIndex = next
        switchNotice = serverSwitchNotice(ServerSwitchReason.Manual, next, playlist.size)
    }

    // Back rides the same ladder as the layout, exactly as the hints under both
    // layouts promise: on the big screen it tucks the channel into the docked
    // side player, and in the dock it closes the panel and hands the browser
    // back. 1.1.2 opens channels docked, so the closing press is now the same
    // one the viewer makes first - without a handler for it, Back left the app.
    BackHandler(enabled = true) {
        if (expanded) onMinimize() else onClose()
    }

    val activeAudioLabel = boundAudioTracks.firstOrNull { it.candidate.selected }?.candidate?.label
        ?: boundAudioTracks.firstOrNull()?.candidate?.label

    Surface(
        modifier = Modifier.fillMaxSize(),
        shape = if (expanded) RectangleShape else RoundedCornerShape(16.dp),
        color = if (expanded) Color.Black else Color(0xFF0B1017),
        border = if (expanded) null else BorderStroke(1.dp, PanelStroke),
    ) {
        // One Column for both layouts, with the same video call site, so the
        // PlayerView is never torn down and re-attached to the player during a
        // side-player flip (the 1.0.8 black-screen shape).
        Column(modifier = Modifier.fillMaxSize()) {
            val videoModifier = if (expanded) {
                Modifier
                    .fillMaxWidth()
                    .weight(1f)
            } else {
                Modifier
                    .fillMaxWidth()
                    .padding(10.dp)
                    .aspectRatio(16f / 9f)
            }

            Box(modifier = videoModifier) {
                AndroidView(
                    modifier = Modifier.fillMaxSize(),
                    factory = { ctx ->
                        PlayerView(ctx).also { view ->
                            view.player = player
                            view.useController = expanded
                            view.controllerShowTimeoutMs = 5000
                            view.setBackgroundColor(android.graphics.Color.BLACK)
                        }
                    },
                    update = { view ->
                        if (view.player !== player) view.player = player
                        view.useController = expanded
                    },
                )

                if (expanded) {
                    BigScreenChrome(
                        channel = channel,
                        programmes = programmes,
                        now = now,
                        playlistSize = playlist.size,
                        serverIndex = serverIndex,
                        backupsUsed = backupsUsed,
                        buffering = buffering,
                        errorMessage = errorMessage,
                        switchNotice = switchNotice,
                        audioNotice = audioNotice,
                        isMuted = isMuted,
                        audioTrackCount = boundAudioTracks.size,
                        activeAudioLabel = activeAudioLabel,
                        isFavorite = isFavorite,
                        onToggleFavorite = onToggleFavorite,
                        onToggleMute = toggleMute,
                        onCycleAudioTrack = cycleAudioTrack,
                        onHopServer = hopServer,
                        onRetryAll = {
                            errorMessage = null
                            buffering = true
                            serverIndex = nextServerIndex(serverIndex, playlist.size, 1)
                        },
                        onMinimize = onMinimize,
                        onClose = onClose,
                    )
                } else {
                    SidePlayerPicture(
                        buffering = buffering,
                        errorMessage = errorMessage,
                        onExpand = onExpand,
                    )
                }
            }

            if (!expanded) {
                SidePanelDetails(
                    modifier = Modifier.weight(1f),
                    channel = channel,
                    programmes = programmes,
                    now = now,
                    serverIndex = serverIndex,
                    playlistSize = playlist.size,
                    backupsUsed = backupsUsed,
                    switchNotice = switchNotice,
                    audioNotice = audioNotice,
                    errorMessage = errorMessage,
                    isVodItem = isVodItem,
                    isPlaying = isPlaying,
                    isMuted = isMuted,
                    positionMs = positionMs,
                    durationMs = durationMs,
                    audioTrackCount = boundAudioTracks.size,
                    activeAudioLabel = activeAudioLabel,
                    isFavorite = isFavorite,
                    onToggleFavorite = onToggleFavorite,
                    onTogglePlayPause = togglePlayPause,
                    onToggleMute = toggleMute,
                    onSkipByMs = skipByMs,
                    onCycleAudioTrack = cycleAudioTrack,
                    onHopServer = hopServer,
                    onExpand = onExpand,
                    onClose = onClose,
                )
            }
        }
    }
}

/** The picture itself: click it (or press OK on it) to go full screen. */
@Composable
private fun SidePlayerPicture(
    buffering: Boolean,
    errorMessage: String?,
    onExpand: () -> Unit,
) {
    var focused by remember { mutableStateOf(false) }
    Box(
        modifier = Modifier
            .fillMaxSize()
            .onFocusChanged { focused = it.isFocused }
            .focusOutline(focused, RoundedCornerShape(12.dp), restColor = Color(0x33101826))
            .tvClickable(onExpand),
        contentAlignment = Alignment.Center,
    ) {
        if (errorMessage != null) {
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                modifier = Modifier.padding(horizontal = 8.dp),
            ) {
                Text(
                    text = "No signal",
                    style = MaterialTheme.typography.labelMedium,
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    text = "All feeds tried",
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                    textAlign = TextAlign.Center,
                )
            }
        } else if (buffering) {
            Text(
                text = "Loading…",
                style = MaterialTheme.typography.labelSmall,
                color = Color.White,
            )
        }
        // The affordance is always visible: a small ⤢ badge in the corner.
        Text(
            text = "⤢",
            style = MaterialTheme.typography.titleMedium,
            color = PremiumGold,
            modifier = Modifier
                .align(Alignment.TopEnd)
                .padding(6.dp),
        )
    }
}

/**
 * Everything under the picture in the side panel: the channel, what is on now,
 * which server is carrying it, the primary action buttons, and the built-in
 * transport + audio controls.
 */
@Composable
private fun SidePanelDetails(
    modifier: Modifier = Modifier,
    channel: Channel,
    programmes: List<Programme>,
    now: Long,
    serverIndex: Int,
    playlistSize: Int,
    backupsUsed: Int,
    switchNotice: String?,
    audioNotice: String?,
    errorMessage: String?,
    isVodItem: Boolean,
    isPlaying: Boolean,
    isMuted: Boolean,
    positionMs: Long,
    durationMs: Long,
    audioTrackCount: Int,
    activeAudioLabel: String?,
    isFavorite: Boolean,
    onToggleFavorite: () -> Unit,
    onTogglePlayPause: () -> Unit,
    onToggleMute: () -> Unit,
    onSkipByMs: (Long) -> Unit,
    onCycleAudioTrack: () -> Unit,
    onHopServer: (Int) -> Unit,
    onExpand: () -> Unit,
    onClose: () -> Unit,
) {
    val currentProgramme = nowPlaying(programmes, now)
    // The details get whatever height the picture leaves. A 1280x720 TV leaves
    // little of it, so the column scrolls instead of pushing the two buttons
    // off the panel - the buttons must always be reachable by a remote.
    Column(
        modifier = modifier
            .fillMaxWidth()
            .verticalScroll(rememberScrollState())
            .padding(start = 14.dp, end = 14.dp, top = 2.dp, bottom = 12.dp),
    ) {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Text(
                text = if (isVodItem) "ON DEMAND" else "WATCHING NOW",
                style = MaterialTheme.typography.labelSmall,
                color = PremiumGold,
                fontWeight = FontWeight.Bold,
                letterSpacing = 1.2.sp,
                modifier = Modifier.weight(1f),
            )
            if (playlistSize > 1) {
                Text(
                    text = "AUTO BACKUP",
                    style = MaterialTheme.typography.labelSmall,
                    color = Color(0xFF12160B),
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .background(FocusRing, RoundedCornerShape(999.dp))
                        .padding(horizontal = 8.dp, vertical = 2.dp),
                )
            }
        }
        Spacer(modifier = Modifier.height(6.dp))
        Text(
            text = channel.name,
            style = MaterialTheme.typography.titleSmall,
            color = Color.White,
            fontWeight = FontWeight.Bold,
            maxLines = 2,
            overflow = TextOverflow.Ellipsis,
        )
        if (currentProgramme != null) {
            Spacer(modifier = Modifier.height(2.dp))
            Text(
                text = "Now · ${currentProgramme.title}",
                style = MaterialTheme.typography.bodySmall,
                color = PremiumGold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
        }
        Spacer(modifier = Modifier.height(4.dp))
        Text(
            text = serverStatusLine(serverIndex, playlistSize, playlistSize > 1),
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
        )
        if (backupsUsed > 0 && playlistSize > 1) {
            Text(
                text = "Switched feeds automatically $backupsUsed×",
                style = MaterialTheme.typography.labelSmall,
                color = FocusRing,
            )
        }

        val notice = when {
            errorMessage != null -> exhaustedServerMessage(playlistSize)
            switchNotice != null -> switchNotice
            audioNotice != null -> audioNotice
            else -> null
        }
        if (notice != null) {
            Spacer(modifier = Modifier.height(6.dp))
            Text(
                text = notice,
                style = MaterialTheme.typography.labelSmall,
                color = if (errorMessage != null) Color(0xFFFF8A80) else FocusRing,
                maxLines = 3,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFF141C26), RoundedCornerShape(8.dp))
                    .padding(horizontal = 8.dp, vertical = 6.dp),
            )
        }

        Spacer(modifier = Modifier.height(10.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            // Keeping this label exact matters: the emulator smoke gate taps
            // "⤢ Big screen" to prove the flip does not restart the stream.
            FocusButton("⤢ Big screen", Modifier.weight(1f)) { onExpand() }
            FocusButton("✕ Close", Modifier.weight(1f)) { onClose() }
        }
        Spacer(modifier = Modifier.height(8.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            if (playlistSize > 1) {
                FocusButton("◀ Server", Modifier.weight(1f)) { onHopServer(-1) }
                FocusButton("Server ▶", Modifier.weight(1f)) { onHopServer(1) }
            }
            FocusButton(if (isFavorite) "★" else "☆", Modifier.weight(0.6f)) { onToggleFavorite() }
        }

        Spacer(modifier = Modifier.height(10.dp))
        SideTransportBar(
            isVodItem = isVodItem,
            isPlaying = isPlaying,
            isMuted = isMuted,
            positionMs = positionMs,
            durationMs = durationMs,
            audioTrackCount = audioTrackCount,
            activeAudioLabel = activeAudioLabel,
            onTogglePlayPause = onTogglePlayPause,
            onToggleMute = onToggleMute,
            onSkipByMs = onSkipByMs,
            onCycleAudioTrack = onCycleAudioTrack,
        )

        Spacer(modifier = Modifier.height(6.dp))
        Text(
            text = "OK on the picture for full screen · Back closes this panel",
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
            maxLines = 2,
        )
    }
}

/** Compact transport & audio bar inside the docked side player. */
@Composable
private fun SideTransportBar(
    isVodItem: Boolean,
    isPlaying: Boolean,
    isMuted: Boolean,
    positionMs: Long,
    durationMs: Long,
    audioTrackCount: Int,
    activeAudioLabel: String?,
    onTogglePlayPause: () -> Unit,
    onToggleMute: () -> Unit,
    onSkipByMs: (Long) -> Unit,
    onCycleAudioTrack: () -> Unit,
) {
    Column(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color(0xFF121822), RoundedCornerShape(10.dp))
            .padding(horizontal = 10.dp, vertical = 8.dp),
        verticalArrangement = Arrangement.spacedBy(6.dp),
    ) {
        if (isVodItem && durationMs > 0L) {
            val ratio = (positionMs.toFloat() / durationMs.toFloat()).coerceIn(0f, 1f)
            LinearProgressIndicator(
                progress = { ratio },
                modifier = Modifier.fillMaxWidth().height(4.dp),
                color = PremiumGold,
                trackColor = Color(0x33FFFFFF),
            )
            Text(
                text = "${formatPlaybackClock(positionMs)} / ${formatPlaybackClock(durationMs)}",
                style = MaterialTheme.typography.labelSmall,
                color = MutedText,
            )
        } else {
            Text(
                text = "● LIVE STREAM",
                style = MaterialTheme.typography.labelSmall,
                color = Color(0xFFFF8076),
                fontWeight = FontWeight.Bold,
            )
        }
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(6.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            FocusButton(if (isPlaying) "❚❚ Pause" else "▶ Play") { onTogglePlayPause() }
            if (isVodItem && durationMs > 0L) {
                FocusButton("↺ 10s") { onSkipByMs(-10_000L) }
                FocusButton("10s ↻") { onSkipByMs(10_000L) }
            }
            FocusButton(if (isMuted) "🔇 Unmute" else "🔊 Mute") { onToggleMute() }
            if (audioTrackCount > 1) {
                val label = activeAudioLabel?.take(12) ?: "Audio"
                FocusButton("🔊 $label ($audioTrackCount)") { onCycleAudioTrack() }
            }
        }
    }
}

/** The full-screen player's overlays: title, status, error card and buttons. */
@Composable
private fun BoxScope.BigScreenChrome(
    channel: Channel,
    programmes: List<Programme>,
    now: Long,
    playlistSize: Int,
    serverIndex: Int,
    backupsUsed: Int,
    buffering: Boolean,
    errorMessage: String?,
    switchNotice: String?,
    audioNotice: String?,
    isMuted: Boolean,
    audioTrackCount: Int,
    activeAudioLabel: String?,
    isFavorite: Boolean,
    onToggleFavorite: () -> Unit,
    onToggleMute: () -> Unit,
    onCycleAudioTrack: () -> Unit,
    onHopServer: (Int) -> Unit,
    onRetryAll: () -> Unit,
    onMinimize: () -> Unit,
    onClose: () -> Unit,
) {
    val currentProgramme = nowPlaying(programmes, now)
    Column(
        modifier = Modifier
            .align(Alignment.TopStart)
            .padding(start = 32.dp, top = 24.dp, end = 32.dp),
    ) {
        Text(
            text = channel.name,
            style = MaterialTheme.typography.headlineSmall,
            color = Color.White,
            fontWeight = FontWeight.Bold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
        if (playlistSize > 1) {
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = serverStatusLine(serverIndex, playlistSize, true),
                style = MaterialTheme.typography.labelSmall,
                color = PremiumGold,
            )
            if (backupsUsed > 0) {
                Text(
                    text = "Automatic backup moved you $backupsUsed× this session",
                    style = MaterialTheme.typography.labelSmall,
                    color = FocusRing,
                )
            }
        }
        if (audioNotice != null) {
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = audioNotice,
                style = MaterialTheme.typography.labelSmall,
                color = FocusRing,
            )
        }
        if (currentProgramme != null) {
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = "Now · ${currentProgramme.title}",
                style = MaterialTheme.typography.bodyMedium,
                color = PremiumGold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
            if (currentProgramme.desc.isNotBlank()) {
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = currentProgramme.desc,
                    style = MaterialTheme.typography.bodySmall,
                    color = MutedText,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.fillMaxWidth(0.55f),
                )
            }
        }
        if (channel.group.isNotBlank()) {
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = channel.group,
                style = MaterialTheme.typography.labelSmall,
                color = MutedText,
            )
        }
    }

    if (errorMessage != null) {
        Box(
            modifier = Modifier
                .align(Alignment.Center)
                .widthIn(max = 640.dp)
                .background(Color(0xEE101720), RoundedCornerShape(16.dp))
                .padding(28.dp),
        ) {
            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(
                    text = "This stream is not playing",
                    style = MaterialTheme.typography.titleMedium,
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    textAlign = TextAlign.Center,
                )
                Spacer(modifier = Modifier.height(10.dp))
                Text(
                    text = exhaustedServerMessage(playlistSize) + " " + errorMessage.orEmpty(),
                    style = MaterialTheme.typography.bodySmall,
                    color = MutedText,
                    textAlign = TextAlign.Center,
                )
                Spacer(modifier = Modifier.height(10.dp))
                Text(
                    text = "This channel is hidden from the browser until the next refresh. " +
                        "Most failures are dead upstream links, and the repository's nightly " +
                        "link check removes them.",
                    style = MaterialTheme.typography.bodySmall,
                    color = MutedText,
                    textAlign = TextAlign.Center,
                )
                Spacer(modifier = Modifier.height(18.dp))
                Row {
                    FocusButton("Back to channels") { onClose() }
                    if (playlistSize > 1) {
                        Spacer(modifier = Modifier.width(16.dp))
                        FocusButton("Try the servers again") { onRetryAll() }
                    }
                }
            }
        }
    } else if (switchNotice != null) {
        Box(
            modifier = Modifier
                .align(Alignment.Center)
                .widthIn(max = 560.dp)
                .background(Color(0xEE101720), RoundedCornerShape(14.dp))
                .padding(horizontal = 24.dp, vertical = 16.dp),
        ) {
            Text(
                text = switchNotice.orEmpty(),
                style = MaterialTheme.typography.bodyMedium,
                color = PremiumGold,
                textAlign = TextAlign.Center,
            )
        }
    } else if (buffering) {
        Text(
            text = "Loading…",
            style = MaterialTheme.typography.titleMedium,
            color = Color.White,
            modifier = Modifier.align(Alignment.Center),
        )
    }

    // Audio controls pinned top-right so bottom-right server/layout chrome never crowds narrow screens.
    Row(
        modifier = Modifier
            .align(Alignment.TopEnd)
            .padding(end = 32.dp, top = 24.dp),
        horizontalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        FocusButton(if (isMuted) "🔇 Unmute" else "🔊 Mute") { onToggleMute() }
        if (audioTrackCount > 1) {
            val label = activeAudioLabel?.take(12) ?: "Audio"
            FocusButton("🔊 $label ($audioTrackCount)") { onCycleAudioTrack() }
        }
    }

    // Manual server switching: the same player-swap path the automatic backup
    // takes, on demand.
    Row(
        modifier = Modifier
            .align(Alignment.BottomEnd)
            .padding(end = 32.dp, bottom = 16.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
    ) {
        if (playlistSize > 1) {
            FocusButton("◀ Server") { onHopServer(-1) }
            FocusButton("Server ▶") { onHopServer(1) }
        }
        FocusButton(if (isFavorite) "★ Favorited" else "☆ Favorite") { onToggleFavorite() }
        FocusButton("⤢ Side player") { onMinimize() }
        FocusButton("✕ Close") { onClose() }
    }

    Text(
        text = "Press Back to tuck this into the side player — it keeps playing while you browse",
        style = MaterialTheme.typography.labelSmall,
        color = MutedText,
        modifier = Modifier
            .align(Alignment.BottomStart)
            .padding(start = 32.dp, bottom = 20.dp),
    )
}

/**
 * One server's media source, carrying that feed's own referrer / origin /
 * user-agent and permissive MPEG-TS packet flags so non-IDR broadcast streams
 * and LATM/ADTS audio access units lock cleanly.
 */
@OptIn(UnstableApi::class)
private fun mediaSourceFor(context: Context, channel: Channel): MediaSource {
    val headers = HashMap<String, String>()
    if (channel.referrer.isNotBlank()) headers["Referer"] = channel.referrer
    if (channel.origin.isNotBlank()) headers["Origin"] = channel.origin

    var http = DefaultHttpDataSource.Factory()
        .setAllowCrossProtocolRedirects(true)
        .setConnectTimeoutMs(15_000)
        .setReadTimeoutMs(30_000)
    if (headers.isNotEmpty()) http = http.setDefaultRequestProperties(headers)
    if (channel.userAgent.isNotBlank()) http = http.setUserAgent(channel.userAgent)

    val extractors = DefaultExtractorsFactory()
        .setTsExtractorFlags(
            DefaultTsPayloadReaderFactory.FLAG_ALLOW_NON_IDR_KEYFRAMES or
                DefaultTsPayloadReaderFactory.FLAG_DETECT_ACCESS_UNITS
        )

    return DefaultMediaSourceFactory(DefaultDataSource.Factory(context, http), extractors)
        .createMediaSource(MediaItem.fromUri(channel.url))
}
