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
 */

window.PremiumPlayer = (function () {
  const video = document.getElementById('video');
  const spinner = document.getElementById('player-spinner');
  const errorBox = document.getElementById('player-error');
  const errorText = document.getElementById('player-error-text');

  let hls = null;
  let mpegtsPlayer = null;
  let currentUrl = '';
  let sourceHint = '';
  let attempts = [];
  let index = 0;

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
      showError(
        'This stream could not be played. The feed is either offline or refuses this connection; the nightly link check removes links like this.',
      );
      return;
    }
    const strategy = attempts[index];
    index += 1;
    showSpinner(true);
    if (strategy === 'hls') playWithHls();
    else if (strategy === 'mpegts') playWithMpegts();
    else playNative();
  }

  function onPlaying() {
    showSpinner(false);
    clearError();
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
    hls.loadSource(currentUrl);
    hls.attachMedia(video);
    hls.on(window.Hls.Events.MANIFEST_PARSED, () => {
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
  video.addEventListener('error', () => {
    if (hls || mpegtsPlayer) return; // those players report their own errors
    teardown();
    tryNext();
  });

  return {
    /** Starts playback of an already-resolved loopback URL. */
    play(url, originalUrl = '') {
      teardown();
      currentUrl = url;
      sourceHint = originalUrl;
      attempts = strategiesFor(originalUrl || url);
      index = 0;
      clearError();
      showSpinner(true);
      if (!attempts.length) {
        showError('No player is available for this stream format.');
        return;
      }
      tryNext();
    },

    stop() {
      teardown();
      currentUrl = '';
      sourceHint = '';
      attempts = [];
      index = 0;
      showSpinner(false);
      clearError();
    },

    retry() {
      if (currentUrl) this.play(currentUrl, sourceHint);
    },

    setMuted(muted) {
      video.muted = muted;
    },

    get element() {
      return video;
    },
  };
})();
