#!/usr/bin/env python3
"""Verify the live GitHub release chain the in-app updaters use.

The Android and macOS updaters both:

  1. read ``https://api.github.com/repos/cgyegcvcecvoc/PremiumTV/releases``;
  2. offer only a published, non-prerelease release numerically above the
     installed build;
  3. require the exact installer for this platform to be attached;
  4. download it and check it against the release's ``SHA256SUMS-*.txt``.

This script checks that chain against the live repository for the current
``VERSION`` (1.1.4): the release exists, is complete, carries the expected
assets, and every checksum file entry matches GitHub's own SHA-256 digest for
the asset. It also checks that the old ``PremiumTV1`` slug still redirects
(installed 1.1.3 builds depend on it) and that the published notice document
targets 1.1.3 and below.

Usage::

    python3 scripts/verify_update_chain.py
    python3 scripts/verify_update_chain.py --version 1.1.4

Exit code 0 when the chain is complete and consistent, 1 otherwise.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import release_version  # noqa: E402

OWNER = "cgyegcvcecvoc"
REPO = "PremiumTV"
OLD_REPO = "PremiumTV1"
API = f"https://api.github.com/repos/{OWNER}/{REPO}"
OLD_API = f"https://api.github.com/repos/{OWNER}/{OLD_REPO}"
RELEASES_API = f"{API}/releases?per_page=30"
NOTICE_API = f"{API}/contents/app-update-notice.json"
USER_AGENT = "PremiumTV-update-chain-verifier/1.0"


def fetch(url: str, *, method: str = "GET") -> bytes:
    request = urllib.request.Request(url, method=method, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def fetch_json(url: str) -> object:
    return json.loads(fetch(url))


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """A redirect handler that refuses to follow, so 301s stay visible."""

    def redirect_request(self, *args, **kwargs):  # noqa: D102
        return None


def fetch_no_redirect(url: str) -> tuple[int, str]:
    opener = urllib.request.build_opener(NoRedirect)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with opener.open(request, timeout=60) as response:
            return response.status, response.headers.get("Location", "")
    except urllib.error.HTTPError as error:
        return error.code, error.headers.get("Location", "")


def asset_digest(asset: dict) -> str | None:
    digest = str(asset.get("digest") or "")
    prefix, _, value = digest.partition(":")
    if prefix.lower() != "sha256":
        return None
    return value.strip().lower()


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--version", default=release_version.current_version(),
                        help="release version to verify (default: VERSION)")
    args = parser.parse_args(argv)
    version = release_version.normalize_version(args.version)
    if version is None:
        fail(f"{args.version!r} is not a PremiumTV version")
        return 1
    expected_tag = f"v{version}"
    mac_version = release_version.macos_version(version) or version
    required = [f"PremiumTV-{version}-debug.apk",
                "SHA256SUMS-android.txt", "SHA256SUMS-macos.txt"]
    for arch in ("arm64", "x64"):
        for ext in ("dmg", "pkg"):
            required.append(f"PremiumTV-{mac_version}-mac-{arch}.{ext}")

    problems: list[str] = []

    # 1. The old slug must still redirect for already-installed builds.
    status, location = fetch_no_redirect(f"{OLD_API}/releases?per_page=30")
    if status != 301 or not location.startswith("https://api.github.com/repositories/"):
        problems.append(
            f"the old {OLD_REPO} releases API did not redirect to the canonical "
            f"repository (status {status}, location {location!r})")
    else:
        print(f"OK: old {OLD_REPO} releases API redirects (301) for installed builds")

    # 2. The canonical release list must be readable and contain the release.
    try:
        releases = fetch_json(RELEASES_API)
    except (urllib.error.URLError, json.JSONDecodeError) as error:
        fail(f"could not read the canonical releases API: {error}")
        return 1
    if not isinstance(releases, list):
        fail("the releases API did not return a list")
        return 1

    def tag_of(release: dict) -> str:
        return str(release.get("tag_name") or release.get("tag") or "")

    def version_of(release: dict) -> str | None:
        return release_version.normalize_version(tag_of(release))

    stable = [r for r in releases
              if not r.get("draft") and not r.get("prerelease")
              and version_of(r) is not None]
    newest = max(stable, key=lambda r: release_version.parse_version(version_of(r)) or (0,),
                 default=None)
    release = next((r for r in releases if tag_of(r) == expected_tag), None)
    if release is None:
        problems.append(f"release {expected_tag} is not in the canonical release list")
    else:
        if release.get("draft") or release.get("prerelease"):
            problems.append(f"{expected_tag} is a draft or pre-release; updaters ignore it")
        if newest is not None and tag_of(newest) != expected_tag:
            problems.append(
                f"the newest stable release is {tag_of(newest)}, not {expected_tag}")
        assets = {str(a.get("name") or ""): a for a in release.get("assets") or []}
        missing = [name for name in required if name not in assets]
        if missing:
            problems.append(f"{expected_tag} is missing assets: {', '.join(missing)}")
        else:
            print(f"OK: {expected_tag} is the newest stable release with all "
                  f"{len(required)} required assets")

        # 3. The checksum files must be exactly the sha256sum/shasum output for
        #    the published assets. GitHub's own digest for each asset is the
        #    SHA-256 of its bytes, so rebuilding the expected checksum file and
        #    comparing its digest verifies the file without downloading it.
        android_name = f"PremiumTV-{version}-debug.apk"
        android_expected = (
            f"{asset_digest(assets[android_name])}  {android_name}\n").encode()
        mac_names = [
            f"PremiumTV-{mac_version}-mac-arm64.dmg",
            f"PremiumTV-{mac_version}-mac-x64.dmg",
            f"PremiumTV-{mac_version}-mac-arm64.pkg",
            f"PremiumTV-{mac_version}-mac-x64.pkg",
        ]
        mac_expected = "".join(
            f"{asset_digest(assets[name])}  {name}\n" for name in mac_names
        ).encode()
        for checksum_name, expected in (
            ("SHA256SUMS-android.txt", android_expected),
            ("SHA256SUMS-macos.txt", mac_expected),
        ):
            asset = assets.get(checksum_name)
            if asset is None:
                continue
            actual = asset_digest(asset)
            expected_digest = hashlib.sha256(expected).hexdigest()
            if actual is None:
                problems.append(f"GitHub returned no SHA-256 digest for {checksum_name}")
            elif actual != expected_digest:
                problems.append(
                    f"{checksum_name} does not match the published asset digests "
                    f"(file {actual}, expected {expected_digest})")
            elif int(asset.get("size") or 0) != len(expected):
                problems.append(
                    f"{checksum_name} is {asset.get('size')} bytes, expected {len(expected)}")
            else:
                print(f"OK: {checksum_name} matches GitHub's digests for "
                      f"{len(expected.splitlines())} assets")

        # 4. The release page and asset URLs must resolve (a 302 is fine).
        page_status, _ = fetch_no_redirect(
            f"https://github.com/{OWNER}/{REPO}/releases/tag/{expected_tag}")
        if page_status not in (200, 302):
            problems.append(f"the {expected_tag} release page returned HTTP {page_status}")
        else:
            print(f"OK: the {expected_tag} release page is reachable (HTTP {page_status})")

    # 5. The published notice must target the previous stable and name this one.
    try:
        notice_payload = fetch_json(NOTICE_API)
        notice = json.loads(base64.b64decode(notice_payload["content"]).decode())
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, TypeError) as error:
        problems.append(f"could not read the published update notice: {error}")
    else:
        rules = {str(rule.get("id")): rule for rule in notice.get("rules", [])}
        sunset = rules.get("update-below-newest", {})
        if sunset.get("max_version") != "1.1.3":
            problems.append(
                f"the update notice targets {sunset.get('max_version')!r}, not 1.1.3")
        if version not in str(sunset.get("surprise", "")):
            problems.append(f"the update notice does not mention {version}")
        for field in ("notice_url", "releases_url", "repo_url"):
            value = str(notice.get(field, ""))
            if f"{OWNER}/{REPO}" not in value:
                problems.append(f"notice {field} is not canonical: {value!r}")
        if not problems:
            print("OK: the published notice targets 1.1.3 and below and names "
                  f"{version} with canonical URLs")

    if problems:
        for problem in problems:
            fail(problem)
        return 1
    print(f"OK: the in-app update chain can offer {version} on Android and macOS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
