package com.premiumtv.app.ui

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/**
 * The Spotify tab's packaged shell (1.1.25).
 *
 * This is not a UI test: a WebView needs a device. It checks the two things a
 * packaging mistake would break silently, on a TV nobody can debug easily -
 * that the shell exists inside the APK with a module beside it, and that the
 * shell does not quietly widen what the WebView may do.
 *
 * The important assertion is the last group: the tab's whole licence to exist is
 * that it *is* Spotify's player. If a later change adds ad-filtering, script
 * injection or a proxy, that is a product decision that must fail a test rather
 * than ship to televisions.
 */
class SpotifyScreenTest {
    private val assets = File("src/main/assets/premiumtv")

    @Test
    fun `the tv shell ships with the shared module beside it`() {
        val shell = File(assets, "index.html")
        val module = File(assets, "spotify.js")
        assertTrue("the Spotify shell must be packaged at ${shell.path}", shell.isFile)
        assertTrue("the Spotify module must be packaged at ${module.path}", module.isFile)
        val html = shell.readText()
        assertTrue("the shell must load the module", html.contains("src=\"spotify.js\""))
        assertTrue(
            "the shell must be explicit that playback is Spotify's",
            html.contains("does not block, mute or skip"),
        )
    }

    @Test
    fun `the packaged module is the shared implementation, not a fork`() {
        // scripts/sync_spotify_assets.py --check is the hard gate in CI; this is
        // the local equivalent, so a drift fails `gradlew test` first.
        val packaged = File(assets, "spotify.js").readBytes()
        val shared = File("../../macos/app/src/renderer/spotify.js").readBytes()
        assertEquals(
            "android/app/src/main/assets/premiumtv/spotify.js is a copy; " +
                "run `python scripts/sync_spotify_assets.py`",
            shared.toList(),
            packaged.toList(),
        )
    }

    @Test
    fun `the shell only trusts spotify and its own assets`() {
        val html = File(assets, "index.html").readText()
        val csp = Regex("Content-Security-Policy\"\\s*\\n?\\s*content=\"([^\"]+)\"")
            .find(html)
            ?.groupValues
            ?.get(1)
            ?: ""
        assertTrue("the shell needs a CSP", csp.isNotEmpty())
        assertTrue("scripts are self plus Spotify's SDK", csp.contains("script-src 'self' https://sdk.scdn.co"))
        assertTrue("frames are Spotify's embed only", csp.contains("frame-src https://open.spotify.com"))
        assertFalse("no inline script may run", csp.contains("script-src 'unsafe-inline'"))
        assertTrue("objects stay disabled", csp.contains("object-src 'none'"))
    }

    @Test
    fun `the tab does not filter or rewrite spotify's traffic`() {
        val screen = File("src/main/kotlin/com/premiumtv/app/ui/SpotifyScreen.kt").readText()
        // Spotify's ad hosts must never be named: this class has no business
        // knowing them, and naming one is the first step to blocking it.
        for (forbidden in listOf(
            "ads-feed", "adstudio", "spclient", "audio-ak",
            "evaluateJavascript", "addJavascriptInterface",
        )) {
            assertFalse(
                "the Spotify screen must not reference $forbidden",
                screen.contains(forbidden, ignoreCase = true),
            )
        }
        // The one script injection point that would let the app alter Spotify's
        // page is absent by design.
        assertFalse(
            "no script may be injected into Spotify's document",
            screen.contains("loadUrl(\"javascript:"),
        )
    }

    @Test
    fun `leaving the tab tears the web view down`() {
        val screen = File("src/main/kotlin/com/premiumtv/app/ui/SpotifyScreen.kt").readText()
        assertTrue(screen.contains("DisposableEffect"))
        assertTrue("the player must not outlive the tab", screen.contains("view.destroy()"))
        assertTrue("no file access is granted", screen.contains("allowFileAccess = false"))
        assertTrue("no content access is granted", screen.contains("allowContentAccess = false"))
    }
}
