'use strict';

// Runs inside the actual packaged Electron app in CI, not a DOM mock.
const assert = require('node:assert/strict');
const { setTimeout: delay } = require('node:timers/promises');

module.exports = async function smokeTest(window, repository, proxy) {
  async function waitFor(expression) {
    const deadline = Date.now() + 45000;
    while (Date.now() < deadline) {
      if (await window.webContents.executeJavaScript(expression)) return;
      await delay(100);
    }
    throw new Error(`Renderer timeout: ${expression}`);
  }
  await waitFor("Boolean(window.premiumtv && document.getElementById('foot-count').textContent.includes('0 channels'))");
  // Deliberately load AFTER the renderer has taken its empty startup snapshot.
  await repository.load();
  assert.equal(repository.state.phase, 'ready');
  assert.ok(repository.library.channels.length > 0);
  await waitFor("document.querySelectorAll('#channels-grid .card').length > 0");
  const count = await window.webContents.executeJavaScript("document.getElementById('foot-count').textContent");
  assert.ok(count.includes(`${repository.library.channels.length} channels`), count);
  assert.equal(await window.webContents.executeJavaScript('document.getElementById("player").hidden'), true);
  assert.equal(await window.webContents.executeJavaScript('Boolean(window.Hls && window.mpegts)'), true);

  // Prove a second state transition updates the library, not just the status.
  repository.library = {
    ...repository.library,
    channels: [{ ...repository.library.channels[0], name: 'CI refreshed channel' }],
    groups: [], programmes: [],
  };
  repository.emit('state', repository.state);
  await waitFor("document.querySelector('.card-name')?.textContent === 'CI refreshed channel'");
  await repository.resetToBundled();
  await waitFor("document.querySelectorAll('#channels-grid .card').length > 1");
  const response = await fetch(`${proxy.origin}/healthz`);
  assert.equal(response.status, 200);
  console.log(`PACKAGED SMOKE PASS: ${repository.library.channels.length} channels, bridge, players, refresh and reset`);
};
