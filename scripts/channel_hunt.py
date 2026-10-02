#!/usr/bin/env python3
"""
Targeted hunt for the channels that matter most (Nickelodeon, NickToons, MeTV,
MeTV Toons, ...) instead of hoping a general scrape happens to find them.

The daily scraper merges whatever the public indexes publish. That is good for
coverage but bad for specific channels: if the index entry rots, the channel
silently disappears. This script inverts the process for a short list of
"priority channels" configured in `sources.json`:

1. **Collect** every candidate entry whose name or `tvg-id` matches a target
   channel, from
     * the local corpus (`playlists/PremiumTV_all.m3u`, `playlists/sources/*.m3u`),
     * the upstream index playlists in `sources.json` (fetched fresh), and
     * GitHub code search (`--github-search`, needs `GITHUB_TOKEN`) for public
       M3U files that mention the channel;
2. **Verify** each candidate with the deep checker in `link_check.py` - HLS
   variant resolution plus a real media-segment download, so a playlist that
   answers but serves no video is rejected;
3. **Publish** the survivors to the curated source playlist
   (`playlists/sources/priority-channels.m3u`), which `sources.json` enables as
   a normal source so every scheduled scrape re-checks them.

Only links that actually played during the hunt are written. Nothing is guessed.

    python scripts/channel_hunt.py                       # all configured targets
    python scripts/channel_hunt.py --channel "MeTV Toons" --github-search
    python scripts/channel_hunt.py --report-only         # verify, change nothing
"""
from __future__ import annotations

import argparse
import base64
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_check  # noqa: E402
import scraper  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CORPUS = ["playlists/PremiumTV_all.m3u", "playlists/sources/*.m3u"]
DEFAULT_OUTPUT = "playlists/sources/priority-channels.m3u"
GITHUB_API = "https://api.github.com"
MAX_SEARCH_FILES = 12
MAX_CANDIDATES_PER_CHANNEL = 40


def log(msg: str) -> None:
    print(msg, flush=True)


def normalize(value: str) -> str:
    """Lowercase alphanumeric key used for name matching ("MeTV Toons" -> "metvtoons")."""
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


# --------------------------------------------------------------------------- #
# Candidate collection
# --------------------------------------------------------------------------- #
def alias_regex(alias: str):
    """Case-insensitive regex for an alias, tolerant of spacing ("MeTVToons")."""
    words = re.findall(r"[a-z0-9]+", (alias or "").lower())
    if not words:
        return None
    # Words may be separated by spaces, dots, dashes or the "@region" suffixes
    # used in tvg-ids ("Nickelodeon.us@East").
    return re.compile(r"[\s._@-]*".join(re.escape(word) for word in words) + r"(?![a-z0-9])",
                      re.IGNORECASE)


def entry_matches(name: str, tvg_id: str, aliases: list, excludes: list = None) -> bool:
    """True when a playlist entry is one of the requested channels.

    `excludes` holds the aliases of the *other*, more specific targets so that
    "MeTV Toons" is never collected as a candidate for "MeTV".
    """
    for regex in (excludes or []):
        if regex and (regex.search(name or "") or regex.search(tvg_id or "")):
            return False
    for alias in aliases:
        regex = alias_regex(alias)
        if regex and (regex.search(name or "") or regex.search(tvg_id or "")):
            return True
    return False


def candidates_from_text(text: str, source: str, aliases: list,
                         excludes: list = None) -> list:
    channels, _ = scraper.parse_m3u(text, source)
    found = []
    for channel in channels:
        if not channel.url:
            continue
        if entry_matches(channel.name, channel.attrs.get("tvg-id", ""), aliases, excludes):
            found.append(channel)
    return found


