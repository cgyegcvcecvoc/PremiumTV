#!/usr/bin/env python3
"""Export the PremiumTV Download Hub as a 100% static site — no server needed.

Produces `hub/dist/static-site/` (and a drag-and-drop zip in
`hub/dist/bundles/`) that works on any free static host: Netlify Drop,
Cloudflare Pages, Surge, Vercel, a plain nginx folder…

Strategy: small files (every .m3u, the zip bundles, the gzipped guide, any
unreleased APK) are copied into the export so the site serves them itself.
Huge files that already have a permanent free home (released APKs and the
macOS installers on GitHub release storage, the 35 MB merged EPG on raw file
storage) are linked directly — same one-click download for visitors, tiny
deploy for you.

Usage:  python3 hub/export_static.py          (requires hub/dist/data.json)
"""
import json
import os
import shutil
import zipfile

HUB = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HUB)
DIST = os.path.join(HUB, "dist")
OUT = os.path.join(DIST, "static-site")

RAW = "https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main"
REL = "https://github.com/cgyegcvcecvoc/PremiumTV1/releases/download"
RELEASED = {"1.0.0", "1.0.1", "1.0.2", "1.1.0", "1.1.1"}

# Files bigger than this stay remote links (they live on GitHub's CDN anyway).
LOCAL_MAX = 8 * 1024 * 1024


def copy_into(relpath):
    """Copy ROOT/relpath into OUT/files/relpath; return the site-relative URL."""
    src = os.path.join(ROOT, relpath)
    dst = os.path.join(OUT, "files", relpath)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not os.path.exists(dst):
        shutil.copy2(src, dst)
    return "files/" + relpath


def localize(entry):
    """Rewrite one playlist/EPG entry's dl link for the static site."""
    rel = entry.get("path")
    if not rel:
        return
    size = entry.get("size") or 0
    if size <= LOCAL_MAX:
        entry["dl"] = copy_into(rel)
    else:
        entry["dl"] = f"{RAW}/{rel}"  # permanent free CDN link
    # country guide XMLs
    if "epg" in entry:
        xml_rel = "EPG/" + entry["name"].replace(".m3u", ".xml")
        if (entry.get("epg_size") or 0) <= LOCAL_MAX:
            entry["epg"] = copy_into(xml_rel)
        else:
            entry["epg"] = entry.get("epg_raw") or f"{RAW}/{xml_rel}"


def main():
    data = json.load(open(os.path.join(DIST, "data.json"), encoding="utf-8"))
    data["server"] = False  # hides server-only extras (e.g. the self-zip card)

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)

    # 1) The page itself
    shutil.copy2(os.path.join(HUB, "static", "index.html"), os.path.join(OUT, "index.html"))
    shutil.copytree(os.path.join(HUB, "static", "assets"), os.path.join(OUT, "assets"))

    # 2) Playlists / categories / EPG
    for e in data["featured"]:
        localize(e)
    for e in data["countries"]:
        localize(e)
    for group in data["categories"].values():
        for e in group:
            localize(e)
    for e in data["epg"]:
        localize(e)

    # 3) Zip bundles — small, include them all
    os.makedirs(os.path.join(OUT, "bundles"), exist_ok=True)
    for b in data["bundles"]:
        src = os.path.join(DIST, "bundles", b["name"])
        shutil.copy2(src, os.path.join(OUT, "bundles", b["name"]))
        b["dl"] = "bundles/" + b["name"]

    # 4) Android APKs: released -> release storage; unreleased -> copy local
    for a in data["android"]:
        if a["version"] in RELEASED:
            a["dl"] = f"{REL}/v{a['version']}/{a['name']}"
        elif a["dl"].startswith("/get/build-out/"):
            src = os.path.join(ROOT, "build-out", a["name"])
            if os.path.isfile(src):
                a["dl"] = copy_into("build-out/" + a["name"])
            else:
                a["dl"] = f"{REL}/v{a['version']}/{a['name']}"

    # 5) macOS entries already point at release storage unless mirrored locally;
    #    static export always uses the release links.
    for m in data["macos"]:
        for asset in m["assets"]:
            if asset["url"].startswith("/get/mac/"):
                tag = "v" + m["version"]
                asset["url"] = f"{REL}/{tag}/{asset['name']}"

    with open(os.path.join(OUT, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    # Netlify/Cloudflare niceties: correct content type + attachment for .m3u
    with open(os.path.join(OUT, "_headers"), "w") as f:
        f.write("/files/*\n  Access-Control-Allow-Origin: *\n"
                "/files/playlists/*\n  Content-Type: audio/x-mpegurl\n"
                "/files/categories/*\n  Content-Type: audio/x-mpegurl\n")

    # 6) Size report + drag-and-drop zip
    total = 0
    nfiles = 0
    for dirpath, _dirs, files in os.walk(OUT):
        for name in files:
            total += os.path.getsize(os.path.join(dirpath, name))
            nfiles += 1
    zpath = os.path.join(DIST, "bundles", "premiumtv-hub-static-site.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for dirpath, _dirs, files in os.walk(OUT):
            for name in files:
                p = os.path.join(dirpath, name)
                z.write(p, os.path.relpath(p, OUT))
    print(f"static site: {OUT}")
    print(f"  {nfiles} files, {total/1e6:.1f} MB uncompressed")
    print(f"  drag-and-drop zip: {zpath} ({os.path.getsize(zpath)/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
