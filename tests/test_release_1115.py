"""1.1.15 contracts: the guide matches the playlist the apps actually ship.

1.1.14 was published without installers because both installer workflows failed
at the Android bundle gate before compiling: ``EPG/USA.xml`` listed guide
channels the live USA feed no longer carries. The guide was still scoped to the
frozen legacy ``playlists/countries/USA.m3u`` while the apps had moved to
``playlists/live/USA.m3u``, so any scheduled guide build could break the gate
again. These tests pin the fix and the release surfaces.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "android" / "tools"))

import build_bundle  # noqa: E402


def text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Version1115Tests(unittest.TestCase):
    def test_the_1_1_15_record_is_kept(self):
        # 1.1.15 was published without installers (the Android build failed on a
        # misplaced @Composable). Its notes stay as the record; every-surface
        # syncing is checked against the current release by test_release_1116.
        notes = text("release-notes-1.1.15.md")
        self.assertIn("# PremiumTV 1.1.15 — Crash diagnostics and hardened sources", notes)
        self.assertIn("versionCode `101150000`", notes)
        self.assertIn("Version 1.1.15 published: crash diagnostics, with installers",
                      text("CHANGELOG.md"))



class GuideMatchesPlaylistTests(unittest.TestCase):
    def test_the_usa_guide_only_lists_playlist_channels(self):
        channels, _ = build_bundle.parse_m3u(str(ROOT / "playlists" / "live" / "USA.m3u"))
        programmes = build_bundle.parse_xmltv(str(ROOT / "EPG" / "USA.xml"))
        known = {channel["id"] for channel in channels if channel["id"]}
        self.assertTrue(programmes, "the USA guide must carry listings")
        orphan = {programme["c"] for programme in programmes} - known
        self.assertEqual(
            orphan, set(),
            "EPG/USA.xml lists channels the live USA playlist does not carry",
        )

    def test_country_guides_are_built_from_the_live_feed(self):
        source = text("scripts/epg_build.py")
        self.assertIn('live = playlist_path.parent.parent / "live" / playlist_path.name', source)
        self.assertIn("if live.is_file():", source)
        self.assertIn("ids = country_playlist_ids(source)", source)


if __name__ == "__main__":
    unittest.main()
