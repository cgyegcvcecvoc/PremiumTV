"""Offline tests for the merged EPG builder (scripts/epg_build.py).

Everything runs against a local HTTP server that serves synthetic XMLTV
guides, so the tests never touch the network.
"""
import datetime as dt
import gzip
import json
import shutil
import sys
import tempfile
import threading
import unittest
import xml.etree.ElementTree as ET
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import epg_build  # noqa: E402

UTC = dt.timezone.utc
NOW = dt.datetime.now(UTC).replace(minute=0, second=0, microsecond=0)


def stamp(moment: dt.datetime) -> str:
    return moment.astimezone(UTC).strftime("%Y%m%d%H%M%S +0000")


def slot(hours_from_now: float, length_hours: float = 1.0):
    start = NOW + dt.timedelta(hours=hours_from_now)
    return stamp(start), stamp(start + dt.timedelta(hours=length_hours))


def programme(channel: str, hours_from_now: float, title: str, length: float = 1.0,
              offset: str = "+0000", extra: str = "") -> str:
    start = NOW + dt.timedelta(hours=hours_from_now)
    stop = start + dt.timedelta(hours=length)

    def shifted(moment: dt.datetime) -> str:
        if offset == "+0000":
            return moment.strftime("%Y%m%d%H%M%S +0000")
        sign, hours = offset[0], int(offset[1:3])
        delta = dt.timedelta(hours=hours) * (1 if sign == "+" else -1)
        return (moment + delta).strftime("%Y%m%d%H%M%S ") + offset

    return (f'<programme start="{shifted(start)}" stop="{shifted(stop)}" '
            f'channel="{channel}"><title>{title}</title>{extra}</programme>')


# Guide A: ids that match the playlist exactly (iptv-org style), gzipped.
GUIDE_A = (
    '<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="guide-a">\n'
    '<channel id="AE.us"><display-name>A&amp;E</display-name>'
    '<display-name>AE.us</display-name>'
    '<icon src="https://example.com/ae.png" /></channel>\n'
    '<channel id="MeTV.us"><display-name>MeTV</display-name></channel>\n'
    '<channel id="NotInPlaylist.us"><display-name>Not In Playlist</display-name></channel>\n'
    + programme("AE.us", 0, "Morning Movie", 2,
                extra='<desc>A long film.</desc><category lang="en">Movie</category>'
                      '<episode-num system="xmltv_ns">0.1.0/1</episode-num><new />')
    + programme("AE.us", 2, "Afternoon Show",
                extra='<desc>Documentary about television.</desc><category>Documentary</category>')
    + programme("MeTV.us", 0, "Classic Sitcom")
    # Ends long before the window, so it must be dropped.
    + programme("MeTV.us", -72, "Ancient Episode")
    # Placeholder title, so it must be dropped.
    + programme("MeTV.us", 3, "No Information")
    # Outside the 48h window, so it must be dropped.
    + programme("MeTV.us", 200, "Far Future Special")
    # A channel nobody publishes: its events must never appear.
    + programme("NotInPlaylist.us", 0, "Should Not Appear")
    + "</tv>\n"
).encode("utf-8")

# Guide B: plain XML, non-UTC offsets, a duplicate of one of A's events, an
# overlapping event on a channel A covers better, and an alias + name match.
GUIDE_B = (
    '<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="guide-b">\n'
    '<channel id="AE.us@HD"><display-name>A&amp;E East</display-name></channel>\n'
    '<channel id="me-tv-central"><display-name>MeTV</display-name></channel>\n'
    '<channel id="bbc1.uk"><display-name>BBC One</display-name></channel>\n'
    # Duplicate of A's first event (same instant, same title) - must merge.
    + programme("AE.us@HD", 0, "Morning Movie", 2, offset="+0200",
                extra='<desc>Short.</desc><category>Movie</category>')
    # Overlaps A's second event on the same channel; A matched more channels,
    # so A's event must win.
    + programme("AE.us@HD", 2, "Filler Slot", 1, offset="+0200")
    # Only in B, so it survives.
    + programme("bbc1.uk", 1, "News At Ten", 1, offset="+0100",
                extra='<credits><actor>Jane Doe</actor></credits>')
    # Matched by display name only (no id in common with the playlist).
    + programme("me-tv-central", 1, "Drama Hour")
    + "</tv>\n"
).encode("utf-8")

# A big guide, served with the gzip stream cut in half: whatever was parsed
# before the cut must survive instead of the whole guide being thrown away.
BIG_GUIDE = (
    b'<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="big">\n'
    b'<channel id="MeTV.us"><display-name>MeTV</display-name></channel>\n'
    + b"".join(programme("MeTV.us", -5 + index * 0.5, f"Episode {index}").encode("utf-8")
               for index in range(400))
    + b"</tv>\n"
)

HTML = b"<html><body>nope</body></html>"