def local_candidates(out_dir: Path, aliases: list, excludes: list = None) -> list:
    """Mine the playlists already in the repo (`<out>/PremiumTV_all.m3u`, sources)."""
    found = []
    seen = set()
    for pattern in DEFAULT_CORPUS:
        relative = pattern[len("playlists/"):] if pattern.startswith("playlists/") else pattern
        if pattern.endswith("*.m3u"):
            paths = sorted((out_dir / relative).parent.glob("*.m3u"))
        else:
            path = out_dir / relative
            paths = [path] if path.exists() else []
        for path in paths:
            if not path.exists():
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for channel in candidates_from_text(text, path.name, aliases, excludes):
                if channel.url in seen:
                    continue
                seen.add(channel.url)
                channel.source_aliases = [f"local:{path.name}"]
                found.append(channel)
    return found


def upstream_candidates(sources: list, aliases: list, timeout: float,
                     excludes: list = None) -> tuple:
    """Mine the configured index playlists for the channel. Returns (channels, notes)."""
    found = []
    seen = set()
    notes: list = []
    for item in sources:
        if not item.get("enabled", True):
            continue
        if str(item.get("type") or "m3u").lower() != "m3u":
            continue
        name = str(item.get("name") or "source")
        local = item.get("local_path")
        text = ""
        if local and (ROOT / local).exists():
            # A source that ships its own cache in the repo (ae-networks, the
            # curated priority list) is read locally instead of re-fetched.
            try:
                text = (ROOT / local).read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                notes.append(f"{name}: could not read {local} ({exc})")
        if not text:
            url = scraper.resolve_source_url(item)
            if not url:
                continue
            try:
                text = scraper.fetch_source_text({"url": url, "type": "m3u",
                                                  "timeout": timeout, "retries": 1})
            except Exception as exc:  # noqa: BLE001 - one bad index is not fatal
                message = f"{name}: {scraper.error_text(exc)}"
                log(f"[hunt] upstream {message}")
                notes.append(message)
                continue
        hits = candidates_from_text(text, name, aliases, excludes)
        for channel in hits:
            if channel.url in seen:
                continue
            seen.add(channel.url)
            channel.source_aliases = [f"upstream:{name}"]
            found.append(channel)
        if hits:
            log(f"[hunt] upstream {name}: {len(hits)} candidate entries")
    return found, notes


def github_api(path: str, token: str, params: dict | None = None, timeout: float = 30) -> dict:
    url = f"{GITHUB_API}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": scraper.DEFAULT_UA,
        **({"Authorization": f"Bearer {token}"} if token else {}),
    })
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", "replace"))


def github_candidates(aliases: list, token: str, limit: int = MAX_SEARCH_FILES,
                   excludes: list = None) -> tuple:
    """Mine public M3U files on GitHub that mention the channel."""
    notes: list = []
    if not token:
        message = "GITHUB_TOKEN not set - skipped GitHub code search"
        log(f"[hunt] {message}")
        return [], [message]
    found = []
    seen_files = set()
    for alias in aliases[:3]:
        query = f'"{alias}" extension:m3u'
        try:
            data = github_api("/search/code", token, {"q": query, "per_page": limit})
        except urllib.error.HTTPError as exc:
            message = f"GitHub code search HTTP {exc.code} for {alias!r}"
            log(f"[hunt] {message}")
            notes.append(message)
            continue
        except Exception as exc:  # noqa: BLE001
            message = f"GitHub code search failed for {alias!r}: {scraper.error_text(exc)}"
            log(f"[hunt] {message}")
            notes.append(message)
            continue
        for item in (data.get("items") or [])[:limit]:
            repo = (item.get("repository") or {}).get("full_name")
            path = item.get("path")
            if not repo or not path or f"{repo}:{path}" in seen_files:
                continue
            seen_files.add(f"{repo}:{path}")
            try:
                blob = github_api(f"/repos/{repo}/contents/{urllib.parse.quote(path)}", token)
            except Exception as exc:  # noqa: BLE001
                message = f"{repo}/{path}: {scraper.error_text(exc)}"
                log(f"[hunt] {message}")
                notes.append(message)
                continue
            if blob.get("encoding") != "base64" or not blob.get("content"):
                continue
            try:
                text = base64.b64decode(blob["content"]).decode("utf-8", "replace")
            except (ValueError, TypeError):
                continue
            hits = candidates_from_text(text, f"github:{repo}", aliases, excludes)
            for channel in hits:
                channel.source_aliases = [f"github:{repo}/{path}"]
                found.append(channel)
            if hits:
                log(f"[hunt] github {repo}/{path}: {len(hits)} candidate entries")
        time.sleep(2)  # stay well inside the code-search rate limit
    if not found and not notes:
        notes.append("GitHub code search returned no M3U file mentioning this channel")
    return found, notes


