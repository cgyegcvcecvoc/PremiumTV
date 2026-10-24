#!/usr/bin/env python3
"""Cold-launch the built APK and verify its channel UI on an Android emulator.

Every adb call gets an explicit timeout. The stable USA bundle is ~6 MB
(2,133 channels, 24k programmes) while the global bundle carries the
library at ~21 MB (9,788 channels, 105k programmes): the APK install, the cold
start and especially `uiautomator dump` all take much longer there, so the gate
sizes its waits for the larger library instead of assuming the stable one.
A dump that times out is retried rather than counted as a failed check.

A build inside the range published in `app-update-notice.json` (1.0.0-1.0.4
today) opens the update popup over the channel list on first launch. That is the
behaviour the notice exists for, so the gate records it, screenshots it once and
presses Back - the remote's own dismissal - instead of failing as though the
channel list never drew.

After the channel check, the Guide tab is opened. A cable-guide build (bundle
preview_features: cable-guide) must show the cable-style grid - channels down
the left, half-hour times across the top, shows to the right - and answer the
remote: the highlight moves with the D-pad, OK opens the channel in the docked
side player beside the still-visible guide, and Back closes it on the same
guide. A stable build must show the "what's on now" list.
Cable-guide runs save screenshots of the guide to build-out/ so the grid can be
checked by eye.

Every build - stable included - then opens a channel end to end: Channels tab,
first category, first card, and the player must stay alive through the
buffering/error machinery, grow from the side player to the big screen, tuck
back into the dock, and close to the browser again. The stable gate never
played a channel before 1.0.9, which is
how the 1.0.8/1.0.8.1 crash-on-watch shipped with every check green; if the
process dies anywhere in this stretch, the crash buffer lands in
build-out/smoke-log.txt with the stack trace.

On failure the logcat tail and the last UI dump are written to
build-out/smoke-log.txt. Actions logs live behind a host some sandboxes cannot
reach, and for branch builds build-out/ is committed back to the branch, which
is what makes a failed emulator run diagnosable.
"""
import json
from pathlib import Path
import re
import subprocess
import time
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "com.premiumtv.app.debug"

# The preview APK is roughly twice the stable one and its channel list is ~4.6x
# larger, so adb needs far more room than the default 30s everywhere.
ADB_TIMEOUT_SECONDS = 60
INSTALL_TIMEOUT_SECONDS = 600
LAUNCH_TIMEOUT_SECONDS = 180
DUMP_TIMEOUT_SECONDS = 120
# How long the UI may take to publish the channel count and a channel card.
# The stable bundle settles well inside a minute; the global one needs longer
# because the guide it parses on start is ~3.4x bigger.
UI_DEADLINE_SECONDS = 240


def adb(*args, timeout=ADB_TIMEOUT_SECONDS):
    return subprocess.check_output(["adb", *args], text=True, timeout=timeout)


def diagnose(reason, last_dump=""):
    """Save what the emulator saw, because the Actions log may not travel."""
    print(reason)
    sections = {"reason": reason}
    probes = {
        "pidof": ("shell", "pidof", PACKAGE),
        "current focus": ("shell", "dumpsys", "window"),
        "top activity": ("shell", "dumpsys", "activity", "activities"),
        "meminfo": ("shell", "dumpsys", "meminfo", PACKAGE),
        "logcat": ("logcat", "-d", "-t", "600"),
        "crash log": ("logcat", "-b", "crash", "-d", "-t", "200"),
    }
    for label, args in probes.items():
        try:
            sections[label] = adb(*args, timeout=150)
        except subprocess.SubprocessError as error:
            sections[label] = f"{label} unavailable: {error}"
    # Keep the parts that answer "did the app start, did it die, did the system
    # hand it to the launcher": the full dumpsys output is far too big to save.
    focus = [line for line in sections["current focus"].splitlines() if "mCurrentFocus" in line or "mFocusedApp" in line]
    top = [line for line in sections["top activity"].splitlines() if PACKAGE in line][:12]
    mem = sections["meminfo"].splitlines()[:24]
    body = "\n\n".join([
        reason,
        "=== process ===\n" + sections["pidof"].strip(),
        "=== focus ===\n" + "\n".join(focus),
        "=== premiumtv activity lines ===\n" + "\n".join(top),
        "=== meminfo ===\n" + "\n".join(mem),
        "=== crash log ===\n" + sections["crash log"],
        "=== logcat ===\n" + sections["logcat"],
        "=== last UI dump ===\n" + last_dump,
    ])
    print(body[:20000])
    try:
        out = ROOT / "build-out"
        out.mkdir(parents=True, exist_ok=True)
        (out / "smoke-log.txt").write_text(body)
    except OSError as error:
        print(f"could not write build-out/smoke-log.txt: {error}")


