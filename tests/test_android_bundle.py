"""Offline tests for android/tools/build_bundle.py.

These guard the bridge between the repository and the APK: if the bundler
silently starts dropping headers, mis-parsing timestamps or emitting a bundle
whose programme rows point at channels that no longer exist, the app ships
wrong data and nothing in the Gradle build would notice.

Timestamps in the fixtures are generated relative to the current clock, so the
"drop listings that have already finished" rule is exercised rather than
sidestepped by a hard-coded date that would eventually go stale.
"""

import json
import os
import sys
import tempfile
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "android" / "tools"))
import build_bundle  # noqa: E402

# One hour from now: comfortably inside the window the bundler keeps.
BASE = int(time.time()) + 3600
# A listing that finished seven hours ago: past the six hour grace window the
# bundler keeps, so it must be dropped.
PAST = int(time.time()) - 8 * 3600
# A listing that ended an hour ago: still inside the grace window, so a viewer
# can see what was on. It must be kept.
RECENT = int(time.time()) - 2 * 3600


def stamp(epoch, offset_hours=0, offset_minutes=0):
    """Format an instant as an XMLTV timestamp, optionally in another offset."""
    shift = offset_hours * 3600 + offset_minutes * 60
    moment = datetime.fromtimestamp(epoch + shift, timezone.utc)
    sign = "-" if shift < 0 else "+"
    return "%s %s%02d%02d" % (
        moment.strftime("%Y%m%d%H%M%S"),
        sign,
        abs(offset_hours),
        abs(offset_minutes),
    )


PLAYLIST = """#EXTM3U x-tvg-url="https://example.invalid/one.xml,https://example.invalid/two.xml"
# 3 channels
#EXTINF:-1 tvg-id="Sports.One.us" tvg-logo="https://logo/one.png" group-title="Sports" tvg-country="US" tvg-chno="7",☆ One Sports (1080p)
https://stream.example/one.m3u8
#EXTINF:-1 tvg-id="Needs.Headers.us" tvg-name="Headers" group-title="Movies",Needs Headers TV
#EXTVLCOPT:http-referrer=https://referrer.example
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Test)
#KODIPROP:http-origin=https://origin.example
http://stream.example/needs.ts
#EXTINF:-1 group-title="Sports",No Id Channel
https://stream.example/noid.m3u8
"""

GUIDE = """<?xml version="1.0" encoding="UTF-8"?>
<tv generator-info-name="test">
  <channel id="Sports.One.us"><display-name>One Sports</display-name></channel>
  <channel id="Needs.Headers.us"><display-name>Needs Headers TV</display-name></channel>
  <channel id="Not.In.The.Playlist"><display-name>Orphan</display-name></channel>
  <programme start="%(morning_start)s" stop="%(morning_end)s" channel="Sports.One.us">
    <title>Morning Sports</title>
    <desc>Desc &amp; more</desc>
    <category lang="en">Football</category>
    <category lang="en">Sports talk</category>
    <icon src="https://art/one.jpg" />
  </programme>
  <programme start="%(offset_start)s" stop="%(offset_end)s" channel="Needs.Headers.us">
    <title>Offset Show</title>
  </programme>
  <programme start="%(orphan_start)s" stop="%(orphan_end)s" channel="Not.In.The.Playlist">
    <title>Orphan Show</title>
  </programme>
  <programme start="%(past_start)s" stop="%(past_end)s" channel="Sports.One.us">
    <title>Already Finished</title>
  </programme>
  <programme start="%(recent_start)s" stop="%(recent_end)s" channel="Sports.One.us">
    <title>Just Ended</title>
  </programme>
</tv>
""" % {
    "morning_start": stamp(BASE),
    "morning_end": stamp(BASE + 3600),
    # The same kind of instant, written in +0530 like some upstream guides do.
    "offset_start": stamp(BASE + 1800, 5, 30),
    "offset_end": stamp(BASE + 5400, 5, 30),
    "orphan_start": stamp(BASE + 7200),
    "orphan_end": stamp(BASE + 10800),
    "past_start": stamp(PAST),
    "past_end": stamp(PAST + 3600),
    "recent_start": stamp(RECENT),
    "recent_end": stamp(RECENT + 3600),
}


