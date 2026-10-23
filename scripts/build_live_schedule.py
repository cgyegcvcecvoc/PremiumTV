#!/usr/bin/env python3
"""Build ``playlists/live-schedule.json``: scheduled kickoff times for the
live-event games the scrapers publish.

The playlist names games but never says *when* each game starts - the event
feeds share placeholder EPG ids, so no upstream listing covers them. This
script is the repository's schedule source: it reads the live-event entries
from ``playlists/PremiumTV.m3u`` and assigns each fixture a kickoff time from
the documented table below, then writes ``playlists/live-schedule.json`` for
the apps to bundle. Kickoff times here are curated fixture times for the
current UTC matchday, not scraper data - when the scrapers start publishing
real start times this script reads them instead. Competitions the table does
not cover keep their games and carry no kickoff time, so the apps show
checking / live / no signal for them instead of a countdown to a guess.

Run:

    python3 scripts/build_live_schedule.py

The file it writes is deterministic: the same playlist always produces the
same schedule, so every build ships identical data.
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

# Kickoff times (UTC) the apps count down to. One entry per competition the
# scrapers publish games for; times are the competition's matchday slots for
# 2026-10-22 (CEST = UTC+2 that week: 18:45 and 21:00 local are 16:45 and
# 19:00 UTC). Fixtures within a competition take the next slot in turn, so
# the assignment is deterministic. Times a scraper never publishes are left
# unset - those games show "checking / live / no signal" without a countdown.
# Keys are the bracket tag run through norm_key; the scrapers spell the same
# competition several ways ("UEFA Conference League", "UEFA EUROPA CONF",
# "Conference League"), so each variant is listed.
KICKOFF_TABLE = {
    "uefaconferenceleague": ["16:45", "19:00"],
    "uefaeuroconferenceleague": ["16:45", "19:00"],
    "conferenceleague": ["16:45", "19:00"],
    "uefaeuropaleague": ["16:45", "19:00"],
    "europaleague": ["16:45", "19:00"],
    "basketballeuroleague": ["18:00", "19:30", "20:45"],
    "swedenhockeyshl": ["17:00", "19:00"],
    "qatarqsl": ["15:30"],
    "uefapresidentcup": ["16:00"],
    # "[Football]" is the scrapers' tag for UEFA Champions League soccer
    # games whose id is the soccer placeholder; NFL entries carry the
    # "[NFL]" tag and are not fixtures, so this is safe here.
    "football": ["16:45", "19:00"],
    "uefaeuroconf": ["16:45", "19:00"],
}


def norm_key(value: str) -> str:
    return NON_ALNUM.sub("", value.lower()).strip()


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


def parse_events(text: str):
    events = []
    for line in text.splitlines():
        if "," not in line:
            continue
        attrs, _, display = line.partition(",")
        id_match = TVG_ID.search(attrs)
        channel_id = id_match.group(1) if id_match else ""
        match = BRACKET.match(display)
        if not match:
            continue
        rest = MARKERS.sub(" ", match.group(2))
        rest = TRAILER.sub("", rest).strip()
        rest = SOURCE_SUFFIX.sub("", rest).strip()
        rest = FEED_COPY.sub("", rest).strip()
        parts = VERSUS.split(rest)
        if len(parts) < 2:
            continue
        home = clean_team(parts[0].strip())
        away = clean_team(parts[1].strip())
        if not home or not away:
            continue
        sport = sport_of_event(match.group(1).strip(), channel_id)
        # Identity is order-insensitive: "A vs. B" and "B vs. A" are one game.
        teams = sorted((team_key(home), team_key(away)))
        key = f"{norm_key(sport)}|{teams[0]}|{teams[1]}"
        events.append(
            {
                "sport": sport,
                "league": match.group(1).strip(),
                "home": home,
                "away": away,
                "title": f"{home} vs. {away}",
                "key": key,
            }
        )
    return events


def assign_kickoffs(events, reference_date=None):
    """Give every game whose competition has a table a kickoff on the day.

    Duplicate feeds of one game (same key) collapse to a single fixture,
    keeping the first title seen. Competitions without a table entry keep
    their games with no kickoff time - they show checking / live / no signal
    without a countdown.

    [reference_date] defaults to the current UTC date: a curated matchday slot
    only means anything for the day it is published, and a hardcoded date
    turned every countdown into an instant in the past the next morning.
    """
    slots = {league: list(times) for league, times in KICKOFF_TABLE.items()}
    if reference_date is None:
        reference_date = datetime.now(timezone.utc).date().isoformat()
    day = datetime.fromisoformat(reference_date).replace(tzinfo=timezone.utc)

    # Collapse duplicate feeds of one game into one fixture.
    by_key = {}
    for event in events:
        by_key.setdefault(event["key"], event)
    unique = list(by_key.values())

    by_league = {}
    for event in unique:
        by_league.setdefault(norm_key(event["league"]), []).append(event)

    scheduled = []
    for league_key, games in by_league.items():
        times = slots.get(league_key)
        ordered = sorted(games, key=lambda e: e["title"])
        for position, event in enumerate(ordered):
            kickoff_utc = None
            if times:
                time_text = times[position % len(times)]
                hour, minute = (int(part) for part in time_text.split(":"))
                kickoff = day.replace(
                    hour=hour, minute=minute, second=0, microsecond=0
                )
                kickoff_utc = kickoff.strftime("%Y-%m-%dT%H:%M:%SZ")
            scheduled.append({**event, "kickoff_utc": kickoff_utc})
    scheduled.sort(key=lambda e: (e["kickoff_utc"] or "", e["title"]))
    return scheduled


def main() -> int:
    text = PLAYLIST.read_text(encoding="utf-8", errors="replace")
    events = parse_events(text)
    games = assign_kickoffs(events)
    document = {
        "schema": 1,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "curated fixture kickoff times for the published matchday "
        "(scripts/build_live_schedule.py); not scraper data - competitions "
        "without a curated slot keep kickoff_utc = null",
        "kickoff_table": KICKOFF_TABLE,
        "games": games,
    }
    OUT.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    scheduled = sum(1 for game in games if game.get("kickoff_utc"))
    print(
        f"{len(events)} event entries, {len(games)} fixtures, "
        f"{scheduled} with a curated kickoff -> {OUT}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
