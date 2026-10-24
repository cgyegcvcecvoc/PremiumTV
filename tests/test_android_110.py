"""Offline regression checks for the 1.1.0 UI contracts.

These are source-level assertions on purpose. The Kotlin UI cannot be compiled
in this repository's offline suite (no JDK, no Android SDK), so the promises a
release makes about its own screens are pinned here: the docked side player,
the category rail, the amber pointer ring, the automatic server backup, the
dead-channel filter and the still loading screen. The Gradle unit tests and the
emulator smoke gate in android-build.yml prove the rest.
"""

from pathlib import Path
import json
import re
import subprocess
import sys
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
    def test_every_surface_reads_the_one_version_file(self):
        current = text(ROOT / "VERSION").strip()
        gradle = text(ROOT / "android/app/build.gradle.kts")
        # The Gradle default comes from the generated properties, not a literal.
        self.assertIn('rootProject.file("version.properties")', gradle)
        self.assertIn('generatedVersion.getProperty("version"', gradle)
        self.assertIn('generatedVersion.getProperty("versionCode"', gradle)
        self.assertNotIn('orElse("1.1.', gradle)
        builder = text(ROOT / "android/tools/build_bundle.py")
        self.assertIn("DEFAULT_VERSION = release_version.current_version()", builder)
        self.assertEqual(
            __import__("json").loads(text(ROOT / "macos/app/package.json"))["version"], current)
        self.assertIn(f"PremiumTV {current}", text(ROOT / f"release-notes-{current}.md"))

    def test_the_notice_never_blocks_the_new_stable(self):
        document = __import__("json").loads(text(ROOT / "app-update-notice.json"))
        rules = {rule["id"]: rule for rule in document["rules"]}
        # The retired-preview rule is gone: 1.1.1 is the stable release, and a
        # stable release cannot be blocked by a notice rule matching itself.
        self.assertNotIn("retired-preview-1-1", rules)
        # Every build below the newest stable is nudged toward it.
        stable = rules["update-below-newest"]
        self.assertEqual((stable["min_version"], stable["max_version"]), ("1.0.4", "1.1.1"))
        self.assertEqual(stable["level"], "warning")

    def test_version_code_is_above_every_published_build(self):
        source = text(ROOT / "scripts/release_version.py")
        self.assertIn("MAJOR_SCALE = 100_000_000", source)
        self.assertIn("1.1.2\" ->", source.replace("``1.1.2`` ->", "1.1.2\" ->"))
        self.assertIn("def current_version()", source)


