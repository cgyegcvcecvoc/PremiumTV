#!/usr/bin/env python3
"""Regenerate the Movies & Shows test card used to exercise the on-demand shelf.

The committed file is a short synthetic film - a moving test pattern, a
per-second timecode, the title text and a tone track - so a viewer can confirm
in one play that the side player receives video, audio and text, and that the
picture is actually advancing rather than showing a frozen first frame.

It is deliberately tiny (under a megabyte) because it is committed to the
repository and served beside the catalogue:

    playlists/vod/media/premiumtv-test-card.mp4
    playlists/vod/media/premiumtv-test-card.jpg

`scripts/vod_catalog.py` publishes it as the `vod-test-card` catalogue entry.

This is a development tool, not part of the nightly data pipeline: it needs
Pillow (drawing the frames) and an ffmpeg binary (encoding H.264/AAC), neither
of which the repository's stdlib-only scripts depend on. Point `VOD_FFMPEG` at
a specific binary, or leave it unset to use `ffmpeg` from PATH / imageio-ffmpeg.

    python3 scripts/vod_test_card.py              # rewrite both files
    python3 scripts/vod_test_card.py --check      # verify the committed file
"""

from __future__ import annotations

import argparse
import math
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = os.path.join(ROOT, "playlists", "vod", "media")
MP4_PATH = os.path.join(MEDIA_DIR, "premiumtv-test-card.mp4")
POSTER_PATH = os.path.join(MEDIA_DIR, "premiumtv-test-card.jpg")

WIDTH, HEIGHT, FPS, SECONDS = 640, 360, 24, 65
SAMPLE_RATE = 44100

INK = (7, 11, 24)
PANEL = (17, 24, 44)
GOLD = (244, 196, 96)
PAPER = (245, 247, 251)
MUTED = (154, 163, 184)
GREEN = (72, 209, 138)
RED = (224, 96, 96)


def log(message: str) -> None:
    print("[test-card] %s" % message, flush=True)


def find_ffmpeg(explicit: str | None) -> str:
    for candidate in (explicit, os.environ.get("VOD_FFMPEG"), shutil.which("ffmpeg")):
        if candidate and os.path.isfile(candidate) and os.access(candidate, os.X_OK):
            return candidate
    try:  # imageio-ffmpeg ships a static binary with its wheel
        import imageio_ffmpeg  # type: ignore

        candidate = imageio_ffmpeg.get_ffmpeg_exe()
        if candidate and os.path.isfile(candidate):
            return candidate
    except Exception:
        pass
    raise SystemExit(
        "no ffmpeg found: install it, set VOD_FFMPEG, or pip install imageio-ffmpeg"
    )


def fonts():
    from PIL import ImageFont

    return {
        "brand": ImageFont.load_default(size=30),
        "kicker": ImageFont.load_default(size=14),
        "title": ImageFont.load_default(size=44),
        "lead": ImageFont.load_default(size=20),
        "body": ImageFont.load_default(size=15),
        "mono": ImageFont.load_default(size=18),
        "small": ImageFont.load_default(size=12),
    }


def background():
    from PIL import Image

    image = Image.new("RGB", (WIDTH, HEIGHT), INK)
    pixels = image.load()
    for y in range(HEIGHT):
        t = y / (HEIGHT - 1)
        colour = tuple(round(INK[i] + (PANEL[i] - INK[i]) * t) for i in range(3))
        for x in range(WIDTH):
            pixels[x, y] = colour
    return image