# Newer ICU puts a narrow no-break space before AM/PM; \s matches either.
TIME_TICK = re.compile(r"^\d{1,2}:\d{2}\s(AM|PM)$")
GUIDE_DATE = re.compile(r"^[A-Z][a-z]{2}, [A-Z][a-z]{2}\s\d{1,2}$")
# The global guide (~105k listings) can still be parsing when the channel cards
# are already up, so the first guide check gets the same room as the UI check.
GUIDE_DEADLINE_SECONDS = 240


def dump_ui():
    """One uiautomator dump: (xml text, parsed nodes)."""
    adb("shell", "uiautomator", "dump", "/sdcard/premiumtv-ui.xml", timeout=DUMP_TIMEOUT_SECONDS)
    xml = adb("shell", "cat", "/sdcard/premiumtv-ui.xml", timeout=DUMP_TIMEOUT_SECONDS)
    return xml, list(ET.fromstring(xml).iter("node"))


def texts_of(nodes):
    return [node.get("text", "") for node in nodes if node.get("text", "")]


def centre_of(node):
    left, top, right, bottom = map(int, re.findall(r"\d+", node.get("bounds", "")))
    return (left + right) // 2, (top + bottom) // 2


def progress(line):
    """Appends a milestone to build-out/smoke-progress.txt as the run goes."""
    print(line)
    try:
        out = ROOT / "build-out"
        out.mkdir(parents=True, exist_ok=True)
        with (out / "smoke-progress.txt").open("a", encoding="utf-8") as handle:
            handle.write(f"{time.strftime('%H:%M:%S')} {line}\n")
    except OSError:
        pass


def screenshot(name):
    """Saves the emulator screen to build-out/<name> (PNG)."""
    out = ROOT / "build-out"
    out.mkdir(parents=True, exist_ok=True)
    try:
        data = subprocess.check_output(["adb", "exec-out", "screencap", "-p"], timeout=ADB_TIMEOUT_SECONDS)
        if data.startswith(b"\x89PNG"):
            (out / name).write_bytes(data)
            print(f"saved build-out/{name} ({len(data) // 1024} KB)")
    except subprocess.SubprocessError as error:
        print(f"screenshot {name} skipped: {error}")


def wait_for(check, label):
    """Polls the UI until check(texts) is truthy; returns (value, texts, xml)."""
    deadline = time.monotonic() + GUIDE_DEADLINE_SECONDS
    last_xml, last_texts, last_error = "", [], ""
    while time.monotonic() < deadline:
        try:
            last_xml, nodes = dump_ui()
            last_texts = texts_of(nodes)
            # The update check is asynchronous: the popup can arrive after the
            # channel list has already drawn and land on top of the Guide tab.
            if dismiss_update_notice(last_texts, nodes):
                continue
            value = check(last_texts, nodes)
            if value:
                return value, last_texts, last_xml
        except (subprocess.SubprocessError, ET.ParseError) as error:
            last_error = f"{type(error).__name__}: {error}"
        time.sleep(2)
    diagnose(f"{label} not seen within {GUIDE_DEADLINE_SECONDS} seconds. "
             f"Texts: {sorted(set(last_texts))[:40]} {last_error}", last_xml)
    raise RuntimeError(f"{label} not seen in time")


def key(code, times=1):
    for _ in range(times):
        adb("shell", "input", "keyevent", str(code))
        time.sleep(0.6)


