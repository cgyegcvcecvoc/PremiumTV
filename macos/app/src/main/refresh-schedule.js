'use strict';

/**
 * When the app should check the repository for new data.
 *
 * The GitHub workflows that publish this repository's playlists and guide use
 * America/New_York for their cron jobs. This module mirrors every daily slot in
 * scrape.yml, quick-update.yml and epg-build.yml, then adds the same 45-minute
 * publishing grace period the Android app uses, so a check lands after the
 * publishing job has finished writing rather than during it.
 *
 * tests/test_macos_app.py fails the build if these slots drift from the
 * workflows; test/refresh-schedule.test.js checks the arithmetic.
 *
 * This module is deliberately free of Electron imports so it can be unit
 * tested with plain Node.
 */

const REPOSITORY_TIME_ZONE = 'America/New_York';
const PUBLISHING_GRACE_MINUTES = 45;

// Keep in sync with scrape.yml, quick-update.yml and epg-build.yml.
const SOURCE_PUBLICATION_SLOTS = [
  { hour: 1, minute: 19 },
  { hour: 3, minute: 7 },
  { hour: 5, minute: 47 },
  { hour: 6, minute: 23 },
  { hour: 7, minute: 31 },
  { hour: 9, minute: 41 },
  { hour: 12, minute: 53 },
  { hour: 13, minute: 47 },
  { hour: 16, minute: 41 },
  { hour: 17, minute: 47 },
  { hour: 19, minute: 23 },
  { hour: 20, minute: 17 },
  { hour: 23, minute: 29 },
];

const MINUTE_MS = 60 * 1000;
const DAY_MS = 24 * 60 * MINUTE_MS;

const partsFormatter = new Intl.DateTimeFormat('en-US', {
  timeZone: REPOSITORY_TIME_ZONE,
  hour12: false,
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
  second: '2-digit',
});

const readableFormatter = new Intl.DateTimeFormat('en-US', {
  timeZone: REPOSITORY_TIME_ZONE,
  hour12: true,
  month: 'short',
  day: 'numeric',
  hour: 'numeric',
  minute: '2-digit',
  timeZoneName: 'short',
});

/** Wall-clock parts of an instant, read in the repository's time zone. */
function wallClockParts(instantMs) {
  const parts = {};
  for (const part of partsFormatter.formatToParts(new Date(instantMs))) {
    if (part.type !== 'literal') parts[part.type] = Number(part.value);
  }
  // ICU renders midnight as hour 24 with hour12:false on some platforms.
  if (parts.hour === 24) parts.hour = 0;
  return parts;
}

/** Milliseconds to add to UTC to get the repository's local time. */
function zoneOffsetMs(instantMs) {
  const p = wallClockParts(instantMs);
  const asUtc = Date.UTC(p.year, p.month - 1, p.day, p.hour, p.minute, p.second);
  return asUtc - instantMs;
}

/**
 * Instant at which the repository's time zone reads `year-month-day hour:minute`.
 *
 * Solved in two passes so a slot that falls on a DST transition still resolves
 * to the intended wall-clock time instead of being an hour out.
 */
function epochForWallClock(year, month, day, hour, minute) {
  const guess = Date.UTC(year, month - 1, day, hour, minute, 0, 0);
  let candidate = guess - zoneOffsetMs(guess);
  const refined = guess - zoneOffsetMs(candidate);
  if (refined !== candidate) candidate = refined;
  return candidate;
}

/** Adds days to a wall-clock date without drifting across a DST boundary. */
function shiftWallClockDay(year, month, day, dayOffset) {
  const shifted = new Date(Date.UTC(year, month - 1, day + dayOffset));
  return {
    year: shifted.getUTCFullYear(),
    month: shifted.getUTCMonth() + 1,
    day: shifted.getUTCDate(),
  };
}

/**
 * Absolute instant of the first publication slot plus grace after `afterMs`.
 *
 * The search starts on the previous repository day because the 23:29 slot plus
 * its grace lands just after midnight; a today-only loop would skip that check.
 */
function nextRunAfter(afterMs) {
  const today = wallClockParts(afterMs);
  let nearest = Number.MAX_SAFE_INTEGER;

  for (let dayOffset = -1; dayOffset <= 2; dayOffset += 1) {
    const day = shiftWallClockDay(today.year, today.month, today.day, dayOffset);
    for (const slot of SOURCE_PUBLICATION_SLOTS) {
      const published = epochForWallClock(day.year, day.month, day.day, slot.hour, slot.minute);
      const candidate = published + PUBLISHING_GRACE_MINUTES * MINUTE_MS;
      if (candidate > afterMs && candidate < nearest) nearest = candidate;
    }
  }

  if (nearest === Number.MAX_SAFE_INTEGER) {
    throw new Error('No automatic refresh slot could be calculated');
  }
  return nearest;
}

/** The slot that produced `runAtMs`, or null when it is not one of ours. */
function slotForRun(runAtMs) {
  const p = wallClockParts(runAtMs);
  const minutesSinceMidnight = p.hour * 60 + p.minute;
  for (const slot of SOURCE_PUBLICATION_SLOTS) {
    const expected = slot.hour * 60 + slot.minute + PUBLISHING_GRACE_MINUTES;
    // Slots past midnight roll over (23:29 + 45m = 00:14).
    if (expected % (24 * 60) === minutesSinceMidnight) return slot;
  }
  return null;
}

/** How long to wait from `fromMs` before the next check is due. */
function delayUntilNextRun(fromMs) {
  return Math.max(0, nextRunAfter(fromMs) - fromMs);
}

/** Human-readable description of an instant, in the repository's time zone. */
function formatInRepositoryZone(instantMs) {
  return readableFormatter.format(new Date(instantMs));
}

/** Every slot plus grace, as repository-local HH:MM strings. */
function slotTimes() {
  return SOURCE_PUBLICATION_SLOTS.map((slot) => {
    const total = (slot.hour * 60 + slot.minute + PUBLISHING_GRACE_MINUTES) % (24 * 60);
    const hour = String(Math.floor(total / 60)).padStart(2, '0');
    const minute = String(total % 60).padStart(2, '0');
    return `${hour}:${minute}`;
  });
}

module.exports = {
  REPOSITORY_TIME_ZONE,
  PUBLISHING_GRACE_MINUTES,
  SOURCE_PUBLICATION_SLOTS,
  nextRunAfter,
  delayUntilNextRun,
  slotForRun,
  slotTimes,
  formatInRepositoryZone,
  epochForWallClock,
  zoneOffsetMs,
  DAY_MS,
};
