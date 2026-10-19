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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import legacy_sunset  # noqa: E402  (which USA feed is still being updated)

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
        "tag": "v1.0.6.1",
        "version": "1.0.6.1",
        "channel": "Stable",
        "badge": "Recommended",
        "summary": "Settings 2.0 — compact version card, one-tap force refresh, update check and a built-in bug check. USA lineup + USA guide.",
        "notes_file": "release-notes-1.0.6.1.md",
        "min_os": "macOS 12 (Monterey) or later · Android 6.0+ (TV, tablet, phone)",
    },
]

# Retired preview builds are deliberately absent from the download page. Their
# release pages may still exist for the historical record, but the site must
# never offer a download that points at a retired channel.
RETIRED_TAGS = {"v1.1.0", "v1.1.1"}

# Releases published only so an updater that reads three-part versions
# (1.0.4-1.0.6) can reach the canonical build.  They are the same code and
# never replace it as the advertised download.  The policy lives in
# scripts/release_version.py so the workflows, the site and both apps agree.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from release_version import COMPATIBILITY_ALIASES, macos_version  # noqa: E402

ALIAS_TAGS = {f"v{alias}" for alias in COMPATIBILITY_ALIASES}


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


def release_tag(release: dict) -> str:
    """Accept the checked-in compact format and GitHub's release API format."""
    return str(release.get("tag") or release.get("tag_name") or "")


def asset_digest(asset: dict) -> str | None:
    """Return the bare SHA-256 from GitHub's ``digest`` field, when present.

    The release API exposes ``sha256:<hex>`` for every uploaded asset.  Using
    it keeps checksums on the download page even when the workflow no longer
    has that release's build-out/ directory checked out.
    """
    digest = str(asset.get("digest") or "").strip()
    prefix, _, value = digest.partition(":")
    if prefix.lower() != "sha256" or not value:
        return None
    value = value.strip().lower()
    return value if re.fullmatch(r"[0-9a-f]{64}", value) else None


MAC_ASSET_SUFFIXES = ("mac-arm64.dmg", "mac-arm64.pkg", "mac-x64.dmg", "mac-x64.pkg")


def mac_assets_for(version: str, releases: list[dict]) -> tuple[set[str], dict | None, str | None]:
    """The Mac installer names belonging to a canonical stable version.

    macOS packaging only accepts three-part versions, so a four-part hotfix is
    built as its compatibility alias and those installers live on the alias
    release (1.0.6.1 -> v1.0.7).  Returns the required asset names, the release
    that carries them, and the version printed in their file names.
    """
    mac_version = macos_version(version)
    if mac_version is None:
        return set(), None, None
    required = {f"PremiumTV-{mac_version}-{suffix}" for suffix in MAC_ASSET_SUFFIXES}
    for release in releases:
        if release_tag(release) != f"v{mac_version}":
            continue
        if release.get("draft") or release.get("prerelease"):
            continue
        available = {a.get("name", "") for a in release.get("assets") or []}
        if required.issubset(available):
            return required, release, mac_version
    return set(), None, mac_version


def latest_complete_stable_release(releases: list[dict]) -> dict | None:
    """Pick the newest published stable release only after every app installer exists.

    A release can be published before the platform build jobs finish attaching
    their assets. Keeping the previous complete stable download live during that
    window is better than advertising a version with no working download links.
    """
    candidates = []
    for release in releases:
        tag = release_tag(release)
        if release.get("draft") or release.get("prerelease"):
            continue
        match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?", tag)
        if not match:
            continue
        version = ".".join(part for part in match.groups() if part is not None)
        if tag in RETIRED_TAGS or tag in ALIAS_TAGS:
            continue
        available = {a.get("name", "") for a in release.get("assets") or []}
        # The APK belongs to this release; the Mac installers may live on the
        # compatibility alias, because macOS packaging needs three parts.
        mac_required, mac_release, _ = mac_assets_for(version, releases)
        mac_available = {a.get("name", "") for a in (mac_release or {}).get("assets") or []}
        if (f"PremiumTV-{version}-debug.apk" in available
                and mac_release is not None and mac_required <= mac_available):
            numbers = tuple(int(part) for part in match.groups() if part is not None)
            candidates.append((numbers + (0,) * (4 - len(numbers)), release))
    return max(candidates, key=lambda item: item[0])[1] if candidates else None


