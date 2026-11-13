"""1.1.5: remote-first speed, a calmer loading screen, and the sleep timer.

The Kotlin UI cannot be compiled by the offline suite, so these source-level
contracts pin the behaviours the release promises. The Gradle unit suite and the
emulator gate cover the rest.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UI = ROOT / "android/app/src/main/kotlin/com/premiumtv/app/ui"
sys.path.insert(0, str(ROOT / "scripts"))


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class Version115Tests(unittest.TestCase):
    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        self.assertGreaterEqual(release_version.compare_versions(release_version.current_version(), "1.1.5"), 0)
        self.assertEqual(release_version.android_version_code("1.1.5"), 101_050_000)
        self.assertEqual(version_sync.check(), [])

        notice = json.loads(text(ROOT / "app-update-notice.json"))
        stable = {rule["id"]: rule for rule in notice["rules"]}["update-below-newest"]
        self.assertEqual(stable["max_version"], "1.1.4")
        self.assertIn("1.1.5", stable["surprise"])

        self.assertIn("PremiumTV 1.1.5", text(ROOT / "release-notes-1.1.5.md"))
        self.assertIn("Version 1.1.5", text(ROOT / "CHANGELOG.md"))


class RemoteResponsiveness115Tests(unittest.TestCase):
    def test_focus_lift_is_a_draw_phase_graphics_layer(self):
        components = text(UI / "Components.kt")
        self.assertIn("graphicsLayer {", components)
        self.assertIn("scaleX = scale.value", components)
        self.assertIn("tween(durationMillis = 110", components)
        # The old composition-read modifier is what recomposed every frame.
        self.assertNotIn(".scale(scale)\n", components)

    def test_a_card_has_one_focus_stop_and_hold_ok_favourites(self):
        components = text(UI / "Components.kt")
        self.assertIn("onLongClick = onToggleFavorite", components)
        self.assertIn("TV_LONG_PRESS_MS", components)
        self.assertIn("onLongPress", components)
        # The star stays usable by touch and accessibility but is not focusable.
        self.assertIn('semanticsOnClick(label = "Favorite")', components)
        self.assertNotIn(".size(26.dp)\n                            .focusable()", components)

    def test_focus_groups_keep_dpad_traversal_inside_the_active_shelf(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn("focusGroup()", home)
        self.assertIn("focusRestorer()", home)
        self.assertIn("private fun ChannelGrid(", home)

    def test_the_pointer_ring_follows_its_shape_and_has_contrast(self):
        components = text(UI / "Components.kt")
        self.assertIn(".border(5.dp, Color(0xE605080C), shape)", components)
        self.assertIn(".border(3.dp, FocusRing, shape)", components)
        # A focused selected tab must not be amber-on-gold.
        self.assertIn("selected && !focused -> PremiumGold", components)

    def test_guide_key_repeat_is_coalesced_and_old_scrolls_are_cancelled(self):
        guide = text(UI / "CableGuide.kt")
        self.assertIn("revealJob?.cancel()", guide)
        self.assertIn("revealJob = scope.launch", guide)
        self.assertIn("native.repeatCount > 0", guide)
        self.assertIn("SystemClock.uptimeMillis()", guide)
        self.assertIn("lastMoveAtMs", guide)

    def test_channel_number_entry_does_not_steal_digits_from_active_search(self):
        home = text(UI / "HomeScreen.kt")
        tuner = text(UI / "ChannelNumberTuner.kt")
        self.assertIn("channelNumberCharacterForKey(native.keyCode)", home)
        self.assertIn("if (searchEditing) return@onPreviewKeyEvent false", home)
        self.assertIn("onEditingChanged = { searchEditing = it }", home)
        self.assertIn("fun changeEditing(value: Boolean)", home)
        self.assertIn("BackHandler(enabled = editing)", home)
        self.assertIn("BackHandler(enabled = channelNumber.isNotBlank()", home)
        self.assertIn("KEYCODE_DPAD_RIGHT", home)
        self.assertIn("CHANNEL_NUMBER_ENTRY_DELAY_MS", home)
        self.assertIn("findChannelByNumber(currentChannels.value, number)", home)
        self.assertIn("Press OK to tune now, or wait a moment", home)
        self.assertIn("Search · remote digits tune", home)
        self.assertIn("KeyEvent.KEYCODE_9", tuner)
        self.assertIn("KeyEvent.KEYCODE_PERIOD", tuner)
        self.assertIn("stripTrailingZeros()", tuner)
        self.assertIn("firstOrNull", tuner)
        self.assertIn("channelNumberCharacterForKey", text(
            ROOT / "android/app/src/test/kotlin/com/premiumtv/app/ui/ChannelNumberTunerTest.kt"
        ))


class RenderAndMemory115Tests(unittest.TestCase):
    def test_live_playback_does_not_poll_the_vod_clock(self):
        player = text(UI / "PlayerScreen.kt")
        self.assertIn("if (!isVodItem) return@LaunchedEffect", player)

    def test_player_lifecycle_observer_tracks_the_active_channel(self):
        player = text(UI / "PlayerScreen.kt")
        self.assertIn(
            "DisposableEffect(player, lifecycleOwner, channel.id, channel.url, isVodItem)",
            player,
        )
        self.assertIn("saveVodPositionMs(context, channel.id, player.currentPosition, durationMs)", player)

    def test_live_events_only_ticks_fast_for_a_visible_countdown(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn("delay(if (countdownVisible) 1_000L else 30_000L)", home)
        self.assertIn("remember(sections, feedStatus, now / 60)", home)

    def test_the_guide_does_not_rebuild_its_entries_every_minute(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn(
            "val entries = remember(library.channels, library.programmes, liveIndex)",
            home,
        )

    def test_the_logo_cache_is_bounded(self):
        app = text(ROOT / "android/app/src/main/kotlin/com/premiumtv/app/PremiumTvApplication.kt")
        self.assertIn("maxSizePercent(0.10)", app)

    def test_personal_shelves_are_memoised(self):
        root = text(UI / "AppRoot.kt")
        self.assertIn("val favoriteUrlSet = remember(favoriteKeys)", root)
        self.assertIn("val recentShelf = remember(recentKeys", root)


class LoadingScreen115Tests(unittest.TestCase):
    def test_the_loading_screen_uses_real_progress_without_a_background_ticker(self):
        components = text(UI / "Components.kt")
        loading = components.split("fun LoadingScreen(", 1)[1].split("fun LoadErrorScreen(", 1)[0]
        self.assertNotIn("stageTrickle", loading)
        self.assertIn("fillMaxWidth(fraction)", loading)
        self.assertNotIn("sweepOffset", loading)
        self.assertNotIn("LaunchedEffect(", loading)

    def test_the_rotating_tip_is_not_part_of_the_startup_screen(self):
        components = text(UI / "Components.kt")
        loading = components.split("fun LoadingScreen(", 1)[1].split("fun LoadErrorScreen(", 1)[0]
        self.assertNotIn("LoadingTip()", loading)


class SleepTimer115Tests(unittest.TestCase):
    def test_the_timer_is_persisted_and_owned_by_the_root(self):
        sleep = text(UI / "SleepTimer.kt")
        self.assertIn("SLEEP_TIMER_ENDS_AT", sleep)
        self.assertIn("System.currentTimeMillis() + minutes * 60_000L", sleep)
        self.assertIn("internal fun sleepTimerLabel", sleep)
        root = text(UI / "AppRoot.kt")
        self.assertIn("SleepTimer(appContext)", root)
        self.assertIn("LaunchedEffect(sleepTimerEndsAt)", root)
        self.assertIn("SleepTimerEndedBanner(", root)

    def test_settings_exposes_the_timer(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn("SleepTimerCard(", home)
        self.assertIn("sleepTimerEndsAt = sleepTimerEndsAt", home)
        self.assertIn("onSetSleepTimer = onSetSleepTimer", home)

    def test_the_label_policy_has_a_jvm_test(self):
        test = text(ROOT / "android/app/src/test/kotlin/com/premiumtv/app/ui/SleepTimerTest.kt")
        self.assertIn("sleepTimerLabel(", test)
        self.assertIn("SLEEP_TIMER_CHOICES", test)


class Layout115Tests(unittest.TestCase):
    def test_the_browser_respects_the_safe_area_but_the_player_does_not(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn("windowInsetsPadding(WindowInsets.safeDrawing)", home)
        player = text(UI / "PlayerScreen.kt")
        self.assertNotIn("windowInsetsPadding", player)

    def test_settings_rows_stack_on_a_narrow_window(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn("maxWidth < 420.dp", home)


if __name__ == "__main__":
    unittest.main()
