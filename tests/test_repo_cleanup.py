"""Offline tests for scripts/cleanup_repo.py (the biweekly repository sweep).

Everything runs against a temporary copy of the log/EPG layout: the tests never let
the tool near the real playlists/logs directory, and a cleanup run that reported on
this repository's own files would depend on when the last scrape happened.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import cleanup_repo  # noqa: E402

SEP = "=" * 88


def entry_for(report: dict, path: Path) -> dict:
    """The log entry for one file, whatever order the rotators ran in."""
    wanted = str(path)
    matches = [item for item in report["logs"] if item["file"] == wanted]
    if not matches:
        raise AssertionError(f"{path.name} is not in the report: "
                             f"{[item['file'] for item in report['logs']]}")
    return matches[0]


def run_cli(out: Path, epg: Path, *extra: str) -> dict:
    args = ["--out", str(out), "--epg-dir", str(epg), "--no-stray", "--no-stale-reports",
            "--dry-run-edit-log", *extra]
    with redirect_stdout(StringIO()):
        code = cleanup_repo.main(args)
    report = json.loads((out / "checks" / "cleanup.json").read_text(encoding="utf-8"))
    report["_exit"] = code
    return report


class CleanupTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.out = self.tmp / "playlists"
        self.logs = self.out / "logs"
        self.epg = self.tmp / "EPG"
        for directory in (self.logs, self.out / "countries", self.epg):
            directory.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_edits_log(self, name: str, blocks: int, lines_per_block: int = 2,
                        banner: bool = False, style: str = "hash") -> Path:
        path = self.logs / name
        rows: list[str] = []
        if banner:
            rows += [SEP, "PREMIUMTV1 CHRONOLOGICAL LOG EDITS (.TXT)", SEP, ""]
        for index in range(blocks):
            if style == "hash":
                rows.append(f"## 2026-01-{index + 1:02d}T00:00:00Z - run {index}")
            else:
                rows += [SEP, f"RUN ID:       run-{index}"]
            rows += [f"  line {number} of block {index}" for number in range(lines_per_block)]
            rows.append("")
        path.write_text("\n".join(rows) + "\n", encoding="utf-8")
        return path

    # -- log rotation -------------------------------------------------------- #
    def test_rotation_keeps_the_newest_blocks_and_the_banner(self):
        path = self.write_edits_log("epg-check-edits.txt", 12, style="hash")
        report = run_cli(self.out, self.epg, "--apply", "--keep-runs", "4",
                         "--max-log-lines", "0")
        entry = entry_for(report, path)
        self.assertEqual(entry["blocks"], 12)
        self.assertEqual(entry["dropped_blocks"], 8)
        self.assertEqual(entry["kept_blocks"], 4)
        text = path.read_text(encoding="utf-8")
        # The newest run survives, the oldest does not, and no block is cut in half.
        self.assertIn("run 11", text)
        self.assertIn("line 1 of block 11", text)
        self.assertNotIn("run 3\n", text)
        self.assertEqual(len([line for line in text.splitlines() if line.startswith("## ")]), 4)

    def test_a_single_pathological_block_is_trimmed_by_the_line_cap(self):
        # One run that logged a line per country playlist is bigger than the whole
        # budget, so the block count alone cannot fix it - the line cap drops the
        # older blocks and still refuses to delete the newest record.
        self.write_edits_log("link-check-edits.txt", 6, lines_per_block=300, style="hash")
        report = run_cli(self.out, self.epg, "--apply", "--keep-runs", "30",
                         "--max-log-lines", "400")
        entry = entry_for(report, self.logs / "link-check-edits.txt")
        self.assertEqual(entry["kept_blocks"], 1)
        self.assertEqual(entry["dropped_blocks"], 5)
        self.assertIn("over 400 lines", entry["reason"])
        text = (self.logs / "link-check-edits.txt").read_text(encoding="utf-8")
        self.assertIn("block 5", text)

    def test_report_only_writes_nothing(self):
        path = self.write_edits_log("epg-build-edits.txt", 40, style="hash")
        before = path.read_text(encoding="utf-8")
        report = run_cli(self.out, self.epg, "--keep-runs", "5")
        self.assertEqual(path.read_text(encoding="utf-8"), before)
        self.assertEqual(entry_for(report, path)["dropped_blocks"], 35)
        self.assertFalse(entry_for(report, path)["written"])
        self.assertIn("Nothing was written by this run",
                      (self.out / "checks" / "CLEANUP.md").read_text(encoding="utf-8"))

    def test_run_id_blocks_ignore_the_banner_separators(self):
        path = self.write_edits_log("log-edits.txt", 9, lines_per_block=3,
                                     banner=True, style="runid")
        report = run_cli(self.out, self.epg, "--apply", "--keep-runs", "3",
                         "--max-log-lines", "0")
        entry = entry_for(report, path)
        self.assertEqual(entry["blocks"], 9)
        self.assertEqual(entry["kept_blocks"], 3)
        lines = path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(lines[1], "PREMIUMTV1 CHRONOLOGICAL LOG EDITS (.TXT)")
        self.assertTrue(any(line.startswith("RUN ID:       run-8") for line in lines))
        self.assertFalse(any(line.startswith("RUN ID:       run-2") for line in lines))

    # -- orphans ------------------------------------------------------------- #
    def test_orphan_country_guide_is_removed_but_the_merged_one_is_not(self):
        (self.out / "countries" / "UK.m3u").write_text("#EXTM3U\n", encoding="utf-8")
        (self.epg / "UK.xml").write_text("<tv/>", encoding="utf-8")
        (self.epg / "Atlantis.xml").write_text("<tv/>", encoding="utf-8")
        (self.epg / "PremiumTV.xml").write_text("<tv/>", encoding="utf-8")
        run_cli(self.out, self.epg)
        self.assertTrue((self.epg / "Atlantis.xml").exists())        # report only
        report = run_cli(self.out, self.epg, "--apply")
        self.assertFalse((self.epg / "Atlantis.xml").exists())
        self.assertTrue((self.epg / "UK.xml").exists())
        self.assertTrue((self.epg / "PremiumTV.xml").exists())
        self.assertEqual([Path(name).name for name in report["removed"]], ["Atlantis.xml"])

    def test_orphan_check_can_be_turned_off(self):
        (self.epg / "Atlantis.xml").write_text("<tv/>", encoding="utf-8")
        report = run_cli(self.out, self.epg, "--no-orphans", "--apply")
        self.assertEqual(report["removed"], [])
        self.assertTrue((self.epg / "Atlantis.xml").exists())

    # -- published-data currency -------------------------------------------- #
    def test_expired_guide_is_called_out_even_though_it_is_full_of_channels(self):
        past = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=5))
        stamp = past.strftime("%Y%m%d%H%M%S")
        (self.epg / "PremiumTV.xml").write_text(
            "<tv>\n"
            '  <channel id="A.us"><display-name>A</display-name></channel>\n'
            '  <channel id="B.us"><display-name>B</display-name></channel>\n'
            f'  <programme start="{stamp} +0000" stop="{stamp} +0000" channel="A.us">\n'
            "    <title>Old</title>\n  </programme>\n"
            "</tv>\n", encoding="utf-8")
        report = run_cli(self.out, self.epg)
        self.assertEqual(report["guide"]["live_channels"], 0)
        self.assertTrue(any("expired data" in problem for problem in report["problems"]))

    def test_current_guide_is_not_flagged(self):
        now = dt.datetime.now(dt.timezone.utc)
        start = (now + dt.timedelta(hours=1)).strftime("%Y%m%d%H%M%S")
        stop = (now + dt.timedelta(hours=2)).strftime("%Y%m%d%H%M%S")
        (self.epg / "PremiumTV.xml").write_text(
            "<tv>\n"
            '  <programme start="{} +0000" stop="{} +0000" channel="A.us">\n'
            "    <title>Live</title>\n  </programme>\n</tv>\n".format(start, stop),
            encoding="utf-8")
        report = run_cli(self.out, self.epg)
        self.assertEqual(report["guide"]["live_channels"], 1)
        self.assertEqual(report["outcome"], "CLEAN")

    # -- quarantine ----------------------------------------------------------- #
    def test_quarantine_drops_entries_a_reader_would_ignore_anyway(self):
        stale = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=30))
        entries = {
            "https://ok/live.m3u8": {"last_seen_utc": dt.datetime.now(
                dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")},
            "https://old/dead.m3u8": {"last_seen_utc": stale.isoformat(
                timespec="seconds").replace("+00:00", "Z")},
            "https://nodate/dead.m3u8": {"reason": "no timestamp recorded"},
            "https://stale-rules/dead.m3u8": {"reason": "variant HTTP 414"},
            "": {"reason": "malformed row"},
        }
        path = self.out / "checks" / "quarantine.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"entries": entries, "count": len(entries)}),
                        encoding="utf-8")
        report = run_cli(self.out, self.epg, "--apply")
        kept = json.loads(path.read_text(encoding="utf-8"))
        # The expired one, the malformed one and the pre-fix "variant HTTP 414"
        # go (the reader ignores all three); the undated one that still proves
        # its link dead stays, because scraper.load_quarantine() honours it and
        # so it must not be un-quarantined here - it is reported instead.
        self.assertEqual(sorted(kept["entries"]),
                         ["https://nodate/dead.m3u8", "https://ok/live.m3u8"])
        self.assertEqual(kept["count"], 2)
        self.assertEqual(report["quarantine"]["dropped"], 3)
        self.assertEqual(report["quarantine"]["stale_rules"], 1)
        self.assertEqual(report["quarantine"]["undated"], 1)
        self.assertTrue(any("no usable" in problem for problem in report["problems"]))

    # -- report --------------------------------------------------------------- #
    def test_empty_playlist_is_reported_as_a_problem(self):
        (self.out / "PremiumTV.m3u").write_text("#EXTM3U\n", encoding="utf-8")
        report = run_cli(self.out, self.epg)
        self.assertTrue(any("holds no channel" in problem for problem in report["problems"]))
        markdown = (self.out / "checks" / "CLEANUP.md").read_text(encoding="utf-8")
        self.assertIn("Empty playlists", markdown)

    def test_strict_fails_when_a_problem_remains(self):
        # A live guide, so the only thing left to complain about is the empty file.
        stop = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=2))
        start = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=1))
        (self.epg / "PremiumTV.xml").write_text(
            "<tv>\n  <programme start=\"{}\" stop=\"{}\" channel=\"A.us\">\n"
            "    <title>Live</title>\n  </programme>\n</tv>\n".format(
                start.strftime("%Y%m%d%H%M%S +0000"), stop.strftime("%Y%m%d%H%M%S +0000")),
            encoding="utf-8")
        (self.out / "PremiumTV.m3u").write_text("#EXTM3U\n", encoding="utf-8")
        report = run_cli(self.out, self.epg, "--strict")
        self.assertEqual(report["_exit"], 1)
        (self.out / "PremiumTV.m3u").write_text(
            "#EXTM3U\n#EXTINF:-1,X\nhttps://example.invalid/a.m3u8\n", encoding="utf-8")
        report = run_cli(self.out, self.epg, "--strict")
        self.assertEqual(report["_exit"], 0)
        self.assertEqual(report["outcome"], "CLEAN")

    def test_missing_logs_are_reported_not_fatal(self):
        report = run_cli(self.out, self.epg)
        self.assertEqual({item.get("skipped") for item in report["logs"]}, {"missing"})
        self.assertEqual(report["_exit"], 0)
        self.assertTrue((self.out / "checks" / "CLEANUP.md").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
