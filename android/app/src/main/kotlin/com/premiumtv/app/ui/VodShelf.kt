package com.premiumtv.app.ui

import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.aspectRatio
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.premiumtv.app.data.Channel
import org.json.JSONObject

/**
 * Movies & Shows — the on-demand test shelf (1.1.2).
 *
 * The 1.1.1 tab was a coming-soon page. This is the working feasibility test
 * behind it: `scripts/vod_catalog.py` resolves a curated set of public-domain
 * films and classic TV episodes from the Internet Archive, verifies each
 * direct stream, and publishes one catalogue document that
 * `android/tools/build_bundle.py` ships as `bundle/vod-catalog.json`.
 *
 * An entry is played exactly like a channel — [VodItem.asChannel] turns it into
 * the same Channel the side player already understands — so the docked panel,
 * the expand-to-full-screen gesture, Recently watched and the dead-feed memory
 * all work without a second player or a parallel path.
 */
data class VodItem(
    val id: String,
    val title: String,
    val kind: String,
    val show: String,
    val season: Int,
    val episode: Int,
    val year: Int,
    val genre: String,
    val runtimeSeconds: Int,
    val summary: String,
    val stream: String,
    val poster: String,
    val license: String,
) {
    val isMovie: Boolean get() = kind == "movie"

    /** "Movie" or "S1 E5" — what the card says above the title. */
    val label: String
        get() = when {
            isMovie -> "FILM"
            season > 0 && episode > 0 -> "S${season} E${episode}"
            season > 0 -> "S$season"
            else -> "EPISODE"
        }

    /** "1968 · Horror · 97 min", dropping whatever the item does not have. */
    val detail: String
        get() = listOfNotNull(
            year.takeIf { it > 0 }?.toString(),
            genre.takeIf { it.isNotBlank() },
            runtimeSeconds.takeIf { it > 0 }?.let { "${it / 60} min" },
        ).joinToString(" · ")

    /** The player's input: one finite stream, one server, no guide listings. */
    fun asChannel(): Channel = Channel(
        id = id,
        name = if (isMovie) title else "$show · $label",
        logo = poster,
        group = if (isMovie) "Movies" else "TV Shows",
        country = "US",
        chno = "",
        url = stream,
        userAgent = "",
        referrer = "",
        origin = "",
    )
}

/** Parses the bundled catalogue; unusable entries are dropped, never faked. */
internal fun parseVodCatalog(text: String?): List<VodItem> {
    if (text.isNullOrBlank()) return emptyList()
    return try {
        val root = JSONObject(text)
        val array = root.optJSONArray("items") ?: return emptyList()
        buildList {
            for (index in 0 until array.length()) {
                val item = array.optJSONObject(index) ?: continue
                val stream = item.optString("stream")
                val title = item.optString("title")
                val id = item.optString("id")
                if (stream.isBlank() || title.isBlank() || id.isBlank()) continue
                add(
                    VodItem(
                        id = id,
                        title = title,
                        kind = item.optString("kind", "movie"),
                        show = item.optString("show"),
                        season = item.optInt("season"),
                        episode = item.optInt("episode"),
                        year = item.optInt("year"),
                        genre = item.optString("genre"),
                        runtimeSeconds = item.optInt("runtime_seconds"),
                        summary = item.optString("summary"),
                        stream = stream,
                        poster = item.optString("poster"),
                        license = item.optString("license"),
                    )
                )
            }
        }
    } catch (_: Exception) {
        emptyList()
    }
}

private enum class VodFilter(val label: String) {
    All("All"),
    Movies("Movies"),
    Shows("TV Shows"),
}

/**
 * The tab itself: a count line, three filter chips and a poster grid.
 * Selecting a card hands the item to the same player a channel uses.
 */
@Composable
fun VodShelfScreen(
    items: List<VodItem>,
    loading: Boolean = false,
    onWatch: (VodItem) -> Unit,
    onBrowseChannels: () -> Unit,
) {
    var filter by rememberSaveable { mutableStateOf(VodFilter.All.name) }
    val active = VodFilter.values().firstOrNull { it.name == filter } ?: VodFilter.All
    val shown = remember(items, active) {
        when (active) {
            VodFilter.All -> items
            VodFilter.Movies -> items.filter { it.isMovie }
            VodFilter.Shows -> items.filter { !it.isMovie }
        }
    }

    if (loading && items.isEmpty()) {
        CenteredMessage("Loading the on-demand shelf…")
        return
    }
    if (items.isEmpty()) {
        EmptyVodShelf(onBrowseChannels)
        return
    }

    Column(modifier = Modifier.fillMaxSize()) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = 28.dp, end = 28.dp, bottom = 6.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "${items.size} on demand",
                style = MaterialTheme.typography.labelMedium,
                color = PremiumGold,
                fontWeight = FontWeight.Bold,
            )
            Spacer(modifier = Modifier.width(10.dp))
            Text(
                text = "Public-domain films and classic TV · plays in the side player",
                style = MaterialTheme.typography.labelSmall,
                color = MutedText,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f),
            )
            VodFilter.values().forEach { option ->
                Spacer(modifier = Modifier.width(8.dp))
                VodChip(option.label, option == active) { filter = option.name }
            }
        }

        LazyVerticalGrid(
            columns = GridCells.Adaptive(186.dp),
            modifier = Modifier.fillMaxSize(),
            contentPadding = PaddingValues(start = 28.dp, end = 28.dp, top = 6.dp, bottom = 48.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
            verticalArrangement = Arrangement.spacedBy(18.dp),
        ) {
            items(items = shown, key = { it.id }) { item ->
                VodCard(item = item, onWatch = { onWatch(item) })
            }
        }
    }
}