# A name-only guide: its channel id matches no playlist tvg-id, so the
# display-name path decides who receives the listings (backup-feed fan-out).
NEWS_GUIDE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<tv generator-info-name="news">\n'
    '<channel id="NewsNet.us"><display-name>Backup News</display-name></channel>\n'
    + programme("NewsNet.us", 0, "Morning News", 3)
    + programme("NewsNet.us", 3, "Midday News", 3)
    + "</tv>\n"
).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body=b"", ctype="application/xml"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        path = self.path
        if path == "/a.xml.gz":
            self._send(200, gzip.compress(GUIDE_A))
        elif path == "/b.xml":
            self._send(200, GUIDE_B)
        elif path == "/gone.xml.gz":
            self._send(404, b"gone", "text/plain")
        elif path == "/html.xml.gz":
            self._send(200, gzip.compress(HTML), "text/html")
        elif path == "/news.xml":
            self._send(200, NEWS_GUIDE)
        elif path == "/truncated.xml.gz":
            packed = gzip.compress(BIG_GUIDE)
            self._send(200, packed[: len(packed) // 2])
        else:
            self._send(404, b"unknown", "text/plain")


PLAYLIST = """#EXTM3U x-tvg-url="{guides}"
#EXTINF:-1 tvg-id="AE.us@East" tvg-country="US" tvg-logo="https://example.com/ae.png" group-title="Docs",A&E (US East)
https://example.com/ae-east.m3u8
#EXTINF:-1 tvg-id="AE.us@West" tvg-country="US" group-title="Docs",A&E (US West)
https://example.com/ae-west.m3u8
#EXTINF:-1 tvg-id="MeTV.us" tvg-country="US" group-title="Classic",MeTV
https://example.com/metv.m3u8
#EXTINF:-1 tvg-id="BBCOne.uk" tvg-country="UK" group-title="UK",BBC One (UK)
https://example.com/bbc1.m3u8
#EXTINF:-1 tvg-country="US" group-title="Misc",No Id Channel
https://example.com/noid.m3u8
"""


class BuildTest(unittest.TestCase):
    """End-to-end build against the synthetic guides."""

    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="epg-build-"))
        self.out = self.tmp / "playlists"
        self.out.mkdir()
        self.epg = self.tmp / "EPG"
        self.guides = [f"http://127.0.0.1:{self.port}/a.xml.gz",
                       f"http://127.0.0.1:{self.port}/b.xml"]
        (self.out / "PremiumTV.m3u").write_text(
            PLAYLIST.format(guides=",".join(self.guides)), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------------ #
    def run_build(self, extra=()):
        args = ["--out", str(self.out), "--epg-dir", str(self.epg), "--label", "test build",
                "--guides-from", "checks/epg-check.json", "--workers", "2",
                "--timeout", "10", "--min-channels", "2", "--min-programmes", "2",
                "--no-curated",
                *extra]
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = epg_build.main(args)
        return code, buffer.getvalue()

    def load_guide(self):
        path = self.epg / "PremiumTV.xml"
        self.assertTrue(path.exists(), "the guide was not written")
        root = ET.parse(path).getroot()
        channels = {channel.get("id"): channel for channel in root.findall("channel")}
        programmes = [element for element in root.findall("programme")]
        return root, channels, programmes

    # ------------------------------------------------------------------ #
    def test_guide_is_filtered_to_playlist_channels(self):
        code, output = self.run_build()
        self.assertEqual(code, 0, output)
        root, channels, programmes = self.load_guide()
        # Every alias of a matched channel is declared; channels nobody
        # publishes are not.
        self.assertEqual(set(channels), {"AE.us@East", "AE.us@West", "MeTV.us", "BBCOne.uk"})
        self.assertNotIn("NotInPlaylist.us", "".join(
            ET.tostring(element, encoding="unicode") for element in programmes))
        # Playlist display name first, then the guide's own names.
        names = [node.text for node in channels["AE.us@East"].findall("display-name")]
        self.assertEqual(names[0], "A&E (US East)")
        self.assertIn("A&E", names)
        self.assertIn("AE.us", names)
        # The guide icon and the playlist logo survive.
        self.assertEqual(channels["AE.us@East"].find("icon").get("src"),
                         "https://example.com/ae.png")

    def test_events_are_utc_windowed_and_deduped(self):
        code, output = self.run_build()
        self.assertEqual(code, 0, output)
        root, channels, programmes = self.load_guide()
        by_channel = {}
        for element in programmes:
            by_channel.setdefault(element.get("channel"), []).append(element)

        # Every timestamp is UTC with an explicit offset.
        for element in programmes:
            for key in ("start", "stop"):
                self.assertTrue(element.get(key).endswith(" +0000"), element.get(key))

        # Alias fan-out: both A&E feeds carry the same events.
        # "Afternoon Show" (guide A) and "Filler Slot" (guide B) overlap; the
        # better-described event wins, so A's listing is kept.
        self.assertEqual([item.findtext("title") for item in by_channel["AE.us@East"]],
                         ["Morning Movie", "Afternoon Show"])
        self.assertEqual([item.findtext("title") for item in by_channel["AE.us@West"]],
                         ["Morning Movie", "Afternoon Show"])

        # Duplicate merged, not duplicated; the richer description wins and the
        # categories are unioned.
        movie = by_channel["AE.us@East"][0]
        self.assertEqual(movie.findtext("desc"), "A long film.")
        # Both guides sent "Movie"; the lang attribute is kept, the word is not
        # listed twice.
        categories = movie.findall("category")
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].text, "Movie")
        self.assertEqual(categories[0].get("lang"), "en")
        self.assertEqual(movie.findtext("episode-num"), "0.1.0/1")
        self.assertIsNotNone(movie.find("new"))

        # MeTV: the placeholder, the ancient and the far-future events are gone;
        # the name-matched event from guide B survived.
        self.assertEqual([item.findtext("title") for item in by_channel["MeTV.us"]],
                         ["Classic Sitcom", "Drama Hour"])

        # BBC One matched by id (BBCOne.uk vs bbc1.uk) and keeps its credits.
        self.assertEqual([item.findtext("title") for item in by_channel["BBCOne.uk"]],
                         ["News At Ten"])
        self.assertEqual(by_channel["BBCOne.uk"][0].find("credits").findtext("actor"),
                         "Jane Doe")

        # The event that started 72h ago is outside --keep-past 6.
        starts = [element.get("start") for element in programmes]
        self.assertEqual(len(starts), 7)

    def test_report_and_files(self):
        playlist = self.out / "PremiumTV.m3u"
        lines = playlist.read_text(encoding="utf-8").splitlines()
        legacy = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml"
        lines[0] = lines[0].replace(self.guides[0], f"{legacy},{self.guides[0]}")
        playlist.write_text("\n".join(lines) + "\n", encoding="utf-8")
        code, output = self.run_build(["--patch"])
        self.assertEqual(code, 0, output)
        self.assertTrue((self.epg / "PremiumTV.xml.gz").exists())
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        self.assertTrue(report["published"])
        self.assertEqual(report["totals"]["guides"], 2)
        self.assertEqual(report["totals"]["guides_ok"], 2)
        self.assertEqual(report["playlist_channels"], 4)
        self.assertEqual(report["channels_with_guide"], 4)
        self.assertEqual(report["coverage"], 1.0)
        self.assertGreaterEqual(report["merge"]["duplicates_merged"], 1)
        self.assertGreaterEqual(report["merge"]["overlaps_dropped"], 1)
        self.assertEqual(report["playlist_entries_without_id"], 1)
        self.assertIn("raw_url", report)
        self.assertTrue(report["raw_url"].endswith("/EPG/PremiumTV.xml"))
        self.assertEqual(report["patch"]["advertised"], 1)
        self.assertTrue((self.out / "checks" / "EPG-BUILD.md").exists())
        self.assertTrue((self.out / "logs" / "epg-build-edits.txt").exists())
        # The gzipped copy decompresses to the same document.
        packed = gzip.decompress((self.epg / "PremiumTV.xml.gz").read_bytes())
        self.assertEqual(packed, (self.epg / "PremiumTV.xml").read_bytes())
        # --patch advertises the merged guide first and keeps the upstreams.
        header = (self.out / "PremiumTV.m3u").read_text().splitlines()[0]
        guides = [part for part in header.split('x-tvg-url="')[1].rstrip('"').split(",")]
        self.assertEqual(guides[0], report["raw_url"])
        self.assertIn(self.guides[0], guides)
        self.assertNotIn(legacy, guides)

    def test_country_guides_are_xmltv_scoped_and_advertised(self):
        countries = self.out / "countries"
        countries.mkdir()
        usa = [
            ('AE.us@East', 'US', 'A&E (US East)'),
            ('AE.us@West', 'US', 'A&E (US West)'),
            ('MeTV.us', 'US', 'MeTV'),
        ]
        uk = [('BBCOne.uk', 'UK', 'BBC One (UK)')]
        for filename, entries in (("USA.m3u", usa), ("UK.m3u", uk)):
            lines = [f'#EXTM3U x-tvg-url="{",".join(self.guides)}"']
            for index, (tvg_id, country, name) in enumerate(entries):
                lines.extend([
                    f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-country="{country}",'
                    f'{name}',
                    f"https://example.com/{filename}-{index}.m3u8",
                ])
            (countries / filename).write_text("\n".join(lines) + "\n", encoding="utf-8")

        code, output = self.run_build(["--countries", "--patch"])
        self.assertEqual(code, 0, output)
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        self.assertTrue(report["country_guides_complete"])
        self.assertEqual(report["country_patch"]["advertised"], 2)
        by_country = {item["country"]: item for item in report["country_guides"]}
        self.assertEqual(set(by_country), {"USA", "UK"})
        self.assertTrue(by_country["USA"]["valid_xmltv"])
        self.assertEqual(by_country["USA"]["playlist_channels"], 3)
        self.assertEqual(by_country["UK"]["playlist_channels"], 1)

        usa_root = ET.parse(self.epg / "USA.xml").getroot()
        usa_channels = {item.get("id") for item in usa_root.findall("channel")}
        self.assertEqual(usa_channels, {"AE.us@East", "AE.us@West", "MeTV.us"})
        usa_programmes = usa_root.findall("programme")
        self.assertTrue(usa_programmes)
        self.assertTrue(all(item.get("channel") in usa_channels for item in usa_programmes))
        uk_root = ET.parse(self.epg / "UK.xml").getroot()
        self.assertEqual({item.get("id") for item in uk_root.findall("channel")},
                         {"BBCOne.uk"})
        self.assertTrue(all(item.get("channel") == "BBCOne.uk"
                            for item in uk_root.findall("programme")))

        for country, url in (("USA", by_country["USA"]["url"]),
                             ("UK", by_country["UK"]["url"])):
            header = (countries / f"{country}.m3u").read_text().splitlines()[0]
            self.assertEqual(epg_build.epg_check.extract_guides(countries / f"{country}.m3u"),
                             [url])
            self.assertIn("x-tvg-url=", header)

        # A channel-set change rebuilds immediately even while the prior report
        # is inside the normal freshness window, and the unmatched station is
        # still represented as a declared XMLTV channel without fake events.
        usa_path = countries / "USA.m3u"
        with usa_path.open("a", encoding="utf-8") as handle:
            handle.write('#EXTINF:-1 tvg-id="NewStation.us" tvg-country="US",New Station\n'
                         'https://example.com/new-station.m3u8\n')
        code, output = self.run_build(["--countries"])
        self.assertEqual(code, 0, output)
        self.assertIn("channel set or expected EPG files changed; rebuilding", output)
        refreshed = ET.parse(self.epg / "USA.xml").getroot()
        self.assertIn("NewStation.us", {item.get("id") for item in refreshed.findall("channel")})
        self.assertFalse(any(item.get("channel") == "NewStation.us"
                             for item in refreshed.findall("programme")))

    def test_stale_country_guide_is_pruned_only_when_every_country_published(self):
        countries = self.out / "countries"
        countries.mkdir()
        for filename, tvg_id, country, name in (
                ("USA.m3u", "AE.us@East", "US", "A&E (US East)"),
                ("UK.m3u", "BBCOne.uk", "UK", "BBC One (UK)")):
            (countries / filename).write_text(
                f'#EXTM3U x-tvg-url="{",".join(self.guides)}"\n'
                f'#EXTINF:-1 tvg-id="{tvg_id}" tvg-country="{country}",{name}\n'
                f"https://example.com/{filename}.m3u8\n", encoding="utf-8")
        self.epg.mkdir(parents=True, exist_ok=True)
        # A guide for a country whose playlist no longer exists, plus the pair of
        # files a real run always keeps.
        stale = self.epg / "Papua_New_Guinea.xml"
        stale.write_text('<tv><channel id="NBCTV.pg@SD" /></tv>', encoding="utf-8")
        keeper = self.epg / "PremiumTV.xml"
        keeper.write_text('<tv></tv>', encoding="utf-8")
        keeper_gz = self.epg / "PremiumTV.xml.gz"
        keeper_gz.write_bytes(b"stub")

        code, output = self.run_build(["--countries"])
        self.assertEqual(code, 0, output)
        self.assertFalse(stale.exists(), "a stale country guide survived the build")
        self.assertTrue(keeper.exists())
        self.assertTrue(keeper_gz.exists())
        self.assertTrue((self.epg / "USA.xml").is_file())
        self.assertTrue((self.epg / "UK.xml").is_file())
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        self.assertEqual([Path(item).name for item in report.get("stale_guides_removed", [])],
                         ["Papua_New_Guinea.xml"])

    def test_country_guides_reuse_a_recent_verified_build_when_feeds_are_unreachable(self):
        # First publish a normal merged guide from verified fixture feeds.
        code, output = self.run_build()
        self.assertEqual(code, 0, output)
        published = self.epg / "PremiumTV.xml"
        previous_xml = published.read_bytes()

        countries = self.out / "countries"
        countries.mkdir()
        (countries / "USA.m3u").write_text(
            '#EXTM3U\n'
            '#EXTINF:-1 tvg-id="AE.us@East" tvg-country="US",A&E East\n'
            'https://example.com/ae.m3u8\n'
            '#EXTINF:-1 tvg-id="MeTV.us" tvg-country="US",MeTV\n'
            'https://example.com/metv.m3u8\n', encoding="utf-8")
        (countries / "UK.m3u").write_text(
            '#EXTM3U\n'
            '#EXTINF:-1 tvg-id="BBCOne.uk" tvg-country="UK",BBC One\n'
            'https://example.com/bbc.m3u8\n', encoding="utf-8")
        # Simulate every current upstream feed being unavailable.
        playlist = self.out / "PremiumTV.m3u"
        playlist.write_text(playlist.read_text(encoding="utf-8").replace(
            playlist.read_text(encoding="utf-8").splitlines()[0], "#EXTM3U", 1),
            encoding="utf-8")

        code, output = self.run_build(["--countries", "--patch", "--force"])
        self.assertEqual(code, 1, output)  # the merged-guide safety gate still fails
        self.assertEqual(published.read_bytes(), previous_xml)
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        self.assertFalse(report["published"])
        self.assertTrue(report["country_guides_complete"])
        self.assertGreater(report["previous_verified_guide"]["programmes_reused"], 0)
        by_country = {item["country"]: item for item in report["country_guides"]}
        self.assertIn("last successfully published guide",
                      by_country["USA"]["programme_data_source"])
        self.assertTrue(ET.parse(self.epg / "USA.xml").getroot().findall("programme"))
        self.assertTrue(ET.parse(self.epg / "UK.xml").getroot().findall("programme"))
        self.assertEqual(epg_build.epg_check.extract_guides(countries / "USA.m3u"),
                         [by_country["USA"]["url"]])
        build_report = (self.out / "checks" / "EPG-BUILD.md").read_text()
        self.assertIn("reused", build_report)
        self.assertIn("Retained guide", build_report)

    def test_country_catalogue_is_published_without_fabricated_programmes(self):
        countries = self.out / "countries"
        countries.mkdir()
        (countries / "USA.m3u").write_text(
            '#EXTM3U\n'
            '#EXTINF:-1 tvg-id="NewStation.us" tvg-country="US",New Station\n'
            'https://example.com/new-station.m3u8\n', encoding="utf-8")
        playlist = self.out / "PremiumTV.m3u"
        playlist.write_text(playlist.read_text(encoding="utf-8").replace(
            playlist.read_text(encoding="utf-8").splitlines()[0], "#EXTM3U", 1),
            encoding="utf-8")

        code, output = self.run_build(["--countries", "--patch", "--force"])
        self.assertEqual(code, 1, output)  # there was no verified programming feed
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        self.assertTrue(report["country_guides_complete"])
        self.assertEqual(report["country_guides"][0]["programme_data_source"],
                         "channel catalogue only; no verified programme data available")
        root = ET.parse(self.epg / "USA.xml").getroot()
        self.assertEqual({item.get("id") for item in root.findall("channel")}, {"NewStation.us"})
        self.assertEqual(root.findall("programme"), [])
        self.assertEqual(epg_build.epg_check.extract_guides(countries / "USA.m3u"),
                         [report["country_guides"][0]["url"]])

    def test_truncated_guide_keeps_what_it_parsed(self):
        checks = self.out / "checks"
        checks.mkdir(exist_ok=True)
        truncated = f"http://127.0.0.1:{self.port}/truncated.xml.gz"
        (checks / "epg-check.json").write_text(
            json.dumps({"guides": [{"url": truncated, "status": "ok"}]}), encoding="utf-8")
        code, output = self.run_build(["--min-channels", "1", "--min-programmes", "2"])
        self.assertEqual(code, 0, output)
        report = json.loads((checks / "epg-build.json").read_text())
        guide = report["guides"][0]
        self.assertEqual(guide["status"], "ok", guide)
        self.assertGreater(guide["programmes_kept"], 10)
        self.assertLess(guide["programmes_kept"], 400)
        root, channels, programmes = self.load_guide()
        # Every playlist channel is declared (catalogue entries for the ones no
        # verified guide had a schedule for); only MeTV.us had parsable listings.
        self.assertEqual(set(channels),
                         {"AE.us@East", "AE.us@West", "MeTV.us", "BBCOne.uk"})
        self.assertEqual({element.get("channel") for element in programmes}, {"MeTV.us"})
        self.assertEqual(report["channels_with_guide"], 1)
        self.assertEqual(report["channels_declared"], 4)
        # The document it wrote is still well formed and complete.
        self.assertEqual(root.tag, "tv")

    def test_freshness_guard_skips_a_recent_build(self):
        code, _ = self.run_build()
        self.assertEqual(code, 0)
        first = (self.epg / "PremiumTV.xml").stat().st_mtime_ns
        code, output = self.run_build()
        self.assertEqual(code, 0)
        self.assertIn("nothing to do", output)
        self.assertEqual((self.epg / "PremiumTV.xml").stat().st_mtime_ns, first)
        code, output = self.run_build(["--force"])
        self.assertEqual(code, 0)
        self.assertNotIn("nothing to do", output)

    def test_dead_and_invalid_guides_are_reported(self):
        code, output = self.run_build([
            "--guide", f"http://127.0.0.1:{self.port}/gone.xml.gz",
            "--guide", f"http://127.0.0.1:{self.port}/html.xml.gz"])
        self.assertEqual(code, 0, output)
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        statuses = {guide["url"].rsplit("/", 1)[-1]: guide["status"]
                    for guide in report["guides"]}
        self.assertEqual(statuses["gone.xml.gz"], "offline")
        self.assertEqual(statuses["html.xml.gz"], "invalid")
        self.assertEqual(statuses["a.xml.gz"], "ok")

    def test_hollow_build_keeps_the_published_guide(self):
        code, _ = self.run_build()
        self.assertEqual(code, 0)
        published = self.epg / "PremiumTV.xml"
        before = published.read_bytes()
        # Restrict the run to a dead guide: the published guide must stay put.
        checks = self.out / "checks"
        (checks / "epg-check.json").write_text(json.dumps({"guides": [
            {"url": f"http://127.0.0.1:{self.port}/gone.xml.gz", "status": "offline"}]}),
            encoding="utf-8")
        code, output = self.run_build(["--force"])
        self.assertEqual(code, 1, output)
        self.assertEqual(published.read_bytes(), before)
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        self.assertFalse(report["published"])
        self.assertIn("publish_reason", report)
        self.assertTrue(report["publish_reason"])

    def test_size_budget_trims_the_window(self):
        code, output = self.run_build(["--max-mb", "0.0004"])
        self.assertEqual(code, 0, output)
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        self.assertTrue(report["published"])
        self.assertLessEqual(report["size_bytes"], 0.0004 * 1024 * 1024 + 2048)
        self.assertTrue(report["trim"], "the size budget should have recorded a trim")

    def test_window_trim_is_proportional_to_the_overshoot(self):
        """A file 5% over budget loses an hour of window, not the whole day."""
        code, output = self.run_build()
        self.assertEqual(code, 0, output)
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        natural = report["size_bytes"]
        self.assertEqual(report["trim"], [])

        budget_mb = natural * 0.95 / (1024 * 1024)
        code, output = self.run_build(["--force", "--max-mb", f"{budget_mb:.6f}"])
        self.assertEqual(code, 0, output)
        report = json.loads((self.out / "checks" / "epg-build.json").read_text())
        self.assertLessEqual(report["size_bytes"], budget_mb * 1024 * 1024)
        self.assertTrue(report["trim"])
        # 48h ahead minus the 6h already in the past leaves 42h of future
        # listings; a 5% overshoot must not collapse that to the 12h floor.
        ahead = report["window"]["ahead_hours"]
        self.assertGreater(ahead, 40, report["trim"])
        self.assertLess(ahead, 48)

    def test_guide_list_prefers_the_verified_report(self):
        checks = self.out / "checks"
        checks.mkdir(exist_ok=True)
        (checks / "epg-check.json").write_text(json.dumps({
            "guides": [
                {"url": self.guides[0], "status": "ok"},
                {"url": f"http://127.0.0.1:{self.port}/gone.xml.gz", "status": "offline"},
            ]}), encoding="utf-8")
        code, output = self.run_build()
        self.assertEqual(code, 0, output)
        report = json.loads((checks / "epg-build.json").read_text())
        urls = [guide["url"] for guide in report["guides"]]
        # The verified guide is merged; the dead one is not; the unverified
        # playlist guide is left out unless --include-unverified is passed.
        self.assertEqual(urls, [self.guides[0]])
        code, output = self.run_build(["--force", "--include-unverified"])
        self.assertEqual(code, 0, output)
        report = json.loads((checks / "epg-build.json").read_text())
        self.assertIn(self.guides[1], [guide["url"] for guide in report["guides"]])


    def test_backup_feeds_receive_listings_by_name(self):
        """Two same-country ids sharing a name both carry the matched schedule."""
        news_guide = f"http://127.0.0.1:{self.port}/news.xml"
        (self.out / "PremiumTV.m3u").write_text(
            f'#EXTM3U x-tvg-url="{news_guide}"\n'
            '#EXTINF:-1 tvg-id="NewsNet.us" tvg-country="US" group-title="News",Backup News\n'
            'https://example.com/news-a.m3u8\n'
            '#EXTINF:-1 tvg-id="premiumtv.us.backup_news_hd" tvg-country="US" '
            'group-title="News",Backup News (720p)\n'
            'https://example.com/news-b.m3u8\n'
            '#EXTINF:-1 tvg-id="NewsNet.de@SD" tvg-country="DE" group-title="News",Backup News\n'
            'https://example.com/news-de.m3u8\n',
            encoding="utf-8")
        code, output = self.run_build(["--min-channels", "2", "--min-programmes", "1"])
        self.assertEqual(code, 0, output)
        _, channels, programmes = self.load_guide()
        by_channel: dict = {}
        for element in programmes:
            by_channel.setdefault(element.get("channel"), []).append(
                element.findtext("title"))
        self.assertIn("NewsNet.us", by_channel)
        self.assertIn("premiumtv.us.backup_news_hd", by_channel,
                      "the same-country backup feed must share the listings")
        self.assertNotIn("NewsNet.de@SD", by_channel,
                         "the German feed must not receive US listings")


