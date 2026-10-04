"""Offline tests for canonical channel categories, re-sorting and verification."""
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import channel_categories as cc  # noqa: E402
import link_check  # noqa: E402
import resort_playlists  # noqa: E402
import scraper  # noqa: E402
import verify_playlists  # noqa: E402

M3U_HEADER = '#EXTM3U x-tvg-url="https://raw.githubusercontent.com/o/r/main/EPG/PremiumTV.xml"'


def channel(name, group="", country="", url=None, tvg_id="", source="fixture"):
    attrs = {}
    if group:
        attrs["group-title"] = group
    if country:
        attrs["tvg-country"] = country
    if tvg_id:
        attrs["tvg-id"] = tvg_id
    return scraper.Channel(name=name, url=url or f"https://example.org/{abs(hash(name))}.m3u8",
                           source=source, attrs=attrs)


class CategoryMappingTest(unittest.TestCase):
    def test_specific_groups_win(self):
        cases = [
            ("NickToons", "Animation;Kids", "Cartoons"),
            ("MeTV Toons", "Classic TV;Priority", "Cartoons"),
            ("MeTV", "Classic TV", "TV"),
            ("Sky Sport 24", "Sports", "Sports"),
            ("CNN International", "News", "News"),
            ("TCM", "Films \U0001f4fd\ufe0f", "Movies"),
            ("Discovery Channel", "Doc & History \U0001f3db\ufe0f", "Documentary"),
            ("WGAL 8", "Local;USA", "Local TV"),
            ("MTV 90s", "Music \u2022 Stingray", "Music"),
        ]
        for name, group, expected in cases:
            with self.subTest(name=name, group=group):
                self.assertEqual(cc.canonical_group(name, group), expected)

    def test_name_keywords_rescue_generic_and_empty_groups(self):
        cases = [
            ("ESPN", "Undefined", "Sports"),
            ("Cartoon Network", "General", "Cartoons"),
            ("CNN", "", "News"),
            ("Vevo Hip-Hop & R&B", "", "Music"),
            ("National Geographic", "Other", "Documentary"),
            ("QVC", "Undefined", "Shopping"),
            ("Teleshopping", "", "Shopping"),
            ("Weather Channel", "General", "Weather"),
        ]
        for name, group, expected in cases:
            with self.subTest(name=name, group=group):
                self.assertEqual(cc.canonical_group(name, group), expected)

    def test_country_only_groups_fall_back_to_tv(self):
        self.assertEqual(cc.canonical_group("TV1", "Italy \U0001f1ee\U0001f1f9"), "TV")
        self.assertEqual(cc.canonical_group("Mongol TV", "Mongolia"), "TV")

    def test_every_category_is_in_the_fixed_order(self):
        for name in ("TV", "News", "Cartoons", "Sports"):
            self.assertIn(name, cc.CATEGORY_ORDER)
        self.assertEqual(cc.canonical_group("Something", "Undefined"), "TV")

    def test_output_is_deterministic(self):
        channels = [channel("B", "Undefined", "US"), channel("A", "General", "US"),
                    channel("ESPN", "", "US")]
        first = [c.name for c in sorted(channels, key=cc.channel_sort_key)]
        second = [c.name for c in sorted(reversed(channels), key=cc.channel_sort_key)]
        self.assertEqual(first, second)

    def test_nothing_lands_outside_the_category_list(self):
        channels = [channel("Whatever %d" % i, "Group %d" % i) for i in range(50)]
        cc.apply_categories(channels)
        self.assertTrue({c.attrs["group-title"] for c in channels} <= set(cc.CATEGORY_ORDER))


