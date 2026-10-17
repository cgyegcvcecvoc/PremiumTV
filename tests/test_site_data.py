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

    def test_site_promotes_only_a_complete_published_stable_release(self):
        version = "1.0.3"
        assets = [
            {"name": f"PremiumTV-{version}-debug.apk", "size": 100},
            {"name": f"PremiumTV-{version}-mac-arm64.dmg", "size": 100},
            {"name": f"PremiumTV-{version}-mac-arm64.pkg", "size": 100},
            {"name": f"PremiumTV-{version}-mac-x64.dmg", "size": 100},
            {"name": f"PremiumTV-{version}-mac-x64.pkg", "size": 100},
        ]
        api_release = {
            "tag_name": "v1.0.3",
            "prerelease": False,
            "draft": False,
            "assets": assets,
        }
        incomplete = {**api_release, "assets": assets[:1]}
        self.assertIsNone(build_site_data.latest_complete_stable_release([incomplete]))
        self.assertIsNone(build_site_data.latest_complete_stable_release([
            {**api_release, "prerelease": True},
        ]))
        # A fixed fixture must not change meaning when 1.0.3 is published.
        previous = {
            "tag_name": "v1.0.2", "prerelease": False, "draft": False,
            "assets": [{**a, "name": a["name"].replace("1.0.3", "1.0.2")} for a in assets],
        }
        fallback_channels, _ = build_site_data.build_apps({}, [previous, incomplete])
        self.assertEqual(fallback_channels[0]["version"], "1.0.2")
        channels, older = build_site_data.build_apps({}, [api_release])
        self.assertEqual(channels[0]["version"], version)
        self.assertEqual(channels[0]["tag"], "v1.0.3")
        self.assertEqual({asset["name"] for asset in channels[0]["assets"]},
                         {asset["name"] for asset in assets})
        self.assertEqual(older, [])

    def test_release_asset_digest_survives_a_missing_build_out(self):
        version = "1.2.3"
        digest = "a" * 64
        names = [
            f"PremiumTV-{version}-debug.apk",
            f"PremiumTV-{version}-mac-arm64.dmg",
            f"PremiumTV-{version}-mac-arm64.pkg",
            f"PremiumTV-{version}-mac-x64.dmg",
            f"PremiumTV-{version}-mac-x64.pkg",
        ]
        release = {
            "tag_name": f"v{version}", "prerelease": False, "draft": False,
            "assets": [{"name": name, "size": 100, "digest": f"sha256:{digest}"}
                       for name in names],
        }
        channels, _ = build_site_data.build_apps({}, [release])
        self.assertEqual(channels[0]["version"], version)
        apk = next(a for a in channels[0]["assets"] if a["name"].endswith(".apk"))
        self.assertEqual(apk["sha256"], digest)
        self.assertEqual(build_site_data.asset_digest({"digest": "sha256:zzz"}), None)

        workflow = (ROOT / ".github/workflows/pages.yml").read_text(encoding="utf-8")
        self.assertIn("digest, browser_download_url", workflow)
        self.assertIn("gh workflow run pages.yml", workflow)
        self.assertIn("github.event_name != 'release'", workflow)

    def test_site_payload_and_feed_are_reproducible(self):
        payload_again, changelog_again = build_site_data.build_payload()
        self.assertEqual(self.payload["generated_utc"], payload_again["generated_utc"])
        self.assertEqual(build_site_data.write_feed(self.changelog),
                         build_site_data.write_feed(changelog_again))

    def test_download_page_and_deploy_workflow_cover_site_contract(self):
        page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "docs" / "assets" / "app.js").read_text(encoding="utf-8")
        workflow = (ROOT / ".github" / "workflows" / "pages.yml").read_text(encoding="utf-8")
        for section in ('id="apps"', 'id="playlists"', 'id="changelog"'):
            self.assertIn(section, page)
        for asset in ('data/site-data.js', 'assets/style.css', 'assets/app.js', 'assets/qrcode.js'):
            self.assertIn(asset, page)
        self.assertIn("JSON.stringify(fresh) !== bakedSignature", script)
        for path in ('CHANGELOG.md', 'playlists/countries/**', 'playlists/report.json',
                     'playlists/STATUS.md', 'release:', 'workflow_run:',
                     'Scrape playlists', 'Quick playlist update', 'Deep link and guide check'):
            self.assertIn(path, workflow)
        self.assertIn("repos/${GITHUB_REPOSITORY}/releases?per_page=100", workflow)

    def test_full_hub_is_built_and_published_on_pages(self):
        workflow = (ROOT / ".github/workflows/pages.yml").read_text()
        page = (ROOT / "docs/index.html").read_text()
        self.assertIn('href="hub/"', page)
        for required in ('"hub/**"', '"categories/**"', '"playlists/categories/**"',
                         'python hub/build_data.py', 'python hub/export_static.py',
                         'cp -a hub/dist/static-site docs/hub'):
            self.assertIn(required, workflow)
        self.assertLess(workflow.index('python hub/build_data.py'),
                        workflow.index('python hub/export_static.py'))
        self.assertLess(workflow.index('cp -a hub/dist/static-site docs/hub'),
                        workflow.index('uses: actions/upload-pages-artifact'))

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
