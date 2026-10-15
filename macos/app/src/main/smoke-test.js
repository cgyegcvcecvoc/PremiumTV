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

  // The Guide tab: the cable-style grid on preview builds, the list on stable.
  const bundled = (await repository.bundledMeta()) || {};
  const cableGuide = Array.isArray(bundled.preview_features) && bundled.preview_features.includes('cable-guide');
  await window.webContents.executeJavaScript("document.querySelector('[data-tab=\"guide\"]').click()");
  let guide;
  if (cableGuide) {
    await waitFor("document.querySelectorAll('#guide-grid .cable-programme').length > 0");
    guide = await window.webContents.executeJavaScript(`({
      ticks: document.querySelectorAll('#guide-grid .cable-header-row .cable-time-tick').length,
      rows: document.querySelectorAll('#guide-grid .cable-row:not(.cable-header-row)').length,
      shows: document.querySelectorAll('#guide-grid .cable-programme').length,
      nowLine: Boolean(document.querySelector('#guide-grid .cable-now-line')),
      list: document.getElementById('guide-list').hidden,
    })`);
    assert.equal(guide.ticks, 16, 'eight hours of half-hour times across the top');
    assert.ok(guide.rows > 0, 'channel rows down the left');
    assert.ok(guide.shows >= guide.rows, 'shows to the right of the channels');
    assert.equal(guide.nowLine, true);
    assert.equal(guide.list, true, 'the list view is replaced by the grid');
  } else {
    await waitFor("document.querySelectorAll('#guide-list .guide-row').length > 0");
    guide = { list: true };
  }
  // Screenshots for the build output, so the guide can be checked by eye.
  const shot = process.env.PREMIUMTV_SMOKE_SHOT;
  if (shot) {
    try {
      await delay(600);
      const image = await window.webContents.capturePage();
      if (!image.isEmpty()) {
        require('node:fs').writeFileSync(shot, image.toPNG());
        console.log(`saved ${shot}`);
      } else {
        console.log('capturePage returned an empty image; no screenshot saved');
      }
    } catch (error) {
      console.log(`screenshot skipped: ${error.message}`);
    }
  }
  console.log(`PACKAGED SMOKE PASS: ${repository.library.channels.length} channels, bridge, players, refresh, reset ` +
    `and the ${cableGuide ? `cable guide (${guide.rows} rows, ${guide.shows} shows)` : 'guide list'}`);
};
