'use strict';

/**
 * Local channels (1.1.7): turn a viewer's location into the published local
 * stations for their area.
 *
 * The app cannot guess a market from an IP address, and a Mac's location fix
 * only has to be good enough to pick a state. So the viewer is asked: use
 * location, or type a ZIP, state or country. The answer is stored on this
 * machine, the bundled `local-channels.json` (meta.local_channels) carries the
 * station list, and nothing is sent anywhere.
 *
 * Pure list logic, no DOM, so it can be unit tested in a VM like personal.js.
 */
window.PremiumLocalChannels = (function () {
  const SELECTION_KEY = 'premiumtv.local.v1';
  const EMPTY = { country: 'US', state: '', zip: '', city: '' };

  function normalizeSelection(selection) {
    const value = selection || {};
    return {
      country: String(value.country || 'US').trim().toUpperCase().slice(0, 2) || 'US',
      state: String(value.state || '').trim().toUpperCase().slice(0, 2),
      zip: String(value.zip || '').replace(/\D+/g, '').slice(0, 5),
      city: String(value.city || '').trim().slice(0, 40),
    };
  }

  function hasSelection(selection) {
    const value = normalizeSelection(selection);
    return Boolean(value.country && (value.state || value.zip || value.city));
  }

  function label(selection) {
    const value = normalizeSelection(selection);
    if (value.city && value.state) return `${value.city}, ${value.state}`;
    if (value.state) return value.state;
    if (value.zip) return `ZIP ${value.zip}`;
    if (value.country && value.country !== 'US') return value.country;
    return 'Not set';
  }

  function load(storage) {
    try {
      const parsed = JSON.parse(storage.getItem(SELECTION_KEY) || 'null');
      return parsed ? normalizeSelection(parsed) : { ...EMPTY };
    } catch (error) {
      return { ...EMPTY };
    }
  }

  function save(storage, selection) {
    const value = normalizeSelection(selection);
    try {
      storage.setItem(SELECTION_KEY, JSON.stringify(value));
    } catch (error) {
      // Private mode / full storage must never break the browser.
    }
    return value;
  }

  function states(directory) {
    return Array.isArray(directory && directory.states) ? directory.states : [];
  }

  /** USPS first-three-digit prefix range -> state code. */
  function stateForZip(zip, directory) {
    const digits = String(zip || '').replace(/\D+/g, '');
    if (digits.length < 3) return '';
    const prefix = digits.slice(0, 3);
    const ranges = Array.isArray(directory && directory.zip_ranges) ? directory.zip_ranges : [];
    for (const range of ranges) {
      if (!Array.isArray(range) || range.length < 3) continue;
      if (prefix >= range[0] && prefix <= range[1]) return String(range[2] || '');
    }
    return '';
  }

  /** The nearest state with a published station, from a coarse location fix. */
  function stateForLocation(latitude, longitude, directory) {
    let best = '';
    let bestDistance = Infinity;
    for (const state of states(directory)) {
      const lat = Number(state.latitude);
      const lon = Number(state.longitude);
      if (!Number.isFinite(lat) || !Number.isFinite(lon)) continue;
      const distance = (lat - latitude) ** 2 + (lon - longitude) ** 2;
      if (distance < bestDistance) {
        bestDistance = distance;
        best = String(state.code || '');
      }
    }
    return best;
  }

  function marketsFor(directory, selection) {
    const value = normalizeSelection(selection);
    if (value.country !== 'US') return [];
    const wanted = value.state || stateForZip(value.zip, directory);
    if (!wanted) return [];
    const wantedCity = value.city.toLowerCase();
    const out = [];
    for (const state of states(directory)) {
      if (String(state.code || '').toUpperCase() !== wanted) continue;
      for (const market of Array.isArray(state.markets) ? state.markets : []) {
        if (wantedCity && !String(market.city || '').toLowerCase().includes(wantedCity)) continue;
        const stations = Array.isArray(market.stations) ? market.stations : [];
        if (stations.length) {
          out.push({ city: market.city || '', state: wanted, stateName: state.name || wanted, stations });
        }
      }
    }
    return out;
  }

  /**
   * The loaded channels that belong to the selected market(s). Identity is the
   * published EPG id first and the stream URL second, so a backup feed still
   * resolves to its station.
   */
  function channelsFor(channels, directory, selection) {
    const markets = marketsFor(directory, selection);
    if (!markets.length) return [];
    const byId = new Map();
    const byUrl = new Map();
    for (const channel of channels || []) {
      if (!channel) continue;
      if (channel.id && !byId.has(channel.id)) byId.set(channel.id, channel);
      if (channel.url && !byUrl.has(channel.url)) byUrl.set(channel.url, channel);
    }
    const out = [];
    const seen = new Set();
    for (const market of markets) {
      for (const station of market.stations) {
        const backups = Array.isArray(station.backup_urls) ? station.backup_urls : [];
        const channel = byId.get(station.channel_id) || byUrl.get(station.url) ||
          backups.map((url) => byUrl.get(url)).find(Boolean);
        if (channel && !seen.has(channel.url)) {
          seen.add(channel.url);
          out.push(channel);
        }
      }
    }
    return out.sort((a, b) =>
      String(a.group || '').localeCompare(String(b.group || '')) ||
      String(a.name || '').localeCompare(String(b.name || '')));
  }

  function summary(directory, selection) {
    const value = normalizeSelection(selection);
    if (!directory) return 'Local-channel data is not bundled in this build.';
    if (value.country !== 'US') return 'Local stations are published for the United States only so far.';
    const state = value.state || stateForZip(value.zip, directory);
    if (!state) return 'Enter a ZIP or state to see your local stations.';
    const markets = marketsFor(directory, value);
    const count = markets.reduce((total, market) => total + market.stations.length, 0);
    if (!count) {
      return `No local stations are published for ${value.city || state} yet.`;
    }
    return `${count} local station${count === 1 ? '' : 's'} in ${markets.map((m) => m.city).join(', ')}.`;
  }

  return {
    SELECTION_KEY, EMPTY,
    normalizeSelection, hasSelection, label, load, save,
    stateForZip, stateForLocation, marketsFor, channelsFor, summary,
  };
})();
