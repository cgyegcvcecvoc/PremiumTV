'use strict';

/**
 * PremiumTV for Mac — application entry point.
 *
 * Wires the four pieces together: the loopback server the window is served
 * from, the repository that owns the channel list and the guide, the refresh
 * scheduler that mirrors the repository's publishing windows, and the window
 * itself. Nothing here talks to the renderer except through the preload bridge.
 */

const { app, BrowserWindow, Menu, ipcMain, powerMonitor, session, shell, dialog } = require('electron');
const path = require('node:path');
const os = require('node:os');
const fs = require('node:fs');

const { TvRepository } = require('./repository');
const { StreamProxy } = require('./stream-proxy');
const { AutoRefresh } = require('./auto-refresh');
const { AppUpdater } = require('./updater');
const schedule = require('./refresh-schedule');
const crashLog = require('./crash-log');

const WINDOW_STATE_KEY = 'window-bounds';
const smokeMode = process.argv.includes('--smoke-test');
if (smokeMode) {
  app.setPath('userData', require('node:fs').mkdtempSync(path.join(os.tmpdir(), 'premiumtv-smoke-')));
  // Backstop so a wedged smoke cannot hang CI - sized for the whole gate,
  // not the old library-only pass: since 1.0.9 the smoke also opens a
  // channel, and the stream machinery legitimately spends tens of seconds
  // on manifest timeouts and server fallback (doubly so under Rosetta).
  // 90s here used to guillotine the app mid-check, which read exactly like
  // a crash ("Object has been destroyed") in the smoke output.
  setTimeout(() => {
    console.error('SMOKE WATCHDOG: still running after 300s, exiting');
    app.exit(1);
  }, 300000).unref();
}

/**
 * Whether this bundle is allowed to ask the system for a location (1.1.18).
 *
 * macOS refuses every geolocation request from a bundle whose Info.plist has no
 * `NSLocationUsageDescription`, and it refuses silently: the renderer just gets
 * "denied", which is exactly how 1.1.7-1.1.17 came to look like a feature that
 * never asked. The packaged Info.plist is read as text (the key is a one-line
 * string) so the app can tell "this build cannot ask" from "you declined".
 * An unreadable plist reports true: no answer here may invent a problem.
 */
function hasLocationUsageDescription() {
  if (process.platform !== 'darwin') return true;
  if (!app.isPackaged) return true;
  try {
    const plist = path.join(process.resourcesPath, '..', 'Info.plist');
    return /NSLocation(Usage|WhenInUseUsage)Description/.test(fs.readFileSync(plist, 'utf8'));
  } catch (error) {
    return true;
  }
}

/**
 * The crash record.
 *
 * 1.1.14: a fatal error in the main process, or a renderer the system killed,
 * left nothing behind, so "it crashed every now and then" could not be
 * diagnosed. The record stays on this Mac (the app's own data folder) and is
 * shown by Settings → Check for bugs; nothing is uploaded.
 */
function recordCrash(kind, error, thread) {
  const detail = crashLog.formatCrash({
    kind,
    thread,
    message: error && error.message ? error.message : String(error || '(no message)'),
    stack: error && error.stack,
  });
  if (crashLog.writeCrash(app.getPath('userData'), detail)) console.error(detail);
}

// Keep the default outcome (the process still exits) while leaving a record.
process.on('uncaughtException', (error, origin) => {
  recordCrash('Uncaught exception', error, origin || 'main');
  app.exit(1);
});

process.on('unhandledRejection', (reason) => {
  recordCrash(
    'Unhandled rejection',
    reason instanceof Error ? reason : new Error(String(reason)),
    'main',
  );
});

/**
 * What the app did with every geolocation request the renderer made (1.1.18).
 *
 * Settings → Local channels reads this so a failed lookup can say which of the
 * three different failures it was: the viewer declined, the OS was never asked
 * (a bundle without a usage description), or the OS asked and nothing answered
 * in time. Module scope because the counting happens in whenReady and the
 * handler that reports it sits with the other ipcMain handlers.
 */
const moduleLocationAsks = { requested: 0, allowed: 0, denied: 0, last: '' };

let mainWindow = null;
let repository = null;
let proxy = null;
let autoRefresh = null;
let updater = null;

// ------------------------------------------------------------------- paths

function paths() {
  const rendererDir = path.join(__dirname, '..', 'renderer');
  const bundleDir = app.isPackaged
    ? path.join(process.resourcesPath, 'bundle')
    : path.join(__dirname, '..', '..', 'resources', 'bundle');
  const userData = app.getPath('userData');
  return {
    rendererDir,
    bundleDir,
    cacheDir: path.join(userData, 'bundle'),
    stateFile: path.join(userData, 'refresh-state.json'),
    logoCacheDir: path.join(userData, 'logo-cache'),
  };
}