class OrderingTest(unittest.TestCase):
    def test_us_channels_come_first_inside_a_category(self):
        channels = [channel("Zeta News", "News", "IT"), channel("Alpha News", "News", "USA"),
                    channel("Beta News", "News", "GB")]
        cc.apply_categories(channels)
        self.assertEqual([c.name for c in channels], ["Alpha News", "Beta News", "Zeta News"])

    def test_categories_follow_the_fixed_order(self):
        channels = [channel("A Sport", "Sports", "US"), channel("A Movie", "Movies", "US"),
                    channel("A Cartoon", "Kids", "US"), channel("A Channel", "General", "US")]
        cc.apply_categories(channels)
        self.assertEqual([c.group for c in channels], ["TV", "Cartoons", "Sports", "Movies"])

    def test_feeds_of_one_channel_sit_together_with_best_quality_first(self):
        channels = [channel("CNN (720p)", "News", "US", tvg_id="CNN.us"),
                    channel("CNN (1080p)", "News", "US", tvg_id="CNN.us"),
                    channel("CNBC", "News", "US", tvg_id="CNBC.us")]
        cc.apply_categories(channels)
        self.assertEqual([c.name for c in channels], ["CNBC", "CNN (1080p)", "CNN (720p)"])

    def test_display_name_keeps_identity_markers(self):
        self.assertEqual(cc.display_name("CNN (1080p)"), "CNN")
        self.assertEqual(cc.display_name("A&E Latin America (Brazil) (720p)"),
                         "A&E Latin America (Brazil)")
        self.assertEqual(cc.display_name("MeTV Toons (Alt)"), "MeTV Toons")

    def test_cap_feeds_keeps_the_best_and_respects_the_limit(self):
        channels = [channel("Nick (1080p)", "Kids", "US", tvg_id="Nickelodeon.us"),
                    channel("Nick (720p)", "Kids", "US", tvg_id="Nickelodeon.us"),
                    channel("Nick (480p)", "Kids", "US", tvg_id="Nickelodeon.us"),
                    channel("Other", "Kids", "US", tvg_id="Other.us")]
        cc.apply_categories(channels)
        kept = cc.cap_feeds(channels, 2)
        self.assertEqual([c.name for c in kept], ["Nick (1080p)", "Nick (720p)", "Other"])


class CountryPersistenceTest(unittest.TestCase):
    def test_group_country_is_persisted_before_the_group_is_replaced(self):
        ch = channel("Rai 1", "Italy")
        self.assertEqual(ch.country, "Italy")
        scraper.canonicalize_channels([ch])
        self.assertEqual(ch.attrs["group-title"], "TV")
        self.assertEqual(ch.attrs["tvg-country"], "IT")
        self.assertEqual(ch.country, "Italy")

    def test_synthetic_ids_are_not_read_as_country_codes(self):
        self.assertEqual(scraper.resolve_country(channel(
            "ET", "TV", tvg_id="premiumtv.international.et")), "International")
        self.assertEqual(scraper.resolve_country(channel(
            "Rai 1", "TV", tvg_id="premiumtv.italy.rai_1")), "Italy")
        # A real source id keeps its country suffix.
        self.assertEqual(scraper.resolve_country(channel("CCTV", "TV", tvg_id="CCTV1.cn")), "China")


class DeepCheckEvidenceTest(unittest.TestCase):
    def write_report(self, directory: Path, finished: datetime, dead: list[dict]) -> Path:
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / "link-check.json"
        path.write_text(json.dumps({
            "started_utc": finished.isoformat(timespec="seconds"),
            "finished_utc": finished.isoformat(timespec="seconds"),
            "per_playlist": {"playlists/PremiumTV.m3u": {"dead": dead}},
        }), encoding="utf-8")
        return path

    def test_fresh_dead_links_are_held_back(self):
        now = datetime.now(timezone.utc)
        with tempfile.TemporaryDirectory() as tmp:
            checks = Path(tmp)
            self.write_report(checks, now, [
                {"name": "Dead One", "url": "https://dead.example/1.m3u8",
                 "status": "offline", "reason": "HTTP 404"},
                {"name": "Slow One", "url": "https://slow.example/1.m3u8",
                 "status": "unreachable", "reason": "timeout"},
            ])
            alive = channel("Dead One", "News", url="https://dead.example/1.m3u8")
            slow = channel("Slow One", "News", url="https://slow.example/1.m3u8")
            self.assertEqual(scraper.apply_deep_check_evidence([alive, slow], checks), 1)
            self.assertEqual(alive.status, "dead")
            self.assertIn("HTTP 404", alive.reason)
            # Unreachable is transient and must never be treated as confirmed dead.
            self.assertEqual(slow.status, "unchecked")

    def test_stale_reports_are_ignored(self):
        old = datetime.now(timezone.utc) - timedelta(days=10)
        with tempfile.TemporaryDirectory() as tmp:
            checks = Path(tmp)
            self.write_report(checks, old, [
                {"name": "Dead One", "url": "https://dead.example/1.m3u8",
                 "status": "offline", "reason": "HTTP 404"},
            ])
            ch = channel("Dead One", "News", url="https://dead.example/1.m3u8")
            self.assertEqual(scraper.apply_deep_check_evidence([ch], checks, 72.0), 0)
            self.assertEqual(ch.status, "unchecked")

    def test_missing_report_is_not_a_problem(self):
        with tempfile.TemporaryDirectory() as tmp:
            ch = channel("Anything", "News")
            self.assertEqual(scraper.apply_deep_check_evidence([ch], Path(tmp)), 0)


