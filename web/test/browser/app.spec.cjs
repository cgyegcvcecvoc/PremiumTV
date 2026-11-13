"use strict";
const { test, expect } = require("@playwright/test");
// The published channel lineup changes after each scrape. Compare the UI to
// this build's actual group data instead of pinning a stale scrape's count.
const groupCount = require("../../dist/data/groups.json").length;


test.beforeEach(async ({ page }) => {
  // Keep tests deterministic and private: only same-origin assets are allowed.
  await page.route("**/*", (route) => {
    const url = new URL(route.request().url());
    return url.hostname === "127.0.0.1" ? route.continue() : route.abort();
  });
});

test("library, categories, search, sorting, favorites and history work", async ({
  page,
}) => {
  expect(groupCount).toBeGreaterThan(0);
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto("/");
  await expect(page.locator(".category-card")).toHaveCount(groupCount);
  await page.locator('[data-category="News"]').click();
  await expect(page.locator(".channel-card")).toHaveCount(60);
  await page.locator(".favorite-button").first().click();
  await expect(page.locator(".favorite-button").first()).toHaveAttribute(
    "aria-pressed",
    "true",
  );
  // Isolate shelf persistence from upstream feed availability; real playback
  // and failure behavior have their own tests below.
  await page.evaluate(() => {
    window.PremiumPlayer.play = () => {};
  });
  await page.locator(".channel-open").first().click();
  await expect(page.locator("#player")).toBeVisible();
  await page.locator("#player-close").click();
  await page.locator('[data-shelf="favorites"]:visible').click();
  await expect(page.locator(".channel-card")).toHaveCount(1);
  await page.reload();
  await expect(page.locator("#favorite-count")).toHaveText("1");
  await page.locator('[data-shelf="recent"]:visible').click();
  await expect(page.locator(".channel-card")).toHaveCount(1);
  await page.locator("#channel-search").fill("no-such-channel-987654");
  await expect(page.locator("#channel-empty")).toBeVisible();
  await page.locator("#clear-search").click();
  await expect(page.locator(".category-card")).toHaveCount(groupCount);
  await page.locator("#channel-sort").selectOption("az");
  await expect(page.locator(".category-card").first()).toContainText(
    "A&E Networks",
  );
  expect(errors).toEqual([]);
});

test("guide, timeline and honest live-event listings render", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.locator(".category-card").first()).toBeVisible();
  await page.getByRole("tab", { name: "TV guide", exact: true }).click();
  await expect(page.locator(".guide-channel").first()).toBeVisible();
  await page.getByRole("button", { name: "Timeline", exact: true }).click();
  await expect(page.locator(".timeline-row").first()).toBeVisible();
  await expect(page.locator(".timeline-program").first()).toBeVisible();
  await page.getByRole("tab", { name: "Live events", exact: true }).click();
  await expect(page.locator(".event-card").first()).toBeVisible();
  await expect(page.locator("#view-live")).toContainText(
    "cannot reliably pre-check",
  );
  await expect(page.locator(".event-status").first()).not.toHaveText("LIVE");
});

test("Movies & shows shows the coming-soon page instead of a shelf", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.locator(".category-card").first()).toBeVisible();
  await page.getByRole("tab", { name: "Movies & shows", exact: true }).click();
  await expect(page.locator("#movies-coming-soon")).toBeVisible();
  await expect(page.locator("#movies-coming-soon")).toContainText("COMING SOON");
  await expect(page.locator("#movies-toolbar")).toBeHidden();
  await expect(page.locator(".movie-card")).toHaveCount(0);
});

test("settings diagnostics, sleep timer, touch layout and install help", async ({
  page,
}) => {
  await page.goto("/");
  await expect(page.locator(".category-card").first()).toBeVisible();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
  await page.getByRole("tab", { name: "Settings", exact: true }).click();
  await page
    .getByRole("button", { name: "Check for bugs", exact: true })
    .click();
  await expect(page.locator(".bug-list li")).toHaveCount(11);
  await page.locator("#sleep-timer").selectOption("30");
  await expect(page.locator("#sleep-description")).toContainText("30 min");
  await page.locator("#settings-install").click();
  await expect(page.locator("#install-dialog")).toBeVisible();
  await page.getByRole("button", { name: "Got it", exact: true }).click();
  await expect(page.locator("#install-dialog")).toBeHidden();
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= innerWidth,
    ),
  ).toBe(true);
});

