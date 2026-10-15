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
# A redirector (jmp2.uk, i.mjh.nz) answers with a 302 to the real master
# playlist, whose variant and segment URIs are relative to *that* address.
REDIRECTED_MASTER = "#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=2000000\nvariant.m3u8?token=abc\n"
REDIRECTED_MEDIA = "#EXTM3U\n#EXT-X-TARGETDURATION:4\n#EXTINF:4.0,\nsegment.ts?token=abc\n"
MEDIA_PLAYLIST_LIMITED = "#EXTM3U\n#EXT-X-TARGETDURATION:4\n#EXTINF:4.0,\nratelimited.ts\n"
MASTER_BUSY_VARIANT = "#EXTM3U\n#EXT-X-STREAM-INF:BANDWIDTH=4000000\nbusy.m3u8\n"
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
        elif path == "/hop/plu-123.m3u8":
            self.send_response(302)
            self.send_header("Location", "/stitch/hls/channel/123/master.m3u8?sid=1")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif path == "/stitch/hls/channel/123/master.m3u8?sid=1":
            self._send(200, REDIRECTED_MASTER.encode())
        elif path == "/stitch/hls/channel/123/variant.m3u8?token=abc":
            self._send(200, REDIRECTED_MEDIA.encode())
        elif path == "/stitch/hls/channel/123/segment.ts?token=abc":
            self._send(200, TS_SEGMENT, "video/mp2t")
        elif path == "/limited.m3u8":
            self._send(200, MEDIA_PLAYLIST_LIMITED.encode())
        elif path == "/ratelimited.ts":
            self._send(429, b"slow down", "text/plain")
        elif path == "/busyvariant.m3u8":
            self._send(200, MASTER_BUSY_VARIANT.encode())
        elif path == "/busy.m3u8":
            self._send(503, b"busy", "text/plain")
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
            '#EXTINF:-1 tvg-id="Master.us" group-title="Live",Master HLS',
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

    def test_redirected_master_resolves_variants_against_the_final_url(self):
        # Resolving "variant.m3u8" against the redirector's own URL asked the
        # redirector for a path it does not serve; on 2026-10-13 that removed
        # ~1,700 working jmp2.uk channels as "variant HTTP 414/404".
        result = self.check(f"{self.base}/hop/plu-123.m3u8")
        self.assertEqual(result["status"], "working", result["reason"])
        self.assertTrue(result["segment_ok"])
        self.assertEqual(result["variant"],
                         f"{self.base}/stitch/hls/channel/123/variant.m3u8?token=abc")

    def test_rate_limited_segment_is_unreachable_not_offline(self):
        # HTTP 429 means the CDN was busy during the sweep, not that the
        # channel died: the link must stay published and out of the quarantine.
        result = self.check(f"{self.base}/limited.m3u8")
        self.assertEqual(result["status"], "unreachable")
        self.assertIn("429", result["reason"])

    def test_server_error_on_the_variant_is_unreachable_not_offline(self):
        result = self.check(f"{self.base}/busyvariant.m3u8")
        self.assertEqual(result["status"], "unreachable")
        self.assertEqual(result["reason"], "variant HTTP 503")

    def test_sub_request_classification_matches_the_playlist_rules(self):
        self.assertEqual(link_check.sub_request_status(404, "HTTP 404"), "offline")
        self.assertEqual(link_check.sub_request_status(410, "HTTP 410"), "offline")
        self.assertEqual(link_check.sub_request_status(403, "HTTP 403"), "offline")
        for code in (408, 414, 425, 429, 500, 502, 503, 504):
            self.assertEqual(link_check.sub_request_status(code, f"HTTP {code}"), "unreachable")
        self.assertEqual(link_check.sub_request_status(0, "timeout"), "unreachable")
        self.assertEqual(link_check.sub_request_status(0, "RemoteDisconnected"), "unreachable")
        self.assertEqual(link_check.sub_request_status(0, "dns lookup failed"), "offline")
        self.assertEqual(link_check.sub_request_status(0, "connection refused"), "offline")

    def test_quarantine_keeps_only_entries_the_current_rules_call_dead(self):
        now = dt.datetime.now(dt.timezone.utc).isoformat()

        def entry(reason, **extra):
            return {"name": reason, "first_seen_utc": now, "last_seen_utc": now,
                    "reason": reason, "status": "offline", "hits": 1, **extra}

        entries = {
            "http://a.invalid/404.m3u8": entry("HTTP 404"),
            "http://a.invalid/seg404.m3u8": entry("playlist only, HTTP 404"),
            "http://a.invalid/html.m3u8": entry("html page, not a stream"),
            "http://a.invalid/429.m3u8": entry("playlist only, HTTP 429"),
            "http://a.invalid/503.m3u8": entry("playlist only, HTTP 503"),
            "http://a.invalid/timeout.m3u8": entry("variant HTTP timeout"),
            "http://jmp2.invalid/plu-1.m3u8": entry("variant HTTP 414"),
            "http://jmp2.invalid/plu-2.m3u8": entry("variant HTTP 404"),
            "http://a.invalid/new-variant-404.m3u8": entry("variant HTTP 404", rules=2),
            "http://a.invalid/revived.m3u8": entry("HTTP 404"),
        }
        path = self.out / "checks" / "quarantine.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"entries": entries}), encoding="utf-8")
        report = {"finished_utc": now}
        results = {"http://a.invalid/revived.m3u8": {"status": "working"}}
        link_check.update_quarantine(self.out, report, {"removed": []}, 7.0, results)
        kept = set(json.loads(path.read_text(encoding="utf-8"))["entries"])
        self.assertEqual(kept, {
            "http://a.invalid/404.m3u8",
            "http://a.invalid/seg404.m3u8",
            "http://a.invalid/html.m3u8",
            "http://a.invalid/new-variant-404.m3u8",
        })

    def test_new_quarantine_entries_record_the_rules_version(self):
        now = dt.datetime.now(dt.timezone.utc).isoformat()
        link_check.update_quarantine(
            self.out, {"finished_utc": now},
            {"removed": [{"url": "http://a.invalid/gone.m3u8", "name": "Gone",
                          "reason": "variant HTTP 404", "status": "offline"}]}, 7.0)
        entries = json.loads((self.out / "checks" / "quarantine.json").read_text())["entries"]
        self.assertEqual(entries["http://a.invalid/gone.m3u8"]["rules"], link_check.QUARANTINE_RULES)
        # ...so the next run keeps it instead of discarding it as pre-fix data.
        link_check.update_quarantine(self.out, {"finished_utc": now}, {"removed": []}, 7.0)
        entries = json.loads((self.out / "checks" / "quarantine.json").read_text())["entries"]
        self.assertIn("http://a.invalid/gone.m3u8", entries)

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

    def test_load_quarantine_ignores_entries_the_current_rules_call_dead(self):
        # The scraper's reader must agree with the deep check's writer: a
        # pre-fix "variant HTTP 414"/"variant HTTP 404" (the 2026-10-13
        # redirector bug) or a transient "playlist only, HTTP 429" says nothing
        # about the stream, so it must not hold a channel back - even though
        # the entry is still sitting on disk between two deep checks.
        now = dt.datetime.now(dt.timezone.utc).isoformat()

        def entry(reason, **extra):
            return {"name": reason, "first_seen_utc": now, "last_seen_utc": now,
                    "reason": reason, "status": "offline", "hits": 1, **extra}

        entries = {
            "http://jmp2.invalid/plu-1.m3u8": entry("variant HTTP 414"),
            "http://jmp2.invalid/plu-2.m3u8": entry("variant HTTP 404"),
            "http://a.invalid/429.m3u8": entry("playlist only, HTTP 429"),
            "http://a.invalid/timeout.m3u8": entry("variant HTTP timeout"),
            "http://a.invalid/gone.m3u8": entry("HTTP 404"),
            "http://a.invalid/new-variant-404.m3u8": entry("variant HTTP 404", rules=2),
        }
        path = self.out / "checks" / "quarantine.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"entries": entries}), encoding="utf-8")
        kept = scraper.load_quarantine(path, 7.0)
        self.assertEqual(set(kept), {
            "http://a.invalid/gone.m3u8",
            "http://a.invalid/new-variant-404.m3u8",
        })

    # -- the biweekly archive scope --------------------------------------- #
    def test_archives_scope_covers_every_playlist_no_daily_run_patches(self):
        out = self.out / "playlists"
        (out / "categories").mkdir(parents=True)
        (out / "sources").mkdir(parents=True)
        (out / "countries").mkdir(parents=True)
        shelf = self.out / "categories"
        (shelf / "USA").mkdir(parents=True)
        for path in (out / "PremiumTV.m3u", out / "AE_Channels.m3u",
                     out / "Priority_Channels.m3u", out / "PremiumTV_all.m3u",
                     out / "categories" / "Sports.m3u", out / "categories" / "Sports_Backups.m3u",
                     out / "sources" / "iptv-org.m3u", out / "countries" / "UK.m3u",
                     shelf / "USA.m3u", shelf / "USA" / "Sports.m3u"):
            path.write_text("#EXTM3U\n", encoding="utf-8")

        daily = {path.name for path in link_check.collect_targets(out, [], True, False)}
        swept = {path.name for path in link_check.collect_targets(out, [], True, False,
                                                                   True, shelf)}
        # Everything the nightly and quick runs already reach stays in scope...
        for name in ("PremiumTV.m3u", "AE_Channels.m3u", "UK.m3u"):
            self.assertIn(name, daily)
        # ...and the archive sweep adds the files no daily run ever rewrites.
        for name in ("Priority_Channels.m3u", "PremiumTV_all.m3u", "Sports.m3u",
                     "Sports_Backups.m3u", "iptv-org.m3u", "USA.m3u"):
            self.assertNotIn(name, daily, f"{name} should not be a daily target")
            self.assertIn(name, swept, f"{name} should be in the archive sweep")
        self.assertTrue(daily <= swept)
        # Nothing is listed twice by --all together with --archives.
        both = link_check.collect_targets(out, [], True, False, True, shelf)
        self.assertEqual(len(both), len({str(path.resolve()) for path in both}))

    def test_archive_sweep_reports_premiumtv_all_without_pruning_it(self):
        # PremiumTV_all.m3u is documented as "all unique links found, including dead
        # or unverified links", so the sweep must count its dead links - that is how
        # they reach the quarantine and stay out of the player - and leave them in.
        out = self.out / "playlists"
        out.mkdir(parents=True, exist_ok=True)
        playlist = out / "PremiumTV_all.m3u"
        playlist.write_text("\n".join([
            "#EXTM3U",
            '#EXTINF:-1 group-title="Live",Working',
            f"{self.base}/master.m3u8",
            '#EXTINF:-1 group-title="Live",Gone',
            f"{self.base}/gone.m3u8",
            "",
        ]), encoding="utf-8")
        player = out / "Priority_Channels.m3u"
        player.write_text("\n".join([
            "#EXTM3U",
            '#EXTINF:-1 group-title="Live",Gone',
            f"{self.base}/gone.m3u8",
            "",
        ]), encoding="utf-8")
        self.assertTrue(link_check.is_report_only(playlist))
        self.assertFalse(link_check.is_report_only(player))

        loaded = link_check.load_playlists([playlist, player])
        results, _ = link_check.run_checks(loaded, 8, 4, 5.0, 0, True)
        before = playlist.read_text(encoding="utf-8")
        patch = link_check.patch_playlists(loaded, results, 0.0, 1.0, dry_run=False,
                                           report_only={playlist})
        self.assertEqual(playlist.read_text(encoding="utf-8"), before)
        self.assertEqual(len(patch["reported_only"]), 1)
        self.assertEqual(patch["reported_only"][0]["dead"], 1)
        self.assertEqual(patch["reported_only"][0]["entries"], 2)
        # The file with no archive exemption loses its dead link under the same run.
        self.assertNotIn("gone.m3u8", player.read_text(encoding="utf-8"))

    def test_biweekly_archive_step_arguments_parse(self):
        # The archive sweep passed --report-suffix "-archives": argparse reads a
        # value that starts with "-" as another option and exits with code 2, so
        # the step crashed in two seconds and failed every biweekly run.
        import shlex
        workflow = (Path(__file__).resolve().parents[1] / ".github" / "workflows"
                    / "biweekly-cleanup.yml").read_text(encoding="utf-8")
        start = workflow.index("args=(--archives")
        block = workflow[start + len("args=("):workflow.index(")", start)]
        args = link_check.build_parser().parse_args(shlex.split(block) + ["--deep", "--patch"])
        self.assertTrue(args.archives)
        self.assertEqual(args.report_suffix, "-archives")
        self.assertEqual(args.quarantine_days, 21.0)

    def test_main_without_playlists_fails_cleanly(self):
        with redirect_stdout(StringIO()):
            code = link_check.main(["--out", str(self.out)])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
