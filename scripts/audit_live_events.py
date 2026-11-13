#!/usr/bin/env python3
"""Audit live-event redundancy, health and upstream diversity offline.

A matchup is reliable only when the published playlist has two confirmed
primary feeds plus a third confirmed feed reserved as backup.  Different names
for the same URL never count twice, and multiple URLs from one origin are shown
as one origin family so mirrors cannot silently masquerade as redundancy.

The regular workflow writes a warning report.  ``--strict`` is available for a
release gate once every active fixture meets the policy; it exits 1 on a
deficit.  This script never invents, duplicates, or probes a feed.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import ipaddress
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_live_schedule  # noqa: E402
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_PLAYLIST = ROOT / "playlists" / "PremiumTV.m3u"
DEFAULT_SCRAPE_REPORT = ROOT / "playlists" / "report.json"
DEFAULT_SOURCES_DIR = ROOT / "playlists" / "sources"
DEFAULT_MARKDOWN = ROOT / "playlists" / "checks" / "LIVE-EVENT-RELIABILITY.md"
DEFAULT_JSON = ROOT / "playlists" / "checks" / "live-event-reliability.json"

# The provider marker is part of the upstream event display name, e.g.
# ``(STRMGATE)``, ``(TVF90)`` or ``(FAWA)``.  Keep the generic uppercase arm so
# newly introduced provider labels are visible without a code release.
PROVIDER_TAG = re.compile(
    r"\((STRMCNTR|STRMGATE|STRMXHD|TVF90|PLIBRE|WEBCAST|DAMITV|FAWA|STP|iSTRMEAST|[A-Z][A-Z0-9_-]{2,13})\)"
)
NON_PROVIDER_TAGS = {
    "BACKUP", "HD", "SD", "UHD", "FHD", "LIVE", "USA", "UK", "ESPN", "NFL", "NBA", "NHL",
}
SECOND_LEVEL_SUFFIXES = {"ac", "co", "com", "edu", "gov", "net", "org"}


def provider_of(name: str) -> str:
    tags = [match.upper() for match in PROVIDER_TAG.findall(name or "")]
    tags = [tag for tag in tags if tag not in NON_PROVIDER_TAGS]
    return tags[-1] if tags else ""


def origin_family(raw_url: str) -> str:
    """A conservative host family: subdomains of one provider count once."""
    host = (urlsplit(raw_url).hostname or "").lower().rstrip(".")
    if not host:
        return "unknown"
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass
    labels = host.split(".")
    if len(labels) <= 2:
        return host
    # Keep co.uk/com.au-style registrable families together without adding a
    # public-suffix dependency to an otherwise standard-library audit.
    if len(labels) >= 3 and labels[-2] in SECOND_LEVEL_SUFFIXES and len(labels[-1]) == 2:
        return ".".join(labels[-3:])
    return ".".join(labels[-2:])


def fingerprint(raw_url: str) -> str:
    return hashlib.sha256(raw_url.encode("utf-8", "replace")).hexdigest()[:12]


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def source_url_index(sources_dir: Path) -> dict[str, set[str]]:
    """Map exact stream URLs to the source-cache files that supplied them."""
    index: dict[str, set[str]] = collections.defaultdict(set)
    if not sources_dir.is_dir():
        return index
    for path in sorted(sources_dir.glob("*.m3u*")):
        try:
            channels, _ = scraper.parse_m3u(path.read_text(encoding="utf-8", errors="replace"), path.stem)
        except OSError:
            continue
        for channel in channels:
            if channel.url:
                index[channel.url].add(path.stem)
    return index


def health_index(report: dict) -> tuple[bool, dict[str, str], set[str]]:
    checked = bool(report.get("checked") and report.get("check_completed"))
    statuses: dict[str, str] = {}
    for key, label in (("dead", "dead"), ("unverified", "unverified"),
                       ("retained_links", "retained-unverified")):
        for item in report.get(key, []) or []:
            if isinstance(item, dict) and item.get("url"):
                statuses[str(item["url"])] = label
    hashes = report.get("reachable_event_url_sha256")
    # Legacy or malformed reports do not establish which exact URLs succeeded.
    reachable = {value for value in hashes if isinstance(value, str)} if isinstance(hashes, list) else set()
    return checked, statuses, reachable if checked else set()


def audit(playlist: Path = DEFAULT_PLAYLIST, scrape_report: Path = DEFAULT_SCRAPE_REPORT,
          sources_dir: Path = DEFAULT_SOURCES_DIR, min_feeds: int = 3,
          min_origins: int = 2) -> dict:
    channels, _ = scraper.parse_m3u(
        playlist.read_text(encoding="utf-8", errors="replace"), playlist.stem
    )
    scrape = load_json(scrape_report)
    checked, known_health, reachable_hashes = health_index(scrape)
    supplied_by = source_url_index(sources_dir)

    grouped: dict[str, dict] = {}
    seen_urls: dict[str, set[str]] = collections.defaultdict(set)
    for channel in channels:
        event = build_live_schedule.parse_event(
            channel.name, (channel.attrs.get("tvg-id", "") or "").strip()
        )
        if event is None or channel.url in seen_urls[event["key"]]:
            continue
        seen_urls[event["key"]].add(channel.url)
        row = grouped.setdefault(event["key"], {**event, "feeds": []})
        safe = scraper.safe_url(channel.url)
        status = known_health.get(safe)
        if status is None:
            url_hash = hashlib.sha256(channel.url.encode("utf-8", "replace")).hexdigest()
            status = "reachable" if url_hash in reachable_hashes else "published-not-checked"
        provider = provider_of(channel.name)
        family = origin_family(channel.url)
        row["feeds"].append({
            "fingerprint": fingerprint(channel.url),
            "role": "",  # assigned after playlist-order deduplication
            "status": status,
            "provider": provider or None,
            "origin_family": family,
            "ingest_sources": sorted(supplied_by.get(channel.url, set())),
        })

    fixtures = []
    for row in grouped.values():
        feeds = row.pop("feeds")
        for index, feed in enumerate(feeds):
            feed["role"] = "primary" if index < 2 else "backup"
        healthy = [feed for feed in feeds if feed["status"] == "reachable"]
        healthy_primaries = [
            feed for feed in healthy if feed["role"] == "primary"
        ]
        healthy_backups = [
            feed for feed in healthy if feed["role"] == "backup"
        ]
        required_primaries = 2
        required_backups = max(1, min_feeds - required_primaries)
        origins = sorted({feed["origin_family"] for feed in healthy})
        providers = sorted({feed["provider"] for feed in healthy if feed.get("provider")})
        ingest_sources = sorted({source for feed in feeds for source in feed["ingest_sources"]})
        reasons = []
        if len(healthy_primaries) < required_primaries:
            reasons.append(
                f"needs {required_primaries - len(healthy_primaries)} more confirmed primary feed(s)"
            )
        if len(healthy_backups) < required_backups:
            reasons.append(
                f"needs {required_backups - len(healthy_backups)} more confirmed dedicated backup feed(s)"
            )
        if len(origins) < min_origins:
            reasons.append(f"needs {min_origins - len(origins)} more independent origin family/families")
        if not checked:
            reasons.append("latest scrape did not complete a health check")
        fixtures.append({
            **row,
            "feed_count": len(feeds),
            "confirmed_feed_count": len(healthy),
            "confirmed_primary_count": len(healthy_primaries),
            "confirmed_backup_count": len(healthy_backups),
            "primary_ready": len(healthy_primaries) >= required_primaries,
            "backup_ready": len(healthy_backups) >= required_backups,
            "origin_families": origins,
            "providers": providers,
            "ingest_sources": ingest_sources,
            "policy_met": not reasons,
            "deficits": reasons,
            "feeds": feeds,
        })
    fixtures.sort(key=lambda item: (item["sport"].casefold(), item["title"].casefold()))

    compliant = sum(1 for item in fixtures if item["policy_met"])
    generated = (scrape.get("finished_utc_iso") or
                 dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"))
    return {
        "schema": 1,
        "generated_utc": generated,
        "playlist": str(playlist.relative_to(ROOT)) if playlist.is_relative_to(ROOT) else str(playlist),
        "scrape_run_id": scrape.get("run_id"),
        "health_check_completed": checked,
        "exact_url_evidence_available": checked and isinstance(scrape.get("reachable_event_url_sha256"), list),
        "policy": {
            "minimum_confirmed_feeds": min_feeds,
            "required_confirmed_primaries": 2,
            "required_confirmed_backups": max(1, min_feeds - 2),
            "roles": "first two feeds are primaries; third and later feeds are dedicated backups",
            "minimum_origin_families": min_origins,
            "duplicate_urls_count_once": True,
        },
        "fixture_count": len(fixtures),
        "compliant_count": compliant,
        "deficit_count": len(fixtures) - compliant,
        "fixtures": fixtures,
    }


def render(report: dict) -> str:
    policy = report["policy"]
    lines = [
        "# Live-event reliability audit",
        "",
        f"- **Scrape snapshot:** {report['generated_utc']}",
        f"- **Scrape run:** `{report.get('scrape_run_id') or 'unknown'}` — health check "
        f"{'completed' if report['health_check_completed'] else 'NOT completed'}",
        f"- **Exact-URL evidence:** {'available' if report['exact_url_evidence_available'] else 'unavailable (legacy or incomplete scrape)'}",
        f"- **Policy:** {policy['minimum_confirmed_feeds']} confirmed, distinct feeds per fixture "
        f"(two primaries + one dedicated backup), across at least "
        f"{policy['minimum_origin_families']} origin families",
        f"- **Fixtures meeting policy:** {report['compliant_count']}/{report['fixture_count']}",
        f"- **Fixtures with a redundancy deficit:** {report['deficit_count']}",
        "",
        "> Duplicate URLs count once. Provider labels, origin families, and ingest source files are "
        "reported separately; a mirror of the same feed is never padded into another backup.",
        "",
        "| Fixture | Confirmed feeds | Primaries | Dedicated backup | Origins | Providers | Ingest sources | Result |",
        "|---|---:|---|---|---:|---|---|---|",
    ]
    for item in report["fixtures"]:
        providers = ", ".join(item["providers"]) or "unknown"
        sources = ", ".join(item["ingest_sources"]) or "unknown"
        result = "PASS" if item["policy_met"] else "DEFICIT"
        lines.append(
            f"| {item['title']} ({item['sport']}) | {item['confirmed_feed_count']}/{item['feed_count']} | "
            f"{item['confirmed_primary_count']}/{policy['required_confirmed_primaries']} | "
            f"{item['confirmed_backup_count']}/{policy['required_confirmed_backups']} | "
            f"{len(item['origin_families'])} | "
            f"{providers} | {sources} | **{result}** |"
        )
    if not report["fixtures"]:
        lines.append(
            f"| No live fixtures published | 0 | 0/{policy['required_confirmed_primaries']} | "
            f"0/{policy['required_confirmed_backups']} | 0 | - | - | - |"
        )

    lines += ["", "## Deficits", ""]
    deficits = [item for item in report["fixtures"] if not item["policy_met"]]
    if deficits:
        for item in deficits:
            lines.append(f"- **{item['title']}** — {'; '.join(item['deficits'])}.")
    else:
        lines.append("None. Every published fixture has two confirmed primaries and a dedicated backup.")
    lines += [
        "",
        "## Interpretation",
        "",
        "- `reachable` requires an exact URL hash in the latest completed scrape; it is a point-in-time result, not a playback guarantee.",
        "- Older reports without the hash index and URLs not checked in that run remain `published-not-checked`.",
        "- A provider tag such as `STRMGATE` is provenance metadata, not proof that two URLs are independent.",
        "- The audit reports deficits instead of publishing dead, expired, private-address, or duplicate mirrors to hit a number.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--playlist", type=Path, default=DEFAULT_PLAYLIST)
    parser.add_argument("--scrape-report", type=Path, default=DEFAULT_SCRAPE_REPORT)
    parser.add_argument("--sources-dir", type=Path, default=DEFAULT_SOURCES_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_MARKDOWN)
    parser.add_argument("--json", dest="json_path", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--min-feeds", type=int, default=3)
    parser.add_argument("--min-origins", type=int, default=2)
    parser.add_argument("--strict", action="store_true",
                        help="exit 1 when any active fixture misses the policy")
    args = parser.parse_args(argv)
    if args.min_feeds < 3 or args.min_origins < 1:
        parser.error("--min-feeds must be at least 3 and --min-origins at least 1")

    report = audit(args.playlist, args.scrape_report, args.sources_dir,
                   args.min_feeds, args.min_origins)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.json_path.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(render(report), encoding="utf-8")
    args.json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"[live-events] {report['compliant_count']}/{report['fixture_count']} fixtures meet "
        f"two-primary-plus-backup policy -> {args.out}"
    )
    if report["deficit_count"]:
        print(
            f"::warning title=Live-event redundancy::"
            f"{report['deficit_count']} fixture(s) lack two confirmed primaries plus a dedicated backup."
        )
    return 1 if args.strict and report["deficit_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
