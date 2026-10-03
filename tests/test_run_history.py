"""Offline end-to-end tests for the playlist scraper; no public streams required."""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading
import unittest
from collections import Counter
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import scraper  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    counts = Counter()
    counts_lock = threading.Lock()

    def do_GET(self):
        base = f"http://127.0.0.1:{self.server.server_port}"
        if self.path == "/source.m3u":
            body = (
                "#EXTM3U\n"
                '#EXTINF:-1 group-title="News",Test Live\n'
                f"{base}/live.m3u8\n"
                '#EXTINF:-1 group-title="News",Bad HTML\n'
                f"{base}/bad\n"
            ).encode()
            ctype = "audio/x-mpegurl"
        elif self.path == "/root.json":
            body = json.dumps({
                "name": "Root",
                "groups": [{"name": "Digital TV", "url": f"{base}/group.json"}],
            }).encode()
            ctype = "application/json"
        elif self.path == "/group.json":
            body = json.dumps({"name": "Digital TV", "stations": [
                {"name": "Duplicate", "url": f"{base}/live.m3u8"},
                {"name": "Other Live", "url": f"{base}/other.m3u8", "referer": "https://example.org/"},
                {"name": "Web page", "url": f"{base}/bad", "embed": "true"},
            ]}).encode()
            ctype = "application/json"
        elif self.path in ("/live.m3u8", "/other.m3u8"):
            body, ctype = b"#EXTM3U\n#EXTINF:5,Segment\nsegment.ts\n", "application/vnd.apple.mpegurl"
        elif self.path == "/bad":
            body, ctype = b"<html>Not a stream</html>", "text/html"
        elif self.path == "/blocked":
            self.send_response(403)
            self.end_headers()
            return
        elif self.path == "/rate-limited":
            with self.counts_lock:
                self.counts["rate-limited"] += 1
            self.send_response(429)
            self.send_header("Retry-After", "0")
            self.end_headers()
            return
        elif self.path == "/eja":
            body, ctype = b"<!doctype html><html><title>Directory</title></html>", "text/html"
        else:
            body, ctype = b"not found", "text/plain"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class ScraperIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    @property
    def base(self):
        return f"http://127.0.0.1:{self.server.server_port}"

    def test_checked_playlists_sources_deduplication_and_diagnostics(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg = root / "sources.json"
            cfg.write_text(json.dumps({
                "sources": [
                    {"name": "m3u", "type": "m3u", "url": self.base + "/source.m3u"},
                    {"name": "w3u", "type": "w3u", "url": self.base + "/root.json",
                     "include_groups": ["Digital TV"], "max_depth": 2},
                    {"name": "optional", "type": "m3u", "optional": True,
                     "url_env": "TEST_OPTIONAL_PLAYLIST_URL"},
                ],
                "reference_checks": [
                    {"name": "eja.tv", "type": "website", "url": self.base + "/eja"},
                    {"name": "StepDaddyLiveHD", "type": "github_repo",
                     "repo": "test/reference", "ref": "master"},
                ],
            }), encoding="utf-8")
            out = root / "playlists"
            args = ["scraper.py", "--sources", str(cfg), "--out", str(out),
                    "--workers", "2", "--per-host-workers", "2", "--timeout", "2", "--retries", "0"]
            real_http_get = scraper.http_get

            def fake_http_get(url, headers=None, timeout=30, retries=2):
                if url == "https://api.github.com/repos/test/reference":
                    return json.dumps({"archived": False, "default_branch": "master"})
                if "api.github.com/repos/test/reference/git/trees/master" in url:
                    return json.dumps({"truncated": False, "tree": [
                        {"path": "README.md", "type": "blob"},
                    ]})
                return real_http_get(url, headers=headers, timeout=timeout, retries=retries)

            with patch.dict(os.environ, {"TEST_OPTIONAL_PLAYLIST_URL": ""}), \
                 patch.object(scraper, "http_get", side_effect=fake_http_get), \
                 patch.object(sys, "argv", args), redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)

            verified = (out / "PremiumTV.m3u").read_text(encoding="utf-8")
            all_links = (out / "PremiumTV_all.m3u").read_text(encoding="utf-8")
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            history = (out / "run-history.jsonl").read_text(encoding="utf-8").splitlines()
            status = (out / "STATUS.md").read_text(encoding="utf-8")

            # The published playlist always advertises the repository's own
            # merged guide first, even when no source carried a guide.
            self.assertTrue(
                verified.splitlines()[0].startswith('#EXTM3U x-tvg-url="https://raw.'
                                                    'githubusercontent.com/'),
                verified.splitlines()[0])
            self.assertIn("/playlists/epg/PremiumTV.xml", verified.splitlines()[0])
            self.assertEqual(verified.count("#EXTINF"), 2)
            self.assertEqual(all_links.count("#EXTINF"), 3)
            self.assertIn("#EXTVLCOPT:http-referrer=https://example.org/", verified)
            self.assertEqual(report["total_unique"], 3)
            self.assertEqual(report["working"], 2)
            self.assertEqual(report["dead_count"], 1)
            self.assertEqual(report["status"], "warning")
            self.assertTrue(report["final_playlist_written"])
            self.assertEqual(report["changes"]["added_count"], 3)
            self.assertEqual(report["sources"]["m3u"]["found"], 2)
            self.assertEqual(report["sources"]["m3u"]["overlap"], 1)
            self.assertEqual(report["sources"]["w3u"]["alive"], 2)
            self.assertEqual(report["sources"]["optional"]["status"], "not_configured")
            self.assertEqual(report["reference_checks"]["eja.tv"]["status"], "reachable")
            self.assertFalse(report["reference_checks"]["eja.tv"]["channels_imported"])
            self.assertEqual(report["reference_checks"]["StepDaddyLiveHD"]["static_playlist_files"], [])
            self.assertTrue(report["diagnostics"])
            self.assertIn("html page, not a stream", status)
            self.assertEqual(len(history), 1)
            self.assertEqual(json.loads(history[0])["run_type"], "manual")
            self.assertTrue((out / "sources" / "m3u.m3u").exists())
            self.assertTrue((out / "sources" / "w3u.m3u").exists())

            # A repeated URL from two sources is probed once but credited to both.
            duplicate = next(item for item in report["dead"] + report["unverified"]
                             if item["name"] == "Bad HTML")
            self.assertEqual(duplicate["sources"], ["m3u"])

    def test_no_check_is_logged_without_overwriting_checked_player_playlist(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg = root / "sources.json"
            cfg.write_text(json.dumps({"sources": [
                {"name": "m3u", "type": "m3u", "url": self.base + "/source.m3u"},
            ]}), encoding="utf-8")
            out = root / "playlists"
            out.mkdir()
            previous = "#EXTM3U\n#EXTINF:-1,Previously checked\nhttps://example.org/good.m3u8\n"
            (out / "PremiumTV.m3u").write_text(previous, encoding="utf-8")
            args = ["scraper.py", "--sources", str(cfg), "--out", str(out), "--no-check"]
            with patch.object(sys, "argv", args), redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)

            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            history = json.loads((out / "run-history.jsonl").read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(report["status"], "unchecked")
            self.assertFalse(report["checked"])
            self.assertFalse(report["final_playlist_written"])
            self.assertEqual(report["sources"]["m3u"]["unchecked"], 2)
            self.assertEqual((out / "PremiumTV.m3u").read_text(encoding="utf-8"), previous)
            self.assertEqual(history["status"], "unchecked")

    def test_failed_recheck_is_logged_and_preserves_last_good_player_playlist(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg = root / "sources.json"
            cfg.write_text(json.dumps({"sources": [
                {"name": "m3u", "type": "m3u", "url": self.base + "/source.m3u"},
            ]}), encoding="utf-8")
            out = root / "playlists"
            args = ["scraper.py", "--sources", str(cfg), "--out", str(out),
                    "--workers", "2", "--timeout", "2", "--retries", "0"]
            with patch.object(sys, "argv", args), redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)
            previous_player_list = (out / "PremiumTV.m3u").read_text(encoding="utf-8")

            def mark_dead(channel, *args, **kwargs):
                channel.status, channel.reason = "dead", "simulated outage"
                return channel

            recheck_args = args + ["--label", "6 AM recheck"]
            with patch.object(sys, "argv", recheck_args), \
                 patch.object(scraper, "fetch_source_text", side_effect=RuntimeError("offline")), \
                 patch.object(scraper, "check_channel", side_effect=mark_dead), \
                 redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 1)

            self.assertEqual((out / "PremiumTV.m3u").read_text(encoding="utf-8"), previous_player_list)
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            history = [json.loads(line) for line in (out / "run-history.jsonl").read_text().splitlines()]
            self.assertEqual(report["status"], "failed")
            self.assertTrue(report["checked"])
            self.assertTrue(report["check_completed"])
            self.assertFalse(report["final_playlist_written"])
            self.assertTrue(report["sources"]["m3u"]["from_cache"])
            self.assertTrue(any("offline" in issue for issue in report["issues"]))
            self.assertEqual(len(history), 2)
            self.assertEqual(history[-1]["run_type"], "recheck")
            self.assertEqual(history[-1]["status"], "failed")

    def test_403_and_429_are_unverified_and_429_retries(self):
        blocked = scraper.Channel("Blocked", self.base + "/blocked", "test")
        self.assertEqual(scraper.check_channel(blocked, timeout=2, retries=0).status, "unverified")
        self.assertEqual(blocked.reason, "HTTP 403")

        with Handler.counts_lock:
            Handler.counts["rate-limited"] = 0
        limited = scraper.Channel("Limited", self.base + "/rate-limited", "test")
        self.assertEqual(scraper.check_channel(limited, timeout=2, retries=1).status, "unverified")
        self.assertEqual(limited.reason, "HTTP 429")
        with Handler.counts_lock:
            self.assertEqual(Handler.counts["rate-limited"], 2)

    def test_reference_audits_do_not_claim_to_import_channels(self):
        def fake_get(url, headers=None, timeout=30, retries=2):
            if url == self.base + "/eja":
                return "<!doctype html><html>Directory</html>"
            if url.endswith("/repos/test/repo"):
                return json.dumps({"archived": True, "default_branch": "main"})
            if "git/trees/main" in url:
                return json.dumps({
                    "truncated": False,
                    "tree": [{"path": "README.md", "type": "blob"},
                             {"path": "catalog.json", "type": "blob"}],
                })
            raise AssertionError(f"unexpected URL: {url}")

        issues = []
        with patch.object(scraper, "http_get", side_effect=fake_get):
            results = scraper.audit_reference_sources([
                {"name": "eja.tv", "type": "website", "url": self.base + "/eja",
                 "note": "directory only"},
                {"name": "StepDaddyLiveHD", "type": "github_repo", "repo": "test/repo",
                 "note": "self-hosted"},
            ], issues)

        self.assertEqual(results["eja.tv"]["status"], "reachable")
        self.assertFalse(results["eja.tv"]["channels_imported"])
        self.assertEqual(results["StepDaddyLiveHD"]["static_playlist_files"], [])
        self.assertEqual(results["StepDaddyLiveHD"]["ingest_status"], "no_static_playlist")
        self.assertTrue(results["StepDaddyLiveHD"]["archived"])
        self.assertFalse(results["StepDaddyLiveHD"]["channels_imported"])
        self.assertEqual(issues, [])

    def test_requested_sources_are_in_the_scraper_configuration(self):
        config_path = Path(__file__).resolve().parents[1] / "sources.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        sources = {source["name"]: source for source in config["sources"]}
        self.assertTrue(sources["aria"]["enabled"])
        self.assertTrue(sources["doms9"]["enabled"])
        self.assertTrue(sources["iptv-org"]["enabled"])
        self.assertTrue(sources["free-tv"]["enabled"])
        self.assertEqual(sources["aria"]["url"],
                         "https://raw.githubusercontent.com/aria-tv/aria/main/aria.m3u")
        self.assertEqual(sources["doms9"]["url"],
                         "https://raw.githubusercontent.com/doms9/iptv/default/M3U8/TV.m3u8")
        self.assertEqual(sources["eja-tv-feed"]["url_env"], "EJA_M3U_URL")
        self.assertEqual(sources["stepdaddylivehd-instance"]["url_env"],
                         "STEPDADDYLIVEHD_PLAYLIST_URL")
        references = {item["name"]: item for item in config["reference_checks"]}
        self.assertEqual(references["eja.tv"]["url"], "https://eja.tv/")
        self.assertEqual(references["StepDaddyLiveHD"]["repo"], "gookie-dev/StepDaddyLiveHD")

    def test_run_labels_cover_regular_recheck_and_final_checks(self):
        self.assertEqual(scraper.classify_run("3:00 AM daily scrape"), "regular_check")
        self.assertEqual(scraper.classify_run("6:00 AM recheck"), "recheck")
        self.assertEqual(scraper.classify_run("4:15 PM final check"), "final_check")

    def test_safe_url_redacts_credentials_and_sensitive_query_values(self):
        value = scraper.safe_url("https://user:pass@example.org/live?token=abc&id=4&password=xyz")
        self.assertEqual(value, "https://example.org/live?token=%5Bredacted%5D&id=4&password=%5Bredacted%5D")


if __name__ == "__main__":
    unittest.main()
