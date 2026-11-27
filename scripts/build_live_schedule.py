#!/usr/bin/env python3
"""Build an honest fixture index for the apps from the published playlist.

The playlist does not contain verified start times. Fixture order and generic
competition time slots cannot establish a kickoff, so all times remain null.
The clients may support verified times in future; never guess them here.

A data-identical rebuild keeps the old `generated_utc`, so scheduled workflows
can self-heal without committing a timestamp-only change on every run. `--check`
is read-only, unlike the older help/check flags that used to rewrite the file.

Run: python3 scripts/build_live_schedule.py
     python3 scripts/build_live_schedule.py --check
"""

from __future__ import annotations

import argparse
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


def split_extinf(line: str) -> tuple[str, str] | None:
    """Split an EXTINF line at the comma outside its quoted attributes.

    Competition names may contain a comma (for example
    ``[FIBA World Cup Qualification, Europe]``), so partitioning at the first
    comma would leave the display name truncated and hide the fixture from the
    apps' schedule.
    """
    in_quotes = False
    escaped = False
    for index, character in enumerate(line):
        if character == '"' and not escaped:
            in_quotes = not in_quotes
        elif character == "," and not in_quotes:
            return line[:index], line[index + 1:]
        escaped = character == "\\" and not escaped
    return None


def parse_events(text: str):
    events = []
    for line in text.splitlines():
        if not line.startswith("#EXTINF"):
            continue
        parts = split_extinf(line)
        if parts is None:
            continue
        attrs, display = parts
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


def build_document(text: str, existing: dict | None = None) -> dict:
    """Return the schedule document, preserving a data-identical timestamp."""
    events = parse_events(text)
    games = assign_kickoffs(events)
    document = {
        "schema": 1,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": "Fixture names from the published playlist; verified kickoff times are unavailable.",
        "games": games,
    }
    # `generated_utc` changes on every run; it must not make a data-identical
    # document look stale, or --check (and CI) could never pass.
    def without_timestamp(value: dict) -> dict:
        return {key: item for key, item in value.items() if key != "generated_utc"}

    if isinstance(existing, dict) and without_timestamp(existing) == without_timestamp(document):
        document["generated_utc"] = existing.get("generated_utc", document["generated_utc"])
    return document


def render(document: dict) -> str:
    return json.dumps(document, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--source", default=str(PLAYLIST),
                        help="published M3U whose fixture names are indexed")
    parser.add_argument("--out", default=str(OUT),
                        help="schedule document to write or check")
    parser.add_argument("--check", action="store_true",
                        help="exit 1 when the published document is out of date; never write")
    args = parser.parse_args(argv)

    source = Path(args.source)
    out = Path(args.out)
    text = source.read_text(encoding="utf-8", errors="replace")
    existing = None
    if out.is_file():
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            existing = None
    document = build_document(text, existing)
    wanted = render(document)
    current = out.read_text(encoding="utf-8") if out.is_file() else None
    unchanged = current == wanted

    if args.check:
        if not unchanged:
            print(f"{out} is out of date - run scripts/build_live_schedule.py", file=sys.stderr)
            return 1
        print(f"{out} is current ({len(document['games'])} fixtures)")
        return 0

    if not unchanged:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(wanted, encoding="utf-8")

    scheduled = sum(1 for game in document["games"] if game.get("kickoff_utc"))
    print(
        f"{len(parse_events(text))} event entries, {len(document['games'])} fixtures, "
        f"{scheduled} with a verified kickoff -> {out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
