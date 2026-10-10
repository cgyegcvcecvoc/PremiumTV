"""Offline tests for the one category/order contract and the verification tool.

Everything here runs without a network: the published files are the fixture, and
the questions are the ones ``scripts/verify_playlists.py`` asks about them -
is a group-title one the taxonomy would have written, is the file in the
published order, does a header advertise more guides than a player should
download, and does a published link survive the last deep check.
"""
import datetime as dt
import json
import sys
import tempfile
import unittest
from io import StringIO
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import categorize  # noqa: E402
import link_check  # noqa: E402
import resort_playlists  # noqa: E402
import scraper  # noqa: E402
import verify_playlists  # noqa: E402


def channel(name: str, url: str, group: str = "", **attrs) -> scraper.Channel:
    data = {"group-title": group, **attrs}
    return scraper.Channel(name=name, url=url, source="unit", attrs=data)


class CanonicalGroupTest(unittest.TestCase):
    """A group-title is canonical when scripts/categorize.py would have written it."""

    def test_generated_labels_are_canonical(self):
        for group in ("Sports", "Cartoons", "PBS", "Game Shows", "News", "Music",
                      "Sports Backups", "Other", "International", "United States",
                      "United Kingdom", "Europe", "Asia", "India"):
            with self.subTest(group=group):
                self.assertTrue(categorize.is_canonical_group(group))
                self.assertFalse(categorize.needs_normalization(group))

    def test_upstream_leftovers_are_not(self):
        for group in ("", "General", "Undefined", "TV", "Italy", "Films 📽️",
                      "Tv • Series 📺", "VOD Italy", "Buy Me a Coffee"):
            with self.subTest(group=group):
                self.assertFalse(categorize.is_canonical_group(group))
                self.assertTrue(categorize.needs_normalization(group))

    def test_a_backup_of_an_upstream_group_is_not_canonical(self):
        # "General Backups" is only canonical if "General" is, and it is not.
        self.assertFalse(categorize.is_canonical_group("General Backups"))


class OrderContractTest(unittest.TestCase):
    """order_channels and the key used by the offline tools must agree."""

    def test_key_and_order_are_the_same_rule(self):
        channels = [
            channel("ZZ News", "u1", "News"),
            channel("NFL Network", "u2", "Sports"),
            channel("NFL News", "u3", "Sports Backups"),
            channel("Odd One", "u4", "Game Shows"),
            channel("Unknown", "u5", categorize.OTHER),
        ]
        key = categorize.order_key_for(channels)
        self.assertEqual(sorted(channels, key=key), categorize.order_channels(channels))

    def test_curated_groups_lead_and_other_trails(self):
        channels = [channel("News A", "u1", "News"), channel("Sports A", "u2", "Sports"),
                    channel("Big Tail", "u3", "Movies"), channel("Big Tail 2", "u4", "Movies"),
                    channel("Loose", "u5", categorize.OTHER)]
        ordered = [ch.name for ch in categorize.order_channels(channels)]
        # Sports is curated so it leads; the tail (Movies, then News) is ordered by
        # size; Other is always last.
        self.assertEqual(ordered, ["Sports A", "Big Tail", "Big Tail 2", "News A", "Loose"])


class CanonicalizeChannelsTest(unittest.TestCase):
    def test_country_is_persisted_before_the_group_is_rewritten(self):
        # The upstream group is the only country signal, and it is about to be
        # replaced by a category - so the country has to be written down first.
        italy = channel("Rai 1", "http://x.test/rai.m3u8", "Italia 🇮🇹")
        usa = channel("ESPN", "http://x.test/espn.m3u8", "General", **{"tvg-country": "us"})
        counts = scraper.canonicalize_channels([italy, usa])
        self.assertEqual(usa.attrs["tvg-country"], "US")   # normalised to a code
        self.assertIn(italy.attrs["tvg-country"], ("IT", "Italy"))
        self.assertTrue(categorize.is_canonical_group(italy.attrs["group-title"]))
        self.assertEqual(sum(counts.values()), 2)

    def test_a_group_the_taxonomy_writes_is_left_alone(self):
        kept = channel("Local News", "http://x.test/a.m3u8", "United States")
        scraper.canonicalize_channels([kept])
        self.assertEqual(kept.attrs["group-title"], "United States")

    def test_an_upstream_group_is_reclassified_by_name(self):
        moved = channel("NFL Network", "http://x.test/nfl.m3u8", "General")
        scraper.canonicalize_channels([moved])
        self.assertEqual(moved.attrs["group-title"], "Sports")

    def test_channels_end_in_the_published_order(self):
        channels = [channel("BB News", "u1", "News"), channel("AA Sports", "u2", "Sports"),
                    channel("CC News", "u3", "News")]
        scraper.canonicalize_channels(channels)
        self.assertEqual([ch.name for ch in channels], ["AA Sports", "BB News", "CC News"])

    def test_max_feeds_keeps_the_best_quality_first(self):
        channels = [channel("CNN (720p)", "u1", "News"), channel("CNN (1080p)", "u2", "News"),
                    channel("CNN (SD)", "u3", "News"), channel("Horn (1080p)", "u4", "News")]
        scraper.canonicalize_channels(channels, max_feeds=2)
        urls = {ch.url for ch in channels}
        self.assertIn("u2", urls)          # best quality of CNN survives
        self.assertIn("u1", urls)
        self.assertNotIn("u3", urls)       # the third CNN feed is dropped
        self.assertEqual(len(channels), 3)


