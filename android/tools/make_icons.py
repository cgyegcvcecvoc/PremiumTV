#!/usr/bin/env python3
"""Render the launcher icon into Android mipmap folders.

Source art lives in android/art/app-icon.png (1024x1024).  This writes the
legacy launcher icon at every density Android uses, plus an adaptive-icon
foreground/background pair for API 26+.

    python android/tools/make_icons.py

Requires Pillow (only for regenerating icons, never at app build time).
"""

from __future__ import annotations

import os
import sys

try:
    from PIL import Image
except ImportError:  # pragma: no cover - developer convenience only
    print("Pillow is required: pip install Pillow", file=sys.stderr)
    raise

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ART = os.path.join(ROOT, "art", "app-icon.png")
RES = os.path.join(ROOT, "app", "src", "main", "res")

# Density -> launcher icon size in px (48dp baseline).
LAUNCHER = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
# Adaptive icons are drawn on a 108dp canvas; Android shows the inner 72dp.
ADAPTIVE = {"mdpi": 108, "hdpi": 162, "xhdpi": 216, "xxhdpi": 324, "xxxhdpi": 432}
# Keep the artwork clear of the mask by scaling it inside the safe zone.
FOREGROUND_SCALE = 0.62


def ensure(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def main() -> int:
    if not os.path.isfile(ART):
        print("MISSING SOURCE ART: %s" % ART, file=sys.stderr)
        return 2

    source = Image.open(ART).convert("RGBA")

    for density, size in LAUNCHER.items():
        folder = os.path.join(RES, "mipmap-%s" % density)
        ensure(folder)
        source.resize((size, size), Image.LANCZOS).save(os.path.join(folder, "ic_launcher.png"))

    for density, size in ADAPTIVE.items():
        folder = os.path.join(RES, "mipmap-%s" % density)
        ensure(folder)
        inner = int(size * FOREGROUND_SCALE)
        art = source.resize((inner, inner), Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        canvas.paste(art, ((size - inner) // 2, (size - inner) // 2), art)
        canvas.save(os.path.join(folder, "ic_launcher_foreground.png"))

    anydpi = os.path.join(RES, "mipmap-anydpi-v26")
    ensure(anydpi)
    with open(os.path.join(anydpi, "ic_launcher.xml"), "w", encoding="utf-8") as handle:
        handle.write(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
            '    <background android:drawable="@color/ic_launcher_background" />\n'
            '    <foreground android:drawable="@mipmap/ic_launcher_foreground" />\n'
            "</adaptive-icon>\n"
        )

    print("icons written to %s" % os.path.relpath(RES, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
