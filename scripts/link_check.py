#!/usr/bin/env python3
"""
Deep M3U link checker (the same job the free-codecs "M3U file checker" tools do,
but scriptable and headless).

The daily scraper only reads the first few KB of a URL, which is enough to say
"a server answered" but not enough to say "a player can play this". This checker
goes further, one link at a time:

    1. fetch the URL with the headers a player would send (#EXTVLCOPT);
    2. if it is an HLS master playlist, resolve the best variant and fetch it;
    3. if it is an HLS media playlist, download (part of) the first segment and
       check it is real media - a TS sync byte, an fMP4 box, or enough bytes;
    4. if it is a DASH manifest, check the manifest is populated;
    5. otherwise classify the payload directly (TS/audio/octet-stream vs HTML).

Each link ends up in exactly one bucket:

| status        | meaning                                                      | patched? |
|---|---|---|
| `working`     | answered and produced playable media                          | keep     |
| `offline`     | confirmed dead: 404/410, DNS failure, refused, HTML, empty    | **removed** |
| `unreachable` | timeout / 429 / 5xx / connection reset - may be transient     | keep     |
| `blocked`     | 401 / 403 / 451 - needs auth or is geo-blocked                | keep     |
| `unsupported` | non-HTTP scheme (rtmp, acestream, ...) that cannot be probed  | keep     |
| `invalid`     | malformed or non-http URL                                     | **removed** |

The variant playlist and the media segment behind a working playlist URL are
held to the same transient/dead split: a segment that is missing (404) or
refused is ``offline``, one whose host answers 429/5xx or times out is
``unreachable``. Relative variant and
segment URIs are resolved against the URL that finally served the playlist,
after redirects.

Only the two confirmed-dead buckets are ever removed, and only with ``--patch``.
Two safety nets keep a bad network day from gutting a good playlist:
``--min-working-ratio`` (default 0.20) aborts patching when too few links are
working overall, and ``--max-remove-ratio`` (default 0.35) skips any single
playlist that would lose more than that share of its entries.

Outputs (all under the playlists directory):

    checks/link-check.json      full machine-readable result of the run
    checks/LINK-CHECK.md        human-readable summary
    logs/link-check-edits.txt   append-only `-removed` log of every patched link

    python scripts/link_check.py --playlist playlists/PremiumTV.m3u
    python scripts/link_check.py --all --patch --workers 96
    python scripts/link_check.py --playlist playlists/AE_Channels.m3u --deep
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import gzip
import http.client
import json
import os
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import zlib
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import categorize  # noqa: E402  (the taxonomy the patched files must match)
import scraper  # noqa: E402  (reuses Channel parsing, host limiting, helpers)

ROOT = Path(__file__).resolve().parent.parent

DEFAULT_UA = scraper.DEFAULT_UA
INSECURE_CTX = scraper.INSECURE_CTX
NON_HTTP_SCHEMES = tuple(scraper.NON_HTTP_SCHEMES)

# How much of a playlist / segment to read. Segments are only probed, never
# downloaded whole: a few KB is enough to prove the stream is alive.
PLAYLIST_READ_BYTES = 256 * 1024
SEGMENT_READ_BYTES = 64 * 1024
SEGMENT_RANGE = f"bytes=0-{SEGMENT_READ_BYTES - 1}"
# Below this, a "segment" is a stub/error page rather than media.
MIN_SEGMENT_BYTES = 512
# Statuses that are confirmed dead and therefore safe to patch out.
DEAD_STATUSES = {"offline", "invalid"}
# A run whose working share falls below this is treated as a network problem.
DEFAULT_MIN_WORKING_RATIO = 0.20
# Never delete more than this share of one playlist in a single patch.
DEFAULT_MAX_REMOVE_RATIO = 0.35

HLS_MASTER_RE = re.compile(r"^#EXT-X-STREAM-INF\b", re.MULTILINE)
HLS_MEDIA_RE = re.compile(r"^#EXT-X-(?:TARGETDURATION|MEDIA-SEQUENCE|DISCONTINUITY-SEQUENCE)\b",
                          re.MULTILINE)
BANDWIDTH_RE = re.compile(r"BANDWIDTH=(\d+)")
SEGMENT_TIMEOUT_RE = re.compile(r"#EXTINF:([0-9.]+)")
MPD_RE = re.compile(r"<MPD\b", re.IGNORECASE)
REPRESENTATION_RE = re.compile(r"<Representation\b", re.IGNORECASE)
STREAM_MEDIA_TYPES = (
    "video/mp2t", "video/mp4", "video/mpeg", "video/x-matroska",
    "audio/mpegurl", "application/vnd.apple.mpegurl", "audio/x-mpegurl",
    "application/octet-stream", "binary/octet-stream", "application/dash+xml",
    "audio/aac", "audio/mp4", "audio/mpeg", "application/mp4",
)


def log(msg: str) -> None:
    print(msg, flush=True)


def display_path(path: Path) -> str:
    """Repo-relative path for reports; absolute when the path lives elsewhere."""
    try:
        return str(Path(path).relative_to(ROOT))
    except ValueError:
        return str(path)


# --------------------------------------------------------------------------- #
# Playlist blocks
# --------------------------------------------------------------------------- #
@dataclass
class Block:
    """One #EXTINF entry plus its option lines and URL, exactly as written."""

    lines: list = field(default_factory=list)
    url: str = ""

    @property
    def name(self) -> str:
        for line in self.lines:
            if line.startswith("#EXTINF"):
                _, _, name = line.partition(",")
                return name.strip() or "Unknown"
        return "Unknown"


