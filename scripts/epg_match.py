#!/usr/bin/env python3
"""
Match published channels to the guide this repository builds.

A player can only show a schedule when the playlist's ``tvg-id`` is the same id
the XMLTV declares. The scraper keeps whatever id the public index shipped, the
guide keeps the id its upstream source used, so the two drift apart - which is
why channels look "missing from the EPG" even though the guide is loaded.

This module reads a merged XMLTV once and answers one question per channel:

    guide.match(tvg_id="NFL.Network.HD.us2", name="NFL Network")
    -> ("NFLNetwork.us", "name")     # use this id instead

Matching order, most trustworthy first:

1. exact id              the id is already declared in the guide
2. base id               "AE.us@East" -> "AE.us"
3. display-name match    the guide declares "NFL Network" under another id
4. no match              keep the playlist id (the guide declares it anyway)

Only unambiguous display-name matches are used: if two guide channels share a
name, neither is guessed.

    python scripts/epg_match.py --guide EPG/PremiumTV.xml --playlist playlists/PremiumTV.m3u
"""
from __future__ import annotations

import argparse
import collections
import gzip
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import categorize  # noqa: E402


def _open_text(path: Path):
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", errors="replace")
    return open(path, "r", encoding="utf-8", errors="replace")


SYNTHETIC_PREFIX = "premiumtv."


class Guide:
    """The channel ids and display-names declared in one XMLTV file."""

    def __init__(self) -> None:
        self.ids: set[str] = set()
        self.names: dict[str, list[str]] = collections.defaultdict(list)
        self.base_ids: dict[str, list[str]] = collections.defaultdict(list)
        self.display: dict[str, str] = {}
        # Ids that actually carry <programme> data. The scraper also declares a
        # synthetic id for every channel it publishes, and those entries are
        # empty shells: matching a channel onto one of them changes nothing.
        self.with_programmes: set[str] = set()

    # -- loading ---------------------------------------------------------- #
    def load(self, path: Path) -> "Guide":
        # Parsed incrementally: the real guide is tens of megabytes, so the root
        # is emptied after every channel/programme instead of building a tree.
        # (Clearing each element as it ends would delete a <channel>'s
        # display-names before its own end event fired.)
        with _open_text(path) as handle:
            context = ET.iterparse(handle, events=("start", "end"))
            root = None
            for event, element in context:
                if event == "start":
                    if root is None:
                        root = element
                    continue
                tag = element.tag
                if tag == "channel":
                    self._add_channel(element)
                elif tag == "programme":
                    channel_id = (element.get("channel") or "").strip()
                    if channel_id:
                        self.with_programmes.add(channel_id)
                else:
                    continue
                if root is not None:
                    root.clear()
        return self

    def _add_channel(self, element) -> None:
        channel_id = (element.get("id") or "").strip()
        if not channel_id:
            return
        self.ids.add(channel_id)
        self.base_ids[categorize.norm_key(base_id(channel_id))].append(channel_id)
        for child in element:
            if child.tag == "display-name" and child.text:
                name = child.text.strip()
                if name:
                    self.display.setdefault(channel_id, name)
                    key = categorize.norm_key(categorize.clean_display_name(name))
                    if key and channel_id not in self.names[key]:
                        self.names[key].append(channel_id)

    # -- querying --------------------------------------------------------- #
    def has(self, channel_id: str) -> bool:
        return (channel_id or "").strip() in self.ids

    def has_schedule(self, channel_id: str) -> bool:
        return (channel_id or "").strip() in self.with_programmes

    def by_exact_id(self, channel_id: str) -> str:
        return channel_id if self.has(channel_id) else ""

    def _pick(self, candidates: list[str]) -> str:
        """One usable id: the only candidate, or the only one with a schedule."""
        usable = [cid for cid in candidates if not cid.startswith(SYNTHETIC_PREFIX)]
        if len(usable) == 1:
            return usable[0]
        scheduled = [cid for cid in usable if cid in self.with_programmes]
        if len(scheduled) == 1:
            return scheduled[0]
        return ""

    def by_base_id(self, channel_id: str) -> str:
        return self._pick(self.base_ids.get(categorize.norm_key(base_id(channel_id)), []))

    def by_name(self, name: str) -> str:
        """Unambiguous display-name match only."""
        key = categorize.norm_key(categorize.clean_display_name(name))
        return self._pick(self.names.get(key, []))

    def by_name_variant(self, name: str) -> str:
        """Try the usual ways a channel name is spelled differently."""
        for variant in name_variants(name):
            found = self.by_name(variant)
            if found:
                return found
        return ""

    def match(self, channel_id: str = "", name: str = "") -> tuple[str, str]:
        """Return (best id, how) where how is 'exact', 'base', 'name' or ''."""
        channel_id = (channel_id or "").strip()
        if channel_id and self.has(channel_id):
            return channel_id, "exact"
        if channel_id:
            found = self.by_base_id(channel_id)
            if found:
                return found, "base"
        if name:
            found = self.by_name(name)
            if found:
                return found, "name"
            found = self.by_name_variant(name)
            if found:
                return found, "variant"
        return "", ""


