"""1.1.4: full-screen player decluttered (bottom overlay buttons removed) and patch version bump."""

from __future__ import annotations

import json
import re
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


class Version114PlumbingTests(unittest.TestCase):
    def test_version_114_is_synced_across_all_surfaces(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        # 1.1.4 is historical now; its note, code and changelog entry stay
        # accurate while the current version moves on.
        self.assertEqual(release_version.android_version_code("1.1.4"), 101_040_000)
        self.assertEqual(version_sync.check(), [])

        notice = json.loads(text(ROOT / "app-update-notice.json"))
        rules = {rule["id"]: rule for rule in notice["rules"]}
        self.assertGreaterEqual(
            release_version.compare_versions(rules["update-below-newest"]["max_version"], "1.1.4"), 0
        )

        notes = text(ROOT / "release-notes-1.1.4.md")
        self.assertIn("PremiumTV 1.1.4", notes)
        self.assertIn("Version 1.1.4", text(ROOT / "CHANGELOG.md"))


class FullScreenDeclutter114Tests(unittest.TestCase):
    """The 1.1.4 removals must not leave dangling references behind.

    The bottom-button removal touched a composable signature, its call site
    and the emulator smoke gate at once; each of the three shipped broken in
    the first 1.1.4 cut (a stray argument that fails compilation, a gate
    marker that matches nothing on screen). These tests pin the three back
    together so a future declutter cannot split them again.
    """

    def test_big_screen_chrome_call_matches_its_signature(self):
        player = text(ROOT / "android/app/src/main/kotlin/com/premiumtv/app/ui/PlayerScreen.kt")

        decl = player.split("private fun BoxScope.BigScreenChrome(", 1)[1]
        params_block = decl.split(") {", 1)[0]
        param_names = set(re.findall(r"(?m)^\s*(\w+)\s*:", params_block))
        self.assertGreater(len(param_names), 5, "the signature scan must see the parameters")

        match = re.search(r"(?m)^\s*BigScreenChrome\($", player)
        self.assertIsNotNone(match, "the BigScreenChrome call site is gone")
        arg_names = set()
        depth = 0
        for line in player[match.end():].splitlines():
            stripped = line.strip()
            if stripped == ")":
                break
            if depth == 0:
                arg = re.match(r"(\w+)\s*=", stripped)
                if arg:
                    arg_names.add(arg.group(1))
            depth += stripped.count("{") - stripped.count("}")
        self.assertTrue(arg_names, "the call-site scan must see the arguments")
        self.assertEqual(arg_names - param_names, set(),
                         f"call site passes undeclared arguments: {sorted(arg_names - param_names)}")

        removed = {"isFavorite", "onToggleFavorite", "onHopServer", "onMinimize"}
        self.assertEqual(arg_names & removed, set(),
                         "the call site still passes removed bottom-button wiring")
        self.assertEqual(param_names & removed, set(),
                         "the signature still declares removed bottom-button wiring")

    def test_removed_full_screen_buttons_are_gone_but_the_dock_keeps_its(self):
        player = text(ROOT / "android/app/src/main/kotlin/com/premiumtv/app/ui/PlayerScreen.kt")
        self.assertNotIn("⤢ Side player", player)
        self.assertNotIn("☆ Favorite", player)
        # The dock (and the smoke gate that drives it) still needs these.
        self.assertIn("⤢ Big screen", player)
        self.assertIn("✕ Close", player)
        self.assertIn("Server ▶", player)

    def test_smoke_gate_markers_resolve_to_text_the_player_composes(self):
        player = text(ROOT / "android/app/src/main/kotlin/com/premiumtv/app/ui/PlayerScreen.kt")
        gate = text(ROOT / "android/tools/smoke_apk.py")
        for marker in ("side_card_marker", "big_screen_marker"):
            chunk = gate.split(f"def {marker}(", 1)[1]
            body = chunk.split("\ndef ", 1)[0]
            returns = [line for line in body.splitlines() if "return next(" in line]
            self.assertTrue(returns, f"{marker} has no marker lookup to check")
            literals = re.findall(r'"([^"]+)"', returns[0])
            self.assertTrue(literals, f"{marker} has no marker text to check")
            self.assertTrue(any(literal in player for literal in literals),
                            f"{marker} matches no text in PlayerScreen.kt: {literals}")

    def test_114_is_documented_as_an_android_only_player_change(self):
        # macOS kept its below-the-picture action bar (mouse-clickable, never
        # covering the stream), so no 1.1.4 copy may claim both apps changed.
        readme = text(ROOT / "docs/README.md")
        paragraph = next(line for line in readme.splitlines() if line.startswith("1.1.4 declutters"))
        self.assertNotIn("both platforms", paragraph)
        self.assertIn("Android TV", paragraph)


if __name__ == "__main__":
    unittest.main()
