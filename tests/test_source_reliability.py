"""Offline guardrails for source identity and honest fixture timing."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_live_schedule  # noqa: E402


class SourceReliabilityTests(unittest.TestCase):
    def test_curated_source_fallbacks_use_current_repository(self):
        config = json.loads((ROOT / "sources.json").read_text())
        by_name = {source["name"]: source for source in config["sources"]}
        for name in ("local-channels", "priority-channels", "ae-networks"):
            with self.subTest(name=name):
                source = by_name[name]
                self.assertEqual(source["github"]["repo"], "cgyegcvcecvoc/PremiumTV")
                self.assertIn("/cgyegcvcecvoc/PremiumTV/", source["url"])
                self.assertEqual(source["github"]["path"], source["local_path"])

    def test_known_league_and_duplicates_never_generate_guess(self):
        event = build_live_schedule.parse_event("[UEFA Conference League] Alpha vs Beta")
        duplicate = {**event, "kickoff_utc": "2026-10-22T16:45:00Z"}
        games = build_live_schedule.assign_kickoffs([duplicate, event])
        self.assertEqual(len(games), 1)
        self.assertIsNone(games[0]["kickoff_utc"])
        self.assertEqual(event["title"], games[0]["title"])


if __name__ == "__main__":
    unittest.main()
