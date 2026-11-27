#!/usr/bin/env python3
"""Pre-publish health gate for live-event feeds.

The daily scraper's shallow check proves a server answered, not that a player
can play the stream.  This gate re-tests every live-event entry with the
``#EXTVLCOPT`` headers a player would send (Referer, User-Agent, Origin, ...),
resolves HLS variants and pulls a real media segment through ``link_check``.

Only a working feed is publishable.  HTTP 403 and 404/410 entries are counted
and dropped explicitly; every other failed probe is dropped as unconfirmed.
If a fixture has no working feed left, the whole fixture is refused: none of
its entries are published.

The gate is used by ``scripts/scraper.py`` before it writes ``PremiumTV.m3u``.
The CLI is also available to the repair workflows and for measurement::

    python3 scripts/live_event_gate.py
    python3 scripts/live_event_gate.py --apply
    python3 scripts/live_event_gate.py --apply --sync-derived playlists/countries/*.m3u
    python3 scripts/live_event_gate.py --json - --md -

It only ever removes live-event entries.  Non-event channels are untouched,
and the original playlist header, comments and entry order are preserved when
``--apply`` is used.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import re
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_live_schedule  # noqa: E402
import legacy_sunset  # noqa: E402

DEFAULT_PLAYLIST = ROOT / "playlists" / "PremiumTV.m3u"
DEFAULT_JSON = ROOT / "playlists" / "checks" / "live-event-gate.json"
DEFAULT_MARKDOWN = ROOT / "playlists" / "checks" / "LIVE-EVENT-GATE.md"
DEFAULT_WORKERS = 12
DEFAULT_PER_HOST_WORKERS = 4
DEFAULT_TIMEOUT = 12.0
DEFAULT_RETRIES = 1
RETIRED_URLS = ROOT / "playlists" / "checks" / "retired-event-urls.json"
RETIREMENT_POLICY = (
    "SHA-256 hashes of live-event URLs that a deep probe confirmed dead "
    "(HTTP 403 or 404/410). A retired hash stays unpublished even if a later "
    "scrape re-adds the URL and a later probe succeeds."
)

DROP_HTTP_CODES = frozenset({403, 404, 410})
# Only an explicit HTTP status in the probe reason is conclusive. A reason such
# as "segment too small (404 bytes)" must stay ``dropped_other``, not become a
# reported 404.
EVIDENCE_CODE_RE = re.compile(r"\bHTTP\s+(403|404|410)\b", re.IGNORECASE)
LIVE_EVENT_GROUPS = frozenset({"live events", "live sports", "sports"})
MAIN_COUNT_RE = re.compile(r"^(# )(\d+)( channels\b)", re.MULTILINE)
DERIVED_COUNT_RE = re.compile(
    r"^(# .*?working channels \()\d+(\))", re.MULTILINE)
README_TOTAL_RE = re.compile(r"Total confirmed working channels: \*\*\d+\*\*")
SENSITIVE_QUERY_KEYS = {
    "access_token", "api_key", "apikey", "auth", "authorization", "key",
    "password", "pass", "secret", "signature", "sig", "token", "username",
}


def _safe_url(raw_url: str) -> str:
    """Redact credentials and common secret query values from report URLs."""
    try:
        parsed = urllib.parse.urlsplit(str(raw_url or ""))
        if not parsed.scheme or not parsed.netloc:
            return str(raw_url or "")
        host = parsed.hostname or ""
        try:
            if parsed.port:
                host = f"{host}:{parsed.port}"
        except ValueError:
            pass
        query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        safe_query = urllib.parse.urlencode([
            (key, "[redacted]" if key.lower() in SENSITIVE_QUERY_KEYS else value)
            for key, value in query
        ])
        return urllib.parse.urlunsplit((parsed.scheme, host, parsed.path, safe_query, ""))
    except Exception:  # noqa: BLE001
        return str(raw_url or "")


def event_of(channel: Any) -> dict | None:
    """Return the shared fixture identity for a channel, or None for non-events."""
    return build_live_schedule.parse_event(
        getattr(channel, "name", "") or "",
        str(getattr(channel, "attrs", {}).get("tvg-id", "") or ""),
    )


def is_live_event(channel: Any) -> bool:
    """Whether a channel belongs to the live-event bracket convention.

    Event feeds are bracket-prefixed and live in the ``Live Events`` group at
    scrape time or the ``Sports``/``Live Sports`` group after categorization.
    The group check matters: a bracket-prefixed movie or news entry is not an
    event feed and must pass through untouched.  Matchups and non-matchup
    events (F1, darts, horse racing) share this convention.
    """
    name = str(getattr(channel, "name", "") or "").lstrip()
    attrs = getattr(channel, "attrs", {}) or {}
    group = str(attrs.get("group-title", "") or "").strip().casefold()
    return name.startswith("[") and group in LIVE_EVENT_GROUPS


def failure_code(result: dict) -> int:
    """The 403/404/410 code a failed probe proved, if any.

    A master playlist can answer 200 while its selected variant or media
    segment answers 403/404.  Those failures are still conclusive and must be
    counted like a direct failure, so inspect the probe reason as well as the
    top-level HTTP status.
    """
    try:
        code = int(result.get("http_status") or 0)
    except (TypeError, ValueError):
        code = 0
    if code in DROP_HTTP_CODES:
        return code
    match = EVIDENCE_CODE_RE.search(str(result.get("reason") or ""))
    return int(match.group(1)) if match else 0


def _probe_one(
    channel: Any,
    timeout: float,
    retries: int,
    host_limiter: Any,
    probe: Callable[..., dict],
) -> dict:
    try:
        result = probe(channel, timeout, retries, host_limiter)
        return result if isinstance(result, dict) else {
            "status": "unreachable", "reason": "probe returned no result",
            "http_status": 0,
        }
    except Exception as exc:  # noqa: BLE001 - one bad feed must not abort the gate
        return {
            "status": "unreachable",
            "reason": f"gate probe error: {type(exc).__name__}",
            "http_status": 0,
        }


def _default_probe(channel: Any, timeout: float, retries: int, host_limiter: Any) -> dict:
    # Imported lazily: link_check imports scraper, and scraper imports this
    # module.  The import is safe only after scraper has finished loading.
    import link_check
    return link_check.verify_link(
        channel, timeout=timeout, retries=retries, deep=True,
        host_limiter=host_limiter,
    )


def _url_hash(channel: Any) -> str:
    return hashlib.sha256(
        str(getattr(channel, "url", "") or "").encode("utf-8", "replace")
    ).hexdigest()


def load_retired_hashes(path: Path = RETIRED_URLS) -> set[str]:
    """Load the permanent retired-event hash registry.

    The registry is intentionally separate from the generated gate report: a
    later scrape must not be able to make a previously dead URL publishable by
    simply discovering it again and probing it while it happens to answer.
    """
    path = Path(path)
    if not path.is_file():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema") != 1:
        raise ValueError(f"{path}: retired-event registry must be schema 1")
    hashes = payload.get("hashes")
    if not isinstance(hashes, list) or not all(
        isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value)
        for value in hashes
    ):
        raise ValueError(f"{path}: hashes must be lowercase SHA-256 strings")
    return set(hashes)


def retirement_candidates(report: dict) -> set[str]:
    """Hashes a report proved dead, excluding transient/unconfirmed failures."""
    candidates: set[str] = set()
    feeds = []
    for fixture in report.get("fixtures_detail") or []:
        feeds.extend(fixture.get("feeds") or [])
    feeds.extend(report.get("singleton_feeds") or [])
    for feed in feeds:
        if feed.get("outcome") in {"dropped_403", "dropped_404"}:
            digest = feed.get("sha256")
            if isinstance(digest, str):
                candidates.add(digest)
    return candidates


def record_retired_hashes(report: dict, path: Path = RETIRED_URLS) -> list[str]:
    """Persist newly confirmed-dead event URLs. Returns the hashes added."""
    candidates = retirement_candidates(report)
    if not candidates:
        return []
    path = Path(path)
    existing = load_retired_hashes(path)
    added = sorted(candidates - existing)
    if not added:
        return []
    document = {
        "schema": 1,
        "updated_utc": dt.datetime.now(dt.timezone.utc).isoformat(
            timespec="seconds").replace("+00:00", "Z"),
        "policy": RETIREMENT_POLICY,
        "hashes": sorted(existing | set(added)),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    return added


def _feed_report(channel: Any, result: dict, outcome: str) -> dict:
    return {
        "name": getattr(channel, "name", ""),
        "url": _safe_url(getattr(channel, "url", "")),
        "sha256": _url_hash(channel),
        "status": result.get("status", ""),
        "outcome": outcome,
        "http_status": result.get("http_status", 0),
        "reason": result.get("reason", ""),
        "segment_ok": result.get("segment_ok"),
        "kind": result.get("kind", ""),
    }


def gate_channels(
    channels: list,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    workers: int = DEFAULT_WORKERS,
    per_host_workers: int = DEFAULT_PER_HOST_WORKERS,
    host_limiter: Any = None,
    probe: Callable[..., dict] | None = None,
    retired_hashes: set[str] | None = None,
) -> tuple[list, dict]:
    """Re-test live-event entries and return ``(publishable_channels, report)``.

    Entries are grouped by the shared fixture key from
    ``build_live_schedule.parse_event``.  A fixture survives only when at least
    one of its feeds is confirmed working; the surviving entries are exactly
    those working feeds, in their original order.  Non-matchup event feeds are
    gated individually (they have no fixture to refuse).  Non-event channels
    always pass through unchanged.

    ``retired_hashes`` is the permanent retired-event URL registry. A retired
    URL is withheld without probing, even if a later scrape re-added it and it
    now answers successfully.
    """
    probe = probe or _default_probe
    retired_hashes = (
        load_retired_hashes() if retired_hashes is None else set(retired_hashes)
    )
    event_items: list[tuple[int, Any, dict | None]] = []
    for index, channel in enumerate(channels):
        if not is_live_event(channel):
            continue
        event_items.append((index, channel, event_of(channel)))

    if not event_items:
        return list(channels), {
            "schema": 1,
            "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(
                timespec="seconds").replace("+00:00", "Z"),
            "entries": 0, "fixtures": 0,
            "non_fixture_entries": 0, "non_fixture_working": 0,
            "non_fixture_dropped": 0,
            "working_entries": 0,
            "published_entries": 0, "published_fixtures": 0,
            "refused_fixtures": 0, "dropped_entries": 0,
            "dropped_403": 0, "dropped_404": 0, "dropped_other": 0,
            "dropped_retired": 0,
            "status_counts": {}, "refused": [],
            "fixtures_detail": [], "singleton_feeds": [],
            "dropped_event_url_sha256": [],
            "retired_event_url_sha256": sorted(retired_hashes),
            "newly_retired_event_url_sha256": [],
        }

    grouped: dict[str, dict] = collections.OrderedDict()
    singletons: list[tuple[int, Any]] = []
    for index, channel, event in event_items:
        if event is None:
            singletons.append((index, channel))
            continue
        row = grouped.setdefault(event["key"], {"event": event, "items": []})
        row["items"].append((index, channel))

    if host_limiter is None:
        # A shared limiter keeps a 67-entry gate from bursting one event host.
        # Imported lazily for the same circular-import reason as the probe.
        try:
            import scraper
            host_limiter = scraper.HostLimiter(per_host_workers)
        except Exception:  # noqa: BLE001 - tests and library callers may not need it
            host_limiter = None

    results: dict[int, dict] = {}
    retired_applied: set[str] = set()
    for _, channel, _ in event_items:
        digest = _url_hash(channel)
        if digest in retired_hashes:
            retired_applied.add(digest)
            results[id(channel)] = {
                "status": "dead",
                "http_status": 0,
                "reason": "retired after a previous dead probe",
                "segment_ok": None,
                "kind": "retired",
                "retired": True,
            }

    with cf.ThreadPoolExecutor(max_workers=max(1, int(workers))) as pool:
        futures = {
            pool.submit(_probe_one, channel, timeout, retries, host_limiter, probe): channel
            for _, channel, _ in event_items
            if id(channel) not in results
        }
        for future in cf.as_completed(futures):
            channel = futures[future]
            results[id(channel)] = future.result()

    working_ids: set[int] = set()
    published_fixtures = 0
    refused: list[dict] = []
    fixtures_detail: list[dict] = []
    singleton_feeds: list[dict] = []
    non_fixture_working = 0
    counts = collections.Counter()
    dropped_403 = dropped_404 = dropped_other = dropped_retired = 0

    def apply_outcome(channel: Any, result: dict) -> str:
        nonlocal dropped_403, dropped_404, dropped_other, dropped_retired
        status = str(result.get("status") or "unreachable")
        counts[status] += 1
        if result.get("retired"):
            dropped_retired += 1
            channel.status = "dead"
            channel.reason = "live-event gate: retired dead event URL"
            return "dropped_retired"
        if status == "working":
            channel.status = "alive"
            channel.reason = f"live-event gate: {result.get('reason') or 'working'}"
            return "working"
        code = failure_code(result)
        if code == 403:
            dropped_403 += 1
            channel.status, channel.reason = "dead", "live-event gate: HTTP 403"
            return "dropped_403"
        if code in (404, 410):
            dropped_404 += 1
            channel.status, channel.reason = "dead", f"live-event gate: HTTP {code}"
            return "dropped_404"
        dropped_other += 1
        channel.status = ("unverified" if status in ("unreachable", "blocked") else "dead")
        channel.reason = (
            f"live-event gate: {status}"
            + (f" ({result.get('reason')})" if result.get("reason") else "")
        )
        return "dropped_other"

    for key, row in grouped.items():
        working = []
        for _, channel in row["items"]:
            result = results[id(channel)]
            if result.get("status") == "working":
                working.append(channel)
                working_ids.add(id(channel))
        refused_here = not working
        if refused_here:
            refused.append({
                "key": key,
                "title": row["event"].get("title") or key,
                "sport": row["event"].get("sport") or "",
                "entries": len(row["items"]),
            })
        else:
            published_fixtures += 1

        feeds = []
        for _, channel in row["items"]:
            result = results[id(channel)]
            outcome = apply_outcome(channel, result)
            feeds.append(_feed_report(channel, result, outcome))
        fixtures_detail.append({
            "key": key,
            "title": row["event"].get("title") or key,
            "sport": row["event"].get("sport") or "",
            "entries": len(row["items"]),
            "working": len(working),
            "refused": refused_here,
            "feeds": feeds,
        })

    event_indices = {index for index, _, _ in event_items}
    for index, channel in singletons:
        result = results[id(channel)]
        outcome = apply_outcome(channel, result)
        if outcome == "working":
            working_ids.add(id(channel))
            non_fixture_working += 1
        singleton_feeds.append(_feed_report(channel, result, outcome))
    kept = [
        channel for index, channel in enumerate(channels)
        if index not in event_indices or id(channel) in working_ids
    ]

    working_entries = len(working_ids)
    total = len(event_items)
    dropped_hashes = sorted({
        _url_hash(channel)
        for _, channel, _ in event_items
        if id(channel) not in working_ids
    })
    report = {
        "schema": 1,
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(
            timespec="seconds").replace("+00:00", "Z"),
        "entries": total,
        "fixtures": len(grouped),
        "non_fixture_entries": len(singletons),
        "non_fixture_working": non_fixture_working,
        "non_fixture_dropped": len(singletons) - non_fixture_working,
        "working_entries": working_entries,
        "published_entries": working_entries,
        "published_fixtures": published_fixtures,
        "refused_fixtures": len(refused),
        "dropped_entries": total - working_entries,
        "dropped_403": dropped_403,
        "dropped_404": dropped_404,
        "dropped_other": dropped_other,
        "dropped_retired": dropped_retired,
        "status_counts": dict(sorted(counts.items())),
        "refused": refused,
        "fixtures_detail": fixtures_detail,
        "singleton_feeds": singleton_feeds,
        "dropped_event_url_sha256": dropped_hashes,
        "retired_event_url_sha256": sorted(retired_applied),
        "newly_retired_event_url_sha256": sorted(
            retirement_candidates({"fixtures_detail": fixtures_detail,
                                   "singleton_feeds": singleton_feeds})
            - retired_hashes
        ),
    }
    return kept, report


def fail_closed(channels: list, reason: str) -> tuple[list, dict]:
    """Drop every live-event entry when the gate itself cannot run.

    A health gate that silently passes feeds it could not test is worse than no
    gate.  Non-event channels still publish; every fixture is reported refused.
    """
    event_items = [(index, channel, event_of(channel))
                   for index, channel in enumerate(channels)
                   if is_live_event(channel)]
    grouped: dict[str, dict] = collections.OrderedDict()
    for _, channel, event in event_items:
        if event is not None:
            grouped.setdefault(event["key"], {"event": event, "items": []})["items"].append(channel)
    for _, channel, _ in event_items:
        channel.status = "unverified"
        channel.reason = f"live-event gate failed: {reason}"
    dropped = len(event_items)
    non_fixture_entries = sum(1 for _, _, event in event_items if event is None)
    dropped_hashes = sorted({_url_hash(channel) for _, channel, _ in event_items})
    singleton_feeds = [
        _feed_report(
            channel,
            {"status": "unverified", "reason": reason, "http_status": 0},
            "dropped_other",
        )
        for _, channel, event in event_items if event is None
    ]
    report = {
        "schema": 1,
        "generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(
            timespec="seconds").replace("+00:00", "Z"),
        "error": reason,
        "entries": dropped,
        "fixtures": len(grouped),
        "non_fixture_entries": non_fixture_entries,
        "non_fixture_working": 0,
        "non_fixture_dropped": non_fixture_entries,
        "working_entries": 0,
        "published_entries": 0,
        "published_fixtures": 0,
        "refused_fixtures": len(grouped),
        "dropped_entries": dropped,
        "dropped_403": 0,
        "dropped_404": 0,
        "dropped_other": dropped,
        "dropped_retired": 0,
        "status_counts": {},
        "refused": [
            {"key": key, "title": row["event"].get("title") or key,
             "sport": row["event"].get("sport") or "", "entries": len(row["items"])}
            for key, row in grouped.items()
        ],
        "fixtures_detail": [],
        "singleton_feeds": singleton_feeds,
        "dropped_event_url_sha256": dropped_hashes,
        "retired_event_url_sha256": [],
        "newly_retired_event_url_sha256": [],
    }
    event_indices = {index for index, _, _ in event_items}
    return [channel for index, channel in enumerate(channels)
            if index not in event_indices], report


def _refresh_counts(text: str, count: int) -> str:
    """Keep advertised entry counts in step with a filtered playlist."""
    text = MAIN_COUNT_RE.sub(
        lambda match: f"{match.group(1)}{count}{match.group(3)}", text, count=1)
    return DERIVED_COUNT_RE.sub(
        lambda match: f"{match.group(1)}{count}{match.group(2)}", text, count=1)


def _advertised_entries(text: str) -> int:
    """Count entries a player sees, excluding the sanctioned legacy notice."""
    return sum(
        1 for line in text.splitlines()
        if line.strip().startswith("#EXTINF")
        and not legacy_sunset.is_notice_entry(line.strip())
    )


def _filtered_playlist_text(text: str, channels: list, kept: list) -> str:
    import link_check

    header, blocks = link_check.split_blocks(text)
    kept_ids = {id(channel) for channel in kept}
    if len(blocks) == len(channels):
        kept_blocks = [
            block for block, channel in zip(blocks, channels)
            if id(channel) in kept_ids
        ]
    else:
        # A malformed block count must not make the gate drop the wrong entry.
        # Fall back to exact URLs; live-event URLs are unique.
        drop_urls = {channel.url for channel in channels if id(channel) not in kept_ids}
        kept_blocks = [block for block in blocks if block.url not in drop_urls]
    return link_check.blocks_to_text(header, kept_blocks)


def sync_derived_playlists(paths: list[Path], dropped_hashes: set[str],
                           main_entries: int | None = None) -> list[dict]:
    """Remove the same dropped event URLs from derived playlists.

    Country files are slices of ``PremiumTV.m3u`` but are not rebuilt by every
    repair workflow. Without this pass, a fixture dropped from the main file
    would keep publishing through ``countries/USA.m3u`` and the USA shelf. Only
    URLs the main gate actually rejected are removed; an event URL that exists
    only in a derived file is left alone rather than guessed at.
    """
    if not dropped_hashes:
        return []
    import link_check
    import scraper

    results = []
    countries_dirs: set[Path] = set()
    for raw_path in paths:
        path = Path(raw_path)
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        channels, _ = scraper.parse_m3u(text, path.stem)
        dropped_ids = {
            id(channel) for channel in channels
            if is_live_event(channel) and _url_hash(channel) in dropped_hashes
        }
        if not dropped_ids:
            continue
        kept = [channel for channel in channels if id(channel) not in dropped_ids]
        filtered = _filtered_playlist_text(text, channels, kept)
        # Preserve comments but do not let the title advertise the pre-filter
        # count after event entries are removed. The legacy USA feed carries a
        # sanctioned notice entry that is a message, not a channel: counting it
        # here made its header disagree with the live feed by one.
        visible_entries = _advertised_entries(filtered)
        filtered = _refresh_counts(filtered, visible_entries)
        if filtered == text:
            continue
        path.write_text(filtered, encoding="utf-8")
        results.append({
            "file": str(path),
            "removed": len(dropped_ids),
            "entries": visible_entries,
        })
        if path.parent.name == "countries":
            countries_dirs.add(path.parent)
    for countries_dir in sorted(countries_dirs):
        link_check.sync_countries_readme(countries_dir)
        if main_entries is not None:
            readme = countries_dir / "README.md"
            if readme.is_file():
                text = readme.read_text(encoding="utf-8")
                text = README_TOTAL_RE.sub(
                    f"Total confirmed working channels: **{main_entries}**", text, count=1)
                readme.write_text(text, encoding="utf-8")
    return results


def apply_to_playlist_text(
    text: str,
    *,
    timeout: float = DEFAULT_TIMEOUT,
    retries: int = DEFAULT_RETRIES,
    workers: int = DEFAULT_WORKERS,
    per_host_workers: int = DEFAULT_PER_HOST_WORKERS,
    probe: Callable[..., dict] | None = None,
    retired_hashes: set[str] | None = None,
) -> tuple[str, dict]:
    """Return the filtered playlist text and the gate report.

    An unexpected gate failure withholds every live-event entry rather than
    returning the original text: the CLI may still be asked to write the file,
    and a failed gate must never publish an untested event playlist.
    """
    import scraper

    channels, _ = scraper.parse_m3u(text, "PremiumTV")
    try:
        kept, report = gate_channels(
            channels, timeout=timeout, retries=retries, workers=workers,
            per_host_workers=per_host_workers, probe=probe,
            retired_hashes=retired_hashes,
        )
    except Exception as exc:  # noqa: BLE001 - fail closed for live events
        kept, report = fail_closed(channels, f"{type(exc).__name__}: {exc}")
    filtered = _filtered_playlist_text(text, channels, kept)
    report["playlist_entries"] = len(kept)
    return _refresh_counts(filtered, len(kept)), report


def _md_cell(value: Any) -> str:
    """Escape one Markdown table cell so a team or reason cannot break it."""
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def render_markdown(report: dict, playlist: str = "") -> str:
    entries = report.get("entries", 0)
    lines = [
        "# Live-event pre-publish gate",
        "",
        f"- **Playlist:** `{playlist or 'playlists/PremiumTV.m3u'}`",
        f"- **Run:** {report.get('generated_utc', '-')}",
        f"- **Entries / fixtures:** {entries} / {report.get('fixtures', 0)}",
        f"- **Working:** {report.get('working_entries', 0)}",
        f"- **Non-matchup event feeds:** {report.get('non_fixture_entries', 0)} "
        f"({report.get('non_fixture_working', 0)} working)",
        f"- **Dropped:** {report.get('dropped_entries', 0)} "
        f"(403: {report.get('dropped_403', 0)}, "
        f"404/410: {report.get('dropped_404', 0)}, "
        f"other: {report.get('dropped_other', 0)}, "
        f"retired: {report.get('dropped_retired', 0)})",
        f"- **Publishable fixtures:** {report.get('published_fixtures', 0)}",
        f"- **Refused fixtures (no working feed):** {report.get('refused_fixtures', 0)}",
        "",
    ]
    if report.get("error"):
        lines += [f"> Gate error: {report['error']}", ""]
    refused = report.get("refused") or []
    if refused:
        lines += ["## Refused fixtures", "",
                  "| Fixture | Sport | Entries |", "|---|---|---:|"]
        for item in refused:
            lines.append(
                f"| {_md_cell(item['title'])} | {_md_cell(item['sport'] or '-')} | "
                f"{item['entries']} |"
            )
        lines.append("")
    dropped = []
    for fixture in report.get("fixtures_detail") or []:
        for feed in fixture.get("feeds") or []:
            if feed.get("outcome") != "working":
                dropped.append((fixture["title"], feed))
    if dropped:
        lines += ["## Dropped fixture entries", "",
                  "| Fixture | Feed | Outcome | HTTP | Reason |",
                  "|---|---|---|---:|---|"]
        for title, feed in dropped:
            lines.append(
                f"| {_md_cell(title)} | {_md_cell(feed.get('name', ''))} | "
                f"{_md_cell(feed.get('outcome', ''))} | {feed.get('http_status', 0)} | "
                f"{_md_cell(feed.get('reason', ''))} |"
            )
        lines.append("")
    singletons = report.get("singleton_feeds") or []
    if singletons:
        lines += ["## Non-matchup event feeds", "",
                  "| Feed | Outcome | HTTP | Reason |",
                  "|---|---|---:|---|"]
        for feed in singletons:
            lines.append(
                f"| {_md_cell(feed.get('name', ''))} | "
                f"{_md_cell(feed.get('outcome', ''))} | {feed.get('http_status', 0)} | "
                f"{_md_cell(feed.get('reason', ''))} |"
            )
        lines.append("")
    derived = report.get("derived") or []
    if derived:
        lines += ["## Derived playlists synchronized", "",
                  "| Playlist | Removed | Entries left |", "|---|---:|---:|"]
        for item in derived:
            lines.append(
                f"| {_md_cell(item.get('file', ''))} | {item.get('removed', 0)} | "
                f"{item.get('entries', 0)} |"
            )
        lines.append("")
    if not entries:
        lines += ["No live-event entries were found; no entries were removed.", ""]
    elif not report.get("dropped_entries"):
        lines += ["No live-event entry was dropped; every entry had a working feed.", ""]
    lines += [
        "## Interpretation",
        "",
        "- Every entry was re-tested with its own `#EXTVLCOPT` headers and a deep "
        "HLS variant/media-segment probe.",
        "- Only `working` feeds are publishable. A fixture with zero working feeds "
        "is refused entirely; no entry from it is published.",
        "- 403 and 404/410 are counted separately because they are conclusive; "
        "other probe failures are also withheld rather than published unverified.",
        "- Confirmed 403/404/410 hashes are retired permanently and are withheld "
        "without probing if a later scrape re-adds the URL.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--playlist", type=Path, default=DEFAULT_PLAYLIST)
    parser.add_argument("--json", dest="json_path", default=str(DEFAULT_JSON),
                        help="report JSON path, or - for stdout")
    parser.add_argument("--md", dest="md_path", default=str(DEFAULT_MARKDOWN),
                        help="report Markdown path, or - for stdout")
    parser.add_argument("--apply", action="store_true",
                        help="write the filtered playlist back after the gate")
    parser.add_argument("--sync-derived", type=Path, nargs="+", default=[],
                        metavar="PATH",
                        help="with --apply, remove the same dropped event URLs from these derived playlists")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--per-host-workers", type=int, default=DEFAULT_PER_HOST_WORKERS)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument("--retired-urls", type=Path, default=RETIRED_URLS,
                        help="retired-event hash registry")
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when any fixture is refused")
    args = parser.parse_args(argv)
    if args.sync_derived and not args.apply:
        parser.error("--sync-derived requires --apply")

    text = args.playlist.read_text(encoding="utf-8", errors="replace")
    retired_hashes = load_retired_hashes(args.retired_urls)
    filtered, report = apply_to_playlist_text(
        text, timeout=args.timeout, retries=args.retries,
        workers=args.workers, per_host_workers=args.per_host_workers,
        retired_hashes=retired_hashes,
    )
    report["playlist"] = str(args.playlist)
    report["applied"] = False
    if args.apply and filtered != text:
        args.playlist.write_text(filtered, encoding="utf-8")
        report["applied"] = True
    if args.apply:
        added = record_retired_hashes(report, args.retired_urls)
        if added:
            print(f"[live-event-gate] retired {len(added)} newly dead URL hash(es)")
    if args.sync_derived:
        report["derived"] = sync_derived_playlists(
            args.sync_derived,
            set(report.get("dropped_event_url_sha256") or []),
            main_entries=report.get("playlist_entries"),
        )

    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    markdown = render_markdown(report, str(args.playlist))
    if args.json_path == "-":
        print(payload, end="")
    else:
        path = Path(args.json_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    if args.md_path == "-":
        print(markdown, end="")
    else:
        path = Path(args.md_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(markdown, encoding="utf-8")

    print(
        f"[live-event-gate] {report['entries']} entries / {report['fixtures']} fixtures "
        f"(+{report.get('non_fixture_entries', 0)} non-matchup event feeds): "
        f"{report['working_entries']} working, {report['dropped_entries']} dropped "
        f"(403 {report['dropped_403']}, 404/410 {report['dropped_404']}, "
        f"other {report['dropped_other']}); "
        f"{report['published_fixtures']} fixtures publishable, "
        f"{report['refused_fixtures']} refused"
    )
    derived = report.get("derived") or []
    if derived:
        print(
            f"[live-event-gate] synchronized {len(derived)} derived playlist(s); "
            f"removed {sum(item['removed'] for item in derived)} entry(ies)"
        )
    if report.get("error"):
        print(f"[live-event-gate] ERROR: {report['error']}", file=sys.stderr)
        return 1
    return 1 if args.strict and report["refused_fixtures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
