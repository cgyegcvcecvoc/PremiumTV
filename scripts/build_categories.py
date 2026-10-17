#!/usr/bin/env python3
"""Build the user-facing category shelf in ``categories/``.

``playlists/categories/`` mirrors the published playlist group by group and is
the machine-facing split; this tool writes the shelf a player is pointed at:

* ``categories/USA.m3u`` - every working US channel, grouped by category and in
  the published order, so the headline file for this repository is one URL;
* ``categories/USA/<Category>.m3u`` - the same list cut per category, so
  "just the US sports channels" is one URL too;
* ``categories/<Category>.m3u`` - the whole library, one category per file.

Every file is a *slice of an already published playlist*: the channels, their
order, their group labels and the guide header are copied verbatim from

    playlists/countries/USA.m3u   ->  categories/USA.m3u, categories/USA/*.m3u
    playlists/PremiumTV.m3u       ->  categories/<Category>.m3u

No network, no re-classification: the sorting is the published sorting
(``scripts/categorize.py``: curated categories in order, each followed by its
own Backups group, the long tail by size, ``Other`` last, channel name inside a
group with a channel's feeds side by side), so the shelf can never disagree with
the playlist it came from. ``scripts/verify_playlists.py --require-shelf``
re-plans the shelf from the published playlists and fails when a committed file
differs, which is what keeps it honest after a scrape or a deep check.

    python scripts/build_categories.py                     # refresh the shelf
    python scripts/build_categories.py --dry-run           # report only
    python scripts/build_categories.py --min-size 5        # bigger groups only
    python scripts/build_categories.py --shelf-dir /tmp/c  # somewhere else

Outputs:

    categories/USA.m3u            every US channel, category order
    categories/USA/*.m3u          per-category slices of the USA list
    categories/*.m3u              per-category slices of the whole library
    categories/README.md          the index a reader lands on
    categories/index.json         the same index, machine-readable
"""
from __future__ import annotations

import argparse
import collections
import dataclasses
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import categorize  # noqa: E402  (the one ordering rule the shelf must preserve)
import legacy_sunset  # noqa: E402  (which USA feed is still being updated)
import rebuild_playlists  # noqa: E402  (playlist reading/writing helpers)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SHELF = "categories"
DEFAULT_MAIN = "playlists/PremiumTV.m3u"
# Fallback only: the USA shelf is cut from the live feed that
# scripts/legacy_sunset.py publishes, resolved by legacy_sunset.live_usa_path().
# Resolving it there is what lets the shelf follow the live channels on the day
# playlists/countries/USA.m3u is pinned for end-of-support builds.
DEFAULT_USA = "playlists/countries/USA.m3u"
REPO_SLUG = "cgyegcvcecvoc/PremiumTV1"
USA_SCOPE = "USA"
WORLD_SCOPE = "World"
# Groups with a channel or two stay in the parent file; a one-link playlist is
# noise in a directory listing (the same rule playlists/categories/ uses).
MIN_SHELF_SIZE = 3


def log(msg: str) -> None:
    print(msg, flush=True)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def committed_files(shelf_dir: Path) -> set[Path]:
    """Every .m3u currently in the shelf directory."""
    if not shelf_dir.is_dir():
        return set()
    return {path for path in shelf_dir.rglob("*.m3u") if path.is_file()}


def prune_shelf(shelf_dir: Path, keep: set[Path], dry_run: bool = False) -> list[str]:
    """Delete shelf files a previous build wrote and this one no longer plans."""
    removed: list[str] = []
    for path in sorted(committed_files(shelf_dir) - keep):
        removed.append(relative(path))
        if not dry_run:
            try:
                path.unlink()
            except OSError:  # noqa: BLE001 - a file we cannot remove is reported, not fatal
                pass
    return removed


def source_link(path: Path) -> str:
    """Markdown link to a playlist, keeping paths outside the repo unlinked."""
    rel = relative(path)
    if Path(rel).is_absolute():
        return f"`{rel}`"
    return f"[`{rel}`](../{rel})"


def stamp() -> tuple[str, str]:
    now = dt.datetime.now(dt.timezone.utc)
    utc = now.strftime("%Y-%m-%d %H:%M UTC")
    try:
        from zoneinfo import ZoneInfo
        local = now.astimezone(ZoneInfo("America/New_York")).strftime("%Y-%m-%d %I:%M %p %Z")
    except Exception:  # noqa: BLE001 - the UTC stamp is enough when tzdata is missing
        local = utc
    return utc, local