def build_apps(checksums: dict[str, str], releases: list[dict]) -> tuple[list[dict], list[dict]]:
    by_tag = {release_tag(r): r for r in releases if release_tag(r)}
    channel_specs = [dict(spec) for spec in CHANNELS]
    current_stable = latest_complete_stable_release(releases)
    stable_version = ""
    if current_stable:
        stable_tag = release_tag(current_stable)
        stable_version = stable_tag[1:]
        channel_specs[0].update({
            "tag": stable_tag,
            "version": stable_version,
            "notes_file": f"release-notes-{stable_version}.md",
        })
        if stable_version == "1.0.3":
            channel_specs[0]["summary"] = "Everyday Polish — USA lineup + list guide, loading indicators, refresh stages, tips and clear result feedback."
        if stable_version == "1.0.4":
            channel_specs[0]["summary"] = ("One Last Manual Install — USA lineup + list guide, with Settings → App updates "
                                          "for every later stable release.")
        if stable_version == "1.0.5":
            channel_specs[0]["summary"] = ("Splash, search, placeholder logos, Live Events and multi-server playback — "
                                          "USA lineup + guide, with in-app updates.")
        if stable_version == "1.0.6":
            channel_specs[0]["summary"] = ("Click-to-search, Recently watched + Favorites, and manual server switching — "
                                          "USA lineup + guide, with in-app updates.")
        if stable_version == "1.0.6.1":
            channel_specs[0]["summary"] = ("Settings 2.0 — compact version card, one-tap force refresh, update check and "
                                          "a built-in bug check. USA lineup + guide, with in-app updates.")

    channels = []
    for spec in channel_specs:
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
                # GitHub's digest describes the bytes that are actually on the
                # release, so it wins over a checksum left in build-out/ by an
                # earlier local build (those can lag a re-uploaded asset).
                "sha256": asset_digest(asset) or checksums.get(asset.get("name", "")),
            })
        notes_title, notes_summary = read_release_notes(spec.get("notes_file", ""))
        mac_version = None
        if spec["id"] == "stable" and current_stable:
            required, mac_release, mac_version = mac_assets_for(stable_version, releases)
            if mac_release is not None and release_tag(mac_release) != spec["tag"]:
                for asset in mac_release.get("assets") or []:
                    kind, arch = classify_asset(asset.get("name", ""))
                    if kind not in ("macos-dmg", "macos-pkg", "checksum"):
                        continue
                    if asset.get("name") in {a["name"] for a in assets}:
                        continue
                    if asset.get("name") == "SHA256SUMS-macos.txt" or \
                            asset.get("name", "").startswith(f"PremiumTV-{mac_version}-mac-"):
                        assets.append({
                            "name": asset.get("name", ""),
                            "kind": kind,
                            "arch": arch,
                            "size": int(asset.get("size") or 0),
                            "url": asset.get("browser_download_url")
                                   or f"{RELEASES_BASE}/{release_tag(mac_release)}/{asset.get('name', '')}",
                            "sha256": asset_digest(asset) or checksums.get(asset.get("name", "")),
                        })
        channels.append({
            **spec,
            "macos_version": mac_version if mac_version and mac_version != spec["version"] else spec["version"],
            "published_at": release.get("published_at", ""),
            "html_url": release.get("html_url",
                                    f"https://github.com/{REPO_OWNER}/{REPO_NAME}"
                                    f"/releases/tag/{spec['tag']}"),
            "notes_title": notes_title,
            "notes_summary": notes_summary,
            "assets": assets,
        })
    older = []
    active_tags = {c["tag"] for c in channel_specs}
    for tag, release in sorted(by_tag.items(), reverse=True):
        if tag in active_tags or not tag or tag in RETIRED_TAGS:
            continue
        # A compatibility alias is not an "older release" while it stands for
        # the stable build the page is promoting.
        if tag in ALIAS_TAGS and COMPATIBILITY_ALIASES.get(tag[1:]) == stable_version:
            continue
        if release.get("draft") or release.get("prerelease"):
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
    # The USA row advertises the feed current builds actually refresh from, so
    # the download site keeps pointing at live channels (and counts them without
    # the sanctioned update notice) after the legacy copy is pinned.
    live_usa = legacy_sunset.live_usa_path(ROOT)
    for path in sorted((ROOT / "playlists" / "countries").glob("*.m3u")):
        stem = path.stem
        name = DISPLAY_NAME.get(stem, stem.replace("_", " "))
        source = live_usa if stem == "USA" and live_usa.is_file() else path
        if source is path and legacy_sunset.is_frozen(path):
            # A pinned legacy feed is an end-of-support artifact, not a playlist
            # to hand to somebody choosing what to watch.
            continue
        count = count_entries(source)
        if not count:
            continue
        countries.append({
            "slug": stem,
            "name": name,
            "iso2": ISO2.get(stem),
            "region": ISO2.get(stem) is None,
            "count": count,
            "playlist_url": f"{RAW_BASE}/{source.relative_to(ROOT).as_posix()}",
            "epg_url": f"{RAW_BASE}/EPG/{stem}.xml",
            "epg_present": (epg_dir / f"{stem}.xml").is_file(),
        })
    countries.sort(key=lambda c: (c["region"], -c["count"], c["name"]))
    return countries