def dedupe(channels: list) -> list:
    """One entry per URL, preferring the richest metadata (logo, id, headers)."""
    best: dict = {}
    for channel in channels:
        key = channel.url
        score = (len(channel.attrs), len(channel.extra), len(channel.name))
        current = best.get(key)
        if current is None or score > current[0]:
            best[key] = (score, channel)
    return [value[1] for value in best.values()]


# --------------------------------------------------------------------------- #
# Verification and publish
# --------------------------------------------------------------------------- #
def verify_all(channels: list, workers: int, timeout: float, retries: int) -> list:
    host_limiter = scraper.HostLimiter(4)
    results = []
    with cf.ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {
            pool.submit(link_check.verify_link, channel, timeout, retries, True,
                        host_limiter): channel
            for channel in channels
        }
        for future in cf.as_completed(futures):
            channel = futures[future]
            try:
                result = future.result()
            except Exception as exc:  # noqa: BLE001
                result = {"status": "unreachable",
                          "reason": f"checker error: {type(exc).__name__}"}
            result["source"] = (channel.source_aliases or [channel.source])[0]
            result["tvg_id"] = channel.attrs.get("tvg-id", "")
            results.append((channel, result))
    return results


def build_excludes(item: dict, targets: list) -> list:
    """Aliases of the *other* targets that must not be collected for this one.

    A shorter alias is skipped when it is a prefix of the channel it would
    exclude: "MeTV" belongs to the MeTV target, but it also matches every
    "MeTV Toons" entry, and using it would empty that target's candidate pool.
    """
    aliases = [str(item.get("name") or "")] + list(item.get("aliases") or [])
    own_keys = {normalize(alias) for alias in aliases}
    excludes = []
    for other in targets:
        if other is item:
            continue
        for alias in [str(other.get("name") or "")] + list(other.get("aliases") or []):
            alias_key = normalize(alias)
            if alias_key and any(key.startswith(alias_key) for key in own_keys):
                continue
            regex = alias_regex(alias)
            if regex:
                excludes.append(regex)
    return excludes


def stream_country(channel: scraper.Channel) -> str:
    """Country of a channel as its tvg-id states it ("MeTV.us@SD" -> "us")."""
    match = re.match(r"^[A-Za-z0-9._-]+\.([A-Za-z]{2})(?:@|$)",
                     str(channel.attrs.get("tvg-id") or "").strip())
    if match:
        return match.group(1).lower()
    return str(channel.attrs.get("tvg-country") or "").strip().lower()


def is_preferred(channel: scraper.Channel, target: dict) -> bool:
    """True when a candidate belongs to the region the target asks for.

    Without this the Nickelodeon target happily publishes the Brazilian or Czech
    feed, because every regional variant is a legitimate name match.
    """
    wanted = str(target.get("country") or "").strip().lower()
    if not wanted:
        return True
    if stream_country(channel) == wanted:
        return True
    if re.search(rf"(?<![a-z]){re.escape(wanted)}(?![a-z])",
                 channel.name or "", re.IGNORECASE):
        return True
    # Name-only matches such as "Nickelodeon (United States) (720p)".
    wanted_names = {"us": ("united states", "usa"), "uk": ("united kingdom",),
                    "ca": ("canada",), "au": ("australia",)}
    for alias in wanted_names.get(wanted, ()):
        if alias in (channel.name or "").lower():
            return True
    return False


def rank(result: dict) -> tuple:
    """Prefer working links, then segment-verified, then fast responses."""
    return (result.get("status") != "working",
            result.get("segment_ok") is False,
            result.get("elapsed") or 99.0)


