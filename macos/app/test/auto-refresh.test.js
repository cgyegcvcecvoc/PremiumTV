'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');

const { AutoRefresh, previousRunBefore } = require('../src/main/auto-refresh');

function makeClock() {
  let now = Date.UTC(2026, 9, 10, 12, 0, 0);
  const timers = [];
  let nextId = 1;
  return {
    get now() {
      return now;
    },
    advance(ms) {
      now += ms;
    },
    setTimeout(fn, ms) {
      const id = nextId++;
      timers.push({ id, fn, at: now + ms });
      return id;
    },
    clearTimeout(id) {
      const index = timers.findIndex((t) => t.id === id);
      if (index !== -1) timers.splice(index, 1);
    },
    fireDue() {
      const due = timers.filter((t) => t.at <= now).sort((a, b) => a.at - b.at);
      for (const timer of due) {
        const index = timers.indexOf(timer);
        if (index !== -1) timers.splice(index, 1);
        timer.fn();
      }
      return due.length;
    },
  };
}

function makeRepository() {
  const calls = [];
  return {
    info: { lastAttemptAt: 0 },
    noted: [],
    refresh(trigger, meta) {
      calls.push({ trigger, meta });
      return Promise.resolve({ ok: true, updated: true, message: 'ok' });
    },
    noteNextAutomaticRefresh(ms) {
      this.noted.push(ms);
      this.info.nextAutomaticAt = ms;
    },
    calls,
  };
}

test('start arms a timer and reports the next run to the repository', () => {
  const clock = makeClock();
  const repository = makeRepository();
  const refresh = new AutoRefresh({
    repository,
    now: () => clock.now,
    setTimeout: (fn, ms) => clock.setTimeout(fn, ms),
    clearTimeout: (id) => clock.clearTimeout(id),
  });

  const next = refresh.start();
  assert.ok(next > clock.now);
  assert.equal(repository.noted.length, 1);
  assert.equal(repository.noted[0], next);
});

test('a due check refreshes automatically then chains the next slot', async () => {
  const clock = makeClock();
  const repository = makeRepository();
  const refresh = new AutoRefresh({
    repository,
    now: () => clock.now,
    setTimeout: (fn, ms) => clock.setTimeout(fn, ms),
    clearTimeout: (id) => clock.clearTimeout(id),
  });

  refresh.start();
  const before = repository.calls.length;
  clock.advance(2 * 24 * 3600 * 1000); // jump past at least one slot
  clock.fireDue();
  await new Promise((resolve) => setImmediate(resolve));
  await new Promise((resolve) => setImmediate(resolve));

  assert.ok(repository.calls.length > before, 'a refresh should have fired');
  assert.equal(repository.calls[0].trigger, 'automatic');
  // A new slot was chained after the run.
  assert.equal(repository.noted.length, 2);
});

test('runManual uses the manual trigger', async () => {
  const clock = makeClock();
  const repository = makeRepository();
  const refresh = new AutoRefresh({
    repository,
    now: () => clock.now,
    setTimeout: (fn, ms) => clock.setTimeout(fn, ms),
    clearTimeout: (id) => clock.clearTimeout(id),
  });
  refresh.start();
  await refresh.runManual();
  assert.equal(repository.calls[0].trigger, 'manual');
});

test('catchUpIfOverdue refreshes when a slot passed without an attempt', async () => {
  const clock = makeClock();
  const repository = makeRepository();
  repository.info.lastAttemptAt = clock.now - 2 * 24 * 3600 * 1000; // long ago
  const refresh = new AutoRefresh({
    repository,
    now: () => clock.now,
    setTimeout: (fn, ms) => clock.setTimeout(fn, ms),
    clearTimeout: (id) => clock.clearTimeout(id),
  });
  const caught = await refresh.catchUpIfOverdue();
  assert.equal(caught, true);
  assert.equal(repository.calls[0].trigger, 'automatic');
});

test('catchUpIfOverdue does nothing when the app just checked', async () => {
  const clock = makeClock();
  const repository = makeRepository();
  repository.info.lastAttemptAt = clock.now; // just checked
  const refresh = new AutoRefresh({
    repository,
    now: () => clock.now,
    setTimeout: (fn, ms) => clock.setTimeout(fn, ms),
    clearTimeout: (id) => clock.clearTimeout(id),
  });
  const caught = await refresh.catchUpIfOverdue();
  assert.equal(caught, false);
  assert.equal(repository.calls.length, 0);
});

test('previousRunBefore lands on a slot plus grace', () => {
  const now = Date.now();
  const previous = previousRunBefore(now);
  assert.ok(previous, 'there is always a previous slot');
  assert.ok(previous <= now);
  assert.ok(now - previous <= 2 * 24 * 3600 * 1000, 'previous slot is within two days');
});
