# 🎪 PremiumTV 1.0.0 — *The Marquee Release*

The lights are up, the house is open. After four beta spot-checks and one experimental preview, **PremiumTV 1.0.0 — The Marquee Release** is officially live on both stages: Android TV and macOS.

## 📺 A guide for every channel

Every channel deserves an answer to *"what's on?"* — so we wrote the guidebook.

- A **curated registry of 345 XMLTV feeds across 172 countries** (iptv-epg.org per-country guides, epg.pw per-country and one-for-all guides, plus `epg-us.xml`), harvested nightly and verified channel by channel.
- Real listings went from **172 channels → 1,658**, and **10,090 programmes → 99,079** — a 10× marquee for the schedule wall, with zero invented listings.
- Backup feeds inherit their station's schedule (country-aware name matching), so "Nickelodeon (backup)" shows the same verified listings as Nickelodeon — never another country's.
- All **8,460 channel ids** are declared in the guide, and country guides publish per playlist (`EPG/USA.xml`, `EPG/UK.xml`, …). Coverage grows automatically as upstream families publish more `epg-<cc>` files.

## 🔄 Refreshes that just work

The refresh buttons in Settings mean what they say: *Force refresh all now*, *Check now*, *Reset to the bundled copy*.

- Conditional downloads (ETag / Last-Modified), serialized refreshes, atomic swap with a backup rollback on every platform.
- Automatic refresh slots mirror the 13 publishing windows; WiFi-only, battery- and idle-friendly.
- Verified end-to-end by 343 Python tests + 95 subtests and 25 Node tests, and both release builds green in CI.

## 🎬 The Marquee look

New and classic, stage-lit:

- Cinema **gold on midnight** palette, marquee-plaque brand mark and version tag.
- Gold-underlined tabs, **ON-AIR** now badges, lifted channel cards, sweep-on-first-heartbeat, and the gold focus halo on the TV remote.

## 📦 Install

| Platform | Artifact |
|---|---|
| Android TV | `PremiumTV-1.0.0-debug.apk` (side-load; the androidtv build stays in beta) |
| macOS | `PremiumTV-1.0.0-arm64.dmg` / `…-x64.dmg`, `PremiumTV-1.0.0-arm64.pkg` / `…-x64.pkg` |

Checksums live in `SHA256SUMS.txt` on both release pages.

## 🙏 Credits

Marquee-plaque cheers to everyone who filed stream-quality reports and caught the empty-guide rows — the whole house is lit now.

**App pages:** [androidtv](https://github.com/cgyegcvcecvoc/PremiumTV1/tree/main/androidtv) · [macos](https://github.com/cgyegcvcecvoc/PremiumTV1/tree/main/macos)

*Run it on the biggest screen you own.* 🍿