class HeaderGuideCapTest(unittest.TestCase):
    def test_general_playlists_keep_the_merged_guide_and_two_fallbacks(self):
        guides = ["https://one.test/g1.xml", "https://two.test/g2.xml",
                  "https://three.test/g3.xml"] + [f"https://n.test/{i}.xml" for i in range(40)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "list.m3u"
            scraper.write_m3u(path, [channel("ESPN", "u1", "Sports")], guides, "test")
            header = path.read_text().splitlines()[0]
            advertised = header.split('x-tvg-url="', 1)[1].rstrip('"').split(",")
            self.assertEqual(len(advertised), 1 + scraper.MAX_HEADER_GUIDES)
            self.assertEqual(advertised[0], scraper.SELF_EPG_URL)

    def test_a_country_playlist_is_not_touched(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "list.m3u"
            scraper.write_m3u(path, [channel("RAI", "u1", "News")],
                              ["https://country.test/it.xml"], "test", advertise_self=False)
            header = path.read_text().splitlines()[0]
            self.assertIn("https://country.test/it.xml", header)

    def test_trim_guides_only_trims_headers_that_lead_with_our_own_guide(self):
        repo = "https://raw.githubusercontent.com/o/r/main/EPG/PremiumTV.xml"
        header = [f'#EXTM3U x-tvg-url="{repo},' + ",".join(f"https://u.test/{i}.xml" for i in range(30)) + '"',
                  "# a note"]
        trimmed, removed = resort_playlists.trim_guides(header, 2)
        self.assertEqual(removed, 28)
        self.assertEqual(trimmed[0].count(","), 2)
        foreign = ['#EXTM3U x-tvg-url="https://someone.else/guide.xml,'
                   + ",".join(f"https://u.test/{i}.xml" for i in range(30)) + '"']
        self.assertEqual(resort_playlists.trim_guides(foreign, 2), (foreign, 0))
        self.assertEqual(resort_playlists.trim_guides(foreign, -1), (foreign, 0))


class DeepCheckEvidenceTest(unittest.TestCase):
    """A link the deep check called dead must not be published, and stale evidence is ignored."""

    def test_offline_and_invalid_urls_are_held_back(self):
        fresh = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=5)).isoformat(timespec="seconds")
        with tempfile.TemporaryDirectory() as tmp:
            checks = Path(tmp)
            (checks / "link-check.json").write_text(json.dumps({
                "finished_utc": fresh,
                "per_playlist": {
                    "playlists/PremiumTV.m3u": {"dead": [
                        {"url": "http://x.test/dead.m3u8", "status": "offline", "reason": "no route"},
                        {"url": "http://x.test/bad.m3u8", "status": "invalid", "reason": "not a playlist"},
                        {"url": "http://x.test/slow.m3u8", "status": "timeout"},
                    ]},
                },
            }), encoding="utf-8")
            dead = scraper.load_deep_check_dead(checks, 72.0)
        self.assertEqual(sorted(dead), ["http://x.test/bad.m3u8", "http://x.test/dead.m3u8"])
        channels = [channel("Dead", "http://x.test/dead.m3u8"), channel("Slow", "http://x.test/slow.m3u8")]
        with tempfile.TemporaryDirectory() as tmp:
            # re-write the file for the helper, then apply it to the channels
            checks = Path(tmp)
            (checks / "link-check.json").write_text(json.dumps({
                "finished_utc": fresh,
                "per_playlist": {"p": {"dead": [
                    {"url": "http://x.test/dead.m3u8", "status": "offline"}]}},
            }), encoding="utf-8")
            held = scraper.apply_deep_check_evidence(channels, checks, 72.0)
        self.assertEqual(held, 1)
        self.assertEqual(channels[0].status, "dead")
        self.assertIn("deep check", channels[0].reason)
        self.assertEqual(channels[1].status, "unchecked")

    def test_stale_evidence_is_ignored(self):
        old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=10)).isoformat(timespec="seconds")
        with tempfile.TemporaryDirectory() as tmp:
            checks = Path(tmp)
            (checks / "link-check.json").write_text(json.dumps({
                "finished_utc": old,
                "dead": [{"url": "http://x.test/dead.m3u8", "status": "offline"}],
            }), encoding="utf-8")
            self.assertEqual(scraper.load_deep_check_dead(checks, 72.0), {})