# Channels a visitor is most likely to look for. Each one is only shown when
# that exact name is in the published lineup; the category is used to pick the
# samples for that category card too. Order is the order we want to show them.
FEATURED_BRANDS = (
    ("ESPN", "Sports"), ("NFL Network", "Sports"), ("MLB Network", "Sports"),
    ("NHL Network", "Sports"), ("WWE Network", "Sports"), ("Tennis Channel", "Sports"),
    ("CNN", "News"), ("Fox News", "Fox Channels"), ("Sky News", "News"),
    ("Al Jazeera", "News"), ("France 24", "News"), ("DW", "News"), ("CNBC", "NBC"),
    ("HBO", "Movies"), ("AMC", "Movies"),
    ("Nickelodeon", "Kids"), ("Nick Jr", "Kids"), ("Cartoon Network", "Cartoons"),
    ("Adult Swim", "Cartoons"), ("Disney Jr.", "Cartoons"),
    ("Comedy Central", "Entertainment"), ("USA Network", "NBC"), ("Syfy", "NBC"),
    ("MTV", "Music"), ("Food Network", "Lifestyle"), ("HGTV", "Lifestyle"),
    ("Travel Channel", "Lifestyle"), ("Lifetime", "Lifestyle"),
    ("Animal Planet", "Documentary"), ("National Geographic", "Documentary"),
    ("Investigation Discovery", "Documentary"),
    ("A&E", "A&E Networks"), ("PBS", "PBS"), ("CBS", "CBS"), ("NBC", "NBC"),
    ("Fox", "Fox Channels"), ("ABC", "United States"), ("Telemundo", "NBC"),
    ("Bloomberg", "Business"), ("Golf Channel", "NBC Sports Channels"),
)

BACKUP_NAME_RE = re.compile(r"^(.*?)\s*\(Backup (\d+)\)\s*$")
QUALITY_TAG_RE = re.compile(r"\((\d{3,4}p|4K|UHD|SD|HD)\)\s*$", re.IGNORECASE)
STATUS_TAG_RE = re.compile(r"\s*\[[^\]]*\]\s*$")


