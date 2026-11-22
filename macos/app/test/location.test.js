'use strict';

/**
 * The location contract, 1.1.18.
 *
 * Local channels are only as good as the ask behind them, and for eleven
 * releases the ask was invisible: macOS refuses a geolocation request from a
 * bundle with no usage description, and the app printed "Location was declined"
 * for something it had never asked. These tests hold the three things that make
 * the difference — the bundle key, the permission handler, and an answer that
 * names the failure it actually saw — plus the market-distance rule that stops
 * a fix in Wilkes-Barre being saved as Philadelphia.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const appRoot = path.join(__dirname, '..');
const repoRoot = path.join(appRoot, '..', '..');
const renderer = path.join(__dirname, '..', 'src', 'renderer');
const main = path.join(__dirname, '..', 'src', 'main');

const read = (...parts) => fs.readFileSync(path.join(...parts), 'utf8');

// ---------------------------------------------------------------- the bundle

test('the Mac bundle tells macOS why it wants a location', () => {
  const builder = read(appRoot, 'electron-builder.yml');
  const extendInfo = builder.slice(builder.indexOf('extendInfo:'));
  // Without one of these keys the system prompt never appears, so the viewer
  // sees a button that does nothing. This is the root cause of "the Mac never
  // asks for my location".
  assert.match(extendInfo, /^ {4}NSLocationUsageDescription: ".*"$/m,
    'NSLocationUsageDescription must be a non-empty string in extendInfo');
  assert.match(extendInfo, /^ {4}NSLocationWhenInUseUsageDescription: ".*"$/m);
  // Approximate only: the feature needs a market, never an address.
  assert.match(extendInfo, /^ {4}NSLocationDefaultAccuracyReduced: true$/m);
  // One codebase, two desktops: the About panel must not promise an
  // Apple-only step to a Linux install, and the local panel must not say
  // "this Mac" at all.
  const about = read(renderer, 'app.js');
  assert.match(about, /appInfo\.platform === 'darwin'[\s\S]{0,240}The Linux build is unsigned/);
  const at = about.indexOf('Local stations such as WGAL');
  assert.ok(at > 0, 'the Local channels panel copy moved');
  const settings = about.slice(at, at + 600);
  assert.ok(!/this Mac/.test(settings),
    'the Local channels copy must not say "this Mac" in a Linux build');
  const sheet = read(renderer, 'index.html');
  assert.match(sheet, /id="local-setup-settings"[^>]*hidden/);
});

test('the main process admits geolocation from the app origin and nothing else', () => {
  const source = read(main, 'main.js');
  assert.match(source, /setPermissionRequestHandler/);
  assert.match(source, /permission !== 'geolocation'[\s\S]{0,120}callback\(false\)/);
  assert.match(source, /callback\(fromApp\)/);
  assert.match(source, /setPermissionCheckHandler/);
  // The handler must be able to say why a request failed, so the renderer is
  // given the bundle facts rather than a bare error code.
  assert.match(source, /ipcMain\.handle\('ptv:location-context'/);
  assert.match(source, /hasLocationUsageDescription/);
  assert.match(source, /NSLocation\(Usage\|WhenInUseUsage\)Description/);
  // The escape hatch for an answer the OS remembers.
  assert.match(source, /ipcMain\.handle\('ptv:open-location-settings'/);
  assert.match(source, /Privacy_LocationServices/);
  // The handler takes no argument and opens only its own literal URLs, so the
  // renderer cannot route an arbitrary address through it.
  assert.match(source, /ipcMain\.handle\('ptv:open-location-settings', async \(\) =>/);
  assert.match(source, /const url = 'x-apple\.systempreferences:com\.apple\.preference\.security\?Privacy_LocationServices';/);
  assert.match(source, /await shell\.openExternal\('ms-settings:privacy-location'\)/);
  // The Linux hint is a sentence, not a button that opens nothing.
  assert.match(source, /return \{\s*ok: false,\s*platform: process\.platform,/);

  const preload = read(main, 'preload.js');
  assert.match(preload, /locationContext: \(\) => ipcRenderer\.invoke\('ptv:location-context'\)/);
  assert.match(preload, /openLocationSettings: \(\) => ipcRenderer\.invoke\('ptv:open-location-settings'\)/);
});

test('the renderer names the failure instead of blaming the viewer', () => {
  const source = read(renderer, 'app.js');
  // The old catch-all: one message for refusal, missing service and timeout.
  assert.doesNotMatch(source, /Location was declined — that is fine\. Enter a ZIP code, a state or a city/);
  assert.match(source, /async function describeLocationFailure\(error\)/);
  for (const needle of [
    'is not allowed to ask macOS for a location',       // no usage description
    'refused the request without asking again',          // remembered refusal
    'No location service on this computer',              // nothing to ask
    'The location request timed out',                    // prompt unanswered
  ]) {
    assert.ok(source.includes(needle), `missing honest message: ${needle}`);
  }
  // One coarse fix, one request per press, and the settings pane when it fails.
  assert.match(source, /enableHighAccuracy: false/);
  assert.match(source, /bind\('local-open-location', 'click'/);
  assert.match(source, /askForLocalMarket\(\{/);
  // One helper, shared by both call sites (the Settings form and the sheet).
  assert.equal(source.match(/askForLocalMarket\(\{/g).length, 3);

  const html = read(renderer, 'index.html');
  assert.match(html, /id="local-setup-settings"[^>]*hidden/);
  const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(ids.length, new Set(ids).size, 'the sheet added a duplicated element id');
});

// ------------------------------------------------------ the distance rule

const directory = {
  schema: 2,
  countries: [{ code: 'US', name: 'United States', local_channels: true }],
  zip_ranges: [],
  zip_prefixes: [],
  markets: [
    { id: 'USPHL', city: 'Philadelphia', state: 'PA', latitude: 39.9526, longitude: -75.1652, stations: [] },
    { id: 'USCLE', city: 'Cleveland', state: 'OH', latitude: 41.4993, longitude: -81.6944, stations: [] },
  ],
  cities: [],
};

function loadLocal() {
  const window = {};
  vm.runInNewContext(fs.readFileSync(path.join(renderer, 'local-channels.js'), 'utf8'), { window });
  return window.PremiumLocalChannels;
}

test('a fix far from every published market is an offer, not an answer', () => {
  const local = loadLocal();
  // Wilkes-Barre, PA: no published market, ~145 km from Philadelphia.
  const far = local.nearestMarketWithDistance(41.2459, -75.8813, directory);
  assert.equal(far.market.id, 'USPHL');
  assert.ok(far.distanceKm > 100, `expected a far fix, got ${far.distanceKm}`);
  assert.equal(local.marketIsNear(far.distanceKm), false);

  // Lancaster-side fix: inside the radius, so it is used as before.
  const near = local.nearestMarketWithDistance(40.0407, -76.3091, directory);
  assert.equal(near.market.id, 'USPHL');
  assert.ok(near.distanceKm < local.NEAREST_MARKET_MAX_KM);
  assert.equal(local.marketIsNear(near.distanceKm), true);

  // The old entry point keeps its contract for every existing caller.
  assert.equal(local.nearestMarket(41.2459, -75.8813, directory).id, 'USPHL');
});

test('the limit is one number shared by the platforms', () => {
  const local = loadLocal();
  assert.equal(local.NEAREST_MARKET_MAX_KM, 120);
  // The Android dialog reads the same limit from its own file, so a ZIP fix and
  // a GPS fix cannot disagree about what "near" means.
  const kotlin = read(repoRoot, 'android', 'app', 'src', 'main', 'kotlin', 'com', 'premiumtv', 'app',
    'data', 'LocalChannels.kt');
  assert.match(kotlin, /const val LOCAL_MARKET_NEAR_KM = 120\.0/);
  assert.match(kotlin, /fun marketIsNear\(distanceKm: Double\)/);
});
