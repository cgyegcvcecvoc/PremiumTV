#!/usr/bin/env python3
"""Repository housekeeping: the slow cleanup the daily and nightly runs never do.

Every other script in ``scripts/`` looks at the *playlists* - is this link alive,
is this guide serving listings, is this channel in the right category. This one
looks at the *repository* and asks the questions nobody asks on a run that has to
finish in five minutes:

* **Do the append-only logs still have a readable size?** Four ``logs/*.txt``
  files are append-only by design and each nightly run adds a block per removed
  link to them. Left alone they crossed a megabyte each within days, which makes
  every ``git clone`` of this repository carry a history nobody reads. The run
  keeps the last ``--keep-runs`` blocks of each (at a block boundary, never
  mid-entry) and leaves the header banner alone.
* **Is anything left behind that nothing owns?** An ``EPG/<Country>.xml`` whose
  country playlist no longer exists, a swap file from a build that was cut off
  mid-write, a ``__pycache__`` directory next to the scripts.
* **Is the published data actually current?** ``STATUS.md`` from three weeks ago
  and a merged guide whose every listing has aged out of the window are both
  failures of the pipeline that no individual run reports as its own problem -
  the scrape succeeds, the guide build succeeds, and the player still gets
  nothing. This is the check that catches the two of them disagreeing.
* **Has the quarantine accumulated entries no run will ever look at again?**
  ``checks/quarantine.json`` is re-read by the scraper on every run; malformed
  and unreadably old entries are dropped here (the deep check prunes by age when
  it writes, so this only catches what it cannot).

It never touches a playlist entry, a channel name or a URL - removing dead
channels is ``scripts/link_check.py --patch`` (run before this in the biweekly
workflow), and it has the working-ratio limits for that job. Two files are
explicitly off-limits: ``logs/run-*.txt`` are push triggers for other workflows,
so rewriting them from a workflow would start those runs again (see
``TRIGGER_FILES``).

Outputs:

    playlists/checks/CLEANUP.md       what was trimmed, removed and found
    playlists/checks/cleanup.json     the same, machine-readable
    playlists/logs/cleanup-edits.txt  append-only history of cleanup runs

    python scripts/cleanup_repo.py                    # report only (nothing changes)
    python scripts/cleanup_repo.py --apply            # trim logs, remove orphans
    python scripts/cleanup_repo.py --apply --keep-runs 20
    python scripts/cleanup_repo.py --strict --apply   # exit 1 when a problem remains
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import epg_build  # noqa: E402  (reuses the guide window scanner)
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUT = ROOT / "playlists"
DEFAULT_EPG_DIR = ROOT / "EPG"

# Append-only logs and the line that opens a run block in each of them. Files that
# a run rewrites from scratch (scrape-log.txt, errors.txt, resort-log.txt) are not
# listed: they cannot grow past one run's output by construction.
RUN_BLOCK_LOGS = {
    "link-check-edits.txt": r"^## ",
    "epg-check-edits.txt": r"^## ",
    "epg-build-edits.txt": r"^## ",
}
# log-edits.txt is banner + blocks of the same 88-character separator the scraper
# uses everywhere else, so its blocks are only the separators that open a record.
RUN_ID_SEPARATORS = {"log-edits.txt": "=" * 88}

# Never rewrite these: a push that changes one of them starts a workflow, and a
# workflow that changes one of them would start that workflow again.
TRIGGER_FILES = "run-"

# Artifacts whose age says something about the pipeline, not about the file.
STALE_REPORTS = {
    "playlists/STATUS.md": 36.0,             # every run rewrites it; 7 scrapes' worth
    "playlists/report.json": 36.0,
    "playlists/checks/link-check.json": 25 * 24.0,   # nightly
    "playlists/checks/epg-check.json": 25 * 24.0,
    "playlists/checks/epg-build.json": 26 * 24.0,    # twice a day
    "playlists/checks/verify.json": 25 * 24.0,
}
# A guide whose newest listing is further behind than this is not a guide any
# more, whatever its channel count says.
GUIDE_STALE_HOURS = 12.0
DEFAULT_KEEP_RUNS = 30
DEFAULT_MAX_LOG_KB = 512
DEFAULT_MAX_LOG_LINES = 2500


def log(msg: str) -> None:
    print(msg, flush=True)


def display_path(path) -> str:
    """Repo-relative path for reports; absolute when the path lives elsewhere."""
    try:
        return str(Path(path).relative_to(ROOT))
    except ValueError:
        return str(path)


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def file_age_hours(path: Path, now: dt.datetime | None = None) -> float | None:
    """Hours since the file was last written, or None when it does not exist."""
    if not path.is_file():
        return None
    modified = dt.datetime.fromtimestamp(path.stat().st_mtime, dt.timezone.utc)
    return round(((now or utc_now()) - modified).total_seconds() / 3600.0, 1)


# --------------------------------------------------------------------------- #
# Log rotation
# --------------------------------------------------------------------------- #
def split_blocks(lines: list[str], pattern: str) -> tuple[list[str], list[list[str]]]:
    """(preamble, blocks) - a block starts at a line matching ``pattern``.

    Everything before the first block start is the file's banner and always kept:
    the header of ``log-edits.txt`` is what explains the format to a reader who
    opens the file in two years.
    """
    matcher = re.compile(pattern)
    starts = [index for index, line in enumerate(lines) if matcher.match(line)]
    if not starts:
        return lines, []
    blocks = []
    for position, start in enumerate(starts):
        stop = starts[position + 1] if position + 1 < len(starts) else len(lines)
        blocks.append(lines[start:stop])
    return lines[:starts[0]], blocks


def fit_blocks(preamble: list[str], blocks: list[list[str]], keep_runs: int,
               max_lines: int) -> tuple[list[list[str]], str]:
    """The blocks to keep, and why the rest go.

    Keeping the last N run blocks is not enough on its own: one pathological run -
    a guide check that logged a removal line per country playlist, say - puts
    more in a single block than the whole budget, so a second limit drops oldest
    blocks until the file fits, and always keeps the newest one even if that one
    block is itself too big (the alternative is a tool that deletes the only
    record of what the last run did).
    """
    if keep_runs > 0 and len(blocks) > keep_runs:
        kept = list(blocks[-keep_runs:])
        why = f"past the last {keep_runs} runs"
    else:
        kept = list(blocks)
        why = ""
    def size(items: list[list[str]]) -> int:
        return len(preamble) + sum(len(item) for item in items)
    while len(kept) > 1 and max_lines > 0 and size(kept) > max_lines:
        kept.pop(0)
        why = f"over {max_lines} lines"
    return kept, why


def trimmed_file(path: Path, preamble: list[str], blocks: list[list[str]],
                 keep_runs: int, max_lines: int, apply: bool) -> dict:
    """Shared tail of both rotators: decide, report, and write when asked."""
    lines = preamble + [line for block in blocks for line in block]
    entry = {"file": display_path(path), "lines": len(lines), "blocks": len(blocks),
             "dropped_blocks": 0, "kept_blocks": len(blocks),
             "bytes_before": path.stat().st_size, "bytes_after": path.stat().st_size,
             "written": False, "reason": ""}
    kept, why = fit_blocks(preamble, blocks, keep_runs, max_lines)
    if len(kept) == len(blocks):
        return entry
    text = "\n".join(list(preamble) + [line for block in kept for line in block]) + "\n"
    entry.update(dropped_blocks=len(blocks) - len(kept), kept_blocks=len(kept),
                 bytes_after=len(text.encode()), reason=why)
    if apply:
        path.write_text(text, encoding="utf-8")
        entry["written"] = True
    log(f"[cleanup] {path.name}: keeping {len(kept)} of {len(blocks)} run blocks "
        f"({entry['bytes_before'] // 1024} KB -> {entry['bytes_after'] // 1024} KB, "
        f"{why})" + ("" if apply else " [report only]"))
    return entry


def rotate_log(path: Path, pattern: str, keep_runs: int, max_lines: int,
               apply: bool) -> dict:
    """Drop all but the last ``keep_runs`` run blocks of an append-only log."""
    if not path.is_file():
        return {"file": display_path(path), "lines": 0, "blocks": 0,
                "dropped_blocks": 0, "kept_blocks": 0, "bytes_before": 0,
                "bytes_after": 0, "written": False, "skipped": "missing"}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    preamble, blocks = split_blocks(lines, pattern)
    return trimmed_file(path, preamble, blocks, keep_runs, max_lines, apply)


def rotate_run_id_log(path: Path, separator: str, keep_runs: int, max_lines: int,
                     apply: bool) -> dict:
    """Same, for the log whose blocks start with a separator line above ``RUN ID:``.

    ``log-edits.txt`` uses the banner separator for its header too, so a plain
    "split on the separator" would cut the banner into blocks and then keep
    trimming it; only separators that open a record end one.
    """
    if not path.is_file():
        return {"file": display_path(path), "lines": 0, "blocks": 0,
                "dropped_blocks": 0, "kept_blocks": 0, "bytes_before": 0,
                "bytes_after": 0, "written": False, "skipped": "missing"}
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    starts = [index for index, line in enumerate(lines)
              if line.strip() == separator
              and index + 1 < len(lines) and lines[index + 1].startswith("RUN ID:")]
    if not starts:
        return {"file": display_path(path), "lines": len(lines), "blocks": 0,
                "dropped_blocks": 0, "kept_blocks": 0,
                "bytes_before": path.stat().st_size,
                "bytes_after": path.stat().st_size, "written": False,
                "skipped": "no run block found"}
    stops = starts[1:] + [len(lines)]
    preamble, blocks = lines[:starts[0]], [lines[a:b] for a, b in zip(starts, stops,
                                                                      strict=True)]
    return trimmed_file(path, preamble, blocks, keep_runs, max_lines, apply)


# --------------------------------------------------------------------------- #
# Orphans and leftovers
# --------------------------------------------------------------------------- #
def orphan_guides(epg_dir: Path, playlists_dir: Path, merged_names: set[str]) -> list[Path]:
    """Guide files in ``epg_dir`` that no published playlist refers to any more.

    A country guide is rebuilt from the matching ``playlists/countries/<C>.m3u``,
    so a guide whose playlist was dropped (or renamed) is served to nobody and
    stays in the repository forever - and ``git`` keeps every version of a 60 MB
    file it has ever seen.
    """
    if not epg_dir.is_dir():
        return []
    owned = {path.stem for path in playlists_dir.glob("countries/*.m3u")}
    orphans = []
    for path in sorted(epg_dir.glob("*.xml")):
        if path.stem in owned or path.stem in merged_names:
            continue
        orphans.append(path)
    for path in sorted(epg_dir.glob("*.xml.gz")):
        if path.stem.replace(".xml", "") in merged_names:
            continue
        if not (epg_dir / path.name.replace(".gz", "")).is_file():
            orphans.append(path)
    return orphans


def stray_files() -> list[Path]:
    """Swap files and byte-code caches left in the tree by an interrupted run."""
    found: list[Path] = []
    for directory in (ROOT / "EPG", ROOT / "playlists", ROOT / "scripts"):
        if not directory.is_dir():
            continue
        found.extend(sorted(directory.glob(".*.tmp")))
        found.extend(sorted(directory.glob("*.tmp")))
        found.extend(sorted(directory.glob("*.pyc")))
    for directory in (ROOT / "scripts", ROOT / "tests"):
        cache = directory / "__pycache__"
        if cache.is_dir():
            found.append(cache)
    return [path for path in found if path.exists()]


def empty_playlists(playlists_dir: Path) -> list[Path]:
    """Published playlists that hold no channel at all."""
    empty = []
    for path in sorted(playlists_dir.glob("**/*.m3u")):
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                if not any(line.strip() and not line.startswith("#") for line in handle):
                    empty.append(path)
        except OSError:
            continue
    return empty


# --------------------------------------------------------------------------- #
# Currency of the published data
# --------------------------------------------------------------------------- #
def stale_reports(limit_hours: dict) -> list[dict]:
    out = []
    for relative, limit in limit_hours.items():
        path = ROOT / relative
        age = file_age_hours(path)
        if age is None:
            out.append({"file": relative, "age_hours": None, "limit_hours": limit,
                        "problem": "missing"})
        elif age > limit:
            out.append({"file": relative, "age_hours": age, "limit_hours": limit,
                        "problem": f"{age:.0f}h old, no run has rewritten it in "
                                   f"{limit / 24:.0f} days"})
    return out


def guide_is_current(epg_dir: Path, name: str, ahead_hours: float,
                     window_hours: float) -> dict:
    """Does the published merged guide still have a listing inside a live window?

    This is the failure mode a green pipeline cannot see: a guide build can be
    refused by its own safety gate for days, leaving the previous file published
    while its listings age out. Players then show an empty grid for every channel
    and every run still reports success.
    """
    xml_path = epg_dir / f"{name}.xml"
    now = utc_now()
    result = {"guide": display_path(xml_path), "exists": xml_path.is_file(),
              "size_kb": (xml_path.stat().st_size // 1024) if xml_path.is_file() else 0,
              "age_hours": file_age_hours(xml_path, now), "live_channels": 0,
              "problem": ""}
    if not xml_path.is_file():
        result["problem"] = "no merged guide is published"
        return result
    start = now - dt.timedelta(hours=window_hours)
    end = now + dt.timedelta(hours=ahead_hours)
    live = epg_build.channels_with_listings(xml_path, start, end)
    result["live_channels"] = live
    if not live:
        result["problem"] = (f"no listing inside the next {ahead_hours:.0f}h - the guide "
                             f"is {result['size_kb'] // 1024} MB of expired data; "
                             f"scripts/epg_build.py --force --patch has to publish a "
                             f"fresh one")
    elif result["age_hours"] is not None and result["age_hours"] > window_hours:
        result["problem"] = (f"last written {result['age_hours']:.0f}h ago, older than the "
                             f"{window_hours:.0f}h window a player asks for")
    return result


def compact_quarantine(checks_dir: Path, days: float, apply: bool) -> dict:
    """Drop the quarantine entries whose clock has run out, and count the rest.

    ``scraper.load_quarantine()`` ignores an entry once its ``last_seen_utc`` is
    older than ``days``, but it never rewrites the file - the deep check only
    compacts it on a run that patches, so on a repository whose nightly check is
    failing the file keeps every link it ever held back. An entry with no usable
    timestamp, on the other hand, is *honoured forever* by that same reader, so
    dropping it here would quietly re-publish a dead link: it is counted and
    reported instead of removed.
    """
    path = checks_dir / scraper.QUARANTINE_FILENAME
    result = {"file": display_path(path), "entries_before": 0, "entries_after": 0,
              "dropped": 0, "undated": 0, "written": False}
    if not path.is_file():
        result["skipped"] = "missing"
        return result
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        result["problem"] = f"unreadable ({type(exc).__name__})"
        return result
    entries = data.get("entries")
    if not isinstance(entries, dict):
        result["problem"] = "no entries block"
        return result
    cutoff = utc_now() - dt.timedelta(days=max(days, 0))
    keep: dict = {}
    undated = 0
    for url, entry in entries.items():
        if not url or not isinstance(entry, dict):
            continue
        last_seen = scraper.parse_utc_iso(str(entry.get("last_seen_utc") or ""))
        if last_seen is None:
            undated += 1
            keep[url] = entry
            continue
        if last_seen.replace(tzinfo=None) < cutoff.replace(tzinfo=None):
            continue
        keep[url] = entry
    result.update(entries_before=len(entries), entries_after=len(keep),
                  dropped=len(entries) - len(keep), undated=undated)
    if keep == entries or not result["dropped"]:
        return result
    if apply:
        data["entries"] = keep
        data["count"] = len(keep)
        data["updated_utc"] = utc_now().isoformat(timespec="seconds").replace("+00:00", "Z")
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        result["written"] = True
    log(f"[cleanup] quarantine: {result['entries_before']} -> {result['entries_after']} "
        f"entries ({result['dropped']} unreadable or past {days:g} days)"
        + ("" if apply else " [report only]"))
    return result


# --------------------------------------------------------------------------- #
# Report
# --------------------------------------------------------------------------- #
def append_edit_log(out_dir: Path, report: dict) -> Path:
    logs_dir = out_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / "cleanup-edits.txt"
    new = report["started_utc"].replace("T", " ").replace("Z", "")[:16]
    lines = [f"## {report['started_utc']} - {report['label']} "
             f"(repository cleanup, run {report['run_id']})"]
    lines.append(f"  outcome={report['outcome']}; {report['freed_bytes'] // 1024} KB freed"
                 + (" (report only, nothing written)" if not report["apply"] else ""))
    for entry in report["logs"]:
        if entry.get("dropped_blocks"):
            lines.append(f"  ~{new} trimmed {Path(entry['file']).name}: "
                         f"-{entry['dropped_blocks']} run blocks")
    for path_removed in report["removed"]:
        lines.append(f"  -removed {path_removed}")
    for problem in report["problems"]:
        lines.append(f"  * {problem}")
    lines.append("")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return path


def write_reports(out_dir: Path, report: dict) -> list:
    checks_dir = out_dir / "checks"
    checks_dir.mkdir(parents=True, exist_ok=True)
    (checks_dir / "cleanup.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Repository cleanup",
        "",
        f"- **Run:** {report['label']} (`{report['run_id']}`)",
        f"- **Started:** {report['started_utc']} | **Finished:** {report['finished_utc']} "
        f"| **Duration:** {report['duration_seconds']}s",
        f"- **Outcome:** **{report['outcome']}**"
        + ("" if report["apply"] else " (report only - pass `--apply` to change files)"),
        f"- **Space {'freed' if report['apply'] else 'this run would free'}:** "
        f"{report['freed_bytes'] // 1024} KB",
        f"- **Append-only logs trimmed:** {report['logs_trimmed']} file(s), "
        f"{report['blocks_dropped']} run block(s) dropped (budget: the last "
        f"{report['keep_runs']} runs and {report['max_log_lines']} lines per file)",
        f"- **Files {'removed' if report['apply'] else 'to remove'}: "
        f"{len(report['removed'])}** (orphaned guides, swap files, caches)",
        f"- **Problems left for a maintainer:** {len(report['problems'])}",
        "",
        "The biweekly run does the deep, slow sweep: `link_check.py --archives` "
        "re-tests and prunes the playlists no daily run patches (the priority "
        "playlist, the per-category playlists, the `categories/` shelf and the "
        "local source copies), then this report covers the repository itself. "
        "Removing dead channels stays `link_check.py`'s job; this tool never "
        "edits a playlist entry.",
        "",
        "## Logs",
        "",
    ]
    if not report["apply"]:
        # Report-only runs describe the future; say so before the table rather than
        # letting a reader think the trimming already happened.
        lines += ["*Nothing was written by this run - the last column below is the "
                  "size `--apply` would leave.*", ""]
    lines += ["| Log | Lines | Run blocks | Dropped | Size before | Size after |",
              "|---|---:|---:|---:|---:|---:|"]
    for entry in report["logs"]:
        lines.append(f"| `{Path(entry['file']).name}` | {entry.get('lines', 0)} | "
                     f"{entry.get('blocks', 0)} | {entry.get('dropped_blocks', 0)} | "
                     f"{entry.get('bytes_before', 0) // 1024} KB | "
                     f"{entry.get('bytes_after', 0) // 1024} KB |")
    if report["oversized_logs"]:
        lines += ["", "## Logs still over the size budget", "",
                  "| Log | Size |", "|---|---:|"]
        for entry in report["oversized_logs"]:
            lines.append(f"| `{Path(entry['file']).name}` | {entry['kb']} KB "
                         f"(budget {entry['budget_kb']} KB; {entry['kept']} run block(s), "
                         f"{entry['lines']} lines after trimming) |")
    lines += ["", "## Guide currency", "",
              f"- Merged guide `{report['guide']['guide']}`: "
              f"{report['guide']['size_kb'] // 1024} MB, "
              f"{report['guide']['live_channels']} channel(s) with a listing in the "
              f"live window"
              + (f" - **{report['guide']['problem']}**" if report["guide"].get("problem")
                 else " - current"),
              f"- Quarantine: {report['quarantine'].get('entries_before', 0)} read, "
              f"{report['quarantine'].get('entries_after', 0)} kept, "
              f"{report['quarantine'].get('dropped', 0)} expired or malformed dropped"
              + (f", {report['quarantine']['undated']} without a usable timestamp "
                 f"(kept: the scraper honours those until they are cleared by hand)"
                 if report['quarantine'].get('undated') else "")]
    if report["stale_reports"]:
        lines += ["", "## Reports no run has refreshed", "",
                  "| File | Problem |", "|---|---|"]
        for entry in report["stale_reports"]:
            lines.append(f"| `{entry['file']}` | {entry['problem']} |")
    if report["empty_playlists"]:
        lines += ["", "## Empty playlists", ""]
        lines += [f"- `{name}` holds no channel" for name in report["empty_playlists"]]
    if report["removed"]:
        lines += ["", "## Removed", ""]
        lines += [f"- `{name}`" for name in report["removed"]]
    if report["problems"]:
        lines += ["", "## Needs a maintainer", ""]
        lines += [f"- {problem}" for problem in report["problems"]]
    else:
        lines += ["", "Nothing needs a maintainer: every artifact is current and no "
                      "orphan was found."]
    lines.append("")
    (checks_dir / "CLEANUP.md").write_text("\n".join(lines), encoding="utf-8")
    return [checks_dir / "cleanup.json", checks_dir / "CLEANUP.md"]


# --------------------------------------------------------------------------- #
# Run
# --------------------------------------------------------------------------- #
def run(args) -> dict:
    started = utc_now()
    out_dir = Path(args.out)
    epg_dir = Path(args.epg_dir)
    logs_dir = out_dir / "logs"
    freed = 0

    logs = []
    for name, pattern in RUN_BLOCK_LOGS.items():
        logs.append(rotate_log(logs_dir / name, pattern, args.keep_runs,
                               args.max_log_lines, args.apply))
    for name, separator in RUN_ID_SEPARATORS.items():
        logs.append(rotate_run_id_log(logs_dir / name, separator, args.keep_runs,
                                       args.max_log_lines, args.apply))
    for entry in logs:
        freed += max(0, entry.get("bytes_before", 0) - entry.get("bytes_after", 0))
    # Judge the size the run leaves behind, not the size it found: in a report-only
    # run the file on disk is still the untrimmed one, and complaining about that
    # size would report a problem this very run has already solved.
    size_after = {item["file"]: item for item in logs}
    oversized = []
    for name in list(RUN_BLOCK_LOGS) + list(RUN_ID_SEPARATORS):
        path = logs_dir / name
        entry = size_after.get(display_path(path), {})
        kb = (entry.get("bytes_after") or (path.stat().st_size if path.is_file() else 0)) // 1024
        if kb > args.max_log_kb:
            oversized.append({"file": display_path(path), "kb": kb,
                              "budget_kb": args.max_log_kb,
                              "lines": entry.get("lines", 0),
                              "kept": entry.get("kept_blocks", 0)})

    merged_names = {args.name, f"{args.name}.xml"}
    orphans = orphan_guides(epg_dir, out_dir, merged_names) if args.orphans else []
    removed = []
    for path in orphans:
        size = path.stat().st_size
        if args.apply:
            path.unlink(missing_ok=True)
            freed += size
        removed.append(display_path(path))
    if removed:
        log(f"[cleanup] {len(removed)} orphan guide file(s) "
            + ("removed" if args.apply else "found (report only)") + ": "
            + ", ".join(Path(item).name for item in removed[:8]))

    stray = stray_files() if args.stray else []
    for path in stray:
        size = path.stat().st_size if path.is_file() else sum(
            item.stat().st_size for item in path.rglob("*") if item.is_file())
        if args.apply:
            shutil.rmtree(path, ignore_errors=True) if path.is_dir() else path.unlink()
            freed += size
        removed.append(display_path(path))

    quarantine = compact_quarantine(out_dir / "checks", args.quarantine_days, args.apply)
    guide = guide_is_current(epg_dir, args.name, args.ahead_hours, args.window_hours)
    stale = stale_reports(STALE_REPORTS) if args.stale_reports else []
    empty = [display_path(path) for path in empty_playlists(out_dir)]

    problems = []
    if guide.get("problem"):
        problems.append(f"published guide: {guide['problem']}")
    if quarantine.get("undated"):
        problems.append(f"{quarantine['undated']} quarantine entr(ies) have no usable "
                        f"last_seen_utc, so the scraper holds those links back forever - "
                        f"they are kept by this run; clear them by hand if that is wrong")
    for entry in stale:
        problems.append(f"{entry['file']}: {entry['problem']}")
    for name in empty:
        problems.append(f"{name} is published but holds no channel")
    for entry in oversized:
        problems.append(f"{entry['file']} is still {entry['kb']} KB after trimming to "
                        f"{args.keep_runs} runs / {args.max_log_lines} lines - lower "
                        f"--keep-runs or --max-log-lines, or move the history out of "
                        f"the repository")

    finished = utc_now()
    report = {
        "run_id": f"{started.strftime('%Y%m%dT%H%M%S')}Z-{started.microsecond // 1000:03d}",
        "label": args.label,
        "started_utc": started.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "finished_utc": finished.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "duration_seconds": round((finished - started).total_seconds(), 2),
        "apply": bool(args.apply),
        "keep_runs": args.keep_runs,
        "max_log_lines": args.max_log_lines,
        "max_log_kb": args.max_log_kb,
        "logs": logs,
        "logs_trimmed": sum(1 for entry in logs if entry.get("dropped_blocks")),
        "blocks_dropped": sum(entry.get("dropped_blocks", 0) for entry in logs),
        "oversized_logs": oversized,
        "removed": removed,
        "empty_playlists": empty,
        "stale_reports": stale,
        "guide": guide,
        "quarantine": quarantine,
        "freed_bytes": freed,
        "problems": problems,
        "outcome": "CLEAN" if not problems else "NEEDS ATTENTION",
    }
    written = write_reports(out_dir, report)
    if not args.dry_run_edit_log:
        report["edit_log"] = display_path(append_edit_log(out_dir, report))
        written.append(out_dir / "logs" / "cleanup-edits.txt")
    report["written"] = [display_path(path) for path in written]
    log(f"[cleanup] {report['outcome']}: {len(problems)} problem(s), "
        f"{report['blocks_dropped']} log block(s) and {len(removed)} orphan file(s) "
        f"{'handled' if args.apply else 'found'}")
    for path in report["written"]:
        log(f"[cleanup] wrote {path}")
    return report


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help="playlists directory (reports go to <out>/checks)")
    ap.add_argument("--epg-dir", default=str(DEFAULT_EPG_DIR),
                    help="directory holding the published guide files")
    ap.add_argument("--name", default="PremiumTV",
                    help="stem of the merged guide, used for the currency check")
    ap.add_argument("--apply", action="store_true",
                    help="write the trims and remove the orphans (default: report only)")
    ap.add_argument("--keep-runs", type=int, default=DEFAULT_KEEP_RUNS,
                    help="how many run blocks to keep in each append-only log")
    ap.add_argument("--max-log-kb", type=int, default=DEFAULT_MAX_LOG_KB,
                    help="report a log that is still bigger than this after trimming")
    ap.add_argument("--max-log-lines", type=int, default=DEFAULT_MAX_LOG_LINES,
                    help="drop oldest kept run blocks until the log is under this many "
                         "lines (the newest block is always kept, however big it is)")
    ap.add_argument("--quarantine-days", type=float, default=7.0,
                    help="drop quarantine entries older than this (same as the deep check)")
    ap.add_argument("--ahead-hours", type=float, default=48.0,
                    help="how far ahead the published guide has to have listings")
    ap.add_argument("--window-hours", type=float, default=48.0,
                    help="how far back a guide's own window reaches, for its age check")
    ap.add_argument("--no-orphans", dest="orphans", action="store_false", default=True,
                    help="do not look for orphaned guide files")
    ap.add_argument("--no-stray", dest="stray", action="store_false", default=True,
                    help="do not remove swap files and __pycache__ directories")
    ap.add_argument("--no-stale-reports", dest="stale_reports", action="store_false",
                    default=True, help="skip the artifact-currency check")
    ap.add_argument("--dry-run-edit-log", action="store_true",
                    help="do not append to logs/cleanup-edits.txt")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 when a problem is reported")
    ap.add_argument("--label", default="repository cleanup", help="run label for reports")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    report = run(args)
    if args.strict and report["problems"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