// ---------------------------------------------------------------- lifecycle

const gotTheLock = app.requestSingleInstanceLock();
if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
  bootstrap();
}

function bootstrap() {
  app.setName('PremiumTV');
  // Async stream resolution and server-fallback hops run after the initial
  // click; relaxing Chromium's gesture gate prevents unmuted playback from
  // being silently muted or rejected. PlatformHEVCDecoderSupport also exposes
  // macOS AudioToolbox / VideoToolbox hardware codecs to MSE.
  app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');
  app.commandLine.appendSwitch('enable-features', 'PlatformHEVCDecoderSupport');
  // The Linux build runs on both X11 and Wayland desktops. `auto` lets Electron
  // pick the native platform it is actually under (instead of always falling
  // back to XWayland), and the flag is darwin/Win-unrelevant, so it is set only
  // where it means something.
  if (process.platform === 'linux') {
    app.commandLine.appendSwitch('ozone-platform-hint', 'auto');
  }
  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
  });
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
    else mainWindow.show();
  });

  app.whenReady().then(async () => {
    // 1.1.7 Local channels: the renderer may ask for an approximate location
    // once, and only when the viewer presses "Use my location". Every other
    // permission request stays denied.
    //
    // 1.1.18: granting here is only half of it. On macOS the *system* prompt
    // (and therefore the answer the viewer gives) needs the
    // NSLocationUsageDescription key in Info.plist — see electron-builder.yml —
    // and on Linux it needs a location service (GeoClue) running. So the
    // outcome of every request is counted, and Settings can say honestly
    // whether the app ever got to ask instead of blaming the viewer.
    const appOrigin = (url) => {
      try { return !!proxy && new URL(url).origin === proxy.origin; }
      catch (error) { return false; }
    };
    session.defaultSession.setPermissionRequestHandler((webContents, permission, callback, details) => {
      if (permission !== 'geolocation') {
        callback(false);
        return;
      }
      const fromApp = appOrigin(details.requestingUrl);
      moduleLocationAsks.requested += 1;
      if (fromApp) moduleLocationAsks.allowed += 1;
      else moduleLocationAsks.denied += 1;
      moduleLocationAsks.last = new Date().toISOString();
      // Saying yes here is what lets the OS ask; the OS answer is the real one.
      callback(fromApp);
    });
    session.defaultSession.setPermissionCheckHandler((webContents, permission, requestingOrigin) =>
      permission === 'geolocation' && appOrigin(requestingOrigin));
    const options = paths();

    proxy = new StreamProxy({ rendererDir: options.rendererDir, logoCacheDir: options.logoCacheDir });
    await proxy.start();

    repository = new TvRepository({
      bundleDir: options.bundleDir,
      cacheDir: options.cacheDir,
      stateFile: options.stateFile,
    });
    repository.on('state', (state) => send('ptv:state', state));
    repository.on('info', (info) => send('ptv:info', info));
    repository.on('progress', (progress) => send('ptv:progress', progress));

    autoRefresh = new AutoRefresh({ repository });

    // App updates are independent of the channel/guide refresh: the same
    // published stable release is offered to both channels, only when its
    // version is above this installed app.
    updater = new AppUpdater({
      currentVersion: app.getVersion(),
      stateFile: path.join(app.getPath('userData'), 'update-state.json'),
      downloadDir: path.join(app.getPath('userData'), 'updates'),
      arch: process.arch,
      // 1.1.18: which installer this machine can use (the Linux build must
      // never be offered the Mac .dmg the same release carries).
      platform: process.platform,
      shell,
    });
    updater.on('state', (state) => send('ptv:update', state));

    await createWindow();
    if (smokeMode) {
      try {
        await require('./smoke-test')(mainWindow, repository, proxy);
        app.exit(0);
      } catch (error) {
        console.error(error);
        app.exit(1);
      }
      return;
    }
    await repository.load();

    autoRefresh.start();
    // The updater throttles itself to once a day; this first call is what
    // makes a newly published stable release appear in Settings.
    updater.start();

    // A Mac that slept through a publishing window gets its check on wake.
    powerMonitor.on('resume', () => {
      autoRefresh.catchUpIfOverdue().catch(() => {});
      if (updater) updater.check().catch(() => {});
    });
    app.on('browser-window-focus', () => {
      autoRefresh.catchUpIfOverdue().catch(() => {});
      if (updater) updater.check().catch(() => {});
    });
  });

  app.on('before-quit', async () => {
    if (autoRefresh) autoRefresh.stop();
    if (proxy) await proxy.stop();
  });
}

