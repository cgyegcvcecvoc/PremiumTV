#!/usr/bin/env python3
"""Keep the Android TV's copy of the Spotify module identical to the shared one.

The Spotify tab's rules - what a Spotify link is, which embed URL it becomes, how
sign-in works - live in exactly one file:

    macos/app/src/renderer/spotify.js

Three hosts read it. The web build copies it into `web/dist/shared/` at build
time; the macOS and Linux renderer loads it from its own folder; and the Android
TV shell (`android/app/src/main/assets/premiumtv/index.html`) needs it beside
itself inside the APK, because a WebView cannot reach outside the asset folder.

That last copy is the one that could silently rot, so this script writes it and
the test suite fails when the two disagree:

    python scripts/sync_spotify_assets.py            # copy the module into the APK
    python scripts/sync_spotify_assets.py --check    # exit 1 if it is out of date

Run it after editing the module. Android's build workflow runs `--check` before
Gradle, so a TV build can never ship an older policy than the desktop app.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "macos" / "app" / "src" / "renderer" / "spotify.js"
TARGET = ROOT / "android" / "app" / "src" / "main" / "assets" / "premiumtv" / "spotify.js"

# The shell that loads it has to exist too; the module on its own is not a page.
SHELL = TARGET.with_name("index.html")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="verify the APK copy matches the shared module; change nothing")
    args = parser.parse_args(argv)

    if not SOURCE.is_file():
        print(f"error: {SOURCE.relative_to(ROOT)} is missing - it is the only source for this module",
              file=sys.stderr)
        return 1
    if not SHELL.is_file():
        print(f"error: {SHELL.relative_to(ROOT)} is missing - the TV tab has no page to load",
              file=sys.stderr)
        return 1

    source_text = SOURCE.read_text(encoding="utf-8")
    if not TARGET.is_file():
        if args.check:
            print(f"[spotify] {TARGET.relative_to(ROOT)} is missing; run "
                  "`python scripts/sync_spotify_assets.py`", file=sys.stderr)
            return 1
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(source_text, encoding="utf-8")
        print(f"[spotify] wrote {TARGET.relative_to(ROOT)}")
        return 0

    if digest(SOURCE) == digest(TARGET):
        print(f"[spotify] {TARGET.relative_to(ROOT)} matches the shared module "
              f"({len(source_text.splitlines())} lines)")
        return 0

    if args.check:
        print(
            f"[spotify] {TARGET.relative_to(ROOT)} is stale: it differs from "
            f"{SOURCE.relative_to(ROOT)}.\n"
            "          The TV would enforce an older policy than the other apps. "
            "Run `python scripts/sync_spotify_assets.py`.",
            file=sys.stderr,
        )
        return 1

    shutil.copyfile(SOURCE, TARGET)
    print(f"[spotify] copied {SOURCE.name} -> {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
