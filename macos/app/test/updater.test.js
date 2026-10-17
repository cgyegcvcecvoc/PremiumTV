'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const fsp = require('node:fs/promises');
const os = require('node:os');
const path = require('node:path');

const { AppUpdater } = require('../src/main/updater');

const VERSION = '1.0.5';
const INSTALLER = 'PremiumTV-1.0.5-mac-arm64.dmg';
const INSTALLER_BYTES = Buffer.from('a verified PremiumTV installer');

function releaseJson(version = VERSION) {
  return [{
    tag_name: `v${version}`,
    draft: false,
    prerelease: false,
    html_url: `https://github.com/cgyegcvcecvoc/PremiumTV1/releases/tag/v${version}`,
    assets: [
      {
        name: `PremiumTV-${version}-mac-arm64.dmg`,
        size: INSTALLER_BYTES.length,
        browser_download_url: `https://github.com/releases/v${version}/PremiumTV-${version}-mac-arm64.dmg`,
      },
      {
        name: 'SHA256SUMS-macos.txt',
        size: 100,
        browser_download_url: `https://github.com/releases/v${version}/SHA256SUMS-macos.txt`,
      },
    ],
  }];
}

function harness(t, options = {}) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'premiumtv-updater-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const calls = [];
  const checksum = crypto.createHash('sha256').update(INSTALLER_BYTES).digest('hex');
  const fetchImpl = async (url) => {
    calls.push(url);
    if (url.includes('/releases?')) {
      return new Response(JSON.stringify(releaseJson()), {
        status: 200,
        headers: { 'content-type': 'application/json', etag: 'W/"release-list-1"' },
      });
    }
    if (url.endsWith('SHA256SUMS-macos.txt')) {
      const line = options.badChecksum
        ? `${'0'.repeat(64)}  ${INSTALLER}\n`
        : `${checksum}  ${INSTALLER}\n`;
      return new Response(line, { status: 200 });
    }
    if (url.endsWith(INSTALLER)) {
      return new Response(INSTALLER_BYTES, {
        status: 200,
        headers: { 'content-length': String(INSTALLER_BYTES.length) },
      });
    }
    return new Response('not found', { status: 404 });
  };
  const updater = new AppUpdater({
    currentVersion: options.currentVersion || '1.0.4',
    stateFile: path.join(dir, 'update-state.json'),
    downloadDir: path.join(dir, 'updates'),
    arch: 'arm64',
    fetchImpl,
    shell: { openPath: async () => '', openExternal: async () => {} },
    now: () => Date.now(),
  });
  return { updater, calls, dir, checksum };
}

test('a check offers the new stable release without downloading anything', async (t) => {
  const { updater, calls } = harness(t);
  const state = await updater.check(true);
  assert.equal(state.availableVersion, VERSION);
  assert.equal(state.downloadedVersion, null);
  // Only the release list was requested; no installer was downloaded.
  assert.equal(calls.length, 1);
  assert.match(calls[0], /\/releases\?per_page=30$/);
  assert.match(state.message, /1\.0\.5 is available/);
});

test('the daily throttle prevents repeated GitHub checks', async (t) => {
  const { updater, calls } = harness(t);
  await updater.check(true);
  await updater.check(false);
  await updater.check(false);
  assert.equal(calls.length, 1, 'an automatic check inside the window must not hit GitHub');
});

test('a forced re-check keeps the downloaded installer and does not download it again', async (t) => {
  const { updater, calls } = harness(t);
  await updater.check(true);
  const downloaded = await updater.download();
  assert.equal(downloaded.downloadedVersion, VERSION);
  assert.ok(fs.existsSync(downloaded.installerPath));
  await updater.check(true);
  const callsAfterCheck = calls.length;
  const state = await updater.download();
  assert.equal(state.downloadedVersion, VERSION);
  assert.equal(calls.length, callsAfterCheck, 'a second download must reuse the verified file');
  assert.match(state.message, /already downloaded and verified/);
});

test('the installer is SHA-256 verified before it is kept', async (t) => {
  const { updater } = harness(t, { badChecksum: true });
  await updater.check(true);
  const state = await updater.download();
  assert.equal(state.downloadedVersion, null);
  assert.match(state.error, /failed its SHA-256 check/);
  assert.equal(fs.existsSync(path.join(path.dirname(updater.stateFile), 'updates', INSTALLER)), false);
});

test('a preview build is ahead of the newest stable release and gets no offer', async (t) => {
  const { updater } = harness(t, { currentVersion: '1.1.1' });
  const state = await updater.check(true);
  assert.equal(state.availableVersion, null);
  assert.match(state.message, /preview above the newest stable release/);
});

test('update memory resets when the app itself is updated', async (t) => {
  const { updater, dir } = harness(t);
  await updater.check(true);
  const downloaded = await updater.download();
  assert.ok(fs.existsSync(downloaded.installerPath));

  // Simulate launching the downloaded 1.0.5 app after installing it.
  const upgraded = new AppUpdater({
    currentVersion: VERSION,
    stateFile: path.join(dir, 'update-state.json'),
    downloadDir: path.join(dir, 'updates'),
    arch: 'arm64',
    fetchImpl: async () => new Response('[]', { status: 200 }),
  });
  assert.equal(upgraded.status().availableVersion, null);
  assert.equal(upgraded.status().downloadedVersion, null);
  assert.equal(fs.existsSync(path.join(dir, 'updates', INSTALLER)), false,
    'the obsolete installer is pruned after the update is installed');
});

test('open installer refuses a missing download instead of pretending', async (t) => {
  const { updater } = harness(t);
  const result = await updater.openInstaller();
  assert.equal(result.ok, false);
  assert.match(result.message, /installer is missing/);
});
