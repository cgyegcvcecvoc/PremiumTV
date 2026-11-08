"use strict";
const { defineConfig, devices } = require("@playwright/test");
const projects = [
  { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  {
    name: "iphone",
    use: { ...devices["iPhone 13"], defaultBrowserType: "chromium" },
  },
];
// Real WebKit is run in CI after `npx playwright install webkit`. The phone
// project above is responsive/touch emulation, not a claim of Safari testing.
if (process.env.WEBKIT_TESTS === "1")
  projects.push({
    name: "webkit",
    use: { ...devices["iPhone 13"], defaultBrowserType: "webkit" },
  });
module.exports = defineConfig({
  testDir: "./test/browser",
  timeout: 90000,
  expect: { timeout: 12000 },
  fullyParallel: false,
  workers: 1,
  reporter: [["list"]],
  outputDir: "test-results",
  use: {
    baseURL: "http://127.0.0.1:4173",
    trace: "retain-on-failure",
    screenshot: "only-on-failure",
    launchOptions: { executablePath: process.env.CHROMIUM_PATH || undefined },
  },
  projects,
  webServer: {
    command: "node tools/serve.cjs",
    url: "http://127.0.0.1:4173/healthz",
    env: { PORT: "4173" },
    reuseExistingServer: !process.env.CI,
    timeout: 15000,
  },
});
