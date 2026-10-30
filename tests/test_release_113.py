"""1.1.3: broadcast audio fixes, moving loading bar, expanded VOD + transport player, and version bump."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ANDROID_UI = ROOT / "android/app/src/main/kotlin/com/premiumtv/app/ui"
MACOS_MAIN = ROOT / "macos/app/src/main"
MACOS_RENDERER = ROOT / "macos/app/src/renderer"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class AudioPlaybackFix113Tests(unittest.TestCase):
    def test_android_bundles_ffmpeg_audio_decoder_and_track_fallback(self):
        gradle = text(ROOT / "android/app/build.gradle.kts")
        self.assertIn("org.jellyfin.media3:media3-ffmpeg-decoder:1.3.1+2", gradle)
        self.assertIn("androidx.media3:media3-exoplayer-dash:1.4.1", gradle)
        self.assertIn("isCoreLibraryDesugaringEnabled = true", gradle)
        self.assertIn("com.android.tools:desugar_jdk_libs:2.0.4", gradle)

        player = text(ANDROID_UI / "PlayerScreen.kt")
        self.assertIn("EXTENSION_RENDERER_MODE_ON", player)
        self.assertIn("setEnableDecoderFallback(true)", player)
        self.assertIn("AudioAttributes.Builder()", player)
        self.assertIn("C.USAGE_MEDIA", player)
        self.assertIn("setAllowAudioMixedMimeTypeAdaptiveness(true)", player)
        self.assertIn("FLAG_DETECT_ACCESS_UNITS", player)
        self.assertIn("selectPreferredAudioTrackIndex(", player)
        self.assertIn("isSecondaryAudioLabel(", player)

    def test_macos_proxy_and_player_recover_separated_and_silent_audio(self):
        main_js = text(MACOS_MAIN / "main.js")
        self.assertIn("autoplay-policy", main_js)
        self.assertIn("PlatformHEVCDecoderSupport", main_js)
        self.assertIn("setAudioMuted(false)", main_js)

        proxy_js = text(MACOS_MAIN / "stream-proxy.js")
        self.assertIn("looksLikeExtM3uHead", proxy_js)
        self.assertIn("inferMediaContentType", proxy_js)
        self.assertIn("upstream.url", proxy_js)

        player_js = text(MACOS_RENDERER / "player.js")
        self.assertIn("isAudioCodecSupported", player_js)
        self.assertIn("isSecondaryTrackName", player_js)
        self.assertIn("webkitAudioDecodedByteCount", player_js)
        self.assertIn("silent: true", player_js)


class MovingLoadingBar113Tests(unittest.TestCase):
    def test_macos_and_android_bars_sweep_and_respect_reduced_motion(self):
        css = text(MACOS_RENDERER / "app.css")
        self.assertIn(".splash-bar-sheen", css)
        self.assertIn("@keyframes loading-sweep", css)
        self.assertIn("prefers-reduced-motion: reduce", css)

        components = text(ANDROID_UI / "Components.kt")
        self.assertIn("sweepOffset", components)
        self.assertIn("Brush.horizontalGradient", components)
        self.assertIn("ANIMATOR_DURATION_SCALE", components)


class VodAndTransportPlayer113Tests(unittest.TestCase):
    def test_vod_catalog_has_21_verified_entries_with_backup_streams(self):
        catalog = json.loads(text(ROOT / "playlists/vod/vod-catalog.json"))
        items = catalog["items"]
        self.assertEqual(len(items), 21)
        self.assertEqual(items[0]["id"], "vod-premiumtv-test-card")

        remote_items = [item for item in items if item["id"] != "vod-premiumtv-test-card"]
        self.assertEqual(len(remote_items), 20)
        multi = [item for item in remote_items if isinstance(item.get("streams"), list)]
        self.assertGreaterEqual(len(multi), 10)
        for item in multi:
            self.assertGreaterEqual(len(item["streams"]), 2, item["id"])
            self.assertEqual(item["streams"][0], item["stream"], item["id"])

    def test_both_apps_expose_vod_search_genres_and_player_transport(self):
        app_js = text(MACOS_RENDERER / "app.js")
        index_html = text(MACOS_RENDERER / "index.html")
        self.assertIn('id="player-controls"', index_html)
        self.assertIn('id="player-seek"', index_html)
        self.assertIn('id="player-audio-track"', index_html)
        self.assertIn("vodQuery", app_js)
        self.assertIn("vodGenre", app_js)
        self.assertIn("premiumtv.vod.positions.v1", app_js)

        vod_kt = text(ANDROID_UI / "VodShelf.kt")
        player_kt = text(ANDROID_UI / "PlayerScreen.kt")
        self.assertIn("fun asChannels(): List<Channel>", vod_kt)
        self.assertIn("Search Movies & Shows", vod_kt)
        self.assertIn("SideTransportBar(", player_kt)
        self.assertIn("saveVodPositionMs(", player_kt)


class Version113PlumbingTests(unittest.TestCase):
    def test_version_113_is_synced_across_all_surfaces(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        self.assertEqual(release_version.current_version(), "1.1.3")
        self.assertEqual(release_version.android_version_code("1.1.3"), 101_030_000)
        self.assertEqual(version_sync.check(), [])

        notice = json.loads(text(ROOT / "app-update-notice.json"))
        rules = {rule["id"]: rule for rule in notice["rules"]}
        self.assertEqual(rules["update-below-newest"]["max_version"], "1.1.2")
        self.assertIn("1.1.3", rules["update-below-newest"]["surprise"])

        notes = text(ROOT / "release-notes-1.1.3.md")
        self.assertIn("PremiumTV 1.1.3", notes)
        self.assertIn("Version 1.1.3", text(ROOT / "CHANGELOG.md"))


if __name__ == "__main__":
    unittest.main()
