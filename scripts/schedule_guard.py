#!/usr/bin/env python3
"""Catch-up guard for the scheduled playlist scrape.

GitHub's scheduler does not guarantee that a `schedule:` cron fires on time. On
this repository every scheduled run between 2026-09-27 and 2026-09-29 started
between 2.8 and 8.1 hours after its intended time, and three of nine slots never
produced a run at all. The cron expressions and their `timezone:` keys were
correct; GitHub simply queued or dropped them under load.

This script makes the schedule self-healing. It is started often (every 20
minutes) by `.github/workflows/schedule-guard.yml` and asks one question:

    "Is any slot from today's schedule still uncovered, and is it late enough
     that we should start it ourselves?"

If yes, it fires the existing `scrape-now` repository_dispatch that
`.github/workflows/scrape.yml` already listens for, labelled with the slot that
was missed. The scrape itself, the link check and the commit to `main` stay
exactly where they were, so there is only ever one code path that publishes
playlists.

The schedule is read from the workflow file rather than duplicated here, so the
guard can never drift away from the crons GitHub actually fires.

Sub-commands (note: the shared options come *before* the sub-command):

    python scripts/schedule_guard.py [--summary-file F] [--dry-run] check
    python scripts/schedule_guard.py report
    python scripts/schedule_guard.py label-for --cron "7 3 * * *"
    python scripts/schedule_guard.py scheduled-for --cron "7 3 * * *"

`check` reports coverage and dispatches a catch-up scrape when one is due.
`report` prints the coverage table only and never dispatches. `label-for` prints
the human label for a cron expression and `scheduled-for` the UTC instant that
cron most recently fired; scrape.yml uses both so the workflow and the guard can
never disagree about what a slot is called or when it was due.

Only the Python standard library is used (3.9+).
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:  # pragma: no cover - zoneinfo is present on 3.9+
    ZoneInfo = None  # type: ignore[assignment]

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scraper  # noqa: E402  (reused so run types can never drift apart)

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_WORKFLOW = ROOT / ".github" / "workflows" / "scrape.yml"
DEFAULT_HISTORY = ROOT / "playlists" / "run-history.jsonl"
DEFAULT_TZ = "America/New_York"

# A slot is only "overdue" once it is this far past its intended start. Without
# the grace period the guard would race the real cron, which is usually a few
# minutes late all by itself.
# The guard runs every ten minutes; a six-minute grace period leaves room for
# GitHub's normal schedule jitter while catching dropped slots promptly.
GRACE_MINUTES = 6
# A full scrape needs ~20 minutes. Dispatching again while one is running, or
# straight after one finished, would only duplicate work.
COOLDOWN_MINUTES = 25
# A successful *checked* run this close to a slot counts as covering it, whatever
# its run type. Without this, a manual re-scrape at 4:37 PM would be followed 4
# minutes later by a catch-up scrape for the 4:41 PM slot - the same playlist,
# verified twice, for no benefit.
FRESHNESS_MINUTES = 45
# Run outcomes that count as covering a slot. "failed" covered nothing, and an
# "unchecked" merge never publishes PremiumTV.m3u, so it cannot satisfy a slot
# whose whole purpose is a verified link check.
COVERING_STATUSES = {"success", "warning"}
# How far back the guard looks for slots that are still uncovered.
LOOKBACK_DAYS = 1

SLOT_LABELS = {
    "7 3 * * *": "3:07 AM daily scrape",
    "23 6 * * *": "6:23 AM recheck",
    "41 16 * * *": "4:41 PM final check",
    # discover.yml asks for its label here too, so a monthly run is still
    # classified as monthly_discovery rather than falling back to a guess.
    "37 4 1 * *": "monthly new-channel discovery",
}


def log(msg: str) -> None:
    print(msg, flush=True)


# --------------------------------------------------------------------------- #
# Cron parsing
# --------------------------------------------------------------------------- #
FIELD_RANGES = ((0, 59), (0, 23), (1, 31), (1, 12), (0, 6))
FIELD_NAMES = ("minute", "hour", "day-of-month", "month", "day-of-week")
MONTH_NAMES = {name: i for i, name in enumerate(
    ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"), 1)}
DOW_NAMES = {name: i for i, name in enumerate(("sun", "mon", "tue", "wed", "thu", "fri", "sat"))}


@dataclass(frozen=True)
class CronSpec:
    """A parsed five-field POSIX cron expression."""
    expression: str
    minutes: frozenset
    hours: frozenset
    days: frozenset
    months: frozenset
    weekdays: frozenset
    day_restricted: bool
    weekday_restricted: bool

    def matches(self, when: dt.datetime) -> bool:
        if when.minute not in self.minutes or when.hour not in self.hours:
            return False
        if when.month not in self.months:
            return False
        # POSIX cron: when both day fields are restricted either may match.
        day_ok = when.day in self.days
        weekday_ok = ((when.weekday() + 1) % 7) in self.weekdays
        if self.day_restricted and self.weekday_restricted:
            return day_ok or weekday_ok
        if self.day_restricted:
            return day_ok
        if self.weekday_restricted:
            return weekday_ok
        return True


def _parse_field(text: str, index: int) -> tuple[frozenset, bool]:
    low, high = FIELD_RANGES[index]
    names = MONTH_NAMES if index == 3 else (DOW_NAMES if index == 4 else {})
    values: set[int] = set()
    restricted = False
    for part in text.split(","):
        part = part.strip()
        if not part:
            raise ValueError(f"empty term in cron field '{text}'")
        step = 1
        if "/" in part:
            part, _, step_text = part.partition("/")
            step = int(step_text)
            if step < 1:
                raise ValueError(f"cron step must be >= 1 in '{text}'")
            restricted = True
        if part in ("*", "?"):
            start, end = low, high
            if part == "*":
                restricted = False if "/" not in text else restricted
        else:
            def resolve(token: str) -> int:
                key = token.strip().lower()
                if key in names:
                    return names[key]
                value = int(key)
                if not low <= value <= high:
                    raise ValueError(f"{FIELD_NAMES[index]} value {value} out of range {low}-{high}")
                return value

            if "-" in part:
                a, _, b = part.partition("-")
                start, end = resolve(a), resolve(b)
            else:
                start = end = resolve(part)
            restricted = True
        if start > end:
            raise ValueError(f"reversed range {start}-{end} in cron field '{text}'")
        values.update(range(start, end + 1, step))
    if not values:
        raise ValueError(f"cron field '{text}' matched no values")
    return frozenset(values), restricted


def parse_cron(expression: str) -> CronSpec:
    fields = expression.split()
    if len(fields) != 5:
        raise ValueError(f"cron expression must have 5 fields, got {len(fields)}: {expression!r}")
    parsed = [_parse_field(field, i) for i, field in enumerate(fields)]
    return CronSpec(
        expression=" ".join(fields),
        minutes=parsed[0][0], hours=parsed[1][0], days=parsed[2][0],
        months=parsed[3][0], weekdays=parsed[4][0],
        day_restricted=parsed[2][1], weekday_restricted=parsed[4][1],
    )


def _timezone(name: str) -> dt.tzinfo:
    if ZoneInfo is None:  # pragma: no cover
        return dt.timezone.utc
    try:
        return ZoneInfo(name)
    except Exception:  # noqa: BLE001
        log(f"[guard] unknown timezone {name!r}; falling back to UTC")
        return dt.timezone.utc


def _walk(now: dt.datetime, spec: CronSpec, tz: dt.tzinfo, step: int, limit: int) -> dt.datetime | None:
    """Step minute by minute in local time until the cron matches."""
    local = now.astimezone(tz).replace(second=0, microsecond=0)
    for _ in range(limit):
        local += dt.timedelta(minutes=step)
        if not spec.matches(local):
            continue
        moment = local.astimezone(dt.timezone.utc)
        # A wall clock inside a DST spring-forward gap does not exist: converting
        # it back yields a different local time. Skip it rather than report an
        # instant the cron never described. (GitHub advances such a schedule to
        # the next valid local time; the crons here stay clear of that window.)
        if moment.astimezone(tz).replace(second=0, microsecond=0) != local:
            continue
        return moment
    return None


def previous_occurrence(now: dt.datetime, spec: CronSpec, tz_name: str = DEFAULT_TZ) -> dt.datetime | None:
    """The most recent instant at or before `now` when the cron fired."""
    tz = _timezone(tz_name)
    local = now.astimezone(tz).replace(second=0, microsecond=0)
    if spec.matches(local):
        return local.astimezone(dt.timezone.utc)
    # 70 days back is enough for a monthly cron and keeps an impossible
    # expression (30 February) from walking the whole calendar.
    return _walk(local, spec, tz, -1, 60 * 24 * 70)


def next_occurrence(now: dt.datetime, spec: CronSpec, tz_name: str = DEFAULT_TZ) -> dt.datetime | None:
    tz = _timezone(tz_name)
    return _walk(now.astimezone(tz), spec, tz, 1, 60 * 24 * 400)


# --------------------------------------------------------------------------- #
# Reading the schedule out of the workflow file
# --------------------------------------------------------------------------- #
CRON_LINE = re.compile(r"^\s*-\s*cron:\s*[\"']?([^\"'#]+?)[\"']?\s*(?:#.*)?$")
TZ_LINE = re.compile(r"^\s*timezone:\s*[\"']?([^\"'#]+?)[\"']?\s*(?:#.*)?$")


@dataclass
class Slot:
    cron: str
    timezone: str
    label: str
    run_type: str
    start_utc: dt.datetime | None = None
    covered_by: str = ""
    delay_minutes: float | None = None
    state: str = "pending"

    @property
    def spec(self) -> CronSpec:
        return parse_cron(self.cron)


def label_for_cron(cron: str) -> str:
    """Human label for a cron expression, looked up then generated as a fallback."""
    normalised = " ".join(cron.split())
    if normalised in SLOT_LABELS:
        return SLOT_LABELS[normalised]
    try:
        spec = parse_cron(normalised)
        if len(spec.minutes) == 1 and len(spec.hours) == 1:
            local = dt.datetime(2026, 1, 1, next(iter(spec.hours)), next(iter(spec.minutes)))
            clock = local.strftime("%I:%M %p").lstrip("0")
            return f"{clock} scheduled scrape"
    except ValueError:
        pass
    return "scheduled scrape"


def load_schedule(workflow_path: Path = DEFAULT_WORKFLOW, tz_default: str = DEFAULT_TZ) -> list[Slot]:
    """Parse every `cron`/`timezone` pair under `on.schedule` in a workflow."""
    text = workflow_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    in_schedule = False
    schedule_indent = 0
    slots: list[Slot] = []
    pending: str | None = None
    pending_tz = tz_default

    def flush() -> None:
        nonlocal pending, pending_tz
        if pending:
            label = label_for_cron(pending)
            slots.append(Slot(cron=pending, timezone=pending_tz, label=label,
                              run_type=scraper.classify_run(label)))
        pending, pending_tz = None, tz_default

    for raw in lines:
        line = raw.rstrip()
        stripped = line.strip()
        indent = len(line) - len(line.lstrip())
        if re.match(r"^\s*schedule:\s*$", line) and not in_schedule:
            in_schedule, schedule_indent = True, indent
            continue
        if in_schedule:
            # Any sibling key at or above the `schedule:` indent ends the block.
            if stripped and not stripped.startswith("#") and indent <= schedule_indent:
                flush()
                in_schedule = False
                continue
            if stripped.startswith("#") or not stripped:
                continue
            match = CRON_LINE.match(line)
            if match:
                flush()
                pending = " ".join(match.group(1).split())
                continue
            tz_match = TZ_LINE.match(line)
            if tz_match and pending is not None:
                pending_tz = tz_match.group(1).strip()
                continue
    flush()
    return slots


# --------------------------------------------------------------------------- #
# Run history
# --------------------------------------------------------------------------- #
def parse_iso(value: str) -> dt.datetime | None:
    text = str(value or "").strip().replace("Z", "+00:00")
    if not text:
        return None
    try:
        moment = dt.datetime.fromisoformat(text)
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=dt.timezone.utc)


def load_run_history(path: Path = DEFAULT_HISTORY) -> list[dict]:
    if not path.exists():
        return []
    runs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(entry, dict):
            runs.append(entry)
    return runs


def covering_run(slot: Slot, runs: list[dict],
                 freshness_minutes: int = FRESHNESS_MINUTES) -> dict | None:
    """A recorded run that already did this slot's job.

    A run covers a slot in either of two ways:

    * it has the slot's own run type and started in the 24 hours after the slot
      came due - this is what lets a catch-up that lands hours late still count;
    * or it is any successful **checked** run that started within
      `freshness_minutes` of the slot, so a manual re-scrape just before or just
      after a slot is not immediately repeated by the guard.

    An unchecked `--no-check` merge never publishes `PremiumTV.m3u`, so it cannot
    stand in for a scheduled check however fresh it is; the same goes for a run
    that failed.
    """
    if slot.start_utc is None:
        return None
    window_end = slot.start_utc + dt.timedelta(hours=24)
    early_tolerance = slot.start_utc - dt.timedelta(minutes=5)
    fresh_from = slot.start_utc - dt.timedelta(minutes=freshness_minutes)
    fresh_to = slot.start_utc + dt.timedelta(minutes=freshness_minutes)
    for run in runs:
        started = parse_iso(run.get("started_utc", ""))
        if started is None:
            continue
        if run.get("status") not in COVERING_STATUSES or run.get("exit_code", 1) != 0:
            continue
        if run.get("run_type") == slot.run_type and early_tolerance <= started < window_end:
            return run
        if run.get("checked") and fresh_from <= started <= fresh_to:
            return run
    return None


# --------------------------------------------------------------------------- #
# GitHub API
# --------------------------------------------------------------------------- #
def gh_api(path: str, token: str = "", method: str = "GET", payload: dict | None = None) -> dict:
    url = path if path.startswith("http") else f"https://api.github.com{path}"
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28",
               "User-Agent": "premiumtv-schedule-guard"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    data = json.dumps(payload).encode() if payload is not None else None
    if data is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        body = response.read()
    return json.loads(body) if body else {}


ACTIVE_STATES = {"queued", "in_progress", "requested", "waiting", "pending"}


def scrape_is_busy(repo: str, token: str, workflow: str = "scrape.yml",
                   cooldown_minutes: int = COOLDOWN_MINUTES) -> tuple[bool, str]:
    """True when a scrape is running or finished very recently."""
    try:
        data = gh_api(f"/repos/{repo}/actions/workflows/{workflow}/runs?per_page=5", token)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as exc:
        return False, f"could not read recent runs ({exc}); assuming idle"
    now = dt.datetime.now(dt.timezone.utc)
    for run in data.get("workflow_runs", []):
        if str(run.get("status", "")).lower() in ACTIVE_STATES:
            return True, f"run {run.get('id')} is {run.get('status')}"
        started = parse_iso(run.get("run_started_at") or run.get("created_at") or "")
        if started and (now - started) < dt.timedelta(minutes=cooldown_minutes):
            return True, f"run {run.get('id')} started {(now - started).seconds // 60} min ago"
    return False, "idle"


def dispatch_scrape(repo: str, token: str, label: str, scheduled_for: str) -> None:
    gh_api(f"/repos/{repo}/dispatches", token, method="POST", payload={
        "event_type": "scrape-now",
        "client_payload": {"label": label, "scheduled_for": scheduled_for,
                           "triggered_by": "schedule-guard"},
    })


# --------------------------------------------------------------------------- #
# Evaluation
# --------------------------------------------------------------------------- #
def evaluate(slots: list[Slot], runs: list[dict], now: dt.datetime,
             grace_minutes: int = GRACE_MINUTES, lookback_days: int = LOOKBACK_DAYS,
             freshness_minutes: int = FRESHNESS_MINUTES) -> list[Slot]:
    """Attach today's (and yesterday's late) start time and coverage to each slot."""
    horizon = now - dt.timedelta(days=lookback_days)
    for slot in slots:
        try:
            spec = slot.spec
        except ValueError as exc:
            slot.state, slot.covered_by = "invalid", str(exc)
            continue
        start = previous_occurrence(now, spec, slot.timezone)
        if start is None or start < horizon:
            slot.state = "not-due"
            continue
        slot.start_utc = start
        run = covering_run(slot, runs, freshness_minutes)
        if run is not None:
            covered_at = parse_iso(run.get("started_utc", ""))
            slot.covered_by = str(run.get("run_id", ""))
            slot.state = "covered"
            if covered_at is not None:
                slot.delay_minutes = (covered_at - start).total_seconds() / 60.0
            continue
        late_minutes = (now - start).total_seconds() / 60.0
        slot.delay_minutes = late_minutes
        slot.state = "overdue" if late_minutes >= grace_minutes else "due-soon"
    return slots


def overdue_slots(slots: list[Slot]) -> list[Slot]:
    return [s for s in slots if s.state == "overdue" and s.start_utc is not None]


# Reused from the scraper so a delay can never be rendered two different ways
# in run-history.jsonl, STATUS.md and the guard summary.
format_delay = scraper.format_delay


def local_label(moment: dt.datetime | None, tz_name: str) -> str:
    if moment is None:
        return "-"
    tz = _timezone(tz_name)
    return f"{moment.astimezone(tz):%Y-%m-%d %I:%M %p %Z}"


def make_report_markdown(slots: list[Slot], now: dt.datetime, busy: bool, busy_reason: str,
                         dispatched: str = "") -> str:
    lines = [
        "## Schedule guard",
        "",
        f"- **Checked at:** {now:%Y-%m-%d %H:%M:%S UTC}",
        f"- **Scrape workflow:** {'busy' if busy else 'idle'} ({busy_reason})",
    ]
    if dispatched:
        lines.append(f"- **Catch-up dispatched:** {dispatched}")
    lines += [
        "",
        "| Intended (New York) | Cron | Intended UTC | Started | Delay | State |",
        "|---|---|---|---|---:|---|",
    ]
    for slot in sorted(slots, key=lambda s: s.start_utc or dt.datetime.max.replace(tzinfo=dt.timezone.utc)):
        started = ""
        if slot.covered_by:
            started = slot.covered_by
        lines.append(
            f"| {local_label(slot.start_utc, slot.timezone)} | `{slot.cron}` | "
            f"{slot.start_utc:%Y-%m-%d %H:%M} UTC | {started} | "
            f"{format_delay(slot.delay_minutes)} | {slot.state} |"
            if slot.start_utc else
            f"| - | `{slot.cron}` | - | - | - | {slot.state} |"
        )
    overdue = overdue_slots(slots)
    lines += ["", f"**Overdue slots:** {len(overdue)}"]
    if not overdue and not dispatched:
        lines.append("")
        lines.append("Nothing to catch up on: every slot that has come due was already covered.")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- #
# Commands
# --------------------------------------------------------------------------- #
def cmd_check(args: argparse.Namespace) -> int:
    now = dt.datetime.now(dt.timezone.utc)
    workflow = Path(args.workflow)
    if not workflow.exists():
        log(f"[guard] workflow file not found: {workflow}")
        return 1
    slots = evaluate(load_schedule(workflow), load_run_history(Path(args.history)), now,
                     grace_minutes=args.grace, lookback_days=args.lookback_days,
                     freshness_minutes=args.freshness)
    for slot in slots:
        log(f"[guard] {slot.label:<26} cron='{slot.cron}' tz={slot.timezone} "
            f"state={slot.state} delay={format_delay(slot.delay_minutes)}")

    repo = args.repo or os.environ.get("GITHUB_REPOSITORY", "")
    token = args.token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    busy, busy_reason = (False, "skipped (--no-api)") if args.no_api else scrape_is_busy(
        repo, token, cooldown_minutes=args.cooldown) if repo else (False, "no repository configured")
    log(f"[guard] scrape workflow: {'busy' if busy else 'idle'} ({busy_reason})")

    dispatched = ""
    due = overdue_slots(slots)
    if due and not busy:
        slot = min(due, key=lambda s: s.start_utc)
        label = f"{slot.label} (catch-up {format_delay(slot.delay_minutes)})"[:80]
        scheduled_for = slot.start_utc.isoformat(timespec="seconds").replace("+00:00", "Z")
        if args.dry_run or not repo or not token:
            why = "dry run" if args.dry_run else "no repository/token available"
            log(f"[guard] would dispatch catch-up for '{slot.label}' -> {label} ({why})")
            dispatched = f"{label} (not sent: {why})"
        else:
            try:
                dispatch_scrape(repo, token, label, scheduled_for)
                dispatched = label
                log(f"[guard] dispatched catch-up scrape: {label} (scheduled for {scheduled_for})")
            except urllib.error.HTTPError as exc:
                detail = exc.read().decode("utf-8", "replace")[:300] if exc.fp else str(exc)
                log(f"[guard] ERROR dispatching catch-up: HTTP {exc.code} {detail}")
                dispatched = f"{label} (dispatch failed: HTTP {exc.code})"
            except (urllib.error.URLError, OSError, ValueError) as exc:
                log(f"[guard] ERROR dispatching catch-up: {exc}")
                dispatched = f"{label} (dispatch failed: {exc})"
    elif due and busy:
        log(f"[guard] {len(due)} slot(s) overdue but the scrape workflow is busy; will retry next cycle")
        dispatched = f"deferred, {len(due)} slot(s) overdue ({busy_reason})"
    elif not due:
        log("[guard] no overdue slots")

    if args.summary_file:
        Path(args.summary_file).write_text(
            make_report_markdown(slots, now, busy, busy_reason, dispatched), encoding="utf-8")
        log(f"[guard] summary written to {args.summary_file}")
    return 0


def cmd_report(args: argparse.Namespace) -> int:
    now = dt.datetime.now(dt.timezone.utc)
    slots = evaluate(load_schedule(Path(args.workflow)), load_run_history(Path(args.history)), now,
                     grace_minutes=args.grace, lookback_days=args.lookback_days,
                     freshness_minutes=args.freshness)
    sys.stdout.write(make_report_markdown(slots, now, False, "not checked (--report)"))
    return 0


def cmd_label_for(args: argparse.Namespace) -> int:
    cron = " ".join(args.cron.split())
    slots = {s.cron: s for s in load_schedule(Path(args.workflow))} if Path(args.workflow).exists() else {}
    slot = slots.get(cron)
    print(slot.label if slot else label_for_cron(cron))
    return 0


def cmd_scheduled_for(args: argparse.Namespace) -> int:
    cron = " ".join(args.cron.split())
    tz_name = args.timezone
    if not tz_name:
        slots = {s.cron: s for s in load_schedule(Path(args.workflow))} if Path(args.workflow).exists() else {}
        tz_name = slots[cron].timezone if cron in slots else DEFAULT_TZ
    now = dt.datetime.now(dt.timezone.utc)
    moment = previous_occurrence(now, parse_cron(cron), tz_name)
    if moment is None:  # pragma: no cover - only for impossible expressions
        return 1
    print(moment.isoformat(timespec="seconds").replace("+00:00", "Z"))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--workflow", default=str(DEFAULT_WORKFLOW),
                    help="workflow whose on.schedule block defines the slots")
    ap.add_argument("--history", default=str(DEFAULT_HISTORY), help="run-history.jsonl to read")
    ap.add_argument("--repo", default="", help="owner/repo (default: $GITHUB_REPOSITORY)")
    ap.add_argument("--token", default="", help="API token (default: $GITHUB_TOKEN)")
    ap.add_argument("--grace", type=int, default=GRACE_MINUTES,
                    help="minutes after a slot before it counts as overdue")
    ap.add_argument("--cooldown", type=int, default=COOLDOWN_MINUTES,
                    help="minutes after a scrape started before another may be dispatched")
    ap.add_argument("--lookback-days", type=int, default=LOOKBACK_DAYS,
                    help="how many days back to look for uncovered slots")
    ap.add_argument("--freshness", type=int, default=FRESHNESS_MINUTES,
                    help="a successful checked run within this many minutes of a slot "
                         "covers it, whatever its run type")
    ap.add_argument("--summary-file", default="", help="write the markdown report here")
    ap.add_argument("--dry-run", action="store_true", help="report only; never dispatch")
    ap.add_argument("--no-api", action="store_true", help="do not query the GitHub API")
    sub = ap.add_subparsers(dest="command", required=True)

    sub.add_parser("check", help="report coverage and dispatch a catch-up scrape when due")
    sub.add_parser("report", help="print the coverage table only")
    label_cmd = sub.add_parser("label-for", help="print the label for a cron expression")
    label_cmd.add_argument("--cron", required=True)
    sched_cmd = sub.add_parser("scheduled-for", help="print the UTC instant a cron last fired")
    sched_cmd.add_argument("--cron", required=True)
    sched_cmd.add_argument("--timezone", default="", help="IANA name (default: from the workflow)")

    args = ap.parse_args(argv)
    handlers = {"check": cmd_check, "report": cmd_report,
                "label-for": cmd_label_for, "scheduled-for": cmd_scheduled_for}
    return handlers[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
