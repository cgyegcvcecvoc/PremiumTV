"""Offline checks on the curated local-channel sources.

These pin the two audit fixes of 2026-11-25:

* WGAL has a second server. Its syndication feed answered HTTP 504 for five
  hours while the Local Now (Amagi) door of the same Hearst asset answered 200,
  so the curated source carries both and the scraper must treat them as one
  channel with a backup - not two channels in the NBC group.
* The A+E Crime 360 doors (LG, Vizio, Xumo, Pluto) are one channel. They all
  carry the same guide id in the curated source so the country split cannot
  scatter them across categories, and the Canadian network feed stays separate.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import categorize  # noqa: E402
import scraper  # noqa: E402


def read_source(relative: str) -> list:
    text = (ROOT / relative).read_text(encoding="utf-8")
    channels, _ = scraper.parse_m3u(text, Path(relative).stem)
    return channels


class LocalChannelsSourceTest(unittest.TestCase):

    def test_wgal_has_two_distinct_servers(self):
        channels = [c for c in read_source("playlists/sources/local-channels.m3u")
                    if "wgal" in c.name.lower()]
        self.assertEqual(len(channels), 2, [c.name for c in channels])
        self.assertEqual(len({c.url for c in channels}), 2)
        # One Uplynk/CloudFront door and one Local Now/Amagi door.
        hosts = " ".join(c.url for c in channels)
        self.assertIn("cloudfront.net", hosts)
        self.assertIn("localnow.api.cms.amdvids.com", hosts)

    def test_wgal_doors_become_one_channel_with_a_backup(self):
        channels = [c for c in read_source("playlists/sources/local-channels.m3u")
                    if "wgal" in c.name.lower()]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 1)
        self.assertEqual(len(backups), 1)
        self.assertEqual(primary[0].attrs["group-title"], "NBC")
        self.assertEqual(backups[0].attrs["group-title"], "NBC Backups")
        # The backup inherits the primary's guide id, so the schedule survives
        # the hop in a player.
        self.assertEqual(backups[0].attrs["tvg-id"], "NBC.us@WGAL")

    def test_local_now_provider_tag_is_recognised_in_brackets(self):
        self.assertEqual(
            categorize.clean_display_name("WGAL 8 (NBC) - Lancaster PA (720p) [Local Now]"),
            "WGAL 8 (NBC) - Lancaster PA")


class AENetworksSourceTest(unittest.TestCase):

    def test_crime_360_doors_share_one_guide_id(self):
        channels = [c for c in read_source("playlists/sources/ae-networks.m3u")
                    if "crime 360" in c.name.lower()]
        us = [c for c in channels if (c.attrs.get("tvg-country") or "") == "US"]
        self.assertGreaterEqual(len(us), 5)
        self.assertEqual({c.attrs.get("tvg-id") for c in us}, {"Crime360.us@SD"})
        # Canada is a different channel and keeps its own id.
        canada = [c for c in channels if (c.attrs.get("tvg-country") or "") == "CA"]
        self.assertEqual(len(canada), 1)
        self.assertNotEqual(canada[0].attrs.get("tvg-id"), "Crime360.us@SD")

    def test_crime_360_folds_to_one_channel_plus_backups(self):
        channels = [c for c in read_source("playlists/sources/ae-networks.m3u")
                    if "crime 360" in c.name.lower()]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 2, [c.name for c in primary])
        self.assertEqual(len(backups), len(channels) - 2)
        self.assertTrue(all(c.attrs["group-title"] == "A&E Networks Backups" for c in backups))
        # The 1080p door leads.
        us_primary = [c for c in primary if (c.attrs.get("tvg-country") or "") == "US"][0]
        self.assertEqual(us_primary.name, "Crime 360 (1080p)")


if __name__ == "__main__":
    unittest.main()
