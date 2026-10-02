"""Offline tests for the deep link checker; a local HTTP server stands in for streams."""
import gzip
import datetime as dt
import json
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import link_check  # noqa: E402
import scraper  # noqa: E402

TS_SEGMENT = b"\x47" + b"\x11" * 4095
MEDIA_PLAYLIST = "#EXTM3U\n#EXT-X-TARGETDURATION:4\n#EXT-X-MEDIA-SEQUENCE:1\n#EXTINF:4.0,\nseg1.ts\n"
MEDIA_PLAYLIST_DEAD = "#EXTM3U\n#EXT-X-TARGETDURATION:4\n#EXTINF:4.0,\nmissing.ts\n"
MASTER_PLAYLIST = ("#EXTM3U\n"
                   "#EXT-X-STREAM-INF:BANDWIDTH=800000\nv1.m3u8\n"
                   "#EXT-X-STREAM-INF:BANDWIDTH=4000000\nv2.m3u8\n")
MASTER_DEAD_VARIANT = ("#EXTM3U\n"
                       "#EXT-X-STREAM-INF:BANDWIDTH=4000000\ngone.m3u8\n")
MPD = ('<?xml version="1.0"?>\n<MPD xmlns="urn:mpeg:dash:schema:mpd:2011">'
       '<Period><AdaptationSet><Representation id="1" bandwidth="1000000"/></AdaptationSet></Period></MPD>')
EMPTY_MPD = '<MPD xmlns="urn:mpeg:dash:schema:mpd:2011"><Period></Period></MPD>'


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body=b"", ctype="application/vnd.apple.mpegurl"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        path = self.path
        if path == "/master.m3u8":
            self._send(200, MASTER_PLAYLIST.encode())
        elif path == "/v1.m3u8":
            self._send(200, MEDIA_PLAYLIST.encode())
        elif path == "/v2.m3u8":
            self._send(200, MEDIA_PLAYLIST.encode())
        elif path == "/seg1.ts":
            self._send(200, TS_SEGMENT, "video/mp2t")
        elif path == "/deadseg.m3u8":
            self._send(200, MEDIA_PLAYLIST_DEAD.encode())
        elif path == "/missing.ts":
            self._send(404, b"nope", "text/plain")
        elif path == "/stub.m3u8":
            self._send(200, b"", "text/plain")
        elif path == "/gone.m3u8":
            self._send(404, b"gone", "text/plain")
        elif path == "/deadvariant.m3u8":
            self._send(200, MASTER_DEAD_VARIANT.encode())
        elif path == "/direct.ts":
            self._send(200, TS_SEGMENT, "video/mp2t")
        elif path == "/page.m3u8":
            self._send(200, b"<html><body>not a stream</body></html>", "text/html")
        elif path == "/blocked.m3u8":
            self._send(403, b"denied", "text/plain")
        elif path == "/slow.m3u8":
            time.sleep(2.5)
            self._send(200, MEDIA_PLAYLIST.encode())
        elif path == "/dash.m3u8":
            self._send(200, MPD.encode(), "application/dash+xml")
        elif path == "/emptydash.m3u8":
            self._send(200, EMPTY_MPD.encode(), "application/dash+xml")
        elif path == "/gz.m3u8":
            body = gzip.compress(MEDIA_PLAYLIST.encode())
            self._send(200, body)
        else:
            self._send(404, b"unknown route", "text/plain")


