#!/usr/bin/env python3
"""Build the independent web client without changing either native release.

Uses the native apps' offline bundle builder and pure browser helpers, then
publishes compact, lazy-loadable JSON. All output paths are relative, so the
same artifact works at a domain root, on GitHub Pages, or in the live preview.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
ROOT = WEB.parent
sys.path.insert(0, str(ROOT / "android" / "tools"))
import build_bundle  # noqa: E402

SHARED = ("category-icons.js", "live-events.js", "personal.js", "health.js")
VENDORS = {
    "hls.js/dist/hls.min.js": "hls.min.js",
    "mpegts.js/dist/mpegts.js": "mpegts.js",
}


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    path.write_bytes(data)
    # Optional pre-compressed copies for nginx/static hosts. Hosts that ignore
    # them still work with the plain JSON files (and GitHub Pages gzip on CDN).
    path.with_suffix(path.suffix + ".gz").write_bytes(gzip.compress(data, mtime=0))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def build(out: Path, scope: str = "usa") -> dict:
    out = out.resolve()
    inside_source = (ROOT in out.parents or WEB in out.parents) and out not in (WEB / "dist", ROOT / "docs" / "web")
    if inside_source or out in (ROOT, WEB) or out in WEB.parents:
        raise ValueError("Output must be web/dist, docs/web, or a dedicated directory outside the source repository")
    playlist, guide = build_bundle.SCOPE_INPUTS[scope]
    with tempfile.TemporaryDirectory(prefix="premiumtv-web-") as tmp:
        bundle = Path(tmp) / "bundle"
        meta = build_bundle.build(str(ROOT / playlist), str(ROOT / guide),
                                  str(ROOT / build_bundle.DEFAULT_INDEX), str(bundle),
                                  build_bundle.DEFAULT_VERSION, scope=scope)
        channels = read_jsonl(bundle / "channels.jsonl")
        groups = read_jsonl(bundle / "groups.jsonl")
        programmes = read_jsonl(bundle / "epg.jsonl")
        if not channels or not groups:
            raise ValueError("The web library is empty")
        if any(not c.get("name") or not c.get("url", "").startswith(("https://", "http://")) for c in channels):
            raise ValueError("Invalid channel in source bundle")
        extras = {key: meta.pop(key, {}) for key in ("team_logos", "live_schedule", "vod_catalog")}
        if out.exists():
            shutil.rmtree(out)
        shutil.copytree(WEB / "src", out)
        for name in SHARED:
            target = out / "shared" / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / "macos" / "app" / "src" / "renderer" / name, target)
        (out / "vendor").mkdir(parents=True, exist_ok=True)
        for source, target in VENDORS.items():
            vendor = WEB / "node_modules" / source
            if not vendor.is_file():
                raise SystemExit("Missing player dependency. Run npm ci in web/ first.")
            shutil.copyfile(vendor, out / "vendor" / target)
            license_file = vendor.parents[1] / "LICENSE"
            if license_file.is_file():
                shutil.copyfile(license_file, out / "vendor" / (Path(target).stem + "-LICENSE.txt"))
        # Self-host the small synthetic test card: a playback smoke test must
        # not depend on a third-party CDN being available. Films stay remote.
        media = ROOT / "playlists" / "vod" / "media"
        shutil.copytree(media, out / "media")
        catalog = extras["vod_catalog"]
        for item in catalog.get("items", []):
            if item.get("test_card"):
                item["stream"] = "media/" + item["file"]
                item["streams"] = [item["stream"]]
                item["poster"] = "media/premiumtv-test-card.jpg"
        (out / "data").mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / playlist, out / "data" / "PremiumTV.m3u")
        dump(out / "data" / "channels.json", channels)
        dump(out / "data" / "groups.json", groups)
        dump(out / "data" / "epg.json", programmes)
        dump(out / "data" / "vod.json", catalog)
        dump(out / "data" / "events.json", {"team_logos": extras["team_logos"],
                                           "live_schedule": extras["live_schedule"]})
        digest = hashlib.sha256()
        for name in ("channels.json", "groups.json", "epg.json", "vod.json", "events.json"):
            digest.update((out / "data" / name).read_bytes())
        for path in sorted((WEB / "src").rglob("*")):
            if path.is_file():
                digest.update(path.read_bytes())
        meta["web_version"] = json.loads((WEB / "package.json").read_text())["version"]
        meta["build_id"] = digest.hexdigest()[:16]
        meta["platform"] = "web"
        dump(out / "data" / "meta.json", meta)
        # Version every application/data URL. A new deploy cannot be hidden by
        # an old immutable browser-cache entry. The service worker cache is
        # also scoped to this content hash.
        html = (out / "index.html").read_text(encoding="utf-8")
        for name in ("style.css", "app.js", "player.js", "store.js", "diagnostics.js"):
            html = html.replace(f'"{name}"', f'"{name}?v={meta["build_id"]}"')
        for name in SHARED:
            html = html.replace(f'"shared/{name}"', f'"shared/{name}?v={meta["build_id"]}"')
        (out / "index.html").write_text(html, encoding="utf-8")
        sw = (out / "sw.js").read_text(encoding="utf-8").replace("BUILD_ID_PLACEHOLDER", meta["build_id"])
        (out / "sw.js").write_text(sw, encoding="utf-8")
        # A useful, private, no-JavaScript fallback rather than an empty shell.
        links = "\n".join(f'<li><strong>{escape(c["name"])}</strong> — {escape(c["group"])}<br>'
                          f'<a href="{escape(c["url"])}" rel="noopener noreferrer">Open original stream</a></li>'
                          for c in channels)
        fallback = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>PremiumTV channel directory</title><style>body{{font:16px/1.6 system-ui;max-width:850px;margin:auto;padding:24px;background:#141619;color:#eee}}a{{color:#edc66d}}li{{margin:20px 0}}</style><h1>PremiumTV · Channel directory</h1><p>The interactive player needs JavaScript. You can still browse the published feeds or <a href="data/PremiumTV.m3u" download>download the M3U playlist</a> for VLC or another IPTV player. Original streams may not play directly in a browser.</p><ol>{links}</ol></html>'''
        (out / "directory.html").write_text(fallback, encoding="utf-8")
        manifest = {"name": "PremiumTV Web", "short_name": "PremiumTV", "id": "./", "start_url": "./",
                    "scope": "./", "display": "standalone", "background_color": "#141619",
                    "theme_color": "#141619", "description": "Live TV, movies and your personal shelves in a browser.",
                    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"}]}
        dump(out / "manifest.webmanifest", manifest)
        make_icons(out)
        report = {"build_id": meta["build_id"], "web_version": meta["web_version"], "scope": scope,
                  "channels": len(channels), "groups": len(groups), "programmes": len(programmes),
                  "movies": len(catalog.get("items", [])), "bytes": sum(p.stat().st_size for p in out.rglob("*") if p.is_file())}
        dump(out / "build-report.json", report)
        return report


def escape(value: str) -> str:
    import html
    return html.escape(str(value), quote=True)


def make_icons(out: Path) -> None:
    """Draw the app's TV mark as PNGs using only the standard library."""
    import struct
    import zlib
    for size in (192, 512):
        rows = []
        for y in range(size):
            row = bytearray([0])
            for x in range(size):
                u, v = x / size, y / size
                screen = .19 <= u <= .81 and .32 <= v <= .76
                inner = .25 <= u <= .62 and .40 <= v <= .67
                antenna = (.29 < v < .34 and abs(u - (.32 + (.34 - v) * .7)) < .022) or \
                          (.20 < v < .34 and abs(u - (.50 + (v - .20) * .55)) < .022)
                feet = .76 <= v < .85 and (abs(u - .31) < .025 or abs(u - .69) < .025)
                gold = (screen and not inner) or antenna or feet
                row.extend((237, 198, 109, 255) if gold else ((36, 40, 46, 255) if screen else (20, 22, 25, 255)))
            rows.append(bytes(row))
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))
        png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
        png += chunk(b"IDAT", zlib.compress(b"".join(rows), 9)) + chunk(b"IEND", b"")
        (out / f"icon-{size}.png").write_bytes(png)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scope", choices=sorted(build_bundle.SCOPE_INPUTS), default="usa")
    parser.add_argument("--out", type=Path, default=WEB / "dist")
    args = parser.parse_args()
    report = build(args.out, args.scope)
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
