# PremiumTV 1.0.6 — Click-to-Search, Your Shelves, Server Switching

**PremiumTV 1.0.6 is the stable release and the default download.** It is
above 1.0.5, so 1.0.4+ installs are offered it from **Settings → App updates**:
downloaded once, verified against the release's SHA-256, installed in place.
Android `versionCode 100000006` (derived by `scripts/release_version.py`).

## Search only when you click it

Hovering over the search bar — or D-pad focus passing over it on a TV — used
to put it straight into search mode. Fixed on both platforms:

- **macOS:** the search field ships read-only. A click (or `/`, or Enter on
  the focused field) activates it; Escape/blur deactivates it. Hovering does
  nothing, and typing is debounced (150 ms) so results don't rebuild per key.
- **Android TV:** focus only highlights the field ("Click OK to search
  channels…"). OK/click opens editing and the keyboard; the IME Search action
  closes it again.

## Switch servers yourself on live events

Automatic multi-server fallback (1.0.5) still walks to the next feed when one
dies — but now you don't have to wait for it to give up. The player shows
**◀ Server / Server ▶** buttons that jump between a live game's streams (or a
channel's backup feeds), wrapping around the list, with the badge confirming
"Server N of M · selected by you". New streams start from the server you picked.

## Recently watched + Favorites

- **Recently watched** — every channel you open is filed here, newest first
  (up to 30, on-device only). It leads the Channels tab / sidebar, so you can
  jump straight back in and keep watching.
- **Favorites** — press **☆ Favorite** in the player (or the ☆ on a channel
  card on Android) and the channel lives on your Favorites shelf. Press again
  to remove it. Both shelves survive restarts; channels that leave the
  playlist drop off automatically.

## Smoother clicking around

- macOS: the 30-second clock no longer rebuilds the whole channel grid under
  your cursor; scroll paging is coalesced through `requestAnimationFrame`
  instead of filtering the full library per scroll event; off-screen cards
  use `content-visibility`, and the hover lift (transform + shadow repaint)
  is gone.
- Android: the focus zoom on channel cards is gentler (1.03× instead of
  1.06×), so moving across a row animates less layout on TV hardware.

## Also carried in the 1.1.1 Encore Preview

The 1.1.1 pre-release is rebuilt from this same tree: everything above, on
top of its global lineup and cable-style Guide. It stays a pre-release —
never the default download, never offered to stable installs.

## Downloads

- Android: `PremiumTV-1.0.6-debug.apk` (`versionCode 100000006`), signed with
  the long-lived update key; installs over 1.0.5/1.0.4 in place.
- Mac Apple Silicon / Intel: `PremiumTV-1.0.6-mac-arm64` / `-mac-x64` `.dmg` / `.pkg`
  (ad-hoc signed, not notarized; first launch right-click → Open).
- Checksums: `SHA256SUMS-android.txt` and `SHA256SUMS-macos.txt` on the release.
