"use strict";

/**
 * The web player uses the same bounded recovery policy as macOS, and the relay
 * rescue must not start a stale feed after the viewer switched channels while
 * an asynchronous `/open` request was in flight.
 */

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const WEB = path.join(__dirname, "..");
const ROOT = path.join(WEB, "..");

function loadShared(name) {
  const context = vm.createContext({ console, Date, Set, Map, Number, String, Boolean });
  context.window = context;
  vm.runInContext(
    fs.readFileSync(
      path.join(ROOT, "macos/app/src/renderer", name), "utf8"), context);
  return context;
}

test("the web build ships the shared recovery policy before the player", () => {
  const html = fs.readFileSync(path.join(WEB, "src/index.html"), "utf8");
  const build = fs.readFileSync(path.join(WEB, "tools/build.py"), "utf8");
  assert.match(build, /"playback-recovery\.js"/);
  assert.match(html, /<script defer src="shared\/playback-recovery\.js"><\/script>/);
  assert.ok(html.indexOf("shared/playback-recovery.js") < html.indexOf('src="player.js"'));
});

test("the shared policy retries transient and media faults but not provider decisions", () => {
  const { PremiumRecovery: policy } = loadShared("playback-recovery.js");
  assert.equal(policy.TRANSIENT_LIMIT, 2);
  assert.equal(policy.MEDIA_LIMIT, 1);
  assert.equal(policy.classifyFault({ response: { code: 404 } }), "permanent");
  assert.equal(policy.classifyFault({ code: 3 }), "media");
  assert.equal(policy.classifyFault({ details: "fragLoadError" }), "transient");
  assert.equal(policy.decideRecovery("transient", 0, false).retryInPlace, true);
  assert.equal(policy.decideRecovery("transient", 2, false).retryInPlace, false);
  assert.equal(policy.decideRecovery("media", 1, false).retryInPlace, false);
  assert.equal(policy.decideRecovery("permanent", 0, false).retryInPlace, false);
  assert.equal(policy.decideRecovery("transient", 0, true).retryInPlace, false);
});

test("a failed feed is classified and a retry keeps its fatal handler", () => {
  const app = fs.readFileSync(path.join(WEB, "src/app.js"), "utf8");
  const player = fs.readFileSync(path.join(WEB, "src/player.js"), "utf8");
  assert.match(app, /recovery\.decideRecovery\(recovery\.classifyFault\(fault\), used, serverIndex > 0\)/);
  assert.match(app, /feedRetries\.set\(source\.url, used \+ 1\)/);
  assert.match(player, /if \(handler\) handler\(lastFault\);/);
  assert.match(player, /this\.play\(url, hint, channel, lastHandlers \|\| \{\}\);/);
});

test("an async relay rescue cannot overwrite a newer player choice", () => {
  const app = fs.readFileSync(path.join(WEB, "src/app.js"), "utf8");
  assert.match(app, /const serial = \+\+playerSerial;/);
  assert.match(app, /const opened = await relay\.open\(source, relayConfig\);\s*\n\s*\/\/[\s\S]*?if \(serial !== playerSerial\) return;/);
  assert.match(app, /onFatal: \(fault\) => \{\s*\n\s*if \(serial !== playerSerial\) return;/);
  assert.match(app, /onState: \(info\) => \{\s*\n\s*if \(serial !== playerSerial\) return;/);
  assert.match(app, /onProgress: \(seconds, duration\) => \{\s*\n\s*if \(serial !== playerSerial\) return;/);
});

test("every exhausted server is remembered and healthy feeds lead the next walk", () => {
  const app = fs.readFileSync(path.join(WEB, "src/app.js"), "utf8");
  const health = loadShared("health.js").PremiumHealth;
  assert.match(app, /health\.recordMany\(S\.storage, queue\.map\(\(c\) => c\.url\)\)/);
  assert.match(app, /health\.healthyServersFirst\(unique, dead\)/);
  const storage = (() => {
    const data = new Map();
    return {
      getItem: (key) => data.get(key),
      setItem: (key, value) => data.set(key, String(value)),
      removeItem: (key) => data.delete(key),
    };
  })();
  const dead = health.recordMany(storage, ["a", "b"], 1000);
  assert.deepEqual(
    health.healthyServersFirst([{ url: "a" }, { url: "c" }, { url: "b" }], dead)
      .map((item) => item.url),
    ["c", "a", "b"],
  );
});
