#!/usr/bin/env python3
"""Build the market directory the apps resolve a viewer's location against.

PremiumTV publishes local affiliates (WGAL, WHP, WTXF, KFW-tv ...) inside the
national lineup, but nothing in an M3U playlist says *where* a station belongs.
Answering "what is local to me?" needs three things, all offline:

  1. which market every published station serves,
  2. where each market is on a map, and
  3. a way from what the viewer gives us - a location fix, a ZIP code, a state
     name or a city name - to that market.

The reference tables live beside this script, built from public-domain /
openly licensed data (see `data/local-markets/README.md`):

    us-tv-markets.csv   callsign -> market code
    us-markets.csv      market code -> market city and state
    us-market-affiliates.csv  market code -> callsigns it also carries
    us-zip3.csv         ZIP prefix -> state + centroid
    us-places.csv       every US place name -> centroid (typed city / state)

This builder reads the checked USA playlist, recognises the stations that
carry a callsign or name a licensed community, and writes the document the
apps ship with:

    playlists/local-channels.json

Document shape (schema 2):

    countries[]     the countries we publish local stations for, with states
    markets[]       id, city, state, centroid, and the stations serving it -
                    this is the unit the apps answer with, so a location fix
                    can pick the nearest *market*, not just the nearest state
    states[]        code, name, centroid and the markets inside it
    zip_prefixes[]  ZIP prefix -> state, market id and centroid
    zip_ranges[]    the same mapping as USPS ranges, for simple players
    cities[]        every market city, so "Lancaster" is typable

Usage:
    python scripts/build_local_channels.py
    python scripts/build_local_channels.py --check
"""

from __future__ import annotations

import argparse
import copy
import csv
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# How far a ZIP's area may be from a published market and still belong to it.
# Mirrors NEAREST_MARKET_MAX_KM in macos/app/src/renderer/local-channels.js and
# LOCAL_MARKET_NEAR_KM in the Android LocalChannels.kt; a test pins all three.
NEAREST_MARKET_MAX_KM = 120.0
SOURCE = ROOT / "playlists" / "live" / "USA.m3u"
OUTPUT = ROOT / "playlists" / "local-channels.json"
DATA = ROOT / "data" / "local-markets"

# --------------------------------------------------------------------------- #
# Reference tables
# --------------------------------------------------------------------------- #
# ZIP prefix ranges as published by the USPS.  The finer per-prefix table comes
# from us-zip3.csv; the ranges stay in the document because they are what a
# simple player understands, and 256 of them are cheaper than 900 rows.
ZIP_RANGES: tuple[tuple[str, str, str], ...] = (
    ("005", "005", "NY"), ("006", "009", "PR"), ("010", "027", "MA"),
    ("028", "029", "RI"), ("030", "038", "NH"), ("039", "049", "ME"),
    ("050", "059", "VT"), ("060", "069", "CT"), ("070", "089", "NJ"),
    ("100", "149", "NY"), ("150", "196", "PA"), ("197", "199", "DE"),
    ("200", "205", "DC"), ("206", "219", "MD"), ("220", "246", "VA"),
    ("247", "268", "WV"), ("270", "289", "NC"), ("290", "299", "SC"),
    ("300", "319", "GA"), ("320", "349", "FL"), ("350", "369", "AL"),
    ("370", "385", "TN"), ("386", "397", "MS"), ("398", "399", "GA"),
    ("400", "427", "KY"), ("430", "459", "OH"), ("460", "479", "IN"),
    ("480", "499", "MI"), ("500", "528", "IA"), ("530", "549", "WI"),
    ("550", "567", "MN"), ("570", "577", "SD"), ("580", "588", "ND"),
    ("590", "599", "MT"), ("600", "629", "IL"), ("630", "658", "MO"),
    ("660", "679", "KS"), ("680", "693", "NE"), ("700", "714", "LA"),
    ("716", "729", "AR"), ("730", "749", "OK"), ("750", "799", "TX"),
    ("800", "816", "CO"), ("820", "831", "WY"), ("832", "838", "ID"),
    ("840", "847", "UT"), ("850", "865", "AZ"), ("870", "884", "NM"),
    ("889", "898", "NV"), ("900", "961", "CA"), ("967", "968", "HI"),
    ("970", "979", "OR"), ("980", "994", "WA"), ("995", "999", "AK"),
)

