"""End-of-support delivery for builds that cannot be given new code.

PremiumTV 1.0.0-1.0.4 refresh one playlist baked into their bundles
(``playlists/countries/USA.m3u``) and carry no updater and no notice code, so
the only way to reach them is through that feed.  These checks guard the
contract ``scripts/legacy_sunset.py`` implements:

  * while support lasts, the live feed the current builds use is kept in step;
  * on the published end-of-support date the legacy feed is pinned, carries one
    sanctioned notice entry, and stops receiving scrape updates;
  * the freeze is idempotent, survives a scrape run rewriting the file, and is
    reported by the CI guard when it does not;
  * every consumer that must not go stale resolves the live feed, not the pin;
  * the notice entry is marked so both apps drop it instead of playing it.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "android" / "tools"))

import build_bundle  # noqa: E402
import legacy_sunset  # noqa: E402

NOTICE_PATH = ROOT / legacy_sunset.NOTICE_FILE
LEGACY = ROOT / legacy_sunset.LEGACY_USA
LIVE = ROOT / legacy_sunset.LIVE_USA
PINNED = ROOT / legacy_sunset.PINNED_USA

# One day past the published sunset, so the freeze is exercised deterministically.
DOCUMENT = json.loads(NOTICE_PATH.read_text(encoding="utf-8"))


def day_after_support_ends() -> int:
    return legacy_sunset.parse_instant(DOCUMENT["support_ends_utc"]) + 86_400


def day_before_support_ends() -> int:
    return legacy_sunset.parse_instant(DOCUMENT["support_ends_utc"]) - 86_400


class FixtureTree:
    """A throwaway repository tree holding just what the sunset script reads."""

    def __init__(self, notice: dict | None = None) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="premiumtv-sunset-"))
        (self.root / "playlists" / "countries").mkdir(parents=True)
        document = json.loads(NOTICE_PATH.read_text(encoding="utf-8"))
        if notice:
            document.update(notice)
        (self.root / legacy_sunset.NOTICE_FILE).write_text(
            json.dumps(document, indent=2), encoding="utf-8")
        # A tiny stand-in for the 2,800-channel USA feed.
        self.channels = (
            '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/cgyegcvcecvoc/'
            'PremiumTV1/main/EPG/USA.xml"\n'
            "# USA working channels (2) - updated 2026-10-17 18:54 UTC\n"
            '#EXTINF:-1 tvg-id="one.us" group-title="News" tvg-country="US",One News\n'
            "https://example.com/one.m3u8\n"
            '#EXTINF:-1 tvg-id="two.us" group-title="Sports" tvg-country="US",Two Sports\n'
            "#EXTVLCOPT:http-referrer=https://example.tv/\n"
            "https://example.com/two.m3u8\n"
        )
        self.legacy = self.root / legacy_sunset.LEGACY_USA
        self.live = self.root / legacy_sunset.LIVE_USA
        self.pinned = self.root / legacy_sunset.PINNED_USA
        self.legacy.write_text(self.channels, encoding="utf-8")

    def apply(self, when: int) -> dict:
        return legacy_sunset.apply(self.root, now=when)

    def close(self) -> None:
        shutil.rmtree(self.root, ignore_errors=True)


class PublishedNoticeTests(unittest.TestCase):
    """The document the apps' popup and this script both read."""

    def test_support_ends_the_published_grace_period_after_the_first_warning(self):
        notice = legacy_sunset.read_notice(ROOT)
        self.assertEqual(notice["problems"], [])
        self.assertTrue(notice["enabled"])
        first = legacy_sunset.parse_instant(DOCUMENT["first_warning_utc"])
        ends = legacy_sunset.parse_instant(DOCUMENT["support_ends_utc"])
        self.assertIsNotNone(first)
        self.assertIsNotNone(ends)
        import datetime as dt
        first_day = dt.datetime.fromtimestamp(first, dt.timezone.utc).date()
        end_day = dt.datetime.fromtimestamp(ends, dt.timezone.utc).date()
        self.assertEqual((end_day - first_day).days, DOCUMENT["grace_days"])
        self.assertEqual(DOCUMENT["grace_days"], 30,
                         "older builds were promised 30 days from the first warning")

    def test_the_notice_sends_people_to_the_newest_release_on_github(self):
        notice = legacy_sunset.read_notice(ROOT)
        self.assertTrue(notice["releases_url"].startswith(
            "https://github.com/cgyegcvcecvoc/PremiumTV1/releases"), notice["releases_url"])
        self.assertEqual(notice["max_version"], "1.0.6",
                         "the sunset targets every stable build below the current one; "
                         "the blocked preview rule is not an upgrade promise")

    def test_an_impossible_sunset_date_is_rejected_not_rolled_forward(self):
        for value in ["2026-11-31", "2026-13-01", "2026-02-30T00:00:00Z",
                      "soon", "", None, "16/11/2026"]:
            self.assertIsNone(legacy_sunset.parse_instant(value), value)

    def test_the_two_published_date_shapes_are_read_as_utc(self):
        self.assertEqual(legacy_sunset.parse_instant("2026-11-16T23:59:59Z"),
                         legacy_sunset.parse_instant("2026-11-16T23:59:59"))
        # A bare date means "that whole day", so it ends on its last second.
        self.assertEqual(legacy_sunset.parse_instant("2026-11-16"),
                         legacy_sunset.parse_instant("2026-11-16T23:59:59Z"))

    def test_the_support_date_reads_the_same_on_screen_as_in_the_playlist(self):
        ends = legacy_sunset.parse_instant(DOCUMENT["support_ends_utc"])
        self.assertEqual(legacy_sunset.format_day(ends), "Nov 16, 2026")


