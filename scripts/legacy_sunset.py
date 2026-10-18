#!/usr/bin/env python3
"""End-of-support delivery for app builds that cannot be given new code.

An installed app can only be told to update through something it already
fetches.  PremiumTV 1.0.0-1.0.4 refresh one playlist, baked into their bundles
at build time:

    playlists/countries/USA.m3u        the *legacy* USA feed

Builds from 1.0.5 on refresh a second file that this script keeps in step:

    playlists/live/USA.m3u             the *live* USA feed

Splitting the two is what makes an end-of-support date enforceable at all.
raw.githubusercontent.com serves the same bytes to every caller and cannot look
at a version, so the only way to stop feeding one set of builds is to give the
others a different address.  While support lasts the two files are identical;
on the published end-of-support date this script pins the legacy feed and the
live one carries on:

* **before** ``support_ends_utc`` - ``playlists/live/USA.m3u`` is refreshed from
  ``playlists/countries/USA.m3u`` and every build, old and new, keeps getting
  the scraped channel list.  The legacy feed also carries the sanctioned notice
  entry from the first publishing run after the warning date, because a build
  with no updater can be told about the new release no other way; the live feed
  is stripped of it, so 1.0.5+ never sees a fake channel.
* **on and after** ``support_ends_utc`` - the last scraped USA channel list is
  pinned once to ``playlists/legacy/USA.m3u``, and ``playlists/countries/USA.m3u``
  is rewritten from that pin with one sanctioned notice entry on top.  Legacy
  builds stop receiving scrape updates: they keep the channels that worked on
  the day support ended, and the first entry in their channel list tells them
  to go and get the newest release from GitHub.  The live feed is untouched, so
  1.0.5+ keeps updating.

The frozen feed keeps advertising the live ``EPG/USA.xml``.  What ends is the
channel scrape, not the listings for the channels a legacy build still has.

The notice entry is marked ``tvg-notice="app-update"`` and both apps' parsers
drop an entry carrying that marker, so it is a message and never a channel: it
cannot reach a channel list, a category, the shelf or the download site.  Only
builds too old to know the marker show it - which is exactly who it is for.

Usage (every publishing workflow runs this after the playlists are written and
before the shelf is built)::

    python scripts/legacy_sunset.py apply           # mirror, warn, freeze if due
    python scripts/legacy_sunset.py status          # what phase, how long left
    python scripts/legacy_sunset.py check           # CI guard, exit 1 on a problem
    python scripts/legacy_sunset.py apply --dry-run # report without writing
    python scripts/legacy_sunset.py apply --now 2026-12-01T00:00:00Z

Dates come from ``app-update-notice.json`` - the same document the apps' popup
reads - so the warning copy, the targeted versions and the sunset date are all
published in one place and change together.
"""
from __future__ import annotations

import argparse
import calendar
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

NOTICE_FILE = "app-update-notice.json"
LEGACY_USA = "playlists/countries/USA.m3u"
LIVE_USA = "playlists/live/USA.m3u"
PINNED_USA = "playlists/legacy/USA.m3u"

RAW_BASE = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main"

# A frozen legacy feed says so in its header, which is how every other script
# tells a pinned artifact from a playlist that is still being published.
FROZEN_MARKER = "PremiumTV legacy feed - FROZEN"

# The marker both apps' M3U parsers drop, so the notice is never a channel.
NOTICE_ATTR = "tvg-notice"
NOTICE_VALUE = "app-update"
NOTICE_ID = "premiumtv.notice.update"
NOTICE_GROUP = "PremiumTV Notice"
NOTICE_LOGO = f"{RAW_BASE}/android/art/app-icon.png"

ISO_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?"
    r"(Z|[+-]\d{2}:?\d{2})?$")


def log(msg: str) -> None:
    print(msg, flush=True)


def relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


# --------------------------------------------------------------------- dates

def parse_instant(value: str | None) -> int | None:
    """Epoch seconds for ``2026-11-16T23:59:59Z`` or ``2026-11-16``.

    Strict on purpose, and identical to both apps: an impossible calendar date
    is rejected rather than rolled forward, so a typo in the published sunset
    cannot quietly move it into another month.  A bare date means "that whole
    day", so support runs to its last second.
    """
    text = str(value or "").strip()
    if not text:
        return None
    match = ISO_RE.match(text)
    if not match:
        return None
    year, month, day, hour, minute, second, _zone = match.groups()
    month_i, day_i = int(month), int(day)
    hour_i, minute_i, second_i = int(hour or 0), int(minute or 0), int(second or 0)
    if not 1 <= month_i <= 12 or hour_i > 23 or minute_i > 59 or second_i > 59:
        return None
    if not 1 <= day_i <= calendar.monthrange(int(year), month_i)[1]:
        return None
    when = dt.datetime(int(year), month_i, day_i, hour_i, minute_i, second_i,
                       tzinfo=dt.timezone.utc)
    epoch = int(when.timestamp())
    date_only = not (hour or minute or second)
    return epoch + 86_399 if date_only else epoch