class HelperTest(unittest.TestCase):
    """Unit tests for the parsing helpers the merge depends on."""

    def test_recent_dead_guide_report_prunes_only_confirmed_dead_urls(self):
        now = dt.datetime.now(UTC)
        dead = "https://feeds.example/dead.xml"
        invalid = "https://feeds.example/invalid.xml"
        transient = "https://feeds.example/transient.xml"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            report_path = root / "epg-check.json"
            report_path.write_text(json.dumps({
                "finished_utc": now.isoformat().replace("+00:00", "Z"),
                "guides": [
                    {"url": dead, "status": "offline"},
                    {"url": invalid, "status": "invalid"},
                    {"url": transient, "status": "unreachable"},
                ],
            }), encoding="utf-8")
            dead_urls = epg_build.recently_dead_guide_urls(report_path, now)
            self.assertEqual(dead_urls, {dead, invalid})

            raw = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/EPG/PremiumTV.xml"
            legacy = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/playlists/epg/PremiumTV.xml"
            playlist = root / "channels.m3u"
            playlist.write_text(
                f'#EXTM3U x-tvg-url="{raw},{legacy},{dead},{transient}"\n',
                encoding="utf-8")
            patch = epg_build.patch_playlists([playlist], raw, dead_urls)
            self.assertEqual(epg_build.epg_check.extract_guides(playlist),
                             [raw, transient])
            self.assertEqual(patch["removed_guides"], 2)

            old = now - dt.timedelta(hours=epg_build.MAX_EP_CHECK_AGE_HOURS + 1)
            report_path.write_text(json.dumps({
                "finished_utc": old.isoformat().replace("+00:00", "Z"),
                "guides": [{"url": dead, "status": "offline"}],
            }), encoding="utf-8")
            self.assertEqual(epg_build.recently_dead_guide_urls(report_path, now), set())

    def test_norm_id_drops_the_variant_suffix(self):
        self.assertEqual(epg_build.norm_id("AE.us@East"), "aeus")
        self.assertEqual(epg_build.norm_id("ae.us"), "aeus")
        self.assertEqual(epg_build.norm_id("BBC One HD.uk"), "bbconehduk")
        self.assertEqual(epg_build.norm_id("MeTV.us@SD"), epg_build.norm_id("MeTV.us"))

    def test_generic_network_guide_does_not_fan_out_to_local_affiliates(self):
        wanted = epg_build.Wanted()
        wanted.add("NBC.us@WGAL", "WGAL 8 (NBC) - Lancaster PA", "US", "",
                   "General")
        wanted.add("NBC.us@WJACTV", "NBC 6 (WJAC) - Johnstown PA", "US", "",
                   "General")
        self.assertEqual(wanted.ids_for_guide_id("NBC.us"), [])
        self.assertEqual(wanted.ids_for_guide_id("NBC.us@WGAL"), ["NBC.us@WGAL"])

    def test_norm_name_ignres_quality_and_brackets(self):
        self.assertEqual(epg_build.norm_name("A&E (720p)"), "ae")
        self.assertEqual(epg_build.norm_name("BBC One [HD]"), "bbcone")
        self.assertEqual(epg_build.norm_name("Sky News HD"), epg_build.norm_name("sky news"))

    def test_cc_of_id(self):
        self.assertEqual(epg_build.cc_of_id("AE.us@East"), "us")
        self.assertEqual(epg_build.cc_of_id("no-suffix"), "")

    def test_clean_text_strips_markup(self):
        self.assertEqual(epg_build.clean_text("<b>Hello</b>\n  world&nbsp; "), "Hello world")

    def test_parse_xmltv_time_handles_offsets_and_junk(self):
        moment = epg_build.parse_xmltv_time("20261002140000 +0200")
        self.assertEqual(moment.isoformat(), "2026-10-02T14:00:00+02:00")
        self.assertEqual(epg_build.format_xmltv_time(moment), "20261002120000 +0000")
        naive = epg_build.parse_xmltv_time("20261002140000")
        self.assertEqual(naive.tzinfo, UTC)
        self.assertIsNone(epg_build.parse_xmltv_time("not a time"))
        self.assertIsNone(epg_build.parse_xmltv_time("20261302140000 +0000"))

    def test_raw_tag(self):
        self.assertEqual(epg_build.raw_tag('<icon src="x" />'), "icon")
        self.assertEqual(epg_build.raw_tag("<credits><a>b</a></credits>"), "credits")
        self.assertEqual(epg_build.raw_tag("<previously-shown />"), "previously-shown")
        self.assertEqual(epg_build.raw_tag(""), "")

    def test_programme_from_element_drops_placeholders(self):
        element = ET.fromstring(
            '<programme start="20261002120000 +0000" stop="20261002130000 +0000" '
            'channel="A.us"><title>No Information</title></programme>')
        self.assertIsNone(epg_build.programme_from_element(element, 0))
        # A zero-length (or reversed, or stop-less) event is not a schedule: it
        # cannot be shown and must not reach the published guide.
        for times in ('start="20261002120000 +0000" stop="20261002120000 +0000"',
                      'start="20261002130000 +0000" stop="20261002120000 +0000"',
                      'start="20261002120000 +0000"'):
            zero = ET.fromstring(
                f'<programme {times} channel="A.us">'
                '<title>Red Mercury Promo</title></programme>')
            self.assertIsNone(epg_build.programme_from_element(zero, 0))
        element = ET.fromstring(
            '<programme start="20261002120000 +0000" stop="20261002130000 +0000" '
            'channel="A.us"><title>Real Show</title><desc>d</desc></programme>')
        programme = epg_build.programme_from_element(element, 3)
        self.assertEqual(programme.title, "Real Show")
        self.assertEqual(programme.source, 3)
        self.assertEqual((programme.stop - programme.start).total_seconds(), 3600)
        self.assertEqual(programme.desc, "d")

    def test_wanted_indexes_aliases_and_names(self):
        wanted = epg_build.Wanted()
        wanted.add("AE.us@East", "A&E (US East)", "us", "")
        wanted.add("AE.us@West", "A&E (US West)", "us", "")
        wanted.add("", "No Id", "", "")
        self.assertEqual(sorted(wanted.by_key["aeus"]), ["AE.us@East", "AE.us@West"])
        self.assertEqual(wanted.ids_for_name("MeTV"), [])
        self.assertEqual(wanted.without_id, 1)
        self.assertEqual(wanted.entries, 3)

    def test_name_match_fans_out_within_one_country_only(self):
        """Backup feeds of one station share its listings; other countries keep theirs."""
        wanted = epg_build.Wanted()
        wanted.add("Nickelodeon.us@East", "Nickelodeon", "US", "")
        wanted.add("premiumtv.us.nickelodeon_hd", "Nickelodeon (720p)", "US", "")
        wanted.add("Nickelodeon.de@SD", "Nickelodeon", "DE", "")

        # One unambiguous name -> its id, even when the name has brackets.
        single = epg_build.Wanted()
        single.add("MeTV.us", "MeTV (1080p)", "US", "")
        self.assertEqual(single.ids_for_name("MeTV"), ["MeTV.us"])

        # Mixed countries without a guide suffix: too ambiguous to guess.
        self.assertEqual(wanted.ids_for_name("Nickelodeon"), [])
        # The same two US backup feeds are both the US channel.
        self.assertEqual(
            sorted(wanted.ids_for_name("Nickelodeon (720p)", "Nickelodeon.us")),
            ["Nickelodeon.us@East", "premiumtv.us.nickelodeon_hd"])
        self.assertEqual(
            sorted(wanted.ids_for_name("Nickelodeon", "Something.us")),
            ["Nickelodeon.us@East", "premiumtv.us.nickelodeon_hd"])
        # A guide id that knows its country picks only its own country's feeds.
        self.assertEqual(wanted.ids_for_name("Nickelodeon", "Nickelodeon.de"),
                         ["Nickelodeon.de@SD"])
        # 'uk' and 'gb' are one country.
        uk = epg_build.Wanted()
        uk.add("BBCOne.uk", "BBC One", "UK", "")
        uk.add("premiumtv.uk.bbc_one_hd", "BBC One HD", "GB", "")
        self.assertEqual(sorted(uk.ids_for_name("BBC One", "bbc1.uk")),
                         ["BBCOne.uk", "premiumtv.uk.bbc_one_hd"])
        # A guide suffix for a country nobody publishes leaves the name unmatched.
        self.assertEqual(wanted.ids_for_name("Nickelodeon", "Nickelodeon.fr"), [])

    def test_guide_list_puts_the_curated_sources_first(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp)
            (out / "checks").mkdir()
            (out / "checks" / "epg-check.json").write_text(json.dumps({
                "guides": [{"url": "https://report/guide.xml", "status": "ok"}]}),
                encoding="utf-8")
            playlist = out / "p.m3u"
            playlist.write_text(
                '#EXTM3U x-tvg-url="https://header/guide.xml"\n'
                "#EXTINF:-1,X\nhttps://example.invalid/x.m3u8\n", encoding="utf-8")
            guides = epg_build.guide_list(
                out, ["https://extra/guide.xml"], "checks/epg-check.json",
                [playlist], True, curated=["https://curated/guide.xml",
                                           "https://extra/guide.xml"])
        self.assertEqual(guides, ["https://extra/guide.xml", "https://curated/guide.xml",
                                  "https://report/guide.xml"])

    def test_merge_prefers_the_richer_then_the_wider_source(self):
        """merge_programmes() keeps one track per channel, best event first."""
        base = dt.datetime(2026, 10, 2, 12, 0, tzinfo=UTC)
        end = base + dt.timedelta(hours=2)

        def make(title, source, desc=""):
            programme = epg_build.Programme(base, end, title, source)
            programme.desc = desc
            programme.score_richness()
            return programme

        per_channel = {"A.us": [make("Stub", 0), make("Detailed", 1, "x" * 80)]}
        merged, stats = epg_build.merge_programmes(per_channel, {0: 1, 1: 1}, True)
        self.assertEqual([item.title for item in merged["A.us"]], ["Detailed"])
        self.assertEqual(stats["overlaps_dropped"], 1)

        # Equal detail: the source that matched more of our channels wins.
        per_channel = {"A.us": [make("Small", 0), make("Wide", 1)]}
        merged, stats = epg_build.merge_programmes(per_channel, {0: 5, 1: 500}, True)
        self.assertEqual([item.title for item in merged["A.us"]], ["Wide"])

        # --keep-overlaps leaves both in place.
        per_channel = {"A.us": [make("Stub", 0), make("Detailed", 1, "x" * 80)]}
        merged, stats = epg_build.merge_programmes(per_channel, {0: 1, 1: 1}, False)
        self.assertEqual(len(merged["A.us"]), 2)
        self.assertEqual(stats["overlaps_dropped"], 0)

    def test_count_channels(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            path = tmp / "guide.xml"
            path.write_text('<tv><channel id="A" /><channel id="B" /></tv>')
            self.assertEqual(epg_build.count_channels(path), 2)
            self.assertEqual(epg_build.count_channels(tmp / "missing.xml"), 0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_channels_with_listings_counts_only_live_channels(self):
        tmp = Path(tempfile.mkdtemp())
        try:
            path = tmp / "PremiumTV.xml"
            path.write_text(
                "<tv>\n"
                '  <channel id="Live.us"><display-name>Live</display-name></channel>\n'
                '  <channel id="Stale.us"><display-name>Stale</display-name></channel>\n'
                '  <programme start="20261010120000 +0000" stop="20261010130000 +0000"'
                ' channel="Live.us">\n    <title>Now</title>\n  </programme>\n'
                '  <programme start="20261005120000 +0000" stop="20261005130000 +0000"'
                ' channel="Stale.us">\n    <title>Expired</title>\n  </programme>\n'
                '  <programme start="20261011120000 +0000" stop="20261011130000 +0000"'
                ' channel="Later.us">\n    <title>Scheduled</title>\n  </programme>\n'
                '  <programme start="20261011060000 +0000"\n'
                '             stop="20261011070000 +0000" channel="Wrapped.us">\n'
                "    <title>Split tag</title>\n  </programme>\n"
                "</tv>\n", encoding="utf-8")
            start = dt.datetime(2026, 10, 10, 6, tzinfo=dt.timezone.utc)
            end = dt.datetime(2026, 10, 12, 6, tzinfo=dt.timezone.utc)
            # Everything inside the window, whatever the file declares, and a tag
            # that a generator wrapped over two lines still counts once.
            self.assertEqual(epg_build.channels_with_listings(path, start, end), 3)
            self.assertEqual(epg_build.channels_with_listings(tmp / "missing.xml",
                                                              start, end), 0)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_previous_programme_channels_prefers_the_window_over_the_last_report(self):
        out = Path(tempfile.mkdtemp())
        try:
            (out / "checks").mkdir(parents=True, exist_ok=True)
            (out / "checks" / "epg-build.json").write_text(json.dumps(
                {"published": True, "channels_with_guide": 8521}), encoding="utf-8")
            xml = out / "PremiumTV.xml"
            xml.write_text(
                "<tv>\n"
                '  <programme start="20261005120000 +0000" stop="20261005130000 +0000"'
                ' channel="Old.us">\n    <title>x</title>\n  </programme>\n'
                "</tv>\n", encoding="utf-8")
            start = dt.datetime(2026, 10, 10, 6, tzinfo=dt.timezone.utc)
            end = dt.datetime(2026, 10, 12, 6, tzinfo=dt.timezone.utc)
            # A guide whose listings have all aged out protects nothing: counting
            # its rows (or trusting the last report) would block its own
            # replacement on every following run.
            self.assertEqual(epg_build.previous_programme_channels(out, xml, start, end), 0)
            self.assertEqual(epg_build.previous_programme_channels(out, xml), 8521)
        finally:
            shutil.rmtree(out, ignore_errors=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
