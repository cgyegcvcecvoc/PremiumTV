#!/usr/bin/env python3
"""
TV guide (EPG) verifier for the published playlists.

Every playlist advertises its guides in the first line:

    #EXTM3U x-tvg-url="https://a/guide.xml.gz,https://b/guide.xml.gz,..."

Players download all of them on every refresh, so a single dead or malformed
guide slows the whole guide load down (and some players stop at the first
failure). This script checks each guide the same way a player would - fetch it,
decompress it if it is gzipped, and confirm it is a real XMLTV document with
channels and programmes in it - then reports what is good and optionally rewrites
the header so only working guides are advertised.

Status per guide:

| status        | meaning                                                    | kept? |
|---|---|---|
| `ok`          | reachable, valid XMLTV, has channels and programmes         | yes   |
| `empty`       | valid XMLTV but no programmes in the sampled window         | yes   |
| `unreachable` | timeout / 5xx / connection error - may come back            | yes   |
| `blocked`     | 401 / 403 - needs auth                                      | yes   |
| `offline`     | 404 / 410 / DNS failure - the guide is gone                 | **no** |
| `invalid`     | answered, but not XMLTV (HTML error page, JSON, stub file)  | **no** |

Only `offline` and `invalid` guides are dropped, and only with ``--patch``.
``--min-working-ratio`` (default 0.25) aborts patching when the whole run looks
like a network outage rather than a genuinely dead guide.

Guides this repository publishes for its own players - ``EPG/PremiumTV.xml`` and
one ``EPG/<Country>.xml`` per country, written by ``scripts/epg_build.py`` - are
reported with an ``own_repo`` flag: their status is still recorded, but they are
left out of the working share (so a private repository, where every raw URL 404s,
can no longer look like an outage) and they are never dropped from a header.

Outputs:

    checks/epg-check.json      full machine-readable result
    checks/EPG-CHECK.md        human-readable guide report
    logs/epg-check-edits.txt   append-only log of every guide added/removed

    python scripts/epg_check.py --all                 # report only
    python scripts/epg_check.py --all --patch         # drop dead guides
    python scripts/epg_check.py --playlist playlists/PremiumTV.m3u --add https://host/guide.xml.gz
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import gzip
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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scraper  # noqa: E402  (reuses the shared HTTP/TLS helpers)
import epg_sources  # noqa: E402  (the curated per-country guide list)

ROOT = Path(__file__).resolve().parent.parent

# Guides are huge (some are 100 MB+), so only the first slice is inspected.
SAMPLE_BYTES = 4 * 1024 * 1024
RANGE_HEADER = f"bytes=0-{SAMPLE_BYTES - 1}"
CHANNEL_RE = re.compile(rb"<channel\b", re.IGNORECASE)
PROGRAMME_RE = re.compile(rb"<programme\b", re.IGNORECASE)
TV_ROOT_RE = re.compile(rb"<tv\b", re.IGNORECASE)
DISPLAY_NAME_RE = re.compile(rb"<display-name[^>]*>(.*?)</display-name>",
                             re.IGNORECASE | re.DOTALL)
STOP_RE = re.compile(rb'stop="(\d{14})')
MIN_WORKING_RATIO = 0.25
DEFAULT_TIMEOUT = 45.0
# Statuses that are confirmed dead and dropped by --patch.
DEAD_STATUSES = {"offline", "invalid"}
# This repository publishes its own merged guide (scripts/epg_build.py) and points
# every player playlist at it. Those URLs are not upstream guides, and the
# verifier must never judge them as if they were: while the repository is private
# (or a push has not landed yet) raw.githubusercontent.com answers 404 for every
# one of them, which is a fact about repository visibility, not about a guide a
# player can no longer download. Counting them made a healthy run look like an
# outage - 173 self-hosted 404s out of 175 guides drove the working share to 1%,
# which tripped the --min-working-ratio guard on every nightly run and disabled
# guide patching altogether.
OWN_REPO = (os.environ.get("GITHUB_REPOSITORY") or "cgyegcvcecvoc/PremiumTV1").strip("/")
# The repository was renamed (PremiumTV1 -> PremiumTV) on 2026-10-21 while
# published playlists already advertised guide URLs under the old slug. Every
# slug the repository has ever published under identifies our own guides -
# matching only the current slug would make the pipeline treat its own
# published (still redirecting) guides as foreign upstreams and re-ingest
# them.
LEGACY_REPO_SLUGS = ("cgyegcvcecvoc/PremiumTV1", "cgyegcvcecvoc/PremiumTV")


def self_repo_slugs(*extra: str) -> tuple:
    """Every owner/repo slug that identifies this repository, past and present."""
    slugs = []
    for slug in (OWN_REPO, *extra, *LEGACY_REPO_SLUGS):
        slug = str(slug or "").strip().strip("/")
        if slug and slug not in slugs:
            slugs.append(slug)
    return tuple(slugs)


def log(msg: str) -> None:
    print(msg, flush=True)


def own_guide_prefixes() -> tuple:
    """URL prefixes of the guide files this repository publishes for its players."""
    prefixes = []
    for repo in self_repo_slugs():
        prefixes.append(f"https://raw.githubusercontent.com/{repo}/")
        prefixes.append(f"https://raw.githubusercontent.com/{repo.lower()}/")
        owner, _, name = repo.partition("/")
        if owner and name:
            prefixes.append(f"https://{owner.lower()}.github.io/{name}/")
    return tuple(prefixes)


def is_own_guide(url: str) -> bool:
    """True when the guide is an EPG file this repository generated itself."""
    text = str(url or "").strip()
    if not text.startswith(own_guide_prefixes()):
        return False
    path = urllib.parse.urlsplit(text).path
    # Only the generated guides: this repository also hosts its own source
    # playlists (playlists/*.m3u) under the same prefix, and those are ordinary
    # inputs, never advertised as guides.
    return "/EPG/" in path or "/playlists/epg/" in path


def display_path(path) -> str:
    """Repo-relative path for reports; absolute when the path lives elsewhere."""
    try:
        return str(Path(path).relative_to(ROOT))
    except ValueError:
        return str(path)


# --------------------------------------------------------------------------- #
# Header handling
# --------------------------------------------------------------------------- #
def extract_guides(path: Path) -> list:
    """Every guide URL in a playlist's #EXTM3U header line."""
    guides: list = []
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped.startswith("#EXTM3U"):
                for key, value in scraper.ATTR_RE.findall(stripped):
                    if key in ("url-tvg", "x-tvg-url") and value:
                        guides.extend(url.strip() for url in value.split(",") if url.strip())
                continue
            if stripped and not stripped.startswith("#"):
                break
    return list(dict.fromkeys(guides))


