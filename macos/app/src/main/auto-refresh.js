'use strict';

/**
 * Schedules the app-side download checks.
 *
 * GitHub Actions publishes this repository's playlists and guide on cron slots
 * in America/New_York. This mirrors each daily slot plus the 45-minute
 * publishing grace period, checks then, and chains the next slot after every
 * completed check. Timers do not survive a quit the way Android's WorkManager
 * request does, so a check that was missed while the Mac slept is caught up
 * when the app is woken or brought to the front (see catchUpIfOverdue).
 *
 * No Electron imports: test/auto-refresh.test.js drives it with fake timers.
 */

const schedule = require('./refresh-schedule');

/** A check older than this counts as missed and is retried on wake. */
const OVERDUE_GRACE_MS = 5 * 60 * 1000;

class AutoRefresh {
  /**
   * @param {object} options
   * @param {{refresh: Function, noteNextAutomaticRefresh?: Function, info?: object}} options.repository
   * @param {Function} [options.now]        clock, injectable
   * @param {Function} [options.setTimeout] injectable for tests
   * @param {Function} [options.clearTimeout] injectable for tests
   * @param {Function} [options.onResult]   called with every refresh outcome
   */
  constructor(options) {
    this.repository = options.repository;
    this.now = options.now || (() => Date.now());
    this.setTimeoutFn = options.setTimeout || global.setTimeout;
    this.clearTimeoutFn = options.clearTimeout || global.clearTimeout;
    this.onResult = options.onResult || (() => {});
    this.timer = null;
    this.nextRunAt = null;
    this.running = false;
  }

  /** Arms the next check and tells the repository when it is due. */
  scheduleNext(afterMs = this.now()) {
    if (this.timer !== null) {
      this.clearTimeoutFn(this.timer);
      this.timer = null;
    }
    const nextRun = schedule.nextRunAfter(afterMs);
    this.nextRunAt = nextRun;
    if (typeof this.repository.noteNextAutomaticRefresh === 'function') {
      this.repository.noteNextAutomaticRefresh(nextRun);
    }
    const delay = Math.max(0, nextRun - this.now());
    this.timer = this.setTimeoutFn(() => {
      this.timer = null;
      this.runDue(nextRun);
    }, delay);
    if (this.timer && typeof this.timer.unref === 'function') this.timer.unref();
    return nextRun;
  }

  start() {
    return this.scheduleNext();
  }

  stop() {
    if (this.timer !== null) {
      this.clearTimeoutFn(this.timer);
      this.timer = null;
    }
  }

  /** The scheduled check fired: refresh, then chain the next slot. */
  async runDue(scheduledFor) {
    if (this.running) return null;
    this.running = true;
    let outcome = null;
    try {
      outcome = await this.repository.refresh('automatic', { scheduledFor });
      this.onResult(outcome);
    } catch (error) {
      outcome = { ok: false, retryable: true, message: `the check failed: ${error.message}` };
      this.onResult(outcome);
    } finally {
      this.running = false;
    }
    this.scheduleNext();
    return outcome;
  }

  /**
   * Runs a check immediately regardless of validators (Settings → Force
   * refresh all now) and re-arms the schedule.
   */
  async runManual() {
    const outcome = await this.repository.refresh('manual');
    this.onResult(outcome);
    this.scheduleNext();
    return outcome;
  }

  /**
   * Refreshes now when a slot passed while the Mac was asleep or the app was
   * closed. Returns true when a catch-up check was started.
   */
  async catchUpIfOverdue() {
    const now = this.now();
    const lastAttempt = (this.repository.info && this.repository.info.lastAttemptAt) || 0;
    const previousSlot = previousRunBefore(now);
    if (!previousSlot) return false;
    if (lastAttempt >= previousSlot - OVERDUE_GRACE_MS) return false;
    await this.repository.refresh('automatic', { scheduledFor: previousSlot });
    this.scheduleNext();
    return true;
  }
}

/** Most recent slot instant that is already in the past. */
function previousRunBefore(beforeMs) {
  let best = 0;
  const dayMs = schedule.DAY_MS;
  for (let dayOffset = -2; dayOffset <= 1; dayOffset += 1) {
    for (const slot of schedule.SOURCE_PUBLICATION_SLOTS) {
      const day = new Date(beforeMs + dayOffset * dayMs);
      const parts = new Intl.DateTimeFormat('en-US', {
        timeZone: schedule.REPOSITORY_TIME_ZONE,
        hour12: false,
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
      }).formatToParts(day);
      const get = (type) => Number(parts.find((p) => p.type === type).value);
      const candidate =
        schedule.epochForWallClock(get('year'), get('month'), get('day'), slot.hour, slot.minute) +
        schedule.PUBLISHING_GRACE_MINUTES * 60 * 1000;
      if (candidate <= beforeMs && candidate > best) best = candidate;
    }
  }
  return best || null;
}

module.exports = { AutoRefresh, previousRunBefore, OVERDUE_GRACE_MS };