class HeaderGuideLimitTest(unittest.TestCase):
    def test_published_playlists_keep_only_a_few_fallbacks(self):
        guides = ["https://upstream.example/%d.xml.gz" % i for i in range(50)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "published.m3u"
            scraper.write_m3u(path, [], guides, "published")
            header = path.read_text(encoding="utf-8").splitlines()[0]
            advertised = header.split('x-tvg-url="', 1)[1].rstrip('"').split(",")
            self.assertEqual(len(advertised), 1 + scraper.MAX_HEADER_GUIDES)
            self.assertEqual(advertised[0], scraper.SELF_EPG_URL)

    def test_source_caches_keep_the_full_upstream_guide_list(self):
        guides = ["https://upstream.example/%d.xml.gz" % i for i in range(50)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cache.m3u"
            scraper.write_m3u(path, [], guides, "cache", advertise_self=False)
            header = path.read_text(encoding="utf-8").splitlines()[0]
            self.assertEqual(len(header.split('x-tvg-url="', 1)[1].rstrip('"').split(",")), 50)

    def test_epg_build_patch_trims_a_hundred_guide_header(self):
        import epg_build
        guides = ["https://upstream.example/%d.xml.gz" % i for i in range(40)]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "PremiumTV.m3u"
            header_line = M3U_HEADER[:-1] + "," + ",".join(guides) + '"'
            path.write_text(f'{header_line}\n'
                            '#EXTINF:-1 group-title="News",Test\nhttps://x.test/1.m3u8\n',
                            encoding="utf-8")
            epg_build.patch_playlists([path], scraper.SELF_EPG_URL, set(), max_fallbacks=2)
            header = path.read_text(encoding="utf-8").splitlines()[0]
            advertised = header.split('x-tvg-url="', 1)[1].rstrip('"').split(",")
            self.assertEqual(advertised[0], scraper.SELF_EPG_URL)
            self.assertEqual(len(advertised), 3)


class ScraperPublishTest(unittest.TestCase):
    """The scraper publishes canonical categories, order and country metadata."""

    def test_published_playlist_is_categorised_and_country_stamped(self):
        source_text = "\n".join([
            "#EXTM3U",
            '#EXTINF:-1 tvg-country="US" group-title="Undefined",ESPN',
            "http://fixture.test/espn.m3u8",
            '#EXTINF:-1 group-title="Kids",Nickelodeon (720p)',
            "http://fixture.test/nick.m3u8",
            '#EXTINF:-1 group-title="Italy",Rai 1',
            "http://fixture.test/rai.m3u8",
            "",
        ])

        def alive(channel, *args, **kwargs):
            channel.status, channel.reason = "alive", "fixture"
            return channel

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cfg = root / "sources.json"
            cfg.write_text(json.dumps({"sources": [
                {"name": "fixture", "type": "m3u", "url": "http://fixture.test/source.m3u"},
            ]}), encoding="utf-8")
            out = root / "playlists"
            args = ["scraper.py", "--sources", str(cfg), "--out", str(out),
                    "--workers", "2", "--timeout", "1"]
            from unittest.mock import patch
            with patch.object(sys, "argv", args), \
                 patch.object(scraper, "fetch_source_text", return_value=source_text), \
                 patch.object(scraper, "check_channel", side_effect=alive), \
                 redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)

            text = (out / "PremiumTV.m3u").read_text(encoding="utf-8")
            entries = [line for line in text.splitlines() if line.startswith("#EXTINF")]
            self.assertEqual(len(entries), 3)
            # TV first, then Cartoons, then Sports - and the country signal that
            # used to live in the group is now explicit.
            self.assertIn('group-title="TV"', entries[0])
            self.assertIn("Rai 1", entries[0])
            self.assertIn('tvg-country="IT"', entries[0])
            self.assertIn('group-title="Cartoons"', entries[1])
            self.assertIn("Nickelodeon", entries[1])
            self.assertIn('group-title="Sports"', entries[2])
            self.assertIn("ESPN", entries[2])

            status = (out / "STATUS.md").read_text(encoding="utf-8")
            self.assertIn("## Channel categories", status)
            self.assertIn("| Cartoons | 1 |", status)
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["categories"],
                             {"TV": 1, "Cartoons": 1, "Sports": 1})

            countries = (out / "countries" / "Italy.m3u").read_text(encoding="utf-8")
            self.assertIn("Rai 1", countries)
            usa = (out / "countries" / "USA.m3u").read_text(encoding="utf-8")
            self.assertNotIn("Rai 1", usa)


