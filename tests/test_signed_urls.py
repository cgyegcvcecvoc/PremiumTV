"""Offline regression tests for signed curated stream URLs.

Some curated doors only generate a manifest when a signed query travels with
the request. WGAL's Uplynk/CloudFront address is one: on 2026-11-25 ten probes
requested it without its ``Signature``/``Policy``/``Key-Pair-Id`` parameters,
read the resulting HTTP 504 ("Unable to obtain template playlist") as an
outage, and filed issues #149-#156. The feed was answering 200 the whole time
for the address actually published.

These tests are offline - they never fetch a stream. They pin two rules:

* a URL that carries any signing parameter must carry all of them, with
  non-empty values, so a trimmed edit cannot publish a half-signed address;
* the WGAL Uplynk door is recognised by host and asset id alone, so stripping
  every query parameter cannot make it look like a different, unsigned feed.
"""
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "playlists" / "sources"

# The published copies of the curated local channels. A scrape that rewrites
# the playlist must not shorten the signing query either.
PUBLISHED_PLAYLISTS = (
    ROOT / "playlists" / "live" / "USA.m3u",
    ROOT / "categories" / "USA.m3u",
)

# CloudFront signed URLs need this trio; any one of them alone is rejected.
SIGNING_PARAMS = ("Signature", "Key-Pair-Id", "Policy")

WGAL_UPLYNK_HOST = "d2b9k7mmyhvjw4.cloudfront.net"
WGAL_ASSET = "90f3abbfb17a4b6eba96038b1d4bd051"


def m3u_urls(path: Path) -> list:
    """Every non-comment http(s) line of an M3U file, stripped."""
    text = path.read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines()
            if line.strip().startswith(("http://", "https://"))]


def query_params(url: str) -> dict:
    """Query parameters with blank values kept, so an empty Signature is visible."""
    return parse_qs(urlsplit(url).query, keep_blank_values=True)


class SignedCuratedUrlsTest(unittest.TestCase):

    def test_partially_signed_urls_are_fully_signed(self):
        """Any URL carrying a signing parameter carries all of them, non-empty."""
        failures = []
        for path in sorted(SOURCES.glob("*.m3u")):
            for url in m3u_urls(path):
                params = query_params(url)
                if not any(name in params for name in SIGNING_PARAMS):
                    continue
                missing = [n for n in SIGNING_PARAMS if n not in params]
                empty = [n for n in SIGNING_PARAMS
                         if n in params and not params[n][0]]
                if missing or empty:
                    failures.append(
                        f"{path.relative_to(ROOT)}: missing={missing} "
                        f"empty={empty} {url[:140]}")
        self.assertEqual(failures, [],
                         "signed curated URL lost part of its signing query")

    def test_wgal_uplynk_door_keeps_its_signing(self):
        """Host + asset id identify the door; it must publish the full query."""
        path = SOURCES / "local-channels.m3u"
        doors = [u for u in m3u_urls(path)
                 if WGAL_UPLYNK_HOST in u and WGAL_ASSET in u]
        self.assertEqual(len(doors), 1,
                         "expected exactly one WGAL Uplynk door, "
                         f"found {len(doors)}")
        params = query_params(doors[0])
        self.assertEqual(sorted(set(SIGNING_PARAMS) & set(params)),
                         sorted(SIGNING_PARAMS),
                         "the WGAL Uplynk address lost its Signature/Policy/"
                         "Key-Pair-Id; an unsigned request answers 504, which "
                         "is a signature check, not an outage")
        for name in SIGNING_PARAMS:
            self.assertTrue(params[name][0], f"{name} is blank")

    def test_published_playlists_keep_the_wgal_signing(self):
        """A scrape that rewrites the playlists must not shorten the query."""
        for path in PUBLISHED_PLAYLISTS:
            if not path.exists():
                continue
            doors = [u for u in m3u_urls(path) if WGAL_UPLYNK_HOST in u]
            self.assertEqual(len(doors), 1,
                             f"{path.relative_to(ROOT)}: expected one WGAL "
                             f"Uplynk entry, found {len(doors)}")
            params = query_params(doors[0])
            missing = [n for n in SIGNING_PARAMS if not params.get(n, [""])[0]]
            self.assertEqual(missing, [],
                             f"{path.relative_to(ROOT)} published the WGAL "
                             f"Uplynk address without {missing}")

    def test_local_now_backup_keeps_its_advertising_query(self):
        """The Local Now stitcher answers 400 unless that query travels whole."""
        path = SOURCES / "local-channels.m3u"
        doors = [u for u in m3u_urls(path)
                 if "localnow.api.cms.amdvids.com" in u and WGAL_ASSET in u]
        self.assertEqual(len(doors), 1)
        params = query_params(doors[0])
        self.assertIn("ads.playbackid", params)
        self.assertIn("ads.v4", params)


if __name__ == "__main__":
    unittest.main()