# Approximate state centroids: a fallback for a prefix missing from us-zip3.csv.
STATE_CENTROIDS: dict[str, tuple[float, float]] = {
    "AL": (32.8, -86.8), "AK": (64.0, -152.0), "AZ": (34.3, -111.7),
    "AR": (34.9, -92.4), "CA": (37.2, -119.3), "CO": (39.0, -105.5),
    "CT": (41.6, -72.7), "DE": (39.0, -75.5), "DC": (38.9, -77.0),
    "FL": (28.6, -82.4), "GA": (32.6, -83.4), "HI": (20.3, -156.4),
    "ID": (44.4, -114.6), "IL": (40.0, -89.2), "IN": (39.9, -86.3),
    "IA": (42.0, -93.5), "KS": (38.5, -98.4), "KY": (37.5, -85.3),
    "LA": (31.1, -92.0), "ME": (45.4, -69.2), "MD": (39.0, -76.8),
    "MA": (42.3, -71.8), "MI": (44.3, -85.4), "MN": (46.3, -94.3),
    "MS": (32.7, -89.7), "MO": (38.4, -92.5), "MT": (47.0, -109.6),
    "NE": (41.5, -99.8), "NV": (39.3, -116.6), "NH": (43.7, -71.6),
    "NJ": (40.2, -74.7), "NM": (34.4, -106.1), "NY": (42.9, -75.5),
    "NC": (35.5, -79.4), "ND": (47.4, -100.5), "OH": (40.3, -82.8),
    "OK": (35.6, -97.5), "OR": (43.9, -120.6), "PA": (40.9, -77.8),
    "RI": (41.7, -71.6), "SC": (33.9, -80.9), "SD": (44.4, -100.2),
    "TN": (35.9, -86.4), "TX": (31.5, -99.3), "UT": (39.3, -111.7),
    "VT": (44.1, -72.7), "VA": (37.5, -78.9), "WA": (47.4, -120.5),
    "WV": (38.6, -80.6), "WI": (44.6, -89.9), "WY": (43.0, -107.6),
    "PR": (18.2, -66.4), "VI": (18.3, -64.9), "GU": (13.4, 144.7),
}

STATE_NAMES: dict[str, str] = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
    "CA": "California", "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware",
    "DC": "District of Columbia", "FL": "Florida", "GA": "Georgia", "HI": "Hawaii",
    "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa", "KS": "Kansas",
    "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada",
    "NH": "New Hampshire", "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York",
    "NC": "North Carolina", "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma",
    "OR": "Oregon", "PA": "Pennsylvania", "RI": "Rhode Island",
    "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas",
    "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming",
    "PR": "Puerto Rico", "VI": "U.S. Virgin Islands", "GU": "Guam",
}

# ZIP prefixes for military posts and territories: no published station, and
# mapping them onto a state would put a viewer in the wrong market.
NON_STATE_PREFIXES = {f"09{n}" for n in range(0, 10)} | {
    "340", "962", "963", "964", "965", "966", "969",
}

COUNTRY_NAMES = {"US": "United States"}
NETWORKS = ("NBC", "CBS", "ABC", "FOX", "PBS", "CW", "MNT", "ION")

ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')
# Spellings the playlist uses that differ from the postal place names.
PLACE_ALIASES: dict[str, tuple[str, str]] = {
    "new york city": ("NY", "new york"),
    "washington": ("DC", "washington"),
    "saint paul": ("MN", "st paul"),
    "ft lauderdale": ("FL", "ft lauderdale"),
    "san louis obispo": ("CA", "san luis obispo"),
}


def attr(line: str, name: str) -> str:
    match = re.search(rf'{re.escape(name)}="([^"]*)"', line)
    return match.group(1).strip() if match else ""


def extinf_name(line: str) -> str:
    """The display name after the first comma outside quoted attributes."""
    quoted = False
    for index, char in enumerate(line):
        if char == '"':
            quoted = not quoted
        elif char == "," and not quoted:
            return line[index + 1:].strip()
    return ""


def country_of(line: str) -> str:
    country = attr(line, "tvg-country").upper()
    if len(country) == 2 and country.isalpha():
        return country
    tvg_id = attr(line, "tvg-id")
    match = re.search(r"\.([a-z]{2})(?:@|$)", tvg_id, re.IGNORECASE)
    return match.group(1).upper() if match else ""


def distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in kilometres; enough to pick a market."""
    radius = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    d_phi = phi2 - phi1
    d_lambda = math.radians(lon2 - lon1)
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(a))


# --------------------------------------------------------------------------- #
# Reference data
# --------------------------------------------------------------------------- #
def load_callsign_markets(path: Path | None = None) -> dict[str, str]:
    """callsign -> market code."""
    path = path or DATA / "us-tv-markets.csv"
    out: dict[str, str] = {}
    if not path.is_file():
        return out
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            callsign = (row.get("callsign") or "").strip().upper()
            market = (row.get("market_code") or "").strip().upper()
            if callsign and market:
                out[callsign] = market
    return out


def load_market_affiliates(path: Path | None = None) -> dict[str, tuple[str, ...]]:
    """market code -> callsigns that also serve it from a neighbouring market.

    A station's table entry names its principal licence city, but a market can
    also be served by an affiliate licensed next door: WGAL, WHP and WPMT all
    cover the Harrisburg-Lancaster-York area, so a Lancaster ZIP receives all
    three.  The table is curated (not derived from upstream) and only adds a
    station to a market that does not already list it.
    """
    path = path or DATA / "us-market-affiliates.csv"
    out: dict[str, list[str]] = {}
    if not path.is_file():
        return {}
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            market = (row.get("market_code") or "").strip().upper()
            callsign = (row.get("callsign") or "").strip().upper()
            if market and callsign and callsign not in out.setdefault(market, []):
                out[market].append(callsign)
    return {market: tuple(callsigns) for market, callsigns in out.items()}


def apply_affiliates(markets: dict[str, dict], affiliates: dict[str, tuple[str, ...]]) -> None:
    """Copy each named station into the markets that also carry it."""
    by_callsign: dict[str, dict] = {}
    for market in markets.values():
        for station in market["stations"].values():
            callsign = station["callsign"]
            if callsign and callsign not in by_callsign:
                by_callsign[callsign] = station
    for market_code, callsigns in affiliates.items():
        target = markets.get(market_code)
        if target is None:
            continue
        for callsign in callsigns:
            station = by_callsign.get(callsign)
            if station is not None:
                target["stations"].setdefault(callsign, copy.deepcopy(station))


def load_market_places(path: Path | None = None) -> dict[str, dict]:
    """market code -> its principal city, state and map position."""
    path = path or DATA / "us-markets.csv"
    out: dict[str, dict] = {}
    if not path.is_file():
        return out
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            code = (row.get("market_code") or "").strip().upper()
            city = (row.get("city") or "").strip()
            state = (row.get("state") or "").strip().upper()
            if not code or not city or state not in STATE_NAMES:
                continue
            try:
                latitude = float(row.get("latitude") or 0)
                longitude = float(row.get("longitude") or 0)
            except ValueError:
                latitude = longitude = 0.0
            if not latitude and not longitude:
                latitude, longitude = STATE_CENTROIDS[state]
            out[code] = {"city": city, "state": state,
                         "latitude": latitude, "longitude": longitude}
    return out


def load_place_coordinates(path: Path | None = None) -> dict[tuple[str, str], tuple[float, float]]:
    """(state, normalised place name) -> centroid, for typed city answers."""
    path = path or DATA / "us-places.csv"
    out: dict[tuple[str, str], tuple[float, float]] = {}
    if not path.is_file():
        return out
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            state = (row.get("state") or "").strip().upper()
            place = normalise_place(row.get("place") or "")
            if not place or state not in STATE_NAMES:
                continue
            try:
                latitude = float(row.get("latitude") or 0)
                longitude = float(row.get("longitude") or 0)
            except ValueError:
                continue
            out[(state, place)] = (latitude, longitude)
    return out


def normalise_place(name: str) -> str:
    """Typed and published spellings of one place have to collide."""
    text = name.lower().strip()
    text = text.replace("’", "'").replace(".", "").replace("-", " ")
    text = re.sub(r"\bsaint\b", "st", text)
    text = re.sub(r"\bfort\b", "ft", text)
    text = re.sub(r"\bmount\b", "mt", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()


def resolve_place(place_coordinates, city: str, state: str) -> tuple[float, float] | None:
    """Coordinates for a typed/published city name, or None when it is not a place.

    The playlist has names like "Pluto TV Cars CA" and "Orange County FL" that
    read like a city and are not one; requiring a real place is what keeps a
    channel from inventing a market.
    """
    key = normalise_place(city)
    if not key:
        return None
    point = place_coordinates.get((state, key))
    if point:
        return point
    alias = PLACE_ALIASES.get(key)
    if alias:
        return place_coordinates.get((alias[0], alias[1])) or place_coordinates.get((state, alias[1]))
    return None


# --------------------------------------------------------------------------- #
# Station recognition
# --------------------------------------------------------------------------- #
# A callsign: a K/W prefix, at least two more letters, and an optional
# (-TV | -DT1 | -CD | -LD | -LP) suffix.  Screen "KID!" and "WOX TV" are not
# callsigns a market table will know, so the table lookup rejects them.
CALLSIGN_RE = re.compile(r"\b([KW][A-Z]{2,4})(?:-(?:TV|DT\d?|CD|LD|LP|CA))?\b")
LOCATION_RE = re.compile(r"(?:[-–]\s*)?([A-Z][A-Za-z.'’ -]{2,28}?)\s*,\s*([A-Z]{2})\b")
LOCATION_NO_COMMA_RE = re.compile(r"(?:[-–]\s*)?([A-Z][A-Za-z.'’ -]{2,28}?)\s+([A-Z]{2})\b")
NOISE_PARENS = re.compile(r"\((?:Backup\s+\d+|Alt|Feed\s+\d+|\d{3,4}p|\d+k|HD|SD)\)", re.IGNORECASE)
NETWORK_PREFIX = re.compile(
    r"^(?:ABC|CBS|NBC|FOX|PBS|CW|ION|MNT|Telemundo|UniMas|Univision|News|TV|Channel|Digital)\s+",
    re.IGNORECASE,
)


def clean_city(city: str) -> str:
    city = NOISE_PARENS.sub(" ", city or "")
    previous = None
    while previous != city:
        previous = city
        city = NETWORK_PREFIX.sub("", city.strip()).strip()
    # A callsign in front of the city ("WCCA 194 Worcester") is not a place.
    city = re.sub(r"^[KW][A-Z]{2,4}(?:-(?:TV|DT\d?|CD|LD))?\s+", "", city.strip())
    city = re.sub(r"^\d+\.?\d*\s+", "", city.strip())
    return city.strip(" -–'’,.")


def station_location(name: str) -> tuple[str, str] | None:
    """``(city, state)`` when the published display name states one."""
    cleaned = NOISE_PARENS.sub(" ", name or "")
    candidates: list[tuple[str, str]] = []
    for regex in (LOCATION_RE, LOCATION_NO_COMMA_RE):
        for match in regex.finditer(cleaned):
            city = clean_city(match.group(1))
            state = match.group(2).upper()
            if state in STATE_NAMES and city:
                candidates.append((city, state))
    return candidates[-1] if candidates else None


PAREN_CALLSIGN = re.compile(r"\(([KW][A-Z]{2,4})(?:-(?:TV|DT\d?|CD|LD|LP|CA))?\)")
TVG_NAME_CALLSIGN = re.compile(r"^([KW][A-Z]{2,4})(?:-(?:TV|DT\d?|CD|LD|LP|CA))?$")


def strong_callsign(name: str, tvg_name: str, local_id: str) -> str:
    """A callsign written so plainly that it needs no market-table lookup.

    "WCCA 194 Worcester MA (WCCA-TV)" and tvg-name="WCCA-TV" are statements of
    identity; a bare token in a show title is not.
    """
    for source, regex in ((name, PAREN_CALLSIGN), (tvg_name, TVG_NAME_CALLSIGN),
                          (local_id, TVG_NAME_CALLSIGN)):
        match = regex.search(source or "")
        if match:
            return match.group(1).upper()
    return ""


def callsigns_of(*sources: str) -> list[str]:
    """Every plausible callsign the channel's own metadata offers."""
    found: list[str] = []
    for source in sources:
        for match in CALLSIGN_RE.finditer(source or ""):
            callsign = match.group(1).upper()
            # WATCH, WEST, KIDS ... are English words, not stations.  A real
            # callsign is looked up in the market table, which filters them.
            if callsign not in found:
                found.append(callsign)
    return found


