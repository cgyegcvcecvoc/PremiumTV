'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const renderer = path.join(__dirname, '..', 'src', 'renderer');

function loadReport() {
  const window = {};
  vm.runInNewContext(fs.readFileSync(path.join(renderer, 'report.js'), 'utf8'), { window });
  return window.PremiumReport;
}

test('a report names the channel, the feed and the player message', () => {
  const report = loadReport();
  const url = new URL(
    report.issueUrl({
      channel: 'BBC America',
      group: 'Entertainment',
      url: 'http://example.test/live/index.m3u8?token=abc',
      serverIndex: 1,
      serverCount: 3,
      error: 'HTTP 403 from the media segment',
      appVersion: 'Android 1.1.24',
      platform: 'Android 14',
    }),
  );
  assert.equal(url.origin, 'https://github.com');
  assert.equal(url.pathname, '/cgyegcvcecvoc/PremiumTV/issues/new');
  assert.match(url.searchParams.get('title'), /BBC America/);
  assert.match(url.searchParams.get('title'), /server 2 of 3/);
  const body = url.searchParams.get('body');
  assert.match(body, /\*\*Channel:\*\* BBC America/);
  assert.match(body, /\*\*Category:\*\* Entertainment/);
  assert.match(body, /example\.test\/live/);
  assert.match(body, /HTTP 403 from the media segment/);
  assert.match(body, /Android 1\.1\.24/);
  assert.match(body, /### Channel report\n\n\*\*Channel:\*\*/);
  assert.match(body, /\n\n\*\*What the player reported:\*\*/);
});

test('a report without optional context stays useful and bounded', () => {
  const report = loadReport();
  const url = new URL(report.issueUrl({ name: 'A very long channel name ' + 'x'.repeat(200) }));
  assert.match(url.searchParams.get('title'), /Unknown channel|very long channel/);
  assert.ok(url.searchParams.get('body').length < 4300);
  assert.equal(report.serverPosition(undefined, undefined), 'unknown');
  assert.equal(report.serverPosition(0, 1), '1 of 1');
});

test('control characters and an oversized URL cannot break the form', () => {
  const report = loadReport();
  const url = new URL(
    report.issueUrl({
      channel: 'News\u0007 Channel',
      url: 'https://example.test/' + 'a'.repeat(5000),
      error: 'bad\u0000news',
    }),
  );
  assert.ok(!url.searchParams.get('body').includes('\u0007'));
  assert.ok(url.searchParams.get('body').length < 4300);
});
