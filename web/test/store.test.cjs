"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const store = require("../src/store.js");
const diagnostics = require("../src/diagnostics.js");

test("search normalizes accents and matches name, country, category and number", () => {
  const channel = {
    name: "☆ Cinéma Classics",
    country: "US",
    group: "Movies",
    chno: "42",
  };
  assert.equal(store.matches(channel, "cinema US 42"), true);
  assert.equal(store.matches(channel, "movies classics"), true);
  assert.equal(store.matches(channel, "weather"), false);
});
test("sorting never mutates the published library", () => {
  const channels = [
    { name: "Z", chno: "1" },
    { name: "A", chno: "9" },
  ];
  assert.equal(store.sortChannels(channels, "az")[0].name, "A");
  assert.equal(store.sortChannels(channels, "za")[0].name, "Z");
  assert.equal(store.sortChannels(channels, "number")[0].chno, "1");
  assert.equal(channels[0].name, "Z");
  const groups = [
    { name: "Z", count: 9 },
    { name: "A", count: 1 },
  ];
  assert.equal(store.sortGroups(groups, "big")[0].name, "Z");
  assert.equal(store.sortGroups(groups, "published")[0].name, "Z");
});
test("resume rejects corrupt/near-end positions and retains valid ones", () => {
  assert.equal(store.resumeAt(50, 100), 50);
  assert.equal(store.resumeAt(95, 100), 0);
  assert.equal(store.resumeAt(2, 100), 0);
  assert.equal(store.resumeAt("bad", 100), 0);
  assert.equal(store.resumeAt(-5, 100), 0);
});
test("sleep uses a wall-clock deadline", () => {
  assert.equal(store.sleepRemaining(90000, 30000), 60000);
  assert.equal(store.sleepRemaining(10000, 30000), 0);
  assert.equal(store.sleepLabel(5400000), "1 hr 30 min");
  assert.equal(store.sleepLabel(0), "Off");
});
test("incomplete and unsafe libraries fail before atomic publication", () => {
  const meta = { platform: "web", build_id: "abcdef0123456789" };
  const channels = [
    { name: "TV", url: "https://example.com/live.m3u8", group: "News" },
  ];
  const groups = [{ name: "News", count: 1 }];
  assert.equal(store.validateLibrary(meta, channels, groups), true);
  assert.throws(() => store.validateLibrary(meta, [], groups));
  assert.throws(() => store.validateLibrary({}, channels, groups));
  assert.throws(() =>
    store.validateLibrary(
      meta,
      [{ ...channels[0], url: "javascript:alert(1)" }],
      groups,
    ),
  );
});
test("11 diagnostics are honest about browser restrictions", () => {
  const library = {
    meta: { window_start: Date.now() / 1000 },
    channels: [
      {
        name: "TV",
        url: "http://example.com/live.m3u8",
        group: "News",
        ua: "Native",
      },
    ],
    groups: [{ name: "News", count: 1 }],
    programmes: [{ c: "tv", s: 1, e: 2 }],
  };
  const report = diagnostics.check(
    library,
    {
      nativeHls: true,
      mse: true,
      storage: false,
      serviceWorker: true,
      online: true,
    },
    Date.now(),
  );
  assert.equal(report.checks.length, 11);
  assert.equal(report.fail, 0);
  assert.ok(report.warn >= 3);
  assert.match(
    report.checks.find((c) => c.label === "Browser headers").detail,
    /cannot attach/,
  );
  assert.match(
    report.checks.find((c) => c.label === "Channel list").detail,
    /Playback is checked only when opened/,
  );
});
function loadShared(name, extra = {}) {
  const context = vm.createContext(
    Object.assign({ console, Date, Set, Map, Intl }, extra),
  );
  context.window = context;
  vm.runInContext(
    fs.readFileSync(
      path.join(__dirname, "../../macos/app/src/renderer", name),
      "utf8",
    ),
    context,
  );
  return context;
}
test("shared favorites, recents and server wrapping match the native app", () => {
  const { PremiumPersonal: p } = loadShared("personal.js");
  assert.equal(
    JSON.stringify(p.recordRecent(["a", "b"], "b")),
    JSON.stringify(["b", "a"]),
  );
  assert.equal(JSON.stringify(p.toggleFavorite(["a"], "a")), "[]");
  assert.equal(
    JSON.stringify(p.toggleFavorite([], "b")),
    JSON.stringify(["b"]),
  );
  assert.equal(p.nextServerIndex(2, 3, 1), 0);
  assert.equal(p.nextServerIndex(0, 3, -1), 2);
  assert.equal(p.recordRecent(["a"], "b", 1).length, 1);
});
test("shared event grouping deduplicates servers and keeps team identity", () => {
  const { PremiumLive: live } = loadShared("live-events.js");
  const channels = [
    {
      id: "Soccer.Dummy.us",
      name: "[Soccer] Alpha vs. Beta",
      url: "https://one.test/live.m3u8",
    },
    {
      id: "Soccer.Dummy.us",
      name: "[Soccer] Beta vs. Alpha",
      url: "https://two.test/live.m3u8",
    },
    {
      id: "Soccer.Dummy.us",
      name: "[Soccer] Alpha vs. Beta",
      url: "https://one.test/live.m3u8",
    },
  ];
  const sections = live.buildSections(channels);
  assert.equal(sections.length, 1);
  assert.equal(sections[0].events[0].servers.length, 2);
  assert.equal(live.serversFor(channels[1], channels)[0].url, channels[1].url);
});
test("failed-feed memory expires after seven days and can be restored", () => {
  const data = new Map();
  const storage = {
    getItem: (k) => data.get(k),
    setItem: (k, v) => data.set(k, v),
    removeItem: (k) => data.delete(k),
  };
  const { PremiumHealth: h } = loadShared("health.js");
  let dead = h.record(storage, "https://dead.test", 1000);
  assert.equal(dead.has("https://dead.test"), true);
  assert.equal(h.load(storage, 1000 + h.TTL_MS + 1).size, 0);
  assert.equal(h.clear(storage).size, 0);
});
