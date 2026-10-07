"""Offline tests for scripts/rebuild_playlists.py."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import categorize  # noqa: E402
import epg_match  # noqa: E402
import rebuild_playlists  # noqa: E402

GUIDE = """<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="test">
  <channel id="NFLNetwork.us"><display-name>NFL Network</display-name></channel>
  <channel id="Buzzr.us"><display-name>Buzzr</display-name></channel>
  <programme channel="NFLNetwork.us" start="20260101000000 +0000" stop="20260101010000 +0000">
    <title>Game day</title>
  </programme>
  <programme channel="Buzzr.us" start="20260101000000 +0000" stop="20260101010000 +0000">
    <title>Family Feud</title>
  </programme>
</tv>
"""

DUPLICATE_URL_PLAYLIST = """#EXTM3U x-tvg-url="https://example.com/guide.xml"
#EXTINF:-1 tvg-id="Nickelodeon.br" group-title="Cartoons",Nickelodeon (Brazil) (480p)
https://stmv2.srvif.com/nicktoons/nicktoons/playlist.m3u8
#EXTINF:-1 tvg-id="NickToons.br" group-title="Cartoons",NickToons Brasil (480p)
https://stmv2.srvif.com/nicktoons/nicktoons/playlist.m3u8
#EXTINF:-1 tvg-id="MeTV.us" group-title="Classic TV",MeTV
http://main.example/metv.m3u8
"""

PLAYLIST = """#EXTM3U x-tvg-url="https://example.com/guide.xml"
# old header comment that should not survive
#EXTINF:-1 tvg-id="NFL.Network.HD.us2" group-title="TV",NFL Network
http://main.example/nfl.m3u8
#EXTINF:-1 tvg-id="NFL.Network.HD.us2" group-title="TV",NFL Network (720p)
http://spare.example/nfl.m3u8
#EXTINF:-1 tvg-id="Buzzr.stream.us2" group-title="Entertainment",Buzzr (1080p)
http://main.example/buzzr.m3u8
#EXTINF:-1 tvg-id="FoxNews.us" group-title="News",Fox News
http://main.example/fox.m3u8
"""


class DuplicateUrlTest(unittest.TestCase):
    """A re-publish resolves a repeated URL instead of copying it forward."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.playlist = self.dir / "priority.m3u"
        self.playlist.write_text(DUPLICATE_URL_PLAYLIST, encoding="utf-8")
        categorize.set_group_votes(None)

    def tearDown(self):
        categorize.set_group_votes(None)
        self.tmp.cleanup()

    def test_the_stream_is_published_once_under_the_name_the_url_supports(self):
        result = rebuild_playlists.rebuild_file(self.playlist, None)
        self.assertEqual(result["duplicate_urls_removed"], 1)
        text = self.playlist.read_text(encoding="utf-8")
        urls = [line for line in text.splitlines() if line.startswith("http")]
        self.assertEqual(sorted(urls), sorted(set(urls)))
        self.assertIn("NickToons Brasil", text)
        self.assertNotIn("Nickelodeon (Brazil)", text)


class RebuildTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.playlist = self.dir / "list.m3u"
        self.playlist.write_text(PLAYLIST, encoding="utf-8")
        self.guide_path = self.dir / "guide.xml"
        self.guide_path.write_text(GUIDE, encoding="utf-8")
        self.guide = epg_match.Guide().load(self.guide_path)
        categorize.set_group_votes(None)

    def tearDown(self):
        categorize.set_group_votes(None)
        self.tmp.cleanup()

    def test_playlist_is_republished_in_curated_order(self):
        result = rebuild_playlists.rebuild_file(self.playlist, self.guide)
        text = self.playlist.read_text(encoding="utf-8")
        self.assertTrue(result["written"])
        self.assertEqual(result["channels"], 4)
        groups = [line for line in text.splitlines() if "group-title=" in line]
        order = [line.split('group-title="')[1].split('"')[0] for line in groups]
        # The curated order: Sports first, then Fox Channels (position 3), Game
        # Shows last of the nine.
        self.assertEqual(order, ["Sports", "Sports Backups", "Fox Channels", "Game Shows"])
        # The x-tvg-url header survives; the stale comment line does not.
        self.assertTrue(text.startswith('#EXTM3U x-tvg-url="https://example.com/guide.xml"'))

    def test_duplicate_becomes_a_named_backup(self):
        rebuild_playlists.rebuild_file(self.playlist, self.guide)
        text = self.playlist.read_text(encoding="utf-8")
        self.assertIn("NFL Network (Backup 1)", text)
        self.assertIn('group-title="Sports Backups"', text)

    def test_guide_ids_are_corrected(self):
        result = rebuild_playlists.rebuild_file(self.playlist, self.guide)
        # Neither "NFL.Network.HD.us2" nor "Buzzr.stream.us2" is declared in the
        # guide; both channels are re-pointed at the id that is.
        self.assertEqual(result["epg"]["unmatched"], 1)      # Fox News only
        self.assertEqual(result["epg"]["name"], 3)           # NFL, its backup, Buzzr
        text = self.playlist.read_text(encoding="utf-8")
        self.assertIn('tvg-id="Buzzr.us"', text)
        self.assertIn('tvg-id="NFLNetwork.us"', text)

    def test_dry_run_leaves_the_file_alone(self):
        before = self.playlist.read_text(encoding="utf-8")
        result = rebuild_playlists.rebuild_file(self.playlist, self.guide, dry_run=True)
        self.assertFalse(result["written"])
        self.assertEqual(self.playlist.read_text(encoding="utf-8"), before)

    def test_category_files_and_index_are_written(self):
        rebuild_playlists.rebuild_file(self.playlist, self.guide)
        channels = rebuild_playlists.read_playlist(self.playlist)[0]
        out_dir = self.dir / "categories"
        summary = rebuild_playlists.write_category_playlists(
            channels, "#EXTM3U", out_dir, self.guide, "now", "now", dry_run=False, min_size=1)
        names = {row["category"] for row in summary}
        self.assertEqual(names, {"Sports", "Sports Backups", "Game Shows", "Fox Channels"})
        self.assertTrue((out_dir / "Sports.m3u").is_file())
        self.assertTrue((out_dir / "Game_Shows.m3u").is_file())
        rebuild_playlists.write_categories_index(summary, out_dir, str(self.playlist), "now")
        index = (out_dir / "README.md").read_text(encoding="utf-8")
        self.assertIn("Cartoons", index)          # the published order is documented
        self.assertIn("Sports.m3u", index)

    def test_tiny_groups_do_not_get_their_own_file(self):
        rebuild_playlists.rebuild_file(self.playlist, self.guide)
        channels = rebuild_playlists.read_playlist(self.playlist)[0]
        out_dir = self.dir / "categories"
        summary = rebuild_playlists.write_category_playlists(
            channels, "#EXTM3U", out_dir, self.guide, "now", "now", dry_run=False, min_size=2)
        # Sports (1) and its backup (1) are skipped, Game Shows and Fox are not
        # (each has exactly one channel too, so only min_size=1 would emit them).
        self.assertEqual(summary, [])

    def test_audit_report_is_generated(self):
        result = rebuild_playlists.rebuild_file(self.playlist, self.guide)
        channels = rebuild_playlists.read_playlist(self.playlist)[0]
        summary = rebuild_playlists.write_category_playlists(
            channels, "#EXTM3U", self.dir / "categories", self.guide, "now", "now",
            dry_run=False, min_size=1)
        report = rebuild_playlists.build_report([result], summary, self.guide, "now", "now")
        self.assertIn("Game Shows", report)
        self.assertIn("no guide entry", report)


if __name__ == "__main__":
    unittest.main()
