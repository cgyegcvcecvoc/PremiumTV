#!/usr/bin/env python3
"""
PremiumTV1 playlist scraper.

Fetches configured M3U/M3U8 and Wiseplay W3U sources, merges and deduplicates
channels, checks each HTTP stream, and writes:

    playlists/PremiumTV.m3u        confirmed working links (when checking is enabled)
    playlists/PremiumTV_all.m3u    all links found, including unverified links
    playlists/sources/<name>.m3u   normalized source cache
    playlists/report.json          detailed latest-run report and diagnostics
    playlists/STATUS.md            human-readable latest-run status
    playlists/run-history.jsonl    append-only one-line summary for every run

The report and history are written even when a source fetch or health check
fails, so failed rechecks remain visible and the last good player playlist is
not replaced by a bad run.

Uses only the Python standard library (3.9+).

    python scripts/scraper.py                  # fetch, merge, check, report
    python scripts/scraper.py --no-check       # fetch and merge without checks
    python scripts/scraper.py --label "6 AM recheck"
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import datetime as dt
import email.utils
import json
import os
import re
import socket
import ssl
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
    NY_TZ = ZoneInfo("America/New_York")
except Exception:  # pragma: no cover - zoneinfo missing on very old Pythons
    NY_TZ = None

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')
VLC_OPT_MAP = {
    "http-user-agent": "User-Agent",
    "http-referrer": "Referer",
    "http-referer": "Referer",
    "http-origin": "Origin",
}
NON_HTTP_SCHEMES = ("rtmp", "rtmps", "rtsp", "rtp", "udp", "mms", "mmsh", "acestream", "srt")
SENSITIVE_QUERY_KEYS = {
    "access_token", "api_key", "apikey", "auth", "authorization", "key",
    "password", "pass", "secret", "signature", "sig", "token", "username",
}

# Lenient TLS context: some public stream hosts have broken/expired certificates.
# This is only for availability checks; it does not change how a player connects.
INSECURE_CTX = ssl.create_default_context()
INSECURE_CTX.check_hostname = False
INSECURE_CTX.verify_mode = ssl.CERT_NONE


def log(msg: str) -> None:
    print(msg, flush=True)


def safe_url(url: str) -> str:
    """Redact URL credentials and common secret query parameters for reports/logs."""
    try:
        parsed = urllib.parse.urlsplit(url)
        if not parsed.scheme or not parsed.netloc:
            return url
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
        return url


def error_text(error: Exception, url: str | None = None) -> str:
    text = str(error)
    if url:
        text = text.replace(url, safe_url(url))
    return text


# --------------------------------------------------------------------------- #
# Data model
# --------------------------------------------------------------------------- #
@dataclass
class Channel:
    name: str
    url: str
    source: str
    attrs: dict = field(default_factory=dict)     # tvg-id, tvg-logo, group-title, ...
    extra: list = field(default_factory=list)     # #EXTVLCOPT / #KODIPROP / #EXTHTTP lines
    status: str = "unchecked"                     # alive | dead | unverified | unchecked
    reason: str = ""
    source_aliases: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.source_aliases:
            self.source_aliases = [self.source]

    @property
    def group(self) -> str:
        return self.attrs.get("group-title", "") or "Other"

    def headers(self) -> dict:
        """HTTP headers a player would send, derived from #EXTVLCOPT / #EXTHTTP lines."""
        headers = {"User-Agent": DEFAULT_UA}
        for line in self.extra:
            if line.startswith("#EXTVLCOPT:"):
                key, _, value = line[len("#EXTVLCOPT:"):].partition("=")
                header = VLC_OPT_MAP.get(key.strip().lower())
                if header and value.strip():
                    headers[header] = value.strip()
            elif line.startswith("#EXTHTTP:"):
                try:
                    for key, value in json.loads(line[len("#EXTHTTP:"):]).items():
                        headers[str(key)] = str(value)
                except (TypeError, ValueError):
                    pass
        return headers

    def to_m3u(self) -> str:
        attrs = " ".join(f'{key}="{value}"' for key, value in self.attrs.items() if value is not None)
        head = f"#EXTINF:-1 {attrs},{self.name}" if attrs else f"#EXTINF:-1,{self.name}"
        return "\n".join([head, *self.extra, self.url])


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #
def http_get(url: str, headers: dict | None = None, timeout: float = 30, retries: int = 2) -> str:
    hdrs = {"User-Agent": DEFAULT_UA, "Accept": "*/*"}
    hdrs.update(headers or {})
    last: Exception | None = None
    for attempt in range(max(0, retries) + 1):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout, context=INSECURE_CTX) as response:
                return response.read().decode("utf-8-sig", errors="replace")
        except Exception as exc:  # noqa: BLE001
            last = exc
            if attempt < retries:
                time.sleep(min(2 ** attempt, 4))
    raise RuntimeError(f"GET {safe_url(url)} failed: {error_text(last or RuntimeError('unknown error'), url)}")


