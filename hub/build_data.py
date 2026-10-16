#!/usr/bin/env python3
"""Build hub/dist/data.json + download bundles for the PremiumTV Download Hub.

Scans the repository (playlists, EPG, build-out, categories) and produces a
single JSON the front-end renders. Also zips up handy bundles. Run from
anywhere; paths resolve relative to this file.
"""
import hashlib
import json
import os
import zipfile
from datetime import datetime, timezone

HUB = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HUB)
DIST = os.path.join(HUB, "dist")
BUNDLES = os.path.join(DIST, "bundles")

RAW = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main"
REL = "https://github.com/cgyegcvcecvoc/PremiumTV1/releases/download"


def count_channels(path):
    n = 0
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("#EXTINF"):
                    n += 1
    except OSError:
        pass
    return n


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def m3u_entry(relpath, label=None, desc=None, with_raw=True):
    path = os.path.join(ROOT, relpath)
    name = os.path.basename(relpath)
    e = {
        "name": name,
        "label": label or name.replace("_", " ").rsplit(".", 1)[0],
        "path": relpath,
        "size": os.path.getsize(path),
        "channels": count_channels(path),
        "dl": "/get/" + relpath,
    }
    if with_raw:
        e["raw"] = f"{RAW}/{relpath}"
    if desc:
        e["desc"] = desc
    return e


def listing(dirrel, suffix=".m3u"):
    d = os.path.join(ROOT, dirrel)
    out = []
    for name in sorted(os.listdir(d)):
        if name.endswith(suffix) and os.path.isfile(os.path.join(d, name)):
            out.append(m3u_entry(f"{dirrel}/{name}"))
    return out