def station_network(name: str) -> str:
    match = re.search(r"\(([A-Za-z+ ]+)\)", name or "")
    if match and match.group(1).strip().upper() in NETWORKS:
        return match.group(1).strip().upper()
    for network in NETWORKS:
        if re.search(rf"\b{network}\b", name or "", re.IGNORECASE):
            return "FOX" if network == "MNT" else network
    return ""


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build(source: Path = SOURCE) -> dict:
    callsign_markets = load_callsign_markets()
    market_places = load_market_places()
    place_coordinates = load_place_coordinates()
    zip_prefixes = load_zip_prefixes()

    # market code -> market record.  A station is one entry however many feeds
    # of it are published: the first URL is the stream, the rest are backups.
    markets: dict[str, dict] = {}
    pending = None
    for raw in source.read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.rstrip("\r\n")
        if line.startswith("#EXTINF"):
            pending = line
            continue
        if not line or line.startswith("#") or pending is None:
            continue
        url = line.strip()
        extinf = pending
        pending = None
        if country_of(extinf) not in ("", "US"):
            continue
        name = extinf_name(extinf)
        tvg_id = attr(extinf, "tvg-id")
        tvg_name = attr(extinf, "tvg-name")
        local_id = tvg_id.split("@")[-1] if "@" in tvg_id else ""
        candidates = callsigns_of(name, tvg_name, local_id)
        callsign = next((c for c in candidates if c in callsign_markets), "")
        if not callsign:
            callsign = strong_callsign(name, tvg_name, local_id)
        stated = station_location(name)
        if stated and stated[1] not in STATE_NAMES:
            stated = None
        if not callsign and not stated:
            continue
        market_code = callsign_markets.get(callsign, "")
        place = market_places.get(market_code)
        if place is not None:
            city, state = place["city"], place["state"]
            latitude, longitude = place["latitude"], place["longitude"]
        elif stated and resolve_place(place_coordinates, *stated) is not None:
            # No market-table entry, but the playlist itself names a real
            # community ("WCCA 194 Worcester MA"): that place is the market.
            city, state = stated
            latitude, longitude = resolve_place(place_coordinates, city, state) or STATE_CENTROIDS[state]
            market_code = "US" + re.sub(r"[^A-Z]", "", normalise_place(city).upper())[:8]
        else:
            continue
        if state not in STATE_NAMES:
            continue
        market = markets.setdefault(market_code, {
            "id": market_code,
            "city": city,
            "state": state,
            "latitude": round(latitude, 4),
            "longitude": round(longitude, 4),
            "stations": {},
        })
        station_key = callsign or normalise_place(name)[:24]
        existing = market["stations"].get(station_key)
        if existing is None:
            market["stations"][station_key] = {
                "callsign": callsign,
                "city": (
                    stated[0]
                    if stated and stated[1] == state
                    and resolve_place(place_coordinates, *stated) is not None
                    else market["city"]
                ),
                "network": station_network(name),
                "name": name,
                "channel_id": tvg_id,
                "chno": attr(extinf, "tvg-chno"),
                "logo": attr(extinf, "tvg-logo"),
                "url": url,
                "backup_urls": [],
            }
        elif url != existing["url"] and url not in existing["backup_urls"]:
            existing["backup_urls"].append(url)

    markets = merge_places(markets)
    apply_affiliates(markets, load_market_affiliates())
    return assemble(markets, zip_prefixes)


