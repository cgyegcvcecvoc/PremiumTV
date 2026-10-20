package com.premiumtv.app.ui

import android.view.KeyEvent as NativeKey
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.BorderStroke
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
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items as gridItems
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
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.SolidColor
import androidx.compose.ui.graphics.vector.ImageVector
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
import com.premiumtv.app.update.DiagnosticStatus
import com.premiumtv.app.update.DiagnosticsReport

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
    diagnostics: DiagnosticsReport?,
    diagnosticsRunning: Boolean,
    tab: HomeTab,
    onTabChange: (HomeTab) -> Unit,
    guideState: CableGuideState,
    recentChannels: List<Channel> = emptyList(),
    favoriteChannels: List<Channel> = emptyList(),
    favoriteUrls: Set<String> = emptySet(),
    onToggleFavorite: (Channel) -> Unit = {},
    onSelect: (Channel) -> Unit,
    onForceRefresh: () -> Unit,
    onReset: () -> Unit,
    onCheckForUpdate: () -> Unit,
    onDownloadUpdate: () -> Unit,
    onInstallUpdate: () -> Unit,
    onCheckForBugs: () -> Unit,
    // 1.0.8 Live Events: which games' feeds answered the live check.
    liveFeedStatus: Map<String, LiveFeedStatus> = emptyMap(),
    liveProbeRunning: Boolean = false,
    onProbeLiveEvents: () -> Unit = {},
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
        // Opening the Live Events tab asks each game's feed whether it still
        // answers (once); the tab's own refresh button re-asks on demand.
        LaunchedEffect(tab, liveSections) {
            if (tab == HomeTab.Events && liveSections.isNotEmpty() && liveFeedStatus.isEmpty()) {
                onProbeLiveEvents()
            }
        }
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
                VersionPlaque(BuildConfig.VERSION_NAME)
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
            HomeTab.Channels -> CategoriesScreen(library, now, liveIndex, onSelect, recentChannels, favoriteChannels, favoriteUrls, onToggleFavorite)
            HomeTab.Events -> EventsScreen(
                sections = liveSections,
                feedStatus = liveFeedStatus,
                probeRunning = liveProbeRunning,
                onSelect = onSelect,
                onRefresh = onProbeLiveEvents,
            )
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
                diagnostics = diagnostics,
                diagnosticsRunning = diagnosticsRunning,
                onForceRefresh = onForceRefresh,
                onReset = onReset,
                onCheckForUpdate = onCheckForUpdate,
                onDownloadUpdate = onDownloadUpdate,
                onInstallUpdate = onInstallUpdate,
                onCheckForBugs = onCheckForBugs,
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
    recentChannels: List<Channel> = emptyList(),
    favoriteChannels: List<Channel> = emptyList(),
    favoriteUrls: Set<String> = emptySet(),
    onToggleFavorite: (Channel) -> Unit = {},
) {
    // 1.0.8, two levels like a cable box: the tab is a LIST of categories,
    // and opening one lands on that category's own page. Back leaves the
    // page before it leaves the tab.
    var selectedCategory by rememberSaveable { mutableStateOf<String?>(null) }
    var categorySort by rememberSaveable { mutableStateOf(CategorySort.Published) }
    var channelSort by rememberSaveable { mutableStateOf(ChannelSort.Default) }
    var query by rememberSaveable { mutableStateOf("") }
    val trimmed = query.trim()

    BackHandler(enabled = selectedCategory != null) { selectedCategory = null }

    // Without a category open, the search field matches every channel; on a
    // category page the same field narrows just that category.
    val matches = remember(library.channels, trimmed, selectedCategory) {
        if (trimmed.isEmpty()) {
            null
        } else {
            val needle = trimmed.lowercase()
            val pool = if (selectedCategory == null) {
                library.channels
            } else {
                library.channels.filter { it.group == selectedCategory }
            }
            pool.filter { channel ->
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

        val category = selectedCategory
        when {
            // ------------------------------------------------ category list
            category == null && matches == null -> {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, top = 2.dp, bottom = 8.dp),
                    verticalAlignment = Alignment.CenterVertically,
                ) {
                    // One cycling button: Published -> A-Z -> Z-A -> biggest.
                    FocusButton("Sort · ${categorySort.label}") { categorySort = categorySort.next }
                    Spacer(modifier = Modifier.width(12.dp))
                    Text(
                        text = "Sort the category list",
                        style = MaterialTheme.typography.labelSmall,
                        color = MutedText,
                    )
                }
                CategoryListScreen(
                    library = library,
                    sort = categorySort,
                    recentChannels = recentChannels,
                    favoriteChannels = favoriteChannels,
                    onSelectCategory = {
                        selectedCategory = it
                        query = ""
                    },
                )
            }

            // ---------------------------------------------- search results
            category == null -> {
                val found = matches.orEmpty()
                Text(
                    text = "${found.size} channels match “$trimmed”",
                    style = MaterialTheme.typography.labelMedium,
                    color = PremiumGold,
                    modifier = Modifier.padding(
                        start = SCREEN_GUTTER,
                        end = SCREEN_GUTTER,
                        top = 4.dp,
                        bottom = 4.dp,
                    ),
                )
                if (found.isEmpty()) {
                    CenteredMessage(
                        "No channels match “$trimmed”.\n\nTry part of a name, a category like News, " +
                            "or a country like US.",
                    )
                } else {
                    ChannelGrid(
                        channels = channelSort.sort(found),
                        programmes = library.programmes,
                        liveIndex = liveIndex,
                        now = now,
                        favoriteUrls = favoriteUrls,
                        onToggleFavorite = onToggleFavorite,
                        onSelect = onSelect,
                    )
                }
            }

            // --------------------------------------------- category page
            else -> {
                val channels = remember(library.channels, category) {
                    when (category) {
                        SHELF_RECENT -> recentChannels
                        SHELF_FAVORITES -> favoriteChannels
                        else -> library.channels.filter { it.group == category }
                    }
                }
                val visible = remember(channels, trimmed, channelSort) {
                    val needle = trimmed.lowercase()
                    val filtered = if (trimmed.isEmpty()) {
                        channels
                    } else {
                        channels.filter { channel ->
                            channel.name.lowercase().contains(needle) ||
                                channel.country.lowercase().contains(needle) ||
                                channel.chno == trimmed
                        }
                    }
                    channelSort.sort(filtered)
                }
                CategoryPageScreen(
                    name = category,
                    totalCount = channels.size,
                    visibleCount = visible.size,
                    query = trimmed,
                    sortLabel = "Sort · ${channelSort.label}",
                    onSortChange = { channelSort = channelSort.next },
                    onBack = { selectedCategory = null },
                ) {
                    if (visible.isEmpty()) {
                        CenteredMessage("No channels in $category match “$trimmed”.")
                    } else {
                        ChannelGrid(
                            channels = visible,
                            programmes = library.programmes,
                            liveIndex = liveIndex,
                            now = now,
                            favoriteUrls = favoriteUrls,
                            onToggleFavorite = onToggleFavorite,
                            onSelect = onSelect,
                        )
                    }
                }
            }
        }
    }
}

