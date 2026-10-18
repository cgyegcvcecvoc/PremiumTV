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
 */
@Composable
fun PlayerScreen(
    channel: Channel,
    servers: List<Channel>,
    programmes: List<Programme>,
    now: Long,
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

    BackHandler { onClose() }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.Black),
    ) {
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { ctx ->
                PlayerView(ctx).also { view ->
                    view.player = player
                    view.useController = true
                    view.controllerShowTimeoutMs = 5000
                }
            },
        )

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

        // Manual server switching (1.0.6): automatic fallback still walks the
        // list on failure, but a viewer whose live event is buffering can jump
        // to the next/previous server themselves instead of waiting it out.
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
        }

        Text(
            text = "Press Back to return to the channel list",
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
            modifier = Modifier
                .align(Alignment.BottomStart)
                .padding(start = 32.dp, bottom = 20.dp),
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
