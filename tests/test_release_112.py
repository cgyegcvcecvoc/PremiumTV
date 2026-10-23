"""1.1.2: side-player-first watching, the on-demand shelf and the version bump."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import release_version  # noqa: E402  (the shared version policy)

ANDROID = ROOT / "android" / "app" / "src" / "main" / "kotlin" / "com" / "premiumtv" / "app"
UI = ANDROID / "ui"
VOD = ROOT / "playlists" / "vod" / "vod-catalog.json"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class SidePlayerFirstTests(unittest.TestCase):
    """Clicking a channel docks it; clicking the picture goes full screen."""

    def test_opening_a_channel_starts_in_the_side_player(self):
        root = text(UI / "AppRoot.kt")
        self.assertIn("playing = channel to serversFor(channel, current.library.channels)", root)
        self.assertIn("sidePlayer = true", root)
        # The dock is what the viewer sees first, not the full-screen player.
        self.assertIn("if (selection == null || sidePlayer)", root)

    def test_the_picture_expands_to_full_screen_without_restarting(self):
        player = text(UI / "PlayerScreen.kt")
        self.assertIn("private fun SidePlayerPicture(", player)
        self.assertIn(".tvClickable(onExpand)", player)
        # One call site for the video in both layouts: the ExoPlayer instance
        # is never rebuilt by a flip.
        self.assertEqual(player.count("AndroidView("), 1)
        self.assertIn("onExpand = { sidePlayer = false }", text(UI / "AppRoot.kt"))
        self.assertIn('FocusButton("⤢ Big screen"', player)

    def test_mac_starts_in_the_side_player_and_expands_on_click(self):
        app = text(ROOT / "macos" / "app" / "src" / "renderer" / "app.js")
        block = app[app.index("async function openPlayer"):app.index("function minimizePlayer")]
        self.assertIn("playerMini = true;", block)
        self.assertIn("if (playerMini && !els.player.hidden) expandPlayer()", app)


class OnDemandShelfTests(unittest.TestCase):
    """The Movies & Shows tab is a working test shelf, not a coming-soon page."""

    def test_the_android_tab_renders_the_bundled_catalogue(self):
        home = text(UI / "HomeScreen.kt")
        self.assertIn("HomeTab.Movies -> VodShelfScreen(", home)
        self.assertIn('context.readVodCatalog()', home)
        self.assertIn('readAsset("vod-catalog.json")', home)
        shelf = text(UI / "VodShelf.kt")
        self.assertIn("internal fun parseVodCatalog(", shelf)
        self.assertIn("fun asChannel(): Channel", shelf)
        self.assertIn("fun VodShelfScreen(", shelf)
        self.assertNotIn("MoviesComingSoonScreen", home)

    def test_the_bundle_ships_the_on_demand_catalogue(self):
        builder = text(ROOT / "android" / "tools" / "build_bundle.py")
        self.assertIn('os.path.join(REPO_ROOT, "playlists", "vod", "vod-catalog.json")', builder)
        self.assertIn("meta.update(meta_extra)", builder)

    def test_the_mac_tab_renders_the_same_catalogue(self):
        app = text(ROOT / "macos" / "app" / "src" / "renderer" / "app.js")
        self.assertIn("function renderMovies()", app)
        self.assertIn("meta.vod_catalog", app)
        self.assertIn("function watchVod(item)", app)
        html = text(ROOT / "macos" / "app" / "src" / "renderer" / "index.html")
        self.assertIn('id="movies-grid"', html)
        self.assertIn("https://archive.org", html)  # CSP allows the poster host

    def test_the_catalogue_is_public_domain_and_playable(self):
        document = json.loads(text(VOD))
        self.assertEqual(document["schema"], 1)
        items = document["items"]
        self.assertGreaterEqual(len(items), 8)
        kinds = {item["kind"] for item in items}
        self.assertEqual(kinds, {"movie", "episode"})
        for item in items:
            self.assertTrue(item["stream"].startswith("https://"), item["id"])
            self.assertTrue(item["poster"].startswith("https://"), item["id"])
            self.assertIn("publicdomain", item["license"], item["id"])
            if item["kind"] == "episode":
                self.assertTrue(item["show"], item["id"])
            self.assertGreater(item["runtime_seconds"], 60, item["id"])

    def test_the_builder_validates_the_committed_file(self):
        import subprocess
        import sys

        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "vod_catalog.py"), "--check"],
            capture_output=True, text=True, cwd=str(ROOT),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class Version112Tests(unittest.TestCase):
    def test_every_surface_agrees_on_1_1_2(self):
        current = text(ROOT / "VERSION").strip()
        self.assertTrue(release_version.is_newer(current, "1.1.1"), current)
        gradle = text(ROOT / "android" / "app" / "build.gradle.kts")
        self.assertIn('rootProject.file("version.properties")', gradle)
        self.assertIn(
            "DEFAULT_VERSION = release_version.current_version()",
            text(ROOT / "android" / "tools" / "build_bundle.py"),
        )
        self.assertEqual(
            json.loads(text(ROOT / "macos" / "app" / "package.json"))["version"], current)

    def test_the_version_code_sits_above_every_published_build(self):
        import sys

        sys.path.insert(0, str(ROOT / "scripts"))
        import release_version  # noqa: E402

        self.assertEqual(release_version.android_version_code("1.1.2"), 101_020_000)
        self.assertTrue(release_version.is_newer("1.1.2", "1.1.1"))
        for older in ("1.0.4", "1.0.6.1", "1.0.8", "1.0.8.1", "1.0.9", "1.1.0", "1.1.1"):
            self.assertGreater(
                release_version.android_version_code("1.1.2"),
                release_version.android_version_code(older),
                older,
            )

    def test_the_notice_covers_every_build_below_1_1_2(self):
        document = json.loads(text(ROOT / "app-update-notice.json"))
        rules = {rule["id"]: rule for rule in document["rules"]}
        stable = rules["update-below-newest"]
        self.assertEqual((stable["min_version"], stable["max_version"]), ("1.0.4", "1.1.1"))
        self.assertIn("1.1.2", stable["surprise"])
        self.assertNotIn("retired-preview-1-1", rules)

    def test_the_download_site_no_longer_retires_a_stable_tag(self):
        site = text(ROOT / "scripts" / "build_site_data.py")
        self.assertIn("RETIRED_TAGS: set[str] = set()", site)

    def test_release_notes_and_changelog_are_present(self):
        notes = text(ROOT / "release-notes-1.1.2.md")
        self.assertIn("PremiumTV 1.1.2", notes)
        self.assertIn("side player", notes.lower())
        self.assertIn("Version 1.1.2", text(ROOT / "CHANGELOG.md"))


if __name__ == "__main__":
    unittest.main()
