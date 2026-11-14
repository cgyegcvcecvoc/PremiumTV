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

const directory = {
  schema: 1,
  zip_ranges: [['150', '196', 'PA'], ['900', '961', 'CA']],
  states: [
    {
      code: 'PA',
      name: 'Pennsylvania',
      latitude: 40.9,
      longitude: -77.8,
      markets: [
        {
          city: 'Lancaster',
          stations: [
            {
              callsign: 'WGAL',
              network: 'NBC',
              name: 'WGAL 8 (NBC) - Lancaster PA (720p)',
              channel_id: 'NBC.us@WGAL',
              url: 'https://example.test/wgal',
              backup_urls: [],
            },
          ],
        },
      ],
    },
  ],
};

const wgal = { id: 'NBC.us@WGAL', name: 'WGAL 8 (NBC) - Lancaster PA', url: 'https://example.test/wgal', group: 'NBC' };
const other = { id: 'CNN.us', name: 'CNN', url: 'https://example.test/cnn', group: 'News' };

test('a ZIP picks the state and the published station for it', () => {
  const local = loadLocal();
  assert.equal(local.stateForZip('17603', directory), 'PA');
  const selection = { zip: '17603' };
  assert.equal(local.channelsFor([wgal, other], directory, selection).length, 1);
  assert.match(local.summary(directory, selection), /1 local station in Lancaster/);
});

test('a state works when location is declined, and a country outside the US is honest', () => {
  const local = loadLocal();
  assert.equal(local.channelsFor([wgal], directory, { state: 'PA' })[0].name, 'WGAL 8 (NBC) - Lancaster PA');
  assert.equal(local.channelsFor([wgal], directory, { country: 'GB' }).length, 0);
  assert.match(local.summary(directory, { country: 'GB' }), /United States only/);
});

test('a coarse location fix picks the nearest state we publish', () => {
  const local = loadLocal();
  assert.equal(local.stateForLocation(40.04, -76.3, directory), 'PA');
  assert.equal(local.stateForLocation(35.0, -80.0, directory), 'PA');
});

test('no answer is stored as empty and never breaks on corrupt storage', () => {
  const local = loadLocal();
  const storage = { getItem: () => '{nope', setItem: () => {} };
  assert.deepEqual({ ...local.load(storage) }, { country: 'US', state: '', zip: '', city: '' });
  assert.equal(local.hasSelection({}), false);
  assert.equal(local.label({ zip: '17603' }), 'ZIP 17603');
});