def split_blocks(text: str) -> tuple[list, list]:
    """Split a playlist into (header_lines, blocks).

    Everything before the first #EXTINF is treated as the header (including the
    #EXTM3U line with its x-tvg-url guide list), so patching can rewrite the
    entries without ever touching the guide list.
    """
    lines = text.splitlines()
    header: list = []
    blocks: list = []
    pending: list = []
    seen_entry = False
    for raw in lines:
        line = raw.rstrip("\r")
        if not line.strip():
            (pending if seen_entry else header).append(line)
            continue
        if line.startswith("#EXTINF"):
            seen_entry = True
            pending = [line]
            continue
        if not seen_entry:
            header.append(line)
            continue
        if line.startswith("#"):
            if pending:
                pending.append(line)
            continue
        # A non-comment line after an #EXTINF is the stream URL.
        blocks.append(Block(lines=pending + [line], url=scraper.fix_url(line.strip())))
        pending = []
        seen_entry = False
    if pending:
        header.extend(pending)
    return header, blocks


def blocks_to_text(header: list, blocks: list) -> str:
    out = list(header)
    for block in blocks:
        out.extend(block.lines)
    return "\n".join(out) + "\n"


EXTINF_GROUP_RE = re.compile(r'\s*group-title="[^"]*"')


def set_block_group(block: Block, group: str) -> bool:
    """Rewrite one block's ``group-title`` in place. Returns True when changed."""
    for index, line in enumerate(block.lines):
        if not line.startswith("#EXTINF"):
            continue
        if EXTINF_GROUP_RE.search(line):
            updated = EXTINF_GROUP_RE.sub(f' group-title="{group}"', line, count=1)
        else:
            head, separator, rest = line.partition(",")
            updated = (f'{head} group-title="{group}"{separator}{rest}'
                       if separator else f'{line} group-title="{group}"')
        if updated == line:
            return False
        block.lines[index] = updated
        return True
    return False


def tidy_blocks(blocks: list, source: str) -> tuple[list, int]:
    """Put blocks back into the repository's published category order.

    After the deep check removes dead entries the remaining blocks are re-sorted
    and any ``group-title`` the taxonomy would not have written is normalised, so
    a patched playlist is in exactly the order and grouping the next scrape
    publishes - otherwise the file drifts until the next full run. The order is
    taken from the channels themselves (``scraper.canonicalize_channels`` applies
    ``categorize.order_channels``), so no second ordering rule exists.
    Returns (blocks, changed_group_count).
    """
    pairs = [(block, channel_from_block(block, source)) for block in blocks]
    channels = [channel for _, channel in pairs]
    scraper.canonicalize_channels(channels)
    position = {id(channel): index for index, channel in enumerate(channels)}
    pairs.sort(key=lambda pair: (position.get(id(pair[1]), len(position)), pair[1].name))
    changed = 0
    for block, channel in pairs:
        if set_block_group(block, channel.attrs.get("group-title") or categorize.OTHER):
            changed += 1
    return [block for block, _ in pairs], changed


def channel_from_block(block: Block, source: str) -> scraper.Channel:
    """Reuse the scraper's M3U parser so attributes/headers stay consistent."""
    text = "\n".join(["#EXTM3U", *block.lines]) + "\n"
    channels, _ = scraper.parse_m3u(text, source)
    if channels:
        return channels[0]
    return scraper.Channel(name=block.name, url=block.url, source=source)


# --------------------------------------------------------------------------- #
# Low-level fetching
# --------------------------------------------------------------------------- #
def _read_body(response, limit: int) -> bytes:
    try:
        return response.read(limit)
    except http.client.IncompleteRead as exc:
        return exc.partial or b""


def fetch(url: str, headers: dict, timeout: float, limit: int = PLAYLIST_READ_BYTES,
          range_header: str | None = None) -> dict:
    """GET a URL; returns a result dict instead of raising for HTTP errors."""
    request_headers = dict(headers)
    request_headers.setdefault("Accept", "*/*")
    if range_header:
        request_headers["Range"] = range_header
    started = time.time()
    request = urllib.request.Request(url, headers=request_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout, context=INSECURE_CTX) as response:
            status = int(getattr(response, "status", 0) or response.getcode() or 0)
            content_type = (response.headers.get("Content-Type") or "").lower()
            body = _read_body(response, limit)
            # urllib follows redirects silently. Relative URIs inside an HLS
            # playlist are relative to the URL that finally served it, not to
            # the link in the M3U (jmp2.uk -> Pluto TV, for example), so the
            # caller needs the final address to resolve variants and segments.
            final_url = response.geturl() or url
            return {"ok": True, "status": status, "content_type": content_type,
                    "body": body, "bytes": len(body), "elapsed": time.time() - started,
                    "error": "", "url": final_url}
    except urllib.error.HTTPError as exc:
        try:
            exc.close()
        except Exception:  # noqa: BLE001
            pass
        return {"ok": False, "status": int(exc.code), "content_type": "", "body": b"",
                "bytes": 0, "elapsed": time.time() - started, "error": f"HTTP {exc.code}"}
    except Exception as exc:  # noqa: BLE001 - network classification happens below
        return {"ok": False, "status": 0, "content_type": "", "body": b"", "bytes": 0,
                "elapsed": time.time() - started, "error": _error_reason(exc), "exception": exc}


def _error_reason(exc: Exception) -> str:
    if isinstance(exc, socket.timeout) or isinstance(exc, TimeoutError):
        return "timeout"
    reason = getattr(exc, "reason", exc)
    if isinstance(reason, str):
        return reason[:120]
    name = type(reason).__name__
    if "NameResolution" in name or name == "gaierror":
        return "dns lookup failed"
    if name in ("ConnectionRefusedError", "ConnectionRefused"):
        return "connection refused"
    return name


def resolve_url(base: str, ref: str) -> str:
    return urllib.parse.urljoin(base, ref.strip())


