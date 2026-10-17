'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const policy = require('../src/main/update-policy');

function release(version, options = {}) {
  const arch = options.arch || 'arm64';
  return {
    tag_name: `v${version}`,
    draft: Boolean(options.draft),
    prerelease: Boolean(options.prerelease),
    html_url: `https://github.com/cgyegcvcecvoc/PremiumTV1/releases/tag/v${version}`,
    assets: options.assets || [
      {
        name: `PremiumTV-${version}-mac-${arch}.dmg`,
        size: 1234,
        browser_download_url: `https://github.com/x/v${version}/PremiumTV-${version}-mac-${arch}.dmg`,
      },
      {
        name: 'SHA256SUMS-macos.txt',
        size: 100,
        browser_download_url: `https://github.com/x/v${version}/SHA256SUMS-macos.txt`,
      },
    ],
  };
}

test('numeric ordering, not string ordering, decides which version is newer', () => {
  assert.equal(policy.compareVersions('1.0.10', '1.0.9'), 1);
  assert.equal(policy.compareVersions('v1.1.0', '1.0.99'), 1);
  assert.equal(policy.compareVersions('1.0.4-debug', '1.0.4'), 0);
  assert.equal(policy.compareVersions('1.0.3', '1.0.4'), -1);
  assert.equal(policy.compareVersions('nonsense', '1.0.4'), null);
});

test('only a published stable release above the app is offered', () => {
  const releases = [
    release('1.0.4'),
    release('1.0.5', { prerelease: true }),
    release('1.0.6', { draft: true }),
    release('0.9.9'),
  ];
  const { update, newestStable } = policy.selectStableUpdate(releases, '1.0.3', 'arm64');
  assert.equal(newestStable, '1.0.4');
  assert.equal(update.version, '1.0.4');
  assert.equal(update.assetName, 'PremiumTV-1.0.4-mac-arm64.dmg');
});

test('the newest complete stable wins when several are available', () => {
  const releases = [release('1.0.4'), release('1.0.6'), release('1.0.5')];
  const { update } = policy.selectStableUpdate(releases, '1.0.3', 'arm64');
  assert.equal(update.version, '1.0.6');
});

test('a release whose installer is still uploading is not offered', () => {
  const incomplete = release('1.0.5', { assets: [] });
  const { update, newestStable } = policy.selectStableUpdate([incomplete], '1.0.4', 'arm64');
  assert.equal(update, null);
  assert.equal(newestStable, '1.0.5');
  assert.match(
    policy.describeState('1.0.4', newestStable, update),
    /Mac installer has not finished uploading/,
  );
});

test('the right installer is selected for Intel and Apple Silicon', () => {
  const releases = [
    release('1.0.5', { arch: 'x64' }),
    release('1.0.5', { arch: 'arm64' }),
  ];
  const intel = policy.selectStableUpdate(releases, '1.0.4', 'x64');
  const apple = policy.selectStableUpdate(releases, '1.0.4', 'arm64');
  assert.equal(intel.update.assetName, 'PremiumTV-1.0.5-mac-x64.dmg');
  assert.equal(apple.update.assetName, 'PremiumTV-1.0.5-mac-arm64.dmg');
});

test('an installed preview is never offered an older stable build', () => {
  const { update, newestStable } = policy.selectStableUpdate([release('1.0.4')], '1.1.1', 'arm64');
  assert.equal(update, null);
  assert.equal(newestStable, '1.0.4');
  assert.match(
    policy.describeState('1.1.1', newestStable, update),
    /preview above the newest stable release/,
  );
});

test('a current stable build is up to date', () => {
  const { update } = policy.selectStableUpdate([release('1.0.4')], '1.0.4', 'arm64');
  assert.equal(update, null);
  assert.match(policy.describeState('1.0.4', '1.0.4', update), /newest stable release/);
});

test('pre-releases never become the newest stable release', () => {
  const { update, newestStable } = policy.selectStableUpdate(
    [release('1.0.4'), release('1.1.2', { prerelease: true })],
    '1.0.3',
    'arm64',
  );
  assert.equal(newestStable, '1.0.4');
  assert.equal(update.version, '1.0.4');
});
