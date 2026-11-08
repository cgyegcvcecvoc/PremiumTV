#!/usr/bin/env node
"use strict";
/* Static preview/production server. Bind publicly for the Arena proxy; the
 * browser only sees same-origin relative paths. No stream proxy or API. */
const http = require("node:http");
const fs = require("node:fs");
const path = require("node:path");
const zlib = require("node:zlib");
const root = path.resolve(__dirname, "..", "dist");
const port = Number(process.env.PORT || 3000);
const types = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".webmanifest": "application/manifest+json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".mp4": "video/mp4",
  ".m3u": "audio/x-mpegurl",
  ".txt": "text/plain; charset=utf-8",
};
function createServer() {
  return http.createServer((req, res) => {
    if (!["GET", "HEAD"].includes(req.method)) {
      res.writeHead(405, { Allow: "GET, HEAD" });
      res.end();
      return;
    }
    let pathname;
    try {
      pathname = decodeURIComponent(
        new URL(req.url, "http://localhost").pathname,
      );
    } catch (_) {
      res.writeHead(400);
      res.end();
      return;
    }
    if (pathname === "/healthz") {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end('{"ok":true}');
      return;
    }
    let file = path.resolve(root, "." + pathname);
    if (file !== root && !file.startsWith(root + path.sep)) {
      res.writeHead(403);
      res.end();
      return;
    }
    try {
      if (fs.statSync(file).isDirectory()) file = path.join(file, "index.html");
      let stat = fs.statSync(file);
      if (!stat.isFile()) throw new Error("not a file");
      const ext = path.extname(file),
        gzip =
          /\.(js|json|css|html|webmanifest|m3u)$/.test(ext) &&
          /\bgzip\b/.test(req.headers["accept-encoding"] || "") &&
          fs.existsSync(file + ".gz");
      const headers = {
        "Content-Type": types[ext] || "application/octet-stream",
        "Cache-Control":
          ext === ".html" ||
          pathname.endsWith("sw.js") ||
          pathname.endsWith("meta.json")
            ? "no-cache"
            : "public, max-age=3600",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Accept-Ranges": "bytes",
        Vary: "Accept-Encoding",
      };
      if (gzip) {
        headers["Content-Encoding"] = "gzip";
        file += ".gz";
        stat = fs.statSync(file);
      }
      let start = 0,
        end = stat.size - 1,
        status = 200;
      const range =
        req.headers.range &&
        !gzip &&
        /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
      if (range && (range[1] || range[2])) {
        start = range[1]
          ? Number(range[1])
          : Math.max(0, stat.size - Number(range[2]));
        end = range[1] && range[2] ? Math.min(Number(range[2]), end) : end;
        if (
          !Number.isSafeInteger(start) ||
          !Number.isSafeInteger(end) ||
          start > end ||
          start >= stat.size
        ) {
          res.writeHead(416, { "Content-Range": `bytes */${stat.size}` });
          res.end();
          return;
        }
        status = 206;
        headers["Content-Range"] = `bytes ${start}-${end}/${stat.size}`;
      }
      headers["Content-Length"] = Math.max(0, end - start + 1);
      res.writeHead(status, headers);
      if (req.method === "HEAD" || stat.size === 0) res.end();
      else {
        const stream = fs.createReadStream(file, { start, end });
        stream.on("error", () => res.destroy());
        stream.pipe(res);
        res.on("close", () => stream.destroy());
      }
    } catch (_) {
      res.writeHead(404, { "Content-Type": "text/plain" });
      res.end("Not found");
    }
  });
}
module.exports = { createServer };
if (require.main === module) {
  if (!fs.existsSync(path.join(root, "index.html"))) {
    console.error("Build first: cd web && npm ci && npm run build");
    process.exit(1);
  }
  createServer().listen(port, "0.0.0.0", () =>
    console.log(`PremiumTV Web listening on http://0.0.0.0:${port}`),
  );
}
