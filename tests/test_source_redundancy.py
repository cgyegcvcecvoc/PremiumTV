"""A source has backup addresses, not one address.

The feature request behind 1.1.20 - "many sources, so if one goes down we have
many backups for everything" - is the same idea the playlists already use for
feeds, applied one level up: a channel keeps spare streams, a source keeps
spare addresses for the identical file, and the browser/macOS/Linux/Android
clients each carry the same shared policy.

These tests are offline: no test here touches the public internet.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import scraper  # noqa: E402


def text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def config() -> dict:
    return json.loads(text("sources.json"))


class MirrorAddressTests(unittest.TestCase):
    def test_a_source_offers_its_mirrors_in_order_without_repeating_itself(self):
        src = {
            "url": "https://raw.githubusercontent.com/owner/repo/main/list.m3u",
            "mirrors": [
                "https://cdn.jsdelivr.net/gh/owner/repo@main/list.m3u",
                "https://cdn.jsdelivr.net/gh/owner/repo@main/list.m3u",
                "ftp://example.org/list.m3u",
                "https://raw.githubusercontent.com/owner/repo/main/list.m3u",
            ],
        }
        attempts = scraper.source_mirror_urls(src, src["url"])
        self.assertEqual(
            [(url, how) for url, how in attempts],
            [("https://cdn.jsdelivr.net/gh/owner/repo@main/list.m3u", "mirrors")],
        )

    def test_a_template_is_expanded_from_the_source_itself(self):
        src = {
            "url": "https://raw.githubusercontent.com/owner/repo/master/tv/list.m3u",
            "github": {"repo": "owner/repo", "path": "tv/list.m3u", "ref": "master"},
            "mirror_templates": ["https://mirror.example/{repo}/{ref}{path}?from={owner}"],
        }
        self.assertEqual(
            scraper.source_mirror_urls(src, src["url"]),
            [("https://mirror.example/owner/repo/master/tv/list.m3u?from=owner", "mirror_templates")],
        )

    def test_a_malformed_template_is_skipped_rather_than_fatal(self):
        src = {
            "url": "https://example.test/list.m3u",
            "github": {"repo": "owner/repo", "path": "list.m3u", "ref": "main"},
            "mirrors": ["https://backup.test/list.m3u"],
            "mirror_templates": [
                "https://bad.example/{not_a_field}",
                "https://ok.example{path}",
            ],
        }
        attempts = scraper.source_mirror_urls(src, src["url"])
        self.assertIn(("https://backup.test/list.m3u", "mirrors"), attempts)
        self.assertIn(("https://ok.example/list.m3u", "mirror_templates"), attempts)
        self.assertFalse(any("bad.example" in url for url, _ in attempts))

    def test_a_source_without_a_github_block_templates_its_url_path(self):
        src = {
            "url": "https://example.test/lists/tv.m3u",
            "mirror_templates": ["https://mirror.example{path}"],
        }
        self.assertEqual(
            scraper.source_mirror_urls(src, src["url"]),
            [("https://mirror.example/lists/tv.m3u", "mirror_templates")],
        )

    def test_a_source_without_mirrors_has_no_extra_attempts(self):
        src = {"url": "https://example.test/list.m3u"}
        self.assertEqual(scraper.source_mirror_urls(src, src["url"]), [])


class MirrorFetchTests(unittest.TestCase):
    def test_the_mirror_answers_when_the_primary_does_not_and_the_report_says_so(self):
        src = {
            "url": "https://primary.test/list.m3u",
            "mirrors": ["https://backup.test/list.m3u"],
        }
        calls = []

        def fake_get(url, headers=None, timeout=30, retries=2):
            calls.append(url)
            if url.startswith("https://primary"):
                raise RuntimeError("primary is down")
            return "#EXTM3U\n#EXTINF:-1,One\nhttps://stream.test/1.m3u8\n"

        with patch.object(scraper, "http_get", side_effect=fake_get):
            body = scraper.fetch_source_text(src)

        self.assertIn("#EXTM3U", body)
        self.assertEqual(calls, ["https://primary.test/list.m3u", "https://backup.test/list.m3u"])
        self.assertEqual(src["_fetch_method"], "mirrors")
        self.assertEqual(src["_mirror_url"], "https://backup.test/list.m3u")
        self.assertEqual(src["_primary_fetch_error"], "primary is down")

    def test_the_github_api_fallback_still_wins_when_every_address_fails(self):
        src = {
            "url": "https://primary.test/list.m3u",
            "mirrors": ["https://backup.test/list.m3u"],
            "github": {"repo": "owner/repo", "path": "list.m3u", "ref": "main"},
        }
        calls = []

        def fake_get(url, headers=None, timeout=30, retries=2):
            calls.append(url)
            if "api.github.com" in url:
                return "#EXTM3U\n#EXTINF:-1,From the API\nhttps://stream.test/1.m3u8\n"
            raise RuntimeError("down")

        with patch.object(scraper, "http_get", side_effect=fake_get):
            body = scraper.fetch_source_text(src)

        self.assertIn("From the API", body)
        self.assertEqual(src["_fetch_method"], "github_api_fallback")
        self.assertEqual(len(calls), 3)  # primary, mirror, API


class ConfiguredSourceTests(unittest.TestCase):
    def test_every_configured_mirror_is_a_valid_https_address(self):
        for source in config()["sources"]:
            for mirror in source.get("mirrors") or []:
                with self.subTest(source=source["name"], mirror=mirror):
                    self.assertIsNone(scraper.source_url_problem(mirror))
                    self.assertTrue(mirror.startswith("https://"))
                    self.assertNotEqual(mirror, source.get("url"))

    def test_the_github_hosted_sources_have_a_backup_address(self):
        by_name = {source["name"]: source for source in config()["sources"]}
        for name in ("aria", "aria-plus", "doms9", "iptv-org", "free-tv", "pluto-us",
                     "aria-overseas", "vbskycn-iptv"):
            with self.subTest(name=name):
                source = by_name[name]
                mirrors = source.get("mirrors") or []
                self.assertTrue(any("cdn.jsdelivr.net" in url for url in mirrors), mirrors)
                self.assertTrue(any("gitmirror" in url for url in mirrors), mirrors)

    def test_the_two_new_sources_are_enabled_and_documented(self):
        by_name = {source["name"]: source for source in config()["sources"]}
        overseas = by_name["aria-overseas"]
        self.assertTrue(overseas["enabled"])
        self.assertEqual(overseas["github"]["repo"], "akiralereal/iptv")
        self.assertEqual(overseas["github"]["path"], "IPTV-overseas.m3u")
        self.assertIn("overseas", overseas["note"])
        china = by_name["vbskycn-iptv"]
        self.assertTrue(china["enabled"])
        self.assertEqual(china["github"]["repo"], "vbskycn/iptv")
        self.assertIn("HTTPS", china["note"])

    def test_the_reference_checks_cover_the_sites_that_publish_no_playlist(self):
        references = {item["name"]: item for item in config()["reference_checks"]}
        self.assertEqual(references["xyzstreams"]["url"], "https://xyzstreams.space/")
        self.assertEqual(references["ppv.st"]["url"], "https://ppv.st/")
        self.assertEqual(references["Easy-Web-TV-M3u8"]["repo"], "zhangboheng/Easy-Web-TV-M3u8")
        for name in ("xyzstreams", "ppv.st", "Easy-Web-TV-M3u8"):
            with self.subTest(name=name):
                # Reference checks observe; they never import channels.
                self.assertEqual(references[name]["type"] if name != "Easy-Web-TV-M3u8"
                                 else "github_repo", references[name]["type"])
                self.assertTrue(references[name]["enabled"])
                self.assertTrue(references[name]["note"])


if __name__ == "__main__":
    unittest.main()
