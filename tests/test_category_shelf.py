"""Offline tests for the categories/ shelf and its verification.

The shelf is a slice of an already published playlist, so every test here asks
one of two questions: does the builder copy the published channels in the
published order, and does ``scripts/verify_playlists.py`` notice when the
committed shelf is not that any more? No network is involved.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import build_categories  # noqa: E402
import categorize  # noqa: E402
import verify_playlists  # noqa: E402

GUIDE = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/EPG/PremiumTV.xml"
USA_GUIDE = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/EPG/USA.xml"

# Two sports channels with a spare feed, two news channels, one cartoon, and one
# channel in a group so small it should not get a file of its own.
MAIN = f"""#EXTM3U x-tvg-url="{GUIDE}"
#EXTINF:-1 tvg-id="ESPN.us" group-title="Sports",ESPN
http://example.test/espn.m3u8
#EXTINF:-1 tvg-id="ESPN.us" group-title="Sports",ESPN (Backup 1)
http://example.test/espn-backup.m3u8
#EXTINF:-1 tvg-id="NFLNetwork.us" group-title="Sports",NFL Network
http://example.test/nfl.m3u8
#EXTINF:-1 tvg-id="CNN.us" group-title="News",CNN
http://example.test/cnn.m3u8
#EXTINF:-1 tvg-id="BBCNews.uk" group-title="News",BBC News
http://example.test/bbc.m3u8
#EXTINF:-1 tvg-id="CartoonNetwork.us" group-title="Cartoons",Cartoon Network
http://example.test/cartoon.m3u8
#EXTINF:-1 tvg-id="Placid.us" group-title="Aria Web Channels",Placid
http://example.test/placid.m3u8
"""

USA = f"""#EXTM3U x-tvg-url="{USA_GUIDE}"
#EXTINF:-1 tvg-id="ESPN.us" group-title="Sports",ESPN
http://example.test/espn.m3u8
#EXTINF:-1 tvg-id="ESPN.us" group-title="Sports",ESPN (Backup 1)
http://example.test/espn-backup.m3u8
#EXTINF:-1 tvg-id="CNN.us" group-title="News",CNN
http://example.test/cnn.m3u8
"""


class ShelfTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.main = self.dir / "PremiumTV.m3u"
        self.usa = self.dir / "USA.m3u"
        self.main.write_text(MAIN, encoding="utf-8")
        self.usa.write_text(USA, encoding="utf-8")
        self.shelf = self.dir / "categories"
        categorize.set_group_votes(None)

    def tearDown(self):
        categorize.set_group_votes(None)
        self.tmp.cleanup()

    def build(self, **kwargs):
        kwargs.setdefault("label", "unit")
        kwargs.setdefault("min_size", 1)
        return build_categories.build(self.shelf, self.main, self.usa, **kwargs)

    def entries(self, path: Path) -> list[tuple[str, str, str]]:
        return verify_playlists.playlist_entries(path)

    # -- layout ------------------------------------------------------------ #
    def test_writes_the_headline_usa_file_first(self):
        index = self.build()
        self.assertEqual(index["files"][0]["file"], str(self.shelf / "USA.m3u"))
        self.assertTrue((self.shelf / "USA.m3u").is_file())
        self.assertTrue((self.shelf / "README.md").is_file())
        self.assertTrue((self.shelf / "index.json").is_file())

    def test_usa_file_is_the_published_usa_playlist_entry_for_entry(self):
        self.build()
        self.assertEqual(self.entries(self.shelf / "USA.m3u"), self.entries(self.usa))

    def test_category_files_are_slices_in_published_order(self):
        self.build()
        sports = self.entries(self.shelf / "USA" / "Sports.m3u")
        self.assertEqual([name for name, _, _ in sports], ["ESPN", "ESPN (Backup 1)"])
        self.assertEqual([group for _, _, group in sports], ["Sports", "Sports"])
        world_sports = self.entries(self.shelf / "All" / "Sports.m3u")
        self.assertEqual([name for name, _, _ in world_sports],
                         ["ESPN", "ESPN (Backup 1)", "NFL Network"])
        news = self.entries(self.shelf / "All" / "News.m3u")
        self.assertEqual([name for name, _, _ in news], ["CNN", "BBC News"])

    def test_a_channel_in_a_tiny_group_stays_in_the_parent_file_only(self):
        self.build(min_size=3)
        for missing in ("Aria_Web_Channels.m3u", "Cartoons.m3u", "News.m3u"):
            self.assertFalse((self.shelf / "All" / missing).exists())
        # ... and the small groups are still in the playlist the shelf came from.
        main_names = [name for name, _, _ in self.entries(self.main)]
        self.assertIn("Placid", main_names)
        self.assertIn("Cartoon Network", main_names)

    def test_every_file_keeps_its_source_guide_header(self):
        self.build()
        usa_first = (self.shelf / "USA.m3u").read_text(encoding="utf-8").splitlines()[0]
        world_first = (self.shelf / "All" / "Sports.m3u").read_text(
            encoding="utf-8").splitlines()[0]
        self.assertIn(USA_GUIDE, usa_first)
        self.assertIn(GUIDE, world_first)

    def test_readme_and_index_describe_what_was_written(self):
        index = self.build()
        readme = (self.shelf / "README.md").read_text(encoding="utf-8")
        self.assertIn("USA.m3u", readme)
        self.assertIn("(USA/Sports.m3u)", readme)
        self.assertIn("(All/News.m3u)", readme)
        self.assertEqual(index["totals"][build_categories.USA_SCOPE], 3)
        self.assertEqual(index["totals"][build_categories.WORLD_SCOPE], 7)
        self.assertEqual(index["sources"][build_categories.USA_SCOPE], str(self.usa))

    # -- rewriting --------------------------------------------------------- #
    def test_unchanged_files_are_left_alone(self):
        self.build()
        before = (self.shelf / "USA.m3u").read_text(encoding="utf-8")
        index = self.build()
        self.assertTrue(all(row["unchanged"] for row in index["files"]))
        self.assertFalse(any(row["written"] for row in index["files"]))
        self.assertEqual((self.shelf / "USA.m3u").read_text(encoding="utf-8"), before)

    def test_a_dead_link_removed_upstream_updates_the_shelf_file(self):
        self.build()
        self.usa.write_text(USA.replace("http://example.test/cnn.m3u8\n", ""), encoding="utf-8")
        index = self.build()
        written = [row["file"] for row in index["files"] if row["written"]]
        self.assertIn(str(self.shelf / "USA.m3u"), written)
        self.assertEqual([name for name, _, _ in self.entries(self.shelf / "USA.m3u")],
                         ["ESPN", "ESPN (Backup 1)"])

    def test_a_group_that_disappears_upstream_loses_its_file(self):
        self.build()
        self.assertTrue((self.shelf / "USA" / "News.m3u").is_file())
        self.usa.write_text(USA.replace("http://example.test/cnn.m3u8\n", ""), encoding="utf-8")
        index = self.build()
        self.assertIn(str(self.shelf / "USA" / "News.m3u"), index["removed"])
        self.assertFalse((self.shelf / "USA" / "News.m3u").exists())

    # -- verification ------------------------------------------------------ #
    def test_verifier_passes_on_a_fresh_shelf(self):
        self.build()
        result = verify_playlists.verify_category_shelf(self.shelf, self.main, self.usa)
        self.assertEqual(result["issues"], [])
        self.assertFalse(result["skipped"])
        statuses = {row["status"] for row in result["files"]}
        self.assertEqual(statuses, {"ok"})

    def test_verifier_catches_a_stale_file(self):
        self.build()
        target = self.shelf / "USA" / "Sports.m3u"
        target.write_text(target.read_text(encoding="utf-8").replace("ESPN", "Gone"),
                          encoding="utf-8")
        result = verify_playlists.verify_category_shelf(self.shelf, self.main, self.usa)
        self.assertTrue(any("stale" in issue for issue in result["issues"]))
        self.assertEqual({row["status"] for row in result["files"] if row["status"] != "ok"},
                         {"stale"})

    def test_verifier_catches_a_missing_file(self):
        self.build()
        (self.shelf / "USA" / "News.m3u").unlink()
        result = verify_playlists.verify_category_shelf(self.shelf, self.main, self.usa)
        self.assertTrue(any("News.m3u is missing" in issue for issue in result["issues"]))

    def test_verifier_catches_a_leftover_file(self):
        self.build()
        (self.shelf / "All" / "Undefined.m3u").write_text("#EXTM3U\n", encoding="utf-8")
        result = verify_playlists.verify_category_shelf(self.shelf, self.main, self.usa)
        self.assertTrue(any("not part of the shelf" in issue for issue in result["issues"]))

    def test_verifier_notes_a_missing_shelf_only_when_it_is_required(self):
        skipped = verify_playlists.verify_category_shelf(self.shelf, self.main, self.usa,
                                                         allow_missing=True)
        self.assertTrue(skipped["skipped"])
        self.assertEqual(skipped["issues"], [])
        required = verify_playlists.verify_category_shelf(self.shelf, self.main, self.usa,
                                                          allow_missing=False)
        self.assertFalse(required["skipped"])
        self.assertTrue(any("is missing" in issue for issue in required["issues"]))


class VerifyRunTest(unittest.TestCase):
    """verify_playlists.py --strict must fail on a shelf that drifted."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.playlists = self.dir / "playlists"
        (self.playlists / "countries").mkdir(parents=True)
        (self.playlists / "PremiumTV.m3u").write_text(MAIN, encoding="utf-8")
        (self.playlists / "countries" / "USA.m3u").write_text(USA, encoding="utf-8")
        self.checks = self.playlists / "checks"
        categorize.set_group_votes(None)

    def tearDown(self):
        categorize.set_group_votes(None)
        self.tmp.cleanup()

    def run_verify(self, *args) -> int:
        return verify_playlists.main([
            "--out", str(self.playlists), "--epg-dir", str(self.dir / "EPG"),
            "--no-epg-parse", *args])

    def test_strict_run_fails_when_the_shelf_is_stale_and_passes_once_rebuilt(self):
        build_categories.build(self.dir / "categories", self.playlists / "PremiumTV.m3u",
                               self.playlists / "countries" / "USA.m3u", label="unit")
        self.assertEqual(self.run_verify("--strict", "--require-shelf"), 0)
        target = self.dir / "categories" / "USA.m3u"
        target.write_text(target.read_text(encoding="utf-8") + "", encoding="utf-8")
        (self.playlists / "countries" / "USA.m3u").write_text(
            USA + '#EXTINF:-1 tvg-id="KTTV.us" group-title="News",KTTV\n'
                  "http://example.test/kttv.m3u8\n", encoding="utf-8")
        self.assertEqual(self.run_verify("--strict", "--require-shelf"), 1)
        build_categories.build(self.dir / "categories", self.playlists / "PremiumTV.m3u",
                               self.playlists / "countries" / "USA.m3u", label="unit")
        self.assertEqual(self.run_verify("--strict", "--require-shelf"), 0)

    def test_without_require_shelf_a_missing_shelf_is_not_a_failure(self):
        self.assertEqual(self.run_verify("--strict"), 0)

    def test_no_shelf_skips_the_check_even_when_required(self):
        self.assertEqual(self.run_verify("--strict", "--require-shelf", "--no-shelf"), 0)


if __name__ == "__main__":
    unittest.main()
