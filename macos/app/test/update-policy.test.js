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

test('four-part stable releases are understood, not rejected', () => {
  assert.equal(policy.normalizeVersion('v1.0.6.1-debug'), '1.0.6.1');
  assert.equal(policy.compareVersions('1.0.6.1', '1.0.6'), 1);
  assert.equal(policy.compareVersions('1.1.0', '1.0.6.1'), 1);
  assert.equal(policy.compareVersions('1.0.6.1', '1.1.0'), -1);
  const { update, newestStable } = policy.selectStableUpdate([release('1.0.6.1')], '1.0.6', 'arm64');
  assert.equal(newestStable, '1.0.6.1');
  assert.equal(update.version, '1.0.6.1');
  assert.equal(update.assetName, 'PremiumTV-1.0.6.1-mac-arm64.dmg');
});

test('the 1.0.7 compatibility alias reaches 1.0.6 but not 1.0.6.1', () => {
  const releases = [release('1.0.6.1'), release('1.0.7')];

  // 1.0.4-1.0.6 cannot parse 1.0.6.1; the alias is the release they can see.
  const older = policy.selectStableUpdate(releases, '1.0.6', 'arm64');
  assert.equal(older.update.version, '1.0.7');
  assert.equal(older.newestStable, '1.0.7');

  // A Mac already on the canonical build must not download the same code
  // again under the alias' name.
  const current = policy.selectStableUpdate(releases, '1.0.6.1', 'arm64');
  assert.equal(current.update, null);
  assert.equal(current.newestStable, '1.0.6.1');
  assert.equal(
    policy.describeState('1.0.6.1', current.newestStable, current.update),
    'PremiumTV 1.0.6.1 is the newest stable release.',
  );

  // The Mac build packaged as 1.0.7 is the same code; it must describe
  // itself as being on the newest stable, not as a preview above it.
  const aliasInstall = policy.selectStableUpdate(releases, '1.0.7', 'arm64');
  assert.equal(aliasInstall.update, null);
  assert.equal(aliasInstall.newestStable, '1.0.6.1');
  assert.equal(
    policy.describeState('1.0.7', aliasInstall.newestStable, aliasInstall.update),
    'PremiumTV 1.0.7 is the newest stable release.',
  );

  assert.equal(policy.canonicalVersion('1.0.7'), '1.0.6.1');
  assert.equal(policy.isCompatibilityAlias('1.0.7', '1.0.6.1'), true);
  assert.equal(policy.isCompatibilityAlias('1.0.7', '1.0.6'), false);
  assert.equal(policy.isCompatibilityAlias('1.0.6.1', '1.0.6.1'), false);
});

test('1.0.9 is a real release offered to every older build', () => {
  // 1.0.9 briefly existed as the alias of 1.0.8.1 (whose release never
  // carried a Mac installer - four-part versions cannot be packaged - so
  // strip its fixture assets). As a real release it now simply outranks
  // both: no alias folding anywhere, and the V scheme is retired.
  const canonical = release('1.0.8.1', { assets: [] });
  const releases = [canonical, release('1.0.9')];

  const older = policy.selectStableUpdate(releases, '1.0.8', 'arm64');
  assert.equal(older.update.version, '1.0.9');
  assert.equal(older.update.assetName, 'PremiumTV-1.0.9-mac-arm64.dmg');
  assert.equal(older.newestStable, '1.0.9');

  // A build still reporting 1.0.8.1 is offered 1.0.9 like any other update
  // (the old alias table used to hide it as "the same code, second name").
  const patchEra = policy.selectStableUpdate(releases, '1.0.8.1', 'arm64');
  assert.equal(patchEra.update.version, '1.0.9');
  assert.equal(patchEra.newestStable, '1.0.9');

  const current = policy.selectStableUpdate(releases, '1.0.9', 'arm64');
  assert.equal(current.update, null);
  assert.equal(current.newestStable, '1.0.9');
  assert.equal(
    policy.describeState('1.0.9', current.newestStable, current.update),
    'PremiumTV 1.0.9 is the newest stable release.',
  );

  assert.equal(policy.canonicalVersion('1.0.9'), '1.0.9');
  assert.equal(policy.canonicalVersion('1.0.10'), '1.0.10');
  assert.equal(policy.isCompatibilityAlias('1.0.9', '1.0.8.1'), false);
  assert.equal(policy.isCompatibilityAlias('1.0.10', '1.0.8.2'), false);
});
