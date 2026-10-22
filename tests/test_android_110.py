"""Offline regression checks for the 1.1.0 UI contracts.

These are source-level assertions on purpose. The Kotlin UI cannot be compiled
in this repository's offline suite (no JDK, no Android SDK), so the promises a
release makes about its own screens are pinned here: the docked side player,
the category rail, the amber pointer ring, the automatic server backup, the
dead-channel filter and the still loading screen. The Gradle unit tests and the
emulator smoke gate in android-build.yml prove the rest.
"""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "android/app/src/main/kotlin/com/premiumtv/app/ui"
DATA = ROOT / "android/app/src/main/kotlin/com/premiumtv/app/data"
MAC_RENDERER = ROOT / "macos/app/src/renderer"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class DockedSidePlayerTests(unittest.TestCase):
    def test_app_root_docks_the_player_on_the_right_without_rebuilding_it(self):
        root = text(UI / "AppRoot.kt")
        # The dock's width is reserved in a Row on a TV, so the browser is
        # never covered; a narrow window overlays the dock instead of squeezing
        # the browser to nothing.
        self.assertIn("val narrow = maxWidth < 720.dp", root)
        self.assertIn("(maxWidth * 0.40f).coerceIn(300.dp, 420.dp)", root)
        self.assertIn("Spacer(modifier = Modifier.width(dockWidth).fillMaxHeight())", root)
        self.assertIn("sidePlayer && !narrow", root)
        # One PlayerScreen call site for both layouts: flipping to full screen
        # must not create a second remembered ExoPlayer.
        self.assertEqual(root.count("PlayerScreen("), 1)
        self.assertIn(".align(Alignment.CenterEnd)", root)
        self.assertIn("expanded = !sidePlayer", root)
        self.assertIn("onMinimize = { sidePlayer = true }", root)

    def test_the_small_picture_and_its_button_both_go_full_screen(self):
        player = text(UI / "PlayerScreen.kt")
        self.assertIn("SidePlayerPicture(", player)
        self.assertIn(".tvClickable(onExpand)", player)
        # The emulator smoke gate taps these exact labels.
        self.assertIn('FocusButton("⤢ Big screen"', player)
        self.assertIn('FocusButton("✕ Close"', player)
        self.assertIn("AUTO BACKUP", player)

    def test_one_video_call_site_keeps_the_surface_across_the_flip(self):
        player = text(UI / "PlayerScreen.kt")
        self.assertEqual(player.count("AndroidView("), 1)
        # The Column and the video Box are built for both layouts, so Compose
        # reuses the same node instead of disposing the PlayerView on a flip.
        self.assertIn("val videoModifier = if (expanded)", player)
        self.assertIn("weight(1f)", player)
        self.assertIn("aspectRatio(16f / 9f)", player)


class AutomaticBackupTests(unittest.TestCase):
    def test_walk_rules_are_pure_and_tested(self):
        fallback = text(UI / "ServerFallback.kt")
        for marker in ("autoNextServerIndex", "hasBackupServer", "serverSwitchNotice",
                       "serverStatusLine", "exhaustedServerMessage"):
            self.assertIn(marker, fallback)
        tests = text(ROOT / "android/app/src/test/kotlin/com/premiumtv/app/ui/ServerFallbackTest.kt")
        self.assertIn("autoNextServerIndex(2, 3)", tests)

    def test_the_player_marks_failed_feeds_and_hides_a_channel_only_when_exhausted(self):
        player = text(UI / "PlayerScreen.kt")
        self.assertIn("onFeedFailed", player)
        self.assertIn("onChannelDead", player)
        self.assertIn("reportFailed.value(failed)", player)
        self.assertIn("reportDead.value(channel)", player)
        self.assertIn("ServerSwitchReason.Stalled", player)
        self.assertIn("autoNextServerIndex(serverIndex, playlist.size)", player)

    def test_known_dead_servers_are_tried_last(self):
        player = text(UI / "PlayerScreen.kt")
        self.assertIn("healthyServersFirst(full, deadUrls)", player)


