#!/usr/bin/env python3
"""Curated upstream XMLTV sources, one family per published country.

The merged guide (``EPG/PremiumTV.xml``) and every country guide are built from
verified upstream XMLTV feeds. Before this module the harvest only saw the two
or three guides a scraped M3U happened to advertise in its own ``x-tvg-url``
header, which left most published channels without a single listing.

This module answers "which public guide should cover this channel?" for every
country the repository publishes:

* ``https://iptv-epg.org/files/epg-<cc>.xml.gz`` - the per-country files
  iptv-epg.org publishes (76 countries; ``epg-us.xml`` is the US one),
* ``https://epg.pw/xmltv/epg_<CC>.xml.gz`` - epg.pw's per-country XMLTV set
  (21 countries, ISO-upper file names),
* ``https://epg.pw/xmltv/epg.xml.gz`` - epg.pw's all-countries file, the
  one-for-all feed for channels whose country has no dedicated file.

Both families are configured in ``sources.json`` under ``epg_sources``; this
module only expands the templates. ``{cc}`` is the lowercase ISO code and
``{CC}`` the uppercase form, so the two file-naming conventions can both be
expressed. Countries the templates cannot describe (``International``,
``Arab World``, ``Latin America``, ...) get the all-countries feed only.

The curated URLs are verified by ``scripts/epg_check.py`` on every run and
merged by ``scripts/epg_build.py`` before the guides found in playlist
headers. They are deliberately never advertised in a playlist ``x-tvg-url``
header: the merged guide already carries their listings, and a player should
not have to download several hundred megabytes of upstream XMLTV on top.

    python scripts/epg_sources.py             # print the curated URL list
    python scripts/epg_sources.py --check     # + what each URL was made from
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scraper  # noqa: E402  (shares the country name/code tables)

ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = ROOT / "sources.json"
CONFIG_KEY = "epg_sources"

# 'uk' is a legacy alias in the scraper's country table; ISO 3166 says GB.
CC_ALIASES = {"uk": "gb"}

# Long-form names guides and metadata use, beyond the scraper's short labels.
NAME_ALIASES = {
    "United Kingdom": "gb",
    "Great Britain": "gb",
    "United States": "us",
    "United States of America": "us",
    "Russian Federation": "ru",
    "Vietnam": "vn",
    "Viet Nam": "vn",
    "South Korea": "kr",
    "Republic of Korea": "kr",
    "North Korea": "kp",
    "Czech Republic": "cz",
    "Ivory Coast": "ci",
    "Cote d'Ivoire": "ci",
    "Taiwan": "tw",
    "Tanzania": "tz",
    "Venezuela": "ve",
    "Bolivia": "bo",
    "Moldova": "md",
    "Syria": "sy",
    "Iran": "ir",
    "Laos": "la",
    "Brunei": "bn",
    "Palestine": "ps",
    "Macedonia": "mk",
    "East Timor": "tl",
    "Timor-Leste": "tl",
    "Swaziland": "sz",
    "Eswatini": "sz",
    "Cape Verde": "cv",
    "Cabo Verde": "cv",
    "Macau": "mo",
    "Hong Kong": "hk",
    "Puerto Rico": "pr",
    "Netherlands": "nl",
    "The Netherlands": "nl",
}


def log(msg: str) -> None:
    print(msg, flush=True)


def country_code(raw: str) -> str:
    """ISO-3166 alpha-2 code for a country display name or code, or ``""``.

    ``"USA"`` / ``"US"`` -> ``"us"``, ``"UK"`` / ``"United Kingdom"`` -> ``"gb"``,
    ``"International"`` -> ``""`` (no per-country guide exists).
    """
    raw = (raw or "").strip()
    if not raw:
        return ""
    code = scraper.COUNTRY_NAME_TO_CODE.get(raw)
    if not code:
        code = NAME_ALIASES.get(raw)
    if not code:
        low = raw.lower()
        canon = scraper.COUNTRY_NAME_LOOKUP.get(low)
        if canon:
            code = scraper.COUNTRY_NAME_TO_CODE.get(canon) or NAME_ALIASES.get(canon)
        if not code:
            for name, alias in NAME_ALIASES.items():
                if name.lower() == low:
                    code = alias
                    break
        if not code and low in scraper.COUNTRY_CODE_MAP:
            code = low
    if not code:
        return ""
    return CC_ALIASES.get(code, code)


def norm_cc(raw: str) -> str:
    """Canonical lowercase code for comparison (``UK``/``uk`` -> ``gb``)."""
    code = (raw or "").strip().lower()
    return CC_ALIASES.get(code, code)


CC_IN_URL_RE = re.compile(r"(?:epg[-_])([a-z]{2})(?:\.xml)", re.IGNORECASE)


def guide_url_country(url: str) -> str:
    """Country code implied by a per-country guide URL, or ``""``.

    ``https://epg.pw/xmltv/epg_DE.xml.gz`` -> ``de`` and
    ``https://iptv-epg.org/files/epg-us.xml.gz`` -> ``us``, so every channel in
    that file can be matched as the country it belongs to, even when the same
    display name exists in several countries. All-countries files (``epg.xml``)
    and unrelated hosts return ``""`` and stay suffix/name-driven.
    """
    name = (url or "").split("?", 1)[0].rsplit("/", 1)[-1]
    match = CC_IN_URL_RE.search(name)
    return norm_cc(match.group(1)) if match else ""


def load_config(path: Path | None = None) -> dict:
    """The ``epg_sources`` block of ``sources.json`` (empty dict if absent)."""
    source = Path(path) if path else SOURCES_FILE
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    block = data.get(CONFIG_KEY)
    return block if isinstance(block, dict) else {}


def expand_template(template: str, code: str) -> str:
    """``https://epg.pw/xmltv/epg_{CC}.xml.gz`` + ``gb`` -> ``...epg_GB.xml.gz``."""
    return template.replace("{CC}", code.upper()).replace("{cc}", code.lower())


