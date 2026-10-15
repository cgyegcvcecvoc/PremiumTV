package com.premiumtv.app.ui

import android.view.KeyEvent as NativeKey
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.focusable
import androidx.compose.foundation.gestures.Orientation
import androidx.compose.foundation.gestures.detectTapGestures
import androidx.compose.foundation.gestures.rememberScrollableState
import androidx.compose.foundation.gestures.scrollBy
import androidx.compose.foundation.gestures.scrollable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.BoxWithConstraints
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
import androidx.compose.foundation.layout.wrapContentWidth
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.Stable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableFloatStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.rememberUpdatedState
import androidx.compose.runtime.setValue
import androidx.compose.runtime.withFrameNanos
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.focus.FocusRequester
import androidx.compose.ui.focus.focusRequester
import androidx.compose.ui.focus.onFocusChanged
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.input.key.KeyEvent
import androidx.compose.ui.input.key.onKeyEvent
import androidx.compose.ui.input.pointer.pointerInput
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.layout.layout
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.IntOffset
import androidx.compose.ui.unit.coerceIn
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.Library
import com.premiumtv.app.data.Programme
import kotlin.math.roundToInt
import kotlinx.coroutines.launch

// Sized so a 1080p TV (960x540 dp) shows five channel rows under the detail
// strip and the time header.
private val ROW_HEIGHT = 58.dp
private val SECTION_HEIGHT = 26.dp
private val HEADER_HEIGHT = 32.dp
private val INFO_HEIGHT = 70.dp
private val MIN_VISIBLE_TITLE = 44.dp

private val GridBackground = Color(0xFF0C1118)
private val HeaderBackground = Color(0xFF161D27)
private val GridLine = Color(0x223F4B5A)
private val CellIdle = Color(0xFF18212B)
private val CellLive = Color(0xFF2A3326)
private val CellHighlight = Color(0xFF3A4757)
private val CellStroke = Color(0x443F4B5A)

/**
 * Where the guide is: the highlighted cell, the horizontal time offset and the
 * channel list position. AppRoot remembers it, so closing the player returns
 * to the same spot in the grid - as a cable box does.
 */
@Stable
class CableGuideState internal constructor() {
    internal val list = LazyListState()
    internal var scrollX by mutableFloatStateOf(0f)
    internal var cursor by mutableStateOf<GuideCursor?>(null)
}

@Composable
fun rememberCableGuideState(): CableGuideState = remember { CableGuideState() }

/**
 * The cable-style guide: channels down the left, what each one is playing to
 * the right, half-hour times across the top, a red NOW line, and a strip above
 * the grid describing the highlighted show.
 *
 * On a TV remote the grid is one focus stop with a highlight that moves the
 * way a cable box guide does (see [moveGuideCursor]); OK plays the highlighted
 * channel and up from the first row returns to the tabs. On a touch screen
 * the grid drags in both directions and a tap on a show plays its channel.
 */