class LiveEvents111Tests(unittest.TestCase):
    """1.1.1: official team crests, "Not live yet" countdowns, Movies & Shows."""

    def test_live_events_carries_team_crests_and_kickoff_times(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn("private fun TeamLogo(", home)
        self.assertIn("VodShelfScreen(", home)
        self.assertIn("countdownText(", home)
        self.assertIn("kickoffTime(", home)
        live = text(UI / "LiveEvents.kt")
        self.assertIn("val kickoffUtc: Long? = null", live)
        self.assertIn("internal fun parseKickoff", live)
        self.assertIn("internal fun secondsUntilKickoff", live)

    def test_group_live_events_merges_duplicate_feeds_and_annotates_kickoffs(self):
        live = text(UI / "LiveEvents.kt")
        self.assertIn("schedule: Map<String, Long> = emptyMap()", live)
        self.assertIn("val teams = listOf(teamKey(home), teamKey(away)).sorted()", live)
        self.assertIn('"${normKey(sport)}|${teams[0]}|${teams[1]}"', live)
        self.assertIn("event.copy(servers = servers.getValue(key).toList(), kickoffUtc = schedule[key])", live)

    def test_home_screen_switches_to_the_movies_tab(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn('Movies("Movies & Shows")', home)
        self.assertIn("HomeTab.Movies -> VodShelfScreen(", home)
        self.assertIn("onWatch = { onSelect(it.asChannel()) }", home)

    def test_the_bundle_ships_team_crests_and_the_schedule(self):
        builder = text(ROOT / "android/tools/build_bundle.py")
        self.assertIn('os.path.join(REPO_ROOT, "playlists", "team-logos.json")', builder)
        self.assertIn('os.path.join(REPO_ROOT, "playlists", "live-schedule.json")', builder)
        self.assertIn("meta_extra[key] = data", builder)
        self.assertIn("meta.update(meta_extra)", builder)

    def test_the_live_data_files_exist_and_parse(self):
        logos = json.loads(text(ROOT / "playlists/team-logos.json"))
        self.assertEqual(logos["schema"], 1)
        self.assertTrue(logos["logos"], "team logos must not be empty")
        schedule = json.loads(text(ROOT / "playlists/live-schedule.json"))
        self.assertEqual(schedule["schema"], 1)
        self.assertTrue(schedule["games"], "the schedule must list games")
        keys = [g["key"] for g in schedule["games"]]
        self.assertEqual(len(keys), len(set(keys)), "schedule keys must be unique")
        # A kickoff is optional: the curated table only covers a few
        # competitions, and a matchday with none of them published legitimately
        # ships no countdowns. Every kickoff that *is* published must be a real
        # UTC instant, though - a malformed one would break the countdown.
        for game in schedule["games"]:
            kickoff = game.get("kickoff_utc")
            if kickoff is not None:
                self.assertRegex(kickoff, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_the_schedule_describes_the_published_playlist(self):
        # The bundle bakes this file, so a stale key would ship a ghost game.
        schedule = json.loads(text(ROOT / "playlists/live-schedule.json"))
        sys.path.insert(0, str(ROOT / "scripts"))
        import build_live_schedule
        events = build_live_schedule.parse_events(
            text(ROOT / "playlists/PremiumTV.m3u")
        )
        self.assertEqual(
            sorted(g["key"] for g in schedule["games"]),
            sorted({event["key"] for event in events}),
            "live-schedule.json must be regenerated after the playlist changes",
        )

    def test_the_data_workflows_rebuild_the_schedule_they_publish(self):
        """A playlist change must never leave the schedule behind again.

        No workflow ran `build_live_schedule.py`, so every scrape that added or
        removed a live-game feed left `playlists/live-schedule.json` stale; the
        next data run then died in `Run offline tests` (this test's sibling),
        and since the tests run before the scrape nothing could repair it -
        three scrapes and four quick updates failed that way on 2026-10-23/24
        and no channel was re-verified. Each publishing workflow now rebuilds
        it once before the tests (self-heal) and once after the playlists are
        rewritten (publish), before it commits.
        """
        for name in ("scrape.yml", "quick-update.yml", "link-check.yml"):
            workflow = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
            self.assertGreaterEqual(
                workflow.count("python3 scripts/build_live_schedule.py"), 2,
                f"{name} must rebuild the schedule before the tests and before the commit",
            )
            self.assertLess(
                workflow.index("build_live_schedule.py"), workflow.index("unittest discover"),
                f"{name}: the self-heal pass has to run before the offline suite",
            )
            self.assertLess(
                workflow.index("Rebuild the Live Events schedule"), workflow.index("git commit"),
                f"{name}: the schedule has to be rebuilt before the run commits",
            )

    def test_the_live_schedule_generator_is_deterministic(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import build_live_schedule
        events = build_live_schedule.parse_events(
            text(ROOT / "playlists/PremiumTV.m3u")
        )
        first = build_live_schedule.assign_kickoffs(events, reference_date="2026-10-23")
        second = build_live_schedule.assign_kickoffs(events, reference_date="2026-10-23")
        self.assertEqual(first, second, "the schedule generator must be deterministic")

    def test_curated_slots_still_produce_a_countdown(self):
        # The countdown itself stays covered even when the current matchday
        # publishes only competitions the table has no slots for.
        sys.path.insert(0, str(ROOT / "scripts"))
        import build_live_schedule
        events = [{
            "sport": "Soccer",
            "league": "UEFA Conference League",
            "home": "A",
            "away": "B",
            "title": "A vs. B",
            "key": "soccer|a|b",
        }]
        games = build_live_schedule.assign_kickoffs(events, reference_date="2026-10-23")
        self.assertEqual(games[0]["kickoff_utc"], "2026-10-23T16:45:00Z")

    def test_the_apps_open_the_files_under_the_names_the_bundle_writes(self):
        # The bundle writes the repository's hyphenated file name beside the
        # channel list; both apps must read exactly that name, and the Mac
        # renderer must flatten the documents held in meta.json.
        builder = text(ROOT / "android/tools/build_bundle.py")
        self.assertIn("shutil.copyfile(source_path, os.path.join(out_dir, name))", builder)
        home = text(UI / "HomeScreen.kt")
        self.assertIn('readAsset("team-logos.json")', home)
        self.assertIn('readAsset("live-schedule.json")', home)
        renderer = text(MAC_RENDERER / "app.js")
        self.assertIn("meta.team_logos", renderer)
        self.assertIn("scheduleDoc.games", renderer)


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
