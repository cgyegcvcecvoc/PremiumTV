"""The Spotify tab's packaging contracts, checked without a device.

`SpotifyScreenTest` covers the same ground under Gradle, but the Android unit
tests only run in one CI job and a television is a hard place to debug. This
suite runs with the rest of the offline checks, so a packaging slip - a shell
that lost its module, a copy that drifted from the shared source, a CSP widened
to make something work - fails before an APK is built.

It also pins the product boundary in the packaged files, which is the part most
likely to be "improved" later: this tab is Spotify's player, so it does not
filter, mute or skip Spotify's advertising, and nothing in the app pretends to.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

ASSETS = ROOT / "android" / "app" / "src" / "main" / "assets" / "premiumtv"
SHARED = ROOT / "macos" / "app" / "src" / "renderer" / "spotify.js"
SHELL = ASSETS / "index.html"
SCREEN = ROOT / "android" / "app" / "src" / "main" / "kotlin" / "com" / "premiumtv" / "app" / "ui" / "SpotifyScreen.kt"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SpotifyPackagingTests(unittest.TestCase):
    def test_the_tv_shell_ships_with_the_module_beside_it(self):
        self.assertTrue(SHELL.is_file(), "the TV shell must be packaged")
        self.assertTrue(SHARED.is_file(), "the shared module is the only source")
        html = SHELL.read_text(encoding="utf-8")
        self.assertIn('src="spotify.js"', html)

    def test_the_packaged_module_is_the_shared_implementation(self):
        # The script is the authority (it writes the file and the Android
        # workflow runs --check); this is the same comparison, earlier.
        self.assertEqual(
            digest(SHARED), digest(ASSETS / "spotify.js"),
            "run `python scripts/sync_spotify_assets.py`",
        )

    def test_the_sync_script_detects_drift(self):
        import sync_spotify_assets

        self.assertEqual(sync_spotify_assets.main(["--check"]), 0)

    def test_the_shell_states_the_ad_boundary_without_javascript(self):
        # It has to survive a module that failed to load, so it is static text.
        html = SHELL.read_text(encoding="utf-8")
        notice = re.search(r'<p class="notice"[^>]*>(.*?)</p>', html, re.S)
        self.assertIsNotNone(notice, "the shell needs a static notice")
        text = " ".join(notice.group(1).split())
        for sentence in ("Free", "ads", "Premium", "does not block, mute or skip"):
            self.assertIn(sentence, text)
        self.assertNotIn("ad-free", text.lower())
        self.assertNotRegex(text.lower(), r"block(s|ing)? (the )?ads")

    def test_the_shell_only_trusts_spotify_and_its_own_assets(self):
        html = SHELL.read_text(encoding="utf-8")
        csp = re.search(r'Content-Security-Policy"\s*\n?\s*content="([^"]+)"', html)
        self.assertIsNotNone(csp, "the shell needs a CSP")
        policy = csp.group(1)
        self.assertIn("script-src 'self' https://sdk.scdn.co", policy)
        self.assertIn("frame-src https://open.spotify.com", policy)
        self.assertNotIn("script-src 'unsafe-inline'", policy)
        self.assertNotIn("'unsafe-eval'", policy)
        self.assertIn("object-src 'none'", policy)
        self.assertIn("form-action 'none'", policy)


class SpotifyScreenSourceTests(unittest.TestCase):
    def setUp(self):
        self.source = SCREEN.read_text(encoding="utf-8")

    def test_the_web_view_is_served_from_a_secure_asset_origin(self):
        # A file:// page is not a secure context, so PKCE's Web Crypto and
        # localStorage are unavailable there. WebViewAssetLoader gives the shell
        # an https origin without granting filesystem access.
        self.assertIn("WebViewAssetLoader", self.source)
        self.assertIn("https://appassets.androidplatform.net/assets/premiumtv/index.html", self.source)
        self.assertIn("allowFileAccess = false", self.source)
        self.assertIn("allowContentAccess = false", self.source)

    def test_navigation_stays_on_spotify(self):
        for host in ("open.spotify.com", "accounts.spotify.com", "sdk.scdn.co", "api.spotify.com"):
            self.assertIn(host, self.source)
        self.assertIn("shouldOverrideUrlLoading", self.source)

    def test_the_tab_does_not_touch_spotifys_audio_or_page(self):
        # No filtering, no rewriting, no injection: the tab's licence to exist is
        # that it is Spotify's own player, unmodified.
        for forbidden in ("ads-feed", "spclient", "audio-ak", "evaluateJavascript",
                          "addJavascriptInterface", 'loadUrl("javascript:'):
            self.assertNotIn(forbidden, self.source, f"the screen must not reference {forbidden}")

    def test_leaving_the_tab_tears_the_player_down(self):
        self.assertIn("DisposableEffect", self.source)
        self.assertIn("view.destroy()", self.source)


class SpotifySharedModuleTests(unittest.TestCase):
    """The module itself, as the other apps load it."""

    def setUp(self):
        self.module = SHARED.read_text(encoding="utf-8")

    def test_playback_is_spotify_s_player_in_both_modes(self):
        self.assertIn("https://open.spotify.com/embed/", self.module)
        self.assertIn("https://sdk.scdn.co/spotify-player.js", self.module)

    def test_sign_in_is_pkce_with_no_secret(self):
        self.assertIn("code_challenge_method', 'S256'", self.module)
        self.assertNotIn("client_secret", self.module)

    def test_the_curated_shelf_holds_real_playlist_ids(self):
        ids = re.findall(r"\{ type: 'playlist', id: '([A-Za-z0-9]+)'", self.module)
        self.assertGreaterEqual(len(ids), 4)
        for playlist_id in ids:
            self.assertRegex(playlist_id, r"^[A-Za-z0-9]{22}$")

    def test_no_ad_evasion_code_exists(self):
        lowered = self.module.lower()
        for forbidden in ("skipad", "blockad", "mutead", "stripad", "removead",
                          "hidead", "adbreak", "adslot", "adbanner"):
            self.assertNotIn(forbidden, lowered, f"must not implement {forbidden}")


class SpotifyEverywhereTests(unittest.TestCase):
    """One tab in each app, and each one wired, not merely present."""

    def test_the_web_build_copies_the_module_and_versions_it(self):
        build = (ROOT / "web" / "tools" / "build.py").read_text(encoding="utf-8")
        self.assertIn('"spotify.js"', build)
        worker = (ROOT / "web" / "src" / "sw.js").read_text(encoding="utf-8")
        self.assertIn('"shared/spotify.js"', worker)

    def test_the_web_page_allows_spotifys_sdk_and_nothing_else(self):
        html = (ROOT / "web" / "src" / "index.html").read_text(encoding="utf-8")
        csp = re.search(r'Content-Security-Policy"\s*\n?\s*content="([^"]+)"', html)
        self.assertIsNotNone(csp)
        self.assertIn("script-src 'self' https://sdk.scdn.co", csp.group(1))
        self.assertNotIn("'unsafe-eval'", csp.group(1))

    def test_the_desktop_renderer_has_a_tab_and_a_session(self):
        html = (ROOT / "macos" / "app" / "src" / "renderer" / "index.html").read_text(encoding="utf-8")
        app = (ROOT / "macos" / "app" / "src" / "renderer" / "app.js").read_text(encoding="utf-8")
        self.assertIn('data-tab="spotify"', html)
        self.assertIn("PremiumSpotify", app)
        self.assertIn("renderSpotify()", app)

    def test_the_android_tab_is_in_the_tab_strip_and_dispatched(self):
        screen = (ROOT / "android" / "app" / "src" / "main" / "kotlin" / "com"
                  / "premiumtv" / "app" / "ui" / "HomeScreen.kt").read_text(encoding="utf-8")
        self.assertIn('Spotify("Spotify")', screen)
        self.assertIn("TabChip(HomeTab.Spotify.label", screen)
        self.assertIn("HomeTab.Spotify -> SpotifyScreen()", screen)


if __name__ == "__main__":
    unittest.main()
