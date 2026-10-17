#!/usr/bin/env python3
"""Fetch downloadable app assets for the PremiumTV Download Hub at deploy time.

A fresh `git clone` doesn't include `build-out/` (it's git-ignored), so on a
deploy host this script downloads the released APKs from GitHub's public
release storage into `build-out/`. No auth needed — the repo is public.

Optionally (MIRROR_MAC=1) it also mirrors the macOS DMG/PKG installers into
`hub/dist/mac/` so the deployed hub self-hosts those too (~1.1 GB — only do
this on hosts with enough disk; otherwise the site links to GitHub's release
URLs, which work fine in any browser).

Failures are warnings, not errors: the hub degrades gracefully (missing APKs
fall back to release links in build_data.py).
"""
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = "https://github.com/cgyegcvcecvoc/PremiumTV1/releases/download"

APK_VERSIONS = ["1.0.0", "1.0.1", "1.0.2", "1.0.3", "1.0.4", "1.1.0", "1.1.1"]
MAC_VERSIONS = ["1.0.3", "1.0.4", "1.1.1"]
MAC_SUFFIXES = ["mac-arm64.dmg", "mac-arm64.pkg", "mac-x64.dmg", "mac-x64.pkg"]


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"  have {os.path.basename(dest)}")
        return True
    tmp = dest + ".part"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "PremiumTVHub/1.0"})
        with urllib.request.urlopen(req, timeout=120) as r, open(tmp, "wb") as f:
            while True:
                chunk = r.read(1 << 20)
                if not chunk:
                    break
                f.write(chunk)
        os.replace(tmp, dest)
        print(f"  got  {os.path.basename(dest)} ({os.path.getsize(dest)/1e6:.1f} MB)")
        return True
    except Exception as e:  # noqa: BLE001 - deploy-time best effort
        print(f"  WARN could not fetch {url}: {e}", file=sys.stderr)
        try:
            os.remove(tmp)
        except OSError:
            pass
        return False


def main():
    bo = os.path.join(ROOT, "build-out")
    os.makedirs(bo, exist_ok=True)
    print("Android APKs -> build-out/")
    for v in APK_VERSIONS:
        name = f"PremiumTV-{v}-debug.apk"
        fetch(f"{REL}/v{v}/{name}", os.path.join(bo, name))

    if os.environ.get("MIRROR_MAC") == "1":
        mac = os.path.join(ROOT, "hub", "dist", "mac")
        os.makedirs(mac, exist_ok=True)
        print("macOS installers -> hub/dist/mac/ (MIRROR_MAC=1)")
        for v in MAC_VERSIONS:
            for suf in MAC_SUFFIXES:
                name = f"PremiumTV-{v}-{suf}"
                fetch(f"{REL}/v{v}/{name}", os.path.join(mac, name))
    else:
        print("macOS installers: linking to GitHub releases (set MIRROR_MAC=1 to self-host, ~1.1 GB)")


if __name__ == "__main__":
    main()
