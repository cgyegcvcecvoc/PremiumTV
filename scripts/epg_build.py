#!/usr/bin/env python3
"""Build one merged, filtered XMLTV guide for the published playlists.

Players load every URL in a playlist's ``x-tvg-url`` header - today that is
90+ separate guides, each with its own channel-id namespace, most of which do
not match the ids the playlists actually use. The result is a guide grid that
is mostly empty and impossible to filter, because the events that *do* load
belong to channels that are not in the playlist.

This script fixes that by publishing **one** guide, in this repository, that is
built from exactly those upstream guides and reduced to exactly the channels in
the published playlists:

    playlists/epg/PremiumTV.xml       the whole merged guide (plain XMLTV)
    playlists/epg/PremiumTV.xml.gz    the same guide gzipped (~10x smaller)

Load it in a player with:

    https://raw.githubusercontent.com/<owner>/PremiumTV1/main/playlists/epg/PremiumTV.xml

Because the file lives in the repository it is a stable ``.xml`` link, it is
versioned with the playlists it describes, and it is rebuilt by the workflows
(``.github/workflows/epg-build.yml``, plus a freshness-guarded step in
``scrape.yml`` and the nightly deep check), so the guide always covers the
channels the last automatic scrape published.

What "filtered" means, concretely:

* only channels whose ``tvg-id`` (or, failing that, display name) appears in a
  published playlist survive - typically a few thousand instead of tens of
  thousands, so a player is not indexing events for channels it cannot play;
* every ``start``/``stop`` is rewritten to UTC (``YYYYMMDDHHMMSS +0000``), so
  time filtering behaves the same no matter which source a programme came from;
* programmes that already ended more than ``--keep-past`` hours ago, or that
  start more than ``--ahead`` hours from now, are dropped;
* placeholder events with no usable title are dropped;
* identical events (same channel, start, stop, title) are merged, and events
  that overlap a better-sourced event on the same channel are dropped, so each
  channel has exactly one continuous programme track;
* titles, sub-titles, descriptions, categories, episode numbers, credits,
  icons, ratings and the ``new``/``live``/``premiere`` flags are preserved, so
  genre and "new episode" filters keep working.

Safety, in the style of the rest of this repository: a build that comes back
suspiciously small (``--min-channels``, ``--min-programmes``, or fewer than
``--min-previous-ratio`` of the channels in the guide it would replace) leaves
the previously published guide untouched and exits non-zero, so a bad network
hour cannot wipe the guide.

    python scripts/epg_build.py                       # build + reports
    python scripts/epg_build.py --patch               # + advertise it in the playlists
    python scripts/epg_build.py --force               # ignore --max-age-hours
    python scripts/epg_build.py --ahead 24 --max-mb 40
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import gzip
import html
import io
import json
import os
import re
import socket
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import zlib
from pathlib import Path
from xml.sax.saxutils import escape, quoteattr

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scraper  # noqa: E402  (reuses the shared HTTP/TLS helpers)
import epg_check  # noqa: E402  (reuses the guide discovery/header helpers)

ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------------- #
# Defaults
# --------------------------------------------------------------------------- #
EPG_DIR_NAME = "epg"
GUIDE_NAME = "PremiumTV"
# Playlists whose channels define the guide. The country playlists are subsets
# of PremiumTV.m3u, but they are cheap to read and they catch anything the
# working playlist does not carry.
DEFAULT_PLAYLISTS = ("PremiumTV.m3u", "AE_Channels.m3u", "Priority_Channels.m3u")
AHEAD_HOURS = 48
KEEP_PAST_HOURS = 6
MAX_PLAIN_MB = 45
MAX_GUIDE_MB = 400
MAX_PROGRAMMES = 1_500_000
MIN_CHANNELS = 25
MIN_PROGRAMMES = 1_000
MIN_PREVIOUS_RATIO = 0.25
MAX_AGE_HOURS = 6
WORKERS = 4
TIMEOUT = 90.0
RETRIES = 1
CHUNK = 1 << 16
# Repo used for the published link when GITHUB_REPOSITORY is not set.
DEFAULT_REPO = "cgyegcvcecvoc/PremiumTV1"
DEFAULT_BRANCH = "main"

# Sub-elements that are copied through verbatim: they carry data this script
# does not need to understand, but players use them for filtering.
PASSTHROUGH_TAGS = (
    "credits", "date", "keyword", "language", "orig-language", "icon", "url",
    "country", "video", "audio", "previously-shown", "last-chance", "premiere",
    "new", "live", "subtitles", "rating", "star-rating", "review",
)
# Titles that carry no information at all. Guides use them for dead air, and a
# grid full of them makes the real events harder to find.
PLACEHOLDER_TITLES = {
    "", "-", "--", "n/a", "na", "none", "null", "unknown", "no information",
    "no information available", "no data", "not available", "tba", "tbd",
    "sign off", "signoff", "close down", "closedown", "off air", "offair",
    "programming", "various", "programme", "program", "content",
}
# Noise stripped out of channel names before they are compared.
NAME_NOISE_RE = re.compile(
    r"\b(hd|sd|fhd|uhd|4k|hq|lq|hd\d*|1080p?|720p?|576p?|480p?|360p?|"
    r"live|stream|streaming|online|tv|web|webrip|iptv)\b", re.IGNORECASE)
BRACKET_RE = re.compile(r"[\[(][^\])]*[\])]")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
CC_SUFFIX_RE = re.compile(r"\.([a-z]{2})$")
XMLTV_TIME_RE = re.compile(r"^(\d{14})(?:\s*([+-]\d{4}))?$")
HTML_TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
GENERATOR = "PremiumTV1 epg_build.py"
TAG_RE = re.compile(r"<\s*([\w:.-]+)")

STATUSES_OK = ("ok", "empty")


def raw_tag(rendered: str) -> str:
    """Element name of a serialised XML fragment (``<icon src=.. />`` -> ``icon``)."""
    match = TAG_RE.match(rendered or "")
    return match.group(1) if match else ""


def log(msg: str) -> None:
    print(msg, flush=True)


def display_path(path) -> str:
    try:
        return str(Path(path).relative_to(ROOT))
    except ValueError:
        return str(path)


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


# --------------------------------------------------------------------------- #
# Normalisation / matching keys
# --------------------------------------------------------------------------- #
def norm_id(value: str) -> str:
    """Comparable form of a channel id: ``AE.us@East`` -> ``aeus``.

    The ``@variant`` suffix is dropped because the playlists carry one id per
    feed (``AE.us@East``, ``AE.us@West``) while guides normally publish a single
    id for the network (``AE.us``).
    """
    return NON_ALNUM_RE.sub("", value.split("@", 1)[0].lower())


def norm_name(value: str) -> str:
    """Comparable form of a display name: ``A&E (US East) (720p)`` -> ``aeuseast``."""
    text = BRACKET_RE.sub(" ", value or "")
    text = NAME_NOISE_RE.sub(" ", text)
    return NON_ALNUM_RE.sub("", text.lower())


def cc_of_id(value: str) -> str:
    """Country suffix of an XMLTV channel id (``AE.us`` -> ``us``), if any."""
    base = value.split("@", 1)[0].strip()
    match = CC_SUFFIX_RE.search(base.lower())
    return match.group(1) if match else ""


def clean_text(value: str) -> str:
    """Plain, single-spaced text: entities resolved, markup and control chars gone."""
    if not value:
        return ""
    text = html.unescape(HTML_TAG_RE.sub(" ", value))
    text = text.replace("\xa0", " ")
    text = "".join(ch for ch in text if ch == "\t" or ch == "\n" or ord(ch) >= 32)
    return WS_RE.sub(" ", text).strip()


# --------------------------------------------------------------------------- #
# XMLTV time handling
# --------------------------------------------------------------------------- #
def parse_xmltv_time(value: str) -> dt.datetime | None:
    """Parse ``20261002120000 +0200`` (offset optional) into an aware datetime."""
    text = (value or "").strip()
    match = XMLTV_TIME_RE.match(text)
    if not match:
        return None
    stamp, offset = match.group(1), match.group(2)
    try:
        naive = dt.datetime.strptime(stamp, "%Y%m%d%H%M%S")
    except ValueError:
        return None
    if offset:
        sign = 1 if offset[0] == "+" else -1
        hours, minutes = int(offset[1:3]), int(offset[3:5])
        if hours > 23 or minutes > 59:
            return None
        tz = dt.timezone(sign * dt.timedelta(hours=hours, minutes=minutes))
    else:
        # No offset means UTC by convention in every guide this repo advertises.
        tz = dt.timezone.utc
    return naive.replace(tzinfo=tz)


def format_xmltv_time(moment: dt.datetime) -> str:
    """Always UTC, always with an explicit offset - the form players handle best."""
    return moment.astimezone(dt.timezone.utc).strftime("%Y%m%d%H%M%S +0000")


# --------------------------------------------------------------------------- #
# Wanted channels (from the published playlists)
# --------------------------------------------------------------------------- #
class Wanted:
    """The channels the published playlists advertise, indexed for matching."""

    def __init__(self) -> None:
        self.by_id: dict = {}      # playlist tvg-id -> record
        self.by_key: dict = {}     # norm_id(tvg-id) -> [tvg-id, ...]
        self.by_name: dict = {}    # norm_name(display name) -> [tvg-id, ...]
        self.entries = 0
        self.without_id = 0

    def add(self, tvg_id: str, name: str, country: str, logo: str) -> None:
        self.entries += 1
        tvg_id = (tvg_id or "").strip()
        if not tvg_id:
            self.without_id += 1
            return
        record = self.by_id.setdefault(
            tvg_id, {"id": tvg_id, "name": clean_text(name), "country": (country or "").strip().upper(),
                     "logo": (logo or "").strip(), "key": norm_id(tvg_id), "names": []})
        name = clean_text(name)
        if name and name not in record["names"]:
            record["names"].append(name)
        if not record["logo"] and logo:
            record["logo"] = logo.strip()
        if not record["country"] and country:
            record["country"] = country.strip().upper()
        self.by_key.setdefault(record["key"], [])
        if tvg_id not in self.by_key[record["key"]]:
            self.by_key[record["key"]].append(tvg_id)
        if name:
            key = norm_name(name)
            if len(key) >= 4:
                self.by_name.setdefault(key, [])
                if tvg_id not in self.by_name[key]:
                    self.by_name[key].append(tvg_id)

    def unique_ids_for_name(self, name: str) -> list:
        """Playlist ids for a display name, only when the name is unambiguous."""
        ids = self.by_name.get(norm_name(name), [])
        return ids if len(ids) == 1 else []

    @property
    def ids(self) -> list:
        return sorted(self.by_id)


def playlist_channels(paths: list) -> Wanted:
    wanted = Wanted()
    for path in paths:
        if not path.exists():
            log(f"[epg-build] skipping missing playlist: {display_path(path)}")
            continue
        count = 0
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                stripped = line.strip()
                if not stripped.startswith("#EXTINF"):
                    continue
                attrs = dict(scraper.ATTR_RE.findall(stripped))
                name = stripped.split(",", 1)[1] if "," in stripped else ""
                wanted.add(attrs.get("tvg-id", ""), name,
                           attrs.get("tvg-country", ""), attrs.get("tvg-logo", ""))
                count += 1
        log(f"[epg-build] {display_path(path)}: {count} entries")
    log(f"[epg-build] {wanted.entries} playlist entries, {len(wanted.by_id)} unique "
        f"tvg-ids, {len(wanted.by_key)} id keys, {wanted.without_id} entries without tvg-id")
    return wanted


# --------------------------------------------------------------------------- #
# Streaming download + parse
# --------------------------------------------------------------------------- #
class ChainedStream(io.RawIOBase):
    """File-like view over an iterator of byte chunks, with a hard byte cap."""

    def __init__(self, chunks, max_bytes: int) -> None:
        self._chunks = iter(chunks)
        self._buffer = b""
        self._max_bytes = max_bytes
        self.read_bytes = 0
        self.truncated = False

    def readable(self) -> bool:
        return True

    def readinto(self, target) -> int:
        while not self._buffer:
            if self.read_bytes >= self._max_bytes:
                self.truncated = True
                return 0
            try:
                chunk = next(self._chunks)
            except StopIteration:
                return 0
            if not chunk:
                continue
            self._buffer = chunk
        take = min(len(target), len(self._buffer))
        target[:take] = self._buffer[:take]
        self._buffer = self._buffer[take:]
        self.read_bytes += take
        return take


def response_chunks(response) -> list:
    """Lazily read a response in chunks; returned as a generator."""

    def reader():
        while True:
            try:
                chunk = response.read(CHUNK)
            except Exception:  # noqa: BLE001 - a truncated body is still usable
                return
            if not chunk:
                return
            yield chunk

    return reader()


def guide_streams(url: str, timeout: float, retries: int, max_bytes: int):
    """Open a guide for streaming.

    Returns ``(stream, gzipped, counter, response)``: ``stream`` is what the XML
    parser reads, ``counter`` is the :class:`ChainedStream` that tracks how much
    was downloaded and whether the byte cap truncated it, and ``response`` must
    be closed by the caller.
    """
    last: Exception | None = None
    headers = {"User-Agent": scraper.DEFAULT_UA, "Accept": "*/*",
               "Accept-Encoding": "identity"}
    for attempt in range(max(0, retries) + 1):
        response = None
        try:
            request = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(request, timeout=timeout,
                                              context=scraper.INSECURE_CTX)
            head = response.read(2)
            if head == b"":
                response.close()
                raise ValueError("empty response")

            def chain(first: bytes):
                yield first
                yield from response_chunks(response)

            raw = ChainedStream(chain(head), max_bytes)
            buffered = io.BufferedReader(raw, buffer_size=1 << 16)
            if head == b"\x1f\x8b":
                return gzip.GzipFile(fileobj=buffered), True, raw, response
            return buffered, False, raw, response
        except urllib.error.HTTPError as exc:
            code = int(exc.code)
            try:
                exc.close()
            except Exception:  # noqa: BLE001
                pass
            if code >= 500 and attempt < max(0, retries):
                time.sleep(min(2 ** attempt, 4))
                last = exc
                continue
            raise RuntimeError(f"HTTP {code}") from exc
        except Exception as exc:  # noqa: BLE001
            if response is not None:
                try:
                    response.close()
                except Exception:  # noqa: BLE001
                    pass
            if attempt < max(0, retries) and not isinstance(exc, ValueError):
                time.sleep(min(2 ** attempt, 4))
                last = exc
                continue
            reason = getattr(exc, "reason", exc)
            raise RuntimeError(scraper.error_text(exc, url) if hasattr(scraper, "error_text")
                               else f"{type(exc).__name__}: {reason}") from exc
    raise RuntimeError(f"GET failed: {last}")  # pragma: no cover - loop always returns/raises


def looks_like_html(text: str) -> bool:
    head = text.lstrip()[:400].lower()
    return head.startswith("<!doctype html") or head.startswith("<html")


# --------------------------------------------------------------------------- #
# Programme model
# --------------------------------------------------------------------------- #
class Programme:
    __slots__ = ("start", "stop", "title", "sub_title", "desc", "categories",
                 "episode_nums", "extra", "source", "richness")

    def __init__(self, start, stop, title, source):
        self.start = start
        self.stop = stop
        self.title = title
        self.sub_title = ""
        self.desc = ""
        self.categories: list = []
        self.episode_nums: list = []
        self.extra: list = []
        self.source = source
        self.richness = 0

    def score_richness(self) -> None:
        self.richness = (
            (1 if len(self.desc) > 40 else 0)
            + (1 if self.categories else 0)
            + (1 if self.episode_nums else 0)
            + (1 if any("credits" in item for item in self.extra) else 0)
            + (1 if self.sub_title else 0)
            + len(self.extra)
        )

    def add_category(self, text: str, lang: str = "") -> None:
        """Record a genre, ignoring the same word arriving with another lang tag."""
        for index, (existing, existing_lang) in enumerate(self.categories):
            if existing.lower() == text.lower():
                if lang and not existing_lang:
                    self.categories[index] = (existing, lang)
                return
        self.categories.append((text, lang))

    def merge_from(self, other: "Programme") -> None:
        """Take whatever this copy is missing from a duplicate of the same event."""
        if len(other.desc) > len(self.desc):
            self.desc = other.desc
        if other.sub_title and not self.sub_title:
            self.sub_title = other.sub_title
        for text, lang in other.categories:
            self.add_category(text, lang)
        for episode in other.episode_nums:
            if episode not in self.episode_nums:
                self.episode_nums.append(episode)
        for item in other.extra:
            tag = raw_tag(item)
            if tag and not any(raw_tag(existing) == tag for existing in self.extra):
                self.extra.append(item)
        self.score_richness()

    def key(self, channel_key: str) -> tuple:
        return (channel_key, self.start, self.stop, NON_ALNUM_RE.sub("", self.title.lower()))


def programme_from_element(element, source: int) -> Programme | None:
    start = parse_xmltv_time(element.get("start", ""))
    if start is None:
        return None
    stop = parse_xmltv_time(element.get("stop", "")) or start
    if stop < start:
        stop = start
    title = ""
    programme = None
    for child in element:
        tag = child.tag
        if tag == "title":
            title = clean_text(child.text or "")
            if programme is None:
                if title.lower() in PLACEHOLDER_TITLES:
                    return None
                programme = Programme(start, stop, title, source)
        elif programme is None:
            continue
        elif tag == "sub-title":
            programme.sub_title = clean_text(child.text or "")
        elif tag == "desc":
            text = clean_text(child.text or "")
            if len(text) > len(programme.desc):
                programme.desc = text
        elif tag == "category":
            text = clean_text(child.text or "")
            if text:
                programme.add_category(text, child.get("lang", ""))
        elif tag == "episode-num":
            text = clean_text(child.text or "")
            system = child.get("system", "onscreen")
            if text:
                entry = f'<episode-num system="{escape(system)}">{escape(text)}</episode-num>'
                if entry not in programme.episode_nums:
                    programme.episode_nums.append(entry)
        elif tag in PASSTHROUGH_TAGS:
            try:
                rendered = ET.tostring(child, encoding="unicode").strip()
            except Exception:  # noqa: BLE001
                continue
            if rendered and rendered not in programme.extra:
                programme.extra.append(rendered)
    if programme is None:
        return None
    programme.score_richness()
    return programme


# --------------------------------------------------------------------------- #
# One guide -> channels + programmes
# --------------------------------------------------------------------------- #
class GuideHarvest:
    """What one upstream guide contributed."""

    def __init__(self, url: str, index: int) -> None:
        self.url = url
        self.index = index
        self.status = "unreachable"
        self.reason = ""
        self.elapsed = 0.0
        self.downloaded = 0
        self.channels_seen = 0
        self.programmes_seen = 0
        self.channels_matched = 0
        self.matched_by_id = 0
        self.matched_by_name = 0
        self.programmes_kept = 0
        self.programmes_dropped = 0
        self.truncated = False


def harvest_guide(url: str, index: int, wanted: Wanted, timeout: float, retries: int,
                  max_bytes: int, window_start: dt.datetime, window_end: dt.datetime,
                  match_names: bool, fanout: bool, counters: dict, lock: threading.Lock,
                  channels: dict, programmes: dict) -> GuideHarvest:
    """Download one guide and fold its wanted channels/programmes into the merge."""
    harvest = GuideHarvest(url, index)
    started = time.time()
    opener = response = None
    stream = None
    try:
        stream, gzipped, raw, response = guide_streams(url, timeout, retries, max_bytes)
        opener, harvest_truncated_flag = raw, raw
        seen_something = False
        matched_ids: dict = {}   # guide channel id -> [playlist ids]

        context = ET.iterparse(stream, events=("start", "end"))
        event, root = next(context)
        depth = 1  # the root's own start event
        for event, element in context:
            if event == "start":
                depth += 1
                continue
            depth -= 1
            # Only top-level <channel>/<programme> elements are consumed here.
            # Anything deeper is still being read when it ends, so it must not
            # be cleared - its text is what programme_from_element() needs.
            if depth != 1:
                continue
            tag = element.tag
            if tag == "channel":
                harvest.channels_seen += 1
                guide_id = (element.get("id") or "").strip()
                if guide_id:
                    targets = wanted.by_key.get(norm_id(guide_id)) or []
                    kind = "id"
                    if not targets and match_names:
                        names = [clean_text(node.text or "") for node in element
                                 if node.tag == "display-name"]
                        for name in names:
                            targets = wanted.unique_ids_for_name(name)
                            if targets:
                                kind = "name"
                                break
                    if targets:
                        matched_ids[guide_id] = targets
                        harvest.channels_matched += 1
                        if kind == "id":
                            harvest.matched_by_id += 1
                        else:
                            harvest.matched_by_name += 1
                        names = [clean_text(node.text or "") for node in element
                                 if node.tag == "display-name"]
                        icon = ""
                        for node in element:
                            if node.tag == "icon" and node.get("src"):
                                icon = node.get("src", "")
                                break
                        for target in targets:
                            record = channels.setdefault(target, {
                                "id": target, "names": [], "icon": "",
                                "country": cc_of_id(guide_id)})
                            for name in names:
                                if name and name not in record["names"]:
                                    record["names"].append(name)
                            if guide_id not in record["names"]:
                                record["names"].append(guide_id)
                            if icon and not record["icon"]:
                                record["icon"] = icon
                seen_something = True
            elif tag == "programme":
                harvest.programmes_seen += 1
                guide_id = (element.get("channel") or "").strip()
                targets = matched_ids.get(guide_id)
                if targets:
                    programme = programme_from_element(element, index)
                    if programme is None:
                        harvest.programmes_dropped += 1
                    elif programme.stop <= window_start or programme.start >= window_end:
                        harvest.programmes_dropped += 1
                    else:
                        with lock:
                            if counters["programmes"] >= MAX_PROGRAMMES:
                                counters["capped"] = True
                            else:
                                counters["programmes"] += 1
                                for target in (targets if fanout else targets[:1]):
                                    programmes.setdefault(target, []).append(programme)
                                harvest.programmes_kept += 1
                else:
                    harvest.programmes_dropped += 1
                seen_something = True
            else:
                seen_something = True
            # Every child of the root is finished at this point, so the whole
            # level can be released: this is what keeps a 500 MB guide from
            # being held in memory.
            element.clear()
            root.clear()

        harvest.downloaded = opener.read_bytes if opener else 0
        harvest.truncated = bool(opener and opener.truncated)
        if not seen_something:
            harvest.status, harvest.reason = "invalid", "no XMLTV elements found"
        elif harvest.channels_seen == 0:
            harvest.status, harvest.reason = "invalid", "no <channel> elements"
        elif harvest.channels_matched == 0:
            harvest.status = "nomatch"
            harvest.reason = (f"{harvest.channels_seen} channels, none matched the "
                              f"published playlists")
        else:
            harvest.status = "ok"
            harvest.reason = (f"{harvest.channels_matched} of {harvest.channels_seen} "
                              f"channels matched, {harvest.programmes_kept} programmes kept")
    except ET.ParseError as exc:
        # A truncated download still produced usable data; say so rather than
        # throwing the whole guide away.
        harvest.downloaded = opener.read_bytes if opener else 0
        harvest.truncated = True
        if harvest.channels_matched or harvest.programmes_kept:
            harvest.status = "ok"
            harvest.reason = (f"truncated at {harvest.downloaded // 1024} KB "
                              f"({exc}); kept {harvest.programmes_kept} programmes")
        else:
            harvest.status, harvest.reason = "invalid", f"XML parse error: {exc}"
    except (socket.timeout, TimeoutError):
        harvest.status, harvest.reason = "unreachable", "timeout"
    except zlib.error as exc:
        # Ran out of compressed data part-way through (byte cap, or a server that
        # closed early). Whatever was parsed before that is still usable.
        harvest.downloaded = opener.read_bytes if opener else 0
        harvest.truncated = True
        if harvest.programmes_kept:
            harvest.status = "ok"
            harvest.reason = (f"stream ended early at {harvest.downloaded // 1024} KB "
                              f"({exc}); kept {harvest.programmes_kept} programmes")
        else:
            harvest.status, harvest.reason = "invalid", f"corrupt gzip stream: {exc}"
    except Exception as exc:  # noqa: BLE001
        text = str(exc) or type(exc).__name__
        if "HTTP 404" in text or "HTTP 410" in text:
            harvest.status = "offline"
        elif "HTTP 401" in text or "HTTP 403" in text or "HTTP 451" in text:
            harvest.status = "blocked"
        elif "gaierror" in text or "NameResolution" in text or "Name or service" in text:
            harvest.status = "offline"
        elif harvest.programmes_kept:
            harvest.status = "ok"
            harvest.reason = (f"stream failed after {harvest.programmes_kept} programmes: "
                              f"{text[:100]}")
        else:
            harvest.status = "unreachable"
        if harvest.status != "ok":
            harvest.reason = text[:160]
    finally:
        for closable in (stream, response):
            if closable is not None:
                try:
                    closable.close()
                except Exception:  # noqa: BLE001
                    pass
        harvest.elapsed = round(time.time() - started, 2)
    return harvest


# --------------------------------------------------------------------------- #
# Guide list
# --------------------------------------------------------------------------- #
def guide_list(out_dir: Path, extra: list, guides_from: str, playlists: list,
               only_verified: bool) -> list:
    """Ordered, de-duplicated guide URLs to merge (first = highest priority)."""
    guides: list = list(dict.fromkeys(extra))
    report_path = Path(guides_from) if Path(guides_from).is_absolute() else out_dir / guides_from
    if report_path.exists():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
            for guide in report.get("guides", []):
                status = guide.get("status")
                if status in STATUSES_OK or (not only_verified and status):
                    url = guide.get("url", "").strip()
                    if url and url not in guides:
                        guides.append(url)
            log(f"[epg-build] {display_path(report_path)}: "
                f"{len(report.get('guides', []))} guides from the last guide check")
        except (json.JSONDecodeError, OSError) as exc:
            log(f"[epg-build] could not read {display_path(report_path)}: {exc}")
    else:
        log(f"[epg-build] no guide report at {display_path(report_path)}")
    if not only_verified or not report_path.exists():
        for path in playlists:
            if not path.exists():
                continue
            for url in epg_check.extract_guides(path):
                if url not in guides:
                    guides.append(url)
    return guides


# --------------------------------------------------------------------------- #
# Merge
# --------------------------------------------------------------------------- #
def merge_programmes(per_channel: dict, source_matches: dict, dedupe_overlaps: bool) -> tuple:
    """Collapse the harvested copies into one track per published channel.

    Returns ``(programmes, stats)`` where ``programmes`` maps a playlist tvg-id
    to a chronologically sorted list of :class:`Programme`.
    """
    stats = {"duplicates_merged": 0, "overlaps_dropped": 0}
    merged: dict = {}
    for target, entries in per_channel.items():
        # A programme harvested for a base channel is fanned out to every alias
        # only on the alias that owns the bucket; the others get a reference to
        # the same object, so the work below happens once per real event.
        best: dict = {}
        for programme in entries:
            key = programme.key(target)
            existing = best.get(key)
            if existing is None:
                best[key] = programme
                continue
            stats["duplicates_merged"] += 1
            keep, drop = (existing, programme) if existing.richness >= programme.richness \
                else (programme, existing)
            keep.merge_from(drop)
            best[key] = keep
        ordered = sorted(best.values(), key=lambda item: (item.start, item.stop, item.title))
        if dedupe_overlaps:
            def rank(item) -> tuple:
                # Lower sorts first. "Better" = the better-described event, then
                # the event from the source that matched more of our channels,
                # then the earlier source.
                return (-item.richness, -source_matches.get(item.source, 0), item.source)

            kept: list = []
            for programme in ordered:
                replaces = None
                blocked = False
                for existing in kept[-8:]:
                    if existing.start <= programme.start < existing.stop:
                        # Same channel, overlapping slot: one of the two has to go.
                        if rank(programme) < rank(existing):
                            replaces = existing
                        else:
                            blocked = True
                        break
                if blocked:
                    stats["overlaps_dropped"] += 1
                    continue
                if replaces is not None:
                    kept.remove(replaces)
                    stats["overlaps_dropped"] += 1
                kept.append(programme)
            ordered = kept
        merged[target] = ordered
    return merged, stats


def channel_order(channels: dict, merged: dict, wanted: Wanted) -> list:
    """Channels with data, in playlist order, then alphabetically."""
    wanted_order = {tvg_id: index for index, tvg_id in enumerate(wanted.ids)}
    return sorted((cid for cid in merged if merged[cid]),
                  key=lambda cid: (wanted_order.get(cid, len(wanted_order)), cid.lower()))


# --------------------------------------------------------------------------- #
# Serialising
# --------------------------------------------------------------------------- #
def serialize(path: Path, channels: dict, merged: dict, order: list, window_end: dt.datetime,
              per_channel_cap: int, repo_url: str, label: str) -> tuple:
    """Write the guide; returns ``(bytes, channels_written, programmes_written)``."""
    written_bytes = 0
    channels_written = 0
    programmes_written = 0
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        def emit(text: str) -> None:
            nonlocal written_bytes
            written_bytes += len(text.encode("utf-8"))
            handle.write(text)

        emit('<?xml version="1.0" encoding="UTF-8"?>\n')
        emit(f"<tv generator-info-name={quoteattr(GENERATOR)} "
             f"generator-info-url={quoteattr(repo_url)}>\n")
        for cid in order:
            items = merged[cid]
            if not items:
                continue
            record = channels.get(cid, {"id": cid, "names": [], "icon": ""})
            names: list = []
            playlist_name = wanted_name_for(cid)
            for name in ([playlist_name] if playlist_name else []) + list(record.get("names", [])):
                if name and name not in names:
                    names.append(name)
            if not names:
                names = [cid]
            emit(f"  <channel id={quoteattr(cid)}>\n")
            for name in names[:6]:
                emit(f"    <display-name>{escape(name)}</display-name>\n")
            icon = record.get("icon") or ""
            if icon:
                emit(f"    <icon src={quoteattr(icon)} />\n")
            emit("  </channel>\n")
            channels_written += 1
        for cid in order:
            items = merged[cid][:per_channel_cap] if per_channel_cap else merged[cid]
            for programme in items:
                if programme.start >= window_end:
                    continue
                emit(f"  <programme start={quoteattr(format_xmltv_time(programme.start))} "
                     f"stop={quoteattr(format_xmltv_time(programme.stop))} "
                     f"channel={quoteattr(cid)}>\n")
                emit(f"    <title>{escape(programme.title)}</title>\n")
                if programme.sub_title:
                    emit(f"    <sub-title>{escape(programme.sub_title)}</sub-title>\n")
                if programme.desc:
                    emit(f"    <desc>{escape(programme.desc)}</desc>\n")
                for text, lang in programme.categories[:12]:
                    if lang:
                        emit(f'    <category lang={quoteattr(lang)}>'
                             f"{escape(text)}</category>\n")
                    else:
                        emit(f"    <category>{escape(text)}</category>\n")
                for episode in programme.episode_nums[:4]:
                    emit(f"    {episode}\n")
                for item in programme.extra[:12]:
                    emit(f"    {item}\n")
                emit("  </programme>\n")
                programmes_written += 1
        emit("</tv>\n")
    return written_bytes, channels_written, programmes_written


# Set by build() so serialize() can put the playlist's own display name first,
# which is what name-matching players compare against.
_WANTED_NAMES: dict = {}


def wanted_name_for(cid: str) -> str:
    return _WANTED_NAMES.get(cid, "")


def gzip_file(source: Path, target: Path) -> int:
    size = 0
    with source.open("rb") as raw, gzip.open(target, "wb", compresslevel=9) as packed:
        while True:
            chunk = raw.read(1 << 20)
            if not chunk:
                break
            packed.write(chunk)
            size += len(chunk)
    return target.stat().st_size


# --------------------------------------------------------------------------- #
# Reports
# --------------------------------------------------------------------------- #
def write_reports(checks_dir: Path, report: dict, epg_dir: Path, name: str,
                  raw_url: str) -> list:
    checks_dir.mkdir(parents=True, exist_ok=True)
    json_path = checks_dir / "epg-build.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    totals = report["totals"]
    lines = [
        "# Merged TV guide build",
        "",
        f"- **Run:** {report['label']} (`{report['run_id']}`)",
        f"- **Started:** {report['started_utc']} | **Finished:** {report['finished_utc']} "
        f"| **Duration:** {report['duration_seconds']}s",
        f"- **Guide link (`.xml`):** `{raw_url}`",
        f"- **Gzipped:** `{raw_url}.gz`",
        f"- **Window:** {report['window']['start']} to {report['window']['end']} UTC "
        f"({report['window']['ahead_hours']:g}h ahead, "
        f"{report['window']['keep_past_hours']:g}h back"
        + (f"; trimmed from {report['window']['requested_ahead_hours']:g}h to fit the size budget)"
           if report["window"]["ahead_hours"] < report["window"]["requested_ahead_hours"]
           else ")"),
        "",
        "| Result | Value |",
        "|---|---:|",
        f"| Guides merged | {totals['guides_ok']} of {totals['guides']} |",
        f"| Playlist channels | {report['playlist_channels']} |",
        f"| Channels with a guide | {report['channels_with_guide']} "
        f"({report['coverage']:.1%}) |",
        f"| Programmes in the guide | {report['programmes']} |",
        f"| Duplicate events merged | {report['merge']['duplicates_merged']} |",
        f"| Overlapping events dropped | {report['merge']['overlaps_dropped']} |",
        f"| Events dropped (out of window / placeholder) | {report['outside_window']} |",
        f"| XML size | {report['size_bytes'] // 1024} KB |",
        f"| Gzipped size | {report['gz_bytes'] // 1024} KB |",
        "",
    ]
    if report.get("published"):
        lines += [f"Published [`playlists/{EPG_DIR_NAME}/{name}.xml`]"
                  f"(../../{EPG_DIR_NAME}/{name}.xml) and "
                  f"[`playlists/{EPG_DIR_NAME}/{name}.xml.gz`]"
                  f"(../../{EPG_DIR_NAME}/{name}.xml.gz).", ""]
    else:
        lines += [f"**Not published:** {report.get('publish_reason', 'unknown reason')} "
                  "The previously published guide was left in place.", ""]
    if report.get("trim"):
        lines += ["## Size trimming", ""]
        lines += [f"- {step}" for step in report["trim"]] + [""]
    lines += ["## Upstream guides", "",
              "| Guide | Status | Channels seen | Matched | By id | By name | "
              "Programmes kept | Dropped | Read |",
              "|---|---|---:|---:|---:|---:|---:|---:|---:|"]
    for guide in sorted(report["guides"], key=lambda item: -item["channels_matched"]):
        short = guide["url"].rsplit("/", 1)[-1]
        lines.append(
            f"| `{short}` | {guide['status']} | {guide['channels_seen']} | "
            f"{guide['channels_matched']} | {guide['matched_by_id']} | "
            f"{guide['matched_by_name']} | {guide['programmes_kept']} | "
            f"{guide['programmes_dropped']} | {guide['downloaded'] // 1024} KB |")
    failed = [guide for guide in report["guides"] if guide["status"] not in STATUSES_OK]
    if failed:
        lines += ["", "## Guides that contributed nothing", "",
                  "| Guide | Status | Reason |", "|---|---|---|"]
        for guide in sorted(failed, key=lambda item: item["status"]):
            short = scraper.safe_url(guide["url"])
            lines.append(f"| `{short}` | {guide['status']} | {guide['reason']} |")
    patch = report.get("patch") or {}
    if patch:
        lines += ["", "## Playlist headers", "",
                  f"- Advertised the merged guide first in **{len(patch.get('files', []))}** "
                  f"playlists."]
    lines.append("")
    md_path = checks_dir / "EPG-BUILD.md"
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return [json_path, md_path]


def append_edit_log(out_dir: Path, report: dict) -> Path:
    logs_dir = out_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    path = logs_dir / "epg-build-edits.txt"
    lines = [f"## {report['finished_utc']} - {report['label']} (EPG build, run {report['run_id']})"]
    if report.get("published"):
        lines.append(f"  +published {report['size_bytes'] // 1024} KB guide: "
                     f"{report['channels_with_guide']} channels, {report['programmes']} "
                     f"programmes from {report['totals']['guides_ok']}/"
                     f"{report['totals']['guides']} guides")
    else:
        lines.append(f"  ! not published: {report.get('publish_reason', 'unknown')}")
    for guide in report["guides"]:
        if guide["status"] not in STATUSES_OK:
            lines.append(f"  -guide {guide['url']} [{guide['status']}: {guide['reason']}]")
    lines.append("")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")
    return path


def raw_url_for(repo: str, branch: str, epg_dir: Path, name: str) -> str:
    try:
        relative = epg_dir.relative_to(ROOT / "playlists")
    except ValueError:
        relative = Path(epg_dir.name)
    return f"https://raw.githubusercontent.com/{repo}/{branch}/playlists/{relative}/{name}.xml"


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build(args) -> dict:
    started = utc_now()
    out_dir = Path(args.out)
    epg_dir = Path(args.epg_dir) if args.epg_dir else out_dir / EPG_DIR_NAME
    epg_dir.mkdir(parents=True, exist_ok=True)
    checks_dir = out_dir / "checks"
    repo = args.repo or os.environ.get("GITHUB_REPOSITORY") or DEFAULT_REPO
    branch = args.branch or DEFAULT_BRANCH
    raw_url = raw_url_for(repo, branch, epg_dir, args.name)

    playlist_paths: list = []
    for item in args.playlist:
        path = Path(item)
        playlist_paths.append(path if path.is_absolute() else ROOT / path)
    if args.countries:
        playlist_paths.extend(sorted((out_dir / "countries").glob("*.m3u")))

    wanted = playlist_channels(playlist_paths)
    global _WANTED_NAMES
    _WANTED_NAMES = {cid: record["name"] for cid, record in wanted.by_id.items()}

    guides = guide_list(out_dir, list(dict.fromkeys(args.guide)), args.guides_from,
                        playlist_paths, not args.include_unverified)
    if args.max_guides:
        guides = guides[:args.max_guides]
    log(f"[epg-build] merging {len(guides)} upstream guides")

    window_end = started + dt.timedelta(hours=args.ahead)
    window_start = started - dt.timedelta(hours=args.keep_past)
    channels: dict = {}
    per_channel: dict = {}
    source_matches: dict = {}
    counters = {"programmes": 0, "capped": False}
    lock = threading.Lock()
    harvests: list = []
    max_bytes = int(args.max_guide_mb * 1024 * 1024)

    if guides:
        with cf.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
            futures = {
                pool.submit(harvest_guide, url, index, wanted, args.timeout, args.retries,
                            max_bytes, window_start, window_end, not args.no_names,
                            not args.no_fanout, counters, lock, channels,
                            per_channel): url
                for index, url in enumerate(guides)
            }
            done = 0
            for future in cf.as_completed(futures):
                url = futures[future]
                try:
                    harvest = future.result()
                except Exception as exc:  # noqa: BLE001
                    harvest = GuideHarvest(url, 0)
                    harvest.status, harvest.reason = "unreachable", f"builder error: {exc}"
                harvests.append(harvest)
                done += 1
                log(f"[epg-build] {done}/{len(guides)} {harvest.url.rsplit('/', 1)[-1]}: "
                    f"{harvest.status} - {harvest.reason}")

    for harvest in harvests:
        source_matches[harvest.index] = harvest.channels_matched
    merged, merge_stats = merge_programmes(per_channel, source_matches,
                                           not args.keep_overlaps)
    order = channel_order(channels, merged, wanted)

    totals = {
        "guides": len(harvests),
        "guides_ok": sum(1 for item in harvests if item.status in STATUSES_OK),
    }
    report = {
        "run_id": f"{started.strftime('%Y%m%dT%H%M%S')}Z-{os.getpid()}",
        "label": args.label,
        "started_utc": started.isoformat(timespec="seconds").replace("+00:00", "Z"),
        "finished_utc": utc_now().isoformat(timespec="seconds").replace("+00:00", "Z"),
        "duration_seconds": 0.0,
        "raw_url": raw_url,
        "gz_url": raw_url + ".gz",
        "window": {
            "start": format_xmltv_time(window_start),
            "end": format_xmltv_time(window_end),
            "requested_ahead_hours": args.ahead,
            "ahead_hours": args.ahead,
            "keep_past_hours": args.keep_past,
        },
        "guides": [item.__dict__ for item in sorted(harvests, key=lambda g: g.index)],
        "totals": totals,
        "playlist_channels": len(wanted.by_id),
        "playlist_entries": wanted.entries,
        "playlist_entries_without_id": wanted.without_id,
        "channels_with_guide": len(order),
        "coverage": round(len(order) / len(wanted.by_id), 4) if wanted.by_id else 0.0,
        "programmes": sum(len(merged[cid]) for cid in order),
        "outside_window": sum(item.programmes_dropped for item in harvests),
        "merge": merge_stats,
        "capped": counters["capped"],
        "trim": [],
        "published": False,
        "publish_reason": "",
        "size_bytes": 0,
        "gz_bytes": 0,
    }

    if counters["capped"]:
        report["trim"].append(f"collection stopped at {MAX_PROGRAMMES} events")

    # ---- safety gate: never replace a good guide with a hollow one ---------- #
    xml_path = epg_dir / f"{args.name}.xml"
    gz_path = epg_dir / f"{args.name}.xml.gz"
    previous_channels = count_channels(xml_path)
    if not order:
        report["publish_reason"] = "no playlist channel matched any upstream guide"
    elif len(order) < args.min_channels:
        report["publish_reason"] = (f"only {len(order)} channels matched "
                                    f"(--min-channels {args.min_channels})")
    elif report["programmes"] < args.min_programmes:
        report["publish_reason"] = (f"only {report['programmes']} programmes collected "
                                    f"(--min-programmes {args.min_programmes})")
    elif previous_channels and len(order) < previous_channels * args.min_previous_ratio:
        report["publish_reason"] = (f"{len(order)} channels is under "
                                    f"{args.min_previous_ratio:.0%} of the "
                                    f"{previous_channels} in the published guide")
    if report["publish_reason"]:
        log(f"[epg-build] NOT PUBLISHED: {report['publish_reason']}")
        report["previous_channels"] = previous_channels
        report["finished_utc"] = utc_now().isoformat(timespec="seconds").replace("+00:00", "Z")
        report["duration_seconds"] = round(
            (utc_now() - started).total_seconds(), 1)
        return report

    # ---- serialise, trimming until it fits the size budget ------------------ #
    max_bytes_out = int(args.max_mb * 1024 * 1024)
    tmp_path = epg_dir / f".{args.name}.xml.tmp"
    attempt_window_end = window_end
    cap = 0
    trimmed_order = order
    size = 0
    channels_written = programmes_written = 0
    size_at_last_cut = None
    while True:
        size, channels_written, programmes_written = serialize(
            tmp_path, channels, merged, trimmed_order, attempt_window_end, cap,
            raw_url, args.label)
        if size <= max_bytes_out:
            break
        ahead_left = (attempt_window_end - started).total_seconds() / 3600
        # Cutting the window only helps while it actually removes events; when a
        # shorter window produced the same file, stop trading coverage for
        # nothing and move on to the next lever.
        if ahead_left > args.min_ahead and (size_at_last_cut is None or size < size_at_last_cut):
            # Cut proportionally to the overshoot instead of in fixed steps: a
            # file 5% over budget should lose an hour, not six.
            target = ahead_left * (max_bytes_out / size) * 0.98
            new_ahead = max(args.min_ahead, min(ahead_left - 1, target))
            if new_ahead < ahead_left:
                size_at_last_cut = size
                attempt_window_end = started + dt.timedelta(hours=new_ahead)
                report["trim"].append(
                    f"{size / 1048576:.1f} MB over the {args.max_mb:g} MB budget: "
                    f"window cut from {ahead_left:.0f}h to {new_ahead:.1f}h ahead")
                continue
        if cap == 0 or cap > 12:
            cap = max(12, (cap or 64) // 2)
            report["trim"].append(
                f"still {size // 1024 // 1024} MB: capped at {cap} events per channel")
            continue
        drop = max(1, len(trimmed_order) // 5)
        keep = len(trimmed_order) - drop
        if keep < args.min_channels:
            report["trim"].append(
                f"kept {len(trimmed_order)} channels at {size // 1024 // 1024} MB "
                f"(cannot trim further without breaking --min-channels)")
            break
        trimmed_order = trimmed_order[:keep]
        report["trim"].append(f"still {size // 1024 // 1024} MB: dropped the last "
                              f"{drop} channels with data")

    if args.dry_run:
        tmp_path.unlink(missing_ok=True)
        report["published"] = False
        report["publish_reason"] = "dry run"
        report["size_bytes"] = size
        report["channels_with_guide"] = channels_written
        report["programmes"] = programmes_written
        note_window(report, started, attempt_window_end)
        report["previous_channels"] = previous_channels
        report["finished_utc"] = utc_now().isoformat(timespec="seconds").replace("+00:00", "Z")
        report["duration_seconds"] = round((utc_now() - started).total_seconds(), 1)
        return report

    tmp_path.replace(xml_path)
    report["gz_bytes"] = gzip_file(xml_path, gz_path)
    report["size_bytes"] = size
    report["channels_with_guide"] = channels_written
    report["programmes"] = programmes_written
    note_window(report, started, attempt_window_end)
    report["previous_channels"] = previous_channels
    report["published"] = True
    report["publish_reason"] = ""
    report["files"] = [display_path(xml_path), display_path(gz_path)]
    report["finished_utc"] = utc_now().isoformat(timespec="seconds").replace("+00:00", "Z")
    report["duration_seconds"] = round((utc_now() - started).total_seconds(), 1)
    log(f"[epg-build] wrote {display_path(xml_path)} ({size // 1024} KB, "
        f"{channels_written} channels, {programmes_written} programmes)")
    log(f"[epg-build] wrote {display_path(gz_path)} "
        f"({report['gz_bytes'] // 1024} KB)")
    return report


def note_window(report: dict, started: dt.datetime, window_end: dt.datetime) -> None:
    """Record the window the guide actually covers after any size trimming."""
    report["window"]["end"] = format_xmltv_time(window_end)
    report["window"]["ahead_hours"] = round(
        (window_end - started).total_seconds() / 3600, 2)


def count_channels(xml_path: Path) -> int:
    """Channels in the guide that is currently published (0 when there is none)."""
    if not xml_path.exists():
        return 0
    count = 0
    try:
        with xml_path.open("rb") as handle:
            while True:
                chunk = handle.read(1 << 20)
                if not chunk:
                    break
                count += chunk.count(b"<channel ")
    except OSError:
        return 0
    return count


def patch_playlists(targets: list, raw_url: str) -> dict:
    """Put the merged guide first in each playlist's x-tvg-url header."""
    files = []
    for path in targets:
        if not path.exists():
            continue
        current = epg_check.extract_guides(path)
        if current and current[0] == raw_url:
            continue
        final = [raw_url] + [url for url in current if url != raw_url]
        if epg_check.rewrite_header(path, final):
            files.append({"file": display_path(path), "guides": len(final)})
            log(f"[epg-build] {path.name}: advertising the merged guide first "
                f"({len(final)} guides)")
    return {"files": files}


