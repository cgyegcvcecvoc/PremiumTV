package com.premiumtv.app.ui

import android.annotation.SuppressLint
import android.graphics.Bitmap
import android.webkit.WebResourceRequest
import android.webkit.WebResourceResponse
import android.webkit.WebSettings
import android.webkit.WebView
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.webkit.WebViewAssetLoader
import androidx.webkit.WebViewClientCompat

/**
 * Spotify on the television (1.1.25).
 *
 * Why a WebView: Spotify's player is a web player. Their iFrame Embed API and
 * their Web Playback SDK are both browser surfaces, and there is no Android TV
 * SDK for Spotify playback. The alternatives were worse - an intent into the
 * phone-only Spotify app, which a TV does not run, or scraping an audio stream,
 * which their terms forbid and this app will not do. A WebView showing
 * Spotify's own pages is the supported surface.
 *
 * The page it loads is `assets/premiumtv/index.html`, and that page's rules come
 * from `assets/premiumtv/spotify.js`, which is a copy of the desktop renderer's
 * module: the same link parsing, the same embed URLs, the same PKCE flow as the
 * browser, macOS and Linux builds. `scripts/sync_spotify_assets.py` keeps the
 * copy identical and the test suite fails if the two ever drift.
 *
 * The assets are served over `https://appassets.androidplatform.net` by
 * WebViewAssetLoader rather than over `file://`. That matters for three
 * reasons: an https origin is a secure context, so the Web Crypto calls PKCE
 * needs actually exist; localStorage persists, so a signed-in TV stays signed
 * in; and a relative `<script src="spotify.js">` resolves normally against the
 * page's own origin.
 *
 * What this screen does NOT do, and will not be extended to do: block, mute,
 * skip or hide Spotify's advertising, or unlock Premium playback. The WebView
 * loads Spotify's origin and nowhere else, the app injects no script into the
 * document, and no request is rewritten or filtered. Spotify therefore decides
 * what plays and what it costs, and the notice under the player says exactly
 * that. Interfering is also futile by construction: the embed is a cross-origin
 * document that neither this page nor this app can read.
 */
@SuppressLint("SetJavaScriptEnabled")
@Composable
internal fun SpotifyScreen() {
    // The app context is enough for the loader: it reads the APK's assets and
    // holds no Activity, so a rotation or a task switch cannot leak one.
    val context = LocalContext.current.applicationContext
    var error by rememberSaveable { mutableStateOf("") }
    var webView by remember { mutableStateOf<WebView?>(null) }
    // Built once: the loader is the only thing that can hand the WebView a file
    // from the APK, and it serves nothing outside assets/premiumtv.
    val loader = remember(context) {
        WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(context))
            .build()
    }

    DisposableEffect(Unit) {
        onDispose {
            // A live WebView keeps Spotify's player and its audio session running
            // after the tab is left, so it is torn down on the way out.
            webView?.let { view ->
                view.stopLoading()
                view.loadUrl("about:blank")
                view.destroy()
            }
            webView = null
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(horizontal = 28.dp, vertical = 18.dp),
    ) {
        Text(
            text = "Spotify",
            style = MaterialTheme.typography.headlineSmall,
            color = MaterialTheme.colorScheme.onBackground,
        )
        Text(
            text = "Spotify's own player, on this device. Audio keeps running while you browse channels.",
            style = MaterialTheme.typography.labelMedium,
            color = MutedText,
            modifier = Modifier.padding(top = 4.dp),
        )
        Surface(
            modifier = Modifier
                .fillMaxWidth()
                .weight(1f)
                .padding(top = 14.dp),
            shape = RoundedCornerShape(14.dp),
            color = CardBackground,
        ) {
            Box(modifier = Modifier.fillMaxSize()) {
                AndroidView(
                    modifier = Modifier.fillMaxSize(),
                    factory = { ctx ->
                        WebView(ctx).apply {
                            setBackgroundColor(android.graphics.Color.parseColor("#0b0f16"))
                            settings.configureForSpotify()
                            webViewClient = SpotifyClient(loader) { message -> error = message }
                            loadUrl(SHELL_URL)
                            webView = this
                        }
                    },
                    update = { view -> if (webView !== view) webView = view },
                )
                if (error.isNotEmpty()) {
                    Surface(
                        modifier = Modifier
                            .align(Alignment.BottomCenter)
                            .fillMaxWidth()
                            .padding(12.dp),
                        shape = RoundedCornerShape(10.dp),
                        color = MaterialTheme.colorScheme.surfaceVariant,
                    ) {
                        Text(
                            text = error,
                            style = MaterialTheme.typography.labelMedium,
                            color = PremiumGold,
                            modifier = Modifier.padding(12.dp),
                        )
                    }
                }
            }
        }
        // The boundary, where the viewer reads it rather than buried in a policy
        // page, and visible on every visit to the tab.
        Text(
            text = "Playback is Spotify's own player, so Spotify's terms apply: a Free account hears " +
                "Spotify's ads here as it does in Spotify's apps, and a Premium account hears none. " +
                "PremiumTV does not block, mute or skip them.",
            style = MaterialTheme.typography.labelSmall,
            color = MutedText,
            modifier = Modifier.padding(top = 10.dp),
        )
    }
}