@Composable
internal fun CableGuideScreen(
    library: Library,
    now: Long,
    state: CableGuideState,
    onSelect: (Channel) -> Unit,
) {
    if (library.guideLoading) {
        GuideMessage("Channels are ready.\nThe guide is still loading…")
        return
    }
    if (library.guideError != null) {
        GuideMessage("${library.guideError}\n\nEvery channel still plays from the Channels tab.")
        return
    }

    val windowStart = guideWindowStart(now)
    val model = remember(library.channels, library.groups, library.programmes, windowStart) {
        buildGuideModel(library.channels, library.groups, library.programmes, windowStart)
    }
    if (model.rows.isEmpty()) {
        GuideMessage(
            "No programme listings cover the next eight hours.\n" +
                "Every channel still plays from the Channels tab."
        )
        return
    }

    val focusRequester = remember { FocusRequester() }
    var gridFocused by remember { mutableStateOf(false) }
    val scope = rememberCoroutineScope()
    val density = LocalDensity.current
    val currentModel by rememberUpdatedState(model)
    val currentNow by rememberUpdatedState(now)
    val currentOnSelect by rememberUpdatedState(onSelect)

    fun cursorNow(): GuideCursor {
        val saved = state.cursor
        val open = currentModel.windowStart
        val fallback = GuideCursor(row = 0, time = currentNow.coerceIn(open, currentModel.windowEnd - 1))
        val cursor = saved ?: fallback
        return cursor.copy(row = cursor.row.coerceIn(0, currentModel.rows.lastIndex))
    }
    val cursor = cursorNow()

    BoxWithConstraints(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = SCREEN_GUTTER),
    ) {
        // About two hours across, like a cable box, with the channel column
        // taking a quarter of the width.
        val labelWidth = (maxWidth * 0.26f).coerceIn(168.dp, 260.dp)
        val viewportWidth = maxWidth - labelWidth
        val slotWidth = (viewportWidth / 4).coerceIn(96.dp, 220.dp)
        val timelineWidth = slotWidth * GUIDE_SLOTS.toFloat()
        val slotPx = with(density) { slotWidth.toPx() }
        val viewportPx = with(density) { viewportWidth.toPx() }
        val maxScroll = (with(density) { timelineWidth.toPx() } - viewportPx).coerceAtLeast(0f)
        val rowPx = with(density) { ROW_HEIGHT.toPx() }
        val pxPerSecond = slotPx / GUIDE_SLOT_SECONDS.toFloat()
        val scrollX = { state.scrollX.coerceIn(0f, maxScroll) }

        val horizontalDrag = rememberScrollableState { delta ->
            val old = state.scrollX.coerceIn(0f, maxScroll)
            val next = (old + delta).coerceIn(0f, maxScroll)
            state.scrollX = next
            next - old
        }

        /** Scrolls so the highlighted row and show are fully on screen. */
        fun reveal(target: GuideCursor) {
            val model = currentModel
            scope.launch {
                val list = state.list
                val itemIndex = model.itemIndexOfRow[target.row]
                val layout = list.layoutInfo
                val visible = layout.visibleItemsInfo.firstOrNull { it.index == itemIndex }
                val top = layout.viewportStartOffset
                val bottom = layout.viewportEndOffset - layout.afterContentPadding
                if (visible == null) {
                    val first = layout.visibleItemsInfo.firstOrNull()?.index ?: 0
                    if (itemIndex < first) {
                        // Show the category heading too when the row opens a category.
                        val heading = itemIndex > 0 && model.items[itemIndex - 1] is GuideItem.Section
                        list.scrollToItem(if (heading) itemIndex - 1 else itemIndex)
                    } else {
                        list.scrollToItem(itemIndex)
                        list.scrollBy(-((bottom - top) - rowPx).coerceAtLeast(0f))
                    }
                } else if (visible.offset < top) {
                    list.scrollBy((visible.offset - top).toFloat())
                } else if (visible.offset + visible.size > bottom) {
                    list.scrollBy((visible.offset + visible.size - bottom).toFloat())
                }

                if (!target.onChannel) {
                    val programmes = model.rows[target.row].programmes
                    val index = programmeIndexAt(programmes, target.time)
                    if (index >= 0) {
                        val programme = programmes[index]
                        val x0 = (maxOf(programme.start, model.windowStart) - model.windowStart) * pxPerSecond
                        val x1 = (minOf(programme.end, model.windowEnd) - model.windowStart) * pxPerSecond
                        val pad = slotPx * 0.25f
                        val current = state.scrollX.coerceIn(0f, maxScroll)
                        val next = when {
                            x0 < current -> x0 - pad
                            x1 > current + viewportPx ->
                                if (x1 - x0 > viewportPx - pad) x0 - pad else x1 - viewportPx + pad
                            else -> current
                        }
                        state.scrollX = next.coerceIn(0f, maxScroll)
                    }
                }
            }
        }

        fun onKey(event: KeyEvent): Boolean {
            val native = event.nativeKeyEvent
            val down = native.action == NativeKey.ACTION_DOWN
            val model = currentModel
            return when (native.keyCode) {
                NativeKey.KEYCODE_DPAD_CENTER, NativeKey.KEYCODE_ENTER, NativeKey.KEYCODE_NUMPAD_ENTER -> {
                    if (native.action == NativeKey.ACTION_UP) {
                        currentOnSelect(model.rows[cursorNow().row].channel)
                    }
                    true
                }
                NativeKey.KEYCODE_DPAD_UP, NativeKey.KEYCODE_DPAD_DOWN,
                NativeKey.KEYCODE_DPAD_LEFT, NativeKey.KEYCODE_DPAD_RIGHT -> {
                    if (!down) {
                        true
                    } else {
                        val move = when (native.keyCode) {
                            NativeKey.KEYCODE_DPAD_UP -> GuideMove.Up
                            NativeKey.KEYCODE_DPAD_DOWN -> GuideMove.Down
                            NativeKey.KEYCODE_DPAD_LEFT -> GuideMove.Left
                            else -> GuideMove.Right
                        }
                        val next = moveGuideCursor(model, cursorNow(), move)
                        if (next == null) {
                            false
                        } else {
                            state.cursor = next
                            reveal(next)
                            true
                        }
                    }
                }
                NativeKey.KEYCODE_PAGE_DOWN, NativeKey.KEYCODE_CHANNEL_DOWN,
                NativeKey.KEYCODE_PAGE_UP, NativeKey.KEYCODE_CHANNEL_UP -> {
                    if (down) {
                        val page = (state.list.layoutInfo.visibleItemsInfo.size - 1).coerceAtLeast(1)
                        val forward = native.keyCode == NativeKey.KEYCODE_PAGE_DOWN ||
                            native.keyCode == NativeKey.KEYCODE_CHANNEL_DOWN
                        val next = pageGuideCursor(model, cursorNow(), if (forward) page else -page)
                        state.cursor = next
                        reveal(next)
                    }
                    true
                }
                else -> false
            }
        }

        Column(modifier = Modifier.fillMaxSize()) {
            GuideInfoPanel(model = model, cursor = cursor, focused = gridFocused, now = now)
            Spacer(modifier = Modifier.height(6.dp))
            GuideTimeHeader(
                windowStart = model.windowStart,
                windowEnd = model.windowEnd,
                now = now,
                labelWidth = labelWidth,
                slotWidth = slotWidth,
                timelineWidth = timelineWidth,
                scrollX = scrollX,
            )
            LazyColumn(
                state = state.list,
                modifier = Modifier
                    .fillMaxSize()
                    .focusRequester(focusRequester)
                    .onFocusChanged { gridFocused = it.isFocused }
                    .focusable()
                    .onKeyEvent { onKey(it) }
                    .scrollable(
                        state = horizontalDrag,
                        orientation = Orientation.Horizontal,
                        reverseDirection = true,
                    ),
                contentPadding = PaddingValues(bottom = 24.dp),
            ) {
                items(
                    count = model.items.size,
                    key = { index ->
                        when (val item = model.items[index]) {
                            is GuideItem.Section -> "section|$index|${item.name}"
                            is GuideItem.Row -> "row|${item.row.channel.id}|${item.row.channel.url}"
                        }
                    },
                    contentType = { index -> if (model.items[index] is GuideItem.Section) 0 else 1 },
                ) { index ->
                    when (val item = model.items[index]) {
                        is GuideItem.Section -> GuideSectionHeading(item, labelWidth)
                        is GuideItem.Row -> {
                            val highlightedRow = gridFocused && cursor.row == item.index
                            GuideChannelRow(
                                row = item.row,
                                windowStart = model.windowStart,
                                windowEnd = model.windowEnd,
                                now = now,
                                labelWidth = labelWidth,
                                slotWidth = slotWidth,
                                timelineWidth = timelineWidth,
                                scrollX = scrollX,
                                channelHighlighted = highlightedRow && cursor.onChannel,
                                highlightedProgramme = if (highlightedRow && !cursor.onChannel) {
                                    programmeIndexAt(item.row.programmes, cursor.time)
                                } else {
                                    -1
                                },
                                onSelect = { currentOnSelect(item.row.channel) },
                            )
                        }
                    }
                }
            }
        }
    }

    // Opening the guide puts the remote's highlight in the grid, on the first
    // channel's current show - or back where it was before a channel played.
    LaunchedEffect(Unit) {
        // The grid is composed inside BoxWithConstraints, i.e. during layout:
        // wait for a frame so its focus target is attached before asking.
        repeat(5) {
            withFrameNanos { }
            val focused = try {
                focusRequester.requestFocus()
                true
            } catch (notAttachedYet: IllegalStateException) {
                false
            }
            if (focused) return@LaunchedEffect
        }
        // Still not attached: the tabs keep focus and the grid is one press
        // of down away.
    }
}

