'use strict';

/**
 * The release-selection rules for PremiumTV's in-app updater.
 *
 * The app may only offer an update when all of these are true:
 *
 *   1. the GitHub release is published (`draft` is false);
 *   2. it is not a pre-release (`prerelease` is false) - previews are never
 *      pushed to stable users, and an installed preview is ahead of them;
 *   3. its MAJOR.MINOR.PATCH version is numerically above the installed app;
 *   4. the installer for *this* Mac (arm64 or x64) is already attached, so a
 *      release whose build jobs are still uploading cannot send someone to a
 *      missing download.
 *
 * Comparing numbers - not strings - is what keeps 1.0.10 above 1.0.9 and stops
 * an older release from being offered over a newer preview.
 */

const VERSION_RE = /^v?(\d+)\.(\d+)\.(\d+)(?:[-+][0-9A-Za-z][0-9A-Za-z.-]*)?$/;

function parseVersion(value) {
  const match = VERSION_RE.exec(String(value == null ? '' : value).trim());
  if (!match) return null;
  return match.slice(1, 4).map((part) => Number(part));
}

function normalizeVersion(value) {
  const parts = parseVersion(value);
  return parts ? parts.join('.') : null;
}

/** 1 when a is newer, -1 when older, 0 when equal; null for unreadable input. */
function compareVersions(a, b) {
  const left = parseVersion(a);
  const right = parseVersion(b);
  if (!left || !right) return null;
  for (let index = 0; index < 3; index += 1) {
    if (left[index] !== right[index]) return left[index] > right[index] ? 1 : -1;
  }
  return 0;
}

function isNewer(candidate, current) {
  return compareVersions(candidate, current) === 1;
}

function macArch(arch) {
  return arch === 'x64' ? 'x64' : 'arm64';
}

function macAssetName(version, arch) {
  return `PremiumTV-${version}-mac-${macArch(arch)}.dmg`;
}

function releaseTag(release) {
  return String((release && (release.tag_name || release.tag)) || '');
}

/**
 * Choose the newest usable update from a GitHub releases list.
 *
 * Returns `{ update, newestStable }`; `update` is null when the installed
 * build is already the newest stable release (or ahead of it as a preview).
 */
function selectStableUpdate(releases, currentVersion, arch = 'arm64') {
  const current = normalizeVersion(currentVersion);
  if (!current) return { update: null, newestStable: null };

  let newestStable = null;
  let update = null;

  for (const release of Array.isArray(releases) ? releases : []) {
    if (!release || release.draft || release.prerelease) continue;
    const version = normalizeVersion(releaseTag(release));
    if (!version) continue;
    if (!newestStable || isNewer(version, newestStable)) newestStable = version;
    if (!isNewer(version, current)) continue;

    const assets = Array.isArray(release.assets) ? release.assets : [];
    const assetName = macAssetName(version, arch);
    const asset = assets.find((candidate) => candidate && candidate.name === assetName);
    if (!asset || typeof asset.browser_download_url !== 'string' ||
        !asset.browser_download_url.startsWith('https://')) {
      continue;
    }
    const checksum = assets.find((candidate) =>
      candidate && candidate.name === 'SHA256SUMS-macos.txt' &&
      typeof candidate.browser_download_url === 'string' &&
      candidate.browser_download_url.startsWith('https://'));
    const candidate = {
      version,
      tag: `v${version}`,
      assetName,
      installerUrl: asset.browser_download_url,
      checksumUrl: checksum ? checksum.browser_download_url : null,
      installerSize: Number(asset.size) || 0,
      releaseUrl: typeof release.html_url === 'string' ? release.html_url : '',
    };
    if (!update || isNewer(version, update.version)) update = candidate;
  }

  return { update, newestStable };
}

/** Human-readable status for Settings, matching the Android wording. */
function describeState(currentVersion, newestStable, update) {
  if (update) return `PremiumTV ${update.version} is available (installed: ${currentVersion}).`;
  if (!newestStable) return 'No stable release was found on GitHub.';
  if (isNewer(newestStable, currentVersion)) {
    return `PremiumTV ${newestStable} is newer, but its Mac installer has not finished uploading yet.`;
  }
  if (isNewer(currentVersion, newestStable)) {
    return `This build (${currentVersion}) is a preview above the newest stable release (${newestStable}).`;
  }
  return `PremiumTV ${currentVersion} is the newest stable release.`;
}

module.exports = {
  parseVersion,
  normalizeVersion,
  compareVersions,
  isNewer,
  macAssetName,
  selectStableUpdate,
  describeState,
};
