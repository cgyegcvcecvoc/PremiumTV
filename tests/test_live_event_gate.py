"""Offline tests for the pre-publish live-event health gate."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import scraper  # noqa: E402
import live_event_gate as gate  # noqa: E402


def channel(name: str, url: str, referer: str = "https://embed.example/1",
            group: str = "Live Events") -> scraper.Channel:
    return scraper.Channel(
        name=name, url=url, source="events",
        attrs={"group-title": group, "tvg-id": "NHL.Hockey.Dummy.us"},
        extra=[f"#EXTVLCOPT:http-referrer={referer}",
               "#EXTVLCOPT:http-user-agent=GateTest/1.0"],
    )


def result(status: str, code: int = 0, reason: str = "") -> dict:
    return {
        "status": status,
        "http_status": code,
        "reason": reason,
        "segment_ok": True if status == "working" else None,
        "kind": "hls",
    }


class LiveEventGateTest(unittest.TestCase):
    def test_only_working_feeds_survive_and_refused_fixture_is_dropped(self):
        alpha_ok = channel("[NHL] Alpha vs Beta (FAWA)", "https://a.example/live.m3u8")
        alpha_404 = channel("[NHL] Alpha vs Beta (STRMGATE)", "https://b.example/gone.m3u8")
        alpha_403 = channel("[NHL] Alpha vs Beta (iSTRMEAST)", "https://c.example/blocked.m3u8")
        beta_404 = channel("[NHL] Gamma vs Delta (FAWA)", "https://d.example/gone.m3u8")
        ordinary = scraper.Channel("News", "https://e.example/news.m3u8", "news",
                                   attrs={"group-title": "News"})
        channels = [alpha_ok, alpha_404, alpha_403, beta_404, ordinary]
        results = {
            alpha_ok.url: result("working", reason="hls, segment ok (4096 bytes)"),
            alpha_404.url: result("offline", 404, "HTTP 404"),
            alpha_403.url: result("blocked", 403, "HTTP 403 (auth or geo-block)"),
            beta_404.url: result("offline", 404, "HTTP 404"),
        }
        seen_headers = []

        def probe(ch, timeout, retries, limiter):
            seen_headers.append(ch.headers())
            return results[ch.url]

        kept, report = gate.gate_channels(channels, probe=probe, workers=2)
        self.assertEqual([ch.url for ch in kept], [alpha_ok.url, ordinary.url])
        self.assertEqual(report["entries"], 4)
        self.assertEqual(report["fixtures"], 2)
        self.assertEqual(report["working_entries"], 1)
        self.assertEqual(report["dropped_403"], 1)
        self.assertEqual(report["dropped_404"], 2)
        self.assertEqual(report["dropped_other"], 0)
        self.assertEqual(report["published_fixtures"], 1)
        self.assertEqual(report["refused_fixtures"], 1)
        self.assertEqual(report["refused"][0]["title"], "Gamma vs. Delta")
        self.assertEqual(alpha_ok.status, "alive")
        self.assertEqual(alpha_404.reason, "live-event gate: HTTP 404")
        self.assertEqual(alpha_403.reason, "live-event gate: HTTP 403")
        # The gate must use the entry's own player headers, including its referer.
        self.assertTrue(seen_headers)
        self.assertTrue(all(headers["Referer"] == "https://embed.example/1"
                            for headers in seen_headers))
        self.assertTrue(all(headers["User-Agent"] == "GateTest/1.0"
                            for headers in seen_headers))

    def test_other_failure_is_withheld_and_counted(self):
        ok = channel("[NHL] Alpha vs Beta (FAWA)", "https://a.example/live.m3u8")
        timeout = channel("[NHL] Alpha vs Beta (STRMGATE)", "https://b.example/slow.m3u8")
        results = {
            ok.url: result("working", reason="hls, segment ok"),
            timeout.url: result("unreachable", 0, "timeout"),
        }
        kept, report = gate.gate_channels(
            [ok, timeout], probe=lambda ch, *_: results[ch.url], workers=2)
        self.assertEqual([ch.url for ch in kept], [ok.url])
        self.assertEqual(report["dropped_other"], 1)
        self.assertEqual(report["dropped_403"], 0)
        self.assertEqual(report["dropped_404"], 0)
        self.assertEqual(timeout.status, "unverified")

    def test_bracket_channel_outside_event_groups_is_not_gated(self):
        # A bracket matchup outside the live-event groups is still not an
        # event feed. event_of() alone would wrongly gate this one.
        movie = channel("[Movies] Alpha vs Beta", "https://m.example/movie.m3u8",
                        group="Movies")
        probed = []

        def probe(ch, *_):
            probed.append(ch.name)
            return result("offline", 404, "HTTP 404")

        kept, report = gate.gate_channels([movie], probe=probe)
        self.assertEqual(kept, [movie])
        self.assertEqual(report["entries"], 0)
        self.assertEqual(report["non_fixture_entries"], 0)
        self.assertEqual(probed, [])

    def test_sports_group_event_feed_is_gated(self):
        darts = channel("[Darts] Darts Final (FAWA)", "https://d.example/darts.m3u8",
                        group="Sports")
        kept, report = gate.gate_channels(
            [darts], probe=lambda *_: result("working", reason="hls, segment ok"))
        self.assertEqual(kept, [darts])
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["non_fixture_working"], 1)

    def test_non_matchup_event_feed_is_gated_without_becoming_a_fixture(self):
        darts = channel("[Darts] Darts Players Championship Finals (FAWA)",
                        "https://d.example/darts.m3u8")
        f1 = channel("[Formula 1] Formula 1 2026 - Qatar GP (iSTRMEAST)",
                    "https://f.example/f1.m3u8")
        results = {
            darts.url: result("working", reason="hls, segment ok"),
            f1.url: result("offline", 404, "HTTP 404"),
        }
        kept, report = gate.gate_channels(
            [darts, f1], probe=lambda ch, *_: results[ch.url], workers=2)
        self.assertEqual([ch.url for ch in kept], [darts.url])
        self.assertEqual(report["entries"], 2)
        self.assertEqual(report["fixtures"], 0)
        self.assertEqual(report["non_fixture_entries"], 2)
        self.assertEqual(report["non_fixture_working"], 1)
        self.assertEqual(report["non_fixture_dropped"], 1)
        self.assertEqual(report["published_fixtures"], 0)
        self.assertEqual(report["refused_fixtures"], 0)
        self.assertEqual(report["dropped_404"], 1)

    def test_failure_code_requires_an_http_status(self):
        self.assertEqual(
            gate.failure_code(result("offline", 0, "segment too small (404 bytes)")), 0)
        self.assertEqual(
            gate.failure_code(result("offline", 0, "variant HTTP 403")), 403)
        self.assertEqual(
            gate.failure_code(result("offline", 0, "playlist only, HTTP 410")), 410)

    def test_markdown_lists_non_matchup_drops_without_a_false_all_clear(self):
        darts = channel("[Darts] Darts Final (FAWA)", "https://d.example/darts.m3u8")
        f1 = channel("[Formula 1] F1 Qatar GP (FAWA)", "https://f.example/f1.m3u8")
        _, report = gate.gate_channels(
            [darts, f1],
            probe=lambda ch, *_: (result("working", reason="hls, segment ok")
                                  if ch is darts else result("offline", 404, "HTTP 404")),
        )
        markdown = gate.render_markdown(report)
        self.assertIn("## Non-matchup event feeds", markdown)
        self.assertIn("F1 Qatar GP", markdown)
        self.assertIn("dropped_404", markdown)
        self.assertNotIn("No live-event entry was dropped", markdown)

    def test_no_events_markdown_is_not_a_false_all_clear(self):
        movie = channel("[Movies] Alpha vs Beta", "https://m.example/movie.m3u8",
                        group="Movies")
        _, report = gate.gate_channels([movie])
        markdown = gate.render_markdown(report)
        self.assertIn("No live-event entries were found", markdown)
        self.assertNotIn("every entry had a working feed", markdown)

    def test_variant_or_segment_403_404_is_counted_as_a_drop(self):
        variant = channel("[NHL] Alpha vs Beta (FAWA)", "https://a.example/live.m3u8")
        segment = channel("[NHL] Gamma vs Delta (FAWA)", "https://b.example/live.m3u8")
        results = {
            variant.url: result("blocked", 200, "variant HTTP 403"),
            segment.url: result("offline", 200, "playlist only, HTTP 404"),
        }
        kept, report = gate.gate_channels(
            [variant, segment], probe=lambda ch, *_: results[ch.url], workers=2)
        self.assertEqual(kept, [])
        self.assertEqual(report["dropped_403"], 1)
        self.assertEqual(report["dropped_404"], 1)
        self.assertEqual(report["refused_fixtures"], 2)

    def test_playlist_apply_preserves_header_comments_and_working_blocks(self):
        text = "\n".join([
            '#EXTM3U x-tvg-url="https://guide.example/one.xml"',
            "# 3 channels - test",
            "# keep this header comment",
            '#EXTINF:-1 tvg-id="NHL.Hockey.Dummy.us" group-title="Live Events",'
            "[NHL] Alpha vs Beta (FAWA)",
            "#EXTVLCOPT:http-referrer=https://embed.example/1",
            "https://a.example/working.m3u8",
            "#EXTINF:-1 group-title=\"News\",News",
            "https://news.example/live.m3u8",
            '#EXTINF:-1 tvg-id="NHL.Hockey.Dummy.us" group-title="Live Events",'
            "[NHL] Gamma vs Delta (FAWA)",
            "#EXTVLCOPT:http-referrer=https://embed.example/2",
            "https://b.example/gone.m3u8",
            "",
        ])
        def probe(ch, *_):
            return (result("working", reason="hls, segment ok")
                    if "working" in ch.url else result("offline", 404, "HTTP 404"))
        filtered, report = gate.apply_to_playlist_text(text, probe=probe, workers=2)
        self.assertIn("#EXTM3U x-tvg-url=", filtered)
        self.assertIn("# 2 channels - test", filtered)
        self.assertIn("# keep this header comment", filtered)
        self.assertIn("https://a.example/working.m3u8", filtered)
        self.assertIn("#EXTVLCOPT:http-referrer=https://embed.example/1", filtered)
        self.assertIn("https://news.example/live.m3u8", filtered)
        self.assertNotIn("https://b.example/gone.m3u8", filtered)
        self.assertEqual(report["refused_fixtures"], 1)
        self.assertEqual(report["dropped_404"], 1)

    def test_derived_sync_removes_only_hashes_reported_dropped(self):
        dropped = channel("[NHL] Alpha vs Beta (FAWA)", "https://a.example/gone.m3u8")
        kept = channel("[NHL] Gamma vs Delta (FAWA)", "https://b.example/keep.m3u8")
        unknown = channel("[Darts] Darts Final (FAWA)", "https://d.example/other.m3u8")
        text = "\n".join([
            "#EXTM3U",
            "# USA working channels (4) - updated now",
            "# keep this header comment",
            dropped.to_m3u(),
            kept.to_m3u(),
            unknown.to_m3u(),
            '#EXTINF:-1 group-title="News",News',
            "https://news.example/live.m3u8",
            "",
        ])
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "USA.m3u"
            path.write_text(text, encoding="utf-8")
            results = gate.sync_derived_playlists([path], {gate._url_hash(dropped)})
            filtered = path.read_text(encoding="utf-8")
        self.assertNotIn(dropped.url, filtered)
        self.assertIn(kept.url, filtered)
        self.assertIn(unknown.url, filtered)
        self.assertIn("News", filtered)
        self.assertIn("# USA working channels (3) - updated now", filtered)
        self.assertIn("# keep this header comment", filtered)
        self.assertEqual(results[0]["removed"], 1)
        self.assertEqual(results[0]["entries"], 3)

    def test_derived_sync_does_not_count_a_sanctioned_notice_as_a_channel(self):
        dropped = channel("[NHL] Alpha vs Beta (FAWA)", "https://a.example/gone.m3u8")
        kept = channel("[NHL] Gamma vs Delta (FAWA)", "https://b.example/keep.m3u8")
        notice = ("#EXTINF:-1 tvg-id=\"premiumtv.notice.update\" "
                  "tvg-notice=\"app-update\" group-title=\"PremiumTV Notice\","
                  "UPDATE PremiumTV")
        text = "\n".join([
            "#EXTM3U",
            "# USA working channels (4) - updated now",
            notice,
            "https://github.com/cgyegcvcecvoc/PremiumTV/releases/latest",
            dropped.to_m3u(),
            kept.to_m3u(),
            '#EXTINF:-1 group-title="News",News',
            "https://news.example/live.m3u8",
            "",
        ])
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "USA.m3u"
            path.write_text(text, encoding="utf-8")
            results = gate.sync_derived_playlists([path], {gate._url_hash(dropped)})
            filtered = path.read_text(encoding="utf-8")
        self.assertIn(notice, filtered)
        self.assertIn("# USA working channels (2) - updated now", filtered)
        self.assertEqual(results[0]["entries"], 2)

    def test_publishers_run_the_gate_before_the_category_shelf(self):
        scraper_source = (ROOT / "scripts" / "scraper.py").read_text(encoding="utf-8")
        self.assertIn("live_event_gate.gate_channels", scraper_source)
        for name in ("quick-update.yml", "link-check.yml"):
            workflow = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
            self.assertIn("scripts/live_event_gate.py", workflow, name)
            self.assertIn("--sync-derived", workflow, name)
            self.assertLess(workflow.index("scripts/live_event_gate.py"),
                            workflow.index("build_categories.py"), name)

    def test_fail_closed_withholds_every_event_but_keeps_other_channels(self):
        event = channel("[NHL] Alpha vs Beta (FAWA)", "https://a.example/live.m3u8")
        darts = channel("[Darts] Darts Final (FAWA)", "https://d.example/darts.m3u8")
        ordinary = scraper.Channel("News", "https://news.example/live.m3u8", "news")
        kept, report = gate.fail_closed([event, darts, ordinary], "network unavailable")
        self.assertEqual(kept, [ordinary])
        self.assertEqual(report["refused_fixtures"], 1)
        self.assertEqual(report["non_fixture_entries"], 1)
        self.assertEqual(report["working_entries"], 0)
        self.assertEqual(report["singleton_feeds"][0]["name"], darts.name)
        self.assertEqual(event.status, "unverified")
        self.assertIn("network unavailable", event.reason)
        markdown = gate.render_markdown(report)
        self.assertIn("## Non-matchup event feeds", markdown)
        self.assertIn("Darts Final", markdown)
        self.assertNotIn("No live-event entry was dropped", markdown)

    def test_playlist_apply_withholds_events_when_the_gate_crashes(self):
        text = (
            '#EXTM3U\n'
            '#EXTINF:-1 group-title="Live Events",[Football] Alpha vs. Beta 1\n'
            '#EXTVLCOPT:http-user-agent=Test UA\n'
            'https://a.example/1.m3u8\n'
            '#EXTINF:-1 group-title="News",News One\n'
            'https://n.example/1.m3u8\n'
        )
        with patch.object(gate, "gate_channels", side_effect=RuntimeError("boom")):
            filtered, report = gate.apply_to_playlist_text(text)
        self.assertIn("News One", filtered)
        self.assertNotIn("[Football] Alpha vs. Beta", filtered)
        self.assertEqual(report["entries"], 1)
        self.assertEqual(report["refused_fixtures"], 1)
        self.assertIn("boom", report["error"])

    def test_scraper_calls_the_gate_before_publishing(self):
        """A refused fixture must not appear in PremiumTV.m3u."""
        import json
        import tempfile
        from contextlib import redirect_stdout
        from io import StringIO

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "events.m3u"
            source.write_text(
                "#EXTM3U\n"
                '#EXTINF:-1 tvg-id="NHL.Hockey.Dummy.us",[NHL] Alpha vs Beta\n'
                "https://a.example/live.m3u8\n"
                '#EXTINF:-1 group-title="News",News\n'
                "https://news.example/live.m3u8\n"
                '#EXTINF:-1 tvg-id="NHL.Hockey.Dummy.us",[NHL] Gamma vs Delta\n'
                "https://b.example/live.m3u8\n",
                encoding="utf-8",
            )
            config = root / "sources.json"
            config.write_text(json.dumps({"sources": [{
                "name": "events", "type": "m3u", "local_path": str(source),
                "url": "https://example.test/events.m3u",
            }]}), encoding="utf-8")
            out = root / "playlists"
            args = ["scraper.py", "--sources", str(config), "--out", str(out),
                    "--workers", "2", "--timeout", "2"]

            def check(ch, *args):
                ch.status = "alive"
                return ch

            def gate(channels, **kwargs):
                # Alpha has one working feed; Gamma's only feed is 404.
                kept = [ch for ch in channels if ch.url != "https://b.example/live.m3u8"]
                return kept, {
                    "entries": 2, "working_entries": 1, "dropped_entries": 1,
                    "dropped_403": 0, "dropped_404": 1, "dropped_other": 0,
                    "published_fixtures": 1, "refused_fixtures": 1,
                }

            with patch.object(sys, "argv", args), \
                 patch.object(scraper, "check_channel", side_effect=check), \
                 patch.object(scraper.live_event_gate, "gate_channels", side_effect=gate), \
                 redirect_stdout(StringIO()):
                self.assertEqual(scraper.main(), 0)
            published = (out / "PremiumTV.m3u").read_text(encoding="utf-8")
            self.assertIn("Alpha vs Beta", published)
            self.assertIn("News", published)
            self.assertNotIn("Gamma vs Delta", published)
            report = json.loads((out / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["live_event_gate"]["dropped_404"], 1)
            self.assertEqual(report["live_event_gate"]["refused_fixtures"], 1)


if __name__ == "__main__":
    unittest.main()
