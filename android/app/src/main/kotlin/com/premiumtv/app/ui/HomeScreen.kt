package com.premiumtv.app.ui

import android.view.KeyEvent as NativeKey
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.focusGroup
import androidx.compose.foundation.focusable
import androidx.compose.foundation.horizontalScroll
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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.foundation.text.KeyboardActions
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Clear
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.LaunchedEffect
import kotlinx.coroutines.delay
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.input.key.onPreviewKeyEvent
import androidx.compose.ui.platform.LocalFocusManager
import androidx.compose.ui.platform.LocalSoftwareKeyboardController
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.premiumtv.app.BuildConfig
import com.premiumtv.app.data.CategoryGroup
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.Library
import com.premiumtv.app.data.Programme
import com.premiumtv.app.data.RefreshInfo
import com.premiumtv.app.data.RefreshTrigger
import com.premiumtv.app.update.AppUpdateState

/** The home screen's sections. AppRoot keeps the choice while a channel plays. */
enum class HomeTab(val label: String) {
    Channels("Channels"),
    Events("Live Events"),
    Guide("Guide"),
    Settings("Settings"),
}

@Composable
fun HomeScreen(
    library: Library,
    now: Long,
    status: String,
    refreshInfo: RefreshInfo,
    updateInfo: AppUpdateState,
    tab: HomeTab,
    onTabChange: (HomeTab) -> Unit,
    guideState: CableGuideState,
    onSelect: (Channel) -> Unit,
    onForceRefresh: () -> Unit,
    onReset: () -> Unit,
    onCheckForUpdate: () -> Unit,
    onDownloadUpdate: () -> Unit,
    onInstallUpdate: () -> Unit,
) {
    // Back leaves the Guide or Settings for Channels before it leaves the app,
    // the way a cable box's Back/Exit closes its guide.
    BackHandler(enabled = tab != HomeTab.Channels) { onTabChange(HomeTab.Channels) }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .onPreviewKeyEvent { event ->
                // The GUIDE button on a TV remote opens the guide from anywhere.
                val native = event.nativeKeyEvent
                if (native.keyCode == NativeKey.KEYCODE_GUIDE) {
                    if (native.action == NativeKey.ACTION_UP) onTabChange(HomeTab.Guide)
                    true
                } else {
                    false
                }
            },
    ) {
        // The title, the version plaque and the status line share the first row;
        // the tabs get their own scrollable row, so on a narrow screen the
        // weighted status line keeps its width (the emulator smoke check looks
        // for "<count> channels" in it).
        //
        // Preview builds (bundle preview_features: cable-guide) show the
        // cable-style grid as the Guide tab; stable builds keep the "what's on
        // now" list there.
        val cableGuide = library.meta.previewFeatures.contains("cable-guide")
        // The scraper's live-game feeds, grouped by sport for the Live Events
        // tab and for the LIVE labels on the channel cards.
        val liveSections = remember(library.channels) { groupLiveEvents(library.channels) }
        val liveIndex = remember(library.channels) { liveEventIndex(library.channels) }
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, top = 18.dp, bottom = 10.dp),
        ) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(
                    text = "PremiumTV",
                    style = MaterialTheme.typography.headlineSmall,
                    color = PremiumGold,
                    fontWeight = FontWeight.Bold,
                )
                Spacer(modifier = Modifier.width(10.dp))
                VersionPlaque(
                    if (cableGuide) "${BuildConfig.VERSION_NAME} · ENCORE PREVIEW" else BuildConfig.VERSION_NAME,
                )
                Spacer(modifier = Modifier.width(16.dp))
                Text(
                    text = when {
                        library.guideLoading -> "${library.channels.size} channels · Loading guide…"
                        library.guideError != null -> "${library.channels.size} channels · Guide unavailable"
                        else -> "${library.channels.size} channels · ${library.programmes.size} with guide"
                    },
                    style = MaterialTheme.typography.labelMedium,
                    color = if (library.guideLoading) PremiumGold else MutedText,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    textAlign = TextAlign.End,
                    modifier = Modifier.weight(1f),
                )
            }
            Spacer(modifier = Modifier.height(10.dp))
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                TabChip(HomeTab.Channels.label, tab == HomeTab.Channels) { onTabChange(HomeTab.Channels) }
                Spacer(modifier = Modifier.width(12.dp))
                TabChip(HomeTab.Events.label, tab == HomeTab.Events) { onTabChange(HomeTab.Events) }
                Spacer(modifier = Modifier.width(12.dp))
                TabChip(HomeTab.Guide.label, tab == HomeTab.Guide) { onTabChange(HomeTab.Guide) }
                Spacer(modifier = Modifier.width(12.dp))
                TabChip(HomeTab.Settings.label, tab == HomeTab.Settings) { onTabChange(HomeTab.Settings) }
            }
        }

        var wasRefreshing by remember { mutableStateOf(false) }
        var showResult by remember { mutableStateOf(false) }
        val guideStartedAt = remember(library.guideLoading) { System.currentTimeMillis() }
        LaunchedEffect(refreshInfo.inProgress) {
            if (refreshInfo.inProgress) {
                wasRefreshing = true
                showResult = false
            } else if (wasRefreshing) {
                showResult = true
                delay(15_000L)
                showResult = false
            }
        }
        if (refreshInfo.inProgress || library.guideLoading || showResult) {
            LibraryActivity(
                active = refreshInfo.inProgress || library.guideLoading,
                message = when {
                    refreshInfo.inProgress -> status.ifBlank { "Starting refresh…" }
                    library.guideLoading -> "Channels ready · Loading programme guide…"
                    else -> refreshInfo.lastMessage
                },
                startedAt = if (refreshInfo.inProgress) refreshInfo.lastAttemptAtMillis else guideStartedAt,
            )
        }

        when (tab) {
            HomeTab.Channels -> CategoriesScreen(library, now, liveIndex, onSelect)
            HomeTab.Events -> EventsScreen(liveSections, now, onSelect)
            HomeTab.Guide -> if (cableGuide) {
                CableGuideScreen(library = library, now = now, state = guideState, onSelect = onSelect)
            } else {
                GuideScreen(library, now, liveIndex, onSelect)
            }
            HomeTab.Settings -> SettingsScreen(
                library = library,
                status = status,
                refreshInfo = refreshInfo,
                updateInfo = updateInfo,
                onForceRefresh = onForceRefresh,
                onReset = onReset,
                onCheckForUpdate = onCheckForUpdate,
                onDownloadUpdate = onDownloadUpdate,
                onInstallUpdate = onInstallUpdate,
            )
        }
    }
}

