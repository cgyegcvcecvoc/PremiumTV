#!/usr/bin/env python3
"""
PremiumTV1 playlist scraper.

Pulls channel lists from the sources in sources.json (M3U/M3U8 and Wiseplay
W3U JSON), normalises them into one M3U, removes duplicates, checks every
stream link, and writes:

    playlists/PremiumTV.m3u        working links only (the one to load in a player)
    playlists/PremiumTV_all.m3u    everything found, unchecked
    playlists/sources/<name>.m3u   raw copy per source (used as a fallback cache)
    playlists/report.json          machine-readable results of the last run
    playlists/STATUS.md            human-readable summary of the last run

Uses only the Python standard library (3.9+).

    python scripts/scraper.py                  # scrape + check
    python scripts/scraper.py --no-check       # scrape only
    python scripts/scraper.py --label "6 AM recheck"
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import os
import re
import socket
import ssl
import sys
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

# Lenient TLS context: many IPTV hosts have broken/expired certificates, and a
# bad cert doesn't mean the stream itself is down.
INSECURE_CTX = ssl.create_default_context()
INSECURE_CTX.check_hostname = False
INSECURE_CTX.verify_mode = ssl.CERT_NONE


def log(msg: str) -> None:
    print(msg, flush=True)


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
    status: str = "unchecked"                     # alive | dead | unchecked
    reason: str = ""

    @property
    def group(self) -> str:
        return self.attrs.get("group-title", "") or "Other"

    def headers(self) -> dict:
        """HTTP headers a player would send, derived from #EXTVLCOPT / #EXTHTTP lines."""
        h = {"User-Agent": DEFAULT_UA}
        for line in self.extra:
            if line.startswith("#EXTVLCOPT:"):
                key, _, val = line[len("#EXTVLCOPT:"):].partition("=")
                hdr = VLC_OPT_MAP.get(key.strip().lower())
                if hdr and val.strip():
                    h[hdr] = val.strip()
            elif line.startswith("#EXTHTTP:"):
                try:
                    for k, v in json.loads(line[len("#EXTHTTP:"):]).items():
                        h[str(k)] = str(v)
                except ValueError:
                    pass
        return h

    def to_m3u(self) -> str:
        attrs = " ".join(f'{k}="{v}"' for k, v in self.attrs.items() if v is not None)
        head = f"#EXTINF:-1 {attrs},{self.name}" if attrs else f"#EXTINF:-1,{self.name}"
        return "\n".join([head, *self.extra, self.url])


# --------------------------------------------------------------------------- #
# Fetching
# --------------------------------------------------------------------------- #
def http_get(url: str, headers: dict | None = None, timeout: float = 30, retries: int = 2) -> str:
    hdrs = {"User-Agent": DEFAULT_UA, "Accept": "*/*"}
    hdrs.update(headers or {})
    last: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout, context=INSECURE_CTX) as r:
                return r.read().decode("utf-8-sig", errors="replace")
        except Exception as e:  # noqa: BLE001
            last = e
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"GET {url} failed: {last}")


def fetch_source_text(src: dict) -> str:
    """Fetch a source, falling back to the GitHub contents API for GitHub-hosted files."""
    try:
        return http_get(src["url"])
    except Exception as e:  # noqa: BLE001
        gh = src.get("github")
        if not gh:
            raise
        log(f"  direct fetch failed ({e}); trying GitHub API")
        api = (f"https://api.github.com/repos/{gh['repo']}/contents/"
               f"{urllib.parse.quote(gh['path'])}?ref={urllib.parse.quote(gh.get('ref', 'main'))}")
        headers = {"Accept": "application/vnd.github.raw"}
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return http_get(api, headers=headers)


