"""1.1.20 contracts: many sources, one clock.

The request was two things at once, and both are about the same idea - a
single provider of anything is a single point of failure:

* "having many sources so if one goes down we have many backups for
  everything" - a playlist now has backup *addresses* the way a channel has
  backup feeds, the three suggested sites are verified (and, since none of them
  publishes a static playlist, recorded as reference checks rather than
  imported), and two measured sources were added;
* "improve the live events page when it checks time ... build in a clock ...
  using location" - the Live Events tab heads with a ticking clock, and every
  kickoff, countdown and summary on it is read in that clock's zone, starting
  from the location the viewer already gave the local-channels shelf.

Nothing here is a style test: each case fails if the rule the release makes
stops being true.
"""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

APP = "macos/app"
RENDERER = f"{APP}/src/renderer"
ANDROID = "android/app/src/main/kotlin/com/premiumtv/app"

# 2026-11-23 20:00 UTC: New York is EST (GMT-5), Berlin GMT+1, Kolkata GMT+5:30.
AT_MS = 1_795_464_000_000


def text(path: str | Path) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class Version1120Tests(unittest.TestCase):
    """The release number and its notes come from the version tooling."""

    def test_the_release_is_synced_across_every_surface(self):
        import release_version  # noqa: E402
        import version_sync  # noqa: E402

        # 1.1.20 still has to be the version the surfaces were built from, but a
        # later release may already be current (1.1.21 and onward), so the check
        # is "at or above 1.1.20", not "exactly 1.1.20".
        current = release_version.current_version()
        self.assertGreaterEqual(release_version.compare_versions(current, "1.1.20"), 0, current)
        self.assertEqual(release_version.android_version_code("1.1.20"), 101_200_000)
        self.assertEqual(version_sync.check(), [])
        # The published surfaces always describe the current release; what this
        # file pins is that 1.1.20 never disappears from them.
        self.assertGreaterEqual(release_version.compare_versions(
            version_sync.PUBLISHED_VERSION, "1.1.20"), 0)

        notes = text("release-notes-1.1.20.md")
        self.assertIn("# PremiumTV 1.1.20 — ", notes)
        self.assertIn("versionCode `101200000`", notes)

    def test_the_notes_follow_the_short_notes_rule(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "new_version.py"), "--check-notes", "1.1.20"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_the_changelog_records_the_release(self):
        changelog = text("CHANGELOG.md")
        self.assertIn("## 2026-11-23 — Many sources, one clock (1.1.20)", changelog)
        self.assertIn("mirror_templates", changelog)

    def test_the_changelog_records_the_publication(self):
        # docs/RELEASING.md, "After publication": the publication record lives
        # in the changelog and names the tag, so a reader can tell a prepared
        # release from a published one.
        changelog = text("CHANGELOG.md")
        heading = "## 2026-11-23 — Version 1.1.20 published: Many sources, one clock"
        self.assertIn(heading, changelog)
        record = changelog.split(heading, 1)[1].split("\n## ", 1)[0]
        self.assertIn("releases/tag/v1.1.20", record)
        self.assertIn("101200000", record)
        # Every platform's installer is attached, which is what the updater
        # needs before it offers the release.
        for asset in ("APK", "DMG", "AppImage"):
            self.assertIn(asset, record)

    def test_the_site_promotes_the_published_release(self):
        import json  # noqa: E402

        site = json.loads(text("docs/data/site.json"))
        stable = [c for c in site["apps"]["channels"] if c["id"] == "stable"]
        self.assertEqual([channel["tag"] for channel in stable], ["v1.1.20"])
        names = {asset["name"] for asset in stable[0]["assets"]}
        # The Mac installers are the ones recent releases lost entirely.
        for arch, ext in (("arm64", "dmg"), ("x64", "dmg"), ("arm64", "pkg"), ("x64", "pkg")):
            self.assertIn(f"PremiumTV-1.1.20-mac-{arch}.{ext}", names)
        self.assertIn("PremiumTV-1.1.20-debug.apk", names)


class SourceRedundancyWiringTests(unittest.TestCase):
    """The mirror rule is reached by the scrape, and a mirror is never silent."""

    def test_the_scrape_tries_mirrors_and_reports_which_address_answered(self):
        scraper = text("scripts/scraper.py")
        self.assertIn("def source_mirror_urls(", scraper)
        # The mirror attempt happens before the GitHub API fallback, so a dead
        # raw host costs a retry, not the source.
        fetch = scraper.split("def fetch_source_text(", 1)[1].split("\ndef ", 1)[0]
        self.assertLess(
            fetch.index("source_mirror_urls(src, url)"),
            fetch.index("github_api_fallback"),
        )
        self.assertIn("_mirror_url", fetch)
        # And the run report keeps it visible as an issue, not a quiet success.
        self.assertIn("mirror_url", scraper.split("stat[\"fetch_method\"]", 1)[1][:600])

    def test_the_reference_checks_are_audited_not_imported(self):
        config = json.loads(text("sources.json"))
        names = {item["name"] for item in config["reference_checks"]}
        self.assertTrue({"xyzstreams", "ppv.st", "Easy-Web-TV-M3u8"} <= names)
        sources = {source["name"] for source in config["sources"]}
        self.assertFalse({"xyzstreams", "ppv.st", "Easy-Web-TV-M3u8"} & sources)
        for name in ("xyzstreams", "ppv.st", "Easy-Web-TV-M3u8"):
            note = next(item["note"] for item in config["reference_checks"] if item["name"] == name)
            self.assertTrue(note.strip(), name)


