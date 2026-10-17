#!/usr/bin/env python3
"""Audit the published channel library and its backup feeds, offline.

The regular ``verify_playlists.py`` run proves that every playlist is in the
published order and advertises a valid guide. This smaller audit answers the
questions that are specific to the "one channel, many feeds" design:

* is every ``(Backup N)`` name unique, so two different streams never share a
  name in a player's channel list?
* does every backup feed have its primary channel in the same category?
* are backup numbers continuous for a channel?
* does each ``playlists/categories/*.m3u`` file still match its group in
  ``PremiumTV.m3u`` entry for entry (same URLs, same order)?
* what quality labels, guide ids and logos does the library actually carry?

    python scripts/audit_backups.py                 # write checks/BACKUP-AUDIT.md
    python scripts/audit_backups.py --strict        # exit 1 when something is wrong
    python scripts/audit_backups.py --playlist -    # audit another file (report to stdout)

The script never touches the network and never changes a playlist.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_check  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLAYLIST = ROOT / "playlists" / "PremiumTV.m3u"
DEFAULT_CATEGORIES = ROOT / "playlists" / "categories"
DEFAULT_REPORT = ROOT / "playlists" / "checks" / "BACKUP-AUDIT.md"
BACKUP_RE = re.compile(r"^(.*?)\s*\(Backup (\d+)\)\s*$")
GUIDE_RE = re.compile(r'x-tvg-url="([^"]*)"')
QUALITY_RE = re.compile(r"\((\d{3,4}p|4K|UHD|SD|HD)\)\s*(?:\[[^\]]*\])?\s*$", re.IGNORECASE)


def attr(attrs: str, key: str) -> str:
    match = re.search(rf'{re.escape(key)}="([^"]*)"', attrs)
    return match.group(1) if match else ""


def read_playlist(path: Path) -> tuple[str, list[dict]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    header, blocks = link_check.split_blocks(text)
    entries: list[dict] = []
    for block in blocks:
        line = block.lines[0]
        split = line.rfind('",')
        if split != -1:
            attrs, name = line[: split + 1], line[split + 2:]
        else:
            head, _, name = line.partition(",")
            attrs = head
        entries.append({
            "name": name.strip(),
            "group": attr(attrs, "group-title"),
            "id": attr(attrs, "tvg-id"),
            "logo": attr(attrs, "tvg-logo"),
            "url": block.url,
        })
    return "\n".join(header), entries


def clean_name(name: str) -> str:
    text = (name or "").strip()
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\s*\[[^\]]*\]\s*$", "", text)
        text = QUALITY_RE.sub("", text)
        text = re.sub(r"\s*\(\s*(?:Backup \d+|Alt|Alternate|Mirror|Feed \d+)\s*\)\s*$",
                      "", text, flags=re.IGNORECASE)
        text = text.strip()
    return text or (name or "").strip()


def quality_label(name: str) -> str:
    match = QUALITY_RE.search(name)
    return match.group(1).lower() if match else "unlabelled"


def audit(playlist: Path, categories_dir: Path) -> dict:
    header, entries = read_playlist(playlist)
    primary = [entry for entry in entries if not BACKUP_RE.match(entry["name"])]
    backups = [entry for entry in entries if BACKUP_RE.match(entry["name"])]

    problems: list[str] = []
    warnings: list[str] = []

    duplicate_urls = [url for url, count in collections.Counter(
        entry["url"] for entry in entries).items() if count > 1]
    if duplicate_urls:
        problems.append(f"{len(duplicate_urls)} stream URL(s) appear more than once")

    backup_names: dict[str, list[str]] = collections.defaultdict(list)
    for entry in backups:
        backup_names[entry["name"].casefold()].append(entry["name"])
    duplicate_backup_names = sorted(names[0] for names in backup_names.values()
                                    if len(names) > 1)
    if duplicate_backup_names:
        problems.append(f"{len(duplicate_backup_names)} backup name(s) are not unique")

    primary_ids = {entry["id"] for entry in primary if entry["id"]}
    primary_names = {clean_name(entry["name"]).lower() for entry in primary}
    orphans: list[str] = []
    for entry in backups:
        match = BACKUP_RE.match(entry["name"])
        base = clean_name(match.group(1)) if match else clean_name(entry["name"])
        if entry["id"] and entry["id"] in primary_ids:
            continue
        if base.lower() in primary_names:
            continue
        orphans.append(entry["name"])
    if orphans:
        problems.append(f"{len(orphans)} backup feed(s) have no primary channel")

    backup_numbers: dict[str, list[int]] = collections.defaultdict(list)
    for entry in backups:
        match = BACKUP_RE.match(entry["name"])
        if match:
            backup_numbers[clean_name(match.group(1)).casefold()].append(int(match.group(2)))
    gaps = {name: sorted(numbers) for name, numbers in backup_numbers.items()
            if sorted(numbers) != list(range(1, len(numbers) + 1))}
    if gaps:
        problems.append(f"{len(gaps)} channel(s) have non-continuous backup numbers")

    guide_count = len([url for url in (GUIDE_RE.search(header) or [None, ""])[1].split(",")
                       if url.strip()]) if GUIDE_RE.search(header) else 0
    if guide_count > 3:
        problems.append(f"the header advertises {guide_count} guides (maximum is 3)")

    missing_ids = [entry["name"] for entry in primary if not entry["id"]]
    if missing_ids:
        problems.append(f"{len(missing_ids)} channel(s) have no tvg-id")
    missing_logos = sum(1 for entry in primary if not entry["logo"])
    if missing_logos:
        warnings.append(f"{missing_logos} channel(s) have no logo")

    qualities = collections.Counter(quality_label(entry["name"]) for entry in primary)

    # Per-group view of PremiumTV.m3u and of each published category file.
    group_primary: dict[str, list[dict]] = collections.defaultdict(list)
    group_backups: dict[str, list[dict]] = collections.defaultdict(list)
    for entry in primary:
        group_primary[entry["group"] or "Other"].append(entry)
    for entry in backups:
        group = entry["group"] or ""
        group_backups[group[:-len(" Backups")] if group.endswith(" Backups") else group].append(entry)

    files: list[dict] = []
    for path in sorted(categories_dir.glob("*.m3u")):
        _, file_entries = read_playlist(path)
        urls = [entry["url"] for entry in file_entries]
        groups = {entry["group"] for entry in file_entries}
        group = next(iter(groups), path.stem.replace("_", " "))
        if group.endswith(" Backups"):
            expected = [entry["url"] for entry in
                        group_backups.get(group[: -len(" Backups")], [])]
        else:
            expected = [entry["url"] for entry in group_primary.get(group, [])]
        if not expected:
            expected = [entry["url"] for entry in group_primary.get(path.stem.replace("_", " "), [])]
        file_duplicates = [url for url, count in collections.Counter(urls).items() if count > 1]
        same_order = urls == expected
        if not same_order:
            problems.append(f"{path.name} does not match the published playlist order")
        if file_duplicates:
            problems.append(f"{path.name} contains {len(file_duplicates)} duplicate URL(s)")
        backup_names_in_file = [entry["name"] for entry in file_entries
                                if BACKUP_RE.match(entry["name"])]
        files.append({
            "name": path.name,
            "group": group,
            "channels": sum(1 for entry in file_entries if not BACKUP_RE.match(entry["name"])),
            "backups": len(backup_names_in_file),
            "same_order": same_order,
            "duplicate_urls": len(file_duplicates),
            "unique_backup_names": len(backup_names_in_file) == len(set(backup_names_in_file)),
        })

    expected_files = {
        f"{re.sub(r'[^A-Za-z0-9]+', '_', group).strip('_')}.m3u"
        for group, members in group_primary.items() if len(members) >= 3
    } | {
        f"{re.sub(r'[^A-Za-z0-9]+', '_', group + ' Backups').strip('_')}.m3u"
        for group, members in group_backups.items() if len(members) >= 3
    }
    missing_files = sorted(expected_files - {row["name"] for row in files})
    if missing_files:
        problems.append(f"{len(missing_files)} category group(s) have no playlist file")

    return {
        "generated_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "playlist": str(playlist.relative_to(ROOT)) if playlist.is_relative_to(ROOT) else str(playlist),
        "entries": len(entries),
        "unique_channels": len(primary),
        "backup_feeds": len(backups),
        "channels_with_backups": len({clean_name(BACKUP_RE.match(e["name"]).group(1))
                                      for e in backups}),
        "guide_count": guide_count,
        "missing_ids": len(missing_ids),
        "missing_logos": missing_logos,
        "orphans": orphans,
        "duplicate_backup_names": duplicate_backup_names,
        "duplicate_urls": len(duplicate_urls),
        "backup_number_gaps": gaps,
        "qualities": dict(qualities.most_common()),
        "files": files,
        "problems": problems,
        "warnings": warnings,
    }


def render(report: dict) -> str:
    lines = [
        "# Backup and channel integrity audit",
        "",
        f"- **Generated:** {report['generated_utc']}",
        f"- **Playlist:** `{report['playlist']}`",
        f"- **Entries:** {report['entries']:,} — **{report['unique_channels']:,} unique channels**, "
        f"**{report['backup_feeds']:,} backup feeds**",
        f"- **Channels with at least one backup:** {report['channels_with_backups']:,}",
        f"- **Duplicate stream URLs:** {report['duplicate_urls']}",
        f"- **Duplicate backup names:** {len(report['duplicate_backup_names'])}",
        f"- **Backup feeds without a primary channel:** {len(report['orphans'])}",
        f"- **Missing `tvg-id`:** {report['missing_ids']} — **missing logo:** {report['missing_logos']}",
        f"- **Guides in the main header:** {report['guide_count']} (own guide + fallbacks)",
        f"- **Category files checked:** {len(report['files'])}",
        "",
        "## Quality labels in `PremiumTV.m3u`",
        "",
        "| Label | Channels |",
        "|---|---:|",
    ]
    for label, count in report["qualities"].items():
        lines.append(f"| {label} | {count:,} |")
    lines += [
        "",
        "## Category files",
        "",
        "| File | Group | Channels | Backups | Same order as main | Duplicate URLs | Unique backup names |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for row in report["files"]:
        lines.append(
            f"| `{row['name']}` | {row['group']} | {row['channels']:,} | {row['backups']:,} | "
            f"{'yes' if row['same_order'] else 'NO'} | {row['duplicate_urls']} | "
            f"{'yes' if row['unique_backup_names'] else 'NO'} |"
        )
    lines += ["", "## Problems", ""]
    if report["problems"]:
        lines += [f"- {problem}" for problem in report["problems"]]
    else:
        lines.append("None: every backup name is unique, every backup has its primary channel, "
                     "backup numbers are continuous, and every category file matches the "
                     "published playlist entry for entry.")
    if report["warnings"]:
        lines += ["", "## Notes", ""]
        lines += [f"- {warning}" for warning in report["warnings"]]
    lines.append("")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--playlist", default=str(DEFAULT_PLAYLIST))
    parser.add_argument("--categories-dir", default=str(DEFAULT_CATEGORIES))
    parser.add_argument("--out", default=str(DEFAULT_REPORT))
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when a backup or channel problem is found")
    args = parser.parse_args(argv)

    report = audit(Path(args.playlist), Path(args.categories_dir))
    text = render(report)
    if args.out == "-":
        print(text)
    else:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"[audit] wrote {out}")
    print(f"[audit] {report['unique_channels']:,} channels + {report['backup_feeds']:,} backups, "
          f"{len(report['problems'])} problem(s)")
    return 1 if args.strict and report["problems"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
