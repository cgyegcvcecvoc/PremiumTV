/* Relay discovery for the browser player.
 *
 * A browser cannot send a Referer/User-Agent a provider demands, cannot read a
 * response without CORS, and cannot load an http:// feed from an https:// page.
 * A relay can do all three, so a feed listed here can be rescued instead of
 * being written off as "web can't play this".
 *
 * The relay is OPT-IN. This module reads `relay.json` next to the player and
 * treats anything other than an explicit `enabled: true` plus an http(s) `base`
 * as "no relay". GitHub Pages ships the disabled document, so nothing changes
 * for that deployment unless an operator points it at their own relay.
 *
 * Failure is always silent: a missing or broken config means the honest
 * no-relay behaviour the player already had.
 */
(function (root) {
  "use strict";

  const CONFIG_PATH = "relay.json";
  const DEFAULT_TIMEOUT = 6000;
  let state = null;

  function validate(raw) {
    if (!raw || typeof raw !== "object") return null;
    if (raw.enabled !== true) return null;
    const base = typeof raw.base === "string" ? raw.base.trim().replace(/\/+$/, "") : "";
    if (!/^https?:\/\/[^\s]+$/i.test(base)) return null;
    return {
      enabled: true,
      base,
      provider: typeof raw.provider === "string" && raw.provider.trim() ? raw.provider.trim() : "Relay",
      note: typeof raw.note === "string" ? raw.note : "",
    };
  }

  /** Absolute cannot be trusted from another origin; a path is fine. */
  function endpoint(path) {
    return new URL(path, document.baseURI).toString();
  }

  async function load() {
    if (state !== null) return state;
    state = false;
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT);
      const response = await fetch(endpoint(CONFIG_PATH), {
        signal: controller.signal,
        cache: "no-store",
        credentials: "omit",
      });
      clearTimeout(timer);
      if (!response.ok) return state;
      state = validate(await response.json()) || false;
    } catch (_) {
      state = false;
    }
    return state;
  }

  /**
   * The best URL to hand the player for a feed.
   *
   * Plain same-origin playback is preferred: it costs nothing and cannot be
   * slower than the origin. A feed is relayed only when this browser has a
   * concrete reason to need it, which keeps the relay off the hot path for the
   * three quarters of the library that are plain HTTPS.
   */
  function plan(source, relay) {
    const url = (source && source.url) || "";
    const off = { url, via: "", needsRelay: false, reason: "", available: Boolean(relay && relay.enabled) };
    if (!/^https?:\/\//i.test(url)) return off;

    const insecure = url.startsWith("http://") && location.protocol === "https:";
    const headers = Boolean(source.ua || source.referrer || source.origin);
    const canMse = typeof root.MediaSource !== "undefined" && Boolean(root.MediaSource);

    // A browser with neither native HLS nor MSE cannot decode a transport
    // stream at all. A relay fixes policy, not codecs, so do not promise it.
    const cannotDecode =
      !canMse &&
      !(
        root.PremiumPlayer &&
        root.PremiumPlayer.element &&
        root.PremiumPlayer.element.canPlayType("application/vnd.apple.mpegurl")
      );

    if (insecure) {
      return {
        ...off,
        needsRelay: off.available,
        reason:
          "This feed is plain HTTP. A secure page cannot load it directly, so only a relay can play it.",
      };
    }
    if (headers) {
      return {
        ...off,
        needsRelay: off.available,
        reason:
          "This feed asks for a Referer, Origin or User-Agent that browsers are not allowed to send.",
      };
    }
    // A browser with neither native HLS nor MSE cannot decode a transport
    // stream at all. A relay fixes policy, not codecs, so do not promise it.
    if (cannotDecode) {
      return {
        ...off,
        reason:
          "This browser has no HLS support at all. A relay cannot add codecs; use a browser with Media Source Extensions or the native app.",
      };
    }
    return off;
  }

  /**
   * Asks the relay for a playback session and returns the URL to hand the
   * player, or null when the relay refuses the feed or is unreachable.
   *
   * The relay decides whether a URL is one it publishes; the browser does not
   * get to talk it into an arbitrary fetch. A refusal is treated exactly like
   * an offline relay: the caller falls back, nothing is invented.
   */
  async function open(source, relay) {
    if (!relay || !relay.enabled) return null;
    const url = (source && source.url) || "";
    if (!/^https?:\/\//i.test(url)) return null;
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT);
      const response = await fetch(
        `${relay.base}/open?u=${encodeURIComponent(url)}`,
        { signal: controller.signal, cache: "no-store", credentials: "omit" },
      );
      clearTimeout(timer);
      if (!response.ok) return null;
      const body = await response.json();
      if (!body || body.ok !== true || typeof body.path !== "string") return null;
      if (!/^\/s\/[A-Za-z0-9]+$/.test(body.path)) return null;
      return {
        url: new URL(body.path, relay.base + "/").toString(),
        sessionId: body.sessionId || "",
        provider: relay.provider,
      };
    } catch (_) {
      return null;
    }
  }

  const api = { load, plan, open, validate, CONFIG_PATH };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.PremiumRelay = api;
})(typeof window !== "undefined" ? window : globalThis);
