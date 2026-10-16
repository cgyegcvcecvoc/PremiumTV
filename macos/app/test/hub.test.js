'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { JSDOM } = require('jsdom');
const hub = path.resolve(__dirname, '../../../hub/static');

test('Netlify cards recommend stable independently of preview order and link release checksums', async (t) => {
  const dom = new JSDOM(fs.readFileSync(path.join(hub, 'index.html'), 'utf8'), {
    runScripts: 'outside-only', url: 'https://premiumtv.example/',
  });
  t.after(() => dom.window.close());
  const android = (version, channel) => ({ version, channel, name: `PremiumTV-${version}-debug.apk`,
    size: 100, desc: channel, dl: `https://github.com/example/releases/v${version}/app.apk`,
    checksums: `https://github.com/example/releases/v${version}/SHA256SUMS-android.txt` });
  const mac = (version, channel) => ({ version, channel, desc: channel, assets: Array.from({ length: 5 }, (_, i) => ({
    url: `https://github.com/example/releases/v${version}/mac-${i}.dmg`, name: `mac-${i}`,
  })) });
  dom.window.fetch = async () => ({ ok: true, json: async () => ({
    stats: {}, android: [android('1.1.1', 'Preview'), android('1.0.3', 'Stable'), android('1.0.2', 'Archive')],
    macos: [mac('1.1.1', 'Preview'), mac('1.0.3', 'Stable')], featured: [], bundles: [],
    categories: {}, countries: [], epg: [],
  }) });
  dom.window.eval(fs.readFileSync(path.join(hub, 'assets/app.js'), 'utf8'));
  await new Promise((resolve) => setImmediate(resolve));
  const doc = dom.window.document;
  const cards = [...doc.querySelectorAll('#app-grid .app-card')];
  assert.equal(cards.length, 3);
  assert.match(cards[0].textContent, /1\.0\.3/);
  assert.match(cards[0].querySelector('a.dl').href, /v1\.0\.3/);
  assert.match(cards[1].textContent, /1\.0\.3/);
  assert.match(cards[2].textContent, /Encore Preview/);
  assert.match(cards[2].textContent, /1\.1\.1/);
  assert.equal(doc.querySelectorAll('#apk-table a[href$="SHA256SUMS-android.txt"]').length, 3);
  assert.doesNotMatch(doc.getElementById('hero-meta').textContent, /Could not load/);
});
