"""Offline tests for scripts/schedule_guard.py.

The guard exists because GitHub's scheduler starts `schedule:` crons late (or
drops them). These tests pin the cron maths, the workflow parsing, the coverage
rules and the catch-up decision, all without touching the network.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
import schedule_guard as guard  # noqa: E402
import scraper  # noqa: E402

UTC = dt.timezone.utc


def at(text: str) -> dt.datetime:
    return dt.datetime.fromisoformat(text.replace("Z", "+00:00"))


def run_entry(started: str, run_type: str, status: str = "warning", exit_code: int = 0,
              run_id: str = "run-1") -> dict:
    return {"run_id": run_id, "started_utc": started, "run_type": run_type,
            "status": status, "exit_code": exit_code}


class CronParsingTest(unittest.TestCase):
    def test_simple_daily_cron(self):
        spec = guard.parse_cron("7 3 * * *")
        self.assertTrue(spec.matches(at("2026-09-29T03:07:00Z")))
        self.assertFalse(spec.matches(at("2026-09-29T03:00:00Z")))
        self.assertFalse(spec.matches(at("2026-09-29T04:07:00Z")))
        self.assertFalse(spec.day_restricted or spec.weekday_restricted)

    def test_lists_ranges_and_steps(self):
        spec = guard.parse_cron("4,24,44 * * * *")
        for minute in (4, 24, 44):
            self.assertTrue(spec.matches(at(f"2026-09-29T13:{minute:02d}:00Z")))
        self.assertFalse(spec.matches(at("2026-09-29T13:00:00Z")))
        stepped = guard.parse_cron("4-59/20 * * * *")
        self.assertEqual(stepped.minutes, frozenset({4, 24, 44}))
        ranged = guard.parse_cron("0 9-17 * * *")
        self.assertEqual(ranged.hours, frozenset(range(9, 18)))

    def test_named_months_and_weekdays(self):
        spec = guard.parse_cron("0 0 * JAN-MAR MON-FRI")
        self.assertTrue(spec.matches(at("2026-01-05T00:00:00Z")))   # a Monday in January
        self.assertFalse(spec.matches(at("2026-06-01T00:00:00Z")))  # June is out of range

    def test_both_day_fields_restricted_is_an_or(self):
        # POSIX cron: 13th of the month OR any Friday.
        spec = guard.parse_cron("0 0 13 * 5")
        self.assertTrue(spec.day_restricted and spec.weekday_restricted)
        self.assertTrue(spec.matches(at("2026-03-13T00:00:00Z")))   # a Friday the 13th
        self.assertTrue(spec.matches(at("2026-04-13T00:00:00Z")))   # a Monday the 13th
        self.assertTrue(spec.matches(at("2026-04-17T00:00:00Z")))   # a Friday, not the 13th
        self.assertFalse(spec.matches(at("2026-04-14T00:00:00Z")))  # neither

    def test_invalid_expressions_are_rejected(self):
        for expression in ("* * * *", "* * * * * *", "60 0 * * *", "0 24 * * *",
                           "0 0 * * 8", "5-1 0 * * *", "0 0 * *", ""):
            with self.subTest(expression=expression):
                with self.assertRaises(ValueError):
                    guard.parse_cron(expression)


class OccurrenceTest(unittest.TestCase):
    def test_previous_occurrence_converts_local_time_to_utc(self):
        spec = guard.parse_cron("7 3 * * *")
        # 2026-09-29 is EDT (UTC-4), so 03:07 in New York is 07:07 UTC.
        self.assertEqual(guard.previous_occurrence(at("2026-09-29T15:00:00Z"), spec, "America/New_York"),
                         at("2026-09-29T07:07:00Z"))
        # Before today's slot it must return yesterday's.
        self.assertEqual(guard.previous_occurrence(at("2026-09-29T06:00:00Z"), spec, "America/New_York"),
                         at("2026-09-28T07:07:00Z"))

    def test_previous_occurrence_rolls_back_over_est(self):
        spec = guard.parse_cron("7 3 * * *")
        # January is EST (UTC-5).
        self.assertEqual(guard.previous_occurrence(at("2026-01-15T18:00:00Z"), spec, "America/New_York"),
                         at("2026-01-15T08:07:00Z"))

    def test_exact_slot_time_counts_as_that_slot(self):
        spec = guard.parse_cron("23 6 * * *")
        self.assertEqual(guard.previous_occurrence(at("2026-09-29T10:23:00Z"), spec, "America/New_York"),
                         at("2026-09-29T10:23:00Z"))

    def test_spring_forward_hour_is_skipped_not_invented(self):
        # 02:30 does not exist in New York on 2026-03-08 (clocks jump 02:00 -> 03:00).
        # The guard must not invent an instant for it, so the previous real 02:30
        # (7 March, EST) is returned instead of a bogus "02:30" on 8 March.
        spec = guard.parse_cron("30 2 * * *")
        found = guard.previous_occurrence(at("2026-03-08T12:00:00Z"), spec, "America/New_York")
        self.assertIsNotNone(found)
        self.assertLessEqual(found, at("2026-03-08T12:00:00Z"))
        self.assertEqual(found, at("2026-03-07T07:30:00Z"))
        self.assertEqual(found.astimezone(guard._timezone("America/New_York")).strftime("%H:%M"), "02:30")

    def test_crons_outside_the_dst_gap_are_unaffected(self):
        # Every cron this repository actually uses is clear of the 02:00-03:00
        # spring-forward window, so each one still resolves on the day itself.
        for cron, expected in (("7 3 * * *", "2026-03-08T07:07:00Z"),
                               ("23 6 * * *", "2026-03-08T10:23:00Z"),
                               ("41 16 * * *", "2026-03-08T20:41:00Z")):
            with self.subTest(cron=cron):
                found = guard.previous_occurrence(at("2026-03-08T23:00:00Z"),
                                                  guard.parse_cron(cron), "America/New_York")
                self.assertEqual(found, at(expected))

    def test_next_occurrence(self):
        spec = guard.parse_cron("41 16 * * *")
        self.assertEqual(guard.next_occurrence(at("2026-09-29T15:00:00Z"), spec, "America/New_York"),
                         at("2026-09-29T20:41:00Z"))

    def test_unknown_timezone_falls_back_to_utc(self):
        spec = guard.parse_cron("0 3 * * *")
        with redirect_stdout(io.StringIO()):
            found = guard.previous_occurrence(at("2026-09-29T12:00:00Z"), spec, "Mars/Olympus")
        self.assertEqual(found, at("2026-09-29T03:00:00Z"))


class WorkflowParsingTest(unittest.TestCase):
    def test_reads_the_real_scrape_workflow(self):
        slots = guard.load_schedule(REPO / ".github" / "workflows" / "scrape.yml")
        self.assertEqual([slot.cron for slot in slots], ["7 3 * * *", "23 6 * * *", "41 16 * * *"])
        for slot in slots:
            self.assertEqual(slot.timezone, "America/New_York")
        self.assertEqual([slot.label for slot in slots],
                         ["3:07 AM daily scrape", "6:23 AM recheck", "4:41 PM final check"])
        self.assertEqual([slot.run_type for slot in slots],
                         ["regular_check", "recheck", "final_check"])

    def test_no_cron_sits_on_a_busy_minute(self):
        # GitHub's scheduler is most congested at minute 0; the whole point of
        # the off-peak minutes is to stop the multi-hour delays this repo saw.
        for slot in guard.load_schedule(REPO / ".github" / "workflows" / "scrape.yml"):
            with self.subTest(cron=slot.cron):
                self.assertNotIn(0, slot.spec.minutes)
                self.assertNotIn(15, slot.spec.minutes)

    def test_every_configured_cron_has_a_known_label(self):
        # Guards against drift between the workflows and SLOT_LABELS: both
        # scrape.yml and discover.yml ask the guard for their run label.
        for workflow in ("scrape.yml", "discover.yml"):
            for slot in guard.load_schedule(REPO / ".github" / "workflows" / workflow):
                with self.subTest(workflow=workflow, cron=slot.cron):
                    self.assertIn(slot.cron, guard.SLOT_LABELS)

    def test_monthly_discovery_cron_keeps_its_run_type(self):
        slots = guard.load_schedule(REPO / ".github" / "workflows" / "discover.yml")
        self.assertEqual([slot.cron for slot in slots], ["37 4 1 * *"])
        self.assertEqual(slots[0].label, "monthly new-channel discovery")
        self.assertEqual(scraper.classify_run(slots[0].label), "monthly_discovery")
        self.assertNotIn(0, slots[0].spec.minutes)

    def test_monthly_cron_resolves_to_the_first_of_the_month(self):
        spec = guard.parse_cron("37 4 1 * *")
        found = guard.previous_occurrence(at("2026-09-29T15:00:00Z"), spec, "America/New_York")
        self.assertEqual(found, at("2026-09-01T08:37:00Z"))

    def test_parses_a_synthetic_workflow_and_stops_at_the_next_key(self):
        yaml_text = """name: Test
