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
    def test_the_committed_catalogue_publishes_titles_and_is_valid(self):
        catalog = json.loads(text(CATALOG))
        self.assertEqual(catalog["schema"], 1)
        self.assertNotEqual(catalog.get("status"), "coming_soon")
        self.assertTrue(catalog["items"], "the shelf must publish titles")
        self.assertEqual(vod_catalog.validate_document(catalog), [])

    def test_every_published_title_is_playable(self):
        """An entry needs a direct stream, an HTML embed, or both."""
        catalog = json.loads(text(CATALOG))
        self.assertGreater(len(catalog["items"]), 0)
        for item in catalog["items"]:
            label = item.get("title") or item.get("id")
            playable = bool(item.get("stream") or item.get("embed") or item.get("embed_html"))
            self.assertTrue(playable, "%s has neither a stream nor an embed" % label)
            if item.get("embed"):
                self.assertTrue(
                    item["embed"].startswith("https://"),
                    "%s publishes an insecure embed" % label,
                )
            if item.get("stream"):
                self.assertTrue(
                    item["stream"].startswith(("http://", "https://")),
                    "%s publishes an insecure stream" % label,
                )

    def test_the_shelf_publishes_an_embed_for_every_archive_title(self):
        """The web and macOS players open the embed first; Android uses the MP4."""
        catalog = json.loads(text(CATALOG))
        archived = [item for item in catalog["items"] if item.get("archive_id")]
        self.assertGreater(len(archived), 0)
        for item in archived:
            self.assertEqual(item["embed"], "https://archive.org/embed/%s" % item["archive_id"])
            self.assertEqual(item["embed_kind"], "iframe")
            self.assertEqual(item["provider"], "Internet Archive")
            self.assertEqual(
                item["embeds"][0],
                {
                    "provider": "Internet Archive",
                    "kind": "iframe",
                    "url": item["embed"],
                },
            )

    def test_the_offline_rebuild_reproduces_the_committed_catalogue(self):
        """A rebuild with no network must resolve every curated entry."""
        resolved = [spec for spec in vod_catalog.CURATED if spec["slug"] in vod_catalog.RESOLVED]
        self.assertEqual(len(resolved), len(vod_catalog.CURATED))
        for spec in vod_catalog.CURATED:
            item = vod_catalog.build_item(spec, offline=True)
            self.assertIsNotNone(item, "%s has no cached derivative" % spec["slug"])

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