@Composable
private fun GuideInfoPanel(model: GuideModel, cursor: GuideCursor, focused: Boolean, now: Long) {
    val row = model.rows[cursor.row]
    val programme: Programme? = if (cursor.onChannel) {
        nowPlaying(row.programmes, now)
    } else {
        row.programmes.getOrNull(programmeIndexAt(row.programmes, cursor.time))
    }
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(INFO_HEIGHT)
            .clip(RoundedCornerShape(10.dp))
            .background(HeaderBackground)
            .border(1.dp, PanelStroke, RoundedCornerShape(10.dp))
            .padding(horizontal = 14.dp, vertical = 6.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                val live = programme != null && now >= programme.start && now < programme.end
                if (live) {
                    Box(
                        modifier = Modifier
                            .background(LiveRed, RoundedCornerShape(4.dp))
                            .padding(horizontal = 6.dp),
                    ) {
                        Text(
                            text = "LIVE",
                            style = MaterialTheme.typography.labelSmall,
                            color = Color.White,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 0.6.sp,
                        )
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                }
                Text(
                    text = if (programme == null) "Nothing listed right now" else programmeWhen(programme, now),
                    style = MaterialTheme.typography.labelMedium,
                    color = PremiumGold,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                )
            }
            Text(
                text = when {
                    programme == null -> row.channel.name
                    programme.episode.isNotBlank() -> "${programme.title} — ${programme.episode}"
                    else -> programme.title
                },
                style = MaterialTheme.typography.titleMedium,
                color = Color.White,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
            Text(
                text = programme?.desc?.takeIf { it.isNotBlank() }
                    ?: if (focused) "OK to watch · ◀ ▶ ▲ ▼ to move through the guide" else "Tap a show to watch it",
                style = MaterialTheme.typography.bodySmall,
                color = MutedText,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
        }
        Spacer(modifier = Modifier.width(14.dp))
        Column(horizontalAlignment = Alignment.End) {
            Text(
                text = if (row.channel.chno.isNotBlank()) "${row.channel.chno} · ${row.channel.name}" else row.channel.name,
                style = MaterialTheme.typography.labelLarge,
                color = Color.White,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
                textAlign = TextAlign.End,
                modifier = Modifier.width(220.dp),
            )
            Text(
                text = row.channel.group,
                style = MaterialTheme.typography.labelSmall,
                color = MutedText,
                maxLines = 1,
                textAlign = TextAlign.End,
                modifier = Modifier.width(220.dp),
            )
            Text(
                text = "${model.rows.size} channels listed",
                style = MaterialTheme.typography.labelSmall,
                color = MutedText,
                maxLines = 1,
                textAlign = TextAlign.End,
                modifier = Modifier.width(220.dp),
            )
        }
    }
}

/** "8:00 PM - 9:00 PM · 34 min left · Sports" for the detail strip. */
private fun programmeWhen(programme: Programme, now: Long): String {
    val range = formatRange(programme.start, programme.end)
    val timing = when {
        now >= programme.end -> "ended"
        now >= programme.start -> "${((programme.end - now + 59) / 60).coerceAtLeast(1)} min left"
        programme.start - now < 3600 -> "starts in ${((programme.start - now + 59) / 60).coerceAtLeast(1)} min"
        else -> "later today"
    }
    val category = programme.category.substringBefore(';').trim()
    return if (category.isEmpty()) "$range · $timing" else "$range · $timing · $category"
}

@Composable
private fun GuideTimeHeader(
    windowStart: Long,
    windowEnd: Long,
    now: Long,
    labelWidth: Dp,
    slotWidth: Dp,
    timelineWidth: Dp,
    scrollX: () -> Float,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(HEADER_HEIGHT)
            .clip(RoundedCornerShape(topStart = 8.dp, topEnd = 8.dp))
            .background(HeaderBackground),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Box(
            modifier = Modifier
                .width(labelWidth)
                .fillMaxHeight()
                .padding(start = 12.dp),
            contentAlignment = Alignment.CenterStart,
        ) {
            Text(
                text = formatGuideDate(windowStart),
                style = MaterialTheme.typography.labelMedium,
                color = PremiumGold,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
            )
        }
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .clipToBounds(),
        ) {
            Box(
                modifier = Modifier
                    .wrapContentWidth(align = Alignment.Start, unbounded = true)
                    .width(timelineWidth)
                    .fillMaxHeight()
                    .offset { IntOffset(-scrollX().roundToInt(), 0) },
            ) {
                repeat(GUIDE_SLOTS) { slot ->
                    val tick = windowStart + slot * GUIDE_SLOT_SECONDS
                    Box(
                        modifier = Modifier
                            .offset(x = slotWidth * slot.toFloat())
                            .width(slotWidth)
                            .fillMaxHeight()
                            .padding(start = 8.dp),
                        contentAlignment = Alignment.CenterStart,
                    ) {
                        Text(
                            text = formatClock(tick),
                            style = MaterialTheme.typography.labelMedium,
                            color = if (slot % 2 == 0) Color.White else MutedText,
                            fontWeight = if (slot % 2 == 0) FontWeight.SemiBold else FontWeight.Normal,
                            maxLines = 1,
                        )
                    }
                    Box(
                        modifier = Modifier
                            .offset(x = slotWidth * slot.toFloat())
                            .width(1.dp)
                            .fillMaxHeight()
                            .background(GridLine),
                    )
                }
                if (now >= windowStart && now < windowEnd) {
                    Box(
                        modifier = Modifier
                            .offset(x = slotWidth * ((now - windowStart).toFloat() / GUIDE_SLOT_SECONDS.toFloat()) - 1.dp)
                            .width(3.dp)
                            .fillMaxHeight()
                            .background(LiveRed),
                    )
                }
            }
        }
    }
}

