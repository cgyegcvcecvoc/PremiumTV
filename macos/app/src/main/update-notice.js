'use strict';

/**
 * The remote "please update" notice for the Mac app.
 *
 * This is the same policy the Android app implements in
 * `android/.../update/UpdateNotice.kt`, reading the same published document
 * (`app-update-notice.json` in the repository).  An installed app cannot be
 * given new code, so the message that tells somebody to update has to come from
 * a file the app was already built to fetch: the wording, the targeted version
 * range and the end-of-support date can all change later without a new release.
 *
 * The rules are total and forgiving on purpose.  Anything unreadable, disabled,
 * out of schema or out of version range resolves to `null`, and a `null` notice
 * never affects the app - a bad edit to the JSON can silence the popup, but it
 * cannot break playback.
 */

const { normalizeVersion, isNewer } = require('./update-policy');

const NOTICE_URL =
  'https://raw.githubusercontent.com/cgyegcvcecvoc/PremiumTV1/main/app-update-notice.json';
const DEFAULT_RELEASES_URL =
  'https://github.com/cgyegcvcecvoc/PremiumTV1/releases/latest';
/** The notice is tiny; a response above this is treated as unreadable. */
const MAX_NOTICE_BYTES = 64 * 1024;
const SUPPORTED_SCHEMA = 1;
const DAY_MS = 24 * 60 * 60 * 1000;

const ISO_RE = /^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2}))?)?(Z|[+-]\d{2}:?\d{2})?$/;

/**
 * Parse `2026-11-16T23:59:59Z` or `2026-11-16` into epoch millis.
 *
 * A bare date means "that whole day", so it ends one millisecond before the
 * next midnight UTC; a timestamp is used exactly as published.  Built by hand
 * rather than with `Date.parse` so the two supported shapes cannot be
 * reinterpreted by the host's locale or time zone.
 */
function parseInstant(value) {
  const text = String(value == null ? '' : value).trim();
  if (!text) return null;
  const match = ISO_RE.exec(text);
  if (!match) return null;
  const [, year, month, day, hour, minute, second] = match;
  const fields = {
    month: Number(month), day: Number(day),
    hour: Number(hour || 0), minute: Number(minute || 0), second: Number(second || 0),
  };
  // Impossible calendar dates are rejected rather than rolled forward, the same
  // rule the XMLTV parser applies: a typo in the published support date must
  // not silently move the sunset into another month.
  const daysInMonth = new Date(Date.UTC(Number(year), fields.month, 0)).getUTCDate();
  if (fields.month < 1 || fields.month > 12) return null;
  if (fields.day < 1 || fields.day > daysInMonth) return null;
  if (fields.hour > 23 || fields.minute > 59 || fields.second > 59) return null;
  const millis = Date.UTC(
    Number(year), fields.month - 1, fields.day,
    fields.hour, fields.minute, fields.second,
  );
  if (Number.isNaN(millis)) return null;
  const dateOnly = !hour && !minute && !second;
  return dateOnly ? millis + DAY_MS - 1 : millis;
}

/** "Nov 16, 2026" in UTC, so the date reads the same on every machine. */
function formatDay(epochMillis) {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const date = new Date(epochMillis);
  return `${months[date.getUTCMonth()]} ${date.getUTCDate()}, ${date.getUTCFullYear()}`;
}

function substitute(text, values) {
  let result = String(text == null ? '' : text);
  for (const [token, value] of Object.entries(values)) {
    result = result.split(token).join(value);
  }
  return result.trim();
}

function httpsUrl(value, fallback) {
  const text = String(value == null ? '' : value).trim();
  return text.startsWith('https://') ? text : fallback;
}

function targetsPlatform(rule, platform) {
  const platforms = Array.isArray(rule.platforms) ? rule.platforms : null;
  if (!platforms || platforms.length === 0) return true;
  return platforms.some((entry) => String(entry).trim().toLowerCase() === platform);
}

/**
 * True when `appVersion` is inside the rule's inclusive range.  A missing or
 * unreadable bound is open-ended, so a rule can target "everything up to 1.0.4"
 * without also spelling out a floor.
 */
