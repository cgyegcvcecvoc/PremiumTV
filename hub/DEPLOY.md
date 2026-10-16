# Deploying the PremiumTV Download Hub to a permanent URL

**Nothing here costs money.** Two ways to go:

- **Static export (easiest, $0, no credit card, no terminal):** drag one
  folder into a browser on Netlify Drop or Cloudflare Pages. See Option 0.
- **Full server (also $0 on Render's free tier):** Options A–D below.

---

## Option 0 — $0 drag-and-drop static deploy (Netlify Drop / Cloudflare Pages)

`hub/export_static.py` turns the hub into a plain folder of files — no server,
no Python on the host, nothing to maintain. Small files (every playlist, the
zip bundles, the gzipped guide, the unreleased 1.0.3 APK) are included in the
folder; huge files that already have a permanent free home (released APKs and
macOS installers on GitHub's release storage, the 35 MB merged guide on raw
file storage) are linked directly. Visitors still get one-click downloads for
everything.

Build it (already done if `hub/dist/static-site/` exists):

```bash
python3 hub/build_data.py
python3 hub/export_static.py
# -> hub/dist/static-site/  (~76 MB, ~590 files)
# -> hub/dist/bundles/premiumtv-hub-static-site.zip  (drag-and-drop copy)
```

**Netlify Drop (no account card, ~1 minute):**
1. Go to <https://app.netlify.com/drop> (free account, email only).
2. Drag the `static-site` folder (or the unzipped contents of
   `premiumtv-hub-static-site.zip`) onto the page.
3. Done — you get a permanent `https://something.netlify.app` URL you can
   rename in Site settings. Never sleeps, free SSL.

**Cloudflare Pages (also free, no card):**
1. <https://dash.cloudflare.com> → Workers & Pages → Create → Pages →
   **Upload assets**.
2. Upload the same folder. Permanent `https://<name>.pages.dev` URL.
   (Every file in the export is under Cloudflare's 25 MB per-file limit.)

**Surge.sh (free, one command):** `npx surge hub/dist/static-site`

To refresh the site after playlists change: rerun the two build commands and
drag the folder in again (Netlify keeps the same URL).

---

## Running it as a real server instead

The hub is one Python process with zero dependencies, so it runs on any free
host. All the config files are already in the repo root — pick a host and go.

| Host | Cost | Permanent URL | Catch |
|---|---|---|---|
| **Render** (easiest) | Free | `https://premiumtv-hub.onrender.com` (or similar) | Sleeps after ~15 min idle; wakes in a few seconds on the next visit |
| **Railway** | ~$5 trial credit, then paid | `https://<name>.up.railway.app` | Trial credit runs out eventually |
| **Fly.io** | Free allowance | `https://premiumtv-hub.fly.dev` | Asks for a credit card at signup (not charged within allowance) |
| **Oracle Cloud / home server** | $0 forever | Your own domain/IP | You manage the box |

What happens on every deploy (all hosts, via the `Dockerfile`):
1. `hub/fetch_assets.py` downloads the released APKs from GitHub's public
   release storage into `build-out/` (a fresh clone doesn't have them).
2. `hub/build_data.py` scans playlists/EPG/categories, hashes the APKs, builds
   the zip bundles and `data.json`.
3. `hub/server.py` serves everything on `$PORT`.

Any APK that can't be fetched simply falls back to a direct release link on
the site — the page never breaks.

---

## Option A — Render (recommended, ~3 minutes, no card)

1. Create a free account at <https://render.com> (sign in with GitHub).
2. Dashboard → **New** → **Blueprint**.
3. Pick the `PremiumTV1` repository (and the branch you want). Render reads
   `render.yaml` automatically.
4. Click **Apply**. First build takes a few minutes (it downloads the APKs).
5. Your permanent link appears at the top of the service page:
   `https://premiumtv-hub-XXXX.onrender.com`.

Every push to the branch auto-redeploys. To also self-host the macOS
installers, change the `MIRROR_MAC` env var to `1` **and** upgrade off the
free disk tier (the installers are ~1.1 GB).

## Option B — Railway

1. <https://railway.app> → **New Project** → **Deploy from GitHub repo** → pick `PremiumTV1`.
2. Railway detects the `Dockerfile` and builds it. Nothing to configure.
3. Service → **Settings → Networking → Generate Domain** → you get
   `https://<name>.up.railway.app`.

## Option C — Fly.io

```bash
flyctl auth signup                       # one-time
flyctl launch --copy-config --no-deploy  # uses fly.toml; pick a unique app name
flyctl deploy
```

Permanent URL: `https://<app-name>.fly.dev`. The config auto-stops the machine
when idle and auto-starts it on traffic, which keeps it inside the free
allowance.

## Option D — Any Docker box (Oracle Cloud Always-Free, Raspberry Pi, old PC)

```bash
git clone https://github.com/cgyegcvcecvoc/PremiumTV1.git
cd PremiumTV1
docker build -t premiumtv-hub .          # add --build-arg MIRROR_MAC=1 to self-host macOS installers
docker run -d --restart unless-stopped -p 80:8000 -e PORT=8000 premiumtv-hub
```

Visit `http://<server-ip>/`. Put Caddy or nginx in front for HTTPS, or use a
free Cloudflare Tunnel for a public HTTPS URL without opening ports.

### No Docker? No problem

The hub is pure Python 3.8+ stdlib:

```bash
python3 hub/fetch_assets.py   # pull APKs (needs internet once)
python3 hub/build_data.py     # build data + bundles
python3 hub/server.py 8000    # serve
```

---

## Keeping the playlists fresh

The deployed image contains the playlists as of the commit it was built from.
The site's **Copy URL** buttons always point at the live raw files, so players
stay current regardless. To refresh the *downloads* served by the hub, just
redeploy (Render/Railway do it automatically on every push; the daily playlist
runs push every day).
