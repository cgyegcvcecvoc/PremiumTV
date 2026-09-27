"""Offline end-to-end checks for the existing scraper; no public streams required."""
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
import scraper  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        base = f"http://127.0.0.1:{self.server.server_port}"
        if self.path == "/source.m3u":
            body = ("#EXTM3U\n#EXTINF:-1 group-title=\"News\",Test Live\n"
                    f"{base}/live.m3u8\n#EXTINF:-1 group-title=\"News\",Bad HTML\n"
                    f"{base}/bad\n").encode()
            ctype = "audio/x-mpegurl"
        elif self.path == "/root.json":
            body = json.dumps({"name": "Root", "groups": [{"name": "Digital TV", "url": f"{base}/group.json"}]}).encode()
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
        else:
            body, ctype = b"<html>Not a stream</html>", "text/html"
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

    def test_checked_playlist_and_failed_refresh_preserves_it(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = f"http://127.0.0.1:{self.server.server_port}"
            cfg = root / "sources.json"
            cfg.write_text(json.dumps({"sources": [
                {"name": "m3u", "type": "m3u", "url": base + "/source.m3u"},
                {"name": "w3u", "type": "w3u", "url": base + "/root.json",
                 "include_groups": ["Digital TV"], "max_depth": 2},
            ]}), encoding="utf-8")
            out = root / "playlists"
            args = ["scraper.py", "--sources", str(cfg), "--out", str(out),
                    "--workers", "2", "--timeout", "2"]
            with patch.object(sys, "argv", args), redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)
            verified = (out / "PremiumTV.m3u").read_text(encoding="utf-8")
            all_links = (out / "PremiumTV_all.m3u").read_text(encoding="utf-8")
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            self.assertTrue(verified.startswith("#EXTM3U\n"))
            self.assertEqual(verified.count("#EXTINF"), 2)
            self.assertEqual(all_links.count("#EXTINF"), 3)
            self.assertIn("#EXTVLCOPT:http-referrer=https://example.org/", verified)
            self.assertEqual(report["total_unique"], 3)
            self.assertEqual(report["working"], 2)
            self.assertTrue((out / "sources" / "m3u.m3u").exists())
            self.assertTrue((out / "sources" / "w3u.m3u").exists())

            # An upstream outage uses the local caches; an unsuccessful check
            # must not wipe the last good player playlist.
            def dead(ch, timeout):
                ch.status, ch.reason = "dead", "simulated outage"
                return ch

            with patch.object(sys, "argv", args), \
                 patch.object(scraper, "fetch_source_text", side_effect=RuntimeError("offline")), \
                 patch.object(scraper, "check_channel", side_effect=dead), \
                 redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 1)
            self.assertEqual((out / "PremiumTV.m3u").read_text(encoding="utf-8"), verified)


if __name__ == "__main__":
    unittest.main()
