'use strict';

/**
 * The clock that heads the Live Events tab.
 *
 * A kickoff is one instant, but "5:45 PM" only means something next to the
 * clock it is read on. This module keeps one clock on screen - ticking, with
 * its zone name and its offset - and then reads every kickoff on the tab
 * through that same zone, so the card and the header can never disagree.
 *
 * Which zone is shown starts from the location the viewer already gave the
 * local-channels shelf: the market's longitude picks the band of zones to
 * offer, the device's own zone is always first, and the viewer's pick is
 * remembered. Nothing here sends a location anywhere - the directory already
 * lives on the device (see local-channels.js).
 *
 * Kept free of app state so it can be unit tested in a VM, exactly like
 * live-events.js and player.js.
 */

window.PremiumLiveClock = (function () {
  const STORAGE_KEY = 'premiumtv.live.clockZone';

  /**
   * Zones offered per band, nearest-used first. These are the zones a viewer
   * in that part of the world is most likely to want when travelling or
   * following a league abroad; the device's own zone always leads the list.
   */
  const BANDS = [
    {
      id: 'americas',
      label: 'The Americas',
      min: -180,
      max: -30,
      zones: [
        'America/New_York', 'America/Chicago', 'America/Denver',
        'America/Los_Angeles', 'America/Anchorage', 'Pacific/Honolulu',
        'America/Toronto', 'America/Mexico_City', 'America/Sao_Paulo',
        'America/Argentina/Buenos_Aires',
      ],
    },
    {
      id: 'atlantic',
      label: 'Europe, Africa & the Atlantic',
      min: -30,
      max: 40,
      // Ordered by how often a US or travelling viewer wants them, because
      // the other bands are only previewed with their first few entries.
      zones: [
        'Europe/London', 'Europe/Paris', 'Europe/Berlin', 'Europe/Madrid',
        'Europe/Rome', 'Europe/Lisbon', 'Europe/Dublin', 'Europe/Amsterdam',
        'Europe/Stockholm', 'Europe/Warsaw', 'UTC', 'Europe/Moscow',
        'Africa/Lagos', 'Africa/Johannesburg',
      ],
    },
    {
      id: 'east',
      label: 'South & East Asia',
      min: 40,
      max: 90,
      zones: [
        'Asia/Dubai', 'Asia/Karachi', 'Asia/Kolkata', 'Asia/Dhaka',
        'Asia/Bangkok', 'Asia/Jakarta', 'Asia/Singapore', 'Asia/Shanghai',
        'Asia/Hong_Kong', 'Asia/Tokyo', 'Asia/Seoul',
      ],
    },
    {
      id: 'pacific',
      label: 'East Asia & the Pacific',
      min: 90,
      max: 180,
      zones: [
        'Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Manila', 'Asia/Tokyo',
        'Asia/Seoul', 'Australia/Perth', 'Australia/Adelaide',
        'Australia/Sydney', 'Pacific/Auckland',
      ],
    },
  ];

  /** A zone name as a person reads it: "America/New_York" -> "New York". */
  function zoneLabel(zone) {
    const text = String(zone || '').trim();
    if (!text) return 'Device time';
    if (text === 'UTC') return 'UTC';
    const leaf = text.split('/').pop() || text;
    return leaf.replace(/_/g, ' ');
  }

  /** True when this runtime can format in `zone`. */
  function isKnownZone(zone) {
    const text = String(zone || '').trim();
    if (!text) return false;
    try {
      new Intl.DateTimeFormat(undefined, { timeZone: text }).format(0);
      return true;
    } catch (_error) {
      return false;
    }
  }

  /**
   * The band a longitude falls in, or null when there is no location.
   * Bands deliberately overlap at their edges: a viewer in Iceland is as
   * likely to follow London as New York, so both lists are readable.
   */
  function bandForLongitude(longitude) {
    // Number(null) is 0, which would silently place a viewer who never gave a
    // location on the Greenwich meridian - so "no location" is checked first.
    if (longitude === null || longitude === undefined || longitude === "") return null;
    const value = Number(longitude);
    if (!Number.isFinite(value)) return null;
    const bounded = ((value + 180) % 360 + 360) % 360 - 180;
    return BANDS.find((band) => bounded >= band.min && bounded < band.max) || null;
  }

  /**
   * The zones to offer, device first, then the location's band, then the
   * other bands truncated - so a viewer who moved (or follows a league
   * elsewhere) still finds their zone without typing it.
   *
   * `longitude` comes from the saved local market when there is one; without
   * it the list is still useful, it is just shorter.
   */
  function suggestZones(deviceZone, longitude, limit) {
    const max = Number.isFinite(limit) ? limit : 24;
    const out = [];
    const seen = new Set();
    function add(zone) {
      const text = String(zone || '').trim();
      if (!text || seen.has(text) || !isKnownZone(text) || out.length >= max) return;
      seen.add(text);
      out.push({ zone: text, label: zoneLabel(text) });
    }
    add(deviceZone);
    add(deviceZone === 'UTC' ? '' : 'UTC');
    const band = bandForLongitude(longitude);
    if (band) band.zones.forEach(add);
    // Two or three from every other band, so a viewer following a league
    // abroad (or about to travel) finds that clock without typing a zone name.
    for (const other of BANDS) {
      if (band && other.id === band.id) continue;
      other.zones.slice(0, 5).forEach(add);
    }
    return out;
  }

  /**
   * The clock's own line: "7:42:05 PM · New York · GMT-5".
   * A zone that is not the device's also says how far off it is.
   */
  function clockLine(nowMs, zone, deviceZone) {
    const live = window.PremiumLive;
    if (!live) return '';
    const resolved = live.resolveTimeZone(zone, deviceZone);
    const clock = live.clockText(nowMs, resolved);
    if (!clock) return '';
    const offset = live.zoneOffset(nowMs, resolved);
    const parts = [clock, zoneLabel(resolved), offset.label];
    if (offset.deltaMinutes && !(zone && resolved === deviceZone)) {
      parts.push(deltaLabel(offset.deltaMinutes));
    }
    return parts.filter(Boolean).join(' · ');
  }

  /** "+3 h", "-2 h 30 m": how far one clock is from the device's own. */
  function deltaLabel(minutes) {
    const total = Math.trunc(Number(minutes) || 0);
    if (!total) return '';
    const sign = total > 0 ? '+' : '-';
    const abs = Math.abs(total);
    const hours = Math.trunc(abs / 60);
    const mins = abs % 60;
    if (!hours) return sign + mins + ' min';
    return sign + hours + ' h' + (mins ? ' ' + mins + ' m' : '');
  }

  /** The date in the clock's zone, e.g. "Mon, Nov 23". */
  function dateLine(nowMs, zone) {
    const options = { weekday: 'short', month: 'short', day: 'numeric' };
    const text = String(zone || '');
    if (text) options.timeZone = text;
    try {
      return new Intl.DateTimeFormat(undefined, options).format(
        new Date(Number.isFinite(nowMs) ? nowMs : Date.now()),
      );
    } catch (_error) {
      return '';
    }
  }

  /**
   * The soonest kickoff still ahead, across every section:
   * `{ ms, title, sport }` or null. Used for the header's "next kickoff" line,
   * which is the one thing a viewer actually wants from a clock here.
   */
  function nextKickoff(events, nowMs) {
    const at = Number.isFinite(nowMs) ? nowMs : Date.now();
    let best = null;
    for (const event of events || []) {
      const kickoff = Number(event && event.kickoffMs);
      if (!Number.isFinite(kickoff) || kickoff <= at) continue;
      if (!best || kickoff < best.ms) {
        best = { ms: kickoff, title: event.title || '', sport: event.sport || '' };
      }
    }
    return best;
  }

  /**
   * The one sentence under the clock: which clock the times are read in, and
   * how long until the next kickoff (or that none is scheduled yet).
   */
  function summary(nowMs, zone, deviceZone, events) {
    const live = window.PremiumLive;
    const resolved = live ? live.resolveTimeZone(zone, deviceZone) : zone;
    const offset = live ? live.zoneOffset(nowMs, resolved).label : '';
    const where = zoneLabel(resolved) + (offset ? ' (' + offset + ')' : '');
    const custom = resolved && deviceZone && resolved !== deviceZone;
    let text = custom
      ? 'Kickoff times are read in ' + where + ', not this device’s clock.'
      : 'Kickoff times are read in your clock, ' + where + '.';
    const next = nextKickoff(events, nowMs);
    if (next && live) {
      const remaining = Math.max(0, (next.ms - nowMs) / 1000);
      text += ' Next kickoff in ' + live.countdownText(remaining) + ': ' + next.title + '.';
    }
    return text;
  }

  /** Persisted zone choice, or '' for "whatever the device (or market) says". */
  function loadChoice(storage) {
    try {
      const value = storage && storage.getItem(STORAGE_KEY);
      return isKnownZone(value) ? String(value) : '';
    } catch (_error) {
      return '';
    }
  }

  function saveChoice(storage, zone) {
    try {
      if (zone && isKnownZone(zone)) storage.setItem(STORAGE_KEY, zone);
      else storage.removeItem(STORAGE_KEY);
    } catch (_error) {
      // A blocked storage area simply means the choice lasts for this session.
    }
  }

  /**
   * Mount the widget into `host`.
   *
   * `options`:
   *   deviceZone     the device's own zone (live.deviceTimeZone())
   *   getLongitude() the saved local market's longitude, or null
   *   getEvents()    the parsed live events, for the next-kickoff line
   *   getZone()      the currently chosen zone ('' = follow the device)
   *   setZone(zone)  called when the viewer picks another zone
   *   storage        localStorage-shaped object for the choice
   *
   * Returns `{ refresh(), destroy() }`; `refresh()` repaints immediately
   * (after a zone change or a library refresh) and the one-second timer keeps
   * the clock honest in between. The caller destroys it when the tab closes.
   */
  function mount(host, options) {
    if (!host) return { refresh() {}, destroy() {} };
    const settings = options || {};
    const deviceZone = String(settings.deviceZone || '') || deviceZoneOf();
    let choice = String(settings.getZone ? settings.getZone() : '') || loadChoice(settings.storage);
    const doc = host.ownerDocument || document;

    host.classList.add('live-clock');
    host.textContent = '';

    const dot = doc.createElement('span');
    dot.className = 'live-clock-dot';
    dot.setAttribute('aria-hidden', 'true');
    const time = doc.createElement('strong');
    time.className = 'live-clock-time';
    time.dataset.liveClock = 'time';
    const zone = doc.createElement('span');
    zone.className = 'live-clock-zone';
    zone.dataset.liveClock = 'zone';
    const next = doc.createElement('span');
    next.className = 'live-clock-next';
    next.dataset.liveClock = 'next';
    const picker = doc.createElement('select');
    picker.className = 'live-clock-zone-picker';
    picker.setAttribute('aria-label', 'Clock zone for kickoff times');
    picker.dataset.liveClock = 'picker';
    const note = doc.createElement('p');
    note.className = 'live-clock-note';
    note.dataset.liveClock = 'note';

    host.append(dot, time, zone, next, picker, note);

    function fillPicker() {
      const longitude = settings.getLongitude ? settings.getLongitude() : null;
      const suggested = suggestZones(deviceZone, longitude);
      const offered = new Set(suggested.map((row) => row.zone));
      // The device's own zone is the top option's job; listing it again below
      // would read as two different clocks.
      if (deviceZone) offered.delete(deviceZone);
      // A zone the viewer chose earlier must stay selectable even if the
      // market's band no longer offers it (they moved, the directory changed).
      const stray = choice && !offered.has(choice) && isKnownZone(choice) ? choice : '';
      picker.textContent = '';
      const auto = doc.createElement('option');
      auto.value = '';
      auto.textContent = 'Device clock' + (deviceZone ? ' (' + zoneLabel(deviceZone) + ')' : '');
      picker.append(auto);
      const placed = new Set();
      for (const band of BANDS) {
        const members = band.zones.filter((zone) => offered.has(zone) && !placed.has(zone));
        if (!members.length) continue;
        const group = doc.createElement('optgroup');
        group.label = band.label;
        for (const zone of members) {
          placed.add(zone);
          group.append(optionFor(zone));
        }
        picker.append(group);
      }
      const leftovers = suggested.map((row) => row.zone)
        .filter((zone) => offered.has(zone) && !placed.has(zone));
      if (stray) leftovers.push(stray);
      for (const zone of leftovers) {
        placed.add(zone);
        picker.append(optionFor(zone));
      }
      picker.value = choice;
    }

    function optionFor(zone) {
      const option = doc.createElement('option');
      option.value = zone;
      option.textContent = zoneLabel(zone);
      return option;
    }

    function paint() {
      const live = window.PremiumLive;
      if (!live) return;
      const now = Date.now();
      const resolved = live.resolveTimeZone(choice, deviceZone);
      const offset = live.zoneOffset(now, resolved);
      time.textContent = live.clockText(now, resolved) || '--:--:--';
      const elsewhere = Boolean(deviceZone) && resolved !== deviceZone;
      zone.textContent = zoneLabel(resolved) + ' · ' + offset.label +
        (elsewhere && offset.deltaMinutes ? ' · ' + deltaLabel(offset.deltaMinutes) : '');
      const events = settings.getEvents ? settings.getEvents() : [];
      const upcoming = nextKickoff(events, now);
      if (upcoming) {
        next.textContent = 'Next kickoff in ' + live.countdownText((upcoming.ms - now) / 1000) +
          ' · ' + live.kickoffStamp(upcoming.ms, resolved);
        next.title = upcoming.title + (upcoming.sport ? ' · ' + upcoming.sport : '');
      } else {
        next.textContent = '';
        next.removeAttribute('title');
      }
      note.textContent = summary(now, choice, deviceZone, events);
      host.dataset.zone = resolved || '';
      host.dataset.delta = String(offset.deltaMinutes);
      host.dataset.date = dateLine(now, resolved);
      dot.classList.toggle('live', Boolean(upcoming && upcoming.ms - now <= 3600000));
    }

    picker.addEventListener('change', () => {
      choice = picker.value;
      saveChoice(settings.storage, choice);
      if (settings.setZone) settings.setZone(choice);
      paint();
    });

    fillPicker();
    paint();
    const timer = window.setInterval(paint, 1000);
    return {
      refresh() {
        fillPicker();
        paint();
      },
      destroy() {
        window.clearInterval(timer);
      },
    };
  }

  function deviceZoneOf() {
    return (window.PremiumLive && window.PremiumLive.deviceTimeZone()) || '';
  }

  return {
    STORAGE_KEY,
    BANDS,
    zoneLabel,
    isKnownZone,
    bandForLongitude,
    suggestZones,
    clockLine,
    dateLine,
    deltaLabel,
    nextKickoff,
    summary,
    loadChoice,
    saveChoice,
    mount,
  };
})();