def name_variants(name: str) -> list[str]:
    """Progressively looser spellings of a channel name."""
    base = categorize.clean_display_name(name)
    candidates = [
        base,
        re.sub(r"\s*\(.*?\)\s*", " ", base).strip(),
        base.split(" by ")[0].strip(),
        base.split(" / ")[0].strip(),
        re.sub(r"\s+(us|usa|uk|ca|east|west|hd|sd|tv)$", "", base, flags=re.IGNORECASE).strip(),
    ]
    return [item for item in dict.fromkeys(candidates) if item]


def base_id(channel_id: str) -> str:
    """'AE.us@East' -> 'AE.us' (the id without its feed qualifier)."""
    return (channel_id or "").split("@", 1)[0].strip()


def remap_channels(channels: list, guide: Guide) -> dict:
    """Point every channel at a guide id it can actually use.

    Returns counters describing how each channel was matched (or not).
    """
    stats = collections.Counter()
    for channel in channels:
        if not hasattr(channel, "attrs"):
            continue
        current = (channel.attrs.get("tvg-id", "") or "").strip()
        matched, how = guide.match(current, getattr(channel, "name", ""))
        if how == "exact":
            stats["exact"] += 1
        elif matched:
            channel.attrs["tvg-id"] = matched
            stats[how] += 1
        else:
            stats["unmatched"] += 1
    return stats


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Match playlist channels to the built guide.")
    parser.add_argument("--guide", default="EPG/PremiumTV.xml", help="merged XMLTV file")
    parser.add_argument("--playlist", default="playlists/PremiumTV.m3u", help="M3U to audit")
    parser.add_argument("--show", type=int, default=20, help="unmatched examples to print")
    args = parser.parse_args(argv)

    import scraper

    guide_path = Path(args.guide)
    if not guide_path.is_file():
        print(f"no guide at {guide_path}", file=sys.stderr)
        return 1
    guide = Guide().load(guide_path)
    print(f"guide: {len(guide.ids)} channels declared in {guide_path}")

    channels, _ = scraper.parse_m3u(
        Path(args.playlist).read_text(encoding="utf-8", errors="replace"), "playlist")
    stats = remap_channels(channels, guide)
    total = sum(stats.values())
    print(f"playlist: {total} entries in {args.playlist}")
    for how in ("exact", "base", "name", "unmatched"):
        print(f"  {how:<10} {stats.get(how, 0):>6}  ({stats.get(how, 0) / max(total, 1):.1%})")

    unmatched = [
        channel for channel in channels
        if not guide.has((channel.attrs.get("tvg-id", "") or "").strip())
    ]
    if unmatched and args.show:
        print(f"\nexamples with no guide entry ({len(unmatched)} total):")
        for channel in unmatched[: args.show]:
            print(f"  {channel.attrs.get('tvg-id', '')[:38]:<40} {channel.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
