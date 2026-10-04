"""Offline tests for scripts/update_m3u.py - no network, no real streams."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import categorize  # noqa: E402
import scraper  # noqa: E402
import update_m3u  # noqa: E402

HEADER = '#EXTM3U x-tvg-url="https://example.com/guide.xml"\n'

PLAYLIST = HEADER + "\n".join([
    '#EXTINF:-1 tvg-id="NFL.Network.HD.us2" group-title="TV",NFL Network',
    "http://main.example/nfl.m3u8",
    '#EXTINF:-1 tvg-id="NFL.Network.HD.us2" group-title="TV",NFL Network (Backup 1)',
    "http://backup.example/nfl.m3u8",
    '#EXTINF:-1 tvg-id="FoxNews.us" group-title="News",Fox News',
    "http://main.example/fox.m3u8",
    '#EXTINF:-1 tvg-id="PBS.us" group-title="TV",PBS',
    "http://main.example/pbs.m3u8",
    "",
])


def fake_results(mapping):
    """Results dict shaped like check_channels() output."""
    return {url: {"status": status, "reason": "", "name": url}
            for url, status in mapping.items()}


def run(tmpdir, results, pool=None, extra=()):
    path = Path(tmpdir) / "list.m3u8"
    path.write_text(PLAYLIST, encoding="utf-8")
    argv = [str(path), "--output-dir", str(Path(tmpdir) / "out"), "--no-corpus", *extra]
    if results is None:
        argv.append("--offline")
    args = update_m3u.build_parser().parse_args(argv)
    with patch.object(update_m3u, "check_channels", return_value=results or {}):
        summary = update_m3u.update_file(path, args, pool or {})
    return path, summary


class OfflineTest(unittest.TestCase):
    """--offline tidies a file that is already downloaded: no network at all."""

    def test_categories_and_order_are_applied_without_checking(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            _path, summary = run(tmpdir, None)
            self.assertEqual(summary["channels"], 4)
            groups = list(summary["counts"])
            self.assertEqual(groups[0], "Sports")
            self.assertEqual(groups[1], "Sports Backups")
            written = (Path(tmpdir) / "out" / "list.m3u8").read_text(encoding="utf-8")
        self.assertIn(HEADER.strip(), written)
        self.assertIn('group-title="Sports"', written)
        self.assertIn('group-title="Sports Backups"', written)
        self.assertIn("NFL Network", written)

    def test_every_link_survives_an_offline_run(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            _path, summary = run(tmpdir, None)
            self.assertEqual(summary["stats"], {})
            self.assertEqual(summary["removed"], [])


class RepairTest(unittest.TestCase):
    """A dead link is repaired from the file's own backups, then from the pool."""

    def test_dead_main_link_is_replaced_by_its_backup(self):
        results = fake_results({
            "http://main.example/nfl.m3u8": "offline",
            "http://backup.example/nfl.m3u8": "working",
            "http://main.example/fox.m3u8": "working",
            "http://main.example/pbs.m3u8": "working",
        })
        with tempfile.TemporaryDirectory() as tmpdir:
            _path, summary = run(tmpdir, results)
            self.assertEqual(summary["stats"]["promoted"], 1)
            self.assertEqual(summary["stats"]["removed"], 0)
            written = (Path(tmpdir) / "out" / "list.m3u8").read_text(encoding="utf-8")
        # The dead URL is gone, the backup's URL now carries the channel.
        self.assertNotIn("http://main.example/nfl.m3u8", written)
        self.assertIn('group-title="Sports",NFL Network', written)
        self.assertEqual(written.count("http://backup.example/nfl.m3u8"), 1)

    def test_pool_candidate_is_used_when_the_file_has_no_backup(self):
        results = fake_results({
            "http://main.example/nfl.m3u8": "offline",
            "http://backup.example/nfl.m3u8": "offline",
            "http://main.example/fox.m3u8": "working",
            "http://main.example/pbs.m3u8": "working",
            "http://pool.example/nfl.m3u8": "working",
        })
        spare = scraper.Channel(name="NFL Network (1080p)", url="http://pool.example/nfl.m3u8",
                                source="pool", attrs={"tvg-id": "NFL.Network.HD.us2",
                                                      "group-title": "Sports"})
        pool = {categorize.channel_key("NFL Network (1080p)", "USA"): [spare]}
        with tempfile.TemporaryDirectory() as tmpdir:
            _path, summary = run(tmpdir, results, pool=pool)
            self.assertEqual(summary["stats"]["replaced"], 1)
            written = (Path(tmpdir) / "out" / "list.m3u8").read_text(encoding="utf-8")
        self.assertIn("http://pool.example/nfl.m3u8", written)

    def test_hopeless_link_is_removed(self):
        results = fake_results({
            "http://main.example/nfl.m3u8": "offline",
            "http://backup.example/nfl.m3u8": "offline",
            "http://main.example/fox.m3u8": "working",
            "http://main.example/pbs.m3u8": "working",
        })
        with tempfile.TemporaryDirectory() as tmpdir:
            _path, summary = run(tmpdir, results, extra=("--max-remove-ratio", "0.75"))
            self.assertEqual(summary["stats"]["removed"], 2)
            self.assertEqual(len(summary["removed"]), 2)

    def test_transient_failures_are_kept(self):
        results = fake_results({
            "http://main.example/nfl.m3u8": "unreachable",
            "http://backup.example/nfl.m3u8": "blocked",
            "http://main.example/fox.m3u8": "working",
            "http://main.example/pbs.m3u8": "working",
        })
        with tempfile.TemporaryDirectory() as tmpdir:
            _path, summary = run(tmpdir, results)
            self.assertEqual(summary["stats"]["removed"], 0)
            self.assertEqual(summary["channels"], 4)

    def test_a_bad_network_day_aborts_instead_of_gutting_the_file(self):
        results = fake_results({url: "offline" for url in (
            "http://main.example/nfl.m3u8", "http://backup.example/nfl.m3u8",
            "http://main.example/fox.m3u8", "http://main.example/pbs.m3u8")})
        with tempfile.TemporaryDirectory() as tmpdir:
            _path, summary = run(tmpdir, results)
            self.assertEqual(summary["status"], "aborted")
            self.assertFalse(summary["written"])
            self.assertIn("minimum", summary["reason"])

    def test_too_many_removals_abort_the_run(self):
        results = fake_results({
            "http://main.example/nfl.m3u8": "working",
            "http://backup.example/nfl.m3u8": "offline",
            "http://main.example/fox.m3u8": "offline",
            "http://main.example/pbs.m3u8": "offline",
        })
        with tempfile.TemporaryDirectory() as tmpdir:
            _path, summary = run(tmpdir, results, extra=("--max-remove-ratio", "0.2"))
            self.assertEqual(summary["status"], "aborted")
            self.assertIn("--max-remove-ratio", summary["reason"])