def configured_urls(config: dict, country_codes: list[str]) -> list[dict]:
    """Every curated guide as ``{name, url, origin}``, ordered and de-duplicated.

    ``fixed`` entries come first (the all-countries feeds), then one entry per
    enabled ``per_country`` template for every published country code. A URL
    produced twice (the US file is both "fixed" and derived) is kept once.
    """
    entries: list[dict] = []
    seen: set[str] = set()

    def add(name: str, url: str, origin: str) -> None:
        url = url.strip()
        if not url or url in seen:
            return
        seen.add(url)
        entries.append({"name": name, "url": url, "origin": origin})

    for item in config.get("fixed", []):
        if isinstance(item, dict) and item.get("enabled", True):
            add(item.get("name", "curated guide"), item.get("url", ""), "fixed")
    for item in config.get("per_country", []):
        if not (isinstance(item, dict) and item.get("enabled", True)):
            continue
        template = item.get("url_template", "")
        name = item.get("name", "curated guide")
        for code in country_codes:
            if template and code:
                add(f"{name} ({code})", expand_template(template, code), code)
    return entries


def published_country_codes(countries_dir: Path) -> list[str]:
    """Codes for every published country playlist, stable order, no duplicates.

    A playlist filename is a display-name slug (``South_Korea.m3u``); the
    country tables in ``scraper.py`` translate it. Pseudo-regions without an
    ISO code are skipped - the all-countries feeds cover them.
    """
    codes: list[str] = []
    seen: set[str] = set()
    if not Path(countries_dir).is_dir():
        return codes
    for path in sorted(Path(countries_dir).glob("*.m3u")):
        code = country_code(path.stem.replace("_", " "))
        if code and code not in seen:
            seen.add(code)
            codes.append(code)
    return codes


def curated_guides(countries_dir: Path, config: dict | None = None) -> list[dict]:
    """The full curated list for one run: fixed feeds plus per-country feeds."""
    block = load_config() if config is None else config
    if not block.get("enabled", True):
        return []
    return configured_urls(block, published_country_codes(countries_dir))


def curated_guide_urls(countries_dir: Path, config: dict | None = None) -> list[str]:
    """Just the URLs, the form ``epg_check``/``epg_build`` merge into their runs."""
    return [entry["url"] for entry in curated_guides(countries_dir, config)]


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--countries", default=str(ROOT / "playlists" / "countries"),
                    help="published country-playlist directory")
    ap.add_argument("--check", action="store_true",
                    help="show which country each per-country URL came from")
    return ap


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    entries = curated_guides(Path(args.countries))
    for entry in entries:
        if args.check:
            log(f"{entry['url']}  [{entry['origin']}]  {entry['name']}")
        else:
            log(entry["url"])
    log(f"[epg-sources] {len(entries)} curated guide URL(s) for "
        f"{len(published_country_codes(Path(args.countries)))} published countries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
