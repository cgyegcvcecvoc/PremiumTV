'use strict';

/**
 * Local channels (1.1.7, market-aware from 1.1.11).
 *
 * Turns a viewer's answer - a location fix, a ZIP code, a state or a city -
 * into the published local stations for their area. The app cannot guess a
 * market from an IP address, and a Mac's location fix is only accurate enough
 * to pick the *nearest published market*, so the viewer is asked and the answer
 * is stored on this machine. Nothing is sent anywhere.
 *
 * The bundled `local-channels.json` (meta.local_channels) carries the markets,
 * their positions, a ZIP prefix table and the station list. Pure list logic,
 * no DOM, so it can be unit tested in a VM like personal.js.
 */
window.PremiumLocalChannels = (function () {
  const SELECTION_KEY = 'premiumtv.local.v2';
  const ASKED_KEY = 'premiumtv.local.asked.v1';
  const EMPTY = { country: 'US', state: '', zip: '', city: '', source: '' };

  function normalizeSelection(selection) {
    const value = selection || {};
    return {
      country: String(value.country || 'US').trim().toUpperCase().slice(0, 2) || 'US',
      state: String(value.state || '').trim().toUpperCase().slice(0, 2),
      zip: String(value.zip || '').replace(/\D+/g, '').slice(0, 5),
      city: String(value.city || '').trim().slice(0, 40),
      source: String(value.source || '').trim().toLowerCase().slice(0, 12),
    };
  }

  function hasSelection(selection) {
    const value = normalizeSelection(selection);
    return Boolean(value.country && (value.state || value.zip || value.city));
  }

  function label(selection) {
    const value = normalizeSelection(selection);
    if (value.city && value.state) return `${value.city}, ${value.state}`;
    if (value.zip.length >= 3) return `ZIP ${value.zip}`;
    if (value.state) return value.state;
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
      storage.setItem(ASKED_KEY, '1');
    } catch (error) {
      // Private mode / full storage must never break the browser.
    }
    return value;
  }

  /** True once the viewer answered or explicitly skipped the location question. */
  function asked(storage) {
    try {
      return storage.getItem(ASKED_KEY) === '1';
    } catch (error) {
      return false;
    }
  }

  function markAsked(storage) {
    try {
      storage.setItem(ASKED_KEY, '1');
    } catch (error) {
      // Ignore: being asked twice is better than breaking the player.
    }
  }

  function markets(directory) {
    return Array.isArray(directory && directory.markets) ? directory.markets : [];
  }

  function states(directory) {
    return Array.isArray(directory && directory.states) ? directory.states : [];
  }

  function stationsOf(market) {
    return Array.isArray(market && market.stations) ? market.stations : [];
  }

  function zipEntry(zip, directory) {
    const digits = String(zip || '').replace(/\D+/g, '');
    if (digits.length < 3) return null;
    const prefix = digits.slice(0, 3);
    const table = Array.isArray(directory && directory.zip_prefixes) ? directory.zip_prefixes : [];
    const row = table.find((entry) => entry && entry.prefix === prefix);
    if (row) return row;
    const ranges = Array.isArray(directory && directory.zip_ranges) ? directory.zip_ranges : [];
    for (const range of ranges) {
      if (!Array.isArray(range) || range.length < 3) continue;
      if (prefix >= range[0] && prefix <= range[1]) {
        return { prefix, state: String(range[2] || ''), market: '' };
      }
    }
    return null;
  }

  /** USPS prefix -> state code. */
  function stateForZip(zip, directory) {
    const row = zipEntry(zip, directory);
    return row ? String(row.state || '') : '';
  }

  function distanceKm(lat1, lon1, lat2, lon2) {
    const radius = 6371;
    const rad = (value) => (value * Math.PI) / 180;
    const dPhi = rad(lat2 - lat1);
    const dLambda = rad(lon2 - lon1);
    const a = Math.sin(dPhi / 2) ** 2 +
      Math.cos(rad(lat1)) * Math.cos(rad(lat2)) * Math.sin(dLambda / 2) ** 2;
    return 2 * radius * Math.asin(Math.min(1, Math.sqrt(a)));
  }

  /** The published market nearest to a coarse fix, optionally inside a state. */
  /**
   * How far a location fix may be from a published market and still be called
   * the viewer's area (1.1.18).
   *
   * The library publishes local stations for around a hundred markets, so a
   * fix that falls nearest to a market 400 km away is not reporting the
   * viewer's market — it is reporting the absence of one. 1.1.11-1.1.17 said
   * "Location set to Philadelphia" to a viewer in Wilkes-Barre. The distance
   * now travels with the market so every screen can say how far the answer is,
   * and an answer beyond this line is offered instead of assumed.
   */
  const NEAREST_MARKET_MAX_KM = 120;

  /** `{ market, distanceKm }`, or null when nothing is published with a position. */
  function nearestMarketWithDistance(latitude, longitude, directory, state) {
    const wanted = String(state || '').toUpperCase();
    let best = null;
    let bestDistance = Infinity;
    for (const market of markets(directory)) {
      const lat = Number(market.latitude);
      const lon = Number(market.longitude);
      if (!Number.isFinite(lat) || !Number.isFinite(lon)) continue;
      if (wanted && String(market.state || '').toUpperCase() !== wanted) continue;
      const km = distanceKm(latitude, longitude, lat, lon);
      if (km < bestDistance) {
        bestDistance = km;
        best = market;
      }
    }
    return best ? { market: best, distanceKm: bestDistance } : null;
  }

  function nearestMarket(latitude, longitude, directory, state) {
    const hit = nearestMarketWithDistance(latitude, longitude, directory, state);
    return hit ? hit.market : null;
  }

  /** True when a fix is close enough to be treated as the viewer's own market. */
  function marketIsNear(distanceKm) {
    return Number.isFinite(distanceKm) && distanceKm <= NEAREST_MARKET_MAX_KM;
  }

  /** The state a coarse fix falls in, for the "no station near you" case. */
  function stateForLocation(latitude, longitude, directory) {
    const market = nearestMarket(latitude, longitude, directory);
    return market ? String(market.state || '') : '';
  }

  function marketForZip(zip, directory) {
    const row = zipEntry(zip, directory);
    if (!row) return null;
    if (row.market) {
      const market = markets(directory).find((entry) => entry.id === row.market);
      if (market) return market;
    }
    const latitude = Number(row.latitude);
    const longitude = Number(row.longitude);
    if (Number.isFinite(latitude) && Number.isFinite(longitude)) {
      return nearestMarket(latitude, longitude, directory, row.state);
    }
    return null;
  }

  /**
   * The markets a selection resolves to.
   *
   * A ZIP resolves to one market when the prefix table has one; a state lists
   * every market published there; a city narrows that list to the match.
   */
  function marketsFor(directory, selection) {
    const value = normalizeSelection(selection);
    const known = Array.isArray(directory && directory.countries) ? directory.countries : [];
    if (value.country && known.length && !known.some((row) => row.code === value.country)) {
      return [];
    }
    const zipMarket = value.zip ? marketForZip(value.zip, directory) : null;
    if (zipMarket && !value.city) return [zipMarket];
    const wantedState = (value.state || stateForZip(value.zip, directory)).toUpperCase();
    const wantedCity = value.city.toLowerCase();
    const out = markets(directory).filter((market) => {
      const marketState = String(market.state || '').toUpperCase();
      const marketCity = String(market.city || '').toLowerCase();
      if (wantedState && marketState !== wantedState) return false;
      if (wantedCity && marketCity !== wantedCity) return false;
      if (zipMarket && !wantedCity) return market.id === zipMarket.id;
      return true;
    });
    if (!out.length && zipMarket) return [zipMarket];
    return out;
  }

  function stationsFor(directory, selection) {
    return marketsFor(directory, selection).flatMap((market) => stationsOf(market));
  }

  /**
   * The loaded channels that belong to the selected market(s). Identity is the
   * published EPG id first and the stream URL second, so a backup feed still
   * resolves to its station.
   */
  function channelsFor(channels, directory, selection) {
    const stations = stationsFor(directory, selection);
    if (!stations.length) return [];
    const byId = new Map();
    const byUrl = new Map();
    for (const channel of channels || []) {
      if (!channel) continue;
      if (channel.id && !byId.has(channel.id)) byId.set(channel.id, channel);
      if (channel.url && !byUrl.has(channel.url)) byUrl.set(channel.url, channel);
    }
    const out = [];
    const seen = new Set();
    for (const station of stations) {
      const backups = Array.isArray(station.backup_urls) ? station.backup_urls : [];
      const channel = byId.get(station.channel_id) || byUrl.get(station.url) ||
        backups.map((url) => byUrl.get(url)).find(Boolean);
      if (channel && !seen.has(channel.url)) {
        seen.add(channel.url);
        out.push(channel);
      }
    }
    return out.sort((a, b) =>
      String(a.group || '').localeCompare(String(b.group || '')) ||
      String(a.name || '').localeCompare(String(b.name || '')));
  }

  function summary(directory, selection) {
    const value = normalizeSelection(selection);
    if (!directory) return 'Local-channel data is not bundled in this build.';
    const known = Array.isArray(directory.countries) ? directory.countries : [];
    if (value.country && known.length && !known.some((row) => row.code === value.country)) {
      return `Local stations are published for ${known.map((row) => row.name).join(', ')} so far.`;
    }
    if (value.zip.length >= 3 && !stateForZip(value.zip, directory)) {
      return 'That ZIP is not in the published US ZIP table. Check it, or enter a state instead.';
    }
    const resolved = marketsFor(directory, value);
    if (!resolved.length) {
      const state = value.state || stateForZip(value.zip, directory);
      if (value.city) return `No local station is published in ${value.city}, ${state || 'your area'} yet.`;
      if (state) return `No local stations are published in ${state} yet.`;
      return 'Enter a ZIP code, state or city to see your local stations.';
    }
    const count = resolved.reduce((total, market) => total + stationsOf(market).length, 0);
    const places = resolved.map((market) => `${market.city}, ${market.state}`).join(', ');
    return `${count} local station${count === 1 ? '' : 's'} in ${places}.`;
  }

  /** Every market city the viewer can type, as "City, ST" strings. */
  function cityChoices(directory) {
    return markets(directory)
      .map((market) => ({ city: market.city, state: market.state }))
      .sort((a, b) => a.state.localeCompare(b.state) || a.city.localeCompare(b.city));
  }

  return {
    SELECTION_KEY, ASKED_KEY, EMPTY,
    normalizeSelection, hasSelection, label, load, save, asked, markAsked,
    stateForZip, stateForLocation, nearestMarket, nearestMarketWithDistance,
    marketIsNear, NEAREST_MARKET_MAX_KM, marketForZip,
    marketsFor, stationsFor, channelsFor, summary, cityChoices,
  };
})();