function createWindow() {
  const saved = readWindowState();
  mainWindow = new BrowserWindow({
    width: saved.width,
    height: saved.height,
    x: saved.x,
    y: saved.y,
    minWidth: 940,
    minHeight: 600,
    title: 'PremiumTV',
    backgroundColor: '#141417',
    titleBarStyle: 'hiddenInset',
    trafficLightPosition: { x: 16, y: 18 },
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
      sandbox: true,
      spellcheck: false,
      backgroundThrottling: false,
    },
  });

  // A renderer the OS or the GPU process kills is the other way this app can
  // disappear with no message; it is worth a record too.
  mainWindow.webContents.on('render-process-gone', (_event, details) => {
    recordCrash(
      'Renderer gone',
      new Error(`${(details && details.reason) || 'unknown'}${
        details && details.exitCode !== undefined ? ` (exit ${details.exitCode})` : ''
      }`),
      'renderer',
    );
  });

  mainWindow.webContents.setAudioMuted(false);
  mainWindow.once('ready-to-show', () => mainWindow.show());
  mainWindow.on('close', writeWindowState);

  // Anything the renderer tries to open in a new window goes to the browser.
  // Sign-in is one of those: Spotify's login page opens in the real browser,
  // where the viewer's password manager and 2FA already work.
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:\/\//i.test(url)) shell.openExternal(url);
    return { action: 'deny' };
  });

  // A redirect to the Spotify callback must never load inside the app. It is
  // read here and replayed to the renderer, which finishes the PKCE exchange.
  mainWindow.webContents.on('will-navigate', (event, url) => {
    const payload = spotifyCallbackPayload(url);
    if (!payload) return;
    event.preventDefault();
    send('ptv:spotify-callback', payload);
  });

  mainWindow.loadURL(proxy.origin);
  buildMenu();
  return mainWindow;
}

/**
 * Spotify sign-in callback (1.1.25).
 *
 * The renderer starts Authorization Code + PKCE in the system browser, because
 * Spotify refuses to let its own login page frame and because typing a Spotify
 * password into an app window is worse than not offering it. Spotify then
 * redirects to this address, which is registered in the viewer's Spotify app.
 * Nothing serves it: `will-navigate` below recognises it, keeps the main window
 * where it is, and hands the query to the renderer over ptv:spotify-callback.
 * The second window Spotify's flow may open is closed.
 */
const SPOTIFY_CALLBACK = 'https://cgyegcvcecvoc.github.io/PremiumTV/spotify-callback';

function spotifyCallbackPayload(url) {
  try {
    const parsed = new URL(url);
    if (parsed.origin + parsed.pathname !== SPOTIFY_CALLBACK) return null;
    return {
      code: parsed.searchParams.get('code') || '',
      state: parsed.searchParams.get('state') || '',
      error: parsed.searchParams.get('error') || '',
    };
  } catch {
    return null;
  }
}

function send(channel, payload) {
  if (mainWindow && !mainWindow.isDestroyed()) mainWindow.webContents.send(channel, payload);
}

function readWindowState() {
  const fallback = { width: 1280, height: 820 };
  try {
    const stored = JSON.parse(require('node:fs').readFileSync(paths().stateFile, 'utf8'));
    const bounds = stored && stored[WINDOW_STATE_KEY];
    if (bounds && bounds.width >= 940 && bounds.height >= 600) return bounds;
  } catch (error) {
    /* first run */
  }
  return fallback;
}

function writeWindowState() {
  if (!mainWindow || mainWindow.isDestroyed()) return;
  try {
    const bounds = mainWindow.getBounds();
    const stateFile = paths().stateFile;
    const existing = JSON.parse(require('node:fs').readFileSync(stateFile, 'utf8'));
    require('node:fs').writeFileSync(
      stateFile,
      `${JSON.stringify({ ...existing, [WINDOW_STATE_KEY]: bounds }, null, 2)}\n`,
      'utf8',
    );
  } catch (error) {
    /* window geometry is a convenience */
  }
}

// ---------------------------------------------------------------- IPC bridge

ipcMain.handle('ptv:snapshot', () => repository.snapshot());

