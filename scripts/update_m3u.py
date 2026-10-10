#!/usr/bin/env python3
"""
Quick update for M3U files you already have.

Point it at any playlist on disk - the one published here, one you downloaded
from somewhere else, or a folder full of them - and it:

1. **re-checks every link** concurrently (shallow by default: it proves a server
   answers with a playlist or media; ``--deep`` proves a media segment plays);
2. **repairs** what broke: a dead link is replaced by the channel's backup in
   the same file, or by a working candidate from ``--pool``, and only removed
   when nothing else plays;
3. **re-categorises and re-orders** the file with `scripts/categorize.py`, so
   channels sit in the curated groups (Sports, Lifestyle, Fox, CBS, NBC, NBC
   Sports, Cartoons, PBS, Game Shows, each with its own Backups group);
4. **reports** what changed, and never writes a file that got worse.

Safety nets, on by default:

* a playlist is only rewritten when at least ``--min-working-ratio`` of its
  links still answer, and never loses more than ``--max-remove-ratio`` in
  one run - a bad network day cannot gut a good file;
* transient failures (timeouts, 5xx, 401/403) are kept, not deleted: only
  confirmed-dead links (404/410, DNS failure, refused, an HTML page) are
  candidates for replacement.

    python scripts/update_m3u.py my-list.m3u                 # check, repair, rewrite
    python scripts/update_m3u.py my-list.m3u --dry-run       # report only
    python scripts/update_m3u.py playlists/*.m3u --pool playlists/PremiumTV_all.m3u
    python scripts/update_m3u.py my-list.m3u --offline       # tidy categories only
    python scripts/update_m3u.py my-list.m3u --deep --workers 96

Needs network access for the checks. The sandbox this repository is developed in
can reach GitHub only, so the verification runs in the scheduled workflow
(.github/workflows/quick-update.yml) and on your own machine.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import datetime as dt
import glob
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import categorize  # noqa: E402
import link_check  # noqa: E402
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MIN_WORKING_RATIO = 0.20
DEFAULT_MAX_REMOVE_RATIO = 0.35
DEAD_STATUSES = {"offline", "invalid"}          # link_check buckets
SHALLOW_DEAD = {"dead"}                          # scraper.check_channel buckets
TRANSIENT_STATUSES = {"unreachable", "blocked", "unsupported"}


def log(msg: str) -> None:
    print(msg, flush=True)


# --------------------------------------------------------------------------- #
# Checking
# --------------------------------------------------------------------------- #
def check_channels(channels: list, workers: int, per_host: int, timeout: float,
                   retries: int, deep: bool) -> dict[str, dict]:
    """Check every channel concurrently. Returns url -> result dict."""
    results: dict[str, dict] = {}
    limiter = scraper.HostLimiter(per_host)
    started = time.monotonic()

    def work(channel):
        if deep:
            result = link_check.verify_link(channel, timeout, retries, deep=True,
                                            host_limiter=limiter)
            result["status"] = result.get("status", "unreachable")
            return channel.url, result
        scraper.check_channel(channel, timeout, retries, limiter)
        status = {"alive": "working", "dead": "offline",
                  "unverified": "unreachable", "unchecked": "unreachable"}.get(
                      channel.status, "unreachable")
        return channel.url, {"status": status, "reason": channel.reason,
                             "name": channel.name}

    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(work, channel) for channel in channels]
        for index, future in enumerate(cf.as_completed(futures), 1):
            try:
                url, result = future.result()
            except Exception:  # noqa: BLE001 - never fail the whole run
                continue
            results[url] = result
            if index % 250 == 0:
                log(f"  ...checked {index}/{len(futures)}")
    log(f"[update] checked {len(results)} links in {time.monotonic() - started:.1f}s")
    return results


def is_deep_dead(result: dict) -> bool:
    return result.get("status") in DEAD_STATUSES


def is_shallow_dead(result: dict) -> bool:
    return result.get("status") in SHALLOW_DEAD or result.get("status") in DEAD_STATUSES


def apply_quarantine(results: dict[str, dict], path: Path, days: float = 7.0) -> int:
    """Treat links the deep check already quarantined as broken.

    Those are the "it loads but never plays" links: the server answers with an
    HLS playlist whose segments 404, so a shallow check calls them fine. The
    nightly deep check records them in playlists/checks/quarantine.json; this
    reuses that verdict instead of trusting the shallow answer.
    """
    if not path or not Path(path).is_file():
        return 0
    entries = scraper.load_quarantine(Path(path), days)
    held = 0
    for url, entry in entries.items():
        current = results.get(url)
        if not current or is_shallow_dead(current):
            continue
        results[url] = {
            "status": "offline",
            "reason": f"quarantined: {entry.get('reason') or 'served no media on the deep check'}",
            "name": current.get("name", ""),
        }
        held += 1
    if held:
        log(f"[update] {held} link(s) held back by the deep-check quarantine")
    return held


# --------------------------------------------------------------------------- #
# Repair
# --------------------------------------------------------------------------- #
def backup_index(channels: list) -> dict[str, list]:
    """channel key -> spare links already in the file, in order."""
    index: dict[str, list] = collections.defaultdict(list)
    for channel in channels:
        index[categorize.channel_key(channel.name, categorize.country_of(channel))].append(channel)
    return index


def load_pool(paths: list[str]) -> dict[str, list]:
    """channel key -> candidate links from other playlists on disk."""
    pool: dict[str, list] = collections.defaultdict(list)
    for raw in paths:
        for match in sorted(glob.glob(raw)):
            path = Path(match)
            if not path.is_file():
                continue
            channels, _ = scraper.parse_m3u(
                path.read_text(encoding="utf-8", errors="replace"), path.stem)
            for channel in channels:
                pool[categorize.channel_key(channel.name,
                                            categorize.country_of(channel))].append(channel)
            log(f"[update] pool: {len(channels)} candidates from {path}")
    return pool


def promote_backup(dead, backups: list, results: dict[str, dict], dead_fn) -> object | None:
    """Return a live spare for a dead channel from the file's own backups."""
    for candidate in backups:
        if candidate is dead or candidate.url == dead.url:
            continue
        result = results.get(candidate.url)
        if result and not dead_fn(result):
            return candidate
    return None


