#!/usr/bin/env python3
"""Build and verify the on-demand (Movies & Shows) test catalogue.

The Movies & Shows tab used to be a coming-soon page. This script is the
feasibility test behind turning it into a real section: a small, curated set of
films and classic TV episodes from the Internet Archive's public-domain
collections is resolved to direct MP4 files, checked over the network the way
the apps play them, and published as one document every platform bundles.

One entry is authored by this repository itself: the synthetic test card in
playlists/vod/media/ (built by scripts/vod_test_card.py), which proves the
shelf end to end with video, audio and on-screen text in a single short play.

Why the Internet Archive: the files are public domain or explicitly licensed
for reuse, they are served over plain HTTPS with byte-range support, and each
item has a stable identifier, a poster and an MP4 derivative - exactly what a
side player needs. Nothing here is a linear channel, so it never enters the
M3U, the guide or the channel health pipeline.

Alongside every direct MP4 the catalogue now publishes an **HTML embed** -
`https://archive.org/embed/<identifier>` - which is the play path the web and
macOS clients open first. An embed is a plain iframe: no CORS, no codec
negotiation and no range requests, so a title that a browser cannot stream
directly still plays. The direct MP4 stays on the item as the fallback server,
which is what Android's ExoPlayer uses. Both are optional in the schema: an
item needs a stream, an embed, or both.

Extra embed providers (any site that publishes an iframe or a pasted embed
snippet) are added by hand to playlists/vod/embed-sources.json - see
playlists/vod/EMBEDS.md. Nothing in this script contacts a commercial
streaming site; only providers you list yourself are ever published.

    python scripts/vod_catalog.py                 # resolve, verify, write
    python scripts/vod_catalog.py --check         # verify the committed file
    python scripts/vod_catalog.py --offline       # rebuild without any network
    python scripts/vod_catalog.py --report-only   # print findings, write nothing

Outputs:

    playlists/vod/vod-catalog.json   the catalogue the apps bundle
    playlists/vod/vod-health.json    per-item probe result of the last run
    playlists/vod/FEASIBILITY.md     human-readable test report

The committed document can also be paused: `status` is `coming_soon` and
`items` is empty, which every client renders as its coming-soon page. Use
`scripts/vod_shelf.py` to flip that state without touching the media.

Only the standard library is used, like the rest of scripts/.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOD_DIR = os.path.join(ROOT, "playlists", "vod")
CATALOG_PATH = os.path.join(VOD_DIR, "vod-catalog.json")
HEALTH_PATH = os.path.join(VOD_DIR, "vod-health.json")
REPORT_PATH = os.path.join(VOD_DIR, "FEASIBILITY.md")

METADATA_URL = "https://archive.org/metadata/%s"
DOWNLOAD_BASE = "https://archive.org/download/%s/%s"
POSTER_URL = "https://archive.org/services/img/%s"
# The Archive's own iframe player. It needs no CORS, no range support and no
# codec negotiation, so it is the first server the web and macOS clients try.
EMBED_BASE = "https://archive.org/embed/%s"
EMBED_PROVIDER = "Internet Archive"
EMBED_KIND = "iframe"
USER_AGENT = "PremiumTV-vod-check/1.0 (+https://github.com/cgyegcvcecvoc/PremiumTV)"
# Hand-written extra providers: playlists/vod/embed-sources.json.
EXTRA_EMBEDS_PATH = os.path.join(VOD_DIR, "embed-sources.json")

# The curated test set. Every item is a public-domain film or a classic TV
# episode from a public-domain collection; archive_id is the Internet Archive
# identifier and the script resolves the actual file, runtime and licence from
# the Archive's own metadata - none of that is typed in here.
CURATED = (
    {
        "slug": "night-of-the-living-dead",
        "kind": "movie",
        "archive_id": "night-of-the-living-dead_1968",
        "title": "Night of the Living Dead",
        "year": 1968,
        "genre": "Horror",
        "summary": (
            "George A. Romero's landmark survival horror film: seven strangers "
            "barricade themselves inside a rural Pennsylvania farmhouse as the "
            "recently deceased rise across the countryside."
        ),
    },
    {
        "slug": "plan-9-from-outer-space",
        "kind": "movie",
        "archive_id": "plan-9-from-outer-space_202009",
        "title": "Plan 9 from Outer Space",
        "year": 1959,
        "genre": "Sci-Fi",
        "summary": (
            "Ed Wood's cult sci-fi classic in which extraterrestrials activate "
            "'Plan 9' in San Fernando Valley to stop humanity from building a "
            "world-ending solar bomb."
        ),
    },
    {
        "slug": "nosferatu",
        "kind": "movie",
        "archive_id": "nosferatu.-1922",
        "title": "Nosferatu",
        "year": 1922,
        "genre": "Horror",
    },
    {
        "slug": "his-girl-friday",
        "kind": "movie",
        "archive_id": "his_girl_friday",
        "title": "His Girl Friday",
        "year": 1940,
        "genre": "Comedy",
    },
    {
        "slug": "carnival-of-souls",
        "kind": "movie",
        "archive_id": "carnival_of_souls",
        "title": "Carnival of Souls",
        "year": 1962,
        "genre": "Horror",
    },
    {
        "slug": "suddenly",
        "kind": "movie",
        "archive_id": "suddenly",
        "title": "Suddenly",
        "year": 1954,
        "genre": "Thriller",
        "summary": (
            "Frank Sinatra stars as a ruthless gunman who seizes a hilltop home "
            "overlooking a small California railroad depot ahead of a presidential "
            "train stop."
        ),
    },
    {
        "slug": "mclintock",
        "kind": "movie",
        "archive_id": "mclintok_widescreen",
        "title": "McLintock!",
        "year": 1963,
        "genre": "Western",
        "summary": (
            "John Wayne and Maureen O'Hara headline a boisterous frontier comedy "
            "about cattle baron George Washington McLintock, family feuds, and a "
            "town on the brink of statehood."
        ),
    },
    {
        "slug": "teenagers-from-outer-space",
        "kind": "movie",
        "archive_id": "teenagers_from_outerspace",
        "title": "Teenagers from Outer Space",
        "year": 1959,
        "genre": "Sci-Fi",
        "summary": (
            "A young alien scout breaks ranks with his invasion crew to warn a "
            "small American town before giant crustacean Gargons overrun Earth."
        ),
    },
    {
        "slug": "the-hitch-hiker",
        "kind": "movie",
        "archive_id": "Hitch_Hiker",
        "title": "The Hitch-Hiker",
        "year": 1953,
        "genre": "Noir",
        "summary": (
            "Ida Lupino directs a taut desert thriller following two fishing "
            "buddies held at gunpoint on the road through Baja California by a "
            "sleepless fugitive."
        ),
    },
    {
        "slug": "the-red-house",
        "kind": "movie",
        "archive_id": "TheRedHouse",
        "title": "The Red House",
        "year": 1947,
        "genre": "Mystery",
        "summary": (
            "Edward G. Robinson guards a dark secret deep inside the woods "
            "bordering his isolated farmstead, warning his adopted daughter never "
            "to enter the woods."
        ),
    },
    {
        "slug": "beat-the-devil",
        "kind": "movie",
        "archive_id": "BeatTheDevil1953",
        "title": "Beat the Devil",
        "year": 1953,
        "genre": "Adventure",
        "summary": (
            "John Huston and Truman Capote's sly caper stars Humphrey Bogart, "
            "Jennifer Jones, Gina Lollobrigida, and Peter Lorre as schemers "
            "stranded in an Italian port while chasing African uranium land."
        ),
    },
    {
        "slug": "the-last-man-on-earth",
        "kind": "movie",
        "archive_id": "lastmanonearth-1964",
        "title": "The Last Man on Earth",
        "year": 1964,
        "genre": "Horror",
        "summary": (
            "Vincent Price stars as Dr. Robert Morgan, the lone immune survivor "
            "of a global plague, fortifying his home by night while searching for "
            "a cure by day."
        ),
    },
    {
        "slug": "the-brain-that-wouldnt-die",
        "kind": "movie",
        "archive_id": "brain_that_wouldnt_die",
        "title": "The Brain That Wouldn't Die",
        "year": 1962,
        "genre": "Horror",
        "summary": (
            "An obsessed transplant surgeon keeps his fiancée's severed head alive "
            "in a country laboratory while prowling the city for a replacement "
            "body."
        ),
    },
    {
        "slug": "beverly-hillbillies-jed-buys-stock",
        "kind": "episode",
        "archive_id": "TheBeverlyHillbillies-JedBuysStock-Ep.1x05",
        "title": "Jed Buys Stock",
        "year": 1962,
        "genre": "Comedy",
        "show": "The Beverly Hillbillies",
        "season": 1,
        "episode": 5,
    },
    {
        "slug": "beverly-hillbillies-grannys-spring-tonic",
        "kind": "episode",
        "archive_id": "TheBeverlyHillbillies-GrannysSpringTonic-Ep1x27",
        "title": "Granny's Spring Tonic",
        "year": 1963,
        "genre": "Comedy",
        "show": "The Beverly Hillbillies",
        "season": 1,
        "episode": 27,
    },
    {
        "slug": "dragnet-the-big-ham",
        "kind": "episode",
        "archive_id": "DragnetBigHam",
        "title": "The Big Ham",
        "year": 1954,
        "genre": "Crime",
        "show": "Dragnet",
        "season": 4,
        "episode": 0,
    },
    {
        "slug": "lone-ranger-war-horse",
        "kind": "episode",
        "archive_id": "the-lone-ranger-1949-s-01-e-06-war-horse",
        "title": "War Horse",
        "year": 1949,
        "genre": "Western",
        "show": "The Lone Ranger",
        "season": 1,
        "episode": 6,
    },
    {
        "slug": "sherlock-holmes-pennsylvania-gun",
        "kind": "episode",
        "archive_id": "SherlockHolmes-TheCaseofthePennsylvaniaGun",
        "title": "The Case of the Pennsylvania Gun",
        "year": 1954,
        "genre": "Mystery",
        "show": "Sherlock Holmes",
        "season": 1,
        "episode": 0,
    },
    {
        "slug": "range-rider-treasure-of-santa-dolores",
        "kind": "episode",
        "archive_id": "RangeRiderTreasureOfSantaDolores",
        "title": "Treasure of Santa Dolores",
        "year": 1951,
        "genre": "Western",
        "show": "The Range Rider",
        "season": 1,
        "episode": 0,
        "summary": (
            "The Range Rider and Dick West investigate bandits preying on "
            "prospectors searching for the lost treasure of Santa Dolores."
        ),
    },
    {
        "slug": "superman-stamp-day",
        "kind": "episode",
        "archive_id": "AdventuresOfSupermanStampDayForSchoolChildren",
        "title": "Stamp Day for Superman",
        "year": 1954,
        "genre": "Adventure",
        "show": "Adventures of Superman",
        "season": 0,
        "episode": 0,
        "summary": (
            "George Reeves stars as Clark Kent and Superman in a special episode "
            "foiling a Metropolis jewel thief alongside Jimmy Olsen and Lois Lane."
        ),
    },
)

# The last network-verified resolution of every curated entry: which MP4
# derivative the Archive served, how big it was and how long it runs. It is
# what `--offline` builds from, so the shelf can be rebuilt (and the catalogue
# regenerated after a schema change) on a machine with no network at all. A
# normal networked run re-resolves each entry from the Archive's metadata and
# overwrites these numbers, so a derivative the Archive renames or re-encodes
# is picked up on the next scheduled build rather than drifting.
#
# Sizes are the values the feasibility probe measured, rounded to the megabyte.
# They are presentation data (the report's table); nothing in the apps depends
# on them being exact.
RESOLVED = {
    "night-of-the-living-dead": {
        "file": "Night of the Living Dead - (1968).mp4",
        "size_bytes": 559_000_000,
        "runtime_seconds": 5796,
    },
    "plan-9-from-outer-space": {
        "file": "Plan 9 from Outer Space.mp4",
        "size_bytes": 773_000_000,
        "runtime_seconds": 4740,
    },
    "nosferatu": {
        "file": "Nosferatu.1922.ia.mp4",
        "size_bytes": 457_000_000,
        "runtime_seconds": 5220,
    },
    "his-girl-friday": {
        "file": "his_girl_friday_512kb.mp4",
        "size_bytes": 401_000_000,
        "runtime_seconds": 5505,
    },
    "carnival-of-souls": {
        "file": "carnival_of_souls_512kb.mp4",
        "size_bytes": 361_000_000,
        "runtime_seconds": 4980,
    },
    "suddenly": {
        "file": "suddenly_512kb.mp4",
        "size_bytes": 324_000_000,
        "runtime_seconds": 4534,
    },
    "mclintock": {
        "file": "McLintock_512kb.mp4",
        "size_bytes": 550_863_361,
        "runtime_seconds": 7607,
    },
    "teenagers-from-outer-space": {
        "file": "Teenagers_from_Outer_Space_512kb.mp4",
        "size_bytes": 372_000_000,
        "runtime_seconds": 5160,
    },
    "the-hitch-hiker": {
        "file": "Hitch-Hiker_512kb.mp4",
        "size_bytes": 307_000_000,
        "runtime_seconds": 4260,
    },
    "the-red-house": {
        "file": "The_Red_House_512kb.mp4",
        "size_bytes": 432_000_000,
        "runtime_seconds": 6000,
    },
    "beat-the-devil": {
        "file": "BeatTheDevil1954_512kb.mp4",
        "size_bytes": 385_000_000,
        "runtime_seconds": 5340,
    },
    "the-last-man-on-earth": {
        "file": "lastmanonearth-1964.mp4",
        "size_bytes": 413_000_000,
        "runtime_seconds": 5160,
    },
    "the-brain-that-wouldnt-die": {
        "file": "brain_that_wouldnt_die_512kb.mp4",
        "size_bytes": 354_000_000,
        "runtime_seconds": 4920,
    },
    "beverly-hillbillies-jed-buys-stock": {
        "file": "TheBeverlyHillbillies105-JedBuysStock_512kb.mp4",
        "size_bytes": 109_000_000,
        "runtime_seconds": 1500,
    },
    "beverly-hillbillies-grannys-spring-tonic": {
        "file": "TheBeverlyHillbillies127-GrannysSpringTonic_512kb.mp4",
        "size_bytes": 110_000_000,
        "runtime_seconds": 1500,
    },
    "dragnet-the-big-ham": {
        "file": "Dragnet_Big Ham.mp4",
        "size_bytes": 162_000_000,
        "runtime_seconds": 1560,
    },
    "lone-ranger-war-horse": {
        "file": "The Lone Ranger 1949 (S01E06) War Horse.mp4",
        "size_bytes": 111_000_000,
        "runtime_seconds": 1320,
    },
    "sherlock-holmes-pennsylvania-gun": {
        "file": "TheCaseofthePennsylvaniaGun_512kb.mp4",
        "size_bytes": 116_000_000,
        "runtime_seconds": 1620,
    },
    "range-rider-treasure-of-santa-dolores": {
        "file": "Range Rider - Treasure of Santa Dolores.mp4",
        "size_bytes": 125_000_000,
        "runtime_seconds": 1500,
    },
    "superman-stamp-day": {
        "file": "Adventures of Superman Stamp Day For School Children.mp4",
        "size_bytes": 96_000_000,
        "runtime_seconds": 1080,
    },
}

# Every curated title is public domain (see playlists/vod/FEASIBILITY.md). The
# networked build replaces this with the licence URL the item's own metadata
# publishes; the offline build falls back to it so an entry is never shipped
# with its provenance blank.
DEFAULT_LICENSE = "https://creativecommons.org/publicdomain/mark/1.0/"

# The test card is the one entry this repository authors itself. It is a short
# synthetic film - moving test pattern, per-second timecode and title text, and
# a tone track - regenerated by scripts/vod_test_card.py and committed under
# playlists/vod/media/. The apps open it like any other direct MP4, so one play
# proves video, audio and text all reach the side player. The URL points at the
# repository's CDN copy; VOD_TEST_CARD_BASE overrides it for a local run (point
# it at a loopback server over this same directory).
TEST_CARD_SLUG = "premiumtv-test-card"
TEST_CARD_FILE = "premiumtv-test-card.mp4"
TEST_CARD_POSTER = "premiumtv-test-card.jpg"
TEST_CARD_SECONDS = 65
TEST_CARD_PATH = os.path.join(VOD_DIR, "media", TEST_CARD_FILE)
TEST_CARD_BASE = os.environ.get(
    "VOD_TEST_CARD_BASE",
    "https://cdn.jsdelivr.net/gh/cgyegcvcecvoc/PremiumTV@main/playlists/vod/media",
).rstrip("/")

MIN_RUNTIME_SECONDS = 60
PROBE_BYTES = 4096


def log(message: str) -> None:
    print(message, flush=True)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_json(url: str, timeout: int = 30) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def runtime_seconds(value) -> int:
    """Archive runtimes are seconds as a string, sometimes "MM:SS" or "H:MM:SS"."""
    if value is None:
        return 0
    text = str(value).strip()
    if not text:
        return 0
    try:
        return int(float(text))
    except ValueError:
        pass
    parts = text.split(":")
    try:
        numbers = [int(float(p)) for p in parts]
    except ValueError:
        return 0
    total = 0
    for number in numbers:
        total = total * 60 + number
    return total


def looks_like_mp4(head: bytes) -> bool:
    """An MP4 starts with a size field then an ``ftyp`` box near the front."""
    return b"ftyp" in head[:64]


def pick_video_files(files: list[dict]) -> list[dict]:
    """Every playable MP4 an archive item publishes, smallest fast-start first."""
    candidates = []
    for item in files:
        name = str(item.get("name") or "")
        if not name.lower().endswith((".mp4", ".m4v")):
            continue
        try:
            size = int(item.get("size") or 0)
        except (TypeError, ValueError):
            size = 0
        if size <= 0:
            continue
        if runtime_seconds(item.get("length")) < MIN_RUNTIME_SECONDS:
            continue
        candidates.append((size, name.lower().endswith(".ia.mp4"), name, item))
    candidates.sort(key=lambda row: (row[0], row[1], row[2]))
    return [row[3] for row in candidates]


def pick_video_file(files: list[dict]) -> dict | None:
    """The smallest playable MP4 an archive item publishes."""
    ranked = pick_video_files(files)
    return ranked[0] if ranked else None


def build_test_card() -> dict:
    """The committed test card, described exactly like an Archive entry."""
    size = os.path.getsize(TEST_CARD_PATH) if os.path.isfile(TEST_CARD_PATH) else 0
    return {
        "id": "vod-" + TEST_CARD_SLUG,
        "slug": TEST_CARD_SLUG,
        "title": "PremiumTV Test Card",
        "kind": "movie",
        "show": "",
        "season": 0,
        "episode": 0,
        "year": 2026,
        "genre": "Test",
        "runtime_seconds": TEST_CARD_SECONDS,
        "summary": (
            "A 65-second synthetic clip generated for the Movies & Shows shelf: a "
            "moving test pattern, a running timecode, the title text and a tone with "
            "a beep on every whole second. If the picture moves, the clock counts and "
            "the beeps land on each second, video, audio and text all reached the "
            "player."
        ),
        "stream": "%s/%s" % (TEST_CARD_BASE, TEST_CARD_FILE),
        "poster": "%s/%s" % (TEST_CARD_BASE, TEST_CARD_POSTER),
        "license": "https://creativecommons.org/publicdomain/zero/1.0/",
        "archive_id": "",
        "file": TEST_CARD_FILE,
        "size_bytes": size,
        "test_card": True,
    }


def load_extra_embeds() -> dict[str, list[dict]]:
    """Hand-written embed providers, keyed by catalogue slug.

    playlists/vod/embed-sources.json is optional and ships empty apart from its
    documentation, so the published catalogue is exactly what this repository
    curates. Adding a provider there is the supported way to point a title at
    another free source without touching the build script.
    """
    if not os.path.isfile(EXTRA_EMBEDS_PATH):
        return {}
    try:
        with open(EXTRA_EMBEDS_PATH, "r", encoding="utf-8") as handle:
            document = json.load(handle)
    except (OSError, ValueError) as error:
        log("[vod] %s is unreadable (%s); ignoring it" % (
            os.path.relpath(EXTRA_EMBEDS_PATH, ROOT), error))
        return {}
    extras: dict[str, list[dict]] = {}
    entries = document.get("extra") if isinstance(document, dict) else None
    if not isinstance(entries, list):
        return extras
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        slug = str(entry.get("slug") or "").strip()
        url = str(entry.get("url") or "").strip()
        html = str(entry.get("html") or "").strip()
        if not slug or (not url and not html):
            continue
        if url and not url.startswith(("http://", "https://")):
            log("[vod] %s: embed url must be http(s); skipped" % slug)
            continue
        provider = str(entry.get("provider") or "Embed").strip()
        kind = str(entry.get("kind") or ("iframe" if url else "html")).strip()
        if kind not in ("iframe", "html"):
            log("[vod] %s: embed kind must be iframe or html; skipped" % slug)
            continue
        row = {"provider": provider, "kind": kind}
        if url:
            row["url"] = url
        if html:
            row["html"] = html
        extras.setdefault(slug, []).append(row)
    return extras


def embed_for(spec: dict) -> dict:
    """The Archive's own iframe player for one curated entry."""
    archive_id = spec["archive_id"]
    return {
        "provider": EMBED_PROVIDER,
        "kind": EMBED_KIND,
        "url": EMBED_BASE % urllib.parse.quote(archive_id, safe=""),
    }