def load_zip_prefixes(path: Path | None = None) -> dict[str, dict]:
    """ZIP prefix -> state + centroid."""
    path = path or DATA / "us-zip3.csv"
    out: dict[str, dict] = {}
    if not path.is_file():
        return out
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            prefix = (row.get("prefix") or "").strip()
            state = (row.get("state") or "").strip().upper()
            if len(prefix) != 3 or not prefix.isdigit():
                continue
            if state not in STATE_NAMES or prefix in NON_STATE_PREFIXES:
                continue
            try:
                latitude = float(row.get("latitude") or 0)
                longitude = float(row.get("longitude") or 0)
            except ValueError:
                continue
            if not latitude and not longitude:
                continue
            out[prefix] = {
                "state": state,
                "latitude": round(latitude, 3),
                "longitude": round(longitude, 3),
            }
    return out


def merge_places(markets: dict[str, dict]) -> dict[str, dict]:
    """Fold a stated-only market into the real market for the same place.

    "DC.gov (Washington DC)" names a place but no callsign, so it has no market
    code; WTTG's table entry does.  Both are Washington, DC, and a viewer must
    see one market, not two.
    """
    by_place: dict[tuple[str, str], str] = {}
    for code in sorted(markets, key=lambda key: (len(markets[key]["stations"]), key)):
        market = markets[code]
        place = (market["state"], normalise_place(market["city"]))
        keeper = by_place.get(place)
        if keeper is None:
            by_place[place] = code
            continue
        target = markets[keeper]
        for key, station in market["stations"].items():
            if key not in target["stations"]:
                target["stations"][key] = station
        del markets[code]
    return markets