# Answers that say "busy right now", not "gone": a rate limit, a gateway or
# server error, a request the server refused to read. 414 belongs here because
# it describes the URL this checker built, never the stream itself.
TRANSIENT_HTTP_CODES = frozenset({408, 414, 425, 429})


def sub_request_status(code: int, error: str) -> str:
    """Classify a failed variant-playlist or media-segment request.

    A variant or segment that answers 429 Too Many Requests, a 5xx or a timeout
    belongs to a host that was busy during the sweep - the playlist above it
    just answered - so the link is ``unreachable`` (kept and re-checked next
    run), exactly like the same answers on the playlist URL itself. Before
    this, a CDN rate-limiting the nightly check had working channels
    quarantined as "playlist only, HTTP 429", and the verifier then failed the
    run because those links were still published.

    Any other HTTP error stays ``offline``: a 404/410 means the media is gone,
    and a 401/403 on the media behind an open playlist is a refusal the app
    would get too, because it sends the same headers as this check.
    """
    if code in TRANSIENT_HTTP_CODES or code >= 500:
        return "unreachable"
    if code:
        return "offline"
    if error in ("dns lookup failed", "connection refused"):
        return "offline"
    return "unreachable"


def pick_variant(body_text: str, base_url: str) -> tuple[str, int]:
    """Choose the highest-bandwidth variant of an HLS master playlist."""
    lines = [line.strip() for line in body_text.splitlines() if line.strip()]
    best_url, best_bandwidth = "", -1
    for index, line in enumerate(lines):
        if not line.startswith("#EXT-X-STREAM-INF"):
            continue
        match = BANDWIDTH_RE.search(line)
        bandwidth = int(match.group(1)) if match else 0
        uri = ""
        for follow in lines[index + 1:]:
            if follow.startswith("#"):
                # A URI attribute on the EXT-X-STREAM-INF line itself.
                uri_match = re.search(r'URI="([^"]+)"', line)
                uri = uri_match.group(1) if uri_match else ""
                break
            uri = follow
            break
        if uri and bandwidth >= best_bandwidth:
            best_url, best_bandwidth = resolve_url(base_url, uri), bandwidth
    return best_url, max(best_bandwidth, 0)


def first_segment(body_text: str, base_url: str) -> str:
    """Newest media segment of an HLS media playlist.

    Live playlists list oldest-first, so the last entry is the newest segment and
    the only one guaranteed to still be inside the server's DVR window. Probing
    the first entry instead would mark healthy streams dead with a stale
    "No DVR" response.
    """
    segments = []
    for line in body_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        segments.append(resolve_url(base_url, line))
    return segments[-1] if segments else ""


def looks_like_media(body: bytes, content_type: str) -> tuple[bool, str]:
    """True when the payload is media rather than an error page."""
    head = body.lstrip()[:8]
    if body[:1] == b"\x47":
        return True, "mpeg-ts transport stream"
    if b"ftyp" in head:
        return True, "fmp4 fragment"
    if head.startswith(b"#EXTM3U") or head.startswith(b"#EXT"):
        return True, "hls playlist"
    if MPD_RE.search(body[:4096].decode("utf-8", "ignore")):
        return True, "dash manifest"
    if any(marker in content_type for marker in STREAM_MEDIA_TYPES):
        return True, content_type.split(";")[0].strip() or "media"
    if head.startswith(b"<") or "html" in content_type or "text/" in content_type:
        return False, "html/text page, not a stream"
    if not body:
        return False, "empty response"
    return bool(body), f"{len(body)} bytes of {content_type or 'unknown type'}"


def probe_segment(url: str, headers: dict, timeout: float) -> dict:
    result = fetch(url, headers, timeout, limit=SEGMENT_READ_BYTES, range_header=SEGMENT_RANGE)
    if not result["ok"]:
        return {"ok": False, "detail": result["error"], "bytes": 0,
                "status": sub_request_status(result["status"], result["error"])}
    body = result["body"]
    if len(body) >= 2 and body[:2] == b"\x1f\x8b":
        try:
            body = gzip.decompress(body)
        except (OSError, zlib.error):
            pass
    if not body:
        return {"ok": False, "detail": "empty segment", "bytes": 0}
    if len(body) < MIN_SEGMENT_BYTES and not (body[:1] == b"\x47" or b"ftyp" in body[:8]):
        return {"ok": False, "detail": f"segment too small ({len(body)} bytes)", "bytes": len(body)}
    return {"ok": True, "detail": f"segment ok ({len(body)} bytes)", "bytes": len(body)}


