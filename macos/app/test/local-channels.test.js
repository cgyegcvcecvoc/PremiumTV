'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const renderer = path.join(__dirname, '..', 'src', 'renderer');

function loadLocal() {
  const window = {};
  vm.runInNewContext(fs.readFileSync(path.join(renderer, 'local-channels.js'), 'utf8'), { window });
  return window.PremiumLocalChannels;
}

/** Schema 2: markets carry their own position and stations. */
const directory = {
  schema: 2,
  countries: [{ code: 'US', name: 'United States', local_channels: true }],
  zip_ranges: [['150', '196', 'PA'], ['900', '961', 'CA']],
  zip_prefixes: [
    { prefix: '176', state: 'PA', market: 'USLNS', latitude: 40.04, longitude: -76.31 },
    { prefix: '150', state: 'PA', market: 'USPIT', latitude: 40.44, longitude: -80.0 },
    { prefix: '902', state: 'CA', market: 'USLAX', latitude: 34.03, longitude: -118.28 },
  ],
  markets: [
    {
      id: 'USLNS',
      city: 'Lancaster',
      state: 'PA',
      state_name: 'Pennsylvania',
      latitude: 40.0407,
      longitude: -76.3091,
      stations: [
        {
          callsign: 'WGAL',
          network: 'NBC',
          name: 'WGAL 8 (NBC) - Lancaster PA (720p)',
          city: 'Lancaster',
          channel_id: 'NBC.us@WGAL',
          url: 'https://example.test/wgal',
          backup_urls: [],
        },
      ],
    },
    {
      id: 'USPIT',
      city: 'Pittsburgh',
      state: 'PA',
      state_name: 'Pennsylvania',
      latitude: 40.4413,
      longitude: -80.0038,
      stations: [
        {
          callsign: 'WPXI',
          network: 'NBC',
          name: 'NBC WPXI (1080p)',
          city: 'Pittsburgh',
          channel_id: 'NBC.us@WPXI',
          url: 'https://example.test/wpxi',
          backup_urls: [],
        },
      ],
    },
    {
      id: 'USLAX',
      city: 'Los Angeles',
      state: 'CA',
      state_name: 'California',
      latitude: 34.0337,
      longitude: -118.2813,
      stations: [],
    },
    {
      // Dallas and Fort Worth are one metro published as two markets ~48 km
      // apart, so a fix in either is inside both at once.
      id: 'USDFW',
      city: 'Dallas',
      state: 'TX',
      state_name: 'Texas',
      latitude: 32.7767,
      longitude: -96.7970,
      stations: [],
    },
    {
      id: 'USFTW',
      city: 'Fort Worth',
      state: 'TX',
      state_name: 'Texas',
      latitude: 32.7555,
      longitude: -97.3308,
      stations: [],
    },
    {
      id: 'USGST',
      city: 'Saint Paul',
      state: 'MN',
      state_name: 'Minnesota',
      latitude: 44.9537,
      longitude: -93.0900,
      stations: [],
    },
  ],
  states: [
    { code: 'CA', name: 'California', latitude: 37.2, longitude: -119.3, markets: ['USLAX'] },
    { code: 'PA', name: 'Pennsylvania', latitude: 40.9, longitude: -77.8, markets: ['USLNS', 'USPIT'] },
  ],
  station_count: 2,
};

const wgal = { id: 'NBC.us@WGAL', name: 'WGAL 8 (NBC) - Lancaster PA', url: 'https://example.test/wgal', group: 'NBC' };
const wpxi = { id: 'NBC.us@WPXI', name: 'NBC WPXI', url: 'https://example.test/wpxi', group: 'NBC' };
const other = { id: 'CNN.us', name: 'CNN', url: 'https://example.test/cnn', group: 'News' };

test('a ZIP resolves to its market, not to the whole state', () => {
  const local = loadLocal();
  assert.equal(local.stateForZip('17603', directory), 'PA');
  assert.equal(local.marketForZip('17603', directory).id, 'USLNS');
  const selection = { zip: '17603' };
  assert.equal(local.channelsFor([wgal, wpxi, other], directory, selection).length, 1);
  assert.match(local.summary(directory, selection), /1 local station in Lancaster, PA/);
});

