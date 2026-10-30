'use strict';

/**
 * Playback.
 *
 * Chromium will not play an HLS playlist or an MPEG-TS transport stream on its
 * own, and both are common in public IPTV feeds, so each is handed to the
 * matching player: hls.js for .m3u8, mpegts.js for .ts, with the native
 * <video> element tried as well. When the first attempt fails the next one is
 * tried before the app gives up and says so - a stream that only plays one way
 * should not look broken.
 *
 * Every URL comes from the loopback proxy, so the referrer, origin and
 * user-agent a playlist entry publishes are attached by the main process, not
 * here.
 *
 * 1.1.3 audio recovery:
 * - Prefers HLS variant levels and alternate audio renditions whose codec MSE
 *   can actually decode (avoiding undecodable AC-3 / E-AC-3 or video-only
 *   variants when an AAC rendition is published beside them).
 * - Monitors `webkitAudioDecodedByteCount` once video frames advance; if zero
 *   audio bytes are decoded, cycles alternate HLS audio tracks (such as silent
 *   SAP tracks), falls back from mpegts.js when MPEG-TS carries AC-3/MP2 audio,
 *   and reports persistent silence so the UI can hop to a backup server or let
 *   the viewer switch audio tracks manually.
 */

window.PremiumPlayer = (function () {
  const video = document.getElementById('video');
  const spinner = document.getElementById('player-spinner');
  const errorBox = document.getElementById('player-error');
  const errorText = document.getElementById('player-error-text');

  const AUDIO_PREF_KEY = 'premiumtv.audio.v1';
  const scheduleTimer = typeof setTimeout === 'function' ? setTimeout : null;
  const cancelTimer = typeof clearTimeout === 'function' ? clearTimeout : null;

  let hls = null;
  let mpegtsPlayer = null;
  let currentUrl = '';
  let sourceHint = '';
  let attempts = [];
  let index = 0;
  let activeStrategy = '';
  let sessionCounter = 0;
  let watchdogTimer = null;
  let triedAudioTracks = new Set();
  let triedAltLevel = false;
  let silentReported = false;
  let audioListener = null;
  // Set by play(): called instead of the error card when this URL has been
  // tried every way, so app.js can switch to the channel's next server.
  let onFatal = null;

  function loadAudioPrefs() {
    try {
      const store = window.localStorage;
      if (!store) return { volume: 1, muted: false };
      const raw = JSON.parse(store.getItem(AUDIO_PREF_KEY) || 'null');
      if (!raw || typeof raw !== 'object') return { volume: 1, muted: false };
      const rawVol = Number(raw.volume);
      const volume = Number.isFinite(rawVol) ? Math.min(1, Math.max(0.05, rawVol)) : 1;
      return { volume, muted: Boolean(raw.muted) };
    } catch (error) {
      return { volume: 1, muted: false };
    }
  }

  function saveAudioPrefs(volume, muted) {
    try {
      const store = window.localStorage;
      if (!store) return;
      store.setItem(AUDIO_PREF_KEY, JSON.stringify({ volume, muted: Boolean(muted) }));
    } catch (error) {
      /* storage unavailable */
    }
  }

  function applySavedAudioPrefs() {
    const prefs = loadAudioPrefs();
    try {
      video.volume = prefs.volume;
      video.muted = prefs.muted;
    } catch (error) {
      /* mock element */
    }
  }

  applySavedAudioPrefs();

  function isAudioCodecSupported(codec) {
    if (!codec || typeof codec !== 'string') return false;
    const trimmed = codec.trim();
    if (!trimmed) return false;
    const mse = window.MediaSource;
    if (mse && typeof mse.isTypeSupported === 'function') {
      try {
        if (mse.isTypeSupported(`audio/mp4; codecs="${trimmed}"`)) return true;
        if (mse.isTypeSupported(`video/mp4; codecs="avc1.42E01E,${trimmed}"`)) return true;
        return false;
      } catch (error) {
        /* fall back to codec pattern */
      }
    }
    return !/^(ac-3|ec-3|dts|dtsc|dtsh|dtse|dtsx|mlp|truehd)/i.test(trimmed);
  }

  function isSecondaryTrackName(track) {
    const label = `${track?.name || ''} ${track?.attrs?.CHARACTERISTICS || ''}`;
    return /\b(sap|descriptive|description|dvs|commentary|clean|karaoke)\b/i.test(label);
  }

  function formatTrackLabel(track, idx) {
    if (!track) return `Track ${idx + 1}`;
    const parts = [];
    if (track.name) parts.push(String(track.name).trim());
    if (track.lang && (!track.name || !track.name.toLowerCase().includes(String(track.lang).toLowerCase()))) {
      parts.push(String(track.lang).toUpperCase());
    }
    return parts.join(' · ') || `Track ${idx + 1}`;
  }

  function currentAudioTracks() {
    if (hls && Array.isArray(hls.audioTracks) && hls.audioTracks.length > 0) {
      return hls.audioTracks.map((track, idx) => ({
        index: idx,
        label: formatTrackLabel(track, idx),
        lang: track.lang || '',
        codec: track.audioCodec || '',
        selected: hls.audioTrack === idx,
      }));
    }
    const nativeTracks = video && video.audioTracks;
    if (nativeTracks && typeof nativeTracks.length === 'number' && nativeTracks.length > 0) {
      const list = [];
      for (let i = 0; i < nativeTracks.length; i += 1) {
        const track = nativeTracks[i];
        list.push({
          index: i,
          label: formatTrackLabel({ name: track.label, lang: track.language }, i),
          lang: track.language || '',
          codec: '',
          selected: Boolean(track.enabled),
        });
      }
      return list;
    }
    return [];
  }

  function emitAudioState(extra = {}) {
    if (typeof audioListener !== 'function') return;
    const tracks = currentAudioTracks();
    const active = tracks.find((t) => t.selected) || tracks[0] || null;
    try {
      audioListener({
        tracks,
        activeTrack: active,
        muted: Boolean(video.muted),
        volume: typeof video.volume === 'number' ? video.volume : 1,
        silent: false,
        ...extra,
      });
    } catch (error) {
      /* listener errors never break playback */
    }
  }

  function clearWatchdog() {
    if (watchdogTimer && cancelTimer) {
      cancelTimer(watchdogTimer);
    }
    watchdogTimer = null;
  }

  function selectPlayableHlsVariantAndTrack() {
    if (!hls) return;
    if (Array.isArray(hls.levels) && hls.levels.length > 1) {
      const playableLevels = hls.levels
        .map((lvl, idx) => ({ lvl, idx }))
        .filter(({ lvl }) => lvl && lvl.audioCodec && isAudioCodecSupported(lvl.audioCodec));
      if (playableLevels.length > 0 && playableLevels.length < hls.levels.length) {
        const currentIdx = typeof hls.currentLevel === 'number' && hls.currentLevel >= 0
          ? hls.currentLevel
          : 0;
        const currentLvl = hls.levels[currentIdx];
        if (!currentLvl || !currentLvl.audioCodec || !isAudioCodecSupported(currentLvl.audioCodec)) {
          const best = playableLevels.sort((a, b) => (b.lvl.bitrate || 0) - (a.lvl.bitrate || 0))[0];
          hls.currentLevel = best.idx;
        }
      }
    }
    if (Array.isArray(hls.audioTracks) && hls.audioTracks.length > 1) {
      const currentIdx = typeof hls.audioTrack === 'number' ? hls.audioTrack : 0;
      const current = hls.audioTracks[currentIdx];
      const currentPlayable = current && (!current.audioCodec || isAudioCodecSupported(current.audioCodec));
      const currentSecondary = isSecondaryTrackName(current);
      if (!currentPlayable || currentSecondary) {
        const candidateIdx = hls.audioTracks.findIndex(
          (track) => (!track.audioCodec || isAudioCodecSupported(track.audioCodec)) && !isSecondaryTrackName(track),
        );
        const fallbackIdx = candidateIdx >= 0
          ? candidateIdx
          : hls.audioTracks.findIndex((track) => !track.audioCodec || isAudioCodecSupported(track.audioCodec));
        if (fallbackIdx >= 0 && fallbackIdx !== currentIdx) {
          hls.audioTrack = fallbackIdx;
        }
      }
      if (typeof hls.audioTrack === 'number' && hls.audioTrack >= 0) {
        triedAudioTracks.add(hls.audioTrack);
      }
    }
    emitAudioState();
  }

  function armAudioWatchdog(sessionId) {
    clearWatchdog();
    if (!scheduleTimer) return;
    const startTime = typeof video.currentTime === 'number' ? video.currentTime : 0;
    const startVideoBytes = typeof video.webkitVideoDecodedByteCount === 'number'
      ? video.webkitVideoDecodedByteCount
      : null;

    watchdogTimer = scheduleTimer(() => {
      watchdogTimer = null;
      if (sessionId !== sessionCounter) return;
      if (video.paused || video.ended) return;
      if (typeof video.webkitAudioDecodedByteCount !== 'number') return;

      const advanced = (typeof video.currentTime === 'number' ? video.currentTime : 0) - startTime;
      const videoBytes = typeof video.webkitVideoDecodedByteCount === 'number'
        ? video.webkitVideoDecodedByteCount
        : null;
      const videoMoving = advanced >= 1.5 && (videoBytes === null || videoBytes > (startVideoBytes || 0));

      if (!videoMoving) {
        armAudioWatchdog(sessionId);
        return;
      }

      if (video.webkitAudioDecodedByteCount > 0) {
        silentReported = false;
        emitAudioState({ silent: false });
        return;
      }

      // Zero audio bytes decoded while video is advancing: recover in order.
      if (hls && Array.isArray(hls.audioTracks) && hls.audioTracks.length > 1) {
        if (typeof hls.audioTrack === 'number' && hls.audioTrack >= 0) {
          triedAudioTracks.add(hls.audioTrack);
        }
        let nextTrack = -1;
        for (let offset = 1; offset <= hls.audioTracks.length; offset += 1) {
          const candidate = ((hls.audioTrack >= 0 ? hls.audioTrack : 0) + offset) % hls.audioTracks.length;
          if (!triedAudioTracks.has(candidate)) {
            const track = hls.audioTracks[candidate];
            if (!track.audioCodec || isAudioCodecSupported(track.audioCodec)) {
              nextTrack = candidate;
              break;
            }
          }
        }
        if (nextTrack >= 0) {
          triedAudioTracks.add(nextTrack);
          hls.audioTrack = nextTrack;
          emitAudioState({
            silent: false,
            switchedTrack: formatTrackLabel(hls.audioTracks[nextTrack], nextTrack),
          });
          armAudioWatchdog(sessionId);
          return;
        }
      }

      if (hls && !triedAltLevel && Array.isArray(hls.levels) && hls.levels.length > 1) {
        const altIdx = hls.levels.findIndex(
          (lvl, idx) => idx !== hls.currentLevel && lvl?.audioCodec && isAudioCodecSupported(lvl.audioCodec),
        );
        if (altIdx >= 0) {
          triedAltLevel = true;
          hls.currentLevel = altIdx;
          armAudioWatchdog(sessionId);
          return;
        }
      }

      if (activeStrategy === 'mpegts' && index < attempts.length) {
        // mpegts.js silently drops AC-3 / E-AC-3 / MP2 audio elementary streams;
        // hand off to the remaining strategy before declaring no audio.
        teardown();
        tryNext();
        return;
      }

      if (!silentReported) {
        silentReported = true;
        emitAudioState({ silent: true });
      }
    }, 3400);
  }

  function showSpinner(on) {
    spinner.hidden = !on;
  }

  function showError(message) {
    showSpinner(false);
    errorText.textContent = message;
    errorBox.hidden = false;
  }

  function clearError() {
    errorBox.hidden = true;
  }

  function teardown() {
    clearWatchdog();
    if (hls) {
      try {
        hls.destroy();
      } catch (error) {
        /* already gone */
      }
      hls = null;
    }
    if (mpegtsPlayer) {
      try {
        mpegtsPlayer.pause();
        mpegtsPlayer.unload();
        mpegtsPlayer.detachMediaElement();
        mpegtsPlayer.destroy();
      } catch (error) {
        /* already gone */
      }
      mpegtsPlayer = null;
    }
    try {
      video.pause();
      video.removeAttribute('src');
      video.load();
    } catch (error) {
      /* nothing attached */
    }
  }

  /** Strategy order depends on what the URL looks like. */
  function strategiesFor(url) {
    const hasHls = Boolean(window.Hls) && window.Hls.isSupported();
    const hasMpegts = Boolean(window.mpegts) && window.mpegts.isSupported();
    const path = url.split('?')[0].toLowerCase();

    if (/\.m3u8?$/.test(path)) {
      return [hasHls && 'hls', 'native', hasMpegts && 'mpegts'].filter(Boolean);
    }
    if (/\.(ts|m2ts)$/.test(path)) {
      return [hasMpegts && 'mpegts', 'native', hasHls && 'hls'].filter(Boolean);
    }
    return ['native', hasHls && 'hls', hasMpegts && 'mpegts'].filter(Boolean);
  }

  function tryNext() {
    if (index >= attempts.length) {
      if (onFatal) {
        const handler = onFatal;
        onFatal = null;
        handler();
        return;
      }
      showError(
        'This stream could not be played. The feed is either offline or refuses this connection; the nightly link check removes links like this.',
      );
      return;
    }
    const strategy = attempts[index];
    activeStrategy = strategy;
    index += 1;
    showSpinner(true);
    if (strategy === 'hls') playWithHls();
    else if (strategy === 'mpegts') playWithMpegts();
    else playNative();
  }

  function onPlaying() {
    showSpinner(false);
    clearError();
    emitAudioState();
    armAudioWatchdog(sessionCounter);
  }

  function playNative() {
    video.src = currentUrl;
    video.play().catch(() => {
      /* autoplay policy or a bad stream: fall through */
    });
  }

  function playWithHls() {
    hls = new window.Hls({
      enableWorker: true,
      lowLatencyMode: false,
      liveDurationInfinity: true,
      backBufferLength: 30,
      manifestLoadingTimeOut: 15000,
      manifestLoadingMaxRetry: 1,
      levelLoadingMaxRetry: 2,
      fragLoadingMaxRetry: 2,
    });
    hls.on(window.Hls.Events.ERROR, (_event, data) => {
      if (!data.fatal) return;
      if (data.type === window.Hls.ErrorTypes.NETWORK_ERROR && index < attempts.length) {
        teardown();
        tryNext();
      } else if (data.type === window.Hls.ErrorTypes.MEDIA_ERROR) {
        try {
          hls.recoverMediaError();
        } catch (error) {
          teardown();
          tryNext();
        }
      } else {
        teardown();
        tryNext();
      }
    });
    if (window.Hls.Events.AUDIO_TRACKS_UPDATED) {
      hls.on(window.Hls.Events.AUDIO_TRACKS_UPDATED, () => {
        selectPlayableHlsVariantAndTrack();
      });
    }
    if (window.Hls.Events.AUDIO_TRACK_SWITCHED) {
      hls.on(window.Hls.Events.AUDIO_TRACK_SWITCHED, () => {
        emitAudioState();
      });
    }
    hls.loadSource(currentUrl);
    hls.attachMedia(video);
    hls.on(window.Hls.Events.MANIFEST_PARSED, () => {
      selectPlayableHlsVariantAndTrack();
      video.play().catch(() => {});
    });
  }

  function playWithMpegts() {
    mpegtsPlayer = window.mpegts.createPlayer(
      { type: 'mpegts', isLive: true, url: currentUrl },
      { enableWorker: false, liveBufferLatencyChasing: true, autoCleanupSourceBuffer: true },
    );
    mpegtsPlayer.on(window.mpegts.Events.ERROR, () => {
      teardown();
      tryNext();
    });
    mpegtsPlayer.attachMediaElement(video);
    mpegtsPlayer.load();
    mpegtsPlayer.play();
  }

  video.addEventListener('playing', onPlaying);
  video.addEventListener('waiting', () => showSpinner(true));
  video.addEventListener('volumechange', () => emitAudioState());
  video.addEventListener('error', () => {
    if (hls || mpegtsPlayer) return; // those players report their own errors
    teardown();
    tryNext();
  });

  return {
    /**
     * Starts playback of an already-resolved loopback URL. `handlers.onFatal`
     * (optional) is called instead of the error card when every strategy for
     * this URL has failed, so the app can fall back to another server.
     */
    play(url, originalUrl = '', handlers = {}) {
      teardown();
      sessionCounter += 1;
      triedAudioTracks = new Set();
      triedAltLevel = false;
      silentReported = false;
      currentUrl = url;
      sourceHint = originalUrl;
      attempts = strategiesFor(originalUrl || url);
      index = 0;
      activeStrategy = '';
      onFatal = typeof handlers.onFatal === 'function' ? handlers.onFatal : null;
      applySavedAudioPrefs();
      clearError();
      showSpinner(true);
      emitAudioState();
      if (!attempts.length) {
        showError('No player is available for this stream format.');
        return;
      }
      tryNext();
    },

    stop() {
      sessionCounter += 1;
      teardown();
      currentUrl = '';
      sourceHint = '';
      attempts = [];
      index = 0;
      activeStrategy = '';
      triedAudioTracks = new Set();
      triedAltLevel = false;
      silentReported = false;
      onFatal = null;
      showSpinner(false);
      clearError();
      emitAudioState();
    },

    retry() {
      if (currentUrl) this.play(currentUrl, sourceHint, { onFatal });
    },

    /** Show the final error card; the app calls this when its server list ran out. */
    fail(message) {
      onFatal = null;
      showSpinner(false);
      showError(message);
    },

    audioTracks() {
      return currentAudioTracks();
    },

    cycleAudioTrack() {
      if (hls && Array.isArray(hls.audioTracks) && hls.audioTracks.length > 1) {
        const next = ((hls.audioTrack >= 0 ? hls.audioTrack : 0) + 1) % hls.audioTracks.length;
        triedAudioTracks.add(next);
        hls.audioTrack = next;
        const chosen = formatTrackLabel(hls.audioTracks[next], next);
        emitAudioState({ switchedTrack: chosen });
        return chosen;
      }
      const nativeTracks = video && video.audioTracks;
      if (nativeTracks && typeof nativeTracks.length === 'number' && nativeTracks.length > 1) {
        let currentIdx = 0;
        for (let i = 0; i < nativeTracks.length; i += 1) {
          if (nativeTracks[i].enabled) {
            currentIdx = i;
            break;
          }
        }
        const next = (currentIdx + 1) % nativeTracks.length;
        for (let i = 0; i < nativeTracks.length; i += 1) {
          nativeTracks[i].enabled = i === next;
        }
        const chosen = formatTrackLabel(
          { name: nativeTracks[next].label, lang: nativeTracks[next].language },
          next,
        );
        emitAudioState({ switchedTrack: chosen });
        return chosen;
      }
      return null;
    },

    isMuted() {
      return Boolean(video.muted);
    },

    setMuted(muted) {
      const next = Boolean(muted);
      video.muted = next;
      const vol = typeof video.volume === 'number' && video.volume > 0 ? video.volume : 1;
      if (!next && video.volume === 0) video.volume = 1;
      saveAudioPrefs(vol, next);
      emitAudioState();
    },

    toggleMute() {
      this.setMuted(!this.isMuted());
      return this.isMuted();
    },

    getVolume() {
      return typeof video.volume === 'number' ? video.volume : 1;
    },

    setVolume(value) {
      const clamped = Math.min(1, Math.max(0, Number(value)));
      if (!Number.isFinite(clamped)) return;
      video.volume = clamped;
      if (clamped > 0 && video.muted) {
        video.muted = false;
      } else if (clamped === 0) {
        video.muted = true;
      }
      saveAudioPrefs(clamped > 0 ? clamped : 1, video.muted);
      emitAudioState();
    },

    onAudioState(listener) {
      audioListener = typeof listener === 'function' ? listener : null;
    },

    isAudioCodecSupported,

    get element() {
      return video;
    },
  };
})();