test("offline app shell and cached library reopen without a network", async ({
  page,
  context,
  browserName,
}) => {
  await page.goto("/");
  await expect(page.locator(".category-card")).toHaveCount(groupCount);
  await page.evaluate(() => navigator.serviceWorker.ready);
  await page.waitForFunction(() => navigator.serviceWorker.controller !== null);
  if (browserName === "webkit") {
    // Playwright's Linux WebKit port raises an internal navigation error for
    // setOffline + active service worker. Verify the actual persisted shell and
    // data here; Chromium below exercises a real offline relaunch. Physical
    // iOS offline behavior remains a device-test requirement, not a CI claim.
    const cached = await page.evaluate(async () => {
      const keys = await caches.keys();
      const cache = await caches.open(
        keys.find((k) => k.startsWith("premiumtv-web-")),
      );
      return Boolean(
        (await cache.match("index.html")) &&
          (await cache.match("data/channels.json")),
      );
    });
    expect(cached).toBe(true);
    test.info().annotations.push({
      type: "platform-limitation",
      description:
        "Linux WebKit offline navigation is unavailable in Playwright; persisted CacheStorage verified instead.",
    });
    return;
  }
  await context.setOffline(true);
  await page.reload({ waitUntil: "domcontentloaded" });
  await expect(page.locator(".category-card")).toHaveCount(groupCount);
  await expect(page.locator("#offline-banner")).toBeVisible();
  await page.getByRole("tab", { name: "Movies & shows", exact: true }).click();
  await expect(page.locator("#movies-coming-soon")).toBeVisible();
  await expect(page.locator(".movie-card")).toHaveCount(0);
  await context.setOffline(false);
});

test("provider failure shows an honest error and does not masquerade as playback", async ({
  page,
}) => {
  // A fulfilled HTTP error is deterministic in every engine. abort() models a
  // socket failure, which Linux WebKit sometimes leaves pending indefinitely.
  await page.route("https://30a-tv.com/feeds/vidaa/**", (route) =>
    route.fulfill({
      status: 503,
      contentType: "text/plain",
      headers: { "access-control-allow-origin": "*" },
      body: "Provider unavailable",
    }),
  );
  await page.goto("/");
  await expect(page.locator(".category-card").first()).toBeVisible();
  await page.locator("#channel-search").fill("30A Golf Kingdom");
  await expect(page.locator(".channel-open")).toHaveCount(1);
  await page.locator(".channel-open").click();
  await expect(page.locator("#player-error")).toBeVisible({ timeout: 40000 });
  await expect(page.locator("#player-error-text")).toContainText("browser");
  await expect(page.locator("#player-original")).toHaveAttribute(
    "href",
    /^https:\/\//,
  );
  await page.locator("#player-close").click();
  await page.getByRole("tab", { name: "Settings", exact: true }).click();
  await expect(page.locator("#restore-hidden")).toBeEnabled();
  await page.locator("#restore-hidden").click();
  await expect(page.locator("#restore-hidden")).toBeDisabled();
});

test("HLS playback uses the pinned browser library and really advances", async ({
  page,
  browserName,
}) => {
  test.skip(
    browserName === "webkit",
    "Linux WebKit lacks the platform HLS decoder; native iOS strategy is unit-tested and MP4 is exercised on WebKit.",
  );
  const fs = require("node:fs");
  const path = require("node:path");
  const fixture = path.join(__dirname, "../fixtures/hls");
  await page.route("https://30a-tv.com/feeds/vidaa/**", (route) => {
    const name = new URL(route.request().url()).pathname.split("/").pop();
    route.fulfill({
      status: 200,
      contentType: name.endsWith(".m3u8")
        ? "application/vnd.apple.mpegurl"
        : "video/mp2t",
      headers: { "access-control-allow-origin": "*" },
      body: fs.readFileSync(
        path.join(fixture, name.endsWith(".m3u8") ? "index.m3u8" : name),
      ),
    });
  });
  await page.goto("/");
  await expect(page.locator(".category-card").first()).toBeVisible();
  await page.locator("#channel-search").fill("30A Golf Kingdom");
  await expect(page.locator(".channel-open")).toHaveCount(1);
  await page.locator(".channel-open").click();
  await expect
    .poll(() => page.locator("video").evaluate((v) => v.currentTime))
    .toBeGreaterThan(0.5);
  await expect(page.locator("#player-error")).toBeHidden();
  await page.locator("#player-close").click();
});

