"""Tests for the download-site data generator (scripts/build_site_data.py)."""
import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import build_site_data  # noqa: E402


class BuildSiteDataTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload, cls.changelog = build_site_data.build_payload()

    def test_every_country_playlist_is_listed_with_its_count(self):
        files = {p.stem for p in (ROOT / "playlists" / "countries").glob("*.m3u")}
        listed = {c["slug"] for c in self.payload["countries"]}
        self.assertEqual(files, listed)
        for c in self.payload["countries"]:
            self.assertGreater(c["count"], 0, c["slug"])
            self.assertTrue(c["playlist_url"].endswith(f"/{c['slug']}.m3u"))
            self.assertIn(c["epg_url"], c["playlist_url"].replace("playlists/countries", "EPG")
                          .replace(".m3u", ".xml"))

    def test_special_regions_have_no_iso_code_but_countries_do(self):
        by_slug = {c["slug"]: c for c in self.payload["countries"]}
        self.assertIsNone(by_slug["International"]["iso2"])
        self.assertTrue(by_slug["International"]["region"])
        self.assertEqual(by_slug["USA"]["iso2"], "US")
        self.assertEqual(by_slug["UK"]["iso2"], "GB")
        self.assertFalse(by_slug["USA"]["region"])

    def test_release_channels_carry_download_assets(self):
        channels = self.payload["apps"]["channels"]
        self.assertGreaterEqual(len(channels), 2)
        kinds = set()
        for ch in channels:
            self.assertTrue(ch["assets"], ch["id"])
            for asset in ch["assets"]:
                self.assertTrue(asset["url"].startswith("https://github.com/"), asset["name"])
                self.assertGreater(asset["size"], 0, asset["name"])
                kinds.add(asset["kind"])
        self.assertIn("android", kinds)
        self.assertIn("macos-dmg", kinds)

    def test_changelog_parses_dated_headings_newest_first(self):
        self.assertGreaterEqual(len(self.changelog), 1)
        dates = [e["date"] for e in self.changelog]
        self.assertEqual(dates, sorted(dates, reverse=True))
        for entry in self.changelog:
            self.assertRegex(entry["date"], r"^\d{4}-\d{2}-\d{2}$")
            self.assertTrue(entry["title"])

    def test_feed_is_valid_atom_with_an_entry_per_changelog_item(self):
        xml = build_site_data.write_feed(self.changelog)
        root = ET.fromstring(xml)
        ns = {"a": "http://www.w3.org/2005/Atom"}
        entries = root.findall("a:entry", ns)
        self.assertEqual(len(entries), len(self.changelog))
        ids = [e.findtext("a:id", "", ns) for e in entries]
        self.assertEqual(len(ids), len(set(ids)), "feed ids must be unique")

    def test_site_data_js_wraps_the_payload(self):
        text = build_site_data.render_site_data_js(self.payload)
        self.assertTrue(text.startswith("/*"))
        self.assertIn("window.SITE_DATA = ", text)
        self.assertTrue(text.rstrip().endswith("};"))


if __name__ == "__main__":
    unittest.main()
