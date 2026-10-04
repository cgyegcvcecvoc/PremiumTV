"""Offline tests for scripts/epg_match.py - guide ids without network access."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import epg_match  # noqa: E402
import scraper  # noqa: E402

GUIDE = """<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="test">
  <channel id="NFLNetwork.us">
    <display-name>NFL Network</display-name>
    <display-name>NFL Network (720p)</display-name>
  </channel>
  <channel id="AE.us">
    <display-name>A&amp;E</display-name>
  </channel>
  <channel id="AE.us@East">
    <display-name>A&amp;E (US East)</display-name>
  </channel>
  <channel id="premiumtv.international.mystery">
    <display-name>Mystery Channel</display-name>
  </channel>
  <channel id="Ambiguous.one">
    <display-name>Two Names</display-name>
  </channel>
  <channel id="Ambiguous.two">
    <display-name>Two Names</display-name>
  </channel>
  <programme channel="NFLNetwork.us" start="20260101000000 +0000" stop="20260101010000 +0000">
    <title>Game day</title>
  </programme>
  <programme channel="AE.us" start="20260101000000 +0000" stop="20260101010000 +0000">
    <title>Live PD</title>
  </programme>
</tv>
"""


def guide_in(tmpdir) -> epg_match.Guide:
    path = Path(tmpdir) / "guide.xml"
    path.write_text(GUIDE, encoding="utf-8")
    return epg_match.Guide().load(path)


def channel(name, tvg_id=""):
    return scraper.Channel(name=name, url="http://example.com/x.m3u8", source="test",
                           attrs={"tvg-id": tvg_id} if tvg_id else {})


class GuideTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.guide = guide_in(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_channel_and_programme_ids_are_loaded(self):
        self.assertIn("NFLNetwork.us", self.guide.ids)
        self.assertEqual(self.guide.with_programmes, {"NFLNetwork.us", "AE.us"})

    def test_exact_id_wins(self):
        self.assertEqual(self.guide.match("NFLNetwork.us", "NFL Network"),
                         ("NFLNetwork.us", "exact"))

    def test_base_id_match_drops_the_feed_qualifier(self):
        self.assertEqual(self.guide.match("AE.us@West", "A&E"), ("AE.us", "base"))

    def test_display_name_match(self):
        self.assertEqual(self.guide.match("SomethingElse.us", "NFL Network"),
                         ("NFLNetwork.us", "name"))

    def test_looser_spelling_match(self):
        # The playlist calls it "NFL Network (720p) [Not 24/7]"; the guide knows
        # it as "NFL Network". Parenthetical noise is stripped before matching.
        self.assertEqual(
            self.guide.match("", "NFL Network (1080p) [Not 24/7]"), ("NFLNetwork.us", "name"))
        self.assertEqual(self.guide.match("", "Storage Wars by A&E (720p)"),
                         ("", ""))

    def test_ambiguous_names_are_never_guessed(self):
        self.assertEqual(self.guide.match("", "Two Names"), ("", ""))

    def test_synthetic_ids_are_not_used_as_a_target(self):
        # A premiumtv.* id is the scraper's own placeholder: it carries no
        # schedule, so pointing another channel at it would change nothing.
        self.assertEqual(self.guide.match("", "Mystery Channel"), ("", ""))

    def test_no_match_keeps_the_playlist_id(self):
        self.assertEqual(self.guide.match("Nothing.us", "Nothing TV"), ("", ""))


class RemapTest(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.guide = guide_in(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_channels_are_pointed_at_a_usable_id(self):
        channels = [
            channel("NFL Network", "NFLNetwork.us"),
            channel("A&E (US East)", "AE.us@East"),
            channel("A&E (US West)", "AE.us@West"),
            channel("Unknown Channel", "Unknown.us"),
        ]
        stats = epg_match.remap_channels(channels, self.guide)
        self.assertEqual(stats["exact"], 2)
        self.assertEqual(stats["base"], 1)
        self.assertEqual(stats["unmatched"], 1)
        self.assertEqual(channels[2].attrs["tvg-id"], "AE.us")
        self.assertEqual(channels[3].attrs["tvg-id"], "Unknown.us")

    def test_remap_never_invents_an_id(self):
        channels = [channel("Nope", "Nope.us")]
        epg_match.remap_channels(channels, self.guide)
        self.assertEqual(channels[0].attrs["tvg-id"], "Nope.us")


if __name__ == "__main__":
    unittest.main()
