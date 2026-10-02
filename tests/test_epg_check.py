"""Offline tests for the TV guide (EPG) verifier."""
import gzip
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
import epg_check  # noqa: E402

XMLTV = b"""<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="test">
  <channel id="MeTV.us"><display-name>MeTV</display-name></channel>
  <channel id="MeTVToons.us"><display-name>MeTV Toons</display-name></channel>
  <programme start="20260102120000 +0000" stop="20260102130000 +0000" channel="MeTV.us">
    <title>Test Show</title>
  </programme>
  <programme start="20260102130000 +0000" stop="20260102140000 +0000" channel="MeTVToons.us">
    <title>Cartoon</title>
  </programme>
</tv>
"""
XMLTV_NO_PROGRAMMES = b'<tv><channel id="A.us"><display-name>A</display-name></channel></tv>'
HTML = b"<html><body>404 not found</body></html>"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body=b"", ctype="application/xml"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        path = self.path
        if path == "/guide.xml.gz":
            self._send(200, gzip.compress(XMLTV))
        elif path == "/empty.xml.gz":
            self._send(200, gzip.compress(XMLTV_NO_PROGRAMMES))
        elif path == "/plain.xml":
            self._send(200, XMLTV)
        elif path == "/bad.xml.gz":
            self._send(200, gzip.compress(HTML), "text/html")
        elif path == "/stub.xml.gz":
            self._send(200, b"")
        elif path == "/gone.xml.gz":
            self._send(404, b"gone", "text/plain")
        elif path == "/blocked.xml.gz":
            self._send(403, b"denied", "text/plain")
        elif path == "/boom.xml.gz":
            self._send(500, b"server error", "text/plain")
        elif path == "/slow.xml.gz":
            time.sleep(2.5)
            self._send(200, gzip.compress(XMLTV))
        else:
            self._send(404, b"unknown", "text/plain")


