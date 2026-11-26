'use strict';

/**
 * Spotify in PremiumTV: links, embeds, sign-in and the playback session.
 *
 * One file, three hosts. The web player copies it at build time
 * (`web/tools/build.py` SHARED), the macOS/Linux renderer loads it directly and
 * the Android TV screen ships it inside the WebView's asset folder
 * (`android/app/src/main/assets/premiumtv/`). Keeping the policy here - not in
 * each UI - is what stops the four surfaces from disagreeing about what a
 * Spotify link means.
 *
 * ---------------------------------------------------------------------------
 * WHAT THIS DOES NOT DO
 * ---------------------------------------------------------------------------
 * It does not remove, mute, skip or hide Spotify's advertising, and it does not
 * touch the audio Spotify serves. Every second of playback goes through
 * Spotify's own player: either their embed iframe (open.spotify.com) or their
 * official Web Playback SDK (sdk.scdn.co), and both talk to Spotify's servers
 * directly. PremiumTV never proxies, re-encodes or filters that traffic.
 *
 * This is a deliberate product decision as well as a technical one. Spotify's
 * ad-supported tier pays rights holders, and the Developer Terms require the
 * player to be used as published; stripping its ads to get Premium-tier
 * listening is not something this repository will build. What PremiumTV adds is
 * a home for audio next to the TV: one tab, your playlists, sign-in once, and
 * playback that keeps running while you browse channels.
 *
 * Consequently: a Free account hears Spotify's ads here, exactly as it does in
 * Spotify's own apps, because it is Spotify's player. A Premium account hears
 * none, because Spotify serves none. Nothing in between is simulated.
 *
 * ---------------------------------------------------------------------------
 * WHY THE SESSION IS BUILT THIS WAY
 * ---------------------------------------------------------------------------
 * Authorization Code + PKCE with no client secret, because a desktop or TV
 * bundle cannot keep a secret and Spotify's public-client flow is exactly that.
 * The access token lives in memory; the refresh token is persisted, because a
 * TV with a remote should not ask you to type a password again every launch.
 * Tokens are only ever read by this file's callers inside the app.
 */