def rewrite_header(path: Path, guides: list) -> bool:
    """Replace the guide list in a playlist's #EXTM3U line. True when changed."""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    for index, line in enumerate(lines):
        if not line.strip().startswith("#EXTM3U"):
            continue
        attrs = scraper.ATTR_RE.findall(line)
        kept = [(key, value) for key, value in attrs
                if key not in ("url-tvg", "x-tvg-url")]
        new_line = "#EXTM3U"
        if kept:
            new_line += " " + " ".join(f'{key}="{value}"' for key, value in kept)
        if guides:
            new_line += f' x-tvg-url="{",".join(guides)}"'
        if new_line == line:
            return False
        lines[index] = new_line
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return True
    return False


# --------------------------------------------------------------------------- #
# Guide verification
# --------------------------------------------------------------------------- #
def decompress(body: bytes) -> bytes:
    if body[:2] == b"\x1f\x8b":
        try:
            return gzip.decompress(body)
        except (OSError, zlib.error, EOFError):
            # A truncated gzip (Range request) still decompresses incrementally.
            try:
                return zlib.decompressobj(16 + zlib.MAX_WBITS).decompress(body)
            except zlib.error:
                return body
    return body


def parse_xmltv(body: bytes) -> dict:
    head = body[:SAMPLE_BYTES]
    channels = len(CHANNEL_RE.findall(head))
    programmes = len(PROGRAMME_RE.findall(head))
    names = DISPLAY_NAME_RE.findall(head)
    stops = [int(match) for match in STOP_RE.findall(head)]
    newest = ""
    if stops:
        try:
            newest = dt.datetime.strptime(str(max(stops)), "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M UTC")
        except ValueError:
            newest = ""
    sample_name = ""
    for name in names[:5]:
        text = name.decode("utf-8", "ignore").strip()
        if text:
            sample_name = text
            break
    return {"channels": channels, "programmes": programmes, "sample_channel": sample_name,
            "newest_programme": newest}