class QuarantineTest(unittest.TestCase):
    """A link that answers but never plays is treated as broken."""

    def test_quarantined_link_counts_as_dead(self):
        import json
        with tempfile.TemporaryDirectory() as tmpdir:
            quarantine = Path(tmpdir) / "quarantine.json"
            quarantine.write_text(json.dumps({"entries": {
                "http://main.example/nfl.m3u8": {
                    "reason": "variant HTTP 404",
                    "hits": 2,
                    "last_seen_utc": __import__("datetime").datetime.now(
                        __import__("datetime").timezone.utc).isoformat(timespec="seconds"),
                }}}), encoding="utf-8")
            results = fake_results({"http://main.example/nfl.m3u8": "working"})
            held = update_m3u.apply_quarantine(results, quarantine)
            self.assertEqual(held, 1)
            self.assertEqual(results["http://main.example/nfl.m3u8"]["status"], "offline")
            # The verdict is reused, not overwritten with a shallow "working".
            self.assertIn("variant HTTP 404", results["http://main.example/nfl.m3u8"]["reason"])

    def test_quarantine_is_repaired_from_the_backup(self):
        import json
        import datetime
        with tempfile.TemporaryDirectory() as tmpdir:
            quarantine = Path(tmpdir) / "quarantine.json"
            quarantine.write_text(json.dumps({"entries": {
                "http://main.example/nfl.m3u8": {
                    "reason": "playlist only", "hits": 1,
                    "last_seen_utc": datetime.datetime.now(
                        datetime.timezone.utc).isoformat(timespec="seconds"),
                }}}), encoding="utf-8")
            results = fake_results({
                "http://main.example/nfl.m3u8": "working",
                "http://backup.example/nfl.m3u8": "working",
                "http://main.example/fox.m3u8": "working",
                "http://main.example/pbs.m3u8": "working",
            })
            _path, summary = run(tmpdir, results, extra=("--quarantine", str(quarantine)))
            self.assertEqual(summary["stats"]["promoted"], 1)
            written = (Path(tmpdir) / "out" / "list.m3u8").read_text(encoding="utf-8")
        self.assertNotIn("http://main.example/nfl.m3u8", written)


if __name__ == "__main__":
    unittest.main()