/** One poster card: art, kind label, title, facts and the first line of the plot. */
@Composable
private fun VodCard(item: VodItem, onWatch: () -> Unit) {
    var focused by remember { mutableStateOf(false) }
    Surface(
        modifier = Modifier
            .fillMaxWidth()
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onWatch)
            .focusOutline(focused, RoundedCornerShape(14.dp)),
        shape = RoundedCornerShape(14.dp),
        color = if (focused) CardBackgroundFocused else CardBackground,
        border = BorderStroke(1.dp, if (focused) FocusRing else PanelStroke),
    ) {
        Column {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .aspectRatio(2f / 3f)
                    .background(Color(0xFF0B1017)),
                contentAlignment = Alignment.Center,
            ) {
                AsyncImage(
                    model = item.poster,
                    contentDescription = null,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize(),
                )
                Text(
                    text = if (item.isMovie) "▶" else "▶ EP",
                    style = MaterialTheme.typography.titleMedium,
                    color = PremiumGold,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .align(Alignment.Center)
                        .background(Color(0x99000000), RoundedCornerShape(999.dp))
                        .padding(horizontal = 12.dp, vertical = 6.dp),
                )
                Text(
                    text = item.label,
                    style = MaterialTheme.typography.labelSmall,
                    color = Color(0xFF12160B),
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier
                        .align(Alignment.TopStart)
                        .padding(8.dp)
                        .background(FocusRing, RoundedCornerShape(999.dp))
                        .padding(horizontal = 8.dp, vertical = 2.dp),
                )
            }
            Column(modifier = Modifier.padding(horizontal = 12.dp, vertical = 10.dp)) {
                Text(
                    text = item.title,
                    style = MaterialTheme.typography.titleSmall,
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
                if (item.detail.isNotBlank()) {
                    Spacer(modifier = Modifier.height(3.dp))
                    Text(
                        text = item.detail,
                        style = MaterialTheme.typography.labelSmall,
                        color = PremiumGold,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
                if (item.summary.isNotBlank()) {
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = item.summary,
                        style = MaterialTheme.typography.bodySmall,
                        color = MutedText,
                        maxLines = 3,
                        overflow = TextOverflow.Ellipsis,
                    )
                }
            }
        }
    }
}

@Composable
private fun VodChip(label: String, selected: Boolean, onClick: () -> Unit) {
    var focused by remember { mutableStateOf(false) }
    Surface(
        modifier = Modifier
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onClick)
            .focusOutline(focused, RoundedCornerShape(999.dp)),
        shape = RoundedCornerShape(999.dp),
        color = when {
            focused -> FocusRing
            selected -> PremiumGold
            else -> CardBackground
        },
        border = BorderStroke(1.dp, if (selected) PremiumGold else PanelStroke),
    ) {
        Text(
            text = label,
            style = MaterialTheme.typography.labelMedium,
            color = if (selected || focused) Color(0xFF12160B) else Color.White,
            fontWeight = FontWeight.Bold,
            modifier = Modifier.padding(horizontal = 14.dp, vertical = 7.dp),
        )
    }
}

/** Shown when the catalogue is absent — the tab still tells the truth. */
@Composable
private fun EmptyVodShelf(onBrowseChannels: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(28.dp),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Text(
            text = "ON-DEMAND TEST",
            style = MaterialTheme.typography.labelMedium,
            color = PremiumGoldDim,
            fontWeight = FontWeight.Bold,
            letterSpacing = 1.6.sp,
        )
        Spacer(modifier = Modifier.height(12.dp))
        Text(
            text = "No on-demand catalogue in this build.",
            style = MaterialTheme.typography.titleMedium,
            color = Color.White,
            fontWeight = FontWeight.SemiBold,
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = "The test shelf ships with the app bundle. Run " +
                "scripts/vod_catalog.py and rebuild the bundle to load it.",
            style = MaterialTheme.typography.bodyMedium,
            color = MutedText,
        )
        Spacer(modifier = Modifier.height(18.dp))
        FocusButton("Browse live TV") { onBrowseChannels() }
    }
}
