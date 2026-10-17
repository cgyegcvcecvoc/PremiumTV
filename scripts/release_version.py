#!/usr/bin/env python3
"""The one version policy shared by builds, releases and the in-app updaters.

Every PremiumTV release must be numbered above the newest stable release that
came before it.  That is what lets the apps trust a simple rule:

  1. a new version exists only when a *published, non-pre-release* GitHub
     release carries a version numerically above the installed one;
  2. the app downloads that installer once and keeps it until it is installed;
  3. previews never become an update target for stable builds, and an
     installed preview (for example 1.1.1) is never offered an older stable
     build.

Android also needs a *monotonic* versionCode: Android refuses to install an
older code over a newer one.  Deriving it from the semantic version means a
future release cannot accidentally ship a code below the installed app
(``1.0.4`` -> ``100000004``, ``1.1.1`` -> ``100010001``).

Usage::

    python3 scripts/release_version.py --code 1.0.4
    python3 scripts/release_version.py --normalize v1.0.4
    python3 scripts/release_version.py --compare 1.0.4 1.0.3
    python3 scripts/release_version.py --guard --tag v1.0.4 --releases releases.json

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

VERSION_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z][0-9A-Za-z.-]*)?$")

# A versionCode is an Android int (max 2,147,483,647).  Major is scaled by
# 100,000,000, minor by 10,000 and patch by 1: 21.0.0 still fits, and every
# sane version sorts strictly by semantic version.
MAJOR_SCALE = 100_000_000
MINOR_SCALE = 10_000
ANDROID_CODE_MAX = 2_147_483_647


def parse_version(value: str) -> tuple[int, int, int] | None:
    """Return ``(major, minor, patch)`` for ``v1.2.3`` / ``1.2.3-preview``."""
    match = VERSION_RE.fullmatch(str(value or "").strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def normalize_version(value: str) -> str | None:
    parts = parse_version(value)
    if parts is None:
        return None
    return ".".join(str(part) for part in parts)


def tag_for(version: str) -> str | None:
    normalized = normalize_version(version)
    return f"v{normalized}" if normalized else None


def compare_versions(candidate: str, current: str) -> int | None:
    """Return 1 when candidate is newer, -1 when older, 0 when equal.

    ``None`` means at least one value is not a version this project writes.
    """
    left = parse_version(candidate)
    right = parse_version(current)
    if left is None or right is None:
        return None
    if left == right:
        return 0
    return 1 if left > right else -1


def is_newer(candidate: str, current: str) -> bool:
    return compare_versions(candidate, current) == 1


def android_version_code(version: str) -> int:
    """Derive a monotonic, installable Android versionCode from a version."""
    parts = parse_version(version)
    if parts is None:
        raise ValueError(f"not a PremiumTV version: {version!r}")
    major, minor, patch = parts
    code = major * MAJOR_SCALE + minor * MINOR_SCALE + patch
    if code > ANDROID_CODE_MAX:
        raise ValueError(f"version {version} exceeds Android's versionCode limit")
    return code


def _release_tag(release: dict) -> str:
    return str(release.get("tag") or release.get("tag_name") or "")


def _is_stable(release: dict) -> bool:
    return not release.get("draft") and not release.get("prerelease")


def stable_versions(releases: Iterable[dict]) -> list[str]:
    versions = []
    for release in releases:
        if not isinstance(release, dict) or not _is_stable(release):
            continue
        version = normalize_version(_release_tag(release))
        if version:
            versions.append(version)
    return versions


def newest_stable(releases: Iterable[dict], exclude: str | None = None) -> str | None:
    wanted = normalize_version(exclude or "")
    versions = [version for version in stable_versions(releases) if version != wanted]
    return max(versions, key=parse_version) if versions else None


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
        return 1, f"{tag!r} is not a version tag (expected vMAJOR.MINOR.PATCH)"
    previous = newest_stable(releases, exclude=version)
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
    parser.add_argument("--normalize", metavar="VERSION", help="print MAJOR.MINOR.PATCH")
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
