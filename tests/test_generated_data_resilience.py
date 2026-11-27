"""Generated data and the workflows that publish it must be able to self-heal.

The 2026-11-19 scheduled failures were not provider failures: a data run
published a changed USA playlist without rebuilding its local-market directory.
The offline suite then raised `KeyError: 'WGAL'` three times, and Pages' web
tests saw Philadelphia/MD instead of Lancaster/PA. The live-schedule generator
also used to write on `--help` and `--check`, and rewrote its timestamp on every
invocation. The published end-of-support date then crossed between scheduled
jobs, leaving the offline suite asserting the warning phase against a frozen
feed. These tests pin the read-only checks, the stable timestamps and the
workflow ordering that repairs stale generated data and the legacy-feed phase
before tests run.
"""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_live_schedule  # noqa: E402

WORKFLOWS = (
    "scrape.yml", "quick-update.yml", "link-check.yml",
    "biweekly-cleanup.yml", "discover.yml", "epg-build.yml",
)
GENERATORS = (
    "python3 scripts/build_live_schedule.py",
    "python3 scripts/build_local_channels.py",
    "python3 scripts/build_site_data.py",
)
CHECKS = (
    "python3 scripts/build_live_schedule.py --check",
    "python3 scripts/build_local_channels.py --check",
    "python3 scripts/build_site_data.py --check",
)
LEGACY_APPLY = "python3 scripts/legacy_sunset.py apply"
LEGACY_CHECK = "python3 scripts/legacy_sunset.py check"


