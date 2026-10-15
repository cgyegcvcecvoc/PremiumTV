package com.premiumtv.app.ui

import com.premiumtv.app.data.CategoryGroup
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.Programme

/*
 * The data behind the cable-style guide, kept free of Compose so the ordering
 * and the remote-control movement can be unit tested on the JVM.
 *
 * The grid is the classic cable box layout: channels down the left, their
 * programmes to the right, half-hour times across the top, eight hours from
 * the current half hour.
 */

internal const val GUIDE_SLOT_SECONDS = 30L * 60L
internal const val GUIDE_WINDOW_SECONDS = 8L * 60L * 60L
internal const val GUIDE_SLOTS = (GUIDE_WINDOW_SECONDS / GUIDE_SLOT_SECONDS).toInt()

/** The half hour the guide starts at: 7:47 PM shows from 7:30 PM. */
internal fun guideWindowStart(now: Long): Long = (now / GUIDE_SLOT_SECONDS) * GUIDE_SLOT_SECONDS

/** One channel line of the grid and the shows it lists inside the window. */
internal data class GuideRow(val channel: Channel, val programmes: List<Programme>)

/** What the grid's lazy list shows: a category heading, or a channel line. */
internal sealed interface GuideItem {
    data class Section(val name: String, val count: Int) : GuideItem
    data class Row(val index: Int, val row: GuideRow) : GuideItem
}

internal class GuideModel(
    val rows: List<GuideRow>,
    val items: List<GuideItem>,
    /** The lazy-list position of each row; the category headings take positions too. */
    val itemIndexOfRow: IntArray,
    val windowStart: Long,
    val windowEnd: Long,
)

/**
 * Builds the grid rows.
 *
 * Channels follow the published category order - the order of the Channels
 * tab - and keep their playlist order inside a category. A channel's backup
 * feeds share its EPG id, so they would repeat the same listings line for
 * line; the first feed (the main category comes before its Backups group)
 * stands for all of them. Only channels with something listed in the window
 * get a row: the rest still play from the Channels tab.
 */
internal fun buildGuideModel(
    channels: List<Channel>,
    groups: List<CategoryGroup>,
    programmes: Map<String, List<Programme>>,
    windowStart: Long,
    windowEnd: Long = windowStart + GUIDE_WINDOW_SECONDS,
): GuideModel {
    val order = HashMap<String, Int>(groups.size * 2)
    groups.forEachIndexed { index, group -> order.putIfAbsent(group.name, index) }
    val ordered = channels.withIndex().sortedWith(
        compareBy<IndexedValue<Channel>>(
            { order[it.value.group] ?: Int.MAX_VALUE },
            // Categories the group list does not know stay together, by name.
            { if (order.containsKey(it.value.group)) "" else it.value.group },
            { it.index },
        ),
    )

    val seen = HashSet<String>()
    val rows = ArrayList<GuideRow>()
    for (entry in ordered) {
        val channel = entry.value
        val key = channel.id.ifBlank { channel.url }
        if (key.isBlank() || key in seen) continue
        val listed = programmes[channel.id].orEmpty()
            .filter { it.end > windowStart && it.start < windowEnd }
        if (listed.isEmpty()) continue
        seen.add(key)
        rows.add(GuideRow(channel, listed.sortedBy { it.start }))
    }

    val counts = HashMap<String, Int>()
    for (row in rows) counts[row.channel.group] = (counts[row.channel.group] ?: 0) + 1
    val items = ArrayList<GuideItem>(rows.size + counts.size)
    val itemIndexOfRow = IntArray(rows.size)
    var group: String? = null
    for ((index, row) in rows.withIndex()) {
        if (row.channel.group != group) {
            group = row.channel.group
            items.add(GuideItem.Section(row.channel.group, counts[row.channel.group] ?: 0))
        }
        itemIndexOfRow[index] = items.size
        items.add(GuideItem.Row(index, row))
    }
    return GuideModel(rows, items, itemIndexOfRow, windowStart, windowEnd)
}

/** A remote-control move inside the grid. */
internal enum class GuideMove { Up, Down, Left, Right }

/**
 * The guide's highlight: a row, and either its channel cell or the show on at
 * [time]. Keeping a time rather than a show index is what stops the highlight
 * drifting sideways while scrolling channels with long and short shows.
 */
internal data class GuideCursor(val row: Int, val time: Long, val onChannel: Boolean = false)

/** The show on at [time]; else the next one; else the last; -1 when there is none. */
internal fun programmeIndexAt(programmes: List<Programme>, time: Long): Int {
    if (programmes.isEmpty()) return -1
    var next = -1
    for (index in programmes.indices) {
        val programme = programmes[index]
        if (time >= programme.start && time < programme.end) return index
        if (next < 0 && programme.start > time) next = index
    }
    return if (next >= 0) next else programmes.lastIndex
}

/**
 * Moves the highlight like a cable remote: up and down keep the highlighted
 * time, right and left step one show at a time, and left of the first show is
 * the channel cell. Returns null when the move leaves the grid (up from the
 * first row, left of the channel column) so the caller hands focus back to
 * the tabs; a move that cannot go further returns the cursor unchanged.
 */
internal fun moveGuideCursor(model: GuideModel, cursor: GuideCursor, move: GuideMove): GuideCursor? {
    if (model.rows.isEmpty()) return null
    val row = cursor.row.coerceIn(0, model.rows.lastIndex)
    val programmes = model.rows[row].programmes
    return when (move) {
        GuideMove.Up -> if (row == 0) null else cursor.copy(row = row - 1)
        GuideMove.Down -> cursor.copy(row = minOf(row + 1, model.rows.lastIndex))
        GuideMove.Right -> {
            val index = programmeIndexAt(programmes, cursor.time)
            when {
                cursor.onChannel -> cursor.copy(row = row, onChannel = false)
                index < 0 || index >= programmes.lastIndex -> cursor.copy(row = row)
                else -> cursor.copy(row = row, time = maxOf(programmes[index + 1].start, model.windowStart))
            }
        }
        GuideMove.Left -> {
            val index = programmeIndexAt(programmes, cursor.time)
            when {
                cursor.onChannel -> null
                index <= 0 -> cursor.copy(row = row, onChannel = true)
                else -> cursor.copy(row = row, time = maxOf(programmes[index - 1].start, model.windowStart))
            }
        }
    }
}

/** Channel up/down and page keys jump [rows] lines, keeping the highlighted time. */
internal fun pageGuideCursor(model: GuideModel, cursor: GuideCursor, rows: Int): GuideCursor {
    if (model.rows.isEmpty()) return cursor
    return cursor.copy(row = (cursor.row + rows).coerceIn(0, model.rows.lastIndex))
}
