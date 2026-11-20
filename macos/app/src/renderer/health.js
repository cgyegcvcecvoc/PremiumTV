/**
 * PremiumTV 1.1.0 — dead-feed memory for the macOS app.
 *
 * The player already walks a channel's servers when a feed fails. When every
 * feed has failed there is no point offering that channel again until the
 * published playlist changes, so the URL is remembered here for seven days and
 * the browser filters it out. Recordings expire so a returning upstream link
 * gets another chance, and Settings has a one-press restore.
 *
 * Pure storage helpers: the renderer passes window.localStorage in, the tests
 * pass a plain object, so nothing here needs Electron or a DOM.
 */
(function (root) {
  'use strict';

  const KEY = 'premiumtv.deadFeeds.v1';
  const TTL_MS = 7 * 24 * 60 * 60 * 1000;

  function prune(entries, now) {
    const moment = Number(now) || Date.now();
    return (Array.isArray(entries) ? entries : []).filter(
      (entry) => entry && entry.url && moment - Number(entry.at) < TTL_MS,
    );
  }

  /** Reads the stored failures, quietly recovering from anything corrupt. */
  function entries(storage, now) {
    if (!storage) return [];
    let parsed = [];
    try {
      parsed = JSON.parse(storage.getItem(KEY) || '[]');
    } catch (error) {
      parsed = [];
    }
    if (!Array.isArray(parsed)) return [];
    return prune(parsed, now);
  }

  /** The URL set the browser filters with. */
  function load(storage, now) {
    return new Set(entries(storage, now).map((entry) => entry.url));
  }

  /** Remembers one failed feed; a repeat failure refreshes its timestamp. */
  function record(storage, url, now) {
    if (!storage || !url) return load(storage, now);
    const moment = Number(now) || Date.now();
    const kept = entries(storage, moment).filter((entry) => entry.url !== url);
    const next = [{ url, at: moment }, ...kept];
    try {
      storage.setItem(KEY, JSON.stringify(next));
    } catch (error) {
      /* A full or disabled storage must never break playback. */
    }
    return load(storage, moment);
  }

  /** Forget one recovered feed without resetting other failures. */
  function forget(storage, url, now) {
    if (!storage || !url) return load(storage, now);
    const kept = entries(storage, now).filter((entry) => entry.url !== url);
    try {
      storage.setItem(KEY, JSON.stringify(kept));
    } catch (error) { /* storage may be unavailable */ }
    return new Set(kept.map((entry) => entry.url));
  }

  /**
   * Remember every feed a channel exhausted. macOS used to record only the
   * *last* server, so a channel whose primary feed was dead kept leading with
   * it on the next open. Android and the web player record the whole walk; this
   * shared helper makes all three agree.
   */
  function recordMany(storage, urls, now) {
    if (!storage) return new Set();
    const moment = Number(now) || Date.now();
    const failed = new Set((Array.isArray(urls) ? urls : [])
      .filter((url) => typeof url === 'string' && url));
    if (!failed.size) return load(storage, moment);
    const kept = entries(storage, moment).filter((entry) => !failed.has(entry.url));
    const next = [...failed].map((url) => ({ url, at: moment })).concat(kept);
    try {
      storage.setItem(KEY, JSON.stringify(next));
    } catch (error) {
      /* a full or disabled storage must never break playback */
    }
    return load(storage, moment);
  }

  /**
   * Try a channel's feeds with no remembered failure first, preserving the
   * published order inside each group. Mirrors Android's healthyServersFirst():
   * a feed that failed last night should be the backup, not the first try.
   */
  function healthyServersFirst(servers, deadUrls) {
    const list = Array.isArray(servers) ? servers : [];
    if (!deadUrls || !deadUrls.size) return list.slice();
    const healthy = list.filter((server) => server && !deadUrls.has(server.url));
    const known = list.filter((server) => server && deadUrls.has(server.url));
    return healthy.concat(known);
  }

  function clear(storage) {
    try {
      storage.removeItem(KEY);
    } catch (error) {
      /* ignore */
    }
    return new Set();
  }

  /** Channels whose own feed is remembered dead drop out of the browser. */
  function filterChannels(channels, deadUrls) {
    if (!deadUrls || !deadUrls.size) return channels || [];
    return (channels || []).filter((channel) => !deadUrls.has(channel.url));
  }

  root.PremiumHealth = {
    KEY, TTL_MS, prune, load, record, recordMany, forget, clear, filterChannels,
    healthyServersFirst,
  };
})(typeof window !== 'undefined' ? window : globalThis);