# The popup's own headline, not the published copy: the wording in
# app-update-notice.json can change without breaking this gate.
# Every popup the notice document can raise. "BUILD RETIRED" matters most: a
# stale copy of app-update-notice.json in the repository can still call the
# build under test a retired preview, and the gate must dismiss that dialog and
# go on testing the app rather than sit on it until the 240 s deadline.
NOTICE_EYEBROWS = {"PREMIUMTV UPDATE", "SUPPORT HAS ENDED", "BUILD RETIRED", "UPDATE REQUIRED"}
# Used when the document cannot be read, or names a label this list forgot: the
# dismissal button is always the safe press, so a missing entry must not wedge
# the gate.
DEFAULT_DISMISS_LABELS = {"Not now", "Later", "Remind me next time", "Dismiss"}
_notice_seen = False
# Counted so the player walk can tell a Back press the popup stole (the dialog
# window takes the key before the dock's handler sees it) from a dock that
# genuinely ignores Back.
_notice_dismissals = 0


def notice_dismiss_labels():
    """The dialog's dismissal button text, as published in the notice.

    Both the warning rule and its end-of-support escalation are read, so the
    gate keeps working on either side of the sunset date.
    """
    labels = set(DEFAULT_DISMISS_LABELS)
    try:
        document = json.loads((ROOT / "app-update-notice.json").read_text(encoding="utf-8"))
        for rule in document.get("rules") or []:
            for source in (rule, rule.get("after_support_ends") or {}):
                label = str(source.get("dismiss_label") or "").strip()
                if label:
                    labels.add(label)
    except (OSError, ValueError):
        pass
    return labels


def dismiss_update_notice(texts, nodes):
    """Dismisses the startup update popup if this build is showing one.

    A targeted build is *supposed* to be told to update, so the gate treats the
    dialog as expected rather than as a missing channel list. It records the
    milestone, keeps one screenshot as evidence, and presses the dialog's own
    dismissal button - the same press a remote makes. Back alone is not enough:
    the emulator's key event can land before the dialog window takes focus, and
    the dialog then simply stays up.
    """
    global _notice_seen, _notice_dismissals
    if not any(text.strip().upper() in NOTICE_EYEBROWS for text in texts):
        return False
    if not _notice_seen:
        _notice_seen = True
        progress("update popup shown: this build is inside the published notice range")
        screenshot("smoke-update-notice.png")
    labels = notice_dismiss_labels()
    target = next((node for node in nodes
                   if node.get("text", "").strip() in labels), None)
    if target is None:
        # Fall back to the last clickable node: the two buttons sit in a row,
        # dismissal second, so this still presses the safe choice.
        clickable = [node for node in nodes if node.get("clickable") == "true"
                     and node.get("text", "").strip()]
        target = clickable[-1] if clickable else None
    if target is not None:
        x, y = centre_of(target)
        progress(f"tapping '{target.get('text', '').strip()}' to dismiss the popup")
        adb("shell", "input", "tap", str(x), str(y))
    else:
        key("KEYCODE_BACK")  # the remote's own dismissal
    time.sleep(1.5)
    _notice_dismissals += 1
    return True