# --------------------------------------------------------------------------- #
# Planning
# --------------------------------------------------------------------------- #
@dataclasses.dataclass
class ShelfFile:
    """One playlist in the shelf, fully planned before anything is written."""

    path: Path
    scope: str
    category: str
    channels: list
    header: str = "#EXTM3U"
    source: str = ""

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def title(self) -> str:
        if self.scope == USA_SCOPE and self.category == USA_SCOPE:
            return f"USA working channels ({len(self.channels)})"
        return f"{self.scope} - {self.category} ({len(self.channels)} channels)"

    def entry_lines(self) -> list[str]:
        lines: list[str] = []
        for channel in self.channels:
            lines.extend(channel.to_m3u().splitlines())
        return lines


def channel_lines(channels: list) -> list[str]:
    lines: list[str] = []
    for channel in channels:
        lines.extend(channel.to_m3u().splitlines())
    return lines


def slice_by_category(channels: list, min_size: int) -> list[tuple[str, list]]:
    """(category, channels) pairs in the published group order."""
    counts = categorize.category_counts(channels)
    order = categorize.order_categories(counts)
    by_group: dict[str, list] = collections.defaultdict(list)
    for channel in channels:
        by_group[channel.attrs.get("group-title", categorize.OTHER)].append(channel)
    return [(category, by_group[category]) for category in order
            if len(by_group.get(category, ())) >= max(1, min_size)]


def plan_shelf(main_path: Path, usa_path: Path, shelf_dir: Path,
               min_size: int = MIN_SHELF_SIZE, include_world: bool = True) -> list[ShelfFile]:
    """Everything the shelf should contain, in the order it should be listed."""
    files: list[ShelfFile] = []

    if usa_path.is_file():
        usa_channels, _, header = rebuild_playlists.read_playlist(usa_path)
        if usa_channels:
            files.append(ShelfFile(path=shelf_dir / "USA.m3u", scope=USA_SCOPE,
                                   category=USA_SCOPE, channels=usa_channels,
                                   header=header, source=relative(usa_path)))
            for category, members in slice_by_category(usa_channels, min_size):
                files.append(ShelfFile(
                    path=shelf_dir / "USA" / f"{rebuild_playlists.slugify(category)}.m3u",
                    scope=USA_SCOPE, category=category, channels=members,
                    header=header, source=relative(usa_path)))

    if include_world and main_path.is_file():
        world_channels, _, header = rebuild_playlists.read_playlist(main_path)
        if world_channels:
            for category, members in slice_by_category(world_channels, min_size):
                files.append(ShelfFile(
                    path=shelf_dir / "All" / f"{rebuild_playlists.slugify(category)}.m3u",
                    scope=WORLD_SCOPE, category=category, channels=members,
                    header=header, source=relative(main_path)))
    return files


# --------------------------------------------------------------------------- #
# Writing
# --------------------------------------------------------------------------- #
def compose(header: str, title: str, channels: list) -> str:
    lines = [header or "#EXTM3U", f"# {title}"]
    lines.extend(channel_lines(channels))
    return "\n".join(lines) + "\n"


def is_unchanged(text: str, header: str, entries: list[str]) -> bool:
    """True when the committed file already holds exactly these entries."""
    existing = text.splitlines()
    if not existing or existing[0].strip() != (header or "#EXTM3U").strip():
        return False
    body = existing[1:]
    # Drop the generated title comment, keeping the #EXTVLCOPT lines that belong
    # to the entries themselves.
    if body and body[0].startswith("# ") and not body[0].startswith("#EXT"):
        body = body[1:]
    return body == entries


def write_shelf(files: list[ShelfFile], label: str = "category shelf",
                dry_run: bool = False) -> list[dict]:
    """Write every planned file, leaving unchanged ones (and their mtime) alone."""
    utc_s, local_s = stamp()
    summary: list[dict] = []
    for item in files:
        title = f"{item.title} - rebuilt {utc_s} ({local_s}) - {label}"
        entries = item.entry_lines()
        existing = ""
        if item.path.is_file():
            existing = item.path.read_text(encoding="utf-8", errors="replace")
        unchanged = bool(existing) and is_unchanged(existing, item.header, entries)
        if not dry_run and not unchanged:
            item.path.parent.mkdir(parents=True, exist_ok=True)
            item.path.write_text(compose(item.header, title, item.channels), encoding="utf-8")
        summary.append({
            "file": relative(item.path),
            "scope": item.scope,
            "category": item.category,
            "channels": len(item.channels),
            "source": item.source,
            "written": not dry_run and not unchanged,
            "unchanged": unchanged,
        })
    return summary