class LinkCheckTidyTest(unittest.TestCase):
    def test_patched_playlist_is_re_sorted_and_regrouped(self):
        text = "\n".join([
            M3U_HEADER,
            '#EXTINF:-1 group-title="Undefined",ESPN',
            "https://x.test/espn.m3u8",
            '#EXTINF:-1 group-title="Undefined",CNN (1080p)',
            "https://x.test/cnn.m3u8",
            "",
        ])
        header, blocks = link_check.split_blocks(text)
        blocks, changed = link_check.tidy_blocks(blocks, "test")
        rendered = link_check.blocks_to_text(header, blocks)
        self.assertEqual(changed, 2)
        # Sports sorts before News in the canonical category order.
        self.assertLess(rendered.index("ESPN"), rendered.index("CNN"))
        self.assertIn('group-title="News"', rendered)
        self.assertIn('group-title="Sports"', rendered)


class ResortPlaylistsTest(unittest.TestCase):
    def test_resort_rewrites_groups_prunes_dead_and_regenerates_countries(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "playlists"
            out.mkdir()
            (out / "checks").mkdir()
            (out / "PremiumTV.m3u").write_text("\n".join([
                M3U_HEADER,
                '#EXTINF:-1 tvg-id="CNN.us" tvg-country="US" group-title="Undefined",CNN (1080p)',
                "https://x.test/cnn.m3u8",
                '#EXTINF:-1 tvg-id="Rai1.it" group-title="Italy",Rai 1',
                "https://x.test/rai.m3u8",
                '#EXTINF:-1 tvg-id="Dead.us" tvg-country="US" group-title="General",Old Channel',
                "https://x.test/dead.m3u8",
                "",
            ]), encoding="utf-8")
            main_text_with_ae = (out / "PremiumTV.m3u").read_text(encoding="utf-8")
            (out / "PremiumTV.m3u").write_text(main_text_with_ae + "\n".join([
                '#EXTINF:-1 tvg-id="AE.us@East" tvg-country="US" group-title="A&E Networks",A&E (US East)',
                "https://x.test/ae-live.m3u8",
                "",
            ]), encoding="utf-8")
            (out / "AE_Channels.m3u").write_text("\n".join([
                M3U_HEADER,
                '#EXTINF:-1 tvg-id="AE.us@East" tvg-country="US" group-title="A&E Networks",A&E (US East)',
                "https://x.test/ae.m3u8",
                "",
            ]), encoding="utf-8")
            (out / "checks" / "link-check.json").write_text(json.dumps({
                "finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "per_playlist": {"playlists/PremiumTV.m3u": {"dead": [
                    {"name": "Old Channel", "url": "https://x.test/dead.m3u8",
                     "status": "offline", "reason": "HTTP 404"},
                ]}},
            }), encoding="utf-8")

            with redirect_stdout(StringIO()):
                self.assertEqual(resort_playlists.main(["--out", str(out)]), 0)

            main_text = (out / "PremiumTV.m3u").read_text(encoding="utf-8")
            self.assertNotIn("dead.m3u8", main_text)
            self.assertIn('group-title="TV"', main_text)
            self.assertIn('group-title="News"', main_text)
            # TV comes before News, so the Italian general channel leads.
            self.assertLess(main_text.index("Rai 1"), main_text.index("CNN"))

            self.assertTrue((out / "countries" / "USA.m3u").exists())
            italy = (out / "countries" / "Italy.m3u").read_text(encoding="utf-8")
            self.assertIn("Rai 1", italy)
            self.assertNotIn("CNN", italy)
            index = (out / "countries" / "README.md").read_text(encoding="utf-8")
            self.assertIn("USA.m3u", index)

            ae_text = (out / "AE_Channels.m3u").read_text(encoding="utf-8")
            self.assertIn("A&E (US East)", ae_text)
            log_text = (out / "logs" / "resort-log.txt").read_text(encoding="utf-8")
            self.assertIn("dead.m3u8", log_text)