def main():
    os.makedirs(BUNDLES, exist_ok=True)

    report = json.load(open(os.path.join(ROOT, "playlists", "report.json")))

    # ---------------- Android apps (served straight from build-out/) -------
    android_meta = {
        "1.0.2": ("Stable", "Published stable release. USA lineup with the USA guide built in."),
        "1.0.3": ("Stable (maintenance build)", "Next maintenance build of the stable channel — USA lineup + USA guide."),
        "1.1.1": ("Preview", "Global checked lineup, merged guide and the cable-style Guide grid."),
        "1.1.0": ("Preview (superseded)", "Earlier preview with the global lineup; kept for reference."),
        "1.0.1": ("Archive", "Channels Back on Air release."),
        "1.0.0": ("Archive", "The original Marquee release."),
    }
    android = []
    bo = os.path.join(ROOT, "build-out")
    for name in sorted(os.listdir(bo), reverse=True):
        if not name.endswith(".apk"):
            continue
        ver = name.replace("PremiumTV-", "").replace("-debug.apk", "")
        channel, desc = android_meta.get(ver, ("Archive", ""))
        p = os.path.join(bo, name)
        android.append({
            "version": ver,
            "channel": channel,
            "desc": desc,
            "name": name,
            "size": os.path.getsize(p),
            "sha256": sha256(p),
            "dl": f"/get/build-out/{name}",
        })

    # ---------------- macOS apps (GitHub release direct-download links) ----
    def mac_assets(tag, ver):
        base = f"{REL}/{tag}"
        return [
            {"label": "Apple Silicon (M1/M2/M3/M4) — DMG", "name": f"PremiumTV-{ver}-mac-arm64.dmg", "url": f"{base}/PremiumTV-{ver}-mac-arm64.dmg"},
            {"label": "Apple Silicon — PKG installer", "name": f"PremiumTV-{ver}-mac-arm64.pkg", "url": f"{base}/PremiumTV-{ver}-mac-arm64.pkg"},
            {"label": "Intel Macs — DMG", "name": f"PremiumTV-{ver}-mac-x64.dmg", "url": f"{base}/PremiumTV-{ver}-mac-x64.dmg"},
            {"label": "Intel Macs — PKG installer", "name": f"PremiumTV-{ver}-mac-x64.pkg", "url": f"{base}/PremiumTV-{ver}-mac-x64.pkg"},
            {"label": "SHA-256 checksums", "name": "SHA256SUMS-macos.txt", "url": f"{base}/SHA256SUMS-macos.txt"},
        ]

    macos = [
        {"version": "1.0.2", "channel": "Stable", "desc": "Published stable release — USA lineup + USA guide.", "assets": mac_assets("v1.0.2", "1.0.2")},
        {"version": "1.1.1", "channel": "Preview", "desc": "Global lineup, merged guide, cable-style Guide grid.", "assets": mac_assets("v1.1.1", "1.1.1")},
    ]

    # ---------------- Playlists --------------------------------------------
    featured = [
        m3u_entry("playlists/PremiumTV.m3u", "PremiumTV — main playlist",
                  "Every channel confirmed working in the latest checked run, grouped by category with backups."),
        m3u_entry("categories/USA.m3u", "USA — full US lineup",
                  "Every US channel, grouped by category and sorted. The playlist the stable apps ship with."),
        m3u_entry("playlists/Priority_Channels.m3u", "Priority channels",
                  "Just the verified priority channels: Nickelodeon, NickToons, MeTV, MeTV Toons, NFL Network, NFL RedZone."),
        m3u_entry("playlists/AE_Channels.m3u", "A&E networks",
                  "Confirmed working A&E / A+E Networks channels, linear and FAST."),
        m3u_entry("playlists/PremiumTV_all.m3u", "Everything (unfiltered)",
                  "All unique links ever found — including dead and unverified ones. For tinkerers."),
        m3u_entry("playlists/discovery/new-channels.m3u", "New discoveries",
                  "Working links found by the latest monthly new-channel hunt."),
    ]

    countries = listing("playlists/countries")
    epg_dir = os.path.join(ROOT, "EPG")
    epg_names = {n for n in os.listdir(epg_dir) if n.endswith(".xml")}
    for c in countries:
        xml = c["name"].replace(".m3u", ".xml")
        if xml in epg_names:
            c["epg"] = f"/get/EPG/{xml}"
            c["epg_raw"] = f"{RAW}/EPG/{xml}"
            c["epg_size"] = os.path.getsize(os.path.join(epg_dir, xml))

    cat_published = listing("playlists/categories")
    cat_all = listing("categories/All")
    cat_usa = listing("categories/USA")

    epg_main = [
        {"label": "Merged guide — every country", "name": "PremiumTV.xml",
         "path": "EPG/PremiumTV.xml", "size": os.path.getsize(os.path.join(epg_dir, "PremiumTV.xml")),
         "dl": "/get/EPG/PremiumTV.xml", "raw": f"{RAW}/EPG/PremiumTV.xml"},
        {"label": "Merged guide (gzipped)", "name": "PremiumTV.xml.gz",
         "path": "EPG/PremiumTV.xml.gz", "size": os.path.getsize(os.path.join(epg_dir, "PremiumTV.xml.gz")),
         "dl": "/get/EPG/PremiumTV.xml.gz", "raw": f"{RAW}/EPG/PremiumTV.xml.gz"},
        {"label": "USA guide", "name": "USA.xml",
         "path": "EPG/USA.xml", "size": os.path.getsize(os.path.join(epg_dir, "USA.xml")),
         "dl": "/get/EPG/USA.xml", "raw": f"{RAW}/EPG/USA.xml"},
    ]

    # ---------------- Bundles ----------------------------------------------
    def make_zip(zname, items, arc_prefix=""):
        zpath = os.path.join(BUNDLES, zname)
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
            for rel in items:
                z.write(os.path.join(ROOT, rel), arc_prefix + os.path.basename(rel))
        return {"name": zname, "size": os.path.getsize(zpath), "dl": f"/get/bundles/{zname}", "files": len(items)}

    bundles = []
    bundles.append({**make_zip("PremiumTV-country-playlists.zip",
                               [c["path"] for c in countries]),
                    "label": "Every country playlist", "desc": f"All {len(countries)} per-country M3U files in one zip."})
    bundles.append({**make_zip("PremiumTV-category-playlists.zip",
                               [c["path"] for c in cat_published]),
                    "label": "Every category playlist", "desc": "The published per-category M3Us (Sports, Cartoons, PBS, …) with their backups."})
    bundles.append({**make_zip("PremiumTV-usa-pack.zip",
                               ["categories/USA.m3u"] + [c["path"] for c in cat_usa] + ["EPG/USA.xml"]),
                    "label": "USA pack", "desc": "The full US playlist, every US category file, and the USA guide XML."})
    bundles.append({**make_zip("PremiumTV-core-playlists.zip",
                               ["playlists/PremiumTV.m3u", "playlists/PremiumTV_all.m3u",
                                "playlists/Priority_Channels.m3u", "playlists/AE_Channels.m3u",
                                "categories/USA.m3u"]),
                    "label": "Core playlists", "desc": "Main, unfiltered, priority and A&E playlists plus the USA lineup."})
    bundles.append({**make_zip("PremiumTV-epg-all-countries.zip",
                               [f"EPG/{n}" for n in sorted(epg_names)]),
                    "label": "Every EPG guide", "desc": "All per-country XMLTV guides plus the merged guide."})

    data = {
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "stats": {
            "working": report.get("working"),
            "unique": report.get("total_unique"),
            "countries": report.get("countries_count"),
            "categories": len(cat_published),
            "updated": report.get("updated_utc"),
            "updated_local": report.get("updated_local"),
            "run_label": report.get("label"),
            "status": report.get("status"),
        },
        "android": android,
        "macos": macos,
        "featured": featured,
        "countries": countries,
        "categories": {
            "published": cat_published,
            "all": cat_all,
            "usa": cat_usa,
        },
        "epg": epg_main,
        "bundles": bundles,
        "raw_base": RAW,
    }

    out = os.path.join(DIST, "data.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"wrote {out} ({os.path.getsize(out)} bytes); "
          f"{len(countries)} countries, {len(android)} APKs, {len(bundles)} bundles")


if __name__ == "__main__":
    main()
