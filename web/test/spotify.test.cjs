"use strict";

/**
 * Spotify in PremiumTV.
 *
 * The important assertions here are the ones that keep the feature honest: the
 * signed-in path is the official PKCE flow, the embed is Spotify's own player,
 * and nothing in the module pretends to remove advertising. The rest pins the
 * link parsing, which is where a pasted URL either becomes a working player or
 * an empty frame.
 */

const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const crypto = require("node:crypto");

const ROOT = path.join(__dirname, "..", "..");
const SOURCE = path.join(ROOT, "macos", "app", "src", "renderer", "spotify.js");

function load() {
  const context = vm.createContext({
    console,
    URL,
    URLSearchParams,
    TextEncoder,
    Uint8Array,
    JSON,
    Date,
    Math,
    Promise,
    String,
    Number,
    Boolean,
    Array,
    Object,
    Set,
    RegExp,
    Error,
    btoa: (value) => Buffer.from(value, "binary").toString("base64"),
    // Deliberately absent: window.crypto. The module takes crypto as an
    // argument so this loader can supply it explicitly, exactly like a host
    // would.
    crypto: {
      getRandomValues(array) {
        const bytes = crypto.randomBytes(array.length);
        array.set(bytes);
        return array;
      },
      subtle: crypto.webcrypto.subtle,
    },
  });
  context.window = context;
  vm.runInContext(fs.readFileSync(SOURCE, "utf8"), context);
  return context.PremiumSpotify;
}

/** Compare data, not realm: the module's literals come from a vm context. */
function same(received, expected, message) {
  assert.deepEqual(JSON.parse(JSON.stringify(received)), expected, message);
}

function memoryStorage(seed) {
  const map = new Map(Object.entries(seed || {}));
  return {
    getItem: (key) => (map.has(key) ? map.get(key) : null),
    setItem: (key, value) => map.set(key, String(value)),
    removeItem: (key) => map.delete(key),
    _map: map,
  };
}

test("the module is shared by every host, not copied per platform", () => {
  const build = fs.readFileSync(path.join(ROOT, "web", "tools", "build.py"), "utf8");
  assert.match(build, /"spotify\.js"/, "web build must copy the shared module");
  const webHtml = fs.readFileSync(path.join(ROOT, "web", "src", "index.html"), "utf8");
  assert.ok(webHtml.includes('src="shared/spotify.js"'), "web page must load the shared module");
  const macHtml = fs.readFileSync(
    path.join(ROOT, "macos", "app", "src", "renderer", "index.html"), "utf8");
  assert.ok(macHtml.includes('src="spotify.js"'), "desktop renderer must load the module");
  const android = fs.readFileSync(
    path.join(ROOT, "android", "app", "src", "main", "assets", "premiumtv", "index.html"), "utf8");
  assert.ok(android.includes('src="spotify.js"'), "TV shell must load the module");
  // The APK copy is a byte-for-byte copy, checked in CI by
  // scripts/sync_spotify_assets.py --check; this catches it earlier.
  const packaged = fs.readFileSync(
    path.join(ROOT, "android", "app", "src", "main", "assets", "premiumtv", "spotify.js"), "utf8");
  assert.equal(packaged, fs.readFileSync(SOURCE, "utf8"), "the TV copy must be the shared module");
  // And the desktop renderer must actually use it, not just load it.
  const desktop = fs.readFileSync(
    path.join(ROOT, "macos", "app", "src", "renderer", "app.js"), "utf8");
  assert.match(desktop, /PremiumSpotify/);
  assert.match(desktop, /data-tab="spotify"|renderSpotify\(\)/);
});

