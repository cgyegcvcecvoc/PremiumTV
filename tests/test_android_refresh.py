"""Static integration checks for the Android beta 4 refresh feature.

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
    def test_beta4_version_and_workmanager_dependency(self):
        gradle = text(ROOT / "android" / "app" / "build.gradle.kts")
        self.assertIn('versionName = "1.0.0-beta4"', gradle)
        self.assertRegex(gradle, r"versionCode\s*=\s*4")
        self.assertIn('androidx.work:work-runtime-ktx:2.9.1', gradle)

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

    def test_refresh_is_serialized_conditional_and_atomically_published(self):
        repository = text(REPOSITORY)
        self.assertIn("private val operations = Mutex()", repository)
        self.assertIn('connection.setRequestProperty("If-None-Match"', repository)
        self.assertIn('connection.setRequestProperty("If-Modified-Since"', repository)
        self.assertIn("stagingCacheDir.renameTo(cacheDir)", repository)
        self.assertIn("backupCacheDir.renameTo(cacheDir)", repository)


if __name__ == "__main__":
    unittest.main()