def check_guide(meta, names):
    """Opens the Guide tab and checks the grid (preview) or the list (stable)."""
    cable = "cable-guide" in (meta.get("preview_features") or [])

    def guide_tab(texts, nodes):
        # Return coordinates, not the element: an ElementTree element with no
        # children is falsy, which made the first version of this wait loop
        # until its deadline with the tab plainly on screen.
        node = next((node for node in nodes if node.get("text") == "Guide"), None)
        return centre_of(node) if node is not None else None

    (x, y), _, _ = wait_for(guide_tab, "the Guide tab")
    progress(f"tapping the Guide tab at {x},{y} (cable grid expected: {cable})")
    adb("shell", "input", "tap", str(x), str(y))

    if not cable:
        wait_for(lambda texts, nodes: any("channels with listings" in t for t in texts),
                 "the stable guide list")
        progress("GUIDE PASS (stable): the Guide tab shows the what's-on-now list")
        return

    def grid(texts, nodes):
        ticks = [t for t in texts if TIME_TICK.match(t)]
        dated = any(GUIDE_DATE.match(t) for t in texts)
        listed = any(t.endswith("channels listed") for t in texts)
        rows = [t for t in texts if t in names]
        return (ticks, rows) if len(ticks) >= 3 and dated and listed and rows else None

    (ticks, rows), texts, _ = wait_for(grid, "the cable-style guide grid")
    progress(f"GUIDE PASS (cable grid): times across the top {ticks[:6]}, "
             f"channels down the left {rows[:4]}")
    screenshot("android-guide.png")

    # The remote: the grid takes focus when it opens; move right and down.
    before = set(texts)
    key("KEYCODE_DPAD_RIGHT", 2)
    key("KEYCODE_DPAD_DOWN", 2)
    moved, texts, _ = wait_for(lambda t, n: set(t) != before and grid(t, n), "the guide after D-pad moves")
    progress("GUIDE PASS (remote): the highlight and the detail strip follow the D-pad")
    screenshot("android-guide-remote.png")

    # OK plays the highlighted channel in the docked side player (1.1.2), so the
    # guide stays on screen beside it; Back in the dock closes the player and
    # hands the same guide back. The player check below then starts from a
    # clean browser.
    key("KEYCODE_DPAD_CENTER")
    wait_alive(side_card_marker, "the side player after OK in the guide")
    wait_for(grid, "the guide still on screen beside the side player")
    key("KEYCODE_BACK")
    wait_for(dock_closed, "the side player to close on Back")
    wait_for(grid, "the guide again after Back from the side player")
    close_side_player()
    progress("GUIDE PASS (player): OK opened the docked channel and Back closed it")


# How long the player may take to appear (or to confess via the error card)
# after a channel is tapped. Far shorter than the guide deadline: the player
# screen composes immediately, and on a crash the dead process is the answer.
PLAYER_DEADLINE_SECONDS = 90


def process_alive():
    try:
        return bool(adb("shell", "pidof", PACKAGE, timeout=30).strip())
    except subprocess.SubprocessError:
        return False


def wait_alive(check, label, deadline_seconds=PLAYER_DEADLINE_SECONDS):
    """wait_for with a shorter fuse and a dead-process short-circuit.

    A crash leaves the UI empty rather than merely wrong, so the missing
    process ends the wait at once and diagnose() captures the crash buffer
    (with the stack trace) instead of polling a launcher desktop for minutes.
    """
    deadline = time.monotonic() + deadline_seconds
    last_xml, last_texts, last_error = "", [], ""
    while time.monotonic() < deadline:
        if not process_alive():
            diagnose(f"{label}: the app process is gone (crash while opening/using the player). "
                     f"Last texts: {sorted(set(last_texts))[:40]}", last_xml)
            raise RuntimeError(f"{label}: app process died")
        try:
            last_xml, nodes = dump_ui()
            last_texts = texts_of(nodes)
            if dismiss_update_notice(last_texts, nodes):
                continue
            value = check(last_texts, nodes)
            if value:
                return value, last_texts, last_xml
        except (subprocess.SubprocessError, ET.ParseError) as error:
            last_error = f"{type(error).__name__}: {error}"
        time.sleep(2)
    diagnose(f"{label} not seen within {deadline_seconds} seconds. "
             f"Process alive: {process_alive()}. Texts: {sorted(set(last_texts))[:40]} {last_error}",
             last_xml)
    raise RuntimeError(f"{label} not seen in time")


def tap_text(nodes, predicate, label):
    """Taps the centre of the first node whose text satisfies predicate."""
    node = next((node for node in nodes if predicate(node.get("text", ""))), None)
    if node is None:
        return False
    x, y = centre_of(node)
    progress(f"tapping '{node.get('text', '').strip()}' ({label}) at {x},{y}")
    adb("shell", "input", "tap", str(x), str(y))
    time.sleep(1.5)
    return True


def close_side_player():
    """If the side player card is up, close it so playback actually stops."""
    try:
        _, nodes = dump_ui()
    except (subprocess.SubprocessError, ET.ParseError):
        return
    texts = texts_of(nodes)
    if any(text == "⤢ Big screen" for text in texts):
        tap_text(nodes, lambda text: text == "✕ Close", "side player close")
        time.sleep(1.5)


