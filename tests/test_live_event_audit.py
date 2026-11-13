"""Offline policy tests for the live-event two-primary-plus-backup audit."""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_live_events as audit  # noqa: E402


def entry(name: str, url: str) -> str:
    return (
        '#EXTINF:-1 tvg-id="Soccer.Dummy.us" group-title="Sports",' + name + "\n" + url + "\n"
    )


class LiveEventReliabilityAuditTest(unittest.TestCase):
    def fixture(self, first_status: str | None = None, third_status: str | None = None,
                duplicate_first: bool = False, *, include_evidence: bool = True,
                exclude_second: bool = False, completed: bool = True):
        first = "https://one.example/live/game.m3u8?token=secret"
        second = "https://edge.two.example.net/live/game.m3u8"
        third = "https://backup.example.org/live/game.m3u8"
        playlist = "#EXTM3U\n" + "".join([
            entry("[Soccer] Alpha vs Beta | English (STRMGATE)", first),
            entry("[Soccer] Beta vs Alpha | Spanish (TVF90)", second),
            entry("[Soccer] Alpha vs. Beta | Backup (FAWA)", third),
            entry("[Soccer] Alpha vs Beta | duplicate mirror name (WEBCAST)", first)
            if duplicate_first else "",
        ])
        report = {
            "run_id": "fixture-run",
            "finished_utc_iso": "2026-11-09T20:00:00Z",
            "checked": True,
            "check_completed": completed,
            "dead": [],
            "unverified": [],
            "retained_links": [],
        }
        if include_evidence:
            checked_urls = [first, third] if exclude_second else [first, second, third]
            report["reachable_event_url_sha256"] = [hashlib.sha256(url.encode()).hexdigest()
                                                       for url in checked_urls]
        if first_status == "unverified":
            report["unverified"].append({"url": audit.scraper.safe_url(first)})
        if third_status == "unverified":
            report["unverified"].append({"url": third})
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            playlist_path = root / "PremiumTV.m3u"
            report_path = root / "report.json"
            sources = root / "sources"
            sources.mkdir()
            playlist_path.write_text(playlist, encoding="utf-8")
            report_path.write_text(json.dumps(report), encoding="utf-8")
            (sources / "source-a.m3u").write_text(
                "#EXTM3U\n" + entry("one", first) + entry("two", second), encoding="utf-8"
            )
            (sources / "source-b.m3u").write_text(
                "#EXTM3U\n" + entry("three", third), encoding="utf-8"
            )
            return audit.audit(playlist_path, report_path, sources)

    def test_three_confirmed_distinct_feeds_assign_two_primaries_and_backup(self):
        report = self.fixture(duplicate_first=True)
        self.assertTrue(report["exact_url_evidence_available"])
        self.assertEqual(report["fixture_count"], 1)
        self.assertEqual(report["compliant_count"], 1)
        game = report["fixtures"][0]
        self.assertEqual(game["feed_count"], 3, "the duplicate URL must not count twice")
        self.assertEqual([feed["role"] for feed in game["feeds"]],
                         ["primary", "primary", "backup"])
        self.assertEqual(game["confirmed_feed_count"], 3)
        self.assertGreaterEqual(len(game["origin_families"]), 2)
        self.assertEqual(game["ingest_sources"], ["source-a", "source-b"])
        self.assertTrue(game["policy_met"])
        self.assertNotIn("secret", json.dumps(report), "reports must not expose stream tokens")

    def test_unverified_third_feed_is_not_claimed_as_a_working_backup(self):
        report = self.fixture(third_status="unverified")
        game = report["fixtures"][0]
        self.assertEqual(game["confirmed_feed_count"], 2)
        self.assertTrue(game["primary_ready"])
        self.assertFalse(game["backup_ready"])
        self.assertFalse(game["policy_met"])
        self.assertIn("needs 1 more confirmed dedicated backup feed(s)", game["deficits"])

    def test_a_dead_declared_primary_cannot_be_relabelled_as_a_ready_backup(self):
        report = self.fixture(first_status="unverified")
        game = report["fixtures"][0]
        self.assertEqual(game["confirmed_feed_count"], 2)
        self.assertEqual(game["confirmed_primary_count"], 1)
        self.assertEqual(game["confirmed_backup_count"], 1)
        self.assertFalse(game["primary_ready"])
        self.assertTrue(game["backup_ready"])
        self.assertFalse(game["policy_met"])
        self.assertIn("needs 1 more confirmed primary feed(s)", game["deficits"])

    def test_legacy_report_never_counts_unknown_urls_as_confirmed(self):
        report = self.fixture(include_evidence=False)
        self.assertTrue(report["health_check_completed"])
        self.assertFalse(report["exact_url_evidence_available"])
        self.assertIn("unavailable (legacy or incomplete scrape)", audit.render(report))
        self.assertEqual(report["fixtures"][0]["confirmed_feed_count"], 0)
        self.assertTrue(all(feed["status"] == "published-not-checked"
                            for feed in report["fixtures"][0]["feeds"]))

    def test_missing_evidence_for_one_url_and_incomplete_run_are_not_reachable(self):
        report = self.fixture(exclude_second=True)
        self.assertEqual(report["fixtures"][0]["confirmed_feed_count"], 2)
        self.assertEqual(report["fixtures"][0]["feeds"][1]["status"], "published-not-checked")
        self.assertEqual(self.fixture(completed=False)["fixtures"][0]["confirmed_feed_count"], 0)

    def test_origin_family_collapses_subdomains_and_preserves_ip_addresses(self):
        self.assertEqual(audit.origin_family("https://a.b.example.com/x"), "example.com")
        self.assertEqual(audit.origin_family("https://cdn.example.co.uk/x"), "example.co.uk")
        self.assertEqual(audit.origin_family("http://193.47.62.44/live"), "193.47.62.44")

    def test_provider_marker_is_extracted_without_treating_quality_as_provider(self):
        self.assertEqual(audit.provider_of("[Soccer] A vs B (STRMGATE)"), "STRMGATE")
        self.assertEqual(audit.provider_of("[Soccer] A vs B (HD)"), "")

    def test_every_playlist_publisher_refreshes_the_reliability_report(self):
        for name in ("scrape.yml", "quick-update.yml", "link-check.yml"):
            workflow = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
            self.assertIn("python3 scripts/audit_live_events.py", workflow, name)


if __name__ == "__main__":
    unittest.main()