/** The two personal shelves, which open like categories but hold their own lists. */
private const val SHELF_RECENT = "Recently watched"
private const val SHELF_FAVORITES = "Favorites"

/** The category page: back to the list, the category's own channels, its own sort. */
@Composable
private fun CategoryPageScreen(
    name: String,
    totalCount: Int,
    visibleCount: Int,
    query: String,
    sortLabel: String,
    onSortChange: () -> Unit,
    onBack: () -> Unit,
    content: @Composable () -> Unit,
) {
    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, top = 2.dp, bottom = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            FocusButton("◀ All categories") { onBack() }
            Spacer(modifier = Modifier.width(14.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = name,
                    style = MaterialTheme.typography.titleMedium,
                    color = Color.White,
                    fontWeight = FontWeight.SemiBold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
                Text(
                    text = if (query.isBlank()) "$totalCount channels" else "$visibleCount of $totalCount channels match",
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                )
            }
            Spacer(modifier = Modifier.width(12.dp))
            FocusButton(sortLabel) { onSortChange() }
        }
        content()
    }
}

/** The tab-level category list: one row per category, name left, count right. */
@Composable
private fun CategoryListScreen(
    library: Library,
    sort: CategorySort,
    recentChannels: List<Channel>,
    favoriteChannels: List<Channel>,
    onSelectCategory: (String) -> Unit,
) {
    val byGroup = remember(library.channels) { library.channels.groupBy { it.group } }
    val categories = remember(library.groups, sort) { sort.sort(library.groups) }
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(top = 2.dp, bottom = 48.dp),
    ) {
        // The viewer's own shelves lead the list (1.0.6): Recently watched is
        // where a channel you opened goes, so you can jump straight back in.
        if (recentChannels.isNotEmpty()) {
            item(key = "shelf|recent") {
                CategoryListRow(
                    name = SHELF_RECENT,
                    count = recentChannels.size,
                    glyph = "◷",
                    onClick = { onSelectCategory(SHELF_RECENT) },
                )
            }
        }
        if (favoriteChannels.isNotEmpty()) {
            item(key = "shelf|favorites") {
                CategoryListRow(
                    name = SHELF_FAVORITES,
                    count = favoriteChannels.size,
                    glyph = "★",
                    onClick = { onSelectCategory(SHELF_FAVORITES) },
                )
            }
        }
        items(items = categories, key = { it.name }) { group ->
            val channels = byGroup[group.name].orEmpty()
            if (channels.isNotEmpty()) {
                CategoryListRow(
                    name = group.name,
                    count = channels.size,
                    icon = placeholderIconFor(group.name),
                    onClick = { onSelectCategory(group.name) },
                )
            }
        }
    }
}

