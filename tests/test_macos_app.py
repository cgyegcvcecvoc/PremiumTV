"""Integration checks for the macOS app.

The sandbox cannot run a Mac, but these checks guard the contracts most likely
to drift, in the same spirit as tests/test_android_refresh.py:

  * the in-app refresh slots must mirror the repository publishers;
  * the schedule must use the repository time zone and the publish grace;
  * refresh must be conditional (ETag/Last-Modified) yet manually bypassable,
    serialized and atomically published;
  * the app must declare macOS 12 and an Electron that still runs on it;
  * a macOS runner must produce the .dmg and .pkg.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAC = ROOT / "macos" / "app"
SCHEDULE = MAC / "src" / "main" / "refresh-schedule.js"
REPOSITORY = MAC / "src" / "main" / "repository.js"
BUILDER = MAC / "electron-builder.yml"
PACKAGE = MAC / "package.json"
WORKFLOW = ROOT / ".github" / "workflows" / "macos-build.yml"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def daily_slots(path: Path) -> set[tuple[int, int]]:
    return {
        (int(hour), int(minute))
        for minute, hour in re.findall(r'cron:\s*"(\d+)\s+(\d+)\s+\*\s+\*\s+\*"', text(path))
    }


class MacRefreshScheduleTests(unittest.TestCase):
    def test_app_slots_match_all_daily_data_publishers(self):
        expected: set[tuple[int, int]] = set()
        for name in ("scrape.yml", "quick-update.yml", "epg-build.yml"):
            expected |= daily_slots(ROOT / ".github" / "workflows" / name)

        source = text(SCHEDULE)
        actual = {
            (int(hour), int(minute))
            for hour, minute in re.findall(r"\{\s*hour:\s*(\d+),\s*minute:\s*(\d+)\s*\}", source)
        }
        self.assertEqual(actual, expected)
        self.assertEqual(len(actual), 13)

    def test_schedule_uses_repository_timezone_and_publish_grace(self):
        source = text(SCHEDULE)
        self.assertIn("'America/New_York'", source)
        self.assertRegex(source, r"PUBLISHING_GRACE_MINUTES\s*=\s*45")

    def test_refresh_is_conditional_serialized_and_atomic(self):
        repository = text(REPOSITORY)
        self.assertIn("const conditional = !isManual &&", repository)
        self.assertIn("serialize", repository)
        self.assertIn("If-None-Match", repository)
        self.assertIn("If-Modified-Since", repository)
        self.assertIn("stagingDir", repository)
        self.assertIn("backupDir", repository)
        self.assertIn("await fsp.rename(this.stagingDir, this.cacheDir)", repository)

    def test_settings_force_refresh_and_reset_exist(self):
        renderer = text(MAC / "src" / "renderer" / "app.js")
        self.assertIn("Force refresh", renderer)
        self.assertIn("Reset to bundled copy", renderer)
        self.assertIn("Check for bugs", renderer)
        self.assertIn("runRefresh(true, 'force-refresh')", renderer)
        self.assertIn("runRefresh(false, 'check-now')", renderer)


class MacPackagingTests(unittest.TestCase):
    def test_minimum_system_version_is_macos_12(self):
        self.assertIn('minimumSystemVersion: "12.0"', text(BUILDER))

    def test_electron_is_pinned_to_a_monterey_capable_major(self):
        # Electron 44 dropped macOS 12, so the app must stay on 43 while the
        # supported floor is Monterey.
        electron = json.loads(text(PACKAGE))["devDependencies"]["electron"]
        major = int(re.search(r"(\d+)", electron).group(1))
        self.assertLess(major, 44, "Electron >= 44 cannot run on macOS 12")

    def test_builder_declares_dmg_and_pkg_targets(self):
        builder = text(BUILDER)
        self.assertIn("dmg", builder)
        self.assertIn("pkg:", builder)

    def test_workflow_builds_dmg_and_pkg_on_macos(self):
        workflow = text(WORKFLOW)
        self.assertIn("runs-on: macos", workflow)
        self.assertIn("dmg", workflow)
        self.assertIn("pkg", workflow)


if __name__ == "__main__":
    unittest.main()
