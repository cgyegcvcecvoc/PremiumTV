"""Static integration checks for the Android refresh feature.

The sandbox test suite cannot run Android WorkManager, but these checks guard
the contracts most likely to drift: the in-app slots must mirror the repository
publishers, the worker must be persisted/network-constrained, and Settings must
invoke a true manual (validator-bypassing) refresh.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ANDROID = ROOT / "android" / "app" / "src" / "main"
SCHEDULER = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "update" / "AutomaticRefreshScheduler.kt"
WORKER = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "update" / "LibraryRefreshWorker.kt"
REPOSITORY = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "data" / "TvRepository.kt"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def daily_slots(path: Path) -> set[tuple[int, int]]:
    """Return (hour, minute) for every daily `minute hour * * *` cron."""
    return {
        (int(hour), int(minute))
        for minute, hour in re.findall(r'cron:\s*"(\d+)\s+(\d+)\s+\*\s+\*\s+\*"', text(path))
    }


class AndroidRefreshScheduleTests(unittest.TestCase):
    def test_app_slots_match_all_daily_data_publishers(self):
        expected: set[tuple[int, int]] = set()
        for name in ("scrape.yml", "quick-update.yml", "epg-build.yml"):
            expected |= daily_slots(ROOT / ".github" / "workflows" / name)

        source = text(SCHEDULER)
        actual = {
            (int(hour), int(minute))
            for hour, minute in re.findall(r"RefreshSlot\((\d+),\s*(\d+)\)", source)
        }
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 13)

    def test_schedule_uses_repository_timezone_and_publish_grace(self):
        source = text(SCHEDULER)
        self.assertIn('TimeZone.getTimeZone("America/New_York")', source)
        self.assertRegex(source, r"PUBLISHING_GRACE_MINUTES\s*=\s*45")
        self.assertIn("add(Calendar.MINUTE, PUBLISHING_GRACE_MINUTES)", source)

    def test_work_is_persistent_unique_and_network_constrained(self):
        scheduler = text(SCHEDULER)
        worker = text(WORKER)
        self.assertIn("OneTimeWorkRequestBuilder<LibraryRefreshWorker>()", scheduler)
        self.assertIn("NetworkType.CONNECTED", scheduler)
        self.assertIn("ExistingWorkPolicy.KEEP", scheduler)
        self.assertIn("AutomaticRefreshScheduler.scheduleNext(applicationContext)", worker)
        self.assertIn("outcome.retryable", worker)


class AndroidRefreshWiringTests(unittest.TestCase):
    def test_release_version_and_workmanager_dependency(self):
        gradle = text(ROOT / "android" / "app" / "build.gradle.kts")
        self.assertIn('orElse("1.0.4")', gradle)
        self.assertIn('orElse("100000004")', gradle)
        self.assertIn("versionName = premiumTvVersion", gradle)
        self.assertIn("versionCode = premiumTvVersionCode", gradle)
        self.assertIn('androidx.work:work-runtime-ktx:2.9.1', gradle)

        builder = text(ROOT / "android" / "tools" / "build_bundle.py")
        self.assertIn('DEFAULT_SCOPE = "usa"', builder)
        self.assertIn('DEFAULT_VERSION = "1.0.4"', builder)
        for workflow in ("android-build.yml", "macos-build.yml"):
            source = text(ROOT / ".github" / "workflows" / workflow)
            # Versions and scopes are resolved from the tag/channel instead of
            # a hardcoded tag list, so a future release needs no workflow edit.
            self.assertIn("scripts/release_version.py", source)
            self.assertIn("scope=all", source)
            self.assertIn("scope=usa", source)
            self.assertIn("channel=preview", source)
            self.assertIn("github.event.release.prerelease", source)
            self.assertNotIn("v1.1.1:false", source)
            self.assertNotIn("v1.0.3:false", source)
            self.assertNotIn("github.event.release.tag_name ==", source)
        android = text(ROOT / ".github" / "workflows" / "android-build.yml")
        self.assertIn('code=$(python3 scripts/release_version.py --code "$version")', android)
        self.assertIn("RELEASE_TAG=v$version", android)

    def test_boot_permission_and_application_scheduler(self):
        manifest = text(ANDROID / "AndroidManifest.xml")
        application = text(
            ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "PremiumTvApplication.kt"
        )
        self.assertIn("android.permission.RECEIVE_BOOT_COMPLETED", manifest)
        self.assertIn("AutomaticRefreshScheduler.scheduleNext(this)", application)
        self.assertIn("val repository: TvRepository", application)

    def test_settings_force_refresh_bypasses_http_validators(self):
        view_model = text(
            ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "TvViewModel.kt"
        )
        settings = text(
            ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "ui" / "HomeScreen.kt"
        )
        repository = text(REPOSITORY)
        self.assertIn("repository.refresh(RefreshTrigger.Manual)", view_model)
        self.assertIn('"Force refresh all now"', settings)
        self.assertIn("val conditional = !isManual && current.refreshed", repository)

    def test_refresh_streams_the_guide_instead_of_buffering_it(self):
        repository = text(REPOSITORY)
        parser = text(ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "data" / "XmlTvParser.kt")
        self.assertNotIn("downloadText", repository)
        self.assertIn("XmlTvParser.parse(input)", repository)
        self.assertIn("fun parse(input: InputStream, keep:", parser)
        self.assertIn("catch (e: OutOfMemoryError)", repository)

    def test_refresh_is_serialized_conditional_and_atomically_published(self):
        repository = text(REPOSITORY)
        self.assertIn("private val operations = Mutex()", repository)
        self.assertIn('connection.setRequestProperty("If-None-Match"', repository)
        self.assertIn('connection.setRequestProperty("If-Modified-Since"', repository)
        self.assertIn("stagingCacheDir.renameTo(cacheDir)", repository)
        self.assertIn("backupCacheDir.renameTo(cacheDir)", repository)




class AndroidCableGuideWiringTests(unittest.TestCase):
    """The cable-style grid must be the Guide tab of a preview build - not a
    separate tab that a stale download can hide, as happened in 1.1.0."""

    UI = ANDROID / "kotlin" / "com" / "premiumtv" / "app" / "ui"

    def test_guide_tab_is_the_cable_grid_on_preview_builds(self):
        home = text(self.UI / "HomeScreen.kt")
        self.assertIn('val cableGuide = library.meta.previewFeatures.contains("cable-guide")', home)
        self.assertRegex(home, r"HomeTab\.Guide -> if \(cableGuide\) \{\s*CableGuideScreen\(")
        self.assertNotIn('Cable("Cable")', home)
        self.assertIn("KEYCODE_GUIDE", home)

    def test_grid_has_channels_left_times_on_top_and_a_remote_highlight(self):
        guide = text(self.UI / "CableGuide.kt")
        model = text(self.UI / "GuideModel.kt")
        for piece in ("GuideTimeHeader(", "GuideChannelCell(", "GuideProgrammeCell(", "GuideInfoPanel("):
            self.assertIn(piece, guide)
        self.assertIn("moveGuideCursor(model, cursorNow(), move)", guide)
        self.assertIn("focusRequester.requestFocus()", guide)
        self.assertIn("internal const val GUIDE_SLOTS", model)

    def test_tab_and_guide_position_survive_the_player(self):
        root = text(self.UI / "AppRoot.kt")
        self.assertIn("rememberSaveable { mutableStateOf(HomeTab.Channels) }", root)
        self.assertIn("rememberCableGuideState()", root)

    def test_a_cache_from_another_build_cannot_hide_the_new_bundle(self):
        repository = text(REPOSITORY)
        self.assertIn("discardCacheFromAnotherBuild()", repository)
        self.assertIn("cached.version == bundle.version && cached.libraryScope == bundle.libraryScope", repository)
        # The repository is public: refresh errors must not blame a private repo.
        self.assertNotIn("Private GitHub raw files", repository)
        self.assertNotIn("repository is private", text(self.UI / "HomeScreen.kt"))


if __name__ == "__main__":
    unittest.main()