on:
  schedule:
    # a comment inside the block
    - cron: "30 4 1 * *"
      timezone: "America/New_York"
    - cron: "0 12 * * 1-5"

  workflow_dispatch:
    inputs:
      cron: "not a schedule entry"
  repository_dispatch:
    types: [scrape-now]

jobs:
  x:
    steps:
      - run: echo "- cron: \\"99 99 * * *\\""
"""
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "wf.yml"
            path.write_text(yaml_text, encoding="utf-8")
            slots = guard.load_schedule(path)
        self.assertEqual([slot.cron for slot in slots], ["30 4 1 * *", "0 12 * * 1-5"])
        self.assertEqual(slots[0].timezone, "America/New_York")
        self.assertEqual(slots[1].timezone, guard.DEFAULT_TZ)

    def test_label_for_cron_generates_a_fallback(self):
        self.assertEqual(guard.label_for_cron("7 3 * * *"), "3:07 AM daily scrape")
        self.assertEqual(guard.label_for_cron("23 6 * * *"), "6:23 AM recheck")
        self.assertEqual(guard.label_for_cron("41 16 * * *"), "4:41 PM final check")
        self.assertEqual(guard.label_for_cron("30 9 * * *"), "9:30 AM scheduled scrape")
        self.assertEqual(guard.label_for_cron("*/20 * * * *"), "scheduled scrape")
        self.assertEqual(guard.label_for_cron("nonsense"), "scheduled scrape")

    def test_extra_whitespace_in_a_cron_is_normalised(self):
        self.assertEqual(guard.label_for_cron("  7   3  *  * * "), "3:07 AM daily scrape")


class CoverageTest(unittest.TestCase):
    now = at("2026-09-29T15:00:00Z")

    def slot(self, cron="7 3 * * *", label="3:07 AM daily scrape"):
        return guard.Slot(cron=cron, timezone="America/New_York", label=label,
                          run_type=scraper.classify_run(label))

    def states(self, slots, runs, now=None, **kwargs):
        return guard.evaluate(slots, runs, now or self.now, **kwargs)

    def test_uncovered_past_slot_is_overdue(self):
        [slot] = self.states([self.slot()], [])
        self.assertEqual(slot.state, "overdue")
        self.assertEqual(slot.start_utc, at("2026-09-29T07:07:00Z"))
        self.assertAlmostEqual(slot.delay_minutes, 473.0, places=1)

    def test_slot_inside_the_grace_period_is_not_overdue_yet(self):
        [slot] = self.states([self.slot()], [], now=at("2026-09-29T07:12:00Z"))
        self.assertEqual(slot.state, "due-soon")
        self.assertEqual(guard.overdue_slots([slot]), [])

    def test_late_run_still_covers_its_slot(self):
        runs = [run_entry("2026-09-29T13:51:00Z", "regular_check")]
        [slot] = self.states([self.slot()], runs)
        self.assertEqual(slot.state, "covered")
        self.assertAlmostEqual(slot.delay_minutes, 404.0, places=1)

    def test_punctual_run_covers_its_slot(self):
        [slot] = self.states([self.slot()], [run_entry("2026-09-29T07:09:00Z", "regular_check")])
        self.assertEqual(slot.state, "covered")
        self.assertAlmostEqual(slot.delay_minutes, 2.0, places=1)

    def test_failed_run_does_not_cover_a_slot(self):
        [slot] = self.states([self.slot()], [run_entry("2026-09-29T08:00:00Z", "regular_check",
                                                       status="failed", exit_code=1)])
        self.assertEqual(slot.state, "overdue")

    def test_unchecked_run_does_not_cover_a_slot(self):
        # A --no-check merge never publishes PremiumTV.m3u, so it cannot stand in
        # for a scheduled check.
        [slot] = self.states([self.slot()], [run_entry("2026-09-29T08:00:00Z", "regular_check",
                                                       status="unchecked")])
        self.assertEqual(slot.state, "overdue")

    def test_run_of_a_different_type_does_not_cover_the_slot(self):
        [slot] = self.states([self.slot()], [run_entry("2026-09-29T08:00:00Z", "recheck")])
        self.assertEqual(slot.state, "overdue")

    def test_run_from_the_previous_day_does_not_cover_the_slot(self):
        [slot] = self.states([self.slot()], [run_entry("2026-09-28T07:20:00Z", "regular_check")])
        self.assertEqual(slot.state, "overdue")

    def test_slot_far_outside_the_lookback_is_not_due(self):
        monthly = self.slot(cron="30 4 1 * *", label="monthly new-channel discovery")
        [slot] = self.states([monthly], [])
        self.assertEqual(slot.state, "not-due")
        self.assertIsNone(slot.start_utc)

    def test_invalid_cron_is_reported_not_fatal(self):
        [slot] = self.states([guard.Slot(cron="bogus", timezone="America/New_York",
                                         label="x", run_type="manual")], [])
        self.assertEqual(slot.state, "invalid")

    def test_earliest_overdue_slot_wins(self):
        slots = self.states([
            self.slot(cron="41 16 * * *", label="4:41 PM final check"),
            self.slot(cron="23 6 * * *", label="6:23 AM recheck"),
            self.slot(cron="7 3 * * *", label="3:07 AM daily scrape"),
        ], [])
        due = guard.overdue_slots(slots)
        self.assertEqual(len(due), 3)
        # At 11:00 EDT the most recently due 4:41 PM slot is yesterday's, so it is
        # the oldest uncovered slot and the one a catch-up should start with.
        earliest = min(due, key=lambda s: s.start_utc)
        self.assertEqual(earliest.label, "4:41 PM final check")
        self.assertEqual(earliest.start_utc, at("2026-09-28T20:41:00Z"))
        # Later in the day every slot belongs to today, so today's earliest leads.
        today = self.states([
            self.slot(cron="41 16 * * *", label="4:41 PM final check"),
            self.slot(cron="23 6 * * *", label="6:23 AM recheck"),
            self.slot(cron="7 3 * * *", label="3:07 AM daily scrape"),
        ], [], now=at("2026-09-29T23:00:00Z"))
        due_today = guard.overdue_slots(today)
        self.assertEqual(len(due_today), 3)
        self.assertEqual(min(due_today, key=lambda s: s.start_utc).label, "3:07 AM daily scrape")

    def test_a_covering_run_clears_only_its_own_slot(self):
        slots = self.states([
            self.slot(cron="7 3 * * *", label="3:07 AM daily scrape"),
            self.slot(cron="23 6 * * *", label="6:23 AM recheck"),
        ], [run_entry("2026-09-29T08:00:00Z", "regular_check")])
        self.assertEqual([slot.state for slot in slots], ["covered", "overdue"])


class CatchUpLabelTest(unittest.TestCase):
    def test_catch_up_labels_keep_their_run_type(self):
        # The guard appends "(catch-up +6h 51m)"; classify_run must still work.
        cases = {
            "3:07 AM daily scrape (catch-up +6h 51m)": "regular_check",
            "6:23 AM recheck (catch-up +1h 02m)": "recheck",
            "4:41 PM final check (catch-up +41m)": "final_check",
        }
        for label, run_type in cases.items():
            with self.subTest(label=label):
                self.assertEqual(scraper.classify_run(label), run_type)
                self.assertLessEqual(len(label), 80)

    def test_format_delay(self):
        self.assertEqual(guard.format_delay(None), "-")
        self.assertEqual(guard.format_delay(0), "+0m")
        self.assertEqual(guard.format_delay(41), "+41m")
        self.assertEqual(guard.format_delay(122), "+2h 02m")
        self.assertEqual(guard.format_delay(-5), "-5m")


class ReportTest(unittest.TestCase):
    def test_report_markdown_lists_every_slot(self):
        now = at("2026-09-29T15:00:00Z")
        slots = guard.evaluate(
            guard.load_schedule(REPO / ".github" / "workflows" / "scrape.yml"),
            [run_entry("2026-09-29T13:51:00Z", "regular_check", run_id="abc123")],
            now,
        )
        markdown = guard.make_report_markdown(slots, now, False, "idle", "")
        self.assertIn("## Schedule guard", markdown)
        self.assertIn("| Intended (New York) | Cron | Intended UTC | Started | Delay | State |", markdown)
        self.assertIn("`7 3 * * *`", markdown)
        self.assertIn("covered", markdown)
        self.assertIn("abc123", markdown)
        self.assertIn("**Overdue slots:**", markdown)

    def test_report_mentions_a_dispatch(self):
        now = at("2026-09-29T15:00:00Z")
        slots = guard.evaluate(guard.load_schedule(REPO / ".github" / "workflows" / "scrape.yml"), [], now)
        markdown = guard.make_report_markdown(slots, now, False, "idle", "6:23 AM recheck (catch-up +4h 37m)")
        self.assertIn("**Catch-up dispatched:** 6:23 AM recheck (catch-up +4h 37m)", markdown)


class CommandLineTest(unittest.TestCase):
    workflow = REPO / ".github" / "workflows" / "scrape.yml"

    def capture(self, argv):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = guard.main(argv)
        self.assertEqual(code, 0)
        return buffer.getvalue()

    def test_label_for(self):
        out = self.capture(["--workflow", str(self.workflow), "label-for", "--cron", "23 6 * * *"])
        self.assertEqual(out.strip(), "6:23 AM recheck")

    def test_scheduled_for_uses_the_workflow_timezone(self):
        out = self.capture(["--workflow", str(self.workflow), "scheduled-for", "--cron", "7 3 * * *"])
        moment = guard.parse_iso(out.strip())
        self.assertIsNotNone(moment)
        local = moment.astimezone(guard._timezone("America/New_York"))
        self.assertEqual((local.hour, local.minute), (3, 7))
        self.assertLessEqual(moment, dt.datetime.now(UTC))

    def test_report_command_runs_offline(self):
        with tempfile.TemporaryDirectory() as temp:
            history = Path(temp) / "run-history.jsonl"
            history.write_text(
                json.dumps(run_entry("2026-09-29T13:51:00Z", "regular_check")) + "\n", encoding="utf-8")
            out = self.capture(["--workflow", str(self.workflow), "--history", str(history), "report"])
        self.assertIn("## Schedule guard", out)

    def test_check_dry_run_never_dispatches(self):
        with tempfile.TemporaryDirectory() as temp:
            history = Path(temp) / "run-history.jsonl"
            summary = Path(temp) / "summary.md"
            out = self.capture([
                "--workflow", str(self.workflow), "--history", str(history),
                "--summary-file", str(summary), "--dry-run", "--no-api", "check",
            ])
            self.assertIn("would dispatch catch-up", out)
            self.assertIn("(dry run)", out)
            self.assertTrue(summary.exists(), "the step summary must be written")
            self.assertIn("## Schedule guard", summary.read_text(encoding="utf-8"))
        self.assertIn("3:07 AM daily scrape", out)

    def test_check_reports_nothing_to_do_when_covered(self):
        now = dt.datetime.now(UTC)
        # Build a history entry that covers whichever slot is most recently due.
        slots = guard.evaluate(guard.load_schedule(self.workflow), [], now)
        due = guard.overdue_slots(slots)
        self.assertTrue(due, "expected at least one overdue slot for this test")
        runs = [run_entry(slot.start_utc.isoformat(timespec="seconds").replace("+00:00", "Z"),
                          slot.run_type, run_id=f"cover-{i}")
                for i, slot in enumerate(guard.evaluate(guard.load_schedule(self.workflow), [], now))]
        with tempfile.TemporaryDirectory() as temp:
            history = Path(temp) / "run-history.jsonl"
            history.write_text("".join(json.dumps(run) + "\n" for run in runs), encoding="utf-8")
            out = self.capture([
                "--workflow", str(self.workflow), "--history", str(history),
                "--dry-run", "--no-api", "check",
            ])
        self.assertIn("no overdue slots", out)
        self.assertNotIn("would dispatch", out)


if __name__ == "__main__":
    unittest.main()
