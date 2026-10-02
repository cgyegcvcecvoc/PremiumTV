"""Offline tests for the targeted priority-channel hunt."""
import json
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import channel_hunt  # noqa: E402
import scraper  # noqa: E402

TS_SEGMENT = b"\x47" + b"\x22" * 4095
MEDIA_PLAYLIST = "#EXTM3U\n#EXT-X-TARGETDURATION:4\n#EXTINF:4.0,\nseg1.ts\n"


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _send(self, code, body=b"", ctype="application/vnd.apple.mpegurl"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def do_GET(self):
        if self.path == "/metvtoons.m3u8":
            self._send(200, MEDIA_PLAYLIST.encode())
        elif self.path == "/seg1.ts":
            self._send(200, TS_SEGMENT, "video/mp2t")
        elif self.path == "/nick.m3u8":
            self._send(200, MEDIA_PLAYLIST.encode())
        elif self.path == "/dead.m3u8":
            self._send(404, b"gone", "text/plain")
        elif self.path == "/stub.m3u8":
            self._send(200, b"#EXTM3U\n#EXT-X-TARGETDURATION:4\n")
        else:
            self._send(404, b"unknown", "text/plain")


CONFIG = {
    "sources": [],
    "priority_channels": {
        "output": "playlists/sources/priority-channels.m3u",
        "targets": [
            {"name": "MeTV Toons", "group": "Classic TV",
             "aliases": ["MeTVToons", "MeTV Toons US"], "max_links": 2},
            {"name": "Nickelodeon (United States)", "group": "Kids",
             "aliases": ["Nickelodeon.us@East", "Nickelodeon US"], "max_links": 3},
            {"name": "Disabled Channel", "enabled": False, "aliases": ["Nothing"]},
        ],
    },
}


class ChannelHuntTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=5)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.out = Path(self.tmp.name)
        (self.out / "sources").mkdir(parents=True, exist_ok=True)
        (self.out / "PremiumTV_all.m3u").write_text("\n".join([
            "#EXTM3U",
            '#EXTINF:-1 tvg-id="MeTVToons.us@SD" group-title="Classic",MeTV Toons (720p)',
            f"{self.base}/metvtoons.m3u8",
            "#EXTINF:-1 group-title=\"Classic\",MeTV Toons mirror",
            f"{self.base}/dead.m3u8",
            "#EXTINF:-1 group-title=\"Classic\",MeTV Toons stub",
            f"{self.base}/stub.m3u8",
            '#EXTINF:-1 tvg-id="Nickelodeon.us@East" group-title="Kids",Nickelodeon (720p)',
            f"{self.base}/nick.m3u8",
            "#EXTINF:-1 group-title=\"News\",Something Else",
            f"{self.base}/metvtoons.m3u8",
            "",
        ]), encoding="utf-8")
        self.config_path = self.out / "sources.json"
        self.config_path.write_text(json.dumps(CONFIG), encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    # -- matching ---------------------------------------------------------- #
    def test_entry_matches_aliases_and_tvg_ids(self):
        aliases = ["MeTV Toons", "MeTVToons.us"]
        self.assertTrue(channel_hunt.entry_matches("MeTV Toons (720p)", "MeTVToons.us@SD", aliases))
        self.assertTrue(channel_hunt.entry_matches("metv toons hd", "", aliases))
        self.assertTrue(channel_hunt.entry_matches("US: MeTV Toons", "", aliases))
        self.assertFalse(channel_hunt.entry_matches("MeTV", "MeTV.us", aliases))
        self.assertFalse(channel_hunt.entry_matches("ToonsTV", "ToonsTV.us", aliases))

    def test_alias_matching_respects_word_boundaries(self):
        # "Chamame TV" and "Awesome TV" both contain the letters of "MeTV".
        aliases = ["MeTV", "MeTV US", "MeTV.us@SD"]
        self.assertFalse(channel_hunt.entry_matches("Chamame TV", "ChamameTV.ar@SD", aliases))
        self.assertFalse(channel_hunt.entry_matches("Awesome TV", "AwesomeTV.my@SD", aliases))
        self.assertTrue(channel_hunt.entry_matches("MeTV (720p)", "MeTV.us@SD", aliases))
        self.assertTrue(channel_hunt.entry_matches("US: MeTV HD", "MeTV.us", aliases))

    def test_blocklist_drops_mislabelled_feeds(self):
        blocked = scraper.Channel(
            name="MeTV Toons KMBY-LD", source="unit",
            url="https://2-fss-2.streamhoster.com/pl_138/205510-3094608-1/playlist.m3u8")
        fine = scraper.Channel(name="MeTV Toons", source="unit",
                               url="https://example.invalid/metvtoons.m3u8")
        blocklist = ["2-fss-2.streamhoster.com/pl_138/205510-3094608-1"]
        self.assertTrue(channel_hunt.is_blocked(blocked, blocklist))
        self.assertFalse(channel_hunt.is_blocked(fine, blocklist))

    def test_blocklisted_urls_are_not_published(self):
        blocklist = ["2-fss-2.streamhoster.com/pl_138/205510-3094608-1"]
        self.assertNotIn(
            "https://2-fss-2.streamhoster.com/pl_138/205510-3094608-1/playlist.m3u8",
            [channel.url for channel in channel_hunt.local_candidates(
                self.out, ["MeTV Toons", "MeTVToons"])
             if not channel_hunt.is_blocked(channel, blocklist)])

    def test_candidates_from_text_filters_to_the_channel(self):
        text = (self.out / "PremiumTV_all.m3u").read_text()
        found = channel_hunt.candidates_from_text(text, "unit", ["MeTV Toons", "MeTVToons"])
        names = {channel.name for channel in found}
        self.assertEqual(len(found), 3)
        self.assertIn("MeTV Toons (720p)", names)
        self.assertNotIn("Something Else", names)

    def test_shorter_alias_does_not_empty_a_longer_target(self):
        # "MeTV" belongs to the MeTV target, but it also matches every "MeTV
        # Toons" entry - using it as an exclusion would leave that target with
        # no candidates at all.
        targets = [
            {"name": "MeTV Toons", "aliases": ["MeTVToons", "MeTV Toons US"],
             "max_links": 2, "country": "us"},
            {"name": "MeTV", "aliases": ["MeTV US", "MeTV.us@SD", "MeTV.us@East"],
             "max_links": 4, "country": "us"},
        ]
        metv_toons, metv = targets
        excludes = channel_hunt.build_excludes(metv_toons, targets)
        self.assertTrue(channel_hunt.entry_matches(
            "MeTV Toons (720p)", "MeTVToons.us@SD",
            [metv_toons["name"]] + metv_toons["aliases"], excludes))
        # ...while the MeTV target still refuses MeTV Toons links.
        metv_excludes = channel_hunt.build_excludes(metv, targets)
        self.assertFalse(channel_hunt.entry_matches(
            "MeTV Toons (720p)", "MeTVToons.us@SD",
            [metv["name"]] + metv["aliases"], metv_excludes))
        self.assertTrue(channel_hunt.entry_matches(
            "MeTV (720p)", "MeTV.us@SD", [metv["name"]] + metv["aliases"], metv_excludes))

    def test_preference_follows_the_configured_country(self):
        target = {"name": "Nickelodeon", "aliases": ["Nickelodeon"], "country": "us"}
        us = scraper.Channel(name="Nickelodeon (United States) (720p)", url="u",
                             source="s", attrs={"tvg-id": "Nickelodeon.us@East"})
        br = scraper.Channel(name="Nickelodeon (Brazil) (480p)", url="u", source="s",
                             attrs={"tvg-id": "Nickelodeon.br@SD"})
        named = scraper.Channel(name="Nickelodeon (United States)", url="u", source="s")
        self.assertTrue(channel_hunt.is_preferred(us, target))
        self.assertTrue(channel_hunt.is_preferred(named, target))
        self.assertFalse(channel_hunt.is_preferred(br, target))
        self.assertEqual(channel_hunt.stream_country(us), "us")
        self.assertEqual(channel_hunt.stream_country(br), "br")

    def test_local_candidates_search_the_corpus(self):
        found = channel_hunt.local_candidates(self.out, ["MeTV Toons", "MeTVToons"])
        self.assertEqual(len(found), 3)

    def test_dedupe_keeps_one_entry_per_url(self):
        text = (self.out / "PremiumTV_all.m3u").read_text()
        twice = channel_hunt.candidates_from_text(text, "a", ["MeTV Toons"]) + \
            channel_hunt.candidates_from_text(text, "b", ["MeTV Toons"])
        deduped = channel_hunt.dedupe(twice)
        self.assertEqual(len({channel.url for channel in deduped}), len(deduped))
        self.assertLessEqual(len(deduped), 3)

    # -- verification ------------------------------------------------------ #
    def test_verify_all_flags_dead_and_stub_playlists(self):
        candidates = channel_hunt.local_candidates(self.out, ["MeTV Toons", "MeTVToons"])
        verified = channel_hunt.verify_all(candidates, 8, 5, 0)
        statuses = {channel.url: result["status"] for channel, result in verified}
        self.assertEqual(statuses[f"{self.base}/metvtoons.m3u8"], "working")
        self.assertEqual(statuses[f"{self.base}/dead.m3u8"], "offline")
        self.assertEqual(statuses[f"{self.base}/stub.m3u8"], "offline")

    def test_rank_puts_working_links_first(self):
        ranked = sorted([{"status": "offline"}, {"status": "working", "segment_ok": True,
                                                 "elapsed": 0.5},
                         {"status": "working", "segment_ok": False, "elapsed": 0.1}],
                        key=channel_hunt.rank)
        self.assertEqual(ranked[0]["status"], "working")
        self.assertTrue(ranked[0]["segment_ok"])

    # -- publishing -------------------------------------------------------- #
    def test_hunt_publishes_only_verified_links(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            code = channel_hunt.main(["--out", str(self.out), "--sources",
                                      str(self.config_path), "--no-upstream",
                                      "--workers", "8", "--timeout", "5"])
        self.assertEqual(code, 0)
        curated = self.out / "sources" / "priority-channels.m3u"
        self.assertTrue(curated.exists())
        text = curated.read_text()
        self.assertIn("MeTV Toons (720p)", text)
        self.assertIn(f"{self.base}/metvtoons.m3u8", text)
        self.assertNotIn("/dead.m3u8", text)
        self.assertNotIn("/stub.m3u8", text)
        channels, _ = scraper.parse_m3u(text, "curated")
        self.assertEqual(len(channels), 2)  # MeTV Toons + Nickelodeon, both verified

    def test_hunt_writes_a_ready_to_load_playlist_with_guides(self):
        (self.out / "PremiumTV.m3u").write_text(
            '#EXTM3U x-tvg-url="https://example.invalid/guide.xml.gz"\n'
            "#EXTINF:-1,X\nhttps://example.invalid/x.m3u8\n", encoding="utf-8")
        with redirect_stdout(StringIO()):
            channel_hunt.main(["--out", str(self.out), "--sources", str(self.config_path),
                               "--no-upstream", "--workers", "8", "--timeout", "5"])
        playlist = self.out / "Priority_Channels.m3u"
        self.assertTrue(playlist.exists())
        text = playlist.read_text()
        self.assertIn('x-tvg-url="https://example.invalid/guide.xml.gz"', text.splitlines()[0])
        self.assertIn("MeTV Toons (720p)", text)
        channels, _ = scraper.parse_m3u(text, "priority")
        self.assertTrue(all(channel.url for channel in channels))

    def test_hunt_report_only_writes_reports_without_publishing(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            channel_hunt.main(["--out", str(self.out), "--sources", str(self.config_path),
                               "--no-upstream", "--report-only", "--channel", "MeTV Toons"])
        self.assertFalse((self.out / "sources" / "priority-channels.m3u").exists())
        report = json.loads((self.out / "checks" / "channel-hunt.json").read_text())
        self.assertEqual(len(report["targets"]), 1)
        target = report["targets"][0]
        self.assertEqual(target["name"], "MeTV Toons")
        self.assertEqual(target["candidates"], 3)
        self.assertEqual(target["working"], 1)
        self.assertEqual(target["published"], 0)
        markdown = (self.out / "checks" / "CHANNEL-HUNT.md").read_text()
        self.assertIn("MeTV Toons", markdown)

    def test_hunt_disabled_and_unknown_channels_are_skipped(self):
        buffer = StringIO()
        with redirect_stdout(buffer):
            channel_hunt.main(["--out", str(self.out), "--sources", str(self.config_path),
                               "--no-upstream", "--channel", "Disabled Channel"])
        output = buffer.getvalue()
        self.assertIn("no priority channels configured", output)


if __name__ == "__main__":
    unittest.main()