class DeadChannelFilterTests(unittest.TestCase):
    def test_health_rules_are_pure_and_tested(self):
        health = text(DATA / "ChannelHealth.kt")
        for marker in ("DEAD_FEED_TTL_MS", "pruneDeadFeeds", "deadUrlSet",
                       "visibleChannels", "hiddenChannelCount", "healthyServersFirst"):
            self.assertIn(marker, health)
        tests = text(ROOT / "android/app/src/test/kotlin/com/premiumtv/app/data/ChannelHealthTest.kt")
        self.assertIn("recordings expire", tests)

    def test_the_browser_gets_a_filtered_library_and_a_restore_action(self):
        root = text(UI / "AppRoot.kt")
        self.assertIn("ChannelHealthStore(appContext)", root)
        self.assertIn("visibleChannels(current.library.channels, deadUrls)", root)
        self.assertIn("onRestoreHiddenChannels = {", root)
        home = text(UI / "HomeScreen.kt")
        self.assertIn("hiddenChannelCount", home)
        self.assertIn('FocusButton("Restore hidden channels")', home)

    def test_the_mac_app_has_the_same_memory(self):
        health = text(MAC_RENDERER / "health.js")
        for marker in ("TTL_MS", "filterChannels", "record", "clear"):
            self.assertIn(marker, health)
        app = text(MAC_RENDERER / "app.js")
        self.assertIn("PremiumHealth", app)
        self.assertIn("health.filterChannels(channels, deadFeeds)", app)
        self.assertIn("restore-hidden", app)
        self.assertIn('src="health.js"', text(MAC_RENDERER / "index.html"))


class PointerOutlineTests(unittest.TestCase):
    def test_one_amber_ring_is_shared_by_every_focusable_surface(self):
        theme = text(UI / "Theme.kt")
        self.assertRegex(theme, r"val FocusRing = Color\(0xFFFFB020\)")
        components = text(UI / "Components.kt")
        self.assertIn("internal fun Modifier.focusOutline(", components)
        # Cards, tabs and buttons.
        self.assertGreaterEqual(components.count("focusOutline("), 4)
        # Guide cells, category rows, search field and the side player picture.
        self.assertIn("FocusRing", text(UI / "CableGuide.kt"))

    def test_the_mac_pointer_ring_matches(self):
        css = text(MAC_RENDERER / "app.css")
        self.assertIn("outline: 3px solid #ffb020", css)
        self.assertIn("#player.mini .player-stage:focus-visible", css)


class StillLoadingScreenTests(unittest.TestCase):
    def test_no_infinite_animation_survives_in_the_android_loading_screen(self):
        components = text(UI / "Components.kt")
        self.assertNotIn("rememberInfiniteTransition", components)
        self.assertNotIn("CircularProgressIndicator", components)
        for keyframe in ("logoPulse", "shimmerShift", "barProgress", "dotCount"):
            self.assertNotIn(keyframe, components)

    def test_the_loading_line_bar_is_kept_and_reports_real_progress(self):
        components = text(UI / "Components.kt")
        self.assertIn("fun LoadingScreen(title: String, detail: String, progress: Float? = null)", components)
        self.assertIn("fillMaxWidth(fraction)", components)
        self.assertIn("LoadingScreen(", text(UI / "AppRoot.kt"))
        self.assertIn("progress = loadProgress", text(UI / "AppRoot.kt"))
        self.assertIn("loadProgress", text(DATA / "TvRepository.kt"))

    def test_the_mac_splash_is_still_and_keeps_the_bar(self):
        html = text(MAC_RENDERER / "index.html")
        css = text(MAC_RENDERER / "app.css")
        self.assertNotIn("splash-spinner", html)
        self.assertNotIn("splash-dots", html)
        self.assertIn('class="splash-bar"', html)
        self.assertIn('class="splash-bar-fill"', html)
        self.assertNotIn("@keyframes splash-", css)


