"""Offline tests for the local-channel directory (scripts/build_local_channels.py)."""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_local_channels  # noqa: E402


class LocalChannelDirectoryTest(unittest.TestCase):
    def setUp(self):
        self.document = build_local_channels.build()

    def test_published_affiliates_carry_a_market_and_a_callsign(self):
        stations = {
            station["callsign"]: (state["code"], market["city"])
            for state in self.document["states"]
            for market in state["markets"]
            for station in market["stations"]
        }
        self.assertEqual(stations.get("WGAL"), ("PA", "Lancaster"))
        self.assertEqual(stations.get("KTNV"), ("NV", "Las Vegas"))
        for callsign, (_state, city) in stations.items():
            self.assertTrue(callsign)
            self.assertTrue(city)
            self.assertNotRegex(city, r"^(ABC|CBS|NBC|FOX|PBS) ")

    def test_zip_ranges_cover_every_state_and_include_the_user_market(self):
        states = {state["code"] for state in self.document["states"]}
        mapped = {entry[2] for entry in self.document["zip_ranges"]}
        self.assertTrue(states.issubset(mapped))
        pa = [entry for entry in self.document["zip_ranges"] if entry[2] == "PA"][0]
        self.assertTrue(pa[0] <= "176" <= pa[1], "ZIP 17603 (Lancaster) must map to PA")

    def test_station_entries_carry_the_identity_the_apps_match(self):
        station = next(
            station
            for state in self.document["states"]
            for market in state["markets"]
            for station in market["stations"]
            if station["callsign"] == "WGAL"
        )
        self.assertEqual(station["channel_id"], "NBC.us@WGAL")
        self.assertTrue(station["url"].startswith("http"))
        self.assertIsInstance(station["backup_urls"], list)

    def test_the_committed_document_matches_the_published_playlist(self):
        path = ROOT / "playlists" / "local-channels.json"
        self.assertTrue(path.is_file())
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            {key: value for key, value in committed.items() if key != "generated_utc"},
            {key: value for key, value in self.document.items() if key != "generated_utc"},
            "run python scripts/build_local_channels.py after changing the playlist",
        )


if __name__ == "__main__":
    unittest.main()