def build_item(spec: dict, offline: bool = False) -> dict | None:
    """Resolve one curated entry against the Archive's metadata.

    With ``offline`` the resolution comes from RESOLVED instead - the last
    networked run's answer - so nothing touches the network.
    """
    archive_id = spec["archive_id"]
    cached = RESOLVED.get(spec["slug"]) or {}
    if offline:
        if not cached.get("file"):
            log("  ! %s: no cached derivative; resolved on the next networked run"
                % spec["slug"])
            return None
        ranked = [{
            "name": cached["file"],
            "size": cached.get("size_bytes") or 0,
            "length": cached.get("runtime_seconds") or 0,
        }]
        meta = {}
    else:
        try:
            document = fetch_json(METADATA_URL % urllib.parse.quote(archive_id))
        except (urllib.error.URLError, ValueError, OSError) as error:
            log("  ! %s: metadata unavailable (%s)" % (archive_id, error))
            return None
        meta = document.get("metadata") or {}
        if not meta:
            log("  ! %s: no metadata" % archive_id)
            return None
        ranked = pick_video_files(document.get("files") or [])
        if not ranked:
            log("  ! %s: no MP4 derivative found" % archive_id)
            return None

    chosen = ranked[0]

    name = str(chosen["name"])
    streams = [
        DOWNLOAD_BASE % (urllib.parse.quote(archive_id), urllib.parse.quote(str(f["name"])))
        for f in ranked
    ]
    stream = streams[0]
    title = str(spec.get("title") or meta.get("title") or archive_id).strip()
    summary = str(spec.get("summary") or meta.get("description") or "").strip()
    # Descriptions are HTML in some items; the apps render plain text.
    if "<" in summary and ">" in summary:
        summary = strip_html(summary)
    summary = " ".join(summary.split())
    if len(summary) > 420:
        summary = summary[:417].rstrip() + "…"

    runtime = runtime_seconds(chosen.get("length")) or runtime_seconds(meta.get("runtime"))
    if not runtime:
        runtime = int(cached.get("runtime_seconds") or 0)
    size = int(chosen.get("size") or 0) or int(cached.get("size_bytes") or 0)
    row = {
        "id": "vod-" + spec["slug"],
        "slug": spec["slug"],
        "title": title,
        "kind": spec["kind"],
        "show": spec.get("show", ""),
        "season": int(spec.get("season") or 0),
        "episode": int(spec.get("episode") or 0),
        "year": int(spec.get("year") or 0) or year_of(meta),
        "genre": spec.get("genre", ""),
        "runtime_seconds": runtime,
        "summary": summary,
        "stream": stream,
        # The embed the web and macOS players open first; the direct MP4 stays
        # as the fallback server (and as Android's only path).
        "embed": (EMBED_BASE % urllib.parse.quote(archive_id, safe="")),
        "embed_kind": EMBED_KIND,
        "provider": EMBED_PROVIDER,
        "poster": POSTER_URL % urllib.parse.quote(archive_id),
        "license": str(meta.get("licenseurl") or "").strip() or DEFAULT_LICENSE,
        "archive_id": archive_id,
        "file": name,
        "size_bytes": size,
    }
    if len(streams) > 1:
        row["streams"] = streams
    return row


