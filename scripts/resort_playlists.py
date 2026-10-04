#!/usr/bin/env python3
"""Re-publish the checked-in playlists in the canonical category order.

``scripts/scraper.py`` already writes every playlist in the canonical order
(see ``scripts/channel_categories.py``), but playlists committed before that
change - or edited by hand - keep their old upstream groups ("General",
"Undefined", "Tv \u2022 Series \U0001f4fa", ...). This tool re-reads the published
playlists, drops anything the last deep check confirmed dead, rewrites each
channel's ``group-title`` to its canonical category, sorts the entries and
writes the playlists back. It touches no network and changes no URL that the
deep check still considers alive.

    python scripts/resort_playlists.py                  # rewrite every playlist
    python scripts/resort_playlists.py --dry-run        # report only
    python scripts/resort_playlists.py --no-prune       # keep deep-checked-dead links
    python scripts/resort_playlists.py --max-feeds 3    # keep 3 feeds per channel

Outputs:

    playlists/PremiumTV.m3u          re-sorted confirmed-working playlist
    playlists/AE_Channels.m3u        re-sorted A&E playlist
    playlists/Priority_Channels.m3u  re-sorted priority playlist
    playlists/countries/*.m3u        re-sorted country playlists + README index
    playlists/logs/resort-log.txt    what was re-sorted and what was pruned
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import channel_categories  # noqa: E402
import link_check  # noqa: E402  (reuses the playlist block reader/writer)
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GUIDE_HEADER_RE = re.compile(r'x-tvg-url="([^"]*)"')


def log(msg: str) -> None:
    print(msg, flush=True)


def guides_from(path: Path) -> list[str]:
    """The x-tvg-url guide list a playlist already advertises, in order."""
    try:
        first = path.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    except (OSError, IndexError):
        return []
    match = GUIDE_HEADER_RE.search(first)
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


def dead_urls(out_dir: Path, checks_dir: Path, max_age_days: float = 7.0) -> dict[str, str]:
    """URLs confirmed dead by the last deep check or held in quarantine."""
    dead: dict[str, str] = {}
    limit = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=max_age_days)
    for url, reason in scraper.load_deep_check_dead(checks_dir, max_age_days * 24.0).items():
        dead[url] = reason
    for url, entry in (scraper.load_quarantine(checks_dir / scraper.QUARANTINE_FILENAME,
                                               max_age_days) or {}).items():
        dead[url] = f"quarantined: {entry.get('reason') or 'deep check found no media'}"
    if not dead:
        log(f"[resort] no fresh deep-check results in {checks_dir}; nothing pruned")
    return dead


def load_playlist(path: Path) -> tuple[list, list]:
    header, blocks = link_check.split_blocks(path.read_text(encoding="utf-8", errors="replace"))
    return header, blocks


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def resort_file(path: Path, dead: dict[str, str], prune: bool, max_feeds: int,
                dry_run: bool) -> dict:
    """Re-sort one playlist: prune dead URLs, canonicalise groups, order entries."""
    header, blocks = load_playlist(path)
    pairs = [(block, link_check.channel_from_block(block, path.name)) for block in blocks]
    pruned = []
    if prune and dead:
        kept_pairs = []
        for block, channel in pairs:
            reason = dead.get(channel.url or "")
            if reason:
                pruned.append({"name": channel.name, "url": channel.url, "reason": reason})
            else:
                kept_pairs.append((block, channel))
        pairs = kept_pairs
    channels = [channel for _, channel in pairs]
    scraper.canonicalize_channels(channels, max_feeds)
    pairs.sort(key=lambda pair: scraper.sort_key(pair[1]))
    for block, channel in pairs:
        link_check.set_block_group(block, channel.attrs.get("group-title") or "TV")
    ordered = [block for block, _ in pairs]
    changed_groups = sum(1 for _, channel in pairs)
    if not dry_run and (pruned or ordered != blocks):
        path.write_text(link_check.blocks_to_text(header, ordered), encoding="utf-8")
    return {
        "file": relative(path),
        "entries_before": len(blocks),
        "entries_after": len(ordered),
        "pruned": pruned,
        "categories": channel_categories.category_counts(channels),
        "regrouped": changed_groups,
        "requested_feeds": max_feeds,
    }


def refresh_title(header: list, utc_s: str, local_s: str, label: str, count: int,
                  prefix: str = "Canonical categories") -> list:
    """Refresh the playlist's "updated ..." comment line, keeping any other notes."""
    note = (f"# {prefix} - {count} channels - "
            f"updated {utc_s} ({local_s}) - {label}")
    for index, line in enumerate(header):
        if line.startswith("#EXTM3U"):
            continue
        if line.startswith("#") and "updated" in line.lower():
            header[index] = note
            return header
    header.insert(1 if header and header[0].startswith("#EXTM3U") else 0, note)
    return header


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(ROOT / "playlists"), help="playlists directory")
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    parser.add_argument("--no-prune", action="store_true",
                        help="keep links the deep check confirmed dead")
    parser.add_argument("--max-feeds", type=int, default=0,
                        help="keep at most this many feeds per channel (0 = all)")
    parser.add_argument("--dead-days", type=float, default=7.0,
                        help="how old deep-check evidence may be before it is ignored")
    parser.add_argument("--label", default="canonical category re-sort",
                        help="run label written into the playlist headers")
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    checks_dir = out_dir / "checks"
    dead = {} if args.no_prune else dead_urls(out_dir, checks_dir, args.dead_days)
    utc_now = dt.datetime.now(dt.timezone.utc)
    utc_s = utc_now.strftime("%Y-%m-%d %H:%M UTC")
    _, local_s = scraper.now_strings(utc_now)

    main_path = out_dir / "PremiumTV.m3u"
    if not main_path.exists():
        log(f"[resort] ERROR: {relative(main_path)} does not exist; nothing to re-sort")
        return 1
    main_guides = guides_from(main_path)

    reports: list[dict] = []
    # The checked working playlist: re-write it from its own verified entries.
    header, blocks = load_playlist(main_path)
    pairs = [(block, link_check.channel_from_block(block, "PremiumTV.m3u")) for block in blocks]
    kept_pairs = []
    pruned = []
    for block, channel in pairs:
        reason = dead.get(channel.url or "")
        if reason:
            pruned.append({"name": channel.name, "url": channel.url, "reason": reason})
        else:
            kept_pairs.append((block, channel))
    working = [channel for _, channel in kept_pairs]
    categories = scraper.canonicalize_channels(working, args.max_feeds)
    kept_pairs.sort(key=lambda pair: scraper.sort_key(pair[1]))
    reports.append({
        "file": "PremiumTV.m3u",
        "entries_before": len(blocks),
        "entries_after": len(working),
        "pruned": pruned,
        "categories": categories,
        "regrouped": len(working),
    })
    if not args.dry_run:
        title = (f"Working links - canonical categories - {len(working)} channels - "
                 f"updated {utc_s} ({local_s}) - {args.label}")
        scraper.write_m3u(main_path, working, main_guides, title, synthesize_missing_ids=True)
        scraper.write_country_playlists(out_dir, working, main_guides, utc_s, local_s, args.label)
        scraper.write_ae_playlist(out_dir, working, main_guides, utc_s, local_s, args.label)
        log(f"[resort] {relative(main_path)}: {len(working)} channels, "
            f"{len(pruned)} pruned")

    # Playlists that are not derived from PremiumTV.m3u: re-sort in place.
    secondary = {
        "PremiumTV_all.m3u": "All links (unchecked, canonical categories)",
        "Priority_Channels.m3u": "Priority channels (canonical categories)",
    }
    for name, prefix in secondary.items():
        path = out_dir / name
        if not path.exists():
            continue
        prune = name != "PremiumTV_all.m3u"  # the "all links" file is a catalogue
        report = resort_file(path, dead, prune=prune, max_feeds=args.max_feeds,
                             dry_run=args.dry_run)
        if not args.dry_run:
            header, blocks = load_playlist(path)
            header = refresh_title(header, utc_s, local_s, args.label,
                                   report["entries_after"], prefix)
            path.write_text(link_check.blocks_to_text(header, blocks), encoding="utf-8")
        reports.append(report)
        log(f"[resort] {name}: {report['entries_before']} -> {report['entries_after']} entries, "
            f"pruned {len(report['pruned'])}")

    log_path = out_dir / "logs" / "resort-log.txt"
    if not args.dry_run:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "CANONICAL CATEGORY RE-SORT",
            "=" * 88,
            f"Run: {utc_s} ({local_s}) - {args.label}",
            f"Dead links pruned: {sum(len(item['pruned']) for item in reports)}"
            + (" (disabled by --no-prune)" if args.no_prune else ""),
            f"Max feeds per channel: {args.max_feeds or 'unlimited'}",
            "",
        ]
        for item in reports:
            lines.append(f"{item['file']}: {item['entries_before']} -> {item['entries_after']} entries")
            for name, count in item["categories"].items():
                lines.append(f"    {name}: {count}")
            for entry in item["pruned"][:500]:
                lines.append(f"    - removed {entry['name']} ({entry['reason']}) {entry['url']}")
            lines.append("")
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        log(f"[resort] wrote {relative(log_path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
