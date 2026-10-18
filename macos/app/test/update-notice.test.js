'use strict';

/**
 * The remote "please update" notice: who it targets, what it says, and how it
 * escalates when the published support window closes.
 *
 * These run against the real `app-update-notice.json` in the repository, so a
 * wording or version-range edit that would silence the popup - or nag a build
 * that is already current - fails here rather than on somebody's TV.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const {
  NOTICE_URL,
  MAX_NOTICE_BYTES,
  parseInstant,
  formatDay,
  selectNotice,
} = require('../src/main/update-notice');
const { AppUpdater } = require('../src/main/updater');

const REPO = path.resolve(__dirname, '..', '..', '..');
const NOTICE_PATH = path.join(REPO, 'app-update-notice.json');
const DOCUMENT = fs.readFileSync(NOTICE_PATH, 'utf8');
const PUBLISHED = JSON.parse(DOCUMENT);

const DAY_MS = 24 * 60 * 60 * 1000;
const BEFORE_SUPPORT_ENDS = parseInstant(PUBLISHED.support_ends_utc) - DAY_MS;
const AFTER_SUPPORT_ENDS = parseInstant(PUBLISHED.support_ends_utc) + DAY_MS;

// ------------------------------------------------------------------ document

test('the published notice is small enough to fetch on every daily check', () => {
  assert.ok(DOCUMENT.length > 0);
  assert.ok(
    DOCUMENT.length <= MAX_NOTICE_BYTES,
    `the notice is ${DOCUMENT.length} bytes; the app refuses more than ${MAX_NOTICE_BYTES}`,
  );
});

test('the notice is published where installed apps already look for it', () => {
  assert.equal(
    NOTICE_URL,
    'https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/app-update-notice.json',
  );
  // The document names its own location, so a moved file is a visible mistake.
  assert.equal(PUBLISHED.notice_url, NOTICE_URL);
  assert.match(PUBLISHED.releases_url, /^https:\/\/github\.com\/cgyegcvcecvoc\/PremiumTV1\/releases/);
});

test('support ends exactly the published grace period after the first warning', () => {
  const warning = parseInstant(PUBLISHED.first_warning_utc);
  const ends = parseInstant(PUBLISHED.support_ends_utc);
  assert.ok(warning && ends, 'both dates must be readable');
  // Compared as calendar dates: support runs to the end of the last grace day,
  // so the timestamps are deliberately not an exact number of days apart.
  const dayOf = (millis) => Date.UTC(
    new Date(millis).getUTCFullYear(),
    new Date(millis).getUTCMonth(),
    new Date(millis).getUTCDate(),
  );
  const days = Math.round((dayOf(ends) - dayOf(warning)) / DAY_MS);
  assert.equal(days, PUBLISHED.grace_days,
    'the sunset must be the grace period after the first warning');
  assert.equal(days, 30, 'the promise to older builds is 30 days');
  assert.ok(ends > Date.now() - DAY_MS,
    'a support window already closed would freeze every older build on the next refresh');
});

// ------------------------------------------------------------------- policy

test('an older stable build is told to update, with the surprise spelled out', () => {
  const notice = selectNotice({
    body: DOCUMENT,
    appVersion: '1.0.2',
    newestVersion: '1.0.5',
    now: BEFORE_SUPPORT_ENDS,
  });
  assert.ok(notice, 'a build inside the targeted range must get a notice');
  assert.equal(notice.level, 'warning');
  assert.equal(notice.supportEnded, false);
  assert.match(notice.title, /newer PremiumTV/i);
  // The placeholders are resolved, never shown raw.
  assert.match(notice.message, /1\.0\.2/);
  assert.match(notice.message, /1\.0\.5/);
  assert.ok(!notice.message.includes('{'), 'no unsubstituted placeholder may survive');
  // The surprise is the point of the message: updating ends manual installs.
  assert.ok(notice.surprise.length > 40, 'the surprise must actually say something');
  assert.match(notice.surprise, /updates? itself|never download/i);
  assert.equal(notice.actionLabel, 'Update now');
  assert.match(notice.releasesUrl, /^https:\/\//);
});

test('every targeted older version is reached, and 1.0.0 is not left out', () => {
  for (const version of ['1.0.0', '1.0.1', '1.0.2', '1.0.3', '1.0.4']) {
    const notice = selectNotice({
      body: DOCUMENT, appVersion: version, newestVersion: '1.0.5', now: BEFORE_SUPPORT_ENDS,
    });
    assert.ok(notice, `${version} must be told to update`);
    assert.match(notice.message, new RegExp(version.replace(/\./g, '\\.')));
  }
});

test('a build at or above the newest release is never nagged', () => {
  for (const version of ['1.0.5', '1.0.6', '1.1.0', '1.1.1', '2.0.0']) {
    const notice = selectNotice({
      body: DOCUMENT, appVersion: version, newestVersion: '1.0.5', now: BEFORE_SUPPORT_ENDS,
    });
    assert.equal(notice, null, `${version} is not inside the targeted range`);
  }
});

test('the same rule escalates by itself once support ends', () => {
  const notice = selectNotice({
    body: DOCUMENT, appVersion: '1.0.3', newestVersion: '1.0.5', now: AFTER_SUPPORT_ENDS,
  });
  assert.ok(notice);
  assert.equal(notice.level, 'end_of_support');
  assert.equal(notice.supportEnded, true);
  assert.match(notice.title, /support .* ended/i);
  // The escalation has to say what actually stopped: the scraped data.
  assert.match(notice.message, /scrape|frozen/i);
  assert.match(notice.message, /Nov 16, 2026/);
  assert.ok(!notice.message.includes('{support_ends}'));
});

test('a disabled, malformed or unknown-schema document shows nothing', () => {
  const cases = {
    'disabled': JSON.stringify({ ...PUBLISHED, enabled: false }),
    'not json': ' PremiumTV ',
    'empty': '',
    'null body': null,
    'unknown schema': JSON.stringify({ ...PUBLISHED, schema: 99 }),
    'no rules': JSON.stringify({ ...PUBLISHED, rules: null }),
    'an array': JSON.stringify([PUBLISHED]),
  };
  for (const [name, body] of Object.entries(cases)) {
    const notice = selectNotice({
      body, appVersion: '1.0.4', newestVersion: '1.0.5', now: BEFORE_SUPPORT_ENDS,
    });
    assert.equal(notice, null, `${name} must never produce a popup`);
  }
});

test('a rule aimed at the other platform does not fire here', () => {
  const targetsCurrent = PUBLISHED.rules.find((rule) => rule.max_version === '1.0.4');
  assert.ok(targetsCurrent, 'the document must still target the last manual install');
  const androidOnly = JSON.stringify({
    ...PUBLISHED,
    rules: [{ ...targetsCurrent, platforms: ['android'] }],
  });
  assert.equal(selectNotice({
    body: androidOnly, appVersion: '1.0.4', now: BEFORE_SUPPORT_ENDS, platform: 'macos',
  }), null);
  assert.ok(selectNotice({
    body: androidOnly, appVersion: '1.0.4', now: BEFORE_SUPPORT_ENDS, platform: 'android',
  }), 'the same document must still reach Android');
});

test('an unreadable version never matches a range', () => {
  for (const version of ['', 'nightly', '1.0', 'v?', null]) {
    assert.equal(selectNotice({
      body: DOCUMENT, appVersion: version, now: BEFORE_SUPPORT_ENDS,
    }), null, `${JSON.stringify(version)} is not a version this app can compare`);
  }
});

test('a missing newest version still produces a usable sentence', () => {
  const notice = selectNotice({
    body: DOCUMENT, appVersion: '1.0.2', newestVersion: null, now: BEFORE_SUPPORT_ENDS,
  });
  assert.ok(notice);
  assert.match(notice.message, /the newest release/);
  assert.ok(!notice.message.includes('{newest}'));
});

// ------------------------------------------------------------------- helpers

test('parseInstant reads the two published shapes and refuses anything else', () => {
  assert.equal(parseInstant('2026-11-16T23:59:59Z'), Date.UTC(2026, 10, 16, 23, 59, 59));
  // A bare date means "that whole day", so support ends on its last millisecond.
  assert.equal(parseInstant('2026-11-16'), Date.UTC(2026, 10, 17) - 1);
  for (const value of [null, undefined, '', 'soon', '16/11/2026', '2026-13-45T00:00:00Z']) {
    assert.equal(parseInstant(value), null, `${JSON.stringify(value)} is not a date`);
  }
});

test('formatDay is UTC, so the date reads the same in every time zone', () => {
  assert.equal(formatDay(Date.UTC(2026, 10, 16, 23, 59, 59)), 'Nov 16, 2026');
  assert.equal(formatDay(parseInstant(PUBLISHED.support_ends_utc)), 'Nov 16, 2026');
});

// ------------------------------------------------------- updater integration

function noticeHarness(t, { currentVersion = '1.0.4', noticeBody = DOCUMENT, now } = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'premiumtv-notice-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const calls = [];
  const fetchImpl = async (url) => {
    calls.push(url);
    if (url.includes('/releases?')) {
      return new Response(JSON.stringify([{
        tag_name: 'v1.0.5',
        draft: false,
        prerelease: false,
        html_url: 'https://github.com/cgyegcvcecvoc/PremiumTV1/releases/tag/v1.0.5',
        assets: [{
          name: 'PremiumTV-1.0.5-mac-arm64.dmg',
          size: 10,
          browser_download_url: 'https://github.com/releases/PremiumTV-1.0.5-mac-arm64.dmg',
        }],
      }]), { status: 200, headers: { etag: 'W/"r1"' } });
    }
    if (url.endsWith('app-update-notice.json')) {
      return noticeBody === null
        ? new Response('nope', { status: 404 })
        : new Response(noticeBody, { status: 200 });
    }
    return new Response('not found', { status: 404 });
  };
  const build = (clockNow) => new AppUpdater({
    currentVersion,
    stateFile: path.join(dir, 'update-state.json'),
    downloadDir: path.join(dir, 'updates'),
    arch: 'arm64',
    fetchImpl,
    shell: { openPath: async () => '', openExternal: async () => {} },
    now: () => (clockNow == null ? (now == null ? Date.now() : now) : clockNow),
  });
  return { build, calls, dir, stateFile: path.join(dir, 'update-state.json') };
}

test('the daily check resolves a popup for an older build', async (t) => {
  const { build, calls } = noticeHarness(t, { now: BEFORE_SUPPORT_ENDS });
  const state = await build().check(true);
  assert.ok(state.notice, 'an older build must come back from a check with a notice');
  assert.equal(state.notice.level, 'warning');
  assert.equal(state.noticeDismissedForLaunch, false);
  assert.ok(calls.some((url) => url.endsWith('app-update-notice.json')),
    'the notice is read during the same daily check');
  // The raw document is persisted but kept out of what the renderer receives.
  assert.equal(state.noticeBody, undefined, 'status() must not ship the raw document');
});

test('a build that is already current gets no popup', async (t) => {
  const { build } = noticeHarness(t, { currentVersion: '1.0.5', now: BEFORE_SUPPORT_ENDS });
  const state = await build().check(true);
  assert.equal(state.notice, null);
});

test('an unreachable notice keeps the app working and shows nothing new', async (t) => {
  const { build } = noticeHarness(t, { noticeBody: null, now: BEFORE_SUPPORT_ENDS });
  const state = await build().check(true);
  assert.equal(state.error, null, 'a missing notice must never fail the update check');
  assert.equal(state.notice, null);
  assert.equal(state.availableVersion, '1.0.5', 'the release list still resolves normally');
});

test('dismissing hides the popup for this launch only', async (t) => {
  const { build, stateFile } = noticeHarness(t, { now: BEFORE_SUPPORT_ENDS });
  const updater = build();
  await updater.check(true);
  assert.ok(updater.status().notice);

  const dismissed = updater.dismissNotice();
  assert.equal(dismissed.noticeDismissedForLaunch, true);
  assert.ok(dismissed.notice, 'dismissing must not delete the notice itself');

  const persisted = JSON.parse(fs.readFileSync(stateFile, 'utf8'));
  assert.equal(persisted.noticeDismissedForLaunch, false,
    'a dismissal written to disk would hide the notice for good');

  // Reopening the app is a new instance reading the same state file.
  const reopened = build();
  assert.ok(reopened.status().notice, 'the notice must be back on the next launch');
  assert.equal(reopened.status().noticeDismissedForLaunch, false);
});

test('the popup is already decided at startup, with no network at all', async (t) => {
  const { build, calls } = noticeHarness(t, { now: BEFORE_SUPPORT_ENDS });
  const first = build();
  await first.check(true);
  const callsAfterFirst = calls.length;

  // A later launch inside the throttle window must not hit GitHub, yet the
  // cached document still decides the popup - offline included.
  const second = build();
  const state = await second.check(false);
  assert.equal(calls.length, callsAfterFirst, 'a throttled launch makes no request');
  assert.ok(state.notice, 'the cached notice still produces the popup');
});

test('crossing the support end date escalates the cached notice on its own', async (t) => {
  const { build } = noticeHarness(t, { now: BEFORE_SUPPORT_ENDS });
  const first = build();
  await first.check(true);
  assert.equal(first.status().notice.level, 'warning');

  // Same document, same cache, 31 days later: no fetch, no new release.
  const later = noticeHarness(t, { now: AFTER_SUPPORT_ENDS });
  fs.copyFileSync(
    path.join(path.dirname(first.stateFile), 'update-state.json'),
    later.stateFile,
  );
  const escalated = later.build().status();
  assert.ok(escalated.notice, 'the notice survives the reopen');
  assert.equal(escalated.notice.level, 'end_of_support');
  assert.equal(escalated.notice.supportEnded, true);
});