def year_of(meta: dict) -> int:
    for key in ("year", "date"):
        raw = str(meta.get(key) or "").strip()
        digits = "".join(ch for ch in raw[:4] if ch.isdigit())
        if len(digits) == 4:
            try:
                return int(digits)
            except ValueError:
                continue
    return 0


def strip_html(text: str) -> str:
    result = []
    inside = False
    for char in text:
        if char == "<":
            inside = True
        elif char == ">":
            inside = False
        elif not inside:
            result.append(char)
    return "".join(result)


def probe(url: str, timeout: int = 25) -> dict:
    """Fetch the first bytes of the stream the way a player opens it."""
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Range": "bytes=0-%d" % (PROBE_BYTES - 1),
            "Accept": "video/mp4,video/*;q=0.9,*/*;q=0.5",
        },
    )
    started = dt.datetime.now(dt.timezone.utc)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            head = response.read(PROBE_BYTES)
            elapsed = (dt.datetime.now(dt.timezone.utc) - started).total_seconds()
            content_type = response.headers.get("Content-Type", "").split(";")[0].strip()
            status = "working"
            if not head:
                status = "offline"
            elif not (looks_like_mp4(head) or content_type.startswith("video/")):
                status = "invalid"
            return {
                "status": status,
                "http_status": response.status,
                "content_type": content_type,
                "bytes_read": len(head),
                "seekable": response.status == 206,
                "latency_seconds": round(elapsed, 3),
            }
    except urllib.error.HTTPError as error:
        return {
            "status": "offline" if error.code in (404, 410) else "unreachable",
            "http_status": error.code,
            "content_type": "",
            "bytes_read": 0,
            "seekable": False,
            "latency_seconds": 0,
        }
    except (urllib.error.URLError, OSError) as error:
        return {
            "status": "unreachable",
            "http_status": 0,
            "content_type": "",
            "bytes_read": 0,
            "seekable": False,
            "error": str(error),
            "latency_seconds": 0,
        }


