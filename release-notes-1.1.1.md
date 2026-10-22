# PremiumTV 1.1.1 — Live Events crests and countdowns, Movies & Shows (stable)

Published 2026-10-22. Android `1.1.1` / `versionCode 101010000`, macOS `1.1.1`.

It installs straight over 1.1.0 (and every earlier build) on both platforms — no uninstall needed. The retired 1.1.x preview carried this same name; now that 1.1.1 is the stable release, the old "preview retired" notice rule was removed from `app-update-notice.json`, and Settings → App updates offers 1.1.1 to every build below it.

## Live Events

- **Official team crests.** Every team name on the Live Events tab is now paired with its official club crest next to its name, on both Android and Mac. Teams the app doesn't yet have a crest for keep the drawn badge they had before.
- **"Not live yet" with a countdown.** Games the scrapers have listed but that haven't kicked off stay on the tab instead of disappearing: they show a "Not live yet" pill and a live countdown ("Kickoff in 2h 04m 12s") ticking down to the scheduled start. Once kickoff passes the pill becomes "NO SIGNAL" until a feed answers, then "LIVE".
- **One card per game.** The same game published under two or three feeds ("… vs. … 1", "… vs. … 2") now shows as one matchup with every feed as a backup, so the tab no longer lists one game twice.

## Movies & Shows (coming soon)

- New **Movies & Shows** tab on both platforms opening a polished coming-soon page for the on-demand section that lands in a future release. Your channels and the guide are unchanged.

## Under the hood

- The Live Events tab refreshes and re-checks feeds faster, and the countdown ticker runs only while the tab is open.
- Release plumbing: version `1.1.1` / Android `versionCode 101010000` everywhere, with the matching GitHub release tag `v1.1.1`.

See [`CHANGELOG.md`](CHANGELOG.md) for the full history and [`docs/UPDATES.md`](docs/UPDATES.md) for how the in-app updater delivers this release.