// --------------------------------------------------------------- channels tab

@Composable
private fun CategoriesScreen(
    library: Library,
    now: Long,
    liveIndex: Map<String, LiveEvent>,
    onSelect: (Channel) -> Unit,
) {
    var query by rememberSaveable { mutableStateOf("") }
    val trimmed = query.trim()
    val matches = remember(library.channels, trimmed) {
        if (trimmed.isEmpty()) {
            null
        } else {
            val needle = trimmed.lowercase()
            library.channels.filter { channel ->
                channel.name.lowercase().contains(needle) ||
                    channel.group.lowercase().contains(needle) ||
                    channel.country.lowercase().contains(needle) ||
                    channel.chno == trimmed
            }
        }
    }

    Column(modifier = Modifier.fillMaxSize()) {
        // Search lives above the rows so a remote can jump straight to a
        // channel name; the field keeps its own focus row on a TV.
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, bottom = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            ChannelSearchField(
                query = query,
                onQueryChange = { query = it },
                modifier = Modifier.weight(1f),
            )
        }

        if (matches == null) {
            CategoryList(library, now, liveIndex, onSelect)
            return@Column
        }

        if (matches.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(
                    text = "No channels match “$trimmed”.\n\nTry part of a name, a category like News, " +
                        "or a country like US.",
                    style = MaterialTheme.typography.bodyMedium,
                    color = MutedText,
                    textAlign = TextAlign.Center,
                    modifier = Modifier.padding(horizontal = 48.dp),
                )
            }
            return@Column
        }

        val groups = remember(library.groups, matches) {
            val present = matches.groupBy { it.group }
            library.groups.filter { present.containsKey(it.name) } +
                present.keys.filter { key -> library.groups.none { it.name == key } }
                    .map { CategoryGroup(it, present.getValue(it).size) }
        }
        Text(
            text = "${matches.size} channels match “$trimmed”",
            style = MaterialTheme.typography.labelMedium,
            color = PremiumGold,
            modifier = Modifier.padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, top = 4.dp),
        )
        CategoryList(library, now, liveIndex, onSelect, only = groups, subset = matches)
    }
}

