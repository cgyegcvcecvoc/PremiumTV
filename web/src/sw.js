/* Only same-origin app/data requests are cached. Streams, logos and viewing
 * history never enter a service-worker cache. Update atomically by build ID. */
"use strict";
const BUILD = "BUILD_ID_PLACEHOLDER";
const CACHE = "premiumtv-web-" + BUILD;
const CORE = [
  "./",
  "index.html",
  "style.css",
  "app.js",
  "player.js",
  "store.js",
  "diagnostics.js",
  "shared/category-icons.js",
  "shared/live-events.js",
  "shared/personal.js",
  "shared/health.js",
  "data/meta.json",
  "data/channels.json",
  "data/groups.json",
  "data/vod.json",
  "data/events.json",
  "manifest.webmanifest",
  "icon-192.png",
  "icon-512.png",
];
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE)
      .then((cache) =>
        cache.addAll(
          CORE.map((path) => new Request(path, { cache: "reload" })),
        ),
      )
      .then(() => self.skipWaiting()),
  );
});
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key.startsWith("premiumtv-web-") && key !== CACHE)
            .map((key) => caches.delete(key)),
        ),
      )
      .then(() => self.clients.claim()),
  );
});
self.addEventListener("fetch", (event) => {
  const request = event.request,
    url = new URL(request.url);
  if (
    request.method !== "GET" ||
    url.origin !== self.location.origin ||
    !url.pathname.startsWith(new URL("./", self.location).pathname)
  )
    return;
  // Media and third-party-looking assets must reach the network untouched,
  // especially Range requests Safari uses for MP4 seeking.
  if (
    request.cache === "no-store" ||
    request.headers.has("range") ||
    /\.(mp4|m4v|mp3|m4a|webm|ts|m2ts|m3u8?)$/.test(url.pathname)
  )
    return;
  event.respondWith(
    (async () => {
      const cache = await caches.open(CACHE);
      // Core files are precached without a query; versioned runtime URLs may
      // match those entries. Never let a new build ID reuse an old cached file.
      const unversioned = new URL(url.href);
      unversioned.search = "";
      const cached =
        (await cache.match(request)) || (await cache.match(unversioned.href));
      if (cached) return cached;
      try {
        const response = await fetch(request);
        if (response.ok && response.type === "basic")
          await cache.put(request, response.clone());
        return response;
      } catch (error) {
        if (request.mode === "navigate") {
          const shell = await cache.match("index.html");
          if (shell) return shell;
        }
        return new Response("Unavailable offline", {
          status: 503,
          headers: { "Content-Type": "text/plain" },
        });
      }
    })(),
  );
});
