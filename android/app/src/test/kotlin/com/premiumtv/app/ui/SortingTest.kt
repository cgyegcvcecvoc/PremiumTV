package com.premiumtv.app.ui

import com.premiumtv.app.data.CategoryGroup
import com.premiumtv.app.data.Channel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/** The 1.0.8 category/channel sorting, on the plain JVM. */
class SortingTest {

    private fun channel(name: String, chno: String = "") =
        Channel("id.$name", name, "", "Group", "US", chno, "https://s/$name", "", "", "")

    private val groups = listOf(
        CategoryGroup("Zoo", 3),
        CategoryGroup("Alpha", 40),
        CategoryGroup("News", 12),
        CategoryGroup("Beta", 40),
    )

    @Test fun publishedKeepsTheRepositoryOrder() {
        assertEquals(listOf("Zoo", "Alpha", "News", "Beta"), CategorySort.Published.sort(groups).map { it.name })
    }

    @Test fun alphabeticalSortsCaseInsensitivelyBothWays() {
        assertEquals(
            listOf("Alpha", "Beta", "News", "Zoo"),
            CategorySort.Alpha.sort(groups).map { it.name },
        )
        assertEquals(
            listOf("Zoo", "News", "Beta", "Alpha"),
            CategorySort.AlphaDesc.sort(groups).map { it.name },
        )
    }

    @Test fun biggestSortsByCountWithAlphabeticalTies() {
        assertEquals(
            listOf("Alpha", "Beta", "News", "Zoo"),
            CategorySort.Biggest.sort(groups).map { it.name },
        )
    }

    @Test fun everySortCyclesBackToItselfInFourSteps() {
        for (sort in CategorySort.entries) {
            val third = sort.next.next.next
            assertEquals(sort, third.next)
        }
    }

    @Test fun channelSortOrdersByNameAndChannelNumber() {
        val channels = listOf(channel("Marco"), channel("anna"), channel("Zed"))
        assertEquals(
            listOf("anna", "Marco", "Zed"),
            ChannelSort.Alpha.sort(channels).map { it.name },
        )
        assertEquals(
            listOf("Zed", "Marco", "anna"),
            ChannelSort.AlphaDesc.sort(channels).map { it.name },
        )
    }

    @Test fun channelNumberSortsNumericallyWithUnnumberedLast() {
        val channels = listOf(
            channel("No Number"),
            channel("Ten", chno = "10"),
            channel("Two", chno = "2"),
            channel("Also None"),
        )
        // Numbers first (2 before 10, numerically), unnumbered channels last
        // in name order.
        val sorted = ChannelSort.Number.sort(channels).map { it.name }
        assertEquals(listOf("Two", "Ten", "Also None", "No Number"), sorted)
    }

    @Test fun defaultChannelSortKeepsPlaylistOrder() {
        val channels = listOf(channel("Zed"), channel("anna"))
        assertEquals(listOf("Zed", "anna"), ChannelSort.Default.sort(channels).map { it.name })
    }

    @Test fun everyChannelSortCyclesBackToItselfInFourSteps() {
        for (sort in ChannelSort.entries) {
            val third = sort.next.next.next
            assertEquals(sort, third.next)
        }
    }
}