class SharedClockRuleTests(unittest.TestCase):
    """Every front end reads kickoff times through one zone, from one rule."""

    def test_the_shared_module_owns_the_zone_rule(self):
        live = text(f"{RENDERER}/live-events.js")
        for needle in (
            "function resolveTimeZone(",
            "function deviceTimeZone(",
            "function zoneOffset(",
            "function clockText(",
            "function kickoffStamp(",
            "function kickoffClockLabel(",
            # Exported, or the apps cannot reach them.
            "resolveTimeZone,\n    deviceTimeZone,\n    zoneOffset,\n    clockText,",
        ):
            self.assertIn(needle, live)
        # A kickoff is formatted in the zone it is given, not only the device's.
        self.assertIn("function kickoffLabel(kickoffMs, timeZone)", live)

    def test_the_widget_is_shared_rather_than_forked(self):
        clock = text(f"{RENDERER}/live-clock.js")
        for needle in (
            "function mount(",
            "function suggestZones(",
            "function bandForLongitude(",
            "function nextKickoff(",
            "function summary(",
            "const STORAGE_KEY = 'premiumtv.live.clockZone';",
        ):
            self.assertIn(needle, clock)
        # The browser build copies it in unchanged, like every shared policy.
        build = text("web/tools/build.py")
        self.assertIn('"live-clock.js"', build)
        self.assertFalse((ROOT / "web/src/live-clock.js").exists(),
                         "the web player must not fork the shared clock")
        self.assertIn('"shared/live-clock.js"', text("web/src/sw.js"))
        self.assertIn('shared/live-clock.js', text("web/src/index.html"))
        self.assertIn("live-clock.js", text("web/tools/verify_export.py"))

    def test_the_web_player_reads_kickoffs_through_the_clock_zone(self):
        app = text("web/src/app.js")
        self.assertIn("function ensureLiveClock(", app)
        self.assertIn("getLongitude: () =>", app)
        self.assertIn("liveClock.mount(", app)
        # The zone reaches the kickoff text and the countdown's date, not just
        # the clock widget at the top of the tab.
        self.assertIn("...(clockZone ? { timeZone: clockZone } : {})", app)

    def test_the_desktop_renderer_reads_kickoffs_through_the_clock_zone(self):
        app = text(f"{RENDERER}/app.js")
        self.assertIn("function ensureLiveClock(", app)
        self.assertIn("function clockLongitude(", app)
        self.assertIn("kickoffStamp(event.kickoffMs, clockZone)", app)
        self.assertIn("kickoffStamp(kickoff, clockZone)", app)
        self.assertIn('id="live-clock"', text(f"{RENDERER}/index.html"))
        self.assertIn('<script src="live-clock.js"></script>', text(f"{RENDERER}/index.html"))

    def test_android_mirrors_the_rule_and_offers_a_remote_friendly_picker(self):
        clock = text(f"{ANDROID}/data/LiveClock.kt")
        for needle in (
            "object LiveClock",
            "fun resolveZone(",
            "fun offsetLabel(",
            "fun kickoffText(",
            "fun kickoffStamp(",
            "fun suggestZones(",
            "fun bandForLongitude(",
            "fun nextKickoff(",
            "fun summary(",
            'const val STORAGE_KEY = "premiumtv.live.clockZone"',
        ):
            self.assertIn(needle, clock)
        home = text(f"{ANDROID}/ui/HomeScreen.kt")
        self.assertIn("private fun LiveClockRow(", home)
        self.assertIn("LiveClock.resolveZone(clockChoice, deviceZone)", home)
        self.assertIn("kickoffTime(event.kickoffUtc ?: 0L, clockZone)", home)
        # The saved market's longitude is what the suggestions start from.
        self.assertIn("marketLongitude = localMarket?.longitude", home)
        self.assertIn("localMarket = localMarket", text(f"{ANDROID}/ui/AppRoot.kt"))

    def test_the_zone_rules_are_pinned_by_tests_on_every_platform(self):
        web = text("web/test/live-clock.test.cjs")
        for needle in ("bandForLongitude", "suggestZones", "resolveTimeZone", "nextKickoff"):
            self.assertIn(needle, web)
        jvm = text("android/app/src/test/kotlin/com/premiumtv/app/data/LiveClockTest.kt")
        for needle in ("suggestZones", "bandForLongitude", "nextKickoff", "loadChoice"):
            self.assertIn(needle, jvm)

    def test_the_clock_never_needs_the_network(self):
        # The suggestion band comes from the bundled local-channel directory,
        # never from an IP lookup or a geocoder.
        for path in (f"{RENDERER}/live-clock.js", f"{ANDROID}/data/LiveClock.kt"):
            source = text(path)
            for forbidden in ("fetch(", "XMLHttpRequest", "ipapi", "geolocat", "HttpURLConnection"):
                self.assertNotIn(forbidden, source, path)
        self.assertIn("localMarkets = remember", text(f"{ANDROID}/ui/AppRoot.kt"))


if __name__ == "__main__":
    unittest.main()