ipcMain.handle('ptv:app-info', async () => {
  const meta = (repository.library && repository.library.meta) || null;
  // What this .app was built with. The renderer decides from these (not from
  // a downloaded copy) whether the Guide is the cable-style grid.
  const bundled = (await repository.bundledMeta()) || {};
  return {
    version: app.getVersion(),
    bundleVersion: bundled.version || '',
    libraryScope: bundled.library_scope || 'usa',
    previewFeatures: Array.isArray(bundled.preview_features) ? bundled.preview_features : [],
    electron: process.versions.electron,
    chromium: process.versions.chrome,
    node: process.versions.node,
    platform: `${os.type()} ${os.release()}`,
    arch: process.arch,
    userData: app.getPath('userData'),
    bundleDir: paths().bundleDir,
    meta,
    repositoryTimeZone: schedule.REPOSITORY_TIME_ZONE,
    publishingGraceMinutes: schedule.PUBLISHING_GRACE_MINUTES,
    checkTimes: schedule.slotTimes(),
    refresh: repository.info,
    nextAutomaticAt: repository.info.nextAutomaticAt || null,
    updates: updater ? updater.status() : null,
  };
});

ipcMain.handle('ptv:update-status', () => (updater ? updater.status() : null));

// Settings → Check for bugs: read-only environment facts for the renderer's
// report. The renderer owns the library checks; this adds only what a web page
// cannot see (whether the bundled data and the writable data folder are there).
ipcMain.handle('ptv:diagnostics', async () => {
  const options = paths();
  let bundleOk = false;
  let userDataWritable = false;
  try {
    bundleOk = fs.existsSync(path.join(options.bundleDir, 'channels.jsonl')) &&
      fs.existsSync(path.join(options.bundleDir, 'meta.json'));
    fs.accessSync(app.getPath('userData'), fs.constants.W_OK);
    userDataWritable = true;
  } catch (error) {
    userDataWritable = false;
  }
  return {
    version: app.getVersion(),
    packaged: app.isPackaged,
    bundleDir: options.bundleDir,
    bundleOk,
    userData: app.getPath('userData'),
    userDataWritable,
    arch: process.arch,
  };
});

/** Settings → Check for bugs: the last crash this Mac recorded, if any. */
ipcMain.handle('ptv:crash-log', () => crashLog.readCrash(app.getPath('userData')));

ipcMain.handle('ptv:clear-crash-log', () => {
  crashLog.clearCrash(app.getPath('userData'));
  return true;
});

ipcMain.handle('ptv:check-update', async (_event, force) => {
  if (!updater) return null;
  return updater.check(Boolean(force));
});

ipcMain.handle('ptv:download-update', async () => (updater ? updater.download() : null));

ipcMain.handle('ptv:install-update', async () =>
  (updater ? updater.openInstaller() : { ok: false, message: 'The updater is unavailable.' }));

ipcMain.handle('ptv:open-release', async () =>
  (updater ? updater.openReleasePage() : { ok: false }));

// The dismissal is launch-scoped on purpose: the updater keeps it out of the
// state file, so the notice is back the next time the app opens.
ipcMain.handle('ptv:dismiss-update-notice', () =>
  (updater ? updater.dismissNotice() : null));

ipcMain.handle('ptv:refresh', async (_event, force) => {
  return force ? autoRefresh.runManual() : repository.refresh('automatic');
});

ipcMain.handle('ptv:reset', async () => {
  await repository.resetToBundled();
  return repository.snapshot();
});

ipcMain.handle('ptv:resolve-stream', (_event, channelId, streamUrl) => {
  const channel = repository.findChannel(channelId, streamUrl);
  if (!channel || !channel.url) return { ok: false, message: 'That channel has no stream URL.' };
  const url = proxy.registerChannel(channel);
  const sessionId = new URL(url).pathname.split('/').filter(Boolean).at(-1);
  return { ok: true, url, sessionId, channel };
});

ipcMain.handle('ptv:release-stream', (_event, sessionId) => {
  proxy.releaseSession(sessionId);
  return { ok: true };
});