/** One row of the category list: the drawn category mark, the name, the count. */
@Composable
private fun CategoryListRow(
    name: String,
    count: Int,
    onClick: () -> Unit,
    icon: ImageVector? = null,
    glyph: String? = null,
) {
    var focused by remember { mutableStateOf(false) }
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .padding(horizontal = SCREEN_GUTTER)
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick)
            .border(
                width = if (focused) 2.dp else 1.dp,
                color = if (focused) PremiumGold else Color(0x22FFFFFF),
                shape = RoundedCornerShape(12.dp),
            ),
        shape = RoundedCornerShape(12.dp),
        color = if (focused) CardBackgroundFocused else CardBackground,
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            if (icon != null) {
                Icon(
                    imageVector = icon,
                    contentDescription = null,
                    tint = PremiumGold,
                    modifier = Modifier.size(24.dp),
                )
                Spacer(modifier = Modifier.width(12.dp))
            }
            if (glyph != null) {
                Text(
                    text = glyph,
                    color = PremiumGold,
                    fontWeight = FontWeight.Bold,
                    fontSize = 17.sp,
                )
                Spacer(modifier = Modifier.width(12.dp))
            }
            Text(
                text = name,
                style = MaterialTheme.typography.bodyLarge,
                color = Color.White,
                fontWeight = FontWeight.SemiBold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f),
            )
            // Categories read as a list: the channel count sits small on the right edge,
            // with a chevron saying the row opens a page.
            Text(
                text = count.toString(),
                style = MaterialTheme.typography.labelMedium,
                color = MutedText,
            )
            Spacer(modifier = Modifier.width(10.dp))
            Text(
                text = "❯",
                color = if (focused) PremiumGold else MutedText,
                fontWeight = FontWeight.Bold,
            )
        }
    }
}

