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
    guideGrid: document.getElementById('guide-grid'),
    guideInfo: document.getElementById('guide-info'),
    guideTag: document.getElementById('guide-tag'),
    liveList: document.getElementById('live-list'),
    liveSubtitle: document.getElementById('live-subtitle'),
    settingsBody: document.getElementById('settings-body'),
    statusText: document.getElementById('status-text'),
    views: {
      channels: document.getElementById('view-channels'),
      live: document.getElementById('view-live'),
      guide: document.getElementById('view-guide'),
      settings: document.getElementById('view-settings'),
    },
    splash: document.getElementById('splash'),
    splashStatus: document.getElementById('splash-status'),
    splashVersion: document.getElementById('splash-version'),
    player: document.getElementById('player'),
    playerName: document.getElementById('player-name'),
    playerNow: document.getElementById('player-now'),
    playerNext: document.getElementById('player-next'),
    playerDetail: document.getElementById('player-detail'),
    playerServer: document.getElementById('player-server'),
    playerClose: document.getElementById('player-close'),
    playerPrevServer: document.getElementById('player-prev-server'),
    playerNextServer: document.getElementById('player-next-server'),
    playerFavorite: document.getElementById('player-favorite'),
    playerRetry: document.getElementById('player-retry'),
    // The startup "go and update" popup.
    updateNotice: document.getElementById('update-notice'),
    updateNoticeEyebrow: document.getElementById('update-notice-eyebrow'),
    updateNoticeTitle: document.getElementById('update-notice-title'),
    updateNoticeMessage: document.getElementById('update-notice-message'),
    updateNoticeSurpriseWrap: document.getElementById('update-notice-surprise-wrap'),
    updateNoticeSurprise: document.getElementById('update-notice-surprise'),
    updateNoticeVersions: document.getElementById('update-notice-versions'),
    updateNoticeUrl: document.getElementById('update-notice-url'),
    updateNoticeAction: document.getElementById('update-notice-action'),
    updateNoticeDismiss: document.getElementById('update-notice-dismiss'),
    updateNoticeFoot: document.getElementById('update-notice-foot'),
  };

  const RECENT_CATEGORY = '__recent__';
  const FAVORITE_CATEGORY = '__favorites__';

  const ui = {
    tab: 'channels',
    category: null, // null = every channel; RECENT/FAVORITE_CATEGORY = personal shelves
    query: '',
    // Search is click-to-activate (1.0.6): hovering or tabbing past the field
    // must never start a search. Only an explicit click (or '/' / Enter on the
    // focused field) makes it editable; typing is debounced before rendering.
    searchActive: false,
    rendered: 0,
    // The cable-style grid: rows (one per channel) interleaved with category
    // headings, rendered a page at a time as the grid scrolls.
    guideItems: [],
    guideRows: [],
    guideRendered: 0,
    guideWindowStart: 0,
    guideMetrics: null,
    guideFocusTime: 0,
  };

  const PAGE = 240;
  let snapshot = { state: { phase: 'loading' }, info: {}, library: { channels: [], groups: [], programmes: [] } };
  let programmeIndex = new Map();
  // The scrapers' live-game feeds, grouped by sport (Live Events tab) and
  // indexed by URL (LIVE labels, server fallback).
  let liveSections = [];
  let liveIndex = new Map();
  // Multi-server playback: the ordered server list of the open player.
  let playQueue = [];
  let playQueueIndex = 0;
  // Recently watched + Favorites, persisted per machine (personal.js logic).
  const personal = window.PremiumPersonal;
  let recentKeys = personal.load(window.localStorage, personal.RECENTS_KEY);
  let favoriteKeys = personal.load(window.localStorage, personal.FAVORITES_KEY);
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
  function formatMegabytes(bytes) {
    const value = Number(bytes) || 0;
    return value > 0 ? `${(value / (1024 * 1024)).toFixed(1)} MB` : '';
  }

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

  /** Everything derived from the library: programme index + live-game views. */
  function rebuildDerivedIndexes(library) {
    programmeIndex = buildProgrammeIndex((library && library.programmes) || []);
    const channels = (library && library.channels) || [];
    liveSections = window.PremiumLive.buildSections(channels);
    liveIndex = window.PremiumLive.indexByChannel(channels);
  }

  /** What is on now, and what follows, for one channel. */
  function nowPlaying(channelId, atSeconds) {
    return nowPlayingFrom(programmeIndex.get(channelId) || [], atSeconds);
  }

  /**
   * The listings a channel shows: its real guide when one exists, otherwise
   * the scrapers' live-game name - event feeds share placeholder EPG ids, so
   * no upstream guide ever lists them, but the matchup is known.
   */
  function listingsFor(channel) {
    const list = programmeIndex.get(channel.id);
    if (list && list.length) return list;
    const event = liveIndex.get(channel.url);
    if (!event) return [];
    const at = nowSeconds();
    return [{
      c: channel.id,
      s: at - 21600,
      e: at + 64800,
      t: event.title,
      d: `Live ${event.sport} event feed. Game streams are published without an upstream schedule, so the matchup comes from the playlist itself.`,
      g: event.sport,
    }];
  }

  /** What is on now, and what follows, in one listing track. */
  function nowPlayingFrom(list, atSeconds) {
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

  // The cable-style guide grid: channels down the left, programmes to the
  // right, times across the top in half-hour slots, eight hours from the
  // current half hour. It replaces the "on now" list on builds whose bundle
  // enables the cable-guide preview feature.
  const GUIDE_WINDOW_SECONDS = 8 * 60 * 60;
  const GUIDE_SLOT_SECONDS = 30 * 60;
  const GUIDE_SLOTS = GUIDE_WINDOW_SECONDS / GUIDE_SLOT_SECONDS;
  const GUIDE_PAGE = 120;
  const channelCollator = new Intl.Collator(undefined, { numeric: true, sensitivity: 'base' });

  /**
   * Whether this build shows the cable-style grid as its Guide. The answer
   * comes from the bundle baked into this app (reported by the main process)
   * first, so a downloaded copy from an older stable install can never hide
   * the grid of a preview build; the active library's metadata is the fallback.
   */
  function cableGuideEnabled() {
    const fromBuild = appInfo && Array.isArray(appInfo.previewFeatures) && appInfo.previewFeatures.includes('cable-guide');
    const features = snapshot.library.meta && snapshot.library.meta.preview_features;
    return Boolean(fromBuild) || (Array.isArray(features) && features.includes('cable-guide'));
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

    const shelves = [
      [RECENT_CATEGORY, '◷ Recently watched', personal.resolve(recentKeys, snapshot.library.channels || []).length],
      [FAVORITE_CATEGORY, '★ Favorites', personal.resolve(favoriteKeys, snapshot.library.channels || []).length],
    ];
    for (const [key, label, count] of shelves) {
      const button = document.createElement('button');
      button.className = 'cat cat-personal';
      button.setAttribute('aria-current', String(ui.category === key));
      button.innerHTML = `<span class="cat-name">${label}</span><span class="cat-count">${count}</span>`;
      button.addEventListener('click', () => selectCategory(key));
      els.categories.appendChild(button);
    }

    els.footCount.textContent = `${total} channels · ${groups.length} categories`;
  }

  function visibleChannels() {
    const all = snapshot.library.channels || [];
    if (ui.category === RECENT_CATEGORY) return personal.resolve(recentKeys, all);
    if (ui.category === FAVORITE_CATEGORY) return personal.resolve(favoriteKeys, all);
    const channels = all;
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
    const event = liveIndex.get(channel.url);
    // The logo URL is percent-encoded, every piece of channel text is set
    // through textContent, and the only interpolated markup is the app's own
    // static placeholder SVG, so nothing remote can inject markup into a card.
    const placeholder = window.PremiumIcons.svgForGroup(channel.group, 'card-logo placeholder');
    card.innerHTML = `${logo ? '<img class="card-logo" loading="lazy" alt="" />' : placeholder}<span class="card-name"></span><span class="card-now"></span>`;

    const logoEl = card.querySelector('img.card-logo');
    if (logoEl) {
      logoEl.addEventListener('error', () => {
        const fallback = document.createElement('div');
        fallback.className = 'card-logo empty';
        fallback.innerHTML = placeholder;
        logoEl.replaceWith(fallback);
      });
      logoEl.src = logo;
    }
    card.querySelector('.card-name').textContent = channel.name;
    const nowEl = card.querySelector('.card-now');
    if (current) {
      nowEl.textContent = current.t;
      nowEl.classList.add('live');
    } else if (event) {
      nowEl.textContent = `LIVE · ${event.sport}`;
      nowEl.classList.add('live');
    } else if (programmeIndex.has(channel.id)) {
      nowEl.textContent = 'Nothing listed at this hour';
    } else {
      nowEl.textContent = channel.country ? `${channel.country} · No listing published` : 'No listing published';
    }
    card.addEventListener('click', () => openPlayer(channel));
    return card;
  }

  function renderChannels() {
    const channels = visibleChannels();
    const specialTitle = ui.category === RECENT_CATEGORY
      ? 'Recently watched'
      : ui.category === FAVORITE_CATEGORY ? 'Favorites' : null;
    els.channelsTitle.textContent = specialTitle || (ui.query.trim() ? `Search: ${ui.query.trim()}` : ui.category || 'All channels');
    els.channelsSubtitle.textContent = specialTitle
      ? (channels.length
        ? `${channels.length} ${ui.category === RECENT_CATEGORY ? 'channels you opened, newest first — pick one to keep watching' : 'favorite channels'}`
        : ui.category === RECENT_CATEGORY
          ? 'Channels you open will appear here so you can jump back in quickly.'
          : 'Star a channel from the player (☆ Favorite) and it will live here.')
      : ui.query.trim()
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
      empty.textContent = snapshot.state.phase === 'error'
        ? snapshot.state.message
        : ui.category === RECENT_CATEGORY
          ? 'Nothing here yet — open any channel and it will appear under Recently watched.'
          : ui.category === FAVORITE_CATEGORY
            ? 'No favorites yet — open a channel and press ☆ Favorite in the player.'
            : 'No channels match this search.';
      els.channelsGrid.appendChild(empty);
    }
  }

  function renderGuide() {
    const grid = cableGuideEnabled();
    els.guideGrid.hidden = !grid;
    els.guideInfo.hidden = !grid;
    els.guideList.hidden = grid;
    els.guideTag.hidden = !grid;
    if (grid) {
      els.guideTag.textContent = 'Cable guide';
      els.guideList.textContent = '';
      renderCableGuide();
      return;
    }
    els.guideGrid.textContent = '';
    renderGuideList();
  }

  function renderGuideList() {
    const at = nowSeconds();
    const query = ui.query.trim().toLowerCase();
    const channels = (snapshot.library.channels || []).filter(
      (channel) => programmeIndex.has(channel.id) || liveIndex.has(channel.url),
    );

    const rows = channels
      .map((channel) => ({ channel, ...nowPlayingFrom(listingsFor(channel), at) }))
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
      if (row.current) {
        const pill = document.createElement('span');
        pill.className = 'now-pill';
        pill.textContent = 'NOW';
        title.appendChild(pill);
      }
      title.appendChild(document.createTextNode(row.current ? row.current.t : 'Nothing on right now'));
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

  // --------------------------------------------------------- live events tab

  function eventCard(event) {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'event-card';
    const servers = event.servers.length > 1
      ? `${event.servers.length} streams · switchable in the player`
      : '1 stream';
    card.innerHTML = '<div class="event-head"><span class="now-pill">LIVE</span>' +
      `<span class="event-sport">${window.PremiumIcons.svgForGroup(event.sport, 'ph-icon event-icon')}</span></div>` +
      '<span class="event-title"></span><span class="event-servers"></span>';
    card.querySelector('.event-sport').insertAdjacentText('beforeend', event.sport);
    card.querySelector('.event-title').textContent = event.title;
    card.querySelector('.event-servers').textContent = servers;
    card.addEventListener('click', () => openPlayer(event.servers[0], event.servers));
    return card;
  }

  function renderLive() {
    const query = ui.query.trim().toLowerCase();
    const sections = liveSections
      .map((section) => ({
        sport: section.sport,
        events: section.events.filter((event) => !query ||
          event.title.toLowerCase().includes(query) ||
          event.sport.toLowerCase().includes(query)),
      }))
      .filter((section) => section.events.length);

    const games = sections.reduce((total, section) => total + section.events.length, 0);
    const feeds = sections.reduce(
      (total, section) => total + section.events.reduce((sum, event) => sum + event.servers.length, 0),
      0,
    );
    els.liveSubtitle.textContent = games
      ? `${games} games across ${feeds} streams · grouped by sport · a game with more than one stream can be switched in the player and falls back by itself`
      : 'Games the repository\u2019s scrapers have on air right now, grouped by sport.';

    els.liveList.textContent = '';
    if (!games) {
      const empty = document.createElement('div');
      empty.className = 'empty-state';
      empty.textContent = query
        ? 'No live game matches that search.'
        : 'No live games are in the current playlist. Game feeds appear here while the ' +
          'repository\u2019s scrapers find them on air - check back around kickoff, or browse ' +
          'the Sports channels in the Channels tab.';
      els.liveList.appendChild(empty);
      return;
    }
    for (const section of sections) {
      const header = document.createElement('div');
      header.className = 'event-section';
      header.innerHTML = `<span class="event-section-icon">${window.PremiumIcons.svgForGroup(section.sport, 'ph-icon')}</span>` +
        '<span class="event-section-name"></span><span class="event-section-count"></span>';
      header.querySelector('.event-section-name').textContent = section.sport;
      header.querySelector('.event-section-count').textContent =
        `${section.events.length} ${section.events.length === 1 ? 'game' : 'games'}`;
      els.liveList.appendChild(header);
      const grid = document.createElement('div');
      grid.className = 'event-grid';
      for (const event of section.events) grid.appendChild(eventCard(event));
      els.liveList.appendChild(grid);
    }
  }

  function guideMetrics() {
    const width = els.guideGrid.clientWidth || 1000;
    const label = Math.round(Math.min(260, Math.max(190, width * 0.24)));
    // About two and a quarter hours across, like a cable box, with room for a
    // title in a half-hour cell.
    const slot = Math.round(Math.min(240, Math.max(130, (width - label) / 4.5)));
    return { label, slot, pxPerSecond: slot / GUIDE_SLOT_SECONDS, timeline: slot * GUIDE_SLOTS };
  }

  function cableRow(channel, start, end, query) {
    const guide = programmeIndex.get(channel.id) || [];
    const programmes = guide.filter((programme) => programme.e > start && programme.s < end);
    if (!programmes.length) return null;
    if (query) {
      const channelMatches = channel.name.toLowerCase().includes(query) ||
        channel.group.toLowerCase().includes(query) ||
        (channel.country || '').toLowerCase().includes(query);
      const programmeMatches = programmes.some((programme) =>
        programme.t.toLowerCase().includes(query) || (programme.g || '').toLowerCase().includes(query),
      );
      if (!channelMatches && !programmeMatches) return null;
    }
    return { channel, programmes };
  }

  /**
   * One row per guide channel, in the published category order (the order the
   * Channels tab uses), each channel's feeds collapsed to the first one: the
   * backups of a channel share its EPG id, so they would only repeat the row.
   */
  function guideRows(start, end, query) {
    const channels = snapshot.library.channels || [];
    const groupOrder = new Map((snapshot.library.groups || []).map((group, index) => [group.name, index]));
    const rank = (channel) => (groupOrder.has(channel.group) ? groupOrder.get(channel.group) : groupOrder.size);
    const ordered = channels
      .map((channel, index) => ({ channel, index }))
      .sort((a, b) => rank(a.channel) - rank(b.channel) || a.index - b.index);
    const seen = new Set();
    const rows = [];
    for (const { channel } of ordered) {
      if (ui.category && channel.group !== ui.category) continue;
      const key = channel.id || channel.url;
      if (seen.has(key)) continue;
      const row = cableRow(channel, start, end, query);
      if (!row) continue;
      seen.add(key);
      rows.push(row);
    }
    return rows;
  }

  function guideItemsFrom(rows) {
    const items = [];
    let group = null;
    const counts = new Map();
    for (const row of rows) counts.set(row.channel.group, (counts.get(row.channel.group) || 0) + 1);
    rows.forEach((row, index) => {
      if (row.channel.group !== group) {
        group = row.channel.group;
        items.push({ type: 'section', name: group, count: counts.get(group) });
      }
      items.push({ type: 'row', row, index });
    });
    return items;
  }

  function channelLogo(channel, className) {
    const logo = document.createElement('span');
    logo.className = className;
    const logoUrl = logoSource(channel);
    if (logoUrl) {
      const image = document.createElement('img');
      image.loading = 'lazy';
      image.alt = '';
      image.src = logoUrl;
      image.addEventListener('error', () => {
        // The category's drawn placeholder replaces art that will not load.
        logo.innerHTML = window.PremiumIcons.svgForGroup(channel.group);
        logo.classList.add('empty');
      }, { once: true });
      logo.appendChild(image);
    } else {
      logo.innerHTML = window.PremiumIcons.svgForGroup(channel.group);
      logo.classList.add('empty');
    }
    return logo;
  }

  function cableSection(item) {
    const section = document.createElement('div');
    section.className = 'cable-section';
    const name = document.createElement('span');
    name.className = 'cable-section-name';
    name.textContent = item.name;
    const count = document.createElement('span');
    count.className = 'cable-section-count';
    count.textContent = `${item.count} ${item.count === 1 ? 'channel' : 'channels'}`;
    section.append(name, count);
    return section;
  }

  function cableChannelRow(row, rowIndex, start, end, at, metrics) {
    const item = document.createElement('div');
    item.className = 'cable-row';
    item.dataset.row = String(rowIndex);
    item.setAttribute('role', 'row');

    const label = document.createElement('button');
    label.type = 'button';
    label.className = 'cable-channel';
    label.dataset.row = String(rowIndex);
    label.title = `${row.channel.name} · ${row.channel.group}`;
    label.setAttribute('role', 'rowheader');
    label.addEventListener('click', () => openPlayer(row.channel));

    const number = document.createElement('span');
    number.className = 'cable-number';
    number.textContent = row.channel.chno || '';
    const text = document.createElement('span');
    text.className = 'cable-channel-text';
    const name = document.createElement('span');
    name.className = 'cable-channel-name';
    name.textContent = row.channel.name;
    const group = document.createElement('span');
    group.className = 'cable-channel-group';
    group.textContent = row.channel.country ? `${row.channel.group} · ${row.channel.country}` : row.channel.group;
    text.append(name, group);
    if (row.channel.chno) label.append(number);
    label.append(channelLogo(row.channel, 'cable-logo'), text);

    const timeline = document.createElement('div');
    timeline.className = 'cable-track';
    for (let slot = 0; slot < GUIDE_SLOTS; slot += 1) {
      const gridline = document.createElement('span');
      gridline.className = 'cable-gridline';
      gridline.style.left = `${slot * metrics.slot}px`;
      timeline.appendChild(gridline);
    }

    row.programmes.forEach((programme, programmeIndex) => {
      const visibleStart = Math.max(programme.s, start);
      const visibleEnd = Math.min(programme.e, end);
      if (visibleEnd <= visibleStart) return;
      const cell = document.createElement('button');
      cell.type = 'button';
      const current = at >= programme.s && at < programme.e;
      cell.className = `cable-programme${current ? ' current' : ''}${programme.e <= at ? ' past' : ''}`;
      cell.dataset.row = String(rowIndex);
      cell.dataset.programme = String(programmeIndex);
      cell.dataset.s = String(programme.s);
      cell.dataset.e = String(programme.e);
      cell.setAttribute('role', 'gridcell');
      cell.style.left = `${(visibleStart - start) * metrics.pxPerSecond}px`;
      cell.style.width = `${Math.max(4, (visibleEnd - visibleStart) * metrics.pxPerSecond)}px`;
      cell.title = `${formatClock(programme.s)}–${formatClock(programme.e)} · ${programme.t}`;
      cell.addEventListener('click', () => openPlayer(row.channel));

      const time = document.createElement('span');
      time.className = 'cable-programme-time';
      time.textContent = programme.s < start ? `‹ ${formatClock(programme.s)}` : formatClock(programme.s);
      const title = document.createElement('span');
      title.className = 'cable-programme-title';
      title.textContent = programme.t;
      cell.append(time, title);
      timeline.appendChild(cell);
    });

    const marker = document.createElement('span');
    marker.className = 'cable-now-line';
    marker.hidden = !(at >= start && at < end);
    marker.style.left = `${(at - start) * metrics.pxPerSecond}px`;
    timeline.appendChild(marker);

    item.append(label, timeline);
    return item;
  }

  function appendCablePage() {
    const items = ui.guideItems;
    if (ui.guideRendered >= items.length) return false;
    const metrics = ui.guideMetrics || guideMetrics();
    const fragment = document.createDocumentFragment();
    const start = ui.guideWindowStart;
    const end = start + GUIDE_WINDOW_SECONDS;
    const at = nowSeconds();
    let rows = 0;
    while (ui.guideRendered < items.length && rows < GUIDE_PAGE) {
      const item = items[ui.guideRendered];
      if (item.type === 'section') {
        fragment.appendChild(cableSection(item));
      } else {
        fragment.appendChild(cableChannelRow(item.row, item.index, start, end, at, metrics));
        rows += 1;
      }
      ui.guideRendered += 1;
    }
    els.guideGrid.appendChild(fragment);
    return true;
  }

  function guideTimeHeader(start, at, metrics) {
    const header = document.createElement('div');
    header.className = 'cable-row cable-header-row';
    header.setAttribute('role', 'row');
    const stub = document.createElement('div');
    stub.className = 'cable-channel cable-header-stub';
    stub.textContent = new Date(start * 1000).toLocaleDateString([], { weekday: 'short', month: 'short', day: 'numeric' });
    const times = document.createElement('div');
    times.className = 'cable-track cable-time-track';
    for (let slot = 0; slot < GUIDE_SLOTS; slot += 1) {
      const tick = document.createElement('span');
      tick.className = 'cable-time-tick';
      tick.style.left = `${slot * metrics.slot}px`;
      tick.textContent = formatClock(start + slot * GUIDE_SLOT_SECONDS);
      tick.setAttribute('role', 'columnheader');
      times.appendChild(tick);
    }
    const nowMarker = document.createElement('span');
    nowMarker.className = 'guide-now-marker';
    placeNowMarker(nowMarker, at, start, metrics);
    times.appendChild(nowMarker);
    header.append(stub, times);
    return header;
  }

  /** The red time pill on the NOW line; kept clear of the date cell just after the half hour. */
  function placeNowMarker(marker, at, start, metrics) {
    const x = (at - start) * metrics.pxPerSecond;
    marker.textContent = formatClock(at);
    marker.style.left = `${x}px`;
    marker.style.transform = x < 36 ? 'translateX(-2px)' : 'translateX(-50%)';
  }

  /** The detail strip above the grid: what the highlighted cell is playing. */
  function showGuideInfo(row, programme) {
    const info = els.guideInfo;
    info.textContent = '';
    const at = nowSeconds();
    if (!row) {
      const lead = document.createElement('div');
      lead.className = 'guide-info-main';
      const title = document.createElement('div');
      title.className = 'guide-info-title';
      title.textContent = ui.guideRows.length
        ? `${ui.guideRows.length} channels with listings${ui.category ? ` in ${ui.category}` : ''}`
        : 'No listings in this window';
      const hint = document.createElement('div');
      hint.className = 'guide-info-desc';
      hint.textContent = 'Point at a show for details · click to watch · arrow keys move through the grid';
      lead.append(title, hint);
      info.appendChild(lead);
      return;
    }
    const lead = document.createElement('div');
    lead.className = 'guide-info-main';
    const kicker = document.createElement('div');
    kicker.className = 'guide-info-kicker';
    const title = document.createElement('div');
    title.className = 'guide-info-title';
    const desc = document.createElement('div');
    desc.className = 'guide-info-desc';
    if (programme) {
      const live = at >= programme.s && at < programme.e;
      if (live) {
        const pill = document.createElement('span');
        pill.className = 'now-pill';
        pill.textContent = 'LIVE';
        kicker.appendChild(pill);
      }
      const minutesLeft = Math.max(1, Math.round((programme.e - at) / 60));
      const startsIn = Math.max(1, Math.round((programme.s - at) / 60));
      const when = live
        ? `${minutesLeft} min left`
        : programme.e <= at
          ? 'ended'
          : startsIn < 60 ? `starts in ${startsIn} min` : `starts at ${formatClock(programme.s)}`;
      kicker.appendChild(document.createTextNode(
        `${formatClock(programme.s)} – ${formatClock(programme.e)} · ${when}${programme.g ? ` · ${programme.g}` : ''}`,
      ));
      title.textContent = programme.ep ? `${programme.t} — ${programme.ep}` : programme.t;
      desc.textContent = programme.d || 'No description in the guide for this listing.';
    } else {
      const current = row.programmes.find((p) => p.s <= at && p.e > at);
      kicker.textContent = current ? `On now · ${formatClock(current.s)} – ${formatClock(current.e)}` : 'Nothing listed right now';
      title.textContent = current ? current.t : row.channel.name;
      desc.textContent = 'Click the channel to watch it live.';
    }
    lead.append(kicker, title, desc);
    const channel = document.createElement('div');
    channel.className = 'guide-info-channel';
    const name = document.createElement('span');
    name.className = 'guide-info-channel-name';
    name.textContent = row.channel.chno ? `${row.channel.chno} · ${row.channel.name}` : row.channel.name;
    const group = document.createElement('span');
    group.className = 'guide-info-channel-group';
    group.textContent = row.channel.group;
    const names = document.createElement('span');
    names.className = 'guide-info-channel-text';
    names.append(name, group);
    channel.append(channelLogo(row.channel, 'guide-info-logo'), names);
    info.append(lead, channel);
  }

  function guideTarget(node) {
    const cell = node && node.closest ? node.closest('.cable-programme, .cable-row > .cable-channel') : null;
    if (!cell || cell.classList.contains('cable-header-stub')) return null;
    const row = ui.guideRows[Number(cell.dataset.row)];
    if (!row) return null;
    const programme = cell.dataset.programme != null ? row.programmes[Number(cell.dataset.programme)] : null;
    return { cell, row, programme };
  }

  function renderCableGuide() {
    if (snapshot.library.guideLoading || snapshot.library.guideError) {
      els.guideGrid.textContent = '';
      els.guideInfo.hidden = true;
      const empty = document.createElement('div');
      empty.className = 'empty-state cable-empty';
      empty.textContent = snapshot.library.guideLoading
        ? 'The guide is still loading. Channels remain available in the Channels tab.'
        : `The programme guide is unavailable: ${snapshot.library.guideError}`;
      els.guideGrid.appendChild(empty);
      els.guideSubtitle.textContent = 'The channel list remains available while the guide is unavailable.';
      return;
    }

    const previousTop = els.guideGrid.scrollTop;
    const previousLeft = els.guideGrid.scrollLeft;
    const at = nowSeconds();
    const start = Math.floor(at / GUIDE_SLOT_SECONDS) * GUIDE_SLOT_SECONDS;
    const end = start + GUIDE_WINDOW_SECONDS;
    const query = ui.query.trim().toLowerCase();
    const metrics = guideMetrics();
    const rows = guideRows(start, end, query);

    if (start !== ui.guideWindowStart) ui.guideFocusTime = 0;
    ui.guideWindowStart = start;
    ui.guideMetrics = metrics;
    ui.guideRows = rows;
    ui.guideItems = guideItemsFrom(rows);
    ui.guideRendered = 0;
    els.guideGrid.style.setProperty('--cable-label', `${metrics.label}px`);
    els.guideGrid.style.setProperty('--cable-slot', `${metrics.slot}px`);
    els.guideGrid.style.setProperty('--cable-timeline', `${metrics.timeline}px`);
    const totalWithGuide = new Set(programmeIndex.keys()).size;
    els.guideSubtitle.textContent = `${rows.length} channels with listings${ui.category ? ` in ${ui.category}` : ''} · ` +
      `${formatClock(start)} – ${formatClock(end)} · the guide covers ${totalWithGuide} of ${(snapshot.library.channels || []).length} channels`;
    els.guideGrid.textContent = '';
    els.guideGrid.appendChild(guideTimeHeader(start, at, metrics));

    if (!rows.length) {
      const empty = document.createElement('div');
      empty.className = 'empty-state cable-empty';
      empty.textContent = query || ui.category
        ? 'No channel or show in this time window matches the search or category.'
        : 'No programme listings cover this time window.';
      els.guideGrid.appendChild(empty);
    } else {
      appendCablePage();
    }
    showGuideInfo(null, null);
    els.guideGrid.scrollTop = previousTop;
    els.guideGrid.scrollLeft = previousLeft;
  }

  /** Moves the NOW line and the live highlight without rebuilding the grid. */
  function updateGuideClock() {
    if (!cableGuideEnabled() || els.guideGrid.hidden) return;
    const at = nowSeconds();
    const start = Math.floor(at / GUIDE_SLOT_SECONDS) * GUIDE_SLOT_SECONDS;
    if (start !== ui.guideWindowStart || !ui.guideMetrics) {
      renderCableGuide();
      return;
    }
    const metrics = ui.guideMetrics;
    const left = `${(at - start) * metrics.pxPerSecond}px`;
    for (const line of els.guideGrid.querySelectorAll('.cable-now-line')) line.style.left = left;
    const marker = els.guideGrid.querySelector('.guide-now-marker');
    if (marker) placeNowMarker(marker, at, start, metrics);
    for (const cell of els.guideGrid.querySelectorAll('.cable-programme')) {
      const s = Number(cell.dataset.s);
      const e = Number(cell.dataset.e);
      cell.classList.toggle('current', at >= s && at < e);
      cell.classList.toggle('past', e <= at);
    }
  }

  /** The time a cell stands for: its start, or the window start if it began earlier. */
  function cellTime(cell) {
    return Math.max(Number(cell.dataset.s), ui.guideWindowStart);
  }

  /**
   * Arrow-key movement through the grid, like a cable remote. Up and down keep
   * the remembered time column (ui.guideFocusTime) instead of the start of
   * whichever show is highlighted, so the highlight does not drift sideways
   * while scrolling past long and short shows.
   */
  function moveInGuide(cell, key) {
    const rowEl = cell.closest('.cable-row');
    if (!rowEl) return null;
    const cells = [...rowEl.querySelectorAll('.cable-channel, .cable-programme')];
    const position = cells.indexOf(cell);
    if (key === 'ArrowRight' || key === 'ArrowLeft') {
      const next = key === 'ArrowRight' ? cells[position + 1] : position > 0 ? cells[position - 1] : null;
      if (next && next.classList.contains('cable-programme')) ui.guideFocusTime = cellTime(next);
      return next || null;
    }
    const step = key === 'ArrowDown' ? 'nextElementSibling' : 'previousElementSibling';
    let next = rowEl[step];
    while (next && !(next.classList.contains('cable-row') && !next.classList.contains('cable-header-row'))) {
      next = next[step];
    }
    if (!next && key === 'ArrowDown' && appendCablePage()) {
      next = rowEl.nextElementSibling;
      while (next && !next.classList.contains('cable-row')) next = next.nextElementSibling;
    }
    if (!next) return null;
    if (cell.classList.contains('cable-channel')) return next.querySelector('.cable-channel');
    const at = ui.guideFocusTime || cellTime(cell);
    const programmes = [...next.querySelectorAll('.cable-programme')];
    return programmes.find((p) => Number(p.dataset.s) <= at && Number(p.dataset.e) > at) ||
      programmes.find((p) => Number(p.dataset.s) >= at) ||
      programmes[programmes.length - 1] ||
      next.querySelector('.cable-channel');
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
          <dt>Version</dt><dd>${escapeHtml(meta.version || 'unknown')}${meta.library_scope === 'all' ? ' · preview (global lineup, cable guide)' : ''}</dd>
          <dt>Library scope</dt><dd>${escapeHtml(meta.library_scope || 'usa')}${Array.isArray(meta.preview_features) && meta.preview_features.length ? ` · preview: ${escapeHtml(meta.preview_features.join(', '))}` : ''}</dd>
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
        <h2>App updates</h2>
        ${(function () {
          const update = updateState || appInfo.updates || {};
          const current = update.currentVersion || appInfo.version || '';
          const latest = update.latestStableVersion || '';
          const available = update.availableVersion || '';
          const ready = Boolean(update.downloadedVersion && update.downloadedVersion === available);
          const busy = Boolean(update.checking || update.downloading);
          const badge = update.error
            ? '<span class="badge bad">Check failed</span>'
            : ready
              ? '<span class="badge ok">Ready to install</span>'
              : available
                ? '<span class="badge ok">Update available</span>'
                : '<span class="badge">Up to date</span>';
          const downloadLabel = update.downloading
            ? `Downloading… ${Math.max(0, Number(update.progressPercent) || 0)}%`
            : ready
              ? 'Open installer'
              : 'Download update';
          return `
        <p>${badge} &nbsp; ${escapeHtml(update.message || 'No update check yet.')}</p>
        <div class="actions">
          <button class="btn" id="check-update" ${busy ? 'disabled' : ''}>${
            update.checking ? 'Checking…' : 'Check for updates'
          }</button>
          ${available ? `<button class="btn btn-primary" id="download-update" ${busy ? 'disabled' : ''}>${
            escapeHtml(downloadLabel)
          }</button>` : ''}
          ${update.releaseUrl ? '<button class="btn" id="release-page">Release notes</button>' : ''}
        </div>
        <dl class="meta">
          <dt>Installed</dt><dd>${escapeHtml(current)}</dd>
          <dt>Newest stable</dt><dd>${escapeHtml(latest || 'not checked yet')}</dd>
          <dt>Last check</dt><dd>${formatStamp(update.lastCheckedAtMillis)}</dd>
          <dt>Installer</dt><dd>${escapeHtml(
            update.installerSize ? formatMegabytes(update.installerSize) : 'not downloaded',
          )}${ready && update.installerPath ? ` · ${escapeHtml(update.installerPath)}` : ''}</dd>
        </dl>
        <p class="muted">Only a published stable release above ${escapeHtml(current)} is offered.
          The daily check sends GitHub the previous ETag, so an unchanged release costs one tiny
          response. An installer downloads only when you press the button, is checked against the
          release's SHA-256 file, and is reused rather than downloaded again.</p>`;
        })()}
      </div>

      <div class="panel">
        <h2>Automatic checks</h2>
        <p>Checks follow this repository's publishing jobs in <b>${escapeHtml(
          appInfo.repositoryTimeZone || 'America/New_York',
        )}</b>, ${escapeHtml(String(appInfo.publishingGraceMinutes || 45))} minutes after each slot so the
        publishing job has finished writing. A check sends the last ETag and Last-Modified value, so an
        unchanged playlist and guide cost two small <code>304 Not Modified</code> responses instead of a
        full guide download (about 15 MB for the USA lineup, about 38 MB for the global preview).</p>
        <p class="muted">Check times: ${escapeHtml((appInfo.checkTimes || []).join(', '))}</p>
      </div>

      <div class="panel">
        <h2>Known limitations</h2>
        <div class="note">
          <p><b>Refreshes download from the public repository.</b> The playlist and the guide come from
          <code>raw.githubusercontent.com</code> with no account or credential. If a download fails, the copy
          already on this Mac stays in use and the result above says why.</p>
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

    renderActivity();
    document.getElementById('force-refresh').addEventListener('click', () => runRefresh(true, 'force-refresh'));
    document.getElementById('check-now').addEventListener('click', () => runRefresh(false, 'check-now'));
    document.getElementById('reset-bundled').addEventListener('click', resetToBundled);

    const checkUpdate = document.getElementById('check-update');
    if (checkUpdate) {
      checkUpdate.addEventListener('click', async () => {
        checkUpdate.disabled = true;
        await api.checkForUpdate(true);
        updateState = await api.updateStatus();
        renderSettings();
      });
    }
    const downloadUpdate = document.getElementById('download-update');
    if (downloadUpdate) {
      downloadUpdate.addEventListener('click', async () => {
        downloadUpdate.disabled = true;
        const current = updateState || appInfo.updates || {};
        if (current.downloadedVersion &&
            current.downloadedVersion === current.availableVersion) {
          await api.installUpdate();
        } else {
          await api.downloadUpdate();
        }
        updateState = await api.updateStatus();
        renderSettings();
      });
    }
    const releasePage = document.getElementById('release-page');
    if (releasePage) releasePage.addEventListener('click', () => api.openReleasePage());
  }

  let appInfo = {};
  // The main process owns the update state; Settings renders the last value
  // pushed on ptv:update and asks for a fresh one after each action.
  let updateState = null;

  // -------------------------------------------------------------- actions

  function selectTab(tab) {
    // 1.1.0 had a separate "Cable" tab; the grid is the Guide tab now.
    if (tab === 'cable') tab = 'guide';
    if (!els.views[tab]) tab = 'channels';
    ui.tab = tab;
    for (const [name, view] of Object.entries(els.views)) view.hidden = name !== tab;
    for (const button of els.tabs.querySelectorAll('.tab')) {
      button.setAttribute('aria-selected', String(button.dataset.tab === tab));
    }
    // The category list filters the grid too, like a cable box's guide filter.
    const categories = tab === 'channels' || (tab === 'guide' && cableGuideEnabled());
    els.categories.style.display = categories ? '' : 'none';
    els.search.placeholder = tab === 'guide'
      ? (cableGuideEnabled() ? 'Search channel or show' : 'Search the guide')
      : tab === 'live'
        ? 'Search live games'
        : 'Search channels';
    render();
  }

  function selectCategory(name) {
    ui.category = name;
    renderCategories();
    if (ui.tab === 'guide') {
      els.guideGrid.scrollTop = 0;
      renderGuide();
    } else {
      renderChannels();
    }
    document.getElementById('content').scrollTop = 0;
  }

  function render() {
    if (ui.tab === 'channels') renderChannels();
    else if (ui.tab === 'live') renderLive();
    else if (ui.tab === 'guide') renderGuide();
    else renderSettings();
  }

  const loadingTips = [
    'TIP · You can browse and watch channels while the guide loads.',
    'TIP · Settings → Force refresh downloads both the channel list and guide.',
    'FACT · XMLTV is the programme-listing format used by PremiumTV.',
    'TIP · Back from a show returns to your previous tab and guide position.',
    'FACT · The bundled library works even when a refresh cannot reach the network.',
    'TIP · A stream may be offline or region-restricted even after a successful check.',
  ];
  let activityStartedAt = Date.now();
  let activityWasBusy = false;
  let activityResultUntil = 0;
  let refreshPending = false;

  function renderActivity() {
    const info = snapshot.info || {};
    const busy = refreshPending || info.inProgress || snapshot.state.phase === 'loading' || snapshot.library.guideLoading;
    const panel = document.getElementById('library-activity');
    if (busy && !activityWasBusy) activityStartedAt = info.inProgress ? info.lastAttemptAt : Date.now();
    if (!busy && activityWasBusy) activityResultUntil = Date.now() + 15000;
    activityWasBusy = Boolean(busy);
    panel.hidden = !busy && Date.now() > activityResultUntil;
    panel.setAttribute('aria-busy', busy ? 'true' : 'false');
    panel.dataset.outcome = !busy && info.lastOutcomeOk === false ? 'error' : 'ok';
    document.getElementById('activity-spinner').hidden = !busy;
    const elapsed = Math.max(0, Math.floor((Date.now() - activityStartedAt) / 1000));
    document.getElementById('activity-elapsed').textContent = busy ? `${elapsed}s` : '';
    document.getElementById('activity-message').textContent = busy
      ? (refreshPending && !info.inProgress ? 'Starting refresh…' : snapshot.state.message || 'Loading programme guide…')
      : info.lastMessage || snapshot.state.message || 'Library ready.';
    const tip = document.getElementById('activity-tip');
    tip.hidden = !busy;
    tip.textContent = loadingTips[Math.floor(elapsed / 8) % loadingTips.length];
    for (const id of ['force-refresh', 'check-now', 'reset-bundled']) {
      const button = document.getElementById(id);
      if (button) button.disabled = Boolean(busy);
    }
  }

  async function runRefresh(force, buttonId) {
    if (refreshPending || snapshot.info.inProgress) return;
    refreshPending = true;
    renderActivity();
    const button = buttonId ? document.getElementById(buttonId) : null;
    if (button) {
      button.disabled = true;
      button.textContent = force ? 'Refreshing…' : 'Checking…';
    }
    els.statusText.textContent = force ? 'Downloading the playlist and the guide…' : 'Checking the repository…';
    try {
      await api.refresh(force);
      snapshot = await api.getSnapshot();
      rebuildDerivedIndexes(snapshot.library);
    } catch (error) {
      snapshot.info = { ...snapshot.info, lastOutcomeOk: false, lastMessage: `Refresh failed: ${error.message}. Your current library is still available.` };
    } finally {
      refreshPending = false;
      if (button) {
        button.disabled = false;
        button.textContent = force ? 'Force refresh all now' : 'Check for changes';
      }
      render();
      renderActivity();
    }
  }

  async function resetToBundled() {
    els.statusText.textContent = 'Resetting to the bundled copy…';
    snapshot = await api.resetToBundled();
    rebuildDerivedIndexes(snapshot.library);
    renderCategories();
    render();
  }

  /** The server badge over the video: which feed of this channel is playing. */
  function renderServerBadge() {
    const multi = playQueue.length > 1;
    if (els.playerPrevServer) els.playerPrevServer.disabled = !multi;
    if (els.playerNextServer) els.playerNextServer.disabled = !multi;
    renderFavoriteButton();
    if (!els.playerServer) return;
    if (multi) {
      els.playerServer.textContent =
        `Server ${playQueueIndex + 1} of ${playQueue.length} · use ◀ Server / Server ▶ to switch · automatic fallback on`;
      els.playerServer.hidden = false;
    } else {
      els.playerServer.hidden = true;
    }
  }

  function describeChannel(channel) {
    els.playerName.textContent = channel.name;
    const at = nowSeconds();
    const { current, next } = nowPlayingFrom(listingsFor(channel), at);
    els.playerNow.textContent = current ? `Now · ${current.t}` : '';
    els.playerNext.textContent = next ? `Next · ${next.t} at ${formatClock(next.s)}` : '';
    els.playerDetail.textContent = current && current.d ? current.d : channel.group;
    renderServerBadge();
  }

  /**
   * Opens a channel with its server list: the game's other streams or the
   * channel's backup feeds. When a feed fails every strategy, the next server
   * takes over by itself and the badge above the video says so; the error
   * card appears only when every server has been tried.
   */
  /** Opening a channel files it under Recently watched (newest first). */
  function noteWatched(channel) {
    recentKeys = personal.recordRecent(recentKeys, personal.keyFor(channel));
    personal.save(window.localStorage, personal.RECENTS_KEY, recentKeys);
    if (ui.tab === 'channels') renderCategories();
  }

  function currentChannel() {
    return playQueue[playQueueIndex] || null;
  }

  function renderFavoriteButton() {
    if (!els.playerFavorite) return;
    const favorite = personal.isFavorite(favoriteKeys, personal.keyFor(currentChannel()));
    els.playerFavorite.textContent = favorite ? '★ Favorited' : '☆ Favorite';
    els.playerFavorite.setAttribute('aria-pressed', String(favorite));
  }

  function toggleFavorite() {
    const channel = currentChannel();
    if (!channel) return;
    favoriteKeys = personal.toggleFavorite(favoriteKeys, personal.keyFor(channel));
    personal.save(window.localStorage, personal.FAVORITES_KEY, favoriteKeys);
    renderFavoriteButton();
    renderCategories();
    els.statusText.textContent = personal.isFavorite(favoriteKeys, personal.keyFor(channel))
      ? `${channel.name} added to Favorites`
      : `${channel.name} removed from Favorites`;
  }

  /** Manual server switch (Live Events fix): wraps around the server list. */
  async function switchServer(delta) {
    if (playQueue.length < 2) return;
    playQueueIndex = personal.nextServerIndex(playQueueIndex, playQueue.length, delta);
    els.statusText.textContent = `Switching to server ${playQueueIndex + 1} of ${playQueue.length}…`;
    await playCurrentServer();
  }

  async function openPlayer(channel, servers) {
    noteWatched(channel);
    const list = Array.isArray(servers) && servers.length
      ? servers
      : window.PremiumLive.serversFor(channel, snapshot.library.channels || []);
    playQueue = list;
    playQueueIndex = Math.max(0, list.findIndex((item) => item.url === channel.url));
    els.player.hidden = false;
    describeChannel(playQueue[playQueueIndex] || channel);
    await playCurrentServer(channel.name);
  }

  async function playCurrentServer(displayName) {
    const channel = playQueue[playQueueIndex];
    if (!channel) return;
    describeChannel(channel);
    if (displayName && channel.name !== displayName) {
      els.playerName.textContent = displayName;
    }
    const resolved = await api.resolveStream(channel.id, channel.url);
    if (!resolved.ok) {
      await advanceServer(resolved.message);
      return;
    }
    if (playingSession) await api.releaseStream(playingSession).catch(() => {});
    playingSession = resolved.sessionId;
    els.statusText.textContent = `Playing ${displayName || channel.name}`;
    // The proxy URL is /p/<session>, without a file extension. Pass the
    // original stream URL as a format hint so HLS/MPEG-TS gets the right
    // player first instead of trying native playback of every feed.
    window.PremiumPlayer.play(resolved.url, channel.url, { onFatal: () => advanceServer() });
  }

  /** Switch to the next server for the open channel, or give up honestly. */
  async function advanceServer(reason) {
    if (playQueueIndex < playQueue.length - 1) {
      playQueueIndex += 1;
      els.statusText.textContent =
        `This feed stopped responding - switching to server ${playQueueIndex + 1} of ${playQueue.length}…`;
      await playCurrentServer();
      return;
    }
    const tried = playQueue.length > 1
      ? `All ${playQueue.length} servers for this channel were tried.`
      : '';
    window.PremiumPlayer.fail(
      `${tried}${reason ? ` ${reason}` : ' The feed is offline or refuses this connection;'}` +
      ' the nightly link check removes links like this.',
    );
  }

  async function closePlayer() {
    window.PremiumPlayer.stop();
    els.player.hidden = true;
    playQueue = [];
    playQueueIndex = 0;
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

  // Click-to-search: the field ships readonly, so hover (and keyboard focus
  // passing over it) can never start a search. A click — or '/' anywhere, or
  // Enter on the focused field — activates it; blur/Escape deactivates it.
  // There is deliberately no mouseover/pointerenter handler on the search box.
  let searchRenderTimer = null;
  function activateSearch() {
    if (ui.searchActive) return;
    ui.searchActive = true;
    els.search.readOnly = false;
    els.search.setAttribute('aria-readonly', 'false');
    els.search.classList.add('search-active');
    els.search.focus();
    els.search.select();
  }
  function deactivateSearch() {
    ui.searchActive = false;
    els.search.readOnly = true;
    els.search.setAttribute('aria-readonly', 'true');
    els.search.classList.remove('search-active');
  }
  els.search.addEventListener('click', activateSearch);
  els.search.addEventListener('keydown', (event) => {
    if (!ui.searchActive && (event.key === 'Enter' || event.key === ' ')) {
      event.preventDefault();
      activateSearch();
    } else if (event.key === 'Escape' || event.key === 'Enter') {
      deactivateSearch();
      els.search.blur();
    }
  });
  els.search.addEventListener('blur', deactivateSearch);
  els.search.addEventListener('input', () => {
    if (!ui.searchActive) return; // never search without an explicit click
    window.clearTimeout(searchRenderTimer);
    searchRenderTimer = window.setTimeout(() => {
      ui.query = els.search.value;
      if (ui.tab === 'settings') selectTab('channels');
      else render();
    }, 150);
  });

  els.playerClose.addEventListener('click', closePlayer);
  if (els.playerPrevServer) els.playerPrevServer.addEventListener('click', () => switchServer(-1));
  if (els.playerNextServer) els.playerNextServer.addEventListener('click', () => switchServer(1));
  if (els.playerFavorite) els.playerFavorite.addEventListener('click', toggleFavorite);
  els.playerRetry.addEventListener('click', () => window.PremiumPlayer.retry());

  // Scroll paging is coalesced through requestAnimationFrame: a scroll burst
  // used to run visibleChannels() (a full filter over every channel) per event.
  let channelPageQueued = false;
  document.getElementById('content').addEventListener('scroll', (event) => {
    if (ui.tab !== 'channels' || channelPageQueued) return;
    const node = event.target;
    if (node.scrollTop + node.clientHeight < node.scrollHeight - 600) return;
    channelPageQueued = true;
    window.requestAnimationFrame(() => {
      channelPageQueued = false;
      if (ui.rendered < visibleChannels().length) appendChannelPage();
    });
  }, { passive: true });

  els.guideGrid.addEventListener('scroll', () => {
    if (ui.tab !== 'guide') return;
    if (els.guideGrid.scrollTop + els.guideGrid.clientHeight >= els.guideGrid.scrollHeight - 480) {
      appendCablePage();
    }
  });

  // The detail strip follows the pointer and the keyboard focus.
  let infoTarget = null;
  function followGuideTarget(event) {
    const target = guideTarget(event.target);
    if (!target || target.cell === infoTarget) return;
    infoTarget = target.cell;
    showGuideInfo(target.row, target.programme);
  }
  els.guideGrid.addEventListener('mouseover', followGuideTarget);
  els.guideGrid.addEventListener('focusin', followGuideTarget);
  // A click or tab into a show sets the time column the arrow keys keep.
  els.guideGrid.addEventListener('mousedown', (event) => {
    const cell = event.target.closest('.cable-programme');
    if (cell) ui.guideFocusTime = cellTime(cell);
  });

  els.guideGrid.addEventListener('keydown', (event) => {
    if (!['ArrowRight', 'ArrowLeft', 'ArrowUp', 'ArrowDown'].includes(event.key)) return;
    const cell = event.target.closest('.cable-programme, .cable-row > .cable-channel');
    if (!cell || cell.classList.contains('cable-header-stub')) return;
    event.preventDefault();
    const next = moveInGuide(cell, event.key);
    if (!next) return;
    next.focus({ preventScroll: true });
    if (typeof next.scrollIntoView === 'function') next.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  });

  let resizeTimer = null;
  window.addEventListener('resize', () => {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(() => {
      if (ui.tab === 'guide' && cableGuideEnabled()) renderCableGuide();
    }, 150);
  });

  // ------------------------------------------------------------ update popup

  /**
   * Show the popup that sends this build to GitHub for the newest release.
   *
   * The main process decides *whether* there is a notice (from the published
   * `app-update-notice.json`, by platform and version range); this only renders
   * it. Every field goes in through textContent, so a remote wording change can
   * never inject markup into the window.
   *
   * It is dismissible on purpose - an app that refuses to run turns "please
   * update" into "your Mac is broken" - but the dismissal lasts one launch, so
   * the notice is back the next time PremiumTV opens.
   */
  function renderUpdateNotice() {
    if (!els.updateNotice) return;
    const state = updateState || (appInfo && appInfo.updates) || {};
    const notice = state.notice;
    if (!notice || state.noticeDismissedForLaunch) {
      els.updateNotice.hidden = true;
      return;
    }
    const ended = notice.level === 'end_of_support';
    els.updateNotice.classList.toggle('ended', ended);
    els.updateNoticeEyebrow.textContent = ended ? 'SUPPORT HAS ENDED' : 'PREMIUMTV UPDATE';
    els.updateNoticeTitle.textContent = notice.title || 'A newer PremiumTV is available';
    els.updateNoticeMessage.textContent = notice.message || '';
    els.updateNoticeSurpriseWrap.hidden = !notice.surprise;
    els.updateNoticeSurprise.textContent = notice.surprise || '';

    const current = state.currentVersion || (appInfo && appInfo.version) || '';
    const newest = state.latestStableVersion || state.availableVersion || '';
    els.updateNoticeVersions.textContent = newest
      ? `Installed ${current} · newest on GitHub ${newest}`
      : `Installed ${current}`;
    els.updateNoticeUrl.textContent = notice.releasesUrl || '';
    els.updateNoticeAction.textContent = notice.actionLabel || 'Update now';
    els.updateNoticeDismiss.textContent = notice.dismissLabel || 'Remind me next time';
    els.updateNoticeFoot.textContent = ended
      ? 'This build no longer receives channel or guide updates from GitHub. ' +
        'Esc dismisses this message for now; it returns every launch.'
      : 'Esc dismisses this message for now; it returns every launch until ' +
        'PremiumTV is updated.';
    els.updateNotice.hidden = false;
    els.updateNoticeAction.focus();
  }

  /** Ask the main process to hide the notice for this launch. */
  async function dismissUpdateNotice() {
    if (typeof api.dismissUpdateNotice === 'function') {
      const next = await api.dismissUpdateNotice();
      if (next) updateState = next;
      else if (updateState) updateState = { ...updateState, noticeDismissedForLaunch: true };
    } else if (updateState) {
      updateState = { ...updateState, noticeDismissedForLaunch: true };
    }
    renderUpdateNotice();
  }

  if (els.updateNotice) {
    els.updateNoticeDismiss.addEventListener('click', () => {
      dismissUpdateNotice().catch(() => {});
    });
    els.updateNoticeAction.addEventListener('click', async () => {
      await dismissUpdateNotice();
      // Open the update centre and re-check GitHub. The installer still
      // downloads only on the Settings button: no background downloads.
      selectTab('settings');
      els.updateNoticeAction.disabled = true;
      try {
        await api.checkForUpdate(true);
        updateState = await api.updateStatus();
        renderSettings();
      } catch (error) {
        els.statusText.textContent = `Could not check for updates: ${error.message}`;
      } finally {
        els.updateNoticeAction.disabled = false;
      }
    });
  }

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && els.updateNotice && !els.updateNotice.hidden) {
      dismissUpdateNotice().catch(() => {});
      return;
    }
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
      activateSearch();
    }
  });

  // State notifications do not contain the library. Re-read it over IPC on
  // each transition, including the early channel-only progress notification.
  // Ignore older replies: a slow startup request must not erase a ready one.
  let snapshotRequest = 0;
  async function syncSnapshot() {
    const request = ++snapshotRequest;
    const next = await api.getSnapshot();
    if (request !== snapshotRequest) return;
    snapshot = next;
    rebuildDerivedIndexes(snapshot.library);
    els.statusText.textContent = snapshot.state.message || '';
    renderCategories();
    render();
    renderActivity();
    if (snapshot.state.phase === 'error') {
      els.channelsGrid.innerHTML = `<div class="empty-state">${escapeHtml(snapshot.state.message)}</div>`;
    }
  }

  function updateSnapshot() {
    syncSnapshot().catch((error) => {
      els.statusText.textContent = `Could not load channels: ${error.message}`;
    });
  }

  api.onState(updateSnapshot);

  api.onInfo((info) => {
    snapshot.info = info;
    els.statusText.textContent = info.lastMessage || snapshot.state.message || '';
    if (ui.tab === 'settings') renderSettings();
    renderActivity();
  });

  api.onProgress(() => {
    updateSnapshot();
  });

  api.onSelectTab((tab) => selectTab(tab));

  if (typeof api.onUpdate === 'function') {
    api.onUpdate((state) => {
      updateState = state;
      if (ui.tab === 'settings') renderSettings();
      // A notice can arrive (or escalate to end-of-support) while the app runs.
      renderUpdateNotice();
    });
  }

  window.addEventListener('beforeunload', () => {
    window.PremiumPlayer.stop();
    window.clearInterval(activityTimer);
  });

  const activityTimer = window.setInterval(renderActivity, 1000);

  /** Fade the launch splash out; the app underneath is already painted. */
  function hideSplash() {
    if (!els.splash || els.splash.classList.contains('done')) return;
    els.splash.classList.add('done');
    els.splash.setAttribute('aria-hidden', 'true');
  }

  async function boot() {
    appInfo = await api.getAppInfo();
    updateState = appInfo.updates || null;
    renderUpdateNotice();
    const brandTag = document.getElementById('brand-tag');
    if (brandTag && appInfo.version) brandTag.textContent = appInfo.version + (appInfo.version.startsWith('1.1.1') ? ' · Encore Preview' : '');
    // The splash names the build the viewer is waiting on, the same way the
    // sidebar plaque and Settings do.
    if (els.splashVersion && appInfo.version) {
      els.splashVersion.textContent =
        `Version ${appInfo.version}${appInfo.version.startsWith('1.1.1') ? ' · Encore Preview' : ''}`;
    }
    await syncSnapshot();
    hideSplash();

    // Keep "now playing" honest without a full re-render storm.
    clockTimer = window.setInterval(() => {
      if (ui.tab === 'guide') {
        // The grid keeps its scroll position and keyboard focus: only the NOW
        // line and the live highlight move, until the next half hour rebuilds it.
        if (cableGuideEnabled()) updateGuideClock();
        else renderGuide();
      } else if (ui.tab === 'live') renderLive();
      // Channels intentionally not re-rendered here: rebuilding the grid every
      // 30 s was a visible stutter while clicking around; "on now" text
      // refreshes on the next navigation/search instead.
    }, 30000);
  }

  boot().catch((error) => {
    hideSplash();
    els.statusText.textContent = `Startup failed: ${error.message}`;
    snapshot.state = { phase: 'error', message: `Startup failed: ${error.message}. Quit and reopen PremiumTV to retry.` };
    renderActivity();
  });
})();
