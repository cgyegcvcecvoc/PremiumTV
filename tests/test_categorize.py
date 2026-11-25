"""Offline tests for the category taxonomy (scripts/categorize.py)."""
import copy
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

    def test_a_and_e_channels_share_one_category(self):
        # "Crime 360" used to be filed under Documentary because of the word
        # "crime"; A&E's own shows and channels all belong in one spot.
        for name in ("A&E Crime 360 (Pluto TV)", "Crime 360 (720p)",
                     "Cold Case Files by A&E (Roku)", "Crime & Investigation Network (US)",
                     "60 Days In by A&E (720p)", "Alone by History / A&E (720p)"):
            with self.subTest(name=name):
                self.assertEqual(categorize.classify(name, "Documentary"), "A&E Networks")
        # The broad documentary vocabulary still owns history/nature channels.
        self.assertEqual(categorize.classify("History Hit (720p)"), "Documentary")

    def test_bbc_america_is_entertainment_not_news(self):
        self.assertEqual(categorize.classify("BBC America", "News", "BBC.America.HD.us2"),
                         "Entertainment")
        self.assertEqual(categorize.classify("BBC News", "News"), "News")

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

    def test_backup_names_stay_unique_across_name_casing(self):
        # The international MOVIEDOME feed and the US Moviedome feed clean up to
        # the same name in different case. Their spare links must not both be
        # published as "MOVIEDOME/Moviedome (Backup 1)".
        channels = [
            channel("MOVIEDOME", "Movies", "premiumtv.international.moviedome", "http://a/1", ""),
            channel("MOVIEDOME", "Movies", "premiumtv.international.moviedome", "http://a/2", ""),
            channel("Moviedome (720p)", "Movies", "Moviedome.us@Germany", "http://b/1", "US"),
            channel("Moviedome (540p)", "Movies", "Moviedome.us@Germany", "http://b/2", "US"),
        ]
        _, backups = categorize.split_primary_backups(channels)
        names = [item.name for item in backups]
        self.assertEqual(len(names), len(set(names)))
        lowered = [name.lower() for name in names]
        self.assertEqual(len(lowered), len(set(lowered)), names)

    def test_rebuilding_a_rebuilt_playlist_keeps_the_same_names(self):
        # The scraper publishes a playlist that a later pass may rebuild. Name
        # assignment must not depend on the order the spare names happen to be
        # in, or every rebuild would renumber the backups.
        channels = [
            channel("Billiard TV", "Sports", "premiumtv.international.billiard_tv", "http://a/1", ""),
            channel("Billiard TV", "Sports", "premiumtv.international.billiard_tv", "http://a/2", ""),
            channel("Billiard TV (1080p) [Geo-blocked]", "Sports", "BilliardTV.us@SD", "http://b/1", "US"),
            channel("Billiard TV (720p)", "Sports", "BilliardTV.us@SD", "http://b/2", "US"),
            channel("Бильярд (1080p)", "Sports", "premiumtv.international.billiard_tv", "http://c/1", "RU"),
            channel("Бильярд (720p)", "Sports", "premiumtv.international.billiard_tv", "http://c/2", "RU"),
        ]
        primary, backups = categorize.split_primary_backups(copy.deepcopy(channels))
        first = {ch.url: ch.name for ch in primary + backups}
        primary2, backups2 = categorize.split_primary_backups(copy.deepcopy(primary + backups))
        second = {ch.url: ch.name for ch in primary2 + backups2}
        self.assertEqual(first, second)

    def test_different_countries_stay_separate_channels(self):
        channels = [
            channel("Nickelodeon (720p)", "Kids", "Nickelodeon.us", "http://a/1.m3u8", "US"),
            channel("Nickelodeon (720p)", "Kids", "Nickelodeon.br", "http://b/2.m3u8", "BR"),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 2)
        self.assertEqual(backups, [])

    def test_existing_backup_lineage_beats_conflicting_inferred_country(self):
        # Regression from the 2026-11-09 scrape: Monster Jam's primary carried
        # explicit PL metadata, while an already-published backup omitted
        # tvg-country and therefore resolved its shared ``.us`` guide id to US.
        # A rebuild promoted "Backup 5" into Sports as another primary, making
        # audit_backups --strict fail after every otherwise successful scrape.
        channels = [
            channel("Monster Jam (720p)", "Sports", "MonsterJam.us@SD",
                    "https://example.test/primary.m3u8", "PL"),
            channel("Monster Jam (Backup 5)", "Sports Backups", "MonsterJam.us@SD",
                    "https://example.test/backup.m3u8", ""),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual([item.url for item in primary],
                         ["https://example.test/primary.m3u8"])
        self.assertEqual([item.url for item in backups],
                         ["https://example.test/backup.m3u8"])
        self.assertEqual(backups[0].name, "Monster Jam (Backup 1)")
        self.assertEqual(backups[0].attrs["group-title"], "Sports Backups")

    def test_tagged_backup_does_not_cross_an_ambiguous_shared_id(self):
        # A bad upstream id reused by two real regional channels is not enough
        # to decide which one owns a tagged spare. Country separation wins.
        channels = [
            channel("Demo Sports", "Sports", "Demo.shared", "http://a/1", "US"),
            channel("Demo Sports", "Sports", "Demo.shared", "http://b/1", "BR"),
            channel("Demo Sports (Backup 1)", "Sports Backups", "Demo.shared", "http://c/1", "CA"),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 3)
        self.assertEqual(backups, [])

    def test_blank_country_merges_with_the_named_feed(self):
        # An upstream entry with no tvg-country is the same station, not a
        # second channel: it must become a backup, not stand alone with no
        # feed to fail over to.
        channels = [
            channel("Fuel TV (1080p)", "Sports", "FuelTV.at", "http://a/1.m3u8", "AT"),
            channel("Fuel TV (720p)", "Sports", "FuelTV.at", "http://b/2.m3u8", ""),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 1)
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].name, "Fuel TV (Backup 1)")
        self.assertEqual(backups[0].attrs.get("tvg-id"), "FuelTV.at")

    def test_blank_country_stays_own_group_when_countries_conflict(self):
        # With two different real countries present, an unknown-country entry
        # is ambiguous and must not be folded into either one.
        channels = [
            channel("ESPN2 (720p)", "Sports", "ESPN2.us", "http://a/1.m3u8", "US"),
            channel("ESPN2 (720p)", "Sports", "ESPN2.br", "http://b/2.m3u8", "BR"),
            channel("ESPN2 (540p)", "Sports", "ESPN2.unknown", "http://c/3.m3u8", ""),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 3)
        self.assertEqual(backups, [])

    def test_max_backups_caps_the_spares(self):
        channels = [channel(f"NFL Network (feed {index})", "TV", url=f"http://x/{index}.m3u8")
                    for index in range(5)]
        primary, backups = categorize.split_primary_backups(channels, max_backups=2)
        self.assertEqual(len(primary), 1)
        self.assertEqual(len(backups), 2)

    def test_backup_names_stay_unique_when_two_feeds_share_a_display_name(self):
        # International and US feeds of the same station have different ids but
        # clean up to the same display name. Numbering used to restart at 1 for
        # each identity group, publishing two different streams as "X (Backup 1)".
        channels = [
            channel("World Poker Tour (1080p)", "Sports", "WorldPokerTour.us", "http://a/1", "US"),
            channel("World Poker Tour (720p)", "Sports", "WorldPokerTour.us", "http://a/2", "US"),
            channel("World Poker Tour (1080p)", "Sports", "world_poker_tour.de", "http://b/1", "DE"),
            channel("World Poker Tour (720p)", "Sports", "world_poker_tour.de", "http://b/2", "DE"),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 2)
        self.assertEqual([item.name for item in backups],
                         ["World Poker Tour (Backup 1)", "World Poker Tour (Backup 2)"])


