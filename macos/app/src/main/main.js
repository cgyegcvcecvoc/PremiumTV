'use strict';

/**
 * PremiumTV for Mac — application entry point.
 *
 * Wires the four pieces together: the loopback server the window is served
 * from, the repository that owns the channel list and the guide, the refresh
 * scheduler that mirrors the repository's publishing windows, and the window
 * itself. Nothing here talks to the renderer except through the preload bridge.
 */

const { app, BrowserWindow, Menu, ipcMain, powerMonitor, shell, dialog } = require('electron');
const path = require('node:path');
const os = require('node:os');
const fs = require('node:fs');

const { TvRepository } = require('./repository');
const { StreamProxy } = require('./stream-proxy');
const { AutoRefresh } = require('./auto-refresh');
const { AppUpdater } = require('./updater');
const schedule = require('./refresh-schedule');

const WINDOW_STATE_KEY = 'window-bounds';
const smokeMode = process.argv.includes('--smoke-test');
if (smokeMode) {
  app.setPath('userData', require('node:fs').mkdtempSync(path.join(os.tmpdir(), 'premiumtv-smoke-')));
  setTimeout(() => app.exit(1), 90000).unref();
}

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
  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit();
  });
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
    else mainWindow.show();
  });

  app.whenReady().then(async () => {
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

  mainWindow.once('ready-to-show', () => mainWindow.show());
  mainWindow.on('close', writeWindowState);

  // Anything the renderer tries to open in a new window goes to the browser.
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (/^https?:\/\//i.test(url)) shell.openExternal(url);
    return { action: 'deny' };
  });

  mainWindow.loadURL(proxy.origin);
  buildMenu();
  return mainWindow;
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

ipcMain.handle('ptv:open-external', (_event, url) => {
  if (/^https?:\/\//i.test(url)) shell.openExternal(url);
  return { ok: true };
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
          label: 'PremiumTV1 repository',
          click: () => shell.openExternal('https://github.com/cgyegcvcecvoc/PremiumTV1'),
        },
      ],
    },
  ];
  Menu.setApplicationMenu(Menu.buildFromTemplate(template));
}