def poll_ui(check, seconds):
    """Quietly polls the UI for check(texts, nodes); None when time runs out.

    For outcomes that are allowed not to happen (a feed that simply plays, a
    bundle with no live games): wait_alive's diagnose-on-timeout would bury
    the real evidence under a non-failure.
    """
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if not process_alive():
            return None
        try:
            _, nodes = dump_ui()
            value = check(texts_of(nodes), nodes)
            if value:
                return value
        except (subprocess.SubprocessError, ET.ParseError):
            pass
        time.sleep(3)
    return None


def side_card_marker(texts, nodes):
    """The docked side player: only its layout carries "⤢ Big screen"."""
    return next((text for text in texts if text == "⤢ Big screen"), None)


def big_screen_marker(texts, nodes):
    """The full-screen player: its chrome carries "⤢ Side player" instead."""
    return next((text for text in texts if text == "⤢ Side player"), None)


def dock_closed(texts, nodes):
    """No docked panel on screen any more."""
    return None if any(text == "⤢ Big screen" for text in texts) else texts


def tap_tab(label):
    def find(texts, nodes):
        node = next((node for node in nodes if node.get("text") == label), None)
        return centre_of(node) if node is not None else None

    (x, y), _, _ = wait_for(find, f"the {label} tab")
    adb("shell", "input", "tap", str(x), str(y))
    time.sleep(1.5)


def press_back_until_dock_closed(context):
    """Close the docked panel with Back, allowing for one stolen press.

    The dock's own hint promises that Back closes it. The only thing that may
    legitimately take that press first is the update popup: it is a dialog
    window, so it consumes the key before the panel's handler sees it. 1.1.2 no
    longer shows one over a playing channel (AppRoot), but a popup that was
    already up - or a build that predates the fix - would otherwise look like a
    dock that ignores Back, which is exactly the failure this gate has to
    report honestly. So: one press, a short quiet wait, and a second press only
    when the popup was seen taking the key in between.
    """
    key("KEYCODE_BACK")
    stolen_at = _notice_dismissals
    if poll_ui(dock_closed, 15):
        return
    if _notice_dismissals > stolen_at:
        progress(f"the update popup took the Back press ({context}); pressing again")
        key("KEYCODE_BACK")
    wait_alive(dock_closed, f"the closed side player ({context})")