def verify_guide(url: str, timeout: float, retries: int = 1) -> dict:
    result = {"url": url, "status": "unreachable", "reason": "", "http_status": 0,
              "bytes": 0, "channels": 0, "programmes": 0, "sample_channel": "",
              "newest_programme": "", "gzipped": False, "elapsed": 0.0,
              "own_repo": is_own_guide(url)}
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme.lower() not in ("http", "https") or not parsed.netloc:
        result.update(status="invalid", reason="not an http(s) URL")
        return result

    headers = {"User-Agent": scraper.DEFAULT_UA, "Accept": "*/*", "Range": RANGE_HEADER}
    attempts = max(0, retries) + 1
    for attempt in range(attempts):
        started = time.time()
        request = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout,
                                        context=scraper.INSECURE_CTX) as response:
                status = int(getattr(response, "status", 0) or response.getcode() or 0)
                content_type = (response.headers.get("Content-Type") or "").lower()
                try:
                    body = response.read(SAMPLE_BYTES)
                except Exception:  # noqa: BLE001 - truncated reads are still usable
                    body = b""
                result["elapsed"] = round(time.time() - started, 2)
                result["http_status"] = status
                result["bytes"] = len(body) if body else 0
                if not body:
                    result.update(status="invalid", reason="empty response")
                    return result
                gzipped = body[:2] == b"\x1f\x8b"
                result["gzipped"] = gzipped
                plain = decompress(body)
                if b"<tv" not in plain[:65536] and not TV_ROOT_RE.search(plain[:65536]):
                    snippet = plain[:80].decode("utf-8", "ignore").replace("\n", " ").strip()
                    if "html" in content_type or plain[:16].lstrip().startswith(b"<!"):
                        result.update(status="invalid", reason=f"not XMLTV: {snippet[:60]}")
                    elif snippet.startswith("{"):
                        result.update(status="invalid", reason="not XMLTV: JSON response")
                    else:
                        result.update(status="invalid", reason=f"not XMLTV: {snippet[:60]}")
                    return result
                info = parse_xmltv(plain)
                result.update(**info)
                if info["programmes"]:
                    result.update(status="ok",
                                  reason=f"{info['channels']} channels, "
                                         f"{info['programmes']} programmes sampled")
                else:
                    result.update(status="empty",
                                  reason="valid XMLTV but no programmes in the sampled window")
                return result
        except urllib.error.HTTPError as exc:
            code = int(exc.code)
            try:
                exc.close()
            except Exception:  # noqa: BLE001
                pass
            result["http_status"] = code
            if code in (401, 403, 451):
                result.update(status="blocked", reason=f"HTTP {code}")
                return result
            if code in (404, 410):
                result.update(status="offline", reason=f"HTTP {code}")
                return result
            if code >= 500 and attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 4))
                continue
            result.update(status="unreachable" if code >= 500 else "offline",
                          reason=f"HTTP {code}")
            return result
        except (socket.timeout, TimeoutError):
            if attempt + 1 < attempts:
                time.sleep(1)
                continue
            result.update(status="unreachable", reason="timeout")
            return result
        except Exception as exc:  # noqa: BLE001
            reason = getattr(exc, "reason", exc)
            if isinstance(reason, str):
                reason = reason[:120]
            else:
                reason = type(reason).__name__
            if "NameResolution" in reason or reason == "gaierror":
                result.update(status="offline", reason="dns lookup failed")
                return result
            if "ConnectionRefused" in reason:
                result.update(status="offline", reason="connection refused")
                return result
            result.update(status="unreachable", reason=reason)
            return result
    return result


