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

    def test_release_digest_beats_a_stale_build_out_checksum(self):
        digest = "b" * 64
        api_release = {
            "tag_name": "v1.0.4", "prerelease": False, "draft": False,
            "assets": [
                {"name": f"PremiumTV-1.0.4-{name}", "size": 100,
                 "digest": f"sha256:{digest}"}
                for name in ("debug.apk", "mac-arm64.dmg", "mac-arm64.pkg",
                             "mac-x64.dmg", "mac-x64.pkg")
            ],
        }
        stale = {a["name"]: "a" * 64 for a in api_release["assets"]}
        channels, _ = build_site_data.build_apps(stale, [api_release])
        self.assertEqual(channels[0]["version"], "1.0.4")
        for asset in channels[0]["assets"]:
            self.assertEqual(asset["sha256"], digest, asset["name"])

    def test_download_checksums_match_the_release_digests(self):
        releases = {r["tag"]: r for r in build_site_data.load_releases()}
        for channel in self.payload["apps"]["channels"]:
            published = {a["name"]: a for a in releases.get(channel["tag"], {}).get("assets", [])}
            for asset in channel["assets"]:
                digest = str(published.get(asset["name"], {}).get("digest") or "")
                if digest.startswith("sha256:"):
                    self.assertEqual(asset["sha256"], digest.split(":", 1)[1], asset["name"])

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

    def test_lineup_preview_matches_the_published_playlist(self):
        lineup = self.payload["lineup"]
        entries = build_site_data.read_playlist_entries(
            ROOT / "playlists" / "PremiumTV.m3u")
        backups = [e for e in entries if build_site_data.BACKUP_NAME_RE.match(e["name"])]
        self.assertEqual(lineup["entries"], len(entries))
        self.assertEqual(lineup["unique_channels"], len(entries) - len(backups))
        self.assertEqual(lineup["backup_feeds"], len(backups))
        self.assertEqual(sum(g["channels"] for g in lineup["groups"]),
                         lineup["unique_channels"])
        self.assertEqual(sum(lineup["qualities"].values()), lineup["unique_channels"])
        # Every category is unique, has at least one sample, and links to a
        # real category file when one is published.
        names = [g["name"] for g in lineup["groups"]]
        self.assertEqual(len(names), len(set(names)))
        for group in lineup["groups"]:
            self.assertTrue(group["samples"], group["name"])
            self.assertFalse(group["samples"][0].startswith("["), group["name"])
            self.assertTrue(group["playlist_url"].startswith("https://raw.githubusercontent.com/"))
            if group["file"]:
                self.assertTrue((ROOT / group["file"]).is_file(), group["file"])
        # Featured channels are real playlist names, in the categories they
        # actually belong to, and never placeholder event titles.
        published = {build_site_data.clean_channel_name(e["name"]).lower(): e
                     for e in entries if not build_site_data.BACKUP_NAME_RE.match(e["name"])}
        self.assertGreaterEqual(len(lineup["featured"]), 10)
        for channel in lineup["featured"]:
            self.assertIn(channel["name"].lower(), published)
            self.assertEqual(channel["category"], published[channel["name"].lower()]["group"])
            self.assertFalse(channel["name"].startswith("["))

    def test_lineup_section_is_wired_into_the_page(self):
        page = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "docs" / "assets" / "app.js").read_text(encoding="utf-8")
        for marker in ('id="channels"', 'id="lineup-stats"', 'id="lineup-grid"',
                       'id="lineup-search"', 'href="#channels"'):
            self.assertIn(marker, page)
        self.assertIn("initLineup", script)
        self.assertIn("lineup.featured", script)

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
