"""Offline tests for the local-channel directory (scripts/build_local_channels.py).

The directory is what turns "I am in Lancaster" or "17603" or "PA" into the
published local stations, so these tests pin the promises the feature makes:
a ZIP finds its market, a location fix finds the nearest market, a state lists
what it has, a state without a station says so, and the committed document
matches the tables and the playlist.
"""

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_local_channels  # noqa: E402


class LocalChannelDirectoryTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = build_local_channels.build()
        cls.markets = {market["id"]: market for market in cls.document["markets"]}
        cls.stations = {
            station["callsign"]: (market, station)
            for market in cls.document["markets"]
            for station in market["stations"]
            if station["callsign"]
        }

    # ---------------------------------------------------------------- shape
    def test_the_document_is_schema_two_with_markets(self):
        self.assertEqual(self.document["schema"], 2)
        for key in ("countries", "markets", "states", "zip_ranges", "zip_prefixes",
                    "cities", "market_count", "station_count"):
            self.assertIn(key, self.document, key)
        self.assertEqual(self.document["market_count"], len(self.document["markets"]))
        self.assertEqual(
            self.document["station_count"],
            sum(len(market["stations"]) for market in self.document["markets"]),
        )

    def test_every_market_has_a_place_on_the_map_and_a_state(self):
        states = {state["code"] for state in self.document["states"]}
        for market in self.document["markets"]:
            self.assertIn(market["state"], states)
            self.assertTrue(market["city"])
            self.assertNotEqual((market["latitude"], market["longitude"]), (0.0, 0.0), market["id"])
            self.assertTrue(market["stations"], market["id"])

    def test_a_market_is_not_listed_twice_for_the_same_place(self):
        places = [(market["state"], market["city"].lower()) for market in self.document["markets"]]
        self.assertEqual(len(places), len(set(places)))

    # ------------------------------------------------------------ identity
    def test_published_affiliates_carry_a_market_and_a_callsign(self):
        self.assertEqual(self.stations["WGAL"][0]["state"], "PA")
        self.assertEqual(self.stations["WGAL"][0]["city"], "Lancaster")
        self.assertEqual(self.stations["KTNV"][0]["state"], "NV")
        for callsign, (market, _station) in self.stations.items():
            self.assertRegex(callsign, r"^[KW][A-Z]{2,4}$")
            self.assertTrue(market["city"])
            self.assertNotRegex(market["city"], r"^(ABC|CBS|NBC|FOX|PBS) ")

    def test_a_station_keeps_the_identity_the_apps_match(self):
        _market, station = self.stations["WGAL"]
        self.assertEqual(station["channel_id"], "NBC.us@WGAL")
        self.assertTrue(station["url"].startswith("http"))
        self.assertIsInstance(station["backup_urls"], list)

    def test_a_show_title_is_not_a_callsign(self):
        # "Pluto TV Cars CA", "The Price Is Right CA" and "One Piece CA" read
        # like city/state pairs; none of them is a station.
        for market in self.document["markets"]:
            self.assertNotIn(market["city"], {"Cars", "Anime", "Comedy", "Reality", "Hours"})
            for station in market["stations"]:
                self.assertNotEqual(station["callsign"], "KID")

    # --------------------------------------------------------------- ZIP
    def test_zip_prefixes_cover_the_states_we_publish(self):
        states = {state["code"] for state in self.document["states"]}
        mapped = {row["state"] for row in self.document["zip_prefixes"]}
        self.assertTrue(states.issubset(mapped), states - mapped)
        self.assertEqual(len(self.document["zip_prefixes"]), len({row["prefix"] for row in self.document["zip_prefixes"]}))

    def test_a_zip_finds_its_market(self):
        by_prefix = {row["prefix"]: row for row in self.document["zip_prefixes"]}
        self.assertEqual(by_prefix["176"]["state"], "PA")
        self.assertEqual(by_prefix["176"]["market"], self.stations["WGAL"][0]["id"])
        self.assertEqual(by_prefix["100"]["market"], self.stations["WNYW"][0]["id"])
        self.assertEqual(by_prefix["193"]["market"], self.stations["WTXF"][0]["id"])
        for row in self.document["zip_prefixes"]:
            if row["market"]:
                self.assertIn(row["market"], self.markets)

    def test_military_and_territory_prefixes_are_not_a_state(self):
        prefixes = {row["prefix"] for row in self.document["zip_prefixes"]}
        for prefix in ("090", "091", "340", "962", "969"):
            self.assertNotIn(prefix, prefixes, prefix)

    def test_the_usps_ranges_still_exist_for_simple_players(self):
        pa = [entry for entry in self.document["zip_ranges"] if entry[2] == "PA"][0]
        self.assertTrue(pa[0] <= "176" <= pa[1], "ZIP 17603 (Lancaster) must map to PA")

    # ------------------------------------------------------------- states
    def test_every_state_with_a_market_is_reachable_by_name(self):
        cities = {(row["state"], row["city"]) for row in self.document["cities"]}
        for market in self.document["markets"]:
            self.assertIn((market["state"], market["city"]), cities)

    # ------------------------------------------------- populated document
    def test_the_committed_document_matches_the_tables_and_playlist(self):
        path = ROOT / "playlists" / "local-channels.json"
        self.assertTrue(path.is_file())
        committed = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(
            {key: value for key, value in committed.items() if key != "generated_utc"},
            {key: value for key, value in self.document.items() if key != "generated_utc"},
            "run python scripts/build_local_channels.py after changing the playlist",
        )

    def test_the_reference_tables_are_present_and_documented(self):
        for name in ("us-tv-markets.csv", "us-markets.csv", "us-zip3.csv", "us-places.csv"):
            self.assertTrue((ROOT / "data" / "local-markets" / name).is_file(), name)
        readme = (ROOT / "data" / "local-markets" / "README.md").read_text(encoding="utf-8")
        # The derived tables are openly licensed; the attribution has to stay.
        self.assertIn("public domain", readme)
        self.assertIn("CC BY 4.0", readme)
        self.assertIn("geonames.org", readme)


if __name__ == "__main__":
    unittest.main()
