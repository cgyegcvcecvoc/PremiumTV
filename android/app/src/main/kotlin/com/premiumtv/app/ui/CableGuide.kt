package com.premiumtv.app.ui

import androidx.compose.foundation.background
import androidx.compose.foundation.border
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
import androidx.compose.foundation.layout.offset
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.zIndex
import coil.compose.AsyncImage
import androidx.compose.ui.layout.ContentScale
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.Library
import com.premiumtv.app.data.Programme

private const val CABLE_WINDOW_SECONDS = 8L * 60L * 60L
private const val CABLE_SLOT_SECONDS = 30L * 60L
private const val CABLE_SLOT_DP = 90
private const val CABLE_ROW_HEIGHT_DP = 76
private val CABLE_LABEL_WIDTH = 230.dp
private val CABLE_SLOT_WIDTH = CABLE_SLOT_DP.dp
private val CABLE_TIMELINE_WIDTH = (CABLE_WINDOW_SECONDS / CABLE_SLOT_SECONDS).toInt() * CABLE_SLOT_DP

private data class CableRow(
    val channel: Channel,
    val programmes: List<Programme>,
)

/**
 * Optional 1.1.0 preview: a traditional channel-by-time grid, enabled only by
 * bundle metadata so stable 1.0.2 builds do not show a preview-only surface.
 */
@Composable
fun CableGuideScreen(library: Library, now: Long, onSelect: (Channel) -> Unit) {
    val windowStart = remember(now) { (now / CABLE_SLOT_SECONDS) * CABLE_SLOT_SECONDS }
    val windowEnd = windowStart + CABLE_WINDOW_SECONDS
    val horizontalState = rememberScrollState()
    val rows = remember(library.channels, library.programmes, windowStart) {
        library.channels.mapNotNull { channel ->
            val visible = library.programmes[channel.id].orEmpty().filter {
                it.end > windowStart && it.start < windowEnd
            }
            if (visible.isEmpty()) null else CableRow(channel, visible)
        }.sortedWith(
            compareBy<CableRow> { it.channel.chno.toIntOrNull() ?: Int.MAX_VALUE }
                .thenBy { it.channel.chno }
                .thenBy { it.channel.name.lowercase() },
        )
    }

    Column(
        modifier = Modifier.fillMaxSize().padding(top = 8.dp),
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = SCREEN_GUTTER, vertical = 8.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(
                    text = "Cable guide",
                    style = MaterialTheme.typography.titleLarge,
                    color = Color.White,
                    fontWeight = FontWeight.Bold,
                )
                Text(
                    text = "${rows.size} channels with listings · 8-hour preview",
                    style = MaterialTheme.typography.bodySmall,
                    color = MutedText,
                )
            }
            Text(
                text = "${formatDay(windowStart)} · ${formatClock(windowStart)} – ${formatClock(windowEnd)}",
                style = MaterialTheme.typography.labelMedium,
                color = PremiumGold,
            )
        }

        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(start = SCREEN_GUTTER, end = SCREEN_GUTTER, top = 4.dp, bottom = 4.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = "CHANNEL",
                modifier = Modifier.width(CABLE_LABEL_WIDTH).padding(start = 12.dp),
                style = MaterialTheme.typography.labelSmall,
                color = MutedText,
                fontWeight = FontWeight.Bold,
            )
            Box(
                modifier = Modifier
                    .weight(1f)
                    .horizontalScroll(horizontalState),
            ) {
                Row(modifier = Modifier.width(CABLE_TIMELINE_WIDTH.dp)) {
                    repeat(CABLE_TIMELINE_WIDTH / CABLE_SLOT_DP) { slot ->
                        val tick = windowStart + slot * CABLE_SLOT_SECONDS
                        Box(
                            modifier = Modifier
                                .width(CABLE_SLOT_WIDTH)
                                .height(34.dp)
                                .padding(start = 8.dp),
                            contentAlignment = Alignment.CenterStart,
                        ) {
                            Text(
                                text = formatClock(tick),
                                style = MaterialTheme.typography.labelSmall,
                                color = if (slot % 2 == 0) Color.White else MutedText,
                                maxLines = 1,
                            )
                        }
                    }
                }
            }
        }

        if (library.guideLoading) {
            CableEmpty("The guide is still loading. Channels remain available in the Channels tab.")
        } else if (library.guideError != null) {
            CableEmpty("${library.guideError}\n\nThe channel list is still available in the Channels tab.")
        } else if (rows.isEmpty()) {
            CableEmpty("No programme listings cover this time window.")
        } else {
            LazyColumn(
                modifier = Modifier.fillMaxSize(),
                contentPadding = PaddingValues(start = SCREEN_GUTTER, end = SCREEN_GUTTER, bottom = 42.dp),
                verticalArrangement = Arrangement.spacedBy(2.dp),
            ) {
                items(
                    items = rows,
                    key = { row -> "${row.channel.id}|${row.channel.url}" },
                ) { row ->
                    CableGuideRow(
                        row = row,
                        now = now,
                        windowStart = windowStart,
                        windowEnd = windowEnd,
                        horizontalScroll = horizontalState,
                        onSelect = { onSelect(row.channel) },
                    )
                }
            }
        }
    }
}

