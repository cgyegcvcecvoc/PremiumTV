# PremiumTV 1.0.8.2 — Bridge for 1.0.8.1 (stranded updater)

> **One-time bridge.** If you are on **1.0.8.1 (1.0.8 V1 Patch)**, Settings → App updates wrongly says “up to date” because that build still thinks **1.0.9** is another name for itself. **1.0.8.2 fixes that lie** — it is the same crash-on-watch fix as 1.0.9, published under a version your updater *can* see. Install it once, then 1.0.9 appears automatically.

**What is in it:** identical application code to **1.0.9** — the crash-on-watch fix (one ExoPlayer per screen, surface rebind, lifecycle pause) and the six healed Mac controls. The only difference is the number on the box: Android `1.0.8.2` (`versionCode 100080002`), Mac `1.0.9` alias (macOS requires three parts). It installs straight over 1.0.8.1 and keeps favorites/settings.

**Who should use it:**
- **On 1.0.8.1?** Use this release: Settings → App updates will now offer **1.0.8.2**. Install it, then Settings will immediately offer **1.0.9** — one more tap finishes you on the newest stable. Or install `PremiumTV-1.0.9-debug.apk` by hand from the 1.0.9 release; both paths land on the same fixed code.
- **On 1.0.8?** You don't need this — Settings already offers **1.0.9** directly.
- **On 1.0.9?** You are already on the fix; this release is behind you and will never be offered.

**Why a bridge exists:** 1.0.8.1's frozen `COMPATIBILITY_ALIASES` table lists `1.0.9 → 1.0.8.1` (the old V-patch alias). Until that device leaves 1.0.8.1, no `1.0.9` can be seen as newer. `1.0.8.2` is *not* in that table, so it *is* seen as newer, and it carries the fix. After you leave 1.0.8.1, the alias is dead and 1.0.9 is the normal path forever — there will be no further `1.0.8.x`.

**No other changes:** same USA lineup + USA guide (`playlists/live/USA.m3u` + `EPG/USA.xml`), same animated loading screen and 11-check diagnostics as 1.0.9. V patches remain retired after this one-time bridge.