def read_playlist_entries(path: Path) -> list[dict]:
    """Entries of an M3U playlist: name, group, id, logo, country and URL.

    ``build_site_data.py`` deliberately stays independent of the scraper: the
    download site only needs the fields it displays, and reading them here keeps
    the site generator runnable without the network-side pipeline.
    """
    entries: list[dict] = []
    pending: tuple[str, str] | None = None
    text = path.read_text(encoding="utf-8", errors="replace")
    for raw in text.splitlines():
        line = raw.rstrip("\r")
        if line.startswith("#EXTINF"):
            # Attribute values can contain commas (an upstream user-agent does),
            # so split on the last quote-comma, not the first comma.
            split = line.rfind('\",')
            if split != -1:
                attrs, name = line[: split + 1], line[split + 2:]
            else:
                head, _, name = line.partition(",")
                attrs = head
            pending = (attrs, name.strip())
            continue
        if line.startswith("#"):
            continue
        if pending is None or not line.strip():
            continue
        attrs, name = pending
        pending = None
        if not line.strip().startswith(("http://", "https://")):
            continue

        def attr(key: str) -> str:
            match = re.search(rf'{key}="([^"]*)"', attrs)
            return match.group(1) if match else ""

        entries.append({
            "name": name,
            "group": attr("group-title"),
            "tvg_id": attr("tvg-id"),
            "logo": attr("tvg-logo"),
            "country": attr("tvg-country"),
            "url": line.strip(),
        })
    return entries


def clean_channel_name(name: str) -> str:
    """Display name without quality/status/backup decoration."""
    text = (name or "").strip()
    previous = None
    while previous != text:
        previous = text
        text = STATUS_TAG_RE.sub("", text)
        text = QUALITY_TAG_RE.sub("", text)
        text = re.sub(r"\s*\(\s*(?:Backup \d+|Alt|Alternate|Mirror|Feed \d+)\s*\)\s*$",
                      "", text, flags=re.IGNORECASE)
        text = text.strip()
    return text or (name or "").strip()


def build_lineup() -> dict:
    """A quick, readable preview of what the published playlist actually carries.

    Counts and samples come from ``playlists/PremiumTV.m3u`` itself, so the
    download page cannot advertise a category or channel the current playlist
    does not publish. Backups are counted separately: they are spare feeds of a
    channel, not additional channels.
    """
    path = ROOT / "playlists" / "PremiumTV.m3u"
    entries = read_playlist_entries(path)
    primary = [entry for entry in entries if not BACKUP_NAME_RE.match(entry["name"])]
    backups = [entry for entry in entries if BACKUP_NAME_RE.match(entry["name"])]

    groups: list[dict] = []
    by_group: dict[str, dict] = {}
    names_by_group: dict[str, list[str]] = {}
    brand_categories = {name.lower(): category for name, category in FEATURED_BRANDS}
    available: dict[str, dict] = {}

    for entry in primary:
        group = entry["group"] or "Other"
        if group not in by_group:
            row = {"name": group, "channels": 0, "backups": 0, "samples": [], "file": ""}
            groups.append(row)
            by_group[group] = row
            names_by_group[group] = []
        row = by_group[group]
        row["channels"] += 1
        clean = clean_channel_name(entry["name"])
        if clean and clean.lower() not in names_by_group[group]:
            names_by_group[group].append(clean)
        key = clean.lower()
        if key in brand_categories and key not in available:
            available[key] = {"name": clean, "category": group,
                              "logo": entry["logo"]}

    # Featured channels in the order this file lists them, not playlist order.
    featured = [available[name.lower()] for name, _ in FEATURED_BRANDS
                if name.lower() in available][:18]

    # Category samples: well-known channels first, then the next published
    # names. This is a preview card, so six readable names is enough.
    for group, row in by_group.items():
        samples: list[str] = []
        seen: set[str] = set()

        def add(name: str) -> None:
            name = (name or "").strip()
            if (not name or name.startswith("[") or len(name) > 44
                    or name.lower() in seen or len(samples) >= 6):
                return
            samples.append(name)
            seen.add(name.lower())

        for brand, category in FEATURED_BRANDS:
            if category == group and brand.lower() in {n.lower() for n in names_by_group[group]}:
                add(available.get(brand.lower(), {}).get("name", brand))
        for name in names_by_group[group]:
            add(name)
        row["samples"] = samples
        slug = re.sub(r"[^A-Za-z0-9]+", "_", group).strip("_")
        candidate = ROOT / "categories" / "All" / f"{slug}.m3u"
        if candidate.is_file():
            row["file"] = f"categories/All/{slug}.m3u"
            row["playlist_url"] = f"{RAW_BASE}/categories/All/{slug}.m3u"
        else:
            row["playlist_url"] = f"{RAW_BASE}/playlists/PremiumTV.m3u"

    for entry in backups:
        group = entry["group"] or ""
        if group.endswith(" Backups"):
            base_group = group[: -len(" Backups")]
            if base_group in by_group:
                by_group[base_group]["backups"] += 1

    qualities = {"4k": 0, "1080p": 0, "720p": 0, "576p": 0, "480p": 0,
                 "lower": 0, "generic_hd_sd": 0, "unlabelled": 0}
    for entry in primary:
        match = re.search(r"\((2160p|\d{3,4}p|4K|UHD|SD|HD)\)\s*(?:\[[^\]]*\])?\s*$",
                          entry["name"], re.IGNORECASE)
        if not match:
            qualities["unlabelled"] += 1
            continue
        tag = match.group(1).lower()
        if tag in ("4k", "uhd", "2160p"):
            qualities["4k"] += 1
        elif tag in ("hd", "sd"):
            qualities["generic_hd_sd"] += 1
        else:
            pixels = int(tag[:-1])
            if pixels >= 1080:
                qualities["1080p"] += 1
            elif pixels >= 720:
                qualities["720p"] += 1
            elif pixels >= 576:
                qualities["576p"] += 1
            elif pixels >= 480:
                qualities["480p"] += 1
            else:
                qualities["lower"] += 1

    channels_with_backups = len({
        clean_channel_name(BACKUP_NAME_RE.match(entry["name"]).group(1))
        for entry in backups
    })
    countries = sorted({entry["country"] for entry in entries if entry["country"]})

    return {
        "entries": len(entries),
        "unique_channels": len(primary),
        "backup_feeds": len(backups),
        "channels_with_backups": channels_with_backups,
        "categories": len(groups),
        "countries": len(countries),
        "qualities": qualities,
        "hd_channels": qualities["4k"] + qualities["1080p"] + qualities["720p"],
        "featured": featured,
        "groups": groups,
    }


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
        # The headline is what a player will actually receive, so count the
        # published playlist's entries; report["working"] can be one higher when
        # the rebuild folded a duplicate URL into an existing channel.
        stats["confirmed_channels"] = (count_entries(ROOT / "playlists" / "PremiumTV.m3u")
                                       or report.get("working"))
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
    # The feed's <updated> must describe its content, not the moment a build ran.
    # A wall-clock timestamp made the generated feed differ on every invocation,
    # so the documented --check command could never be reproducible.
    latest_date = max((entry["date"] for entry in entries), default="1970-01-01")
    updated = f"{latest_date}T12:00:00Z"

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


