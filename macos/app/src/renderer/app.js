'use strict';

/**
 * The PremiumTV interface: Channels, Guide and Settings.
 *
 * The channels and the guide arrive from the main process, which owns both the
 * copy bundled inside the .app and any copy a refresh downloaded. This file
 * only renders that data and asks for playback; it never touches the network
 * or the filesystem.
 */

(function () {
  const api = window.premiumtv;

  const els = {
    tabs: document.getElementById('tabs'),
    categories: document.getElementById('categories'),
    footCount: document.getElementById('foot-count'),
    search: document.getElementById('search'),
    channelsTitle: document.getElementById('channels-title'),
    channelsSubtitle: document.getElementById('channels-subtitle'),
    channelsGrid: document.getElementById('channels-grid'),
    guideList: document.getElementById('guide-list'),
    guideSubtitle: document.getElementById('guide-subtitle'),
    settingsBody: document.getElementById('settings-body'),
    statusText: document.getElementById('status-text'),
    views: {
      channels: document.getElementById('view-channels'),
      guide: document.getElementById('view-guide'),
      settings: document.getElementById('view-settings'),
    },
    player: document.getElementById('player'),
    playerName: document.getElementById('player-name'),
    playerNow: document.getElementById('player-now'),
    playerNext: document.getElementById('player-next'),
    playerDetail: document.getElementById('player-detail'),
    playerClose: document.getElementById('player-close'),
    playerRetry: document.getElementById('player-retry'),
  };

  const ui = {
    tab: 'channels',
    category: null, // null = every channel
    query: '',
    rendered: 0,
  };

  const PAGE = 240;
  let snapshot = { state: { phase: 'loading' }, info: {}, library: { channels: [], groups: [], programmes: [] } };
  let programmeIndex = new Map();
  let playingSession = null;
  let clockTimer = null;

  // ------------------------------------------------------------- utilities

  function nowSeconds() {
    return Math.floor(Date.now() / 1000);
  }

  function formatClock(epochSeconds) {
    return new Date(epochSeconds * 1000).toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' });
  }

  function formatStamp(epochMillis) {
    if (!epochMillis) return 'never';
    return new Date(epochMillis).toLocaleString([], {
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    });
  }

  function relativeFromNow(epochMillis) {
    if (!epochMillis) return '';
    const minutes = Math.round((epochMillis - Date.now()) / 60000);
    if (minutes < 1) return 'in under a minute';
    if (minutes < 60) return `in ${minutes} min`;
    const hours = Math.round(minutes / 60);
    if (hours < 24) return `in ${hours} h`;
    return `in ${Math.round(hours / 24)} d`;
  }

  function escapeText(value) {
    return String(value == null ? '' : value);
  }

  /** For the few places a value is interpolated into markup rather than textContent. */
  function escapeHtml(value) {
    return escapeText(value).replace(/[&<>"']/g, (char) => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
    })[char]);
  }

  function logoSource(channel) {
    if (!channel.logo) return '';
    return `/logo/?u=${encodeURIComponent(channel.logo)}`;
  }

  function buildProgrammeIndex(programmes) {
    const index = new Map();
    for (const programme of programmes) {
      const list = index.get(programme.c);
      if (list) list.push(programme);
      else index.set(programme.c, [programme]);
    }
    return index;
  }

  /** What is on now, and what follows, for one channel. */
  function nowPlaying(channelId, atSeconds) {
    const list = programmeIndex.get(channelId);
    if (!list || !list.length) return { current: null, next: null };
    let current = null;
    let next = null;
    for (const programme of list) {
      if (programme.s <= atSeconds && programme.e > atSeconds) {
        current = programme;
        continue;
      }
      if (programme.s > atSeconds) {
        next = programme;
        break;
      }
    }
    if (!current && next === null && list.length) {
      // Everything listed has finished: the next listing is still worth naming.
      const upcoming = list.find((p) => p.e > atSeconds);
      if (upcoming) next = upcoming;
    }
    return { current, next };
  }

  function progressOf(programme, atSeconds) {
    if (!programme) return 0;
    const total = Math.max(1, programme.e - programme.s);
    return Math.min(100, Math.max(0, ((atSeconds - programme.s) / total) * 100));
  }

  // -------------------------------------------------------------- rendering

  function renderCategories() {
    const groups = snapshot.library.groups || [];
    const total = (snapshot.library.channels || []).length;
    els.categories.textContent = '';

    const all = document.createElement('button');
    all.className = 'cat';
    all.setAttribute('aria-current', String(ui.category === null));
    all.innerHTML = `<span class="cat-name">All channels</span><span class="cat-count">${total}</span>`;
    all.addEventListener('click', () => selectCategory(null));
    els.categories.appendChild(all);

    for (const group of groups) {
      const button = document.createElement('button');
      button.className = 'cat';
      button.setAttribute('aria-current', String(ui.category === group.name));
      button.innerHTML = `<span class="cat-name"></span><span class="cat-count">${group.count}</span>`;
      button.querySelector('.cat-name').textContent = group.name;
      button.addEventListener('click', () => selectCategory(group.name));
      els.categories.appendChild(button);
    }

    els.footCount.textContent = `${total} channels · ${groups.length} categories`;
  }

  function visibleChannels() {
    const channels = snapshot.library.channels || [];
    const query = ui.query.trim().toLowerCase();
    return channels.filter((channel) => {
      if (ui.category && channel.group !== ui.category) return false;
      if (!query) return true;
      return (
        channel.name.toLowerCase().includes(query) ||
        channel.group.toLowerCase().includes(query) ||
        (channel.country || '').toLowerCase().includes(query)
      );
    });
  }

  function channelCard(channel) {
    const card = document.createElement('button');
    card.className = 'card';
    card.type = 'button';

    const logo = logoSource(channel);
    const { current } = nowPlaying(channel.id, nowSeconds());
    // The logo URL is percent-encoded and every piece of channel text is set
    // through textContent, so a hostile group name or logo URL cannot inject
    // markup into a card.
    card.innerHTML = `${logo ? '<img class="card-logo" loading="lazy" alt="" />' : '<div class="card-logo empty"></div>'}<span class="card-name"></span><span class="card-now"></span>`;

    const logoEl = card.querySelector('.card-logo');
    if (logo) {
      logoEl.addEventListener('error', () => {
        const fallback = document.createElement('div');
        fallback.className = 'card-logo empty';
        fallback.textContent = channel.group;
        logoEl.replaceWith(fallback);
      });
      logoEl.src = logo;
    } else {
      logoEl.textContent = channel.group;
    }
    card.querySelector('.card-name').textContent = channel.name;
    const nowEl = card.querySelector('.card-now');
    if (current) {
      nowEl.textContent = current.t;
      nowEl.classList.add('live');
    } else {
      nowEl.textContent = programmeIndex.has(channel.id) ? 'Nothing listed at this hour' : channel.country || channel.group;
    }
    card.addEventListener('click', () => openPlayer(channel));
    return card;
  }

  function renderChannels() {
    const channels = visibleChannels();
    els.channelsTitle.textContent = ui.query.trim() ? `Search: ${ui.query.trim()}` : ui.category || 'All channels';
    els.channelsSubtitle.textContent = ui.query.trim()
      ? `${channels.length} matching channels`
      : `${channels.length} channels in ${ui.category || 'every category'}`;

    els.channelsGrid.textContent = '';
    ui.rendered = 0;
    appendChannelPage(channels);
  }

  function appendChannelPage(channels) {
    const list = channels || visibleChannels();
    const slice = list.slice(ui.rendered, ui.rendered + PAGE);
    const fragment = document.createDocumentFragment();
    for (const channel of slice) fragment.appendChild(channelCard(channel));
    els.channelsGrid.appendChild(fragment);
    ui.rendered += slice.length;

    if (!list.length && !els.channelsGrid.querySelector('.empty-state')) {
      const empty = document.createElement('div');
      empty.className = 'empty-state';
      empty.textContent = snapshot.state.phase === 'error' ? snapshot.state.message : 'No channels match this search.';
      els.channelsGrid.appendChild(empty);
    }
  }

  function renderGuide() {
    const at = nowSeconds();
    const query = ui.query.trim().toLowerCase();
    const channels = (snapshot.library.channels || []).filter((channel) => programmeIndex.has(channel.id));

    const rows = channels
      .map((channel) => ({ channel, ...nowPlaying(channel.id, at) }))
      .filter((row) => row.current || row.next)
      .filter((row) =>
        !query
          ? true
          : row.channel.name.toLowerCase().includes(query) ||
            (row.current && row.current.t.toLowerCase().includes(query)) ||
            row.channel.group.toLowerCase().includes(query),
      )
      .sort((a, b) => a.channel.name.localeCompare(b.channel.name));

    const withGuide = new Set(programmeIndex.keys()).size;
    els.guideSubtitle.textContent = `${rows.length} channels with something listed right now · the guide covers ${withGuide} of ${(snapshot.library.channels || []).length} channels`;

    els.guideList.textContent = '';
    if (!rows.length) {
      const empty = document.createElement('div');
      empty.className = 'empty-state';
      empty.textContent = snapshot.library.guideError
        ? `The programme guide is unavailable: ${snapshot.library.guideError}`
        : 'Nothing is listed at this hour. The repository publishes a new guide twice a day.';
      els.guideList.appendChild(empty);
      return;
    }

    const fragment = document.createDocumentFragment();
    for (const row of rows) {
      const item = document.createElement('div');
      item.className = 'guide-row';
      item.tabIndex = 0;
      item.setAttribute('role', 'button');

      const left = document.createElement('div');
      left.className = 'guide-channel';
      const name = document.createElement('span');
      name.textContent = row.channel.name;
      const category = document.createElement('span');
      category.className = 'guide-cat';
      category.textContent = row.channel.group;
      left.append(name, category);

      const middle = document.createElement('div');
      const title = document.createElement('div');
      title.className = 'guide-title';
      title.textContent = row.current ? row.current.t : 'Nothing on right now';
      const times = document.createElement('div');
      times.className = 'guide-times';
      times.textContent = row.current
        ? `${formatClock(row.current.s)} – ${formatClock(row.current.e)}`
        : row.next
          ? `Next at ${formatClock(row.next.s)}`
          : '';
      middle.append(title, times);

      if (row.current) {
        const bar = document.createElement('div');
        bar.className = 'bar';
        const fill = document.createElement('span');
        fill.style.width = `${progressOf(row.current, at).toFixed(1)}%`;
        bar.appendChild(fill);
        middle.appendChild(bar);
      }

      const nextLine = document.createElement('div');
      nextLine.className = 'guide-next';
      if (row.next) {
        nextLine.innerHTML = 'Next · <b></b>';
        nextLine.querySelector('b').textContent = row.next.t;
      } else {
        nextLine.textContent = 'No further listing today';
      }
      middle.appendChild(nextLine);

      const clock = document.createElement('div');
      clock.className = 'guide-clock';
      clock.textContent = formatClock(at);

      item.append(left, middle, clock);
      item.addEventListener('click', () => openPlayer(row.channel));
      item.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          openPlayer(row.channel);
        }
      });
      fragment.appendChild(item);
    }
    els.guideList.appendChild(fragment);
  }

  function renderSettings() {
    const meta = snapshot.library.meta || {};
    const info = snapshot.info || {};
    const source = snapshot.state.source;

    const sourceBadge =
      source === 'cache'
        ? '<span class="badge ok">Downloaded copy</span>'
        : source === 'bundled'
          ? '<span class="badge">Bundled in the app</span>'
          : '<span class="badge bad">Unavailable</span>';

    const lastResult = info.lastMessage
      ? `${info.lastMessage}`
      : 'No refresh has been attempted in this install yet.';
    const resultClass = info.lastSuccessAt && info.lastSuccessAt >= (info.lastAttemptAt || 0) ? 'ok' : 'warn';

    els.settingsBody.innerHTML = `
      <div class="panel">
        <h2>Library</h2>
        <div class="actions">
          <button class="btn btn-primary" id="force-refresh">Force refresh all now</button>
          <button class="btn" id="check-now">Check for changes</button>
          <button class="btn btn-danger" id="reset-bundled">Reset to the bundled copy</button>
        </div>
        <p><span id="busy" class="badge ${resultClass}">${escapeHtml(info.lastTrigger || 'idle')}</span> &nbsp; ${sourceBadge}</p>
        <dl class="meta">
          <dt>Last attempt</dt><dd>${formatStamp(info.lastAttemptAt)}${info.lastTrigger ? ` · ${escapeHtml(info.lastTrigger)}` : ''}</dd>
          <dt>Last success</dt><dd>${formatStamp(info.lastSuccessAt)}</dd>
          <dt>Last result</dt><dd>${escapeHtml(lastResult)}</dd>
          <dt>Next automatic check</dt><dd>${formatStamp(info.nextAutomaticAt)} <span class="muted">${escapeHtml(
            relativeFromNow(info.nextAutomaticAt),
          )}</span></dd>
        </dl>
      </div>

      <div class="panel">
        <h2>What is installed</h2>
        <dl class="meta">
          <dt>Version</dt><dd>${escapeHtml(meta.version || 'unknown')}</dd>
          <dt>Channels</dt><dd>${escapeHtml(meta.channel_count || (snapshot.library.channels || []).length)}</dd>
          <dt>Categories</dt><dd>${escapeHtml(meta.group_count || (snapshot.library.groups || []).length)}</dd>
          <dt>Guide listings</dt><dd>${escapeHtml(meta.programme_count || (snapshot.library.programmes || []).length)} for ${escapeHtml(
            meta.guide_channels || new Set(programmeIndex.keys()).size,
          )} channels</dd>
          <dt>Guide window</dt><dd>${meta.window_start ? `${formatClock(meta.window_start)} – ${formatClock(meta.window_end)}` : 'unknown'}</dd>
          <dt>Playlist source</dt><dd>${escapeHtml(meta.playlist || '')}</dd>
          <dt>Guide source</dt><dd>${escapeHtml(meta.guide || '')}</dd>
          <dt>Built</dt><dd>${escapeHtml(meta.generated_utc || '')}</dd>
          <dt>Refresh URL (playlist)</dt><dd>${escapeHtml(meta.playlist_url || '')}</dd>
          <dt>Refresh URL (guide)</dt><dd>${escapeHtml(meta.guide_url || '')}</dd>
        </dl>
      </div>

      <div class="panel">
        <h2>Automatic checks</h2>
        <p>Checks follow this repository's publishing jobs in <b>${escapeHtml(
          appInfo.repositoryTimeZone || 'America/New_York',
        )}</b>, ${escapeHtml(String(appInfo.publishingGraceMinutes || 45))} minutes after each slot so the
        publishing job has finished writing. A check sends the last ETag and Last-Modified value, so an
        unchanged playlist and guide cost two small <code>304 Not Modified</code> responses instead of a
        10 MB guide download.</p>
        <p class="muted">Check times: ${escapeHtml((appInfo.checkTimes || []).join(', '))}</p>
      </div>

      <div class="panel">
        <h2>Known limitations</h2>
        <div class="note">
          <p><b>Automatic and forced refreshes cannot read this repository while it is private.</b>
          <code>raw.githubusercontent.com</code> returns an access error to an unauthenticated Mac, so a refresh
          reports that result and the bundled copy stays in use. Refreshes start working when an owner-approved
          public mirror or delivery URL exists; no GitHub credential is stored in this app.</p>
        </div>
        <ul class="plain">
          <li>Only ${escapeHtml(String(meta.guide_channels || new Set(programmeIndex.keys()).size))} of the bundled
            channels have real listings. The rest show "Nothing listed at this hour" rather than an invented schedule.</li>
          <li>A link stays in the playlist until the nightly deep check confirms it is dead, so a few channels
            will not play.</li>
          <li>This app is ad-hoc signed: it is not notarized by Apple. On first launch, right-click it in
            Applications and choose Open, or clear the quarantine attribute.</li>
        </ul>
      </div>

      <div class="panel">
        <h2>About this build</h2>
        <dl class="meta">
          <dt>PremiumTV</dt><dd>${escapeHtml(appInfo.version || '')}</dd>
          <dt>Electron</dt><dd>${escapeHtml(appInfo.electron || '')}</dd>
          <dt>Chromium</dt><dd>${escapeHtml(appInfo.chromium || '')}</dd>
          <dt>Platform</dt><dd>${escapeHtml(appInfo.platform || '')} (${escapeHtml(appInfo.arch || '')})</dd>
          <dt>App data</dt><dd>${escapeHtml(appInfo.userData || '')}</dd>
          <dt>Bundled data</dt><dd>${escapeHtml(appInfo.bundleDir || '')}</dd>
        </dl>
      </div>
    `;

    document.getElementById('force-refresh').addEventListener('click', () => runRefresh(true, 'force-refresh'));
    document.getElementById('check-now').addEventListener('click', () => runRefresh(false, 'check-now'));
    document.getElementById('reset-bundled').addEventListener('click', resetToBundled);
  }

  let appInfo = {};

  // -------------------------------------------------------------- actions

  function selectTab(tab) {
    ui.tab = tab;
    for (const [name, view] of Object.entries(els.views)) view.hidden = name !== tab;
    for (const button of els.tabs.querySelectorAll('.tab')) {
      button.setAttribute('aria-selected', String(button.dataset.tab === tab));
    }
    els.categories.style.display = tab === 'channels' ? '' : 'none';
    els.search.placeholder = tab === 'guide' ? 'Search the guide' : 'Search channels';
    render();
  }

  function selectCategory(name) {
    ui.category = name;
    renderCategories();
    renderChannels();
    document.getElementById('content').scrollTop = 0;
  }

  function render() {
    if (ui.tab === 'channels') renderChannels();
    else if (ui.tab === 'guide') renderGuide();
    else renderSettings();
  }

  async function runRefresh(force, buttonId) {
    const button = buttonId ? document.getElementById(buttonId) : null;
    if (button) {
      button.disabled = true;
      button.textContent = force ? 'Refreshing…' : 'Checking…';
    }
    els.statusText.textContent = force ? 'Downloading the playlist and the guide…' : 'Checking the repository…';
    try {
      await api.refresh(force);
      snapshot = await api.getSnapshot();
      programmeIndex = buildProgrammeIndex(snapshot.library.programmes || []);
    } finally {
      if (button) {
        button.disabled = false;
        button.textContent = force ? 'Force refresh all now' : 'Check for changes';
      }
      render();
    }
  }

  async function resetToBundled() {
    els.statusText.textContent = 'Resetting to the bundled copy…';
    snapshot = await api.resetToBundled();
    programmeIndex = buildProgrammeIndex(snapshot.library.programmes || []);
    renderCategories();
    render();
  }

  async function openPlayer(channel) {
    const resolved = await api.resolveStream(channel.id);
    if (!resolved.ok) {
      els.statusText.textContent = resolved.message;
      return;
    }
    playingSession = resolved.sessionId;
    els.playerName.textContent = channel.name;
    const at = nowSeconds();
    const { current, next } = nowPlaying(channel.id, at);
    els.playerNow.textContent = current ? `Now · ${current.t}` : '';
    els.playerNext.textContent = next ? `Next · ${next.t} at ${formatClock(next.s)}` : '';
    els.playerDetail.textContent = current && current.d ? current.d : channel.group;
    els.player.hidden = false;
    els.statusText.textContent = `Playing ${channel.name}`;
    // The proxy URL is /p/<session>, without a file extension. Pass the
    // original stream URL as a format hint so HLS/MPEG-TS gets the right
    // player first instead of trying native playback of every feed.
    window.PremiumPlayer.play(resolved.url, channel.url);
  }

  async function closePlayer() {
    window.PremiumPlayer.stop();
    els.player.hidden = true;
    if (playingSession) {
      await api.releaseStream(playingSession);
      playingSession = null;
    }
    els.statusText.textContent = snapshot.state.message || '';
  }

  // ---------------------------------------------------------------- wiring

  els.tabs.addEventListener('click', (event) => {
    const button = event.target.closest('.tab');
    if (button) selectTab(button.dataset.tab);
  });

  els.search.addEventListener('input', () => {
    ui.query = els.search.value;
    if (ui.tab === 'settings') selectTab('channels');
    render();
  });

  els.playerClose.addEventListener('click', closePlayer);
  els.playerRetry.addEventListener('click', () => window.PremiumPlayer.retry());

  document.getElementById('content').addEventListener('scroll', (event) => {
    if (ui.tab !== 'channels') return;
    const node = event.target;
    if (node.scrollTop + node.clientHeight >= node.scrollHeight - 600) {
      const total = visibleChannels().length;
      if (ui.rendered < total) appendChannelPage();
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !els.player.hidden) {
      closePlayer();
      return;
    }
    if (event.key === ' ' && !els.player.hidden && event.target === document.body) {
      event.preventDefault();
      const video = window.PremiumPlayer.element;
      if (video.paused) video.play();
      else video.pause();
    }
    if (event.key === '/' && document.activeElement !== els.search) {
      event.preventDefault();
      els.search.focus();
    }
  });

  api.onState((state) => {
    snapshot.state = state;
    els.statusText.textContent = state.message || '';
    if (state.phase === 'ready') {
      renderCategories();
      render();
    } else if (state.phase === 'error') {
      els.channelsGrid.innerHTML = `<div class="empty-state">${escapeHtml(state.message)}</div>`;
    }
  });

  api.onInfo((info) => {
    snapshot.info = info;
    els.statusText.textContent = info.lastMessage || snapshot.state.message || '';
    if (ui.tab === 'settings') renderSettings();
  });

  api.onProgress(() => {
    els.statusText.textContent = 'Channels ready; loading the guide…';
  });

  api.onSelectTab((tab) => selectTab(tab));

  window.addEventListener('beforeunload', () => {
    window.PremiumPlayer.stop();
  });

  async function boot() {
    appInfo = await api.getAppInfo();
    snapshot = await api.getSnapshot();
    programmeIndex = buildProgrammeIndex(snapshot.library.programmes || []);
    els.statusText.textContent = snapshot.state.message || '';
    renderCategories();
    selectTab('channels');

    // Keep "now playing" honest without a full re-render storm.
    clockTimer = window.setInterval(() => {
      if (ui.tab === 'guide') renderGuide();
      else if (ui.tab === 'channels' && ui.rendered <= PAGE) renderChannels();
    }, 30000);
  }

  boot().catch((error) => {
    els.statusText.textContent = `Startup failed: ${error.message}`;
  });
})();