class WarningPhaseTests(unittest.TestCase):
    """Before the sunset: everything keeps updating, nothing is pinned."""

    def setUp(self):
        self.tree = FixtureTree()
        self.addCleanup(self.tree.close)

    def test_the_live_feed_is_published_from_the_legacy_one(self):
        result = self.tree.apply(day_before_support_ends())
        self.assertTrue(result["ok"], result["problems"])
        self.assertEqual(result["phase"], "warning")
        self.assertTrue(self.tree.live.is_file(), "the live feed must exist for current builds")
        self.assertEqual(self.tree.live.read_text(encoding="utf-8"), self.tree.channels)

    def test_nothing_is_pinned_or_frozen_while_support_lasts(self):
        self.tree.apply(day_before_support_ends())
        self.assertFalse(self.tree.pinned.exists())
        self.assertFalse(legacy_sunset.is_frozen(self.tree.legacy))
        # The channels still arrive; the notice rides in front of them.
        warned = self.tree.legacy.read_text(encoding="utf-8")
        self.assertEqual(legacy_sunset.strip_notice_entries(warned), self.tree.channels,
                         "a legacy build must keep receiving scrape updates until the sunset")
        self.assertEqual(legacy_sunset.count_notice_entries(warned), 1,
                         "the warning phase must actually warn: one sanctioned entry")

    def test_the_warning_entry_is_first_so_an_old_build_shows_it(self):
        self.tree.apply(day_before_support_ends())
        lines = self.tree.legacy.read_text(encoding="utf-8").splitlines()
        first_entry = next(index for index, line in enumerate(lines)
                           if line.startswith("#EXTINF"))
        self.assertTrue(legacy_sunset.is_notice_entry(lines[first_entry]), lines[first_entry])
        self.assertIn("UPDATE PremiumTV", lines[first_entry])
        self.assertIn("updates itself", lines[first_entry])

    def test_the_live_feed_never_carries_the_notice(self):
        self.tree.apply(day_before_support_ends())
        self.assertEqual(legacy_sunset.count_notice_entries(
            self.tree.live.read_text(encoding="utf-8")), 0,
            "current builds must never see a fake channel")

    def test_a_missing_notice_entry_is_a_problem(self):
        self.tree.apply(day_before_support_ends())
        self.tree.legacy.write_text(self.tree.channels, encoding="utf-8")
        problems = legacy_sunset.check(self.tree.root, now=day_before_support_ends())
        self.assertTrue(any("carries no notice entry" in problem for problem in problems),
                        problems)

    def test_a_second_run_changes_nothing(self):
        self.tree.apply(day_before_support_ends())
        before = self.tree.live.read_text(encoding="utf-8")
        result = self.tree.apply(day_before_support_ends())
        self.assertEqual(result["wrote"], [], "the mirror is already in step")
        self.assertEqual(self.tree.live.read_text(encoding="utf-8"), before)

    def test_a_frozen_feed_before_the_sunset_is_a_problem(self):
        self.tree.apply(day_after_support_ends())
        result = self.tree.apply(day_before_support_ends())
        self.assertFalse(result["ok"])
        self.assertTrue(any("has not closed" in problem for problem in result["problems"]),
                        result["problems"])


