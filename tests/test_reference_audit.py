"""Offline tests for the HTML channel-index reference audit (dlive.sx).

Nothing here touches the public internet: a local HTTP server stands in for the
channel index page so the audit can be exercised end to end.
"""
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
import scraper  # noqa: E402

# Shaped like the real DaddyLiveHD index: the channel name and its numeric id
# are both inside the anchor, split across nested tags.
INDEX_PAGE = """<!doctype html>
<html><head><title>24/7 Channels | DaddyLiveHD</title></head>
<body>
<nav>
  <a href="/webmasters.php">Webmasters</a>
  <a href="/contact.php">Contact Us</a>
  <a href="/api.php">API</a>
</nav>
<h2>24/7 Live Sports &amp; Entertainment Channels</h2>
<div class="channel">
  <a href="https://dlive.sx/watch.php?id=51"><img src="/logos/abc.png">ABC USA<br>
     <span>ID: 51</span></a>
</div>
<div class="channel">
  <a href="https://dlive.sx/watch.php?id=302">A&amp;E USA<br><span>ID: 302</span></a>
</div>
<div class="channel">
  <a href="/watch.php?id=61">beIN SPORTS en Espa&ntilde;ol<br><span>ID: 61</span></a>
</div>
<div class="channel">
  <!-- the same channel linked twice, once as a bare logo -->
  <a href="https://dlive.sx/watch.php?id=51"><img src="/logos/abc.png"></a>
</div>
<div class="channel">
  <a href="https://dlive.sx/watch.php?id=940">Arena Sport 5 Serbia<br><span>ID: 940</span></a>
</div>
</body></html>
"""

INDEX_WITH_PLAYLIST = INDEX_PAGE.replace(
    '<a href="/api.php">API</a>',
    '<a href="/api.php">API</a>\n  <a href="/downloads/channels.m3u">Download M3U</a>',
)