def write(path, text):
    path.write_text(text, encoding="utf-8")
    return str(path)


class ParsePlaylistTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.playlist = write(Path(self.tmp.name) / "list.m3u", PLAYLIST)
        self.channels, self.guide = build_bundle.parse_m3u(self.playlist)

    def tearDown(self):
        self.tmp.cleanup()

    def test_channels_and_header_guide_url(self):
        self.assertEqual(len(self.channels), 3)
        # Only the first advertised guide is taken, as the app does.
        self.assertEqual(self.guide, "https://example.invalid/one.xml")

    def test_attributes_are_read(self):
        one = self.channels[0]
        self.assertEqual(one["id"], "Sports.One.us")
        self.assertEqual(one["group"], "Sports")
        self.assertEqual(one["country"], "US")
        self.assertEqual(one["chno"], "7")
        self.assertEqual(one["url"], "https://stream.example/one.m3u8")

    def test_decorative_prefix_is_stripped_but_quality_kept(self):
        self.assertEqual(self.channels[0]["name"], "One Sports (1080p)")

    def test_stream_options_are_captured(self):
        needs = self.channels[1]
        self.assertEqual(needs["referrer"], "https://referrer.example")
        self.assertEqual(needs["ua"], "Mozilla/5.0 (Test)")
        self.assertEqual(needs["origin"], "https://origin.example")

    def test_missing_tvg_id_falls_back_to_a_slug(self):
        noid = self.channels[2]
        self.assertEqual(noid["id"], "no.id.channel")
        self.assertEqual(noid["group"], "Sports")

    def test_commas_in_quoted_attributes_and_display_names_are_preserved(self):
        playlist = write(
            Path(self.tmp.name) / "comma.m3u",
            '#EXTM3U\n#EXTINF:-1 tvg-id="local.news" group-title="News, Local",News, Local\n'
            'https://stream.example/news.m3u8\n',
        )
        channels, _ = build_bundle.parse_m3u(playlist)
        self.assertEqual(channels[0]["group"], "News, Local")
        self.assertEqual(channels[0]["name"], "News, Local")


class ParseGuideTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        path = write(Path(self.tmp.name) / "guide.xml", GUIDE)
        self.programmes = build_bundle.parse_xmltv(path)

    def tearDown(self):
        self.tmp.cleanup()

    def by_title(self, title):
        matches = [p for p in self.programmes if p["t"] == title]
        self.assertEqual(len(matches), 1, title)
        return matches[0]

    def test_programmes_are_parsed_and_entities_decoded(self):
        self.assertEqual(len(self.programmes), 5)
        first = self.by_title("Morning Sports")
        self.assertEqual(first["c"], "Sports.One.us")
        self.assertEqual(first["d"], "Desc & more")
        self.assertEqual(first["g"], "Football; Sports talk")
        self.assertEqual(first["i"], "https://art/one.jpg")

    def test_utc_timestamp(self):
        programme = self.by_title("Morning Sports")
        self.assertEqual(programme["s"], BASE)
        self.assertEqual(programme["e"], BASE + 3600)

    def test_offset_timestamp_is_normalised_to_utc(self):
        # 06:30 +0530 and 01:00 +0000 are the same instant.
        programme = self.by_title("Offset Show")
        self.assertEqual(programme["s"], BASE + 1800)
        self.assertEqual(programme["e"], BASE + 5400)

    def test_bogus_timestamp_is_zero_not_a_crash(self):
        self.assertEqual(build_bundle.xmltv_time("not-a-time"), 0)
        self.assertEqual(build_bundle.xmltv_time(""), 0)

    def test_invalid_dates_offsets_and_trailing_text_are_rejected(self):
        self.assertEqual(build_bundle.xmltv_time("20261131010000 +0000"), 0)
        self.assertEqual(build_bundle.xmltv_time("00000101000000 +0000"), 0)
        self.assertEqual(build_bundle.xmltv_time("20261101010000 +2460"), 0)
        self.assertEqual(build_bundle.xmltv_time("20261101010000 +0000 junk"), 0)

    def test_invalid_stop_falls_back_to_a_valid_thirty_minute_window(self):
        path = write(
            Path(self.tmp.name) / "bad-stop.xml",
            '<tv><programme channel="demo" start="20261101010000 +0000" '
            'stop="20261101000000 +0000"><title>Good start</title></programme>'
            '<programme channel="demo" start="20261131010000 +0000" '
            'stop="20261131020000 +0000"><title>Invalid date</title></programme></tv>',
        )
        programmes = build_bundle.parse_xmltv(path)
        self.assertEqual(len(programmes), 1)
        self.assertEqual(programmes[0]["t"], "Good start")
        self.assertEqual(programmes[0]["e"] - programmes[0]["s"], 1800)

    def test_sorted_by_channel_then_start(self):
        pairs = [(p["c"], p["s"]) for p in self.programmes]
        self.assertEqual(pairs, sorted(pairs))


