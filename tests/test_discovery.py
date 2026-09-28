"""Offline end-to-end tests for the monthly discovery engine; no public streams required."""
from __future__ import annotations

import json
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import discover  # noqa: E402
import scraper  # noqa: E402


def playlist(entries, header="#EXTM3U\n"):
    body = header
    for name, path in entries:
        body += f'#EXTINF:-1 group-title="Test",{name}\n{path}\n'
    return body


def working_playlist(base: str, count: int) -> str:
    return playlist([(f"Seeded Channel {index}", f"{base}/live{index}.m3u8") for index in range(count)])


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        base = f"http://127.0.0.1:{self.server.server_port}"
        if self.path == "/good.m3u":
            # 30 new working channels, spread over two hosts.
            entries = [(f"New Channel {index}", f"{base}/live{index}.m3u8") for index in range(15)]
            entries += [(f"Other Channel {index}", f"{base}/alt{index}.m3u8") for index in range(15)]
            body, ctype = playlist(entries).encode(), "audio/x-mpegurl"
        elif self.path == "/dead.m3u":
            entries = [(f"Dead Channel {index}", f"{base}/dead{index}.m3u8") for index in range(40)]
            body, ctype = playlist(entries).encode(), "audio/x-mpegurl"
        elif self.path == "/known.m3u":
            body, ctype = playlist([("Already Known", f"{base}/known.m3u8")]).encode(), "audio/x-mpegurl"
        elif self.path == "/not-a-playlist":
            body, ctype = b"<!doctype html><html><body>directory</body></html>", "text/html"
        elif self.path == "/known.m3u8":
            body, ctype = b"#EXTM3U\n", "application/vnd.apple.mpegurl"
        elif self.path == "/missing.m3u":
            body, ctype = b"gone", "text/plain"
        elif "/live" in self.path or "/alt" in self.path:
            body, ctype = b"#EXTM3U\n#EXTINF:5,Segment\nsegment.ts\n", "application/vnd.apple.mpegurl"
        else:
            body, ctype = b"<html>Not a stream</html>", "text/html"
        if self.path == "/missing.m3u":
            self.send_response(404)
            self.send_header("Content-Type", ctype)
            self.end_headers()
            self.wfile.write(body)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class DiscoveryTest(unittest.TestCase):
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

    def make_config(self, root: Path, **discovery):
        section = {
            "enabled": True,
            "corpus_playlist": "playlists/PremiumTV_all.m3u",
            "candidates": [
                {"name": "good", "type": "m3u", "url": self.base + "/good.m3u"},
                {"name": "dead", "type": "m3u", "url": self.base + "/dead.m3u"},
                {"name": "known", "type": "m3u", "url": self.base + "/known.m3u"},
                {"name": "html", "type": "m3u", "url": self.base + "/not-a-playlist"},
                {"name": "missing", "type": "m3u", "url": self.base + "/missing.m3u"},
            ],
            "github_search": {"enabled": False, "queries": []},
            "thresholds": {"sample_size": 6, "active_source_sample_size": 4, "min_new_links": 25,
                           "min_working_checked": 3, "min_working_ratio": 0.5, "min_score": 55.0},
            "auto_promote": True,
            "max_promote_per_run": 2,
            "recheck_after_days": 90,
        }
        section.update(discovery)
        config = {"sources": [{"name": "active", "type": "m3u", "url": self.base + "/good.m3u"}],
                  "discovery": section}
        (root / "sources.json").write_text(json.dumps(config), encoding="utf-8")
        playlists = root / "playlists"
        playlists.mkdir(parents=True, exist_ok=True)
        (playlists / "PremiumTV_all.m3u").write_text(
            playlist([("Already Known", self.base + "/known.m3u8")]), encoding="utf-8"
        )
        return root / "sources.json", playlists / "discovery"

    def run_discovery(self, cfg: Path, out: Path, extra=()):
        args = ["discover.py", "--sources", str(cfg), "--out", str(out), "--no-search",
                "--workers", "4", "--per-host-workers", "2", "--timeout", "3", "--retries", "0", *extra]
        with patch.object(sys, "argv", args), redirect_stdout(StringIO()):
            code = discover.main()
        return code

    def test_candidates_are_ranked_promoted_and_reported(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg, out = self.make_config(root)
            self.assertEqual(self.run_discovery(cfg, out), 0)

            payload = json.loads((out / "discovery.json").read_text(encoding="utf-8"))
            results = {item["name"]: item for item in payload["candidates"]}
            self.assertEqual(payload["status"], "warning")
            self.assertEqual(results["good"]["verdict"], "promote")
            self.assertEqual(results["good"]["new_links"], 30)
            self.assertEqual(results["good"]["sample"]["alive"], 6)
            self.assertEqual(results["good"]["sample"]["working_ratio"], 1.0)
            self.assertGreaterEqual(results["good"]["score"], 55.0)
            self.assertEqual(results["dead"]["verdict"], "reject")
            self.assertEqual(results["known"]["status"], "no_new_links")
            self.assertEqual(results["html"]["status"], "not_a_playlist")
            self.assertEqual(results["missing"]["status"], "fetch_failed")
            self.assertEqual(payload["summary"]["promoted_names"], ["good"])
            self.assertTrue(any("not an M3U" in issue or "0 channels" in issue
                                or "could not be fetched" in issue for issue in payload["issues"]))

            approved = json.loads((out / "approved-sources.json").read_text(encoding="utf-8"))
            self.assertEqual([item["name"] for item in approved["sources"]], ["good"])
            self.assertEqual(approved["sources"][0]["url"], self.base + "/good.m3u")
            self.assertTrue(approved["sources"][0]["enabled"])
            self.assertIn("monthly discovery", approved["sources"][0]["note"])

            report = (out / "REPORT.md").read_text(encoding="utf-8")
            self.assertIn("# Monthly new-channel discovery", report)
            self.assertIn("| good | seed | 30 | 30 | 6/6 (100%) | 78.8 | **promote** |", report)
            self.assertIn("Known channels in the published playlist", report)
            self.assertIn("| active | 30 | 30 | 4/4 (100%) | ok |", report)

            exported = (out / "new-channels.m3u").read_text(encoding="utf-8")
            self.assertTrue(exported.startswith("#EXTM3U"))
            self.assertIn("/live0.m3u8", exported)

            history = [json.loads(line) for line in (out / "history.jsonl").read_text().splitlines()]
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0]["run_type"], "monthly_discovery")
            self.assertEqual(history[0]["promoted"], ["good"])
            self.assertEqual(history[0]["new_working_links"], 6)

            # The active source is reviewed too, and its known links are not counted as new.
            active = {item["name"]: item for item in payload["active_sources"]}
            self.assertEqual(active["active"]["status"], "ok")
            self.assertEqual(active["active"]["new_links"], 30)
            self.assertEqual(active["active"]["sample"]["alive"], 4)

    def test_promoted_sources_are_merged_into_the_next_scrape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg, out = self.make_config(root)
            self.assertEqual(self.run_discovery(cfg, out), 0)
            approved_path = out / "approved-sources.json"
            self.assertTrue(approved_path.exists())

            merged, promoted = scraper.load_approved_sources(str(approved_path), [
                {"name": "active", "type": "m3u", "url": self.base + "/good.m3u"},
            ])
            self.assertEqual([item["name"] for item in merged], ["active", "good"])
            self.assertEqual([item["name"] for item in promoted], ["good"])
            self.assertTrue(merged[1]["promoted_by_discovery"])

            # Running it again must not duplicate the entry.
            merged_again, _ = scraper.load_approved_sources(str(approved_path), merged)
            self.assertEqual([item["name"] for item in merged_again], ["active", "good"])

            # A disabled or URL-less entry is never merged.
            data = json.loads(approved_path.read_text(encoding="utf-8"))
            data["sources"].append({"name": "disabled", "enabled": False, "url": self.base + "/good.m3u"})
            data["sources"].append({"name": "no-url", "enabled": True})
            approved_path.write_text(json.dumps(data), encoding="utf-8")
            merged_final, promoted_final = scraper.load_approved_sources(str(approved_path), [])
            self.assertEqual([item["name"] for item in merged_final], ["good"])
            self.assertEqual([item["name"] for item in promoted_final], ["good"])

            # End to end: the scraper fetches the promoted source and marks it in STATUS.md.
            playlists = root / "playlists"
            args = ["scraper.py", "--sources", str(cfg), "--out", str(playlists), "--workers", "4",
                    "--per-host-workers", "2", "--timeout", "3", "--retries", "0",
                    "--label", "monthly discovery integration scrape"]
            with patch.object(sys, "argv", args), redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)
            report = json.loads((playlists / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["promoted_sources"], ["good"])
            self.assertTrue(report["sources"]["good"]["promoted_by_discovery"])
            self.assertTrue(report["sources"]["good"]["fetched"])
            self.assertIn("good 🌱", (playlists / "STATUS.md").read_text(encoding="utf-8"))
            history = [json.loads(line) for line in
                       (playlists / "run-history.jsonl").read_text().splitlines()]
            self.assertEqual(history[-1]["run_type"], "monthly_discovery")
            self.assertEqual(history[-1]["promoted_sources"], ["good"])

    def test_cooldown_no_promote_and_dry_run_modes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg, out = self.make_config(root)

            # --no-promote reports the qualifying candidate but writes no approval file.
            self.assertEqual(self.run_discovery(cfg, out, ["--no-promote"]), 0)
            self.assertFalse((out / "approved-sources.json").exists())
            payload = json.loads((out / "discovery.json").read_text(encoding="utf-8"))
            good = next(item for item in payload["candidates"] if item["name"] == "good")
            self.assertEqual(good["verdict"], "promote")
            self.assertFalse(good["promoted"])

            # Second run: rejected candidates are remembered and skipped, the qualifying
            # one is re-measured and this time promoted.
            self.assertEqual(self.run_discovery(cfg, out), 0)
            payload = json.loads((out / "discovery.json").read_text(encoding="utf-8"))
            results = {item["name"]: item for item in payload["candidates"]}
            self.assertEqual(results["good"]["status"], "evaluated")
            self.assertEqual(results["dead"]["status"], "skipped_cooldown")
            self.assertEqual(results["html"]["status"], "skipped_cooldown")
            self.assertEqual(payload["summary"]["skipped"], 4)
            self.assertEqual(payload["summary"]["promoted_names"], ["good"])
            self.assertEqual([item["name"] for item in
                              json.loads((out / "approved-sources.json").read_text())["sources"]], ["good"])

            # Third run: the promoted source is never evaluated twice, and --force only
            # re-opens the candidates that were not promoted.
            self.assertEqual(self.run_discovery(cfg, out, ["--force"]), 0)
            payload = json.loads((out / "discovery.json").read_text(encoding="utf-8"))
            results = {item["name"]: item for item in payload["candidates"]}
            self.assertEqual(results["good"]["status"], "already_promoted")
            self.assertEqual(results["dead"]["status"], "evaluated")
            self.assertEqual(
                [item["name"] for item in
                 json.loads((out / "approved-sources.json").read_text())["sources"]], ["good"])

            fresh_out = root / "dry"
            self.assertEqual(self.run_discovery(cfg, fresh_out, ["--dry-run", "--force"]), 0)
            self.assertFalse(fresh_out.exists())

    def test_github_search_candidate_is_evaluated_and_state_is_saved(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg, out = self.make_config(root, candidates=[])
            config = json.loads(cfg.read_text())
            config["discovery"]["github_search"] = {
                "enabled": True, "queries": ["topic:iptv"], "max_results_per_query": 5,
                "max_repositories": 3, "sort": "updated",
            }
            cfg.write_text(json.dumps(config), encoding="utf-8")

            def fake_github_json(url, timeout=25.0, retries=1):
                if "/search/repositories" in url:
                    return {"items": [{"full_name": "test/fresh-tv", "default_branch": "main",
                                       "name": "fresh-tv", "stargazers_count": 3}]}
                if url.endswith("/repos/test/fresh-tv"):
                    return {"full_name": "test/fresh-tv", "default_branch": "main", "name": "fresh-tv",
                            "stargazers_count": 3, "archived": False}
                if "/git/trees/" in url:
                    return {"truncated": False, "tree": [
                        {"path": "README.md", "type": "blob", "size": 100},
                        {"path": "movies/series.m3u", "type": "blob", "size": 900000},
                        {"path": "tv-playlist.m3u", "type": "blob", "size": 90000},
                    ]}
                raise AssertionError(f"unexpected URL: {url}")

            with patch.object(discover, "github_json", side_effect=fake_github_json), \
                 patch.object(discover, "SEARCH_COOLDOWN", 0), \
                 patch.object(sys, "argv", ["discover.py", "--sources", str(cfg), "--out", str(out),
                                            "--workers", "4", "--per-host-workers", "2",
                                            "--timeout", "3", "--retries", "0"]), \
                 redirect_stdout(StringIO()):
                self.assertEqual(discover.main(), 0)

            payload = json.loads((out / "discovery.json").read_text(encoding="utf-8"))
            candidate = next(item for item in payload["candidates"] if item["name"] == "fresh-tv")
            # tv-playlist.m3u wins over the large movies/series.m3u file.
            self.assertEqual(candidate["playlist_path"], "tv-playlist.m3u")
            self.assertEqual(candidate["url"],
                             "https://raw.githubusercontent.com/test/fresh-tv/main/tv-playlist.m3u")
            state = json.loads((out / "state.json").read_text(encoding="utf-8"))
            self.assertIn("test/fresh-tv:tv-playlist.m3u", state["candidates"])
            self.assertEqual(state["candidates"]["test/fresh-tv:tv-playlist.m3u"]["verdict"], candidate["verdict"])

    def test_seeded_repository_candidate_uses_the_resolved_playlist_path(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg, out = self.make_config(root, candidates=[
                {"name": "seed-repo", "github": {"repo": "test/seeded"}},
            ])

            def fake_github_json(url, timeout=25.0, retries=1):
                if url.endswith("/repos/test/seeded"):
                    return {"full_name": "test/seeded", "default_branch": "main", "name": "seeded",
                            "stargazers_count": 5, "archived": False}
                if "/git/trees/" in url:
                    return {"truncated": False, "tree": [
                        {"path": "tv-playlist.m3u", "type": "blob", "size": 90000},
                    ]}
                raise AssertionError(f"unexpected URL: {url}")

            def fake_http_get(url, headers=None, timeout=30, retries=2):
                if url == "https://raw.githubusercontent.com/test/seeded/main/tv-playlist.m3u":
                    return working_playlist(self.base, 30)
                raise AssertionError(f"unexpected URL: {url}")

            with patch.object(discover, "github_json", side_effect=fake_github_json), \
                 patch.object(scraper, "http_get", side_effect=fake_http_get), \
                 patch.object(sys, "argv", ["discover.py", "--sources", str(cfg), "--out", str(out),
                                            "--no-search", "--workers", "4", "--per-host-workers", "2",
                                            "--timeout", "3", "--retries", "0"]), \
                 redirect_stdout(StringIO()):
                self.assertEqual(discover.main(), 0)

            payload = json.loads((out / "discovery.json").read_text(encoding="utf-8"))
            candidate = payload["candidates"][0]
            self.assertEqual(candidate["name"], "seed-repo")
            self.assertEqual(candidate["verdict"], "promote")
            self.assertEqual(candidate["playlist_path"], "tv-playlist.m3u")
            approved = json.loads((out / "approved-sources.json").read_text(encoding="utf-8"))
            entry = approved["sources"][0]
            self.assertEqual(entry["url"], "https://raw.githubusercontent.com/test/seeded/main/tv-playlist.m3u")
            self.assertEqual(entry["github"], {"repo": "test/seeded", "path": "tv-playlist.m3u"})

    def test_seeded_repository_without_a_playlist_is_recorded_as_an_issue(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg, out = self.make_config(root, candidates=[
                {"name": "seed-repo", "github": {"repo": "test/seeded"}},
            ])

            def fake_github_json(url, timeout=25.0, retries=1):
                if url.endswith("/repos/test/seeded"):
                    return {"full_name": "test/seeded", "default_branch": "main", "archived": False}
                return {"truncated": False, "tree": [{"path": "README.md", "type": "blob", "size": 10}]}

            with patch.object(discover, "github_json", side_effect=fake_github_json), \
                 patch.object(sys, "argv", ["discover.py", "--sources", str(cfg), "--out", str(out),
                                            "--no-search", "--no-check"]), \
                 redirect_stdout(StringIO()):
                self.assertEqual(discover.main(), 0)
            payload = json.loads((out / "discovery.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["candidates"], [])
            self.assertTrue(any("no static playlist file" in issue for issue in payload["issues"]))
            self.assertEqual(payload["status"], "warning")

    def test_missing_corpus_is_reported_and_search_failure_is_recorded(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg, out = self.make_config(root, candidates=[])
            (root / "playlists" / "PremiumTV_all.m3u").unlink()
            config = json.loads(cfg.read_text())
            config["discovery"]["github_search"] = {"enabled": True, "queries": ["topic:iptv"]}
            cfg.write_text(json.dumps(config), encoding="utf-8")

            with patch.object(discover, "github_json",
                              side_effect=RuntimeError("403 rate limit exceeded")), \
                 patch.object(discover, "SEARCH_COOLDOWN", 0), \
                 patch.object(sys, "argv", ["discover.py", "--sources", str(cfg), "--out", str(out),
                                            "--no-check", "--workers", "2", "--per-host-workers", "1"]), \
                 redirect_stdout(StringIO()):
                self.assertEqual(discover.main(), 0)

            payload = json.loads((out / "discovery.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["summary"]["corpus_channels"], 0)
            self.assertEqual(payload["status"], "warning")
            self.assertTrue(any("Corpus playlist" in issue for issue in payload["issues"]))
            self.assertTrue(any("rate limit" in issue.lower() for issue in payload["issues"]))
            self.assertTrue(any("DISCOVERY_GITHUB_TOKEN" in issue for issue in payload["issues"]))
            self.assertEqual(payload["summary"]["evaluated"], 0)

    def test_repository_configuration_enables_monthly_discovery(self):
        config_path = Path(__file__).resolve().parents[1] / "sources.json"
        config = json.loads(config_path.read_text(encoding="utf-8"))
        discovery = config["discovery"]
        self.assertTrue(discovery["enabled"])
        self.assertTrue(discovery["auto_promote"])
        self.assertGreaterEqual(discovery["max_promote_per_run"], 1)
        self.assertTrue(discovery["candidates"])
        self.assertTrue(discovery["github_search"]["queries"])
        self.assertGreaterEqual(discovery["thresholds"]["min_new_links"], 1)
        workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows" / "discover.yml")
        self.assertTrue(workflow.exists(), "the monthly discovery workflow must be committed")
        text = workflow.read_text(encoding="utf-8")
        self.assertIn("schedule:", text)
        self.assertIn("discover.py", text)
        self.assertIn("workflow_dispatch:", text)


if __name__ == "__main__":
    unittest.main()