def previous_report_age(out_dir: Path) -> float | None:
    """Hours since the last successful build, or None when there was none."""
    path = out_dir / "checks" / "epg-build.json"
    if not path.exists():
        return None
    try:
        report = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    if not report.get("published"):
        return None
    stamp = report.get("finished_utc", "")
    try:
        moment = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc)
    except ValueError:
        return None
    return (utc_now() - moment).total_seconds() / 3600


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=str(ROOT / "playlists"), help="playlists directory")
    ap.add_argument("--epg-dir", default="", help="where to write the guide "
                    "(default: <out>/epg)")
    ap.add_argument("--name", default=GUIDE_NAME, help="guide file name without extension")
    ap.add_argument("--playlist", action="append", default=[],
                    help="playlist whose channels define the guide (repeatable; "
                         "default: the published working playlists)")
    ap.add_argument("--countries", action="store_true",
                    help="also read playlists/countries/*.m3u")
    ap.add_argument("--guide", action="append", default=[],
                    help="extra guide URL to merge first (repeatable)")
    ap.add_argument("--guides-from", default="checks/epg-check.json",
                    help="guide report to read the verified guide list from")
    ap.add_argument("--include-unverified", action="store_true",
                    help="also merge guides the last guide check could not verify")
    ap.add_argument("--max-guides", type=int, default=0,
                    help="merge at most this many guides (0 = all)")
    ap.add_argument("--ahead", type=float, default=AHEAD_HOURS,
                    help="hours of future listings to keep")
    ap.add_argument("--min-ahead", type=float, default=12.0,
                    help="never trim the window below this many hours ahead")
    ap.add_argument("--keep-past", type=float, default=KEEP_PAST_HOURS,
                    help="hours of already-started listings to keep")
    ap.add_argument("--max-mb", type=float, default=MAX_PLAIN_MB,
                    help="size budget for the plain .xml file")
    ap.add_argument("--max-guide-mb", type=float, default=MAX_GUIDE_MB,
                    help="download cap per upstream guide")
    ap.add_argument("--timeout", type=float, default=TIMEOUT, help="per-guide timeout")
    ap.add_argument("--retries", type=int, default=RETRIES, help="retries per guide")
    ap.add_argument("--workers", type=int, default=WORKERS, help="concurrent guide downloads")
    ap.add_argument("--no-names", action="store_true",
                    help="match channels by tvg-id only, never by display name")
    ap.add_argument("--no-fanout", action="store_true",
                    help="do not copy events to alias tvg-ids of the same channel")
    ap.add_argument("--keep-overlaps", action="store_true",
                    help="keep overlapping events instead of one track per channel")
    ap.add_argument("--min-channels", type=int, default=MIN_CHANNELS,
                    help="refuse to publish below this many channels with a guide")
    ap.add_argument("--min-programmes", type=int, default=MIN_PROGRAMMES,
                    help="refuse to publish below this many programmes")
    ap.add_argument("--min-previous-ratio", type=float, default=MIN_PREVIOUS_RATIO,
                    help="refuse to publish below this share of the published channel count")
    ap.add_argument("--max-age-hours", type=float, default=MAX_AGE_HOURS,
                    help="skip the build when the published guide is newer than this "
                         "(0 = always build)")
    ap.add_argument("--force", action="store_true", help="ignore --max-age-hours")
    ap.add_argument("--patch", action="store_true",
                    help="advertise the merged guide first in the playlists' x-tvg-url")
    ap.add_argument("--dry-run", action="store_true", help="build to a temp file only")
    ap.add_argument("--repo", default="", help="owner/repo for the published link")
    ap.add_argument("--branch", default=DEFAULT_BRANCH, help="branch for the published link")
    ap.add_argument("--label", default="EPG build", help="run label for the reports")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    out_dir = Path(args.out)
    if not args.playlist:
        args.playlist = [str(out_dir / name) for name in DEFAULT_PLAYLISTS]

    if not args.force and args.max_age_hours > 0:
        age = previous_report_age(out_dir)
        if age is not None and age < args.max_age_hours:
            log(f"[epg-build] published guide is {age:.1f}h old "
                f"(< {args.max_age_hours:g}h); nothing to do")
            return 0

    report = build(args)
    if args.patch and report.get("published") and not args.dry_run:
        targets = [Path(item) if Path(item).is_absolute() else ROOT / item
                   for item in args.playlist]
        if args.countries:
            targets.extend(sorted((out_dir / "countries").glob("*.m3u")))
        report["patch"] = patch_playlists(targets, report["raw_url"])
    written = write_reports(out_dir / "checks", report,
                            Path(args.epg_dir) if args.epg_dir else out_dir / EPG_DIR_NAME,
                            args.name, report["raw_url"])
    report["edit_log"] = display_path(append_edit_log(out_dir, report))
    (out_dir / "checks" / "epg-build.json").write_text(json.dumps(report, indent=2),
                                                       encoding="utf-8")
    log(f"[epg-build] {report['channels_with_guide']}/{report['playlist_channels']} "
        f"playlist channels have a guide ({report['coverage']:.1%}), "
        f"{report['programmes']} programmes, "
        f"{report['totals']['guides_ok']}/{report['totals']['guides']} guides merged")
    log(f"[epg-build] link: {report['raw_url']}")
    for path in written:
        log(f"[epg-build] wrote {display_path(path)}")
    return 0 if report.get("published") or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
