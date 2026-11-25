"""The release gate for the packaged local-channel directory.

The check runs on the APK and DMG themselves, so these tests pin its judgement
(what counts as a stale or mismatched bundle) and the APK reader.  DMG reading
uses hdiutil or 7-Zip and is exercised by the build workflows on the real
installer.
"""

import copy
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import verify_release_bundle as verify  # noqa: E402

CHANNEL_IDS = {
    "WGAL": "NBC.us@WGAL",
    "WHP": "CBS.us@WHP",
    "WPMT": "FOX.us@WPMT",
}


def _stations():
    return [
        {
            "callsign": callsign,
            "channel_id": channel_id,
            "name": f"{callsign} test",
            "city": "Test",
            "network": "",
            "url": f"https://example.test/{callsign.lower()}",
            "backup_urls": [],
        }
        for callsign, channel_id in CHANNEL_IDS.items()
    ]


def _directory():
    stations = _stations()
    return {
        "schema": 2,
        "markets": [
            {"id": "USLNS", "city": "Lancaster", "state": "PA", "stations": copy.deepcopy(stations)},
            {"id": "USHAR", "city": "Harrisburg", "state": "PA", "stations": copy.deepcopy(stations)},
            {"id": "USTHV", "city": "York", "state": "PA", "stations": copy.deepcopy(stations)},
        ],
        "zip_prefixes": [
            {"prefix": prefix, "state": "PA", "market": market}
            for prefix, market in verify.EXPECTED_PREFIX_MARKETS.items()
        ],
        "station_count": 9,
        "market_count": 3,
    }


def _meta(document):
    return {"version": "1.1.23", "channel_count": 3, "local_channels": document}


class DirectoryCheckTests(unittest.TestCase):
    def test_the_expected_area_passes(self):
        document = _directory()
        self.assertEqual(verify.directory_problems(document), [])

    def test_a_prefix_pointing_at_the_wrong_market_fails(self):
        document = _directory()
        document["zip_prefixes"] = [
            row if row["prefix"] != "175" else {**row, "market": "USHAR"}
            for row in document["zip_prefixes"]
        ]
        problems = verify.directory_problems(document)
        self.assertTrue(any("ZIP prefix 175" in problem and "USHAR" in problem
                            for problem in problems), problems)

    def test_a_market_missing_one_station_fails(self):
        document = _directory()
        harrisburg = next(market for market in document["markets"] if market["id"] == "USHAR")
        harrisburg["stations"] = [station for station in harrisburg["stations"]
                                  if station["callsign"] != "WPMT"]
        problems = verify.directory_problems(document)
        self.assertTrue(any("USHAR" in problem and "WPMT" in problem
                            for problem in problems), problems)

    def test_a_wrong_channel_id_fails(self):
        document = _directory()
        york = next(market for market in document["markets"] if market["id"] == "USTHV")
        wpmt = next(station for station in york["stations"] if station["callsign"] == "WPMT")
        wpmt["channel_id"] = "FOX.us@WPMT-OLD"
        problems = verify.directory_problems(document)
        self.assertTrue(any("channel_id" in problem and "WPMT" in problem
                            for problem in problems), problems)


class BundleCheckTests(unittest.TestCase):
    def test_meta_must_match_the_bundled_directory(self):
        document = _directory()
        meta = _meta(copy.deepcopy(document))
        meta["local_channels"]["zip_prefixes"] = [
            row if row["prefix"] != "173" else {**row, "market": "USLNS"}
            for row in meta["local_channels"]["zip_prefixes"]
        ]
        problems = verify.bundle_problems(document, meta, CHANNEL_IDS.values())
        self.assertTrue(any("differs from bundle/local-channels.json" in problem
                            for problem in problems), problems)

    def test_the_playlist_must_contain_the_station_ids(self):
        document = _directory()
        problems = verify.bundle_problems(
            document, _meta(document), ["NBC.us@WGAL", "CBS.us@WHP"]
        )
        self.assertTrue(any("FOX.us@WPMT" in problem and "not in the packaged playlist" in problem
                            for problem in problems), problems)

    def test_a_complete_bundle_passes(self):
        document = _directory()
        self.assertEqual(
            verify.bundle_problems(document, _meta(document), CHANNEL_IDS.values()),
            [],
        )


class ApkReaderTests(unittest.TestCase):
    def _apk(self, directory, meta, channel_rows):
        path = Path(self.tmp.name) / "app-debug.apk"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("assets/bundle/local-channels.json",
                             json.dumps(directory))
            archive.writestr("assets/bundle/meta.json", json.dumps(meta))
            archive.writestr("assets/bundle/channels.jsonl",
                             "\n".join(json.dumps(row) for row in channel_rows) + "\n")
        return path

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def test_reads_the_packaged_apk_bundle(self):
        document = _directory()
        rows = [{"id": channel_id, "url": f"https://example.test/{callsign.lower()}"}
                for callsign, channel_id in CHANNEL_IDS.items()]
        path = self._apk(document, _meta(document), rows)
        bundle = verify.read_bundle(path, "apk")
        self.assertEqual(
            verify.bundle_problems(bundle.document, bundle.meta, bundle.channel_ids),
            [],
        )

    def test_an_apk_without_the_directory_is_rejected(self):
        path = Path(self.tmp.name) / "empty.apk"
        with zipfile.ZipFile(path, "w") as archive:
            archive.writestr("AndroidManifest.xml", "not a real manifest")
        with self.assertRaises(verify.BundleError):
            verify.read_bundle(path, "apk")


class WorkflowGateTests(unittest.TestCase):
    def test_both_installer_builds_run_the_check(self):
        for name in ("android-build.yml", "macos-build.yml"):
            text = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
            self.assertIn("verify_release_bundle.py", text, name)


if __name__ == "__main__":
    unittest.main()
