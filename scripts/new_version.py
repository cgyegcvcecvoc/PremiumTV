#!/usr/bin/env python3
"""Start the next PremiumTV version from one command.

The user's trigger is simply **"new version"**. This script turns that into the
mechanical part of a release:

  * bump ``VERSION`` by one patch (1.1.7 -> 1.1.8, the naming rule);
  * write a short ``release-notes-<version>.md`` from a one-line name and at
    most five one-line notes - long release essays are against the rule;
  * refresh the generated Android/macOS version surfaces;
  * update the two app README build targets.

It does **not** publish. Publishing is the deliberate GitHub Actions step
documented in docs/RELEASING.md, which creates the tag and release the in-app
updater polls, and starts the APK/DMG builds.

Usage:
    python scripts/new_version.py --name "Local channels" \\
        --note "Local stations from a ZIP, state or country." \\
        --note "A&E channels share one category."

    python scripts/new_version.py --check-notes 1.1.7

The release name printed by ``--next`` and accepted by ``--name`` is
``PremiumTV <version> — <feature name>``: the number is always the next patch,
and the feature name is the one-to-five-word theme of the change
(docs/RELEASING.md). ``--feature`` supplies the standard name and notes for a
themed release so no agent has to invent either.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import release_version  # noqa: E402

MAX_NOTES = 5
MAX_NOTE_CHARS = 110
MAX_NAME_CHARS = 48
VERSION_FILE = ROOT / "VERSION"

# Release names the tooling can supply by itself, so an agent never has to
# invent a feature name for a release it was not told a name for. The order is
# the order docs/RELEASING.md lists the themes in; `--next` prints them.
KNOWN_RELEASE_NAMES = {
    "local-channels": "Local channels by location",
    "a-and-e": "A&E Networks in one category",
    "version-scheme": "Named releases",
}

# Standard one-line notes for the features whose wording must not drift.
STANDARD_NOTES = {
    "local-channels": (
        "Local stations from a location, ZIP code, state or city.",
        "Decline location and a ZIP or state still finds your market.",
    ),
    "a-and-e": (
        "Every A&E Networks channel, History and Lifetime included, in one category.",
    ),
    "version-scheme": (
        "One phrase, \"new version\", now means bump, notes, publish and verify.",
    ),
}


def next_version(current: str) -> str:
    parts = release_version.parse_version(current)
    if parts is None or len(parts) != 3:
        raise ValueError(f"VERSION must be MAJOR.MINOR.PATCH, got {current!r}")
    major, minor, patch = parts
    return f"{major}.{minor}.{patch + 1}"


def release_title(version: str, name: str) -> str:
    """`PremiumTV <version> — <feature name>`, the one title everywhere."""
    return f"PremiumTV {version} — {name}"


def release_notes(version: str, name: str, notes: list[str]) -> str:
    code = release_version.android_version_code(version)
    lines = [
        f"# {release_title(version, name)}",
        "",
        f"Android `{version}` / versionCode `{code}` · macOS `{version}`.",
        "",
    ]
    lines += [f"- {note.strip()}" for note in notes if note.strip()]
    lines.append("")
    return "\n".join(lines)


def check_notes(path: Path) -> list[str]:
    """The concise-notes rule, checked so it cannot drift into an essay."""
    problems: list[str] = []
    if not path.is_file():
        return [f"{path.name}: missing"]
    bullets = [
        line[2:].strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ")
    ]
    if not bullets:
        problems.append(f"{path.name}: needs at least one '- ' note")
    if len(bullets) > MAX_NOTES:
        problems.append(
            f"{path.name}: {len(bullets)} notes, the rule allows {MAX_NOTES}; "
            "combine them or leave the detail for the changelog"
        )
    for bullet in bullets:
        if len(bullet) > MAX_NOTE_CHARS:
            problems.append(
                f"{path.name}: note is {len(bullet)} characters, keep it under "
                f"{MAX_NOTE_CHARS}: {bullet[:60]}…"
            )
    return problems


def notes_report() -> int:
    """Every release-notes file, and which ones still break the short rule.

    History is not rewritten: releases published before the rule keep their
    prose. This report is how a new release is checked, and how the next agent
    can see what the current wording looks like.
    """
    files = sorted(ROOT.glob("release-notes-*.md"), key=lambda path: path.name)
    long_files: list[str] = []
    for path in files:
        version = path.stem.replace("release-notes-", "")
        problems = check_notes(path)
        if problems:
            long_files.append(path.name)
            for problem in problems:
                print(f"[notes] {problem}", file=sys.stderr)
    print(f"[notes] {len(files)} release-notes files, {len(long_files)} above the rule:")
    for name in long_files:
        print(f"  {name}")
    if long_files:
        print("[notes] Those predate the rule; new releases must pass "
              "`--check-notes <version>`.")
    return 0


def update_readmes(old: str, version: str) -> list[str]:
    """Only the build-target lines; historical release prose stays put."""
    old_code = release_version.android_version_code(old)
    code = release_version.android_version_code(version)
    changed: list[str] = []

    android = ROOT / "android" / "README.md"
    text = android.read_text(encoding="utf-8")
    replacements = [
        (f"default build target is **{old}**", f"default build target is **{version}**"),
        (f"(`versionCode` `{old_code}`)", f"(`versionCode` `{code}`)"),
        (f"# Build target (USA, {old}, versionCode {old_code})",
         f"# Build target (USA, {version}, versionCode {code})"),
        (f"--version {old}", f"--version {version}"),
        (f"-PpremiumTvVersion={old} -PpremiumTvVersionCode={old_code}",
         f"-PpremiumTvVersion={version} -PpremiumTvVersionCode={code}"),
        (f"manual builds default to `{old}`", f"manual builds default to `{version}`"),
        (f"(Android code {old_code})", f"(Android code {code})"),
    ]
    for needle, replacement in replacements:
        if needle in text:
            text = text.replace(needle, replacement)
            changed.append(f"android/README.md: {needle[:40]}")
    android.write_text(text, encoding="utf-8")

    macos = ROOT / "macos" / "README.md"
    text = macos.read_text(encoding="utf-8")
    needle = f"**{old} stable build"
    if needle in text:
        text = text.replace(needle, f"**{version} stable build")
        changed.append("macos/README.md: stable build target")
    macos.write_text(text, encoding="utf-8")
    return changed


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Bump PremiumTV to the next version.")
    parser.add_argument("--name", help='short release name, e.g. "Local channels"')
    parser.add_argument("--note", action="append", default=[],
                        help=f"one release note (max {MAX_NOTES}, {MAX_NOTE_CHARS} chars)")
    parser.add_argument("--check-notes", metavar="VERSION",
                        help="check an existing release-notes file against the short-notes rule")
    parser.add_argument("--feature", choices=sorted(KNOWN_RELEASE_NAMES),
                        help="use a standard release name and its standard notes")
    parser.add_argument("--local-channels", dest="feature", action="store_const",
                        const="local-channels", help="alias for --feature local-channels")
    parser.add_argument("--a-and-e", dest="feature", action="store_const",
                        const="a-and-e", help="alias for --feature a-and-e")
    parser.add_argument("--version-scheme", dest="feature", action="store_const",
                        const="version-scheme", help="alias for --feature version-scheme")
    parser.add_argument("--next", action="store_true",
                        help="print the next version, its release name and the themes")
    parser.add_argument("--notes-report", action="store_true",
                        help="list every release-notes file and whether it still follows the rule")
    args = parser.parse_args(argv)

    if args.check_notes:
        try:
            normalized = release_version.normalize_version(args.check_notes)
        except Exception:  # noqa: BLE001 - normalize returns None, but be explicit
            normalized = None
        if not normalized:
            print(f"error: not a PremiumTV version: {args.check_notes!r}", file=sys.stderr)
            return 1
        problems = check_notes(ROOT / f"release-notes-{normalized}.md")
        for problem in problems:
            print(f"[new-version] {problem}", file=sys.stderr)
        if problems:
            return 1
        print(f"[new-version] release-notes-{normalized}.md follows the short-notes rule")
        return 0

    if args.notes_report:
        return notes_report()

    if args.next:
        current = release_version.current_version()
        upcoming = next_version(current)
        print(f"[new-version] current {current}; next {upcoming} "
              f"(versionCode {release_version.android_version_code(upcoming)})")
        print("[new-version] release name: PremiumTV <version> — <feature name>, where the")
        print("              feature name is the theme of the change (see docs/RELEASING.md).")
        for key, name in KNOWN_RELEASE_NAMES.items():
            notes = STANDARD_NOTES.get(key, ())
            print(f"  --feature {key:14} -> \"{name}\" ({len(notes)} standard note(s))")
        return 0

    if args.feature:
        args.name = args.name or KNOWN_RELEASE_NAMES[args.feature]
        for note in STANDARD_NOTES.get(args.feature, ()):
            if note not in args.note:
                args.note.append(note)

    if not args.name:
        parser.error("--name is required (a short release name, e.g. \"Local channels\")")
    notes = args.note
    if not notes:
        notes = [args.name]
    if len(notes) > MAX_NOTES:
        print(f"error: at most {MAX_NOTES} notes; this release has {len(notes)}", file=sys.stderr)
        return 1
    if len(args.name.strip()) > MAX_NAME_CHARS:
        print(
            f"error: keep the release name under {MAX_NAME_CHARS} characters "
            f"(one to five words): {args.name[:48]}…",
            file=sys.stderr,
        )
        return 1
    for note in notes:
        if len(note) > MAX_NOTE_CHARS:
            print(
                f"error: keep each note under {MAX_NOTE_CHARS} characters: {note[:60]}…",
                file=sys.stderr,
            )
            return 1

    try:
        current = release_version.current_version()
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    version = next_version(current)
    notes_path = ROOT / f"release-notes-{version}.md"
    if notes_path.exists():
        print(f"error: {notes_path.name} already exists; VERSION may already be bumped", file=sys.stderr)
        return 1

    VERSION_FILE.write_text(f"{version}\n", encoding="utf-8")
    notes_path.write_text(release_notes(version, args.name.strip(), notes), encoding="utf-8")
    print(f"[new-version] VERSION {current} -> {version}")
    print(f"[new-version] wrote {notes_path.name}")

    for change in update_readmes(current, version):
        print(f"[new-version] updated {change}")

    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "version_sync.py"), "--write"],
        cwd=ROOT,
        text=True,
    )
    if result.returncode != 0:
        print(
            "[new-version] version_sync still reports drift; fix the named files, "
            "then run `python scripts/version_sync.py`",
            file=sys.stderr,
        )
        return result.returncode

    code = release_version.android_version_code(version)
    print()
    print(f"Next: publish PremiumTV {version} (Android {code}, macOS {version}).")
    print("  1. Add a short CHANGELOG.md entry (a dated heading and a few lines).")
    print("  2. Commit and push this branch to main.")
    print("  3. GitHub -> Actions -> 'Publish a release' -> Run workflow.")
    print("     It publishes VERSION, refuses an existing tag, builds and attaches")
    print("     the APK and both Mac installers, and installed apps see it on their")
    print("     next update check once the release is published.")
    print("  4. After publication, record it (see docs/RELEASING.md step 5).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