def fetch_source_text(src: dict) -> str:
    """Fetch a source, falling back to the GitHub contents API when configured."""
    try:
        text = http_get(src["url"])
        src["_fetch_method"] = "direct"
        return text
    except Exception as exc:  # noqa: BLE001
        github = src.get("github")
        if not github:
            raise
        direct_error = error_text(exc, src["url"])
        src["_fetch_method"] = "github_api_fallback"
        src["_direct_fetch_error"] = direct_error
        log(f"  direct fetch failed ({direct_error}); trying GitHub API")
        api = (
            f"https://api.github.com/repos/{github['repo']}/contents/"
            f"{urllib.parse.quote(github['path'])}?ref={urllib.parse.quote(github.get('ref', 'main'))}"
        )
        headers = {"Accept": "application/vnd.github.raw"}
        # Public playlist repositories work unauthenticated. Only use an
        # explicitly supplied GH_TOKEN here, not the workflow's repo-scoped token.
        token = os.environ.get("GH_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return http_get(api, headers=headers)


# --------------------------------------------------------------------------- #
# Parsers
# --------------------------------------------------------------------------- #
def fix_url(url: str) -> str:
    """Repair common typos found in upstream lists (e.g. 'ttp://host')."""
    url = url.strip()
    low = url.lower()
    if low.startswith(("ttp://", "ttps://")):
        return "h" + url
    if low.startswith("//"):
        return "https:" + url
    return url


def parse_m3u(text: str, source: str) -> tuple[list[Channel], list[str]]:
    """Parse an extended M3U. Returns (channels, EPG URLs)."""
    channels: list[Channel] = []
    epg: list[str] = []
    current: Channel | None = None
    pending_extra: list[str] = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#EXTM3U"):
            for key, value in ATTR_RE.findall(line):
                if key in ("url-tvg", "x-tvg-url") and value:
                    epg.extend(url.strip() for url in value.split(",") if url.strip())
            continue
        if line.startswith("#EXTINF"):
            meta, _, name = line.partition(",")
            # A comma can legitimately appear inside quoted attributes, so re-split
            # after the last closing quote when attributes are present.
            if '"' in meta and meta.count('"') % 2:
                idx = line.rfind('",')
                meta, name = line[:idx + 1], line[idx + 2:]
            current = Channel(
                name=name.strip() or "Unknown",
                url="",
                source=source,
                attrs=dict(ATTR_RE.findall(meta)),
                extra=pending_extra,
            )
            pending_extra = []
            continue
        if line.startswith(("#EXTVLCOPT", "#KODIPROP", "#EXTHTTP")):
            (current.extra if current else pending_extra).append(line)
            continue
        if line.startswith("#EXTGRP:") and current is not None:
            current.attrs.setdefault("group-title", line[len("#EXTGRP:"):].strip())
            continue
        if line.startswith("#"):
            continue
        if current is not None:
            current.url = fix_url(line)
            channels.append(current)
            current = None
    return channels, epg


def _match_any(name: str, patterns: list[str], exact: bool) -> bool:
    normalized = name.strip().lower()
    for pattern in patterns:
        pattern = pattern.strip().lower()
        if normalized == pattern if exact else pattern in normalized:
            return True
    return False


def parse_w3u(src: dict, root_text: str, issues: list[str] | None = None) -> list[Channel]:
    """Walk a Wiseplay W3U JSON playlist and its selected nested groups."""
    include = src.get("include_groups") or []
    exclude = src.get("exclude_groups") or []
    max_depth = int(src.get("max_depth", 2))
    seen_urls: set[str] = set()
    output: list[Channel] = []

    def walk(data: dict, path: list[str], depth: int) -> None:
        group_title = " / ".join(path) if path else (data.get("name") or src["name"])
        for station in data.get("stations") or []:
            url = fix_url(station.get("url") or "")
            # Embed stations are web pages rendered in a webview, not direct streams.
            if not url or str(station.get("embed", "")).lower() == "true":
                continue
            extra = []
            if station.get("userAgent"):
                extra.append(f"#EXTVLCOPT:http-user-agent={station['userAgent']}")
            if station.get("referer"):
                extra.append(f"#EXTVLCOPT:http-referrer={station['referer']}")
            output.append(Channel(
                name=(station.get("name") or "Unknown").strip(),
                url=url,
                source=src["name"],
                attrs={"tvg-id": "", "tvg-logo": station.get("image", ""), "group-title": group_title},
                extra=extra,
            ))
        if depth >= max_depth:
            return
        for group in data.get("groups") or []:
            group_name = (group.get("name") or "").strip()
            group_url = (group.get("url") or "").strip()
            if not group_url or group_url in seen_urls:
                continue
            if depth == 0 and include and not _match_any(group_name, include, exact=True):
                continue
            if exclude and _match_any(group_name, exclude, exact=False):
                continue
            seen_urls.add(group_url)
            try:
                child = json.loads(http_get(group_url, retries=1))
                if not isinstance(child, dict):
                    raise ValueError("nested W3U response is not a JSON object")
            except Exception as exc:  # noqa: BLE001
                message = f"nested group '{group_name}' fetch failed: {error_text(exc, group_url)}"
                log(f"    ! {message}")
                if issues is not None:
                    issues.append(message)
                continue
            walk(child, path + [group_name], depth + 1)

    data = json.loads(root_text)
    if not isinstance(data, dict):
        raise ValueError("W3U root is not a JSON object")
    walk(data, [], 0)
    return output


# --------------------------------------------------------------------------- #
# Reference-source audits
# --------------------------------------------------------------------------- #
def audit_reference_source(item: dict) -> dict:
    """Check a directory/repository that is not itself a static playlist source."""
    name = item.get("name", "unnamed reference")
    kind = item.get("type", "")
    result = {
        "name": name,
        "type": kind,
        "status": "failed",
        "reachable": False,
        "channels_imported": False,
        "note": item.get("note", ""),
    }

    if kind == "website":
        url = item.get("url", "")
        result["url"] = safe_url(url)
        text = http_get(url, timeout=float(item.get("timeout", 20)), retries=0)
        result.update({
            "status": "reachable",
            "reachable": True,
            "response_bytes": len(text.encode("utf-8")),
            "playlist_detected": text.lstrip().startswith("#EXTM3U"),
            "ingest_status": "not_imported",
        })
        return result

    if kind == "github_repo":
        repository = item["repo"]
        # These audits target public repositories. Avoid the workflow's
        # repository-scoped GITHUB_TOKEN so it cannot obscure public-read access.
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        metadata_url = f"https://api.github.com/repos/{repository}"
        metadata = json.loads(http_get(metadata_url, headers=headers, timeout=20, retries=1))
        ref = item.get("ref") or metadata.get("default_branch") or "main"
        tree_url = (
            f"https://api.github.com/repos/{repository}/git/trees/"
            f"{urllib.parse.quote(ref)}?recursive=1"
        )
        tree_data = json.loads(http_get(tree_url, headers=headers, timeout=20, retries=1))
        tree = tree_data.get("tree") or []
        playlist_files = sorted(
            entry.get("path", "") for entry in tree
            if entry.get("type") == "blob"
            and entry.get("path", "").lower().endswith((".m3u", ".m3u8"))
        )
        result.update({
            "status": "reachable",
            "reachable": True,
            "repository": repository,
            "ref": ref,
            "archived": bool(metadata.get("archived", False)),
            "tree_truncated": bool(tree_data.get("truncated", False)),
            "static_playlist_files": playlist_files,
            "ingest_status": "static_playlist_found_not_configured" if playlist_files else "no_static_playlist",
        })
        return result

    raise ValueError(f"unsupported reference-check type: {kind or '(missing)'}")


def audit_reference_sources(items: list[dict], issues: list[str]) -> dict[str, dict]:
    results = {}
    for index, item in enumerate(items, 1):
        if not isinstance(item, dict):
            issues.append(f"Reference check entry {index} is not an object; skipped.")
            continue
        name = item.get("name", "unnamed reference")
        if not item.get("enabled", True):
            results[name] = {"name": name, "status": "disabled", "channels_imported": False}
            log(f"[audit:{name}] disabled")
            continue
        try:
            result = audit_reference_source(item)
            if result["status"] == "reachable":
                summary = result.get("static_playlist_files")
                if summary is not None:
                    archived = "; repository is archived" if result.get("archived") else ""
                    log(f"[audit:{name}] repository reachable; static playlists found: {len(summary)}{archived}")
                else:
                    detected = result.get("playlist_detected", False)
                    log(f"[audit:{name}] website reachable; static_m3u_detected={detected}; channels imported=no")
        except Exception as exc:  # noqa: BLE001
            url = item.get("url")
            message = error_text(exc, url) if url else str(exc)
            result = {
                "name": name,
                "type": item.get("type", ""),
                "status": "failed",
                "reachable": False,
                "channels_imported": False,
                "note": item.get("note", ""),
                "error": message,
            }
            issues.append(f"Reference check '{name}' failed: {message}")
            log(f"[audit:{name}] ERROR: {message}")
        results[name] = result
    return results


# --------------------------------------------------------------------------- #
# Link checking
# --------------------------------------------------------------------------- #
class HostLimiter:
    """Keep a burst of parallel checks from overwhelming any single host."""
    def __init__(self, per_host_workers: int):
        self.per_host_workers = max(1, per_host_workers)
        self._lock = threading.Lock()
        self._semaphores: dict[str, threading.BoundedSemaphore] = {}

    def semaphore_for(self, url: str) -> threading.BoundedSemaphore:
        parsed = urllib.parse.urlsplit(url)
        netloc = parsed.netloc.lower().rsplit("@", 1)[-1]
        key = f"{parsed.scheme.lower()}://{netloc}"
        with self._lock:
            if key not in self._semaphores:
                self._semaphores[key] = threading.BoundedSemaphore(self.per_host_workers)
            return self._semaphores[key]


def _connection_reason(exc: Exception) -> str:
    reason = getattr(exc, "reason", exc)
    if isinstance(reason, str):
        return reason[:120]
    return type(reason).__name__


def _retry_delay(error: urllib.error.HTTPError, attempt: int) -> float:
    retry_after = error.headers.get("Retry-After") if error.headers else None
    if retry_after:
        try:
            return min(10.0, max(0.0, float(retry_after)))
        except ValueError:
            try:
                retry_at = email.utils.parsedate_to_datetime(retry_after)
                if retry_at.tzinfo is None:
                    retry_at = retry_at.replace(tzinfo=dt.timezone.utc)
                seconds = (retry_at - dt.datetime.now(dt.timezone.utc)).total_seconds()
                return min(10.0, max(0.0, seconds))
            except (TypeError, ValueError, OverflowError):
                pass
    return min(2 ** attempt, 8)


def check_channel(
    channel: Channel,
    timeout: float,
    retries: int = 2,
    host_limiter: HostLimiter | None = None,
) -> Channel:
    """Check a stream; transient/access failures are kept distinct from confirmed dead links."""
    try:
        scheme = urllib.parse.urlsplit(channel.url).scheme.lower()
    except ValueError:
        channel.status, channel.reason = "dead", "invalid URL"
        return channel

    if scheme in NON_HTTP_SCHEMES:
        # These schemes cannot be probed by an HTTP GET, so do not label them alive.
        channel.status, channel.reason = "unverified", f"not probed: unsupported scheme {scheme}"
        return channel
    if scheme not in ("http", "https"):
        channel.status, channel.reason = "dead", "invalid URL"
        return channel

    headers = channel.headers()
    headers.setdefault("Accept", "*/*")
    attempts = max(0, retries) + 1

    for attempt in range(attempts):
        try:
            request = urllib.request.Request(channel.url, headers=headers)
            semaphore = host_limiter.semaphore_for(channel.url) if host_limiter else None
            if semaphore:
                semaphore.acquire()
            try:
                with urllib.request.urlopen(request, timeout=timeout, context=INSECURE_CTX) as response:
                    content_type = (response.headers.get("Content-Type") or "").lower()
                    body = response.read(4096)
            finally:
                if semaphore:
                    semaphore.release()

            head = body.lstrip()[:16]
            if head.startswith(b"#EXTM3U") or head.startswith(b"#EXT"):
                channel.status, channel.reason = "alive", "hls"
            elif body[:1] == b"\x47" or any(
                marker in content_type for marker in ("video", "mpegurl", "octet-stream", "audio", "dash")
            ):
                channel.status, channel.reason = "alive", content_type or "stream"
            elif head.startswith(b"<") or "html" in content_type:
                channel.status, channel.reason = "dead", "html page, not a stream"
            elif body:
                channel.status, channel.reason = "alive", content_type or "data"
            else:
                channel.status, channel.reason = "dead", "empty response"
            return channel
        except urllib.error.HTTPError as exc:
            code = exc.code
            try:
                exc.close()
            except Exception:  # noqa: BLE001
                pass
            if code in (401, 403):
                channel.status, channel.reason = "unverified", f"HTTP {code}"
                return channel
            retryable = code in (408, 425, 429) or code >= 500
            if retryable and attempt + 1 < attempts:
                time.sleep(_retry_delay(exc, attempt))
                continue
            channel.status = "unverified" if retryable else "dead"
            channel.reason = f"HTTP {code}"
            return channel
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, ssl.SSLError, OSError) as exc:
            reason = _connection_reason(exc)
            if attempt + 1 < attempts:
                time.sleep(min(2 ** attempt, 8))
                continue
            channel.status, channel.reason = "unverified", reason
            return channel
        except Exception as exc:  # noqa: BLE001
            # Unexpected checker/runtime issues should be visible without treating a
            # potentially good channel as a confirmed dead link.
            channel.status, channel.reason = "unverified", f"checker error: {type(exc).__name__}"
            return channel

    channel.status, channel.reason = "unverified", "check attempts exhausted"
    return channel


