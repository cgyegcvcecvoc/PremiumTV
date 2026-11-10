"""The Movies & Shows shelf states: paused, restored, and honest in every client."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "playlists" / "vod" / "vod-catalog.json"

sys.path.insert(0, str(ROOT / "scripts"))
import vod_catalog  # noqa: E402
import vod_shelf  # noqa: E402


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class ShelfStateTests(unittest.TestCase):
    def test_the_committed_catalogue_is_paused_and_valid(self):
        catalog = json.loads(text(CATALOG))
        self.assertEqual(catalog["schema"], 1)
        self.assertEqual(catalog.get("status"), "coming_soon")
        self.assertEqual(catalog["items"], [])
        self.assertEqual(vod_catalog.validate_document(catalog), [])

    def test_a_paused_catalogue_may_not_publish_titles(self):
        catalog = vod_shelf.pause_document({"source": "test"}, "2026-11-10T00:00:00Z")
        self.assertEqual(catalog["status"], "coming_soon")
        self.assertEqual(catalog["items"], [])
        self.assertEqual(vod_catalog.validate_document(catalog), [])
        catalog["items"] = [{"id": "vod-hidden", "title": "Hidden"}]
        self.assertTrue(
            any("must not publish items" in problem for problem in vod_catalog.validate_document(catalog))
        )

    def test_an_available_catalogue_still_needs_titles(self):
        problems = vod_catalog.validate_document({"schema": 1, "status": "available", "items": []})
        self.assertTrue(any("non-empty" in problem for problem in problems))

    def test_the_shelf_keeps_its_test_media_for_a_later_restore(self):
        media = ROOT / "playlists" / "vod" / "media"
        self.assertTrue((media / "premiumtv-test-card.mp4").is_file())
        self.assertTrue((media / "premiumtv-test-card.jpg").is_file())
        self.assertIn("--resume", text(ROOT / "scripts" / "vod_shelf.py"))

    def test_every_client_has_a_coming_soon_page(self):
        web = text(ROOT / "web" / "src" / "index.html") + text(ROOT / "web" / "src" / "app.js")
        self.assertIn("movies-coming-soon", web)
        android = text(ROOT / "android" / "app" / "src" / "main" / "kotlin" / "com" / "premiumtv" / "app" / "ui" / "VodShelf.kt")
        self.assertIn("comingSoon", android)
        macos = text(ROOT / "macos" / "app" / "src" / "renderer" / "app.js")
        self.assertIn("vodComingSoon", macos)


if __name__ == "__main__":
    unittest.main()