# --------------------------------------------------------------------------- #
# One link, start to finish
# --------------------------------------------------------------------------- #
def verify_link(channel: scraper.Channel, timeout: float, retries: int, deep: bool,
                host_limiter: scraper.HostLimiter | None = None) -> dict:
    """Classify a single stream URL. Returns a result dict (never raises)."""
    result = {
        "name": channel.name,
        "url": channel.url,
        "group": channel.group,
        "status": "unreachable",
        "reason": "",
        "http_status": 0,
        "content_type": "",
        "bytes": 0,
        "kind": "",
        "variant": "",
        "segment_ok": None,
        "elapsed": 0.0,
    }
    url = (channel.url or "").strip()
    if not url or any(ch.isspace() for ch in url):
        result.update(status="invalid", reason="empty or malformed URL")
        return result
    parsed = urllib.parse.urlsplit(url)
    scheme = parsed.scheme.lower()
    if scheme in NON_HTTP_SCHEMES:
        result.update(status="unsupported", reason=f"not probed: {scheme} scheme")
        return result
    if scheme not in ("http", "https") or not parsed.netloc:
        result.update(status="invalid", reason="not an http(s) URL")
        return result

    headers = channel.headers()
    attempts = max(0, retries) + 1
    last_error = ""
    for attempt in range(attempts):
        semaphore = host_limiter.semaphore_for(url) if host_limiter else None
        if semaphore:
            semaphore.acquire()
        try:
            response = fetch(url, headers, timeout)
        finally:
            if semaphore:
                semaphore.release()
        result["elapsed"] = round(response.get("elapsed", 0.0), 3)
        result["http_status"] = response["status"]
        result["content_type"] = response["content_type"]

        if not response["ok"]:
            error = response["error"]
            code = response["status"]
            if code in (401, 403, 451):
                result.update(status="blocked", reason=f"HTTP {code} (auth or geo-block)")
                return result
            if code in (404, 410):
                result.update(status="offline", reason=f"HTTP {code}")
                return result
            if code in (400, 402, 405, 406, 409, 415, 422) and code < 500:
                result.update(status="offline", reason=f"HTTP {code}")
                return result
            last_error = error
            if host_limiter:
                host_limiter.record_connection_failure(url)
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 4))
                continue
            reason = last_error or "no response"
            # A DNS failure or a refused port is a dead host, not a slow one.
            if reason in ("dns lookup failed", "connection refused"):
                result.update(status="offline", reason=reason)
            else:
                result.update(status="unreachable", reason=reason)
            return result

        if host_limiter:
            host_limiter.record_response(url)
        body = response["body"]
        result["bytes"] = response["bytes"]
        text = body.decode("utf-8", "ignore")
        base_url = response.get("url") or url

        if HLS_MASTER_RE.search(text):
            result["kind"] = "hls-master"
            if deep:
                variant, bandwidth = pick_variant(text, base_url)
                if variant:
                    result["variant"] = variant
                    variant_response = fetch(variant, headers, timeout)
                    if not variant_response["ok"]:
                        result.update(
                            status=sub_request_status(variant_response["status"],
                                                      variant_response["error"]),
                            reason=f"variant HTTP {variant_response['status'] or variant_response['error']}")
                        return result
                    text = variant_response["body"].decode("utf-8", "ignore")
                    base_url = variant_response.get("url") or variant
                    result["kind"] = f"hls-variant ({bandwidth // 1000} kbps)"
            if HLS_MEDIA_RE.search(text) or "#EXTINF" in text:
                segment = first_segment(text, base_url)
                if segment:
                    probe = probe_segment(segment, headers, timeout)
                    result["segment_ok"] = probe["ok"]
                    if not probe["ok"]:
                        # The playlist exists but the media behind it is gone:
                        # exactly the case a shallow check reports as "working".
                        # A busy segment host is not that case (see
                        # sub_request_status), so it stays "unreachable".
                        result.update(status=probe.get("status", "offline"),
                                      reason=f"playlist only, {probe['detail']}")
                        return result
                    result.update(status="working", reason=f"hls, {probe['detail']}")
                    return result
            result.update(status="working", reason="hls playlist")
            return result

        if HLS_MEDIA_RE.search(text) or (text.startswith("#EXTM3U") and "#EXTINF" in text):
            # A media playlist served directly (no master above it): the only way
            # to know it is alive is to pull a segment.
            result["kind"] = "hls-media"
            segment = first_segment(text, base_url)
            if not segment:
                result.update(status="offline", reason="playlist lists no segments")
                return result
            if deep:
                probe = probe_segment(segment, headers, timeout)
                result["segment_ok"] = probe["ok"]
                if not probe["ok"]:
                    result.update(status=probe.get("status", "offline"),
                                  reason=f"playlist only, {probe['detail']}")
                    return result
                result.update(status="working", reason=f"hls, {probe['detail']}")
                return result
            result.update(status="working", reason="hls playlist")
            return result

        if MPD_RE.search(text):
            result["kind"] = "dash"
            if not REPRESENTATION_RE.search(text):
                result.update(status="offline", reason="dash manifest has no representations")
                return result
            result.update(status="working", reason="dash manifest")
            return result

        media, detail = looks_like_media(body, response["content_type"])
        result["kind"] = detail
        if media:
            result.update(status="working", reason=detail)
        elif not body:
            result.update(status="offline", reason="empty response")
        elif detail.startswith("html") or "html" in response["content_type"]:
            result.update(status="offline", reason="html page, not a stream")
        else:
            result.update(status="offline", reason=detail)
        return result

    result.update(status="unreachable", reason=last_error or "check attempts exhausted")
    return result


# --------------------------------------------------------------------------- #
# Playlist-level runs
# --------------------------------------------------------------------------- #
def collect_targets(out_dir: Path, extra: list, all_playlists: bool,
                    countries: bool, archives: bool = False,
                    shelf_dir: Path | None = None) -> list:
    targets: list = []
    if all_playlists:
        for name in ("PremiumTV.m3u", "AE_Channels.m3u"):
            path = out_dir / name
            if path.exists():
                targets.append(path)
        countries = True
    if archives:
        targets.extend(archive_targets(out_dir, shelf_dir))
    for item in extra:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / path
        if path.exists():
            targets.append(path)
        else:
            log(f"[check] skipping missing playlist: {path}")
    if countries:
        targets.extend(sorted((out_dir / "countries").glob("*.m3u")))
    # Keep order, drop duplicates.
    seen = set()
    ordered = []
    for path in targets:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        ordered.append(path)
    return ordered