class PatchRegroupsTest(unittest.TestCase):
    """A patched playlist comes back in the same order the scraper would publish."""

    def test_tidy_blocks_sorts_and_rewrites_raw_groups(self):
        text = "\n".join([
            "#EXTM3U",
            '#EXTINF:-1 tvg-id="Rai1.it" group-title="General",Rai 1',
            "http://x.test/rai.m3u8",
            '#EXTINF:-1 tvg-id="ESPN.us" group-title="TV",ESPN (1080p)',
            "http://x.test/espn.m3u8",
            '#EXTINF:-1 tvg-id="CNN.us" group-title="News",CNN',
            "http://x.test/cnn.m3u8",
            "",
        ])
        header, blocks = link_check.split_blocks(text)
        ordered, changed = link_check.tidy_blocks(blocks, "PremiumTV.m3u")
        names = [block.name for block in ordered]
        self.assertEqual(names, ["ESPN (1080p)", "Rai 1", "CNN"])  # curated first, then by size
        body = link_check.blocks_to_text(header, ordered)
        self.assertIn('group-title="Sports"', body)  # ESPN moved out of "TV"
        # "General" said nothing, so Rai 1 is placed by the only other signal it
        # carries - its .it tvg-id - which is a world region, not one "Other" pile.
        self.assertIn('group-title="Europe"', body)
        self.assertGreaterEqual(changed, 1)


class VerifyPlaylistTest(unittest.TestCase):
    """The report the workflows publish, and what --strict fails on."""

    def good_playlist(self) -> str:
        repo = "https://raw.githubusercontent.com/o/r/main/EPG/PremiumTV.xml"
        return "\n".join([
            f'#EXTM3U x-tvg-url="{repo}"',
            "# working links",
            '#EXTINF:-1 tvg-id="ESPN.us" group-title="Sports",ESPN (1080p)',
            "http://x.test/espn.m3u8",
            '#EXTINF:-1 tvg-id="CNN.us" group-title="News",CNN',
            "http://x.test/cnn.m3u8",
            "",
        ])

    def report_for(self, text: str, dead: dict | None = None) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            playlist = root / "list.m3u"
            playlist.write_text(text, encoding="utf-8")
            previous = verify_playlists.ROOT
            verify_playlists.ROOT = root
            try:
                return verify_playlists.verify_playlist(playlist, root / "EPG", dead or {}, {},
                                                       parse_epg=False)
            finally:
                verify_playlists.ROOT = previous

    def test_a_canonical_file_has_no_issues(self):
        report = self.report_for(self.good_playlist())
        self.assertEqual(report["issues"], [])
        self.assertEqual(report["out_of_order"], 0)
        self.assertEqual(report["entries"], 2)
        self.assertEqual(report["guides_advertised"], 1)

    def test_raw_groups_dead_links_and_a_fat_header_are_all_reported(self):
        repo = "https://raw.githubusercontent.com/o/r/main/EPG/PremiumTV.xml"
        padded = f'#EXTM3U x-tvg-url="{repo},' + ",".join(f"https://u.test/{i}.xml" for i in range(20)) + '"'
        text = "\n".join([
            padded,
            '#EXTINF:-1 tvg-id="CNN.us" group-title="News",CNN',
            "http://x.test/cnn.m3u8",
            '#EXTINF:-1 tvg-id="Rai1.it" group-title="Undefined",Rai 1',
            "http://x.test/dead.m3u8",
            '#EXTINF:-1 tvg-id="CNN.us" group-title="News",CNN again',
            "http://x.test/cnn.m3u8",
            "",
        ])
        report = self.report_for(text, dead={"http://x.test/dead.m3u8": "deep check: offline"})
        joined = " | ".join(report["issues"])
        self.assertIn("group the taxonomy never writes", joined)
        self.assertIn("duplicate URL", joined)
        self.assertIn("confirmed dead by the last deep check", joined)
        self.assertIn("advertises 21 guides", joined)
        self.assertEqual(len(report["dead_links"]), 1)
        self.assertGreater(report["out_of_order"], 0)

    def test_missing_ids_are_reported(self):
        text = "\n".join(['#EXTM3U', '#EXTINF:-1 group-title="News",No Id', "http://x.test/a.m3u8", ""])
        report = self.report_for(text)
        self.assertEqual(report["missing_tvg_id"], 1)
        self.assertEqual(report["missing_tvg_id_sample"], ["No Id"])

    def test_strict_run_on_a_touched_tree(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "countries").mkdir()
            good = root / "PremiumTV.m3u"
            good.write_text(self.good_playlist(), encoding="utf-8")
            self.assertEqual(verify_playlists.main([ "--out", str(root), "--no-epg-parse",
                                                     "--strict"]), 0)
            good.write_text(
                "\n".join(['#EXTM3U', '#EXTINF:-1 tvg-id="X.us" group-title="General",X',
                           "http://x.test/x.m3u8", ""]), encoding="utf-8")
            self.assertEqual(verify_playlists.main(["--out", str(root), "--no-epg-parse",
                                                     "--strict"]), 1)
            # ...and the reports it promises exist afterwards
            self.assertTrue((root / "checks" / "VERIFY.md").exists())
            payload = json.loads((root / "checks" / "verify.json").read_text(encoding="utf-8"))
            self.assertEqual(payload["totals"]["playlists_with_issues"], 1)
            self.assertIn("curated_categories", payload)