def workflow(name: str) -> str:
    return (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")


class PublishingWorkflowTests(unittest.TestCase):
    def test_every_publishing_workflow_self_heals_before_the_offline_suite(self):
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                text = workflow(name)
                first_test = text.index("unittest discover")
                for generator in GENERATORS:
                    self.assertIn(generator, text)
                    self.assertLess(text.index(generator), first_test,
                                    f"{name}: {generator} must self-heal before tests")
                self.assertIn(LEGACY_APPLY, text)
                self.assertIn(LEGACY_CHECK, text)
                self.assertLess(text.index(LEGACY_APPLY), first_test,
                                f"{name}: the legacy feed must be repaired before tests")
                self.assertLess(text.index(LEGACY_CHECK), first_test,
                                f"{name}: the legacy feed must be checked before tests")

    def test_every_publishing_workflow_regenerates_and_verifies_before_commit(self):
        for name in WORKFLOWS:
            with self.subTest(workflow=name):
                text = workflow(name)
                commit = text.index("git commit")
                self.assertLess(text.index("Rebuild the Live Events schedule"), commit)
                for generator in GENERATORS:
                    self.assertGreaterEqual(
                        text.count(generator), 2,
                        f"{name}: {generator} must run before tests and before commit",
                    )
                for check in CHECKS:
                    self.assertIn(check, text)
                    self.assertLess(text.rindex(check), commit,
                                    f"{name}: {check} must run before commit")
                for generated in (
                    "docs/data/site.json", "docs/data/site-data.js",
                    "docs/data/changelog.json", "docs/data/feed.xml",
                ):
                    self.assertIn(generated, text,
                                  f"{name}: {generated} must be committed with the playlists")

    def test_repository_checks_verify_generated_data_and_the_sunset(self):
        ci = workflow("ci.yml")
        for check in (
            "python scripts/build_live_schedule.py --check",
            "python scripts/build_local_channels.py --check",
            "python scripts/build_site_data.py --check",
            "python scripts/legacy_sunset.py check",
        ):
            self.assertIn(check, ci)
        self.assertLess(ci.index("python scripts/legacy_sunset.py check"),
                        ci.index("unittest discover"))

    def test_pages_rebuilds_local_markets_before_testing_the_web_player(self):
        pages = workflow("pages.yml")
        self.assertIn("python scripts/build_local_channels.py", pages)
        self.assertIn("python scripts/build_local_channels.py --check", pages)
        step = pages.index("Self-heal the local-market directory")
        self.assertLess(step, pages.index("npm test", step))
        self.assertLess(step, pages.index("npm run build", step))
        web = workflow("web-build.yml")
        self.assertIn("../scripts/build_local_channels.py --check", web)
        self.assertLess(web.index("../scripts/build_local_channels.py --check"),
                        web.index("npm test"))

    def test_the_end_of_support_freeze_has_its_own_scheduled_publication(self):
        text = workflow("legacy-sunset.yml")
        self.assertIn('cron: "5 0 20 11 *"', text)
        self.assertIn("python scripts/legacy_sunset.py apply", text)
        self.assertIn("python scripts/legacy_sunset.py check", text)
        self.assertIn("playlists/legacy/USA.m3u", text)
        self.assertIn("[skip ci]", text)


class LiveScheduleGeneratorTests(unittest.TestCase):
    def test_check_is_read_only_and_a_data_identical_rebuild_keeps_its_timestamp(self):
        source = (
            '#EXTM3U\n'
            '#EXTINF:-1 tvg-id="Soccer.Dummy.us" group-title="Sports",'
            '[Soccer] Alpha vs. Beta\n'
            'https://example.com/alpha.m3u8\n'
        )
        with tempfile.TemporaryDirectory(prefix="premiumtv-schedule-") as tmp:
            root = Path(tmp)
            playlist = root / "PremiumTV.m3u"
            out = root / "live-schedule.json"
            playlist.write_text(source, encoding="utf-8")

            self.assertEqual(build_live_schedule.main(
                ["--source", str(playlist), "--out", str(out)]), 0)
            document = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(len(document["games"]), 1)
            document["generated_utc"] = "2000-01-01T00:00:00Z"
            out.write_text(build_live_schedule.render(document), encoding="utf-8")
            before = out.read_bytes()

            # --check must not write, even when the document is stale; here it
            # is current, so it must succeed and leave the bytes untouched.
            self.assertEqual(build_live_schedule.main(
                ["--source", str(playlist), "--out", str(out), "--check"]), 0)
            self.assertEqual(out.read_bytes(), before)
            self.assertEqual(build_live_schedule.main(
                ["--source", str(playlist), "--out", str(out)]), 0)
            self.assertEqual(out.read_bytes(), before)

            # Help must be read-only too; the old generator wrote the schedule.
            with self.assertRaises(SystemExit) as raised:
                build_live_schedule.main(["--help"])
            self.assertEqual(raised.exception.code, 0)
            self.assertEqual(out.read_bytes(), before)

            # A changed playlist is real data drift: the timestamp and game
            # index must both move, so the next committed copy cannot be stale.
            playlist.write_text(source + (
                '#EXTINF:-1 tvg-id="Soccer.Dummy.us" group-title="Sports",'
                '[Soccer] Gamma vs. Delta\n'
                'https://example.com/gamma.m3u8\n'
            ), encoding="utf-8")
            self.assertEqual(build_live_schedule.main(
                ["--source", str(playlist), "--out", str(out)]), 0)
            changed = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(len(changed["games"]), 2)
            self.assertNotEqual(changed["generated_utc"], "2000-01-01T00:00:00Z")

    def test_commas_inside_quoted_competition_names_do_not_hide_fixtures(self):
        text = (
            '#EXTM3U\n'
            '#EXTINF:-1 tvg-id="Live.Event.us" '
            'tvg-name="[FIBA World Cup Qualification, Europe] Poland vs Croatia '
            '(iSTRMEAST)" group-title="Sports",'
            '[FIBA World Cup Qualification, Europe] Poland vs Croatia (iSTRMEAST)\n'
            'https://example.com/poland-croatia.m3u8\n'
        )
        events = build_live_schedule.parse_events(text)
        self.assertEqual(
            [event["key"] for event in events],
            ["fibaworldcupqualificationeurope|croatia|poland"],
        )
        self.assertEqual(events[0]["title"], "Poland vs. Croatia")


if __name__ == "__main__":
    unittest.main()