def timecode(seconds: int) -> str:
    return "%02d:%02d" % (seconds // 60, seconds % 60)


def draw_chrome(image, f, seconds: float, frame_index: int) -> None:
    """Everything that changes with time. `seconds` is the playback clock."""
    from PIL import ImageDraw

    draw = ImageDraw.Draw(image)
    draw.text((36, 24), "PremiumTV", font=f["brand"], fill=GOLD)
    draw.text((36, 60), "MOVIES & SHOWS  /  ON DEMAND", font=f["kicker"], fill=MUTED)
    draw.line((36, 84, WIDTH - 36, 84), fill=(52, 63, 92), width=1)

    draw.text((36, 104), "ON-DEMAND TEST CARD", font=f["title"], fill=PAPER)
    draw.text(
        (38, 158),
        "One short clip that proves video, audio and text reach the side player.",
        font=f["body"],
        fill=MUTED,
    )

    rows = (
        ("VIDEO", "640 x 360  /  24 fps  /  H.264", GREEN),
        ("AUDIO", "440 Hz bed + a beep on every whole second  /  AAC", GREEN),
        ("TEXT", "this caption is the text check  /  rendered, not overlaid by the app", GREEN),
    )
    for index, (label, detail, colour) in enumerate(rows):
        y = 200 + index * 26
        draw.ellipse((38, y + 5, 48, y + 15), fill=colour)
        draw.text((58, y), label, font=f["body"], fill=PAPER)
        draw.text((118, y), detail, font=f["body"], fill=MUTED)

    # The travelling marker is the motion check: if this dot is not moving, the
    # player is showing a still frame even when the clock below is correct.
    travel = 36 + (WIDTH - 72 - 12) * (seconds % 8) / 8.0
    draw.rounded_rectangle((36, 286, WIDTH - 36, 300), radius=7, fill=(31, 40, 66))
    draw.rounded_rectangle((36, 286, travel, 300), radius=7, fill=GOLD)

    elapsed = int(seconds)
    draw.text(
        (36, 312),
        "%s / %s" % (timecode(elapsed), timecode(SECONDS)),
        font=f["mono"],
        fill=PAPER,
    )
    draw.text(
        (WIDTH - 36 - 176, 314),
        "frame %04d / %04d" % (frame_index + 1, SECONDS * FPS),
        font=f["small"],
        fill=MUTED,
    )
    # A red flash on every whole second lands in step with the audio beep, so a
    # muted player is obvious at a glance.
    if seconds % 1.0 < FPS_INVERSE * 2:
        draw.ellipse((WIDTH - 64, 312, WIDTH - 50, 326), fill=RED)


FPS_INVERSE = 1.0 / FPS


def poster(f) -> None:
    from PIL import Image, ImageDraw

    image = background()
    draw = ImageDraw.Draw(image)
    draw.text((36, 24), "PremiumTV", font=f["brand"], fill=GOLD)
    draw.text((36, 60), "MOVIES & SHOWS  /  ON DEMAND", font=f["kicker"], fill=MUTED)
    draw.line((36, 84, WIDTH - 36, 84), fill=(52, 63, 92), width=1)
    draw.text((36, 104), "PremiumTV Test Card", font=f["title"], fill=PAPER)
    draw.text((38, 158), "65 seconds  /  2026  /  Test", font=f["lead"], fill=GOLD)
    for index, line in enumerate((
        "Generated for the Movies and Shows shelf.",
        "Watch for the moving gold bar, the running",
        "timecode and the beep on every second.",
    )):
        draw.text((38, 202 + index * 22), line, font=f["body"], fill=MUTED)
    draw.text((38, 292), "Tap to play", font=f["lead"], fill=GREEN)
    image.save(POSTER_PATH, "JPEG", quality=88, optimize=True)


def write_tone(path: str) -> None:
    """A deterministic tone track: bed + one beep per second + a chime every 10s."""
    frames = bytearray()
    total = SECONDS * SAMPLE_RATE
    for n in range(total):
        t = n / SAMPLE_RATE
        envelope = min(1.0, t / 0.4, (SECONDS - t) / 1.2)
        # Soft low bed so the file is never digitally silent.
        sample = 0.10 * math.sin(2 * math.pi * 220 * t)
        sample += 0.04 * math.sin(2 * math.pi * 330 * t)
        # Beep on each whole second, its rising edge aligned with the red flash.
        since = t % 1.0
        if since < 0.06:
            sample += 0.34 * math.sin(2 * math.pi * 1000 * t) * (1 - since / 0.06)
        # A three-note chime at every ten-second mark.
        phase = t % 10.0
        for note_index, frequency in enumerate((523.25, 659.25, 783.99)):
            start = note_index * 0.14
            if start <= phase < start + 0.14:
                local = (phase - start) / 0.14
                sample += 0.28 * math.sin(2 * math.pi * frequency * t) * (1 - local)
        value = max(-1.0, min(1.0, sample * envelope))
        frames += struct.pack("<h", int(value * 32767))
    with wave.open(path, "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SAMPLE_RATE)
        handle.writeframes(bytes(frames))


def encode(ffmpeg: str, frames_dir: str, tone_path: str, out_path: str) -> None:
    command = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-framerate", str(FPS), "-i", os.path.join(frames_dir, "frame_%05d.png"),
        "-i", tone_path,
        "-c:v", "libx264", "-preset", "medium", "-crf", "30",
        "-profile:v", "main", "-level", "3.1", "-pix_fmt", "yuv420p",
        "-g", str(FPS * 2),
        "-c:a", "aac", "-b:a", "48k", "-ac", "1", "-ar", str(SAMPLE_RATE),
        "-shortest", "-movflags", "+faststart",
        "-metadata", "title=PremiumTV Movies & Shows Test Card",
        "-metadata", "comment=Generated by scripts/vod_test_card.py",
        out_path,
    ]
    subprocess.run(command, check=True)


def build(ffmpeg: str) -> dict[str, int]:
    os.makedirs(MEDIA_DIR, exist_ok=True)
    f = fonts()
    frame_count = SECONDS * FPS
    with tempfile.TemporaryDirectory(prefix="premiumtv-test-card-") as work:
        frames_dir = os.path.join(work, "frames")
        os.makedirs(frames_dir)
        base = background()
        for index in range(frame_count):
            image = base.copy()
            draw_chrome(image, f, index / FPS, index)
            image.save(os.path.join(frames_dir, "frame_%05d.png" % index), "PNG")
        log("drew %d frames" % frame_count)
        tone_path = os.path.join(work, "tone.wav")
        write_tone(tone_path)
        log("wrote %.1f MB of tone" % (os.path.getsize(tone_path) / 1e6))
        encode(ffmpeg, frames_dir, tone_path, MP4_PATH)
    poster(f)
    return {
        "mp4_bytes": os.path.getsize(MP4_PATH),
        "poster_bytes": os.path.getsize(POSTER_PATH),
        "seconds": SECONDS,
    }


def check() -> int:
    """Offline sanity check of the committed clip, without ffmpeg."""
    if not os.path.isfile(MP4_PATH) or os.path.getsize(MP4_PATH) < 10_000:
        log("missing or tiny %s" % os.path.relpath(MP4_PATH, ROOT))
        return 1
    with open(MP4_PATH, "rb") as handle:
        head = handle.read(4096)
    if b"ftyp" not in head:
        log("the committed file is not an MP4 (no ftyp box)")
        return 1
    atoms = mp4_sample_descriptions(MP4_PATH)
    if "video" not in atoms or "audio" not in atoms:
        log("the committed file has no video+audio track pair: %s" % atoms)
        return 1
    if os.path.getsize(MP4_PATH) > 4_000_000:
        log("the test card grew past 4 MB; it is committed to Git")
        return 1
    log(
        "OK %s (%.2f MB, video+audio)"
        % (os.path.relpath(MP4_PATH, ROOT), os.path.getsize(MP4_PATH) / 1e6)
    )
    return 0


def mp4_sample_descriptions(path: str) -> set[str]:
    """Find the H.264/AAC sample entries so `--check` needs no ffprobe."""
    with open(path, "rb") as handle:
        data = handle.read()
    found: set[str] = set()
    if b"avc1" in data or b"avc3" in data:
        found.add("video")
    if b"mp4a" in data:
        found.add("audio")
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true", help="verify the committed clip and exit")
    parser.add_argument("--ffmpeg", help="path to the ffmpeg binary (or set VOD_FFMPEG)")
    args = parser.parse_args()
    if args.check:
        return check()
    ffmpeg = find_ffmpeg(args.ffmpeg)
    result = build(ffmpeg)
    log("wrote %s (%.2f MB)" % (os.path.relpath(MP4_PATH, ROOT), result["mp4_bytes"] / 1e6))
    log("wrote %s (%.0f KB)" % (os.path.relpath(POSTER_PATH, ROOT), result["poster_bytes"] / 1e3))
    return check()


if __name__ == "__main__":
    sys.exit(main())