/** The full-width card grid a category page (or a search) shows its channels in. */
@Composable
private fun ChannelGrid(
    channels: List<Channel>,
    programmes: Map<String, List<Programme>>,
    liveIndex: Map<String, LiveEvent>,
    now: Long,
    favoriteUrls: Set<String>,
    onToggleFavorite: (Channel) -> Unit,
    onSelect: (Channel) -> Unit,
) {
    LazyVerticalGrid(
        columns = GridCells.Adaptive(168.dp),
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(
            start = SCREEN_GUTTER,
            end = SCREEN_GUTTER,
            top = 4.dp,
            bottom = 48.dp,
        ),
        horizontalArrangement = Arrangement.spacedBy(CARD_GAP),
        verticalArrangement = Arrangement.spacedBy(CARD_GAP),
    ) {
        gridItems(
            items = channels,
            key = { "${it.id}|${it.url}" },
        ) { channel ->
            val current = nowPlaying(programmes[channel.id].orEmpty(), now)
            val event = liveIndex[channel.url]
            ChannelCard(
                channel = channel,
                isFavorite = channel.url in favoriteUrls,
                onToggleFavorite = { onToggleFavorite(channel) },
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

/**
 * The TV-friendly search field: click-to-activate (1.0.6).
 *
 * D-pad focus merely passing over the field used to put it straight into
 * editing mode, so browsing past it "automatically searched". Now focus only
 * highlights it; an explicit OK/click opens editing (and the keyboard), and
 * the IME Search action or Back closes it again. One focus stop either way.
 */
@Composable
private fun ChannelSearchField(
    query: String,
    onQueryChange: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    var focused by remember { mutableStateOf(false) }
    var editing by remember { mutableStateOf(false) }
    val keyboard = LocalSoftwareKeyboardController.current
    val focusManager = LocalFocusManager.current
    val editFocus = remember { FocusRequester() }
    LaunchedEffect(editing) {
        if (editing) {
            editFocus.requestFocus()
            keyboard?.show()
        }
    }
    Surface(
        modifier = modifier
            .height(48.dp)
            .onFocusChanged { focused = it.isFocused }
            // Activation is a click/OK only: focus (the TV "hover") highlights
            // the field but must not open the keyboard or start a search.
            .then(if (editing) Modifier else Modifier.tvClickable { editing = true })
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
                        text = if (editing) "Type to search…" else "Click OK to search channels…",
                        style = MaterialTheme.typography.bodyMedium,
                        color = MutedText,
                    )
                }
                if (editing) {
                    BasicTextField(
                        value = query,
                        onValueChange = onQueryChange,
                        singleLine = true,
                        textStyle = MaterialTheme.typography.bodyMedium.copy(color = Color.White),
                        cursorBrush = SolidColor(PremiumGold),
                        keyboardOptions = KeyboardOptions(imeAction = ImeAction.Search),
                        keyboardActions = KeyboardActions(
                            onSearch = {
                                editing = false
                                keyboard?.hide()
                                focusManager.clearFocus()
                            },
                        ),
                        modifier = Modifier
                            .fillMaxWidth()
                            .focusRequester(editFocus),
                    )
                } else if (query.isNotEmpty()) {
                    Text(
                        text = query,
                        style = MaterialTheme.typography.bodyMedium,
                        color = Color.White,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
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

// ---------------------------------------------------------- live events tab

@Composable
private fun EventsScreen(
    sections: List<LiveEventSection>,
    feedStatus: Map<String, LiveFeedStatus>,
    probeRunning: Boolean,
    onSelect: (Channel) -> Unit,
    onRefresh: () -> Unit,
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
    // The refresh button (and opening this tab) asks every game's feed
    // whether it still answers, so the tab can show which games are live.
    val answering = feedStatus.values.count { it == LiveFeedStatus.Answering }
    val decided = feedStatus.values.count { it != LiveFeedStatus.Checking }
    LazyColumn(
        modifier = Modifier.fillMaxSize(),
        contentPadding = PaddingValues(bottom = 48.dp),
    ) {
        item(key = "events-head") {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, top = 8.dp, bottom = 2.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Column(modifier = Modifier.weight(1f)) {
                    Text(
                        text = "Live games on now",
                        style = MaterialTheme.typography.titleMedium,
                        color = Color.White,
                        fontWeight = FontWeight.SemiBold,
                    )
                    Text(
                        text = when {
                            probeRunning -> "Checking which games are still on air…"
                            decided > 0 -> "$totalGames games across $totalFeeds streams · " +
                                "$answering of $decided checked live"
                            else -> "$totalGames games across $totalFeeds streams · grouped by sport · " +
                                "a game with more than one stream switches servers by itself"
                        },
                        style = MaterialTheme.typography.labelSmall,
                        color = if (probeRunning) PremiumGold else MutedText,
                    )
                }
                Spacer(modifier = Modifier.width(12.dp))
                // The tab's own refresh: pulls the newest playlist, then
                // re-asks every game whether its feed is still answering.
                FocusButton(
                    if (probeRunning) "Refreshing…" else "⟳ Refresh live games",
                    enabled = !probeRunning,
                ) { onRefresh() }
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
                        key = { _, event -> event.key },
                    ) { _, event ->
                        EventCard(
                            event = event,
                            status = feedStatus[event.key],
                            onClick = { onSelect(event.servers.first()) },
                        )
                    }
                }
            }
        }
    }
}

@Composable
private fun EventCard(
    event: LiveEvent,
    status: LiveFeedStatus?,
    onClick: () -> Unit,
) {
    var focused by remember { mutableStateOf(false) }
    val scale by androidx.compose.animation.core.animateFloatAsState(
        targetValue = if (focused) 1.03f else 1f,
        label = "eventCardScale",
    )
    val teams = remember(event.title) { teamsOf(event.title) }
    Surface(
        modifier = Modifier
            .width(320.dp)
            .height(172.dp)
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
                // Live or not: the pill answers it. A game nobody has checked
                // yet keeps the plain LIVE pill; a check that got an answer
                // confirms it; silence turns the pill grey.
                val (pillColor, pillText) = when (status) {
                    LiveFeedStatus.Answering -> LiveRed to "LIVE"
                    LiveFeedStatus.Silent -> Color(0xFF57626F) to "NO SIGNAL"
                    LiveFeedStatus.Checking, null -> PremiumGoldDim to "CHECKING"
                }
                Box(
                    modifier = Modifier
                        .background(pillColor, RoundedCornerShape(4.dp))
                        .padding(horizontal = 6.dp, vertical = 2.dp),
                ) {
                    Text(
                        text = pillText,
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
            if (teams != null) {
                EventTeamRow(name = teams.first)
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    text = "vs",
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                    modifier = Modifier.padding(start = 44.dp),
                )
                Spacer(modifier = Modifier.height(2.dp))
                EventTeamRow(name = teams.second)
            } else {
                Text(
                    text = event.title,
                    style = MaterialTheme.typography.titleSmall,
                    color = Color.White,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier.weight(1f),
                )
            }
            Spacer(modifier = Modifier.weight(1f))
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

/** One team line of an event card: its badge and its name. */
@Composable
private fun EventTeamRow(name: String) {
    Row(verticalAlignment = Alignment.CenterVertically) {
        TeamCrest(name = name, size = 34.dp)
        Spacer(modifier = Modifier.width(10.dp))
        Text(
            text = name,
            style = MaterialTheme.typography.bodyMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
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
    diagnostics: DiagnosticsReport?,
    diagnosticsRunning: Boolean,
    onForceRefresh: () -> Unit,
    onReset: () -> Unit,
    onCheckForUpdate: () -> Unit,
    onDownloadUpdate: () -> Unit,
    onInstallUpdate: () -> Unit,
    onCheckForBugs: () -> Unit,
) {
    val meta = library.meta
    var showDetails by rememberSaveable { mutableStateOf(false) }
    val busy = refreshInfo.inProgress || library.guideLoading
    val guideLine = when {
        library.guideLoading -> "loading…"
        library.guideError != null -> "unavailable"
        else -> "${library.programmes.size} channels with guide"
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(rememberScrollState())
            .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, bottom = 48.dp),
    ) {
        // ---------------------------------------------------- version card
        // One compact card replaces the old three headings: the version, what
        // it carries and the only three actions most people need.
        Surface(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(16.dp),
            color = CardBackground,
            border = BorderStroke(1.dp, PremiumGoldDim.copy(alpha = 0.45f)),
        ) {
            Column(modifier = Modifier.padding(horizontal = 20.dp, vertical = 16.dp)) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Column(modifier = Modifier.weight(1f)) {
                        Text(
                            text = "PremiumTV",
                            style = MaterialTheme.typography.labelMedium,
                            color = PremiumGoldDim,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 1.4.sp,
                        )
                        Text(
                            text = "Version ${BuildConfig.VERSION_NAME}",
                            style = MaterialTheme.typography.headlineSmall,
                            color = Color.White,
                            fontWeight = FontWeight.Bold,
                        )
                    }
                    Text(
                        text = if (meta.libraryScope == "all") "PREVIEW" else "STABLE · USA",
                        style = MaterialTheme.typography.labelMedium,
                        color = if (meta.libraryScope == "all") PremiumGold else MutedText,
                        fontWeight = FontWeight.Bold,
                        letterSpacing = 1.2.sp,
                    )
                }
                Spacer(modifier = Modifier.height(10.dp))
                Row(modifier = Modifier.fillMaxWidth()) {
                    CompactStat("Channels", library.channels.size.toString(), Modifier.weight(1f))
                    CompactStat("Categories", library.groups.size.toString(), Modifier.weight(1f))
                    CompactStat("Guide", guideLine, Modifier.weight(1.4f))
                }
                Spacer(modifier = Modifier.height(6.dp))
                Text(
                    text = "Library built ${meta.generatedUtc.ifBlank { "unknown" }}",
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                )
            }
        }

        Spacer(modifier = Modifier.height(14.dp))

        // ------------------------------------------------------- actions
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .horizontalScroll(rememberScrollState()),
            horizontalArrangement = Arrangement.spacedBy(10.dp),
        ) {
            FocusButton(
                if (busy) "Refreshing…" else "Force refresh",
                enabled = !busy,
            ) { onForceRefresh() }
            FocusButton(
                if (updateInfo.checking) "Checking…" else "Check for update",
                enabled = !updateInfo.busy,
            ) { onCheckForUpdate() }
            FocusButton(
                if (diagnosticsRunning) "Checking for bugs…" else "Check for bugs",
                enabled = !diagnosticsRunning,
            ) { onCheckForBugs() }
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

        // One status line, not a paragraph: whichever action ran last wins.
        val statusLine = when {
            refreshInfo.inProgress -> status.ifBlank { "Refreshing all data…" }
            library.guideLoading -> "Channels ready · loading the guide…"
            updateInfo.error != null -> updateInfo.error
            diagnosticsRunning -> "Checking the library for bugs…"
            diagnostics != null -> diagnostics.headline
            status.isNotBlank() -> status
            else -> updateInfo.message
        }
        Spacer(modifier = Modifier.height(10.dp))
        Text(
            text = statusLine,
            style = MaterialTheme.typography.bodySmall,
            color = when {
                updateInfo.error != null -> Color(0xFFFF8A80)
                refreshInfo.inProgress || diagnosticsRunning -> PremiumGold
                else -> MutedText
            },
            maxLines = 2,
            overflow = TextOverflow.Ellipsis,
        )

        // --------------------------------------------------- bug check card
        if (diagnostics != null) {
            Spacer(modifier = Modifier.height(12.dp))
            DiagnosticsCard(diagnostics)
        }

        Spacer(modifier = Modifier.height(14.dp))

        // ------------------------------------------------------ quick facts
        Surface(
            modifier = Modifier.fillMaxWidth(),
            shape = RoundedCornerShape(14.dp),
            color = CardBackground,
            border = BorderStroke(1.dp, PanelStroke),
        ) {
            Column(modifier = Modifier.padding(horizontal = 18.dp, vertical = 10.dp)) {
                CompactRow("Newest stable release", updateInfo.latestStableVersion ?: "Not checked yet")
                CompactRow(
                    "Last update check",
                    if (updateInfo.lastCheckedAtMillis > 0L) {
                        formatRefreshInstant(updateInfo.lastCheckedAtMillis)
                    } else {
                        "Not yet"
                    },
                )
                CompactRow(
                    "Last successful refresh",
                    if (refreshInfo.lastSuccessAtMillis > 0L) {
                        formatRefreshInstant(refreshInfo.lastSuccessAtMillis)
                    } else {
                        "Not yet"
                    },
                )
                CompactRow(
                    "Next background check",
                    if (refreshInfo.nextAutomaticAtMillis > 0L) {
                        formatRefreshInstant(refreshInfo.nextAutomaticAtMillis)
                    } else {
                        "Being scheduled"
                    },
                )
                CompactRow(
                    "Showing",
                    if (library.refreshed) "Latest copy downloaded by the app" else "Data bundled in this APK",
                )
            }
        }

        Spacer(modifier = Modifier.height(10.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
            FocusButton(if (showDetails) "Hide details" else "Show details", enabled = true) {
                showDetails = !showDetails
            }
            FocusButton("Reset to bundled data", enabled = !busy) { onReset() }
        }

        if (showDetails) {
            Spacer(modifier = Modifier.height(12.dp))
            Surface(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(14.dp),
                color = Color(0xFF0E141B),
                border = BorderStroke(1.dp, PanelStroke),
            ) {
                Column(modifier = Modifier.padding(horizontal = 18.dp, vertical = 10.dp)) {
                    CompactRow("Source playlist", meta.playlist.ifBlank { "unknown" })
                    CompactRow("Source guide", meta.guide.ifBlank { "unknown" })
                    CompactRow("Playlist URL", meta.playlistUrl.ifBlank { "(not bundled)" })
                    CompactRow("Guide URL", meta.guideUrl.ifBlank { "(not bundled)" })
                    if (meta.windowStart > 0L) {
                        CompactRow("Guide window", "${formatDay(meta.windowStart)} – ${formatDay(meta.windowEnd)}")
                    }
                    if (meta.previewFeatures.isNotEmpty()) {
                        CompactRow("Preview features", meta.previewFeatures.sorted().joinToString())
                    }
                    CompactRow("Last refresh result", refreshInfo.lastMessage)
                }
            }
        }

        Spacer(modifier = Modifier.height(16.dp))
        Text(
            text = "Force refresh downloads the playlist and guide again. Checks and " +
                "downloads use GitHub only; the bug check stays on this device. " +
                "PremiumTV ${BuildConfig.VERSION_NAME} — publicly listed streams only.",
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
        )
    }
}

@Composable
private fun CompactStat(label: String, value: String, modifier: Modifier = Modifier) {
    Column(modifier = modifier.padding(end = 8.dp)) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodyMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
        )
    }
}

@Composable
private fun CompactRow(label: String, value: String) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        verticalAlignment = Alignment.Top,
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = MutedText,
            modifier = Modifier.width(190.dp),
        )
        Text(
            text = value,
            style = MaterialTheme.typography.bodySmall,
            color = Color.White,
            modifier = Modifier.weight(1f),
        )
    }
}

@Composable
private fun DiagnosticsCard(report: DiagnosticsReport) {
    val accent = when {
        report.problemCount > 0 -> Color(0xFFFF8A80)
        report.warningCount > 0 -> PremiumGold
        else -> Color(0xFF7EDCA2)
    }
    Surface(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(14.dp),
        color = CardBackground,
        border = BorderStroke(1.dp, accent.copy(alpha = 0.55f)),
    ) {
        Column(modifier = Modifier.padding(horizontal = 18.dp, vertical = 12.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Text(
                    text = report.headline,
                    style = MaterialTheme.typography.titleSmall,
                    color = accent,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.weight(1f),
                )
                Text(
                    text = "${report.okCount} ok · ${report.warningCount} warn · ${report.problemCount} fail",
                    style = MaterialTheme.typography.labelSmall,
                    color = MutedText,
                )
            }
            Spacer(modifier = Modifier.height(6.dp))
            for (check in report.checks) {
                val color = when (check.status) {
                    DiagnosticStatus.Ok -> Color(0xFF7EDCA2)
                    DiagnosticStatus.Warning -> PremiumGold
                    DiagnosticStatus.Problem -> Color(0xFFFF8A80)
                }
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(vertical = 3.dp),
                    verticalAlignment = Alignment.Top,
                ) {
                    Text(
                        text = when (check.status) {
                            DiagnosticStatus.Ok -> "OK"
                            DiagnosticStatus.Warning -> "WARN"
                            DiagnosticStatus.Problem -> "FAIL"
                        },
                        style = MaterialTheme.typography.labelSmall,
                        color = color,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.width(52.dp),
                    )
                    Text(
                        text = check.label,
                        style = MaterialTheme.typography.bodySmall,
                        color = Color.White,
                        fontWeight = FontWeight.SemiBold,
                        modifier = Modifier.width(150.dp),
                    )
                    Text(
                        text = check.detail,
                        style = MaterialTheme.typography.bodySmall,
                        color = MutedText,
                        modifier = Modifier.weight(1f),
                    )
                }
            }
        }
    }
}
