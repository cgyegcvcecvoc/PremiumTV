/* Browser playback adapter. iOS uses native HLS first (including inline and
 * native full-screen playback); other browsers lazy-load the same pinned HLS
 * and MPEG-TS libraries as the desktop app. No proxy, forbidden headers or
 * no-cors "health checks": a response we cannot read is not a working feed. */
(function (root) {
  "use strict";
  const video = document.getElementById("video");
  const loading = document.getElementById("player-loading");
  const gesture = document.getElementById("player-gesture");
  const errorBox = document.getElementById("player-error");
  const errorText = document.getElementById("player-error-text");
  const store = root.PremiumStore;
  const scripts = new Map();
  let hls = null,
    mpegts = null,
    watchdog = null,
    audioWatchdog = null;
  let session = 0,
    strategies = [],
    attempt = 0,
    url = "",
    hint = "",
    channel = null;
  let fatalHandler = null,
    stateHandler = null,
    progressHandler = null;
  let started = false,
    manualPaused = false,
    mediaRecoveries = 0,
    triedAudio = new Set();
  let currentStrategy = "",
    pendingGesture = false;

  function emit(extra) {
    if (stateHandler)
      stateHandler(
        Object.assign(
          {
            strategy: currentStrategy,
            playing: started && !video.paused,
            paused: video.paused,
            muted: video.muted,
            volume: video.volume,
            tracks: audioTracks(),
          },
          extra || {},
        ),
      );
  }
  function clearTimers() {
    clearTimeout(watchdog);
    clearTimeout(audioWatchdog);
    watchdog = audioWatchdog = null;
  }
  function teardown() {
    clearTimers();
    if (hls) {
      try {
        hls.destroy();
      } catch (_) {}
      hls = null;
    }
    if (mpegts) {
      try {
        mpegts.pause();
        mpegts.unload();
        mpegts.detachMediaElement();
        mpegts.destroy();
      } catch (_) {}
      mpegts = null;
    }
    try {
      video.pause();
      video.removeAttribute("src");
      video.load();
    } catch (_) {}
  }
  function nativeHls() {
    return Boolean(
      video.canPlayType("application/vnd.apple.mpegurl") ||
        video.canPlayType("application/x-mpegURL"),
    );
  }
  function appleDevice() {
    return (
      /iPad|iPhone|iPod/.test(navigator.userAgent) ||
      (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1)
    );
  }
  function mse() {
    return Boolean(root.MediaSource && root.MediaSource.isTypeSupported);
  }
  function plan(original, apple, native, supported) {
    const path = String(original || "")
      .split(/[?#]/)[0]
      .toLowerCase();
    if (/\.m3u8?$/.test(path))
      return apple && native
        ? ["native", supported && "hls"].filter(Boolean)
        : [supported && "hls", native && "native"].filter(Boolean);
    if (/\.(ts|m2ts)$/.test(path))
      return [supported && !apple && "mpegts", native && "native"].filter(
        Boolean,
      );
    if (/\.(mp4|m4v|webm|ogg|mov|m4a|mp3)$/.test(path)) return ["native"];
    return ["native", native && !apple && "hls"].filter(Boolean);
  }
  function loadScript(name) {
    if (scripts.has(name)) return scripts.get(name);
    const promise = new Promise((resolve, reject) => {
      const script = document.createElement("script");
      script.src = "vendor/" + name;
      script.onload = resolve;
      script.onerror = () => {
        scripts.delete(name);
        reject(
          new Error("The player library could not load. Reconnect and retry."),
        );
      };
      document.head.appendChild(script);
    });
    scripts.set(name, promise);
    return promise;
  }
  function showError(message) {
    clearTimers();
    loading.hidden = true;
    gesture.hidden = true;
    errorBox.hidden = false;
    errorText.textContent =
      message ||
      "The provider may be offline, block browser origins (CORS), require custom headers, or use an unsupported codec. Try another server or the native app.";
    emit({ error: true });
  }
  function fatal() {
    const handler = fatalHandler;
    fatalHandler = null;
    if (handler) handler();
    else showError();
  }
  function nextStrategy() {
    teardown();
    started = false;
    pendingGesture = false;
    if (attempt >= strategies.length) fatal();
    else run(strategies[attempt++]);
  }
  function hlsConfig(isLive) {
    return {
      enableWorker: true,
      // Live events should track the edge instead of building a large safety
      // buffer. VOD keeps the more forgiving defaults for seeking/resume.
      lowLatencyMode: isLive,
      liveDurationInfinity: true,
      liveSyncDurationCount: isLive ? 3 : undefined,
      liveMaxLatencyDurationCount: isLive ? 8 : undefined,
      backBufferLength: isLive ? 10 : 30,
      maxBufferLength: isLive ? 12 : 20,
      maxMaxBufferLength: isLive ? 24 : 40,
      maxBufferSize: 30 * 1000 * 1000,
      manifestLoadingTimeOut: isLive ? 8000 : 15000,
      manifestLoadingMaxRetry: 1,
      levelLoadingTimeOut: isLive ? 8000 : 10000,
      levelLoadingMaxRetry: 1,
      fragLoadingTimeOut: isLive ? 10000 : 20000,
      fragLoadingMaxRetry: 2,
    };
  }
  function armWatchdog(id) {
    clearTimeout(watchdog);
    if (manualPaused || pendingGesture) return;
    watchdog = setTimeout(() => {
      // Also recover a previously-playing feed that stalls mid-show. A user
      // pause or autoplay gesture is never treated as a failed server.
      if (
        id === session &&
        !manualPaused &&
        !pendingGesture &&
        (!started || (video.readyState < 3 && !video.paused))
      )
        nextStrategy();
    }, channel && !channel.vod ? 12000 : 20000);
  }
  function requestPlay(id) {
    if (id !== session || manualPaused) return;
    let promise;
    try {
      promise = video.play();
    } catch (_) {
      showGesture();
      return;
    }
    if (promise && promise.catch)
      promise.catch((error) => {
        if (id !== session) return;
        if (error.name === "NotAllowedError" || error.name === "SecurityError")
          showGesture();
        else if (error.name !== "AbortError" && !hls && !mpegts) nextStrategy();
      });
  }
  function showGesture() {
    pendingGesture = true;
    clearTimers();
    loading.hidden = true;
    gesture.hidden = false;
    emit({ gesture: true });
  }
  function codecSupported(codec) {
    if (!codec) return true;
    if (/^(ac-3|ec-3|dts[chxe]?|dtsc|mlp|truehd)/i.test(codec)) return false;
    try {
      return (
        root.MediaSource.isTypeSupported('audio/mp4; codecs="' + codec + '"') ||
        root.MediaSource.isTypeSupported(
          'video/mp4; codecs="avc1.42E01E,' + codec + '"',
        )
      );
    } catch (_) {
      return false;
    }
  }
  function selectAudio() {
    if (!hls || !hls.audioTracks.length) return;
    const tracks = hls.audioTracks;
    let index = tracks.findIndex(
      (t) =>
        (!t.audioCodec || codecSupported(t.audioCodec)) &&
        !/sap|commentary|descriptive/i.test(t.name || ""),
    );
    if (index < 0)
      index = tracks.findIndex(
        (t) => !t.audioCodec || codecSupported(t.audioCodec),
      );
    if (index >= 0) {
      hls.audioTrack = index;
      triedAudio.add(index);
    }
    if (hls.levels && hls.levels.length > 1) {
      const current = hls.levels[hls.currentLevel];
      if (
        current &&
        current.audioCodec &&
        !codecSupported(current.audioCodec)
      ) {
        const best = hls.levels
          .map((level, i) => ({ level, i }))
          .filter(
            (x) => x.level.audioCodec && codecSupported(x.level.audioCodec),
          )
          .sort((a, b) => b.level.bitrate - a.level.bitrate)[0];
        if (best) hls.currentLevel = best.i;
      }
    }
  }
  function audioTracks() {
    if (hls && hls.audioTracks.length)
      return hls.audioTracks.map((t, i) => ({
        index: i,
        label: [t.name || "Audio", t.lang || ""].filter(Boolean).join(" · "),
        selected: hls.audioTrack === i,
      }));
    return Array.from(video.audioTracks || []).map((t, i) => ({
      index: i,
      label: t.label || t.language || `Audio ${i + 1}`,
      selected: t.enabled,
    }));
  }
  function monitorAudio(id) {
    clearTimeout(audioWatchdog);
    audioWatchdog = setTimeout(() => {
      if (id !== session || !started || video.paused) return;
      if (
        typeof video.webkitAudioDecodedByteCount === "number" &&
        video.webkitAudioDecodedByteCount === 0 &&
        !video.muted
      ) {
        const tracks = audioTracks();
        const next = tracks.find((t) => !triedAudio.has(t.index));
        if (next) {
          setAudio(next.index);
          monitorAudio(id);
          return;
        }
        emit({ silent: true });
      }
    }, 5000);
  }
  function onPlaying() {
    if (!started) emit({ started: true });
    started = true;
    pendingGesture = false;
    clearTimers();
    loading.hidden = true;
    gesture.hidden = true;
    errorBox.hidden = true;
    emit();
    monitorAudio(session);
  }
  async function run(strategy) {
    const id = session;
    currentStrategy = strategy;
    loading.hidden = false;
    gesture.hidden = true;
    errorBox.hidden = true;
    armWatchdog(id);
    try {
      if (strategy === "native") {
        video.src = url;
        video.addEventListener(
          "loadedmetadata",
          () => {
            if (id === session && channel && channel.vod && channel.resume)
              video.currentTime = channel.resume;
          },
          { once: true },
        );
        requestPlay(id);
      } else if (strategy === "hls") {
        await loadScript("hls.min.js");
        if (id !== session) return;
        if (!root.Hls.isSupported()) {
          nextStrategy();
          return;
        }
        hls = new root.Hls(hlsConfig(!channel.vod));
        hls.on(root.Hls.Events.ERROR, (_, data) => {
          if (id !== session || !data.fatal) return;
          if (
            data.type === root.Hls.ErrorTypes.MEDIA_ERROR &&
            mediaRecoveries++ === 0
          ) {
            try {
              hls.recoverMediaError();
              return;
            } catch (_) {}
          }
          nextStrategy();
        });
        hls.on(root.Hls.Events.MANIFEST_PARSED, () => {
          if (id !== session) return;
          selectAudio();
          requestPlay(id);
        });
        hls.on(root.Hls.Events.AUDIO_TRACKS_UPDATED, () => {
          if (id === session) {
            selectAudio();
            emit();
          }
        });
        hls.on(root.Hls.Events.AUDIO_TRACK_SWITCHED, () => {
          if (id === session) emit();
        });
        hls.loadSource(url);
        hls.attachMedia(video);
      } else {
        await loadScript("mpegts.js");
        if (id !== session) return;
        if (!root.mpegts.isSupported()) {
          nextStrategy();
          return;
        }
        mpegts = root.mpegts.createPlayer(
          { type: "mpegts", isLive: !channel.vod, url },
          {
            enableWorker: false,
            lazyLoad: true,
            lazyLoadMaxDuration: 30,
            autoCleanupSourceBuffer: true,
            liveBufferLatencyChasing: true,
          },
        );
        mpegts.on(root.mpegts.Events.ERROR, () => {
          if (id === session) nextStrategy();
        });
        mpegts.attachMediaElement(video);
        mpegts.load();
        requestPlay(id);
      }
    } catch (_) {
      if (id === session) nextStrategy();
    }
  }
  function setAudio(index) {
    if (hls && hls.audioTracks[index]) {
      hls.audioTrack = index;
      triedAudio.add(index);
    } else if (video.audioTracks && video.audioTracks[index])
      Array.from(video.audioTracks).forEach((t, i) => {
        t.enabled = i === index;
      });
    emit();
  }
  function saveAudio() {
    store.write(store.KEYS.audio, {
      volume: video.volume || 1,
      muted: video.muted,
    });
  }
  video.addEventListener("playing", onPlaying);
  video.addEventListener("waiting", () => {
    if (!manualPaused && !pendingGesture) {
      loading.hidden = false;
      // Do not restart an already-armed deadline. Some WebKit builds emit
      // repeated waiting events for a dead HLS source; resetting the timer on
      // each event could postpone failure forever.
      if (!watchdog) armWatchdog(session);
    }
  });
  video.addEventListener("error", () => {
    if (
      !video.getAttribute("src") ||
      hls ||
      mpegts ||
      manualPaused ||
      pendingGesture
    )
      return;
    nextStrategy();
  });
  video.addEventListener("pause", () => {
    // Only a deliberate user pause cancels failure detection. WebKit can deliver
    // teardown's pause event *after* the next strategy has assigned its new src;
    // checking src alone still let that stale event cancel the new watchdog.
    if (manualPaused) clearTimers();
    loading.hidden = true;
    emit();
  });
  video.addEventListener("play", () => emit());
  video.addEventListener("volumechange", () => {
    saveAudio();
    emit();
  });
  video.addEventListener("timeupdate", () => {
    if (progressHandler) progressHandler(video.currentTime, video.duration);
  });
  video.addEventListener("ended", () => {
    clearTimers();
    emit({ ended: true });
  });
  video.addEventListener("loadedmetadata", () => emit());
  const prefs = store.read(store.KEYS.audio, {});
  video.muted = Boolean(prefs.muted);
  try {
    video.volume = Number.isFinite(prefs.volume)
      ? Math.max(0, Math.min(1, prefs.volume))
      : 1;
  } catch (_) {}
  if (typeof module !== "undefined" && module.exports)
    module.exports = { plan, hlsConfig };
  root.PremiumPlayer = {
    element: video,
    plan,
    nativeHls,
    appleDevice,
    audioTracks,
    setAudio,
    play(source, original, item, handlers) {
      session++;
      teardown();
      url = source;
      hint = original || source;
      channel = item || {};
      fatalHandler = handlers.onFatal;
      stateHandler = handlers.onState;
      progressHandler = handlers.onProgress;
      started = false;
      manualPaused = false;
      pendingGesture = false;
      mediaRecoveries = 0;
      triedAudio = new Set();
      attempt = 0;
      strategies = plan(hint, appleDevice(), nativeHls(), mse());
      if (!strategies.length) {
        showError(
          "This transport stream needs Media Source Extensions, which this browser does not provide. Try Safari with native HLS, or use the native app.",
        );
        return;
      }
      loading.hidden = false;
      errorBox.hidden = true;
      gesture.hidden = true;
      // Native playback starts in the original click gesture, not after fetch.
      run(strategies[attempt++]);
    },
    stop() {
      session++;
      teardown();
      url = "";
      hint = "";
      channel = null;
      started = false;
      manualPaused = false;
      pendingGesture = false;
      fatalHandler = stateHandler = progressHandler = null;
      loading.hidden = gesture.hidden = true;
      errorBox.hidden = false;
      emit();
    },
    retry() {
      if (!channel) return;
      manualPaused = false;
      pendingGesture = false;
      started = false;
      attempt = 0;
      mediaRecoveries = 0;
      strategies = plan(hint, appleDevice(), nativeHls(), mse());
      teardown();
      if (strategies.length) run(strategies[attempt++]);
      else showError();
    },
    fail(message) {
      fatalHandler = null;
      showError(message);
    },
    toggle() {
      if (video.paused) {
        manualPaused = false;
        pendingGesture = false;
        gesture.hidden = true;
        requestPlay(session);
      } else {
        manualPaused = true;
        video.pause();
      }
    },
    resumeGesture() {
      manualPaused = false;
      pendingGesture = false;
      gesture.hidden = true;
      loading.hidden = false;
      armWatchdog(session);
      requestPlay(session);
    },
    mute() {
      video.muted = !video.muted;
      saveAudio();
      emit();
    },
    volume(value) {
      const v = Number(value);
      if (!Number.isFinite(v)) return;
      try {
        video.volume = Math.max(0, Math.min(1, v));
        if (video.volume > 0) video.muted = false;
        saveAudio();
      } catch (_) {}
      emit();
    },
    seek(seconds) {
      if (Number.isFinite(seconds) && video.seekable.length)
        video.currentTime = Math.max(
          0,
          Math.min(seconds, video.duration || seconds),
        );
    },
    skip(delta) {
      this.seek(video.currentTime + delta);
    },
    goLive() {
      if (video.seekable.length)
        video.currentTime = Math.max(
          0,
          video.seekable.end(video.seekable.length - 1) - 1,
        );
      requestPlay(session);
    },
    get isStarted() {
      return started;
    },
  };
})(window);