def write_curated_playlist(path: Path, entries: list, label: str,
                           utc_s: str, local_s: str) -> None:
    """Write the verified priority channels as a normal M3U source playlist."""
    lines = ["#EXTM3U",
             f"# Priority channels verified by channel_hunt.py - {utc_s} ({local_s}) - {label}",
             "# Every link here was re-verified (HLS variant + media segment) during the "
             "hunt; the daily scrape re-checks them like any other source."]
    for channel in entries:
        lines.append(channel.to_m3u())
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def load_config(config_path: Path) -> dict:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    return config.get("priority_channels") or {}


def write_reports(out_dir: Path, report: dict) -> list:
    checks_dir = out_dir / "checks"
    checks_dir.mkdir(parents=True, exist_ok=True)
    (checks_dir / "channel-hunt.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    lines = [
        "# Priority channel hunt",
        "",
        f"- **Run:** {report['label']} (`{report['run_id']}`)",
        f"- **Started:** {report['started_utc']} | **Finished:** {report['finished_utc']} "
        f"| **Duration:** {report['duration_seconds']}s",
        f"- **Curated source:** `{report['output']}` "
        f"({report['published_count']} verified links)",
        "",
        "| Channel | Candidates | Verified working | Published |",
        "|---|---:|---:|---:|",
    ]
    for target in report["targets"]:
        lines.append(f"| {target['name']} | {target['candidates']} | "
                     f"{target['working']} | {target['published']} |")
    for target in report["targets"]:
        lines += ["", f"## {target['name']}", ""]
        if not target["results"]:
            lines.append("No candidates found.")
            continue
        lines += ["| Status | Channel name | Source | Reason | URL |",
                  "|---|---|---|---|---|"]
        for item in target["results"][:20]:
            lines.append(
                f"| {item['status']} | {item['name'][:48]} | {item['source'][:28]} | "
                f"{item['reason'][:44]} | `{scraper.safe_url(item['url'])[:110]}` |")
    lines.append("")
    (checks_dir / "CHANNEL-HUNT.md").write_text("\n".join(lines), encoding="utf-8")
    return [checks_dir / "channel-hunt.json", checks_dir / "CHANNEL-HUNT.md"]


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", default=str(ROOT / "sources.json"))
    ap.add_argument("--out", default=str(ROOT / "playlists"))
    ap.add_argument("--channel", action="append", default=[],
                    help="only hunt these channel names (default: every configured target)")
    ap.add_argument("--github-search", action="store_true",
                    help="also mine public M3U files found by GitHub code search")
    ap.add_argument("--no-upstream", action="store_true",
                    help="skip fetching configured upstream index playlists")
    ap.add_argument("--report-only", action="store_true",
                    help="verify and report, but do not update the curated playlist")
    ap.add_argument("--workers", type=int, default=24, help="concurrent link checks")
    ap.add_argument("--timeout", type=float, default=10.0, help="per-link timeout")
    ap.add_argument("--retries", type=int, default=1, help="retries for transient failures")
    ap.add_argument("--max-per-channel", type=int, default=4,
                    help="how many verified links to keep per channel")
    ap.add_argument("--label", default="priority channel hunt", help="run label")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = Path(args.out)
    config = load_config(Path(args.sources))
    targets = [item for item in (config.get("targets") or [])
               if item.get("enabled", True)]
    if args.channel:
        wanted = {normalize(name) for name in args.channel}
        targets = [item for item in targets if normalize(item.get("name", "")) in wanted]
    if not targets:
        log("[hunt] no priority channels configured (sources.json -> priority_channels)")
        return 2

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    source_items = json.loads(Path(args.sources).read_text(encoding="utf-8")).get("sources", [])
    started = dt.datetime.now(dt.timezone.utc)

    published: list = []
    target_reports = []
    for item in targets:
        name = str(item.get("name") or "channel")
        # "Nickelodeon (United States)" should still match an entry that is just
        # "Nickelodeon", so the bare name is always an alias too.
        bare_name = re.sub(r"\s*\([^)]*\)", "", name).strip()
        aliases = [name] + ([bare_name] if bare_name and bare_name != name else []) \
            + list(item.get("aliases") or [])
        # "MeTV" must not collect "MeTV Toons" links, so every other target's
        # aliases act as exclusions for this one.
        excludes = build_excludes(item, targets)
        log(f"[hunt] {name}: collecting candidates")
        notes: list = []
        candidates = local_candidates(out_dir, aliases, excludes)
        if not args.no_upstream:
            upstream, upstream_notes = upstream_candidates(source_items, aliases,
                                                           args.timeout, excludes)
            candidates += upstream
            notes += upstream_notes
        if args.github_search:
            github, github_notes = github_candidates(aliases, token,
                                                     MAX_SEARCH_FILES, excludes)
            candidates += github
            notes += github_notes
        candidates = dedupe(candidates)[:MAX_CANDIDATES_PER_CHANNEL]
        log(f"[hunt] {name}: {len(candidates)} unique candidates - verifying")
        verified = verify_all(candidates, args.workers, args.timeout, args.retries)
        # Prefer an exact name/tvg-id match, then the deep-check ranking.
        target_keys = {normalize(alias) for alias in aliases}
        verified.sort(key=lambda pair: (
            not is_preferred(pair[0], item),
            not (normalize(pair[0].name) in target_keys
                 or normalize(pair[0].attrs.get("tvg-id", "")).startswith(normalize(name))),
            *rank(pair[1])))
        working = [(channel, result) for channel, result in verified
                   if result.get("status") == "working"]
        keep_count = int(item.get("max_links") or args.max_per_channel)
        publish_now = bool(working) and not args.report_only
        for channel, _ in working[:keep_count]:
            if "group-title" not in channel.attrs:
                channel.attrs["group-title"] = str(item.get("group") or "Priority")
            channel.source = f"priority:{name}"
            published.append(channel)
        target_reports.append({
            "name": name,
            "country": str(item.get("country") or "").lower(),
            "candidates": len(candidates),
            "notes": notes,
            "working": len(working),
            "published": min(len(working), keep_count) if publish_now else 0,
            "results": [{"name": channel.name, "url": channel.url,
                         "status": result.get("status", ""),
                         "reason": result.get("reason", ""),
                         "source": result.get("source", ""),
                         "segment_ok": result.get("segment_ok"),
                         "elapsed": result.get("elapsed", 0.0)}
                        for channel, result in verified],
        })
        log(f"[hunt] {name}: {len(working)} working of {len(candidates)} candidates; "
            f"keeping {min(len(working), keep_count)}")

    finished = dt.datetime.now(dt.timezone.utc)
    _, local_s = scraper.now_strings(finished)
    utc_s = finished.isoformat(timespec="seconds").replace("+00:00", "Z")
    output = Path(config.get("output") or DEFAULT_OUTPUT)
    if not output.is_absolute():
        # Configured as "playlists/sources/..."; resolve it against the playlists
        # directory the run is working in, so tests never write into the repo.
        relative = str(output)
        if relative.startswith("playlists/"):
            relative = relative[len("playlists/"):]
        output = out_dir / relative
    if published and not args.report_only:
        write_curated_playlist(output, published, args.label, utc_s, local_s)
        log(f"[hunt] wrote {output} ({len(published)} verified links)")
    elif not published:
        log("[hunt] no verified links this run; curated playlist left untouched")

    report = {
        "run_id": f"{started.strftime('%Y%m%dT%H%M%S')}Z-{os.getpid()}",
        "label": args.label,
        "started_utc": started.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "finished_utc": utc_s,
        "duration_seconds": round((finished - started).total_seconds(), 1),
        "output": str(output.relative_to(ROOT)) if str(output).startswith(str(ROOT)) else str(output),
        "published_count": len(published) if not args.report_only else 0,
        "github_search": bool(args.github_search),
        "targets": target_reports,
    }
    for path in write_reports(out_dir, report):
        log(f"[hunt] wrote {path}")
    missing = [item["name"] for item in target_reports if not item["working"]]
    if missing:
        log(f"[hunt] no working link found for: {', '.join(missing)}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
