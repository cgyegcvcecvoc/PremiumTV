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
        self.guides = [f"http://127.0.0.1:{self.port}/a.xml.gz",
                       f"http://127.0.0.1:{self.port}/b.xml"]
        (self.out / "PremiumTV.m3u").write_text(
            PLAYLIST.format(guides=",".join(self.guides)), encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # ------------------------------------------------------------------ #
    def run_build(self, extra=()):
        args = ["--out", str(self.out), "--label", "test build",
                "--guides-from", "checks/epg-check.json", "--workers", "2",
                "--timeout", "10", "--min-channels", "2", "--min-programmes", "2",
                *extra]
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = epg_build.main(args)
        return code, buffer.getvalue()

    def load_guide(self):
        path = self.out / "epg" / "PremiumTV.xml"
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
        code, output = self.run_build(["--patch"])
        self.assertEqual(code, 0, output)
        self.assertTrue((self.out / "epg" / "PremiumTV.xml.gz").exists())
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
        self.assertTrue(report["raw_url"].endswith("playlists/epg/PremiumTV.xml"))
        self.assertTrue((self.out / "checks" / "EPG-BUILD.md").exists())
        self.assertTrue((self.out / "logs" / "epg-build-edits.txt").exists())
        # The gzipped copy decompresses to the same document.
        packed = gzip.decompress((self.out / "epg" / "PremiumTV.xml.gz").read_bytes())
        self.assertEqual(packed, (self.out / "epg" / "PremiumTV.xml").read_bytes())
        # --patch advertises the merged guide first and keeps the upstreams.
        header = (self.out / "PremiumTV.m3u").read_text().splitlines()[0]
        guides = [part for part in header.split('x-tvg-url="')[1].rstrip('"').split(",")]
        self.assertEqual(guides[0], report["raw_url"])
        self.assertIn(self.guides[0], guides)

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
        self.assertEqual(set(channels), {"MeTV.us"})
        # The document it wrote is still well formed and complete.
        self.assertEqual(root.tag, "tv")

    def test_freshness_guard_skips_a_recent_build(self):
        code, _ = self.run_build()
        self.assertEqual(code, 0)
        first = (self.out / "epg" / "PremiumTV.xml").stat().st_mtime_ns
        code, output = self.run_build()
        self.assertEqual(code, 0)
        self.assertIn("nothing to do", output)
        self.assertEqual((self.out / "epg" / "PremiumTV.xml").stat().st_mtime_ns, first)
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
        published = self.out / "epg" / "PremiumTV.xml"
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


class HelperTest(unittest.TestCase):
    """Unit tests for the parsing helpers the merge depends on."""

    def test_norm_id_drops_the_variant_suffix(self):
        self.assertEqual(epg_build.norm_id("AE.us@East"), "aeus")
        self.assertEqual(epg_build.norm_id("ae.us"), "aeus")
        self.assertEqual(epg_build.norm_id("BBC One HD.uk"), "bbconehduk")
        self.assertEqual(epg_build.norm_id("MeTV.us@SD"), epg_build.norm_id("MeTV.us"))

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
        self.assertEqual(wanted.unique_ids_for_name("MeTV"), [])
        self.assertEqual(wanted.without_id, 1)
        self.assertEqual(wanted.entries, 3)

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


if __name__ == "__main__":
    unittest.main(verbosity=2)