@Composable
private fun GuideSectionHeading(section: GuideItem.Section, labelWidth: Dp) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(SECTION_HEIGHT)
            .background(Color(0xFF10161E))
            .padding(start = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Text(
            text = section.name.uppercase(),
            style = MaterialTheme.typography.labelSmall,
            color = PremiumGold,
            fontWeight = FontWeight.Bold,
            letterSpacing = 0.9.sp,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.width(labelWidth - 12.dp),
        )
        Text(
            text = "${section.count} ${if (section.count == 1) "channel" else "channels"}",
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
            maxLines = 1,
        )
    }
}

@Composable
private fun GuideChannelRow(
    row: GuideRow,
    windowStart: Long,
    windowEnd: Long,
    now: Long,
    labelWidth: Dp,
    slotWidth: Dp,
    timelineWidth: Dp,
    scrollX: () -> Float,
    channelHighlighted: Boolean,
    highlightedProgramme: Int,
    onSelect: () -> Unit,
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .height(ROW_HEIGHT),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        GuideChannelCell(
            channel = row.channel,
            width = labelWidth,
            highlighted = channelHighlighted,
            onClick = onSelect,
        )
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .clipToBounds()
                .background(GridBackground),
        ) {
            Box(
                modifier = Modifier
                    .wrapContentWidth(align = Alignment.Start, unbounded = true)
                    .width(timelineWidth)
                    .fillMaxHeight()
                    .offset { IntOffset(-scrollX().roundToInt(), 0) },
            ) {
                repeat(GUIDE_SLOTS) { slot ->
                    Box(
                        modifier = Modifier
                            .offset(x = slotWidth * slot.toFloat())
                            .width(1.dp)
                            .fillMaxHeight()
                            .background(GridLine),
                    )
                }
                row.programmes.forEachIndexed { index, programme ->
                    GuideProgrammeCell(
                        programme = programme,
                        now = now,
                        windowStart = windowStart,
                        windowEnd = windowEnd,
                        slotWidth = slotWidth,
                        scrollX = scrollX,
                        highlighted = index == highlightedProgramme,
                        onClick = onSelect,
                    )
                }
                if (now >= windowStart && now < windowEnd) {
                    Box(
                        modifier = Modifier
                            .offset(x = slotWidth * ((now - windowStart).toFloat() / GUIDE_SLOT_SECONDS.toFloat()))
                            .width(2.dp)
                            .fillMaxHeight()
                            .background(LiveRed),
                    )
                }
            }
        }
    }
}

