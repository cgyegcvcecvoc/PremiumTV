"""Offline guardrails for source identity, fetch policy and honest fixture timing."""
import json
import ssl
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import build_live_schedule  # noqa: E402
import scraper  # noqa: E402


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

    def test_the_live_event_source_has_a_real_mirror(self):
        config = json.loads((ROOT / "sources.json").read_text())
        by_name = {source["name"]: source for source in config["sources"]}
        source = by_name["doms9-events"]
        self.assertEqual(source["type"], "m3u")
        self.assertEqual(source["github"]["path"], "M3U8/events.m3u8")
        self.assertTrue(source["url"].startswith("https://raw.githubusercontent.com/doms9/iptv/"))
        self.assertTrue(any("gitlab.com/doms9/iptv" in mirror for mirror in source["mirrors"]))
        # Codeberg's copy held 205 of the GitHub file's 381 entries on
        # 2026-11-27; treating it as an identical mirror would silently shorten
        # the live-event set on any run that fell back to it.
        self.assertFalse(any("codeberg.org" in mirror for mirror in source["mirrors"]))
        self.assertIn("381 entries", source["note"])

    def test_committed_sources_are_https_without_credentials(self):
        config = json.loads((ROOT / "sources.json").read_text())
        for source in config["sources"]:
            with self.subTest(name=source.get("name")):
                if source.get("github"):
                    self.assertIsNone(scraper.github_repo_problem(source["github"]["repo"]))
                    path = source["github"]["path"]
                    self.assertFalse(path.startswith("/"))
                    self.assertNotIn("..", Path(path).parts)
                local = source.get("local_path")
                if local:
                    self.assertFalse(Path(local).is_absolute(), local)
                    resolved = scraper.configured_local_path(local)
                    self.assertTrue(resolved.is_relative_to(ROOT.resolve()), local)
                url = source.get("url")
                if not url:
                    self.assertTrue(source.get("url_env"), source)
                    continue
                self.assertIsNone(scraper.source_url_problem(url), url)
                self.assertTrue(url.startswith("https://"), url)
        for feed in config["epg_sources"]["fixed"]:
            if not feed.get("enabled", True):
                continue
            self.assertIsNone(scraper.source_url_problem(feed["url"]), feed["url"])
            self.assertTrue(feed["url"].startswith("https://"))
        self.assertIn("cgyegcvcecvoc", config["discovery"]["github_search"]["exclude_owners"])

    def test_known_league_and_duplicates_never_generate_guess(self):
        event = build_live_schedule.parse_event("[UEFA Conference League] Alpha vs Beta")
        duplicate = {**event, "kickoff_utc": "2026-10-22T16:45:00Z"}
        games = build_live_schedule.assign_kickoffs([duplicate, event])
        self.assertEqual(len(games), 1)
        self.assertIsNone(games[0]["kickoff_utc"])
        self.assertEqual(event["title"], games[0]["title"])


class SourceFetchPolicyTests(unittest.TestCase):
    def test_source_fetches_use_verified_tls(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self):
                return b"#EXTM3U\n"

        with patch.object(scraper.urllib.request, "urlopen", return_value=Response()) as request:
            text = scraper.http_get("https://example.test/list.m3u", retries=0)
        self.assertEqual(text, "#EXTM3U\n")
        _args, kwargs = request.call_args
        self.assertIs(kwargs.get("context"), scraper.SECURE_CTX)
        self.assertIsNot(kwargs.get("context"), scraper.INSECURE_CTX)
        self.assertEqual(scraper.SECURE_CTX.verify_mode, ssl.CERT_REQUIRED)

    def test_stream_probes_keep_the_lenient_tls_context(self):
        channel = scraper.Channel(
            name="Probe", url="https://example.test/live.m3u8", source="fixture",
        )

        class Response:
            headers = {"Content-Type": "application/vnd.apple.mpegurl"}

            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _size=4096):
                return b"#EXTM3U\n#EXTINF:5,\nsegment.ts\n"

        with patch.object(scraper.urllib.request, "urlopen", return_value=Response()) as request:
            scraper.check_channel(channel, timeout=1, retries=0)
        _args, kwargs = request.call_args
        self.assertIs(kwargs.get("context"), scraper.INSECURE_CTX)

    def test_file_and_credential_urls_are_refused(self):
        self.assertEqual(scraper.source_url_problem("file:///etc/passwd"), "unsupported scheme file")
        self.assertEqual(
            scraper.source_url_problem("https://user:secret@example.test/list.m3u"),
            "URL credentials are not allowed",
        )
        self.assertEqual(scraper.source_url_problem("javascript:alert(1)"), "unsupported scheme javascript")
        with self.assertRaisesRegex(RuntimeError, "credentials"):
            scraper.http_get("https://user:secret@example.test/list.m3u")
        with self.assertRaisesRegex(RuntimeError, "unsupported scheme"):
            scraper.fetch_source_text({"name": "bad", "url": "file:///tmp/list.m3u"})

    def test_relative_local_path_cannot_leave_the_repository(self):
        with self.assertRaisesRegex(ValueError, "escapes"):
            scraper.configured_local_path("../outside.m3u")
        inside = scraper.configured_local_path("playlists/sources/local-channels.m3u")
        self.assertTrue(inside.is_relative_to(ROOT.resolve()))

    def test_github_fallback_rejects_a_crafted_repo(self):
        with patch.object(scraper, "http_get", side_effect=RuntimeError("offline")):
            with self.assertRaisesRegex(RuntimeError, "owner/name"):
                scraper.fetch_source_text({
                    "name": "bad",
                    "url": "https://example.test/missing.m3u",
                    "github": {"repo": "../evil/repo", "path": "list.m3u", "ref": "main"},
                })
            with self.assertRaisesRegex(RuntimeError, "relative file"):
                scraper.fetch_source_text({
                    "name": "bad",
                    "url": "https://example.test/missing.m3u",
                    "github": {"repo": "owner/name", "path": "../secret.m3u", "ref": "main"},
                })

    def test_macos_player_libraries_are_pinned_exactly(self):
        package = json.loads((ROOT / "macos/app/package.json").read_text())
        web = json.loads((ROOT / "web/package.json").read_text())
        for name in ("hls.js", "mpegts.js"):
            self.assertEqual(package["dependencies"][name], web["dependencies"][name])
            self.assertRegex(package["dependencies"][name], r"^\d+\.\d+\.\d+$")
        for name, value in package["dependencies"].items():
            self.assertFalse(value.startswith("^") or value.startswith("~"), name)
        for name, value in package["devDependencies"].items():
            self.assertFalse(value.startswith("^") or value.startswith("~"), name)


if __name__ == "__main__":
    unittest.main()