INDEX_WITHOUT_CHANNELS = """<!doctype html><html><body>
<a href="/webmasters.php">Webmasters</a>
<p>Maintenance.</p>
</body></html>
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        pages = {
            "/24-7-channels.php": INDEX_PAGE,
            "/with-playlist.php": INDEX_WITH_PLAYLIST,
            "/empty.php": INDEX_WITHOUT_CHANNELS,
        }
        if self.path == "/live.m3u8":
            body, ctype = b"#EXTM3U\n#EXTINF:5,Segment\nsegment.ts\n", "application/vnd.apple.mpegurl"
        elif self.path in pages:
            body, ctype = pages[self.path].encode(), "text/html; charset=utf-8"
        elif self.path == "/index.m3u":
            body = ("#EXTM3U\n#EXTINF:-1 group-title=\"24/7\",Proxy Channel\n"
                    f"http://127.0.0.1:{self.server.server_port}/live.m3u8\n").encode()
            ctype = "audio/x-mpegurl"
        else:
            body, ctype = b"<html>Not found</html>", "text/html"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class ChannelIndexParserTest(unittest.TestCase):
    def test_clean_channel_name_drops_tags_and_the_id_suffix(self):
        self.assertEqual(scraper.clean_channel_name('<img src="x.png">ABC USA<br>\n <span>ID: 51</span>'),
                         "ABC USA")
        self.assertEqual(scraper.clean_channel_name("A&amp;E USA"), "A&E USA")
        self.assertEqual(scraper.clean_channel_name("beIN SPORTS en Espa&ntilde;ol"),
                         "beIN SPORTS en Español")
        self.assertEqual(scraper.clean_channel_name("<img only>"), "")

    def test_parse_channel_index_counts_unique_channels_and_keeps_names(self):
        index = scraper.parse_channel_index(INDEX_PAGE, r"watch\.php\?id=\d+", "https://dlive.sx/x.php")
        # Five anchors match, but id 51 appears twice and must count once.
        self.assertEqual(index["count"], 4)
        self.assertEqual(index["with_id"], 4)
        self.assertEqual(index["sample"][0], "ABC USA")
        self.assertIn("A&E USA", index["sample"])
        self.assertIn("beIN SPORTS en Español", index["sample"])
        # Relative hrefs are resolved against the page URL.
        urls = {channel["url"] for channel in index["channels"]}
        self.assertIn("https://dlive.sx/watch.php?id=61", urls)

    def test_parse_channel_index_ignores_unrelated_links(self):
        index = scraper.parse_channel_index(INDEX_PAGE, r"watch\.php\?id=\d+")
        for channel in index["channels"]:
            self.assertNotIn("webmasters", channel["url"])
            self.assertNotIn("api.php", channel["url"])

    def test_parse_channel_index_rejects_a_bad_regex(self):
        with self.assertRaises(ValueError):
            scraper.parse_channel_index(INDEX_PAGE, "watch\\.php(?id=")

    def test_find_playlist_links(self):
        self.assertEqual(scraper.find_playlist_links(INDEX_PAGE, "https://dlive.sx/x.php"), [])
        links = scraper.find_playlist_links(INDEX_WITH_PLAYLIST, "https://dlive.sx/x.php")
        self.assertEqual(links, ["https://dlive.sx/downloads/channels.m3u"])

    def test_index_with_no_channels(self):
        index = scraper.parse_channel_index(INDEX_WITHOUT_CHANNELS, r"watch\.php\?id=\d+")
        self.assertEqual(index["count"], 0)


class ChannelIndexAuditTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def audit(self, path, **extra):
        item = {"name": "dlive.sx", "type": "website_channel_index",
                "url": f"{self.base}{path}",
                "channel_href_regex": r"watch\.php\?id=\d+",
                "player_url_template": "https://dlive.sx/stream/stream-{id}.php"}
        item.update(extra)
        return scraper.audit_reference_source(item)

    def test_player_pages_only(self):
        result = self.audit("/24-7-channels.php")
        self.assertEqual(result["status"], "reachable")
        self.assertTrue(result["reachable"])
        self.assertFalse(result["playlist_detected"])
        self.assertEqual(result["channel_count"], 4)
        self.assertEqual(result["playlist_links"], [])
        self.assertEqual(result["ingest_status"], "player_pages_only")
        self.assertEqual(result["player_url_template"], "https://dlive.sx/stream/stream-{id}.php")
        self.assertNotIn("channels", result)  # the full list stays out of the report

    def test_static_playlist_link_is_reported(self):
        result = self.audit("/with-playlist.php")
        self.assertEqual(result["ingest_status"], "static_playlist_found_not_configured")
        self.assertEqual(len(result["playlist_links"]), 1)
        self.assertEqual(result["channel_count"], 4)

    def test_page_without_channels(self):
        result = self.audit("/empty.php")
        self.assertEqual(result["channel_count"], 0)
        self.assertEqual(result["ingest_status"], "no_channels_found")

    def test_unreachable_site_is_reported_not_fatal(self):
        issues: list[str] = []
        results = scraper.audit_reference_sources(
            [{"name": "gone.example", "type": "website_channel_index",
              "url": f"{self.base}/does-not-exist", "channel_href_regex": r"watch\.php\?id=\d+"},
             {"name": "off", "type": "website_channel_index", "enabled": False, "url": "http://x/"}],
            issues,
        )
        # A 200 HTML page with no channels is still "reachable"; the disabled one is skipped.
        self.assertEqual(results["gone.example"]["ingest_status"], "no_channels_found")
        self.assertEqual(results["off"]["status"], "disabled")
        self.assertFalse(results["off"]["channels_imported"])

    def test_audit_never_imports_channels(self):
        for path in ("/24-7-channels.php", "/with-playlist.php", "/empty.php"):
            with self.subTest(path=path):
                self.assertFalse(self.audit(path)["channels_imported"])


class ChannelIndexEndToEndTest(unittest.TestCase):
    """The audit must show up in report.json, STATUS.md and run-history.jsonl."""

    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_scraper_run_reports_the_index_and_an_unconfigured_feed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            cfg = root / "sources.json"
            cfg.write_text(json.dumps({
                "sources": [
                    {"name": "m3u", "type": "m3u", "url": f"{self.base}/index.m3u"},
                    # Mirrors the real dlive-sx-feed entry: skipped until configured.
                    {"name": "dlive-sx-feed", "type": "m3u", "enabled": True,
                     "optional": True, "url_env": "DLIVE_M3U_URL_TEST_UNSET"},
                ],
                "reference_checks": [
                    {"name": "dlive.sx", "type": "website_channel_index",
                     "url": f"{self.base}/24-7-channels.php",
                     "channel_href_regex": r"watch\.php\?id=\d+",
                     "note": "Catalogue counted only; not imported."},
                ],
            }), encoding="utf-8")
            out = root / "playlists"
            args = ["scraper.py", "--sources", str(cfg), "--out", str(out),
                    "--workers", "2", "--timeout", "2", "--label", "3:07 AM daily scrape"]
            with patch.object(sys, "argv", args), redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)

            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            audit = report["reference_checks"]["dlive.sx"]
            self.assertEqual(audit["channel_count"], 4)
            self.assertEqual(audit["ingest_status"], "player_pages_only")
            self.assertEqual(audit["sample_channels"][0], "ABC USA")
            self.assertEqual(report["sources"]["dlive-sx-feed"]["status"], "not_configured")
            self.assertEqual(report["sources"]["dlive-sx-feed"]["found"], 0)

            status_md = (out / "STATUS.md").read_text(encoding="utf-8")
            self.assertIn("| Reference | Check | Channels seen | Playlist links | Ingest status | Note |",
                          status_md)
            self.assertIn("player_pages_only", status_md)
            self.assertIn("dlive-sx-feed", status_md)
            self.assertIn("not_configured", status_md)

            history = [json.loads(line) for line in
                       (out / "run-history.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
            self.assertEqual(history[-1]["reference_checks"]["dlive.sx"]["channel_count"], 4)
            self.assertEqual(history[-1]["reference_checks"]["dlive.sx"]["ingest_status"],
                             "player_pages_only")
            self.assertEqual(history[-1]["run_type"], "regular_check")

            # No channel from the HTML index may reach a playlist.
            for playlist in ("PremiumTV.m3u", "PremiumTV_all.m3u"):
                body = (out / playlist).read_text(encoding="utf-8")
                self.assertNotIn("watch.php?id=", body)
                self.assertNotIn("ABC USA", body)


if __name__ == "__main__":
    unittest.main()
