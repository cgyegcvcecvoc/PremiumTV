#!/usr/bin/env node
'use strict';

/**
 * Copies the vendored player libraries into the renderer.
 *
 * The packaged app must work with no network at all, so hls.js and mpegts.js
 * are taken from node_modules at build time instead of being fetched from a
 * CDN. src/renderer/vendor is gitignored: it is derived from the lockfile,
 * exactly like the playlist bundle is derived from the repository.
 */

const fs = require('node:fs');
const path = require('node:path');

const appRoot = path.join(__dirname, '..');
const vendorDir = path.join(appRoot, 'src', 'renderer', 'vendor');

const ASSETS = [
  { from: 'hls.js/dist/hls.min.js', to: 'hls.min.js', minBytes: 200 * 1024 },
  { from: 'mpegts.js/dist/mpegts.js', to: 'mpegts.js', minBytes: 100 * 1024 },
];

function main() {
  fs.mkdirSync(vendorDir, { recursive: true });
  for (const asset of ASSETS) {
    const source = path.join(appRoot, 'node_modules', asset.from);
    const target = path.join(vendorDir, asset.to);
    if (!fs.existsSync(source)) {
      console.error(`MISSING ASSET: ${source} — run "npm install" first`);
      return 2;
    }
    fs.copyFileSync(source, target);
    const size = fs.statSync(target).size;
    if (size < asset.minBytes) {
      console.error(`SUSPICIOUS ASSET: ${target} is only ${size} bytes`);
      return 2;
    }
    console.log(`vendored ${asset.to} (${Math.round(size / 1024)} KB)`);
  }
  return 0;
}

process.exit(main());