class GroupOrderTests(unittest.TestCase):
    def test_published_order_comes_first_then_count_desc(self):
        channels = [
            {"group": "Other"},
            {"group": "Cartoons"},
            {"group": "Sports"},
            {"group": "Sports"},
        ]
        groups = build_bundle.order_groups(channels, ["Sports", "Cartoons", "Missing"])
        self.assertEqual([g["name"] for g in groups], ["Sports", "Cartoons", "Other"])
        self.assertEqual([g["count"] for g in groups], [2, 1, 1])


class BuildBundleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.playlist = write(self.root / "list.m3u", PLAYLIST)
        self.guide = write(self.root / "guide.xml", GUIDE)
        self.out = str(self.root / "bundle")
        self.meta = build_bundle.build(
            self.playlist, self.guide, str(self.root / "missing-index.json"),
            self.out, "9.9.9",
        )

    def tearDown(self):
        self.tmp.cleanup()

    def read_jsonl(self, name):
        rows = []
        with open(os.path.join(self.out, name), encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
        return rows

    def test_every_line_is_valid_json(self):
        self.assertEqual(len(self.read_jsonl("channels.jsonl")), 3)
        self.assertEqual(len(self.read_jsonl("groups.jsonl")), 2)

    def test_orphan_and_finished_programmes_are_dropped(self):
        programmes = self.read_jsonl("epg.jsonl")
        channels = self.read_jsonl("channels.jsonl")
        known = {c["id"] for c in channels}
        self.assertTrue(known)
        for programme in programmes:
            self.assertIn(programme["c"], known)
        # The orphan channel and the listing that finished hours ago are gone...
        self.assertEqual({p["c"] for p in programmes}, {"Sports.One.us", "Needs.Headers.us"})
        self.assertNotIn("Already Finished", {p["t"] for p in programmes})
        # ...while a listing that only just ended is kept, so "what was on" works.
        self.assertEqual(
            {p["t"] for p in programmes},
            {"Morning Sports", "Offset Show", "Just Ended"},
        )

    def test_meta_counts_match_the_files(self):
        channels = self.read_jsonl("channels.jsonl")
        programmes = self.read_jsonl("epg.jsonl")
        self.assertEqual(self.meta["channel_count"], len(channels))
        self.assertEqual(self.meta["programme_count"], len(programmes))
        self.assertEqual(self.meta["guide_channels"], len({p["c"] for p in programmes}))
        self.assertEqual(self.meta["version"], "9.9.9")
        self.assertEqual(self.meta["library_scope"], "usa")
        self.assertEqual(self.meta["preview_features"], [])
        self.assertEqual(self.meta["guide_url"], "https://example.invalid/one.xml")
        self.assertEqual(self.meta["window_start"], min(p["s"] for p in programmes))
        self.assertEqual(self.meta["window_end"], max(p["e"] for p in programmes))

    def test_every_channel_has_a_playable_url(self):
        for channel in self.read_jsonl("channels.jsonl"):
            self.assertTrue(channel["url"].startswith(("http://", "https://")), channel)

    def test_programme_windows_are_sane(self):
        for programme in self.read_jsonl("epg.jsonl"):
            self.assertGreater(programme["e"], programme["s"])
            self.assertGreater(programme["s"], 1_600_000_000)

    def test_all_scope_is_explicit_preview_and_stable_default_stays_usa(self):
        self.assertEqual(build_bundle.DEFAULT_SCOPE, "usa")
        self.assertEqual(build_bundle.DEFAULT_VERSION, "1.1.0")
        meta = build_bundle.build(
            self.playlist,
            self.guide,
            str(self.root / "missing-index.json"),
            str(self.root / "preview-bundle"),
            "1.1.0",
            scope="all",
        )
        self.assertEqual(meta["library_scope"], "all")
        self.assertEqual(meta["preview_features"], ["cable-guide"])


@unittest.skipUnless(
    (REPO_ROOT / "playlists" / "countries" / "USA.m3u").is_file()
    and (REPO_ROOT / "EPG" / "USA.xml").is_file(),
    "repository playlist/guide not available",
)
class RepositoryBundleTests(unittest.TestCase):
    """Runs against the real files the APK is built from."""

    def test_all_preview_bundle_uses_the_checked_player_list_and_merged_guide(self):
        playlist_rel, guide_rel = build_bundle.SCOPE_INPUTS["all"]
        self.assertEqual(playlist_rel, "playlists/PremiumTV.m3u")
        self.assertEqual(guide_rel, "EPG/PremiumTV.xml")
        playlist = REPO_ROOT / playlist_rel
        guide = REPO_ROOT / guide_rel
        channels, _ = build_bundle.parse_m3u(str(playlist))
        programmes = build_bundle.parse_xmltv(str(guide))
        known = {channel["id"] for channel in channels}
        matched = {programme["c"] for programme in programmes if programme["c"] in known}

        self.assertGreater(len(channels), 9000)
        self.assertEqual(len({channel["url"] for channel in channels}), len(channels))
        self.assertTrue(matched, "the global EPG must match the active player playlist")
        self.assertTrue(all(p["e"] > p["s"] for p in programmes))

    def test_usa_bundle_is_complete(self):
        playlist = REPO_ROOT / "playlists" / "countries" / "USA.m3u"
        guide = REPO_ROOT / "EPG" / "USA.xml"
        channels, header_guide = build_bundle.parse_m3u(str(playlist))
        programmes = build_bundle.parse_xmltv(str(guide))

        self.assertTrue(len(channels) > 1000)
        self.assertTrue(header_guide.endswith(".xml"))
        self.assertTrue(all(c["url"] for c in channels))

        known = {c["id"] for c in channels if c["id"]}
        matched = {p["c"] for p in programmes if p["c"] in known}
        self.assertTrue(matched, "no guide entries matched the playlist - ids drifted")
        # Every guide channel the USA playlist declares exists in the playlist.
        self.assertTrue(set(known) >= {p["c"] for p in programmes})

    def test_bundled_channels_are_reachable(self):
        channels, _ = build_bundle.parse_m3u(str(REPO_ROOT / "playlists" / "countries" / "USA.m3u"))
        with_logo = sum(1 for c in channels if c["logo"])
        self.assertGreater(with_logo, 0)
        # Duplicate ids are legal (backup feeds); duplicate URLs are not.
        urls = [c["url"] for c in channels]
        self.assertEqual(len(urls), len(set(urls)), "the playlist repeats a stream URL")


if __name__ == "__main__":
    unittest.main()
