'use strict';

const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');

const crashLog = require('../src/main/crash-log');

function tempDir() {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'premiumtv-crash-'));
}

test('a written crash round-trips with its message and frames', () => {
  const dir = tempDir();
  const error = new Error('renderer went away');
  assert.equal(
    crashLog.writeCrash(
      dir,
      crashLog.formatCrash({ kind: 'Renderer gone', thread: 'renderer', message: error.message, stack: error.stack }),
    ),
    true,
  );

  const crash = crashLog.readCrash(dir);
  assert.ok(crash);
  assert.equal(crash.summary, 'Renderer gone: renderer went away');
  assert.equal(crash.thread, 'renderer');
  assert.ok(crash.frames.length > 0);
  assert.ok(crash.frames[0].includes('crash-log.test.js'));
});

test('no record reads as no crash', () => {
  assert.equal(crashLog.readCrash(tempDir()), null);
  assert.equal(crashLog.parseCrash(''), null);
  assert.equal(crashLog.parseCrash(null), null);
});

test('a truncated record still yields its summary', () => {
  const crash = crashLog.parseCrash('time=2026-11-20T12:00:00Z\nUncaught exception: out of memory\n');
  assert.ok(crash);
  assert.equal(crash.time, '2026-11-20T12:00:00Z');
  assert.equal(crash.summary, 'Uncaught exception: out of memory');
  assert.deepEqual(crash.frames, []);
});

test('clearing removes the record so an old crash stops showing', () => {
  const dir = tempDir();
  crashLog.writeCrash(dir, crashLog.formatCrash({ kind: 'Error', message: 'once' }));
  assert.ok(crashLog.readCrash(dir));

  assert.equal(crashLog.clearCrash(dir), true);
  assert.equal(crashLog.readCrash(dir), null);
  assert.equal(fs.existsSync(crashLog.crashFile(dir)), false);
  // Clearing again is harmless.
  assert.equal(crashLog.clearCrash(dir), true);
});

test('the described line names the error and the first frame', () => {
  const error = new Error('bad feed');
  const crash = crashLog.parseCrash(
    crashLog.formatCrash({ kind: 'Uncaught exception', message: error.message, stack: error.stack }),
  );
  const line = crashLog.describeCrash(crash);
  assert.ok(line.startsWith('Uncaught exception: bad feed'));
  assert.ok(line.length <= 220);
});