class VerifyPlaylistsTest(unittest.TestCase):
    def build(self, tmp: str) -> Path:
        out = Path(tmp) / "playlists"
        (out / "countries").mkdir(parents=True)
        (out / "checks").mkdir()
        guide = Path(tmp) / "EPG"
        guide.mkdir()
        (guide / "PremiumTV.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?><tv>'
            '<channel id="CNN.us"><display-name>CNN</display-name></channel>'
            '</tv>', encoding="utf-8")
        (out / "PremiumTV.m3u").write_text("\n".join([
            M3U_HEADER,
            '#EXTINF:-1 tvg-id="CNN.us" tvg-country="US" group-title="News",CNN',
            "https://x.test/cnn.m3u8",
            "",
        ]), encoding="utf-8")
        return out

    def run_verify(self, out: Path, extra: list | None = None) -> int:
        args = ["--out", str(out), "--epg-dir", str(out.parent / "EPG")] + (extra or [])
        with redirect_stdout(StringIO()):
            return verify_playlists.main(args)

    def test_clean_playlist_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self.build(tmp)
            self.assertEqual(self.run_verify(out), 0)
            report = json.loads((out / "checks" / "verify.json").read_text(encoding="utf-8"))
            entry = next(item for item in report["playlists"]
                         if item["file"].endswith("PremiumTV.m3u"))
            self.assertEqual(entry["issues"], [])
            self.assertEqual(entry["non_canonical_groups"], {})
            self.assertEqual(entry["epg"]["matched_ids"], 1)
            self.assertIn("Playlist and guide verification",
                          (out / "checks" / "VERIFY.md").read_text(encoding="utf-8"))

    def test_non_canonical_group_and_dead_link_are_reported(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = self.build(tmp)
            (out / "PremiumTV.m3u").write_text("\n".join([
                M3U_HEADER,
                '#EXTINF:-1 tvg-id="CNN.us" tvg-country="US" group-title="Undefined",CNN',
                "https://x.test/cnn.m3u8",
                '#EXTINF:-1 tvg-id="Dead.us" tvg-country="US" group-title="General",Old',
                "https://x.test/dead.m3u8",
                "",
            ]), encoding="utf-8")
            (out / "checks" / "link-check.json").write_text(json.dumps({
                "finished_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "per_playlist": {"playlists/PremiumTV.m3u": {"dead": [
                    {"name": "Old", "url": "https://x.test/dead.m3u8",
                     "status": "offline", "reason": "HTTP 404"},
                ]}},
            }), encoding="utf-8")
            self.assertEqual(self.run_verify(out, ["--strict"]), 1)
            report = json.loads((out / "checks" / "verify.json").read_text(encoding="utf-8"))
            entry = next(item for item in report["playlists"]
                         if item["file"].endswith("PremiumTV.m3u"))
            self.assertTrue(entry["issues"])
            self.assertEqual(len(entry["dead_links"]), 1)
            self.assertIn("Undefined", entry["non_canonical_groups"])


if __name__ == "__main__":
    unittest.main()
