"use strict";
/* The Live Events clock, shared by the web player and the desktop apps.
 *
 * A kickoff is one instant, but "5:45 PM" only means something next to the
 * clock it is read on. These tests pin the rule the tab promises: one zone for
 * the clock, the cards, the countdowns and the summary, the device's own zone
 * unless the viewer picked another, and no crash on a stale saved name.
 */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const renderer = path.join(__dirname, "..", "..", "macos", "app", "src", "renderer");

function load(modules) {
  const context = vm.createContext({ console, Date, Set, Map, Intl, Number, String, Math, RegExp });
  context.window = context;
  context.setInterval = () => 0;
  context.clearInterval = () => {};
  for (const name of modules) {
    vm.runInContext(fs.readFileSync(path.join(renderer, name), "utf8"), context);
  }
  return context;
}

function loadClock() {
  const context = load(["live-events.js", "live-clock.js"]);
  return { clock: context.PremiumLiveClock, live: context.PremiumLive };
}

const AT = 1_795_464_000_000; // 2026-11-23 20:00 UTC: New York EST, Berlin GMT+1

test("a kickoff is said in the same zone as the clock", () => {
  const { live, clock } = loadClock();
  assert.equal(live.kickoffLabel(AT, "America/New_York"), "3:00 PM");
  assert.equal(live.kickoffStamp(AT, "Europe/Berlin"), "9:00 PM · GMT+1");
  assert.match(clock.clockLine(AT, "America/New_York", "Europe/Berlin"), /New York · GMT-5/);
});

test("an unknown saved zone falls back to the device instead of throwing", () => {
  const { live } = loadClock();
  assert.equal(live.resolveTimeZone("Mars/Olympus_Mons", "Europe/Berlin"), "Europe/Berlin");
  assert.equal(live.resolveTimeZone("", ""), "");
  assert.equal(live.deviceOffsetLabel(AT), "GMT+0");
});

test("the offset, the delta and the half-hour zones are read from the zone itself", () => {
  const { live } = loadClock();
  assert.equal(live.zoneOffset(AT, "America/New_York").label, "GMT-5");
  assert.equal(live.zoneOffset(AT, "Asia/Kolkata").label, "GMT+5:30");
  assert.ok(live.zoneOffset(AT, "Europe/Berlin").deltaMinutes > live.zoneOffset(AT, "America/New_York").deltaMinutes);
});

test("zones are offered from the saved market's longitude, device first", () => {
  const { clock } = loadClock();
  // -76.3 is Pennsylvania; 151.2 is Sydney, which the Pacific band carries.
  assert.equal(clock.bandForLongitude(-76.3055).id, "americas");
  assert.equal(clock.bandForLongitude(151.2).id, "pacific");
  assert.equal(clock.bandForLongitude(null), null);
  const zones = clock.suggestZones("Europe/Berlin", -76.3055).map((row) => row.zone);
  assert.equal(zones[0], "Europe/Berlin");
  assert.ok(zones.includes("America/New_York"));
  assert.equal(new Set(zones).size, zones.length);
  assert.ok(clock.suggestZones("America/Los_Angeles", null).length >= 3);
});

test("the next kickoff is the soonest one still ahead, and the summary names the clock", () => {
  const { clock } = loadClock();
  const now = AT;
  const events = [
    { kickoffMs: now - 600_000, title: "Started", sport: "Soccer" },
    { kickoffMs: null, title: "Unknown", sport: "Soccer" },
    { kickoffMs: now + 3_600_000, title: "Later", sport: "Soccer" },
    { kickoffMs: now + 1_200_000, title: "Sooner", sport: "Soccer" },
  ];
  assert.equal(clock.nextKickoff(events, now).title, "Sooner");
  const own = clock.summary(now, "", "Europe/Berlin", events);
  assert.match(own, /read in your clock, Berlin \(GMT\+1\)/);
  assert.match(own, /Next kickoff in 20:00: Sooner\./);
  const away = clock.summary(now, "America/New_York", "Europe/Berlin", []);
  assert.match(away, /not this device.s clock/);
});

test("a saved choice is honoured only when it still names a real zone", () => {
  const { clock } = loadClock();
  const store = new Map();
  const storage = {
    getItem: (key) => (store.has(key) ? store.get(key) : null),
    setItem: (key, value) => store.set(key, String(value)),
    removeItem: (key) => store.delete(key),
  };
  clock.saveChoice(storage, "Asia/Tokyo");
  assert.equal(clock.loadChoice(storage), "Asia/Tokyo");
  storage.setItem(clock.STORAGE_KEY, "Mars/Olympus_Mons");
  assert.equal(clock.loadChoice(storage), "");
  clock.saveChoice(storage, "");
  assert.equal(clock.loadChoice(storage), "");
  // A storage area that throws (private mode, a blocked origin) is survivable.
  const blocked = { getItem() { throw new Error("blocked"); }, setItem() { throw new Error("blocked"); }, removeItem() {} };
  assert.equal(clock.loadChoice(blocked), "");
  clock.saveChoice(blocked, "Europe/Paris");
});

test("the widget paints the clock, the picker and the note into its host", () => {
  const { clock } = loadClock();
  const created = [];
  function element(tag) {
    const node = {
      tagName: tag,
      children: [],
      dataset: {},
      attributes: {},
      classList: { values: new Set(), add(value) { this.values.add(value); }, toggle() {} },
      textContent: "",
      setAttribute(name, value) { this.attributes[name] = value; },
      removeAttribute(name) { delete this.attributes[name]; },
      append(...nodes) { this.children.push(...nodes); },
      set innerHTML(value) { this.children = []; this._html = value; },
      addEventListener(name, handler) { this._on = { name, handler }; },
      ownerDocument: null,
    };
    created.push(node);
    return node;
  }
  const doc = { createElement: element };
  const host = element("div");
  host.ownerDocument = doc;
  const picked = [];
  const widget = clock.mount(host, {
    deviceZone: "Europe/Berlin",
    storage: {
      getItem: () => null,
      setItem: () => {},
      removeItem: () => {},
    },
    getZone: () => "",
    setZone: (zone) => picked.push(zone),
    getLongitude: () => -76.3055,
    getEvents: () => [{ kickoffMs: Date.now() + 3_600_000, title: "Arsenal vs. Chelsea", sport: "Soccer" }],
  });
  const byRole = (role) => host.children.find((node) => node.dataset.liveClock === role);
  assert.ok(byRole("time").textContent.length >= 5, "the clock shows a time");
  assert.match(byRole("zone").textContent, /Berlin · GMT\+1/);
  assert.match(byRole("next").textContent, /^Next kickoff in /);
  assert.match(byRole("note").textContent, /are read in/);
  const picker = byRole("picker");
  assert.ok(picker.children.length > 1, "the picker lists the device zone first");
  assert.equal(picker.children[0].value, "");
  // Choosing a zone reports it and repaints through the same one.
  picker.value = "America/New_York";
  picker._on.handler();
  assert.deepEqual(picked, ["America/New_York"]);
  widget.refresh();
  widget.destroy();
});
