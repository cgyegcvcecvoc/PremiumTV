# PremiumTV 1.0.9 — the crash-on-watch fix (update now)

**If you are on 1.0.8 or 1.0.8.1 (the "1.0.8 V1 Patch"), update to 1.0.9
right away.** Those builds carry a serious player bug: opening a channel can
leave the picture frozen on black — or crash the app outright — especially
when a channel switches to another server. **1.0.9 fixes it.** It is the
current stable and the best working release; nothing is wrong with your TV,
your network or the channels.

1.0.9 briefly existed as a same-code "compatibility" copy of 1.0.8.1. It is
now a real release with the fix, and it replaces that build: the APK reports
**1.0.9** (`versionCode 100090000`, unchanged, so it reinstalls in place),
and this release carries the Android APK and the Mac `.dmg`/`.pkg`.

## What was wrong

- The Android player created and released a whole media player for every
  server a channel tried, while the on-screen video surface stayed attached
  to the first — already released — player. After an automatic server
  fallback, a manual server hop, or a flip between the full-screen and side
  players, the screen showed a dead player: a permanently black or frozen
  picture, and on some devices a crash.
- 1.0.9 keeps **one player per watch screen** and swaps the stream inside
  it, rebinds the video surface on every flip, keeps each server's own
  playback headers, and only releases the player when you leave the screen.
  Playback also pauses when the app is backgrounded and resumes on return
  instead of playing on blind.
- The Mac app never had this defect (its player is a different design), but
  the packaged-app test on both platforms now **opens a channel for real**
  before a build may publish — and that new Mac check caught a different
  1.0.8 bug the day it landed (below).
- **Mac: six controls that never worked now work.** The **⧉ Side player**
  button, the category **Sort** toolbar, the **◀ All categories** back
  button (and the whole category-page toolbar it lives in), the channel
  sort chips and **⟳ Refresh live games** were all wired to elements the
  app never collected, so clicking them did nothing since 1.0.8 shipped
  (keyboard shortcuts still worked, which hid it). All six are wired up in
  1.0.9, with a regression test so a control can never ship uncollected
  again. The Android gate taps a channel, rides the
  automatic server fallback, hops servers by hand, flips the side player
  both ways, and watches a live event end-to-end — the exact taps that used
  to break.

## How to update

- **Settings → App updates** works from every build except 1.0.8.1.
- **On 1.0.8.1 ("1.0.8 V1"):** that build still believes "1.0.9" is another
  name for itself, so its update check can wrongly say you are up to date.
  Install `PremiumTV-1.0.9.apk` from this release by hand — it installs over
  1.0.8.1 and keeps your settings, favorites and categories.
- **Mac:** install the `.dmg` or `.pkg` from this release; it replaces the
  earlier build that was also packaged as 1.0.9.

## Version numbers, simplified

- **The V-patch scheme is retired.** 1.0.8.1 ("V1") was the only V patch
  ever cut. From now on every fix is simply the next version — 1.0.9 today,
  1.0.10 next. No more four-part versions and no more paired
  "compatibility alias" releases. (The historical 1.0.7 → 1.0.6.1 mapping
  stays in the policy so old installs and tags still resolve.)
- Android: `1.0.9` / `versionCode 100090000`. Mac: `1.0.9`.

## ⚠️ Warning on 1.0.8 and 1.0.8.1

Both releases are marked with a crash warning. Android builds 1.0.8–1.0.8.1
show an extreme "update now" popup when the app opens
(`app-update-notice.json`, rule `crash-on-watch-1-0-8`), and their release
pages say the same. If you see that popup, you are on an affected build —
update to this release.
