"use strict";
/* The web edition answers the same local-channel question as the native apps,
 * from the same bundled directory, using the same shared logic. These tests
 * pin the fallback chain (location -> ZIP -> state -> city -> country) and the
 * guarantee that no national channel is mistaken for a local one. */
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const directory = JSON.parse(
  fs.readFileSync(path.join(__dirname, "..", "..", "playlists", "local-channels.json"), "utf8"),
);
const source = fs.readFileSync(
  path.join(__dirname, "..", "..", "macos", "app", "src", "renderer", "local-channels.js"),
  "utf8",
);

function loadLocal() {
  const sandbox = { window: {}, console };
  sandbox.globalThis = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox);
  return sandbox.window.PremiumLocalChannels;
}

function memoryStorage(initial) {
  const data = new Map(Object.entries(initial || {}));
  return {
    getItem: (key) => (data.has(key) ? data.get(key) : null),
    setItem: (key, value) => data.set(key, String(value)),
    removeItem: (key) => data.delete(key),
  };
}

const local = loadLocal();

test("the bundled directory is schema 2 with markets, states and a ZIP table", () => {
  assert.equal(directory.schema, 2);
  assert.ok(directory.markets.length >= 80);
  assert.ok(directory.states.length >= 30);
  assert.ok(directory.zip_ranges.length >= 50, "the USPS 3-digit ranges are bundled");
  assert.ok(directory.zip_prefixes.length > 500, "the ZIP prefix table is bundled");
  const lancaster = directory.markets.find((market) => market.id === "USLNS");
  assert.ok(lancaster, "Lancaster, PA is the market that serves WGAL");
  assert.ok(lancaster.stations.some((station) => station.callsign === "WGAL"));
});

test("a ZIP resolves to its market and its state", () => {
  assert.equal(local.stateForZip("17601", directory), "PA");
  const market = local.marketForZip("17603", directory);
  assert.equal(market.city, "Lancaster");
  assert.equal(market.state, "PA");
  assert.equal(market.stations[0].callsign, "WGAL");
  assert.equal(local.stateForZip("10001", directory), "NY");
  assert.equal(local.stateForZip("90210", directory), "CA");
  assert.equal(local.stateForZip("00000", directory), "");
});

test("a location fix picks the nearest published market, never a far one", () => {
  // Lancaster, PA
  const market = local.nearestMarket(40.0379, -76.3055, directory);
  assert.equal(market.state, "PA");
  assert.ok(["Lancaster", "Harrisburg", "York", "Philadelphia"].includes(market.city));
  // A fix in the Atlantic is not a market; the caller gets null, not a guess.
  assert.equal(local.nearestMarket(0, 0, directory, "ZZ"), null);
});

test("the fallback chain ends in a plain sentence for an unpublishable answer", () => {
  // No answer yet is the default `country: US` selection, so the first thing
  // the viewer sees is what the whole shelf holds, not an error.
  assert.match(local.summary(directory, { country: "US" }), /local stations in/);
  assert.match(
    local.summary(directory, { country: "US", city: "Nowhere" }),
    /No local station is published in Nowhere/,
  );
  assert.match(local.summary(null, { country: "US" }), /not bundled/);
  assert.match(local.summary(directory, { country: "GB" }), /United States/);
  assert.match(
    local.summary(directory, { country: "US", zip: "00000" }),
    /not in the published US ZIP table/,
  );
  const selected = local.summary(directory, { country: "US", state: "PA" });
  assert.match(selected, /local station/);
  assert.match(selected, /Lancaster|Philadelphia|Pittsburgh/);
});

test("only real local stations are picked out of the national library", () => {
  // Identity is the published EPG id first and the stream URL second.
  const library = [
    { name: "History Channel", group: "A&E Networks", id: "History.us@East", url: "https://x/h" },
    { name: "WGAL 8", group: "Local", id: "NBC.us@WGAL", url: "https://x/wgal" },
    { name: "Telemundo 62", group: "Local", id: "Telemundo.us@WCAU", url: "https://x/wcau" },
  ];
  const pa = local.channelsFor(library, directory, { country: "US", state: "PA" });
  const names = pa.map((channel) => channel.name);
  // Arrays come back across the VM realm, so compare by value.
  assert.deepEqual([...names].sort(), ["Telemundo 62", "WGAL 8"]);
  assert.ok(!names.includes("History Channel"));
  assert.equal(local.channelsFor(library, directory, { country: "US", zip: "17601" })[0].name, "WGAL 8");
  // A backup feed still resolves to its station through its URL.
  const backup = local.channelsFor(
    [
      {
        name: "WGAL 8 (Backup 1)",
        group: "Local Backups",
        id: "",
        url: "https://aegis-cloudfront-1.tubi.video/5d314174-0110-42af-8811-feaae073ea1e/playlist.m3u8",
      },
    ],
    directory,
    { country: "US", zip: "17601" },
  );
  assert.equal(backup.length, 1);
});

test("the answer is stored in this browser and can be cleared", () => {
  const storage = memoryStorage();
  assert.equal(local.hasSelection(local.load(storage)), false);
  local.save(storage, { country: "us", state: "pa", city: "Lancaster", zip: "17601" });
  const saved = local.load(storage);
  assert.equal(saved.country, "US");
  assert.equal(saved.state, "PA");
  assert.equal(saved.zip, "17601");
  assert.equal(local.label(saved), "Lancaster, PA");
  assert.equal(local.asked(storage), true);
  storage.removeItem(local.SELECTION_KEY);
  storage.removeItem(local.ASKED_KEY);
  assert.equal(local.hasSelection(local.load(storage)), false);
  assert.equal(local.asked(storage), false);
});

test("the web build ships the directory and the shared module", () => {
  const root = path.join(__dirname, "..", "..");
  const web = fs.readFileSync(path.join(__dirname, "..", "src", "app.js"), "utf8");
  const html = fs.readFileSync(path.join(__dirname, "..", "src", "index.html"), "utf8");
  const build = fs.readFileSync(path.join(__dirname, "..", "tools", "build.py"), "utf8");
  assert.match(html, /shared\/local-channels\.js/);
  assert.match(html, /id="local-zip"/);
  assert.match(build, /local-channels\.json/);
  assert.match(build, /"local-channels\.js"/);
  assert.match(web, /data\/local-channels\.json/);
  assert.match(web, /function localFromLocation\(\)/);
  assert.ok(fs.existsSync(path.join(root, "playlists", "local-channels.json")));
});
