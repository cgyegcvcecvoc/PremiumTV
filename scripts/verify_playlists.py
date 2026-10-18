#!/usr/bin/env python3
"""Offline verification of the published playlists and guides.

Everything here is computed from files already in the repository - no network -
so it can run after a scrape, after a deep check, or by hand, and always answer
the same questions:

* Is every published link one the last deep check still considers alive?
  (URLs the deep check confirmed dead or that sit in the quarantine file are
  called out; nothing else is assumed about a link.)
* Does every playlist use the repository's own categories and the published
  order (`scripts/categorize.py`: curated groups first, each followed by its
  `<category> Backups` group, the long tail by size, `Other` last, name inside a
  group)? A group-title that the taxonomy would never have written - "General",
  "Undefined", "Tv • Series 📺" - is called out, because it means the file was
  not published (or not re-sorted) through it.
* Is every ``tvg-id`` a well-formed, unique id, and does the guide each playlist
  advertises actually declare that id? EPG coverage is reported per playlist and
  per category, so a guide that is not sourced for a channel is visible instead
  of silently blank.
* Is each advertised guide a real, parseable XMLTV file, and is it the right
  guide for that playlist (a country playlist must advertise its own
  ``EPG/<Country>.xml``)?
* Is the ``categories/`` shelf (`scripts/build_categories.py`) still exactly the
  shelf the published playlists call for? Every file is re-planned from
  ``playlists/PremiumTV.m3u`` and ``playlists/countries/USA.m3u`` and compared
  entry by entry, so a folder left behind by an old scrape - or one that lost a
  channel - is named instead of shipped.

    python scripts/verify_playlists.py                # report + checks/VERIFY.md
    python scripts/verify_playlists.py --strict       # exit 1 when something is wrong
    python scripts/verify_playlists.py --no-epg-parse # skip the big XMLTV files
    python scripts/verify_playlists.py --require-shelf  # a missing shelf is a problem too

Outputs:

    playlists/checks/verify.json    machine-readable result of every check
    playlists/checks/VERIFY.md      human-readable summary
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_categories  # noqa: E402  (the shelf this repository publishes)
import categorize  # noqa: E402  (the taxonomy the published files must match)
import epg_check  # noqa: E402  (knows which guide URLs this repository publishes itself)
import legacy_sunset  # noqa: E402  (which USA feed is live and which is pinned)
import link_check  # noqa: E402
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GUIDE_HEADER_RE = re.compile(r'x-tvg-url="([^"]*)"')
SELF_URL_RE = re.compile(
    r"https://raw\.githubusercontent\.com/[^/]+/[^/]+/(?:refs/heads/)?[^/]+/EPG/([A-Za-z0-9_]+)\.xml$")
HTTP_SCHEMES = ("http", "https")
KNOWN_OTHER_SCHEMES = tuple(scraper.NON_HTTP_SCHEMES)


def log(msg: str) -> None:
    print(msg, flush=True)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def read_guides(path: Path) -> list[str]:
    try:
        first = path.read_text(encoding="utf-8", errors="replace").splitlines()[0]
    except (OSError, IndexError):
        return []
    match = GUIDE_HEADER_RE.search(first)
    if not match:
        return []
    return [item.strip() for item in match.group(1).split(",") if item.strip()]


def guide_file_for_url(url: str, epg_dir: Path) -> Path | None:
    """Local EPG/*.xml file for a guide URL this repository publishes, if any."""
    match = SELF_URL_RE.match(url)
    if match:
        candidate = epg_dir / f"{match.group(1)}.xml"
        return candidate if candidate.exists() else None
    if url.startswith(("http://", "https://")):
        return None
    candidate = Path(url)
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    return candidate if candidate.exists() else None


def xml_channel_stats(path: Path, limit_bytes: int | None = None) -> dict:
    """Channel ids, programme count and ids with real listings, streamed element by element."""
    ids: set[str] = set()
    scheduled: set[str] = set()
    programmes = 0
    if limit_bytes and path.stat().st_size > limit_bytes:
        return {"ids": ids, "scheduled": scheduled, "programmes": programmes,
                "error": f"skipped: {path.stat().st_size // 1_000_000} MB over the parse limit"}
    try:
        for _, element in ET.iterparse(path, events=("end",)):
            if element.tag == "channel":
                channel_id = (element.get("id") or "").strip()
                if channel_id:
                    ids.add(channel_id)
            elif element.tag == "programme":
                programmes += 1
                channel_id = (element.get("channel") or "").strip()
                if channel_id:
                    scheduled.add(channel_id)
            element.clear()
    except ET.ParseError as exc:
        return {"ids": ids, "scheduled": scheduled, "programmes": programmes,
                "error": f"invalid XML: {exc}"}
    except OSError as exc:
        return {"ids": ids, "scheduled": scheduled, "programmes": programmes,
                "error": f"unreadable: {exc}"}
    return {"ids": ids, "scheduled": scheduled, "programmes": programmes, "error": ""}


def local_guide_ids(playlist_guides: list[str], epg_dir: Path,
                    cache: dict[str, dict],
                    limit_bytes: int | None = None) -> tuple[set[str], set[str], list[str], str, int]:
    """Declared and scheduled ids from the local guides a playlist advertises."""
    declared: set[str] = set()
    scheduled: set[str] = set()
    files: list[str] = []
    problems: list[str] = []
    programmes = 0
    for url in playlist_guides:
        path = guide_file_for_url(url, epg_dir)
        if path is None:
            continue
        files.append(relative(path))
        if str(path) not in cache:
            cache[str(path)] = xml_channel_stats(path, limit_bytes)
        stats = cache[str(path)]
        if stats["error"]:
            problems.append(f"{relative(path)}: {stats['error']}")
            continue
        declared |= stats["ids"]
        scheduled |= stats["scheduled"]
        programmes += stats["programmes"]
    return declared, scheduled, files, "; ".join(problems), programmes


def verify_playlist(path: Path, epg_dir: Path, dead: dict[str, str], cache: dict,
                    parse_epg: bool, max_bytes: int | None = None) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    header, blocks = link_check.split_blocks(text)
    # The legacy USA feed carries one sanctioned end-of-support notice so an
    # installed build with no updater can be told about a newer release. It is a
    # message, not a channel: it is excluded from every structural check (group,
    # order, id, dead links) and counted separately, exactly as the live feed is
    # free of it.
    sanctioned = [block for block in blocks if link_check.is_notice_block(block)]
    blocks = [block for block in blocks if not link_check.is_notice_block(block)]
    channels = [link_check.channel_from_block(block, path.name) for block in blocks]
    guides = read_guides(path)

    issues: list[str] = []
    first_line = text.splitlines()[0] if text.splitlines() else ""
    if not first_line.startswith("#EXTM3U"):
        issues.append("missing #EXTM3U header")
    # A playlist that leads with this repository's own guide is a published one, so
    # its header is expected to hold that guide plus MAX_HEADER_GUIDES fallbacks.
    leads_with_own_guide = bool(guides) and "raw.githubusercontent.com" in guides[0] and "/EPG/" in guides[0]
    allowed_guides = 1 + scraper.MAX_HEADER_GUIDES
    if leads_with_own_guide and scraper.MAX_HEADER_GUIDES >= 0 and len(guides) > allowed_guides:
        issues.append(f"the header advertises {len(guides)} guides; a player downloads every one "
                      f"before it shows a listing ({allowed_guides} is the published maximum: "
                      f"the merged guide plus {scraper.MAX_HEADER_GUIDES} fallbacks)")

    urls = [channel.url for channel in channels]
    duplicates = collections.Counter(url for url in urls if url)
    duplicate_urls = sorted(url for url, count in duplicates.items() if count > 1)
    if duplicate_urls:
        issues.append(f"{len(duplicate_urls)} duplicate URL(s) inside the playlist")

    bad_scheme = collections.Counter()
    missing_id: list[str] = []
    dead_hits: list[dict] = []
    group_counts: dict[str, int] = collections.Counter()
    non_canonical: dict[str, int] = collections.Counter()
    categories: dict[str, int] = collections.Counter()
    ids_seen: set[str] = set()
    duplicate_ids: dict[str, list[str]] = collections.defaultdict(list)

    for channel in channels:
        scheme = channel.url.split(":", 1)[0].lower() if ":" in channel.url else ""
        if scheme not in HTTP_SCHEMES:
            bad_scheme[scheme or "(none)"] += 1
        group = (channel.attrs.get("group-title") or "").strip()
        group_counts[group or "(none)"] += 1
        category = categorize.base_category(group) or "(none)"
        categories[category] += 1
        # "Would the taxonomy write this label?" is the only fair test for a
        # committed file: the Backups split, the curated order and the long tail
        # are all answers to that same question.
        if categorize.needs_normalization(group):
            non_canonical[group or "(none)"] += 1
        tvg_id = (channel.attrs.get("tvg-id") or "").strip()
        if not tvg_id:
            missing_id.append(channel.name)
        else:
            if tvg_id in ids_seen and len(duplicate_ids[tvg_id]) < 5:
                duplicate_ids[tvg_id].append(channel.name)
            ids_seen.add(tvg_id)
        reason = dead.get(channel.url or "")
        if reason and len(dead_hits) < 200:
            dead_hits.append({"name": channel.name, "url": channel.url, "reason": reason})

    if bad_scheme:
        issues.append("non-HTTP URLs: "
                      + ", ".join(f"{scheme} ({count})" for scheme, count in bad_scheme.items()))
    if non_canonical:
        issues.append(f"{sum(non_canonical.values())} entries carry a group the taxonomy never "
                      f"writes (run scripts/resort_playlists.py): "
                      + ", ".join(f"{group} ({count})"
                                  for group, count in list(non_canonical.most_common(8))))
    if dead_hits:
        issues.append(f"{len(dead_hits)} published link(s) confirmed dead by the last deep check")

    # The published order is a property of the whole file (which groups exist and
    # how big they are), so the check re-orders the file's own entries and counts
    # the positions that differ instead of comparing a per-entry key.
    ordered = categorize.order_channels(channels)
    if len(ordered) != len(channels):
        # order_channels() is a permutation of its input: a different length means it
        # lost or invented an entry. That is a fault worth reporting - and reporting
        # beats crashing the verifier on a traceback.
        issues.append(f"the taxonomy re-order kept {len(ordered)} of {len(channels)} "
                      f"entries; every channel must survive the sort")
    out_of_order = sum(1 for left, right in zip(channels, ordered, strict=False)
                       if (left.name, left.url, left.attrs.get("group-title", ""))
                       != (right.name, right.url, right.attrs.get("group-title", "")))

    declared: set[str] = set()
    scheduled: set[str] = set()
    guide_files: list[str] = []
    guide_problem = ""
    guide_programmes = 0
    if parse_epg and guides:
        declared, scheduled, guide_files, guide_problem, guide_programmes = local_guide_ids(
            guides, epg_dir, cache, max_bytes)
        if guide_problem:
            issues.append(guide_problem)

    matched = sorted(ids_seen & declared) if declared else []
    listed = sorted(ids_seen & scheduled) if scheduled else []
    coverage = (len(matched) / len(ids_seen)) if ids_seen and declared else 0.0
    warnings: list[str] = []
    if declared and len(ids_seen) > len(declared):
        warnings.append(f"the advertised guide declares {len(declared)} of "
                        f"{len(ids_seen)} playlist ids; the next EPG build adds the rest")
    if declared and not guide_programmes:
        warnings.append("the advertised local guide has no programme entries "
                        "(upstream listings were unreachable); channel ids are still declared")

    return {
        "file": relative(path),
        "entries": len(channels),
        "sanctioned_notice": len(sanctioned),
        "unique_urls": len(set(urls)),
        "duplicate_urls": duplicate_urls[:50],
        "guides": guides,
        "guides_advertised": len(guides),
        "local_guide_files": guide_files,
        "missing_tvg_id": len(missing_id),
        "missing_tvg_id_sample": missing_id[:10],
        "duplicate_tvg_ids": {key: value for key, value in list(duplicate_ids.items())[:20]},
        "groups": dict(group_counts.most_common(20)),
        "non_canonical_groups": dict(non_canonical.most_common(20)),
        "categories": dict(categories),
        "out_of_order": out_of_order,
        "dead_links": dead_hits,
        "epg": {
            "declared_ids": len(declared),
            "playlist_ids": len(ids_seen),
            "matched_ids": len(matched),
            "coverage": round(coverage, 4),
            "ids_with_programmes": len(listed),
            "programme_coverage": round(len(listed) / len(ids_seen), 4) if ids_seen else 0.0,
            "guide_programmes": guide_programmes,
            "problem": guide_problem,
        },
        "issues": issues,
        "warnings": warnings,
    }


def playlist_entries(path: Path) -> list[tuple[str, str, str]]:
    """(name, url, group-title) of every entry in a playlist, in file order."""
    text = path.read_text(encoding="utf-8", errors="replace")
    _, blocks = link_check.split_blocks(text)
    entries: list[tuple[str, str, str]] = []
    for block in blocks:
        channel = link_check.channel_from_block(block, path.name)
        entries.append((channel.name, channel.url,
                        (channel.attrs.get("group-title") or "").strip()))
    return entries


def committed_shelf_files(shelf_dir: Path) -> set[Path]:
    """Every .m3u a reader could find in the shelf directory."""
    if not shelf_dir.is_dir():
        return set()
    return {path for path in shelf_dir.rglob("*.m3u") if path.is_file()}


def verify_category_shelf(shelf_dir: Path, main_path: Path, usa_path: Path,
                          min_size: int | None = None,
                          allow_missing: bool = False) -> dict:
    """Compare the committed ``categories/`` shelf with the shelf in force now.

    The expected layout is re-planned by the same code that writes it
    (``build_categories.plan_shelf``), so this is an equality check on the
    channel list and its order - not a heuristic that can drift.
    """
    issues: list[str] = []
    rows: list[dict] = []
    # The shelf records the group size it was built with, so the comparison uses
    # the same rule instead of guessing (and flagging every small group as extra).
    if min_size is None:
        min_size = build_categories.recorded_min_size(shelf_dir)
    planned = build_categories.plan_shelf(main_path, usa_path, shelf_dir, min_size=min_size)
    planned_paths = {item.path for item in planned}

    if not shelf_dir.is_dir() or not planned:
        if allow_missing:
            return {"dir": relative(shelf_dir), "skipped": True, "files": [], "issues": [],
                    "note": "no shelf directory to check (pass --require-shelf to demand one)"}
        if not planned:
            return {"dir": relative(shelf_dir), "skipped": True, "files": [], "issues": [],
                    "note": "no published playlists to plan a shelf from"}
        issues.append(f"{relative(shelf_dir)}/ is missing: the published playlists call for "
                      f"{len(planned)} shelf file(s) (run scripts/build_categories.py)")

    for item in planned:
        entry = {"file": relative(item.path), "scope": item.scope,
                 "category": item.category, "channels": len(item.channels), "status": "ok"}
        if not item.path.is_file():
            entry["status"] = "missing"
            issues.append(f"{relative(item.path)} is missing (run scripts/build_categories.py)")
        else:
            committed = playlist_entries(item.path)
            expected = [(channel.name, channel.url,
                         (channel.attrs.get("group-title") or "").strip())
                        for channel in item.channels]
            if committed != expected:
                entry["status"] = "stale"
                entry["committed"] = len(committed)
                issue = (f"{relative(item.path)} is stale: {len(committed)} entries committed, "
                         f"{len(expected)} expected (run scripts/build_categories.py)")
                committed_names = {name for name, _, _ in committed}
                missing = next((name for name, _, _ in expected if name not in committed_names),
                               "")
                if missing:
                    issue += f"; e.g. {missing!r} is not in it"
                issues.append(issue)
        if item.path.is_file():
            guides = read_guides(item.path)
            allowed = 1 + scraper.MAX_HEADER_GUIDES
            if scraper.MAX_HEADER_GUIDES >= 0 and len(guides) > allowed:
                entry["status"] = "problem"
                issues.append(f"{relative(item.path)} advertises {len(guides)} guides; "
                              f"the published maximum is {allowed}")
            elif not guides:
                entry["status"] = "problem"
                issues.append(f"{relative(item.path)} has no x-tvg-url header")
        rows.append(entry)

    for extra in sorted(committed_shelf_files(shelf_dir) - planned_paths):
        issues.append(f"{relative(extra)} is not part of the shelf any more "
                      f"(remove it or re-run scripts/build_categories.py)")
    for name in ("README.md", "index.json"):
        if shelf_dir.is_dir() and not (shelf_dir / name).is_file():
            issues.append(f"{relative(shelf_dir / name)} is missing "
                          f"(run scripts/build_categories.py)")

    return {"dir": relative(shelf_dir), "skipped": False, "files": rows,
            "expected_files": len(planned), "issues": issues,
            "note": "" if issues else "every shelf file matches the published order"}


def epg_source_summary(checks_dir: Path) -> dict:
    """How the last guide check rated the advertised upstream guides."""
    path = checks_dir / "epg-check.json"
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    results = data.get("results") or data.get("guides") or {}
    items = results if isinstance(results, list) else (
        list(results.values()) if isinstance(results, dict) else [])
    items = [item for item in items if isinstance(item, dict)]
    # The guides this repository publishes itself are recorded with their real
    # status, but they are not upstream sources: counting 173 self-hosted 404s
    # here made every verify report look as though the whole guide shelf had died.
    def is_own(item: dict) -> bool:
        return bool(item.get("own_repo")) or epg_check.is_own_guide(str(item.get("url") or ""))

    own = sum(1 for item in items if is_own(item))
    counts = collections.Counter(str(item.get("status") or "unknown")
                                 for item in items if not is_own(item))
    return {
        "finished_utc": data.get("finished_utc") or data.get("started_utc") or "",
        "counts": dict(counts),
        "own_repo_guides": own,
        "verified": data.get("verified_count"),
        "unreachable": data.get("unreachable_count"),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", default=str(ROOT / "playlists"), help="playlists directory")
    parser.add_argument("--epg-dir", default=str(ROOT / "EPG"), help="XMLTV directory")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero when a playlist has a structural problem")
    parser.add_argument("--no-epg-parse", action="store_true",
                        help="skip reading the (large) XMLTV files")
    parser.add_argument("--max-epg-mb", type=float, default=0.0,
                        help="do not parse a guide larger than this many MB (0 = no limit)")
    parser.add_argument("--shelf-dir", default="auto",
                        help="categories/ shelf to check (default: next to the playlists dir)")
    parser.add_argument("--no-shelf", action="store_true",
                        help="do not check the categories/ shelf at all")
    parser.add_argument("--require-shelf", action="store_true",
                        help="a missing or stale categories/ shelf is a problem, not a note")
    args = parser.parse_args(argv)

    out_dir = Path(args.out)
    epg_dir = Path(args.epg_dir)
    checks_dir = out_dir / "checks"
    dead = scraper.load_deep_check_dead(checks_dir, 7 * 24.0)
    dead.update({url: f"quarantined: {entry.get('reason') or 'no media on the deep check'}"
                 for url, entry in (scraper.load_quarantine(
                     checks_dir / scraper.QUARANTINE_FILENAME, 7.0) or {}).items()})

    targets = [out_dir / name for name in ("PremiumTV.m3u", "AE_Channels.m3u",
                                           "Priority_Channels.m3u")]
    targets = [path for path in targets if path.exists()]
    targets += sorted((out_dir / "countries").glob("*.m3u"))
    # playlists/live/ carries the USA feed current builds refresh from, so it is
    # verified like any published playlist. A *frozen* legacy feed is not: it is
    # a pinned end-of-support artifact whose channels were verified on the day
    # they were pinned, and whose sanctioned notice entry is deliberately not a
    # channel (both apps' parsers drop an entry marked tvg-notice="app-update").
    targets += sorted((out_dir / "live").glob("*.m3u"))
    frozen = [path for path in targets if legacy_sunset.is_frozen(path)]
    targets = [path for path in targets if path not in frozen]
    for path in frozen:
        log(f"[verify] FROZEN {relative(path)}: pinned for end-of-support builds, not re-verified")
    if not targets:
        log(f"[verify] ERROR: no playlists found under {relative(out_dir)}")
        return 1

    cache: dict[str, dict] = {}
    # A cap on the guide size keeps the run bounded on a huge merged guide; the
    # limit is applied where the files are read, so it must be passed down.
    max_bytes = int(args.max_epg_mb * 1_000_000) if args.max_epg_mb > 0 else None

    reports = []
    for path in targets:
        report = verify_playlist(path, epg_dir, dead, cache, parse_epg=not args.no_epg_parse,
                                 max_bytes=max_bytes)
        reports.append(report)
        status = "OK " if not report["issues"] else "ISSUES"
        log(f"[verify] {status} {report['file']}: {report['entries']} entries, "
            f"EPG {report['epg']['matched_ids']}/{report['epg']['playlist_ids']} ids"
            + (f" - {'; '.join(report['issues'])}" if report["issues"] else ""))

    violating = [item for item in reports if item["issues"]]
    warned = [item for item in reports if item.get("warnings")]
    shelf = {"dir": "", "skipped": True, "files": [], "issues": [],
             "note": "disabled with --no-shelf"}
    if not args.no_shelf:
        # "auto" keeps the shelf next to the playlists directory, so a run against
        # a copy of the repository checks that copy's shelf, not this one's.
        shelf_dir = (out_dir.parent / build_categories.DEFAULT_SHELF
                     if args.shelf_dir in ("", "auto") else Path(args.shelf_dir))
        # The shelf is re-planned from the same live USA feed build_categories.py
        # cuts it from, so a pinned legacy feed cannot make the shelf look stale.
        shelf = verify_category_shelf(
            shelf_dir, out_dir / "PremiumTV.m3u",
            legacy_sunset.live_usa_path(out_dir.parent),
            allow_missing=not args.require_shelf)
    totals = {
        "playlists": len(reports),
        "entries": sum(item["entries"] for item in reports),
        "playlists_with_issues": len(violating),
        "playlists_with_warnings": len(warned),
        "dead_links_published": sum(len(item["dead_links"]) for item in reports),
        "frozen_legacy_feeds": [relative(path) for path in frozen],
        "shelf_files": len(shelf.get("files") or []),
        "shelf_problems": len(shelf.get("issues") or []),
        "epg_sources": epg_source_summary(checks_dir),
    }
    result = {
        "run_id": dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "group_order": list(categorize.order_categories(
            collections.Counter(g for item in reports for g in item["groups"]))),
        "curated_categories": list(categorize.CURATED_CATEGORIES),
        "max_header_guides": scraper.MAX_HEADER_GUIDES,
        "totals": totals,
        "playlists": reports,
        "shelf": shelf,
        "quarantine_entries": len(scraper.load_quarantine(
            checks_dir / scraper.QUARANTINE_FILENAME, 7.0) or {}),
    }

    checks_dir.mkdir(parents=True, exist_ok=True)
    (checks_dir / "verify.json").write_text(json.dumps(result, indent=2), encoding="utf-8")

    lines = [
        "# Playlist and guide verification",
        "",
        f"- **Generated:** {result['generated_utc']} UTC",
        f"- **Playlists checked:** {totals['playlists']} ({totals['entries']} entries)",
        f"- **Playlists with problems:** {totals['playlists_with_issues']}",
        f"- **Playlists with guide-coverage notes:** {totals['playlists_with_warnings']}",
        f"- **Links published that the deep check called dead:** {totals['dead_links_published']}",
        f"- **Category shelf files:** {totals['shelf_files']} "
        f"({totals['shelf_problems']} problem(s))",
        f"- **Curated categories (in the published order):** {', '.join(result['group_order'])}",
        f"- **Maximum guides a header may advertise:** {result['max_header_guides']}",
        "",
        "## Playlists",
        "",
        "| Playlist | Entries | Groups in use | Out of order | Groups to normalise | "
        "Header guides | Dead links | EPG ids declared | EPG ids with listings |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in reports:
        categories = ", ".join(item["categories"].keys())
        declared_text = (f"{item['epg']['matched_ids']}/{item['epg']['playlist_ids']}"
                         f" ({item['epg']['coverage']:.1%})"
                         if item["epg"]["declared_ids"] else "no local guide")
        listed_text = (f"{item['epg']['ids_with_programmes']} "
                       f"({item['epg']['programme_coverage']:.1%})"
                       if item["epg"]["declared_ids"] else "-")
        lines.append(
            f"| `{item['file']}` | {item['entries']} | {categories} | {item['out_of_order']} | "
            f"{sum(item['non_canonical_groups'].values())} | {item.get('guides_advertised', 0)} | "
            f"{len(item['dead_links'])} | {declared_text} | {listed_text} |"
        )
    lines += ["", "## Problems", ""]
    shelf_issues = list(shelf.get("issues") or [])
    if violating or shelf_issues:
        for item in violating:
            lines.append(f"### `{item['file']}`")
            lines.append("")
            lines.extend(f"- {issue}" for issue in item["issues"])
            for entry in item["dead_links"][:20]:
                lines.append(f"  - dead: {entry['name']} — {entry['reason']}")
            lines.append("")
        if shelf_issues:
            lines.append("### Category shelf")
            lines.append("")
            lines.extend(f"- {issue}" for issue in shelf_issues)
            lines.append("")
    else:
        lines.append("None: every playlist is canonical, in order, and free of links the deep "
                     "check confirmed dead.")
    lines += ["", "## Category shelf", ""]
    if shelf.get("skipped"):
        lines.append(f"Not checked: {shelf.get('note') or 'no shelf directory'}.")
    else:
        lines += [
            f"The `{shelf['dir']}/` shelf is re-planned from the published playlists on every "
            f"run: **{len(shelf['files'])} of {shelf.get('expected_files', len(shelf['files']))} "
            f"file(s) present**, {sum(1 for row in shelf['files'] if row['status'] == 'ok')} in "
            "step with the published order.",
            "",
            "| # | Shelf file | Scope | Category | Channels | Status |",
            "|---|---|---|---|---:|---|",
        ]
        for index, row in enumerate(shelf["files"], 1):
            lines.append(f"| {index} | `{row['file']}` | {row['scope']} | {row['category']} | "
                         f"{row['channels']} | {row['status']} |")
        lines += [
            "",
            "Each file is a slice of an already published playlist, so its sorting is the "
            "published sorting: curated categories in order, each followed by its own Backups "
            "group, the long tail by size, `Other` last, and a channel's feeds side by side "
            "with the best quality first. `scripts/build_categories.py` writes the shelf and "
            "`scripts/verify_playlists.py --require-shelf` fails a run that leaves it stale.",
        ]
    warned = [item for item in reports if item.get("warnings")]
    if warned:
        lines += ["", "## Guide coverage notes", ""]
        for item in warned:
            for warning in item["warnings"]:
                lines.append(f"- `{item['file']}`: {warning}")
    epg_sources = totals.get("epg_sources") or {}
    if epg_sources:
        lines += [
            "",
            "## EPG sources (last deep guide check)",
            "",
            f"- **Checked:** {epg_sources.get('finished_utc') or 'unknown'}",
            "- **Upstream status counts:** " + (", ".join(
                f"{key}: {value}" for key, value in (epg_sources.get("counts") or {}).items())
                or "no upstream guide in the last report"),
            f"- **Own guides:** {epg_sources.get('own_repo_guides') or 0} "
            "(this repository's own `EPG/*.xml`, recorded but not counted above - a "
            "private repository answers 404 for them and that says nothing about the "
            "guides a player needs)",
            "",
            "A guide that is unreachable upstream is dropped by `scripts/epg_check.py`, so a "
            "channel whose guide is not merged correctly shows as missing coverage above "
            "rather than as a wrong schedule.",
        ]
    lines += [
        "",
        "## Notes",
        "",
        "- Categories and ordering come from `scripts/categorize.py` and are applied by "
        "`scripts/scraper.py` when it publishes, `scripts/link_check.py --patch` when it removes "
        "dead links, `scripts/rebuild_playlists.py` and `scripts/resort_playlists.py` offline.",
        "- EPG coverage counts the `tvg-id` values the advertised local guide declares. A channel "
        "without a public schedule counts as uncovered; its ID is still declared so a player "
        "asks for it instead of guessing.",
        "- The `categories/` shelf (headline file `categories/USA.m3u`) is written by "
        "`scripts/build_categories.py` and checked here against the published playlists, so its "
        "sorting cannot drift from theirs.",
        "",
    ]
    (checks_dir / "VERIFY.md").write_text("\n".join(lines), encoding="utf-8")
    log(f"[verify] wrote {relative(checks_dir / 'VERIFY.md')} and verify.json")
    if shelf.get("skipped"):
        log(f"[verify] shelf not checked: {shelf.get('note')}")
    else:
        log(f"[verify] shelf {shelf['dir']}: {len(shelf['files'])} file(s), "
            f"{len(shelf_issues)} problem(s)"
            + ("; " + "; ".join(shelf_issues[:3]) if shelf_issues else ""))
    if args.strict and (violating or shelf_issues):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
