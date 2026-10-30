# PremiumTV 1.1.3 — moving loading bar, expanded Movies & Shows + transport player, and broadcast audio fixes (stable)

Prepared 2026-10-25. Android `1.1.3` / `versionCode 101030000`, macOS `1.1.3`.

It installs straight over 1.1.2, 1.1.1, 1.1.0 and every earlier build — no
uninstall needed — and Settings → App updates offers it to every build below
it.

## Channel health and a quieter welcome

- `playlists/HEALTH.txt` summarizes the latest scrape, source status and the share of checked links that were reachable. Unverified links remain separate from confirmed failures; a probe is not a playback or signal-quality guarantee.
- The loading screen motto is “Good TV, quietly ready.” on Android and macOS.

## Broadcast audio recovery for silent channels

- **AC-3 / E-AC-3 / DTS / MP2 software decoding on Android.** Many IPTV feeds
  transmit Dolby Digital (`ac-3`), Dolby Digital Plus (`ec-3`), DTS or MPEG-1
  Layer II (`mp2`) audio without an AAC companion. Android TV Stick, emulator
  and non-Dolby devices previously decoded the H.264/HEVC video while silently
  dropping the unsupported audio track. `1.1.3` adds the Media3 FFmpeg audio
  decoder extension (`org.jellyfin.media3:media3-ffmpeg-decoder:1.3.1+2`) with
  `EXTENSION_RENDERER_MODE_ON`, decoder fallback, mixed-MIME audio adaptiveness,
  relaxed capability selection, explicit `AudioAttributes` with audio-focus
  management, and MPEG-TS access-unit detection.
- **Extensionless HLS audio renditions & codec selection on macOS.** The local
  loopback stream proxy now inspects post-redirect URLs, sniffs `#EXTM3U` on
  extensionless `#EXT-X-MEDIA:TYPE=AUDIO` rendition playlists so their `.aac` /
  `.ac3` / `.m4s` segments are whitelisted into the session instead of rejected
  with `403`, and infers missing upstream `Content-Type` headers (`audio/aac`,
  `audio/ac3`, `audio/eac3`, `video/mp4`, `video/mp2t`). `player.js` filters
  HLS variants toward `MediaSource.isTypeSupported(...)` audio codecs, prefers
  primary non-SAP audio tracks, and runs a decoded-audio byte watchdog
  (`webkitAudioDecodedByteCount`) that automatically cycles alternate audio
  renditions, switches HLS variants, or hops to a backup server when a stream
  produces video frames with zero decoded audio.
- **In-player audio track switcher & mute.** Both the docked side player and
  full-screen view now include a **Mute / Unmute** toggle and an **Audio track**
  selector whenever a feed carries multiple audio streams (languages, stereo vs
  surround, or SAP).

## Moving gold loading bar on startup

- **Visible motion while loading.** The startup gold progress bar on both macOS
  and Android now carries a smooth moving highlight sweep on top of the real
  stage-by-stage repository progress (`TvRepository.loadProgress` on Android,
  `setSplashProgress` on macOS), so cold launch and first-run playlist parsing
  always read as responsive rather than frozen.
- **Reduced-motion friendly.** `prefers-reduced-motion: reduce` on macOS and
  the system `ANIMATOR_DURATION_SCALE` check on Android disable the sweep
  cleanly while keeping determinate progress updates.

## Movies & Shows expanded + built-in player transport controls

- **21 verified on-demand items with backup derivatives.** `scripts/vod_catalog.py`
  now curates 20 Internet Archive public-domain films and classic TV episodes
  (plus the bundled 10-second `PremiumTV Test Card` self-check) — 14 movies
  including *Charade*, *The General*, *Steamboat Bill, Jr.*, *Detour*, *D.O.A.*,
  *Suddenly*, *McLintock!*, *The Hitch-Hiker*, *The Little Shop of Horrors*,
  *Night of the Living Dead*, *His Girl Friday*, *Nosferatu*, *Carnival of
  Souls*, and *Plan 9 from Outer Space*, alongside 7 TV episodes from *Sherlock
  Holmes*, *Dragnet*, *The Beverly Hillbillies*, *The Lone Ranger*, *The Dick
  Van Dyke Show*, *One Step Beyond*, and *Bonanza*. Every entry ships ordered
  primary + backup MP4 derivatives (`streams`) so automatic server fallback
  recovers seamlessly if an archive mirror stalls.
- **Search and genre pills.** Movies & Shows now offers instant title/show/plot
  search alongside **All / Movies / TV Shows** and dynamic genre filter pills on
  both platforms.
- **Built-in player transport bar & local resume.** Both apps add a transport
  control bar (`Play / Pause`, `⟲ 10s`, `10s ⟳`, interactive seek scrubber +
  elapsed/total time for VOD, `LIVE` badge for live TV, `Mute`, and `Audio`
  track cycling) that works in the docked side player and full screen alike, and
  automatically remembers and resumes VOD playback positions locally.

## Under the hood

- Country playlist link pruning in `scripts/link_check.py` now exempts tiny
  derived `playlists/countries/*.m3u` files (`<= 5` entries) from the bulk
  truncation guard, removes empty country files cleanly, and keeps
  `playlists/countries/README.md` synchronized automatically.
- Version plumbing: [`VERSION`](VERSION) is `1.1.3` (`versionCode 101030000`),
  `app-update-notice.json` nudges every build up through `1.1.2`, and all
  version surfaces are verified by `scripts/version_sync.py`.

See [`CHANGELOG.md`](CHANGELOG.md) for the full history and
[`docs/UPDATES.md`](docs/UPDATES.md) for how the in-app updater delivers it.