def archive_targets(out_dir: Path, shelf_dir: Path | None = None) -> list:
    """Every playlist a player can be pointed at that the daily runs never patch.

    The nightly deep check covers the player playlists (the main one, A&E and the
    country files); the quick daily updates repair the main and priority playlists
    with a shallow check. That leaves three sets of files nobody ever walks end to
    end: the per-category playlists and the ``categories/`` shelf (which a player
    is pointed at in the README), the local copies of the upstream sources that a
    scrape falls back to when an index is down, and the archive of every link ever
    found. A channel that died in one of those stays there until a viewer hits a
    black screen - so the biweekly sweep checks them too.
    """
    paths: list = []
    for name in ("Priority_Channels.m3u", "PremiumTV_all.m3u"):
        path = out_dir / name
        if path.exists():
            paths.append(path)
    for pattern in ("categories/*.m3u", "sources/*.m3u"):
        paths.extend(sorted((out_dir / Path(pattern).parent).glob(Path(pattern).name)))
    # The published category shelf lives at the repository root, next to playlists/.
    shelf = Path(shelf_dir) if shelf_dir else ROOT / "categories"
    for pattern in ("*.m3u", "*/*.m3u"):
        paths.extend(sorted(shelf.glob(pattern)))
    return [path for path in paths if path.is_file()]


def is_report_only(path: Path) -> bool:
    """A checked-but-never-rewritten archive: it exists to hold every link found.

    ``playlists/PremiumTV_all.m3u`` is documented as "all unique links found,
    including dead or unverified links", so pruning it would break the file's
    purpose. It is still worth checking - a dead link confirmed here is added to
    the quarantine, which is what keeps it out of the published playlists - but
    the file itself keeps its contents.
    """
    return path.name == "PremiumTV_all.m3u"


def load_playlists(paths: list) -> dict:
    """Return {path: (header_lines, blocks, channels)} for every target."""
    loaded = {}
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        header, blocks = split_blocks(text)
        channels = [channel_from_block(block, path.name) for block in blocks]
        loaded[path] = {"header": header, "blocks": blocks, "channels": channels}
    return loaded


def run_checks(loaded: dict, workers: int, per_host_workers: int, timeout: float,
               retries: int, deep: bool) -> tuple[dict, dict]:
    """Check every unique URL once; return (url -> result, playlist -> stats)."""
    unique: dict = {}
    for _path, data in loaded.items():
        for channel in data["channels"]:
            url = channel.url
            if url and url not in unique:
                unique[url] = channel

    log(f"[check] {len(loaded)} playlists | {sum(len(d['channels']) for d in loaded.values())} "
        f"entries | {len(unique)} unique links | deep={deep}")
    host_limiter = scraper.HostLimiter(per_host_workers)
    results: dict = {}
    started = time.time()
    done = 0
    total = len(unique)
    with cf.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {
            pool.submit(verify_link, channel, timeout, retries, deep, host_limiter): url
            for url, channel in unique.items()
        }
        for future in cf.as_completed(futures):
            url = futures[future]
            try:
                results[url] = future.result()
            except Exception as exc:  # noqa: BLE001 - never lose the whole run
                results[url] = {"name": unique[url].name, "url": url, "group": unique[url].group,
                                "status": "unreachable",
                                "reason": f"checker error: {type(exc).__name__}",
                                "http_status": 0, "content_type": "", "bytes": 0,
                                "kind": "", "variant": "", "segment_ok": None, "elapsed": 0.0}
            done += 1
            if done % 500 == 0 or done == total:
                elapsed = time.time() - started
                log(f"[check] {done}/{total} links ({elapsed:.0f}s, "
                    f"{done / max(elapsed, 0.1):.1f} links/s)")
    return results, {}


def summarize(loaded: dict, results: dict) -> dict:
    per_playlist = {}
    totals = {"working": 0, "offline": 0, "unreachable": 0, "blocked": 0,
              "unsupported": 0, "invalid": 0, "unchecked": 0}
    host_failures: dict = {}
    for path, data in loaded.items():
        counts = dict.fromkeys(totals, 0)
        dead = []
        for channel in data["channels"]:
            result = results.get(channel.url or "", {})
            status = result.get("status", "unchecked")
            counts[status] = counts.get(status, 0) + 1
            totals[status] = totals.get(status, 0) + 1
            if status in DEAD_STATUSES:
                dead.append(result)
            if status in ("offline", "unreachable"):
                host = urllib.parse.urlsplit(channel.url or "").netloc.lower()
                if host:
                    bucket = host_failures.setdefault(host, {"offline": 0, "unreachable": 0})
                    bucket[status] += 1
        per_playlist[str(path)] = {
            "file": str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT)) else str(path),
            "entries": len(data["channels"]),
            "counts": counts,
            "dead": dead[:200],
        }
    return {"per_playlist": per_playlist, "totals": totals,
            "host_failures": dict(sorted(host_failures.items(),
                                         key=lambda item: -(item[1]["offline"] + item[1]["unreachable"]))[:40])}


