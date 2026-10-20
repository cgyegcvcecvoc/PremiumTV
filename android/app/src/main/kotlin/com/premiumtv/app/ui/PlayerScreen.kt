package com.premiumtv.app.ui

import android.content.Context
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.RectangleShape
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.common.PlaybackException
import androidx.media3.common.Player
import androidx.media3.datasource.DefaultHttpDataSource
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.exoplayer.source.DefaultMediaSourceFactory
import androidx.media3.ui.PlayerView
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.Programme

/**
 * Playback with automatic multi-server fallback.
 *
 * A backup feed, a second stream of the same live game or a dead upstream
 * link all used to end in the same dead-end error card. The player now walks
 * the channel's server list by itself: when a feed fails fatally it switches
 * to the next one, says so on screen, and only shows the error card when
 * every server for this channel has been tried.
 *
 * 1.0.8 adds the side player: [expanded] = false renders the same player as
 * a small corner card while the channel browser stays up. The ExoPlayer
 * instance is remembered across the flip — the stream keeps playing when the
 * card grows to the big screen or tucks back into the corner. Clicking the
 * side card ([onExpand]) goes to the big screen; Back on the big screen
 * tucks it into the corner; the card's ✕ is what actually stops playback.
 */
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
) {
    val context = LocalContext.current
    val playlist = remember(channel.url) {
        if (servers.any { it.url == channel.url }) servers else listOf(channel) + servers
    }
    var serverIndex by remember(channel.url) {
        mutableStateOf(playlist.indexOfFirst { it.url == channel.url }.coerceAtLeast(0))
    }
    val current = playlist[serverIndex.coerceIn(0, playlist.lastIndex)]

    var errorMessage by remember { mutableStateOf<String?>(null) }
    var switchNotice by remember { mutableStateOf<String?>(null) }
    var buffering by remember { mutableStateOf(true) }
    val player = remember(current) { buildPlayer(context, current) }

    DisposableEffect(player) {
        val listener = object : Player.Listener {
            override fun onPlayerError(error: PlaybackException) {
                buffering = false
                if (serverIndex < playlist.lastIndex) {
                    // The next server takes over without the viewer doing
                    // anything; the notice explains the jump.
                    serverIndex += 1
                    switchNotice = "This feed stopped responding - switching to server " +
                        "${serverIndex + 1} of ${playlist.size}…"
                } else {
                    switchNotice = null
                    errorMessage = error.message ?: "This stream could not be played."
                }
            }

            override fun onPlaybackStateChanged(playbackState: Int) {
                buffering = playbackState == Player.STATE_BUFFERING
                if (playbackState == Player.STATE_READY) {
                    errorMessage = null
                    switchNotice = null
                }
            }
        }
        player.addListener(listener)
        onDispose {
            player.removeListener(listener)
            player.release()
        }
    }

    // On the big screen, Back tucks the channel into the side player instead
    // of stopping it. With the side player up, Back belongs to the browser
    // underneath (navigating categories and tabs), so no handler is set.
    BackHandler(enabled = expanded) { onMinimize() }

    Box(
        modifier = if (expanded) {
            Modifier
                .fillMaxSize()
                .background(Color.Black)
        } else {
            // Transparent: touches outside the card fall through to the
            // browser underneath.
            Modifier.fillMaxSize()
        },
        contentAlignment = if (expanded) Alignment.TopStart else Alignment.BottomEnd,
    ) {
        Surface(
            modifier = if (expanded) {
                Modifier.fillMaxSize()
            } else {
                Modifier
                    .padding(16.dp)
                    .width(352.dp)
            },
            shape = if (expanded) RectangleShape else RoundedCornerShape(14.dp),
            color = Color.Black,
            border = if (expanded) {
                null
            } else {
                BorderStroke(2.dp, PremiumGold)
            },
        ) {
            Column {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .then(
                            if (expanded) {
                                Modifier.weight(1f)
                            } else {
                                // Clicking the picture (or pressing OK on it)
                                // grows the side player to the big screen.
                                Modifier
                                    .aspectRatio(16f / 9f)
                                    .tvClickable(onExpand)
                            }
                        ),
                ) {
                    AndroidView(
                        modifier = Modifier.fillMaxSize(),
                        factory = { ctx ->
                            PlayerView(ctx).also { view ->
                                view.player = player
                                view.useController = expanded
                                view.controllerShowTimeoutMs = 5000
                            }
                        },
                        update = { view ->
                            view.useController = expanded
                        },
                    )
                    if (!expanded && buffering) {
                        Text(
                            text = "Loading…",
                            style = MaterialTheme.typography.labelSmall,
                            color = Color.White,
                            modifier = Modifier.align(Alignment.Center),
                        )
                    }
                    if (!expanded && errorMessage != null) {
                        Text(
                            text = "All ${playlist.size} servers tried — nothing is answering. " +
                                "The nightly link check removes feeds like this.",
                            style = MaterialTheme.typography.labelSmall,
                            color = MutedText,
                            textAlign = TextAlign.Center,
                            modifier = Modifier
                                .align(Alignment.Center)
                                .padding(horizontal = 12.dp),
                        )
                    }
                }
                if (!expanded) {
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .background(Color(0xFF0B0F14))
                            .padding(horizontal = 10.dp, vertical = 6.dp),
                        verticalAlignment = Alignment.CenterVertically,
                    ) {
                        Text(
                            text = channel.name,
                            style = MaterialTheme.typography.labelSmall,
                            color = Color.White,
                            fontWeight = FontWeight.SemiBold,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f),
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        MiniChip("⤢ Big screen") { onExpand() }
                        Spacer(modifier = Modifier.width(6.dp))
                        MiniChip("✕ Close") { onClose() }
                    }
                }
            }
        }

        if (expanded) {
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
                if (playlist.size > 1) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = "Server ${serverIndex + 1} of ${playlist.size} · automatic fallback on",
                        style = MaterialTheme.typography.labelSmall,
                        color = PremiumGold,
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
                            text = if (playlist.size > 1) {
                                "All ${playlist.size} servers for this channel were tried. " +
                                    (errorMessage.orEmpty())
                            } else {
                                errorMessage.orEmpty()
                            },
                            style = MaterialTheme.typography.bodySmall,
                            color = MutedText,
                            textAlign = TextAlign.Center,
                        )
                        Spacer(modifier = Modifier.height(10.dp))
                        Text(
                            text = "Most failures are dead upstream links. The repository's " +
                                "nightly link check removes them on its next run.",
                            style = MaterialTheme.typography.bodySmall,
                            color = MutedText,
                            textAlign = TextAlign.Center,
                        )
                        Spacer(modifier = Modifier.height(18.dp))
                        Row {
                            FocusButton("Back to channels") { onClose() }
                            if (playlist.size > 1) {
                                Spacer(modifier = Modifier.width(16.dp))
                                FocusButton("Try the servers again") {
                                    errorMessage = null
                                    buffering = true
                                    serverIndex = (serverIndex + 1) % playlist.size
                                }
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

            // Manual server switching (1.0.6): automatic fallback still walks
            // the list on failure, but a viewer whose live event is buffering
            // can jump to the next/previous server themselves.
            Row(
                modifier = Modifier
                    .align(Alignment.BottomEnd)
                    .padding(end = 32.dp, bottom = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(12.dp),
            ) {
                if (playlist.size > 1) {
                    FocusButton("◀ Server") {
                        errorMessage = null
                        buffering = true
                        serverIndex = nextServerIndex(serverIndex, playlist.size, -1)
                        switchNotice = "Server ${serverIndex + 1} of ${playlist.size} · selected by you"
                    }
                    FocusButton("Server ▶") {
                        errorMessage = null
                        buffering = true
                        serverIndex = nextServerIndex(serverIndex, playlist.size, 1)
                        switchNotice = "Server ${serverIndex + 1} of ${playlist.size} · selected by you"
                    }
                }
                FocusButton(if (isFavorite) "★ Favorited" else "☆ Favorite") { onToggleFavorite() }
                // 1.0.8 side player: keep the channel playing in the corner
                // while the channel browser comes back up.
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
    }
}

/** One of the small buttons on the side player's bar. */
@Composable
private fun MiniChip(label: String, onClick: () -> Unit) {
    Surface(
        modifier = Modifier.tvClickable(onClick),
        shape = RoundedCornerShape(14.dp),
        color = Color(0xFF1D2733),
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(horizontal = 10.dp, vertical = 6.dp),
        )
    }
}

private fun buildPlayer(context: Context, channel: Channel): ExoPlayer {
    val headers = HashMap<String, String>()
    if (channel.referrer.isNotBlank()) headers["Referer"] = channel.referrer
    if (channel.origin.isNotBlank()) headers["Origin"] = channel.origin

    var http = DefaultHttpDataSource.Factory()
        .setAllowCrossProtocolRedirects(true)
        .setConnectTimeoutMs(15_000)
        .setReadTimeoutMs(30_000)
    if (headers.isNotEmpty()) http = http.setDefaultRequestProperties(headers)
    if (channel.userAgent.isNotBlank()) http = http.setUserAgent(channel.userAgent)

    val mediaSourceFactory = DefaultMediaSourceFactory(context).setDataSourceFactory(http)
    return ExoPlayer.Builder(context)
        .setMediaSourceFactory(mediaSourceFactory)
        .build()
        .apply {
            setMediaItem(MediaItem.fromUri(channel.url))
            playWhenReady = true
            prepare()
        }
}