function targetsVersion(rule, appVersion) {
  const current = normalizeVersion(appVersion);
  if (!current) return false;
  const min = normalizeVersion(rule.min_version);
  const max = normalizeVersion(rule.max_version);
  if (min && current !== min && !isNewer(current, min)) return false;
  if (max && isNewer(current, max)) return false;
  return true;
}

function levelOf(value) {
  if (value === 'end_of_support') return 'end_of_support';
  if (value === 'blocked') return 'blocked';
  if (value === 'critical') return 'critical';
  return 'warning';
}

/**
 * Resolve the notice this build should show.
 *
 * @param {object}   options
 * @param {?string}  options.body          the published document, as fetched
 * @param {string}   options.appVersion    this app's version ("1.0.4")
 * @param {?string}  options.newestVersion newest stable release found, if any
 * @param {string}  [options.platform]     "macos" (default) or "android"
 * @param {number}  [options.now]          current epoch millis
 * @returns {?object} the notice, or null when this build should not be nagged
 */
function selectNotice(options = {}) {
  const {
    body = null,
    appVersion = '',
    newestVersion = null,
    platform = 'macos',
    now = Date.now(),
  } = options;

  if (!body || !String(body).trim()) return null;
  let document;
  try {
    document = typeof body === 'string' ? JSON.parse(body) : body;
  } catch (error) {
    return null;
  }
  if (!document || typeof document !== 'object') return null;
  if (document.enabled !== true) return null;
  // A schema this build has never seen may mean a changed contract: show
  // nothing rather than guess at fields that moved.
  if (Number(document.schema) !== SUPPORTED_SCHEMA) return null;

  const supportEndsAtMillis = parseInstant(document.support_ends_utc);
  const supportEnded = supportEndsAtMillis != null && now >= supportEndsAtMillis;
  const releasesUrl = httpsUrl(document.releases_url, DEFAULT_RELEASES_URL);
  const rules = Array.isArray(document.rules) ? document.rules : null;
  if (!rules) return null;

  const values = {
    '{version}': appVersion,
    '{newest}': newestVersion && String(newestVersion).trim() ? String(newestVersion) : 'the newest release',
    '{support_ends}': supportEndsAtMillis != null
      ? formatDay(supportEndsAtMillis)
      : 'the published date',
  };

  for (const rule of rules) {
    if (!rule || typeof rule !== 'object') continue;
    if (!targetsPlatform(rule, platform)) continue;
    if (!targetsVersion(rule, appVersion)) continue;

    // Once the published support window has closed the same rule escalates: the
    // wording switches from "a surprise is waiting" to "this build is frozen".
    // Both texts ship in the JSON, so day 30 needs no new build and no edit.
    const active = (supportEnded && rule.after_support_ends && typeof rule.after_support_ends === 'object')
      ? { ...rule, ...rule.after_support_ends }
      : rule;
    const level = levelOf(active.level);

    // A build that is already the newest stable must never be told to update to
    // itself. That happened to 1.0.9 the moment the document started covering
    // every build below 1.1.0: the newest release was still 1.0.9, so the
    // warning would have nagged a current app. "blocked" rules are exempt on
    // purpose - a retired preview can be newer by name than the stable release.
    if (level !== 'blocked' && newestVersion
        && !isNewer(newestVersion, appVersion)) {
      continue;
    }

    const title = substitute(active.title, values);
    const message = substitute(active.message, values);
    if (!title && !message) continue;

    return {
      id: String(rule.id || 'notice'),
      level,
      title: title || 'A newer PremiumTV is available',
      message,
      surprise: substitute(active.surprise, values),
      actionLabel: substitute(active.action_label, values) || 'Update now',
      dismissLabel: substitute(active.dismiss_label, values) || 'Remind me next time',
      releasesUrl: httpsUrl(rule.releases_url, releasesUrl),
      supportEndsAtMillis: supportEndsAtMillis == null ? 0 : supportEndsAtMillis,
      supportEnded,
    };
  }

  return null;
}

module.exports = {
  NOTICE_URL,
  DEFAULT_RELEASES_URL,
  MAX_NOTICE_BYTES,
  SUPPORTED_SCHEMA,
  parseInstant,
  formatDay,
  targetsVersion,
  selectNotice,
};
