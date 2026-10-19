#!/usr/bin/env python3
"""The one version policy shared by builds, releases and the in-app updaters.

Every PremiumTV release must be numbered above the newest stable release that
came before it.  That is what lets the apps trust a simple rule:

  1. a new version exists only when a *published, non-pre-release* GitHub
     release carries a version numerically above the installed one;
  2. the app downloads that installer once and keeps it until it is installed;
  3. retired previews never become an update target for stable builds.

Versions are written as ``MAJOR.MINOR.PATCH`` or ``MAJOR.MINOR.PATCH.HOTFIX``.
Small fixes to a stable line use the fourth component (``1.0.6.1``): it sorts
above ``1.0.6`` but below every later release, so shipping it never consumes a
minor or patch number the roadmap still needs.

Android also needs a *monotonic* versionCode: Android refuses to install an
older code over a newer one.  Deriving it from the semantic version means a
future release cannot accidentally ship a code below the installed app.  The
scale is ``MAJOR * 100000000 + MINOR * 1000000 + PATCH * 10000 + HOTFIX``:
``1.0.6`` -> ``100060000``, ``1.0.6.1`` -> ``100060001``, ``1.1.0`` ->
``101000000``.  Every code from 1.0.2 on is above the codes the original
previews published (7-11 and ``100010001``), so 1.0.6.1 installs straight over
an installed 1.1.1 preview.

A four-part version cannot be read by the updater in 1.0.4-1.0.6, which only
accepts three numeric parts.  Such a release is therefore paired with a
*compatibility alias*: a second, identical build published one patch above it
(``1.0.7`` for ``1.0.6.1``) whose only job is to be visible to those updaters.
The alias never replaces the canonical version on the download page, and an app
already running the canonical build ignores it instead of downloading the same
code again.

Usage::

    python3 scripts/release_version.py --code 1.0.6.1
    python3 scripts/release_version.py --normalize v1.0.6.1
    python3 scripts/release_version.py --canonical 1.0.7
    python3 scripts/release_version.py --compare 1.0.6.1 1.0.6
    python3 scripts/release_version.py --guard --tag v1.0.6.1 --releases releases.json

``--guard`` exits 0 when the release is above every earlier stable release,
2 when it is not (the release guard then marks it as a pre-release), and 1 for
a malformed tag or an unreadable release list.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Iterable

VERSION_RE = re.compile(
    r"^v?(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?(?:[-+][0-9A-Za-z][0-9A-Za-z.-]*)?$"
)

# A versionCode is an Android int (max 2,147,483,647).  Major by 100,000,000,
# minor by 1,000,000, patch by 10,000 and hotfix by 1: 21.0.0 still fits, and
# every sane version sorts strictly by semantic version.
MAJOR_SCALE = 100_000_000
MINOR_SCALE = 1_000_000
PATCH_SCALE = 10_000
ANDROID_CODE_MAX = 2_147_483_647

# Releases that exist only so an updater which cannot read a four-part version
# can still reach the canonical build.  They carry the same application code.
COMPATIBILITY_ALIASES = {
    "1.0.7": "1.0.6.1",
}


def parse_version(value: str) -> tuple[int, ...] | None:
    """Return the numeric parts of ``v1.2.3`` / ``1.2.3.1-beta``.

    Three-part versions return three values, four-part versions four.  Compare
    them with :func:`compare_versions`, never with ``<`` directly: Python
    compares ``(1, 0, 6)`` and ``(1, 0, 6, 0)`` as different tuples even though
    they describe the same release.
    """
    match = VERSION_RE.fullmatch(str(value or "").strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups() if part is not None)


def _pad(parts: tuple[int, ...]) -> tuple[int, int, int, int]:
    return tuple(parts) + (0,) * (4 - len(parts))  # type: ignore[return-value]


def normalize_version(value: str) -> str | None:
    parts = parse_version(value)
    if parts is None:
        return None
    return ".".join(str(part) for part in parts)


def tag_for(version: str) -> str | None:
    normalized = normalize_version(version)
    return f"v{normalized}" if normalized else None


def canonical_version(value: str) -> str | None:
    """The version a compatibility alias stands for, or the version itself."""
    normalized = normalize_version(value)
    if normalized is None:
        return None
    return COMPATIBILITY_ALIASES.get(normalized, normalized)


def macos_version(value: str) -> str | None:
    """The version the macOS build can carry.

    electron-builder and macOS packaging require a three-part version, so a
    four-part hotfix is built as its compatibility alias (1.0.6.1 -> 1.0.7) and
    the alias release carries the Mac installers.  Every three-part version is
    returned unchanged.
    """
    normalized = normalize_version(value)
    if normalized is None:
        return None
    if len(parse_version(normalized)) <= 3:
        return normalized
    for alias, canonical in COMPATIBILITY_ALIASES.items():
        if canonical == normalized:
            return alias
    return None


def is_compatibility_alias(candidate: str, current: str) -> bool:
    """True when [candidate] is the alias of the build [current] runs.

    Two names, one build: offering the alias to a machine already running the
    canonical version would be a pointless full-size download.
    """
    canonical = canonical_version(candidate)
    return canonical is not None and canonical == canonical_version(current)


def compare_versions(candidate: str, current: str) -> int | None:
    """Return 1 when candidate is newer, -1 when older, 0 when equal.

    ``None`` means at least one value is not a version this project writes.
    """
    left = parse_version(candidate)
    right = parse_version(current)
    if left is None or right is None:
        return None
    left_padded = _pad(left)
    right_padded = _pad(right)
    if left_padded == right_padded:
        return 0
    return 1 if left_padded > right_padded else -1


def is_newer(candidate: str, current: str) -> bool:
    return compare_versions(candidate, current) == 1


def android_version_code(version: str) -> int:
    """Derive a monotonic, installable Android versionCode from a version."""
    parts = parse_version(version)
    if parts is None:
        raise ValueError(f"not a PremiumTV version: {version!r}")
    major, minor, patch, hotfix = _pad(parts)
    if minor > 99 or patch > 99 or hotfix > 9999:
        raise ValueError(
            f"version {version} does not fit the Android versionCode scale "
            "(minor/patch <= 99, hotfix <= 9999)"
        )
    code = (
        major * MAJOR_SCALE
        + minor * MINOR_SCALE
        + patch * PATCH_SCALE
        + hotfix
    )
    if code > ANDROID_CODE_MAX:
        raise ValueError(f"version {version} exceeds Android's versionCode limit")
    return code


def _release_tag(release: dict) -> str:
    # The GitHub REST API uses tag_name, the compact file uses tag, and
    # `gh release list --json tagName,isPrerelease,isDraft` uses camelCase.
    return str(
        release.get("tag")
        or release.get("tag_name")
        or release.get("tagName")
        or ""
    )


def _is_stable(release: dict) -> bool:
    # Accept both the REST API (draft/prerelease) and `gh release list --json`
    # (isDraft/isPrerelease) shapes.
    draft = release.get("draft", release.get("isDraft"))
    prerelease = release.get("prerelease", release.get("isPrerelease"))
    return not draft and not prerelease


def stable_versions(releases: Iterable[dict]) -> list[str]:
    versions = []
    for release in releases:
        if not isinstance(release, dict) or not _is_stable(release):
            continue
        version = normalize_version(_release_tag(release))
        if version:
            versions.append(version)
    return versions


def newest_stable(releases: Iterable[dict], exclude: str | None = None,
                  ignore_aliases: bool = False) -> str | None:
    """The newest stable version in [releases].

    [ignore_aliases] leaves out compatibility aliases (1.0.7 for 1.0.6.1).
    A canonical release must be compared with real stable releases only: its
    alias is usually published afterwards, and it is the same build.
    """
    wanted = normalize_version(exclude or "")
    versions = [
        version for version in stable_versions(releases)
        if version != wanted and not (ignore_aliases and version in COMPATIBILITY_ALIASES)
    ]
    return max(versions, key=lambda value: _pad(parse_version(value) or (0, 0, 0, 0))) if versions else None


def load_releases(path: str) -> list[dict]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, list):
        raise ValueError("the release list must be a JSON array")
    return data


def guard(tag: str, releases: list[dict]) -> tuple[int, str]:
    """Check that a stable release is above every earlier stable release."""
    version = normalize_version(tag)
    if version is None:
        return 1, f"{tag!r} is not a version tag (expected vMAJOR.MINOR.PATCH[.HOTFIX])"
    # A compatibility alias is published after the canonical release it
    # mirrors (v1.0.7 after v1.0.6.1), so it must not make that canonical
    # release look older than the current stable and demote it to a preview.
    previous = newest_stable(
        releases, exclude=version, ignore_aliases=version not in COMPATIBILITY_ALIASES)
    if previous is None:
        return 0, f"v{version} is the first stable release; nothing earlier to compare."
    if is_newer(version, previous):
        return 0, f"v{version} is above the previous stable v{previous}."
    return (
        2,
        f"v{version} is not above the newest stable v{previous}. "
        "PremiumTV releases must always move above the current stable so the "
        "in-app updater can offer them without downgrades or repeated downloads.",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--code", metavar="VERSION", help="print the Android versionCode")
    parser.add_argument("--normalize", metavar="VERSION", help="print MAJOR.MINOR.PATCH[.HOTFIX]")
    parser.add_argument("--canonical", metavar="VERSION",
                        help="print the canonical version behind a compatibility alias")
    parser.add_argument("--macos", metavar="VERSION",
                        help="print the three-part version the Mac build carries")
    parser.add_argument("--compare", nargs=2, metavar=("CANDIDATE", "CURRENT"),
                        help="exit 0 when candidate is newer, 1 otherwise")
    parser.add_argument("--tag", help="release tag to guard (with --guard)")
    parser.add_argument("--releases", help="JSON release list (with --guard)")
    parser.add_argument("--guard", action="store_true", help="enforce the release-order policy")
    args = parser.parse_args(argv)

    if args.code:
        try:
            print(android_version_code(args.code))
        except ValueError as error:
            print(f"error: {error}", file=sys.stderr)
            return 1
        return 0

    if args.normalize:
        normalized = normalize_version(args.normalize)
        if normalized is None:
            print(f"error: not a PremiumTV version: {args.normalize!r}", file=sys.stderr)
            return 1
        print(normalized)
        return 0

    if args.canonical:
        canonical = canonical_version(args.canonical)
        if canonical is None:
            print(f"error: not a PremiumTV version: {args.canonical!r}", file=sys.stderr)
            return 1
        print(canonical)
        return 0

    if args.macos:
        version = macos_version(args.macos)
        if version is None:
            print(f"error: {args.macos!r} has no three-part macOS build version", file=sys.stderr)
            return 1
        print(version)
        return 0

    if args.compare:
        result = compare_versions(args.compare[0], args.compare[1])
        if result is None:
            print("error: both values must be PremiumTV versions", file=sys.stderr)
            return 1
        if result == 0:
            print(f"{args.compare[0]} == {args.compare[1]}")
            return 1
        newer = result > 0
        print(f"{args.compare[0]} is {'newer' if newer else 'older'} than {args.compare[1]}")
        return 0 if newer else 1

    if args.guard:
        if not args.tag or not args.releases:
            print("error: --guard needs --tag and --releases", file=sys.stderr)
            return 1
        try:
            releases = load_releases(args.releases)
        except (OSError, ValueError) as error:
            print(f"error: could not read the release list: {error}", file=sys.stderr)
            return 1
        status, message = guard(args.tag, releases)
        print(message)
        return status

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
