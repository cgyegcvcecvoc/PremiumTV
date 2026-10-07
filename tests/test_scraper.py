"""Offline end-to-end checks for the existing scraper; no public streams required."""
import json
import sys
import tempfile
import threading
import unittest
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import epg_check  # noqa: E402
import scraper  # noqa: E402


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        base = f"http://127.0.0.1:{self.server.server_port}"
        if self.path == "/source.m3u":
            body = ("#EXTM3U\n#EXTINF:-1 group-title=\"News\",Test Live\n"
                    f"{base}/live.m3u8\n#EXTINF:-1 group-title=\"News\",Bad HTML\n"
                    f"{base}/bad\n").encode()
            ctype = "audio/x-mpegurl"
        elif self.path == "/root.json":
            body = json.dumps({"name": "Root", "groups": [{"name": "Digital TV", "url": f"{base}/group.json"}]}).encode()
            ctype = "application/json"
        elif self.path == "/group.json":
            body = json.dumps({"name": "Digital TV", "stations": [
                {"name": "Duplicate", "url": f"{base}/live.m3u8"},
                {"name": "Other Live", "url": f"{base}/other.m3u8", "referer": "https://example.org/"},
                {"name": "Web page", "url": f"{base}/bad", "embed": "true"},
            ]}).encode()
            ctype = "application/json"
        elif self.path in ("/live.m3u8", "/other.m3u8"):
            body, ctype = b"#EXTM3U\n#EXTINF:5,Segment\nsegment.ts\n", "application/vnd.apple.mpegurl"
        else:
            body, ctype = b"<html>Not a stream</html>", "text/html"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class WriteM3uTest(unittest.TestCase):
    """The header every playlist is published with."""

    def test_merged_guide_is_advertised_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "p.m3u"
            scraper.write_m3u(path, [], ["https://upstream/guide.xml.gz"], "title")
            self.assertEqual(
                path.read_text(encoding="utf-8").splitlines()[0],
                f'#EXTM3U x-tvg-url="{scraper.SELF_EPG_URL},https://upstream/guide.xml.gz"')
            # The source caches mirror an upstream file, so they leave it out.
            scraper.write_m3u(path, [], ["https://upstream/guide.xml.gz"], "title",
                              advertise_self=False)
            self.assertEqual(path.read_text(encoding="utf-8").splitlines()[0],
                             '#EXTM3U x-tvg-url="https://upstream/guide.xml.gz"')

    def test_published_playlist_assigns_stable_ids_only_when_requested(self):
        channel = scraper.Channel(
            name="Tést Channel", url="https://example.org/live.m3u8", source="fixture",
            attrs={"tvg-country": "us", "group-title": "News"},
        )
        with tempfile.TemporaryDirectory() as tmp:
            published = Path(tmp) / "published.m3u"
            scraper.write_m3u(published, [channel], [], "published",
                              advertise_self=False, synthesize_missing_ids=True)
            self.assertEqual(channel.attrs["tvg-id"],
                             "premiumtv.usa.test_channel")
            self.assertIn('tvg-id="premiumtv.usa.test_channel"',
                          published.read_text(encoding="utf-8"))

            source_copy = scraper.Channel(
                name="No ID", url="https://example.org/no-id.m3u8", source="fixture",
            )
            cache = Path(tmp) / "cache.m3u"
            scraper.write_m3u(cache, [source_copy], [], "source cache",
                              advertise_self=False)
            self.assertNotIn("tvg-id", source_copy.attrs)
            self.assertIn("#EXTINF:-1,No ID", cache.read_text(encoding="utf-8"))


class ScraperIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_checked_playlist_and_failed_refresh_preserves_it(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = f"http://127.0.0.1:{self.server.server_port}"
            cfg = root / "sources.json"
            cfg.write_text(json.dumps({"sources": [
                {"name": "m3u", "type": "m3u", "url": base + "/source.m3u"},
                {"name": "w3u", "type": "w3u", "url": base + "/root.json",
                 "include_groups": ["Digital TV"], "max_depth": 2},
            ]}), encoding="utf-8")
            out = root / "playlists"
            args = ["scraper.py", "--sources", str(cfg), "--out", str(out),
                    "--workers", "2", "--timeout", "2"]
            with patch.object(sys, "argv", args), redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)
            verified = (out / "PremiumTV.m3u").read_text(encoding="utf-8")
            all_links = (out / "PremiumTV_all.m3u").read_text(encoding="utf-8")
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            # No upstream guide in these fixtures, so the header advertises only
            # this repository's own merged guide - every playlist always does.
            self.assertEqual(verified.splitlines()[0],
                             f'#EXTM3U x-tvg-url="{scraper.SELF_EPG_URL}"')
            self.assertEqual((out / "sources" / "m3u.m3u").read_text(
                encoding="utf-8").splitlines()[0], "#EXTM3U")
            self.assertEqual(verified.count("#EXTINF"), 2)
            self.assertEqual(all_links.count("#EXTINF"), 3)
            self.assertIn("#EXTVLCOPT:http-referrer=https://example.org/", verified)
            self.assertEqual(report["total_unique"], 3)
            self.assertEqual(report["working"], 2)
            self.assertTrue((out / "sources" / "m3u.m3u").exists())
            self.assertTrue((out / "sources" / "w3u.m3u").exists())

            # An upstream outage uses the local caches; an unsuccessful check
            # must not wipe the last good player playlist.
            def dead(ch, timeout):
                ch.status, ch.reason = "dead", "simulated outage"
                return ch

            with patch.object(sys, "argv", args), \
                 patch.object(scraper, "fetch_source_text", side_effect=RuntimeError("offline")), \
                 patch.object(scraper, "check_channel", side_effect=dead), \
                 redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 1)
            self.assertEqual((out / "PremiumTV.m3u").read_text(encoding="utf-8"), verified)

    def test_country_separation_ae_playlist_and_txt_logs(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = f"http://127.0.0.1:{self.server.server_port}"
            local_m3u = root / "test_channels.m3u"
            local_m3u.write_text(
                "#EXTM3U\n"
                "#EXTINF:-1 tvg-id=\"AE.us@East\" tvg-country=\"US\" group-title=\"A&E Networks\",A&E HD (East)\n"
                f"{base}/live.m3u8\n"
                "#EXTINF:-1 tvg-id=\"CCTV1.cn\" tvg-country=\"CN\" group-title=\"China\",CCTV-1 HD\n"
                f"{base}/other.m3u8\n"
                "#EXTINF:-1 tvg-id=\"NashuaETV.us\" tvg-country=\"US\" group-title=\"Public\",Nashua ETV\n"
                f"{base}/bad\n",
                encoding="utf-8",
            )
            cfg = root / "sources.json"
            cfg.write_text(json.dumps({"sources": [
                {"name": "ae-and-intl", "type": "m3u", "url": base + "/source.m3u",
                 "local_path": str(local_m3u)},
            ]}), encoding="utf-8")
            out = root / "playlists"
            epg_dir = root / "EPG"
            epg_dir.mkdir()
            for country in ("USA", "China"):
                (epg_dir / f"{country}.xml").write_text(
                    '<?xml version="1.0" encoding="UTF-8"?><tv/>', encoding="utf-8")
            args = ["scraper.py", "--sources", str(cfg), "--out", str(out),
                    "--workers", "2", "--timeout", "2", "--label", "manual rescrape check"]
            with patch.object(sys, "argv", args), patch.object(scraper, "EPG_DIR", epg_dir), \
                    redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)

            self.assertTrue((out / "countries" / "USA.m3u").exists())
            self.assertTrue((out / "countries" / "China.m3u").exists())
            self.assertTrue((out / "countries" / "README.md").exists())
            self.assertIn("A&E HD (East)", (out / "countries" / "USA.m3u").read_text(encoding="utf-8"))
            self.assertIn("CCTV-1 HD", (out / "countries" / "China.m3u").read_text(encoding="utf-8"))
            self.assertEqual(
                epg_check.extract_guides(out / "countries" / "USA.m3u"),
                [scraper.country_epg_url("USA")],
            )
            self.assertEqual(
                epg_check.extract_guides(out / "countries" / "China.m3u"),
                [scraper.country_epg_url("China")],
            )
            index = (out / "countries" / "README.md").read_text(encoding="utf-8")
            self.assertIn("USA.xml", index)
            self.assertIn("Raw EPG URL", index)

            self.assertTrue((out / "AE_Channels.m3u").exists())
            ae_text = (out / "AE_Channels.m3u").read_text(encoding="utf-8")
            self.assertIn("A&E HD (East)", ae_text)
            self.assertNotIn("Nashua ETV", ae_text)

            for log_name in ("scrape-log.txt", "log-edits.txt", "errors.txt", "run-history.txt"):
                log_path = out / "logs" / log_name
                self.assertTrue(log_path.exists(), f"Missing {log_name}")
                self.assertTrue(log_path.read_text(encoding="utf-8").strip())

            self.assertIn("LOG EDITS:", (out / "logs" / "log-edits.txt").read_text(encoding="utf-8"))
            self.assertIn("Nashua ETV", (out / "logs" / "errors.txt").read_text(encoding="utf-8"))

    def test_attribute_values_are_stripped_and_plus_urls_repaired(self):
        # A padded tvg-id is a literal id a player cannot match against the guide
        # (the Tastemade Travel entry arrives as "USBD700017WC "), so parsing and
        # publishing both trim it.
        channels, _ = scraper.parse_m3u(
            '#EXTM3U\n#EXTINF:-1 tvg-id="USBD700017WC " tvg-name=" Tastemade Travel " '
            'group-title="Lifestyle",Tastemade Travel\n'
            'https://example.com/tastemade.m3u8\n', "m3u")
        self.assertEqual(channels[0].attrs["tvg-id"], "USBD700017WC")
        self.assertEqual(channels[0].attrs["tvg-name"], "Tastemade Travel")
        self.assertIn('tvg-id="USBD700017WC"', channels[0].to_m3u())
        self.assertNotIn('USBD700017WC "', channels[0].to_m3u())
        # A leading '+' is not a scheme: the repaired URL has to play.
        self.assertEqual(scraper.fix_url("+https://host.example/live.m3u8"),
                         "https://host.example/live.m3u8")
        self.assertEqual(scraper.fix_url("++https://host.example/live.m3u8"),
                         "https://host.example/live.m3u8")
        self.assertEqual(scraper.fix_url(" https://host.example/live.m3u8 "),
                         "https://host.example/live.m3u8")

    def test_iri_percent_encoding_and_w3u_trailing_comma(self):
        encoded = scraper.fix_url("https://stream.example.com/live/มายาHD/index.m3u8")
        self.assertTrue(encoded.isascii())
        self.assertIn("%E0%B8%A1", encoded)
        bad_ch = scraper.Channel(name="Space URL", url="https://a.example/1.m3u8 https://b.example/2.m3u8", source="xtemus")
        scraper.check_channel(bad_ch, timeout=1.0, retries=0)
        self.assertEqual(bad_ch.status, "dead")
        self.assertEqual(bad_ch.reason, "invalid URL")
        data = scraper._loads_w3u_json('{"name": "Youtube Music", "stations": [{"name": "A", "url": "https://x.test/a.m3u8"},]}')
        self.assertEqual(data["name"], "Youtube Music")


if __name__ == "__main__":
    unittest.main()