test("link parsing accepts every Spotify share form", () => {
  const S = load();
  const cases = [
    ["https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M?si=abc123", "playlist", "37i9dQZF1DXcBWIGoYBM5M"],
    ["https://open.spotify.com/intl-de/album/4aawyAB9vmqN3uQ7FjRGTy", "album", "4aawyAB9vmqN3uQ7FjRGTy"],
    ["https://open.spotify.com/embed/track/79e0IMV7d0IgXrKQmCPspS", "track", "79e0IMV7d0IgXrKQmCPspS"],
    ["open.spotify.com/show/4rOoJ6Egrf8K2IrywzwOMk", "show", "4rOoJ6Egrf8K2IrywzwOMk"],
    ["spotify:playlist:37i9dQZF1DWWQRwui0ExPn", "playlist", "37i9dQZF1DWWQRwui0ExPn"],
    ["spotify:user:spotify:playlist:37i9dQZF1DX4sWSpwq3LiO", "playlist", "37i9dQZF1DX4sWSpwq3LiO"],
  ];
  for (const [input, type, id] of cases) {
    const parsed = S.parseLink(input);
    assert.ok(parsed, "should parse " + input);
    assert.equal(parsed.type, type, input);
    assert.equal(parsed.id, id, input);
    assert.equal(parsed.uri, "spotify:" + type + ":" + id);
    assert.equal(parsed.openUrl, "https://open.spotify.com/" + type + "/" + id);
    assert.match(parsed.embedUrl, /^https:\/\/open\.spotify\.com\/embed\//);
  }
});

test("link parsing refuses anything that is not a Spotify item", () => {
  const S = load();
  assert.equal(S.parseLink("https://example.com/playlist/37i9dQZF1DXcBWIGoYBM5M"), null);
  assert.equal(S.parseLink("https://open.spotify.com/genre/party"), null);
  assert.equal(S.parseLink("hello"), null);
  assert.equal(S.parseLink(""), null);
  // An id with characters that could break out of an attribute is refused
  // outright rather than sanitized: nothing invalid reaches an iframe src.
  const injected = S.parseLink('https://open.spotify.com/playlist/"><script>');
  assert.equal(injected.id, "", "nothing invalid may reach an iframe src");
  assert.match(injected.error, /not a Spotify/);
  const short = S.parseLink("https://spotify.link/abc123");
  assert.equal(short.type, "shortlink");
  assert.equal(short.id, "");
});

test("the embed is Spotify's official player, dark, and carries no ad logic", () => {
  const S = load();
  const url = S.embedUrl("playlist", "37i9dQZF1DXcBWIGoYBM5M");
  assert.equal(url, "https://open.spotify.com/embed/playlist/37i9dQZF1DXcBWIGoYBM5M?utm_source=generator&theme=0");
  assert.ok(S.embedUrl("playlist", "37i9dQZF1DXcBWIGoYBM5M", { compact: true }).endsWith("&view=coverart"));

  // The module must not carry anything that names, filters, mutes or skips
  // advertising. This is a product boundary, so it is asserted, not assumed.
  const source = fs.readFileSync(SOURCE, "utf8").toLowerCase();
  for (const forbidden of [
    "skipad", "blockad", "mutead", "stripad", "removead", "hidead",
    "adbreak", "adslot", "adbanner", "adsendpoint", "nomute", "filtercast",
  ]) {
    assert.equal(source.includes(forbidden), false, "must not implement " + forbidden);
  }
  // And no CSS/DOM surgery that could hide Spotify's ad slots in the frame.
  assert.equal(/style\.(display|visibility)|innerHTML\s*=/.test(source), false);
  // The one honest statement about ads is present and does not promise blocking.
  assert.match(S.NOTICE, /does not block, mute or skip/);
});

test("the curated shelf is real playlist ids, deduplicated and typed", () => {
  const S = load();
  assert.ok(S.CURATED.length >= 4);
  const seen = new Set();
  for (const entry of S.CURATED) {
    assert.match(entry.id, /^[A-Za-z0-9]{22}$/, entry.name + " needs a real 22-character id");
    assert.ok(!seen.has(entry.id), "duplicate " + entry.id);
    seen.add(entry.id);
    assert.equal(entry.type, "playlist");
    assert.ok(entry.name && entry.note, "every card needs a name and a note");
  }
  const library = S.library(S.defaultSettings());
  assert.equal(library.length, S.CURATED.length);
  assert.equal(library[0].curated, true);
});

test("the viewer's own links are stored, normalized and capped", () => {
  const S = load();
  const settings = S.normalizeSettings({
    clientId: "  abc123def456  ",
    custom: [
      { link: "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U", name: "Road trip" },
      { link: "https://open.spotify.com/playlist/37i9dQZF1DWXRqgorJj26U" },
      { link: "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" },
      { link: "not a link" },
    ],
    lastId: "37i9dQZF1DXbITWG1ZJKYt",
    autoTransfer: false,
  });
  assert.equal(settings.clientId, "abc123def456");
  assert.equal(settings.autoTransfer, false);
  // An unparseable entry is dropped at the door; a viewer link that repeats a
  // curated playlist is kept (it is their save) and de-duplicated at display.
  assert.equal(settings.custom.length, 3, "the invalid link is dropped, the valid ones stay");
  assert.equal(settings.custom[0].name, "Road trip");
  assert.equal(settings.custom[1].name, "Playlist", "an unnamed link still gets a readable label");
  assert.equal(settings.lastId, "37i9dQZF1DXbITWG1ZJKYt");

  // The curated list wins over a viewer entry with the same id.
  const library = S.library(settings);
  const dupes = library.filter((row) => row.id === "37i9dQZF1DXcBWIGoYBM5M");
  assert.equal(dupes.length, 1);
  assert.equal(dupes[0].curated, true);
});

test("a saved link survives the round trip back through the shelf", () => {
  const S = load();
  const storage = memoryStorage();
  const session = S.Session({
    storage,
    fetch: async () => ({ ok: true, status: 200, text: async () => "{}" }),
  });
  // A pinning regression: normalizeSettings() re-reads its own output on every
  // save, and once treated a stored {type,id,name} as if it were a pasted URL,
  // which dropped the viewer's link the next time the tab rendered.
  session.saveSettings({
    custom: [{ type: "album", id: "4aawyAB9vmqN3uQ7FjRGTy", name: "Midnights" }],
    lastId: "4aawyAB9vmqN3uQ7FjRGTy",
  });
  const saved = session.settings();
  assert.equal(saved.custom.length, 1);
  const rows = S.library(saved);
  assert.ok(rows.some((row) => row.id === "4aawyAB9vmqN3uQ7FjRGTy" && row.name === "Midnights" && !row.curated));
  // A second save must not lose it either.
  session.saveSettings({ lastId: saved.custom[0].id });
  assert.equal(session.settings().custom.length, 1);
});

test("a viewer's link that repeats a curated playlist does not duplicate the card", () => {
  const S = load();
  const rows = S.library({ custom: [{ type: "playlist", id: "37i9dQZF1DWXRqgorJj26U", name: "Mine" }] });
  const matches = rows.filter((row) => row.id === "37i9dQZF1DWXRqgorJj26U");
  assert.equal(matches.length, 1);
  assert.equal(matches[0].curated, true, "Spotify's own card keeps the name");
});

test("PKCE signs in with S256 and a verifier the tests can verify", async () => {
  const S = load();
  const verifier = S.randomString(96);
  assert.equal(verifier.length, 96);
  assert.match(verifier, /^[A-Za-z0-9\-._~]+$/);
  const challenge = await S.challengeFor(verifier);
  assert.match(challenge, /^[A-Za-z0-9\-_]{43}$/, "base64url of a SHA-256 digest is 43 chars");
  const expected = crypto
    .createHash("sha256")
    .update(verifier)
    .digest("base64")
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
  assert.equal(challenge, expected);

  const url = S.authorizeUrl({
    clientId: "client-id",
    redirectUri: "https://cgyegcvcecvoc.github.io/PremiumTV/web/",
    challenge,
    state: "state-1",
  });
  assert.ok(url.startsWith("https://accounts.spotify.com/authorize?"));
  const query = new URL(url).searchParams;
  assert.equal(query.get("code_challenge_method"), "S256");
  assert.equal(query.get("code_challenge"), challenge);
  assert.equal(query.get("response_type"), "code");
  assert.equal(query.get("client_id"), "client-id");
  assert.equal(query.get("state"), "state-1");
  // No secret ever travels with a public client.
  assert.equal(query.get("client_secret"), null);
  assert.match(query.get("scope"), /streaming/);
  assert.match(query.get("scope"), /user-read-private/);
});

test("the redirect is read from a query or a fragment, and errors surface", () => {
  const S = load();
  same(S.parseRedirect("https://x.test/?code=abc&state=s1"), { code: "abc", state: "s1", error: "" });
  same(S.parseRedirect("https://x.test/#code=abc&state=s1"), { code: "abc", state: "s1", error: "" });
  same(S.parseRedirect("?code=abc&state=s1"), { code: "abc", state: "s1", error: "" });
  assert.equal(S.parseRedirect("#error=access_denied").error, "access_denied");
  same(S.parseRedirect(""), { code: "", state: "", error: "" });
});

test("token bodies are form-encoded, as the token endpoint requires", () => {
  const S = load();
  const exchange = S.codeExchange({
    code: "the code",
    redirectUri: "https://x.test/",
    clientId: "id",
    verifier: "v-1",
  });
  assert.equal(exchange.url, "https://accounts.spotify.com/api/token");
  const params = new URLSearchParams(exchange.body);
  assert.equal(params.get("grant_type"), "authorization_code");
  assert.equal(params.get("code_verifier"), "v-1");
  assert.equal(params.get("redirect_uri"), "https://x.test/");
  assert.equal(params.get("client_secret"), null);

  const refresh = new URLSearchParams(S.refreshRequest({ refreshToken: "r", clientId: "id" }).body);
  assert.equal(refresh.get("grant_type"), "refresh_token");
  assert.equal(refresh.get("refresh_token"), "r");
});

test("a session refreshes an expiring token exactly once and keeps its refresh token", async () => {
  const S = load();
  const storage = memoryStorage({
    [S.KEYS.SETTINGS_KEY]: JSON.stringify({ clientId: "id", custom: [] }),
    [S.KEYS.TOKENS_KEY]: JSON.stringify({
      accessToken: "old",
      refreshToken: "refresh-1",
      expiresAt: 1000,
      scope: S.SCOPES,
    }),
  });
  let clock = 2000;
  const calls = [];
  const session = S.Session({
    storage,
    now: () => clock,
    fetch: async (url, init) => {
      calls.push({ url, init });
      if (url === S.TOKEN_URL) {
        return {
          ok: true,
          status: 200,
          text: async () => JSON.stringify({ access_token: "new", expires_in: 3600 }),
        };
      }
      return {
        ok: true,
        status: 200,
        text: async () => JSON.stringify({ id: "me", display_name: "Viewer", product: "premium" }),
      };
    },
  });

  assert.equal(session.signedIn(), true);
  const access = await session.token();
  assert.equal(access, "new");
  assert.equal(calls.filter((call) => call.url === S.TOKEN_URL).length, 1);
  const params = new URLSearchParams(calls[0].init.body);
  assert.equal(params.get("refresh_token"), "refresh-1");
  // The rotated refresh token would be absent from this response; the original
  // must survive, or the next launch cannot sign in.
  assert.equal(JSON.parse(storage.getItem(S.KEYS.TOKENS_KEY)).refreshToken, "refresh-1");
  // A still-fresh token is reused without another round trip.
  clock += 1000;
  assert.equal(await session.token(), "new");
  assert.equal(calls.filter((call) => call.url === S.TOKEN_URL).length, 1);
});

test("an API 401 refreshes and retries once, then reports plainly", async () => {
  const S = load();
  const storage = memoryStorage({
    [S.KEYS.SETTINGS_KEY]: JSON.stringify({ clientId: "id" }),
    [S.KEYS.TOKENS_KEY]: JSON.stringify({
      accessToken: "expired", refreshToken: "refresh-1", expiresAt: Date.now() + 3600_000,
    }),
  });
  let playerCalls = 0;
  const session = S.Session({
    storage,
    fetch: async (url) => {
      if (url === S.TOKEN_URL) {
        return { ok: true, status: 200, text: async () => JSON.stringify({ access_token: "fresh" }) };
      }
      playerCalls += 1;
      if (playerCalls === 1) {
        return {
          ok: false,
          status: 401,
          text: async () => JSON.stringify({ error: { status: 401 } }),
        };
      }
      return { ok: true, status: 200, text: async () => JSON.stringify({ devices: [] }) };
    },
  });
  same(await session.devices(), []);
  assert.equal(playerCalls, 2);
});

test("Spotify's Premium rule is explained, never worked around", async () => {
  const S = load();
  const storage = memoryStorage({
    [S.KEYS.SETTINGS_KEY]: JSON.stringify({ clientId: "id" }),
    [S.KEYS.TOKENS_KEY]: JSON.stringify({ accessToken: "a", refreshToken: "r", expiresAt: Date.now() + 3600_000 }),
  });
  const session = S.Session({
    storage,
    fetch: async () => ({
      ok: false,
      status: 403,
      text: async () => JSON.stringify({ error: { status: 403, message: "Player command failed: Premium required" } }),
    }),
  });
  await assert.rejects(() => session.play("device", { type: "playlist", id: "37i9dQZF1DXcBWIGoYBM5M" }), (error) => {
    assert.match(error.message, /Spotify Premium account/);
    assert.match(error.message, /Spotify's rule|Spotify\u2019s rule/);
    return true;
  });
  // explain() adds the fallback the UI offers instead of implying a bypass.
  const friendly = S.explain(new Error("In-app playback needs a Spotify Premium account."));
  assert.match(friendly, /embed/);
});

test("sign-in state is verified, so a forged redirect cannot complete a session", async () => {
  const S = load();
  const storage = memoryStorage({ [S.KEYS.SETTINGS_KEY]: JSON.stringify({ clientId: "id" }) });
  const session = S.Session({
    storage,
    fetch: async () => ({ ok: true, status: 200, text: async () => JSON.stringify({ access_token: "a" }) }),
  });
  await assert.rejects(
    () => session.complete("https://x.test/?code=abc&state=forged"),
    /state was lost|did not match/,
  );
});

test("a window with no storage still signs in for the session, and says so", () => {
  const S = load();
  // The apps can run where localStorage does not exist or throws on touch.
  const session = S.Session({ storage: undefined, fetch: async () => ({ ok: true, status: 200, text: async () => "{}" }) });
  assert.equal(session.signedIn(), false, "a fresh session with no token is still signed out");
  session.saveSettings({ clientId: "id", custom: [{ type: "album", id: "4aawyAB9vmqN3uQ7FjRGTy", name: "One" }] });
  // The in-memory fallback keeps the answer for this session instead of throwing.
  assert.equal(session.settings().clientId, "id");
  assert.equal(session.settings().custom.length, 1);
  // Throwing storage is treated the same way rather than crashing the tab.
  const throwing = {
    getItem() { throw new Error("blocked"); },
    setItem() { throw new Error("blocked"); },
    removeItem() { throw new Error("blocked"); },
  };
  const second = S.Session({ storage: throwing, fetch: async () => ({ ok: true, status: 200, text: async () => "{}" }) });
  second.saveSettings({ clientId: "abc" });
  assert.equal(second.settings().clientId, "abc");
});

test("signing out removes the persisted refresh token", async () => {
  const S = load();
  const storage = memoryStorage({
    [S.KEYS.SETTINGS_KEY]: JSON.stringify({ clientId: "id" }),
    [S.KEYS.TOKENS_KEY]: JSON.stringify({ accessToken: "a", refreshToken: "r", expiresAt: 1 }),
  });
  const session = S.Session({ storage, fetch: async () => ({ ok: true, status: 200, text: async () => "{}" }) });
  assert.equal(session.signedIn(), true);
  session.signOut();
  assert.equal(session.signedIn(), false);
  assert.equal(storage.getItem(S.KEYS.TOKENS_KEY), null);
});

test("every host documents that playback stays Spotify's", () => {
  const notice = load().NOTICE;
  for (const sentence of ["Free account", "Premium account", "does not block"]) {
    assert.ok(notice.includes(sentence), "notice must mention: " + sentence);
  }
});