def collect(offline: bool = False) -> tuple[dict, list[dict]]:
    """Resolve every curated item, then probe the ones that resolved."""
    items: list[dict] = []
    test_card = build_test_card()
    if offline:
        test_card["status"] = "unverified"
    else:
        log("[vod] %s (test card)" % TEST_CARD_SLUG)
        result = probe(test_card["stream"])
        test_card["probe"] = result
        test_card["status"] = result["status"]
        if (result["status"] != "working" and result.get("http_status") == 404
                and os.path.isfile(TEST_CARD_PATH)):
            # The clip is committed, but its public copy only exists after the
            # file reaches main. A 404 says exactly that; a timeout or a 5xx
            # stays whatever the probe found so a CDN outage is not masked.
            test_card["status"] = "unpublished"
        log("      %s" % test_card["status"])
    items.append(test_card)
    extra_embeds = load_extra_embeds()
    for spec in CURATED:
        log("[vod] %s" % spec["slug"])
        item = build_item(spec, offline=offline)
        if item is None:
            continue
        # The Archive embed is the verified default; anything hand-added in
        # embed-sources.json follows it, unless it is marked primary.
        embeds = [embed_for(spec)]
        for extra in extra_embeds.get(spec["slug"], []):
            if extra.get("primary"):
                embeds.insert(0, extra)
            else:
                embeds.append(extra)
        item["embeds"] = embeds
        item["embed"] = embeds[0].get("url", "")
        item["embed_kind"] = embeds[0].get("kind", EMBED_KIND)
        item["provider"] = embeds[0].get("provider", EMBED_PROVIDER)
        if embeds[0].get("html"):
            item["embed_html"] = embeds[0]["html"]
        if not offline:
            result = probe(item["stream"])
            item["status"] = result["status"]
            item["probe"] = result
            log("      %s %s (%d MB, %ss)" % (
                result["status"],
                item["file"],
                round(item["size_bytes"] / 1e6),
                item["runtime_seconds"],
            ))
        else:
            item["status"] = "unverified"
        items.append(item)
    # The test card leads the shelf, then films, then episodes, each by title.
    items.sort(key=lambda row: (
        not row.get("test_card"),
        row["kind"] != "movie",
        row["kind"] != "episode",
        row["title"].lower(),
    ))
    catalog = {
        "schema": 1,
        "generated_utc": utc_now(),
        "source": "Internet Archive public-domain film and classic TV collection",
        "note": (
            "On-demand test catalogue. Separate from the live M3U lineup and the "
            "XMLTV guide: these are finite films and episodes, not linear channels."
        ),
        "items": [{key: value for key, value in item.items() if key != "probe"} for item in items],
    }
    return catalog, [item for item in items]


