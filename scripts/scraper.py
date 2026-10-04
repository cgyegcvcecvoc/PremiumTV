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
import hashlib
import html
import http.client
import json
import os
import re
import socket
import ssl
import sys
import threading
import time
import unicodedata
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
# The merged guide this repository publishes (scripts/epg_build.py). General
# playlists advertise it before their source guides; each country playlist uses
# its own root-level EPG/<Country>.xml once that verified file is available.
SELF_EPG_URL = os.environ.get("SELF_EPG_URL") or (
    "https://raw.githubusercontent.com/"
    f"{os.environ.get('GITHUB_REPOSITORY') or 'cgyegcvcecvoc/PremiumTV1'}/main"
    "/EPG/PremiumTV.xml"
)
EPG_DIR = ROOT / "EPG"
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

# A scheduled run that starts this many minutes after its slot is reported as
# late. GitHub's scheduler is not punctual; schedule-guard.yml catches up.
LATE_START_MINUTES = 15
# How many channel names a website channel-index audit keeps as a sample.
CHANNEL_SAMPLE_LIMIT = 12

ANCHOR_RE = re.compile(r"<a\b[^>]*?href\s*=\s*[\"']([^\"']+)[\"'][^>]*>(.*?)</a>",
                       re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
CHANNEL_ID_RE = re.compile(r"[?&](?:id|channel_id|channel|ch)\s*=\s*([A-Za-z0-9_-]+)", re.IGNORECASE)
PLAYLIST_HREF_RE = re.compile(r"(?:\.m3u8?(?:[?#]|$)|[?&/._-](?:playlist|m3u))", re.IGNORECASE)

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

    @property
    def country(self) -> str:
        return resolve_country(self)

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
# Country and A&E classification
# --------------------------------------------------------------------------- #
COUNTRY_CODE_MAP: dict[str, str] = {
    "ad": "Andorra",
    "ae": "United Arab Emirates",
    "af": "Afghanistan",
    "ag": "Antigua and Barbuda",
    "al": "Albania",
    "am": "Armenia",
    "ao": "Angola",
    "ar": "Argentina",
    "at": "Austria",
    "au": "Australia",
    "aw": "Aruba",
    "az": "Azerbaijan",
    "ba": "Bosnia and Herzegovina",
    "bb": "Barbados",
    "bd": "Bangladesh",
    "be": "Belgium",
    "bf": "Burkina Faso",
    "bg": "Bulgaria",
    "bh": "Bahrain",
    "bi": "Burundi",
    "bj": "Benin",
    "bm": "Bermuda",
    "bn": "Brunei",
    "bo": "Bolivia",
    "bq": "Caribbean Netherlands",
    "br": "Brazil",
    "bs": "Bahamas",
    "bt": "Bhutan",
    "bw": "Botswana",
    "by": "Belarus",
    "bz": "Belize",
    "ca": "Canada",
    "ca2": "Canada",
    "cd": "DR Congo",
    "cf": "Central African Republic",
    "cg": "Republic of the Congo",
    "ch": "Switzerland",
    "ci": "Ivory Coast",
    "cl": "Chile",
    "cm": "Cameroon",
    "cn": "China",
    "co": "Colombia",
    "cr": "Costa Rica",
    "cu": "Cuba",
    "cv": "Cape Verde",
    "cw": "Curacao",
    "cy": "Cyprus",
    "cz": "Czechia",
    "de": "Germany",
    "dj": "Djibouti",
    "dk": "Denmark",
    "dm": "Dominica",
    "do": "Dominican Republic",
    "dz": "Algeria",
    "ec": "Ecuador",
    "ee": "Estonia",
    "eg": "Egypt",
    "eh": "Western Sahara",
    "er": "Eritrea",
    "es": "Spain",
    "et": "Ethiopia",
    "fi": "Finland",
    "fj": "Fiji",
    "fo": "Faroe Islands",
    "fr": "France",
    "ga": "Gabon",
    "gb": "UK",
    "gd": "Grenada",
    "ge": "Georgia",
    "gf": "French Guiana",
    "gh": "Ghana",
    "gi": "Gibraltar",
    "gl": "Greenland",
    "gm": "Gambia",
    "gn": "Guinea",
    "gp": "Guadeloupe",
    "gq": "Equatorial Guinea",
    "gr": "Greece",
    "gt": "Guatemala",
    "gu": "Guam",
    "gw": "Guinea-Bissau",
    "gy": "Guyana",
    "hk": "Hong Kong",
    "hn": "Honduras",
    "hr": "Croatia",
    "ht": "Haiti",
    "hu": "Hungary",
    "id": "Indonesia",
    "ie": "Ireland",
    "il": "Israel",
    "in": "India",
    "iq": "Iraq",
    "ir": "Iran",
    "is": "Iceland",
    "it": "Italy",
    "jm": "Jamaica",
    "jo": "Jordan",
    "jp": "Japan",
    "ke": "Kenya",
    "kg": "Kyrgyzstan",
    "kh": "Cambodia",
    "kn": "Saint Kitts and Nevis",
    "kp": "North Korea",
    "kr": "South Korea",
    "kw": "Kuwait",
    "ky": "Cayman Islands",
    "kz": "Kazakhstan",
    "la": "Laos",
    "lb": "Lebanon",
    "lc": "Saint Lucia",
    "li": "Liechtenstein",
    "lk": "Sri Lanka",
    "lr": "Liberia",
    "ls": "Lesotho",
    "lt": "Lithuania",
    "lu": "Luxembourg",
    "lv": "Latvia",
    "ly": "Libya",
    "ma": "Morocco",
    "mc": "Monaco",
    "md": "Moldova",
    "me": "Montenegro",
    "mg": "Madagascar",
    "mk": "North Macedonia",
    "ml": "Mali",
    "mm": "Myanmar",
    "mn": "Mongolia",
    "mo": "Macau",
    "mq": "Martinique",
    "mr": "Mauritania",
    "mt": "Malta",
    "mu": "Mauritius",
    "mv": "Maldives",
    "mw": "Malawi",
    "mx": "Mexico",
    "my": "Malaysia",
    "mz": "Mozambique",
    "na": "Namibia",
    "ne": "Niger",
    "ng": "Nigeria",
    "ni": "Nicaragua",
    "nl": "Netherlands",
    "no": "Norway",
    "np": "Nepal",
    "nz": "New Zealand",
    "om": "Oman",
    "pa": "Panama",
    "pe": "Peru",
    "peacock": "USA",
    "pf": "French Polynesia",
    "pg": "Papua New Guinea",
    "ph": "Philippines",
    "pk": "Pakistan",
    "pl": "Poland",
    "plex": "USA",
    "pr": "Puerto Rico",
    "ps": "Palestine",
    "pt": "Portugal",
    "py": "Paraguay",
    "qa": "Qatar",
    "re": "Reunion",
    "ro": "Romania",
    "rs": "Serbia",
    "ru": "Russia",
    "rw": "Rwanda",
    "sa": "Saudi Arabia",
    "sd": "Sudan",
    "se": "Sweden",
    "sg": "Singapore",
    "si": "Slovenia",
    "sk": "Slovakia",
    "sl": "Sierra Leone",
    "sm": "San Marino",
    "sn": "Senegal",
    "so": "Somalia",
    "sr": "Suriname",
    "ss": "South Sudan",
    "sv": "El Salvador",
    "sx": "Sint Maarten",
    "sy": "Syria",
    "sz": "Eswatini",
    "td": "Chad",
    "tg": "Togo",
    "th": "Thailand",
    "tj": "Tajikistan",
    "tl": "Timor-Leste",
    "tm": "Turkmenistan",
    "tn": "Tunisia",
    "tr": "Turkey",
    "tt": "Trinidad and Tobago",
    "tw": "Taiwan",
    "tz": "Tanzania",
    "ua": "Ukraine",
    "ug": "Uganda",
    "uk": "UK",
    "us": "USA",
    "us2": "USA",
    "us_locals1": "USA",
    "uy": "Uruguay",
    "uz": "Uzbekistan",
    "va": "Vatican City",
    "vc": "Saint Vincent and the Grenadines",
    "ve": "Venezuela",
    "vg": "British Virgin Islands",
    "vi": "US Virgin Islands",
    "vn": "Vietnam",
    "vu": "Vanuatu",
    "ws": "Samoa",
    "xk": "Kosovo",
    "ye": "Yemen",
    "za": "South Africa",
    "zm": "Zambia",
    "zw": "Zimbabwe",
}

GROUP_COUNTRY_PATTERNS: list[tuple[str, str]] = [
    ("united states", "USA"),
    ("usa", "USA"),
    ("u.s.", "USA"),
    ("vod movies (en)", "USA"),
    ("united kingdom", "UK"),
    ("uk", "UK"),
    ("china", "China"),
    ("italia", "Italy"),
    ("italy", "Italy"),
    ("czech", "Czechia"),
    ("türkyie", "Turkey"),
    ("türkiye", "Turkey"),
    ("turkey", "Turkey"),
    ("columbia", "Colombia"),
    ("colombia", "Colombia"),
    ("united arab emirates", "United Arab Emirates"),
    ("south korea", "South Korea"),
    ("north korea", "North Korea"),
    ("north macedonia", "North Macedonia"),
    ("bosnia", "Bosnia and Herzegovina"),
    ("new zealand", "New Zealand"),
    ("costa rica", "Costa Rica"),
    ("dominican republic", "Dominican Republic"),
    ("el salvador", "El Salvador"),
    ("puerto rico", "Puerto Rico"),
    ("saudi arabia", "Saudi Arabia"),
    ("south africa", "South Africa"),
    ("sri lanka", "Sri Lanka"),
    ("hong kong", "Hong Kong"),
    ("trinidad", "Trinidad and Tobago"),
    ("latin america", "Latin America"),
    ("arab world", "Arab World"),
    ("albania", "Albania"),
    ("algeria", "Algeria"),
    ("argentina", "Argentina"),
    ("armenia", "Armenia"),
    ("australia", "Australia"),
    ("austria", "Austria"),
    ("azerbaijan", "Azerbaijan"),
    ("bahrain", "Bahrain"),
    ("bangladesh", "Bangladesh"),
    ("belarus", "Belarus"),
    ("belgium", "Belgium"),
    ("bolivia", "Bolivia"),
    ("brazil", "Brazil"),
    ("bulgaria", "Bulgaria"),
    ("cambodia", "Cambodia"),
    ("cameroon", "Cameroon"),
    ("canada", "Canada"),
    ("chile", "Chile"),
    ("croatia", "Croatia"),
    ("cuba", "Cuba"),
    ("cyprus", "Cyprus"),
    ("denmark", "Denmark"),
    ("ecuador", "Ecuador"),
    ("egypt", "Egypt"),
    ("estonia", "Estonia"),
    ("ethiopia", "Ethiopia"),
    ("finland", "Finland"),
    ("france", "France"),
    ("georgia", "Georgia"),
    ("germany", "Germany"),
    ("ghana", "Ghana"),
    ("greece", "Greece"),
    ("greenland", "Greenland"),
    ("guatemala", "Guatemala"),
    ("guyana", "Guyana"),
    ("haiti", "Haiti"),
    ("honduras", "Honduras"),
    ("hungary", "Hungary"),
    ("iceland", "Iceland"),
    ("india", "India"),
    ("indonesia", "Indonesia"),
    ("iran", "Iran"),
    ("iraq", "Iraq"),
    ("ireland", "Ireland"),
    ("israel", "Israel"),
    ("jamaica", "Jamaica"),
    ("japan", "Japan"),
    ("jordan", "Jordan"),
    ("kazakhstan", "Kazakhstan"),
    ("kenya", "Kenya"),
    ("kosovo", "Kosovo"),
    ("kuwait", "Kuwait"),
    ("kyrgyzstan", "Kyrgyzstan"),
    ("laos", "Laos"),
    ("latvia", "Latvia"),
    ("lebanon", "Lebanon"),
    ("libya", "Libya"),
    ("lithuania", "Lithuania"),
    ("luxembourg", "Luxembourg"),
    ("macau", "Macau"),
    ("malaysia", "Malaysia"),
    ("maldives", "Maldives"),
    ("mali", "Mali"),
    ("malta", "Malta"),
    ("mexico", "Mexico"),
    ("moldova", "Moldova"),
    ("monaco", "Monaco"),
    ("mongolia", "Mongolia"),
    ("montenegro", "Montenegro"),
    ("morocco", "Morocco"),
    ("mozambique", "Mozambique"),
    ("myanmar", "Myanmar"),
    ("nepal", "Nepal"),
    ("netherlands", "Netherlands"),
    ("nicaragua", "Nicaragua"),
    ("nigeria", "Nigeria"),
    ("norway", "Norway"),
    ("oman", "Oman"),
    ("pakistan", "Pakistan"),
    ("palestine", "Palestine"),
    ("panama", "Panama"),
    ("paraguay", "Paraguay"),
    ("peru", "Peru"),
    ("philippines", "Philippines"),
    ("poland", "Poland"),
    ("portugal", "Portugal"),
    ("qatar", "Qatar"),
    ("romania", "Romania"),
    ("russia", "Russia"),
    ("rwanda", "Rwanda"),
    ("senegal", "Senegal"),
    ("serbia", "Serbia"),
    ("singapore", "Singapore"),
    ("slovakia", "Slovakia"),
    ("slovenia", "Slovenia"),
    ("somalia", "Somalia"),
    ("spain", "Spain"),
    ("sudan", "Sudan"),
    ("sweden", "Sweden"),
    ("switzerland", "Switzerland"),
    ("syria", "Syria"),
    ("taiwan", "Taiwan"),
    ("tajikistan", "Tajikistan"),
    ("tanzania", "Tanzania"),
    ("thailand", "Thailand"),
    ("tunisia", "Tunisia"),
    ("turkmenistan", "Turkmenistan"),
    ("uganda", "Uganda"),
    ("ukraine", "Ukraine"),
    ("uruguay", "Uruguay"),
    ("uzbekistan", "Uzbekistan"),
    ("venezuela", "Venezuela"),
    ("vietnam", "Vietnam"),
    ("yemen", "Yemen"),
    ("zimbabwe", "Zimbabwe"),
    ("dltv", "Thailand"),
    ("สารคดี", "Thailand"),
    ("songtopia", "Thailand"),
    ("the watcher documentary", "Thailand"),
]

AE_TVG_ID_PREFIXES = (
    "ae.us",
    "aelatinamerica",
    "a.and.e.",
    "aande",
    "ae-us-",
    "crime360.us",
    "thefirst48.us",
    "plutotvstoragewars.us",
    "storagewars.us",
    "coldcasefiles.us",
    "60daysin.us",
    "hoarders.us",
    "chaosoncam.us",
    "crimescultskillers.us",
    "crimethrillher.us",
    "homemadenation.us",
    "flippingnation.us",
    "isurvived.us",
    "witnesstojustice.us",
    "mysteriesxplored.us",
    "perform.us",
    "alonebyhistory.us",
    "axmen.us",
    "iceroadtruckers.us",
    "xtremeoutdoor.us",
    "crimeplusinvestigation",
    "crime.and.investigation",
    "insidecrime.us",
    "mysterytv.us",
    "worldwartv.uk",
    "dogthebountyhunter.us",
    "duckdynasty.us",
)

AE_NAME_RE = re.compile(
    r"(?:"
    r"\ba\s*&\s*e\b"
    r"|\ba\s*\+\s*e\s+networks\b"
    r"|\bby\s+a\s*&\s*e\b"
    r"|(?<![a-z0-9])a&e(?![a-z0-9])"
    r"|\bcrime\s*360\b"
    r"|\bthe\s+first\s+48\b"
    r"|\bstorage\s+wars\b"
    r"|\bcold\s+case\s+files\b"
    r"|\b60\s+days\s+in\b"
    r"|\bhoarders\b"
    r"|\bchaos\s+on\s+cam\b"
    r"|\bcrimes\s+cults\s+killers\b"
    r"|\bcrime\s+thrillher\b"
    r"|\bhome\.made\.nation\b"
    r"|\bcrime\s*[+&]\s*investigation\b"
    r"|\binside\s+crime\b"
    r"|\bmystery\s+tv\b"
    r"|\bdog\s+the\s+bounty\s+hunter\b"
    r"|\bduck\s+dynasty\b"
    r")",
    re.IGNORECASE,
)


def resolve_country(channel: Channel) -> str:
    """Resolve the country name for a channel from its attributes, ID, or group."""
    tc = channel.attrs.get("tvg-country", "").strip().lower()
    if tc in COUNTRY_CODE_MAP:
        return COUNTRY_CODE_MAP[tc]
    tid = channel.attrs.get("tvg-id", "").strip()
    if "." in tid:
        suf = tid.rsplit(".", 1)[-1].split("@")[0].lower()
        if suf in COUNTRY_CODE_MAP:
            return COUNTRY_CODE_MAP[suf]
    grp = channel.group.lower()
    for pattern, country in GROUP_COUNTRY_PATTERNS:
        if pattern in grp:
            return country
    if re.search(r"[\u0e00-\u0e7f]", f"{channel.name} {channel.group}"):
        return "Thailand"
    return "International"


def country_filename(country: str) -> str:
    """Turn a country display name into a clean M3U filename (e.g. 'USA.m3u', 'South_Korea.m3u')."""
    slug = re.sub(r"[^A-Za-z0-9]+", "_", country.strip()).strip("_")
    return f"{slug or 'International'}.m3u"


def country_epg_url(country: str) -> str:
    """Raw URL for this country's independently generated XMLTV guide."""
    stem = Path(country_filename(country)).stem
    return f"{SELF_EPG_URL.rsplit('/', 1)[0]}/{stem}.xml"


def is_ae_channel(channel: Channel) -> bool:
    """Return True if a channel belongs to A&E or A+E Networks."""
    if channel.source == "ae-networks" or "ae-networks" in channel.source_aliases:
        return True
    tid = channel.attrs.get("tvg-id", "").strip().lower()
    if tid and any(tid.startswith(prefix) for prefix in AE_TVG_ID_PREFIXES):
        return True
    low_url = channel.url.lower()
    if "aenetworks" in low_url or "aetelevisionnetworks" in low_url:
        return True
    if AE_NAME_RE.search(channel.name) or AE_NAME_RE.search(channel.group):
        return True
    return False


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
    """Fetch a source, reading a curated local_path first when configured, or falling back to GitHub API."""
    local_rel = str(src.get("local_path") or "").strip()
    if local_rel:
        local_file = Path(local_rel) if Path(local_rel).is_absolute() else (ROOT / local_rel)
        if local_file.exists():
            src["_fetch_method"] = "local_file"
            return local_file.read_text(encoding="utf-8")
    try:
        text = http_get(src["url"])
        src["_fetch_method"] = "direct"
        return text
    except Exception as exc:  # noqa: BLE001
        github = src.get("github")
        if not github or not github.get("repo") or not github.get("path"):
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
    """Repair common typos found in upstream lists (e.g. 'ttp://host') and percent-encode non-ASCII paths."""
    url = url.strip()
    low = url.lower()
    if low.startswith(("ttp://", "ttps://")):
        url = "h" + url
    elif low.startswith("//"):
        url = "https:" + url
    if any(ch.isspace() for ch in url):
        return url
    try:
        url.encode("ascii")
        return url
    except UnicodeEncodeError:
        try:
            parts = urllib.parse.urlsplit(url)
            if not parts.scheme or not parts.netloc:
                return url
            netloc = parts.netloc.encode("idna").decode("ascii")
            path = urllib.parse.quote(parts.path, safe="/:@!$&'()*+,;=-._~%")
            query = urllib.parse.quote(parts.query, safe="=&/:@!$'()*+,;-._~%?[]")
            fragment = urllib.parse.quote(parts.fragment, safe="")
            return urllib.parse.urlunsplit((parts.scheme, netloc, path, query, fragment))
        except Exception:  # noqa: BLE001
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


def _loads_w3u_json(raw_text: str) -> dict:
    """Parse W3U JSON, tolerating trailing commas before closing braces/brackets."""
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        cleaned = re.sub(r",(\s*[}\]])", r"\1", raw_text)
        data = json.loads(cleaned)
    if not isinstance(data, dict):
        raise ValueError("W3U JSON root is not an object")
    return data


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
            if depth == 0 and include and not _match_any(group_name, include, exact=True):
                continue
            if exclude and _match_any(group_name, exclude, exact=False):
                continue
            if not group_url:
                if group.get("stations") or group.get("groups"):
                    walk(group, path + [group_name], depth + 1)
                continue
            if group_url in seen_urls:
                continue
            seen_urls.add(group_url)
            try:
                child = _loads_w3u_json(http_get(group_url, retries=1))
            except Exception as exc:  # noqa: BLE001
                message = f"nested group '{group_name}' fetch failed: {error_text(exc, group_url)}"
                log(f"    ! {message}")
                if issues is not None:
                    issues.append(message)
                continue
            walk(child, path + [group_name], depth + 1)

    data = _loads_w3u_json(root_text)
    walk(data, [], 0)
    return output


# --------------------------------------------------------------------------- #
# Reference-source audits
# --------------------------------------------------------------------------- #
def clean_channel_name(raw: str) -> str:
    """Turn the inner HTML of a channel link into a readable channel name."""
    text = html.unescape(TAG_RE.sub(" ", raw or ""))
    # Index pages often repeat the numeric id inside the link text ("ID: 51").
    text = re.sub(r"(?i)\bid\s*[:#]?\s*\d+\b", " ", text)
    return WHITESPACE_RE.sub(" ", text).strip(" \t-–—|·:,")


def parse_channel_index(text: str, href_regex: str, base_url: str = "") -> dict:
    """Extract the catalogue an HTML channel-index page links to.

    Only the catalogue is read: nothing found here is treated as a playable
    stream. Sites such as DaddyLiveHD publish their channels as HTML player
    pages whose stream address is resolved by JavaScript at run time, so
    importing those links would add hundreds of entries that the link checker
    can only report as "html page, not a stream".
    """
    try:
        pattern = re.compile(href_regex, re.IGNORECASE)
    except re.error as exc:
        raise ValueError(f"invalid channel_href_regex {href_regex!r}: {exc}") from exc

    channels: list[dict] = []
    by_key: dict[str, dict] = {}
    for href, inner in ANCHOR_RE.findall(text or ""):
        href = html.unescape(href.strip())
        if not href or href.startswith(("#", "javascript:", "mailto:")):
            continue
        if not pattern.search(href):
            continue
        url = urllib.parse.urljoin(base_url, href) if base_url else href
        match = CHANNEL_ID_RE.search(url)
        ident = match.group(1) if match else ""
        key = ident or url
        name = clean_channel_name(inner)
        entry = by_key.get(key)
        if entry is None:
            entry = {"id": ident, "name": name or f"Channel {ident or len(by_key) + 1}",
                     "url": safe_url(url)}
            by_key[key] = entry
            channels.append(entry)
        elif name and (not entry["name"] or entry["name"].startswith("Channel ")):
            # The same channel is often linked twice (logo + text); keep a name.
            entry["name"] = name
    return {
        "count": len(channels),
        "with_id": sum(1 for c in channels if c["id"]),
        "channels": channels,
        "sample": [c["name"] for c in channels[:CHANNEL_SAMPLE_LIMIT]],
    }


def find_playlist_links(text: str, base_url: str = "") -> list[str]:
    """Every .m3u/.m3u8 or playlist-looking href on a page, made absolute."""
    found: list[str] = []
    for href, _ in ANCHOR_RE.findall(text or ""):
        href = html.unescape(href.strip())
        if not href or href.startswith(("#", "javascript:", "mailto:")):
            continue
        if not PLAYLIST_HREF_RE.search(href):
            continue
        url = urllib.parse.urljoin(base_url, href) if base_url else href
        if url not in found:
            found.append(url)
    return [safe_url(url) for url in found[:10]]


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

    if kind == "website_channel_index":
        # An HTML page that lists channels but publishes no playlist file. The
        # catalogue is counted so the report shows what the site offers; the
        # links themselves are HTML player pages and are never imported.
        url = item.get("url", "")
        result["url"] = safe_url(url)
        text = http_get(url, timeout=float(item.get("timeout", 25)), retries=0)
        href_regex = str(item.get("channel_href_regex") or r"watch\.php\?id=\d+")
        index = parse_channel_index(text, href_regex, url)
        playlist_links = find_playlist_links(text, url)
        is_playlist = text.lstrip().startswith("#EXTM3U")
        if is_playlist or playlist_links:
            ingest_status = "static_playlist_found_not_configured"
        elif index["count"]:
            ingest_status = "player_pages_only"
        else:
            ingest_status = "no_channels_found"
        result.update({
            "status": "reachable",
            "reachable": True,
            "response_bytes": len(text.encode("utf-8")),
            "playlist_detected": is_playlist,
            "channel_count": index["count"],
            "channels_with_id": index["with_id"],
            "sample_channels": index["sample"],
            "playlist_links": playlist_links,
            "player_url_template": str(item.get("player_url_template", "")),
            "ingest_status": ingest_status,
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
                elif result.get("channel_count") is not None:
                    log(f"[audit:{name}] channel index reachable; channels listed={result['channel_count']}; "
                        f"playlist links={len(result.get('playlist_links') or [])}; "
                        f"ingest={result.get('ingest_status')}; channels imported=no")
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
HIGH_CAPACITY_HOSTS = (
    "jmp2.uk",
    "pluto.tv",
    "cloudfront.net",
    "akamaized.net",
    "amagi.tv",
    "wurl.tv",
    "uplynk.com",
    "stream.mcquack.net",
    "playlist.xtemus.com",
)


class HostLimiter:
    """Keep a burst of parallel checks from overwhelming any single host, and fast-fail dead hosts."""
    def __init__(self, per_host_workers: int):
        self.per_host_workers = max(1, per_host_workers)
        self._lock = threading.Lock()
        self._semaphores: dict[str, threading.BoundedSemaphore] = {}
        self._consecutive_failures: collections.Counter = collections.Counter()
        self._responses: collections.Counter = collections.Counter()

    @staticmethod
    def _host_key(url: str) -> str:
        parsed = urllib.parse.urlsplit(url)
        netloc = parsed.netloc.lower().rsplit("@", 1)[-1]
        return f"{parsed.scheme.lower()}://{netloc}"

    def _limit_for_key(self, key: str) -> int:
        host = key.split("://", 1)[-1].split(":", 1)[0]
        if any(host == suffix or host.endswith("." + suffix) for suffix in HIGH_CAPACITY_HOSTS):
            return max(self.per_host_workers, 32)
        return self.per_host_workers

    def semaphore_for(self, url: str) -> threading.BoundedSemaphore:
        key = self._host_key(url)
        with self._lock:
            if key not in self._semaphores:
                self._semaphores[key] = threading.BoundedSemaphore(self._limit_for_key(key))
            return self._semaphores[key]

    def record_response(self, url: str) -> None:
        key = self._host_key(url)
        with self._lock:
            self._responses[key] += 1
            self._consecutive_failures[key] = 0

    def record_connection_failure(self, url: str) -> None:
        key = self._host_key(url)
        with self._lock:
            self._consecutive_failures[key] += 1

    def is_unresponsive(self, url: str, threshold: int = 5) -> bool:
        key = self._host_key(url)
        with self._lock:
            return self._responses[key] == 0 and self._consecutive_failures[key] >= threshold


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


def _classify_stream_body(channel: Channel, body: bytes, content_type: str) -> Channel:
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


# --------------------------------------------------------------------------- #
# Dead-link quarantine
# --------------------------------------------------------------------------- #
# The daily check only proves a server answered. scripts/link_check.py proves a
# stream actually plays, and records the links that answered but served no media
# in playlists/checks/quarantine.json. Those links are held back here for a few
# days so a shallow scrape cannot put a known-dead link back in the player
# playlist between two deep checks.
QUARANTINE_FILENAME = "quarantine.json"


def load_quarantine(path: Path, days: float) -> dict:
    """Read the quarantine file, dropping entries older than `days`."""
    if days <= 0 or not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, dict):
        return {}
    if days <= 0:
        return entries
    cutoff = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    fresh = {}
    for url, entry in entries.items():
        if not isinstance(entry, dict) or not url:
            continue
        last_seen = parse_utc_iso(str(entry.get("last_seen_utc") or ""))
        if last_seen is None or last_seen.replace(tzinfo=None) >= cutoff.replace(tzinfo=None):
            fresh[url] = entry
    return fresh


def apply_quarantine(channels: list, path: Path, days: float = 7.0) -> int:
    """Mark quarantined links dead so they cannot be published. Returns the count."""
    entries = load_quarantine(path, days)
    if not entries:
        return 0
    held = 0
    for channel in channels:
        entry = entries.get(channel.url or "")
        if not entry:
            continue
        if channel.status not in ("alive", "unverified", "unchecked"):
            continue
        hits = entry.get("hits", 1)
        channel.status = "dead"
        channel.reason = (
            f"quarantined: {entry.get('reason') or 'served no media on the deep check'} "
            f"(failed the deep check {hits}x, last {entry.get('last_seen_utc', 'recently')})"
        )
        held += 1
    return held


def check_channel(
    channel: Channel,
    timeout: float,
    retries: int = 2,
    host_limiter: HostLimiter | None = None,
) -> Channel:
    """Check a stream; transient/access failures are kept distinct from confirmed dead links."""
    if not channel.url or any(ch.isspace() for ch in channel.url):
        channel.status, channel.reason = "dead", "invalid URL"
        return channel
    try:
        parsed = urllib.parse.urlsplit(channel.url)
        scheme = parsed.scheme.lower()
    except ValueError:
        channel.status, channel.reason = "dead", "invalid URL"
        return channel

    if scheme in NON_HTTP_SCHEMES:
        # These schemes cannot be probed by an HTTP GET, so do not label them alive.
        channel.status, channel.reason = "unverified", f"not probed: unsupported scheme {scheme}"
        return channel
    if scheme not in ("http", "https") or not parsed.netloc:
        channel.status, channel.reason = "dead", "invalid URL"
        return channel

    headers = channel.headers()
    headers.setdefault("Accept", "*/*")
    unresponsive = host_limiter.is_unresponsive(channel.url) if host_limiter else False
    effective_retries = 0 if unresponsive else max(0, retries)
    effective_timeout = min(timeout, 2.5) if unresponsive else timeout
    attempts = effective_retries + 1

    for attempt in range(attempts):
        try:
            request = urllib.request.Request(channel.url, headers=headers)
            semaphore = host_limiter.semaphore_for(channel.url) if host_limiter else None
            if semaphore:
                semaphore.acquire()
            try:
                with urllib.request.urlopen(request, timeout=effective_timeout, context=INSECURE_CTX) as response:
                    content_type = (response.headers.get("Content-Type") or "").lower()
                    try:
                        body = response.read(4096)
                    except http.client.IncompleteRead as inc:
                        body = inc.partial or b""
            finally:
                if semaphore:
                    semaphore.release()

            if host_limiter:
                host_limiter.record_response(channel.url)
            return _classify_stream_body(channel, body, content_type)
        except http.client.InvalidURL:
            channel.status, channel.reason = "dead", "invalid URL"
            return channel
        except urllib.error.HTTPError as exc:
            if host_limiter:
                host_limiter.record_response(channel.url)
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
        except (
            urllib.error.URLError,
            http.client.HTTPException,
            socket.timeout,
            TimeoutError,
            ConnectionError,
            ssl.SSLError,
            OSError,
        ) as exc:
            if host_limiter:
                host_limiter.record_connection_failure(channel.url)
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
            for attr_key, attr_val in channel.attrs.items():
                if attr_val and not existing.attrs.get(attr_key):
                    existing.attrs[attr_key] = attr_val
    return output


def sort_key(channel: Channel):
    return (channel.group.lower(), re.sub(r"\W+", "", channel.name.lower()), channel.source)


def synthetic_tvg_id(channel: Channel) -> str:
    """Stable repo-scoped id for a published channel whose source has no tvg-id."""
    country = channel.country or "International"
    def slug(value: str, fallback: str) -> str:
        ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
        result = re.sub(r"[^a-z0-9]+", "_", ascii_value.lower()).strip("_")
        if not result:
            result = fallback
        if len(result) > 72:
            digest = hashlib.sha1(value.encode("utf-8", errors="replace")).hexdigest()[:10]
            result = f"{result[:61].rstrip('_')}_{digest}"
        return result

    name = channel.name.strip() or channel.url
    country_slug = slug(country, "international")
    name_slug = slug(name, "channel_" + hashlib.sha1(name.encode("utf-8", errors="replace")).hexdigest()[:10])
    return f"premiumtv.{country_slug}.{name_slug}"


def write_m3u(path: Path, channels: list[Channel], epg: list[str], title: str,
              advertise_self: bool = True, synthesize_missing_ids: bool = False) -> None:
    """Write a playlist, advertising the repository's matching XMLTV first.

    General playlists use ``SELF_EPG_URL`` and may retain verified upstream
    guides behind it as fallbacks. Country playlists pass their one country
    guide with ``advertise_self=False``. Source caches also use that flag and
    keep their upstream metadata unchanged. Published player playlists can set
    ``synthesize_missing_ids`` so channels without a source ``tvg-id`` receive
    stable repo-scoped ids that the generated XMLTV can declare and match.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if synthesize_missing_ids:
        for channel in channels:
            if not channel.attrs.get("tvg-id", "").strip():
                channel.attrs["tvg-id"] = synthetic_tvg_id(channel)
    header = "#EXTM3U"
    guides = list(dict.fromkeys(
        ([SELF_EPG_URL] if advertise_self and SELF_EPG_URL else []) + list(epg)))
    if guides:
        header += f' x-tvg-url="{",".join(guides)}"'
    lines = [header, f"# {title}"]
    lines += [channel.to_m3u() for channel in channels]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_country_playlists(
    out_dir: Path,
    channels: list[Channel],
    epg: list[str],
    utc_s: str,
    local_s: str,
    label: str,
) -> dict[str, dict]:
    """Separate confirmed working channels by country into playlists/countries/<Country>.m3u."""
    countries_dir = out_dir / "countries"
    countries_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[Channel]] = collections.defaultdict(list)
    for channel in channels:
        grouped[channel.country].append(channel)

    ordered_countries = sorted(grouped.keys(), key=lambda name: (-len(grouped[name]), name.lower()))
    active_files: set[str] = set()
    summary: dict[str, dict] = {}

    for country in ordered_countries:
        country_channels = sorted(grouped[country], key=sort_key)
        fname = country_filename(country)
        active_files.add(fname)
        # Use a country-scoped guide on its own. If this is a newly added
        # country whose XMLTV has not been built yet, retain the merged guide
        # and source fallbacks until the immediately-following EPG build runs.
        country_guide = EPG_DIR / f"{Path(fname).stem}.xml"
        guides = ([country_epg_url(country)] if country_guide.is_file()
                  else ([SELF_EPG_URL] if SELF_EPG_URL else []) + list(epg))
        write_m3u(
            countries_dir / fname,
            country_channels,
            guides,
            f"{country} working channels ({len(country_channels)}) - updated {utc_s} ({local_s}) - {label}",
            advertise_self=False,
            synthesize_missing_ids=True,
        )
        summary[country] = {
            "file": f"countries/{fname}",
            "count": len(country_channels),
        }

    for existing in countries_dir.glob("*.m3u"):
        if existing.name not in active_files:
            try:
                existing.unlink()
            except OSError:
                pass

    index_lines = [
        "# Country Playlists",
        "",
        f"Updated: **{local_s}** ({utc_s}) — _{label}_",
        "",
        f"Total countries: **{len(summary)}**  |  Total confirmed working channels: **{len(channels)}**",
        "",
        "| Country | Working channels | Playlist file | Country EPG (`.xml`) | Raw M3U URL | Raw EPG URL |",
        "|---|---:|---|---|---|---|",
    ]
    for country, info in summary.items():
        fname = Path(info["file"]).name
        raw_url = f"https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/countries/{fname}"
        epg_url = country_epg_url(country)
        epg_file = f"../../EPG/{Path(fname).stem}.xml"
        index_lines.append(
            f"| {country} | {info['count']} | [`{fname}`]({fname}) | "
            f"[`{Path(fname).stem}.xml`]({epg_file}) | `{raw_url}` | `{epg_url}` |"
        )
    (countries_dir / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return summary


def summarize_ae_channels(channels: list[Channel]) -> dict:
    """Summarize A&E / A+E Networks channels and their check statuses."""
    ae_all = [channel for channel in channels if is_ae_channel(channel)]
    ae_working = [channel for channel in ae_all if channel.status == "alive"]
    ae_dead = [channel for channel in ae_all if channel.status == "dead"]
    ae_unverified = [channel for channel in ae_all if channel.status == "unverified"]
    return {
        "file": "AE_Channels.m3u",
        "total_unique": len(ae_all),
        "working_count": len(ae_working),
        "dead_count": len(ae_dead),
        "unverified_count": len(ae_unverified),
        "working": [report_channel(channel) for channel in ae_working],
        "dead": [report_channel(channel) for channel in ae_dead],
        "unverified": [report_channel(channel) for channel in ae_unverified],
    }


def write_ae_playlist(
    out_dir: Path,
    working_channels: list[Channel],
    epg: list[str],
    utc_s: str,
    local_s: str,
    label: str,
) -> int:
    """Write confirmed working A&E / A+E Networks channels to playlists/AE_Channels.m3u."""
    ae_working = sorted([channel for channel in working_channels if is_ae_channel(channel)], key=sort_key)
    write_m3u(
        out_dir / "AE_Channels.m3u",
        ae_working,
        epg,
        f"A&E and A+E Networks working channels ({len(ae_working)}) - updated {utc_s} ({local_s}) - {label}",
        synthesize_missing_ids=True,
    )
    return len(ae_working)


def now_strings(when: dt.datetime | None = None) -> tuple[str, str]:
    utc = when or dt.datetime.now(dt.timezone.utc)
    if utc.tzinfo is None:
        utc = utc.replace(tzinfo=dt.timezone.utc)
    utc = utc.astimezone(dt.timezone.utc)
    local = utc.astimezone(NY_TZ) if NY_TZ else utc
    return utc.strftime("%Y-%m-%d %H:%M UTC"), local.strftime("%Y-%m-%d %I:%M %p %Z")


def parse_utc_iso(value: str) -> dt.datetime | None:
    """Parse an ISO-8601 timestamp into an aware UTC datetime."""
    text = str(value or "").strip().replace("Z", "+00:00")
    if not text:
        return None
    try:
        moment = dt.datetime.fromisoformat(text)
    except ValueError:
        return None
    return (moment if moment.tzinfo else moment.replace(tzinfo=dt.timezone.utc)).astimezone(dt.timezone.utc)


def format_delay(minutes: float | None) -> str:
    """Render a delay in minutes as e.g. '+6h 51m' or '+4m'."""
    if minutes is None:
        return "-"
    if minutes < 0:
        return f"-{format_delay(-minutes).lstrip('+')}"
    total = int(round(minutes))
    hours, mins = divmod(total, 60)
    return f"+{hours}h {mins:02d}m" if hours else f"+{mins}m"



def classify_run(label: str) -> str:
    low = label.lower()
    if "monthly" in low or "discovery" in low:
        return "monthly_discovery"
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


def load_approved_sources(approved_path: str, source_items: list) -> tuple[list, list[dict]]:
    """Merge sources vetted by the monthly discovery engine into the source list.

    The file is written by scripts/discover.py. Entries are additive: anything
    already configured in sources.json wins, and a promoted entry can be rolled
    back by removing it or setting "enabled": false in approved-sources.json.
    """
    path = Path(approved_path)
    if not path.exists():
        return source_items, []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        log(f"[discover] ignoring unreadable {path}: {error_text(exc)}")
        return source_items, []
    if not isinstance(data, dict) or not isinstance(data.get("sources"), list):
        return source_items, []

    known = {str(item.get("name")) for item in source_items if isinstance(item, dict)}
    merged = list(source_items)
    promoted: list[dict] = []
    for entry in data["sources"]:
        if not isinstance(entry, dict):
            continue
        name = str(entry.get("name") or "").strip()
        if not name or name in known or not entry.get("enabled", True):
            continue
        if not str(entry.get("url") or "").strip() and not entry.get("url_env"):
            continue
        known.add(name)
        merged.append({**entry, "promoted_by_discovery": True})
        promoted.append(entry)
    return merged, promoted


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
    sample_limit = 30
    return {
        "baseline": baseline,
        "added_count": len(added_urls),
        "removed_count": len(removed_urls),
        "added_sample": [
            {"name": current[url].name, "country": current[url].country, "group": current[url].group,
             "source": current[url].source, "url": safe_url(url)}
            for url in added_urls[:sample_limit]
        ],
        "removed_sample": [
            {"name": previous[url].name, "country": previous[url].country, "group": previous[url].group,
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
        "country": channel.country,
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

    countries = report.get("countries") or {}
    ae_info = report.get("ae_channels") or {}

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
        f"- **Country playlists:** [`countries/`](countries/README.md) ({len(countries)} countries separated)",
        f"- **A&E channels playlist:** [`AE_Channels.m3u`](AE_Channels.m3u) "
        f"({ae_info.get('working_count', 0)} confirmed working / {ae_info.get('total_unique', 0)} unique A&E links)",
        "- **Plain-text (.txt) logs:** "
        "[`logs/scrape-log.txt`](logs/scrape-log.txt) | "
        "[`logs/log-edits.txt`](logs/log-edits.txt) | "
        "[`logs/errors.txt`](logs/errors.txt) | "
        "[`logs/run-history.txt`](logs/run-history.txt)",
        f"- **Run history:** [`run-history.jsonl`](run-history.jsonl) (append-only; one entry per run)",
        "",
        "## Playlist sources",
        "",
        "| Source | Fetch | Entries | Unique URLs | Overlap | Working | Dead | Unverified |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, stat in report["sources"].items():
        label = f"{name} 🌱" if stat.get("promoted_by_discovery") else name
        lines.append(
            f"| {label} | {stat.get('status', 'unknown')} | {stat.get('found', 0)} | "
            f"{stat.get('unique', 0)} | {stat.get('overlap', 0)} | {stat.get('alive', 0)} | "
            f"{stat.get('dead', 0)} | {stat.get('unverified', 0)} |"
        )
    promoted = [name for name, stat in report["sources"].items() if stat.get("promoted_by_discovery")]
    if promoted:
        lines += [
            "",
            f"🌱 = source added automatically by the monthly discovery engine: {', '.join(promoted)}. "
            "Set `\"enabled\": false` for it in `discovery/approved-sources.json` to roll it back.",
        ]

    if countries:
        lines += [
            "",
            f"## Country playlists (`playlists/countries/` — {len(countries)} countries)",
            "",
            "All confirmed working channels are separated by country into [`playlists/countries/`](countries/README.md). "
            "Top 25 countries by working channel count:",
            "",
            "| Country | Working channels | Playlist |",
            "|---|---:|---|",
        ]
        for country, info in list(countries.items())[:25]:
            lines.append(f"| {country} | {info['count']} | [`{info['file']}`]({info['file']}) |")
        if len(countries) > 25:
            lines.append(f"| _…and {len(countries) - 25} more countries_ | | [Full country index](countries/README.md) |")

    if ae_info.get("total_unique"):
        lines += [
            "",
            "## A&E and A+E Networks channels (`playlists/AE_Channels.m3u`)",
            "",
            f"- **Confirmed working:** {ae_info.get('working_count', 0)} / {ae_info.get('total_unique', 0)} unique links "
            f"(dead: {ae_info.get('dead_count', 0)}, unverified: {ae_info.get('unverified_count', 0)})",
        ]

    lines += [
        "",
        "## Reference-source checks (not automatically imported)",
        "",
        "| Reference | Check | Channels seen | Playlist links | Ingest status | Note |",
        "|---|---|---:|---:|---|---|",
    ]
    for name, result in report["reference_checks"].items():
        files = result.get("static_playlist_files")
        links = result.get("playlist_links")
        playlist_count = len(files) if files is not None else (len(links) if links is not None else 0)
        channels = result.get("channel_count")
        note = result.get("note", "").replace("|", "\\|")
        if result.get("archived"):
            note = f"{note} (repository is archived)".strip()
        if result.get("error"):
            note = f"{note} — {result['error']}".strip(" —")
        lines.append(
            f"| {name} | {result.get('status', 'unknown')} | "
            f"{'-' if channels is None else channels} | {playlist_count} | "
            f"{result.get('ingest_status', 'not_imported')} | {note} |"
        )
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
    if report.get("scheduled_for_utc"):
        delay = report.get("schedule_delay_minutes")
        verdict = ("on time" if isinstance(delay, (int, float)) and delay < LATE_START_MINUTES
                   else f"late by {format_delay(delay)}")
        # Directly under the "Run:" bullet: punctuality is the first thing to see.
        lines.insert(4, f"- **Scheduled for:** {report['scheduled_for_utc']} — started {verdict}")
    return "\n".join(lines) + "\n"


def _format_edit_block_from_history(entry: dict) -> str:
    """Format a historical run-history.jsonl record into a plain-text log-edits block."""
    sep = "=" * 88
    lines = [
        sep,
        f"RUN ID:       {entry.get('run_id', '-')}",
        f"TIMESTAMP:    {entry.get('updated_local', '-')} ({entry.get('started_utc', '-')} -> {entry.get('finished_utc', '-')})",
        f"LABEL / TYPE: {entry.get('label', '-')} [{entry.get('run_type', '-')}]",
        f"STATUS:       {str(entry.get('status', 'unknown')).upper()} (checked={entry.get('checked')}, duration={entry.get('duration_seconds', 0)}s)",
        f"PLAYLISTS:    working={entry.get('working')} / unique={entry.get('total_unique')} "
        f"(dead={entry.get('dead', 0)}, unverified={entry.get('unverified', 0)})",
        f"LOG EDITS:    +{entry.get('added', 0)} channels added / -{entry.get('removed', 0)} channels removed",
    ]
    issues = entry.get("issues") or []
    if issues:
        lines.append("ISSUES / ERRORS:")
        for issue in issues:
            lines.append(f"  * {issue}")
    else:
        lines.append("ISSUES / ERRORS: None")
    lines.append("")
    return "\n".join(lines)


def write_txt_logs(out_dir: Path, report: dict, history_path: Path) -> None:
    """Write human-readable .txt log files under playlists/logs/ for run logs, log edits, and errors."""
    logs_dir = out_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    sep = "=" * 88
    subsep = "-" * 88

    countries = report.get("countries") or {}
    ae_info = report.get("ae_channels") or {}
    changes = report.get("changes") or {}

    # 1. playlists/logs/scrape-log.txt (complete latest-run plain-text log)
    scrape_lines = [
        sep,
        "PREMIUMTV1 SCRAPER RUN LOG (.TXT)",
        sep,
        f"Run ID:                  {report['run_id']}",
        f"Run Label:               {report['label']} ({report['run_type']})",
        f"Started (UTC):           {report['started_utc_iso']}",
        f"Finished (UTC):          {report['finished_utc_iso']}",
        f"Local Time (New York):   {report['updated_local']}",
        f"Duration:                {report['duration_seconds']} seconds",
        f"Outcome Status:          {report['status'].upper()}",
        f"Link Check Completed:    {report['check_completed']}",
        f"Player Playlist Updated: {'YES' if report['final_playlist_written'] else 'NO'}",
        f"Total Input Entries:     {report['total_input_entries']}",
        f"Total Unique URLs:       {report['total_unique']}",
        f"Confirmed Working:       {report['working']}",
        f"Confirmed Dead:          {report['dead_count']}",
        f"Unverified:              {report['unverified_count']}",
        f"Log Edits (vs {changes.get('baseline', 'previous')}): +{changes.get('added_count', 0)} added / -{changes.get('removed_count', 0)} removed",
        f"Countries Separated:     {len(countries)} country playlists in playlists/countries/",
        f"A&E Working Channels:    {ae_info.get('working_count', 0)} / {ae_info.get('total_unique', 0)} unique links (playlists/AE_Channels.m3u)",
        "",
        subsep,
        "1. PLAYLIST SOURCES",
        subsep,
        f"{'Source':<26} {'Status':<15} {'Entries':>8} {'Unique':>8} {'Overlap':>8} {'Working':>8} {'Dead':>8} {'Unverif':>8}",
        "-" * 95,
    ]
    for name, stat in report["sources"].items():
        scrape_lines.append(
            f"{name:<26} {str(stat.get('status', 'unknown')):<15} "
            f"{stat.get('found', 0):>8} {stat.get('unique', 0):>8} {stat.get('overlap', 0):>8} "
            f"{stat.get('alive', 0):>8} {stat.get('dead', 0):>8} {stat.get('unverified', 0):>8}"
        )

    scrape_lines += [
        "",
        subsep,
        f"2. A&E AND A+E NETWORKS CHANNELS ({ae_info.get('working_count', 0)} WORKING / {ae_info.get('total_unique', 0)} UNIQUE)",
        subsep,
    ]
    for item in ae_info.get("working") or []:
        scrape_lines.append(f"  [WORKING] [{item.get('country', 'USA')}] {item['name']} -> {item['url']}")
    for item in ae_info.get("dead") or []:
        scrape_lines.append(f"  [DEAD: {item['reason']}] [{item.get('country', 'USA')}] {item['name']} -> {item['url']}")
    for item in ae_info.get("unverified") or []:
        scrape_lines.append(f"  [UNVERIFIED: {item['reason']}] [{item.get('country', 'USA')}] {item['name']} -> {item['url']}")
    if not ae_info.get("total_unique"):
        scrape_lines.append("  No A&E channels configured in this run.")

    scrape_lines += [
        "",
        subsep,
        f"3. COUNTRY PLAYLISTS SUMMARY ({len(countries)} COUNTRIES IN playlists/countries/)",
        subsep,
        f"{'Country':<34} {'Working':>10}   {'Playlist Path'}",
        "-" * 80,
    ]
    for country, info in countries.items():
        scrape_lines.append(f"{country:<34} {info['count']:>10}   playlists/{info['file']}")

    scrape_lines += [
        "",
        subsep,
        "4. LOG EDITS IN THIS RUN (ADDED & REMOVED CHANNELS)",
        subsep,
        f"Baseline: {changes.get('baseline', 'none')}",
        f"Added:    +{changes.get('added_count', 0)} channels",
        f"Removed:  -{changes.get('removed_count', 0)} channels",
    ]
    if changes.get("added_sample"):
        scrape_lines.append("\nAdded Channels (sample):")
        for item in changes["added_sample"]:
            scrape_lines.append(
                f"  + [{item.get('country', 'International')}] {item['name']} "
                f"(source={item['source']}, group={item['group']}) -> {item['url']}"
            )
    if changes.get("removed_sample"):
        scrape_lines.append("\nRemoved Channels (sample):")
        for item in changes["removed_sample"]:
            scrape_lines.append(
                f"  - [{item.get('country', 'International')}] {item['name']} "
                f"(source={item['source']}, group={item['group']}) -> {item['url']}"
            )

    scrape_lines += [
        "",
        subsep,
        "5. DIAGNOSTICS & RUN/SOURCE ISSUES",
        subsep,
    ]
    if report["diagnostics"]:
        scrape_lines.append(f"{'Reason':<38} {'Dead':>8} {'Unverified':>12}   {'Guidance'}")
        scrape_lines.append("-" * 100)
        for diag in report["diagnostics"]:
            scrape_lines.append(
                f"{diag['reason']:<38} {diag['dead']:>8} {diag['unverified']:>12}   {diag['guidance']}"
            )
    else:
        scrape_lines.append("No link-check failures or unverified links recorded.")

    scrape_lines.append("\nRun / Source Issues:")
    if report["issues"]:
        for issue in report["issues"]:
            scrape_lines.append(f"  * {issue}")
    else:
        scrape_lines.append("  None.")

    (logs_dir / "scrape-log.txt").write_text("\n".join(scrape_lines) + "\n", encoding="utf-8")

    # 2. playlists/logs/log-edits.txt (append-only chronological log of edits across runs)
    edits_path = logs_dir / "log-edits.txt"
    history_entries: list[dict] = []
    if history_path.exists():
        for raw_line in history_path.read_text(encoding="utf-8").splitlines():
            raw_line = raw_line.strip()
            if not raw_line:
                continue
            try:
                history_entries.append(json.loads(raw_line))
            except json.JSONDecodeError:
                continue

    if not edits_path.exists():
        header_lines = [
            sep,
            "PREMIUMTV1 CHRONOLOGICAL LOG EDITS (.TXT)",
            "Tracks every scraper run's playlist edits (+added / -removed channels), country separation,",
            "A&E channel checks, and any source or link errors.",
            sep,
            "",
        ]
        # Seed prior runs from run-history.jsonl (all except the current run_id)
        for past in history_entries:
            if past.get("run_id") != report["run_id"]:
                header_lines.append(_format_edit_block_from_history(past))
        edits_path.write_text("\n".join(header_lines), encoding="utf-8")

    current_edit_lines = [
        sep,
        f"RUN ID:       {report['run_id']}",
        f"TIMESTAMP:    {report['updated_local']} ({report['started_utc_iso']} -> {report['finished_utc_iso']})",
        f"LABEL / TYPE: {report['label']} [{report['run_type']}]",
        f"STATUS:       {report['status'].upper()} (checked={report['checked']}, duration={report['duration_seconds']}s)",
        f"PLAYLISTS:    working={report['working']} / unique={report['total_unique']} "
        f"(dead={report['dead_count']}, unverified={report['unverified_count']})",
        f"COUNTRIES:    {len(countries)} country playlists updated in playlists/countries/",
        f"A&E CHANNELS: {ae_info.get('working_count', 0)} working / {ae_info.get('total_unique', 0)} unique (playlists/AE_Channels.m3u)",
        f"LOG EDITS:    +{changes.get('added_count', 0)} channels added / -{changes.get('removed_count', 0)} channels removed "
        f"(baseline: {changes.get('baseline', 'none')})",
    ]
    if changes.get("added_sample"):
        current_edit_lines.append("ADDED CHANNELS (SAMPLE):")
        for item in changes["added_sample"]:
            current_edit_lines.append(
                f"  + [{item.get('country', 'International')}] {item['name']} ({item['source']}) -> {item['url']}"
            )
    if changes.get("removed_sample"):
        current_edit_lines.append("REMOVED CHANNELS (SAMPLE):")
        for item in changes["removed_sample"]:
            current_edit_lines.append(
                f"  - [{item.get('country', 'International')}] {item['name']} ({item['source']}) -> {item['url']}"
            )
    if report["issues"]:
        current_edit_lines.append("ISSUES / ERRORS:")
        for issue in report["issues"]:
            current_edit_lines.append(f"  * {issue}")
    else:
        current_edit_lines.append("ISSUES / ERRORS: None")
    current_edit_lines.append("")
    with edits_path.open("a", encoding="utf-8") as edits_file:
        edits_file.write("\n".join(current_edit_lines) + "\n")

    # 3. playlists/logs/errors.txt (detailed error & dead/unverified link diagnostics)
    err_lines = [
        sep,
        "PREMIUMTV1 ERRORS & DIAGNOSTICS LOG (.TXT)",
        sep,
        f"Run ID:      {report['run_id']}",
        f"Timestamp:   {report['updated_local']} ({report['updated_utc']})",
        f"Label:       {report['label']} ({report['run_type']})",
        f"Outcome:     {report['status'].upper()}",
        f"Dead Links:  {report['dead_count']}  |  Unverified Links: {report['unverified_count']}",
        "",
        subsep,
        "1. RUN & SOURCE ISSUES",
        subsep,
    ]
    if report["issues"]:
        for issue in report["issues"]:
            err_lines.append(f"  * {issue}")
    else:
        err_lines.append("  None (all enabled sources and reference audits succeeded without parser/fetch errors).")

    err_lines += [
        "",
        subsep,
        "2. ERROR REASON BREAKDOWN",
        subsep,
    ]
    if report["diagnostics"]:
        err_lines.append(f"{'Reason':<38} {'Dead':>8} {'Unverified':>12}   {'Total':>8}")
        err_lines.append("-" * 74)
        for diag in report["diagnostics"]:
            err_lines.append(
                f"{diag['reason']:<38} {diag['dead']:>8} {diag['unverified']:>12}   {diag['count']:>8}"
            )
    else:
        err_lines.append("  No dead or unverified links recorded.")

    err_lines += [
        "",
        subsep,
        f"3. CONFIRMED DEAD LINKS ({len(report['dead'])})",
        subsep,
    ]
    for item in report["dead"][:500]:
        err_lines.append(
            f"  [DEAD] [{item['reason']}] [{item.get('country', 'International')}] "
            f"{item['name']} (source={item['source']}) -> {item['url']}"
        )
    if len(report["dead"]) > 500:
        err_lines.append(f"  ... and {len(report['dead']) - 500} more dead links (see report.json).")

    err_lines += [
        "",
        subsep,
        f"4. UNVERIFIED LINKS ({len(report['unverified'])})",
        subsep,
    ]
    for item in report["unverified"][:500]:
        err_lines.append(
            f"  [UNVERIFIED] [{item['reason']}] [{item.get('country', 'International')}] "
            f"{item['name']} (source={item['source']}) -> {item['url']}"
        )
    if len(report["unverified"]) > 500:
        err_lines.append(f"  ... and {len(report['unverified']) - 500} more unverified links (see report.json).")

    (logs_dir / "errors.txt").write_text("\n".join(err_lines) + "\n", encoding="utf-8")

    # 4. playlists/logs/run-history.txt (plain-text table of all historical runs)
    hist_lines = [
        sep,
        "PREMIUMTV1 RUN HISTORY LOG (.TXT)",
        sep,
        f"{'Run ID':<24} {'Local Time':<24} {'Type':<16} {'Status':<10} {'Working':>8} {'Unique':>8} {'Dead':>6} {'Unver':>6} {'+Add':>6} {'-Rem':>6}",
        "-" * 124,
    ]
    for entry in history_entries:
        hist_lines.append(
            f"{str(entry.get('run_id', '-')):<24} "
            f"{str(entry.get('updated_local', '-')):<24} "
            f"{str(entry.get('run_type', '-')):<16} "
            f"{str(entry.get('status', '-')).upper():<10} "
            f"{str(entry.get('working') if entry.get('working') is not None else '-'):>8} "
            f"{entry.get('total_unique', 0):>8} "
            f"{entry.get('dead', 0):>6} "
            f"{entry.get('unverified', 0):>6} "
            f"{entry.get('added', 0):>6} "
            f"{entry.get('removed', 0):>6}"
        )
    (logs_dir / "run-history.txt").write_text("\n".join(hist_lines) + "\n", encoding="utf-8")


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
    ap.add_argument("--approved-sources", default=None,
                    help="vetted sources from monthly discovery "
                         "(default: <out>/discovery/approved-sources.json when it exists)")
    ap.add_argument("--no-check", action="store_true", help="skip link checking")
    ap.add_argument("--workers", type=int, default=112, help="maximum concurrent link checks")
    ap.add_argument("--per-host-workers", type=int, default=8, help="maximum concurrent checks per host")
    ap.add_argument("--timeout", type=float, default=6.0, help="per-link timeout in seconds")
    ap.add_argument("--retries", type=int, default=1, help="retries for transient link-check failures")
    ap.add_argument("--min-working-ratio", type=float, default=0.03,
                    help="abort publishing if fewer than this share of links are confirmed working")
    ap.add_argument("--quarantine-days", type=float, default=7.0,
                    help="hold back links the deep check found dead for this many days "
                         "(0 disables the quarantine)")
    ap.add_argument("--label", default="manual run", help="run label shown in reports")
    ap.add_argument("--scheduled-for", default="",
                    help="ISO-8601 UTC instant this run was scheduled for; used to report "
                         "how late GitHub's scheduler started it")
    args = ap.parse_args()
    if args.workers < 1 or args.per_host_workers < 1 or args.timeout <= 0 or args.retries < 0:
        ap.error("workers, per-host-workers and timeout must be positive; retries cannot be negative")
    if args.min_working_ratio < 0:
        ap.error("min-working-ratio cannot be negative")

    out_dir = Path(args.out)
    cache_dir = out_dir / "sources"
    if args.approved_sources is None:
        args.approved_sources = str(out_dir / "discovery" / "approved-sources.json")
    started = dt.datetime.now(dt.timezone.utc)
    started_utc_iso = started.isoformat(timespec="seconds").replace("+00:00", "Z")
    run_id = f"{started.strftime('%Y%m%dT%H%M%S')}Z-{os.getpid()}"
    run_type = classify_run(args.label)
    scheduled_moment = parse_utc_iso(args.scheduled_for)
    scheduled_for_utc = ""
    schedule_delay_minutes: float | None = None
    if args.scheduled_for and scheduled_moment is None:
        log(f"[schedule] ignoring unparsable --scheduled-for value {args.scheduled_for!r}")
    elif scheduled_moment is not None:
        scheduled_for_utc = scheduled_moment.isoformat(timespec="seconds").replace("+00:00", "Z")
        schedule_delay_minutes = round((started - scheduled_moment).total_seconds() / 60.0, 1)
        _, scheduled_local = now_strings(scheduled_moment)
        log(f"[schedule] due {scheduled_for_utc} ({scheduled_local}); "
            f"started {started_utc_iso}; delay {format_delay(schedule_delay_minutes)}")

    source_stats: dict[str, dict] = {}
    reference_checks: dict[str, dict] = {}
    source_issues: list[str] = []
    all_channels: list[Channel] = []
    channels: list[Channel] = []
    working: list[Channel] = []
    all_epg: list[str] = []
    changes = {"baseline": "none", "added_count": 0, "removed_count": 0,
               "added_sample": [], "removed_sample": []}
    countries_summary: dict[str, dict] = {}
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

        source_items, promoted = load_approved_sources(args.approved_sources, source_items)
        for item in promoted:
            log(f"[discover] merged promoted source '{item['name']}' "
                f"({item.get('new_links', '?')} new links, score {item.get('score', '?')})")

        for index, src in enumerate(source_items, 1):
            if not isinstance(src, dict):
                source_issues.append(f"Source entry {index} is not an object; skipped.")
                continue
            name = str(src.get("name") or f"source-{index}")
            source_stats[name] = {
                "type": src.get("type", "m3u"),
                "url": source_display_url(src),
                "promoted_by_discovery": bool(src.get("promoted_by_discovery")),
                "discovery_note": src.get("note", "") if src.get("promoted_by_discovery") else "",
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
                local_src_path = (ROOT / str(src["local_path"])).resolve() if src.get("local_path") else None
                if local_src_path is None or local_src_path != cache.resolve():
                    write_m3u(cache, fetched_channels, epg, f"cached copy of source '{name}'",
                              advertise_self=False)
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
                synthesize_missing_ids=True,
            )
            all_playlist_written = True

            if args.no_check:
                # Keep the checked player playlist intact. Unchecked links are
                # available in PremiumTV_all.m3u instead.
                if (out_dir / "PremiumTV.m3u").exists():
                    try:
                        existing_working, existing_epg = parse_m3u(
                            (out_dir / "PremiumTV.m3u").read_text(encoding="utf-8"), "PremiumTV"
                        )
                        countries_summary = write_country_playlists(
                            out_dir, existing_working, existing_epg or all_epg, utc_s, local_s, args.label
                        )
                        write_ae_playlist(
                            out_dir, existing_working, existing_epg or all_epg, utc_s, local_s, args.label
                        )
                    except Exception as exc:  # noqa: BLE001
                        log(f"[countries] could not refresh country playlists from PremiumTV.m3u: {exc}")
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
                quarantine_path = out_dir / "checks" / QUARANTINE_FILENAME
                quarantined = apply_quarantine(channels, quarantine_path,
                                               args.quarantine_days)
                if quarantined:
                    log(f"[links] {quarantined} links held back by the deep-check "
                        f"quarantine ({quarantine_path.name})")
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
                        synthesize_missing_ids=True,
                    )
                    countries_summary = write_country_playlists(
                        out_dir, working, all_epg, utc_s, local_s, args.label
                    )
                    ae_written = write_ae_playlist(
                        out_dir, working, all_epg, utc_s, local_s, args.label
                    )
                    log(f"[playlists] separated {len(working)} working channels into "
                        f"{len(countries_summary)} country playlists and {ae_written} A&E channels")
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
    ae_summary = summarize_ae_channels(channels)
    issue_messages = list(dict.fromkeys(source_issues))
    if status_counts.get("unverified", 0):
        issue_messages.append(
            f"{status_counts['unverified']} links could not be confirmed after retries (see unverified details)."
        )
    if status_counts.get("dead", 0):
        issue_messages.append(f"{status_counts['dead']} links returned a confirmed failure (see dead details).")
    if schedule_delay_minutes is not None and schedule_delay_minutes >= LATE_START_MINUTES:
        issue_messages.append(
            f"This run started {format_delay(schedule_delay_minutes)} after its scheduled time "
            f"({scheduled_for_utc}); GitHub's scheduler delayed it. The schedule guard "
            f"(.github/workflows/schedule-guard.yml) now catches up on delayed or dropped slots."
        )
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
        "scheduled_for_utc": scheduled_for_utc or None,
        "schedule_delay_minutes": schedule_delay_minutes,
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
        "countries_count": len(countries_summary),
        "countries": countries_summary,
        "ae_channels": ae_summary,
        "promoted_sources": [name for name, stat in source_stats.items() if stat.get("promoted_by_discovery")],
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
        "scheduled_for_utc": scheduled_for_utc or None,
        "schedule_delay_minutes": schedule_delay_minutes,
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
        "countries_count": len(countries_summary),
        "ae_working": ae_summary.get("working_count", 0),
        "promoted_sources": [name for name, stat in source_stats.items() if stat.get("promoted_by_discovery")],
        "sources": {
            name: {
                key: stat.get(key)
                for key in ("status", "found", "unique", "alive", "dead", "unverified", "error",
                            "promoted_by_discovery")
                if key in stat
            }
            for name, stat in source_stats.items()
        },
        "reference_checks": {
            name: {
                key: result.get(key)
                for key in ("status", "reachable", "playlist_detected", "static_playlist_files",
                            "playlist_links", "channel_count", "ingest_status")
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
        write_txt_logs(out_dir, report, out_dir / "run-history.jsonl")
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
