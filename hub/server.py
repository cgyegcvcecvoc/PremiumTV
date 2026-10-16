#!/usr/bin/env python3
"""PremiumTV Download Hub — zero-dependency static + file server.

Serves the hub front-end plus every downloadable artifact in the repository
(playlists, EPG guides, Android APKs, zip bundles). Pure Python stdlib, so it
runs anywhere Python 3.8+ exists. Binds 0.0.0.0 so sandbox/preview proxies work.

Usage:  python3 hub/server.py [port]       (default 8000)
"""
import json
import mimetypes
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

HUB = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HUB)
STATIC = os.path.join(HUB, "static")
DIST = os.path.join(HUB, "dist")

# /get/<zone>/... -> real directory. Only these zones are reachable.
ZONES = {
    "playlists": os.path.join(ROOT, "playlists"),
    "categories": os.path.join(ROOT, "categories"),
    "EPG": os.path.join(ROOT, "EPG"),
    "build-out": os.path.join(ROOT, "build-out"),
    "bundles": os.path.join(DIST, "bundles"),
    "mac": os.path.join(DIST, "mac"),
}

# Only these extensions may leave the server through /get/.
ALLOWED_EXT = {".m3u", ".m3u8", ".xml", ".gz", ".apk", ".zip", ".txt", ".json", ".jsonl", ".md", ".png",
               ".dmg", ".pkg"}

MIME = {
    ".m3u": "audio/x-mpegurl",
    ".m3u8": "application/vnd.apple.mpegurl",
    ".xml": "application/xml",
    ".gz": "application/gzip",
    ".apk": "application/vnd.android.package-archive",
    ".zip": "application/zip",
    ".txt": "text/plain; charset=utf-8",
    ".md": "text/plain; charset=utf-8",
    ".json": "application/json",
    ".jsonl": "application/json",
    ".dmg": "application/x-apple-diskimage",
    ".pkg": "application/octet-stream",
}

# Always download these instead of rendering in the browser.
FORCE_ATTACH = {".apk", ".zip", ".gz", ".m3u", ".m3u8", ".dmg", ".pkg"}

CHUNK = 1 << 16


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "PremiumTVHub/1.0"

    # ---- helpers -----------------------------------------------------
    def _deny(self, code=404, msg="Not found"):
        body = msg.encode()
        self.send_response(code)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_file(self, path, download=False, cache="no-cache"):
        ext = os.path.splitext(path)[1].lower()
        ctype = MIME.get(ext) or mimetypes.guess_type(path)[0] or "application/octet-stream"
        try:
            size = os.path.getsize(path)
            f = open(path, "rb")
        except OSError:
            return self._deny()
        with f:
            start, end = 0, size - 1
            status = 200
            rng = self.headers.get("Range")
            m = re.match(r"bytes=(\d*)-(\d*)$", rng or "")
            if m and size and (m.group(1) or m.group(2)):
                if m.group(1):
                    start = int(m.group(1))
                    if m.group(2):
                        end = min(int(m.group(2)), size - 1)
                else:  # suffix range: last N bytes
                    start = max(size - int(m.group(2)), 0)
                if start > end or start >= size:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                status = 206
            length = end - start + 1
            self.send_response(status)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(length))
            self.send_header("Accept-Ranges", "bytes")
            self.send_header("Cache-Control", cache)
            self.send_header("Access-Control-Allow-Origin", "*")
            if status == 206:
                self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            if download or ext in FORCE_ATTACH:
                self.send_header("Content-Disposition",
                                 f'attachment; filename="{os.path.basename(path)}"')
            self.end_headers()
            if self.command == "HEAD":
                return
            f.seek(start)
            remaining = length
            while remaining > 0:
                chunk = f.read(min(CHUNK, remaining))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return
                remaining -= len(chunk)

    @staticmethod
    def _safe_join(base, rel):
        """Resolve rel under base; return None on traversal attempts."""
        p = os.path.realpath(os.path.join(base, rel))
        if p == os.path.realpath(base) or p.startswith(os.path.realpath(base) + os.sep):
            return p
        return None

    # ---- routing ------------------------------------------------------
    def do_GET(self):
        self.do_HEAD()

    def do_HEAD(self):
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        download = "dl=1" in (parsed.query or "")

        if path in ("/", "/index.html"):
            return self._send_file(os.path.join(STATIC, "index.html"))
        if path == "/data.json":
            return self._send_file(os.path.join(DIST, "data.json"))
        if path == "/healthz":
            return self._deny(200, "ok")

        if path.startswith("/assets/"):
            p = self._safe_join(os.path.join(STATIC, "assets"), path[len("/assets/"):])
            if p and os.path.isfile(p):
                return self._send_file(p, cache="no-cache")
            return self._deny()

        if path.startswith("/get/"):
            rest = path[len("/get/"):]
            zone, _, rel = rest.partition("/")
            base = ZONES.get(zone)
            if not base or not rel:
                return self._deny()
            p = self._safe_join(base, rel)
            if not p or not os.path.isfile(p):
                return self._deny()
            if os.path.splitext(p)[1].lower() not in ALLOWED_EXT:
                return self._deny(403, "File type not served")
            return self._send_file(p, download=download)

        return self._deny()

    def log_message(self, fmt, *args):  # quieter logs
        sys.stderr.write("%s %s\n" % (self.address_string(), fmt % args))


def main():
    # Priority: CLI arg > $PORT (Render/Railway/Fly inject this) > 8000
    port = int(sys.argv[1]) if len(sys.argv) > 1 else int(os.environ.get("PORT", "8000"))
    if not os.path.isfile(os.path.join(DIST, "data.json")):
        sys.exit("hub/dist/data.json missing — run: python3 hub/build_data.py")
    httpd = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    print(f"PremiumTV Download Hub serving on 0.0.0.0:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    main()