class EpgBuildHeaderPatchTest(unittest.TestCase):
    """The guide build patches headers too, and must honour the same allowance."""

    def test_patch_keeps_the_merged_guide_plus_the_shared_allowance(self):
        import epg_build
        raw = "https://raw.githubusercontent.com/o/r/main/EPG/PremiumTV.xml"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "PremiumTV.m3u"
            guides = ",".join([raw] + [f"https://u.test/{i}.xml" for i in range(40)])
            path.write_text(f'#EXTM3U x-tvg-url="{guides}"\n# a playlist\n', encoding="utf-8")
            epg_build.patch_playlists([path], raw, set(),
                                       max_fallbacks=scraper.MAX_HEADER_GUIDES)
            import re
            advertised = re.search(r'x-tvg-url="([^"]*)"', path.read_text()).group(1).split(",")
            self.assertEqual(advertised[0], raw)
            self.assertEqual(len(advertised), 1 + scraper.MAX_HEADER_GUIDES)
            # the two parsers agree on the default, so neither can widen the header back up
            self.assertEqual(epg_build.patch_playlists.__defaults__[1], scraper.MAX_HEADER_GUIDES)


class CommittedPlaylistsTest(unittest.TestCase):
    """The repository's own published files have to satisfy the same contract."""

    ROOT = Path(__file__).resolve().parents[1]

    def _channels(self, name: str):
        path = self.ROOT / "playlists" / name
        if not path.exists():
            self.skipTest(f"{name} is not checked in")
        text = path.read_text(encoding="utf-8", errors="replace")
        _, blocks = link_check.split_blocks(text)
        return [link_check.channel_from_block(block, name) for block in blocks]

    def test_main_playlist_uses_only_generated_groups(self):
        channels = self._channels("PremiumTV.m3u")
        self.assertGreater(len(channels), 1000)
        raw = sorted({ch.attrs.get("group-title", "") for ch in channels
                      if categorize.needs_normalization(ch.attrs.get("group-title", ""))})
        self.assertEqual(raw, [], f"upstream groups survived publishing: {raw[:10]}")

    def test_main_playlist_is_in_the_published_order(self):
        channels = self._channels("PremiumTV.m3u")
        expected = categorize.order_channels(channels)
        self.assertEqual([(ch.name, ch.url) for ch in channels],
                         [(ch.name, ch.url) for ch in expected],
                         "PremiumTV.m3u is not in the order scripts/categorize.py defines")

    def test_published_headers_do_not_advertise_hundreds_of_guides(self):
        import re
        for name in ("PremiumTV.m3u", "AE_Channels.m3u", "Priority_Channels.m3u",
                     "PremiumTV_all.m3u"):
            first = (self.ROOT / "playlists" / name).read_text(encoding="utf-8").splitlines()[0]
            match = re.search(r'x-tvg-url="([^"]*)"', first)
            guides = [item for item in (match.group(1).split(",") if match else []) if item.strip()]
            self.assertLessEqual(len(guides), 1 + scraper.MAX_HEADER_GUIDES,
                                 f"{name} advertises {len(guides)} guides")