@Composable
private fun CableGuideRow(
    row: CableRow,
    now: Long,
    windowStart: Long,
    windowEnd: Long,
    horizontalScroll: androidx.compose.foundation.ScrollState,
    onSelect: () -> Unit,
) {
    Row(
        modifier = Modifier.fillMaxWidth().height(CABLE_ROW_HEIGHT_DP.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Row(
            modifier = Modifier
                .width(CABLE_LABEL_WIDTH)
                .fillMaxHeight()
                .clip(RoundedCornerShape(topStart = 8.dp, bottomStart = 8.dp))
                .background(CardBackground)
                .padding(horizontal = 10.dp),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = row.channel.chno.ifBlank { "–" },
                modifier = Modifier.width(38.dp),
                style = MaterialTheme.typography.labelMedium,
                color = PremiumGold,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
            )
            if (row.channel.logo.isNotBlank()) {
                AsyncImage(
                    model = row.channel.logo,
                    contentDescription = null,
                    contentScale = ContentScale.Fit,
                    modifier = Modifier.width(42.dp).height(36.dp),
                )
            } else {
                Box(
                    modifier = Modifier
                        .width(42.dp)
                        .height(36.dp)
                        .background(Color(0xFF202A36), RoundedCornerShape(5.dp)),
                    contentAlignment = Alignment.Center,
                ) {
                    Text(
                        text = initialsOf(row.channel.name),
                        style = MaterialTheme.typography.labelMedium,
                        color = PremiumGold,
                        fontWeight = FontWeight.Bold,
                    )
                }
            }
            Spacer(modifier = Modifier.width(9.dp))
            Text(
                text = row.channel.name,
                style = MaterialTheme.typography.labelMedium,
                color = Color.White,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                modifier = Modifier.weight(1f),
            )
        }

        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .horizontalScroll(horizontalScroll)
                .background(Color(0xFF0C1118)),
        ) {
            Box(
                modifier = Modifier
                    .width(CABLE_TIMELINE_WIDTH.dp)
                    .fillMaxHeight(),
            ) {
                repeat(CABLE_TIMELINE_WIDTH / CABLE_SLOT_DP) { slot ->
                    Box(
                        modifier = Modifier
                            .offset(x = (slot * CABLE_SLOT_DP).dp)
                            .width(1.dp)
                            .fillMaxHeight()
                            .background(Color(0x223F4B5A)),
                    )
                }
                row.programmes.forEach { programme ->
                    CableProgrammeCell(
                        programme = programme,
                        now = now,
                        windowStart = windowStart,
                        windowEnd = windowEnd,
                        onSelect = onSelect,
                    )
                }
                if (now >= windowStart && now < windowEnd) {
                    val nowOffset = ((now - windowStart) / 60f * (CABLE_SLOT_DP / 30f)).dp
                    Box(
                        modifier = Modifier
                            .offset(x = nowOffset)
                            .width(2.dp)
                            .fillMaxHeight()
                            .background(LiveRed)
                            .zIndex(2f),
                    )
                }
            }
        }
    }
}

@Composable
private fun CableProgrammeCell(
    programme: Programme,
    now: Long,
    windowStart: Long,
    windowEnd: Long,
    onSelect: () -> Unit,
) {
    val visibleStart = maxOf(programme.start, windowStart)
    val visibleEnd = minOf(programme.end, windowEnd)
    if (visibleEnd <= visibleStart) return

    val pixelsPerMinute = CABLE_SLOT_DP / 30f
    val x = ((visibleStart - windowStart) / 60f * pixelsPerMinute).dp
    val width = ((visibleEnd - visibleStart) / 60f * pixelsPerMinute).dp
    val current = now >= programme.start && now < programme.end
    var focused by remember(programme) { mutableStateOf(false) }
    val shape = RoundedCornerShape(6.dp)

    Box(
        modifier = Modifier
            .offset(x = x)
            .width(width)
            .fillMaxHeight()
            .padding(2.dp)
            .clip(shape)
            .background(
                when {
                    focused -> Color(0xFF343D47)
                    current -> Color(0xFF27313B)
                    else -> Color(0xFF18212B)
                },
            )
            .border(
                width = if (focused) 2.dp else if (current) 1.5.dp else 1.dp,
                color = if (focused || current) PremiumGold else Color(0x443F4B5A),
                shape = shape,
            )
            .onFocusChanged { focused = it.isFocused }
            .tvClickable(onSelect),
    ) {
        Column(modifier = Modifier.fillMaxSize().padding(horizontal = 8.dp, vertical = 5.dp)) {
            Text(
                text = "${formatClock(visibleStart)}${if (current) " · NOW" else ""}",
                style = MaterialTheme.typography.labelSmall,
                color = if (current) PremiumGold else MutedText,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
                overflow = TextOverflow.Clip,
            )
            Text(
                text = programme.title,
                style = MaterialTheme.typography.bodySmall,
                color = Color.White,
                fontWeight = if (current) FontWeight.SemiBold else FontWeight.Normal,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}

@Composable
private fun CableEmpty(message: String) {
    Box(
        modifier = Modifier.fillMaxSize().padding(horizontal = SCREEN_GUTTER, vertical = 28.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text = message,
            style = MaterialTheme.typography.bodyMedium,
            color = MutedText,
        )
    }
}
