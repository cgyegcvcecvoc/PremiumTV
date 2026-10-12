"""Offline tests for the curated upstream guide list (scripts/epg_sources.py)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import epg_sources  # noqa: E402


class CountryCodeTest(unittest.TestCase):
    def test_names_and_codes_resolve_to_iso(self):
        self.assertEqual(epg_sources.country_code("USA"), "us")
        self.assertEqual(epg_sources.country_code("US"), "us")
        self.assertEqual(epg_sources.country_code("us"), "us")
        self.assertEqual(epg_sources.country_code("UK"), "gb")
        self.assertEqual(epg_sources.country_code("United Kingdom"), "gb")
        self.assertEqual(epg_sources.country_code("South Korea"), "kr")
        self.assertEqual(epg_sources.country_code("DR Congo"), "cd")
        self.assertEqual(epg_sources.country_code("Antigua and Barbuda"), "ag")

    def test_pseudo_regions_have_no_code(self):
        self.assertEqual(epg_sources.country_code("International"), "")
        self.assertEqual(epg_sources.country_code("Arab World"), "")
        self.assertEqual(epg_sources.country_code("Latin America"), "")
        self.assertEqual(epg_sources.country_code(""), "")

    def test_norm_cc_unifies_uk_and_gb(self):
        self.assertEqual(epg_sources.norm_cc("uk"), "gb")
        self.assertEqual(epg_sources.norm_cc("UK"), "gb")
        self.assertEqual(epg_sources.norm_cc("us"), "us")

    def test_guide_url_country_reads_per_country_file_names(self):
        self.assertEqual(epg_sources.guide_url_country(
            "https://epg.pw/xmltv/epg_DE.xml.gz"), "de")
        self.assertEqual(epg_sources.guide_url_country(
            "https://iptv-epg.org/files/epg-us.xml.gz"), "us")
        self.assertEqual(epg_sources.guide_url_country(
            "https://iptv-epg.org/files/epg-uk.xml.gz"), "gb")
        self.assertEqual(epg_sources.guide_url_country(
            "https://epg.pw/xmltv/epg.xml.gz"), "")
        self.assertEqual(epg_sources.guide_url_country(
            "https://example.com/guide.xml.gz"), "")
        self.assertEqual(epg_sources.guide_url_country(""), "")


class TemplateTest(unittest.TestCase):
    def test_expand_template_handles_both_cases(self):
        self.assertEqual(
            epg_sources.expand_template("https://epg.pw/xmltv/epg_{CC}.xml.gz", "gb"),
            "https://epg.pw/xmltv/epg_GB.xml.gz")
        self.assertEqual(
            epg_sources.expand_template("https://iptv-epg.org/files/epg-{cc}.xml.gz", "US"),
            "https://iptv-epg.org/files/epg-us.xml.gz")

    def test_configured_urls_are_ordered_and_deduped(self):
        config = {
            "fixed": [
                {"name": "all", "url": "https://feeds.example/all.xml.gz", "enabled": True},
                {"name": "us", "url": "https://feeds.example/us.xml.gz", "enabled": True},
                {"name": "off", "url": "https://feeds.example/off.xml.gz", "enabled": False},
            ],
            "per_country": [
                {"name": "per", "url_template": "https://feeds.example/{cc}.xml.gz",
                 "enabled": True},
            ],
        }
        entries = epg_sources.configured_urls(config, ["us", "de"])
        urls = [entry["url"] for entry in entries]
        self.assertEqual(urls, ["https://feeds.example/all.xml.gz",
                                "https://feeds.example/us.xml.gz",
                                "https://feeds.example/de.xml.gz"])

    def test_disabled_block_or_templates_produce_nothing(self):
        self.assertEqual(epg_sources.configured_urls(
            {"per_country": [{"name": "x", "url_template": "https://a/{cc}.xml",
                              "enabled": False}]}, ["us"]), [])
        self.assertEqual(epg_sources.curated_guides(
            Path("/nonexistent"), {"enabled": False,
                                   "fixed": [{"name": "x", "url": "https://a/x.xml"}]}), [])


class PublishedCountriesTest(unittest.TestCase):
    def test_country_playlists_become_codes_in_stable_order(self):
        with tempfile.TemporaryDirectory() as temp:
            countries = Path(temp)
            for stem in ("USA", "UK", "South_Korea", "International",
                         "Antigua_and_Barbuda"):
                (countries / f"{stem}.m3u").write_text("#EXTM3U\n", encoding="utf-8")
            codes = epg_sources.published_country_codes(countries)
        self.assertEqual(codes, ["ag", "kr", "gb", "us"])
        self.assertEqual(epg_sources.published_country_codes(Path("/nonexistent")), [])

    def test_real_country_shelf_covers_every_iso_country(self):
        codes = epg_sources.published_country_codes(
            Path(__file__).resolve().parents[1] / "playlists" / "countries")
        self.assertIn("us", codes)
        self.assertIn("gb", codes)
        self.assertGreater(len(codes), 150)
        self.assertNotIn("", codes)

    def test_repo_sources_json_produces_the_two_curated_families(self):
        entries = epg_sources.curated_guides(
            Path(__file__).resolve().parents[1] / "playlists" / "countries")
        urls = [entry["url"] for entry in entries]
        # The two user-facing picks are always in the list.
        self.assertIn("https://iptv-epg.org/files/epg-us.xml.gz", urls)
        self.assertIn("https://epg.pw/xmltv/epg.xml.gz", urls)
        self.assertIn("https://epg.pw/xmltv/epg_US.xml.gz", urls)
        # Every URL is unique and https.
        self.assertEqual(len(urls), len(set(urls)))
        self.assertTrue(all(url.startswith("https://") for url in urls))
        # The fixed feeds come before the per-country expansion.
        self.assertLess(urls.index("https://epg.pw/xmltv/epg.xml.gz"),
                        urls.index("https://iptv-epg.org/files/epg-af.xml.gz"))


class SourcesJsonTest(unittest.TestCase):
    def test_sources_json_still_parses_and_carries_epg_sources(self):
        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "sources.json").read_text(encoding="utf-8"))
        block = data["epg_sources"]
        self.assertTrue(block["enabled"])
        self.assertTrue(any("iptv-epg.org" in item.get("url", "")
                            for item in block["fixed"]))
        self.assertTrue(any("epg.pw" in item.get("url_template", "")
                            for item in block["per_country"]))


if __name__ == "__main__":
    unittest.main()
