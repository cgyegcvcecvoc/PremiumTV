"""1.1.17 contracts: the stutter, and the crashes that could hide behind it.

The report came in as two things at once - "it lags badly when I open some
screens, and it has stopped on me when I open others or watch a channel". The
causes found were:

* opening any channel re-parsed **every** channel name in the library with six
  regular expressions on the UI thread (``serversFor`` -> ``liveEventIndex`` ->
  ``groupLiveEvents``), and the Channels tab ran the same two passes again
  during its first composition - the lag, and GC churn on a small-heap stick;
* a focused search field called ``FocusRequester.requestFocus()`` unguarded,
  which throws ``IllegalStateException`` when the node is detached;
* ``playlist[serverIndex.coerceIn(0, playlist.lastIndex)]`` throws on an empty
  feed list, and ``mediaSourceFor`` could throw from inside player setup;
* a lazy list given two identical keys throws during measure - and a
  *refreshed* library is whatever upstream published, deduplicated only by
  convention.

This pins the shape of the fix so a later edit cannot quietly reintroduce the
UI-thread scan, the unguarded focus request, or the unguarded index read.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "android" / "tools"))

MAIN = "android/app/src/main/kotlin/com/premiumtv/app"
TEST = "android/app/src/test/kotlin/com/premiumtv/app"


def text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Version1117Tests(unittest.TestCase):
    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        # 1.1.17 is published and 1.1.18 is the build in progress, so the
        # current-version pin lives in tests/test_release_1118.py; this keeps
        # 1.1.17's own artifacts and version math in place.
        self.assertEqual(release_version.android_version_code("1.1.17"), 101_170_000)
        self.assertEqual(release_version.compare_versions("1.1.17", "1.1.16"), 1)
        self.assertEqual(version_sync.check(), [])
        self.assertTrue(
            release_version.is_newer(version_sync.PUBLISHED_VERSION, "1.1.16"),
            "the published version must be at least 1.1.17",
        )

        notes = text("release-notes-1.1.17.md")
        self.assertIn("# PremiumTV 1.1.17 — ", notes)
        self.assertIn("versionCode `101170000`", notes)


class ChannelOpenTests(unittest.TestCase):
    def test_the_feeds_are_prepared_once_per_library(self):
        events = text(f"{MAIN}/ui/LiveEvents.kt")
        self.assertIn("internal class ChannelIndex", events)
        self.assertIn("internal fun buildChannelIndex(", events)
        self.assertIn("fun serversFor(channel: Channel): List<Channel>", events)
        # The free function keeps its signature for callers without an index,
        # but it is now the index's answer rather than a second implementation.
        self.assertIn(
            "internal fun serversFor(channel: Channel, channels: List<Channel>): List<Channel> =\n"
            "    buildChannelIndex(channels).serversFor(channel)",
            events,
        )
        self.assertNotIn("val servers = channels.filter { it.url != channel.url &&", events)

    def test_the_index_is_built_off_the_ui_thread(self):
        view_model = text(f"{MAIN}/TvViewModel.kt")
        self.assertIn("val channelIndex = _channelIndex.asStateFlow()", view_model)
        self.assertIn("withContext(Dispatchers.Default) { buildChannelIndex(channels) }", view_model)
        self.assertIn("PerfLog.recordIndexBuild(", view_model)
        self.assertIn("PerfLog.recordIndexFailure(", view_model)
        # A build that fails must leave an empty index, not a crash.
        self.assertIn("ChannelIndex.EMPTY", view_model)

    def test_the_browser_never_re_derives_the_feeds(self):
        screen = text(f"{MAIN}/ui/HomeScreen.kt")
        for gone in ("groupLiveEvents(", "liveEventIndex(", "serversFor("):
            self.assertNotIn(gone, screen, f"HomeScreen must not call {gone} any more")
        self.assertIn("channelIndex: ChannelIndex? = null", screen)
        self.assertIn("preparing = channelIndex == null", screen)
        self.assertIn("Preparing the live games", screen)

    def test_opening_a_channel_reads_the_index(self):
        root = text(f"{MAIN}/ui/AppRoot.kt")
        self.assertIn("val channelIndex by viewModel.channelIndex.collectAsState()", root)
        self.assertIn("index?.serversFor(channel)", root)
        self.assertIn("PerfLog.recordChannelOpen(", root)
        # The scan survives only as the pre-index fallback.
        self.assertIn("?: serversFor(channel, current.library.channels)", root)


class PlayerTests(unittest.TestCase):
    def test_an_index_can_never_be_read_out_of_bounds(self):
        player = text(f"{MAIN}/ui/PlayerScreen.kt")
        self.assertIn("fun feedAt(index: Int): Channel", player)
        self.assertNotIn("playlist[serverIndex", player)
        self.assertIn("getOrNull(index.coerceIn(0, (playlist.size - 1).coerceAtLeast(0)))", player)

    def test_a_feed_that_cannot_open_shows_the_error_card(self):
        player = text(f"{MAIN}/ui/PlayerScreen.kt")
        self.assertIn("private fun mediaSourceFor(context: Context, channel: Channel): MediaSource?", player)
        self.assertIn('errorMessage = "This feed could not be opened', player)
        self.assertIn("if (mediaSource == null) {", player)
        # The track callback is a callback: an unreadable layout costs the menu.
        self.assertIn('Log.w(TAG, "The stream\'s audio track layout could not be read", error)', player)
        self.assertIn("runCatching { player.pause() }", player)


class FocusTests(unittest.TestCase):
    def test_focus_requests_go_through_the_safe_helper(self):
        components = text(f"{MAIN}/ui/Components.kt")
        self.assertIn("fun FocusRequester.requestFocusSafely(): Boolean", components)
        self.assertIn("} catch (_: IllegalStateException) {", components)
        self.assertIn("requestFocusSafely()", text(f"{MAIN}/ui/HomeScreen.kt"))
        self.assertIn("requestFocusSafely()", text(f"{MAIN}/ui/CableGuide.kt"))

    def test_no_focus_request_is_left_unguarded(self):
        """One guard for every initial focus request in the app.

        ``requestFocus()`` throws ``IllegalStateException`` when the node is not
        attached yet, and every call site used to hand-roll its own answer
        (``runCatching``, a five-frame retry, nothing at all). 1.1.17 routes them
        all through ``requestFocusSafely()`` so a new call site cannot forget.
        """
        offenders = []
        for path in sorted((ROOT / MAIN / "ui").glob("*.kt")):
            source = path.read_text(encoding="utf-8")
            if ".requestFocus()" in source:
                offenders.append(path.name)
        self.assertEqual([], offenders, "call requestFocusSafely() instead")
        self.assertIn("actionFocus.requestFocusSafely()", text(f"{MAIN}/ui/UpdateNoticeDialog.kt"))


class DuplicateRowTests(unittest.TestCase):
    def test_the_data_boundary_de_duplicates_what_the_ui_keys(self):
        sanitize = text(f"{MAIN}/data/LibrarySanitize.kt")
        for name in ("internal fun dedupeChannels(", "internal fun dedupeGroups(", "internal fun channelRowKey("):
            self.assertIn(name, sanitize)

        repository = text(f"{MAIN}/data/TvRepository.kt")
        self.assertIn("dedupeChannels(parsedPlaylist?.first ?: current.channels)", repository)
        self.assertIn("dedupeChannels(readJsonLines(stream(\"channels.jsonl\"))", repository)
        self.assertIn("val uniqueChannels = dedupeChannels(channels)", repository)
        self.assertIn("groups = dedupeGroups(groups)", repository)

        self.assertIn("val unique = if (items.size < 2)", text(f"{MAIN}/ui/VodShelf.kt"))
        self.assertIn("key = { channelRowKey(it) }", text(f"{MAIN}/ui/HomeScreen.kt"))

    def test_the_jvm_tests_cover_the_new_rules(self):
        index_test = text(f"{TEST}/ui/ChannelIndexTest.kt")
        self.assertIn("buildChannelIndex(library)", index_test)
        self.assertIn("serversFor(channel, library)", index_test)
        self.assertIn("groupLiveEvents(library)", index_test)
        sanitize_test = text(f"{TEST}/data/LibrarySanitizeTest.kt")
        self.assertIn("dedupeChannels(", sanitize_test)
        self.assertIn("channelRowKey(", sanitize_test)


class DiagnosticsTests(unittest.TestCase):
    def test_the_bug_check_reports_measured_ui_work(self):
        diagnostics = text(f"{MAIN}/update/Diagnostics.kt")
        self.assertIn("uiWork: UiWorkSnapshot = UiWorkSnapshot()", diagnostics)
        self.assertIn('label = "UI work"', diagnostics)
        perf = text(f"{MAIN}/update/PerfLog.kt")
        self.assertIn("data class UiWorkSnapshot(", perf)
        self.assertIn("fun recordChannelOpen(", perf)
        self.assertIn("uiWork = PerfLog.snapshot", text(f"{MAIN}/TvViewModel.kt"))


class GuideGuardTests(unittest.TestCase):
    def test_the_guide_does_not_trust_a_stale_cursor(self):
        guide = text(f"{MAIN}/ui/CableGuide.kt")
        self.assertIn("model.itemIndexOfRow.getOrNull(target.row) ?: return@launch", guide)
        self.assertIn("model.rows.getOrNull(target.row)?.programmes.orEmpty()", guide)
        self.assertIn("val row = model.rows.getOrNull(cursor.row) ?: return", guide)
        self.assertIn('null -> "stale|$index"', guide)
        self.assertNotIn("model.rows[cursorNow().row]", guide)


if __name__ == "__main__":
    unittest.main()