ipcMain.handle('ptv:logo-url', (_event, logoUrl) => {
  if (!logoUrl || !/^https?:\/\//i.test(logoUrl)) return '';
  return `${proxy.origin}/logo/?u=${encodeURIComponent(logoUrl)}`;
});

// The Live Events tab's live check (1.0.8): asks a game's stream server
// whether anything still answers. The renderer cannot reach these hosts
// itself (CSP keeps it on the loopback origin), so the main process asks:
// any HTTP answer counts — even 403 from a geo-blocked edge — because the
// viewer's question is "is anything still answering on this game". Only a
// timeout, abort or refused connection means nothing is. One byte of Range
// keeps a cooperating server from sending a body.
ipcMain.handle('ptv:probe-stream', async (_event, streamUrl) => {
  if (!streamUrl || !/^https?:\/\//i.test(streamUrl)) return false;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 5000);
  try {
    const response = await fetch(streamUrl, {
      method: 'GET',
      headers: { Range: 'bytes=0-1' },
      redirect: 'follow',
      signal: controller.signal,
    });
    return Number(response.status) > 0;
  } catch {
    return false;
  } finally {
    clearTimeout(timer);
  }
});


ipcMain.handle('ptv:open-external', (_event, url) => {
  if (/^https?:\/\//i.test(url)) shell.openExternal(url);
  return { ok: true };
});

/**
 * Settings → what the app knows about location access (1.1.18).
 *
 * Whether this bundle may ask at all, and how many times it did.
 */
ipcMain.handle('ptv:location-context', () => ({
  platform: process.platform,
  // Whether this bundle is allowed to ask at all: macOS refuses every
  // request from a bundle with no usage description.
  hasUsageDescription: process.platform !== 'darwin' || hasLocationUsageDescription(),
  asks: { ...moduleLocationAsks },
}));

/**
 * Settings → "Open location settings" (1.1.18).
 *
 * A viewer who once clicked "Don't Allow" is not asked again by the OS, so the
 * only way back is the system pane. Each platform has its own address, and
 * Linux has none that works across desktops — there, the answer is the
 * instructions instead of a dead button. Only these fixed URLs are opened; the
 * renderer cannot route an arbitrary address through this handler.
 */
ipcMain.handle('ptv:open-location-settings', async () => {
  if (process.platform === 'darwin') {
    const url = 'x-apple.systempreferences:com.apple.preference.security?Privacy_LocationServices';
    try {
      await shell.openExternal(url);
      return { ok: true, platform: 'darwin' };
    } catch (error) {
      return { ok: false, platform: 'darwin', error: error.message };
    }
  }
  if (process.platform === 'win32') {
    try {
      await shell.openExternal('ms-settings:privacy-location');
      return { ok: true, platform: 'win32' };
    } catch (error) {
      return { ok: false, platform: 'win32', error: error.message };
    }
  }
  return {
    ok: false,
    platform: process.platform,
    hint: 'Linux desktops get location from the GeoClue service: open your system settings and '
      + 'turn location on (GNOME: Settings → Privacy → Location). PremiumTV then asks as usual.',
  };
});

// -------------------------------------------------------------------- menu

function buildMenu() {
  const isMac = process.platform === 'darwin';
  const template = [
    ...(isMac ? [{ role: 'appMenu' }] : []),
    { role: 'fileMenu' },
    { role: 'editMenu' },
    {
      label: 'View',
      submenu: [
        {
          label: 'Channels',
          accelerator: 'CmdOrCtrl+1',
          click: () => send('ptv:select-tab', 'channels'),
        },
        {
          label: 'Guide',
          accelerator: 'CmdOrCtrl+2',
          click: () => send('ptv:select-tab', 'guide'),
        },
        {
          label: 'Settings',
          accelerator: 'CmdOrCtrl+3',
          click: () => send('ptv:select-tab', 'settings'),
        },
        { type: 'separator' },
        {
          label: 'Refresh Library Now',
          accelerator: 'CmdOrCtrl+R',
          click: () => {
            if (autoRefresh) autoRefresh.runManual().catch(() => {});
          },
        },
        { type: 'separator' },
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' },
      ],
    },
    { role: 'windowMenu' },
    {
      role: 'help',
      submenu: [
        {
          label: 'About the bundled playlist',
          click: () => {
            const meta = (repository.library && repository.library.meta) || {};
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: 'PremiumTV data',
              message: `Bundled ${meta.version || 'unknown'}`,
              detail: [
                `Channels: ${meta.channel_count || 0}`,
                `Categories: ${meta.group_count || 0}`,
                `Guide listings: ${meta.programme_count || 0} for ${meta.guide_channels || 0} channels`,
                `Playlist: ${meta.playlist || ''}`,
                `Guide: ${meta.guide || ''}`,
                `Generated: ${meta.generated_utc || ''}`,
              ].join('\n'),
            });
          },
        },
        {
          label: 'Check for App Updates…',
          click: () => {
            send('ptv:select-tab', 'settings');
            if (updater) updater.check(true).catch(() => {});
          },
        },
        {
          label: 'PremiumTV repository',
          click: () => shell.openExternal('https://github.com/cgyegcvcecvoc/PremiumTV'),
        },
      ],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}