def patch_playlists(loaded: dict, results: dict, min_working_ratio: float,
                    max_remove_ratio: float, dry_run: bool,
                    report_only: set | None = None) -> dict:
    """Remove confirmed-dead entries in place, with per-playlist safety limits."""
    patch_report = {"patched_files": [], "skipped_files": [], "removed_total": 0,
                    "removed": [], "aborted": False, "abort_reason": "",
                    "reported_only": []}
    report_only = report_only or set()

    checked = 0
    working = 0
    for data in loaded.values():
        for channel in data["channels"]:
            status = results.get(channel.url or "", {}).get("status", "unchecked")
            if status != "unsupported":
                checked += 1
            if status == "working":
                working += 1
    ratio = working / checked if checked else 0.0
    patch_report["working_ratio"] = round(ratio, 4)
    if checked and ratio < min_working_ratio:
        patch_report["aborted"] = True
        patch_report["abort_reason"] = (
            f"only {working}/{checked} links working ({ratio:.1%}) is below "
            f"--min-working-ratio {min_working_ratio:.0%}; treating this run as a "
            f"network problem and patching nothing"
        )
        log(f"[patch] ABORTED: {patch_report['abort_reason']}")
        return patch_report

    for path, data in loaded.items():
        entries = len(data["blocks"])
        if path in report_only:
            # Checked (and its dead links feed the quarantine), but never rewritten:
            # see is_report_only().
            dead_here = sum(1 for block in data["blocks"]
                            if results.get(block.url or "", {}).get("status")
                            in DEAD_STATUSES)
            patch_report["reported_only"].append({
                "file": str(path), "entries": entries, "dead": dead_here,
                "reason": "every link found stays in this archive, dead ones "
                          "included; the quarantine is what keeps them out of the "
                          "player playlists"})
            log(f"[patch] {path.name}: reported {dead_here} dead of {entries}, "
                f"file left complete (documented archive)")
            continue
        kept, removed = [], []
        for block in data["blocks"]:
            status = results.get(block.url or "", {}).get("status", "unchecked")
            if status in DEAD_STATUSES:
                removed.append({"name": block.name, "url": block.url,
                                "status": status,
                                "reason": results.get(block.url, {}).get("reason", ""),
                                "file": path.name})
            else:
                kept.append(block)
        if not removed:
            continue
        remove_ratio = len(removed) / entries if entries else 0.0
        if remove_ratio > max_remove_ratio:
            patch_report["skipped_files"].append({
                "file": str(path), "entries": entries, "would_remove": len(removed),
                "ratio": round(remove_ratio, 4),
                "reason": f"removing {len(removed)}/{entries} entries exceeds "
                          f"--max-remove-ratio {max_remove_ratio:.0%}"})
            log(f"[patch] skipped {path.name}: would remove {len(removed)}/{entries} "
                f"({remove_ratio:.0%}) - over the safety limit")
            continue
        # Re-sort the survivors into the canonical category order and make sure
        # every group title is one of the fixed categories, so a patched file
        # matches what the next scrape would publish.
        kept, regrouped = tidy_blocks(kept, path.name)
        if not dry_run:
            path.write_text(blocks_to_text(data["header"], kept), encoding="utf-8")
        patch_report["regrouped"] = patch_report.get("regrouped", 0) + regrouped
        patch_report["removed_total"] += len(removed)
        patch_report["removed"].extend(removed)
        patch_report["patched_files"].append({
            "file": str(path), "entries_before": entries, "entries_after": len(kept),
            "removed": len(removed), "ratio": round(remove_ratio, 4)})
        log(f"[patch] {path.name}: removed {len(removed)} dead of {entries} "
            f"({len(kept)} remain)")
    return patch_report


# --------------------------------------------------------------------------- #
# Reports
# --------------------------------------------------------------------------- #
def write_reports(out_dir: Path, report: dict, suffix: str = "") -> list:
    """Write ``checks/link-check{suffix}.json`` and ``checks/LINK-CHECK{SUFFIX}.md``.

    A separate suffix lets a second sweep (the biweekly archive pass) report on the
    playlists the nightly one skips without overwriting the ``link-check.json`` the
    re-sort and the guide build read back.
    """
    checks_dir = out_dir / "checks"
    checks_dir.mkdir(parents=True, exist_ok=True)
    (checks_dir / f"link-check{suffix}.json").write_text(
        json.dumps(report, indent=2, sort_keys=False), encoding="utf-8")

    totals = report["totals"]
    lines = [
        "# Deep link check" + (" - archives and category shelf" if suffix else ""),
        "",
        f"- **Run:** {report['label']} (`{report['run_id']}`)",
        f"- **Started:** {report['started_utc']}  |  **Finished:** {report['finished_utc']}"
        f"  |  **Duration:** {report['duration_seconds']}s",
        f"- **Mode:** {'deep (playlist + segment probe)' if report['deep'] else 'shallow (headers only)'}",
        f"- **Unique links checked:** {report['unique_links']} from "
        f"{report['entry_count']} playlist entries in {report['playlist_count']} playlists",
        "",
        "| Result | Links | Share | Meaning |",
        "|---|---:|---:|---|",
    ]
    meaning = {
        "working": "answered with playable media",
        "offline": "confirmed dead - removed when patching",
        "unreachable": "timeout or server error - kept, may recover",
        "blocked": "HTTP 401/403/451 - needs auth or is geo-blocked",
        "unsupported": "non-HTTP scheme, cannot be probed",
        "invalid": "malformed or non-http URL",
        "unchecked": "not checked this run",
    }
    total_links = max(1, sum(totals.values()))
    for status in ("working", "offline", "unreachable", "blocked", "unsupported",
                   "invalid", "unchecked"):
        if totals.get(status):
            lines.append(f"| {status} | {totals[status]} | {totals[status] / total_links:.1%} "
                         f"| {meaning[status]} |")
    lines += ["", "## Per playlist", "",
              "| Playlist | Entries | Working | Offline | Unreachable | Blocked | Other |",
              "|---|---:|---:|---:|---:|---:|---:|"]
    for info in report["per_playlist"].values():
        counts = info["counts"]
        other = (counts.get("unsupported", 0) + counts.get("invalid", 0)
                 + counts.get("unchecked", 0))
        lines.append(
            f"| `{info['file']}` | {info['entries']} | {counts.get('working', 0)} | "
            f"{counts.get('offline', 0)} | {counts.get('unreachable', 0)} | "
            f"{counts.get('blocked', 0)} | {other} |")
    if report.get("patch"):
        patch = report["patch"]
        lines += ["", "## Patches applied", ""]
        if patch.get("aborted"):
            lines.append(f"- **Patching aborted:** {patch['abort_reason']}")
        else:
            lines.append(f"- Removed **{patch['removed_total']}** confirmed-dead links "
                         f"across **{len(patch['patched_files'])}** playlists "
                         f"(working ratio {patch.get('working_ratio', 0):.1%}).")
            for info in patch["patched_files"]:
                lines.append(f"  - `{Path(info['file']).name}`: -{info['removed']} "
                             f"({info['entries_before']} -> {info['entries_after']})")
            for info in patch["skipped_files"]:
                lines.append(f"  - skipped `{Path(info['file']).name}`: {info['reason']}")
            for info in patch.get("reported_only", []):
                lines.append(f"  - reported only `{Path(info['file']).name}`: "
                             f"{info['dead']} of {info['entries']} links are dead; the file "
                             f"keeps every one of them by design")
    if report["host_failures"]:
        lines += ["", "## Hosts with the most failing links", "",
                  "| Host | Offline | Unreachable |", "|---|---:|---:|"]
        for host, counts in list(report["host_failures"].items())[:25]:
            lines.append(f"| `{host}` | {counts['offline']} | {counts['unreachable']} |")
    dead_sample = []
    for info in report["per_playlist"].values():
        for item in info.get("dead", [])[:5]:
            dead_sample.append(item)
        if len(dead_sample) >= 25:
            break
    if dead_sample:
        lines += ["", "## Sample of confirmed-dead links", "",
                  "| Channel | Reason | URL |", "|---|---|---|"]
        for item in dead_sample[:25]:
            url = scraper.safe_url(item.get("url", ""))
            lines.append(f"| {item.get('name', '')[:60]} | {item.get('reason', '')} | `{url}` |")
    lines.append("")
    (checks_dir / f"LINK-CHECK{suffix.upper()}.md").write_text("\n".join(lines),
                                                                encoding="utf-8")
    return [checks_dir / f"link-check{suffix}.json",
            checks_dir / f"LINK-CHECK{suffix.upper()}.md"]


