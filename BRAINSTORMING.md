# Brainstorming future versions

This is the open notebook for PremiumTV ideas. Add a short proposal here before
it becomes a release theme; the release itself still follows the naming and
short-notes rules in [docs/RELEASING.md](docs/RELEASING.md).

## Themes to explore

### Live events
- Which additional verified event sources can fill gaps without adding
  unprobed feeds?
- Can a fixture carry a verified kickoff time from a trusted schedule source,
  instead of always showing `null`?
- How should a refused fixture be reported to users without exposing dead URLs?

### Playback reliability
- Which player failures still need a manual backup-server switch?
- Can recovery policies be shared more completely between Android, macOS and
  the web player?
- What diagnostics would make a feed failure actionable for an operator?

### Data quality
- Which source families should be audited next, and what measurement proves a
  source is worth importing?
- Can the schedule and guide agree on a fixture's identity without guessing
  kickoff times?
- Which generated surfaces still need a drift check?

### Platforms
- What would a useful TV-first layout look like on another platform?
- Which accessibility improvements matter most on a remote-controlled device?
- Is there a safe, opt-in path to surface the existing on-demand catalogue
  again?

## Adding an idea

Write the problem first, then the smallest useful outcome, then how we would
know it worked. Include a measurement or a test where one is possible. Keep
ideas separate from release promises: a proposal here is not scheduled until it
has a release name and a passing implementation.