# --------------------------------------------------------------------------- #
# Run
# --------------------------------------------------------------------------- #
def collect_targets(out_dir: Path, extra: list, all_playlists: bool,
                    countries: bool) -> list:
    targets: list = []
    if all_playlists:
        for name in ("PremiumTV.m3u", "AE_Channels.m3u"):
            path = out_dir / name
            if path.exists():
                targets.append(path)
        countries = True
    for item in extra:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / path
        if path.exists():
            targets.append(path)
        else:
            log(f"[epg] skipping missing playlist: {path}")
    if countries:
        targets.extend(sorted((out_dir / "countries").glob("*.m3u")))
    seen, ordered = set(), []
    for path in targets:
        key = str(path.resolve())
        if key not in seen:
            seen.add(key)
            ordered.append(path)
    return ordered


def run(out_dir: Path, targets: list, timeout: float, workers: int, retries: int,
        extra_guides: list, patch: bool, dry_run: bool, min_working_ratio: float,
        label: str, curated: list | None = None) -> dict:
    started = dt.datetime.now(dt.timezone.utc)
    per_playlist = {}
    guides: list = []
    for path in targets:
        found = extract_guides(path)
        per_playlist[str(path)] = found
        guides.extend(found)
    guides.extend(extra_guides)
    # Curated per-country sources (sources.json -> epg_sources) are verified
    # like any other guide, but never advertised in a playlist header: the
    # merged guide already carries their listings.
    curated_urls = [url for url in (curated or []) if url]
    curated_set = set(curated_urls)
    guides.extend(curated_urls)
    guides = list(dict.fromkeys(guides))
    log(f"[epg] {len(guides)} unique guide URLs across {len(targets)} playlists"
        + (f" ({len(curated_set)} curated sources)" if curated_set else ""))

    results: dict = {}
    if guides:
        with cf.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futures = {pool.submit(verify_guide, url, timeout, retries): url for url in guides}
            for index, future in enumerate(cf.as_completed(futures), 1):
                url = futures[future]
                try:
                    results[url] = future.result()
                except Exception as exc:  # noqa: BLE001
                    results[url] = {"url": url, "status": "unreachable",
                                    "reason": f"checker error: {type(exc).__name__}",
                                    "http_status": 0, "bytes": 0, "channels": 0,
                                    "programmes": 0, "sample_channel": "",
                                    "newest_programme": "", "gzipped": False,
                                    "elapsed": 0.0, "own_repo": is_own_guide(url)}
                if index % 25 == 0 or index == len(guides):
                    log(f"[epg] {index}/{len(guides)} guides checked")
    for url in curated_set:
        if url in results:
            results[url]["curated"] = True
    finished = dt.datetime.now(dt.timezone.utc)

    totals: dict = {}
    for result in results.values():
        totals[result["status"]] = totals.get(result["status"], 0) + 1
    curated_totals: dict = {}
    for url in curated_set:
        status = results.get(url, {}).get("status", "unchecked")
        curated_totals[status] = curated_totals.get(status, 0) + 1
    # The working share is what decides whether a run looks like an outage, so it
    # is measured over the upstream guides only - see is_own_guide(). A curated
    # per-country URL that answers 404 was simply never published (no epg-xx
    # file for that country): that is the normal shape of the curated list, not
    # evidence of a network problem, so it is left out of the share entirely.
    upstream = [result for result in results.values() if not result.get("own_repo")]
    own = [result for result in results.values() if result.get("own_repo")]
    own_totals: dict = {}
    for result in own:
        own_totals[result["status"]] = own_totals.get(result["status"], 0) + 1
    unpublished_curated = [result for result in upstream
                           if result.get("curated") and result.get("status") == "offline"]
    checked = len(upstream) - len(unpublished_curated)
    working = sum(1 for result in upstream if result["status"] in ("ok", "empty"))
    ratio = working / checked if checked else 0.0
    if unpublished_curated:
        log(f"[epg] {len(unpublished_curated)} curated per-country guides were never "
            f"published (404); excluded from the working share")
    if own:
        log(f"[epg] {len(own)} of {len(results)} guides are this repository's own "
            f"published files; excluded from the working share "
            f"({', '.join(f'{status}={count}' for status, count in sorted(own_totals.items()))})")

    patch_report = {"aborted": False, "abort_reason": "", "patched_files": [],
                    "removed": [], "added": [], "working_ratio": round(ratio, 4),
                    "own_guides_kept": len([url for url in guides if is_own_guide(url)])}
    if patch:
        if checked and ratio < min_working_ratio:
            patch_report["aborted"] = True
            patch_report["abort_reason"] = (
                f"only {working}/{checked} upstream guides answered ({ratio:.0%}) is below "
                f"--min-working-ratio {min_working_ratio:.0%}; treating this run as a "
                f"network problem and changing nothing")
            log(f"[epg] ABORTED: {patch_report['abort_reason']}")
        else:
            for path in targets:
                original = per_playlist.get(str(path), [])
                kept = [url for url in original
                        if url not in results
                        or results[url].get("own_repo")
                        or results[url].get("status") not in DEAD_STATUSES]
                removed = [url for url in original if url not in kept]
                added = [url for url in extra_guides
                         if url not in original
                         and results.get(url, {}).get("status") == "ok"]
                final = list(dict.fromkeys(kept + added))
                if final == original and not added:
                    continue
                patch_report["removed"].extend(
                    {"file": path.name, "url": url,
                     "reason": results.get(url, {}).get("reason", "")} for url in removed)
                patch_report["added"].extend({"file": path.name, "url": url} for url in added)
                if not dry_run and original:
                    if rewrite_header(path, final):
                        patch_report["patched_files"].append({
                            "file": str(path), "before": len(original), "after": len(final),
                            "removed": len(removed), "added": len(added)})
                        log(f"[epg] {path.name}: guides {len(original)} -> {len(final)} "
                            f"(-{len(removed)} dead, +{len(added)} new)")
                elif not dry_run:
                    log(f"[epg] {path.name}: no x-tvg-url header line found; skipped")
    return {
        "run_id": f"{started.strftime('%Y%m%dT%H%M%S')}Z-{os.getpid()}",
        "label": label,
        "started_utc": started.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "finished_utc": finished.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "duration_seconds": round((finished - started).total_seconds(), 1),
        "timeout": timeout,
        "playlists": [str(path.relative_to(ROOT)) if str(path).startswith(str(ROOT))
                      else str(path) for path in targets],
        "guides": [results.get(url, {"url": url, "status": "unchecked",
                                     "own_repo": is_own_guide(url)}) for url in guides],
        "totals": totals,
        "working_ratio": round(ratio, 4),
        "upstream_guides": checked,
        "curated_sources": {
            "count": len(curated_set),
            "statuses": curated_totals,
            "unpublished": len(unpublished_curated),
            "note": ("per-country XMLTV feeds from sources.json (epg_sources), verified "
                     "here and merged by epg_build; never advertised in playlist headers"),
            "urls": sorted(curated_set),
        },
        "own_guides": {
            "count": len(own),
            "statuses": own_totals,
            "note": ("guides this repository publishes itself; advertised to players but "
                     "never treated as an upstream source, and 404 here means the repository "
                     "is private rather than the guide being gone"),
        },
        "patch": patch_report,
        "per_playlist_guide_count": {path.name: len(per_playlist[str(path)]) for path in targets},
    }