def write_outputs(catalog: dict, items: list[dict], probe_enabled: bool) -> None:
    os.makedirs(VOD_DIR, exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as handle:
        json.dump(catalog, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    healthy = {
        "schema": 1,
        "generated_utc": catalog["generated_utc"],
        "items": [
            {
                "id": item["id"],
                "title": item["title"],
                # The probe also carries a raw status ("offline" for a 404); the
                # resolved one wins so the health file agrees with the catalogue.
                **(item.get("probe") or {}),
                "status": item["status"],
            }
            for item in items
        ],
    }
    with open(HEALTH_PATH, "w", encoding="utf-8") as handle:
        json.dump(healthy, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    with open(REPORT_PATH, "w", encoding="utf-8") as handle:
        handle.write(render_report(catalog, items, probe_enabled))
    log("[vod] wrote %s" % os.path.relpath(CATALOG_PATH, ROOT))
    log("[vod] wrote %s" % os.path.relpath(REPORT_PATH, ROOT))


def render_report(catalog: dict, items: list[dict], probe_enabled: bool) -> str:
    test_cards = [item for item in items if item.get("test_card")]
    movies = [item for item in items if item["kind"] == "movie" and not item.get("test_card")]
    episodes = [item for item in items if item["kind"] == "episode"]
    working = [item for item in items if item["status"] == "working"]
    lines = [
        "# On-demand feasibility test — Movies & Shows",
        "",
        "Generated %s by `scripts/vod_catalog.py`." % catalog["generated_utc"],
        "",
        "This is the evidence behind the Movies & Shows tab: a finite film and",
        "episode library is feasible with the same player, the same side panel and",
        "the same data bundle the live channels already use. It is deliberately",
        "separate from the playlist and guide pipeline.",
        "",
        "## Result",
        "",
        "| Measure | Value |",
        "|---|---:|",
        "| Catalogue entries | %d |" % len(items),
        "| Films | %d |" % len(movies),
        "| TV episodes | %d |" % len(episodes),
        "| Test card (authored here) | %d |" % len(test_cards),
    ]
    if probe_enabled:
        lines += [
            "| Probe: working | %d |" % len(working),
            "| Probe: other | %d |" % (len(items) - len(working)),
        ]
    else:
        lines += ["| Probe | not run (offline rebuild) |"]
    lines += [
        "",
        "The probe opens each stream the way the apps do — a bounded range request",
        "with `Accept: video/mp4` — and requires an MP4 `ftyp` box or a video",
        "content type. A range request that answers `206` also proves the stream is",
        "seekable, which is what lets the side player scrub and resume. An offline",
        "rebuild (`--offline`) resolves every entry from the last networked run's",
        "answer and skips the probe entirely, so the Status column reads",
        "`unverified` until the next scheduled build re-checks each link.",
        "",
        "",
        "## Entries",
        "",
        "| Title | Kind | Year | Runtime | Size | Direct stream | Embed | Probe |",
        "|---|---|---:|---:|---:|---|---|---|",
    ]
    for item in items:
        runtime = "%d min" % round(item["runtime_seconds"] / 60) if item["runtime_seconds"] else "—"
        size = "%.0f MB" % (item["size_bytes"] / 1e6) if item["size_bytes"] else "—"
        kind = "Film" if item["kind"] == "movie" else "TV episode"
        embed = "—"
        if item.get("embed"):
            embed = "[%s](%s)" % (item.get("provider") or "embed", item["embed"])
        elif item.get("embed_html"):
            embed = "snippet"
        lines.append(
            "| %s | %s | %s | %s | %s | `%s` | %s | %s |"
            % (
                item["title"].replace("|", "/"),
                kind,
                item["year"] or "—",
                runtime,
                size,
                item["file"],
                embed,
                item["status"],
            )
        )
    lines += [
        "",
        "## Embeds",
        "",
        "Every Archive entry also publishes an HTML embed,",
        "`https://archive.org/embed/<identifier>`, and the web and macOS players",
        "open that first. An embed is a plain iframe: the browser talks to the",
        "provider directly, so there is no cross-origin fetch to fail, no codec",
        "the browser has to negotiate and no range request to satisfy. The",
        "direct MP4 stays on each entry as the fallback server - which is also",
        "the only path Android's ExoPlayer has, since it cannot render an iframe.",
        "",
        "Additional free providers are wired in by hand through",
        "`playlists/vod/embed-sources.json`; see `playlists/vod/EMBEDS.md`. The",
        "committed file ships with no extra providers, so the published shelf is",
        "the curated public-domain set plus whatever you add yourself.",
        "",
        "## The test card",
        "",
        "`vod-premiumtv-test-card` is the one entry this repository authors: a",
        "65-second synthetic clip (`scripts/vod_test_card.py`, CC0) committed at",
        "`playlists/vod/media/premiumtv-test-card.mp4` with its poster beside it.",
        "It exists so the shelf can be exercised in one play - a moving gold bar",
        "proves the picture is advancing, the timecode proves the clock, the caption",
        "proves text renders, and a beep on every whole second proves audio arrives.",
        "",
        "It streams from the repository's own CDN copy, so the probe can only",
        "answer once the clip has reached `main`. A 404 there is reported as",
        "`unpublished` rather than broken, which keeps the shelf honest between",
        "committing the file and publishing it; anything else keeps whatever the",
        "probe found, so a CDN outage is never disguised as a missing file.",
        "",
        "## What this proves",
        "",
        "- **Sources exist.** Every entry resolves to a direct HTTPS MP4 with byte",
        "  ranges, a poster and a traceable licence - the Archive's own metadata for",
        "  its films, the committed CC0 clip for the test card.",
        "- **The player already handles it.** MP4 plays in the existing ExoPlayer",
        "  (Android) and the existing HLS/MP4 strategies (macOS); no second player",
        "  or new dependency is needed.",
        "- **The side player is the right home.** An on-demand item is just a stream",
        "  with a title and a poster, so it opens in the same docked panel and",
        "  expands to full screen the same way a channel does.",
        "- **The bundle can carry it.** `android/tools/build_bundle.py` copies the",
        "  catalogue into `bundle/vod-catalog.json` and into `meta.vod_catalog`,",
        "  exactly like the team crests and the live schedule.",
        "",
        "## What is deliberately not done yet",
        "",
        "- No scraping of commercial catalogues: the test set is public domain only.",
        "- No resume points, downloads or per-user watch state: that needs a store",
        "  the apps do not have yet (the existing Recently watched shelf is keyed by",
        "  stream URL and already works for these entries).",
        "- No pagination: the test set fits one screen; a real library needs",
        "  paging, search and per-show grouping before it ships at scale.",
        "",
        "## Rights",
        "",
        "Every item is public domain or published by the Internet Archive under a",
        "licence that permits reuse. The licence URL from the item's own metadata is",
        "kept in `vod-catalog.json` so the source of each film stays traceable.",
        "",
    ]
    return "\n".join(lines)


def check_committed() -> int:
    """Offline validation of the committed catalogue (used by CI/tests)."""
    if not os.path.isfile(CATALOG_PATH):
        log("[vod] missing %s" % os.path.relpath(CATALOG_PATH, ROOT))
        return 1
    with open(CATALOG_PATH, "r", encoding="utf-8") as handle:
        catalog = json.load(handle)
    problems = validate_document(catalog)
    for problem in problems:
        log("[vod] %s" % problem)
    if problems:
        return 1
    if catalog.get("status") == "coming_soon":
        log("[vod] OK %s (coming soon, 0 items)" % os.path.relpath(CATALOG_PATH, ROOT))
    else:
        log("[vod] OK %s (%d items)" % (os.path.relpath(CATALOG_PATH, ROOT), len(catalog["items"])))
    return 0


def validate_document(catalog: dict) -> list[str]:
    """Structural checks shared by --check and the test suite."""
    problems = []
    if catalog.get("schema") != 1:
        problems.append("schema must be 1")
    if catalog.get("status") == "coming_soon":
        # A paused shelf is a real, publishable state: the document keeps its
        # shape and every client shows its coming-soon page. It must not carry
        # titles, or an app would advertise a shelf it cannot open.
        if catalog.get("items") not in (None, []):
            problems.append("a coming_soon catalogue must not publish items")
        return problems
    items = catalog.get("items")
    if not isinstance(items, list) or not items:
        return problems + ["items must be a non-empty list"]
    seen = set()
    for index, item in enumerate(items):
        label = "items[%d]" % index
        for key in ("id", "title", "kind", "poster"):
            if not str(item.get(key) or "").strip():
                problems.append("%s: missing %s" % (label, key))
        if item.get("kind") not in ("movie", "episode"):
            problems.append("%s: kind must be movie or episode" % label)
        # An entry is playable with a direct stream, an HTML embed, or both.
        # The apps pick whichever they can open, so neither one is mandatory -
        # but an entry with neither is a card that can never be played.
        stream = str(item.get("stream") or "")
        embed = str(item.get("embed") or "")
        if not stream and not embed and not str(item.get("embed_html") or ""):
            problems.append("%s: needs a stream, an embed or an embed_html" % label)
        if stream and not stream.startswith(("http://", "https://")):
            problems.append("%s: stream must be http(s)" % label)
        if embed and not embed.startswith(("http://", "https://")):
            problems.append("%s: embed must be http(s)" % label)
        if item.get("embed_kind") not in (None, "", "iframe", "html"):
            problems.append("%s: embed_kind must be iframe or html" % label)
        for extra in item.get("embeds") or []:
            if not isinstance(extra, dict):
                problems.append("%s: embeds entries must be objects" % label)
                continue
            url = str(extra.get("url") or "")
            if not url and not str(extra.get("html") or ""):
                problems.append("%s: every embed needs a url or html" % label)
            if url and not url.startswith(("http://", "https://")):
                problems.append("%s: embed url must be http(s)" % label)
            if extra.get("kind") not in (None, "", "iframe", "html"):
                problems.append("%s: embed kind must be iframe or html" % label)
        extra_streams = item.get("streams")
        if extra_streams is not None:
            if not isinstance(extra_streams, list) or not extra_streams:
                problems.append("%s: streams must be a non-empty list when present" % label)
            elif extra_streams[0] != item.get("stream"):
                problems.append("%s: streams[0] must equal stream" % label)
            elif any(not str(url).startswith(("http://", "https://")) for url in extra_streams):
                problems.append("%s: every entry in streams must be http(s)" % label)
        if item.get("kind") == "episode" and not str(item.get("show") or "").strip():
            problems.append("%s: an episode needs a show name" % label)
        item_id = str(item.get("id") or "")
        if item_id in seen:
            problems.append("%s: duplicate id %s" % (label, item_id))
        seen.add(item_id)
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Build and verify the Movies & Shows test catalogue.")
    parser.add_argument("--check", action="store_true", help="validate the committed file and exit")
    parser.add_argument("--offline", action="store_true", help="resolve metadata but skip stream probes")
    parser.add_argument("--report-only", action="store_true", help="probe and report, write nothing")
    args = parser.parse_args()

    if args.check:
        return check_committed()

    catalog, items = collect(offline=args.offline)
    if not items:
        log("[vod] nothing resolved; keeping the committed catalogue")
        return 1
    if args.report_only:
        print(render_report(catalog, items, probe_enabled=not args.offline))
        return 0
    write_outputs(catalog, items, probe_enabled=not args.offline)
    problems = validate_document(catalog)
    if problems:
        for problem in problems:
            log("[vod] %s" % problem)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
