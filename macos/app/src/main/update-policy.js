'use strict';

/**
 * The release-selection rules for PremiumTV's in-app updater.
 *
 * The app may only offer an update when all of these are true:
 *
 *   1. the GitHub release is published (`draft` is false);
 *   2. it is not a pre-release (`prerelease` is false) - previews are never
 *      pushed to stable users, and an installed preview is ahead of them;
 *   3. its MAJOR.MINOR.PATCH[.HOTFIX] version is numerically above the app;
 *   4. the installer for *this* Mac (arm64 or x64) is already attached, so a
 *      release whose build jobs are still uploading cannot send someone to a
 *      missing download.
 *
 * Comparing numbers - not strings - is what keeps 1.0.10 above 1.0.9 and
 * 1.0.6.1 above 1.0.6 without treating it as 1.0.7.
 */

const VERSION_RE = /^v?(\d+)\.(\d+)\.(\d+)(?:\.(\d+))?(?:[-+][0-9A-Za-z][0-9A-Za-z.-]*)?$/;

function parseVersion(value) {
  const match = VERSION_RE.exec(String(value == null ? '' : value).trim());
  if (!match) return null;
  const parts = match.slice(1).filter((part) => part !== undefined).map(Number);
  while (parts.length < 4) parts.push(0);
  return parts;
}

function normalizeVersion(value) {
  const parts = parseVersion(value);
  if (!parts) return null;
  while (parts.length > 3 && parts[parts.length - 1] === 0) parts.pop();
  return parts.join('.');
}

/** 1 when a is newer, -1 when older, 0 when equal; null for unreadable input. */
function compareVersions(a, b) {
  const left = parseVersion(a);
  const right = parseVersion(b);
  if (!left || !right) return null;
  for (let index = 0; index < 4; index += 1) {
    if (left[index] !== right[index]) return left[index] > right[index] ? 1 : -1;
  }
  return 0;
}

function isNewer(candidate, current) {
  return compareVersions(candidate, current) === 1;
}

/**
 * Releases published only so an updater that reads three-part versions
 * (1.0.4-1.0.6) can reach the canonical build. They carry the same app code:
 * offering the alias to a Mac already running the canonical version would be
 * a pointless full-size download, so it is skipped for that machine.
 */
const COMPATIBILITY_ALIASES = { '1.0.7': '1.0.6.1' };

function canonicalVersion(value) {
  const version = normalizeVersion(value);
  return version ? (COMPATIBILITY_ALIASES[version] || version) : null;
}

function isCompatibilityAlias(candidate, current) {
  // Only a registered alias qualifies; the canonical version is not itself an
  // alias even though canonicalVersion() maps it to itself.
  const version = normalizeVersion(candidate);
  const canonical = version ? COMPATIBILITY_ALIASES[version] : null;
  return canonical != null && canonical === canonicalVersion(current);
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
    // A compatibility alias of the installed build is the same code under a
    // second name; it must not read as a newer stable release. The canonical
    // version behind it is still what "newest stable" means for this Mac.
    if (isCompatibilityAlias(version, current)) {
      const canonical = canonicalVersion(version);
      if (canonical && (!newestStable || isNewer(canonical, newestStable))) {
        newestStable = canonical;
      }
      continue;
    }
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
  // A Mac packaged as the three-part compatibility alias (1.0.7) is the same
  // build as 1.0.6.1, so it is not a preview above the stable release.
  const installed = canonicalVersion(currentVersion) || currentVersion;
  if (isNewer(newestStable, installed)) {
    return `PremiumTV ${newestStable} is newer, but its Mac installer has not finished uploading yet.`;
  }
  if (isNewer(installed, newestStable)) {
    return `This build (${currentVersion}) is a preview above the newest stable release (${newestStable}).`;
  }
  return `PremiumTV ${currentVersion} is the newest stable release.`;
}

module.exports = {
  COMPATIBILITY_ALIASES,
  canonicalVersion,
  isCompatibilityAlias,
  parseVersion,
  normalizeVersion,
  compareVersions,
  isNewer,
  macAssetName,
  selectStableUpdate,
  describeState,
};
