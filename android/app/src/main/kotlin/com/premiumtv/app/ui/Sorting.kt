package com.premiumtv.app.ui

import com.premiumtv.app.data.CategoryGroup
import com.premiumtv.app.data.Channel

/**
 * How the category list is ordered (1.0.8).
 *
 * The Channels tab is a list of categories now, so the list itself gets the
 * sorting a long list needs: the repository's published order, alphabetical
 * both ways, or biggest first. [next] is the mode one click cycles to, so the
 * whole control is one D-pad-focusable button — no dropdown on a TV remote.
 */
enum class CategorySort(val label: String) {
    Published("Published order"),
    Alpha("A to Z"),
    AlphaDesc("Z to A"),
    Biggest("Most channels"),
    ;

    /** The mode one click cycles to. */
    val next: CategorySort
        get() = when (this) {
            Published -> Alpha
            Alpha -> AlphaDesc
            AlphaDesc -> Biggest
            Biggest -> Published
        }

    /** Returns [groups] in this order; ties break alphabetically. */
    fun sort(groups: List<CategoryGroup>): List<CategoryGroup> = when (this) {
        Published -> groups
        Alpha -> groups.sortedBy { it.name.lowercase() }
        AlphaDesc -> groups.sortedByDescending { it.name.lowercase() }
        Biggest -> groups.sortedWith(
            compareByDescending<CategoryGroup> { it.count }.thenBy { it.name.lowercase() },
        )
    }
}

/**
 * How the channels inside one category page are ordered. [Default] is the
 * playlist order the scraper published; [Number] sorts by channel number with
 * unnumbered channels last.
 */
enum class ChannelSort(val label: String) {
    Default("Playlist order"),
    Alpha("A to Z"),
    AlphaDesc("Z to A"),
    Number("Channel number"),
    ;

    /** The mode one click cycles to. */
    val next: ChannelSort
        get() = when (this) {
            Default -> Alpha
            Alpha -> AlphaDesc
            AlphaDesc -> Number
            Number -> Default
        }

    /** Returns [channels] in this order. */
    fun sort(channels: List<Channel>): List<Channel> = when (this) {
        Default -> channels
        Alpha -> channels.sortedBy { it.name.lowercase() }
        AlphaDesc -> channels.sortedByDescending { it.name.lowercase() }
        Number -> channels.sortedWith(
            compareBy<Channel> { it.chno.toIntOrNull() ?: Int.MAX_VALUE }
                .thenBy { it.name.lowercase() },
        )
    }
}