class LinkCheckTest(unittest.TestCase):
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
        cls.thread.join(timeout=5)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, url, deep=True, timeout=5.0, retries=0, extra=None):
        channel = scraper.Channel(name="test", url=url, source="unit")
        if extra:
            channel.extra = extra
        return link_check.verify_link(channel, timeout, retries, deep)

    def write_playlist(self, name="channels.m3u", guides=True):
        header = "#EXTM3U" + (' x-tvg-url="https://example.invalid/guide.xml.gz"' if guides else "")
        text = "\n".join([
            header,
            "# test playlist",
            f'#EXTINF:-1 tvg-id="Master.us" group-title="Live",Master HLS',
            f"{self.base}/master.m3u8",
            "#EXTINF:-1 group-title=\"Live\",Direct TS",
            f"{self.base}/direct.ts",
            "#EXTINF:-1 group-title=\"Live\",Dead link",
            f"{self.base}/gone.m3u8",
            "#EXTINF:-1 group-title=\"Live\",HTML page",
            f"{self.base}/page.m3u8",
            "#EXTINF:-1 group-title=\"Live\",Blocked",
            f"{self.base}/blocked.m3u8",
            "#EXTINF:-1 group-title=\"Live\",Playlist without media",
            f"{self.base}/deadseg.m3u8",
            "#EXTINF:-1 group-title=\"Live\",DASH",
            f"{self.base}/dash.m3u8",
            "#EXTINF:-1 group-title=\"Other\",Unsupported scheme",
            "rtmp://example.invalid/live/stream",
            "",
        ])
        path = self.out / name
        path.write_text(text, encoding="utf-8")
        return path

    # -- parsing ---------------------------------------------------------- #
    def test_split_blocks_roundtrip_preserves_header(self):
        path = self.write_playlist()
        text = path.read_text(encoding="utf-8")
        header, blocks = link_check.split_blocks(text)
        self.assertEqual(len(header), 2)
        self.assertTrue(header[0].startswith("#EXTM3U x-tvg-url="))
        self.assertEqual(len(blocks), 8)
        self.assertEqual(link_check.blocks_to_text(header, blocks), text)

    def test_channel_from_block_reads_attributes_and_names(self):
        _, blocks = link_check.split_blocks(self.write_playlist().read_text())
        channel = link_check.channel_from_block(blocks[0], "unit")
        self.assertEqual(channel.name, "Master HLS")
        self.assertEqual(channel.attrs.get("tvg-id"), "Master.us")
        self.assertEqual(channel.url, f"{self.base}/master.m3u8")

    # -- classification --------------------------------------------------- #
    def test_master_playlist_with_segment_is_working(self):
        result = self.check(f"{self.base}/master.m3u8")
        self.assertEqual(result["status"], "working")
        self.assertTrue(result["segment_ok"])
        self.assertIn("hls", result["kind"])
        self.assertTrue(result["variant"].endswith("v2.m3u8"))

    def test_direct_ts_stream_is_working(self):
        result = self.check(f"{self.base}/direct.ts")
        self.assertEqual(result["status"], "working")

    def test_playlist_with_missing_segment_is_offline(self):
        result = self.check(f"{self.base}/deadseg.m3u8")
        self.assertEqual(result["status"], "offline")
        self.assertIn("playlist only", result["reason"])

    def test_master_with_dead_variant_is_offline(self):
        result = self.check(f"{self.base}/deadvariant.m3u8")
        self.assertEqual(result["status"], "offline")

    def test_segment_probe_uses_the_newest_segment(self):
        # Live playlists list oldest-first; the newest segment is the only one
        # still inside the server's DVR window.
        self.assertEqual(
            link_check.first_segment(
                "#EXTM3U\n#EXTINF:4,\nold.ts\n#EXTINF:4,\nnew.ts\n",
                "http://host/live.m3u8"),
            "http://host/new.ts")
        self.assertEqual(link_check.first_segment("#EXTM3U\n", "http://host/live.m3u8"), "")

    def test_deep_off_accepts_playlist_without_segment_probe(self):
        result = self.check(f"{self.base}/deadseg.m3u8", deep=False)
        self.assertEqual(result["status"], "working")

    def test_http_404_is_offline(self):
        result = self.check(f"{self.base}/gone.m3u8")
        self.assertEqual(result["status"], "offline")
        self.assertEqual(result["reason"], "HTTP 404")

    def test_html_page_is_offline(self):
        result = self.check(f"{self.base}/page.m3u8")
        self.assertEqual(result["status"], "offline")
        self.assertIn("html", result["reason"])

    def test_empty_body_is_offline(self):
        result = self.check(f"{self.base}/stub.m3u8")
        self.assertEqual(result["status"], "offline")

    def test_403_is_blocked_not_offline(self):
        result = self.check(f"{self.base}/blocked.m3u8")
        self.assertEqual(result["status"], "blocked")
        self.assertIn("403", result["reason"])

    def test_timeout_is_unreachable(self):
        result = self.check(f"{self.base}/slow.m3u8", timeout=0.5)
        self.assertEqual(result["status"], "unreachable")
        self.assertEqual(result["reason"], "timeout")

    def test_dash_manifest_is_working(self):
        result = self.check(f"{self.base}/dash.m3u8")
        self.assertEqual(result["status"], "working")
        self.assertEqual(result["kind"], "dash")

    def test_dash_without_representations_is_offline(self):
        result = self.check(f"{self.base}/emptydash.m3u8")
        self.assertEqual(result["status"], "offline")

    def test_non_http_scheme_is_unsupported(self):
        result = self.check("rtmp://example.invalid/live/stream")
        self.assertEqual(result["status"], "unsupported")

    def test_malformed_url_is_invalid(self):
        result = self.check("not-a-url")
        self.assertEqual(result["status"], "invalid")

    # -- patching --------------------------------------------------------- #
    def test_patch_removes_only_dead_entries(self):
        path = self.write_playlist()
        before = path.read_text(encoding="utf-8")
        loaded = link_check.load_playlists([path])
        results, _ = link_check.run_checks(loaded, 8, 4, 5.0, 0, True)
        patch = link_check.patch_playlists(loaded, results, 0.0, 0.9, dry_run=True)
        self.assertFalse(patch["aborted"])
        removed_urls = {item["url"] for item in patch["removed"]}
        self.assertIn(f"{self.base}/gone.m3u8", removed_urls)
        self.assertIn(f"{self.base}/page.m3u8", removed_urls)
        self.assertIn(f"{self.base}/deadseg.m3u8", removed_urls)
        self.assertNotIn(f"{self.base}/master.m3u8", removed_urls)
        self.assertNotIn(f"{self.base}/blocked.m3u8", removed_urls)
        self.assertNotIn("rtmp://example.invalid/live/stream", removed_urls)
        # A dry run must not touch the file.
        self.assertEqual(path.read_text(encoding="utf-8"), before)

    def test_patch_rewrites_file_and_keeps_guides(self):
        path = self.write_playlist()
        loaded = link_check.load_playlists([path])
        results, _ = link_check.run_checks(loaded, 8, 4, 5.0, 0, True)
        link_check.patch_playlists(loaded, results, 0.0, 0.9, dry_run=False)
        text = path.read_text(encoding="utf-8")
        self.assertIn('x-tvg-url="https://example.invalid/guide.xml.gz"', text.splitlines()[0])
        self.assertIn("Master HLS", text)
        self.assertIn("Blocked", text)
        self.assertNotIn("Dead link", text)
        self.assertNotIn("HTML page", text)
        self.assertNotIn("Playlist without media", text)

    def test_patch_aborts_when_too_few_links_work(self):
        path = self.out / "offline.m3u"
        path.write_text("\n".join(["#EXTM3U",
                                   "#EXTINF:-1,A",
                                   f"{self.base}/slow.m3u8",
                                   "#EXTINF:-1,B",
                                   f"{self.base}/slow.m3u8"]), encoding="utf-8")
        loaded = link_check.load_playlists([path])
        results, _ = link_check.run_checks(loaded, 4, 2, 0.4, 0, True)
        patch = link_check.patch_playlists(loaded, results, 0.5, 0.9, dry_run=False)
        self.assertTrue(patch["aborted"])
        self.assertEqual(patch["removed_total"], 0)
        self.assertIn("below", patch["abort_reason"])
        self.assertIn("slow.m3u8", path.read_text(encoding="utf-8"))

    def test_max_remove_ratio_skips_a_playlist(self):
        path = self.out / "mostlydead.m3u"
        lines = ["#EXTM3U", "#EXTINF:-1,Alive", f"{self.base}/direct.ts"]
        for index in range(6):
            lines += [f"#EXTINF:-1,Dead {index}", f"{self.base}/gone.m3u8"]
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        loaded = link_check.load_playlists([path])
        results, _ = link_check.run_checks(loaded, 8, 4, 5.0, 0, True)
        patch = link_check.patch_playlists(loaded, results, 0.0, 0.35, dry_run=False)
        self.assertEqual(patch["removed_total"], 0)
        self.assertEqual(len(patch["skipped_files"]), 1)
        self.assertIn("gone.m3u8", path.read_text(encoding="utf-8"))

    # -- reports ---------------------------------------------------------- #
    def test_main_writes_reports_and_edit_log(self):
        path = self.write_playlist()
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = link_check.main(["--out", str(self.out), "--playlist", str(path),
                                    "--workers", "8", "--timeout", "5", "--retries", "0",
                                    "--patch", "--min-working-ratio", "0.1",
                                    "--max-remove-ratio", "0.9",
                                    "--label", "unit test"])
        self.assertEqual(code, 0)
        checks = self.out / "checks"
        self.assertTrue((checks / "link-check.json").exists())
        self.assertTrue((checks / "LINK-CHECK.md").exists())
        report = json.loads((checks / "link-check.json").read_text())
        self.assertEqual(report["label"], "unit test")
        self.assertEqual(report["playlist_count"], 1)
        self.assertGreater(report["totals"].get("working", 0), 0)
        self.assertGreater(report["totals"].get("offline", 0), 0)
        markdown = (checks / "LINK-CHECK.md").read_text()
        self.assertIn("Deep link check", markdown)
        self.assertIn("per playlist", markdown.lower())
        edit_log = self.out / "logs" / "link-check-edits.txt"
        self.assertTrue(edit_log.exists())
        self.assertIn("-removed", edit_log.read_text())

    def test_patch_records_a_quarantine_for_the_next_scrape(self):
        path = self.write_playlist()
        with redirect_stdout(StringIO()):
            link_check.main(["--out", str(self.out), "--playlist", str(path),
                             "--workers", "8", "--timeout", "5", "--retries", "0",
                             "--patch", "--min-working-ratio", "0.1",
                             "--max-remove-ratio", "0.9"])
        quarantine = json.loads((self.out / "checks" / "quarantine.json").read_text())
        dead_url = f"{self.base}/gone.m3u8"
        self.assertIn(dead_url, quarantine["entries"])
        entry = quarantine["entries"][dead_url]
        self.assertEqual(entry["hits"], 1)
        self.assertEqual(entry["status"], "offline")
        self.assertNotIn(f"{self.base}/master.m3u8", quarantine["entries"])
        # The scraper holds quarantined links back so a shallow check cannot
        # publish them again a few hours later. It sees the link again because
        # the index it comes from still lists it - the patched playlist does not.
        reimported = self.write_playlist(name="reimported.m3u")
        channels, _ = scraper.parse_m3u(reimported.read_text(), "unit")
        held = scraper.apply_quarantine(channels, self.out / "checks" / "quarantine.json", 7.0)
        self.assertGreaterEqual(held, 1)
        statuses = {channel.url: channel.status for channel in channels}
        self.assertEqual(statuses[dead_url], "dead")
        self.assertNotEqual(statuses[f"{self.base}/master.m3u8"], "dead")

    def test_quarantine_entries_expire(self):
        stale = {
            "entries": {
                "http://dead.invalid/x.m3u8": {
                    "name": "x", "first_seen_utc": "2020-01-01T00:00:00Z",
                    "last_seen_utc": "2020-01-01T00:00:00Z",
                    "reason": "HTTP 404", "status": "offline", "hits": 3,
                }
            }
        }
        path = self.out / "checks" / "quarantine.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(stale), encoding="utf-8")
        self.assertEqual(
            scraper.load_quarantine(path, 7.0), {})
        fresh = dict(stale["entries"])
        fresh["http://dead.invalid/x.m3u8"] = dict(
            fresh["http://dead.invalid/x.m3u8"],
            last_seen_utc=dt.datetime.now(dt.timezone.utc).isoformat())
        path.write_text(json.dumps({"entries": fresh}), encoding="utf-8")
        self.assertIn("http://dead.invalid/x.m3u8", scraper.load_quarantine(path, 7.0))

    def test_main_without_playlists_fails_cleanly(self):
        with redirect_stdout(StringIO()):
            code = link_check.main(["--out", str(self.out)])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
