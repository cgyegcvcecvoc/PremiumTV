"""The Movies & Shows test card: kept, playable and ready for a later shelf."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "playlists" / "vod" / "vod-catalog.json"
MEDIA = ROOT / "playlists" / "vod" / "media"
CLIP = MEDIA / "premiumtv-test-card.mp4"
POSTER = MEDIA / "premiumtv-test-card.jpg"


def catalogue() -> dict:
    return json.loads(CATALOG.read_text(encoding="utf-8"))


class TestCardTests(unittest.TestCase):
    """One short synthetic film the shelf can be exercised with in one play."""

    def test_the_test_card_leads_the_published_catalogue(self):
        document = catalogue()
        self.assertNotEqual(document.get("status"), "coming_soon")
        self.assertTrue(document["items"], "the shelf publishes titles")
        # The clip is first on the shelf so one short play proves the player.
        self.assertEqual(document["items"][0].get("test_card"), True)
        # It is the one entry authored here, so it streams from the repo's own
        # copy and has no Archive embed of its own.
        self.assertTrue(document["items"][0]["stream"])
        self.assertFalse(document["items"][0].get("embed"))

    def test_the_clip_is_committed_and_within_size(self):
        self.assertTrue(CLIP.is_file(), "playlists/vod/media/premiumtv-test-card.mp4 is missing")
        self.assertTrue(POSTER.is_file(), "playlists/vod/media/premiumtv-test-card.jpg is missing")
        # The poster is a JPEG and the clip is under the size a committed test
        # asset may reach; Git keeps every version of it forever.
        self.assertEqual(POSTER.read_bytes()[:3], b"\xff\xd8\xff")
        self.assertLess(CLIP.stat().st_size, 4_000_000)

    def test_the_clip_carries_a_video_and_an_audio_track(self):
        data = CLIP.read_bytes()
        self.assertIn(b"ftyp", data[:64], "the clip is not an MP4")
        # The sample description boxes the players rely on: H.264 video and
        # AAC audio. `scripts/vod_test_card.py --check` makes the same call.
        self.assertTrue(b"avc1" in data or b"avc3" in data, "no H.264 sample entry")
        self.assertIn(b"mp4a", data, "no AAC sample entry")
        self.assertIn(b"moov", data)
        self.assertIn(b"mdat", data)

    def test_the_generator_accepts_the_committed_clip(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "vod_test_card.py"), "--check"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_the_packaged_renderer_may_show_the_poster(self):
        html = (ROOT / "macos" / "app" / "src" / "renderer" / "index.html").read_text(encoding="utf-8")
        self.assertRegex(html, r"img-src[^;]*https://cdn\.jsdelivr\.net")
        self.assertRegex(html, r"img-src[^;]*https://archive\.org")

    def test_the_bundle_builder_still_ships_the_catalogue(self):
        builder = (ROOT / "android" / "tools" / "build_bundle.py").read_text(encoding="utf-8")
        self.assertIn('os.path.join(REPO_ROOT, "playlists", "vod", "vod-catalog.json")', builder)


if __name__ == "__main__":
    unittest.main()
