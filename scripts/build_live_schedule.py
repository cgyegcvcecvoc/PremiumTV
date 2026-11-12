#!/usr/bin/env python3
"""Build an honest fixture index for the apps from the published playlist.

The playlist does not contain verified start times. Fixture order and generic
competition time slots cannot establish a kickoff, so all times remain null.
The clients may support verified times in future; never guess them here.
Run: python3 scripts/build_live_schedule.py
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLAYLIST = REPO_ROOT / "playlists" / "PremiumTV.m3u"
OUT = REPO_ROOT / "playlists" / "live-schedule.json"

VERSUS = re.compile(r"\s+vs\.?\s+", re.IGNORECASE)
TRAILER = re.compile(r"\s*\|.*$")
# Source/backup markers the scrapers append to team names, removed anywhere
# they appear (not just at the end): "Torreense (DAMITV) (Backup 1)" and
# "Ferencváros vs Torreense" are one fixture.
MARKERS = re.compile(r"\s*\((?:STRMCNTR|[A-Z0-9]{3,14}|BACKUP|iSTRMEAST|FAWA)\)")
SOURCE_SUFFIX = re.compile(r"\s*\((?:STRMCNTR|[A-Z0-9]{3,14})\)\s*$")
FEED_COPY = re.compile(r"\s+\d{1,2}$")
BRACKET = re.compile(r"^\[([^\]]{2,48})\]\s*(.*)$")
TVG_ID = re.compile(r'tvg-id="([^"]*)"')
NON_ALNUM = re.compile(r"[^a-z0-9]+")

# Team-name variants the scrapers use for the same club, normalized through
# norm_key. Applied before keying so "FC Lugano" vs "Lugano" or
# "Crvena Zvezda vs F.C. København" vs "F.C. København vs Red Star Belgrade"
# merge into a single game card instead of two.
TEAM_ALIASES = {
    "fckbenhavn": "fccopenhagen",
    "fclugano": "lugano",
    "hapoelbeer": "hapoelbeersheva",
    "mjallbyaif": "mjallby",
    "royaleunionsg": "unionstgilloise",
    "univcraiova": "csucraiova",
    "interdescaldes": "interescaldes",
    "staderennais": "rennes",
    "fcnordsjaelland": "nordsjaelland",
    "skbrann": "brann",
    "rigafc": "riga",
    "mjallby": "mjallby",
}


def norm_key(value: str) -> str:
    return NON_ALNUM.sub("", value.lower()).strip()


def team_key(name: str) -> str:
    """Norm key for one team, alias-collapsed so spelling variants match."""
    key = norm_key(name)
    return TEAM_ALIASES.get(key, key)

def clean_team(name: str) -> str:
    """A team name with the feed-copy suffix stripped.

    The same game is often published two or three times ("... vs. … 1",
    "... vs. … 2", "... vs. … 3"); the trailing number names the feed, not a
    different team. Strip it so duplicate feeds of one game merge into one
    card with every stream as a backup.
    """
    return FEED_COPY.sub("", name).strip()


def sport_of_event(sport_tag: str, channel_id: str) -> str:
    """The same sport resolution the apps use (LiveEvents.kt / live-events.js).

    The shared placeholder id (…Dummy.us) is the strongest hint; the bracket
    tag decides everywhere else.
    """
    sport_labels = {
        "soccer": "Soccer",
        "football": "American Football",
        "americanfootball": "American Football",
        "nfl": "American Football",
        "ncaaf": "College Football",
        "collegefootball": "College Football",
        "nhl": "NHL Hockey",
        "nhlhockey": "NHL Hockey",
        "hockey": "Hockey",
        "basketball": "Basketball",
        "nba": "NBA Basketball",
        "ncaabasketball": "College Basketball",
        "mlb": "MLB Baseball",
        "baseball": "Baseball",
        "ufc": "UFC / MMA",
        "mma": "UFC / MMA",
        "boxing": "Boxing",
        "wrestling": "Wrestling",
        "golf": "Golf",
        "tennis": "Tennis",
        "f1": "Formula 1",
        "nascar": "NASCAR",
        "cricket": "Cricket",
        "rugby": "Rugby",
        "sports": "Sports",
    }
    soccer_leagues = {
        "ligamx", "laliga", "premierleague", "epl", "mls", "bundesliga",
        "seriea", "ligue1", "ligaprofesional", "liga1", "championsleague",
        "europaleague", "copa", "eredivisie", "primeiraliga",
        "saudiproleague", "worldcup", "euros",
    }
    from_id = None
    channel_id_lower = (channel_id or "").lower()
    if ".dummy." in channel_id_lower:
        prefix = norm_key(channel_id_lower.split(".dummy.")[0].split(".")[0])
        from_id = {
            "soccer": "Soccer",
            "football": "American Football",
            "nhlhockey": "NHL Hockey",
            "ncaasports": "College Football",
            "ncaa": "College Football",
        }.get(prefix)
    tag_key = norm_key(sport_tag)
    from_tag = sport_labels.get(tag_key)
    if not from_tag and tag_key in soccer_leagues:
        from_tag = "Soccer"
    if from_id:
        return from_id
    return from_tag or sport_tag


def parse_event(display: str, channel_id: str = "") -> dict | None:
    """Parse one published channel name into a stable matchup identity."""
    match = BRACKET.match(display or "")
    if not match:
        return None
    rest = MARKERS.sub(" ", match.group(2))
    rest = TRAILER.sub("", rest).strip()
    rest = SOURCE_SUFFIX.sub("", rest).strip()
    rest = FEED_COPY.sub("", rest).strip()
    parts = VERSUS.split(rest)
    if len(parts) < 2:
        return None
    home = clean_team(parts[0].strip())
    away = clean_team(parts[1].strip())
    if not home or not away:
        return None
    sport = sport_of_event(match.group(1).strip(), channel_id)
    # Identity is order-insensitive: "A vs. B" and "B vs. A" are one game.
    teams = sorted((team_key(home), team_key(away)))
    return {
        "sport": sport,
        "league": match.group(1).strip(),
        "home": home,
        "away": away,
        "title": f"{home} vs. {away}",
        "key": f"{norm_key(sport)}|{teams[0]}|{teams[1]}",
    }


def parse_events(text: str):
    events = []
    for line in text.splitlines():
        if "," not in line:
            continue
        attrs, _, display = line.partition(",")
        id_match = TVG_ID.search(attrs)
        event = parse_event(display, id_match.group(1) if id_match else "")
        if event is not None:
            events.append(event)
    return events


def assign_kickoffs(events):
    """Collapse duplicate fixture entries without inventing kickoff times."""
    by_key = {}
    for event in events:
        by_key.setdefault(event["key"], event)
    return sorted(
        ({**event, "kickoff_utc": None} for event in by_key.values()),
        key=lambda event: event["title"],
    )


def main() -> int:
    text = PLAYLIST.read_text(encoding="utf-8", errors="replace")
    events = parse_events(text)
    games = assign_kickoffs(events)
    document = {
        "schema": 1,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Fixture names from the published playlist; verified kickoff times are unavailable.",
        "games": games,
    }
    OUT.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    scheduled = sum(1 for game in games if game.get("kickoff_utc"))
    print(
        f"{len(events)} event entries, {len(games)} fixtures, "
        f"{scheduled} with a verified kickoff -> {OUT}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
