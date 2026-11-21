'use strict';

/**
 * The macOS crash record.
 *
 * The Mac app had no record of a fatal error at all: a crash in the main
 * process, or a renderer that was killed, left nothing behind. This writes the
 * same device-local `last-crash.txt` the Android app writes, so Settings →
 * Check for bugs can show the class, message and stack and the viewer can clear
 * it. Nothing is uploaded and no identifier is stored.
 */

const fs = require('node:fs');
const path = require('node:path');

const FILE_NAME = 'last-crash.txt';
const MAX_FRAMES = 24;

function crashFile(dir) {
  return path.join(dir, FILE_NAME);
}

/** The record's text, in the one shape readCrash() understands. */
function formatCrash({ kind, thread, message, stack, time } = {}) {
  const lines = [];
  lines.push(`time=${time || new Date().toISOString()}`);
  if (thread) lines.push(`thread=${thread}`);
  lines.push(`${kind || 'Error'}: ${message || '(no message)'}`);
  // Only stack frames: the first line of an Error.stack is the error itself,
  // which is already written as the summary above.
  const frames = String(stack || '')
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('at '))
    .slice(0, MAX_FRAMES);
  for (const frame of frames) lines.push(`  ${frame}`);
  return `${lines.join('\n')}\n`;
}

/** Writes the record. Never throws: a dying process must still exit. */
function writeCrash(dir, detail) {
  try {
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(crashFile(dir), detail);
    return true;
  } catch (_) {
    return false;
  }
}

/**
 * Parses the stored record, or returns null when there is none.
 *
 * Tolerant by design: the file is written by a process that is already
 * failing, so a truncated record still yields whatever was saved.
 */
function parseCrash(text) {
  if (!text || !String(text).trim()) return null;
  const lines = String(text)
    .split('\n')
    .filter((line) => line.trim());
  if (!lines.length) return null;
  const value = (prefix) => {
    const line = lines.find((entry) => entry.startsWith(prefix));
    return line ? line.slice(prefix.length).trim() : '';
  };
  const frames = lines
    .filter((line) => line.trimStart().startsWith('at '))
    .map((line) => line.trim())
    .slice(0, MAX_FRAMES);
  const summaryLine = lines.find(
    (line) =>
      !line.startsWith('time=') &&
      !line.startsWith('thread=') &&
      !line.trimStart().startsWith('at '),
  );
  const summary = summaryLine ? summaryLine.trim() : '';
  if (!summary && !frames.length) return null;
  return {
    time: value('time='),
    thread: value('thread='),
    summary: summary || 'The app stopped unexpectedly',
    frames,
    text: String(text),
  };
}

function readCrash(dir) {
  try {
    return parseCrash(fs.readFileSync(crashFile(dir), 'utf8'));
  } catch (_) {
    return null;
  }
}

/** Deletes the record so an old crash stops being reported. */
function clearCrash(dir) {
  try {
    fs.rmSync(crashFile(dir), { force: true });
    return true;
  } catch (_) {
    return false;
  }
}

/** The one-line shape Settings shows next to the record. */
function describeCrash(crash) {
  if (!crash) return '';
  const parts = [crash.summary];
  if (crash.frames && crash.frames.length) parts.push(crash.frames[0]);
  if (crash.time) parts.push(crash.time);
  const line = parts.filter(Boolean).join(' · ').replace(/\s+/g, ' ').trim();
  return line.length <= 220 ? line : `${line.slice(0, 217)}…`;
}

module.exports = {
  FILE_NAME,
  MAX_FRAMES,
  crashFile,
  formatCrash,
  parseCrash,
  writeCrash,
  readCrash,
  clearCrash,
  describeCrash,
};