def find_replacements(dead_channels: list, pool: dict[str, list], results: dict[str, dict],
                      used: set[str], workers: int, per_host: int, timeout: float,
                      retries: int, dead_fn, max_candidates: int = 4) -> dict[str, object]:
    """Check pool candidates for channels whose every link died."""
    wanted: list = []
    for dead in dead_channels:
        key = categorize.channel_key(dead.name, categorize.country_of(dead))
        candidates = [item for item in pool.get(key, [])
                      if item.url not in used and item.url != dead.url][:max_candidates]
        wanted.extend(candidates)
    if not wanted:
        return {}

    log(f"[update] testing {len(wanted)} replacement candidates for "
        f"{len(dead_channels)} dead channels")
    fresh = check_channels(wanted, workers, per_host, timeout, retries, deep=False)
    results.update(fresh)

    replacements: dict[str, object] = {}
    for dead in dead_channels:
        key = categorize.channel_key(dead.name, categorize.country_of(dead))
        for candidate in pool.get(key, []):
            if candidate.url in used or candidate.url == dead.url:
                continue
            result = fresh.get(candidate.url)
            if result and not dead_fn(result):
                replacements[dead.url] = candidate
                used.add(candidate.url)
                break
    return replacements


# --------------------------------------------------------------------------- #
# One file
# --------------------------------------------------------------------------- #
def update_file(path: Path, args, pool: dict[str, list], guide_check=None) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    header = next((line.strip() for line in text.splitlines()
                   if line.strip().startswith("#EXTM3U")), "#EXTM3U")
    channels, _ = scraper.parse_m3u(text, path.stem)
    if not channels:
        return {"file": str(path), "channels": 0, "status": "empty", "written": False}

    stats: collections.Counter = collections.Counter()
    if args.offline:
        results = {}
        log(f"[update] {path}: offline run, categories only")
    else:
        results = check_channels(channels, args.workers, args.per_host_workers,
                                 args.timeout, args.retries, args.deep)
        if args.quarantine:
            apply_quarantine(results, Path(args.quarantine), args.quarantine_days)
        dead_fn = is_deep_dead if args.deep else is_shallow_dead
        buckets: collections.Counter = collections.Counter(
            results.get(channel.url, {}).get("status", "unreachable") for channel in channels)
        for status, count in buckets.items():
            stats[f"status_{status}"] = count
        working = [channel for channel in channels
                   if not dead_fn(results.get(channel.url, {"status": "unreachable"}))]
        ratio = len(working) / max(len(channels), 1)
        stats["playable"] = len(working)
        stats["dead"] = len(channels) - len(working)
        if ratio < args.min_working_ratio:
            return {
                "file": str(path), "channels": len(channels), "status": "aborted",
                "reason": f"only {ratio:.0%} of links answer (minimum "
                          f"{args.min_working_ratio:.0%}); file left untouched",
                "written": False, "stats": dict(stats),
            }

        # 1. Dead link with a live backup in the same file -> promote the backup.
        index = backup_index(channels)
        used = {channel.url for channel in channels}
        restored: dict[str, object] = {}
        consumed: set[str] = set()          # spares moved up to replace a dead link
        still_dead: list = []
        for channel in channels:
            if not dead_fn(results.get(channel.url, {"status": "unreachable"})):
                continue
            key = categorize.channel_key(channel.name, categorize.country_of(channel))
            replacement = promote_backup(channel, index.get(key, []), results, dead_fn)
            if replacement is not None:
                restored[channel.url] = replacement
                consumed.add(replacement.url)
                stats["promoted"] += 1
            else:
                still_dead.append(channel)

        # 2. Nothing left in the file -> try the pool.
        replacements: dict[str, object] = {}
        if still_dead and pool and not args.no_pool:
            replacements = find_replacements(still_dead, pool, results, used, args.workers,
                                             args.per_host_workers, args.timeout,
                                             args.retries, dead_fn,
                                             max_candidates=args.pool_candidates)
            stats["replaced"] = len(replacements)

        # 3. Whatever is still dead goes, unless the run would gut the file.
        final_dead = [channel for channel in still_dead if channel.url not in replacements]
        if final_dead and len(final_dead) > args.max_remove_ratio * len(channels):
            return {
                "file": str(path), "channels": len(channels), "status": "aborted",
                "reason": f"removing {len(final_dead)} of {len(channels)} entries exceeds "
                          f"--max-remove-ratio {args.max_remove_ratio:.0%}; file left untouched",
                "written": False, "stats": dict(stats),
            }

        removed_urls = {channel.url for channel in final_dead}
        stats["removed"] = len(removed_urls)
        survivors: list = []
        for channel in channels:
            if channel.url in removed_urls:
                continue
            if channel.url in consumed:
                # The spare was moved up to replace the dead main link; keeping it
                # as well would publish the same URL twice.
                continue
            if channel.url in restored:
                spare = restored[channel.url]
                channel.url = spare.url
                channel.name = categorize.clean_display_name(channel.name)
                channel.extra = list(spare.extra)
                stats["promoted_done"] += 1
            elif channel.url in replacements:
                spare = replacements[channel.url]
                channel.url = spare.url
                channel.name = categorize.clean_display_name(channel.name)
                channel.extra = list(spare.extra)
            survivors.append(channel)
        channels = survivors
        stats["removed_urls"] = sorted(removed_urls)

    # 4. Categories and order (always - it is what makes the file browsable).
    if not args.no_recategorize:
        if not args.no_corpus:
            categorize.load_corpus()
        ordered = categorize.build_main_order(channels, max_backups=args.max_backups)
    else:
        ordered = sorted(channels, key=lambda ch: categorize.sort_key(ch))
    counts = categorize.category_counts(ordered)

    utc_s = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    title = (f"{len(ordered)} channels - quick update {utc_s} "
             f"({len(counts)} categories, {sum(1 for c in counts if categorize.is_backup_group(c))} "
             f"backup groups)")
    target = Path(args.output_dir) / path.name if args.output_dir else path
    if not args.dry_run:
        target.parent.mkdir(parents=True, exist_ok=True)
        lines = [header, f"# {title}"]
        lines.extend(channel.to_m3u() for channel in ordered)
        target.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {
        "file": str(path),
        "output": str(target),
        "channels": len(ordered),
        "groups": len(counts),
        "status": "updated" if not args.dry_run else "dry-run",
        "written": not args.dry_run,
        "stats": {key: value for key, value in stats.items() if key != "removed_urls"},
        "removed": stats.get("removed_urls", []),
        "counts": dict(counts),
    }


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Quickly re-check, repair and re-order M3U files you already have.")
    parser.add_argument("playlists", nargs="+", help="M3U files or globs to update")
    parser.add_argument("--pool", nargs="*", default=[],
                        help="playlists to draw replacement links from "
                             "(e.g. playlists/PremiumTV_all.m3u playlists/sources/*.m3u)")
    parser.add_argument("--no-pool", action="store_true", help="never pull in replacements")
    parser.add_argument("--pool-candidates", type=int, default=4,
                        help="how many pool candidates to test per dead channel")
    parser.add_argument("--workers", type=int, default=64, help="concurrent checks")
    parser.add_argument("--per-host-workers", type=int, default=4,
                        help="concurrent checks per host")
    parser.add_argument("--timeout", type=float, default=8.0, help="per-request timeout")
    parser.add_argument("--retries", type=int, default=1, help="retries per link")
    parser.add_argument("--deep", action="store_true",
                        help="prove a media segment plays (slower, stricter)")
    parser.add_argument("--offline", action="store_true",
                        help="skip every check: only re-group and re-order")
    parser.add_argument("--no-recategorize", action="store_true",
                        help="keep the group titles the file already has")
    parser.add_argument("--no-corpus", action="store_true",
                        help="do not learn categories from the local corpus")
    parser.add_argument("--max-backups", type=int, default=0,
                        help="keep at most N spare links per channel (0 = all)")
    parser.add_argument("--min-working-ratio", type=float, default=DEFAULT_MIN_WORKING_RATIO,
                        help="abort a file when fewer than this share of links answer")
    parser.add_argument("--max-remove-ratio", type=float, default=DEFAULT_MAX_REMOVE_RATIO,
                        help="abort a file when it would lose more than this share")
    parser.add_argument("--output-dir", default="", help="write updated copies here")
    parser.add_argument("--report", default="", help="write a JSON report to this path")
    parser.add_argument("--quarantine", default="playlists/checks/quarantine.json",
                        help="deep-check quarantine file ('' to ignore it)")
    parser.add_argument("--quarantine-days", type=float, default=7.0,
                        help="how long a quarantine entry stays relevant")
    parser.add_argument("--dry-run", action="store_true", help="report only, write nothing")
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    paths: list[Path] = []
    for raw in args.playlists:
        matches = sorted(glob.glob(raw))
        if not matches and Path(raw).is_file():
            matches = [raw]
        for match in matches:
            path = Path(match)
            if path.is_file():
                paths.append(path)
            else:
                log(f"[update] skipping {raw}: not a file")
    if not paths:
        log("[update] nothing to do: no readable playlists given")
        return 1

    pool = load_pool(args.pool) if (args.pool and not args.no_pool and not args.offline) else {}
    summaries = []
    exit_code = 0
    for path in paths:
        summary = update_file(path, args, pool)
        summaries.append(summary)
        stats = summary.get("stats", {})
        if summary["status"] == "aborted":
            exit_code = 1
            log(f"[update] {path}: ABORTED - {summary.get('reason', '')}")
            continue
        log(f"[update] {path}: {summary['channels']} channels, {summary['groups']} groups, "
            f"{stats.get('playable', '-')} answered, {stats.get('dead', 0)} confirmed dead, "
            f"{stats.get('status_unreachable', 0)} unreachable (kept), "
            f"{stats.get('promoted', 0)} backup(s) promoted, "
            f"{stats.get('replaced', 0)} replaced from pool, {stats.get('removed', 0)} removed"
            + (" [dry run]" if args.dry_run else ""))

    if args.report and not args.dry_run:
        report_path = Path(args.report)
        if not report_path.is_absolute():
            report_path = ROOT / report_path
        report_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "updated_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "options": {key: value for key, value in vars(args).items()
                        if key not in ("playlists",)},
            "files": summaries,
        }
        report_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        log(f"[update] report: {report_path}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
