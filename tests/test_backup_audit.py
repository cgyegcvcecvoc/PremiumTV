"""Tests for the offline backup/channel integrity audit."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_backups  # noqa: E402

PLAYLIST = """#EXTM3U x-tvg-url="https://example.com/guide.xml"
#EXTINF:-1 tvg-id="ESPN.us" tvg-logo="https://example.com/espn.png" group-title="Sports",ESPN (1080p)
https://example.com/espn.m3u8
#EXTINF:-1 tvg-id="ESPN.us" tvg-logo="https://example.com/espn.png" group-title="Sports Backups",ESPN (Backup 1)
https://example.com/espn-backup.m3u8
#EXTINF:-1 tvg-id="CNN.us" group-title="News",CNN (720p)
https://example.com/cnn.m3u8
#EXTINF:-1 tvg-id="CNN.us" group-title="News Backups",CNN (Backup 1)
https://example.com/cnn-backup.m3u8
"""


class BackupAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.playlist = self.dir / "PremiumTV.m3u"
        self.playlist.write_text(PLAYLIST, encoding="utf-8")
        self.categories = self.dir / "categories"
        self.categories.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def test_a_healthy_backup_pair_has_no_problems(self):
        report = audit_backups.audit(self.playlist, self.categories)
        self.assertEqual(report["entries"], 4)
        self.assertEqual(report["unique_channels"], 2)
        self.assertEqual(report["backup_feeds"], 2)
        self.assertEqual(report["duplicate_backup_names"], [])
        self.assertEqual(report["orphans"], [])
        self.assertEqual(report["problems"], [])
        self.assertIn("None: every backup name is unique",
                      audit_backups.render(report))

    def test_duplicate_backup_name_and_orphan_are_reported(self):
        text = PLAYLIST + (
            '#EXTINF:-1 tvg-id="ESPN.us" group-title="Sports Backups",ESPN (Backup 1)\n'
            "https://example.com/espn-backup-2.m3u8\n"
            '#EXTINF:-1 tvg-id="Ghost.us" group-title="Sports Backups",Ghost (Backup 1)\n'
            "https://example.com/ghost.m3u8\n"
        )
        self.playlist.write_text(text, encoding="utf-8")
        report = audit_backups.audit(self.playlist, self.categories)
        self.assertIn("ESPN (Backup 1)", report["duplicate_backup_names"])
        self.assertIn("Ghost (Backup 1)", report["orphans"])
        self.assertTrue(any("not unique" in problem for problem in report["problems"]))
        self.assertTrue(any("no primary" in problem for problem in report["problems"]))

    def test_strict_exit_code_reflects_problems(self):
        self.assertEqual(audit_backups.main(
            ["--playlist", str(self.playlist), "--categories-dir", str(self.categories),
             "--out", "-", "--strict"]), 0)
        self.playlist.write_text(
            PLAYLIST + '#EXTINF:-1 tvg-id="X.us" group-title="Sports Backups",X (Backup 1)\n'
            "https://example.com/x.m3u8\n", encoding="utf-8")
        self.assertEqual(audit_backups.main(
            ["--playlist", str(self.playlist), "--categories-dir", str(self.categories),
             "--out", "-", "--strict"]), 1)


if __name__ == "__main__":
    unittest.main()
