#!/usr/bin/env python3
"""Generate the download site's data files from the repository itself.

The site under ``docs/`` (GitHub Pages) is static: it downloads nothing from the
repository at build time and runs no server. Everything it shows - the country
list with channel counts, the app download cards with sizes and checksums, the
change log timeline and the Atom feed - is generated here from files this
repository already publishes:

    playlists/countries/*.m3u   -> country list + per-country channel counts
    playlists/report.json       -> latest run stats (confirmed channels, run id)
    playlists/STATUS.md         -> latest run label
    EPG/*.xml                   -> which country guides exist
    release-notes-*.md          -> one-line summaries for the download cards
    build-out/SHA256SUMS*.txt   -> checksums shown next to each file
    docs/data/releases.src.json -> GitHub release assets (refresh with gh api)
    CHANGELOG.md                -> the changelog timeline + Atom feed

Outputs (all committed):

    docs/data/site-data.js      window.SITE_DATA = {...}  (script-tag include,
                              so the page works even where fetch is blocked)
    docs/data/site.json         the same payload, for other tools
    docs/data/changelog.json    structured changelog entries
    docs/feed.xml               Atom feed of the changelog ("subscribe to
                              updates" - every change the project records)

Change-log policy: every change made to this repository is recorded in
CHANGELOG.md under a dated heading, and this script is re-run so the site and
the feed show it. If you changed something and the site does not show it, run:

    python scripts/build_site_data.py

    python scripts/build_site_data.py            # regenerate everything
    python scripts/build_site_data.py --check    # exit 1 if outputs are stale
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
DATA = DOCS / "data"

REPO_OWNER = "cgyegcvcecvoc"
REPO_NAME = "PremiumTV1"
REPO_BRANCH = "main"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{REPO_BRANCH}"
RELEASES_BASE = f"https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/download"
PAGES_URL = f"https://{REPO_OWNER}.github.io/{REPO_NAME}/"
GOOGLE_DOC_CHANGELOG = ("https://docs.google.com/document/d/"
                        "1anjXfhv6qXz9ZsSldHBMqsfDt8d44W8N_ayqYAloeNM/edit?usp=drivesdk")

# ISO 3166-1 alpha-2 for every country playlist. Region playlists that are not
# countries (International, Arab_World, Latin_America) map to None and are
# shown as regions on the site.
ISO2 = {
    "Afghanistan": "AF", "Albania": "AL", "Algeria": "DZ", "Andorra": "AD",
    "Angola": "AO", "Antigua_and_Barbuda": "AG", "Arab_World": None,
    "Argentina": "AR", "Armenia": "AM", "Aruba": "AW", "Australia": "AU",
    "Austria": "AT", "Azerbaijan": "AZ", "Bahamas": "BS", "Bahrain": "BH",
    "Bangladesh": "BD", "Barbados": "BB", "Belarus": "BY", "Belgium": "BE",
    "Belize": "BZ", "Benin": "BJ", "Bolivia": "BO",
    "Bosnia_and_Herzegovina": "BA", "Brazil": "BR",
    "British_Virgin_Islands": "VG", "Bulgaria": "BG", "Burkina_Faso": "BF",
    "Burundi": "BI", "Cambodia": "KH", "Cameroon": "CM", "Canada": "CA",
    "Cape_Verde": "CV", "Caribbean_Netherlands": "BQ", "Chad": "TD",
    "Chile": "CL", "China": "CN", "Colombia": "CO", "Costa_Rica": "CR",
    "Croatia": "HR", "Cuba": "CU", "Curacao": "CW", "Cyprus": "CY",
    "Czechia": "CZ", "DR_Congo": "CD", "Denmark": "DK",
    "Dominican_Republic": "DO", "Ecuador": "EC", "Egypt": "EG",
    "El_Salvador": "SV", "Equatorial_Guinea": "GQ", "Eritrea": "ER",
    "Estonia": "EE", "Ethiopia": "ET", "Faroe_Islands": "FO", "Finland": "FI",
    "France": "FR", "French_Guiana": "GF", "Gambia": "GM", "Georgia": "GE",
    "Germany": "DE", "Ghana": "GH", "Greece": "GR", "Guadeloupe": "GP",
    "Guam": "GU", "Guatemala": "GT", "Guinea": "GN", "Guyana": "GY",
    "Haiti": "HT", "Honduras": "HN", "Hong_Kong": "HK", "Hungary": "HU",
    "Iceland": "IS", "India": "IN", "Indonesia": "ID", "International": None,
    "Iran": "IR", "Iraq": "IQ", "Ireland": "IE", "Israel": "IL", "Italy": "IT",
    "Ivory_Coast": "CI", "Jamaica": "JM", "Japan": "JP", "Jordan": "JO",
    "Kazakhstan": "KZ", "Kenya": "KE", "Kosovo": "XK", "Kuwait": "KW",
    "Kyrgyzstan": "KG", "Laos": "LA", "Latin_America": None, "Latvia": "LV",
    "Lebanon": "LB", "Libya": "LY", "Lithuania": "LT", "Luxembourg": "LU",
    "Malaysia": "MY", "Maldives": "MV", "Mali": "ML", "Malta": "MT",
    "Martinique": "MQ", "Mexico": "MX", "Moldova": "MD", "Monaco": "MC",
    "Mongolia": "MN", "Montenegro": "ME", "Morocco": "MA", "Mozambique": "MZ",
    "Myanmar": "MM", "Namibia": "NA", "Nepal": "NP", "Netherlands": "NL",
    "New_Zealand": "NZ", "Nicaragua": "NI", "Niger": "NE", "Nigeria": "NG",
    "North_Korea": "KP", "North_Macedonia": "MK", "Norway": "NO", "Oman": "OM",
    "Pakistan": "PK", "Palestine": "PS", "Panama": "PA",
    "Papua_New_Guinea": "PG", "Paraguay": "PY", "Peru": "PE",
    "Philippines": "PH", "Poland": "PL", "Portugal": "PT", "Puerto_Rico": "PR",
    "Qatar": "QA", "Republic_of_the_Congo": "CG", "Romania": "RO",
    "Russia": "RU", "Rwanda": "RW", "Saint_Kitts_and_Nevis": "KN",
    "Saint_Lucia": "LC", "Saudi_Arabia": "SA", "Senegal": "SN", "Serbia": "RS",
    "Sierra_Leone": "SL", "Singapore": "SG", "Sint_Maarten": "SX",
    "Slovakia": "SK", "Slovenia": "SI", "Somalia": "SO", "South_Africa": "ZA",
    "South_Korea": "KR", "Spain": "ES", "Sri_Lanka": "LK", "Sudan": "SD",
    "Suriname": "SR", "Sweden": "SE", "Switzerland": "CH", "Syria": "SY",
    "Taiwan": "TW", "Tanzania": "TZ", "Thailand": "TH", "Togo": "TG",
    "Trinidad_and_Tobago": "TT", "Tunisia": "TN", "Turkey": "TR",
    "Turkmenistan": "TM", "UK": "GB", "USA": "US", "Uganda": "UG",
    "Ukraine": "UA", "United_Arab_Emirates": "AE", "Uruguay": "UY",
    "Uzbekistan": "UZ", "Venezuela": "VE", "Vietnam": "VN",
    "Western_Sahara": "EH", "Yemen": "YE", "Zimbabwe": "ZW",
}
DISPLAY_NAME = {
    "USA": "United States", "UK": "United Kingdom",
    "DR_Congo": "DR Congo", "Republic_of_the_Congo": "Republic of the Congo",
    "Ivory_Coast": "Ivory Coast", "Bosnia_and_Herzegovina": "Bosnia & Herzegovina",
    "United_Arab_Emirates": "United Arab Emirates",
    "Antigua_and_Barbuda": "Antigua & Barbuda",
    "British_Virgin_Islands": "British Virgin Islands",
    "Saint_Kitts_and_Nevis": "St Kitts & Nevis", "Saint_Lucia": "St Lucia",
    "Trinidad_and_Tobago": "Trinidad & Tobago",
    "Cape_Verde": "Cape Verde", "Sint_Maarten": "Sint Maarten",
    "Caribbean_Netherlands": "Caribbean Netherlands",
    "Equatorial_Guinea": "Equatorial Guinea",
    "Dominican_Republic": "Dominican Republic",
    "El_Salvador": "El Salvador", "Papua_New_Guinea": "Papua New Guinea",
    "North_Macedonia": "North Macedonia", "Hong_Kong": "Hong Kong",
    "Faroe_Islands": "Faroe Islands", "Western_Sahara": "Western Sahara",
    "Latin_America": "Latin America", "Arab_World": "Arab World",
}

# Which channel each published release is. Anything not listed here shows on
# the site as an older release. Sizes come from docs/data/releases.src.json.
CHANNELS = [
    {
        "id": "stable",
        "tag": "v1.0.2",
        "version": "1.0.2",
        "channel": "Stable",
        "badge": "Recommended",
        "summary": "USA lineup + USA guide. The default download.",
        "notes_file": "release-notes-1.0.2.md",
        "min_os": "macOS 12 (Monterey) or later · Android 5.0+ (TV, tablet, phone)",
    },
    {
        "id": "preview",
        "tag": "v1.1.1",
        "version": "1.1.1",
        "channel": "Preview",
        "badge": "Pre-release",
        "summary": "Global checked lineup + merged guide + cable-style Guide grid.",
        "notes_file": "release-notes-1.1.1.md",
        "min_os": "macOS 12 (Monterey) or later · Android 5.0+ (TV, tablet, phone)",
    },
]


def log(msg: str) -> None:
    print(msg, flush=True)


def iso_time(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def count_entries(path: Path) -> int:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    return sum(1 for line in text.splitlines() if line.startswith("#EXTINF"))


def load_checksums() -> dict[str, str]:
    sums: dict[str, str] = {}
    for name in ("SHA256SUMS.txt", "SHA256SUMS-android.txt"):
        path = ROOT / "build-out" / name
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = line.split()
            if len(parts) >= 2:
                sums[parts[-1].strip().lstrip("*")] = parts[0].strip()
    return sums


def load_releases() -> list[dict]:
    path = DATA / "releases.src.json"
    if path.is_file():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, list):
                return data
        except (OSError, ValueError):
            pass
    log("[site] warning: docs/data/releases.src.json missing - app cards will "
        "have links but no sizes")
    return []


def classify_asset(name: str) -> tuple[str, str]:
    """Return (kind, arch) for a release asset name."""
    lower = name.lower()
    if lower.endswith(".apk"):
        return "android", "universal"
    if "mac-arm64" in lower:
        return ("macos-dmg" if lower.endswith(".dmg") else "macos-pkg"), "arm64"
    if "mac-x64" in lower:
        return ("macos-dmg" if lower.endswith(".dmg") else "macos-pkg"), "x64"
    if "sha256" in lower:
        return "checksum", "—"
    return "other", "—"


def build_apps(checksums: dict[str, str], releases: list[dict]) -> tuple[list[dict], list[dict]]:
    by_tag = {r.get("tag"): r for r in releases}
    channels = []
    for spec in CHANNELS:
        release = by_tag.get(spec["tag"], {})
        assets = []
        for asset in release.get("assets") or []:
            kind, arch = classify_asset(asset.get("name", ""))
            assets.append({
                "name": asset.get("name", ""),
                "kind": kind,
                "arch": arch,
                "size": int(asset.get("size") or 0),
                "url": asset.get("browser_download_url")
                       or f"{RELEASES_BASE}/{spec['tag']}/{asset.get('name', '')}",
                "sha256": checksums.get(asset.get("name", "")),
            })
        notes_title, notes_summary = read_release_notes(spec.get("notes_file", ""))
        channels.append({
            **spec,
            "published_at": release.get("published_at", ""),
            "html_url": release.get("html_url",
                                    f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
                                    f"/releases/tag/{spec['tag']}"),
            "notes_title": notes_title,
            "notes_summary": notes_summary,
            "assets": assets,
        })
    older = []
    for tag, release in sorted(by_tag.items(), reverse=True):
        if tag in {c["tag"] for c in CHANNELS} or not tag:
            continue
        older.append({
            "tag": tag,
            "name": release.get("name", tag),
            "published_at": release.get("published_at", ""),
            "html_url": release.get("html_url", ""),
        })
    return channels, older


def read_release_notes(filename: str) -> tuple[str, str]:
    path = ROOT / filename
    if not path.is_file():
        return "", ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    title = ""
    summary = []
    for line in lines:
        if not title:
            if line.startswith("# "):
                title = line[2:].strip()
            continue
        if line.startswith("#"):
            break
        if line.strip():
            summary.append(line.strip())
        if len(summary) >= 3:
            break
    return title, " ".join(summary)[:400]


def build_countries() -> list[dict]:
    countries = []
    epg_dir = ROOT / "EPG"
    for path in sorted((ROOT / "playlists" / "countries").glob("*.m3u")):
        stem = path.stem
        name = DISPLAY_NAME.get(stem, stem.replace("_", " "))
        count = count_entries(path)
        if not count:
            continue
        countries.append({
            "slug": stem,
            "name": name,
            "iso2": ISO2.get(stem),
            "region": ISO2.get(stem) is None,
            "count": count,
            "playlist_url": f"{RAW_BASE}/playlists/countries/{stem}.m3u",
            "epg_url": f"{RAW_BASE}/EPG/{stem}.xml",
            "epg_present": (epg_dir / f"{stem}.xml").is_file(),
        })
    countries.sort(key=lambda c: (c["region"], -c["count"], c["name"]))
    return countries


def build_stats() -> dict:
    stats = {
        "confirmed_channels": None,
        "unique_links": None,
        "countries": None,
        "last_run_utc": None,
        "last_run_label": None,
    }
    report_path = ROOT / "playlists" / "report.json"
    if report_path.is_file():
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            report = {}
        stats["confirmed_channels"] = report.get("working")
        stats["unique_links"] = report.get("total_unique")
        stats["countries"] = report.get("countries_count")
        stats["last_run_utc"] = report.get("updated_utc")
        stats["last_run_label"] = report.get("label")
    return stats


def parse_changelog() -> list[dict]:
    path = ROOT / "CHANGELOG.md"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8", errors="replace")
    entries = []
    current = None
    for line in text.splitlines():
        heading = re.match(r"^##\s+(\d{4}-\d{2}-\d{2})\s+[—-]\s+(.*)$", line)
        if heading:
            if current:
                entries.append(current)
            current = {
                "id": heading.group(1),
                "date": heading.group(1),
                "title": heading.group(2).strip(),
                "body_md": [],
            }
            continue
        if current is not None:
            if line.startswith("## "):
                entries.append(current)
                current = None
                continue
            current["body_md"].append(line)
    if current:
        entries.append(current)
    for entry in entries:
        body = "\n".join(entry["body_md"]).strip()
        entry["body_md"] = body
        bullets = []
        for line in body.splitlines():
            if line.startswith("- "):
                bullets.append(line[2:].strip())
        entry["bullets"] = bullets[:8]
    return entries


def write_feed(entries: list[dict]) -> str:
    updated = iso_time(dt.datetime.now(dt.timezone.utc))
    def esc(text: str) -> str:
        return (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        "  <title>PremiumTV1 change log</title>",
        f"  <id>{PAGES_URL}data/feed.xml</id>",
        f'  <link rel="self" href="{PAGES_URL}data/feed.xml"/>',
        f'  <link rel="alternate" href="https://github.com/{REPO_OWNER}/{REPO_NAME}'
        f'/blob/{REPO_BRANCH}/CHANGELOG.md"/>',
        f"  <updated>{updated}</updated>",
        "  <subtitle>Every change recorded in the PremiumTV1 repository: "
        "playlist fixes, app releases, and site updates.</subtitle>",
    ]
    for index, entry in enumerate(entries):
        when = f"{entry['date']}T12:00:00Z"
        body = "\n".join(entry["bullets"]) or entry["body_md"]
        lines += [
            "  <entry>",
            f"    <title>{esc(entry['title'])}</title>",
            f"    <id>urn:premiumtv1:changelog:{entry['date']}:{index}</id>",
            f"    <link href=\"https://github.com/{REPO_OWNER}/{REPO_NAME}"
            f"/blob/{REPO_BRANCH}/CHANGELOG.md\"/>",
            f"    <updated>{when}</updated>",
            "    <summary>" + esc(re.sub(r"\s+", " ", body))[:600] + "</summary>",
            "  </entry>",
        ]
    lines.append("</feed>")
    return "\n".join(lines) + "\n"


def build_payload() -> tuple[dict, list[dict]]:
    checksums = load_checksums()
    releases = load_releases()
    channels, older = build_apps(checksums, releases)
    countries = build_countries()
    changelog = parse_changelog()
    payload = {
        "generated_utc": iso_time(dt.datetime.now(dt.timezone.utc)),
        "repo": {
            "owner": REPO_OWNER,
            "name": REPO_NAME,
            "branch": REPO_BRANCH,
            "url": f"https://github.com/{REPO_OWNER}/{REPO_NAME}",
            "raw_base": RAW_BASE,
            "pages_url": PAGES_URL,
            "changelog_md": f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
                            f"/blob/{REPO_BRANCH}/CHANGELOG.md",
            "changelog_doc": GOOGLE_DOC_CHANGELOG,
        },
        "stats": build_stats(),
        "playlists": {
            "main": {
                "name": "PremiumTV.m3u",
                "description": "Every confirmed-working channel, grouped by category.",
                "url": f"{RAW_BASE}/playlists/PremiumTV.m3u",
                "count": count_entries(ROOT / "playlists" / "PremiumTV.m3u"),
            },
            "priority": {
                "name": "Priority_Channels.m3u",
                "description": "Nickelodeon, NickToons, MeTV, MeTV Toons, "
                               "NFL Network, NFL RedZone - verified links only.",
                "url": f"{RAW_BASE}/playlists/Priority_Channels.m3u",
                "count": count_entries(ROOT / "playlists" / "Priority_Channels.m3u"),
            },
            "usa": {
                "name": "categories/USA.m3u",
                "description": "Every US channel in category order.",
                "url": f"{RAW_BASE}/categories/USA.m3u",
                "count": count_entries(ROOT / "categories" / "USA.m3u"),
            },
            "ae": {
                "name": "AE_Channels.m3u",
                "description": "A&E and A+E Networks channels, linear and FAST.",
                "url": f"{RAW_BASE}/playlists/AE_Channels.m3u",
                "count": count_entries(ROOT / "playlists" / "AE_Channels.m3u"),
            },
            "guide": {
                "name": "EPG/PremiumTV.xml",
                "description": "Merged XMLTV guide for the whole library.",
                "url": f"{RAW_BASE}/EPG/PremiumTV.xml",
            },
        },
        "apps": {"channels": channels, "older": older},
        "countries": countries,
        "changelog": changelog,
    }
    return payload, changelog


def render_site_data_js(payload: dict) -> str:
    body = json.dumps(payload, indent=1, ensure_ascii=False)
    return ("/* Generated by scripts/build_site_data.py - do not edit by hand. */\n"
            "window.SITE_DATA = " + body + ";\n")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="exit 1 when the generated files are out of date")
    args = ap.parse_args(argv)

    payload, changelog = build_payload()
    DATA.mkdir(parents=True, exist_ok=True)
    outputs = {
        DATA / "site-data.js": render_site_data_js(payload),
        DATA / "site.json": json.dumps(payload, indent=1, ensure_ascii=False) + "\n",
        DATA / "changelog.json": json.dumps(changelog, indent=1, ensure_ascii=False) + "\n",
        DATA / "feed.xml": write_feed(changelog),
    }
    stale = []
    for path, content in outputs.items():
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current != content:
            stale.append(path)
            if not args.check:
                path.write_text(content, encoding="utf-8")
    if args.check:
        if stale:
            for path in stale:
                log(f"[site] stale: {path.relative_to(ROOT)}")
            log("[site] run: python scripts/build_site_data.py")
            return 1
        log("[site] generated files are up to date")
        return 0
    countries = payload["countries"]
    log(f"[site] {len(countries)} countries "
        f"({sum(1 for c in countries if not c['region'])} with ISO codes), "
        f"{len(changelog)} changelog entries, "
        f"{sum(len(c['assets']) for c in payload['apps']['channels'])} app assets")
    for path in outputs:
        log(f"[site] wrote {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