test("failed refresh keeps the last usable library and personal shelves", async ({
  browser,
}) => {
  // Service-worker-originated no-store refreshes bypass page routing in
  // Chromium. This test deliberately disables the worker to inject the outage;
  // the separate offline test exercises the real worker and caches.
  const context = await browser.newContext({ serviceWorkers: "block" });
  const page = await context.newPage();
  await page.goto("http://127.0.0.1:4173/");
  await expect(page.locator(".category-card")).toHaveCount(groupCount);
  await page.route(/\/data\/meta\.json(?:\?.*)?$/, (route) =>
    route.fulfill({ status: 503, body: "Unavailable" }),
  );
  await page.getByRole("tab", { name: "Settings", exact: true }).click();
  await page.locator("#force-refresh").click();
  await expect(page.locator("#settings-body")).toContainText("503");
  await page.getByRole("tab", { name: "Channels", exact: true }).click();
  await expect(page.locator(".category-card")).toHaveCount(groupCount);
  await context.close();
});

test("blocked browser storage does not prevent watching the library", async ({
  page,
}) => {
  await page.addInitScript(() => {
    Object.defineProperty(window, "localStorage", {
      get() {
        throw new DOMException("Blocked", "SecurityError");
      },
    });
  });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await page.goto("/");
  await expect(page.locator(".category-card")).toHaveCount(groupCount);
  await page.locator('[data-category="News"]').click();
  await expect(page.locator(".channel-card").first()).toBeVisible();
  expect(errors).toEqual([]);
});

test("no-JavaScript directory and playlist remain available", async ({
  browser,
}) => {
  const context = await browser.newContext({ javaScriptEnabled: false });
  const page = await context.newPage();
  await page.goto("http://127.0.0.1:4173/directory.html");
  await expect(
    page.getByRole("heading", { name: "PremiumTV · Channel directory" }),
  ).toBeVisible();
  expect(await page.locator("ol li").count()).toBeGreaterThan(1000);
  await expect(
    page.getByRole("link", { name: "download the M3U playlist" }),
  ).toHaveAttribute("href", "data/PremiumTV.m3u");
  await context.close();
});

test("repository-subpath deployment keeps assets and service worker scoped", async ({
  page,
}) => {
  const http = require("node:http");
  const proxy = http.createServer((req, res) => {
    const prefix = "/PremiumTV/web";
    if (!req.url.startsWith(prefix + "/")) {
      res.writeHead(404);
      res.end();
      return;
    }
    const upstream = http.request(
      {
        hostname: "127.0.0.1",
        port: 4173,
        path: req.url.slice(prefix.length),
        method: req.method,
        headers: req.headers,
      },
      (response) => {
        res.writeHead(response.statusCode, response.headers);
        response.pipe(res);
      },
    );
    upstream.on("error", () => {
      res.writeHead(502);
      res.end();
    });
    req.pipe(upstream);
  });
  await new Promise((resolve) => proxy.listen(0, "127.0.0.1", resolve));
  try {
    await page.goto(`http://127.0.0.1:${proxy.address().port}/PremiumTV/web/`);
    await expect(page.locator(".category-card")).toHaveCount(groupCount);
    await page.evaluate(() => navigator.serviceWorker.ready);
    const scope = await page.evaluate(
      () => navigator.serviceWorker.controller?.scriptURL || "",
    );
    expect(scope).toContain("/PremiumTV/web/sw.js");
  } finally {
    await new Promise((resolve) => proxy.close(resolve));
  }
});

test("official viewing options remain separate from playable feeds", async ({ page }) => {
  await page.goto("/");
  const channels = page.locator("#channel-provider-options");
  await channels.locator("summary").click();
  await expect(channels).toContainText("not in the PremiumTV player");
  await expect(channels.getByRole("link", { name: /WNEP/ })).toHaveAttribute("href", "https://www.wnep.com/watch");
  await expect(channels.getByRole("link", { name: /WNEP/ })).toHaveAttribute("rel", "noopener noreferrer");
  await page.getByRole("tab", { name: "Live events", exact: true }).click();
  const sports = page.locator("#event-provider-options");
  await sports.locator("summary").click();
  await expect(sports).toContainText("not verified feeds or backups");
  await expect(sports.getByRole("link", { name: /NBA League Pass/ })).toBeVisible();
  expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
});
