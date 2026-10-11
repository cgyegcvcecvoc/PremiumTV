package com.premiumtv.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.heightIn
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import coil.compose.AsyncImage
import com.premiumtv.app.BuildConfig
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.Library
import com.premiumtv.app.data.Programme

private enum class Tab(val label: String) {
    Channels("Channels"),
    Guide("Guide"),
    Settings("Settings"),
}

@Composable
fun HomeScreen(
    library: Library,
    now: Long,
    status: String,
    onSelect: (Channel) -> Unit,
    onRefresh: () -> Unit,
    onReset: () -> Unit,
) {
    var tab by remember { mutableStateOf(Tab.Channels) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, top = 18.dp, bottom = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "PremiumTV",
                style = MaterialTheme.typography.headlineSmall,
                color = PremiumGold,
                fontWeight = FontWeight.Bold,
            )
            Spacer(modifier = Modifier.width(28.dp))
            TabChip(Tab.Channels.label, tab == Tab.Channels) { tab = Tab.Channels }
            Spacer(modifier = Modifier.width(12.dp))
            TabChip(Tab.Guide.label, tab == Tab.Guide) { tab = Tab.Guide }
            Spacer(modifier = Modifier.width(12.dp))
            TabChip(Tab.Settings.label, tab == Tab.Settings) { tab = Tab.Settings }
            Spacer(modifier = Modifier.weight(1f))
            Text(
                text = "${library.channels.size} channels · ${library.programmes.size} with guide",
                style = MaterialTheme.typography.labelMedium,
                color = MutedText,
            )
        }

        when (tab) {
            Tab.Channels -> CategoriesScreen(library, now, onSelect)
            Tab.Guide -> GuideScreen(library, now, onSelect)
            Tab.Settings -> SettingsScreen(library, status, onRefresh, onReset)
        }
    }
}

// --------------------------------------------------------------- channels tab

@Composable
private fun CategoriesScreen(
    library: Library,
    now: Long,
    onSelect: (Channel) -> Unit,
) {
    val byGroup = remember(library) { library.channels.groupBy { it.group } }
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 48.dp),
    ) {
        items(items = library.groups, key = { it.name }) { group ->
            val channels = byGroup[group.name].orEmpty()
            if (channels.isNotEmpty()) {
                CategoryRow(
                    name = group.name,
                    count = channels.size,
                    channels = channels,
                    programmes = library.programmes,
                    now = now,
                    onSelect = onSelect,
                )
            }
        }
    }
}

@Composable
private fun CategoryRow(
    name: String,
    count: Int,
    channels: List<Channel>,
    programmes: Map<String, List<Programme>>,
    now: Long,
    onSelect: (Channel) -> Unit,
) {
    Column(modifier = Modifier.fillMaxWidth().padding(vertical = 10.dp)) {
        Row(
            modifier = Modifier.padding(
                start = SCREEN_GUTTER,
                end = SCREEN_GUTTER,
                bottom = 8.dp,
            ),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = name,
                style = MaterialTheme.typography.titleMedium,
                color = Color.White,
                fontWeight = FontWeight.SemiBold,
            )
            Spacer(modifier = Modifier.width(10.dp))
            Text(
                text = count.toString(),
                style = MaterialTheme.typography.labelMedium,
                color = MutedText,
            )
        }
        LazyRow(
            contentPadding = PaddingValues(horizontal = SCREEN_GUTTER),
            horizontalArrangement = Arrangement.spacedBy(CARD_GAP),
        ) {
            items(items = channels, key = { it.id + "|" + it.url }) { channel ->
                val current = nowPlaying(programmes[channel.id].orEmpty(), now)
                ChannelCard(
                    channel = channel,
                    subtitle = current?.title,
                    onClick = { onSelect(channel) },
                )
            }
        }
    }
}

// ------------------------------------------------------------------ guide tab

@Composable
private fun GuideScreen(
    library: Library,
    now: Long,
    onSelect: (Channel) -> Unit,
) {
    val entries = remember(library) {
        library.channels
            .mapNotNull { channel ->
                val list = library.programmes[channel.id]
                if (list.isNullOrEmpty()) null else channel to list
            }
            .sortedBy { it.first.name.lowercase() }
    }

    if (entries.isEmpty()) {
        CenteredMessage(
            "No guide listings are bundled with this build.\n" +
                "Run the repository's EPG build, then android/tools/build_bundle.py."
        )
        return
    }

    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(
            start = SCREEN_GUTTER,
            end = SCREEN_GUTTER,
            bottom = 48.dp,
        ),
        verticalArrangement = Arrangement.spacedBy(10.dp),
    ) {
        item {
            Text(
                text = "What's on now · ${entries.size} channels with listings",
                style = MaterialTheme.typography.titleMedium,
                color = Color.White,
                modifier = Modifier.padding(bottom = 6.dp),
            )
        }
        items(items = entries, key = { it.first.id + "|" + it.first.url }) { (channel, programmes) ->
            GuideRow(
                channel = channel,
                programmes = programmes,
                now = now,
                onClick = { onSelect(channel) },
            )
        }
    }
}