class CategoryRailTests(unittest.TestCase):
    def test_channels_tab_is_a_rail_beside_the_channel_pane(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn("private fun CategoryRail(", home)
        self.assertIn("private fun CategoryListRow(", home)
        self.assertIn('name = "All channels"', home)
        self.assertIn("PaneHeader(", home)
        # The old full-page category list is gone; the rail is always in reach.
        self.assertNotIn("CategoryPageScreen(", home)
        self.assertNotIn("CategoryListScreen(", home)

    def test_search_is_library_wide_and_each_pane_sorts_itself(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn('"Sort · ${channelSort.label}"', home)
        self.assertIn('"⇅ ${sort.label}"', home)


class VersionTests(unittest.TestCase):
    def test_every_surface_agrees_on_1_1_0(self):
        gradle = text(ROOT / "android/app/build.gradle.kts")
        self.assertIn('orElse("1.1.0")', gradle)
        self.assertIn('orElse("101000000")', gradle)
        builder = text(ROOT / "android/tools/build_bundle.py")
        self.assertIn('DEFAULT_VERSION = "1.1.0"', builder)
        self.assertEqual(
            __import__("json").loads(text(ROOT / "macos/app/package.json"))["version"], "1.1.0")
        self.assertIn("PremiumTV 1.1.0", text(ROOT / "release-notes-1.1.0.md"))

    def test_the_notice_never_blocks_the_new_stable(self):
        document = __import__("json").loads(text(ROOT / "app-update-notice.json"))
        rules = {rule["id"]: rule for rule in document["rules"]}
        blocked = rules["retired-preview-1-1"]
        self.assertEqual((blocked["min_version"], blocked["max_version"]), ("1.1.1", "1.1.1"))
        stable = rules["update-below-newest"]
        self.assertEqual(stable["max_version"], "1.0.9")

    def test_version_code_is_above_every_published_build(self):
        source = text(ROOT / "scripts/release_version.py")
        self.assertIn("MAJOR_SCALE = 100_000_000", source)
        self.assertIn("1.1.0\" ->", source.replace("``1.1.0`` ->", "1.1.0\" ->"))


if __name__ == "__main__":
    unittest.main()


class ComposableAnnotationTests(unittest.TestCase):
    """A dropped @Composable is a compile error the offline suite can catch.

    1.1.0 rewrote most of the loading screen; while doing so the annotation on
    `LoadErrorScreen` went missing and only the Gradle build noticed. Compose
    composables are capitalised and plain helpers are not, so the convention is
    enough to pin the annotation offline.
    """

    def test_every_capitalised_ui_function_is_composable(self):
        pattern = re.compile(r"^fun ([A-Z]\w*)\(", re.MULTILINE)
        checked = 0
        for path in sorted(UI.glob("*.kt")):
            source = text(path)
            for match in pattern.finditer(source):
                before = source[:match.start()].rstrip().splitlines()
                self.assertTrue(
                    before and before[-1].strip() == "@Composable",
                    f"{path.name}: fun {match.group(1)}() is capitalised but has no @Composable",
                )
                checked += 1
        self.assertGreater(checked, 10, "the scan must actually see the UI composables")


class SidePanelReachabilityTests(unittest.TestCase):
    """The dock's buttons must survive a 720p TV, where the panel is short."""

    def test_the_side_panel_details_scroll_instead_of_clipping(self):
        player = text(UI / "PlayerScreen.kt")
        self.assertIn("modifier = Modifier.weight(1f),\n                    channel = channel,", player)
        self.assertIn("verticalScroll(rememberScrollState())", player)


class UpdateGateTests(unittest.TestCase):
    """A stale published notice must not wedge the emulator gate."""

    def test_the_gate_dismisses_a_retired_build_popup(self):
        gate = text(ROOT / "android/tools/smoke_apk.py")
        self.assertIn('"BUILD RETIRED"', gate)
        self.assertIn("DEFAULT_DISMISS_LABELS", gate)
