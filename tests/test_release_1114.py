"""1.1.14 contracts: the crash record is kept, shown in Settings and clearable.

The reported 1.1.12 crashes had no signature anywhere: 1.1.12 started writing
``last-crash.txt`` but nothing read it, and app-private storage cannot be
reached from the UI. These tests pin the plumbing that turns the next crash into
something a viewer can quote, on both apps, without any upload.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))


def text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Version1114PlumbingTests(unittest.TestCase):
    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        self.assertEqual(release_version.current_version(), "1.1.14")
        self.assertEqual(release_version.android_version_code("1.1.14"), 101_140_000)
        self.assertEqual(version_sync.check(), [])
        self.assertEqual(version_sync.PUBLISHED_VERSION, "1.1.14")

        notes = text("release-notes-1.1.14.md")
        self.assertIn("# PremiumTV 1.1.14 — Crash diagnostics and hardened sources", notes)
        self.assertIn("versionCode `101140000`", notes)
        self.assertIn("Version 1.1.14 prepared: crash diagnostics", text("CHANGELOG.md"))

    def test_the_update_notice_moves_to_the_new_release(self):
        notice = json.loads(text("app-update-notice.json"))
        rule = next(r for r in notice["rules"] if r["id"] == "update-below-newest")
        self.assertEqual(rule["max_version"], "1.1.13")
        self.assertIn("1.1.14", rule["surprise"])


class AndroidCrashRecordTests(unittest.TestCase):
    def test_the_record_is_written_and_read_through_one_module(self):
        module = text("android/app/src/main/kotlin/com/premiumtv/app/update/CrashLog.kt")
        for needle in (
            "object CrashLog",
            "const val FILE_NAME",
            "fun write(",
            "fun read(",
            "fun clear(",
            "fun parse(",
        ):
            self.assertIn(needle, module)

    def test_the_application_records_an_uncaught_crash_through_it(self):
        application = text("android/app/src/main/kotlin/com/premiumtv/app/PremiumTvApplication.kt")
        self.assertIn("CrashLog.write(filesDir, thread, throwable)", application)
        self.assertIn("previous?.uncaughtException(thread, throwable)", application)

    def test_settings_shows_and_clears_the_record(self):
        view_model = text("android/app/src/main/kotlin/com/premiumtv/app/TvViewModel.kt")
        self.assertIn("CrashLog.read(getApplication<Application>().filesDir)", view_model)
        self.assertIn("fun clearCrashLog()", view_model)
        self.assertIn("lastCrash = _lastCrash.value", view_model)

        diagnostics = text("android/app/src/main/kotlin/com/premiumtv/app/update/Diagnostics.kt")
        self.assertIn("lastCrash: RecordedCrash? = null", diagnostics)
        self.assertIn('label = "Last crash"', diagnostics)

        screen = text("android/app/src/main/kotlin/com/premiumtv/app/ui/HomeScreen.kt")
        self.assertIn("fun CrashLogCard(", screen)
        self.assertIn('FocusButton("Clear crash log")', screen)
        self.assertIn("if (lastCrash != null)", screen)

        root = text("android/app/src/main/kotlin/com/premiumtv/app/ui/AppRoot.kt")
        self.assertIn("viewModel.lastCrash.collectAsState()", root)
        self.assertIn("viewModel.clearCrashLog()", root)


class MacCrashRecordTests(unittest.TestCase):
    def test_the_module_formats_reads_and_clears(self):
        module = text("macos/app/src/main/crash-log.js")
        for needle in (
            "function formatCrash(",
            "function parseCrash(",
            "function writeCrash(",
            "function readCrash(",
            "function clearCrash(",
            "module.exports",
        ):
            self.assertIn(needle, module)

    def test_the_main_process_records_crashes_and_exposes_the_ipc(self):
        main = text("macos/app/src/main/main.js")
        self.assertIn("require('./crash-log')", main)
        self.assertIn("process.on('uncaughtException'", main)
        self.assertIn("process.on('unhandledRejection'", main)
        self.assertIn("'render-process-gone'", main)
        self.assertIn("ipcMain.handle('ptv:crash-log'", main)
        self.assertIn("ipcMain.handle('ptv:clear-crash-log'", main)

        preload = text("macos/app/src/main/preload.js")
        self.assertIn("crashLog: () => ipcRenderer.invoke('ptv:crash-log')", preload)
        self.assertIn("clearCrashLog: () => ipcRenderer.invoke('ptv:clear-crash-log')", preload)

    def test_the_report_renders_and_clears_it(self):
        renderer = text("macos/app/src/renderer/app.js")
        self.assertIn("await api.crashLog()", renderer)
        self.assertIn("<h2>Last crash</h2>", renderer)
        self.assertIn('id="clear-crash"', renderer)
        self.assertIn("bind('clear-crash', 'click'", renderer)
        self.assertIn("await api.clearCrashLog()", renderer)

    def test_the_record_never_leaves_the_device(self):
        """No crash upload: the modules only touch the local file."""
        for name in ("macos/app/src/main/crash-log.js", "android/app/src/main/kotlin/com/premiumtv/app/update/CrashLog.kt"):
            body = text(name)
            for forbidden in ("http://", "https://", "fetch(", "HttpURLConnection"):
                self.assertNotIn(forbidden, body, f"{name} must not send the record anywhere")


if __name__ == "__main__":
    unittest.main()
