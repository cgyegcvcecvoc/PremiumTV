#!/usr/bin/env python3
"""Pause, inspect or restore the Movies & Shows shelf.

The shelf has one source of truth - `playlists/vod/vod-catalog.json` - and the
web player, the Android app and the macOS app all render whatever it contains.
When it carries `status: "coming_soon"` and no items, every client shows its
coming-soon page instead of a poster grid.

    python3 scripts/vod_shelf.py             # report the current state
    python3 scripts/vod_shelf.py --pause     # empty the shelf, keep the media
    python3 scripts/vod_shelf.py --resume    # rebuild it from the curated list

`--pause` rewrites the catalogue and the health document and leaves the
test-card media in `playlists/vod/media/` alone, so the shelf can be exercised
again later. `--resume` runs `scripts/vod_catalog.py`, which needs network
access to resolve and probe the Internet Archive entries.

Only the standard library is used, like the rest of scripts/.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOD_DIR = os.path.join(ROOT, "playlists", "vod")
CATALOG_PATH = os.path.join(VOD_DIR, "vod-catalog.json")
HEALTH_PATH = os.path.join(VOD_DIR, "vod-health.json")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vod_catalog  # noqa: E402

COMING_SOON_NOTE = (
    "Movies & Shows is paused. The curated public-domain films and classic TV "
    "episodes were removed from the shelf; live channels, the guide and the "
    "rest of the app are unchanged. Run python3 scripts/vod_shelf.py --resume "
    "to rebuild the catalogue when a replacement is chosen."
)


def log(message: str) -> None:
    print(message, flush=True)


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, ValueError):
        return {}
    return document if isinstance(document, dict) else {}


def write(path: str, document: dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(document, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def pause_document(catalog: dict, generated_utc: str) -> dict:
    """The paused catalogue: same shape, no titles, explicit reason."""
    return {
        "schema": 1,
        "generated_utc": generated_utc,
        "source": catalog.get("source")
        or "Internet Archive public-domain film and classic TV collection",
        "status": "coming_soon",
        "note": COMING_SOON_NOTE,
        "items": [],
    }


def paused_health(generated_utc: str) -> dict:
    return {
        "schema": 1,
        "generated_utc": generated_utc,
        "status": "coming_soon",
        "note": "No on-demand streams are published while the Movies & Shows shelf is paused.",
        "items": [],
    }


def is_coming_soon(catalog: dict) -> bool:
    return catalog.get("status") == "coming_soon"


def describe(catalog: dict) -> str:
    if is_coming_soon(catalog):
        return "coming soon (0 titles)"
    items = catalog.get("items")
    count = len(items) if isinstance(items, list) else 0
    return "%d title%s" % (count, "" if count == 1 else "s")


def report() -> int:
    catalog = load(CATALOG_PATH)
    if not catalog:
        log("[vod] no catalogue at %s" % os.path.relpath(CATALOG_PATH, ROOT))
        return 1
    log("[vod] Movies & Shows: %s" % describe(catalog))
    log("[vod] source: %s" % os.path.relpath(CATALOG_PATH, ROOT))
    if is_coming_soon(catalog):
        log("[vod] clients render their coming-soon page")
        log("[vod] restore with: python3 scripts/vod_shelf.py --resume")
    else:
        log("[vod] clients render the shelf; pause with: python3 scripts/vod_shelf.py --pause")
    return 0


def pause() -> int:
    catalog = load(CATALOG_PATH)
    catalog = pause_document(catalog, now_utc())
    problems = vod_catalog.validate_document(catalog)
    if problems:
        for problem in problems:
            log("[vod] %s" % problem)
        return 1
    write(CATALOG_PATH, catalog)
    write(HEALTH_PATH, paused_health(catalog["generated_utc"]))
    log("[vod] Movies & Shows paused; %s now publishes 0 items" % os.path.relpath(CATALOG_PATH, ROOT))
    log("[vod] media kept in %s" % os.path.relpath(os.path.join(VOD_DIR, "media"), ROOT))
    return 0


def resume() -> int:
    log("[vod] rebuilding the catalogue with scripts/vod_catalog.py ...")
    result = subprocess.run(
        [sys.executable, os.path.join(ROOT, "scripts", "vod_catalog.py")],
        cwd=ROOT,
    )
    if result.returncode != 0:
        log("[vod] the rebuild failed; the shelf stays paused")
        return result.returncode
    return report()


def main() -> int:
    parser = argparse.ArgumentParser(description="Pause, inspect or restore the Movies & Shows shelf.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--pause", action="store_true", help="publish an empty coming-soon catalogue")
    group.add_argument("--resume", action="store_true", help="rebuild the catalogue from the curated list")
    args = parser.parse_args()

    if args.pause:
        return pause()
    if args.resume:
        return resume()
    return report()


if __name__ == "__main__":
    sys.exit(main())