@Composable
private fun GuideRow(
    channel: Channel,
    programmes: List<Programme>,
    now: Long,
    onClick: () -> Unit,
) {
    var focused by remember { mutableStateOf(false) }
    val current = nowPlaying(programmes, now)
    val next = nextUp(programmes, now)

    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .heightIn(min = 96.dp)
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick)
            .border(
                width = if (focused) 2.dp else 1.dp,
                color = if (focused) PremiumGold else Color(0x1AFFFFFF),
                shape = RoundedCornerShape(12.dp),
            ),
        shape = RoundedCornerShape(12.dp),
        color = if (focused) CardBackgroundFocused else CardBackground,
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 12.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Box(
                modifier = Modifier
                    .width(72.dp)
                    .height(56.dp),
                contentAlignment = Alignment.Center,
            ) {
                if (channel.logo.isNotBlank()) {
                    AsyncImage(
                        model = channel.logo,
                        contentDescription = channel.name,
                        contentScale = ContentScale.Fit,
                        modifier = Modifier.fillMaxSize(),
                    )
                } else {
                    Text(
                        text = channel.name.take(2).uppercase(),
                        style = MaterialTheme.typography.titleMedium,
                        color = PremiumGold,
                        fontWeight = FontWeight.Bold,
                    )
                }
            }
            Spacer(modifier = Modifier.width(16.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = channel.name,
                    style = MaterialTheme.typography.titleSmall,
                    color = Color.White,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Spacer(modifier = Modifier.height(4.dp))
                if (current != null) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "NOW",
                            style = MaterialTheme.typography.labelSmall,
                            color = PremiumGold,
                            fontWeight = FontWeight.Bold,
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = current.title,
                            style = MaterialTheme.typography.bodyMedium,
                            color = Color.White,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f, fill = false),
                        )
                        Spacer(modifier = Modifier.width(12.dp))
                        Text(
                            text = formatRange(current.start, current.end),
                            style = MaterialTheme.typography.labelSmall,
                            color = MutedText,
                        )
                    }
                    Spacer(modifier = Modifier.height(6.dp))
                    ProgressLine(fraction = progressOf(current, now))
                } else {
                    Text(
                        text = "Nothing listed at this hour",
                        style = MaterialTheme.typography.bodySmall,
                        color = MutedText,
                    )
                }
                if (next != null) {
                    Spacer(modifier = Modifier.height(6.dp))
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "NEXT",
                            style = MaterialTheme.typography.labelSmall,
                            color = MutedText,
                            fontWeight = FontWeight.Bold,
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = "${formatClock(next.start)} · ${next.title}",
                            style = MaterialTheme.typography.bodySmall,
                            color = MutedText,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun ProgressLine(fraction: Float) {
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(4.dp)
            .background(Color(0x33FFFFFF), RoundedCornerShape(2.dp)),
    ) {
        Box(
            modifier = Modifier
                .fillMaxWidth(fraction.coerceIn(0f, 1f))
                .height(4.dp)
                .background(PremiumGold, RoundedCornerShape(2.dp)),
        )
    }
}

// --------------------------------------------------------------- settings tab

@Composable
private fun SettingsScreen(
    library: Library,
    status: String,
    onRefresh: () -> Unit,
    onReset: () -> Unit,
) {
    val meta = library.meta
    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, bottom = 48.dp),
    ) {
        Text(
            text = "Data bundle",
            style = MaterialTheme.typography.headlineSmall,
            color = Color.White,
            fontWeight = FontWeight.Bold,
        )
        Spacer(modifier = Modifier.height(12.dp))
        InfoRow("App version", BuildConfig.VERSION_NAME)
        InfoRow("Bundle built", meta.generatedUtc.ifBlank { "unknown" })
        InfoRow("Source playlist", meta.playlist.ifBlank { "unknown" })
        InfoRow("Source guide", meta.guide.ifBlank { "unknown" })
        InfoRow("Channels", library.channels.size.toString())
        InfoRow("Categories", library.groups.size.toString())
        InfoRow(
            "Guide listings",
            "${meta.programmeCount} across ${library.programmes.size} channels",
        )
        if (meta.windowStart > 0L) {
            InfoRow("Guide window", "${formatDay(meta.windowStart)} – ${formatDay(meta.windowEnd)}")
        }
        InfoRow(
            "Showing now",
            if (library.refreshed) "Copy downloaded from GitHub" else "Data bundled in this APK",
        )

        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "Update",
            style = MaterialTheme.typography.titleMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
        )
        Spacer(modifier = Modifier.height(12.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            FocusButton("Refresh from GitHub") { onRefresh() }
            FocusButton("Reset to bundled data") { onReset() }
        }
        Spacer(modifier = Modifier.height(12.dp))
        Text(
            text = status.ifBlank {
                "Refresh downloads the playlist and guide straight from this " +
                    "repository. The repository is private today, so the download " +
                    "will fail with HTTP 404 until it is public or mirrored."
            },
            style = MaterialTheme.typography.bodySmall,
            color = MutedText,
        )

        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "Update URLs",
            style = MaterialTheme.typography.titleMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = meta.playlistUrl.ifBlank { "(no playlist URL bundled)" },
            style = MaterialTheme.typography.bodySmall,
            color = MutedText,
        )
        Text(
            text = meta.guideUrl.ifBlank { "(no guide URL bundled)" },
            style = MaterialTheme.typography.bodySmall,
            color = MutedText,
        )

        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "About playback",
            style = MaterialTheme.typography.titleMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "Streams are played with ExoPlayer (Media3). When a playlist entry " +
                "publishes a referrer, an origin or a user-agent, the app sends them, " +
                "because several public feeds refuse the connection without them. " +
                "Plain http streams are allowed for the same reason. A channel that " +
                "will not play is almost always a dead upstream link: the repository's " +
                "nightly link check drops those on its next run.",
            style = MaterialTheme.typography.bodySmall,
            color = MutedText,
        )
        Spacer(modifier = Modifier.height(32.dp))
        Text(
            text = "PremiumTV 1.0.0 beta — a first test build. Publicly listed " +
                "streams only; nothing is hosted by this app.",
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
            textAlign = TextAlign.Start,
        )
    }
}
