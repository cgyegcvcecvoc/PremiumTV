"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { createServer } = require("../tools/serve.cjs");
const zlib = require("node:zlib");
const http = require("node:http");
const fs = require("node:fs");
const os = require("node:os");
const path = require("node:path");

test("static server supports gzip, media ranges, HEAD and safe paths", async (t) => {
  // Self-contained: CI runs unit tests before building the ignored dist/.
  const root = fs.mkdtempSync(path.join(os.tmpdir(), "premiumtv-server-"));
  fs.mkdirSync(path.join(root, "data"));
  fs.mkdirSync(path.join(root, "media"));
  const channels = Buffer.from(JSON.stringify([{ name: "Test channel" }]));
  fs.writeFileSync(path.join(root, "data/channels.json"), channels);
  fs.writeFileSync(
    path.join(root, "data/channels.json.gz"),
    zlib.gzipSync(channels),
  );
  fs.writeFileSync(
    path.join(root, "media/premiumtv-test-card.mp4"),
    Buffer.alloc(1024, 7),
  );
  fs.writeFileSync(path.join(root, "sw.js"), 'const BUILD = "test-build";');
  const server = createServer(root);
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  t.after(async () => {
    await new Promise((resolve) => server.close(resolve));
    fs.rmSync(root, { recursive: true, force: true });
  });
  const base = `http://127.0.0.1:${server.address().port}`;
  const raw = await new Promise((resolve, reject) => {
    http
      .get(
        base + "/data/channels.json",
        { headers: { "Accept-Encoding": "gzip" } },
        (response) => {
          const chunks = [];
          response.on("data", (chunk) => chunks.push(chunk));
          response.on("end", () =>
            resolve({ headers: response.headers, body: Buffer.concat(chunks) }),
          );
        },
      )
      .on("error", reject);
  });
  assert.equal(raw.headers["content-encoding"], "gzip");
  assert.ok(JSON.parse(zlib.gunzipSync(raw.body)).length > 0);
  let response = await fetch(base + "/media/premiumtv-test-card.mp4", {
    headers: { Range: "bytes=0-99" },
  });
  assert.equal(response.status, 206);
  assert.equal((await response.arrayBuffer()).byteLength, 100);
  assert.match(response.headers.get("content-range"), /^bytes 0-99\//);
  response = await fetch(base + "/media/premiumtv-test-card.mp4", {
    headers: { Range: "bytes=999999999-" },
  });
  assert.equal(response.status, 416);
  response = await fetch(base + "/media/premiumtv-test-card.mp4", {
    method: "HEAD",
  });
  assert.equal(response.status, 200);
  assert.equal((await response.arrayBuffer()).byteLength, 0);
  response = await fetch(base + "/%2e%2e%2fpackage.json");
  assert.equal(response.status, 403);
  response = await fetch(base + "/", { method: "POST" });
  assert.equal(response.status, 405);
  response = await fetch(base + "/healthz");
  assert.deepEqual(await response.json(), { ok: true });
  // A relative build also works behind a repository-path reverse proxy.
  response = await fetch(base + "/sw.js");
  assert.equal(response.headers.get("cache-control"), "no-cache");
  assert.doesNotMatch(await response.text(), /BUILD_ID_PLACEHOLDER/);
});