# --------------------------------------------------------------------------- #
# Parsers
# --------------------------------------------------------------------------- #
NON_HTTP_SCHEMES = ("rtmp", "rtmps", "rtsp", "rtp", "udp", "mms", "mmsh", "acestream", "srt")


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
    """Parse an extended M3U. Returns (channels, epg_urls)."""
    channels: list[Channel] = []
    epg: list[str] = []
    cur: Channel | None = None
    pending_extra: list[str] = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#EXTM3U"):
            for k, v in ATTR_RE.findall(line):
                if k in ("url-tvg", "x-tvg-url") and v:
                    epg.extend(u.strip() for u in v.split(",") if u.strip())
            continue
        if line.startswith("#EXTINF"):
            meta, _, name = line.partition(",")
            # A comma can legitimately appear inside quoted attributes, so re-split
            # after the last closing quote when attributes are present.
            if '"' in meta and meta.count('"') % 2:
                idx = line.rfind('",')
                meta, name = line[: idx + 1], line[idx + 2:]
            cur = Channel(name=name.strip() or "Unknown", url="", source=source,
                          attrs=dict(ATTR_RE.findall(meta)), extra=pending_extra)
            pending_extra = []
            continue
        if line.startswith(("#EXTVLCOPT", "#KODIPROP", "#EXTHTTP")):
            (cur.extra if cur else pending_extra).append(line)
            continue
        if line.startswith("#EXTGRP:") and cur is not None:
            cur.attrs.setdefault("group-title", line[len("#EXTGRP:"):].strip())
            continue
        if line.startswith("#"):
            continue
        # A URL line
        if cur is not None:
            cur.url = fix_url(line)
            channels.append(cur)
            cur = None
    return channels, epg


def _match_any(name: str, patterns: list[str], exact: bool) -> bool:
    n = name.strip().lower()
    for p in patterns:
        p = p.strip().lower()
        if (n == p) if exact else (p in n):
            return True
    return False


def parse_w3u(src: dict, root_text: str) -> list[Channel]:
    """Walk a Wiseplay W3U JSON playlist (and its nested groups)."""
    include = src.get("include_groups") or []
    exclude = src.get("exclude_groups") or []
    max_depth = int(src.get("max_depth", 2))
    seen_urls: set[str] = set()
    out: list[Channel] = []

    def walk(data: dict, path: list[str], depth: int) -> None:
        group_title = " / ".join(path) if path else (data.get("name") or src["name"])
        for st in data.get("stations") or []:
            url = fix_url(st.get("url") or "")
            # "embed" stations are web pages rendered in a webview, not streams.
            if not url or str(st.get("embed", "")).lower() == "true":
                continue
            extra = []
            if st.get("userAgent"):
                extra.append(f"#EXTVLCOPT:http-user-agent={st['userAgent']}")
            if st.get("referer"):
                extra.append(f"#EXTVLCOPT:http-referrer={st['referer']}")
            out.append(Channel(
                name=(st.get("name") or "Unknown").strip(), url=url, source=src["name"],
                attrs={"tvg-id": "", "tvg-logo": st.get("image", ""), "group-title": group_title},
                extra=extra,
            ))
        if depth >= max_depth:
            return
        for g in data.get("groups") or []:
            gname = (g.get("name") or "").strip()
            gurl = (g.get("url") or "").strip()
            if not gurl or gurl in seen_urls:
                continue
            if depth == 0 and include and not _match_any(gname, include, exact=True):
                continue
            if exclude and _match_any(gname, exclude, exact=False):
                continue
            seen_urls.add(gurl)
            try:
                child = json.loads(http_get(gurl, retries=1))
            except Exception as e:  # noqa: BLE001
                log(f"    ! group '{gname}' skipped: {e}")
                continue
            walk(child, path + [gname], depth + 1)

    walk(json.loads(root_text), [], 0)
    return out