QUARANTINE_REASON_PREFIXES = ("playlist only, ", "variant HTTP ", "variant ", "HTTP ")
# Version of the rules a quarantine entry was recorded under. Version 2 is the
# first that resolved a redirected master playlist's variants against the URL
# that served it; a variant failure recorded before that (jmp2.uk and the
# mjh.nz redirectors produced ~1,700 "variant HTTP 414/404" entries on
# 2026-10-13) says nothing about the stream and is not carried forward.
QUARANTINE_RULES = 2


def quarantine_reason_is_conclusive(reason: str) -> bool:
    """Whether a recorded quarantine reason still proves a link dead today.

    Entries written before the variant/segment rules matched the playlist-URL
    rules (see ``sub_request_status``) can hold reasons such as "playlist only,
    HTTP 429", "variant HTTP 503" or "variant HTTP 414" (the last one came from
    resolving a redirected master playlist's variants against the wrong URL).
    None of those is evidence that a channel died, so they are not kept.
    """
    text = (reason or "").strip()
    for prefix in QUARANTINE_REASON_PREFIXES:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    if text.isdigit():
        return sub_request_status(int(text), "") == "offline"
    if text.startswith("HTTP ") and text[5:].isdigit():
        return sub_request_status(int(text[5:]), "") == "offline"
    if text in ("dns lookup failed", "connection refused"):
        return True
    transient_words = ("timeout", "timed out", "timeouterror", "remotedisconnected",
                       "connectionreset", "connectionaborted", "incompleteread",
                       "ssl", "checker error")
    if any(word in text.lower() for word in transient_words):
        return False
    return True


def update_quarantine(out_dir: Path, report: dict, patch: dict, days: float,
                      results: dict | None = None) -> Path:
    """Remember the links that answered but served no media.

    The daily scrape re-imports everything the indexes list, so without this a
    link that only fails the deep check would be published again a few hours
    later. `scraper.py` reads this file and holds those links back for `days`.

    A link this run re-checked and did not find dead (working, blocked or merely
    unreachable) leaves the quarantine, and so does an entry whose recorded
    reason the current rules no longer count as dead: the quarantine only ever
    holds links the last deep check could prove were gone.
    """
    checks_dir = out_dir / "checks"
    checks_dir.mkdir(parents=True, exist_ok=True)
    path = checks_dir / "quarantine.json"
    entries: dict = {}
    if path.exists():
        try:
            entries = (json.loads(path.read_text(encoding="utf-8")) or {}).get("entries") or {}
        except (OSError, ValueError):
            entries = {}
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=max(days, 0))
    rechecked = results or {}
    pruned = {}
    for url, entry in entries.items():
        if not isinstance(entry, dict):
            continue
        reason = str(entry.get("reason") or "")
        if not quarantine_reason_is_conclusive(reason):
            continue
        try:
            rules = int(entry.get("rules") or 1)
        except (TypeError, ValueError):
            rules = 1
        if rules < QUARANTINE_RULES and reason.startswith("variant "):
            continue
        status = (rechecked.get(url) or {}).get("status")
        if status and status not in ("offline", "invalid"):
            continue
        last_seen = scraper.parse_utc_iso(str(entry.get("last_seen_utc") or ""))
        if last_seen is None or last_seen.replace(tzinfo=None) >= cutoff.replace(tzinfo=None):
            pruned[url] = entry
    entries = pruned
    for item in patch.get("removed", []):
        url = item.get("url") or ""
        if not url:
            continue
        existing = entries.get(url) or {}
        entries[url] = {
            "name": item.get("name") or existing.get("name") or "",
            "first_seen_utc": existing.get("first_seen_utc") or report["finished_utc"],
            "last_seen_utc": report["finished_utc"],
            "reason": item.get("reason") or existing.get("reason") or "served no media",
            "status": item.get("status") or "offline",
            "hits": int(existing.get("hits") or 0) + 1,
            "rules": QUARANTINE_RULES,
        }
    path.write_text(json.dumps({
        "updated_utc": report["finished_utc"],
        "expires_after_days": days,
        "count": len(entries),
        "entries": entries,
    }, indent=2), encoding="utf-8")
    return path


