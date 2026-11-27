# Source hunt — 2026-11-27 (live events, and the mirrors that are not mirrors)

## Why this pass

The 2026-11-25 audit ended with two follow-ups: prune the weakest configured
sources, and find better coverage for live events. This pass measured the one
thing live events were missing — a second address per fixture — and checked the
backup addresses the existing sources advertise.

## The live-events gap

`playlists/checks/live-event-reliability.json` on 2026-11-26 showed **4 published
fixtures, 0 meeting the two-primaries-plus-backup policy**. Every published event
entry came from `doms9`'s combined playlist, and only one feed per fixture had
survived the link check. The other configured sources publish no event entries at
all on that run.

`doms9/iptv` also publishes `M3U8/events.m3u8`, the live-events half of the same
hourly project, which this repository was not importing.

| Measurement (2026-11-27) | `M3U8/events.m3u8` |
|---|---:|
| Entries | 381 |
| Unique URLs | 380 |
| URLs not in `PremiumTV.m3u` | 378 |
| URLs new to `PremiumTV_all.m3u` | 376 |
| Entries parsed into fixtures | 335 |
| Distinct fixtures | 176 |
| Fixtures with more than one feed | 48 |

That is the difference between a card that has one server and a card that can
fail over. It is now configured as **`doms9-events`**, with GitLab's
byte-identical copy (SHA-256 verified) as its backup address.

**Codeberg is not configured.** The project advertises a Codeberg mirror, but on
2026-11-27 that copy held **205 of the 381 entries**, so treating it as identical
would have silently shortened the live-events set on any run that fell back to
it.

## The existing source's mirrors

`doms9` gains the verified GitLab copy of `TV.m3u8` alongside its jsDelivr and
raw.gitmirror.com addresses. The GitHub file and the GitLab file are the same
bytes; the Codeberg copy is not used for the reason above.

## The candidate that was not promoted

`felixiptv/streams` (ZeroStreams) publishes a validated live HLS playlist with
clean event titles and alternate feeds. Measured the same day: **51 entries, 51
unique URLs, all 51 new to this corpus** — mostly motorsport, baseball and
basketball. Its `status.json` was last written **2026-10-19**, so the repository's
"refreshed every 15 minutes" claim is not proven by its own status file. It is
therefore a **monthly discovery candidate**, not a configured source: the
discovery engine sample-checks it and nothing is promoted unless the links
answer.

## What changed

- `sources.json` — `doms9-events` (GitHub primary, GitLab mirror, measurement in
  the note); `doms9` gains its GitLab mirror; `felixiptv/streams` joins
  `discovery.candidates`.
- `docs/data/releases.src.json` — refreshed from GitHub's release API (the
  release-page fix this pass shipped with).
- No playlist was edited by hand. The next checked scrape imports the new
  source, verifies every link, and republishes the event cards with whatever
  actually answers.

## What this does not claim

The numbers above are a source-side measurement, not a playback test. The scrape
that follows re-checks every URL like any other source, and the reliability audit
will keep reporting a deficit for any fixture that still has only one confirmed
feed rather than padding it with a duplicate.
