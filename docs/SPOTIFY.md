# Spotify in PremiumTV

Every PremiumTV app — the browser player, macOS, Linux and Android TV — has a
**Spotify** tab. It is a home for audio next to the television: playlists,
albums and podcasts, sign-in once, and playback that keeps running while you
browse channels.

## What it does

| | Web | macOS / Linux | Android TV |
|---|---|---|---|
| Spotify's embed (no account needed) | ✓ | ✓ | ✓ |
| In-app playback (Premium) | ✓ | ✓ | ✓ |
| Your own pasted links | ✓ | ✓ | ✓ |
| Keeps playing while you browse channels | ✓ | ✓ | ✓ |

Two modes, and both are **Spotify's own player**:

- **The embed.** Spotify's iFrame Embed API, in a sandboxed frame. No account,
  no sign-in, works before anything is configured.
- **In-app playback.** Spotify's Web Playback SDK. Spotify creates a device
  called *PremiumTV* and streams to it, so audio continues while you look at the
  guide or open a channel.

## Setting it up (only needed for in-app playback)

The embed works out of the box. In-app playback needs your own Spotify app,
because Spotify issues the tokens:

1. Open the [Spotify developer dashboard](https://developer.spotify.com/dashboard)
   and create an app. It is free to create.
2. Add this exact **Redirect URI** to that app:
   `https://cgyegcvcecvoc.github.io/PremiumTV/spotify-callback`
   (the Spotify tab shows it too, so you can copy it from there).
3. Copy the app's **Client ID** into the Spotify tab and press **Save**.
4. Press **Sign in to Spotify**. The web edition navigates to Spotify; the
   desktop opens your default browser; the TV follows Spotify's own pages in the
   tab. Nothing is typed into a PremiumTV window.

There is no client *secret*, because there is nowhere safe to keep one in an app
anyone can unzip. Sign-in is **Authorization Code + PKCE**: the access token
lives in memory, only the refresh token is saved on the device, and it never
leaves it. PremiumTV runs no server and receives no part of your Spotify account.

## Playing in the app: Premium only, by Spotify's rule

Spotify's Web Playback SDK is available to **Premium** accounts. A Free account
can use the embed and will hear Spotify's ads in it — exactly as it does in
Spotify's own apps. PremiumTV reads the account's product once and says so
plainly instead of showing a button that fails.

## What this tab deliberately does not do

**It does not remove, mute, skip or hide Spotify's advertising, and it does not
unlock Premium playback.** That is a product decision as much as a technical one:

- Spotify's ad-supported tier is what pays the artists and rights holders whose
  music the app plays. Turning it into Premium-tier listening for free is not
  something this repository will build.
- Spotify's Developer Terms require the player to be used as published.
- It would not work anyway. The embed is a cross-origin frame: neither the page
  around it nor the app can read or script what is inside, and the WebView is
  pinned to Spotify's hosts with no script injection and no request rewriting.
  An "ad blocker" here would be a claim with nothing behind it.

So the honest summary is the one printed on the tab: *a Free account hears
Spotify's ads here as it does in Spotify's apps, and a Premium account hears
none — PremiumTV does not block, mute or skip them.*

Three test suites assert that absence, so it cannot be added quietly later:
`web/test/spotify.test.cjs`, `macos/app/test/spotify-desktop.test.js` and
`android/app/src/test/kotlin/com/premiumtv/app/ui/SpotifyScreenTest.kt`.

## One module, four apps

The policy lives in exactly one file:

```
macos/app/src/renderer/spotify.js        ← the only source
├── web/dist/shared/spotify.js           ← copied by web/tools/build.py
├── android/app/src/main/assets/premiumtv/spotify.js  ← written by scripts/sync_spotify_assets.py
└── loaded directly by the macOS/Linux renderer
```

The TV copy is the one that could rot silently, so
`python scripts/sync_spotify_assets.py --check` fails the Android build when it
disagrees, and `gradlew test` fails the same way locally. Run it with no flags
after editing the module.

## Files

| Path | What it is |
|---|---|
| `macos/app/src/renderer/spotify.js` | Link parsing, embed URLs, PKCE, the session, the curated shelf |
| `web/src/app.js` (`renderSpotify`) | The browser tab |
| `macos/app/src/renderer/app.js` (`renderSpotify`) | The desktop tab |
| `macos/app/src/main/main.js` (`SPOTIFY_CALLBACK`) | Catches the sign-in redirect and replays it to the app |
| `android/.../ui/SpotifyScreen.kt` | The TV tab: `WebViewAssetLoader`, navigation allowlist, teardown |
| `android/app/src/main/assets/premiumtv/index.html` | The TV shell |
| `scripts/sync_spotify_assets.py` | Keeps the APK copy identical, and fails the build when it is not |

## Limits worth knowing

- Spotify's editorial playlists rotate their contents; the **ids** are stable,
  which is why the curated set is data rather than a runtime search.
- `https://spotify.link/…` short links cannot be resolved offline, so the tab
  says to open them once and paste the full link instead of guessing.
- The TV needs a reasonably modern Android WebView (a current Google TV, Fire TV
  or Android TV box). An old box with an unmaintained WebView will show its own
  error, and channels still play normally.
- Signing in from a link that carries a stale address bar is rejected: the PKCE
  `state` is compared, so a forged redirect cannot complete a session.