def exercise_player_transitions(meta, context):
    """Once the player is up: fallback walk, manual server hop, side player.

    The 1.0.8 player rebuilds its ExoPlayer on every server switch and keeps
    the same PlayerScreen alive across the big-screen/side-player flip, so
    this walks the whole chain and demands a living process after each hop.
    """
    # 1.1.2 opens a channel in the docked side player, so the walk starts there
    # and climbs to the big screen before coming back down.
    wait_alive(side_card_marker, f"the side player ({context})")
    progress(f"channel opened docked in the side player ({context})")

    # Let the stream machinery run: buffering, a dead feed walking the server
    # list (each hop rebuilds the player under the same view), the error
    # card. Whatever it does, the process must still be there at the end.
    def settled(texts, nodes):
        return next((text for text in texts
                     if "This stream is not playing" in text
                     or "servers for this channel were tried" in text
                     or "switching to server" in text
                     or re.search(r"Server [2-9] of \d+", text)), None)

    outcome = poll_ui(settled, 90)
    if outcome:
        progress(f"player settled ({context}): '{outcome.strip()}'")
    else:
        # A feed that quietly plays (or buffers forever) never shows those
        # texts; that is fine as long as the app is alive.
        progress(f"player still working after the settle window ({context})")
    if not process_alive():
        diagnose(f"the app died while the player was up ({context})")
        raise RuntimeError("app process died with the player up")
    screenshot("android-side-player.png")

    # Manual server hop, when this channel has more than one server: the same
    # player-rebuild path the automatic fallback takes, on demand.
    try:
        _, nodes = dump_ui()
        if tap_text(nodes, lambda text: text == "Server ▶", "manual server hop"):
            time.sleep(6)
            if not process_alive():
                diagnose(f"the app died on a manual server hop ({context})")
                raise RuntimeError("app process died on a manual server hop")
            progress(f"manual server hop survived ({context})")
    except (subprocess.SubprocessError, ET.ParseError):
        pass

    # Grow the docked picture to the big screen: the same PlayerScreen and the
    # same ExoPlayer, so the stream must not restart.
    _, nodes = dump_ui()
    tap_text(nodes, lambda text: text == "⤢ Big screen", "side player grow")
    wait_alive(big_screen_marker, f"the big screen ({context})")
    time.sleep(3)
    if not process_alive():
        diagnose(f"the app died growing the side player ({context})")
        raise RuntimeError("app process died growing the side player")
    screenshot("android-player.png")
    progress(f"big screen composed ({context}); tucking it back")

    # Back tucks the big screen into the dock again, and Back in the dock closes
    # the panel and hands the browser back. The dock's own hint promises that;
    # with nothing listening for the key it used to leave the app instead.
    key("KEYCODE_BACK")
    wait_alive(side_card_marker, f"the side player again ({context})")
    press_back_until_dock_closed(context)
    close_side_player()
    progress(f"side player closed on Back ({context})")

    def browser_back(texts, nodes):
        # Any "<n> channels" header, not the bundled count: the app may have
        # refreshed its library from the live feed while the player was up
        # (the emulator has internet), and the newer count is just as much
        # "the browser is back" as the baked one.
        return any(re.search(r"\b\d+ channels\b", text) for text in texts) \
            and not any(text == "⤢ Big screen" for text in texts)

    wait_alive(browser_back, f"the browser after closing the player ({context})")
    if not process_alive():
        diagnose(f"the app died on the way back from the player ({context})")
        raise RuntimeError("app process died leaving the player")


def check_player(meta, channels):
    """Opens a channel from the Channels tab and proves the player survives.

    This is the tap a viewer makes first and the one 1.0.8/1.0.8.1 crashed on
    while the stable gate only ever looked at the guide. Screenshots of the
    full player and the side player land in build-out/ for an eyeball check.
    The target channel carries backup feeds (same EPG id, several URLs) when
    the bundle has one, so the player's automatic server fallback - the path
    that rebuilds the player mid-screen - is exercised, not just first paint.
    """
    urls_by_id = {}
    for channel in channels:
        if channel.get("id") and channel.get("url"):
            urls_by_id.setdefault(channel["id"], set()).add(channel["url"])
    multi = [channel for channel in channels
             if len(urls_by_id.get(channel.get("id", ""), ())) > 1
             and 0 < len(channel.get("name", "")) <= 28]
    pool = multi or channels
    target_channel = pool[0]
    group = target_channel.get("group") or ""
    target = (target_channel.get("name") or "").strip()
    servers = len(urls_by_id.get(target_channel.get("id", ""), ()))
    progress(f"player check: category '{group}', channel '{target}' "
             f"({servers} feed(s) under its EPG id)")

    tap_tab("Channels")

    def category_row(texts, nodes):
        node = next((node for node in nodes if node.get("text", "") == group), None)
        return centre_of(node) if node is not None else None

    (x, y), _, _ = wait_alive(category_row, f"the '{group}' category row")
    adb("shell", "input", "tap", str(x), str(y))
    time.sleep(1.5)

    def card(texts, nodes):
        node = next((node for node in nodes
                     if node.get("text", "") == target
                     or (node.get("text", "") and target.startswith(node.get("text", "").rstrip("…")))),
                    None)
        return centre_of(node) if node is not None else None

    (x, y), _, _ = wait_alive(card, f"the '{target}' channel card")
    adb("shell", "input", "tap", str(x), str(y))

    exercise_player_transitions(meta, f"channel '{target}'")
    progress(f"PLAYER PASS: '{target}' opened, survived the stream machinery, "
             "the server hops and both side-player flips")


