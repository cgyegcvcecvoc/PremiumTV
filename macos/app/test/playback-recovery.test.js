'use strict';

/**
 * The macOS/web in-place retry policy. Android pins the same limits in
 * ServerFallback.kt (TRANSIENT_RETRY_LIMIT = 2, MEDIA_RETRY_LIMIT = 1).
 */

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

function loadPolicy() {
  const window = {};
  const code = fs.readFileSync(
    path.join(__dirname, '..', 'src', 'renderer', 'playback-recovery.js'), 'utf8');
  vm.runInNewContext(code, { window, module: { exports: {} } });
  return window.PremiumRecovery;
}

test('network and stall faults are transient', () => {
  const policy = loadPolicy();
  for (const error of [
    null,
    { type: 'networkError', details: 'manifestLoadError' },
    { type: 'networkError', details: 'fragLoadError' },
    { code: 2, message: 'MEDIA_ERR_NETWORK' },
    'a timeout while reading the segment',
  ]) {
    assert.equal(policy.classifyFault(error), 'transient', JSON.stringify(error));
  }
});

test('decoder and audio faults are media faults', () => {
  const policy = loadPolicy();
  for (const error of [
    { type: 'mediaError', details: 'bufferAppendError' },
    { code: 3, message: 'MEDIA_ERR_DECODE' },
    'codec initialization failed',
  ]) {
    assert.equal(policy.classifyFault(error), 'media', JSON.stringify(error));
  }
});

test('provider decisions never waste a retry', () => {
  const policy = loadPolicy();
  for (const error of [
    { response: { code: 404 } },
    { response: { code: 403 } },
    { code: 4, message: 'MEDIA_ERR_SRC_NOT_SUPPORTED' },
    { type: 'otherError', details: 'manifestParsingError' },
    'DRM key request refused',
  ]) {
    assert.equal(policy.classifyFault(error), 'permanent', JSON.stringify(error));
  }
});

test('a transient fault reconnects twice, a media fault once, a permanent fault never', () => {
  const policy = loadPolicy();
  assert.equal(policy.TRANSIENT_LIMIT, 2);
  assert.equal(policy.MEDIA_LIMIT, 1);
  assert.equal(policy.decideRecovery('transient', 0, false).retryInPlace, true);
  assert.equal(policy.decideRecovery('transient', 1, false).retryInPlace, true);
  assert.equal(policy.decideRecovery('transient', 2, false).retryInPlace, false);
  assert.equal(policy.decideRecovery('media', 0, false).retryInPlace, true);
  assert.equal(policy.decideRecovery('media', 1, false).retryInPlace, false);
  assert.equal(policy.decideRecovery('permanent', 0, false).retryInPlace, false);
  assert.match(policy.decideRecovery('media', 0, false).notice, /decoder/);
  assert.match(policy.decideRecovery('transient', 0, false).notice, /Reconnect/);
});

test('a server switch ends the in-place retries', () => {
  const policy = loadPolicy();
  assert.equal(policy.decideRecovery('transient', 0, true).retryInPlace, false);
  assert.equal(policy.decideRecovery('media', 0, true).retryInPlace, false);
});
