'use strict';

/**
 * The viewer's own shelves: Recently watched and Favorites (1.0.6).
 *
 * Pure list logic plus localStorage persistence, kept in its own file (like
 * live-events.js) so it can be unit tested in a VM without the renderer.
 * A channel is keyed by its stream URL: backup feeds share an EPG id, but the
 * URL is the one identity every feed in the playlist actually has.
 */
window.PremiumPersonal = (function () {
  const RECENTS_KEY = 'premiumtv.recents.v1';
  const FAVORITES_KEY = 'premiumtv.favorites.v1';
  const MAX_RECENTS = 30;

  function keyFor(channel) {
    return channel ? String(channel.url || channel.id || '') : '';
  }

  /** Newest first, deduplicated, capped. Opening a channel moves it to front. */
  function recordRecent(keys, key, limit) {
    if (!key) return (keys || []).slice();
    const rest = (keys || []).filter((item) => item !== key);
    return [key].concat(rest).slice(0, limit || MAX_RECENTS);
  }

  function toggleFavorite(keys, key) {
    if (!key) return (keys || []).slice();
    return (keys || []).includes(key)
      ? (keys || []).filter((item) => item !== key)
      : [key].concat(keys || []);
  }

  function isFavorite(keys, key) {
    return Boolean(key) && (keys || []).includes(key);
  }

  /** Keys -> channels in key order; channels that left the playlist drop out. */
  function resolve(keys, channels) {
    const byKey = new Map();
    for (const channel of channels || []) {
      const key = keyFor(channel);
      if (key && !byKey.has(key)) byKey.set(key, channel);
    }
    const out = [];
    for (const key of keys || []) {
      const channel = byKey.get(key);
      if (channel) out.push(channel);
    }
    return out;
  }

  /** Manual server switching wraps around; auto-fallback only walks forward. */
  function nextServerIndex(current, count, delta) {
    if (!count || count < 1) return 0;
    return (((current + delta) % count) + count) % count;
  }

  function load(storage, storageKey) {
    try {
      const parsed = JSON.parse(storage.getItem(storageKey) || '[]');
      return Array.isArray(parsed) ? parsed.filter((item) => typeof item === 'string' && item) : [];
    } catch (error) {
      return [];
    }
  }

  function save(storage, storageKey, keys) {
    try {
      storage.setItem(storageKey, JSON.stringify(keys || []));
    } catch (error) {
      // Private-mode / full storage must never break playback.
    }
  }

  return {
    RECENTS_KEY, FAVORITES_KEY, MAX_RECENTS,
    keyFor, recordRecent, toggleFavorite, isFavorite, resolve, nextServerIndex, load, save,
  };
})();
