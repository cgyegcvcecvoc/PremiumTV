#!/usr/bin/env python3
"""
PremiumTV1 monthly new-channel discovery engine.

The daily scraper refreshes the sources that are already configured. This engine
looks for *new* channels: it hunts for candidate playlists (seeded candidates
plus public GitHub repositories found through repository search), fetches them,
measures how many links they would actually add to the current playlist, samples
and link-checks those new links, and ranks the candidates by quality.

It never silently changes the published playlist. Good candidates are written to
    playlists/discovery/approved-sources.json
which the regular scraper merges into its source list on the next run (see
`scripts/scraper.py --approved-sources`), so every promotion is visible in
`STATUS.md` and reversible by editing one JSON file.

Outputs (all under --out, default playlists/discovery):
    REPORT.md              human-readable summary of the monthly hunt
    discovery.json         detailed machine-readable results
    new-channels.m3u       new working links found, ready to review in a player
    approved-sources.json  vetted sources for the next regular scrape
    state.json             per-candidate memory (avoids re-testing every month)
    history.jsonl          append-only one-line summary per discovery run

Uses only the Python standard library (3.9+).

    python scripts/discover.py                       # full monthly hunt
    python scripts/discover.py --no-search           # seeds only (no GitHub API)
    python scripts/discover.py --dry-run --max-candidates 5
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
GITHUB_API = "https://api.github.com"
PLAYLIST_SUFFIXES = (".m3u", ".m3u8")
SEARCH_COOLDOWN = 2.0  # be polite to the unauthenticated search rate limit

DEFAULT_SETTINGS = {
    "corpus_playlist": "playlists/PremiumTV_all.m3u",
    "candidates": [],
    "github_search": {
        "enabled": True,
        "queries": [
            "topic:iptv",
            "topic:iptv-playlist",
            "topic:m3u",
            "iptv m3u playlist in:name,description",
            "live tv m3u playlist in:name,description",
        ],
        "max_results_per_query": 10,
        "max_repositories": 20,
        "sort": "updated",
        "min_playlist_bytes": 4096,
        "exclude_owners": [],
    },
    "thresholds": {
        "sample_size": 12,
        "active_source_sample_size": 8,
        "min_new_links": 25,
        "min_working_checked": 3,
        "min_working_ratio": 0.30,
        "min_score": 55.0,
    },
    "auto_promote": True,
    "max_promote_per_run": 2,
    "recheck_after_days": 90,
    "max_new_channels_export": 300,
    "max_report_rows": 40,
    "playlist_path_exclude_regex": r"(?i)(series|movie|vod|adult|xxx|radio|podcast|music|trailer)",
}


def log(message: str) -> None:
    print(message, flush=True)


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
def load_settings(config_path: Path) -> dict:
    """Read sources.json and return the discovery section merged over defaults."""
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        config = {}
    except json.JSONDecodeError as exc:
        raise ValueError(f"{config_path} is not valid JSON: {exc}") from exc
    if not isinstance(config, dict):
        raise ValueError("source configuration root must be a JSON object")

    section = config.get("discovery") or {}
    if not isinstance(section, dict):
        raise ValueError("'discovery' must be a JSON object")
    if not section.get("enabled", True):
        raise ValueError("discovery is disabled in sources.json (discovery.enabled=false)")

    settings = dict(DEFAULT_SETTINGS)
    settings.update({key: value for key, value in section.items() if key not in ("github_search", "thresholds")})
    search = dict(DEFAULT_SETTINGS["github_search"])
    search.update(section.get("github_search") or {})
    thresholds = dict(DEFAULT_SETTINGS["thresholds"])
    thresholds.update(section.get("thresholds") or {})
    settings["github_search"] = search
    settings["thresholds"] = thresholds
    settings["_config"] = config
    settings["_config_dir"] = config_path.resolve().parent
    return settings


def resolve_path(value: str, base: Path) -> Path:
    path = Path(str(value))
    return path if path.is_absolute() else (base / path)


# --------------------------------------------------------------------------- #
# Corpus (what the repository already publishes)
# --------------------------------------------------------------------------- #
def normalized_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (name or "").lower())


class Corpus:
    """The channels the repository already knows about."""

    def __init__(self) -> None:
        self.urls: set[str] = set()
        self.names: set[str] = set()
        self.source = "empty"
        self.channels: int = 0

    @classmethod
    def load(cls, playlist_path: Path) -> "Corpus":
        corpus = cls()
        if not playlist_path.exists():
            corpus.source = "missing"
            return corpus
        try:
            channels, _ = scraper.parse_m3u(playlist_path.read_text(encoding="utf-8"), "corpus")
        except Exception as exc:  # noqa: BLE001
            corpus.source = f"unreadable: {scraper.error_text(exc)}"
            return corpus
        corpus.urls = {channel.url for channel in channels if channel.url}
        corpus.names = {normalized_name(channel.name) for channel in channels if normalized_name(channel.name)}
        corpus.channels = len(channels)
        corpus.source = playlist_path.name
        return corpus


# --------------------------------------------------------------------------- #
# GitHub helpers
# --------------------------------------------------------------------------- #
def github_token() -> str:
    for name in ("DISCOVERY_GITHUB_TOKEN", "GH_TOKEN", "GITHUB_TOKEN"):
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def github_headers() -> dict:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": scraper.DEFAULT_UA,
    }
    token = github_token()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def github_json(url: str, timeout: float = 25.0, retries: int = 1) -> dict:
    data = json.loads(scraper.http_get(url, headers=github_headers(), timeout=timeout, retries=retries))
    if not isinstance(data, dict):
        raise ValueError("GitHub API response is not a JSON object")
    return data


def rate_limit_note(exc: Exception) -> str:
    text = str(exc)
    if "403" in text and "rate limit" in text.lower():
        return "GitHub API rate limit reached; set a DISCOVERY_GITHUB_TOKEN Actions secret to raise it."
    if "429" in text:
        return "GitHub API throttled the request; it will be retried next month or with a token."
    return ""


# --------------------------------------------------------------------------- #
# Candidate discovery
# --------------------------------------------------------------------------- #
def candidate_key(candidate: dict) -> str:
    github = candidate.get("github") or {}
    if github.get("repo"):
        return f"{github['repo']}:{github.get('path') or '*'}"
    return str(candidate.get("url") or candidate.get("name") or "")


def playlist_file_score(path: str, size: int, exclude_re: re.Pattern) -> float:
    low = path.lower()
    score = 0.0
    if "/" in path:
        score -= 1.5
    if re.search(r"(?<![a-z])tv(?![a-z])", low):
        score += 3.0
    if "playlist" in low:
        score += 2.0
    if any(word in low for word in ("all", "world", "global", "country", "countries")):
        score += 1.5
    if low.count("/") == 0:
        score += 1.0
    if exclude_re.search(path):
        score -= 6.0
    score += min(2.0, size / 200_000)
    return score


def pick_playlist_file(entries: list[dict], exclude_re: re.Pattern) -> dict | None:
    blobs = [
        entry for entry in entries
        if entry.get("type") == "blob"
        and str(entry.get("path", "")).lower().endswith(PLAYLIST_SUFFIXES)
        and int(entry.get("size") or 0) >= 4096
    ]
    if not blobs:
        return None
    ranked = sorted(
        blobs,
        key=lambda entry: (-playlist_file_score(entry["path"], int(entry.get("size") or 0), exclude_re),
                           len(entry["path"]), entry["path"]),
    )
    best = ranked[0]
    if playlist_file_score(best["path"], int(best.get("size") or 0), exclude_re) <= 0:
        return None
    return best


def repo_candidate(repository: dict, settings: dict, exclude_re: re.Pattern) -> dict | None:
    """Turn a GitHub repository into a playlist candidate by finding its M3U file."""
    full_name = repository.get("full_name")
    if not full_name:
        return None
    ref = repository.get("default_branch") or "main"
    metadata: dict = {}
    if repository.get("archived"):
        return None
    try:
        metadata = github_json(f"{GITHUB_API}/repos/{full_name}")
    except Exception as exc:  # noqa: BLE001
        log(f"  [{full_name}] repository metadata failed: {scraper.error_text(exc)}")
    if metadata.get("archived"):
        log(f"  [{full_name}] skipped: repository is archived")
        return None
    ref = metadata.get("default_branch") or ref
    tree_url = f"{GITHUB_API}/repos/{full_name}/git/trees/{urllib.parse.quote(ref)}?recursive=1"
    tree = github_json(tree_url).get("tree") or []
    best = pick_playlist_file(tree, exclude_re)
    if not best:
        log(f"  [{full_name}] no usable static playlist file found")
        return None
    path = best["path"]
    log(f"  [{full_name}] playlist candidate: {path} ({int(best.get('size') or 0)} bytes)")
    return {
        "name": metadata.get("name") or full_name.split("/")[-1],
        "type": "m3u",
        "url": f"https://raw.githubusercontent.com/{full_name}/{urllib.parse.quote(ref)}/{urllib.parse.quote(path)}",
        "github": {"repo": full_name, "path": path, "ref": ref},
        "origin": "github_search",
        "repo": full_name,
        "playlist_path": path,
        "bytes": int(best.get("size") or 0),
        "stars": int(metadata.get("stargazers_count") or 0),
        "updated_at": metadata.get("pushed_at") or repository.get("pushed_at") or "",
    }


def search_repositories(query: str, settings: dict) -> list[dict]:
    search = settings["github_search"]
    url = (
        f"{GITHUB_API}/search/repositories?q={urllib.parse.quote(query)}"
        f"&sort={urllib.parse.quote(str(search.get('sort', 'updated')))}&order=desc"
        f"&per_page={int(search.get('max_results_per_query', 10))}"
    )
    items = github_json(url).get("items") or []
    log(f"  search '{query}' -> {len(items)} repositories")
    return items


def collect_candidates(settings: dict, known_repos: set[str], state: dict,
                       use_search: bool, limit: int | None, issues: list[str]) -> list[dict]:
    """Seeded candidates first, then public repositories found through search."""
    exclude_re = re.compile(settings["playlist_path_exclude_regex"])
    candidates: list[dict] = []
    seen: set[str] = set()

    def add(candidate: dict) -> None:
        key = candidate_key(candidate)
        if not key or key in seen:
            return
        repo = (candidate.get("github") or {}).get("repo")
        if repo and repo.lower() in known_repos:
            log(f"  [{candidate.get('name')}] skipped: already an active or known source")
            return
        seen.add(key)
        candidates.append(candidate)

    for item in settings.get("candidates") or []:
        if not isinstance(item, dict):
            issues.append("A discovery candidate entry is not an object; skipped.")
            continue
        if not item.get("enabled", True):
            continue
        candidate = dict(item)
        candidate.setdefault("type", "m3u")
        candidate["origin"] = candidate.get("origin") or "seed"
        if candidate.get("github") and not candidate.get("url"):
            try:
                resolved = repo_candidate({"full_name": candidate["github"]["repo"]}, settings, exclude_re)
            except Exception as exc:  # noqa: BLE001
                message = scraper.error_text(exc)
                issues.append(f"Seeded candidate '{candidate.get('name')}' could not be inspected: {message}")
                log(f"  [{candidate.get('name')}] ERROR: {message}")
                continue
            if not resolved:
                issues.append(
                    f"Seeded candidate '{candidate.get('name')}' has no static playlist file "
                    "(its playlists are generated at runtime, not committed)."
                )
                continue
            # The seed only names the repository; the resolved entry supplies the
            # concrete playlist path and ref that the fetch fallback needs.
            merged = dict(resolved)
            merged.update({key: value for key, value in candidate.items() if key != "github" and value})
            merged["github"] = {**(candidate.get("github") or {}), **(resolved.get("github") or {})}
            merged["origin"] = "seed"
            candidate = merged
        add(candidate)

    search_cfg = settings["github_search"]
    if use_search and search_cfg.get("enabled", True):
        max_repositories = int(search_cfg.get("max_repositories", 20))
        checked = 0
        for query in search_cfg.get("queries") or []:
            if checked >= max_repositories or (limit and len(candidates) >= limit):
                break
            try:
                items = search_repositories(query, settings)
            except Exception as exc:  # noqa: BLE001
                message = scraper.error_text(exc)
                note = rate_limit_note(exc)
                issues.append(f"GitHub search '{query}' failed: {message}")
                log(f"  search '{query}' ERROR: {message}")
                if note:
                    issues.append(note)
                    log(f"  note: {note}")
                if limit is None and checked == 0:
                    continue
                continue
            for item in items:
                if checked >= max_repositories or (limit and len(candidates) >= limit):
                    break
                full_name = (item.get("full_name") or "").lower()
                if not full_name or full_name in known_repos:
                    continue
                if any(full_name == key.split(":")[0].lower() for key in seen):
                    continue
                if (item.get("owner") or {}).get("login", "").lower() in {
                    str(owner).lower() for owner in search_cfg.get("exclude_owners") or []
                }:
                    continue
                try:
                    candidate = repo_candidate(item, settings, exclude_re)
                except Exception as exc:  # noqa: BLE001
                    log(f"  [{item.get('full_name')}] ERROR: {scraper.error_text(exc)}")
                    continue
                if not candidate:
                    continue
                checked += 1
                add(candidate)
            time.sleep(SEARCH_COOLDOWN)

    if limit:
        return candidates[:limit]
    return candidates


# --------------------------------------------------------------------------- #
# Candidate evaluation
# --------------------------------------------------------------------------- #
def host_of(url: str) -> str:
    try:
        return (urllib.parse.urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""


def sample_channels(channels: list[scraper.Channel], limit: int) -> list[scraper.Channel]:
    """Round-robin across hosts so one provider cannot dominate the sample."""
    if limit <= 0 or not channels:
        return []
    by_host: dict[str, list[scraper.Channel]] = collections.OrderedDict()
    for channel in channels:
        by_host.setdefault(host_of(channel.url), []).append(channel)
    picked: list[scraper.Channel] = []
    while len(picked) < limit and any(by_host.values()):
        for host in list(by_host):
            if by_host[host]:
                picked.append(by_host[host].pop(0))
            if len(picked) >= limit:
                break
    return picked


def check_sample(channels: list[scraper.Channel], args) -> dict:
    if not channels:
        return {"checked": 0, "alive": 0, "dead": 0, "unverified": 0, "working_ratio": 0.0, "results": []}
    limiter = scraper.HostLimiter(args.per_host_workers)
    with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(scraper.check_channel, channel, args.timeout, args.retries, limiter): channel
                   for channel in channels}
        for future in cf.as_completed(futures):
            channel = futures[future]
            try:
                future.result()
            except Exception as exc:  # noqa: BLE001
                channel.status, channel.reason = "unverified", f"checker error: {type(exc).__name__}"
    counts = collections.Counter(channel.status for channel in channels)
    checked = len(channels)
    return {
        "checked": checked,
        "alive": counts.get("alive", 0),
        "dead": counts.get("dead", 0),
        "unverified": counts.get("unverified", 0),
        "working_ratio": round(counts.get("alive", 0) / checked, 3) if checked else 0.0,
        "results": [
            {"name": channel.name, "group": channel.group, "status": channel.status,
             "reason": channel.reason, "url": scraper.safe_url(channel.url)}
            for channel in channels
        ],
    }


def score_candidate(result: dict) -> float:
    quality = float(result["sample"]["working_ratio"])
    volume = min(1.0, result["new_links"] / 200.0)
    freshness = float(result["new_name_ratio"])
    return round(100 * (0.55 * quality + 0.25 * volume + 0.20 * freshness), 1)


def evaluate_candidate(candidate: dict, corpus: Corpus, settings: dict, args,
                       issues: list[str]) -> dict:
    thresholds = settings["thresholds"]
    name = str(candidate.get("name") or candidate_key(candidate))
    result = {
        "name": name,
        "key": candidate_key(candidate),
        "origin": candidate.get("origin", "seed"),
        "type": candidate.get("type", "m3u"),
        "url": scraper.safe_url(str(candidate.get("url") or "")),
        "repo": candidate.get("repo") or (candidate.get("github") or {}).get("repo", ""),
        "playlist_path": candidate.get("playlist_path") or (candidate.get("github") or {}).get("path", ""),
        "bytes": candidate.get("bytes"),
        "stars": candidate.get("stars"),
        "updated_at": candidate.get("updated_at", ""),
        "status": "pending",
        "verdict": "reject",
        "reason": "",
        "channels": 0,
        "new_links": 0,
        "duplicate_links": 0,
        "new_names": 0,
        "new_name_ratio": 0.0,
        "score": 0.0,
        "sample": {"checked": 0, "alive": 0, "dead": 0, "unverified": 0, "working_ratio": 0.0, "results": []},
        "new_channel_sample": [],
    }

    try:
        text = scraper.fetch_source_text(dict(candidate))
    except Exception as exc:  # noqa: BLE001
        result["status"] = "fetch_failed"
        result["reason"] = scraper.error_text(exc)
        issues.append(f"Candidate '{name}' could not be fetched: {result['reason']}")
        return result

    if not text.lstrip().startswith("#EXTM3U"):
        result["status"] = "not_a_playlist"
        result["reason"] = "response is not an M3U playlist"
        return result

    try:
        if result["type"] == "w3u":
            channels = scraper.parse_w3u(dict(candidate), text, [])
        else:
            channels, _ = scraper.parse_m3u(text, name)
    except Exception as exc:  # noqa: BLE001
        result["status"] = "parse_failed"
        result["reason"] = scraper.error_text(exc)
        issues.append(f"Candidate '{name}' could not be parsed: {result['reason']}")
        return result

    result["bytes"] = result.get("bytes") or len(text.encode("utf-8"))
    if not channels:
        result["status"] = "empty"
        result["reason"] = "playlist contained 0 channels"
        return result

    unique = scraper.dedupe(channels)
    new_channels = [channel for channel in unique if channel.url not in corpus.urls]
    new_names = {
        normalized_name(channel.name) for channel in unique
        if normalized_name(channel.name) and normalized_name(channel.name) not in corpus.names
    }
    result.update({
        "status": "evaluated",
        "channels": len(unique),
        "new_links": len(new_channels),
        "duplicate_links": len(unique) - len(new_channels),
        "new_names": len(new_names),
        "new_name_ratio": round(len(new_names) / max(1, len(unique)), 3),
    })

    if not new_channels:
        result["status"] = "no_new_links"
        result["reason"] = "every link in this candidate is already in the playlist"
        return result

    result["sample"] = check_sample(
        sample_channels(new_channels, int(thresholds["sample_size"])), args
    )
    result["score"] = score_candidate(result)

    passes_links = result["new_links"] >= int(thresholds["min_new_links"])
    passes_quality = (
        result["sample"]["alive"] >= int(thresholds["min_working_checked"])
        and result["sample"]["working_ratio"] >= float(thresholds["min_working_ratio"])
    )
    if passes_links and passes_quality and result["score"] >= float(thresholds["min_score"]):
        result["verdict"] = "promote"
    elif passes_quality:
        result["verdict"] = "watch"
    else:
        result["verdict"] = "reject"
        missing = []
        if not passes_links:
            missing.append(f"only {result['new_links']} new links (needs {thresholds['min_new_links']})")
        if result["sample"]["alive"] < int(thresholds["min_working_checked"]):
            missing.append(f"{result['sample']['alive']} working in sample (needs {thresholds['min_working_checked']})")
        elif not passes_quality:
            missing.append(
                f"{int(result['sample']['working_ratio'] * 100)}% working sample "
                f"(needs {int(float(thresholds['min_working_ratio']) * 100)}%)"
            )
        result["reason"] = "; ".join(missing) or "below promotion thresholds"
    result["new_channel_sample"] = [
        {"name": channel.name, "group": channel.group, "url": scraper.safe_url(channel.url)}
        for channel in new_channels[:10]
    ]
    return result


# --------------------------------------------------------------------------- #
# Active-source new-channel report
# --------------------------------------------------------------------------- #
def review_active_sources(config: dict, corpus: Corpus, settings: dict, args,
                          issues: list[str]) -> list[dict]:
    """Show which new channels the already-configured sources would add."""
    thresholds = settings["thresholds"]
    output: list[dict] = []
    for index, src in enumerate(config.get("sources") or [], 1):
        if not isinstance(src, dict) or not src.get("enabled", True):
            continue
        name = str(src.get("name") or f"source-{index}")
        entry = {"name": name, "status": "pending", "channels": 0, "new_links": 0,
                 "new_names": 0, "sample": {"checked": 0, "alive": 0, "working_ratio": 0.0},
                 "url": scraper.safe_url(str(src.get("url") or f"${src.get('url_env', '')}")), "reason": ""}
        source_url = scraper.resolve_source_url(src)
        if not source_url:
            entry.update({"status": "not_configured", "reason": "no URL or url_env secret set"})
            output.append(entry)
            continue
        try:
            runtime = dict(src)
            runtime["url"] = source_url
            text = scraper.fetch_source_text(runtime)
            channels, _ = scraper.parse_m3u(text, name)
        except Exception as exc:  # noqa: BLE001
            entry.update({"status": "fetch_failed", "reason": scraper.error_text(exc, source_url)})
            issues.append(f"Active source '{name}' could not be reviewed: {entry['reason']}")
            log(f"[active:{name}] ERROR: {entry['reason']}")
            output.append(entry)
            continue
        unique = scraper.dedupe(channels)
        new_channels = [channel for channel in unique if channel.url not in corpus.urls]
        new_names = {
            normalized_name(channel.name) for channel in unique
            if normalized_name(channel.name) and normalized_name(channel.name) not in corpus.names
        }
        entry.update({
            "status": "ok",
            "channels": len(unique),
            "new_links": len(new_channels),
            "new_names": len(new_names),
        })
        if new_channels and not args.no_check:
            entry["sample"] = check_sample(
                sample_channels(new_channels, int(thresholds["active_source_sample_size"])), args
            )
        output.append(entry)
        log(f"[active:{name}] {len(unique)} channels, {len(new_channels)} new links, "
            f"sample alive {entry['sample'].get('alive', 0)}/{entry['sample'].get('checked', 0)}")
    return output


# --------------------------------------------------------------------------- #
# State and promotions
# --------------------------------------------------------------------------- #
def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        log(f"  ignoring unreadable {path.name}: {exc}")
        return default


def save_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cooldown_active(entry: dict, settings: dict, now: dt.datetime, force: bool) -> bool:
    if force or not isinstance(entry, dict):
        return False
    last = entry.get("last_evaluated_utc")
    verdict = entry.get("verdict")
    if verdict == "promote" or not last:
        return False
    try:
        last_dt = dt.datetime.fromisoformat(str(last).replace("Z", "+00:00"))
    except ValueError:
        return False
    age_days = (now - last_dt).total_seconds() / 86400
    return age_days < float(settings.get("recheck_after_days", 90))


def approved_entry(result: dict, when: str) -> dict:
    entry = {
        "name": result["name"],
        "type": result.get("type", "m3u"),
        "enabled": True,
        "url": result.get("raw_url") or result["url"],
        "promoted_by": "monthly discovery",
        "promoted_utc": when,
        "score": result["score"],
        "new_links": result["new_links"],
        "sample_checked": result["sample"]["checked"],
        "sample_working_ratio": result["sample"]["working_ratio"],
        "note": (f"Auto-promoted by the monthly discovery engine on {when}: {result['new_links']} new links, "
                 f"{result['sample']['alive']}/{result['sample']['checked']} of the sample working, "
                 f"score {result['score']}. Set \"enabled\": false here or delete this entry to roll back."),
    }
    if result.get("repo"):
        entry["github"] = {"repo": result["repo"], "path": result["playlist_path"]}
    return entry


def update_approved(path: Path, promoted: list[dict], when: str) -> tuple[dict, list[str]]:
    """Add vetted sources while preserving manual edits to existing entries."""
    current = load_json(path, {"sources": []})
    if not isinstance(current, dict) or not isinstance(current.get("sources", []), list):
        current = {"sources": []}
    existing = {str(item.get("name")): item for item in current["sources"] if isinstance(item, dict)}
    added: list[str] = []
    for result in promoted:
        name = str(result["name"])
        if name in existing:
            continue
        existing[name] = approved_entry(result, when)
        added.append(name)
    current["sources"] = sorted(existing.values(), key=lambda item: str(item.get("name", "")))
    current["updated_utc"] = when
    current.setdefault("schema_version", 1)
    return current, added


def review_approved(path: Path, args) -> list[dict]:
    """Flag promoted sources whose links stopped working, without disabling them."""
    data = load_json(path, {"sources": []})
    review: list[dict] = []
    for item in data.get("sources", []) if isinstance(data, dict) else []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "unnamed"))
        entry = {"name": name, "enabled": bool(item.get("enabled", True)), "status": "pending",
                 "score": item.get("score"), "working_ratio": None, "promoted_utc": item.get("promoted_utc", ""),
                 "reason": ""}
        if not item.get("enabled", True) or not item.get("url"):
            entry.update({"status": "disabled", "reason": "disabled or no URL configured"})
            review.append(entry)
            continue
        try:
            runtime = dict(item)
            text = scraper.fetch_source_text(runtime)
            channels, _ = scraper.parse_m3u(text, name)
        except Exception as exc:  # noqa: BLE001
            entry.update({"status": "fetch_failed", "reason": scraper.error_text(exc, item.get("url"))})
            review.append(entry)
            continue
        unique = scraper.dedupe(channels)
        if not unique:
            entry.update({"status": "empty", "reason": "playlist contained 0 channels"})
            review.append(entry)
            continue
        sample = check_sample(sample_channels(unique, 6), args)
        entry.update({
            "status": "ok",
            "channels": len(unique),
            "working_ratio": sample["working_ratio"],
        })
        if sample["checked"] and sample["working_ratio"] < 0.1:
            entry["status"] = "degraded"
            entry["reason"] = (f"only {sample['alive']}/{sample['checked']} sampled links work; "
                               f"consider disabling '{name}' in approved-sources.json")
        review.append(entry)
    return review


# --------------------------------------------------------------------------- #
# Reports
# --------------------------------------------------------------------------- #
def percent(value: float | None) -> str:
    return "n/a" if value is None else f"{round(float(value) * 100)}%"


def make_report_markdown(payload: dict) -> str:
    summary = payload["summary"]
    lines = [
        "# Monthly new-channel discovery",
        "",
        f"- **Run:** _{payload['label']}_ (`{payload['run_type']}`; ID `{payload['run_id']}`)",
        f"- **Last run:** {payload['updated_local']} ({payload['updated_utc']})",
        f"- **Outcome:** **{payload['status'].upper()}**",
        f"- **Known channels in the published playlist:** {summary['corpus_channels']} "
        f"from `{summary['corpus_source']}`",
        f"- **Candidates:** {summary['candidates']} "
        f"(evaluated {summary['evaluated']}, promoted {summary['promoted']}, watch {summary['watch']}, "
        f"rejected {summary['rejected']}, skipped {summary['skipped']})",
        f"- **New working links found:** {summary['new_working_links']} "
        f"(from active sources: {summary['active_new_links']})",
        f"- **Sources promoted for the next scrape:** {summary['promoted_names'] or 'none'}",
        "",
        "## Candidate results",
        "",
        "| Candidate | Found via | Channels | New links | Sample working | Score | Verdict |",
        "|---|---|---:|---:|---:|---:|---|",
    ]
    for result in payload["candidates"][: int(payload["settings"]["max_report_rows"])]:
        sample = result["sample"]
        lines.append(
            f"| {result['name']} | {result['origin']} | {result['channels']} | {result['new_links']} | "
            f"{sample['alive']}/{sample['checked']} ({percent(sample['working_ratio'])}) | "
            f"{result['score']} | **{result['verdict']}** |"
        )
        if result.get("reason"):
            lines.append(f"| ↳ {result['reason']} | | | | | | |")
    if not payload["candidates"]:
        lines.append("| _no candidates were evaluated_ | | | | | | |")

    lines += [
        "",
        "## New channels from the active sources",
        "",
        "| Source | Channels | New links | Sample working | Note |",
        "|---|---:|---:|---:|---|",
    ]
    for entry in payload["active_sources"]:
        sample = entry["sample"]
        lines.append(
            f"| {entry['name']} | {entry['channels']} | {entry['new_links']} | "
            f"{sample.get('alive', 0)}/{sample.get('checked', 0)} ({percent(sample.get('working_ratio'))}) | "
            f"{entry.get('reason') or entry['status']} |"
        )
    if not payload["active_sources"]:
        lines.append("| _no active sources reviewed_ | | | | |")

    lines += ["", "## Promoted source health", "", "| Source | Status | Channels | Working sample | Note |",
              "|---|---|---:|---:|---|"]
    for entry in payload.get("approved_review", []):
        lines.append(
            f"| {entry['name']} | {entry['status']} | {entry.get('channels', 0)} | "
            f"{percent(entry.get('working_ratio'))} | {entry.get('reason', '')} |"
        )
    if not payload.get("approved_review"):
        lines.append("| _no promoted sources yet_ | | | | |")

    lines += ["", "## New working channels (sample)", ""]
    sample = payload.get("new_channels", [])
    if sample:
        lines.append(f"{len(sample)} new working links are in "
                     "[`new-channels.m3u`](new-channels.m3u). First 20 by source:")
        lines.append("")
        for channel in sample[:20]:
            lines.append(f"- **{channel['name']}** ({channel['group']}) — {channel['source']}")
    else:
        lines.append("No new working links were confirmed in this run.")

    lines += ["", "## Issues and diagnostics", ""]
    if payload["issues"]:
        lines.extend(f"- {issue}" for issue in payload["issues"][:30])
        if len(payload["issues"]) > 30:
            lines.append(f"- …and {len(payload['issues']) - 30} more; see `discovery.json`.")
    else:
        lines.append("None.")
    lines += [
        "",
        "Promotion is not automatic publication: promoted sources are added to the next regular scrape, "
        "and every link is link-checked there before it can appear in `PremiumTV.m3u`. "
        "Roll back by removing or disabling an entry in `approved-sources.json`.",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def classify_run(label: str) -> str:
    low = label.lower()
    if "discovery" in low or "discover" in low or "monthly" in low:
        return "monthly_discovery"
    return "manual"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", default=str(ROOT / "sources.json"))
    ap.add_argument("--out", default=str(ROOT / "playlists" / "discovery"))
    ap.add_argument("--label", default="monthly new-channel discovery", help="run label shown in reports")
    ap.add_argument("--max-candidates", type=int, default=0,
                    help="evaluate at most this many candidates (0 = all)")
    ap.add_argument("--workers", type=int, default=24, help="maximum concurrent sample checks")
    ap.add_argument("--per-host-workers", type=int, default=2, help="maximum concurrent checks per host")
    ap.add_argument("--timeout", type=float, default=10.0, help="per-link timeout in seconds")
    ap.add_argument("--retries", type=int, default=1, help="retries for transient sample-check failures")
    ap.add_argument("--no-search", action="store_true", help="skip GitHub search; evaluate seeded candidates only")
    ap.add_argument("--no-check", action="store_true", help="skip link checks; report counts only")
    ap.add_argument("--no-promote", action="store_true", help="evaluate and report, but never promote")
    ap.add_argument("--force", action="store_true", help="re-evaluate candidates inside the cooldown")
    ap.add_argument("--dry-run", action="store_true", help="print results without writing files")
    args = ap.parse_args()
    if args.max_candidates < 0 or args.workers < 1 or args.per_host_workers < 1 or args.timeout <= 0:
        ap.error("max-candidates cannot be negative and workers, per-host-workers and timeout must be positive")
    if args.retries < 0:
        ap.error("retries cannot be negative")

    out_dir = Path(args.out)
    started = dt.datetime.now(dt.timezone.utc)
    started_iso = started.isoformat(timespec="seconds").replace("+00:00", "Z")
    run_id = f"discover-{started.strftime('%Y%m%dT%H%M%S')}Z-{os.getpid()}"
    issues: list[str] = []
    candidates: list[dict] = []
    active_sources: list[dict] = []
    approved_review: list[dict] = []
    new_channels: list[dict] = []
    promoted_names: list[str] = []
    promoted_results: list[dict] = []
    counts: collections.Counter = collections.Counter()
    evaluated: list[dict] = []
    settings: dict = dict(DEFAULT_SETTINGS)
    state: dict = {"candidates": {}}
    state_path = out_dir / "state.json"
    approved_path = out_dir / "approved-sources.json"
    corpus = Corpus()
    status = "failed"
    exit_code = 1
    fatal_error = ""

    log(f"[discovery] {run_id} | {args.label} | started={started_iso}")

    try:
        settings = load_settings(Path(args.sources))
        config = settings.pop("_config", {})
        config_dir = settings.pop("_config_dir", ROOT)
        corpus_path = resolve_path(settings["corpus_playlist"], config_dir)
        corpus = Corpus.load(corpus_path)
        log(f"[discovery] corpus: {corpus.channels} channels from {corpus.source}")
        if corpus.source.startswith(("missing", "unreadable")):
            issues.append(
                f"Corpus playlist {corpus_path.name} is {corpus.source}; every candidate looks new. "
                "Check that playlists/PremiumTV_all.m3u is committed."
            )

        if not args.no_check:
            active_sources = review_active_sources(config, corpus, settings, args, issues)
        else:
            log("[discovery] active-source review skipped (--no-check)")

        known_repos = {
            str((item.get("github") or {}).get("repo", "")).lower()
            for item in config.get("sources", []) if isinstance(item, dict)
        }
        known_repos.discard("")
        state_path = out_dir / "state.json"
        state = load_json(state_path, {"candidates": {}})
        if not isinstance(state, dict) or not isinstance(state.get("candidates"), dict):
            state = {"candidates": {}}
        state_candidates = state["candidates"]
        approved_data = load_json(approved_path, {"sources": []})
        approved_names = {
            str(item.get("name")) for item in approved_data.get("sources", []) if isinstance(item, dict)
        }

        limit = args.max_candidates or None
        candidates = collect_candidates(settings, known_repos, state_candidates,
                                        not args.no_search, limit, issues)
        log(f"[discovery] {len(candidates)} candidate playlists to evaluate")

        for index, candidate in enumerate(candidates, 1):
            name = str(candidate.get("name") or candidate_key(candidate))
            key = candidate_key(candidate)
            if name in approved_names:
                log(f"  [{index}/{len(candidates)}] {name}: already promoted; skipping")
                candidates[index - 1] = {
                    "name": name, "key": key, "origin": candidate.get("origin", "seed"),
                    "type": candidate.get("type", "m3u"), "url": scraper.safe_url(str(candidate.get("url", ""))),
                    "repo": candidate.get("repo", ""), "playlist_path": candidate.get("playlist_path", ""),
                    "status": "already_promoted", "verdict": "promote", "reason": "already in approved-sources.json",
                    "channels": 0, "new_links": 0, "duplicate_links": 0, "new_names": 0, "new_name_ratio": 0.0,
                    "score": 0.0, "bytes": candidate.get("bytes"), "stars": candidate.get("stars"),
                    "updated_at": candidate.get("updated_at", ""),
                    "sample": {"checked": 0, "alive": 0, "dead": 0, "unverified": 0, "working_ratio": 0.0,
                               "results": []},
                    "new_channel_sample": [],
                }
                continue
            if cooldown_active(state_candidates.get(key), settings, started, args.force):
                previous = state_candidates[key]
                log(f"  [{index}/{len(candidates)}] {name}: re-checked {previous.get('last_evaluated_utc', 'recently')}"
                    f" with verdict '{previous.get('verdict')}'; skipping until the cooldown expires")
                candidates[index - 1] = {
                    "name": name, "key": key, "origin": candidate.get("origin", "seed"),
                    "type": candidate.get("type", "m3u"), "url": scraper.safe_url(str(candidate.get("url", ""))),
                    "repo": candidate.get("repo", ""), "playlist_path": candidate.get("playlist_path", ""),
                    "status": "skipped_cooldown", "verdict": previous.get("verdict", "reject"),
                    "reason": f"last checked {previous.get('last_evaluated_utc', 'recently')}",
                    "channels": previous.get("channels", 0), "new_links": previous.get("new_links", 0),
                    "duplicate_links": previous.get("duplicate_links", 0), "new_names": previous.get("new_names", 0),
                    "new_name_ratio": previous.get("new_name_ratio", 0.0), "score": previous.get("score", 0.0),
                    "bytes": candidate.get("bytes"), "stars": candidate.get("stars"),
                    "updated_at": candidate.get("updated_at", ""),
                    "sample": {"checked": 0, "alive": 0, "dead": 0, "unverified": 0, "working_ratio": 0.0,
                               "results": []},
                    "new_channel_sample": [],
                }
                continue

            log(f"  [{index}/{len(candidates)}] evaluating {name} ({candidate.get('url')})")
            result = evaluate_candidate(candidate, corpus, settings, args, issues)
            result["raw_url"] = str(candidate.get("url", ""))
            log(f"    -> {result['status']}: {result['channels']} channels, {result['new_links']} new, "
                f"sample {result['sample']['alive']}/{result['sample']['checked']} working, "
                f"score {result['score']} ({result['verdict']})")
            for link in result["sample"].get("results", []):
                if link["status"] == "alive":
                    new_channels.append({
                        "name": link["name"], "group": link["group"], "url": link["url"],
                        "source": result["name"],
                    })
            candidates[index - 1] = result
            state_candidates[key] = {
                "name": result["name"],
                "repo": result.get("repo", ""),
                "url": result["raw_url"],
                "first_seen_utc": state_candidates.get(key, {}).get("first_seen_utc", started_iso),
                "last_evaluated_utc": started_iso,
                "status": result["status"],
                "verdict": result["verdict"],
                "score": result["score"],
                "channels": result["channels"],
                "new_links": result["new_links"],
            }

        approved_review = review_approved(approved_path, args) if not args.no_check else []

        # ---- promote -------------------------------------------------------- #
        promote = settings.get("auto_promote", True) and not args.no_promote and not args.dry_run
        limit_promotions = int(settings.get("max_promote_per_run", 2))
        ranked = sorted(
            (result for result in candidates if result["verdict"] == "promote"),
            key=lambda result: (-result["score"], -result["new_links"]),
        )
        if promote and ranked:
            if limit_promotions <= 0:
                log(f"[discovery] {len(ranked)} candidates qualified but auto-promotion is disabled "
                    "(max_promote_per_run = 0)")
            else:
                for result in ranked[:limit_promotions]:
                    result["promoted"] = True
        elif ranked:
            for result in ranked:
                result["promoted"] = False
                result["reason"] = result["reason"] or "qualifies, but promotion is disabled for this run"

        finished = dt.datetime.now(dt.timezone.utc)
        promoted_results = [result for result in candidates if result.get("promoted")]
        if promoted_results and not args.dry_run:
            approved, added = update_approved(approved_path, promoted_results, started_iso)
            save_json(approved_path, approved)
            promoted_names = added
            log(f"[discovery] promoted: {', '.join(added) if added else 'nothing new'}")
        elif promoted_results:
            promoted_names = [result["name"] for result in promoted_results]
            log(f"[discovery] dry run: would promote {', '.join(promoted_names)}")

        counts = collections.Counter(result["verdict"] for result in candidates)
        evaluated = [result for result in candidates if result.get("status") == "evaluated"]
        status = "success"
        if any(result["status"] in ("fetch_failed", "parse_failed", "not_a_playlist", "empty")
               for result in candidates) or issues:
            status = "warning"
        if not candidates:
            status = "warning"
            issues.append("No candidate playlists were evaluated. Check the discovery configuration "
                          "and GitHub search access.")
        exit_code = 0
    except Exception as exc:  # noqa: BLE001
        fatal_error = scraper.error_text(exc)
        issues.append(f"Fatal discovery error: {fatal_error}")
        log(f"[discovery] FATAL: {fatal_error}")
        status, exit_code = "failed", 1

    finished = dt.datetime.now(dt.timezone.utc)
    updated_utc, updated_local = scraper.now_strings(finished)
    issue_messages = list(dict.fromkeys(issues))
    public_candidates = [
        {key: value for key, value in result.items() if key != "raw_url"} for result in candidates
    ]
    payload = {
        "schema_version": 1,
        "run_id": run_id,
        "label": args.label,
        "run_type": classify_run(args.label),
        "status": status,
        "started_utc_iso": started_iso,
        "finished_utc_iso": finished.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "updated_utc": updated_utc,
        "updated_local": updated_local,
        "duration_seconds": round((finished - started).total_seconds(), 2),
        "settings": {
            "thresholds": settings.get("thresholds", DEFAULT_SETTINGS["thresholds"]),
            "auto_promote": settings.get("auto_promote", True),
            "max_promote_per_run": settings.get("max_promote_per_run", 2),
            "recheck_after_days": settings.get("recheck_after_days", 90),
            "max_report_rows": settings.get("max_report_rows", 40),
            "max_new_channels_export": settings.get("max_new_channels_export", 300),
            "search_enabled": not args.no_search,
        },
        "summary": {
            "corpus_channels": corpus.channels,
            "corpus_source": corpus.source,
            "candidates": len(candidates),
            "evaluated": len(evaluated),
            "promoted": len(promoted_results),
            "watch": counts.get("watch", 0),
            "rejected": counts.get("reject", 0),
            "skipped": sum(1 for result in candidates if result.get("status") in
                           ("skipped_cooldown", "already_promoted")),
            "new_working_links": len(new_channels),
            "active_new_links": sum(entry.get("new_links", 0) for entry in active_sources),
            "promoted_names": promoted_names,
        },
        "candidates": public_candidates,
        "active_sources": active_sources,
        "approved_review": approved_review,
        # discovery.json is a published report: redact credentials, while the
        # exported new-channels.m3u keeps the playable URL.
        "new_channels": [
            {**item, "url": scraper.safe_url(item["url"])} for item in new_channels
        ],
        "issues": issue_messages,
    }

    history_entry = {
        "run_id": run_id,
        "label": args.label,
        "run_type": payload["run_type"],
        "status": status,
        "started_utc": started_iso,
        "finished_utc": payload["finished_utc_iso"],
        "updated_local": updated_local,
        "duration_seconds": payload["duration_seconds"],
        "corpus_channels": corpus.channels,
        "candidates_evaluated": payload["summary"]["evaluated"],
        "promoted": payload["summary"]["promoted_names"],
        "new_working_links": payload["summary"]["new_working_links"],
        "active_new_links": payload["summary"]["active_new_links"],
        "issues": issue_messages[:20],
    }

    if not args.dry_run:
        try:
            out_dir.mkdir(parents=True, exist_ok=True)
            save_json(out_dir / "discovery.json", payload)
            (out_dir / "REPORT.md").write_text(make_report_markdown(payload), encoding="utf-8")
            export_limit = int(settings.get("max_new_channels_export", 300))
            scraper.write_m3u(
                out_dir / "new-channels.m3u",
                [scraper.Channel(item["name"], item["url"], item["source"],
                                 attrs={"group-title": item.get("group", "Discovered")})
                 for item in new_channels[:export_limit]],
                [],
                f"New working channels from monthly discovery - {updated_utc} - {args.label}",
            )
            state["updated_utc"] = started_iso
            state["version"] = 1
            save_json(state_path, state)
            scraper.append_run_history(out_dir / "history.jsonl", history_entry)
        except Exception as exc:  # noqa: BLE001
            log(f"[discovery] ERROR writing reports: {scraper.error_text(exc)}")
            return 1

    ranked_names = ", ".join(
        f"{result['name']}({result['verdict']},{result['score']})" for result in candidates[:10]
    ) or "none"
    log(f"[discovery] finished: status={status}; candidates={len(candidates)}; "
        f"promoted={', '.join(promoted_names) or 'none'}; new working links={len(new_channels)}")
    log(f"[discovery] results: {ranked_names}")
    if fatal_error:
        log(f"[discovery] issue: {fatal_error}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
