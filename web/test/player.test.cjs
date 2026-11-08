"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const vm = require("node:vm");
const fs = require("node:fs");
const path = require("node:path");
function player() {
  const element = {
    canPlayType: () => "",
    addEventListener() {},
    removeAttribute() {},
    load() {},
    volume: 1,
    muted: false,
    audioTracks: [],
  };
  const elements = new Map([["video", element]]);
  const context = vm.createContext({
    console,
    Set,
    Map,
    Promise,
    Number,
    Boolean,
    Array,
    Object,
    setTimeout,
    clearTimeout,
    navigator: { userAgent: "test", platform: "test", maxTouchPoints: 0 },
    module: { exports: {} },
  });
  context.window = context;
  context.document = {
    getElementById: (id) => {
      if (!elements.has(id))
        elements.set(id, { hidden: false, textContent: "" });
      return elements.get(id);
    },
  };
  context.PremiumStore = {
    read: () => ({}),
    write() {},
    KEYS: { audio: "audio" },
  };
  vm.runInContext(
    fs.readFileSync(path.join(__dirname, "../src/player.js"), "utf8"),
    context,
  );
  return {
    plan: (...args) => Array.from(context.module.exports.plan(...args)),
  };
}
test("iPhone HLS starts natively even when ManagedMediaSource exists", () => {
  assert.deepEqual(
    player().plan("https://example.com/live.m3u8?token=1", true, true, true),
    ["native", "hls"],
  );
});
test("basic Safari without MSE can still play native HLS", () => {
  assert.deepEqual(
    player().plan("https://example.com/live.m3u8", true, true, false),
    ["native"],
  );
});
test("desktop HLS prefers MSE and retains native fallback", () => {
  assert.deepEqual(
    player().plan("https://example.com/live.m3u8", false, true, true),
    ["hls", "native"],
  );
});
test("MPEG-TS is not sent to an unsupported iOS MSE player", () => {
  assert.deepEqual(
    player().plan("http://example.com/live.ts", true, false, true),
    [],
  );
  assert.deepEqual(
    player().plan("http://example.com/live.ts", false, false, true),
    ["mpegts"],
  );
});
test("finite movies use native playback without loading a streaming library", () => {
  assert.deepEqual(
    player().plan("https://example.com/movie.mp4", false, true, true),
    ["native"],
  );
  assert.deepEqual(
    player().plan("https://example.com/movie.mp4", true, true, false),
    ["native"],
  );
});
test("extensionless feeds get native and HLS attempts, not a guessed CORS probe", () => {
  assert.deepEqual(
    player().plan("https://example.com/watch/123", false, true, true),
    ["native", "hls"],
  );
});
