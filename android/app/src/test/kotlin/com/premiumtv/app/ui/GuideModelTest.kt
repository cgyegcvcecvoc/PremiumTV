package com.premiumtv.app.ui

import com.premiumtv.app.data.CategoryGroup
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.Programme
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

/** The cable guide's ordering and remote-control movement, on the plain JVM. */
class GuideModelTest {
    private val start = 1_800_000_000L - (1_800_000_000L % GUIDE_SLOT_SECONDS)

    private fun channel(id: String, name: String, group: String, url: String = "https://example.org/$name") =
        Channel(id, name, "", group, "US", "", url, "", "", "")

    private fun show(channel: String, from: Long, minutes: Long, title: String) =
        Programme(channel, from, from + minutes * 60L, title, "", "", "", "")

    private fun model(): GuideModel {
        val channels = listOf(
            channel("news.us", "Newsroom", "News"),
            channel("sports.us", "Sports One", "Sports"),
            channel("sports.us", "Sports One (Backup 1)", "Sports Backups"),
            channel("quiet.us", "No Listings", "Sports"),
            channel("movies.us", "Movie House", "Movies"),
        )
        val groups = listOf(
            CategoryGroup("Sports", 2), CategoryGroup("News", 1),
            CategoryGroup("Movies", 1), CategoryGroup("Sports Backups", 1),
        )
        val programmes = mapOf(
            // Started before the window, a gap, then shows of different lengths.
            "sports.us" to listOf(
                show("sports.us", start - 900, 30, "Match"),
                show("sports.us", start + 1800, 30, "Highlights"),
                show("sports.us", start + 3600, 120, "Late Game"),
            ),
            "news.us" to listOf(
                show("news.us", start, 60, "Evening News"),
                show("news.us", start + 3600, 60, "World Report"),
            ),
            // Ends before the window opens: no row.
            "movies.us" to listOf(show("movies.us", start - 7200, 60, "Matinee")),
        )
        return buildGuideModel(channels, groups, programmes, start)
    }

    @Test fun rowsFollowThePublishedCategoryOrderAndCollapseBackups() {
        val model = model()
        assertEquals(listOf("Sports One", "Newsroom"), model.rows.map { it.channel.name })
        assertEquals(
            listOf("Sports", "row", "News", "row"),
            model.items.map { if (it is GuideItem.Section) it.name else "row" },
        )
        assertEquals(1, model.itemIndexOfRow[0])
        assertEquals(3, model.itemIndexOfRow[1])
        assertEquals(start + GUIDE_WINDOW_SECONDS, model.windowEnd)
        assertEquals(16, GUIDE_SLOTS)
    }

    @Test fun windowStartsAtTheCurrentHalfHour() {
        assertEquals(start, guideWindowStart(start + 17 * 60L))
        assertEquals(start + GUIDE_SLOT_SECONDS, guideWindowStart(start + GUIDE_SLOT_SECONDS))
    }

    @Test fun programmeAtFindsTheLiveShowThenTheNextOne() {
        val shows = model().rows[0].programmes
        assertEquals(0, programmeIndexAt(shows, start + 60))
        // 15:00 into the window falls in a gap: the next show is chosen.
        assertEquals(1, programmeIndexAt(shows, start + 1000))
        assertEquals(2, programmeIndexAt(shows, start + 4000))
        assertEquals(2, programmeIndexAt(shows, start + 99_999))
        assertEquals(-1, programmeIndexAt(emptyList(), start))
    }

    @Test fun rightAndLeftStepOneShowAndLeftOfTheFirstIsTheChannel() {
        val model = model()
        var cursor = GuideCursor(row = 0, time = start + 60)
        cursor = moveGuideCursor(model, cursor, GuideMove.Right)!!
        assertEquals(start + 1800, cursor.time)
        cursor = moveGuideCursor(model, cursor, GuideMove.Right)!!
        assertEquals(start + 3600, cursor.time)
        // The last show: right stays put rather than leaving the grid.
        assertEquals(cursor, moveGuideCursor(model, cursor, GuideMove.Right))
        cursor = moveGuideCursor(model, cursor, GuideMove.Left)!!
        cursor = moveGuideCursor(model, cursor, GuideMove.Left)!!
        // The first show began before the window: its cell starts at the window.
        assertEquals(start, cursor.time)
        cursor = moveGuideCursor(model, cursor, GuideMove.Left)!!
        assertTrue(cursor.onChannel)
        assertNull(moveGuideCursor(model, cursor, GuideMove.Left))
        assertEquals(false, moveGuideCursor(model, cursor, GuideMove.Right)!!.onChannel)
    }

    @Test fun upAndDownKeepTheHighlightedTime() {
        val model = model()
        val cursor = GuideCursor(row = 0, time = start + 3600)
        val down = moveGuideCursor(model, cursor, GuideMove.Down)!!
        assertEquals(1, down.row)
        assertEquals(start + 3600, down.time)
        assertEquals("World Report", model.rows[1].programmes[programmeIndexAt(model.rows[1].programmes, down.time)].title)
        // Bottom row: down stays; top row: up leaves the grid for the tabs.
        assertEquals(down, moveGuideCursor(model, down, GuideMove.Down))
        assertNull(moveGuideCursor(model, cursor, GuideMove.Up))
        assertEquals(1, pageGuideCursor(model, cursor, 8).row)
        assertEquals(0, pageGuideCursor(model, down, -8).row)
    }
}
