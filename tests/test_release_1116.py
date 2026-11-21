"""1.1.16 contracts: the release whose installers build.

1.1.14 failed the Android bundle gate (guide drift), 1.1.15 failed in
``compileDebugKotlin`` (the crash card's ``@Composable`` annotation landed on the
wrong function), and the publish queue could tag a version at a commit that was
not the one that version came from. The offline suite could not see any of the
three, so this pins them.
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


class Version1116Tests(unittest.TestCase):
    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        self.assertEqual(release_version.current_version(), "1.1.16")
        self.assertEqual(release_version.android_version_code("1.1.16"), 101_160_000)
        self.assertEqual(version_sync.check(), [])
        self.assertEqual(version_sync.PUBLISHED_VERSION, "1.1.16")

        notes = text("release-notes-1.1.16.md")
        self.assertIn("# PremiumTV 1.1.16 — Crash diagnostics and hardened sources", notes)
        self.assertIn("versionCode `101160000`", notes)

    def test_settings_composables_keep_their_annotation(self):
        """The 1.1.15 failure: an annotation above the wrong declaration."""
        screen = text("android/app/src/main/kotlin/com/premiumtv/app/ui/HomeScreen.kt")
        for name in ("CrashLogCard", "DiagnosticsCard"):
            marker = f"private fun {name}("
            self.assertIn(marker, screen)
            before = screen[: screen.index(marker)].rstrip()
            self.assertTrue(
                before.endswith("@Composable"),
                f"{name} must be the declaration its @Composable annotation applies to",
            )


class PublishQueueTests(unittest.TestCase):
    def test_a_queued_publish_checks_out_its_own_commit(self):
        """Concurrency parks runs, so a run must not re-read main's VERSION.

        Tagging main's newest version at an older ``GITHUB_SHA`` publishes a
        release whose APK was never built from that commit (the 1.1.14/1.1.15
        asset-less chain).
        """
        workflow = text(".github/workflows/publish-release.yml")
        self.assertIn("ref: ${{ github.sha }}", workflow)
        self.assertNotIn("ref: main\n", workflow)
        self.assertIn('--target "$GITHUB_SHA"', workflow)


class GuideStillMatchesPlaylistTests(unittest.TestCase):
    def test_the_usa_guide_only_lists_playlist_channels(self):
        channels, _ = build_bundle.parse_m3u(str(ROOT / "playlists" / "live" / "USA.m3u"))
        programmes = build_bundle.parse_xmltv(str(ROOT / "EPG" / "USA.xml"))
        known = {channel["id"] for channel in channels if channel["id"]}
        self.assertTrue(programmes, "the USA guide must carry listings")
        self.assertEqual({programme["c"] for programme in programmes} - known, set())


if __name__ == "__main__":
    unittest.main()