def format_day(epoch_seconds: int | None) -> str:
    """"Nov 16, 2026" in UTC - the same wording both apps put on screen."""
    if not epoch_seconds:
        return "the published date"
    when = dt.datetime.fromtimestamp(epoch_seconds, dt.timezone.utc)
    return f"{when.strftime('%b')} {when.day}, {when.year}"


def now_seconds(now: str | None = None) -> int:
    if not now:
        return int(dt.datetime.now(dt.timezone.utc).timestamp())
    parsed = parse_instant(now)
    if parsed is None:
        raise SystemExit(f"[sunset] --now is not a readable date: {now}")
    return parsed


# -------------------------------------------------------------------- notice

def read_notice(root: Path = ROOT) -> dict:
    """The published notice document, reduced to what delivery needs."""
    path = root / NOTICE_FILE
    empty = {"enabled": False, "first_warning": None, "support_ends": None,
             "grace_days": 0, "releases_url": "", "problems": [
                 f"{NOTICE_FILE} is missing or unreadable"]}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - a bad document must be reported, not raised
        empty["problems"] = [f"{NOTICE_FILE} could not be read: {exc}"]
        return empty

    problems = []
    releases_url = str(document.get("releases_url") or "").strip()
    if not releases_url.startswith("https://"):
        problems.append("the notice has no https releases_url to send people to")
    first_warning = parse_instant(document.get("first_warning_utc"))
    support_ends = parse_instant(document.get("support_ends_utc"))
    if first_warning is None:
        problems.append("first_warning_utc is missing or unreadable")
    if support_ends is None:
        problems.append("support_ends_utc is missing or unreadable")
    grace_days = int(document.get("grace_days") or 0)
    if first_warning and support_ends and grace_days:
        # Compared as calendar dates: support runs to the end of the last day.
        first_day = dt.datetime.fromtimestamp(first_warning, dt.timezone.utc).date()
        end_day = dt.datetime.fromtimestamp(support_ends, dt.timezone.utc).date()
        if (end_day - first_day).days != grace_days:
            problems.append(
                f"support_ends_utc is {(end_day - first_day).days} days after the first "
                f"warning, not the published grace period of {grace_days}")
    return {
        "enabled": document.get("enabled") is True,
        "first_warning": first_warning,
        "support_ends": support_ends,
        "grace_days": grace_days,
        "releases_url": releases_url,
        "max_version": max_version(document),
        "problems": problems,
    }


def max_version(document: dict) -> str:
    """The highest version the published rules target, for the notice wording."""
    highest = ""
    for rule in document.get("rules") or []:
        candidate = str((rule or {}).get("max_version") or "").strip()
        if candidate and (not highest or tuple(int(p) for p in candidate.split("."))
                          > tuple(int(p) for p in highest.split("."))):
            highest = candidate
    return highest


# -------------------------------------------------------------- live vs legacy

def is_frozen(path: Path) -> bool:
    """True when a playlist is the pinned legacy feed rather than a live one."""
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for index, line in enumerate(handle):
                if index > 12:
                    return False
                if FROZEN_MARKER in line:
                    return True
    except OSError:
        return False
    return False


def live_usa_path(root: Path = ROOT) -> Path:
    """The USA playlist that is still being updated.

    Every consumer that must not go stale - the app bundle, the ``categories/``
    shelf, the download site - resolves the USA list through here, so the day
    the legacy feed freezes they follow the live one without being edited.
    """
    live = root / LIVE_USA
    return live if live.is_file() else root / LEGACY_USA


def live_usa_url(root: Path = ROOT) -> str:
    """The raw URL a build should be pointed at for the live USA playlist."""
    return f"{RAW_BASE}/{relative(live_usa_path(root)).replace(os.sep, '/')}"


def is_notice_entry(attrs_line: str) -> bool:
    match = re.search(rf'{NOTICE_ATTR}="([^"]*)"', attrs_line)
    return bool(match) and match.group(1).strip().lower() == NOTICE_VALUE