@Composable
private fun GuideChannelCell(channel: Channel, width: Dp, highlighted: Boolean, onClick: () -> Unit) {
    val currentOnClick by rememberUpdatedState(onClick)
    val shape = RoundedCornerShape(topStart = 6.dp, bottomStart = 6.dp)
    Row(
        modifier = Modifier
            .width(width)
            .fillMaxHeight()
            .padding(vertical = 1.dp)
            .clip(shape)
            .background(if (highlighted) CardBackgroundFocused else CardBackground)
            .then(if (highlighted) Modifier.border(2.dp, Color.White, shape) else Modifier)
            .pointerInput(Unit) { detectTapGestures(onTap = { currentOnClick() }) }
            .padding(horizontal = 10.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        if (channel.chno.isNotBlank()) {
            Text(
                text = channel.chno,
                style = MaterialTheme.typography.labelMedium,
                color = PremiumGold,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
                overflow = TextOverflow.Clip,
                modifier = Modifier.width(34.dp),
            )
        }
        var logoShown by remember(channel.logo) { mutableStateOf(false) }
        Box(
            modifier = Modifier
                .width(42.dp)
                .height(32.dp)
                .clip(RoundedCornerShape(5.dp))
                .background(Color(0xFF202A36)),
            contentAlignment = Alignment.Center,
        ) {
            if (!logoShown) {
                Text(
                    text = initialsOf(channel.name),
                    style = MaterialTheme.typography.labelMedium,
                    color = PremiumGold,
                    fontWeight = FontWeight.Bold,
                )
            }
            if (channel.logo.isNotBlank()) {
                AsyncImage(
                    model = channel.logo,
                    contentDescription = null,
                    contentScale = ContentScale.Fit,
                    modifier = Modifier.fillMaxSize(),
                    onSuccess = { logoShown = true },
                )
            }
        }
        Spacer(modifier = Modifier.width(8.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = channel.name,
                style = MaterialTheme.typography.labelMedium,
                color = Color.White,
                fontWeight = FontWeight.SemiBold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
            )
            Text(
                text = if (channel.country.isNotBlank()) "${channel.group} · ${channel.country}" else channel.group,
                style = MaterialTheme.typography.labelSmall,
                color = MutedText,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis,
            )
        }
    }
}

@Composable
private fun GuideProgrammeCell(
    programme: Programme,
    now: Long,
    windowStart: Long,
    windowEnd: Long,
    slotWidth: Dp,
    scrollX: () -> Float,
    highlighted: Boolean,
    onClick: () -> Unit,
) {
    val visibleStart = maxOf(programme.start, windowStart)
    val visibleEnd = minOf(programme.end, windowEnd)
    if (visibleEnd <= visibleStart) return
    val currentOnClick by rememberUpdatedState(onClick)
    val x = slotWidth * ((visibleStart - windowStart).toFloat() / GUIDE_SLOT_SECONDS.toFloat())
    val width = slotWidth * ((visibleEnd - visibleStart).toFloat() / GUIDE_SLOT_SECONDS.toFloat())
    val live = now >= programme.start && now < programme.end
    val shape = RoundedCornerShape(6.dp)
    val density = LocalDensity.current
    val cellStartPx = with(density) { x.toPx() }
    val minVisiblePx = with(density) { MIN_VISIBLE_TITLE.roundToPx() }
    Box(
        modifier = Modifier
            .offset(x = x)
            .width(width)
            .fillMaxHeight()
            .padding(horizontal = 1.5.dp, vertical = 3.dp)
            .clip(shape)
            .background(
                when {
                    highlighted -> CellHighlight
                    live -> CellLive
                    else -> CellIdle
                },
            )
            .border(
                width = if (highlighted) 2.dp else 1.dp,
                color = when {
                    highlighted -> Color.White
                    live -> PremiumGold
                    else -> CellStroke
                },
                shape = shape,
            )
            .pointerInput(Unit) { detectTapGestures(onTap = { currentOnClick() }) },
    ) {
        if (width >= 30.dp) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .layout { measurable, constraints ->
                        // A show that started left of the visible window keeps
                        // its time and title at the visible edge, as on a
                        // cable box, instead of showing the cut-off tail.
                        val hidden = (scrollX() - cellStartPx).roundToInt().coerceIn(0, constraints.maxWidth)
                        val remaining = constraints.maxWidth - hidden
                        val placeable = measurable.measure(constraints.copy(minWidth = 0, maxWidth = remaining))
                        layout(constraints.maxWidth, placeable.height) {
                            // A sliver too narrow for a title stays an empty block.
                            if (hidden == 0 || remaining >= minVisiblePx) placeable.place(hidden, 0)
                        }
                    }
                    .padding(horizontal = 7.dp, vertical = 4.dp),
                verticalArrangement = Arrangement.Center,
            ) {
                Text(
                    text = (if (programme.start < windowStart) "‹ " else "") + formatClock(programme.start),
                    style = MaterialTheme.typography.labelSmall,
                    color = if (live || highlighted) PremiumGold else MutedText,
                    fontWeight = FontWeight.Bold,
                    maxLines = 1,
                    overflow = TextOverflow.Clip,
                )
                Text(
                    text = programme.title,
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.White,
                    fontWeight = if (live || highlighted) FontWeight.SemiBold else FontWeight.Normal,
                    maxLines = 2,
                    overflow = TextOverflow.Ellipsis,
                )
            }
        }
    }
}

@Composable
private fun GuideMessage(message: String) {
    Box(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = SCREEN_GUTTER, vertical = 28.dp),
        contentAlignment = Alignment.Center,
    ) {
        Text(
            text = message,
            style = MaterialTheme.typography.bodyMedium,
            color = MutedText,
            textAlign = TextAlign.Center,
        )
    }
}
