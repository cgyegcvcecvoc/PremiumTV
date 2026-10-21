'use strict';

// Runs inside the actual packaged Electron app in CI, not a DOM mock.
const assert = require('node:assert/strict');
const { setTimeout: delay } = require('node:timers/promises');

module.exports = async function smokeTest(window, repository, proxy) {
  // executeJavaScript never answers while the renderer main thread is
  // blocked, so race every call: a wedged renderer must fail this gate in
  // seconds with a readable message, not hang the CI job for an hour.
  async function evalInPage(expression) {
    const pending = window.webContents.executeJavaScript(expression);
    pending.catch(() => {});
    return Promise.race([
      pending,
      delay(10000).then(() => {
        throw new Error(`renderer did not answer within 10s: ${expression}`);
      }),
    ]);
  }
  async function waitFor(expression) {
    const deadline = Date.now() + 45000;
    while (Date.now() < deadline) {
      if (await evalInPage(expression)) return;
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
  const count = await evalInPage("document.getElementById('foot-count').textContent");
  assert.ok(count.includes(`${repository.library.channels.length} channels`), count);
  assert.equal(await evalInPage('document.getElementById("player").hidden'), true);
  assert.equal(await evalInPage('Boolean(window.Hls && window.mpegts)'), true);

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

  // Watch a channel - the one click this gate never made before 1.0.9,
  // which is how the Android crash-on-watch shipped under a green gate.
  // The stream itself will not play in CI (the runner is geo-blocked or
  // the feed is dead); what must hold is the whole non-crash path: the
  // player opens over the browser, names the channel, reaches the spinner
  // or the honest error card, tucks into the side player and closes back.
  try {
    await checkPlayer(window, waitFor);
  } catch (error) {
    // Say what the renderer looked like when it failed: the Actions log is
    // not reachable from every sandbox, so this dump rides the build log.
    try {
      const dump = await evalInPage(`({
        playerHidden: document.getElementById('player')?.hidden,
        name: document.getElementById('player-name')?.textContent,
        spinner: document.getElementById('player-spinner')?.hidden,
        error: document.getElementById('player-error')?.hidden,
        mini: document.getElementById('player')?.classList.contains('mini'),
        cards: document.querySelectorAll('#channels-grid .card').length,
      })`);
      console.log(`PLAYER SMOKE STATE AT FAILURE: ${JSON.stringify(dump)}`);
    } catch (dumpError) {
      console.log(`PLAYER SMOKE STATE AT FAILURE: unreadable (${dumpError.message})`);
    }
    throw error;
  }

  async function checkPlayer(window, waitFor) {
  console.log('PLAYER SMOKE: clicking the first channel card');
  await evalInPage("document.querySelector('[data-tab=\"channels\"]').click()");
  await waitFor("document.querySelectorAll('#channels-grid .card').length > 0");
  await evalInPage("document.querySelector('#channels-grid .card').click()");
  await waitFor("document.getElementById('player').hidden === false");
  const playerName = await evalInPage(
    "document.getElementById('player-name').textContent");
  assert.ok(playerName.trim().length > 0, 'the player names the channel it opened');
  console.log(`PLAYER SMOKE: player open for '${playerName}', letting the stream machinery run`);
  await delay(3000);
  const playerState = await evalInPage(`({
    hidden: document.getElementById('player').hidden,
    spinning: !document.getElementById('player-spinner').hidden,
    errorShown: !document.getElementById('player-error').hidden,
    errorText: document.getElementById('player-error-text').textContent,
    readyState: document.getElementById('video').readyState,
    rendererAlive: document.querySelectorAll('#channels-grid .card').length > 0,
  })`);
  assert.equal(playerState.hidden, false, 'the player is still open after the stream machinery ran');
  assert.ok(
    playerState.spinning || playerState.errorShown || playerState.readyState > 0,
    `the player reached a sane state (${JSON.stringify(playerState)})`);
  assert.equal(playerState.rendererAlive, true, 'the browser behind the player is still rendered');
  console.log(`PLAYER SMOKE: settled state ${JSON.stringify(playerState)}; flipping the side player`);
  // The 1.0.8 side player flip, then a real close.
  await evalInPage("document.getElementById('player-minimize').click()");
  await waitFor("document.getElementById('player').classList.contains('mini')");
  await evalInPage("document.getElementById('player-minimize').click()");
  await waitFor("!document.getElementById('player').classList.contains('mini')");
  await evalInPage("document.getElementById('player-close').click()");
  await waitFor("document.getElementById('player').hidden === true");
  console.log(`PLAYER SMOKE PASS: opened '${playerName}', ` +
    `${playerState.errorShown ? 'reached the error card' : 'stream machinery sane'}, ` +
    'side-player flip and close all survived');
  }

  // The Guide tab: the cable-style grid on preview builds, the list on stable.
  const bundled = (await repository.bundledMeta()) || {};
  const cableGuide = Array.isArray(bundled.preview_features) && bundled.preview_features.includes('cable-guide');
  await evalInPage("document.querySelector('[data-tab=\"guide\"]').click()");
  let guide;
  if (cableGuide) {
    await waitFor("document.querySelectorAll('#guide-grid .cable-programme').length > 0");
    guide = await evalInPage(`({
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
