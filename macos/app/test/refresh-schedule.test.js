'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const schedule = require('../src/main/refresh-schedule');

test('there are 13 publication slots mirroring the three workflows', () => {
  assert.equal(schedule.SOURCE_PUBLICATION_SLOTS.length, 13);
});

test('nextRunAfter is always in the future and at a slot plus grace', () => {
  for (const sample of [0, Date.now(), Date.now() + 3 * 3600 * 1000]) {
    const next = schedule.nextRunAfter(sample);
    assert.ok(next > sample, 'next run must be after the sample instant');

    // The instant must read as slot+45 minutes on the New York wall clock.
    const p = new Intl.DateTimeFormat('en-US', {
      timeZone: schedule.REPOSITORY_TIME_ZONE,
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
    }).formatToParts(new Date(next));
    const hour = Number(p.find((x) => x.type === 'hour').value) % 24;
    const minute = Number(p.find((x) => x.type === 'minute').value);
    const wall = (hour * 60 + minute) % (24 * 60);

    const expected = new Set(
      schedule.SOURCE_PUBLICATION_SLOTS.map(
        (s) => (s.hour * 60 + s.minute + schedule.PUBLISHING_GRACE_MINUTES) % (24 * 60),
      ),
    );
    assert.ok(expected.has(wall), `wall ${hour}:${minute} is not a known slot+grace`);
  }
});

test('the schedule is dense: at most a day separates consecutive checks', () => {
  let now = Date.UTC(2026, 9, 10, 12, 0, 0);
  let previous = now;
  for (let i = 0; i < 20; i += 1) {
    const next = schedule.nextRunAfter(now);
    assert.ok(next - now <= schedule.DAY_MS, 'a check should never be more than a day away');
    assert.ok(next > now);
    previous = next;
    now = next;
  }
  assert.ok(previous > now - 1);
});

test('epochForWallClock resolves midnight correctly', () => {
  // New York midnight on a fixed date, converted and checked both directions.
  const instant = schedule.epochForWallClock(2026, 10, 10, 0, 0);
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: schedule.REPOSITORY_TIME_ZONE,
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
  }).formatToParts(new Date(instant));
  assert.equal(Number(parts.find((x) => x.type === 'hour').value) % 24, 0);
  assert.equal(Number(parts.find((x) => x.type === 'minute').value), 0);
});