def write_reports(out_dir: Path, report: dict) -> list:
    checks_dir = out_dir / "checks"
    checks_dir.mkdir(parents=True, exist_ok=True)
    (checks_dir / "epg-check.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    totals = report["totals"]
    own = report.get("own_guides") or {}
    own_count = own.get("count", 0)
    lines = [
        "# TV guide (EPG) check",
        "",
        f"- **Run:** {report['label']} (`{report['run_id']}`)",
        f"- **Started:** {report['started_utc']} | **Finished:** {report['finished_utc']} "
        f"| **Duration:** {report['duration_seconds']}s",
        f"- **Guides checked:** {len(report['guides'])} across "
        f"{len(report['playlists'])} playlists"
        + (f" ({own_count} of them are this repository's own published guides)"
           if own_count else ""),
        f"- **Working share of upstream guides:** {report['working_ratio']:.1%}",
        "",
        "| Result | Guides |", "|---|---:|",
    ]
    for status in ("ok", "empty", "unreachable", "blocked", "offline", "invalid"):
        if totals.get(status):
            lines.append(f"| {status} | {totals[status]} |")
    if own_count:
        lines.append(f"| own guide (excluded from the share above) | {own_count} |")
    lines += ["", "## Working guides (kept)", "",
              "| Guide | Channels | Programmes sampled | Newest programme | Size read |",
              "|---|---:|---:|---|---:|"]
    for guide in report["guides"]:
        if guide.get("status") != "ok" or guide.get("own_repo"):
            continue
        name = guide["url"].rsplit("/", 1)[-1]
        lines.append(f"| `{name}` | {guide.get('channels', 0)} | "
                     f"{guide.get('programmes', 0)} | {guide.get('newest_programme') or '-'} | "
                     f"{guide.get('bytes', 0) // 1024} KB |")
    curated = report.get("curated_sources") or {}
    if curated.get("count"):
        statuses = ", ".join(f"{status}={count}" for status, count
                             in sorted((curated.get("statuses") or {}).items()))
        curated_guides = [guide for guide in report["guides"] if guide.get("curated")]
        lines += ["", "## Curated per-country sources", "",
                  f"{curated['count']} guide URL(s) from `sources.json` (`epg_sources`) are "
                  "verified on every run and merged by `scripts/epg_build.py` ahead of the "
                  "guides found in playlist headers. They are never advertised in an "
                  "`x-tvg-url` header - the merged guide already carries their listings. "
                  f"Status this run: {statuses or 'unchecked'}.", "",
                  "| Source | Status | Channels | Programmes sampled |",
                  "|---|---|---:|---:|"]
        for guide in curated_guides[:30]:
            name = guide["url"].rsplit("/", 1)[-1]
            lines.append(f"| `{name}` | {guide.get('status')} | {guide.get('channels', 0)} | "
                         f"{guide.get('programmes', 0)} |")
        if len(curated_guides) > 30:
            lines.append(f"| … {len(curated_guides) - 30} more | | | |")
    broken = [guide for guide in report["guides"]
              if not guide.get("own_repo")
              and (guide.get("status") in DEAD_STATUSES or guide.get("status") == "blocked")]
    if broken:
        lines += ["", "## Guides that failed", "",
                  "| Guide | Status | Reason |", "|---|---|---|"]
        for guide in broken:
            lines.append(f"| `{scraper.safe_url(guide['url'])}` | {guide.get('status')} | "
                         f"{guide.get('reason', '')} |")
    if own_count:
        statuses = ", ".join(f"{status}={count}"
                             for status, count in sorted((own.get("statuses") or {}).items()))
        own_guides = [guide for guide in report["guides"] if guide.get("own_repo")]
        lines += ["", "## This repository's own guides", "",
                  f"{own_count} advertised guide URL(s) are files this repository publishes "
                  f"itself (`EPG/*.xml`), so they are never counted as upstream guides and "
                  f"never removed. Status of those: {statuses or 'unchecked'}. A `404` here "
                  "means the repository is private - GitHub only serves raw files to readers "
                  "who can see it (see the note at the top of `README.md`); it does not mean "
                  "the guide is gone for someone who can.",
                  "", "| Own guide | Status | Reason |", "|---|---|---|"]
        for guide in own_guides[:15]:
            name = guide["url"].rsplit("/", 1)[-1]
            lines.append(f"| `{name}` | {guide.get('status')} | {guide.get('reason', '')} |")
        if len(own_guides) > 15:
            lines.append(f"| … {len(own_guides) - 15} more (one per country playlist) | | |")
    patch = report.get("patch") or {}
    if patch:
        lines += ["", "## Patch", ""]
        if patch.get("aborted"):
            lines.append(f"- **Aborted:** {patch['abort_reason']}")
        else:
            removed = len(patch.get("removed", []))
            added = len(patch.get("added", []))
            lines.append(f"- Removed **{removed}** dead guides, added **{added}** verified "
                         f"guides across **{len(patch.get('patched_files', []))}** playlists.")
            for item in patch.get("removed", [])[:40]:
                lines.append(f"  - `-{item['url'].rsplit('/', 1)[-1]}` ({item['reason']})")
            for item in patch.get("added", [])[:40]:
                lines.append(f"  - `+{item['url'].rsplit('/', 1)[-1]}`")
    lines.append("")
    (checks_dir / "EPG-CHECK.md").write_text("\n".join(lines), encoding="utf-8")
    return [checks_dir / "epg-check.json", checks_dir / "EPG-CHECK.md"]


def append_edit_log(out_dir: Path, report: dict) -> Path:
    logs_dir = out_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / "epg-check-edits.txt"
    lines = [f"## {report['finished_utc']} - {report['label']} (EPG check, run {report['run_id']})"]
    patch = report.get("patch") or {}
    if patch.get("aborted"):
        lines.append(f"  ! aborted: {patch['abort_reason']}")
    for item in patch.get("removed", []):
        lines.append(f"  -removed guide {item['url']} [{item['reason']}] ({item['file']})")
    for item in patch.get("added", []):
        lines.append(f"  +added guide {item['url']} ({item['file']})")
    lines.append("")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return path


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "playlists"), help="playlists directory")
    ap.add_argument("--playlist", action="append", default=[],
                    help="playlist whose guides should be checked (repeatable)")
    ap.add_argument("--all", action="store_true",
                    help="check the guides of every published playlist")
    ap.add_argument("--countries", action="store_true", help="include country playlists")
    ap.add_argument("--guide", action="append", default=[],
                    help="extra guide URL to verify (and add with --patch)")
    ap.add_argument("--no-curated", action="store_true",
                    help="skip the curated per-country guides from sources.json "
                         "(epg_sources)")
    ap.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                    help="per-guide timeout in seconds")
    ap.add_argument("--workers", type=int, default=12, help="concurrent guide checks")
    ap.add_argument("--retries", type=int, default=1, help="retries for transient failures")
    ap.add_argument("--patch", action="store_true", help="drop dead guides from playlists")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --patch: report what would change, change nothing")
    ap.add_argument("--min-working-ratio", type=float, default=MIN_WORKING_RATIO,
                    help="abort patching below this share of working guides")
    ap.add_argument("--label", default="EPG check", help="run label for the reports")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = Path(args.out)
    targets = collect_targets(out_dir, args.playlist, args.all, args.countries)
    if not targets:
        log("[epg] no playlists to check - pass --all or --playlist <file>")
        return 2
    report = run(out_dir, targets, args.timeout, args.workers, args.retries,
                 list(dict.fromkeys(args.guide)), args.patch, args.dry_run,
                 args.min_working_ratio, args.label,
                 curated=[] if args.no_curated
                 else epg_sources.curated_guide_urls(out_dir / "countries"))
    if args.patch and not args.dry_run:
        report["patch"]["edit_log"] = str(
            display_path(append_edit_log(out_dir, report)))
    written = write_reports(out_dir, report)
    totals = report["totals"]
    log(f"[epg] done: ok={totals.get('ok', 0)} empty={totals.get('empty', 0)} "
        f"offline={totals.get('offline', 0)} invalid={totals.get('invalid', 0)} "
        f"unreachable={totals.get('unreachable', 0)} blocked={totals.get('blocked', 0)}")
    for path in written:
        log(f"[epg] wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