def check_live_event(meta, channels):
    """Opens a game from the Live Events tab - the other tap-to-watch path.

    A game's card hands the player its whole server list, so this is the
    multi-server path with the largest lists in the app. Bundles with no
    games in them skip quietly.
    """
    tap_tab("Live Events")

    def pill(texts, nodes):
        node = next((node for node in nodes
                     if node.get("text", "") in ("LIVE", "CHECKING", "NO SIGNAL")), None)
        return centre_of(node) if node is not None else None

    centre = poll_ui(pill, 45)
    if not centre:
        progress("no live games in this bundle; skipping the Live Events player check")
        return
    x, y = centre
    progress("tapping the first live event card")
    adb("shell", "input", "tap", str(x), str(y))

    exercise_player_transitions(meta, "live event")
    progress("LIVE EVENT PASS: a game opened and survived the same chain")


def main():
    bundle = ROOT / "android/app/src/main/assets/bundle"
    meta = json.loads((bundle / "meta.json").read_text())
    channels = [json.loads(row) for row in (bundle / "channels.jsonl").read_text().splitlines() if row]
    names = {channel["name"] for channel in channels}
    progress(f"bundled library: {meta['channel_count']} channels, {len(names)} names, version {meta['version']}, "
             f"preview features {meta.get('preview_features') or []}")
    adb("install", "-r", str(ROOT / "android/app/build/outputs/apk/debug/app-debug.apk"),
        timeout=INSTALL_TIMEOUT_SECONDS)
    for attempt in range(2):
        adb("shell", "am", "force-stop", PACKAGE)
        if attempt == 0:
            adb("shell", "pm", "clear", PACKAGE)
        adb("shell", "am", "start", "-W", "-n", f"{PACKAGE}/com.premiumtv.app.MainActivity",
            timeout=LAUNCH_TIMEOUT_SECONDS)
        deadline = time.monotonic() + UI_DEADLINE_SECONDS
        last_dump = ""
        last_error = ""
        while time.monotonic() < deadline:
            try:
                adb("shell", "uiautomator", "dump", "/sdcard/premiumtv-ui.xml", timeout=DUMP_TIMEOUT_SECONDS)
                xml = adb("shell", "cat", "/sdcard/premiumtv-ui.xml", timeout=DUMP_TIMEOUT_SECONDS)
                last_dump = xml
                nodes = ET.fromstring(xml)
                texts = {node.get("text", "") for node in nodes.iter("node")}
                if dismiss_update_notice(texts, list(nodes.iter("node"))):
                    continue
                count = any(re.search(rf"\b{meta['channel_count']} channels\b", value) for value in texts)
                named = [value for value in texts for name in names if name and name in value]
                if count and named:
                    progress(f"APK SMOKE PASS ({'cold launch' if attempt == 0 else 'relaunch'}): "
                             f"{meta['channel_count']} channels and visible channel cards")
                    try:
                        check_guide(meta, names)
                        check_player(meta, channels)
                        check_live_event(meta, channels)
                    except Exception as error:  # noqa: BLE001 - always leave a diagnosable log
                        import traceback
                        # A gate failure writes a fresh smoke-log via diagnose();
                        # the committed file from older runs must not mask it, so
                        # only skip when this run already wrote one (mtime check
                        # via the progress file's own trail is overkill - the log
                        # existing AND the failure coming from wait_alive means
                        # diagnose() has just run).
                        if "process died" not in str(error) and "not seen" not in str(error):
                            diagnose(f"Guide/player check crashed: {type(error).__name__}: {error}\n"
                                     f"{traceback.format_exc()}", last_dump)
                        raise
                    return
                last_error = f"channel count seen: {count}; visible channel names: {named[:3]}; texts: {sorted(texts)[:12]}"
            except (subprocess.SubprocessError, ET.ParseError) as error:
                # A dump that did not finish is not evidence of a broken app.
                last_error = f"{type(error).__name__}: {error}"
            time.sleep(2)
        diagnose(f"APK did not show bundled channels within {UI_DEADLINE_SECONDS} seconds "
                 f"(attempt {'cold launch' if attempt == 0 else 'relaunch'}). Last check: {last_error}",
                 last_dump)
        raise RuntimeError("APK did not show bundled channels in time")


if __name__ == "__main__":
    main()
