#!/usr/bin/env python3
"""Offline acceptance gate for the static web export."""
import gzip
import json
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]
DIST = WEB / "dist"
ROOT = WEB.parent


def verify(dist=DIST):
    meta = json.loads((dist / "data/meta.json").read_text())
    channels = json.loads((dist / "data/channels.json").read_text())
    groups = json.loads((dist / "data/groups.json").read_text())
    assert meta["platform"] == "web" and meta["library_scope"] == "usa"
    assert len(channels) == meta["channel_count"] == sum(g["count"] for g in groups)
    assert len(groups) == meta["group_count"]
    assert len(json.loads((dist / "data/epg.json").read_text())) == meta["programme_count"]
    assert not list(dist.rglob("*.apk")) + list(dist.rglob("*.dmg")) + list(dist.rglob("*.pkg"))
    assert "BUILD_ID_PLACEHOLDER" not in (dist / "sw.js").read_text()
    for name in ("category-icons.js", "live-events.js", "personal.js", "health.js"):
        assert (dist / "shared" / name).read_bytes() == (ROOT / "macos/app/src/renderer" / name).read_bytes()
    for path in (dist / "data").glob("*.json.gz"):
        assert gzip.decompress(path.read_bytes()) == path.with_suffix("").read_bytes()
    html = (dist / "index.html").read_text()
    assert 'src="/' not in html and 'href="/' not in html
    assert (dist / "directory.html").is_file()
    assert (dist / "media/premiumtv-test-card.mp4").stat().st_size > 100000
    return meta


if __name__ == "__main__":
    result = verify()
    print(f"Web export verified: {result['channel_count']} feeds, build {result['build_id']}; no native release assets.")