class ProviderDedupTest(unittest.TestCase):
    """TV-network copies of one channel become one channel plus backups."""

    def test_crime_360_folds_every_provider_into_one_channel(self):
        # The regression this rule exists for: the A&E shelf published six
        # "A&E Crime 360 (LG)" / "(Vizio)" / "(Xumo)" / "(Pluto TV)" entries
        # side by side, plus "Crime 360", "Crime 360 (720p)" and "Crime 360 by
        # A&E" under three more names. They are one channel.
        channels = [
            channel("A&E Crime 360", "A&E Networks", "", "http://a/0.m3u8", "US"),
            channel("A&E Crime 360 (LG)", "A&E Networks", "Crime360.us@LG", "http://a/1.m3u8", "US"),
            channel("A&E Crime 360 (Pluto TV)", "A&E Networks", "Crime360.us@SD", "http://a/2.m3u8", "US"),
            channel("A&E Crime 360 (Vizio)", "A&E Networks", "Crime360.us@Vizio", "http://a/3.m3u8", "US"),
            channel("A&E Crime 360 (Xumo)", "A&E Networks", "Crime360.us@Xumo", "http://a/4.m3u8", "US"),
            channel("Crime 360 by A&E", "A&E Networks", "", "http://a/5.m3u8", ""),
            channel("Crime 360 (720p)", "A&E Networks", "Crime360.us@SD", "http://a/6.m3u8", "US"),
            channel("Crime 360 (Canada)", "A&E Networks", "CA4700015P1", "http://ca/1.m3u8", "CA"),
        ]
        primary, backups = categorize.split_primary_backups(channels)
        # The seven US feeds are one channel; the Canadian network copy is a
        # second channel, not a backup.
        self.assertEqual(sorted(item.url for item in primary),
                         ["http://a/6.m3u8", "http://ca/1.m3u8"])
        self.assertEqual(primary[0].attrs["group-title"], "A&E Networks")
        self.assertEqual(len(backups), 6)
        self.assertTrue(all(item.attrs["group-title"] == "A&E Networks Backups"
                            for item in backups))
        # The one feed that claims a resolution is the best of them.
        self.assertEqual(primary[0].url, "http://a/6.m3u8")
        names = [item.name for item in backups]
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(names, [f"Crime 360 (Backup {index})" for index in range(1, 7)])

    def test_a_brand_suffix_is_not_a_quality_penalty(self):
        # "Crime 360 by A&E" used to score below "Crime 360 (Xumo)" because the
        # duplicate-marker penalty matched the "A&E" in the suffix.
        self.assertEqual(categorize.quality_score("Crime 360 by A&E"), 0)
        self.assertGreater(categorize.quality_score("Crime 360 (720p)"), 0)

    def test_regional_variants_stay_separate_channels(self):
        channels = [
            channel("Crime 360 (720p)", "A&E Networks", "Crime360.us@SD", "http://a/1", "US"),
            channel("Crime 360 (UK)", "A&E Networks", "Crime360.uk@SD", "http://b/1", "UK"),
            channel("Crime 360 (Canada)", "A&E Networks", "Crime360.ca@SD", "http://c/1", "CA"),
        ]
        primary, _ = categorize.split_primary_backups(channels)
        self.assertEqual(len(primary), 3)


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
        # The distribution platform is a tag, not part of the station's name.
        self.assertEqual(categorize.clean_display_name("Fox News (Xumo) (720p)"), "Fox News")

    def test_provider_tags_collapse_to_one_channel(self):
        """One station seen through several free providers is one channel."""
        for name in ("A&E Crime 360", "A&E Crime 360 (LG)", "A&E Crime 360 (Pluto TV)",
                     "A&E Crime 360 (Vizio)", "A&E Crime 360 (Xumo)",
                     "A&E Crime 360 (Pluto TV Alt)", "A&E Crime 360 (Roku)",
                     "A&E Crime 360 (Samsung TV Plus)", "A&E Crime 360 (Tubi)",
                     "A&E Crime 360 (Plex)", "A&E Crime 360 (720p)"):
            with self.subTest(name=name):
                self.assertEqual(categorize.clean_display_name(name), "Crime 360")
        self.assertEqual(categorize.clean_display_name("Crime 360 by A&E"), "Crime 360")
        self.assertEqual(categorize.clean_display_name("Cold Case Files by A&E (Tubi)"),
                         "Cold Case Files")
        self.assertEqual(categorize.clean_display_name("Modern Marvels Presented by HISTORY"),
                         "Modern Marvels")
        self.assertEqual(categorize.clean_display_name("Home.Made.Nation by A&E (Samsung)"),
                         "Home.Made.Nation")

    def test_words_that_identify_another_channel_are_not_tags(self):
        """A country or region must keep two feeds apart; a resolution must not."""
        for name, cleaned in (
            ("Crime 360 (UK)", "Crime 360 (UK)"),
            ("Crime + Investigation Asia (720p)", "Crime + Investigation Asia"),
            ("History (Poland) (576i)", "History (Poland)"),
            ("A&E Networks Brazil", "A&E Networks Brazil"),
            ("A&E Latin America", "A&E Latin America"),
            ("A&E", "A&E"),
            ("A&E Latin America (1080p)", "A&E Latin America"),
            ("Crime & Investigation Network (US)", "Crime & Investigation Network (US)"),
            ("A&E Latin America Brazil (720p)", "A&E Latin America Brazil"),
        ):
            with self.subTest(name=name):
                self.assertEqual(categorize.clean_display_name(name), cleaned)
        # A brand word that starts the title is not a suffix.
        self.assertEqual(categorize.clean_display_name("Love Crime & History"),
                         "Love Crime & History")
        self.assertEqual(categorize.clean_display_name("History 2 Latin America (1080p)"),
                         "History 2 Latin America")

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
