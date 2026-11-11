"""Tests for the published Pages link/asset checker (scripts/pages_site_check.py)."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import pages_site_check  # noqa: E402


class _QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):  # noqa: A002 - stdlib signature
        pass


def core_sw(build: str = "abc123") -> str:
    return f""""use strict";
const BUILD = "{build}";
const CORE = [
  "./",
  "index.html",
  "style.css",
  "app.js",
  "data/meta.json",
  "data/vod.json",
  "data/channels.json",
  "data/groups.json",
  "data/events.json",
  "manifest.webmanifest",
  "icon-192.png",
  "icon-512.png",
];
"""


class PagesSiteCheckTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.write_fixture()
        self.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(_QuietHandler, directory=str(self.root))
        )
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}/"

    def tearDown(self) -> None:
        self.server.shutdown()
        self.server.server_close()
        self._tmp.cleanup()

    def write(self, relative: str, content: str | bytes) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
        return path

    def write_fixture(self) -> None:
        self.write(
            "index.html",
            """<!doctype html>
<link rel="stylesheet" href="assets/style.css">
<script src="assets/app.js"></script>
<a href="web/">web player</a>
<a href="#top">top</a>
<a href="mailto:hello@example.com">mail</a>
<a href="https://example.com/elsewhere">elsewhere</a>
<img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=">
""",
        )
        self.write("assets/style.css", "body { color: #fff; }")
        self.write("assets/app.js", "console.log('site');")
        self.write(
            "web/index.html",
            """<!doctype html>
<link rel="stylesheet" href="style.css">
<link rel="manifest" href="manifest.webmanifest">
<script src="app.js"></script>
<img src="icon-192.png" alt="">
""",
        )
        self.write("web/style.css", "body { margin: 0; }")
        self.write("web/app.js", "console.log('web');")
        self.write("web/icon-192.png", b"\x89PNG\r\n\x1a\n192")
        self.write("web/icon-512.png", b"\x89PNG\r\n\x1a\n512")
        self.write("web/sw.js", core_sw())
        self.write(
            "web/manifest.webmanifest",
            json.dumps(
                {
                    "name": "PremiumTV Web",
                    "start_url": "./",
                    "scope": "./",
                    "icons": [
                        {"src": "icon-192.png", "sizes": "192x192"},
                        {"src": "icon-512.png", "sizes": "512x512"},
                    ],
                }
            ),
        )
        self.write(
            "web/data/meta.json",
            json.dumps(
                {
                    "build_id": "abc123",
                    "generated_utc": "2026-11-10 21:46 UTC",
                    "channel_count": 1,
                }
            ),
        )
        self.write("web/data/vod.json", json.dumps({"status": "coming_soon", "items": []}))
        for name in ("channels", "groups", "events"):
            self.write(f"web/data/{name}.json", json.dumps({name: []}))

    def check(self):
        return pages_site_check.run_checks(self.base, timeout=5, retries=0)

    def fail_urls(self, report) -> list[str]:
        return [finding.url for finding in report.failures]

    def test_the_healthy_site_passes(self) -> None:
        report = self.check()
        self.assertEqual([f.detail for f in report.failures], [])
        self.assertEqual(report.build_id, "abc123")
        self.assertGreaterEqual(report.pages, 2)
        self.assertTrue(
            any(f.url.endswith("/assets/style.css") and f.ok for f in report.findings)
        )

    def test_a_missing_root_asset_is_reported(self) -> None:
        (self.root / "assets/app.js").unlink()
        report = self.check()
        self.assertTrue(
            any(url.endswith("/assets/app.js") for url in self.fail_urls(report))
        )

    def test_a_missing_linked_page_is_reported(self) -> None:
        # Remove the whole app: deleting only index.html makes the test server
        # serve a directory listing, which real Pages does not do.
        shutil.rmtree(self.root / "web")
        report = self.check()
        self.assertTrue(any(url.endswith("/web/") for url in self.fail_urls(report)))

    def test_a_missing_manifest_icon_is_reported(self) -> None:
        (self.root / "web/icon-512.png").unlink()
        report = self.check()
        self.assertTrue(
            any(url.endswith("/web/icon-512.png") for url in self.fail_urls(report))
        )

    def test_a_stale_service_worker_build_is_reported(self) -> None:
        self.write("web/sw.js", core_sw("older-build"))
        report = self.check()
        messages = " ".join(finding.detail for finding in report.failures)
        self.assertIn("older-build", messages)
        self.assertIn("does not match", messages)

    def test_a_placeholder_service_worker_build_is_reported(self) -> None:
        self.write("web/sw.js", core_sw("BUILD_ID_PLACEHOLDER"))
        report = self.check()
        messages = " ".join(finding.detail for finding in report.failures)
        self.assertIn("placeholder", messages.lower())

    def test_a_missing_precached_asset_is_reported(self) -> None:
        (self.root / "web/data/groups.json").unlink()
        report = self.check()
        self.assertTrue(
            any(url.endswith("/web/data/groups.json") for url in self.fail_urls(report))
        )

    def test_external_and_non_http_references_are_ignored(self) -> None:
        report = self.check()
        self.assertEqual(report.failures, [])
        self.assertFalse(
            any("example.com" in finding.url for finding in report.findings)
        )


if __name__ == "__main__":
    unittest.main()
