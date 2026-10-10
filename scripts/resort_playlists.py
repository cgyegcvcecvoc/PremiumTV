#!/usr/bin/env python3
"""Re-publish the checked-in playlists in the curated category order.

``scripts/scraper.py`` already writes every playlist in the curated order (see
``scripts/categorize.py``), but playlists committed before that change - or
touched by hand or by a patch run - can keep their old upstream groups
(``General``, ``Undefined``, ``Tv • Series 📺``, ``Italy 🇮🇹``, ...). This tool
re-reads the published playlists, drops anything the last deep check confirmed
dead, normalises group titles that are not labels the taxonomy generates, sorts
the entries and writes the files back. It touches no network and changes no URL:
a link that is in a playlist before the run is still in it afterwards (unless the
last deep check called it dead), only its group, its order and its metadata move.

The country playlists are re-sorted in place rather than rebuilt from
``PremiumTV.m3u``, so a file this tool cannot resolve on its own is never
emptied by mistake.

    python scripts/resort_playlists.py                  # rewrite every playlist
    python scripts/resort_playlists.py --dry-run        # report only
    python scripts/resort_playlists.py --no-prune       # keep deep-checked-dead links
    python scripts/resort_playlists.py --max-feeds 3    # keep 3 feeds per channel
    python scripts/resort_playlists.py --no-guides      # leave x-tvg-url headers alone

Outputs:

    playlists/PremiumTV.m3u          re-sorted confirmed-working playlist
    playlists/AE_Channels.m3u        re-sorted A&E playlist
    playlists/PremiumTV_all.m3u      re-sorted catalogue (links kept, groups normalised)
    playlists/Priority_Channels.m3u  re-sorted priority playlist
    playlists/countries/*.m3u        re-sorted country playlists
    playlists/logs/resort-log.txt    what was re-sorted and what was pruned
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import categorize  # noqa: E402  (the shared category taxonomy)
import link_check  # noqa: E402  (reuses the playlist block reader/writer)
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GUIDE_HEADER_RE = re.compile(r'x-tvg-url="([^"]*)"')
SELF_GUIDE_RE = re.compile(
    r"https://raw\.githubusercontent\.com/[^/]+/[^/]+/(?:refs/heads/)?[^/]+/EPG/[A-Za-z0-9_]+\.xml$")

# Files that are a catalogue of everything found, not a player playlist: their
# links are never pruned, only their groups and order are fixed.
CATALOGUE_FILES = ("PremiumTV_all.m3u",)


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


def trim_guides(header: list, max_fallbacks: int) -> tuple[list, int]:
    """Cap the guide list of a playlist that advertises this repository's own guide.

    The merged guide already contains every programme the verified upstream guides
    have, so a header with ~100 URLs only makes a player download (and wait on)
    100 guides before it shows a listing. ``max_fallbacks`` keeps the first guide
    plus at most that many fallbacks; -1 leaves the header untouched.
    """
    if max_fallbacks < 0 or not header:
        return header, 0
    match = GUIDE_HEADER_RE.search(header[0])
    if not match:
        return header, 0
    guides = [item.strip() for item in match.group(1).split(",") if item.strip()]
    if not guides or not SELF_GUIDE_RE.match(guides[0]):
        return header, 0  # not a playlist that leads with our own guide
    keep = guides[:1 + max_fallbacks]
    if keep == guides:
        return header, 0
    header = list(header)
    header[0] = header[0][:match.start(1)] + ",".join(keep) + header[0][match.end(1):]
    return header, len(guides) - len(keep)


def dead_urls(out_dir: Path, checks_dir: Path, max_age_days: float = 7.0) -> dict[str, str]:
    """URLs confirmed dead by the last deep check or held in quarantine."""
    dead: dict[str, str] = {}
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


def resort_file(path: Path, dead: dict[str, str], *, prune: bool, max_feeds: int,
                max_guides: int, dry_run: bool) -> dict:
    """Re-sort one playlist in place: prune dead URLs, normalise groups, order entries."""
    header, blocks = load_playlist(path)
    pairs = [(block, link_check.channel_from_block(block, path.name)) for block in blocks]
    pruned: list[dict] = []
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
    survivors, duplicates = categorize.dedupe_urls(channels)
    if duplicates:
        keep = {id(channel) for channel in survivors}
        pairs = [(block, channel) for block, channel in pairs if id(channel) in keep]
        channels = survivors
    # Persists tvg-country, rewrites only the group titles the taxonomy does not
    # generate itself, caps the feeds of one channel when asked, and puts the
    # list in the published order (categorize.order_channels).
    categories = scraper.canonicalize_channels(channels, max_feeds)
    order_before = [id(block) for block, _ in pairs]
    position = {id(channel): index for index, channel in enumerate(channels)}
    pairs.sort(key=lambda pair: position.get(id(pair[1]), len(position)))
    regrouped = 0
    for block, channel in pairs:
        if link_check.set_block_group(block, channel.attrs.get("group-title") or categorize.OTHER):
            regrouped += 1
    reordered = order_before != [id(block) for block, _ in pairs]
    header, guides_trimmed = trim_guides(header, max_guides)
    changed = bool(pruned) or reordered or bool(guides_trimmed) or bool(regrouped) or bool(duplicates)
    ordered = [block for block, _ in pairs]
    if not dry_run and changed:
        path.write_text(link_check.blocks_to_text(header, ordered), encoding="utf-8")
    return {
        "file": relative(path),
        "entries_before": len(blocks),
        "entries_after": len(ordered),
        "pruned": pruned,
        "duplicates_dropped": duplicates,
        "categories": categories,
        "reordered": reordered,
        "regrouped": regrouped,
        "guides_trimmed": guides_trimmed,
        "changed": changed,
        "requested_feeds": max_feeds,
    }


def refresh_title(header: list, utc_s: str, local_s: str, label: str, count: int,
                  prefix: str = "Curated categories") -> list:
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


def published_targets(out_dir: Path, files: list[str]) -> list[tuple[Path, str]]:
    """Every committed playlist, with the title prefix its note line should carry."""
    if files:
        return [(Path(item), "Curated categories") for item in files]
    targets: list[tuple[Path, str]] = [
        (out_dir / "PremiumTV.m3u", "Working links - curated categories"),
        (out_dir / "AE_Channels.m3u", "A&E channels - curated categories"),
        (out_dir / "PremiumTV_all.m3u", "All links (unchecked, curated categories)"),
        (out_dir / "Priority_Channels.m3u", "Priority channels (curated categories)"),
    ]
    targets += [(path, "Country playlist (curated categories)")
                for path in sorted((out_dir / "countries").glob("*.m3u"))]
    return [(path, prefix) for path, prefix in targets if path.exists()]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(ROOT / "playlists"), help="playlists directory")
    parser.add_argument("files", nargs="*",
                        help="specific playlist files to re-sort (default: every published one)")
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    parser.add_argument("--no-prune", action="store_true",
                        help="keep links the deep check confirmed dead")
    parser.add_argument("--no-guides", action="store_true",
                        help="leave the advertised x-tvg-url guide list alone")
    parser.add_argument("--max-feeds", type=int, default=0,
                        help="keep at most this many feeds per channel (0 = all)")
    parser.add_argument("--max-guides", type=int, default=scraper.MAX_HEADER_GUIDES,
                        help="fallback guides to keep behind this repository's own guide "
                             "in a published header (-1 leaves every guide advertised)")
    parser.add_argument("--dead-days", type=float, default=7.0,
                        help="how old deep-check evidence may be before it is ignored")
    parser.add_argument("--keep-titles", action="store_true",
                        help="do not refresh the 'updated ...' note line in each header")
    parser.add_argument("--label", default="curated category re-sort",
                        help="run label written into the playlist headers")
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    checks_dir = out_dir / "checks"
    dead = {} if args.no_prune else dead_urls(out_dir, checks_dir, args.dead_days)
    utc_now = dt.datetime.now(dt.timezone.utc)
    utc_s, local_s = scraper.now_strings(utc_now)

    targets = published_targets(out_dir, list(args.files))
    if not targets:
        log(f"[resort] ERROR: no playlists found under {relative(out_dir)}")
        return 1

    reports: list[dict] = []
    max_guides = -1 if args.no_guides else args.max_guides
    for path, prefix in targets:
        report = resort_file(path, dead, prune=path.name not in CATALOGUE_FILES,
                             max_feeds=args.max_feeds, max_guides=max_guides,
                             dry_run=args.dry_run)
        if (not args.dry_run and not args.keep_titles and report["changed"]
                and report["entries_after"]):
            header, blocks = load_playlist(path)
            header = refresh_title(header, utc_s, local_s, args.label,
                                   report["entries_after"], prefix)
            path.write_text(link_check.blocks_to_text(header, blocks), encoding="utf-8")
        reports.append(report)
        flags = []
        if report["reordered"]:
            flags.append("reordered")
        if report["regrouped"]:
            flags.append(f"{report['regrouped']} group titles")
        if report["guides_trimmed"]:
            flags.append(f"-{report['guides_trimmed']} header guides")
        log(f"[resort] {report['file']}: {report['entries_before']} -> "
            f"{report['entries_after']} entries"
            + (f", pruned {len(report['pruned'])}" if report["pruned"] else "")
            + (f" ({', '.join(flags)})" if flags else " (already canonical)"))

    log_path = out_dir / "logs" / "resort-log.txt"
    if not args.dry_run:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "CURATED CATEGORY RE-SORT",
            "=" * 88,
            f"Run: {utc_s} ({local_s}) - {args.label}",
            f"Playlists touched: {len(reports)}",
            "Links changed: 0 (this tool re-groups and re-orders; it never edits a URL)",
            f"Dead links pruned: {sum(len(item['pruned']) for item in reports)}"
            + (" (disabled by --no-prune)" if args.no_prune else ""),
            f"Max feeds per channel: {args.max_feeds or 'unlimited'}",
            "",
        ]
        for item in reports:
            lines.append(f"{item['file']}: {item['entries_before']} -> {item['entries_after']} entries"
                         + (", reordered" if item["reordered"] else "")
                         + (f", {item['regrouped']} group titles normalised" if item["regrouped"] else "")
                         + (f", {item['guides_trimmed']} header guides trimmed"
                            if item["guides_trimmed"] else ""))
            for name, count in list(item["categories"].items())[:40]:
                lines.append(f"    {name}: {count}")
            for entry in item["pruned"][:500]:
                lines.append(f"    - removed {entry['name']} ({entry['reason']}) {entry['url']}")
            lines.append("")
        log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        log(f"[resort] wrote {relative(log_path)}")
    touched = sum(1 for item in reports if item["reordered"] or item["regrouped"]
                   or item["pruned"] or item["guides_trimmed"])
    log(f"[resort] {touched} of {len(reports)} playlists needed a change; "
        f"{sum(len(item['pruned']) for item in reports)} links pruned")
    return 0


if __name__ == "__main__":
    sys.exit(main())
