#!/usr/bin/env python3
"""Turn the repository's M3U playlists and XMLTV guide into app bundle assets.

The Android app ships with the channel list and the guide baked in, so this
script is the single, testable bridge between the repository data and what the
APK contains.  Nothing here touches the network: it only reads files that the
repository already publishes.

Inputs (defaults match the USA bundle the app ships):

    playlists/live/USA.m3u        the checked, confirmed-working channel list
    EPG/USA.xml                   the XMLTV guide for exactly those channels
    categories/index.json         the published group order (optional)

Outputs, written to the app's asset folder:

    bundle/meta.json      version, source files, counts, guide window, refresh URLs
    bundle/channels.jsonl one JSON object per channel (streaming-parsed on device)
    bundle/groups.jsonl   one JSON object per category, in published order
    bundle/epg.jsonl      one JSON object per programme

JSON Lines is used instead of one big JSON array so the app can stream it with
android.util.JsonReader without ever holding 9,000 programmes in memory.

Usage:
    python android/tools/build_bundle.py                       # USA bundle
    python android/tools/build_bundle.py --playlist ... --guide ...
    python android/tools/build_bundle.py --check               # verify only
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEFAULT_SCOPE = "usa"
# The stable scope is built from playlists/live/USA.m3u - the feed
# scripts/legacy_sunset.py keeps current for builds that can still update.
# playlists/countries/USA.m3u is the *legacy* feed baked into 1.0.0-1.0.4; it
# is pinned on the published end-of-support date, so a build must not be pointed
# at it or it would stop receiving channels with the versions it replaces.
SCOPE_INPUTS = {
    "usa": ("playlists/live/USA.m3u", "EPG/USA.xml"),
    "all": ("playlists/PremiumTV.m3u", "EPG/PremiumTV.xml"),
}
DEFAULT_INDEX = "categories/index.json"
DEFAULT_OUT = os.path.join("android", "app", "src", "main", "assets", "bundle")
DEFAULT_VERSION = "1.0.6.1"

# The repository the app refreshes from.  These are the same raw URLs the
# playlists advertise; they only resolve for a device if the repository is
# public (or mirrored somewhere public).  The app reports a failure honestly
# instead of pretending the refresh worked.
RAW_BASE = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main"

ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')
# Decorative prefixes/suffixes that only add noise on a TV screen.
NOISE_PREFIX_RE = re.compile(r"^[\s\u2605\u2606\u2b50\u2728\u2022\u25b6\-\u2013]+")


def clean_name(raw: str) -> str:
    """Trim decorative noise but keep country flags and quality markers."""
    name = NOISE_PREFIX_RE.sub("", raw or "").strip()
    name = re.sub(r"\s{2,}", " ", name)
    return name or (raw or "").strip() or "Unknown channel"


def parse_attrs(line: str) -> dict:
    return {k: v for k, v in ATTR_RE.findall(line)}


def extinf_name(line: str, attrs: dict) -> str:
    """Read the display name after the first comma outside quoted attributes.

    Channel names may contain commas, and quoted attribute values may contain
    them too. Splitting at the last comma silently truncated names in every
    generated app bundle.
    """
    quoted = False
    for index, char in enumerate(line):
        if char == '"':
            quoted = not quoted
        elif char == "," and not quoted:
            return line[index + 1:].strip()
    return (attrs.get("tvg-name") or "").strip()


def parse_m3u(path: str) -> tuple[list[dict], str]:
    """Parse an M3U playlist into channel dicts.

    Handles the tags the repository actually writes: #EXTINF with tvg-*
    attributes, #EXTVLCOPT / #KODIPROP headers (referrer, user-agent, origin)
    and the x-tvg-url guide list on the #EXTM3U header line.
    """
    channels: list[dict] = []
    guide_urls: list[str] = []
    pending: dict | None = None
    pending_opts: dict = {}

    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        for raw_line in handle:
            line = raw_line.rstrip("\r\n")
            if not line.strip():
                continue

            if line.startswith("#EXTM3U"):
                head = parse_attrs(line)
                if head.get("x-tvg-url"):
                    guide_urls = [u.strip() for u in head["x-tvg-url"].split(",") if u.strip()]
                continue

            if line.startswith("#EXTINF"):
                # Any stream options seen after the previous entry are dropped.
                pending_opts = {}
                attrs = parse_attrs(line)
                name = extinf_name(line, attrs)
                pending = {
                    "id": (attrs.get("tvg-id") or "").strip(),
                    "name": clean_name(name),
                    "logo": (attrs.get("tvg-logo") or "").strip(),
                    "group": (attrs.get("group-title") or "Other").strip() or "Other",
                    "country": (attrs.get("tvg-country") or "").strip().upper(),
                    "chno": (attrs.get("tvg-chno") or "").strip(),
                    "ua": (attrs.get("http-user-agent") or "").strip(),
                    "referrer": (attrs.get("http-referrer") or "").strip(),
                }
                continue

            opt = None
            if line.startswith("#EXTVLCOPT:"):
                opt = line[len("#EXTVLCOPT:"):]
            elif line.startswith("#KODIPROP:"):
                opt = line[len("#KODIPROP:"):]
            if opt:
                key, _, value = opt.partition("=")
                key = key.strip().lower()
                value = value.strip()
                if key in ("http-referrer", "referer"):
                    pending_opts["referrer"] = value
                elif key in ("http-user-agent", "user-agent"):
                    pending_opts["ua"] = value
                elif key in ("http-origin", "origin"):
                    pending_opts["origin"] = value
                continue

            if line.startswith("#"):
                continue

            url = line.strip()
            if not url or url.startswith("#"):
                continue
            if pending is None:
                # A bare URL with no #EXTINF: keep it, named after the URL.
                pending = {
                    "id": "", "name": clean_name(url.rsplit("/", 1)[-1]),
                    "logo": "", "group": "Other", "country": "", "chno": "",
                    "ua": "", "referrer": "",
                }
            pending["url"] = url
            pending.setdefault("origin", "")
            pending.update(pending_opts)
            pending_opts = {}
            if not pending["id"]:
                pending["id"] = re.sub(r"[^a-z0-9]+", ".", pending["name"].lower()).strip(".")
            channels.append(pending)
            pending = None

    return channels, (guide_urls[0] if guide_urls else "")


def xmltv_time(value: str) -> int:
    """Parse a complete XMLTV timestamp, returning epoch seconds or zero.

    Reject trailing junk, impossible calendar dates and out-of-range UTC
    offsets instead of allowing permissive parsers to normalize them.
    """
    value = (value or "").strip()
    if not value:
        return 0
    match = re.fullmatch(r"(\d{14})(?:\s*([+-])(\d{2})(\d{2}))?", value)
    if not match:
        return 0
    stamp, sign, hours_text, minutes_text = match.groups()
    try:
        if sign:
            if int(hours_text) > 23 or int(minutes_text) > 59:
                return 0
            offset = f"{sign}{hours_text}{minutes_text}"
        else:
            offset = "+0000"
        moment = datetime.strptime(stamp + " " + offset, "%Y%m%d%H%M%S %z")
    except ValueError:
        return 0
    return int(moment.astimezone(timezone.utc).timestamp())


def child_text(node: ET.Element, tag: str) -> str:
    found = node.find(tag)
    if found is None or found.text is None:
        return ""
    return " ".join(found.text.split())


def parse_xmltv(path: str) -> list[dict]:
    """Stream an XMLTV guide into programme dicts (start/stop as epoch seconds)."""
    programmes: list[dict] = []
    for event, node in ET.iterparse(path, events=("end",)):
        if node.tag != "programme":
            continue
        start = xmltv_time(node.get("start", ""))
        stop = xmltv_time(node.get("stop", ""))
        channel = (node.get("channel") or "").strip()
        if not channel or not start:
            node.clear()
            continue
        if stop <= start:
            stop = start + 1800
        categories = [c.text.strip() for c in node.findall("category") if c.text]
        episode = node.find("sub-title")
        programmes.append({
            "c": channel,
            "s": start,
            "e": stop,
            "t": child_text(node, "title") or "(no title)",
            "d": child_text(node, "desc"),
            "g": "; ".join([c for c in categories if c]),
            "i": (node.find("icon").get("src") if node.find("icon") is not None else "") or "",
            "ep": (episode.text or "").strip() if episode is not None and episode.text else "",
        })
        node.clear()
    programmes.sort(key=lambda p: (p["c"], p["s"]))
    return programmes


def load_group_order(path: str) -> list[str]:
    """Published category order from categories/index.json, when available."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError):
        return []
    order = data.get("order") or []
    return [str(name) for name in order if str(name).strip()]


