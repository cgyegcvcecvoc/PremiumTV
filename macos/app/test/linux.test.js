'use strict';

/**
 * The Linux edition of the same app (1.1.18).
 *
 * A Linux build is only honest if three things hold: the packager produces
 * Linux artifacts and not a second Mac disk image; the smoke test still runs
 * without a Mac-only tool in the loop; and the in-app updater never offers a
 * Linux install a Mac installer. The last one is the dangerous one, because the
 * Mac .dmg is attached to the very same release, so an installer lookup that
 * ignores the platform finds it and downloads 130 MB of something unusable.
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const appRoot = path.join(__dirname, '..');
const repoRoot = path.join(appRoot, '..', '..');
const policy = require('../src/main/update-policy');
const { AppUpdater } = require('../src/main/updater');

const LINUX_INSTALLER = 'PremiumTV-1.0.5-linux-arm64.AppImage';
const INSTALLER_BYTES = Buffer.from('an AppImage a Linux viewer can run');

test('electron-builder is configured for Linux installers', () => {
  const builder = fs.readFileSync(path.join(appRoot, 'electron-builder.yml'), 'utf8');
  const linux = builder.slice(builder.indexOf('\nlinux:'));
  assert.ok(linux.length > 0, 'the linux block is missing');
  for (const target of ['AppImage', 'deb', 'tar.xz']) {
    assert.match(linux, new RegExp(`target: ${target.replace('.', '\\.')}`));
  }
  // Names must carry the platform, or the release page gets two files called
  // PremiumTV-1.1.18 and no way to tell which one to install.
  assert.match(linux, /artifactName: PremiumTV-\$\{version\}-linux-\$\{arch\}\.\$\{ext\}/);
  // A .desktop entry is what puts the app in an applications menu.
  assert.match(linux, /syncDesktopName: true/);
  assert.match(linux, /category: AudioVideo/);
  // The mac targets keep their own name, unchanged.
  assert.match(builder, /artifactName: PremiumTV-\$\{version\}-mac-\$\{arch\}\.\$\{ext\}/);
});

test('the packager carries the metadata a .deb control file requires', () => {
  // The first real Linux build died in FpmTarget with "Please specify project
  // homepage": electron-builder writes `Homepage:` into the Debian control file
  // and refuses to invent one. package.json is where npm metadata lives, so
  // that is where the fix belongs - and this is the check that keeps it there,
  // because the failure only shows up when a Linux target is built.
  const pkg = require('../package.json');
  assert.equal(typeof pkg.homepage, 'string');
  assert.match(pkg.homepage, /^https:\/\//);
  assert.equal(typeof pkg.license, 'string');
  assert.ok(pkg.author && pkg.author.email, 'the deb control file needs a maintainer address');
  assert.ok(pkg.description && pkg.description.length > 10, 'deb needs a Description:');
  const builder = fs.readFileSync(path.join(appRoot, 'electron-builder.yml'), 'utf8');
  const linux = builder.slice(builder.indexOf('\nlinux:'));
  assert.match(linux, /maintainer: .+<.+>/);
  // A desktop entry with no Category: is rejected by desktop-file-validate.
  assert.match(linux, /category: AudioVideo/);
});

test('the packager signs nothing on Linux and does not need codesign', () => {
  const hook = fs.readFileSync(path.join(appRoot, 'tools', 'after-pack.cjs'), 'utf8');
  assert.match(hook, /if \(process\.platform !== 'darwin'\) return;/);
  const main = fs.readFileSync(path.join(appRoot, 'src', 'main', 'main.js'), 'utf8');
  // Wayland and X11 desktops both need to work from one binary.
  assert.match(main, /process\.platform === 'linux'[\s\S]{0,120}ozone-platform-hint/);
});

test('the updater picks the installer this platform can run', () => {
  assert.equal(policy.installerAssetName('1.1.18', 'arm64', 'darwin'), 'PremiumTV-1.1.18-mac-arm64.dmg');
  assert.equal(policy.installerAssetName('1.1.18', 'x64', 'linux'), 'PremiumTV-1.1.18-linux-x64.AppImage');
  // A release page never carries "arm64" for a Mac named x64 and vice versa.
  assert.equal(policy.installerAssetName('1.1.18', 'arm64', 'linux'), 'PremiumTV-1.1.18-linux-arm64.AppImage');
  assert.equal(policy.checksumAssetName('darwin'), 'SHA256SUMS-macos.txt');
  assert.equal(policy.checksumAssetName('linux'), 'SHA256SUMS-linux.txt');
  // The Mac name is still exported: the download site and the old tests use it.
  assert.equal(policy.macAssetName('1.1.18', 'x64'), 'PremiumTV-1.1.18-mac-x64.dmg');
});

function releaseJson(withLinux) {
  const assets = [{
    name: 'PremiumTV-1.0.5-mac-arm64.dmg',
    size: 10,
    browser_download_url: 'https://github.com/releases/v1.0.5/PremiumTV-1.0.5-mac-arm64.dmg',
  }, {
    name: 'SHA256SUMS-macos.txt',
    size: 10,
    browser_download_url: 'https://github.com/releases/v1.0.5/SHA256SUMS-macos.txt',
  }];
  if (withLinux) {
    assets.push({
      name: LINUX_INSTALLER,
      size: INSTALLER_BYTES.length,
      browser_download_url: `https://github.com/releases/v1.0.5/${LINUX_INSTALLER}`,
    }, {
      name: 'SHA256SUMS-linux.txt',
      size: 10,
      browser_download_url: 'https://github.com/releases/v1.0.5/SHA256SUMS-linux.txt',
    });
  }
  return [{
    tag_name: 'v1.0.5',
    draft: false,
    prerelease: false,
    html_url: 'https://github.com/cgyegcvcecvoc/PremiumTV/releases/tag/v1.0.5',
    assets,
  }];
}

test('a Mac-only release offers a Linux install nothing', () => {
  const macOnly = policy.selectStableUpdate(releaseJson(false), '1.0.4', 'arm64', 'linux');
  assert.equal(macOnly.update, null);
  // The same release is a real update for the Mac it was built for.
  assert.equal(policy.selectStableUpdate(releaseJson(false), '1.0.4', 'arm64', 'darwin').update.version, '1.0.5');
  // …and for Linux once the linux job has attached its AppImage.
  assert.equal(policy.selectStableUpdate(releaseJson(true), '1.0.4', 'arm64', 'linux').update.assetName,
    LINUX_INSTALLER);
});

test('a Linux install downloads the AppImage and hands it over executable', async (t) => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'premiumtv-linux-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const checksum = require('node:crypto').createHash('sha256').update(INSTALLER_BYTES).digest('hex');
  const opened = [];
  const fetchImpl = async (url) => {
    if (url.includes('/releases?')) {
      return new Response(JSON.stringify(releaseJson(true)), {
        status: 200, headers: { 'content-type': 'application/json' },
      });
    }
    if (url.endsWith('SHA256SUMS-linux.txt')) {
      return new Response(`${checksum}  ${LINUX_INSTALLER}\n`, { status: 200 });
    }
    if (url.endsWith(LINUX_INSTALLER)) {
      return new Response(INSTALLER_BYTES, {
        status: 200, headers: { 'content-length': String(INSTALLER_BYTES.length) },
      });
    }
    return new Response('not found', { status: 404 });
  };
  const updater = new AppUpdater({
    currentVersion: '1.0.4',
    stateFile: path.join(dir, 'update-state.json'),
    downloadDir: path.join(dir, 'updates'),
    arch: 'arm64',
    platform: 'linux',
    fetchImpl,
    shell: {
      openPath: async () => { throw new Error('a Linux update must not open a .dmg'); },
      showItemInFolder: (file) => opened.push(file),
      openExternal: async () => {},
    },
    now: () => Date.now(),
  });
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));

  const checked = await updater.check(true);
  assert.equal(checked.availableVersion, '1.0.5');
  const downloaded = await updater.download();
  assert.equal(downloaded.downloadedVersion, '1.0.5');
  assert.equal(path.basename(downloaded.installerPath), LINUX_INSTALLER);
  assert.match(downloaded.message, /Show update file/);
  assert.equal(updater.userAgent, 'PremiumTV/1.0.4 (Linux)',
    'the version check must not claim to be a Mac');

  const openedResult = await updater.openInstaller();
  assert.equal(openedResult.ok, true);
  assert.deepEqual(opened, [downloaded.installerPath], 'the file manager is shown the AppImage');
  const mode = fs.statSync(downloaded.installerPath).mode & 0o111;
  assert.ok(mode, 'an AppImage is only runnable when it is executable');
});