def scope_totals(summary: list[dict]) -> dict[str, int]:
    totals: collections.Counter = collections.Counter()
    for row in summary:
        if row["category"] == row["scope"]:
            continue  # the parent file (USA.m3u) repeats its own category files
        totals[row["scope"]] += row["channels"]
    return dict(totals)


def shelf_readme(summary: list[dict], main_path: Path, usa_path: Path,
                 utc_s: str, local_s: str, label: str, min_size: int = MIN_SHELF_SIZE) -> str:
    usa_rows = [row for row in summary if row["scope"] == USA_SCOPE and row["category"] != USA_SCOPE]
    world_rows = [row for row in summary if row["scope"] == WORLD_SCOPE]
    usa_total = next((row["channels"] for row in summary
                      if row["scope"] == USA_SCOPE and row["category"] == USA_SCOPE), 0)
    raw = f"https://raw.githubusercontent.com/{REPO_SLUG}/main"
    lines = [
        "# Category shelf",
        "",
        f"- **Shelf rebuilt:** {utc_s} ({local_s}) — _{label}_",
        f"- **Sources:** {source_link(main_path)} for `All/`, {source_link(usa_path)} "
        f"for `USA.m3u` and `USA/`",
        f"- **Order:** {' -> '.join(categorize.CURATED_CATEGORIES)} (each followed by its own "
        "Backups group), then the long tail by size, `Other` last — the published order from "
        "`scripts/categorize.py`.",
        "- **One entry per channel:** a channel's spare feeds sit right after it in its "
        "`<category> Backups` group, best quality first.",
        "",
        "Every file here is a slice of an already published playlist: same channels, same "
        "order, same group labels, same guide header. Nothing is re-classified, so loading "
        "the shelf can never show a channel the playlist does not have.",
        "",
        "## USA",
        "",
        f"[`USA.m3u`](USA.m3u) — every one of the **{usa_total}** working US channels in one "
        "file, in category order. The per-category files below are the same list cut up.",
        "",
        "| # | Category | Channels | Playlist |",
        "|---|---|---:|---|",
    ]
    for index, row in enumerate(usa_rows, 1):
        name = Path(row["file"]).name
        lines.append(f"| {index} | {row['category']} | {row['channels']} | "
                     f"[`{name}`](USA/{name}) |")
    if not usa_rows:
        lines.append("| — | _no US channels published yet_ | 0 | — |")
    lines += [
        "",
        f"Groups smaller than {min_size} channels keep no file of their own (they would be a "
        f"one-link playlist) - they stay in `USA.m3u`, which always holds every US channel.",
    ]

    lines += [
        "",
        "## All countries",
        "",
        "One file per category for the whole library (US channels first inside a category, "
        "because that is the published order).",
        "",
        "| # | Category | Channels | Playlist |",
        "|---|---|---:|---|",
    ]
    for index, row in enumerate(world_rows, 1):
        name = Path(row["file"]).name
        lines.append(f"| {index} | {row['category']} | {row['channels']} | "
                     f"[`{name}`](All/{name}) |")
    if not world_rows:
        lines.append("| — | _the main playlist is not published yet_ | 0 | — |")
    lines += [
        "",
        f"Groups smaller than {min_size} channels keep no file of their own; they stay in "
        f"`{relative(main_path)}`.",
    ]

    lines += [
        "",
        "## Load it",
        "",
        "```text",
        f"{raw}/categories/USA.m3u          # every US channel, by category",
        f"{raw}/categories/USA/Sports.m3u   # just the US sports channels",
        f"{raw}/categories/All/Sports.m3u  # every sports channel in the library",
        "```",
        "",
        "## Keeping it in order",
        "",
        "Rebuilt by `scripts/build_categories.py` after every scrape, deep check and quick "
        "update; a file is only rewritten when its channel list actually changed. "
        "`scripts/verify_playlists.py --require-shelf` re-plans the shelf from the published "
        "playlists and fails the run when a committed file is stale, so this directory can "
        "not drift away from the playlists it mirrors.",
        "",
    ]
    return "\n".join(lines)


