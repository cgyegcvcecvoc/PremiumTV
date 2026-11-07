# PremiumTV 1.1.5 — remote-first speed, a calmer start, and a sleep timer (stable)

Prepared 2026-11-06. Android `1.1.5` / `versionCode 101050000`, macOS `1.1.5`.

It installs straight over 1.1.4, 1.1.3 and every earlier build — no uninstall
needed — and Settings → App updates offers it to every build below it. The
channel list, the guide and the update policy are unchanged.

## A remote that keeps up

- **Focus motion no longer recomposes the card.** The 3% lift on a focused
  channel or event card is now applied in the graphics layer and read in the
  draw phase, with a 110 ms tween. Before, every animation frame recomposed the
  card and its logo while the D-pad moved across a row — the largest avoidable
  cost in TV browsing, and the reason focus could trail the remote on a Fire TV
  stick or an older Android TV box.
- **One focus stop per channel card.** The tiny favourite star inside every card
  used to be a second focusable target, so ▼ from a card stopped on that card's
  star before it reached the next row. The star is now a touch-only control and
  a remote favourites a channel by **holding OK** on it. The side player keeps
  its own ★ button.
- **Focus groups keep the D-pad in the shelf.** The category rail, the channel
  grid, the tab row and each Live Events row are focus groups, so traversal
  stays inside the section you are browsing instead of escaping into the next
  one when you reach its edge.
- **A pointer that matches its shape.** The amber outline is drawn from the
  control's own shape, inside its bounds, with a dark under-stroke. A 22 dp tab
  pill no longer gets a visibly cut 15 dp ring, and the selected tab darkens
  while focused so "selected" and "you are here" are different states.
- **The guide coalesces key auto-repeat.** Holding ◀/▶ used to launch one scroll
  coroutine per repeat event, which queued faster than the grid could move. Only
  one reveal job runs now, and repeats are folded into at most one cursor move
  per 90 ms. The grid still moves continuously, but the highlight stays with the
  remote.
- Select/centre keys are handled on both down and up: a long press is tracked
  explicitly, a release fires once, and a focus move cancels the pending press.

## Less work while you watch

- **The live player no longer polls its clock twice a second.** A live channel
  has no position to display; the 500 ms loop existed only for the VOD transport
  bar and resume position, and it now runs only for on-demand items. Watching a
  live programme costs one listener callback instead of 7,200 UI wake-ups an hour.
- **Live Events ticks once a second only when a countdown is on screen.** Its
  sorted section list rebuilds once a minute instead of 60 times a minute.
- **The Guide tab no longer remaps every channel once a minute.** The synthetic
  live-event rows are built once per library and reused; only the visible
  current/next/progress text updates with the clock.
- **The loading screen's sheen is drawn, not recomposed.** Real load progress is
  kept; the fake trickle and the rotating tips are gone.
- **Memoised personal shelves.** Recently watched and Favorites are resolved once
  per library or key change rather than on every recomposition.
- **A bounded logo cache.** Coil's memory cache is capped at 10% of the app heap
  (it followed `largeHeap` before), so a long browse keeps logos warm without
  competing with the guide and player.

## A cleaner, faster start

- The startup screen is now one calm composition: the drawn marquee mark, the
  wordmark and motto, a determinate gold bar driven only by the loader's real
  stages (15% → 60% → 100%), the current stage, and one version credit. The
  rotating tip, the invented progress trickle and the second slogan line are
  gone, and the sheen only invalidates the bar.
- The browser respects the system safe area on a phone or tablet, so the header
  no longer sits under the status bar. TV layouts are unchanged (their insets are
  zero), and the player stays full-bleed.
- Settings rows stack their label and value on a narrow window instead of
  squeezing the value into a fixed 190 dp column.
- In the narrow channel browser, the category heading and sort control stack
  above the rail, keeping category names visible instead of wrapping the heading
  into a tall column that pushed the list off-screen.

## New: Sleep timer

Settings → **Sleep timer** now offers **Off**, **30 min**, **60 min** and
**90 min**. The deadline is a wall-clock value stored on the device, so it
survives a refresh, a docked flip or an app restart; when it arrives the player
closes and the browser shows a short "Sleep timer ended — playback stopped"
banner. A TV left on overnight no longer plays until morning.

## Platform notes

- **Android TV / Google TV / Fire TV / tablet / phone:** all of the above.
- **macOS:** carries version `1.1.5` with no functional changes in this release;
  the Mac updater, side player and guide are unchanged from 1.1.4.

The Android APK and both Mac architectures are built and smoke-gated by the
release workflows; the APK is signed with the pinned update key and installs in
place. Unit tests cover the sleep-timer policy, audio-track selection, guides,
server fallback and the repository, and the offline Python suite covers version
sync, canonical update links and the source-level UI contracts.
