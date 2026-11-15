"""1.1.11 contracts: the location question, one A&E shelf, and named releases.

These are source-level assertions on purpose: the Kotlin UI cannot be compiled
in this repository's offline suite, so the promises the release makes about its
own screens, its category rule and its release tooling are pinned here. The
Gradle unit tests and the emulator gate in android-build.yml prove the rest.
"""

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UI = ROOT / "android" / "app" / "src" / "main" / "kotlin" / "com" / "premiumtv" / "app" / "ui"
DATA = ROOT / "android" / "app" / "src" / "main" / "kotlin" / "com" / "premiumtv" / "app" / "data"
MAC = ROOT / "macos" / "app" / "src" / "renderer"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class LocalChannelsAskTests(unittest.TestCase):
    """1.1.11: the location question is asked once, and declining is fine."""

    def test_android_asks_after_setup_and_remembers_a_skip(self):
        root = text(UI / "AppRoot.kt")
        dialog = text(UI / "LocalChannelsDialog.kt")
        settings = text(DATA / "LocalChannels.kt")
        self.assertIn("var localAsked by remember { mutableStateOf(localSettings.asked()) }", root)
        # Asked once, after setup, never over a playing channel or an update popup.
        self.assertIn("(showLocalSetup || (setupComplete && !localAsked && !noticeFirst))", root)
        self.assertIn("&& playing == null", root)
        self.assertIn("localSettings.markAsked()", root)
        # Declining is a first-class answer, not a dismissal that re-asks.
        self.assertIn("onDecline", dialog)
        self.assertIn("Skip for now", dialog)
        self.assertIn("fun asked(): Boolean", settings)
        self.assertIn("fun markAsked()", settings)

    def test_the_dialog_offers_location_then_zip_then_state_then_country(self):
        dialog = text(UI / "LocalChannelsDialog.kt")
        self.assertIn('Text(if (locating) "Locating…" else "Use my location")', dialog)
        self.assertIn("No thanks", dialog)
        self.assertIn('label = { Text("ZIP code") }', dialog)
        self.assertLess(dialog.index('Text("ZIP code")'), dialog.index('Text("State")'))
        self.assertLess(dialog.index('Text("State")'), dialog.index('Text("Country")'))
        # The ZIP hint names the state and the market it resolves to.
        self.assertIn("zipState", dialog)
        self.assertIn("directory?.marketForZip(current.zip)", dialog)
        # A country we do not publish for is answered honestly.
        self.assertIn("hasCountry", dialog)
        self.assertIn("published for the United States only so far", dialog)

    def test_a_location_fix_resolves_to_a_market(self):
        data = text(DATA / "LocalChannels.kt")
        self.assertIn("fun nearestMarket(latitude: Double, longitude: Double, state: String? = null)", data)
        # kotlin.math has no `radians`; importing it fails the APK build.
        self.assertNotIn("import kotlin.math.radians", data)
        self.assertIn("fun marketForZip(zip: String): LocalMarket?", data)
        self.assertIn("fun marketsFor(selection: LocalSelection): List<LocalMarket>", data)
        dialog = text(UI / "LocalChannelsDialog.kt")
        self.assertIn("known?.nearestMarket(latitude, longitude)", dialog)

    def test_the_mac_asks_once_and_names_the_market(self):
        app = text(MAC / "app.js")
        html = text(MAC / "index.html")
        local = text(MAC / "local-channels.js")
        self.assertIn("function maybeAskLocalArea()", app)
        self.assertIn("window.setTimeout(maybeAskLocalArea, 350)", app)
        self.assertIn("local.asked(window.localStorage)", app)
        self.assertIn("local.markAsked(window.localStorage)", app)
        self.assertIn('id="local-setup"', html)
        self.assertIn("Where do you watch from?", html)
        self.assertIn("Enter a ZIP or state", html)
        self.assertIn("Skip for now", html)
        # The same market resolution as Android.
        self.assertIn("function nearestMarket(latitude, longitude, directory, state)", local)
        self.assertIn("function marketForZip(zip, directory)", local)
        self.assertIn("localMarkets().map((market) => `${market.city}, ${market.state}`)", app)