def shelf_index(summary: list[dict], main_path: Path, usa_path: Path, utc_s: str,
                min_size: int = MIN_SHELF_SIZE) -> dict:
    return {
        "generated_utc": utc_s,
        "min_size": min_size,
        "order": list(categorize.CURATED_CATEGORIES),
        "sources": {
            WORLD_SCOPE: relative(main_path),
            USA_SCOPE: relative(usa_path),
        },
        "totals": scope_totals(summary),
        "files": summary,
    }


def recorded_min_size(shelf_dir: Path) -> int:
    """The group size the committed shelf was built with (from its own index)."""
    path = shelf_dir / "index.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        value = int(data.get("min_size", MIN_SHELF_SIZE))
    except (OSError, ValueError, TypeError):
        return MIN_SHELF_SIZE
    return value if value >= 1 else MIN_SHELF_SIZE


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build(shelf_dir: Path, main_path: Path, usa_path: Path, min_size: int = MIN_SHELF_SIZE,
          label: str = "category shelf", dry_run: bool = False,
          include_world: bool = True) -> dict:
    """Plan and write the whole shelf; returns the machine-readable index."""
    files = plan_shelf(main_path, usa_path, shelf_dir, min_size=min_size,
                       include_world=include_world)
    summary = write_shelf(files, label=label, dry_run=dry_run)
    removed = prune_shelf(shelf_dir, {item.path for item in files}, dry_run=dry_run)
    utc_s, local_s = stamp()
    if not dry_run:
        shelf_dir.mkdir(parents=True, exist_ok=True)
        (shelf_dir / "README.md").write_text(
            shelf_readme(summary, main_path, usa_path, utc_s, local_s, label, min_size),
            encoding="utf-8")
        (shelf_dir / "index.json").write_text(
            json.dumps(shelf_index(summary, main_path, usa_path, utc_s, min_size), indent=2)
            + "\n", encoding="utf-8")
    index = shelf_index(summary, main_path, usa_path, utc_s, min_size)
    index["removed"] = removed
    return index


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--shelf-dir", default=DEFAULT_SHELF, help="where to write the shelf")
    parser.add_argument("--main", default=DEFAULT_MAIN,
                        help="published playlist the All/ files come from")
    parser.add_argument("--usa", default="",
                        help="published USA playlist USA.m3u and USA/ come from "
                             "(default: the live USA feed scripts/legacy_sunset.py publishes)")
    parser.add_argument("--min-size", type=int, default=MIN_SHELF_SIZE,
                        help="smallest group that gets its own file")
    parser.add_argument("--label", default="category shelf",
                        help="run label written into every title line")
    parser.add_argument("--no-world", action="store_true",
                        help="only build the USA shelf")
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    args = parser.parse_args(argv)

    shelf_dir = Path(args.shelf_dir)
    if not shelf_dir.is_absolute():
        shelf_dir = ROOT / shelf_dir
    main_path = Path(args.main)
    if not main_path.is_absolute():
        main_path = ROOT / main_path
    usa_path = legacy_sunset.live_usa_path(ROOT) if not args.usa else Path(args.usa)
    if args.usa and not usa_path.is_absolute():
        usa_path = ROOT / usa_path

    if not main_path.is_file() and not usa_path.is_file():
        log(f"[shelf] no source playlists ({relative(main_path)}, {relative(usa_path)})")
        return 1

    index = build(shelf_dir, main_path, usa_path, min_size=args.min_size,
                  label=args.label, dry_run=args.dry_run, include_world=not args.no_world)
    written = sum(1 for row in index["files"] if row["written"])
    unchanged = sum(1 for row in index["files"] if row["unchanged"])
    totals = index["totals"]
    log(f"[shelf] {'would write' if args.dry_run else 'wrote'} {written} of "
        f"{len(index['files'])} files ({unchanged} unchanged"
        + (f", {len(index['removed'])} removed" if index.get("removed") else "")
        + f") to {relative(shelf_dir)}: USA {totals.get(USA_SCOPE, 0)} channels, all countries "
        f"{totals.get(WORLD_SCOPE, 0)} channels")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