def order_groups(channels: list[dict], published_order: list[str]) -> list[dict]:
    counts: dict[str, int] = {}
    for channel in channels:
        counts[channel["group"]] = counts.get(channel["group"], 0) + 1

    names = [name for name in published_order if name in counts]
    rest = sorted((n for n in counts if n not in names), key=lambda n: (-counts[n], n.lower()))
    return [{"name": name, "count": counts[name]} for name in names + rest]


def write_jsonl(path: str, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            handle.write("\n")


def build(playlist: str, guide: str, index: str, out_dir: str, version: str,
          scope: str = DEFAULT_SCOPE) -> dict:
    channels, header_guide = parse_m3u(playlist)
    programmes = parse_xmltv(guide)
    published_order = load_group_order(index)
    groups = order_groups(channels, published_order)

    guide_url = header_guide or "%s/%s" % (RAW_BASE, os.path.relpath(guide, REPO_ROOT).replace(os.sep, "/"))
    playlist_url = "%s/%s" % (RAW_BASE, os.path.relpath(playlist, REPO_ROOT).replace(os.sep, "/"))

    # Only keep guide entries for channels we actually publish, and only keep
    # listings that have not already finished.
    known = {c["id"] for c in channels if c["id"]}
    now = int(datetime.now(timezone.utc).timestamp())
    programmes = [p for p in programmes if p["c"] in known and p["e"] > now - 6 * 3600]

    starts = [p["s"] for p in programmes] or [now]
    stops = [p["e"] for p in programmes] or [now]

    os.makedirs(out_dir, exist_ok=True)
    write_jsonl(os.path.join(out_dir, "channels.jsonl"), channels)
    write_jsonl(os.path.join(out_dir, "groups.jsonl"), groups)
    write_jsonl(os.path.join(out_dir, "epg.jsonl"), programmes)

    meta = {
        "version": version,
        "library_scope": scope,
        "preview_features": ["cable-guide"] if scope == "all" else [],
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "playlist": os.path.relpath(playlist, REPO_ROOT).replace(os.sep, "/"),
        "guide": os.path.relpath(guide, REPO_ROOT).replace(os.sep, "/"),
        "channel_count": len(channels),
        "group_count": len(groups),
        "programme_count": len(programmes),
        "guide_channels": len({p["c"] for p in programmes}),
        "window_start": min(starts),
        "window_end": max(stops),
        "playlist_url": playlist_url,
        "guide_url": guide_url,
        "raw_base": RAW_BASE,
        # The category order the taxonomy published, so an app-side refresh can
        # re-order a freshly parsed playlist exactly like the bundle (the Mac
        # app rebuilds categories from this after a download).
        "published_order": published_order,
    }
    with open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8") as handle:
        json.dump(meta, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    return meta


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the PremiumTV app data bundle.")
    parser.add_argument("--scope", choices=sorted(SCOPE_INPUTS), default=DEFAULT_SCOPE,
                        help="usa (stable default) or all (global lineup with the cable-style guide)")
    parser.add_argument("--playlist", default=None,
                        help="override the playlist selected by --scope")
    parser.add_argument("--guide", default=None,
                        help="override the XMLTV guide selected by --scope")
    parser.add_argument("--index", default=os.path.join(REPO_ROOT, DEFAULT_INDEX))
    parser.add_argument("--out", default=os.path.join(REPO_ROOT, DEFAULT_OUT))
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--check", action="store_true", help="report only, write nothing")
    args = parser.parse_args()
    default_playlist, default_guide = SCOPE_INPUTS[args.scope]
    playlist = args.playlist or os.path.join(REPO_ROOT, default_playlist)
    guide = args.guide or os.path.join(REPO_ROOT, default_guide)

    for input_path in (playlist, guide):
        if not os.path.isfile(input_path):
            print("MISSING INPUT: %s" % input_path, file=sys.stderr)
            return 2

    channels, _ = parse_m3u(playlist)
    programmes = parse_xmltv(guide)
    groups = order_groups(channels, load_group_order(args.index))
    known = {c["id"] for c in channels if c["id"]}
    now = int(datetime.now(timezone.utc).timestamp())
    programmes = [p for p in programmes if p["e"] > now - 6 * 3600]
    matched = len({p["c"] for p in programmes if p["c"] in known})

    print("scope         : %s" % args.scope)
    print("channels      : %d" % len(channels))
    print("groups        : %d" % len(groups))
    print("programmes    : %d (for %d bundled channels)" % (len(programmes), matched))
    print("channels with a url : %d" % sum(1 for c in channels if c.get("url")))
    print("channels with a logo: %d" % sum(1 for c in channels if c.get("logo")))
    if args.check:
        return 0

    meta = build(playlist, guide, args.index, args.out, args.version, scope=args.scope)
    print("wrote bundle  : %s (%s)" % (args.out, meta["generated_utc"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