# --------------------------------------------------------------------------- #
# Output and diagnostics
# --------------------------------------------------------------------------- #
def dedupe(channels: list[Channel]) -> list[Channel]:
    by_url: dict[str, Channel] = {}
    output: list[Channel] = []
    for channel in channels:
        key = channel.url.strip()
        if not key:
            continue
        existing = by_url.get(key)
        if existing is None:
            by_url[key] = channel
            output.append(channel)
        else:
            existing.source_aliases = list(dict.fromkeys(existing.source_aliases + channel.source_aliases))
    return output


def sort_key(channel: Channel):
    return (channel.group.lower(), re.sub(r"\W+", "", channel.name.lower()), channel.source)


def write_m3u(path: Path, channels: list[Channel], epg: list[str], title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = "#EXTM3U"
    if epg:
        header += f' x-tvg-url="{",".join(dict.fromkeys(epg))}"'
    lines = [header, f"# {title}"]
    lines += [channel.to_m3u() for channel in channels]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def now_strings(when: dt.datetime | None = None) -> tuple[str, str]:
    utc = when or dt.datetime.now(dt.timezone.utc)
    if utc.tzinfo is None:
        utc = utc.replace(tzinfo=dt.timezone.utc)
    utc = utc.astimezone(dt.timezone.utc)
    local = utc.astimezone(NY_TZ) if NY_TZ else utc
    return utc.strftime("%Y-%m-%d %H:%M UTC"), local.strftime("%Y-%m-%d %I:%M %p %Z")


def classify_run(label: str) -> str:
    low = label.lower()
    if "recheck" in low:
        return "recheck"
    if "final" in low:
        return "final_check"
    if "daily" in low or "regular" in low or "3:00 am" in low:
        return "regular_check"
    return "manual"


def source_display_url(src: dict) -> str:
    if src.get("url_env"):
        return f"${src['url_env']}"
    return safe_url(str(src.get("url") or ""))


def resolve_source_url(src: dict) -> str:
    env_name = src.get("url_env")
    if env_name:
        env_value = os.environ.get(env_name, "").strip()
        if env_value:
            return env_value
    return str(src.get("url") or "").strip()


def previous_playlist_index(out_dir: Path) -> tuple[dict[str, Channel], str]:
    for filename in ("PremiumTV_all.m3u", "PremiumTV.m3u"):
        path = out_dir / filename
        if not path.exists():
            continue
        try:
            channels, _ = parse_m3u(path.read_text(encoding="utf-8"), "previous")
            return {channel.url: channel for channel in channels if channel.url}, filename
        except Exception as exc:  # noqa: BLE001
            log(f"Could not read previous {filename} for change tracking: {exc}")
    return {}, "none"


def summarize_changes(channels: list[Channel], previous: dict[str, Channel], baseline: str) -> dict:
    current = {channel.url: channel for channel in channels}
    added_urls = sorted(set(current) - set(previous))
    removed_urls = sorted(set(previous) - set(current))
    sample_limit = 20
    return {
        "baseline": baseline,
        "added_count": len(added_urls),
        "removed_count": len(removed_urls),
        "added_sample": [
            {"name": current[url].name, "group": current[url].group,
             "source": current[url].source, "url": safe_url(url)}
            for url in added_urls[:sample_limit]
        ],
        "removed_sample": [
            {"name": previous[url].name, "group": previous[url].group,
             "source": previous[url].source, "url": safe_url(url)}
            for url in removed_urls[:sample_limit]
        ],
    }


def diagnostic_for_reason(reason: str) -> str:
    if reason in ("HTTP 401", "HTTP 403"):
        return "Access denied, authentication, referrer, or geo restrictions may be involved; verify the source headers and test from the intended region."
    if reason == "HTTP 404" or reason == "HTTP 410":
        return "The upstream path is missing or expired; check the source playlist and replace the URL if the publisher has a current one."
    if reason == "HTTP 429":
        return "The host rate-limited the check; this scraper now limits parallel requests per host and retries with Retry-After/backoff."
    if reason.startswith("HTTP 5") or reason in ("HTTP 408", "HTTP 425"):
        return "The upstream server or gateway returned a temporary error; review it on the next scheduled check before removing the source link."
    if any(word in reason.lower() for word in ("timeout", "timed out", "gaierror", "ssl", "tls", "connection", "network")):
        return "Likely transient DNS, TLS, connection, or network trouble; compare the next run and test from another network."
    if reason == "html page, not a stream":
        return "The URL returned a web page rather than media; the source may need a direct stream URL or player-specific redirect."
    if reason.startswith("not probed:"):
        return "This scheme cannot be validated with HTTP; it is retained in the all-links playlist but is not advertised as confirmed working."
    if reason == "empty response":
        return "The server returned no stream data; check whether the source requires an active session or has expired."
    return "Inspect the channel URL and source entry in report.json; this result was not confirmed as playable."


def reason_diagnostics(channels: list[Channel]) -> list[dict]:
    by_reason: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for channel in channels:
        if channel.status in ("dead", "unverified"):
            by_reason[channel.reason][channel.status] += 1
    output = []
    for reason, counts in sorted(by_reason.items(), key=lambda item: (-sum(item[1].values()), item[0])):
        output.append({
            "reason": reason,
            "dead": counts.get("dead", 0),
            "unverified": counts.get("unverified", 0),
            "count": sum(counts.values()),
            "guidance": diagnostic_for_reason(reason),
        })
    return output


def report_channel(channel: Channel) -> dict:
    return {
        "name": channel.name,
        "group": channel.group,
        "source": channel.source,
        "sources": channel.source_aliases,
        "url": safe_url(channel.url),
        "status": channel.status,
        "reason": channel.reason,
    }


def count_source_results(source_stats: dict[str, dict], channels: list[Channel], all_channels: list[Channel]) -> None:
    entries_by_source: collections.Counter = collections.Counter()
    urls_by_source: dict[str, set[str]] = collections.defaultdict(set)
    for channel in all_channels:
        entries_by_source[channel.source] += 1
        urls_by_source[channel.source].add(channel.url)
    status_by_url = {channel.url: channel.status for channel in channels}

    for name, stat in source_stats.items():
        urls = urls_by_source.get(name, set())
        stat["found"] = entries_by_source.get(name, 0)
        stat["unique"] = len(urls)
        stat["overlap"] = sum(
            1 for channel in channels
            if channel.url in urls and len(channel.source_aliases) > 1
        )
        stat["alive"] = sum(status_by_url.get(url) == "alive" for url in urls)
        stat["dead"] = sum(status_by_url.get(url) == "dead" for url in urls)
        stat["unverified"] = sum(status_by_url.get(url) == "unverified" for url in urls)
        stat["unchecked"] = sum(status_by_url.get(url) == "unchecked" for url in urls)
        stat["checked"] = stat["alive"] + stat["dead"] + stat["unverified"]


def make_status_markdown(report: dict) -> str:
    checked = report["checked"]
    if checked:
        link_summary = (
            f"- **Confirmed working:** {report['working']} / {report['total_unique']} unique links\n"
            f"- **Dead:** {report['dead_count']}  |  **Unverified:** {report['unverified_count']}"
        )
    else:
        link_summary = (
            "- **Link check:** not completed in this run; the existing player playlist was left untouched.\n"
            f"- **All-links entries:** {report['total_unique']} (not checked)"
        )

    lines = [
        "# Scraper status",
        "",
        f"- **Last run:** {report['updated_local']} ({report['updated_utc']})",
        f"- **Run:** _{report['label']}_ (`{report['run_type']}`; ID `{report['run_id']}`)",
        f"- **Outcome:** **{report['status'].upper()}**",
        link_summary,
        f"- **Unique links found:** {report['total_unique']} from {report['total_input_entries']} source entries",
        f"- **Changes vs. {report['changes'].get('baseline', 'previous playlist')}:** "
        f"+{report['changes'].get('added_count', 0)} added / -{report['changes'].get('removed_count', 0)} removed",
        f"- **Player playlist updated:** {'yes' if report['final_playlist_written'] else 'no (previous good copy preserved or no output)'}",
        f"- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)",
        "",
        "## Playlist sources",
        "",
        "| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, stat in report["sources"].items():
        lines.append(
            f"| {name} | {stat.get('status', 'unknown')} | {stat.get('found', 0)} | "
            f"{stat.get('unique', 0)} | {stat.get('overlap', 0)} | {stat.get('alive', 0)} | "
            f"{stat.get('dead', 0)} | {stat.get('unverified', 0)} |"
        )
    lines += [
        "",
        "## Reference-source checks (not automatically imported)",
        "",
        "| Reference | Check | Playlist files | Note |",
        "|---|---|---:|---|",
    ]
    for name, result in report["reference_checks"].items():
        playlists = result.get("static_playlist_files", [])
        note = result.get("note", "").replace("|", "\\|")
        if result.get("archived"):
            note = f"{note} (repository is archived)".strip()
        if result.get("error"):
            note = f"{note} — {result['error']}".strip(" —")
        lines.append(f"| {name} | {result.get('status', 'unknown')} | {len(playlists)} | {note} |")
    lines += ["", "## Diagnostics", ""]
    if report["diagnostics"]:
        lines += [
            "| Result | Dead | Unverified | What to check next |",
            "|---|---:|---:|---|",
        ]
        for item in report["diagnostics"]:
            guidance = item["guidance"].replace("|", "\\|")
            lines.append(
                f"| {item['reason']} | {item['dead']} | {item['unverified']} | {guidance} |"
            )
    elif not report["checked"]:
        lines.append("No completed link-check results were recorded for this run.")
    else:
        lines.append("No link-check failures or unverified links were reported.")
    lines += ["", "### Run/source issues", ""]
    if report["issues"]:
        lines.extend(f"- {issue}" for issue in report["issues"][:30])
        if len(report["issues"]) > 30:
            lines.append(f"- …and {len(report['issues']) - 30} more; see `report.json`.")
    else:
        lines.append("None.")
    return "\n".join(lines) + "\n"


def append_run_history(path: Path, entry: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", default=str(ROOT / "sources.json"))
    ap.add_argument("--out", default=str(ROOT / "playlists"))
    ap.add_argument("--no-check", action="store_true", help="skip link checking")
    ap.add_argument("--workers", type=int, default=48, help="maximum concurrent link checks")
    ap.add_argument("--per-host-workers", type=int, default=4, help="maximum concurrent checks per host")
    ap.add_argument("--timeout", type=float, default=12.0, help="per-link timeout in seconds")
    ap.add_argument("--retries", type=int, default=2, help="retries for transient link-check failures")
    ap.add_argument("--min-working-ratio", type=float, default=0.03,
                    help="abort publishing if fewer than this share of links are confirmed working")
    ap.add_argument("--label", default="manual run", help="run label shown in reports")
    args = ap.parse_args()
    if args.workers < 1 or args.per_host_workers < 1 or args.timeout <= 0 or args.retries < 0:
        ap.error("workers, per-host-workers and timeout must be positive; retries cannot be negative")
    if args.min_working_ratio < 0:
        ap.error("min-working-ratio cannot be negative")

    out_dir = Path(args.out)
    cache_dir = out_dir / "sources"
    started = dt.datetime.now(dt.timezone.utc)
    started_utc_iso = started.isoformat(timespec="seconds").replace("+00:00", "Z")
    run_id = f"{started.strftime('%Y%m%dT%H%M%S')}Z-{os.getpid()}"
    run_type = classify_run(args.label)

    source_stats: dict[str, dict] = {}
    reference_checks: dict[str, dict] = {}
    source_issues: list[str] = []
    all_channels: list[Channel] = []
    channels: list[Channel] = []
    working: list[Channel] = []
    all_epg: list[str] = []
    changes = {"baseline": "none", "added_count": 0, "removed_count": 0,
               "added_sample": [], "removed_sample": []}
    checked = False
    check_completed = False
    final_playlist_written = False
    all_playlist_written = False
    status = "failed"
    exit_code = 1
    fatal_error = ""
    started_check = False

    log(f"[run] {run_id} | {args.label} | type={run_type} | started={started_utc_iso}")

    try:
        config_path = Path(args.sources)
        config = json.loads(config_path.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError("source configuration root must be a JSON object")
        source_items = config.get("sources", [])
        if not isinstance(source_items, list):
            raise ValueError("'sources' must be a JSON array")

        for index, src in enumerate(source_items, 1):
            if not isinstance(src, dict):
                source_issues.append(f"Source entry {index} is not an object; skipped.")
                continue
            name = str(src.get("name") or f"source-{index}")
            source_stats[name] = {
                "type": src.get("type", "m3u"),
                "url": source_display_url(src),
                "fetched": False,
                "from_cache": False,
                "status": "pending",
                "found": 0,
                "unique": 0,
                "overlap": 0,
                "alive": 0,
                "dead": 0,
                "unverified": 0,
                "unchecked": 0,
                "checked": 0,
                "issues": [],
            }

        reference_items = config.get("reference_checks", [])
        if not isinstance(reference_items, list):
            source_issues.append("'reference_checks' must be a JSON array; reference checks skipped.")
            reference_items = []
        reference_checks = audit_reference_sources(reference_items, source_issues)

        for index, src in enumerate(source_items, 1):
            if not isinstance(src, dict):
                continue
            name = str(src.get("name") or f"source-{index}")
            stat = source_stats[name]
            if not src.get("enabled", True):
                stat["status"] = "disabled"
                log(f"[{name}] disabled")
                continue

            source_url = resolve_source_url(src)
            if not source_url:
                env_name = src.get("url_env")
                message = f"Set {env_name} to a playlist URL" if env_name else "No source URL configured"
                if src.get("optional", False):
                    stat["status"] = "not_configured"
                    stat["note"] = message
                    log(f"[{name}] not configured (optional): {message}")
                else:
                    stat["status"] = "failed"
                    stat["error"] = message
                    stat["issues"].append(message)
                    source_issues.append(f"[{name}] {message}")
                    log(f"[{name}] ERROR: {message}")
                continue

            source_type = str(src.get("type") or "m3u").lower()
            if source_type not in ("m3u", "w3u"):
                message = f"Unsupported playlist type '{source_type}'"
                stat["status"] = "failed"
                stat["error"] = message
                stat["issues"].append(message)
                source_issues.append(f"[{name}] {message}")
                log(f"[{name}] ERROR: {message}")
                continue

            cache = cache_dir / f"{name}.m3u"
            stat["url"] = source_display_url(src)
            log(f"[{name}] fetching {stat['url']} ({source_type})")
            runtime_source = dict(src)
            runtime_source["url"] = source_url
            parse_issues: list[str] = []
            try:
                text = fetch_source_text(runtime_source)
                stat["fetch_method"] = runtime_source.get("_fetch_method", "direct")
                if runtime_source.get("_direct_fetch_error"):
                    fallback_note = (
                        "Direct URL fetch failed; GitHub API fallback succeeded: "
                        + runtime_source["_direct_fetch_error"]
                    )
                    stat["issues"].append(fallback_note)
                    source_issues.append(f"[{name}] {fallback_note}")
                if source_type == "w3u":
                    fetched_channels = parse_w3u(runtime_source, text, parse_issues)
                    epg = []
                else:
                    fetched_channels, epg = parse_m3u(text, name)
                if not fetched_channels:
                    raise RuntimeError("source returned 0 channels")
                stat["bytes"] = len(text.encode("utf-8"))
                stat["issues"].extend(parse_issues)
                write_m3u(cache, fetched_channels, epg, f"cached copy of source '{name}'")
                stat["fetched"] = True
                stat["status"] = "ok"
                fetched_from = "source"
            except Exception as exc:  # noqa: BLE001
                message = error_text(exc, source_url)
                stat["error"] = message
                stat["issues"].append(message)
                source_issues.append(f"[{name}] fetch/parse failed: {message}")
                log(f"[{name}] ERROR: {message}")
                fetched_from = "none"
                if cache.exists():
                    try:
                        log(f"[{name}] using cached copy from previous run")
                        fetched_channels, epg = parse_m3u(cache.read_text(encoding="utf-8"), name)
                        stat["from_cache"] = True
                        stat["status"] = "from_cache"
                        fetched_from = "cache"
                    except Exception as cache_exc:  # noqa: BLE001
                        cache_message = f"cache parse failed: {error_text(cache_exc)}"
                        stat["issues"].append(cache_message)
                        source_issues.append(f"[{name}] {cache_message}")
                        fetched_channels, epg = [], []
                        stat["status"] = "failed"
                else:
                    fetched_channels, epg = [], []
                    stat["status"] = "failed"

            stat["found"] = len(fetched_channels)
            if parse_issues and fetched_from == "source":
                source_issues.extend(f"[{name}] {issue}" for issue in parse_issues)
            all_channels.extend(fetched_channels)
            all_epg.extend(epg)
            log(f"[{name}] {len(fetched_channels)} entries ({stat['status']})")

        channels = sorted(dedupe(all_channels), key=sort_key)
        log(f"[sources] {len(channels)} unique links from {len(all_channels)} entries")

        if not channels:
            fatal_error = "No channels found from any configured playlist source; existing playlists were left untouched."
            source_issues.append(fatal_error)
            log(f"[run] ERROR: {fatal_error}")
            status, exit_code = "failed", 1
        else:
            previous, baseline = previous_playlist_index(out_dir)
            changes = summarize_changes(channels, previous, baseline)
            utc_s, local_s = now_strings()
            write_m3u(
                out_dir / "PremiumTV_all.m3u", channels, all_epg,
                f"All links (unchecked) - updated {utc_s} ({local_s}) - {args.label}",
            )
            all_playlist_written = True

            if args.no_check:
                # Keep the checked player playlist intact. Unchecked links are
                # available in PremiumTV_all.m3u instead.
                has_source_problem = any(
                    stat.get("status") in ("failed", "from_cache") or stat.get("issues")
                    for stat in source_stats.values()
                )
                has_audit_problem = any(
                    result.get("status") == "failed" for result in reference_checks.values()
                )
                status = "warning" if (has_source_problem or has_audit_problem) else "unchecked"
                exit_code = 0
                log("[links] checking skipped by --no-check; existing PremiumTV.m3u left untouched")
            else:
                started_check = True
                log(f"[links] checking {len(channels)} unique links with {args.workers} workers "
                    f"({args.per_host_workers} per host, timeout={args.timeout:g}s, retries={args.retries})")
                check_start = time.monotonic()
                limiter = HostLimiter(args.per_host_workers)
                with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
                    futures = {
                        pool.submit(check_channel, channel, args.timeout, args.retries, limiter): channel
                        for channel in channels
                    }
                    for index, future in enumerate(cf.as_completed(futures), 1):
                        channel = futures[future]
                        try:
                            future.result()
                        except Exception as exc:  # noqa: BLE001
                            channel.status = "unverified"
                            channel.reason = f"checker error: {type(exc).__name__}"
                        if index % 200 == 0:
                            log(f"  ...{index}/{len(channels)}")
                check_completed = True
                checked = True
                log(f"[links] checks completed in {time.monotonic() - check_start:.1f}s")
                working = [channel for channel in channels if channel.status == "alive"]
                minimum_working = max(1, args.min_working_ratio * len(channels))
                if len(working) < minimum_working:
                    fatal_error = (
                        f"Only {len(working)} of {len(channels)} links passed; the minimum is "
                        f"{minimum_working:.1f}. Keeping the previous PremiumTV.m3u."
                    )
                    source_issues.append(fatal_error)
                    log(f"[run] WARNING: {fatal_error}")
                    status, exit_code = "failed", 1
                else:
                    write_m3u(
                        out_dir / "PremiumTV.m3u", working, all_epg,
                        f"Working links - updated {utc_s} ({local_s}) - {args.label}",
                    )
                    final_playlist_written = True
                    has_source_problem = any(
                        stat.get("status") in ("failed", "from_cache") or stat.get("issues")
                        for stat in source_stats.values()
                    )
                    has_audit_problem = any(
                        result.get("status") == "failed" for result in reference_checks.values()
                    )
                    has_link_problem = any(channel.status in ("dead", "unverified") for channel in channels)
                    status = "warning" if (has_source_problem or has_audit_problem or has_link_problem) else "success"
                    exit_code = 0

        if status not in ("failed", "warning", "success", "unchecked"):
            status = "failed"
            exit_code = 1
    except Exception as exc:  # noqa: BLE001
        fatal_error = error_text(exc)
        source_issues.append(f"Fatal scraper error: {fatal_error}")
        log(f"[run] FATAL: {fatal_error}")
        status, exit_code = "failed", 1

    finished = dt.datetime.now(dt.timezone.utc)
    updated_utc, updated_local = now_strings(finished)
    finished_utc_iso = finished.isoformat(timespec="seconds").replace("+00:00", "Z")
    count_source_results(source_stats, channels, all_channels)
    reason_details = reason_diagnostics(channels)
    status_counts = collections.Counter(channel.status for channel in channels)
    issue_messages = list(dict.fromkeys(source_issues))
    if status_counts.get("unverified", 0):
        issue_messages.append(
            f"{status_counts['unverified']} links could not be confirmed after retries (see unverified details)."
        )
    if status_counts.get("dead", 0):
        issue_messages.append(f"{status_counts['dead']} links returned a confirmed failure (see dead details).")
    issue_messages = list(dict.fromkeys(issue_messages))

    report = {
        "schema_version": 2,
        "run_id": run_id,
        "started_utc_iso": started_utc_iso,
        "finished_utc_iso": finished_utc_iso,
        "updated_utc": updated_utc,
        "updated_local": updated_local,
        "label": args.label,
        "run_type": run_type,
        "status": status,
        "checked": checked,
        "check_started": started_check,
        "check_completed": check_completed,
        "total_input_entries": len(all_channels),
        "total_unique": len(channels),
        "working": status_counts.get("alive", 0) if checked else None,
        "dead_count": status_counts.get("dead", 0),
        "unverified_count": status_counts.get("unverified", 0),
        "unchecked_count": status_counts.get("unchecked", 0),
        "published": len(working) if final_playlist_written else None,
        "final_playlist_written": final_playlist_written,
        "all_playlist_written": all_playlist_written,
        "duration_seconds": round((finished - started).total_seconds(), 2),
        "changes": changes,
        "sources": source_stats,
        "reference_checks": reference_checks,
        "issues": issue_messages,
        "diagnostics": reason_details,
        "dead": [report_channel(channel) for channel in channels if channel.status == "dead"],
        "unverified": [report_channel(channel) for channel in channels if channel.status == "unverified"],
    }

    history_entry = {
        "run_id": run_id,
        "started_utc": started_utc_iso,
        "finished_utc": finished_utc_iso,
        "updated_local": updated_local,
        "label": args.label,
        "run_type": run_type,
        "status": status,
        "exit_code": exit_code,
        "checked": checked,
        "check_completed": check_completed,
        "duration_seconds": round((finished - started).total_seconds(), 2),
        "final_playlist_written": final_playlist_written,
        "total_input_entries": len(all_channels),
        "total_unique": len(channels),
        "working": status_counts.get("alive", 0) if checked else None,
        "dead": status_counts.get("dead", 0),
        "unverified": status_counts.get("unverified", 0),
        "added": changes.get("added_count", 0),
        "removed": changes.get("removed_count", 0),
        "sources": {
            name: {
                key: stat.get(key)
                for key in ("status", "found", "unique", "alive", "dead", "unverified", "error")
                if key in stat
            }
            for name, stat in source_stats.items()
        },
        "reference_checks": {
            name: {
                key: result.get(key)
                for key in ("status", "reachable", "playlist_detected", "static_playlist_files", "ingest_status")
                if key in result
            }
            for name, result in reference_checks.items()
        },
        "issue_reasons": {item["reason"]: item["count"] for item in reason_details},
        "issues": issue_messages[:20],
    }

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        # Prioritize the append-only audit trail before refreshing the snapshots.
        append_run_history(out_dir / "run-history.jsonl", history_entry)
        (out_dir / "report.json").write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (out_dir / "STATUS.md").write_text(make_status_markdown(report), encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        log(f"[report] ERROR writing run diagnostics: {error_text(exc)}")
        return 1

    log(
        f"[run] finished: status={status}; checked={checked}; unique={len(channels)}; "
        f"working={status_counts.get('alive', 0)}; dead={status_counts.get('dead', 0)}; "
        f"unverified={status_counts.get('unverified', 0)}; "
        f"added={changes.get('added_count', 0)}; removed={changes.get('removed_count', 0)}"
    )
    log(f"[report] {out_dir / 'STATUS.md'} | {out_dir / 'report.json'} | {out_dir / 'run-history.jsonl'}")
    if status == "warning":
        log("::warning title=Scraper diagnostics::This run completed with source or link issues; see STATUS.md and report.json.")
    if fatal_error:
        log(f"[run] issue: {fatal_error}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