def append_edit_log(out_dir: Path, report: dict, patch: dict) -> Path:
    logs_dir = out_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / "link-check-edits.txt"
    lines = [f"## {report['finished_utc']} - {report['label']} "
             f"(deep link check, run {report['run_id']})"]
    if patch.get("aborted"):
        lines.append(f"  ! patch aborted: {patch['abort_reason']}")
    for info in patch.get("patched_files", []):
        lines.append(f"  # {Path(info['file']).name}: -{info['removed']} "
                     f"({info['entries_before']} -> {info['entries_after']})")
    for item in patch.get("removed", [])[:2000]:
        lines.append(f"  -removed {item['name'][:80]} [{item['status']}: {item['reason']}] "
                     f"{scraper.safe_url(item['url'])}")
    for info in patch.get("skipped_files", []):
        lines.append(f"  ! skipped {Path(info['file']).name}: {info['reason']}")
    for info in patch.get("reported_only", []):
        lines.append(f"  ~ reported {Path(info['file']).name}: {info['dead']} dead of "
                     f"{info['entries']} entries, none removed (archive by design)")
    lines.append("")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return path


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "playlists"),
                    help="playlists directory (reports go to <out>/checks)")
    ap.add_argument("--playlist", action="append", default=[],
                    help="playlist file to check (repeatable)")
    ap.add_argument("--all", action="store_true",
                    help="check PremiumTV.m3u, AE_Channels.m3u and every country playlist")
    ap.add_argument("--countries", action="store_true",
                    help="include playlists/countries/*.m3u")
    ap.add_argument("--archives", action="store_true",
                    help="also check the playlists no daily run patches: the priority "
                         "playlist, the per-category playlists, the categories/ shelf "
                         "and the local source copies (PremiumTV_all.m3u is checked but "
                         "never pruned - see is_report_only)")
    ap.add_argument("--workers", type=int, default=96, help="maximum concurrent checks")
    ap.add_argument("--per-host-workers", type=int, default=8,
                    help="maximum concurrent checks per host")
    ap.add_argument("--timeout", type=float, default=8.0, help="per-request timeout")
    ap.add_argument("--retries", type=int, default=1, help="retries for transient failures")
    ap.add_argument("--deep", dest="deep", action="store_true", default=True,
                    help="resolve HLS variants and probe a media segment (default)")
    ap.add_argument("--no-deep", dest="deep", action="store_false",
                    help="skip HLS variant/segment probing (fast mode)")
    ap.add_argument("--patch", action="store_true",
                    help="remove confirmed-dead links from the checked playlists")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --patch: report what would be removed, change nothing")
    ap.add_argument("--min-working-ratio", type=float, default=DEFAULT_MIN_WORKING_RATIO,
                    help="abort patching when fewer than this share of links work")
    ap.add_argument("--max-remove-ratio", type=float, default=DEFAULT_MAX_REMOVE_RATIO,
                    help="skip patching a playlist that would lose more than this share")
    ap.add_argument("--quarantine-days", type=float, default=7.0,
                    help="with --patch: remember dead links for this many days so the "
                         "daily scrape cannot publish them again (0 disables)")
    ap.add_argument("--label", default="deep link check", help="run label for the reports")
    ap.add_argument("--report-suffix", default="",
                    help="write checks/link-check<SUFFIX>.json and "
                         "checks/LINK-CHECK<SUFFIX>.md instead of the nightly reports")
    ap.add_argument("--categories-dir", default="",
                    help="directory holding the published categories/ shelf that "
                         "--archives sweeps (default: categories/ in the repository)")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    if args.workers < 1 or args.per_host_workers < 1 or args.timeout <= 0:
        log("[check] workers and timeout must be positive")
        return 2
    out_dir = Path(args.out)
    targets = collect_targets(out_dir, args.playlist, args.all, args.countries,
                              args.archives, Path(args.categories_dir)
                              if args.categories_dir else None)
    if not targets:
        log("[check] no playlists to check - pass --all, --archives or --playlist <file>")
        return 2
    started = dt.datetime.now(dt.timezone.utc)
    loaded = load_playlists(targets)
    results, _ = run_checks(loaded, args.workers, args.per_host_workers, args.timeout,
                            args.retries, args.deep)
    summary = summarize(loaded, results)
    finished = dt.datetime.now(dt.timezone.utc)
    report = {
        "run_id": f"{started.strftime('%Y%m%dT%H%M%S')}Z-{os.getpid()}",
        "label": args.label,
        "started_utc": started.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "finished_utc": finished.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "duration_seconds": round((finished - started).total_seconds(), 1),
        "deep": args.deep,
        "playlist_count": len(loaded),
        "entry_count": sum(len(data["channels"]) for data in loaded.values()),
        "unique_links": len({channel.url for data in loaded.values()
                             for channel in data["channels"] if channel.url}),
        "workers": args.workers,
        "timeout": args.timeout,
        "retries": args.retries,
        **summary,
    }
    if args.patch:
        report["patch"] = patch_playlists(
            loaded, results, args.min_working_ratio, args.max_remove_ratio,
            args.dry_run, report_only={path for path in targets if is_report_only(path)})
        if not args.dry_run:
            quarantine = update_quarantine(out_dir, report, report["patch"],
                                           args.quarantine_days, results)
            report["patch"]["quarantine"] = {
                "file": display_path(quarantine),
                "count": (json.loads(quarantine.read_text(encoding="utf-8")) or {})
                         .get("count", 0) if quarantine.exists() else 0,
                "days": args.quarantine_days,
            }
            report["patch"]["edit_log"] = str(
                display_path(append_edit_log(out_dir, report, report["patch"])))
    written = write_reports(out_dir, report, args.report_suffix)
    totals = report["totals"]
    log(f"[check] done in {report['duration_seconds']}s: "
        f"working={totals.get('working', 0)} offline={totals.get('offline', 0)} "
        f"unreachable={totals.get('unreachable', 0)} blocked={totals.get('blocked', 0)}")
    for path in written:
        log(f"[check] wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
