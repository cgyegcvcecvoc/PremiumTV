#!/usr/bin/env python3
"""
Re-publish already downloaded M3U files with the curated category order.

This is the offline half of the pipeline: it never touches the network. It takes
a playlist that is already on disk (the published one, or one you downloaded),
re-classifies every entry with `scripts/categorize.py`, folds duplicate links
into "<category> Backups" groups, points each channel at a guide id it can
actually use, and writes the file back in the published group order.

It also splits the main playlist into one file per category under
`playlists/categories/` so "just the Sports" or "just the Cartoons" is a single
URL, and writes an audit of what is (and is not) covered by the guide.

    python scripts/rebuild_playlists.py                       # main playlists
    python scripts/rebuild_playlists.py my-playlist.m3u       # any local file
    python scripts/rebuild_playlists.py --dry-run --report -  # audit to stdout

The daily scraper calls the same functions, so a scrape cannot undo this.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import categorize  # noqa: E402
import epg_match  # noqa: E402
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLAYLISTS = (
    "playlists/PremiumTV.m3u",
    "playlists/Priority_Channels.m3u",
)
DEFAULT_CATEGORIES_DIR = "playlists/categories"
DEFAULT_REPORT = "playlists/checks/CATEGORIES.md"
DEFAULT_JSON = "playlists/checks/categories.json"
DEFAULT_GUIDE = "EPG/PremiumTV.xml"
MIN_CATEGORY_NOTE = 3


def log(msg: str) -> None:
    print(msg, flush=True)


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9]+", "_", (value or "").strip()).strip("_")
    return slug or "Other"


# --------------------------------------------------------------------------- #
# Reading / writing
# --------------------------------------------------------------------------- #
def read_playlist(path: Path) -> tuple[list, list[str], str]:
    """Parse a playlist, returning (channels, epg urls, original header line)."""
    text = path.read_text(encoding="utf-8", errors="replace")
    header = ""
    for line in text.splitlines():
        if line.strip().startswith("#EXTM3U"):
            header = line.strip()
            break
    channels, epg = scraper.parse_m3u(text, path.stem)
    return channels, epg, header or "#EXTM3U"


def write_playlist(path: Path, channels: list, header: str, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [header, f"# {title}"]
    lines.extend(channel.to_m3u() for channel in channels)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def stamp() -> tuple[str, str]:
    now = dt.datetime.now(dt.timezone.utc)
    utc = now.strftime("%Y-%m-%d %H:%M UTC")
    try:
        from zoneinfo import ZoneInfo
        local = now.astimezone(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %I:%M %p %Z")
    except Exception:  # noqa: BLE001
        local = utc
    return utc, local


# --------------------------------------------------------------------------- #
# Rebuild
# --------------------------------------------------------------------------- #
def rebuild_file(path: Path, guide: epg_match.Guide | None, max_backups: int = 0,
                 dry_run: bool = False, label: str = "category rebuild") -> dict:
    """Re-categorise, de-duplicate and rewrite one playlist. Returns stats."""
    channels, epg, header = read_playlist(path)
    if not channels:
        return {"file": str(path), "channels": 0, "written": False}

    epg_stats = epg_match.remap_channels(channels, guide) if guide else collections.Counter()
    # A repeated URL is a structural fault the verifier reports, so a re-publish
    # resolves it here: one entry per stream, keeping the name the URL supports.
    channels, duplicates = categorize.dedupe_urls(channels)
    if duplicates:
        log(f"[rebuild] {path}: dropped {duplicates} duplicate/empty URL(s)")
    ordered = categorize.build_main_order(channels, max_backups=max_backups)
    counts = categorize.category_counts(ordered)

    utc_s, local_s = stamp()
    title = (f"{len(ordered)} channels - categories rebuilt {utc_s} ({local_s}) - {label} - "
             f"{len(counts)} groups")
    if not dry_run:
        write_playlist(path, ordered, header, title)

    return {
        "file": str(path),
        "channels": len(ordered),
        "groups": len(counts),
        "duplicate_urls_removed": duplicates,
        "backups": sum(count for group, count in counts.items()
                       if categorize.is_backup_group(group)),
        "written": not dry_run,
        "epg": dict(epg_stats),
        "counts": dict(counts),
        "channels_parsed": channels,
        "epg_urls": epg,
        "header": header,
    }


def write_category_playlists(ordered: list, header: str, out_dir: Path,
                             guide: epg_match.Guide | None, utc_s: str,
                             local_s: str, dry_run: bool = False,
                             min_size: int = 3) -> list[dict]:
    """One playlist per category, in the published category order."""
    counts = categorize.category_counts(ordered)
    order = categorize.order_categories(counts)
    by_group: dict[str, list] = collections.defaultdict(list)
    for channel in ordered:
        by_group[channel.attrs.get("group-title", categorize.OTHER)].append(channel)

    summary: list[dict] = []
    out_dir.mkdir(parents=True, exist_ok=True)
    for category in order:
        members = by_group.get(category, [])
        # Groups with a channel or two are listed in the main playlist but do
        # not get a file of their own; that would be 90 playlists for 10k links.
        if not members or len(members) < min_size:
            continue
        target = out_dir / f"{slugify(category)}.m3u"
        title = (f"{category} - {len(members)} channels - rebuilt {utc_s} ({local_s})")
        if not dry_run:
            write_playlist(target, members, header, title)
        with_guide = sum(
            1 for channel in members
            if guide and guide.has_schedule((channel.attrs.get("tvg-id", "") or "").strip())
        ) if guide else 0
        summary.append({
            "category": category,
            "channels": len(members),
            "with_guide": with_guide,
            "file": str(target.relative_to(ROOT)) if target.is_relative_to(ROOT) else str(target),
        })
    return summary


def write_categories_index(summary: list[dict], out_dir: Path, source: str,
                           utc_s: str, dry_run: bool = False) -> None:
    lines = [
        "# Playlists by category",
        "",
        f"- **Source playlist:** [`{source}`](../{Path(source).name})",
        f"- **Rebuilt:** {utc_s}",
        f"- **Category order:** {' -> '.join(categorize.CURATED_CATEGORIES)} "
        f"(each followed by its own Backups group), then the rest by size.",
        "",
        "| # | Category | Channels | With guide data | Playlist |",
        "|---|---|---:|---:|---|",
    ]
    for index, row in enumerate(summary, 1):
        lines.append(
            f"| {index} | {row['category']} | {row['channels']} | {row['with_guide']} | "
            f"[`{Path(row['file']).name}`]({Path(row['file']).name}) |"
        )
    lines += [
        "",
        "Every file advertises the same merged guide as the main playlist, so the",
        "categories can be loaded on their own.",
        "",
        "Rebuilt by `scripts/rebuild_playlists.py` - re-run it after any scrape to",
        "regenerate these files.",
        "",
    ]
    if not dry_run:
        (out_dir / "README.md").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- #
# Audit
# --------------------------------------------------------------------------- #
def build_report(results: list[dict], summary: list[dict], guide: epg_match.Guide | None,
                 utc_s: str, local_s: str) -> str:
    total = sum(row["channels"] for row in summary)
    with_guide = sum(row["with_guide"] for row in summary)
    published_total = max((item["channels"] for item in results), default=0)
    lines = [
        "# Category and guide audit",
        "",
        f"- **Rebuilt:** {utc_s} ({local_s})",
        f"- **Channels in the main playlist:** {published_total}",
        f"- **Channels in the category files:** {total}"
        + (f" (groups smaller than {MIN_CATEGORY_NOTE} stay in the main playlist only)"
           if published_total > total else ""),
        f"- **With guide data:** {with_guide} "
        + (f"({with_guide / total:.1%})" if total else "(0%)"),
        f"- **Categories:** {len(summary)} groups "
        f"({sum(1 for row in summary if categorize.is_backup_group(row['category']))} backup groups)",
        "",
        "## Published category order",
        "",
        "| # | Category | Channels | With guide |",
        "|---|---|---:|---:|",
    ]
    for index, row in enumerate(summary, 1):
        lines.append(f"| {index} | {row['category']} | {row['channels']} | {row['with_guide']} |")

    lines += ["", "## Files rewritten", "", "| Playlist | Channels | Groups | Backups |",
              "|---|---:|---:|---:|"]
    for result in results:
        if not result.get("channels"):
            continue
        try:
            rel = Path(result["file"]).resolve().relative_to(ROOT)
        except ValueError:
            rel = Path(result["file"])
        lines.append(f"| [`{rel.name}`](../{rel.as_posix().split('/', 1)[-1]}) "
                     f"| {result['channels']} | {result['groups']} | {result['backups']} |")

    if results:
        epg_stats: collections.Counter = collections.Counter()
        for result in results:
            epg_stats.update(result.get("epg", {}))
        total_ids = sum(epg_stats.values())
        lines += [
            "",
            "## Guide matching",
            "",
            "| Match | Channels |",
            "|---|---:|",
        ]
        labels = {
            "exact": "already declared in the guide",
            "base": "matched on the base id (feed qualifier dropped)",
            "name": "matched on the display name",
            "variant": "matched on a looser spelling of the name",
            "unmatched": "no guide entry (upstream publishes no schedule for it)",
        }
        for key in ("exact", "base", "name", "variant", "unmatched"):
            count = epg_stats.get(key, 0)
            if not count:
                continue
            share = f"{count / total_ids:.1%}" if total_ids else "0%"
            lines.append(f"| {labels.get(key, key)} | {count} ({share}) |")

    missing_examples: list[str] = []
    if guide and results:
        seen: set[str] = set()
        for result in results:
            for channel in result.get("channels_parsed", [])[:4000]:
                tvg_id = (channel.attrs.get("tvg-id", "") or "").strip()
                if guide.has_schedule(tvg_id) or tvg_id in seen:
                    continue
                seen.add(tvg_id)
                missing_examples.append(f"{channel.name} (`{tvg_id}`)")
                if len(missing_examples) >= 15:
                    break
            if len(missing_examples) >= 15:
                break
    if missing_examples:
        lines += [
            "",
            "## Channels with no schedule yet",
            "",
            "The guide only carries what the upstream sources publish. These are examples",
            "of channels still waiting for a listing - they stay in the playlist, they",
            "just have nothing to show until an upstream guide picks them up:",
            "",
        ]
        lines.extend(f"- {item}" for item in missing_examples)

    lines += [
        "",
        "Generated by `scripts/rebuild_playlists.py`. Run it after a scrape, or let the",
        "daily workflow do it - the scraper calls the same `categorize` module, so a",
        "scrape cannot put the groups back the way the indexes shipped them.",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Re-publish playlists with curated categories.")
    parser.add_argument("playlists", nargs="*", default=list(DEFAULT_PLAYLISTS),
                        help="M3U files to rebuild (default: the published playlists)")
    parser.add_argument("--guide", default=DEFAULT_GUIDE,
                        help="merged XMLTV used to match channels ('' to skip)")
    parser.add_argument("--categories-dir", default=DEFAULT_CATEGORIES_DIR,
                        help="where to write one playlist per category")
    parser.add_argument("--no-categories", action="store_true",
                        help="do not write the per-category playlists")
    parser.add_argument("--min-category-size", type=int, default=3,
                        help="smallest group that gets its own playlist file")
    parser.add_argument("--report", default=DEFAULT_REPORT, help="markdown audit path")
    parser.add_argument("--json", dest="json_path", default=DEFAULT_JSON, help="JSON audit path")
    parser.add_argument("--max-backups", type=int, default=0,
                        help="keep at most N spare links per channel (0 = keep all)")
    parser.add_argument("--no-corpus", action="store_true",
                        help="do not learn categories from the local corpus")
    parser.add_argument("--label", default="category rebuild",
                        help="run label written into the playlist header comment")
    parser.add_argument("--dry-run", action="store_true", help="audit without writing")
    args = parser.parse_args(argv)

    if not args.no_corpus:
        votes = categorize.load_corpus()
        log(f"[rebuild] learned group votes for {len(votes)} channels from the local corpus")

    guide = None
    if args.guide:
        guide_path = Path(args.guide)
        if guide_path.is_file():
            guide = epg_match.Guide().load(guide_path)
            log(f"[rebuild] guide: {len(guide.ids)} channels, "
                f"{len(guide.with_programmes)} with schedules ({args.guide})")
        else:
            log(f"[rebuild] no guide at {guide_path}; skipping EPG matching")

    utc_s, local_s = stamp()
    results: list[dict] = []
    for raw in args.playlists:
        path = Path(raw)
        if not path.is_file():
            log(f"[rebuild] missing playlist: {path}")
            continue
        result = rebuild_file(path, guide, max_backups=args.max_backups,
                              dry_run=args.dry_run, label=args.label)
        results.append(result)
        if result.get("channels"):
            log(f"[rebuild] {path}: {result['channels']} channels in {result['groups']} groups "
                f"({result['backups']} backups)"
                + (" [dry run]" if args.dry_run else ""))

    summary: list[dict] = []
    main_result = next((item for item in results
                        if item.get("channels") and "PremiumTV.m3u" in item["file"]), None)
    if main_result is None:
        main_result = next((item for item in results if item.get("channels")), None)
    if main_result and not args.no_categories:
        ordered = main_result["channels_parsed"]
        out_dir = Path(args.categories_dir)
        if not out_dir.is_absolute():
            out_dir = ROOT / out_dir
        summary = write_category_playlists(
            ordered, main_result["header"], out_dir, guide, utc_s, local_s, args.dry_run,
            min_size=args.min_category_size)
        write_categories_index(summary, out_dir, main_result["file"], utc_s, args.dry_run)
        log(f"[rebuild] {'wrote' if not args.dry_run else 'would write'} "
            f"{len(summary)} category playlists to {out_dir}")

    report = build_report(results, summary, guide, utc_s, local_s)
    if args.report == "-":
        print(report)
    elif not args.dry_run:
        report_path = Path(args.report)
        if not report_path.is_absolute():
            report_path = ROOT / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding="utf-8")
        log(f"[rebuild] audit: {report_path}")

    if not args.dry_run and args.json_path:
        json_path = Path(args.json_path)
        if not json_path.is_absolute():
            json_path = ROOT / json_path
        json_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "updated_utc": utc_s,
            "updated_local": local_s,
            "categories": summary,
            "playlists": [
                {key: value for key, value in item.items()
                 if key not in ("channels_parsed", "epg_urls", "header")}
                for item in results
            ],
        }
        json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