# --------------------------------------------------------------------------- #
# Link checking
# --------------------------------------------------------------------------- #
def check_channel(ch: Channel, timeout: float) -> Channel:
    """Mark a channel alive/dead by requesting the stream the way a player would."""
    scheme = urllib.parse.urlsplit(ch.url).scheme.lower()
    if scheme in NON_HTTP_SCHEMES:
        # rtmp://, acestream://, etc. can't be probed over HTTP; keep them.
        ch.status, ch.reason = "alive", f"unprobed scheme {scheme}"
        return ch
    if scheme not in ("http", "https"):
        ch.status, ch.reason = "dead", "invalid URL"
        return ch

    headers = ch.headers()
    headers.setdefault("Accept", "*/*")
    for attempt in range(2):
        try:
            req = urllib.request.Request(ch.url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout, context=INSECURE_CTX) as r:
                ctype = (r.headers.get("Content-Type") or "").lower()
                body = r.read(4096)
            head = body.lstrip()[:16]
            if head.startswith(b"#EXTM3U") or head.startswith(b"#EXT"):
                ch.status, ch.reason = "alive", "hls"
            elif body[:1] == b"\x47" or any(t in ctype for t in ("video", "mpegurl", "octet-stream", "audio", "dash")):
                ch.status, ch.reason = "alive", ctype or "stream"
            elif head.startswith(b"<") or "html" in ctype:
                ch.status, ch.reason = "dead", "html page, not a stream"
            elif body:
                ch.status, ch.reason = "alive", ctype or "data"
            else:
                ch.status, ch.reason = "dead", "empty response"
            return ch
        except urllib.error.HTTPError as e:
            ch.status, ch.reason = "dead", f"HTTP {e.code}"
            if e.code < 500:
                return ch
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, ssl.SSLError, OSError) as e:
            ch.status, ch.reason = "dead", type(getattr(e, "reason", e)).__name__
        except Exception as e:  # noqa: BLE001
            ch.status, ch.reason = "dead", type(e).__name__
        time.sleep(1)
    return ch


# --------------------------------------------------------------------------- #
# Output
# --------------------------------------------------------------------------- #
def dedupe(channels: list[Channel]) -> list[Channel]:
    seen: set[str] = set()
    out = []
    for ch in channels:
        key = ch.url.strip()
        if key and key not in seen:
            seen.add(key)
            out.append(ch)
    return out


def sort_key(ch: Channel):
    return (ch.group.lower(), re.sub(r"\W+", "", ch.name.lower()), ch.source)


