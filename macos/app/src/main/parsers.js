'use strict';

/**
 * Playlist and guide parsers.
 *
 * These mirror android/tools/build_bundle.py, which is what produced the
 * bundle inside the app. They exist so a downloaded refresh can be turned into
 * exactly the same shape as the bundled copy: a refresh that succeeds and a
 * first launch must show the same channels in the same order.
 *
 * Pure functions, no Electron, no filesystem - test/parsers.test.js runs them
 * against real repository files.
 */

const { XMLParser } = require('fast-xml-parser');

const ATTR_RE = /([\w-]+)="([^"]*)"/g;
// Decorative prefixes/suffixes that only add noise on screen.
const NOISE_PREFIX_RE = /^[\s\u2605\u2606\u2b50\u2728\u2022\u25b6\-\u2013]+/u;

const MAX_PLAYLIST_CHARS = 16 * 1024 * 1024;
const MAX_GUIDE_CHARS = 80 * 1024 * 1024;

function parseAttrs(line) {
  const attrs = {};
  let match;
  ATTR_RE.lastIndex = 0;
  while ((match = ATTR_RE.exec(line)) !== null) attrs[match[1]] = match[2];
  return attrs;
}

/** Trim decorative noise but keep country flags and quality markers. */
function cleanName(raw) {
  const name = (raw || '').replace(NOISE_PREFIX_RE, '');
  const collapsed = name.replace(/\s{2,}/g, ' ').trim();
  return collapsed || (raw || '').trim() || 'Unknown channel';
}

/**
 * Parse an M3U playlist.
 *
 * Handles the tags this repository actually writes: #EXTINF with tvg-*
 * attributes, #EXTVLCOPT / #KODIPROP stream headers (referrer, user-agent,
 * origin) and the x-tvg-url guide list on the #EXTM3U header line.
 */
function parseM3u(text) {
  if (typeof text !== 'string') throw new TypeError('playlist must be a string');
  if (text.length > MAX_PLAYLIST_CHARS) throw new Error('playlist is larger than the 16 MB the app accepts');

  const channels = [];
  let guideUrl = '';
  let pending = null;
  let pendingOpts = {};

  const lines = text.split(/\r?\n/);
  for (const rawLine of lines) {
    const line = rawLine.replace(/\r$/, '');
    if (!line.trim()) continue;

    if (line.startsWith('#EXTM3U')) {
      const head = parseAttrs(line);
      if (head['x-tvg-url']) {
        const first = head['x-tvg-url'].split(',').map((u) => u.trim()).find(Boolean);
        if (first) guideUrl = first;
      }
      continue;
    }

    if (line.startsWith('#EXTINF')) {
      // Any stream options seen after the previous entry are dropped.
      pendingOpts = {};
      const attrs = parseAttrs(line);
      const name = line.includes(',') ? line.slice(line.lastIndexOf(',') + 1).trim() : (attrs['tvg-name'] || '').trim();
      pending = {
        id: (attrs['tvg-id'] || '').trim(),
        name: cleanName(name),
        logo: (attrs['tvg-logo'] || '').trim(),
        group: (attrs['group-title'] || 'Other').trim() || 'Other',
        country: (attrs['tvg-country'] || '').trim().toUpperCase(),
        chno: (attrs['tvg-chno'] || '').trim(),
        ua: (attrs['http-user-agent'] || '').trim(),
        referrer: (attrs['http-referrer'] || '').trim(),
      };
      continue;
    }

    let opt = null;
    if (line.startsWith('#EXTVLCOPT:')) opt = line.slice('#EXTVLCOPT:'.length);
    else if (line.startsWith('#KODIPROP:')) opt = line.slice('#KODIPROP:'.length);
    if (opt !== null) {
      if (!pending) continue;
      const eq = opt.indexOf('=');
      const key = (eq === -1 ? opt : opt.slice(0, eq)).trim().toLowerCase();
      const value = (eq === -1 ? '' : opt.slice(eq + 1)).trim();
      if (key === 'http-referrer' || key === 'referer') pendingOpts.referrer = value;
      else if (key === 'http-user-agent' || key === 'user-agent') pendingOpts.ua = value;
      else if (key === 'http-origin' || key === 'origin') pendingOpts.origin = value;
      continue;
    }

    if (line.startsWith('#')) continue;

    const url = line.trim();
    if (!url || url.startsWith('#')) continue;
    if (pending === null) {
      // A bare URL with no #EXTINF: keep it, named after the URL.
      pending = {
        id: '',
        name: cleanName(url.split('/').pop() || url),
        logo: '',
        group: 'Other',
        country: '',
        chno: '',
        ua: '',
        referrer: '',
      };
    }
    pending.url = url;
    if (!('origin' in pending)) pending.origin = '';
    Object.assign(pending, pendingOpts);
    pendingOpts = {};
    if (!pending.id) pending.id = slugify(pending.name);
    channels.push(pending);
    pending = null;
  }

  return { channels, guideUrl };
}

function slugify(name) {
  return (name || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '.')
    .replace(/^\.+|\.+$/g, '');
}