class FreezeTests(unittest.TestCase):
    """On and after the sunset: the legacy feed is pinned and stops updating."""

    def setUp(self):
        self.tree = FixtureTree()
        self.addCleanup(self.tree.close)

    def test_the_legacy_feed_is_pinned_and_carries_the_notice(self):
        result = self.tree.apply(day_after_support_ends())
        self.assertTrue(result["ok"], result["problems"])
        self.assertEqual(result["phase"], "frozen")
        self.assertTrue(self.tree.pinned.is_file(), "the last scraped channels must be pinned")
        self.assertEqual(self.tree.pinned.read_text(encoding="utf-8"), self.tree.channels)

        frozen = self.tree.legacy.read_text(encoding="utf-8")
        self.assertTrue(legacy_sunset.is_frozen(self.tree.legacy))
        self.assertIn(legacy_sunset.FROZEN_MARKER, frozen)
        self.assertIn(legacy_sunset.NOTICE_VALUE, frozen)
        self.assertIn("Nov 16, 2026", frozen, "the frozen feed must name the day support ended")
        self.assertIn(DOCUMENT["releases_url"], frozen,
                      "the frozen feed must say where the newest release is")

    def test_the_pinned_channels_survive_the_freeze(self):
        self.tree.apply(day_after_support_ends())
        frozen = self.tree.legacy.read_text(encoding="utf-8")
        self.assertIn("https://example.com/one.m3u8", frozen)
        self.assertIn("https://example.com/two.m3u8", frozen)
        self.assertIn("#EXTVLCOPT:http-referrer=https://example.tv/", frozen,
                      "stream options belong to their entry and must be kept")
        # Pinned channels plus exactly one notice entry.
        self.assertEqual(legacy_sunset.count_entries(frozen), 3)

    def test_the_frozen_feed_keeps_advertising_the_live_guide(self):
        self.tree.apply(day_after_support_ends())
        frozen = self.tree.legacy.read_text(encoding="utf-8")
        self.assertIn('x-tvg-url="https://raw.githubusercontent.com/cgyegcvcecvoc/'
                      'PremiumTV1/main/EPG/USA.xml"', frozen,
                      "what ends is the channel scrape, not the listings")

    def test_the_frozen_feed_cannot_claim_a_fresh_update_time(self):
        self.tree.apply(day_after_support_ends())
        head = self.tree.legacy.read_text(encoding="utf-8").splitlines()[:8]
        self.assertFalse(any("USA working channels" in line for line in head),
                         "the pinned file's own header must be replaced by the banner")

    def test_the_freeze_is_idempotent(self):
        self.tree.apply(day_after_support_ends())
        frozen = self.tree.legacy.read_text(encoding="utf-8")
        result = self.tree.apply(day_after_support_ends() + 86_400)
        self.assertEqual(result["wrote"], [], "re-running must not churn the pinned feed")
        self.assertEqual(self.tree.legacy.read_text(encoding="utf-8"), frozen)

    def test_a_scrape_run_overwriting_the_freeze_is_put_back(self):
        self.tree.apply(day_after_support_ends())
        pinned = self.tree.pinned.read_text(encoding="utf-8")
        # A publishing workflow that does not know about the sunset rewrites the
        # legacy path with fresh channels; the next apply must undo that.
        fresh = self.tree.channels.replace("(2)", "(3)").replace(
            "https://example.com/two.m3u8", "https://example.com/three.m3u8")
        self.tree.legacy.write_text(fresh, encoding="utf-8")
        self.assertFalse(legacy_sunset.is_frozen(self.tree.legacy))

        self.tree.apply(day_after_support_ends() + 86_400)
        self.assertTrue(legacy_sunset.is_frozen(self.tree.legacy))
        self.assertEqual(self.tree.pinned.read_text(encoding="utf-8"), pinned,
                         "the pin is written once and never re-pinned from a later run")
        self.assertNotIn("https://example.com/three.m3u8",
                         self.tree.legacy.read_text(encoding="utf-8"),
                         "a legacy build must not receive channels scraped after the sunset")

    def test_the_live_feed_still_receives_the_scrape_after_the_freeze(self):
        self.tree.apply(day_after_support_ends())
        fresh = self.tree.channels.replace("https://example.com/one.m3u8",
                                           "https://example.com/one-v2.m3u8")
        self.tree.legacy.write_text(fresh, encoding="utf-8")
        self.tree.apply(day_after_support_ends() + 86_400)
        self.assertIn("https://example.com/one-v2.m3u8",
                      self.tree.live.read_text(encoding="utf-8"),
                      "current builds keep getting fresh channels after the sunset")