class EpgCheckTest(unittest.TestCase):
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

    def write_playlist(self, guides, name="tv.m3u", extra_attr='cache="500"'):
        header = "#EXTM3U"
        if extra_attr:
            header += f" {extra_attr}"
        if guides:
            header += f' x-tvg-url="{",".join(guides)}"'
        path = self.out / name
        path.write_text("\n".join([header, "# playlist",
                                   "#EXTINF:-1 group-title=\"Live\",MeTV",
                                   "https://example.invalid/live.m3u8"]), encoding="utf-8")
        return path

    # -- header handling --------------------------------------------------- #
    def test_extract_guides_reads_both_attribute_names(self):
        path = self.out / "a.m3u"
        path.write_text('#EXTM3U x-tvg-url="https://a/g1.xml.gz,https://b/g2.xml.gz"\n'
                        "#EXTINF:-1,X\nhttps://example.invalid/x.m3u8\n", encoding="utf-8")
        self.assertEqual(epg_check.extract_guides(path),
                         ["https://a/g1.xml.gz", "https://b/g2.xml.gz"])

    def test_extract_guides_deduplicates(self):
        path = self.out / "b.m3u"
        path.write_text('#EXTM3U url-tvg="https://a/g1.xml.gz, https://a/g1.xml.gz"\n',
                        encoding="utf-8")
        self.assertEqual(epg_check.extract_guides(path), ["https://a/g1.xml.gz"])

    def test_rewrite_header_keeps_other_attributes(self):
        path = self.write_playlist([f"{self.base}/guide.xml.gz", f"{self.base}/gone.xml.gz"])
        changed = epg_check.rewrite_header(path, [f"{self.base}/guide.xml.gz"])
        self.assertTrue(changed)
        first = path.read_text(encoding="utf-8").splitlines()[0]
        self.assertIn(f'x-tvg-url="{self.base}/guide.xml.gz"', first)
        self.assertIn('cache="500"', first)
        self.assertNotIn("gone.xml.gz", first)

    def test_rewrite_header_returns_false_when_unchanged(self):
        path = self.write_playlist([f"{self.base}/guide.xml.gz"])
        self.assertFalse(epg_check.rewrite_header(path, [f"{self.base}/guide.xml.gz"]))

    # -- guide verification ------------------------------------------------ #
    def test_valid_gzipped_guide_is_ok(self):
        result = epg_check.verify_guide(f"{self.base}/guide.xml.gz", 10)
        self.assertEqual(result["status"], "ok")
        self.assertEqual(result["channels"], 2)
        self.assertEqual(result["programmes"], 2)
        self.assertEqual(result["sample_channel"], "MeTV")
        self.assertTrue(result["gzipped"])
        self.assertIn("2026", result["newest_programme"])

    def test_plain_xml_guide_is_ok(self):
        result = epg_check.verify_guide(f"{self.base}/plain.xml", 10)
        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["gzipped"])

    def test_guide_without_programmes_is_empty(self):
        result = epg_check.verify_guide(f"{self.base}/empty.xml.gz", 10)
        self.assertEqual(result["status"], "empty")

    def test_html_response_is_invalid(self):
        result = epg_check.verify_guide(f"{self.base}/bad.xml.gz", 10)
        self.assertEqual(result["status"], "invalid")
        self.assertIn("not XMLTV", result["reason"])

    def test_empty_response_is_invalid(self):
        result = epg_check.verify_guide(f"{self.base}/stub.xml.gz", 10)
        self.assertEqual(result["status"], "invalid")

    def test_404_is_offline(self):
        result = epg_check.verify_guide(f"{self.base}/gone.xml.gz", 10)
        self.assertEqual(result["status"], "offline")
        self.assertEqual(result["reason"], "HTTP 404")

    def test_403_is_blocked(self):
        result = epg_check.verify_guide(f"{self.base}/blocked.xml.gz", 10)
        self.assertEqual(result["status"], "blocked")

    def test_timeout_is_unreachable(self):
        result = epg_check.verify_guide(f"{self.base}/slow.xml.gz", 0.5, retries=0)
        self.assertEqual(result["status"], "unreachable")

    def test_malformed_url_is_invalid(self):
        result = epg_check.verify_guide("not-a-url", 5)
        self.assertEqual(result["status"], "invalid")

    # -- patching ---------------------------------------------------------- #
    def test_patch_drops_dead_guides_and_logs_them(self):
        path = self.write_playlist([f"{self.base}/guide.xml.gz",
                                    f"{self.base}/gone.xml.gz",
                                    f"{self.base}/bad.xml.gz"])
        report = epg_check.run(self.out, [path], 10, 6, 1, [], True, False, 0.25, "unit")
        patch = report["patch"]
        self.assertFalse(patch["aborted"])
        self.assertEqual(len(patch["removed"]), 2)
        first = path.read_text(encoding="utf-8").splitlines()[0]
        self.assertIn("guide.xml.gz", first)
        self.assertNotIn("gone.xml.gz", first)
        self.assertNotIn("bad.xml.gz", first)
        edits = (self.out / "logs" / "epg-check-edits.txt")
        epg_check.append_edit_log(self.out, report)
        self.assertIn("-removed guide", edits.read_text())

    def test_patch_adds_verified_extra_guides(self):
        path = self.write_playlist([f"{self.base}/guide.xml.gz"])
        report = epg_check.run(self.out, [path], 10, 6, 1,
                               [f"{self.base}/plain.xml"], True, False, 0.25, "unit")
        self.assertEqual(len(report["patch"]["added"]), 1)
        first = path.read_text(encoding="utf-8").splitlines()[0]
        self.assertIn("plain.xml", first)

    def test_patch_aborts_when_guides_are_unreachable(self):
        path = self.write_playlist([f"{self.base}/slow.xml.gz"])
        report = epg_check.run(self.out, [path], 0.5, 4, 0, [], True, False, 0.9, "unit")
        self.assertTrue(report["patch"]["aborted"])
        first = path.read_text(encoding="utf-8").splitlines()[0]
        self.assertIn("slow.xml.gz", first)

    def test_dry_run_changes_nothing(self):
        path = self.write_playlist([f"{self.base}/guide.xml.gz", f"{self.base}/gone.xml.gz"])
        before = path.read_text(encoding="utf-8")
        report = epg_check.run(self.out, [path], 10, 6, 1, [], True, True, 0.25, "unit")
        self.assertEqual(len(report["patch"]["removed"]), 1)
        self.assertEqual(path.read_text(encoding="utf-8"), before)

    # -- reports ------------------------------------------------------------ #
    def test_main_writes_reports(self):
        path = self.write_playlist([f"{self.base}/guide.xml.gz", f"{self.base}/gone.xml.gz"])
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = epg_check.main(["--out", str(self.out), "--playlist", str(path),
                                   "--patch", "--label", "unit test"])
        self.assertEqual(code, 0)
        checks = self.out / "checks"
        report = json.loads((checks / "epg-check.json").read_text())
        self.assertEqual(report["totals"].get("ok"), 1)
        self.assertEqual(report["totals"].get("offline"), 1)
        markdown = (checks / "EPG-CHECK.md").read_text()
        self.assertIn("TV guide", markdown)
        self.assertIn("guide.xml.gz", markdown)
        self.assertIn("Guides that failed", markdown)

    def test_main_without_playlists_fails_cleanly(self):
        with redirect_stdout(StringIO()):
            code = epg_check.main(["--out", str(self.out)])
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