def stable_generated_time(stats: dict, changelog: list[dict]) -> str:
    """Return a deterministic timestamp for the inputs represented on the site."""
    dates: list[dt.datetime] = []
    raw_run_time = stats.get("last_run_utc")
    if raw_run_time:
        for fmt in ("%Y-%m-%d %H:%M UTC", "%Y-%m-%d %H:%M:%S UTC"):
            try:
                dates.append(dt.datetime.strptime(raw_run_time, fmt).replace(tzinfo=dt.timezone.utc))
                break
            except ValueError:
                continue
        if not dates:
            try:
                parsed = dt.datetime.fromisoformat(raw_run_time.replace("Z", "+00:00"))
                dates.append(parsed.replace(tzinfo=dt.timezone.utc) if parsed.tzinfo is None else parsed)
            except (AttributeError, TypeError, ValueError):
                pass
    if changelog:
        try:
            dates.append(dt.datetime.strptime(changelog[0]["date"], "%Y-%m-%d")
                         .replace(tzinfo=dt.timezone.utc))
        except (KeyError, TypeError, ValueError):
            pass
    if not dates:
        return "1970-01-01T00:00:00Z"
    return iso_time(max(dates))


def build_payload() -> tuple[dict, list[dict]]:
    checksums = load_checksums()
    releases = load_releases()
    channels, older = build_apps(checksums, releases)
    countries = build_countries()
    changelog = parse_changelog()
    stats = build_stats()
    payload = {
        "generated_utc": stable_generated_time(stats, changelog),
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
        "stats": stats,
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
        "lineup": build_lineup(),
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