def strip_notice_entries(text: str) -> str:
    """Drop every sanctioned notice entry, so a live feed never carries one."""
    kept: list[str] = []
    skipping = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#EXTINF"):
            skipping = is_notice_entry(stripped)
            if skipping:
                continue
        if skipping:
            # Everything up to and including the entry's URL line belongs to it.
            if not stripped.startswith("#"):
                skipping = False
            continue
        kept.append(line)
    return "\n".join(kept) + ("\n" if kept else "")


def count_entries(text: str) -> int:
    return sum(1 for line in text.splitlines()
               if line.strip() and not line.strip().startswith("#"))


# ------------------------------------------------------------------ publishing

def notice_lines(notice: dict, ended: bool) -> list[str]:
    """The one sanctioned entry a legacy build shows instead of new channels."""
    host = notice["releases_url"].replace("https://", "").rstrip("/")
    when = format_day(notice["support_ends"])
    oldest = notice["max_version"] or "1.0.4"
    name = (f"⚠ UPDATE PremiumTV — support for {oldest} and older ended {when} · "
            f"the newest build updates itself: {host}") if ended else \
           (f"⚠ UPDATE PremiumTV — support for {oldest} and older ends {when} · "
            f"the newest build updates itself: {host}")
    attrs = (f'#EXTINF:-1 tvg-id="{NOTICE_ID}" {NOTICE_ATTR}="{NOTICE_VALUE}" '
             f'group-title="{NOTICE_GROUP}" tvg-logo="{NOTICE_LOGO}" '
             f'tvg-country="US" tvg-name="{name}",{name}')
    return [attrs, notice["releases_url"]]


def frozen_header(text: str, notice: dict) -> list[str]:
    """The frozen feed's header: the guide it already advertised, plus the banner."""
    guide = ""
    for line in text.splitlines()[:4]:
        match = re.search(r'x-tvg-url="([^"]*)"', line)
        if line.strip().startswith("#EXTM3U") and match:
            guide = match.group(1).split(",")[0].strip()
            break
    head = ["#EXTM3U" + (f' x-tvg-url="{guide}"' if guide else "")]
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    head.append(f"# {FROZEN_MARKER} {stamp}")
    head.append(f"# Support for PremiumTV {notice['max_version'] or '1.0.4'} and older ended "
                f"{format_day(notice['support_ends'])}. This feed is pinned: it no longer "
                f"receives the GitHub channel scrape updates.")
    head.append(f"# The live USA playlist is {LIVE_USA} - what PremiumTV "
                f"{notice['max_version'] or '1.0.4'} and newer refresh from.")
    head.append(f"# Update free: {notice['releases_url']}")
    return head


def render_frozen(pinned: str, notice: dict) -> str:
    """The legacy feed after support ends: pinned channels under one notice."""
    body: list[str] = []
    past_head = False
    for line in strip_notice_entries(pinned).splitlines():
        stripped = line.strip()
        if not past_head:
            # Drop the pinned file's own header and comment lines; the banner
            # replaces them so the file cannot claim a fresh update time.
            if stripped.startswith("#EXTINF"):
                past_head = True
            else:
                continue
        body.append(line)
    lines = frozen_header(pinned, notice) + notice_lines(notice, ended=True) + body
    return "\n".join(lines) + "\n"


def inject_notice(text: str, notice: dict, ended: bool = False) -> str:
    """The live legacy feed plus exactly one sanctioned notice entry, first.

    This is how an installed build with no updater is told that a newer release
    exists.  It keeps the freshly scraped channels untouched and only prepends
    the notice, so a legacy build's library grows by one row instead of losing
    anything.  Re-running is idempotent: any earlier notice entry is stripped
    first, then a single fresh one is written in the same place.
    """
    lines = strip_notice_entries(text).splitlines()
    split_at = len(lines)
    for index, line in enumerate(lines):
        if line.startswith("#EXTINF"):
            split_at = index
            break
    head, body = lines[:split_at], lines[split_at:]
    while head and not head[-1].strip():
        head.pop()
    out = head + notice_lines(notice, ended) + body
    return "\n".join(out) + "\n"


def write_if_changed(path: Path, text: str, dry_run: bool) -> bool:
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return False
    if dry_run:
        log(f"[sunset] would write {relative(path)} ({count_entries(text)} entries)")
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    log(f"[sunset] wrote {relative(path)} ({count_entries(text)} entries)")
    return True


