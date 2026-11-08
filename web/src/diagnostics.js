/* Read-only checks. Never claim a format-valid URL is a verified live feed. */
(function (root) {
  "use strict";
  function check(library, environment, now) {
    const checks = [];
    const add = (label, status, detail) =>
      checks.push({ label, status, detail });
    const channels = library.channels || [],
      groups = library.groups || [],
      programmes = library.programmes || [];
    const invalid = channels.filter(
      (c) => !c.name || !/^https?:\/\//i.test(c.url),
    ).length;
    const urls = new Set(channels.map((c) => c.url));
    add(
      "Channel list",
      !channels.length || invalid ? "fail" : "ok",
      invalid
        ? `${invalid} malformed entries.`
        : `${channels.length} entries with HTTP(S) URLs; ${urls.size} unique feeds. Playback is checked only when opened.`,
    );
    const names = new Set(groups.map((g) => g.name));
    const missing = channels.filter((c) => !names.has(c.group)).length;
    add(
      "Categories",
      missing || !groups.length ? "warn" : "ok",
      `${groups.length} categories; ${missing} channels without a matching category.`,
    );
    add(
      "TV guide",
      library.guideError ? "warn" : programmes.length ? "ok" : "warn",
      library.guideError ||
        (programmes.length
          ? `${programmes.length} listings for ${new Set(programmes.map((p) => p.c)).size} channels.`
          : "No guide loaded. Channels still work."),
    );
    const age = (now / 1000 - Number(library.meta.window_start || 0)) / 86400;
    add(
      "Guide freshness",
      !library.meta.window_start || age > 7 ? "warn" : "ok",
      !library.meta.window_start
        ? "Guide window unknown."
        : age > 7
          ? `Guide window starts ${Math.floor(age)} days ago; some listings may be stale.`
          : `Guide window starts ${Math.max(0, age).toFixed(1)} days ago.`,
    );
    const restricted = channels.filter(
      (c) => c.ua || c.referrer || c.origin,
    ).length;
    add(
      "Browser headers",
      restricted ? "warn" : "ok",
      restricted
        ? `${restricted} feeds request custom headers. Browsers cannot attach forbidden User-Agent, Referer or Origin headers; these may need the native app.`
        : "No custom-header requirements in this library.",
    );
    const insecure = channels.filter((c) => c.url.startsWith("http:")).length;
    add(
      "Secure streams",
      insecure ? "warn" : "ok",
      insecure
        ? `${insecure} HTTP feeds may be blocked as mixed content on an HTTPS site. No insecure proxy is used.`
        : "All published stream URLs use HTTPS.",
    );
    add(
      "Playback support",
      environment.nativeHls || environment.mse ? "ok" : "warn",
      `Native HLS: ${environment.nativeHls ? "yes" : "no"}; MSE: ${environment.mse ? "yes" : "no"}. MP4 works natively; codec support varies by device.`,
    );
    add(
      "Browser storage",
      environment.storage ? "ok" : "warn",
      environment.storage
        ? "Favorites, recents and resume positions can persist on this browser."
        : "Storage is blocked. The player works, but personal shelves last only for this session.",
    );
    add(
      "Offline shell",
      environment.serviceWorker ? "ok" : "warn",
      environment.serviceWorker
        ? "Service workers are available. The shell/library cache depends on a successful HTTPS load; streams are never cached."
        : "No service worker in this context. Online browsing and playback still work.",
    );
    add(
      "Connection",
      environment.online ? "ok" : "warn",
      environment.online
        ? "Browser reports an online connection. This does not guarantee a provider is reachable."
        : "Offline. Cached browsing works; live streams and remote films need internet.",
    );
    add(
      "Library health",
      groups.some((g) => !g.count) ? "warn" : "ok",
      `${groups.filter((g) => !g.count).length} empty categories; largest category ${Math.max(0, ...groups.map((g) => g.count))} feeds. Results are paged to limit DOM size.`,
    );
    return {
      checks,
      fail: checks.filter((c) => c.status === "fail").length,
      warn: checks.filter((c) => c.status === "warn").length,
      ok: checks.filter((c) => c.status === "ok").length,
    };
  }
  const api = { check };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.PremiumDiagnostics = api;
})(typeof window !== "undefined" ? window : globalThis);