class NoticeEntryTests(unittest.TestCase):
    """The sanctioned entry is a message, never a channel."""

    def test_the_live_feed_never_carries_a_notice_entry(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        tree.apply(day_after_support_ends())
        self.assertFalse(legacy_sunset.is_notice_entry_text(
            tree.live.read_text(encoding="utf-8")))

    def test_stripping_removes_the_entry_and_its_url_and_options(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        tree.apply(day_after_support_ends())
        frozen = tree.legacy.read_text(encoding="utf-8")
        self.assertTrue(legacy_sunset.is_notice_entry_text(frozen))
        stripped = legacy_sunset.strip_notice_entries(frozen)
        self.assertFalse(legacy_sunset.is_notice_entry_text(stripped))
        self.assertNotIn(legacy_sunset.NOTICE_ID, stripped)
        entry_urls = [line.strip() for line in stripped.splitlines()
                      if line.strip() and not line.strip().startswith("#")]
        self.assertNotIn(DOCUMENT["releases_url"], entry_urls,
                         "the notice entry's URL line must go; the banner may still name it")
        self.assertEqual(legacy_sunset.count_entries(stripped), 2,
                         "only the notice entry is removed; the pinned channels stay")
        self.assertIn("https://example.com/one.m3u8", stripped)

    def test_stripping_a_clean_playlist_changes_nothing(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        self.assertEqual(legacy_sunset.strip_notice_entries(tree.channels), tree.channels)

    def test_exactly_one_notice_entry_is_published(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        tree.apply(day_after_support_ends())
        frozen = tree.legacy.read_text(encoding="utf-8")
        marked = [line for line in frozen.splitlines()
                  if line.strip().startswith("#EXTINF") and legacy_sunset.is_notice_entry(line)]
        self.assertEqual(len(marked), 1, "a legacy build shows this as a channel row")

    def test_both_apps_drop_an_entry_carrying_the_marker(self):
        """Static contract: the marker this script writes is the one the apps read."""
        kotlin = (ROOT / "android" / "app" / "src" / "main" / "kotlin" / "com" / "premiumtv"
                  / "app" / "data" / "M3uParser.kt").read_text(encoding="utf-8")
        javascript = (ROOT / "macos" / "app" / "src" / "main"
                      / "parsers.js").read_text(encoding="utf-8")
        for source, name in ((kotlin, "Android"), (javascript, "macOS")):
            self.assertIn(f'"{legacy_sunset.NOTICE_ATTR}"', source.replace("'", '"'), name)
            self.assertIn(legacy_sunset.NOTICE_VALUE, source, name)


class GuardTests(unittest.TestCase):
    """What CI fails on, so a sunset cannot be quietly undone."""

    def test_a_healthy_warning_tree_passes(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        tree.apply(day_before_support_ends())
        self.assertEqual(legacy_sunset.check(tree.root, now=day_before_support_ends()), [])

    def test_a_healthy_frozen_tree_passes(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        tree.apply(day_after_support_ends())
        self.assertEqual(legacy_sunset.check(tree.root, now=day_after_support_ends()), [])

    def test_an_unfrozen_feed_after_the_sunset_fails(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        problems = legacy_sunset.check(tree.root, now=day_after_support_ends())
        self.assertTrue(any("still live" in problem for problem in problems), problems)

    def test_a_missing_live_feed_fails(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        problems = legacy_sunset.check(tree.root, now=day_before_support_ends())
        self.assertTrue(any(legacy_sunset.LIVE_USA in problem for problem in problems), problems)

    def test_an_edited_frozen_feed_fails(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        tree.apply(day_after_support_ends())
        tree.legacy.write_text(
            tree.legacy.read_text(encoding="utf-8").replace("one.m3u8", "tampered.m3u8"),
            encoding="utf-8")
        problems = legacy_sunset.check(tree.root, now=day_after_support_ends())
        self.assertTrue(any("pinned feed" in problem for problem in problems), problems)

    def test_a_frozen_feed_without_its_notice_fails(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        tree.apply(day_after_support_ends())
        tree.legacy.write_text(
            legacy_sunset.strip_notice_entries(tree.legacy.read_text(encoding="utf-8")),
            encoding="utf-8")
        problems = legacy_sunset.check(tree.root, now=day_after_support_ends())
        self.assertTrue(any("no notice entry" in problem for problem in problems), problems)

    def test_a_notice_entry_in_the_live_feed_fails(self):
        tree = FixtureTree()
        self.addCleanup(tree.close)
        tree.apply(day_before_support_ends())
        tree.live.write_text(
            "\n".join(legacy_sunset.notice_lines(
                legacy_sunset.read_notice(tree.root), ended=False)) + "\n"
            + tree.live.read_text(encoding="utf-8"),
            encoding="utf-8")
        problems = legacy_sunset.check(tree.root, now=day_before_support_ends())
        self.assertTrue(any("must stay clean" in problem for problem in problems), problems)

    def test_a_grace_period_that_disagrees_with_the_dates_fails(self):
        tree = FixtureTree(notice={"grace_days": 7})
        self.addCleanup(tree.close)
        tree.apply(day_before_support_ends())
        problems = legacy_sunset.check(tree.root, now=day_before_support_ends())
        self.assertTrue(any("grace period" in problem for problem in problems), problems)


class ToolingToleranceTests(unittest.TestCase):
    """Every publisher must treat the notice as a message, not a dead channel."""

    def setUp(self):
        self.dir = Path(tempfile.mkdtemp(prefix="premiumtv-notice-tools-"))
        self.addCleanup(shutil.rmtree, self.dir, True)
        self.notice = legacy_sunset.read_notice(ROOT)
        body = (
            '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/cgyegcvcecvoc/'
            'PremiumTV1/main/EPG/USA.xml"\n'
            '# USA working channels (2) - updated 2026-10-17 18:54 UTC\n'
            '#EXTINF:-1 tvg-id="one.us" group-title="Sports" tvg-country="US",One Sports\n'
            "https://example.com/one.m3u8\n"
            '#EXTINF:-1 tvg-id="two.us" group-title="News" tvg-country="US",Two News\n'
            "https://example.com/two.m3u8\n"
        )
        self.text = legacy_sunset.inject_notice(body, self.notice)
        self.path = self.dir / "USA.m3u"
        self.path.write_text(self.text, encoding="utf-8")

    def test_verify_playlists_excludes_the_notice_from_every_structural_check(self):
        import verify_playlists

        result = verify_playlists.verify_playlist(
            self.path, self.dir / "EPG", dead={}, cache={}, parse_epg=False)
        self.assertEqual(result["entries"], 2)
        self.assertEqual(result["sanctioned_notice"], 1)
        joined = " ".join(result["issues"])
        self.assertNotIn("PremiumTV Notice", joined)
        self.assertNotIn("taxonomy never writes", joined)
        self.assertNotIn("out of order", joined)
        self.assertEqual(result["out_of_order"], 0)

    def test_the_deep_check_never_probes_the_notice_url(self):
        import link_check

        loaded = link_check.load_playlists([self.path])
        urls = [channel.url for channel in loaded[self.path]["channels"]]
        self.assertEqual(urls, ["https://example.com/one.m3u8",
                                "https://example.com/two.m3u8"])

    def test_the_deep_check_cannot_patch_the_notice_out(self):
        import link_check

        loaded = link_check.load_playlists([self.path])
        results = {
            "https://example.com/one.m3u8": {"status": "offline", "reason": "404"},
            # Even if the notice URL were probed and called dead, it must survive.
            self.notice["releases_url"]: {"status": "offline", "reason": "HTML"},
        }
        link_check.patch_playlists(loaded, results, min_working_ratio=0.0,
                                   max_remove_ratio=1.0, dry_run=False)
        patched = self.path.read_text(encoding="utf-8")
        self.assertEqual(legacy_sunset.count_notice_entries(patched), 1)
        self.assertTrue(legacy_sunset.is_notice_entry(patched.splitlines()[2]))
        self.assertIn("https://example.com/two.m3u8", patched)
        self.assertNotIn("https://example.com/one.m3u8", patched)

    def test_the_guide_builder_never_turns_the_notice_into_a_channel(self):
        import epg_build

        ids = epg_build.country_playlist_ids(self.path)
        self.assertNotIn(legacy_sunset.NOTICE_ID, ids)
        self.assertEqual(ids, ["one.us", "two.us"])

    def test_both_app_parsers_drop_the_same_marker_the_script_writes(self):
        kotlin = (ROOT / "android/app/src/main/kotlin/com/premiumtv/app/data/"
                         "M3uParser.kt").read_text(encoding="utf-8")
        script = (ROOT / "scripts/link_check.py").read_text(encoding="utf-8")
        self.assertIn('const val NOTICE_ATTR = "tvg-notice"', kotlin)
        self.assertIn('const val NOTICE_VALUE = "app-update"', kotlin)
        self.assertIn(legacy_sunset.NOTICE_ATTR, script)
        self.assertIn(legacy_sunset.NOTICE_VALUE, script)


class ConsumerWiringTests(unittest.TestCase):
    """Nothing that must stay current may be pointed at the pinned feed."""

    def test_the_repository_is_in_the_warning_phase_with_a_live_feed(self):
        self.assertTrue(LEGACY.is_file())
        self.assertTrue(LIVE.is_file(),
                        "playlists/live/USA.m3u must be committed for CI to build from it")
        self.assertFalse(legacy_sunset.is_frozen(LEGACY),
                         "the legacy feed must not be frozen before its published sunset")
        self.assertFalse(legacy_sunset.is_notice_entry_text(LIVE.read_text(encoding="utf-8")))

    def test_the_live_feed_is_the_legacy_feed_without_the_notice(self):
        live = LIVE.read_text(encoding="utf-8")
        legacy = LEGACY.read_text(encoding="utf-8")
        self.assertEqual(live, legacy_sunset.strip_notice_entries(legacy),
                         "while support lasts the two feeds carry the same channels")
        self.assertEqual(legacy_sunset.count_notice_entries(legacy), 1,
                         "an installed 1.0.0-1.0.4 must be told about the newer release")
        self.assertEqual(legacy_sunset.count_notice_entries(live), 0)

    def test_apps_are_built_from_the_live_feed(self):
        playlist, guide = build_bundle.SCOPE_INPUTS["usa"]
        self.assertEqual(playlist, legacy_sunset.LIVE_USA,
                         "a build pointed at the legacy feed stops getting channels at the sunset")
        self.assertEqual(guide, "EPG/USA.xml")
        self.assertTrue((ROOT / playlist).is_file(), f"{playlist} must exist to build from")

    def test_the_shelf_and_the_site_resolve_the_live_feed(self):
        import build_categories
        import build_site_data
        import verify_playlists

        self.assertEqual(legacy_sunset.live_usa_path(ROOT), LIVE)
        self.assertEqual(legacy_sunset.live_usa_url(ROOT),
                         f"{legacy_sunset.RAW_BASE}/{legacy_sunset.LIVE_USA}")
        # The shelf's USA source is resolved at run time, not pinned to a path.
        source = (ROOT / "scripts" / "build_categories.py").read_text(encoding="utf-8")
        self.assertIn("legacy_sunset.live_usa_path", source)
        self.assertIn("legacy_sunset.live_usa_path",
                      (ROOT / "scripts" / "build_site_data.py").read_text(encoding="utf-8"))
        self.assertIn("legacy_sunset.is_frozen",
                      (ROOT / "scripts" / "verify_playlists.py").read_text(encoding="utf-8"))
        self.assertTrue(callable(build_categories.build) and callable(build_site_data.build_payload)
                        and callable(verify_playlists.verify_playlist))

    def test_the_guard_accepts_the_repository_as_published(self):
        self.assertEqual(legacy_sunset.check(ROOT), [],
                         "run scripts/legacy_sunset.py apply and commit the result")


if __name__ == "__main__":
    unittest.main()