window.PremiumSpotify = (function () {
  'use strict';

  const PROVIDER = 'Spotify';

  // Spotify accounts. The same endpoints for every host.
  const AUTHORIZE_URL = 'https://accounts.spotify.com/authorize';
  const TOKEN_URL = 'https://accounts.spotify.com/api/token';
  const API_ROOT = 'https://api.spotify.com/v1';
  const PLAYER_SDK = 'https://sdk.scdn.co/spotify-player.js';

  // streaming            - the Web Playback SDK (Premium only, Spotify's rule)
  // user-modify-playback-state / read-playback-state - transfer + play/pause
  // user-read-private    - the account's product ("premium" / "free"), so the
  //                        UI can explain why in-app playback is unavailable
  //                        instead of letting Spotify's SDK fail silently.
  const SCOPES = [
    'streaming',
    'user-read-email',
    'user-read-private',
    'user-read-playback-state',
    'user-modify-playback-state',
  ].join(' ');

  const SETTINGS_KEY = 'premiumtv.spotify.v1';
  const TOKENS_KEY = 'premiumtv.spotify.tokens.v1';
  const PKCE_KEY = 'premiumtv.spotify.pkce.v1';

  // Refresh a little early so a request never races the expiry.
  const EXPIRY_MARGIN_MS = 60 * 1000;

  /**
   * The shelf every install starts with.
   *
   * These are Spotify's own editorial playlists, chosen for the thing a TV app
   * is actually good at - long-running background audio - rather than for
   * discovery. Every id below was resolved to its real playlist on 2026-11-26;
   * a wrong id is not a broken card, it is a "content not available" iframe,
   * which is why they are listed here as data instead of being searched for at
   * runtime (a search needs a signed-in token for no benefit).
   *
   * Spotify rotates the contents of these lists; the *ids* are stable. Add a
   * playlist of your own from the tab's "Your link" box, which is stored on this
   * device only.
   */
  const CURATED = [
    { type: 'playlist', id: '37i9dQZF1DXcBWIGoYBM5M', name: "Today's Top Hits", note: 'The current pop chart' },
    { type: 'playlist', id: '37i9dQZF1DWWQRwui0ExPn', name: 'Lo-Fi Beats', note: 'Steady background focus' },
    { type: 'playlist', id: '37i9dQZF1DX4sWSpwq3LiO', name: 'Peaceful Piano', note: 'Quiet, no vocals' },
    { type: 'playlist', id: '37i9dQZF1DWXRqgorJj26U', name: 'Rock Classics', note: 'The songs everyone knows' },
    { type: 'playlist', id: '37i9dQZF1DXbITWG1ZJKYt', name: 'Jazz Classics', note: 'Standards, late-night' },
    { type: 'playlist', id: '37i9dQZF1DX1lVhptIYRda', name: 'Hot Country', note: 'Nashville current' },
  ];

  // ---------------------------------------------------------------- links

  const LINK_TYPES = ['playlist', 'album', 'track', 'artist', 'episode', 'show'];

  /**
   * A detached, data-only copy of a structured result.
   *
   * Two reasons this exists rather than returning object literals. It keeps
   * everything crossing a boundary (this file runs in a WebView, an iframe-free
   * renderer and a browser tab) free of prototypes, getters or functions, so a
   * host can post it over IPC or contextBridge without surprises. And it makes
   * "these are values, not live view objects" a property of the code instead of
   * a comment: a caller cannot mutate module state through a result.
   */
  function plain(value) {
    return Object.assign(Object.create(null), value);
  }

  function cleanId(value) {
    // Spotify ids are 22 base-62 characters. Be liberal in what we accept
    // (a trailing query string is common when copying a link) but strict about
    // what we emit: only [A-Za-z0-9] ever reaches an iframe src.
    const match = String(value || '').match(/^([A-Za-z0-9]{10,64})$/);
    return match ? match[1] : '';
  }

  /**
   * Accept everything a viewer might paste and answer with a canonical target:
   *
   *   https://open.spotify.com/playlist/37i9...?si=abc
   *   https://open.spotify.com/intl-de/album/...
   *   https://open.spotify.com/embed/playlist/...
   *   spotify:playlist:37i9...
   *   spotify:user:spotify:playlist:37i9...   (the legacy share form)
   *   https://spotify.link/xxxx                 (short links cannot be resolved
   *                                              offline - reported, not guessed)
   *
   * Returns null when it is not a Spotify item link, so the caller can say so
   * instead of mounting an empty frame.
   */
  function parseLink(input) {
    const raw = String(input == null ? '' : input).trim();
    if (!raw) return null;

    // spotify:playlist:<id>, and the legacy share form
    // spotify:user:<owner>:playlist:<id>. The *item* type is the segment before
    // the id, not the first segment, or a user: URI would be read as "user".
    const uri = raw.match(/^spotify:(.+):([A-Za-z0-9]{10,64})$/i);
    if (uri) {
      const segments = uri[1].split(':').filter(Boolean);
      const type = String(segments[segments.length - 1] || '').toLowerCase();
      return plain(item(type, cleanId(uri[2])));
    }

    // A short link is opaque until fetched; the UI offers to open it instead.
    if (/^https?:\/\/spotify\.link\//i.test(raw)) {
      return plain({
        type: 'shortlink',
        id: '',
        openUrl: raw,
        error: 'Spotify short links have to be opened once to see the full link.',
      });
    }

    let url;
    try {
      url = new URL(/^[a-z]+:\/\//i.test(raw) ? raw : 'https://' + raw);
    } catch (_) {
      return null;
    }
    if (!/(^|\.)spotify\.com$/i.test(url.hostname)) return null;

    // /intl-de/playlist/<id>, /embed/playlist/<id>, /playlist/<id>
    const parts = url.pathname.split('/').filter(Boolean);
    const at = parts.findIndex((part) => LINK_TYPES.includes(part.toLowerCase()));
    if (at === -1) return null;
    return plain(item(parts[at].toLowerCase(), cleanId(parts[at + 1])));
  }

  function item(type, id) {
    if (!LINK_TYPES.includes(type) || !id) {
      return plain({
        type: type || '',
        id: id || '',
        error: 'That link is not a Spotify playlist, album, track, artist, show or episode.',
      });
    }
    return plain({
      type: type,
      id: id,
      uri: 'spotify:' + type + ':' + id,
      embedUrl: embedUrl(type, id),
      openUrl: 'https://open.spotify.com/' + type + '/' + id,
    });
  }

  /** Spotify's official embed, as their generator produces it. */
  function embedUrl(type, id, options) {
    const safeType = LINK_TYPES.includes(type) ? type : 'playlist';
    const safeId = cleanId(id);
    const query = ['utm_source=generator'];
    // theme=0 is Spotify's dark surface, which is the only thing that makes the
    // frame sit inside this app's palette instead of flashing white on open.
    query.push('theme=0');
    if (options && options.compact) query.push('view=coverart');
    return 'https://open.spotify.com/embed/' + safeType + '/' + safeId + '?' + query.join('&');
  }

  // ------------------------------------------------------------- settings

  function defaultSettings() {
    return plain({ clientId: '', custom: [], lastId: '', autoTransfer: true });
  }

  function normalizeSettings(value) {
    const base = defaultSettings();
    if (!value || typeof value !== 'object') return base;
    const custom = Array.isArray(value.custom) ? value.custom : [];
    return plain({
      clientId: typeof value.clientId === 'string' ? value.clientId.trim().slice(0, 128) : '',
      custom: custom
        .map((entry) => {
          if (!entry) return null;
          // Two shapes arrive here: a viewer's paste ({ link }) and this
          // function's own output ({ type, id, name }), because every save
          // re-normalizes what is already stored. Reading a saved entry as a
          // link would drop it - a bare id is not a URL.
          const isSaved = LINK_TYPES.includes(entry.type) && Boolean(cleanId(entry.id));
          const parsed = isSaved
            ? plain({ type: entry.type, id: cleanId(entry.id) })
            : parseLink(entry.link || entry.id);
          if (!parsed || !parsed.id) return null;
          return plain({
            type: parsed.type,
            id: parsed.id,
            name: String(entry.name || '').slice(0, 80) || defaultName(parsed),
          });
        })
        .filter(Boolean)
        .slice(0, 40),
      lastId: typeof value.lastId === 'string' ? value.lastId.slice(0, 64) : '',
      autoTransfer: value.autoTransfer !== false,
    });
  }

  function defaultName(parsed) {
    const titles = {
      playlist: 'Playlist',
      album: 'Album',
      track: 'Track',
      artist: 'Artist',
      show: 'Podcast',
      episode: 'Episode',
    };
    return titles[parsed.type] || 'Spotify item';
  }

  function readSettings(storage) {
    try {
      return normalizeSettings(JSON.parse(storage.getItem(SETTINGS_KEY)));
    } catch (_) {
      return defaultSettings();
    }
  }

  function writeSettings(storage, settings) {
    storage.setItem(SETTINGS_KEY, JSON.stringify(normalizeSettings(settings)));
  }

  /** Curated shelf first, then the viewer's own links, deduplicated by id. */
  function library(settings) {
    const custom = normalizeSettings(settings).custom;
    const seen = new Set();
    const rows = [];
    for (const entry of CURATED.concat(custom)) {
      const key = entry.type + ':' + entry.id;
      if (seen.has(key)) continue;
      seen.add(key);
      rows.push(plain({
        type: entry.type,
        id: entry.id,
        name: entry.name,
        note: entry.note || 'Your link',
        curated: CURATED.indexOf(entry) !== -1,
        embedUrl: embedUrl(entry.type, entry.id, { compact: true }),
        openUrl: 'https://open.spotify.com/' + entry.type + '/' + entry.id,
      }));
    }
    return rows;
  }

  // --------------------------------------------------------------- tokens

  /**
   * PKCE needs a high-entropy verifier and its SHA-256 challenge, base64url
   * encoded. `cryptoObj` is injectable so the offline tests can run this in a
   * VM without a browser; in the apps it is always `window.crypto`.
   */
  function base64Url(bytes) {
    let binary = '';
    for (let index = 0; index < bytes.length; index += 1) binary += String.fromCharCode(bytes[index]);
    return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  }

  function randomString(length, cryptoObj) {
    const source = cryptoObj || (typeof crypto !== 'undefined' ? crypto : null);
    if (!source || typeof source.getRandomValues !== 'function') {
      throw new Error('This browser cannot create a secure Spotify sign-in (no crypto.getRandomValues).');
    }
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';
    const bytes = new Uint8Array(length || 64);
    source.getRandomValues(bytes);
    let out = '';
    for (let index = 0; index < bytes.length; index += 1) out += alphabet[bytes[index] % alphabet.length];
    return out;
  }

  async function challengeFor(verifier, cryptoObj) {
    const source = cryptoObj || (typeof crypto !== 'undefined' ? crypto : null);
    if (!source || !source.subtle) {
      throw new Error('This browser cannot complete Spotify sign-in (no Web Crypto). Sign-in needs a secure context.');
    }
    const digest = await source.subtle.digest('SHA-256', new TextEncoder().encode(verifier));
    return base64Url(new Uint8Array(digest));
  }

  function authorizeUrl(options) {
    const params = [
      ['client_id', options.clientId],
      ['response_type', 'code'],
      ['redirect_uri', options.redirectUri],
      ['code_challenge_method', 'S256'],
      ['code_challenge', options.challenge],
      ['state', options.state],
      ['scope', SCOPES],
      ['show_dialog', options.forcePrompt ? 'true' : 'false'],
    ];
    const query = params
      .map(([key, value]) => encodeURIComponent(key) + '=' + encodeURIComponent(value))
      .join('&');
    return AUTHORIZE_URL + '?' + query;
  }

  /** The token endpoint takes form bodies, never JSON - even for PKCE. */
  function codeExchange(options) {
    return {
      url: TOKEN_URL,
      body: formBody({
        grant_type: 'authorization_code',
        code: options.code,
        redirect_uri: options.redirectUri,
        client_id: options.clientId,
        code_verifier: options.verifier,
      }),
    };
  }

  function refreshRequest(options) {
    return {
      url: TOKEN_URL,
      body: formBody({
        grant_type: 'refresh_token',
        refresh_token: options.refreshToken,
        client_id: options.clientId,
      }),
    };
  }

  function formBody(values) {
    return Object.keys(values)
      .map((key) => encodeURIComponent(key) + '=' + encodeURIComponent(values[key]))
      .join('&');
  }

  /**
   * Read the answer from Spotify's redirect.
   *
   * Accepts a full URL, a bare `?query` or a bare `#fragment`, because the two
   * hosts differ: a browser navigates to `?code=`, while the Web Playback SDK
   * and some TV shells hand back `#code=`.
   */
  function parseRedirect(input) {
    const raw = String(input || '');
    if (!raw) return plain({ code: '', state: '', error: '' });
    let params;
    try {
      const url = new URL(raw, 'https://premiumtv.invalid/');
      params = url.searchParams;
      // A fragment-only payload has to be read separately.
      if (!params.get('code') && !params.get('error') && url.hash) {
        params = new URLSearchParams(url.hash.replace(/^#/, ''));
      }
    } catch (_) {
      params = new URLSearchParams(raw.replace(/^[?#]/, ''));
    }
    return plain({
      code: params.get('code') || '',
      state: params.get('state') || '',
      error: params.get('error') || '',
    });
  }

  function normalizeTokens(payload, nowMs) {
    if (!payload || !payload.access_token) return null;
    const expiresIn = Number(payload.expires_in) || 3600;
    return plain({
      accessToken: payload.access_token,
      refreshToken: payload.refresh_token || '',
      expiresAt: (nowMs || Date.now()) + expiresIn * 1000,
      scope: payload.scope || SCOPES,
    });
  }

  // -------------------------------------------------------------- session

  /**
   * The signed-in session: one object per app, created with everything it
   * touches injected. No globals are read below this line, which is what makes
   * the whole flow testable offline - and what makes it identical on a desktop,
   * a phone and a TV.
   *
   *   Session({ storage, fetch, crypto, now, redirectUri, clientId })
   *
   * `storage` persists the refresh token (localStorage in every host).
   */
  /**
   * A storage that always answers.
   *
   * Private browsing, a hardened privacy mode, an app window with storage
   * disabled and a file:// page all leave `localStorage` absent or throwing on
   * access. Signing in must still work for the session in those cases: the
   * module keeps a memory copy and simply forgets it when the app closes, which
   * is the honest behaviour - and better than a tab that throws on open.
   */
  function safeStorage(candidate) {
    const memory = Object.create(null);
    const call = (method, args) => {
      if (!candidate) return undefined;
      try {
        return candidate[method].apply(candidate, args);
      } catch (_) {
        return undefined;
      }
    };
    return {
      durable: (() => {
        if (!candidate) return false;
        try {
          candidate.setItem('premiumtv.spotify.probe', '1');
          candidate.removeItem('premiumtv.spotify.probe');
          return true;
        } catch (_) {
          return false;
        }
      })(),
      getItem(key) {
        const value = call('getItem', [key]);
        return value == null ? (key in memory ? memory[key] : null) : value;
      },
      setItem(key, value) {
        memory[key] = String(value);
        call('setItem', [key, String(value)]);
      },
      removeItem(key) {
        delete memory[key];
        call('removeItem', [key]);
      },
    };
  }

  function Session(options) {
    const opts = options || {};
    // `opts.storage` is usually the caller's `window.localStorage`, and merely
    // *reading* that property throws in a browser with storage blocked. Reading
    // it here, eagerly, took the whole app down before this tab existed - a
    // Spotify failure must never cost the viewer their television. A session is
    // therefore created even when there is no storage at all; safeStorage()
    // keeps the answers in memory for the session and everything else works.
    // Resolving the storage is itself part of the guard: the getter the web app
    // passes throws in a browser with storage blocked, and a working tab
    // matters more than persistence.
    let candidate = null;
    try {
      candidate = typeof opts.storage === 'function' ? opts.storage() : opts.storage;
    } catch (_) {
      candidate = null;
    }
    const storage = safeStorage(candidate);
    const doFetch = opts.fetch;
    const cryptoObj = opts.crypto;
    const now = opts.now || (() => Date.now());

    let settings = readSettings(storage);
    if (opts.clientId) settings.clientId = String(opts.clientId);
    let tokens = null;
    let lastError = '';
    let account = null;
    const listeners = [];

    function notify(event) {
      for (const listener of listeners) {
        try {
          listener(event);
        } catch (_) {
          /* a broken listener must not break playback */
        }
      }
    }

    function subscribe(listener) {
      listeners.push(listener);
      return () => {
        const at = listeners.indexOf(listener);
        if (at !== -1) listeners.splice(at, 1);
      };
    }

    function restore() {
      if (tokens) return tokens;
      try {
        const saved = JSON.parse(storage.getItem(TOKENS_KEY));
        if (saved && saved.refreshToken) {
          // The access token from a previous launch is normally expired; keep it
          // anyway and let ensureToken() decide, so reopening the app does not
          // spend a refresh round-trip before the first paint.
          tokens = {
            accessToken: saved.accessToken || '',
            refreshToken: saved.refreshToken,
            expiresAt: Number(saved.expiresAt) || 0,
            scope: saved.scope || SCOPES,
          };
        }
      } catch (_) {
        tokens = null;
      }
      return tokens;
    }

    function persist() {
      if (!tokens || !tokens.refreshToken) {
        try {
          storage.removeItem(TOKENS_KEY);
        } catch (_) {
          /* private mode */
        }
        return;
      }
      try {
        storage.setItem(
          TOKENS_KEY,
          JSON.stringify({
            accessToken: tokens.accessToken,
            refreshToken: tokens.refreshToken,
            expiresAt: tokens.expiresAt,
            scope: tokens.scope,
          }),
        );
      } catch (_) {
        /* a TV with full storage still plays until the app closes */
      }
    }

    function signedIn() {
      const current = restore();
      return Boolean(current && (current.accessToken || current.refreshToken));
    }

    function configured() {
      return Boolean(readSettings(storage).clientId);
    }

    /** Begin sign-in: stores the verifier, then returns the URL to open. */
    async function begin(redirectUri, forcePrompt) {
      const current = readSettings(storage);
      if (!current.clientId) {
        throw new Error(
          'Add your Spotify app\u2019s Client ID in Spotify settings first (see the note on this tab).',
        );
      }
      const verifier = randomString(96, cryptoObj);
      const challenge = await challengeFor(verifier, cryptoObj);
      const state = randomString(24, cryptoObj);
      try {
        storage.setItem(PKCE_KEY, JSON.stringify({ verifier, state, redirectUri, at: now() }));
      } catch (_) {
        throw new Error('This device cannot store the sign-in state. Browser storage is required.');
      }
      return authorizeUrl({
        clientId: current.clientId,
        redirectUri,
        challenge,
        state,
        forcePrompt: Boolean(forcePrompt),
      });
    }

    /** Finish sign-in with whatever Spotify redirected to. */
    async function complete(redirectInput) {
      const answer = parseRedirect(redirectInput);
      const pending = readPending();
      if (answer.error) {
        throw new Error(
          answer.error === 'access_denied'
            ? 'Spotify sign-in was cancelled.'
            : 'Spotify refused the sign-in: ' + answer.error,
        );
      }
      if (!answer.code) throw new Error('Spotify did not send an authorization code.');
      if (!pending || !pending.state) throw new Error('The sign-in state was lost. Start the sign-in again.');
      if (answer.state !== pending.state) throw new Error('The sign-in answer did not match this request. Start again.');
      const current = readSettings(storage);
      const request = codeExchange({
        code: answer.code,
        redirectUri: pending.redirectUri,
        clientId: current.clientId,
        verifier: pending.verifier,
      });
      const payload = await postForm(request);
      tokens = normalizeTokens(payload, now());
      if (!tokens) throw new Error('Spotify did not return an access token.');
      persist();
      clearPending();
      account = null;
      notify({ type: 'signed-in' });
      return { ok: true };
    }

    function readPending() {
      try {
        const pending = JSON.parse(storage.getItem(PKCE_KEY));
        // Ten minutes is Spotify's own tolerance for a sign-in attempt.
        if (!pending || now() - Number(pending.at || 0) > 10 * 60 * 1000) return null;
        return pending;
      } catch (_) {
        return null;
      }
    }

    function clearPending() {
      try {
        storage.removeItem(PKCE_KEY);
      } catch (_) {
        /* nothing to clear */
      }
    }

    async function postForm(request) {
      const response = await doFetch(request.url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: request.body,
      });
      const text = await response.text();
      let payload = {};
      try {
        payload = text ? JSON.parse(text) : {};
      } catch (_) {
        payload = {};
      }
      if (!response.ok) {
        if (response.status === 400 && payload.error === 'invalid_grant') {
          throw new Error('Spotify no longer accepts this sign-in. Sign in again.');
        }
        throw new Error(
          'Spotify sign-in failed (' + response.status + ')' + (payload.error ? ': ' + payload.error : ''),
        );
      }
      return payload;
    }

    async function refresh() {
      const current = restore();
      if (!current || !current.refreshToken) throw new Error('Not signed in to Spotify.');
      const settingsNow = readSettings(storage);
      const request = refreshRequest({
        refreshToken: current.refreshToken,
        clientId: settingsNow.clientId,
      });
      const payload = await postForm(request);
      const next = normalizeTokens(payload, now());
      if (!next) throw new Error('Spotify did not return an access token.');
      // A refresh response usually omits refresh_token; keep the one we have.
      tokens = {
        accessToken: next.accessToken,
        refreshToken: next.refreshToken || current.refreshToken,
        expiresAt: next.expiresAt,
        scope: next.scope || current.scope,
      };
      persist();
      notify({ type: 'token' });
      return tokens;
    }

    /** A usable access token, refreshed if it is about to expire. */
    async function token() {
      const current = restore();
      if (!current) throw new Error('Not signed in to Spotify.');
      if (current.accessToken && current.expiresAt - EXPIRY_MARGIN_MS > now()) return current.accessToken;
      const refreshed = await refresh();
      return refreshed.accessToken;
    }

    /** One authenticated API call, with a single refresh-and-retry on 401. */
    async function api(path, init) {
      const access = await token();
      const call = (bearer) =>
        doFetch(API_ROOT + path, Object.assign({}, init, {
          headers: Object.assign(
            { Authorization: 'Bearer ' + bearer },
            (init && init.headers) || {},
          ),
        }));
      let response = await call(access);
      if (response.status === 401) {
        const refreshed = await refresh();
        response = await call(refreshed.accessToken);
      }
      const text = await response.text();
      let payload = null;
      if (text) {
        try {
          payload = JSON.parse(text);
        } catch (_) {
          payload = null;
        }
      }
      if (!response.ok) {
        throw apiError(response.status, payload);
      }
      return payload;
    }

    function apiError(status, payload) {
      const reason = payload && payload.error && (payload.error.message || payload.error);
      if (status === 403) {
        return new Error(
          'Spotify declined that request' + (reason ? ': ' + reason : '') +
            '. In-app playback needs a Spotify Premium account - Spotify\u2019s rule, not PremiumTV\u2019s.',
        );
      }
      if (status === 404) return new Error('No Spotify playback device is active right now.');
      if (status === 429) return new Error('Spotify is rate-limiting this account. Try again in a moment.');
      const error = new Error('Spotify request failed (' + status + ')' + (reason ? ': ' + reason : ''));
      error.status = status;
      return error;
    }

    /** The account, cached: the product decides what the UI offers. */
    async function me() {
      if (account) return account;
      const payload = await api('/me');
      account = {
        id: (payload && payload.id) || '',
        name: (payload && (payload.display_name || payload.id)) || 'Spotify account',
        product: (payload && payload.product) || 'free',
        country: (payload && payload.country) || '',
      };
      notify({ type: 'account', account: account });
      return account;
    }

    async function devices() {
      try {
        const payload = await api('/me/player/devices');
        return (payload && payload.devices) || [];
      } catch (_) {
        return [];
      }
    }

    /** Hand playback to this app's SDK device, keeping the current track. */
    async function transferTo(deviceId, play) {
      await api('/me/player', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ device_ids: [deviceId], play: play !== false }),
      });
    }

    /** Start (or resume) one item on a device. */
    async function play(deviceId, target) {
      const suffix = deviceId ? '?device_id=' + encodeURIComponent(deviceId) : '';
      const body = target && target.id
        ? target.type === 'track' || target.type === 'episode'
          ? { uris: ['spotify:' + target.type + ':' + target.id] }
          : { context_uri: 'spotify:' + target.type + ':' + target.id }
        : {};
      await api('/me/player/play' + suffix, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
    }

    async function pause() {
      await api('/me/player/pause', { method: 'PUT' });
    }

    async function resume() {
      await api('/me/player/play', { method: 'PUT' });
    }

    function signOut() {
      tokens = null;
      account = null;
      clearPending();
      try {
        storage.removeItem(TOKENS_KEY);
      } catch (_) {
        /* private mode */
      }
      notify({ type: 'signed-out' });
    }

    function setError(message) {
      lastError = message || '';
      notify({ type: 'error', message: lastError });
    }

    return {
      // state
      signedIn,
      configured,
      settings: () => readSettings(storage),
      saveSettings: (next) => {
        settings = normalizeSettings(Object.assign({}, readSettings(storage), next));
        writeSettings(storage, settings);
        notify({ type: 'settings', settings: settings });
        return settings;
      },
      me,
      // sign-in
      begin,
      complete,
      token,
      refresh,
      api,
      devices,
      transferTo,
      play,
      pause,
      resume,
      signOut,
      // plumbing
      subscribe,
      lastError: () => lastError,
      setError,
      SCOPES,
      PLAYER_SDK,
    };
  }

  // ------------------------------------------------------------- utilities

  /**
   * Plain-language status for the tab, so a failure is never a bare code.
   * `product` is included because the most common "it will not play" is a Free
   * account trying the SDK - which is Spotify's rule and is worth saying once,
   * clearly, instead of letting the button appear broken.
   */
  function explain(error) {
    const message = String((error && error.message) || error || '');
    if (!message) return '';
    if (/Premium/i.test(message)) {
      return message + ' Use Spotify\u2019s embed, or sign in with a Premium account.';
    }
    if (/crypto|secure context|storage/i.test(message)) {
      return message + ' This needs the app build or an https:// page.';
    }
    return message;
  }

  const NOTICE =
    'Playback is Spotify\u2019s own player, so Spotify\u2019s terms apply: a Free account hears ' +
    'Spotify\u2019s ads here exactly as it does in Spotify\u2019s apps, and a Premium account ' +
    'hears none. PremiumTV does not block, mute or skip them.';

  return {
    PROVIDER,
    SCOPES,
    PLAYER_SDK,
    AUTHORIZE_URL,
    TOKEN_URL,
    API_ROOT,
    KEYS: { SETTINGS_KEY, TOKENS_KEY, PKCE_KEY },
    NOTICE,
    CURATED,
    LINK_TYPES,
    library,
    embedUrl,
    parseLink,
    parseRedirect,
    authorizeUrl,
    challengeFor,
    randomString,
    codeExchange,
    refreshRequest,
    normalizeTokens,
    normalizeSettings,
    defaultSettings,
    readSettings,
    writeSettings,
    explain,
    Session,
  };
})();