/** '20261011043000 +0000' -> epoch seconds (UTC). 0 when unparseable. */
function xmltvTime(value) {
  const text = (value || '').trim();
  if (!text) return 0;
  const match = text.match(/^(\d{14})\s*([+-]\d{4})?/);
  if (!match) return 0;
  const [, stamp, offset] = match;
  const year = Number(stamp.slice(0, 4));
  const month = Number(stamp.slice(4, 6));
  const day = Number(stamp.slice(6, 8));
  const hour = Number(stamp.slice(8, 10));
  const minute = Number(stamp.slice(10, 12));
  const second = Number(stamp.slice(12, 14));
  if (month < 1 || month > 12 || day < 1 || day > 31 || hour > 23 || minute > 59 || second > 60) return 0;
  const asUtc = Date.UTC(year, month - 1, day, hour, minute, second);
  if (Number.isNaN(asUtc)) return 0;
  const sign = (offset || '+0000')[0] === '-' ? -1 : 1;
  const offHours = Number((offset || '+0000').slice(1, 3));
  const offMinutes = Number((offset || '+0000').slice(3, 5));
  return Math.floor((asUtc - sign * (offHours * 60 + offMinutes) * 60 * 1000) / 1000);
}

function textOf(node, key) {
  if (!node || node[key] === undefined || node[key] === null) return '';
  const value = node[key];
  if (typeof value === 'object') return collapse(value['#text']);
  return collapse(String(value));
}

function collapse(value) {
  return (value || '').replace(/\s+/g, ' ').trim();
}

function listOf(value) {
  if (value === undefined || value === null) return [];
  return Array.isArray(value) ? value : [value];
}

/**
 * Parse an XMLTV guide into programme records.
 *
 * Same output shape as build_bundle.py's epg.jsonl: {c, s, e, t, d, g, i, ep},
 * with start/stop as epoch seconds. Listings that finished more than six hours
 * ago are dropped, matching the bundle.
 */
function parseXmltv(text, options = {}) {
  if (typeof text !== 'string') throw new TypeError('guide must be a string');
  if (text.length > MAX_GUIDE_CHARS) throw new Error('guide is larger than the 80 MB the app accepts');
  const knownIds = options.knownIds instanceof Set ? options.knownIds : null;
  const nowSeconds = Number.isFinite(options.nowSeconds)
    ? options.nowSeconds
    : Math.floor(Date.now() / 1000);

  const parser = new XMLParser({
    ignoreAttributes: false,
    attributeNamePrefix: '@_',
    parseAttributeValue: false,
    parseTagValue: false,
    trimValues: false,
    isArray: (name) => name === 'programme' || name === 'channel' || name === 'category',
  });

  let document;
  try {
    document = parser.parse(text);
  } catch (error) {
    throw new Error(`the guide is not valid XML (${error.message})`);
  }

  const root = document && (document.tv || document);
  const programmes = [];
  for (const item of listOf(root && root.programme)) {
    if (!item || typeof item !== 'object') continue;
    const attrs = {};
    for (const key of Object.keys(item)) {
      if (key.startsWith('@_')) attrs[key.slice(2)] = item[key];
    }
    const channel = (attrs.channel || '').trim();
    const start = xmltvTime(attrs.start || '');
    if (!channel || !start) continue;
    const stop = xmltvTime(attrs.stop || '') || start + 1800;
    if (knownIds && !knownIds.has(channel)) continue;
    if (stop <= nowSeconds - 6 * 3600) continue;

    const categories = listOf(item.category)
      .map((c) => (typeof c === 'object' ? textOf(c, '#text') : String(c || '')))
      .map(collapse)
      .filter(Boolean);
    const icon = item.icon;
    programmes.push({
      c: channel,
      s: start,
      e: stop,
      t: textOf(item, 'title') || '(no title)',
      d: textOf(item, 'desc'),
      g: categories.join('; '),
      i: (icon && typeof icon === 'object' && icon['@_src']) || '',
      ep: collapse(textOf(item, 'sub-title')),
    });
  }

  programmes.sort((a, b) => (a.c === b.c ? a.s - b.s : a.c < b.c ? -1 : 1));
  return programmes;
}

/**
 * Category order: the published order from categories/index.json first, then
 * every remaining group by size. Same rule as build_bundle.py.
 */
function orderGroups(channels, publishedOrder = []) {
  const counts = new Map();
  for (const channel of channels) counts.set(channel.group, (counts.get(channel.group) || 0) + 1);

  const ordered = [];
  for (const name of publishedOrder) {
    if (counts.has(name)) {
      ordered.push({ name, count: counts.get(name) });
      counts.delete(name);
    }
  }
  const rest = [...counts.entries()]
    .sort((a, b) => (b[1] - a[1] || a[0].toLowerCase().localeCompare(b[0].toLowerCase())))
    .map(([name, count]) => ({ name, count }));
  return ordered.concat(rest);
}

module.exports = {
  parseM3u,
  parseXmltv,
  orderGroups,
  xmltvTime,
  cleanName,
  slugify,
  MAX_PLAYLIST_CHARS,
  MAX_GUIDE_CHARS,
};