def apply(root: Path = ROOT, now: int | None = None, dry_run: bool = False) -> dict:
    """The publishing step: refresh the live feed, then freeze if the date has passed."""
    now = now if now is not None else now_seconds()
    notice = read_notice(root)
    legacy = root / LEGACY_USA
    live = root / LIVE_USA
    pinned = root / PINNED_USA
    # A wording-level problem in the notice document is reported but does not
    # stop the feeds being published; `check` is the guard that fails a run.
    result = {"ok": True, "problems": list(notice["problems"]), "frozen": False,
              "wrote": [], "phase": "unknown", "days_left": None}

    if not legacy.is_file() and not live.is_file():
        result.update(ok=False, problems=result["problems"] +
                      [f"neither {LEGACY_USA} nor {LIVE_USA} exists"])
        return result

    already_frozen = is_frozen(legacy)
    # When the legacy feed is frozen it is this script's own artifact, so the
    # live feed is already the freshest USA list.  Otherwise the scrape pipeline
    # has just written fresh channels to the legacy path: mirror them first,
    # before anything overwrites them.
    source = live if already_frozen else legacy
    if source.is_file():
        mirrored = strip_notice_entries(source.read_text(encoding="utf-8"))
        if write_if_changed(live, mirrored, dry_run):
            result["wrote"].append(LIVE_USA)

    due = notice["support_ends"] is not None and now >= notice["support_ends"]
    if notice["support_ends"] is not None:
        result["days_left"] = max(0, (notice["support_ends"] - now) // 86_400)
    result["phase"] = "frozen" if (due or already_frozen) else "warning"

    if already_frozen and not due:
        result["problems"].append(
            f"{LEGACY_USA} is frozen but the published support window has not closed")
        result["ok"] = False

    if due or already_frozen:
        # Pin the last scraped channel list once: this is what legacy builds
        # keep after support ends.
        if not pinned.is_file():
            donor = legacy if not already_frozen else live
            if donor.is_file():
                if write_if_changed(pinned, strip_notice_entries(
                        donor.read_text(encoding="utf-8")), dry_run):
                    result["wrote"].append(PINNED_USA)
        if pinned.is_file() or dry_run:
            basis = pinned.read_text(encoding="utf-8") if pinned.is_file() else \
                strip_notice_entries((legacy if legacy.is_file() else live)
                                     .read_text(encoding="utf-8"))
            if write_if_changed(legacy, render_frozen(basis, notice), dry_run):
                result["wrote"].append(LEGACY_USA)
        result["frozen"] = True
    elif legacy.is_file():
        # Still supported, so the legacy feed keeps the channels the scrape just
        # wrote - but it also carries the sanctioned notice entry.  This is the
        # delivery: an installed 1.0.0-1.0.4 has no notice code, so the only
        # place it can read a message is the playlist it already refreshes.
        warned = inject_notice(legacy.read_text(encoding="utf-8"), notice)
        if write_if_changed(legacy, warned, dry_run):
            result["wrote"].append(LEGACY_USA)

    return result


# ----------------------------------------------------------------------- guard

def check(root: Path = ROOT, now: int | None = None) -> list[str]:
    """Everything that must hold for the sunset to be real. Empty means healthy."""
    now = now if now is not None else now_seconds()
    notice = read_notice(root)
    problems = list(notice["problems"])
    legacy = root / LEGACY_USA
    live = root / LIVE_USA
    pinned = root / PINNED_USA

    if not legacy.is_file():
        problems.append(f"{LEGACY_USA} is missing: legacy builds would refresh a 404")
    if not live.is_file():
        problems.append(f"{LIVE_USA} is missing: run scripts/legacy_sunset.py apply")

    if live.is_file() and is_notice_entry_text(live.read_text(encoding="utf-8")):
        problems.append(f"{LIVE_USA} carries a notice entry: the live feed must stay clean")

    due = notice["support_ends"] is not None and now >= notice["support_ends"]
    frozen = is_frozen(legacy) if legacy.is_file() else False

    if due and not frozen:
        problems.append(
            f"support ended {format_day(notice['support_ends'])} but {LEGACY_USA} is still "
            f"live: run scripts/legacy_sunset.py apply")
    if frozen:
        if not pinned.is_file():
            problems.append(f"{LEGACY_USA} is frozen but the pin {PINNED_USA} is missing")
        else:
            expected = render_frozen(pinned.read_text(encoding="utf-8"), notice)
            actual = legacy.read_text(encoding="utf-8")
            if strip_notice_entries(actual) != strip_notice_entries(expected):
                problems.append(
                    f"{LEGACY_USA} no longer matches the pinned feed: a frozen legacy "
                    f"file must not be edited by hand or by a scrape run")
            if not is_notice_entry_text(actual):
                problems.append(
                    f"{LEGACY_USA} is frozen but carries no notice entry, so a legacy "
                    f"build would never learn why its channels stopped updating")
    if not due and frozen:
        problems.append(
            f"{LEGACY_USA} is frozen {format_day(notice['support_ends'])} before support ends")
    if legacy.is_file() and not frozen:
        # The warning phase has to actually warn: this entry is the only message
        # an installed 1.0.0-1.0.4 can receive, so its absence means the update
        # was never pushed to the builds that need it.
        count = count_notice_entries(legacy.read_text(encoding="utf-8"))
        if count == 0:
            problems.append(
                f"{LEGACY_USA} carries no notice entry: legacy builds would never learn "
                f"about the newer release (run scripts/legacy_sunset.py apply)")
        elif count > 1:
            problems.append(
                f"{LEGACY_USA} carries {count} notice entries; exactly one is allowed")
    return problems


def is_notice_entry_text(text: str) -> bool:
    return count_notice_entries(text) > 0


def count_notice_entries(text: str) -> int:
    return sum(1 for line in text.splitlines()
               if line.strip().startswith("#EXTINF") and is_notice_entry(line))


def status(root: Path = ROOT, now: int | None = None) -> dict:
    now = now if now is not None else now_seconds()
    notice = read_notice(root)
    legacy = root / LEGACY_USA
    live = root / LIVE_USA
    pinned = root / PINNED_USA
    frozen = is_frozen(legacy) if legacy.is_file() else False
    due = notice["support_ends"] is not None and now >= notice["support_ends"]

    def entries(path: Path) -> int:
        return count_entries(path.read_text(encoding="utf-8")) if path.is_file() else 0

    return {
        "phase": "frozen" if frozen else ("due" if due else "warning"),
        "enabled": notice["enabled"],
        "first_warning": format_day(notice["first_warning"]),
        "support_ends": format_day(notice["support_ends"]),
        "days_left": None if notice["support_ends"] is None
        else max(0, (notice["support_ends"] - now) // 86_400),
        "targeted_up_to": notice["max_version"],
        "releases_url": notice["releases_url"],
        "legacy_entries": entries(legacy),
        "live_entries": entries(live),
        "pinned_entries": entries(pinned),
        "legacy_notice": bool(legacy.is_file() and
                              is_notice_entry_text(legacy.read_text(encoding="utf-8"))),
        "problems": list(notice["problems"]),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", nargs="?", default="apply",
                        choices=("apply", "status", "check"),
                        help="apply: mirror, attach the notice, freeze if due (default). "
                             "status: report the phase. check: CI guard, exit 1 on a problem.")
    parser.add_argument("--root", default=str(ROOT), help="repository root")
    parser.add_argument("--now", default="", help="pretend it is this UTC date (testing)")
    parser.add_argument("--dry-run", action="store_true", help="report without writing")
    parser.add_argument("--json", action="store_true", help="print the status as JSON")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    now = now_seconds(args.now)

    if args.action == "apply":
        result = apply(root, now, dry_run=args.dry_run)
        for problem in result["problems"]:
            log(f"[sunset] PROBLEM: {problem}")
        log(f"[sunset] {result['phase']} phase: support ends "
            f"{format_day(read_notice(root)['support_ends'])}"
            + (f" ({result['days_left']} day(s) left)" if result["days_left"] is not None else ""))
        if not result["wrote"]:
            log("[sunset] nothing to write; the published feeds are already correct")
        return 0 if result["ok"] else 1

    if args.action == "status":
        report = status(root, now)
        if args.json:
            print(json.dumps(report, indent=2))
            return 0
        log(f"[sunset] phase              : {report['phase']}")
        log(f"[sunset] notice enabled     : {report['enabled']}")
        log(f"[sunset] first warning      : {report['first_warning']}")
        log(f"[sunset] support ends       : {report['support_ends']}"
            + (f" ({report['days_left']} day(s) left)" if report["days_left"] is not None else ""))
        log(f"[sunset] targeted up to     : {report['targeted_up_to']}")
        log(f"[sunset] legacy feed        : {LEGACY_USA} "
            f"({report['legacy_entries']} entries, notice: {report['legacy_notice']})")
        log(f"[sunset] live feed          : {LIVE_USA} ({report['live_entries']} entries)")
        log(f"[sunset] pinned snapshot    : {PINNED_USA} ({report['pinned_entries']} entries)")
        for problem in report["problems"]:
            log(f"[sunset] PROBLEM: {problem}")
        return 0

    problems = check(root, now)
    for problem in problems:
        log(f"[sunset] PROBLEM: {problem}")
    if problems:
        return 1
    log("[sunset] OK: the live and legacy USA feeds agree with the published notice")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