@Composable
private fun CategoryList(
    library: Library,
    now: Long,
    liveIndex: Map<String, LiveEvent>,
    onSelect: (Channel) -> Unit,
    only: List<CategoryGroup>? = null,
    subset: List<Channel>? = null,
) {
    val source = subset ?: library.channels
    val byGroup = remember(source) { source.groupBy { it.group } }
    val groups = only ?: library.groups
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 48.dp),
    ) {
        items(items = groups, key = { it.name }) { group ->
            val channels = byGroup[group.name].orEmpty()
            if (channels.isNotEmpty()) {
                CategoryRow(
                    name = group.name,
                    count = channels.size,
                    channels = channels,
                    programmes = library.programmes,
                    liveIndex = liveIndex,
                    now = now,
                    onSelect = onSelect,
                )
            }
        }
    }
}

/** The TV-friendly search field: one focus stop, an on-screen clear key. */
@Composable
private fun ChannelSearchField(
    query: String,
    onQueryChange: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    var focused by remember { mutableStateOf(false) }
    val keyboard = LocalSoftwareKeyboardController.current
    val focusManager = LocalFocusManager.current
    Surface(
        modifier = modifier
            .height(48.dp)
            .onFocusChanged { focused = it.isFocused }
            .border(
                width = if (focused) 2.dp else 1.dp,
                color = if (focused) PremiumGold else Color(0x22FFFFFF),
                shape = RoundedCornerShape(24.dp),
            ),
        shape = RoundedCornerShape(24.dp),
        color = if (focused) CardBackgroundFocused else CardBackground,
    ) {
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 16.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Icon(
                imageVector = Icons.Filled.Search,
                contentDescription = null,
                tint = if (focused) PremiumGold else MutedText,
                modifier = Modifier.size(20.dp),
            )
            Spacer(modifier = Modifier.width(10.dp))
            Box(modifier = Modifier.weight(1f)) {
                if (query.isEmpty()) {
                    Text(
                        text = "Search channels…",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MutedText,
                    )
                }
                BasicTextField(
                    value = query,
                    onValueChange = onQueryChange,
                    singleLine = true,
                    textStyle = MaterialTheme.typography.bodyMedium.copy(color = Color.White),
                    cursorBrush = SolidColor(PremiumGold),
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                    keyboardActions = KeyboardActions(
                        onSearch = {
                            keyboard?.hide()
                            focusManager.clearFocus()
                        },
                    ),
                    modifier = Modifier.fillMaxWidth(),
                )
            }
            if (query.isNotEmpty()) {
                Spacer(modifier = Modifier.width(8.dp))
                Box(
                    modifier = Modifier
                        .size(28.dp)
                        .focusable()
                        .tvClickable { onQueryChange("") },
                    contentAlignment = Alignment.Center,
                ) {
                    Icon(
                        imageVector = Icons.Filled.Clear,
                        contentDescription = "Clear search",
                        tint = MutedText,
                        modifier = Modifier.size(18.dp),
                    )
                }
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
    liveIndex: Map<String, LiveEvent>,
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
            modifier = Modifier.focusGroup(),
            contentPadding = PaddingValues(horizontal = SCREEN_GUTTER),
            horizontalArrangement = Arrangement.spacedBy(CARD_GAP),
        ) {
            itemsIndexed(
                items = channels,
                key = { index, channel -> "$index|${channel.id}|${channel.url}" },
            ) { _, channel ->
                val current = nowPlaying(programmes[channel.id].orEmpty(), now)
                val event = liveIndex[channel.url]
                ChannelCard(
                    channel = channel,
                    subtitle = when {
                        current != null -> current.title
                        event != null -> "LIVE · ${event.sport}"
                        else -> "No listing published"
                    },
                    onClick = { onSelect(channel) },
                )
            }
        }
    }
}

// ---------------------------------------------------------- live events tab

