#!/usr/bin/env python3
"""Build the local-channel directory the apps ask a viewer's location against.

PremiumTV publishes a handful of local affiliates alongside the national
lineup, but nothing in an M3U file says *where* a station belongs.  This script
reads the checked USA playlist, recognises the stations whose names carry a
callsign and a city/state (``WGAL 8 (NBC) - Lancaster PA``), and writes one
small document the Android and macOS apps ship with:

    playlists/local-channels.json

The document also carries what the apps need to turn an answer into a filter:
US ZIP prefix ranges to a state, state names and centroids (so a location fix
can pick the nearest state we have stations for), and the country list.  The
apps never guess a market from a channel name themselves - they match the
document's callsigns/EPG ids against the loaded library.

Nothing here touches the network.  Like the rest of the app bundle data it is
regenerated from the repository's own published playlist.

Usage:
    python scripts/build_local_channels.py
    python scripts/build_local_channels.py --check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "playlists" / "live" / "USA.m3u"
OUTPUT = ROOT / "playlists" / "local-channels.json"

# --------------------------------------------------------------------------- #
# Reference tables
# --------------------------------------------------------------------------- #
# The first three digits of a US ZIP code, as published by the USPS.  A range
# covers every ZIP that starts with a number inside it.
ZIP_RANGES: tuple[tuple[str, str, str], ...] = (
    ("005", "005", "NY"),
    ("006", "009", "PR"),
    ("010", "027", "MA"),
    ("028", "029", "RI"),
    ("030", "038", "NH"),
    ("039", "049", "ME"),
    ("050", "059", "VT"),
    ("060", "069", "CT"),
    ("070", "089", "NJ"),
    ("090", "099", "AE"),
    ("100", "149", "NY"),
    ("150", "196", "PA"),
    ("197", "199", "DE"),
    ("200", "205", "DC"),
    ("206", "219", "MD"),
    ("220", "246", "VA"),
    ("247", "268", "WV"),
    ("270", "289", "NC"),
    ("290", "299", "SC"),
    ("300", "319", "GA"),
    ("320", "349", "FL"),
    ("350", "369", "AL"),
    ("370", "385", "TN"),
    ("386", "397", "MS"),
    ("398", "399", "GA"),
    ("400", "427", "KY"),
    ("430", "459", "OH"),
    ("460", "479", "IN"),
    ("480", "499", "MI"),
    ("500", "528", "IA"),
    ("530", "549", "WI"),
    ("550", "567", "MN"),
    ("570", "577", "SD"),
    ("580", "588", "ND"),
    ("590", "599", "MT"),
    ("600", "629", "IL"),
    ("630", "658", "MO"),
    ("660", "679", "KS"),
    ("680", "693", "NE"),
    ("700", "714", "LA"),
    ("716", "729", "AR"),
    ("730", "749", "OK"),
    ("750", "799", "TX"),
    ("800", "816", "CO"),
    ("820", "831", "WY"),
    ("832", "838", "ID"),
    ("840", "847", "UT"),
    ("850", "865", "AZ"),
    ("870", "884", "NM"),
    ("889", "898", "NV"),
    ("900", "961", "CA"),
    ("967", "968", "HI"),
    ("970", "979", "OR"),
    ("980", "994", "WA"),
    ("995", "999", "AK"),
)

# Approximate state centroids.  A coarse location fix (city-level permission or
# a browser's IP-based estimate) only has to pick the nearest state that has a
# published station; the viewer can always type a ZIP instead.
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
}

COUNTRY_NAMES = {"US": "United States"}
NETWORKS = ("NBC", "CBS", "ABC", "FOX", "PBS", "CW", "MNT", "ION", "MNT")

ATTR_RE = re.compile(r'([\w-]+)="([^"]*)"')


def attr(line: str, name: str) -> str:
    match = re.search(rf'{re.escape(name)}="([^"]*)"', line)
    return match.group(1).strip() if match else ""


def extinf_name(line: str) -> str:
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


CALLSIGN_RE = re.compile(r"\(\s*([KW][A-Z]{2,4}(?:-TV|-DT\d?)?)\s*\)")
LOCATION_RE = re.compile(
    r"(?:[-–]\s*)?([A-Z][A-Za-z.'’ -]{2,28}?)\s*,\s*([A-Z]{2})\b"
)
LOCATION_NO_COMMA_RE = re.compile(
    r"(?:[-–]\s*)?([A-Z][A-Za-z.'’ -]{2,28}?)\s+([A-Z]{2})\b"
)


def station_location(name: str) -> tuple[str, str] | None:
    """Return ``(city, state)`` when the published name says where it is."""
    cleaned = re.sub(r"\((?:Backup\s+\d+|\d{3,4}p|\d+k|HD|SD)\)", " ", name, flags=re.I)
    candidates: list[tuple[str, str]] = []
    for regex in (LOCATION_RE, LOCATION_NO_COMMA_RE):
        for match in regex.finditer(cleaned):
            city = match.group(1).strip(" -–'’")
            state = match.group(2).upper()
            if state in STATE_NAMES and city:
                candidates.append((city, state))
    if not candidates:
        return None
    # The last city/state mention is the licensed community in every station
    # name the playlist publishes ("CBS 3 Omaha NE (KMTV-TV)").
    city, state = candidates[-1]
    # "PBS KET Louisville" / "ABC Bakersfield" / "PBS MPT Baltimore" carry the
    # network (and often the station's callsign) before the community; strip it
    # so a market reads as a place, not as a channel name.
    city = re.sub(
        r"^(?:ABC|CBS|NBC|FOX|PBS|CW|ION)\s+(?:[A-Z]{2,4}\s+)?", "", city
    ).strip(" -–'’")
    return city, state


def station_network(name: str) -> str:
    match = re.search(r"\(([A-Z]+)\)", name)
    if match and match.group(1) in NETWORKS:
        return match.group(1)
    for network in NETWORKS:
        if re.search(rf"\b{network}\b", name, re.IGNORECASE):
            return "FOX" if network == "MNT" else network
    return ""


def station_callsign(name: str, tvg_name: str) -> str:
    match = CALLSIGN_RE.search(name)
    if match:
        return match.group(1)
    if re.fullmatch(r"[KW][A-Z]{2,4}(?:-TV|-DT\d?)?", tvg_name or ""):
        return tvg_name
    return ""


def build(source: Path = SOURCE) -> dict:
    stations_by_state: dict[str, dict[str, list[dict]]] = {}
    pending = None
    with source.open("r", encoding="utf-8", errors="replace") as handle:
        for raw in handle:
            line = raw.rstrip("\r\n")
            if line.startswith("#EXTINF"):
                pending = line
                continue
            if not line or line.startswith("#") or pending is None:
                continue
            url = line.strip()
            name = extinf_name(pending)
            if country_of(pending) != "US":
                pending = None
                continue
            location = station_location(name)
            callsign = station_callsign(name, attr(pending, "tvg-name"))
            if not location or not callsign:
                pending = None
                continue
            city, state = location
            markets = stations_by_state.setdefault(state, {})
            stations = markets.setdefault(city, [])
            stations.append({
                "callsign": callsign,
                "network": station_network(name),
                "name": name,
                "channel_id": attr(pending, "tvg-id"),
                "chno": attr(pending, "tvg-chno"),
                "logo": attr(pending, "tvg-logo"),
                "url": url,
            })
            pending = None

    states = []
    for state in sorted(stations_by_state):
        markets = stations_by_state[state]
        markets_out = []
        for city in sorted(markets):
            # One row per callsign, keeping the first published feed and
            # folding later feeds of the same station in as backups.
            by_callsign: dict[str, dict] = {}
            for station in markets[city]:
                existing = by_callsign.get(station["callsign"])
                if existing is None:
                    by_callsign[station["callsign"]] = dict(station, backup_urls=[])
                else:
                    existing["backup_urls"].append(station["url"])
            markets_out.append({
                "city": city,
                "stations": [by_callsign[key] for key in sorted(by_callsign)],
            })
        latitude, longitude = STATE_CENTROIDS.get(state, (0.0, 0.0))
        states.append({
            "code": state,
            "name": STATE_NAMES.get(state, state),
            "latitude": latitude,
            "longitude": longitude,
            "markets": markets_out,
        })

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "schema": 1,
        "generated_utc": now,
        "source": "playlists/live/USA.m3u",
        "countries": [
            {"code": code, "name": name, "states": [s["code"] for s in states]}
            for code, name in COUNTRY_NAMES.items()
        ],
        "zip_ranges": [[low, high, state] for low, high, state in ZIP_RANGES],
        "states": states,
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
    station_count = sum(
        len(market["stations"]) for state in document["states"] for market in state["markets"]
    )

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
        print(f"{out} is current ({station_count} local stations)")
        return 0
    if not unchanged:
        out.write_text(text, encoding="utf-8")
    print(
        f"wrote {out.relative_to(ROOT)}: {station_count} stations in "
        f"{len(document['states'])} states"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
