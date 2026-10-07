"""Offline tests for the category taxonomy (scripts/categorize.py)."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import categorize  # noqa: E402
import scraper  # noqa: E402


def channel(name, group="", tvg_id="", url=None, country=""):
    attrs = {}
    if tvg_id:
        attrs["tvg-id"] = tvg_id
    if group:
        attrs["group-title"] = group
    if country:
        attrs["tvg-country"] = country
    return scraper.Channel(name=name, url=url or f"http://example.com/{abs(hash(name))}.m3u8",
                           source="test", attrs=attrs)


class ClassificationTest(unittest.TestCase):
    """The nine curated categories, recognised by what a channel actually is."""

    def test_nfl_network_is_sports_not_tv(self):
        # The regression this module exists for: the index shipped it in "TV".
        self.assertEqual(categorize.classify("NFL Network", "TV", "NFL.Network.HD.us2"),
                         "Sports")
        self.assertEqual(categorize.classify("[American Football] NFL Network | English (STRMCNTR)",
                                             "Live Events"), "Sports")

    def test_league_and_network_channels_are_sports(self):
        for name in ("ESPN", "ESPN2", "FS1", "Fox Sports 1", "CBS Sports Network",
                     "beIN Sports 1", "NBA TV", "MLB Network",
                     "Premier League TV", "UFC Fight Pass", "NASCAR on Fox"):
            with self.subTest(name=name):
                self.assertEqual(categorize.classify(name), "Sports")

    def test_nbc_sports_is_its_own_category(self):
        for name in ("NBC Sports", "NBC Sports Philadelphia", "Golf Channel", "NBCSN",
                     "Golf Channel Latin America"):
            with self.subTest(name=name):
                self.assertEqual(categorize.classify(name), "NBC Sports Channels")

    def test_network_families(self):
        self.assertEqual(categorize.classify("Fox News", "News"), "Fox Channels")
        self.assertEqual(categorize.classify("Fox 29 (WTXF) - Philadelphia PA (1080p)"),
                         "Fox Channels")
        self.assertEqual(categorize.classify("CBS News 24/7"), "CBS")
        self.assertEqual(categorize.classify("CBS 21 (WHP)"), "CBS")
        self.assertEqual(categorize.classify("NBC (Eastern Feed)"), "NBC")
        self.assertEqual(categorize.classify("CNBC"), "NBC")
        self.assertEqual(categorize.classify("Bravo Vault"), "NBC")

    def test_cartoons_are_not_kids(self):
        for name in ("Cartoon Network", "Boomerang", "Adult Swim", "MeTV Toons",
                     "Nicktoons", "Toonami", "Cartoonito"):
            with self.subTest(name=name):
                self.assertEqual(categorize.classify(name), "Cartoons")

    def test_pbs_and_game_shows_have_their_own_categories(self):
        self.assertEqual(categorize.classify("PBS Kids Eastern/Central (720p)"), "PBS")
        self.assertEqual(categorize.classify("WVIA PBS (1080p)"), "PBS")
        self.assertEqual(categorize.classify("Buzzr (1080p)", "Entertainment"), "Game Shows")
        self.assertEqual(categorize.classify("Game Show Network"), "Game Shows")

    def test_lifestyle_channels(self):
        for name in ("HGTV", "Food Network", "Travel Channel", "The Cooking Channel",
                     "Hallmark Channel"):
            with self.subTest(name=name):
                self.assertEqual(categorize.classify(name), "Lifestyle")

    def test_kids_brand_stays_kids(self):
        self.assertEqual(categorize.classify("Nickelodeon (United States) (720p)", "TV"), "Kids")

    def test_classification_is_idempotent(self):
        """A second pass must not re-interpret an assigned category."""
        channels = [channel("NFL Network", "TV"), channel("PBS Kids", "Undefined")]
        categorize.assign_categories(channels)
        first = [item.attrs["group-title"] for item in channels]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(first, [item.attrs["group-title"] for item in primary])

    def test_country_group_becomes_international(self):
        self.assertEqual(categorize.normalize_group("Italy"), "International")
        self.assertEqual(categorize.normalize_group("日本 Japan"), "International")

    def test_generic_groups_carry_nothing(self):
        for group in ("General", "Undefined", "TV", "", "Diversos"):
            with self.subTest(group=group):
                self.assertEqual(categorize.normalize_group(group), "")

    def test_decorated_groups_are_cleaned_up(self):
        self.assertEqual(categorize.normalize_group("Sports 🌍"), "Sports")
        self.assertEqual(categorize.normalize_group("Doc & History 🏛️"), "Documentary")
        self.assertEqual(categorize.normalize_group("Films 📽️"), "Movies")
        self.assertEqual(categorize.normalize_group("Music • Stingray"), "Music")
        self.assertEqual(categorize.normalize_group("Culture Education"), "Culture")
        self.assertEqual(categorize.normalize_group("Live Events"), "Sports")

    def test_unknown_channel_falls_back_to_its_region(self):
        self.assertEqual(categorize.classify("Kos TV (720p)", "General", "KosTV.gr@SD"), "Europe")
        self.assertEqual(categorize.classify("Almaty TV (576p)", "", "AlmatyTV.kz@SD"), "Asia")


class BackupTest(unittest.TestCase):
    """Duplicate links become backups instead of cluttering the category."""

    def test_duplicates_move_to_the_backup_group(self):
        channels = [
            channel("NFL Network (1080p)", "TV", "NFL.Network.HD.us2", "http://a/1.m3u8"),
            channel("NFL Network (720p)", "TV", "NFL.Network.HD.us2", "http://b/2.m3u8"),
            channel("NFL Network (Alt)", "TV", "NFL.Network.HD.us2", "http://c/3.m3u8"),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 1)
        self.assertEqual(len(backups), 2)
        self.assertEqual(primary[0].attrs["group-title"], "Sports")
        self.assertTrue(all(item.attrs["group-title"] == "Sports Backups" for item in backups))
        # The highest-quality link stays in front.
        self.assertEqual(primary[0].url, "http://a/1.m3u8")
        self.assertEqual([item.name for item in backups],
                         ["NFL Network (Backup 1)", "NFL Network (Backup 2)"])
        # Backups share the primary's guide id so a player keeps the schedule.
        self.assertTrue(all(item.attrs.get("tvg-id") == "NFL.Network.HD.us2"
                            for item in backups))

    def test_different_countries_stay_separate_channels(self):
        channels = [
            channel("Nickelodeon (720p)", "Kids", "Nickelodeon.us", "http://a/1.m3u8", "US"),
            channel("Nickelodeon (720p)", "Kids", "Nickelodeon.br", "http://b/2.m3u8", "BR"),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 2)
        self.assertEqual(backups, [])

    def test_max_backups_caps_the_spares(self):
        channels = [channel(f"NFL Network (feed {index})", "TV", url=f"http://x/{index}.m3u8")
                    for index in range(5)]
        primary, backups = categorize.split_primary_backups(channels, max_backups=2)
        self.assertEqual(len(primary), 1)
        self.assertEqual(len(backups), 2)


class OrderTest(unittest.TestCase):
    """The published order is the curated order, backups right behind."""

    def test_curated_categories_come_first_in_order(self):
        counts = {category: 1 for category in categorize.CURATED_CATEGORIES}
        counts.update({"Music": 900, "News": 900, categorize.OTHER: 10})
        order = categorize.order_categories(counts)
        self.assertEqual(order[:len(categorize.CURATED_CATEGORIES)],
                         list(categorize.CURATED_CATEGORIES))
        self.assertEqual(order[-1], categorize.OTHER)

    def test_backup_group_follows_its_category(self):
        counts = {"Sports": 5, "Sports Backups": 2, "Music": 9, "Music Backups": 1}
        order = categorize.order_categories(counts)
        self.assertEqual(order, ["Sports", "Sports Backups", "Music", "Music Backups"])

    def test_long_tail_is_sorted_by_size(self):
        counts = {"Movies": 10, "Music": 900, "News": 90, "Sports": 1}
        order = categorize.order_categories(counts)
        self.assertEqual(order[-3:], ["Music", "News", "Movies"])

    def test_build_main_order_keeps_every_link(self):
        channels = [
            channel("NFL Network (1080p)", "TV", "NFL.Network.HD.us2", "http://a/1.m3u8"),
            channel("NFL Network (720p)", "TV", "NFL.Network.HD.us2", "http://b/2.m3u8"),
            channel("Fox News", "News", "FoxNews.us", "http://c/3.m3u8"),
            channel("Music Choice", "Music", "MusicChoice.us", "http://d/4.m3u8"),
        ]
        ordered = categorize.build_main_order(channels)
        self.assertEqual(len(ordered), 4)
        self.assertEqual([item.attrs["group-title"] for item in ordered],
                         ["Sports", "Sports Backups", "Fox Channels", "Music"])


class VotingTest(unittest.TestCase):
    """When this index says "General" and everyone else says "Music", Music wins."""

    def setUp(self):
        categorize.set_group_votes(None)

    def tearDown(self):
        categorize.set_group_votes(None)

    def test_vote_is_used_when_the_own_group_says_nothing(self):
        corpus = [channel("Kos TV (720p)", "General"), channel("Kos TV (720p)", "Music"),
                  channel("Kos TV (720p)", "Music")]
        categorize.set_group_votes(categorize.build_group_votes(corpus))
        self.assertEqual(categorize.classify("Kos TV (720p)", "General"), "Music")

    def test_own_group_wins_over_a_vote(self):
        corpus = [channel("Kos TV (720p)", "News"), channel("Kos TV (720p)", "Music")]
        categorize.set_group_votes(categorize.build_group_votes(corpus))
        self.assertEqual(categorize.classify("Kos TV (720p)", "News"), "News")

    def test_generic_groups_never_vote(self):
        corpus = [channel("Kos TV (720p)", "General"), channel("Kos TV (720p)", "Undefined")]
        votes = categorize.build_group_votes(corpus)
        self.assertEqual(votes, {})


class DuplicateUrlTest(unittest.TestCase):
    """One stream, one entry: the verifier treats a repeated URL as a fault."""

    def test_a_url_supported_name_survives(self):
        first = channel("Nickelodeon (Brazil) (480p)",
                        url="https://stmv2.srvif.com/nicktoons/nicktoons/playlist.m3u8")
        second = channel("NickToons Brasil (480p)",
                         url="https://stmv2.srvif.com/nicktoons/nicktoons/playlist.m3u8")
        kept, dropped = categorize.dedupe_urls([first, second])
        self.assertEqual(dropped, 1)
        self.assertEqual([item.name for item in kept], ["NickToons Brasil (480p)"])

    def test_first_entry_wins_when_the_url_supports_neither_name(self):
        first = channel("ESPN", url="http://example.com/a.m3u8")
        second = channel("ESPN (Backup 1)", url="http://example.com/a.m3u8")
        kept, dropped = categorize.dedupe_urls([first, second])
        self.assertEqual(dropped, 1)
        self.assertEqual([item.name for item in kept], ["ESPN"])

    def test_a_dropped_entry_still_passes_on_metadata(self):
        first = channel("NickToons Brasil", url="https://host/nicktoons/live.m3u8",
                        tvg_id="NickToons.br")
        second = channel("Nickelodeon Brazil", url="https://host/nicktoons/live.m3u8",
                         country="BR")
        kept, _ = categorize.dedupe_urls([first, second])
        self.assertEqual(kept[0].attrs.get("tvg-country"), "BR")

    def test_entries_without_a_url_are_dropped(self):
        empty = scraper.Channel(name="No URL", url="", source="test", attrs={})
        kept, dropped = categorize.dedupe_urls([empty])
        self.assertEqual(kept, [])
        self.assertEqual(dropped, 1)

    def test_distinct_urls_are_left_alone(self):
        kept, dropped = categorize.dedupe_urls([
            channel("ESPN", url="http://example.com/espn.m3u8"),
            channel("ESPN (Backup 1)", url="http://example.com/espn-2.m3u8")])
        self.assertEqual(dropped, 0)
        self.assertEqual(len(kept), 2)


class NamingTest(unittest.TestCase):

    def test_clean_display_name_drops_quality_tags(self):
        self.assertEqual(categorize.clean_display_name("NFL Network (1080p)"), "NFL Network")
        self.assertEqual(categorize.clean_display_name("A&E Latin America (Alt)"),
                         "A&E Latin America")
        self.assertEqual(categorize.clean_display_name("Fox News (Xumo) (720p)"),
                         "Fox News (Xumo)")

    def test_quality_score_prefers_higher_resolution(self):
        self.assertGreater(categorize.quality_score("NFL Network (1080p)"),
                           categorize.quality_score("NFL Network (480p)"))
        self.assertGreater(categorize.quality_score("NFL Network (720p)"),
                           categorize.quality_score("NFL Network (Backup)"))

    def test_channel_key_ignores_quality_but_not_country(self):
        self.assertEqual(categorize.channel_key("NFL Network (1080p)", "US"),
                         categorize.channel_key("NFL Network (720p)", "US"))
        self.assertNotEqual(categorize.channel_key("NFL Network", "US"),
                            categorize.channel_key("NFL Network", "BR"))

    def test_backup_group_naming(self):
        self.assertEqual(categorize.backup_group("Sports"), "Sports Backups")
        self.assertTrue(categorize.is_backup_group("Sports Backups"))
        self.assertEqual(categorize.base_category("Sports Backups"), "Sports")


if __name__ == "__main__":
    unittest.main()