@Composable
private fun EventsScreen(
    sections: List<LiveEventSection>,
    now: Long,
    onSelect: (Channel) -> Unit,
) {
    if (sections.isEmpty()) {
        CenteredMessage(
            "No live games are in the current playlist.\n\n" +
                "Game feeds appear here while the repository's scrapers find " +
                "them on air - check back around kickoff, or browse the " +
                "Sports channels in the Channels tab."
        )
        return
    }
    val totalGames = sections.sumOf { it.events.size }
    val totalFeeds = sections.sumOf { section -> section.events.sumOf { it.servers.size } }
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 48.dp),
    ) {
        item(key = "events-head") {
            Column(
                modifier = Modifier.padding(
                    start = SCREEN_GUTTER,
                    end = SCREEN_GUTTER,
                    top = 8.dp,
                    bottom = 2.dp,
                ),
            ) {
                Text(
                    text = "Live games on now",
                    style = MaterialTheme.typography.titleMedium,
                    color = Color.White,
                    fontWeight = FontWeight.SemiBold,
                )
                Text(
                    text = "$totalGames games across $totalFeeds streams · grouped by sport · " +
                        "a game with more than one stream switches servers by itself",
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                )
            }
        }
        items(items = sections, key = { "section|${it.sport}" }) { section ->
            Column(modifier = Modifier.fillMaxWidth().padding(vertical = 8.dp)) {
                Row(
                    modifier = Modifier.padding(
                        start = SCREEN_GUTTER,
                        end = SCREEN_GUTTER,
                        bottom = 8.dp,
                    ),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    Icon(
                        imageVector = placeholderIconFor(section.sport),
                        contentDescription = null,
                        tint = PremiumGold,
                        modifier = Modifier.size(22.dp),
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Text(
                        text = section.sport,
                        style = MaterialTheme.typography.titleMedium,
                        color = Color.White,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Spacer(modifier = Modifier.width(10.dp))
                    Text(
                        text = section.events.size.toString(),
                        style = MaterialTheme.typography.labelMedium,
                        color = MutedText,
                    )
                }
                LazyRow(
                    modifier = Modifier.focusGroup(),
                    contentPadding = PaddingValues(horizontal = SCREEN_GUTTER),
                    horizontalArrangement = Arrangement.spacedBy(CARD_GAP),
                ) {
                    itemsIndexed(
                        items = section.events,
                        key = { index, event -> "$index|${event.key}" },
                    ) { _, event ->
                        EventCard(event = event, onClick = { onSelect(event.servers.first()) })
                    }
                }
            }
        }
    }
}

@Composable
private fun EventCard(
    event: LiveEvent,
    onClick: () -> Unit,
) {
    var focused by remember { mutableStateOf(false) }
    val scale by androidx.compose.animation.core.animateFloatAsState(
        targetValue = if (focused) 1.04f else 1f,
        label = "eventCardScale",
    )
    Surface(
        modifier = Modifier
            .width(280.dp)
            .height(128.dp)
            .scale(scale)
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick),
        shape = RoundedCornerShape(12.dp),
        color = if (focused) CardBackgroundFocused else CardBackground,
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .border(
                    width = if (focused) 3.dp else 1.dp,
                    color = if (focused) PremiumGold else Color(0x22FFFFFF),
                    shape = RoundedCornerShape(12.dp),
                )
                .padding(12.dp),
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    modifier = Modifier
                        .background(LiveRed, RoundedCornerShape(4.dp))
                        .padding(horizontal = 6.dp, vertical = 2.dp),
                ) {
                    Text(
                        text = "LIVE",
                        style = MaterialTheme.typography.labelSmall,
                        color = Color.White,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 0.8.sp,
                    )
                }
                Spacer(modifier = Modifier.width(8.dp))
                Text(
                    text = event.sport,
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            Spacer(modifier = Modifier.height(8.dp))
            Text(
                text = event.title,
                style = MaterialTheme.typography.titleSmall,
                color = Color.White,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f),
            )
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = Icons.Filled.PlayArrow,
                    contentDescription = null,
                    tint = PremiumGold,
                    modifier = Modifier.size(14.dp),
                )
                Spacer(modifier = Modifier.width(6.dp))
                Text(
                    text = if (event.servers.size > 1) {
                        "${event.servers.size} streams · automatic fallback"
                    } else {
                        "1 stream"
                    },
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                    maxLines = 1,
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
    liveIndex: Map<String, LiveEvent>,
    onSelect: (Channel) -> Unit,
) {
    if (library.guideLoading) {
        CenteredMessage("Channels are ready.\nLoading programme listings…")
        return
    }
    if (library.guideError != null) {
        CenteredMessage(
            "${library.guideError}\n\n" +
                "You can still browse and play channels from the Channels tab."
        )
        return
    }

    val entries = remember(library.channels, library.programmes, liveIndex, now) {
        val withGuide = library.channels
            .mapNotNull { channel ->
                val list = library.programmes[channel.id]
                if (list.isNullOrEmpty()) null else channel to list
            }
        // The scrapers' live-game feeds share placeholder EPG ids, so no
        // upstream guide ever lists them. The name itself says what is on:
        // show the matchup as the listing instead of "nothing listed".
        val eventRows = library.channels.mapNotNull { channel ->
            val event = liveIndex[channel.url] ?: return@mapNotNull null
            if (!library.programmes[channel.id].isNullOrEmpty()) return@mapNotNull null
            channel to listOf(
                Programme(
                    channelId = channel.id,
                    start = now - 6L * 3600L,
                    end = now + 18L * 3600L,
                    title = event.title,
                    desc = "Live ${event.sport} event feed. Game streams are " +
                        "published without an upstream schedule, so the " +
                        "matchup comes from the playlist itself.",
                    category = event.sport,
                    icon = "",
                    episode = "",
                ),
            )
        }
        (withGuide + eventRows).sortedBy { it.first.name.lowercase() }
    }

    if (entries.isEmpty()) {
        CenteredMessage(
            "No programme listings are in this build.\n" +
                "Every channel still opens from the Channels tab."
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
        itemsIndexed(
            items = entries,
            key = { index, entry -> "$index|${entry.first.id}|${entry.first.url}" },
        ) { _, entry ->
            val (channel, programmes) = entry
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
                ChannelLogoBox(
                    channel = channel,
                    modifier = Modifier.fillMaxSize(),
                )
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
                        Box(
                            modifier = Modifier
                                .background(LiveRed, RoundedCornerShape(4.dp))
                                .padding(horizontal = 6.dp, vertical = 2.dp),
                        ) {
                            Text(
                                text = "NOW",
                                style = MaterialTheme.typography.labelSmall,
                                color = Color.White,
                                fontWeight = FontWeight.Bold,
                                letterSpacing = 0.6.sp,
                            )
                        }
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

/** Small playbill-style plaque: the shipped version under the brand name. */
@Composable
private fun VersionPlaque(version: String) {
    Box(
        modifier = Modifier
            .border(
                width = 1.dp,
                color = PremiumGoldDim,
                shape = RoundedCornerShape(6.dp),
            )
            .padding(horizontal = 8.dp, vertical = 3.dp),
    ) {
        Text(
            text = version,
            style = MaterialTheme.typography.labelSmall,
            color = PremiumGoldDim,
            fontWeight = FontWeight.SemiBold,
            letterSpacing = 0.8.sp,
            maxLines = 1,
        )
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

private fun formatMegabytes(bytes: Long): String =
    String.format(java.util.Locale.US, "%.1f MB", bytes / (1024.0 * 1024.0))

@Composable
private fun SettingsScreen(
    library: Library,
    status: String,
    refreshInfo: RefreshInfo,
    updateInfo: AppUpdateState,
    onForceRefresh: () -> Unit,
    onReset: () -> Unit,
    onCheckForUpdate: () -> Unit,
    onDownloadUpdate: () -> Unit,
    onInstallUpdate: () -> Unit,
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
        InfoRow("Library scope", if (meta.libraryScope == "all") "Global · preview" else "USA · stable")
        if (meta.previewFeatures.isNotEmpty()) {
            InfoRow("Preview features", meta.previewFeatures.sorted().joinToString())
        }
        InfoRow("Bundle built", meta.generatedUtc.ifBlank { "unknown" })
        InfoRow("Source playlist", meta.playlist.ifBlank { "unknown" })
        InfoRow("Source guide", meta.guide.ifBlank { "unknown" })
        InfoRow("Channels", library.channels.size.toString())
        InfoRow("Categories", library.groups.size.toString())
        InfoRow(
            "Guide listings",
            when {
                library.guideLoading -> "Loading programme listings…"
                library.guideError != null -> "Unavailable — channels are still ready"
                else -> "${library.meta.programmeCount} across ${library.programmes.size} channels"
            },
        )
        if (meta.windowStart > 0L) {
            InfoRow("Guide window", "${formatDay(meta.windowStart)} – ${formatDay(meta.windowEnd)}")
        }
        InfoRow(
            "Showing now",
            if (library.refreshed) "Latest copy downloaded by the app" else "Data bundled in this APK",
        )

        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "App updates",
            style = MaterialTheme.typography.titleMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
        )
        Spacer(modifier = Modifier.height(8.dp))
        InfoRow("Installed version", updateInfo.currentVersion)
        InfoRow(
            "Newest stable release",
            updateInfo.latestStableVersion ?: "Not checked yet",
        )
        if (updateInfo.updateAvailable) {
            InfoRow(
                "Update available",
                buildString {
                    append(updateInfo.availableVersion.orEmpty())
                    if (updateInfo.installerSize > 0L) {
                        append(" · ")
                        append(formatMegabytes(updateInfo.installerSize))
                    }
                },
            )
        }
        InfoRow(
            "Last update check",
            if (updateInfo.lastCheckedAtMillis > 0L) {
                formatRefreshInstant(updateInfo.lastCheckedAtMillis)
            } else {
                "Not yet"
            },
        )
        Text(
            text = updateInfo.message,
            style = MaterialTheme.typography.bodySmall,
            color = if (updateInfo.error != null) Color(0xFFFF8A80) else MutedText,
        )
        Spacer(modifier = Modifier.height(12.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            FocusButton(
                if (updateInfo.checking) "Checking for updates…" else "Check for updates",
                enabled = !updateInfo.busy,
            ) { onCheckForUpdate() }
            if (updateInfo.updateAvailable) {
                FocusButton(
                    when {
                        updateInfo.downloading && updateInfo.progressPercent >= 0 ->
                            "Downloading… ${updateInfo.progressPercent}%"
                        updateInfo.downloading -> "Downloading…"
                        updateInfo.installerReady -> "Install update"
                        else -> "Download update"
                    },
                    enabled = !updateInfo.busy,
                ) {
                    if (updateInfo.installerReady) onInstallUpdate() else onDownloadUpdate()
                }
            }
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "Only a published stable release above ${updateInfo.currentVersion} is " +
                "offered. The check runs at most once a day and sends GitHub the last ETag, " +
                "so an unchanged release costs one tiny response. The installer downloads " +
                "only when you press the button, is verified against the release's SHA-256 " +
                "file, and is reused instead of downloaded again.",
            style = MaterialTheme.typography.bodySmall,
            color = MutedText,
        )

        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "Automatic refresh",
            style = MaterialTheme.typography.titleMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
        )
        Spacer(modifier = Modifier.height(8.dp))
        InfoRow(
            "Background updates",
            when {
                refreshInfo.inProgress && refreshInfo.lastTrigger == RefreshTrigger.Automatic ->
                    "On — checking now"
                else -> "On — waits for a connected network"
            },
        )
        InfoRow(
            "Next background check",
            if (refreshInfo.nextAutomaticAtMillis > 0L) {
                formatRefreshInstant(refreshInfo.nextAutomaticAtMillis)
            } else {
                "Being scheduled"
            },
        )
        InfoRow(
            "Last successful refresh",
            if (refreshInfo.lastSuccessAtMillis > 0L) {
                formatRefreshInstant(refreshInfo.lastSuccessAtMillis)
            } else {
                "Not yet"
            },
        )
        if (refreshInfo.lastAttemptAtMillis > 0L) {
            InfoRow("Last refresh result", refreshInfo.lastMessage)
        }
        Text(
            text = "PremiumTV checks shortly after the repository's playlist, " +
                "quick-update and guide publishing windows. Android may defer a " +
                "background check while the device is asleep. Unchanged files use " +
                "HTTP validators, so they are not downloaded again.",
            style = MaterialTheme.typography.bodySmall,
            color = MutedText,
        )

        Spacer(modifier = Modifier.height(24.dp))
        Text(
            text = "Refresh now",
            style = MaterialTheme.typography.titleMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
        )
        Spacer(modifier = Modifier.height(12.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
            FocusButton(
                if (refreshInfo.inProgress) "Refreshing all data…" else "Force refresh all now",
                enabled = !refreshInfo.inProgress && !library.guideLoading,
            ) { onForceRefresh() }
            FocusButton("Reset to bundled data", enabled = !refreshInfo.inProgress && !library.guideLoading) { onReset() }
        }
        Spacer(modifier = Modifier.height(12.dp))
        Text(
            text = status.ifBlank {
                "Force refresh bypasses saved validators and downloads both the complete " +
                    "channel list and programme guide, then replaces the cache only after " +
                    "both files parse successfully."
            },
            style = MaterialTheme.typography.bodySmall,
            color = MutedText,
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "Refreshes download the playlist and the guide from the public " +
                "repository on raw.githubusercontent.com; no account is needed. If a " +
                "download fails, the copy already on this device stays in use. The " +
                "global preview's guide is a large file (about 38 MB of XML), so a " +
                "forced refresh can take a minute on a TV.",
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
            text = "PremiumTV ${BuildConfig.VERSION_NAME} — every channel, one guide. " +
                "Publicly listed streams only; nothing is hosted by this app.",
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
            textAlign = TextAlign.Start,
        )
    }
}