/** Where the packaged shell is served from. One constant, used by both sides. */
private const val SHELL_URL =
    "https://appassets.androidplatform.net/assets/premiumtv/index.html"

private fun WebSettings.configureForSpotify() {
    javaScriptEnabled = true
    domStorageEnabled = true // the refresh token and the viewer's own links
    mediaPlaybackRequiresUserGesture = false // opening the tab is the gesture
    loadWithOverviewMode = true
    useWideViewPort = true
    builtInZoomControls = false
    displayZoomControls = false
    // No mixed content: Spotify is https end to end, and a downgrade here would
    // be a hole in an otherwise pinned surface.
    mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
    // Nothing outside the loader's own origin may read this WebView's files, and
    // the WebView may not touch the filesystem itself.
    allowFileAccess = false
    allowContentAccess = false
    // Keep the desktop layout: the TV has the width for Spotify's full player,
    // and the phone-width layout wastes it.
    userAgentString = userAgentString.replace(" Mobile", "")
}

/**
 * Serves the shell from the APK, and keeps navigation inside Spotify.
 *
 * Allowed: the asset loader's own origin (the page and its module), Spotify's
 * embed, its account pages and its SDK. Everything else is refused and reported.
 * That allowlist is what stops an unexpected or hijacked link from turning a
 * television into a general-purpose browser, and it is also why no ad-serving
 * endpoint is special-cased here: there is no filtering in this class at all.
 */
private class SpotifyClient(
    private val loader: WebViewAssetLoader,
    private val onBlocked: (String) -> Unit,
) : WebViewClientCompat() {
    private val allowed = listOf(
        "https://appassets.androidplatform.net/",
        "https://open.spotify.com/",
        "https://accounts.spotify.com/",
        "https://sdk.scdn.co/",
        "https://api.spotify.com/",
    )

    override fun shouldInterceptRequest(
        view: WebView,
        request: WebResourceRequest,
    ): WebResourceResponse? = loader.shouldInterceptRequest(request.url)

    override fun shouldOverrideUrlLoading(
        view: WebView,
        request: WebResourceRequest,
    ): Boolean {
        val url = request.url.toString()
        if (allowed.any { url.startsWith(it) }) return false
        onBlocked("PremiumTV keeps the Spotify tab on Spotify. That link goes elsewhere and was not opened.")
        return true
    }

    override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
        super.onPageStarted(view, url, favicon)
        if (url != null && url != "about:blank" && allowed.none { url.startsWith(it) }) {
            view?.stopLoading()
            onBlocked("Spotify tried to leave its own pages, so PremiumTV stopped it.")
        }
    }
}