class AAndEOneCategoryTests(unittest.TestCase):
    """1.1.11: every A+E Networks channel sits in one category."""

    def test_the_rule_covers_the_whole_family(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import categorize
        for name in ("A&E Crime 360 (Pluto TV)", "Crime 360 (720p)", "History Channel",
                     "History Asia (720p)", "History Latin America (1080p)", "Lifetime",
                     "Lifetime Movie Network", "LMN", "FYI", "VICE TV", "Home.Made.Nation",
                     "☆ Live PD Greatest Shifts 🇺🇸", "Crime & Investigation Network (US)"):
            with self.subTest(name=name):
                self.assertEqual(categorize.classify(name, "Documentary"), "A&E Networks")

    def test_documentaries_with_a_brand_word_stay_documentaries(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        import categorize
        for name in ("History Hit (720p)", "True History (720p)", "☆ Autentic History 🇺🇸"):
            with self.subTest(name=name):
                self.assertEqual(categorize.classify(name), "Documentary")

    def test_the_curated_a_and_e_playlist_carries_the_history_and_lifetime_feeds(self):
        lines = text(ROOT / "playlists" / "sources" / "ae-networks.m3u").splitlines()
        groups = {re.search(r'group-title="([^"]*)"', line).group(1)
                  for line in lines if line.startswith("#EXTINF")}
        self.assertEqual(groups, {"A&E Networks"})
        # History's own FAST feeds are on the same shelf, not split off.
        self.assertIn("by History / A&E", text(ROOT / "playlists" / "sources" / "ae-networks.m3u"))

    def test_the_published_usa_feeds_and_shelves_agree(self):
        for path in ("playlists/live/USA.m3u", "playlists/countries/USA.m3u"):
            feed = text(ROOT / path)
            for name in ("History Channel\n", "Lifetime\n"):
                with self.subTest(path=path, name=name.strip()):
                    line = next(l for l in feed.splitlines()
                                if l.startswith("#EXTINF") and l.endswith("," + name.strip()))
                    self.assertIn('group-title="A&E Networks"', line)
        shelf = text(ROOT / "categories" / "USA" / "A_E_Networks.m3u")
        for channel in ("History Channel", "Lifetime", "Crime 360 (720p)"):
            self.assertIn(channel, shelf)
        documentary = text(ROOT / "categories" / "USA" / "Documentary.m3u")
        self.assertNotIn(",History Channel\n", documentary)
        # No A&E-owned channel is left behind in Documentary or Lifestyle.
        for path in ("categories/USA/Documentary.m3u", "categories/USA/Lifestyle.m3u",
                     "categories/All/Documentary.m3u"):
            feed = text(ROOT / path)
            for name in ("Lifetime\n", "Lifetime Movie Network\n", "History Channel\n"):
                self.assertNotIn("," + name, feed, f"{path} still carries {name.strip()}")


class NamedReleaseTests(unittest.TestCase):
    """1.1.11: a release name is derived, and “new version” needs no questions."""

    def test_the_next_version_and_its_name_come_from_one_command(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "new_version.py"), "--next"],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        version = text(ROOT / "VERSION").strip()
        self.assertIn(version, result.stdout)
        self.assertIn("release name: PremiumTV <version> — <feature name>", result.stdout)
        for feature in ("local-channels", "a-and-e", "version-scheme"):
            self.assertIn(feature, result.stdout)

    def test_the_release_notes_follow_the_name_rule(self):
        version = text(ROOT / "VERSION").strip()
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "new_version.py"), "--check-notes", version],
            cwd=ROOT, capture_output=True, text=True, timeout=120,
        )
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        first = text(ROOT / f"release-notes-{version}.md").splitlines()[0]
        self.assertRegex(first, rf"^# PremiumTV {re.escape(version)} — \S.*\S$")

    def test_the_publishing_workflow_uses_the_notes_heading_as_the_title(self):
        workflow = text(ROOT / ".github" / "workflows" / "publish-release.yml")
        self.assertIn('title=$(head -1 "$notes" | sed \'s/^# *//\')', workflow)
        # Publishing is triggered by the VERSION push or the manual run; either
        # way it is the one step that makes an installed app see the release.
        self.assertIn("- VERSION", workflow)
        self.assertIn("workflow_dispatch", workflow)

    def test_the_docs_carry_the_rule_so_no_agent_has_to_be_told(self):
        agents = text(ROOT / "AGENTS.md")
        releasing = text(ROOT / "docs" / "RELEASING.md")
        for needle in ("release name", "next patch", "--next", "--check-notes"):
            self.assertIn(needle, agents.lower())
            self.assertIn(needle, releasing.lower())
        self.assertIn("PremiumTV <version> — <feature name>", releasing)
        self.assertIn("No question back to the user", releasing)

    def test_the_update_notice_nudges_every_build_below_the_release(self):
        document = json.loads(text(ROOT / "app-update-notice.json"))
        rules = {rule["id"]: rule for rule in document["rules"]}
        version = text(ROOT / "VERSION").strip()
        major, minor, patch = version.split(".")
        expected = f"{major}.{minor}.{int(patch) - 1}"
        self.assertEqual(rules["update-below-newest"]["max_version"], expected)
        self.assertIn(version, rules["update-below-newest"]["surprise"])


if __name__ == "__main__":
    unittest.main()
