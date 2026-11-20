'use strict';

/**
 * Bounded in-place playback recovery, shared by the macOS and web players.
 *
 * Android's `ServerFallback.kt` `decideRetry()` is the same rule: a dropped
 * segment, a slow CDN edge or a decoder hiccup is not a dead feed. Retrying the
 * *same* feed a bounded number of times before spending a backup server is the
 * difference between a one-second blip and an error card on a channel that has
 * only one published feed. A permanent fault (bad HTTP status, unsupported
 * format, DRM, malformed manifest) must walk on immediately: waiting cannot fix
 * it. Each server hop starts with a fresh feed, so retries never stack on top
 * of an exhausted server list.
 *
 * Pure policy: no DOM, no Electron, no network. The tests run in plain Node,
 * and `web/tools/build.py` copies this file into the web player unchanged.
 */
(function (root) {
  const TRANSIENT_LIMIT = 2;
  const MEDIA_LIMIT = 1;

  /**
   * Classify a fatal player error without importing hls.js, mpegts.js or
   * ExoPlayer. Accepts an hls.js error `data` object, a DOM `MediaError`, an
   * `{ code, message }`-shaped object, or a plain string.
   */
  function classifyFault(error) {
    if (!error) return 'transient'; // a stall watchdog has no error object
    // DOM MediaError codes: 1 aborted, 2 network, 3 decode, 4 source unsupported.
    const mediaCode = Number((error && error.code) || 0);
    if (mediaCode === 2) return 'transient';
    if (mediaCode === 3) return 'media';
    if (mediaCode === 1 || mediaCode === 4) return 'permanent';
    const status = Number(
      (error && (error.status || error.httpStatus
        || (error.response && error.response.code))) || 0,
    );
    if (status >= 400) return 'permanent';

    const type = String((error && error.type) || '').toLowerCase();
    const detail = String(
      (error && (error.details || error.message || error.code || '')) || error,
    ).toLowerCase();

    // Provider decisions, not timing: a bad status, a key/DRM refusal, an
    // unsupported codec or a malformed/unparseable manifest.
    if (/drm|keyload|key.*error|unsupported|not.?supported|src_not_supported|parsing|invalid|forbidden|not found/.test(detail)) {
      return 'permanent';
    }
    if (type.includes('media')
      || /decode|codec|demux|mux|buffer.?append|audio.?track/.test(detail)) {
      return 'media';
    }
    return 'transient';
  }

  /**
   * @param {'transient'|'media'|'permanent'} fault
   * @param {number} retries already spent on this exact feed
   * @param {boolean} serverSwitched whether a backup server was already used
   */
  function decideRecovery(fault, retries, serverSwitched) {
    const used = Number(retries) || 0;
    const limit = fault === 'permanent' ? 0
      : fault === 'media' ? MEDIA_LIMIT : TRANSIENT_LIMIT;
    const retryInPlace = !serverSwitched && used < limit;
    return {
      retryInPlace,
      limit,
      notice: retryInPlace
        ? (fault === 'media'
          ? 'Rebuilding the decoder for this feed…'
          : 'Reconnecting to this feed…')
        : '',
    };
  }

  const api = {
    TRANSIENT_LIMIT,
    MEDIA_LIMIT,
    classifyFault,
    decideRecovery,
  };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  root.PremiumRecovery = api;
})(typeof window !== 'undefined' ? window : globalThis);
