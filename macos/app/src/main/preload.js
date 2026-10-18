'use strict';

/**
 * The only surface the renderer gets. contextIsolation is on and nodeIntegration
 * is off, so the window sees these functions and nothing else: no require, no
 * filesystem, no shell.
 */

const { contextBridge, ipcRenderer } = require('electron');

function subscribe(channel, callback) {
  const listener = (_event, payload) => callback(payload);
  ipcRenderer.on(channel, listener);
  return () => ipcRenderer.removeListener(channel, listener);
}

contextBridge.exposeInMainWorld('premiumtv', {
  /** Everything the UI needs on first paint. */
  getSnapshot: () => ipcRenderer.invoke('ptv:snapshot'),
  /** Versions, paths, refresh slots and the bundle provenance. */
  getAppInfo: () => ipcRenderer.invoke('ptv:app-info'),
  /** Settings → Force refresh all now (true) or a validator-based check (false). */
  refresh: (force) => ipcRenderer.invoke('ptv:refresh', Boolean(force)),
  /** Settings → Reset to the bundled copy. */
  resetToBundled: () => ipcRenderer.invoke('ptv:reset'),
  /** Returns the loopback URL whose requests carry the channel's headers. */
  resolveStream: (channelId, streamUrl) => ipcRenderer.invoke('ptv:resolve-stream', channelId, streamUrl),
  releaseStream: (sessionId) => ipcRenderer.invoke('ptv:release-stream', sessionId),
  /** Logo URLs go through the main process so they can be cached and proxied. */
  logoUrl: (logoUrl) => ipcRenderer.invoke('ptv:logo-url', logoUrl),
  openExternal: (url) => ipcRenderer.invoke('ptv:open-external', url),

  /** App updates: check GitHub, download once, then open the verified DMG. */
  updateStatus: () => ipcRenderer.invoke('ptv:update-status'),
  checkForUpdate: (force) => ipcRenderer.invoke('ptv:check-update', Boolean(force)),
  downloadUpdate: () => ipcRenderer.invoke('ptv:download-update'),
  installUpdate: () => ipcRenderer.invoke('ptv:install-update'),
  openReleasePage: () => ipcRenderer.invoke('ptv:open-release'),
  /** The popup's "Remind me next time": hides it for this launch only. */
  dismissUpdateNotice: () => ipcRenderer.invoke('ptv:dismiss-update-notice'),

  onState: (callback) => subscribe('ptv:state', callback),
  onInfo: (callback) => subscribe('ptv:info', callback),
  onProgress: (callback) => subscribe('ptv:progress', callback),
  onSelectTab: (callback) => subscribe('ptv:select-tab', callback),
  onUpdate: (callback) => subscribe('ptv:update', callback),
});