def assemble(markets: dict[str, dict], zip_prefixes) -> dict:
    """Turn the recognised stations into the published document."""
    out_markets = []
    for code in sorted(markets, key=lambda key: (markets[key]["state"], markets[key]["city"].lower(), key)):
        market = markets[code]
        out_markets.append({
            "id": code,
            "city": market["city"],
            "state": market["state"],
            "state_name": STATE_NAMES[market["state"]],
            "latitude": market["latitude"],
            "longitude": market["longitude"],
            "stations": sorted(market["stations"].values(),
                               key=lambda station: (station["callsign"], station["name"])),
        })

    states: dict[str, dict] = {}
    for market in out_markets:
        state = states.setdefault(market["state"], {
            "code": market["state"],
            "name": STATE_NAMES[market["state"]],
            "latitude": STATE_CENTROIDS[market["state"]][0],
            "longitude": STATE_CENTROIDS[market["state"]][1],
            "markets": [],
        })
        state["markets"].append(market["id"])

    cities = [
        {
            "city": market["city"],
            "state": market["state"],
            "state_name": market["state_name"],
            "market": market["id"],
            "stations": len(market["stations"]),
            "latitude": market["latitude"],
            "longitude": market["longitude"],
        }
        for market in out_markets
    ]
    cities.sort(key=lambda row: (row["state"], row["city"].lower()))

    # A ZIP prefix points at the state's published market nearest to it, but
    # only inside NEAREST_MARKET_MAX_KM (1.1.21). Beyond that the prefix has no
    # market: Wilkes-Barre is ~150 km from the one Pennsylvania market nearest
    # it, and "nearest in the state" would file it under Philadelphia.
    by_state: dict[str, list[dict]] = {}
    for market in out_markets:
        by_state.setdefault(market["state"], []).append(market)
    zip_rows = []
    for prefix in sorted(zip_prefixes):
        row = zip_prefixes[prefix]
        candidates = by_state.get(row["state"]) or []
        nearest = None
        best = float("inf")
        for market in candidates:
            kilometres = distance(row["latitude"], row["longitude"],
                                  market["latitude"], market["longitude"])
            if kilometres < best:
                best = kilometres
                nearest = market["id"]
        if nearest is not None and best > NEAREST_MARKET_MAX_KM:
            nearest = None
        zip_rows.append({
            "prefix": prefix,
            "state": row["state"],
            "market": nearest or "",
            "latitude": row["latitude"],
            "longitude": row["longitude"],
        })

    station_count = sum(len(market["stations"]) for market in out_markets)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema": 2,
        "generated_utc": now,
        "source": "playlists/live/USA.m3u",
        "reference": [
            "data/local-markets/us-tv-markets.csv",
            "data/local-markets/us-markets.csv",
            "data/local-markets/us-market-affiliates.csv",
            "data/local-markets/us-zip3.csv",
            "data/local-markets/us-places.csv",
        ],
        "countries": [
            {
                "code": code,
                "name": name,
                "states": sorted(states),
                "local_channels": True,
            }
            for code, name in COUNTRY_NAMES.items()
        ],
        "markets": out_markets,
        "states": [states[code] for code in sorted(states)],
        "zip_ranges": [[low, high, state] for low, high, state in ZIP_RANGES],
        "zip_prefixes": zip_rows,
        "cities": cities,
        "market_count": len(out_markets),
        "station_count": station_count,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build playlists/local-channels.json.")
    parser.add_argument("--source", default=str(SOURCE))
    parser.add_argument("--out", default=str(OUTPUT))
    parser.add_argument("--check", action="store_true",
                        help="fail when the published document is out of date")
    args = parser.parse_args(argv)

    document = build(Path(args.source))
    out = Path(args.out)

    # `generated_utc` changes on every run; it must not make a data-identical
    # document look stale, or --check (and CI) could never pass.
    def without_timestamp(value: dict) -> dict:
        return {key: item for key, item in value.items() if key != "generated_utc"}

    existing = None
    if out.is_file():
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
        except ValueError:
            existing = None
    unchanged = existing is not None and without_timestamp(existing) == without_timestamp(document)
    if unchanged:
        document["generated_utc"] = existing.get("generated_utc", document["generated_utc"])

    text = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    if args.check:
        if not unchanged:
            print(f"{out} is out of date - run scripts/build_local_channels.py", file=sys.stderr)
            return 1
        print(f"{out} is current ({document['station_count']} local stations, "
              f"{document['market_count']} markets)")
        return 0
    if not unchanged:
        out.write_text(text, encoding="utf-8")
    print(
        f"wrote {out.relative_to(ROOT)}: {document['station_count']} stations in "
        f"{document['market_count']} markets / {len(document['states'])} states"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
