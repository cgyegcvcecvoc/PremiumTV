# PremiumTV1 XMLTV guides

This repository-root `EPG/` directory is separate from `playlists/` and is the stable publication
location for all generated XMLTV files. The guide builder updates these outputs from the currently
verified upstream EPG feeds and the channel IDs in the published M3U files.

## All-library guide

- Plain XMLTV: [`PremiumTV.xml`](PremiumTV.xml)
- Gzip copy: [`PremiumTV.xml.gz`](PremiumTV.xml.gz)
- Raw URL: `https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/EPG/PremiumTV.xml`

## Country guides

Each current `playlists/countries/<Country>.m3u` has a matching `<Country>.xml` here. The country
playlist's `x-tvg-url` points to its country-scoped guide, so players load the guide for only those
channels. For example:

- USA: [`USA.xml`](USA.xml)
- UK: [`UK.xml`](UK.xml)
- Canada: [`Canada.xml`](Canada.xml)

The full country playlist/EPG URL index is maintained in
[`playlists/countries/README.md`](../playlists/countries/README.md). Country XMLTV files declare the
playlist's channels even when a public listings source has no schedule for them; programme data is
included only when a verified upstream guide matches the channel. Local affiliates require a
station-specific match—generic network schedules are not copied to a local station.

All generated files use XMLTV `<tv>`, `<channel>` and `<programme>` elements with XML-safe text and
explicit UTC offsets. Published playlists assign stable repository-scoped `tvg-id` values to any
channel whose source has no ID, which lets the guide declare it without altering normalized source
caches. An ID does not imply programme coverage: listings are emitted only for verified, safe
matches. If upstream feeds are temporarily unreachable, country outputs can reuse the last successful
verified merged guide for up to 36 hours; with no recent verified cache, they remain channel-only.
Build status, source verification, coverage and per-country XML validation are reported in
[`playlists/checks/EPG-BUILD.md`](../playlists/checks/EPG-BUILD.md).