def write_m3u(path: Path, channels: list[Channel], epg: list[str], title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = "#EXTM3U"
    if epg:
        header += f' x-tvg-url="{",".join(dict.fromkeys(epg))}"'
    lines = [header, f"# {title}"]
    lines += [ch.to_m3u() for ch in channels]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def now_strings() -> tuple[str, str]:
    utc = dt.datetime.now(dt.timezone.utc)
    local = utc.astimezone(NY_TZ) if NY_TZ else utc
    return utc.strftime("%Y-%m-%d %H:%M UTC"), local.strftime("%Y-%m-%d %I:%M %p %Z")


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sources", default=str(ROOT / "sources.json"))
    ap.add_argument("--out", default=str(ROOT / "playlists"))
    ap.add_argument("--no-check", action="store_true", help="skip link checking")
    ap.add_argument("--workers", type=int, default=48)
    ap.add_argument("--timeout", type=float, default=12.0, help="per-link timeout in seconds")
    ap.add_argument("--min-working-ratio", type=float, default=0.03,
                    help="abort without overwriting if fewer than this share of links work")
    ap.add_argument("--label", default="manual run", help="run label shown in STATUS.md")
    args = ap.parse_args()

    out_dir = Path(args.out)
    cache_dir = out_dir / "sources"
    cfg = json.loads(Path(args.sources).read_text(encoding="utf-8"))

    all_channels: list[Channel] = []
    all_epg: list[str] = []
    source_stats: dict[str, dict] = {}

    for src in cfg.get("sources", []):
        if not src.get("enabled", True):
            continue
        name = src["name"]
        cache = cache_dir / f"{name}.m3u"
        stat = {"type": src.get("type", "m3u"), "url": src["url"], "fetched": False, "from_cache": False}
        log(f"[{name}] fetching {src['url']}")
        try:
            text = fetch_source_text(src)
            if src.get("type") == "w3u":
                chans = parse_w3u(src, text)
                epg = []
            else:
                chans, epg = parse_m3u(text, name)
            if not chans:
                raise RuntimeError("source returned 0 channels")
            stat["fetched"] = True
            write_m3u(cache, chans, epg, f"cached copy of source '{name}'")
        except Exception as e:  # noqa: BLE001
            log(f"[{name}] ERROR: {e}")
            stat["error"] = str(e)
            if cache.exists():
                log(f"[{name}] using cached copy from previous run")
                chans, epg = parse_m3u(cache.read_text(encoding="utf-8"), name)
                stat["from_cache"] = True
            else:
                chans, epg = [], []
        stat["found"] = len(chans)
        log(f"[{name}] {len(chans)} entries")
        source_stats[name] = stat
        all_channels.extend(chans)
        all_epg.extend(epg)

    channels = sorted(dedupe(all_channels), key=sort_key)
    log(f"Total unique links: {len(channels)} (from {len(all_channels)} entries)")

    if not channels:
        log("No channels found from any source; leaving existing playlists untouched.")
        return 1

    utc_s, local_s = now_strings()
    write_m3u(out_dir / "PremiumTV_all.m3u", channels, all_epg,
              f"All links (unchecked) - updated {utc_s} ({local_s}) - {args.label}")

    if not args.no_check:
        log(f"Checking {len(channels)} links with {args.workers} workers...")
        t0 = time.time()
        with cf.ThreadPoolExecutor(max_workers=args.workers) as pool:
            futures = [pool.submit(check_channel, ch, args.timeout) for ch in channels]
            for i, _ in enumerate(cf.as_completed(futures), 1):
                if i % 200 == 0:
                    log(f"  ...{i}/{len(channels)}")
        log(f"Checked in {time.time() - t0:.0f}s")
        working = [c for c in channels if c.status == "alive"]
        if len(working) < max(1, args.min_working_ratio * len(channels)):
            # Almost certainly a network problem on the runner, not (nearly) every
            # stream dying at once - don't wipe out the last good playlist.
            log(f"Only {len(working)} links passed the check; that looks like a network "
                f"problem, so the previous PremiumTV.m3u is kept.")
            return 1
    else:
        working = channels

    write_m3u(out_dir / "PremiumTV.m3u", working, all_epg,
              f"Working links - updated {utc_s} ({local_s}) - {args.label}")

    for name, stat in source_stats.items():
        mine = [c for c in channels if c.source == name]
        stat["unique"] = len(mine)
        stat["alive"] = sum(c.status == "alive" for c in mine)
        stat["dead"] = sum(c.status == "dead" for c in mine)

    report = {
        "updated_utc": utc_s,
        "updated_local": local_s,
        "label": args.label,
        "checked": not args.no_check,
        "total_unique": len(channels),
        "working": len(working),
        "sources": source_stats,
        "dead": [
            {"name": c.name, "group": c.group, "source": c.source, "url": c.url, "reason": c.reason}
            for c in channels if c.status == "dead"
        ],
    }
    (out_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    md = [
        "# Playlist status",
        "",
        f"- **Last run:** {local_s} ({utc_s}) — _{args.label}_",
        f"- **Working links:** {len(working)} / {len(channels)} unique"
        + ("" if not args.no_check else " (not checked)"),
        "",
        "| Source | Fetched | Entries | Unique | Working | Dead |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for name, s in source_stats.items():
        fetched = "yes" if s["fetched"] else ("cache" if s["from_cache"] else "**failed**")
        md.append(f"| {name} | {fetched} | {s['found']} | {s['unique']} | {s['alive']} | {s['dead']} |")
    groups: dict[str, int] = {}
    for c in working:
        groups[c.group] = groups.get(c.group, 0) + 1
    md += ["", "## Working links by group", "", "| Group | Links |", "|---|---:|"]
    md += [f"| {g} | {n} |" for g, n in sorted(groups.items(), key=lambda kv: (-kv[1], kv[0]))]
    (out_dir / "STATUS.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    log(f"Done: {len(working)} working / {len(channels)} unique -> {out_dir / 'PremiumTV.m3u'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
