#!/usr/bin/env python3
"""Fail a release build when the packaged local-channel directory is stale.

The apps resolve a ZIP code against the directory baked into the installer
(``assets/bundle/local-channels.json`` in the APK, ``Contents/Resources/bundle``
in the macOS app), and the macOS renderer reads the copy inside ``meta.json``.
A release can therefore look correct in the repository while the installer
still ships yesterday's markets.  This check runs on the built artifact, after
the bundle has been packed and before the installer is attached to the release:

    python3 scripts/verify_release_bundle.py --apk path/to/app-debug.apk
    python3 scripts/verify_release_bundle.py --dmg macos/app/dist/*.dmg

It requires ZIP prefixes 170-176 to resolve to the Harrisburg, York and
Lancaster markets, each carrying WGAL (NBC), WHP (CBS 21) and WPMT (FOX 43),
and their channel ids to be present in the packaged playlist.  APKs are read
with the standard library; DMGs use ``hdiutil`` on macOS and 7-Zip elsewhere.

Exit status is 1 when any artifact fails, so the build workflow stops before
uploading or attaching the installer.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

# The three stations the Harrisburg-Lancaster-York viewing area receives, and
# the id each one is matched by in the published playlist.
REQUIRED_STATIONS = {
    "WGAL": "NBC.us@WGAL",
    "WHP": "CBS.us@WHP",
    "WPMT": "FOX.us@WPMT",
}

# ZIP prefix -> the market it must resolve to. 170-172 are Harrisburg
# (USHAR), 173-174 York (USTHV), 175-176 Lancaster (USLNS).
EXPECTED_PREFIX_MARKETS = {
    "170": "USHAR",
    "171": "USHAR",
    "172": "USHAR",
    "173": "USTHV",
    "174": "USTHV",
    "175": "USLNS",
    "176": "USLNS",
}

BUNDLE_FILES = ("local-channels.json", "meta.json", "channels.jsonl")
APK_BUNDLE_DIR = "assets/bundle"
DMG_BUNDLE_SUFFIX = "Contents/Resources/bundle"


class BundleError(RuntimeError):
    """The artifact could not be read as a PremiumTV bundle."""


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _loads(raw: bytes, label: str):
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as error:
        raise BundleError(f"{label} is not valid JSON ({error})") from error


def directory_problems(document, label: str = "local-channels.json") -> list[str]:
    """Every reason the directory cannot answer ZIPs 170-176 with the trio."""
    problems: list[str] = []
    if not isinstance(document, dict):
        return [f"{label}: the document is not an object"]
    markets = {
        market.get("id"): market
        for market in document.get("markets") or []
        if isinstance(market, dict)
    }
    prefixes = {
        row.get("prefix"): row
        for row in document.get("zip_prefixes") or []
        if isinstance(row, dict)
    }

    for prefix, expected_market in sorted(EXPECTED_PREFIX_MARKETS.items()):
        row = prefixes.get(prefix)
        if row is None:
            problems.append(f"{label}: ZIP prefix {prefix} is missing")
        elif (row.get("market") or "") != expected_market:
            problems.append(
                f"{label}: ZIP prefix {prefix} resolves to "
                f"{row.get('market') or 'nothing'}, expected {expected_market}"
            )

    # Check each market once, not once per prefix that points at it.
    for market_id in sorted(set(EXPECTED_PREFIX_MARKETS.values())):
        market = markets.get(market_id)
        if market is None:
            problems.append(f"{label}: market {market_id} is missing")
            continue
        stations = {
            station.get("callsign"): station
            for station in market.get("stations") or []
            if isinstance(station, dict) and station.get("callsign")
        }
        missing = [call for call in REQUIRED_STATIONS if call not in stations]
        if missing:
            present = ", ".join(sorted(stations)) or "none"
            problems.append(
                f"{label}: {market_id} ({market.get('city', '?')}, "
                f"{market.get('state', '?')}) is missing {', '.join(missing)}; "
                f"it carries {present}"
            )
        for callsign, expected_id in REQUIRED_STATIONS.items():
            station = stations.get(callsign)
            if station is None:
                continue
            if station.get("channel_id") != expected_id:
                problems.append(
                    f"{label}: {callsign} in {market_id} has channel_id "
                    f"{station.get('channel_id')!r}, expected {expected_id!r}"
                )
            if not station.get("url"):
                problems.append(f"{label}: {callsign} in {market_id} has no stream URL")
    return problems


def bundle_problems(document, meta, channel_ids) -> list[str]:
    """Check both copies of the directory and the playlist it resolves against."""
    problems = directory_problems(document)
    problems += directory_problems(meta.get("local_channels"), "meta.json local_channels")

    meta_directory = meta.get("local_channels")
    if not isinstance(meta_directory, dict):
        problems.append("meta.json: local_channels is missing")
    elif _canonical(meta_directory) != _canonical(document):
        problems.append(
            "meta.json: local_channels differs from bundle/local-channels.json "
            "(the macOS app resolves against meta.json)"
        )

    known_ids = set(channel_ids)
    for callsign, channel_id in REQUIRED_STATIONS.items():
        if channel_id not in known_ids:
            problems.append(
                f"channels.jsonl: {callsign} id {channel_id!r} is not in the packaged playlist"
            )
    return problems


class Bundle:
    def __init__(self, document, meta, channel_ids):
        self.document = document
        self.meta = meta
        self.channel_ids = channel_ids


def _read_apk(path: Path) -> Bundle:
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as error:
        raise BundleError(f"cannot open the APK ({error})") from error
    with archive:
        names = set(archive.namelist())
        missing = [f"{APK_BUNDLE_DIR}/{name}" for name in BUNDLE_FILES
                   if f"{APK_BUNDLE_DIR}/{name}" not in names]
        if missing:
            raise BundleError(f"the APK is missing {', '.join(missing)}")
        document = _loads(archive.read(f"{APK_BUNDLE_DIR}/local-channels.json"),
                          "assets/bundle/local-channels.json")
        meta = _loads(archive.read(f"{APK_BUNDLE_DIR}/meta.json"),
                      "assets/bundle/meta.json")
        channel_ids = _channel_ids(archive.read(f"{APK_BUNDLE_DIR}/channels.jsonl"),
                                   "assets/bundle/channels.jsonl")
    return Bundle(document, meta, channel_ids)


def _channel_ids(raw: bytes, label: str) -> list[str]:
    ids: list[str] = []
    for number, line in enumerate(raw.decode("utf-8", errors="replace").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except ValueError as error:
            raise BundleError(f"{label} line {number} is not JSON ({error})") from error
        channel_id = str(row.get("id") or "").strip()
        if channel_id:
            ids.append(channel_id)
    return ids


def _sevenzip() -> str | None:
    for name in ("7zz", "7z", "7za"):
        found = shutil.which(name)
        if found:
            return found
    return None


def _dmg_member_7z(tool: str, image: Path, name: str) -> bytes:
    patterns = [
        f"*/PremiumTV.app/{DMG_BUNDLE_SUFFIX}/{name}",
        f"*/{DMG_BUNDLE_SUFFIX}/{name}",
    ]
    for pattern in patterns:
        result = subprocess.run(
            [tool, "e", "-so", str(image), pattern],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
    detail = result.stderr.decode("utf-8", errors="replace").strip().splitlines()
    raise BundleError(
        f"cannot find {name} in the DMG"
        + (f" ({detail[-1]})" if detail else "")
    )


def _bundle_from_dir(directory: Path) -> Bundle:
    missing = [name for name in BUNDLE_FILES if not (directory / name).is_file()]
    if missing:
        raise BundleError(f"the bundle is missing {', '.join(missing)}")
    document = json.loads((directory / "local-channels.json").read_text(encoding="utf-8"))
    meta = json.loads((directory / "meta.json").read_text(encoding="utf-8"))
    channel_ids = _channel_ids((directory / "channels.jsonl").read_bytes(),
                               "bundle/channels.jsonl")
    return Bundle(document, meta, channel_ids)


def _read_dmg_hdiutil(path: Path) -> Bundle:
    with tempfile.TemporaryDirectory(prefix="premiumtv-dmg-") as tmp:
        mount = Path(tmp) / "mount"
        mount.mkdir()
        attach = subprocess.run(
            ["hdiutil", "attach", "-nobrowse", "-readonly", "-noautoopen",
             "-mountpoint", str(mount), str(path)],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        if attach.returncode != 0:
            detail = attach.stderr.decode("utf-8", errors="replace").strip()
            raise BundleError(f"hdiutil could not mount the DMG ({detail})")
        try:
            directories = [
                candidate for candidate in mount.rglob("bundle")
                if candidate.is_dir()
                and candidate.parent.name == "Resources"
                and candidate.parent.parent.name == "Contents"
            ]
            if len(directories) != 1:
                raise BundleError(
                    f"expected one {DMG_BUNDLE_SUFFIX} in the DMG, found {len(directories)}"
                )
            return _bundle_from_dir(directories[0])
        finally:
            detach = subprocess.run(
                ["hdiutil", "detach", str(mount), "-quiet"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )
            if detach.returncode != 0:
                subprocess.run(
                    ["hdiutil", "detach", str(mount), "-force", "-quiet"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )


def _read_dmg_7z(path: Path) -> Bundle:
    tool = _sevenzip()
    if tool is None:
        raise BundleError(
            "no DMG extractor available: run on macOS (hdiutil) or install 7-Zip"
        )
    document = _loads(_dmg_member_7z(tool, path, "local-channels.json"),
                      "local-channels.json")
    meta = _loads(_dmg_member_7z(tool, path, "meta.json"), "meta.json")
    channel_ids = _channel_ids(_dmg_member_7z(tool, path, "channels.jsonl"),
                               "bundle/channels.jsonl")
    return Bundle(document, meta, channel_ids)


def _read_dmg(path: Path) -> Bundle:
    if sys.platform == "darwin" and shutil.which("hdiutil"):
        return _read_dmg_hdiutil(path)
    return _read_dmg_7z(path)


def read_bundle(path: Path, kind: str) -> Bundle:
    if not path.is_file():
        raise BundleError(f"{path} does not exist")
    if kind == "apk":
        return _read_apk(path)
    if kind == "dmg":
        return _read_dmg(path)
    raise BundleError(f"unknown artifact kind {kind!r}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apk", nargs="+", default=[], metavar="APK",
                        help="Android APK to inspect")
    parser.add_argument("--dmg", nargs="+", default=[], metavar="DMG",
                        help="macOS DMG to inspect")
    args = parser.parse_args(argv)
    if not args.apk and not args.dmg:
        parser.error("give at least one --apk or --dmg")

    failed = False
    for kind, paths in (("apk", args.apk), ("dmg", args.dmg)):
        for raw_path in paths:
            path = Path(raw_path)
            try:
                bundle = read_bundle(path, kind)
            except BundleError as error:
                failed = True
                print(f"[FAIL] {kind.upper()} {path}: {error}", file=sys.stderr)
                continue
            problems = bundle_problems(bundle.document, bundle.meta, bundle.channel_ids)
            if problems:
                failed = True
                print(f"[FAIL] {kind.upper()} {path.name}", file=sys.stderr)
                for problem in problems:
                    print(f"  - {problem}", file=sys.stderr)
                continue
            print(
                f"[ok] {kind.upper()} {path.name}: "
                f"{bundle.document.get('station_count')} station entries, "
                f"{bundle.document.get('market_count')} markets; "
                "ZIP 170-176 -> WGAL, WHP, WPMT"
            )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
