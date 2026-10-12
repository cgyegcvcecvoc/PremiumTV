'use strict';

/**
 * electron-builder afterPack hook: ad-hoc sign the assembled .app on macOS.
 *
 * This repository has no Apple Developer ID certificate, so the build cannot be
 * Developer-ID signed or notarized. An ad-hoc signature still makes the app
 * launchable on Apple Silicon (an entirely unsigned arm64 binary would be
 * killed at load time), and is the same approach the Android sibling uses with
 * its debug key: it installs and runs, it just is not notarized.
 *
 * On non-darwin builders (the DMG-only Linux job) there is no codesign, so this
 * is a no-op there.
 */

const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

module.exports = async function afterPack(context) {
  if (process.platform !== 'darwin') return;

  const appOutDir = context.appOutDir;
  const productName = context.packager.appInfo.productFilename;
  const appPath = path.join(appOutDir, `${productName}.app`);
  if (!fs.existsSync(appPath)) return;

  // Sign the whole bundle. --deep is deprecated but remains the pragmatic way to
  // cover every nested helper/framework Electron ships in one pass.
  execFileSync(
    'codesign',
    ['--force', '--deep', '--sign', '-', '--timestamp=none', appPath],
    { stdio: 'inherit' },
  );

  // Report, but do not fail the build on, a verification complaint: Electron's
  // nested frameworks occasionally trip --strict while remaining launchable.
  try {
    const verify = execFileSync('codesign', ['--verify', '--deep', '--verbose=2', appPath], {
      stdio: 'pipe',
    });
    process.stdout.write(verify.toString());
  } catch (error) {
    process.stdout.write(`codesign verify reported (non-fatal): ${error.message}\n`);
  }
};