if __name__ == "__main__":
    unittest.main()


class PruneEmptiedPlaylistTest(unittest.TestCase):
    """What a re-sort leaves behind when it prunes the last link of a playlist.

    The biweekly run's own report caught three country playlists published as an
    empty body under a header that still said "working channels (1)": the header
    count is only refreshed while a file has entries, so the files the prune
    emptied kept advertising a channel nobody can play. These tests pin the two
    halves of that fix - generated playlists are dropped when they hold nothing,
    and a playlist that has to stay gets a header that tells the truth.
    """

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.playlists = self.root / "playlists"
        (self.playlists / "countries").mkdir(parents=True)
        (self.playlists / "checks").mkdir(parents=True)
        self.addCleanup(self.tmp.cleanup)

    def write_playlist(self, relative: str, urls: list, note: str) -> Path:
        path = self.playlists / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = ["#EXTM3U", f"# {note}"]
        for index, url in enumerate(urls):
            lines.append(f'#EXTINF:-1 tvg-id="c{index}.x@SD" group-title="Other",Chan {index}')
            lines.append(url)
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def mark_dead(self, *urls: str) -> None:
        finished = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
        report = {"finished_utc": finished,
                  "dead": [{"url": url, "status": "offline", "reason": "no media segment"}
                           for url in urls]}
        (self.playlists / "checks" / "link-check.json").write_text(
            json.dumps(report), encoding="utf-8")

    def run_resort(self, *extra: str) -> str:
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = resort_playlists.main(["--out", str(self.playlists), "--no-guides",
                                          "--label", "unit test", *extra])
        self.assertEqual(0, code)
        return buffer.getvalue()

    def test_the_last_pruned_channel_takes_the_file_with_it(self):
        url = "https://stream.test/bermuda.m3u8"
        path = self.write_playlist("countries/Bermuda.m3u", [url],
                                   "Bermuda working channels (1) - updated once")
        self.mark_dead(url)
        output = self.run_resort()
        self.assertFalse(path.exists(), "an emptied country playlist stays published")
        self.assertIn("removed (no channel left)", output)

    def test_a_husk_left_by_an_earlier_run_is_also_cleaned_up(self):
        path = self.write_playlist("countries/Macau.m3u", [],
                                  "Macau working channels (1) - updated once")
        self.mark_dead("https://stream.test/other.m3u8")
        output = self.run_resort()
        self.assertFalse(path.exists())
        self.assertIn("1 emptied country playlist(s) removed", output)

    def test_dry_run_only_says_it_would(self):
        url = "https://stream.test/san.m3u8"
        path = self.write_playlist("countries/San_Marino.m3u", [url],
                                  "San Marino working channels (1) - updated once")
        self.mark_dead(url)
        output = self.run_resort("--dry-run")
        self.assertTrue(path.exists())
        self.assertIn("would remove (no channel left)", output)
        self.assertIn(url, path.read_text(encoding="utf-8"))

    def test_a_published_entry_point_keeps_its_file_and_a_true_count(self):
        url = "https://stream.test/main.m3u8"
        path = self.write_playlist("PremiumTV.m3u", [url],
                                   "Working links - curated categories - 1 channels - updated once")
        self.mark_dead(url)
        self.run_resort()
        self.assertTrue(path.exists(), "PremiumTV.m3u must survive even when empty")
        text = path.read_text(encoding="utf-8")
        self.assertNotIn(url, text)
        self.assertIn("0 channels", text)
        self.assertNotIn("1 channels", text)

    def test_only_generated_directories_may_be_dropped(self):
        cases = {
            "countries/Bermuda.m3u": True,
            "countries/USA.m3u": True,
            "PremiumTV.m3u": False,
            "PremiumTV_all.m3u": False,
            "Priority_Channels.m3u": False,
            "categories/News.m3u": False,
            "sources/priority-channels.m3u": False,
            "countries/README.md": False,
            "Bermuda.m3u": False,
        }
        for relative, expected in cases.items():
            with self.subTest(relative=relative):
                self.assertIs(expected,
                              resort_playlists.droppable_when_empty(
                                  self.playlists / relative, self.playlists))
