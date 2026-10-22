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

  root.PremiumHealth = { KEY, TTL_MS, prune, load, record, clear, filterChannels };
})(typeof window !== 'undefined' ? window : globalThis);