test('a state works when location is declined, and lists every market there', () => {
  const local = loadLocal();
  const channels = local.channelsFor([wgal, wpxi, other], directory, { state: 'PA' });
  assert.deepEqual([...channels].map((channel) => channel.name).sort(),
    ['NBC WPXI', 'WGAL 8 (NBC) - Lancaster PA']);
  assert.match(local.summary(directory, { state: 'PA' }), /2 local stations in Lancaster, PA, Pittsburgh, PA/);
});

test('a typed city narrows the state to one market', () => {
  const local = loadLocal();
  const selection = { state: 'PA', city: 'Pittsburgh' };
  assert.deepEqual([...local.marketsFor(directory, selection)].map((market) => market.id), ['USPIT']);
  assert.equal(local.channelsFor([wgal, wpxi], directory, selection)[0].url, 'https://example.test/wpxi');
});

test('a country outside the published list is honest instead of empty', () => {
  const local = loadLocal();
  assert.equal(local.channelsFor([wgal], directory, { country: 'GB' }).length, 0);
  assert.match(local.summary(directory, { country: 'GB' }), /United States/);
});

test('a coarse location fix picks the nearest published market', () => {
  const local = loadLocal();
  assert.equal(local.nearestMarket(40.04, -76.3, directory).id, 'USLNS');
  assert.equal(local.nearestMarket(40.5, -80.1, directory).id, 'USPIT');
  // 600 km away from both Pennsylvania markets: still the nearest, not null.
  assert.equal(local.stateForLocation(35.0, -80.0, directory), 'PA');
});

test('a fix inside a metro cluster reports every market in reach, nearest first', () => {
  const local = loadLocal();
  const area = local.nearbyMarketsWithDistance(32.7555, -97.3308, directory);
  assert.deepEqual(area.map((hit) => hit.market.id), ['USFTW', 'USDFW']);
  assert.ok(area[0].distanceKm < area[1].distanceKm);
  assert.ok(local.marketIsNear(area[1].distanceKm), 'Dallas is inside the radius');
  // Nothing published near the fix is an empty area, not the nearest thing.
  assert.deepEqual(local.nearbyMarketsWithDistance(0, 0, directory), []);
  assert.ok(local.nearbyMarketsWithDistance(0, 0, directory, null, 20000).length > 1);
  // A state filter narrows the same area.
  assert.deepEqual(local.nearbyMarketsWithDistance(32.7555, -97.3308, directory, 'MN'), []);
});

test('a typed city matches the place, not the spelling', () => {
  const local = loadLocal();
  const matches = (city) =>
    [...local.marketsFor(directory, { state: 'MN', city })].map((market) => market.id);
  assert.deepEqual(matches('St. Paul'), ['USGST']);
  assert.deepEqual(matches('saint paul'), ['USGST']);
  assert.equal(local.normalizePlace('Wilkes-Barre'), local.normalizePlace('Wilkes Barre'));
  assert.equal(local.normalizePlace('München'), 'munchen');
  assert.equal(local.normalizePlace('   '), '');
});

test('a state with no published station says so', () => {
  const local = loadLocal();
  const selection = { state: 'WY' };
  assert.equal(local.channelsFor([wgal], directory, selection).length, 0);
  assert.match(local.summary(directory, selection), /No local stations are published in WY yet/);
});

test('no answer is stored as empty and never breaks on corrupt storage', () => {
  const local = loadLocal();
  const storage = { getItem: () => '{nope', setItem: () => {} };
  assert.deepEqual({ ...local.load(storage) }, { country: 'US', state: '', zip: '', city: '', source: '' });
  assert.equal(local.hasSelection({}), false);
  assert.equal(local.label({ zip: '17603' }), 'ZIP 17603');
});

test('the location question is remembered as answered', () => {
  const local = loadLocal();
  const store = new Map();
  const storage = { getItem: (key) => (store.has(key) ? store.get(key) : null), setItem: (key, value) => store.set(key, value) };
  assert.equal(local.asked(storage), false);
  local.markAsked(storage);
  assert.equal(local.asked(storage), true);
  const saved = local.save(storage, { zip: '17603', source: 'zip' });
  assert.equal(saved.source, 'zip');
  assert.equal(local.load(storage).zip, '17603');
});
