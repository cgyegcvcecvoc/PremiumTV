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
    catSort: document.getElementById('cat-sort'),
    categoryPageTools: document.getElementById('category-page-tools'),
    catBack: document.getElementById('cat-back'),
    channelSort: document.getElementById('channel-sort'),
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
    liveRefresh: document.getElementById('live-refresh'),
    settingsBody: document.getElementById('settings-body'),
    statusText: document.getElementById('status-text'),
    views: {
      channels: document.getElementById('view-channels'),
      live: document.getElementById('view-live'),
      movies: document.getElementById('view-movies'),
      guide: document.getElementById('view-guide'),
      settings: document.getElementById('view-settings'),
    },
    moviesGrid: document.getElementById('movies-grid'),
    moviesEmpty: document.getElementById('movies-empty'),
    moviesSubtitle: document.getElementById('movies-subtitle'),
    moviesFilters: document.getElementById('movies-filters'),
    moviesSearch: document.getElementById('movies-search'),
    moviesGenres: document.getElementById('movies-genres'),
    splash: document.getElementById('splash'),
    splashBar: document.getElementById('splash-bar'),
    splashBarFill: document.getElementById('splash-bar-fill'),
    splashStatus: document.getElementById('splash-status'),
    splashVersion: document.getElementById('splash-version'),
    player: document.getElementById('player'),
    video: document.getElementById('video'),
    playerName: document.getElementById('player-name'),
    playerNow: document.getElementById('player-now'),
    playerNext: document.getElementById('player-next'),
    playerDetail: document.getElementById('player-detail'),
    playerServer: document.getElementById('player-server'),
    playerAudioBadge: document.getElementById('player-audio-badge'),
    playerControls: document.getElementById('player-controls'),
    playerToggle: document.getElementById('player-toggle'),
    playerBack10: document.getElementById('player-back-10'),
    playerFwd10: document.getElementById('player-fwd-10'),
    playerSeek: document.getElementById('player-seek'),
    playerTime: document.getElementById('player-time'),
    playerLivePill: document.getElementById('player-live-pill'),
    playerAudioTrack: document.getElementById('player-audio-track'),
    playerMute: document.getElementById('player-mute'),
    playerVolume: document.getElementById('player-volume'),
    playerClose: document.getElementById('player-close'),
    playerMinimize: document.getElementById('player-minimize'),
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
    // 1.0.8 sorting: the sidebar's category list and the channel page's grid
    // each get an order the viewer picks (published / A-Z / Z-A / biggest).
    categorySort: 'published',
    channelSort: 'default',
    // 1.0.8 Live Events: per-game feed check results, keyed by game key —
    // 'checking' | 'live' | 'silent'.
    liveStatus: new Map(),
    // 1.1.1 Live Events: curated team crests and scheduled kickoffs, both
    // bundled with the app data and shipped through the library snapshot's
    // meta ("team-logos" and "live-schedule").
    teamLogos: {},
    schedule: {},
    // 1.1.2 Movies & Shows: the on-demand test catalogue shipped in the
    // bundle (meta.vod_catalog) and the filter the viewer picked.
    vodItems: [],
    vodFilter: 'all',
    vodGenre: 'all',
    vodQuery: '',
    sportsDoc: null,
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

  // ------------------------------------------------------- 1.0.8 sorting

  /** The sidebar's category list in the viewer's chosen order. */
  function sortedGroups() {
    const groups = [...(snapshot.library.groups || [])];
    const byName = (a, b) => channelCollator.compare(a.name, b.name);
    if (ui.categorySort === 'az') return groups.sort(byName);
    if (ui.categorySort === 'za') return groups.sort((a, b) => byName(b, a));
    if (ui.categorySort === 'big') {
      return groups.sort((a, b) => b.count - a.count || byName(a, b));
    }
    return groups; // 'published': the order the repository publishes
  }

  /** The channel page's grid in the viewer's chosen order. */
  function sortedChannels(channels) {
    const list = [...channels];
    const byName = (a, b) => channelCollator.compare(a.name, b.name);
    const byNumber = (a, b) => {
      const left = parseInt(a.chno, 10);
      const right = parseInt(b.chno, 10);
      return (Number.isNaN(left) ? Number.MAX_SAFE_INTEGER : left) -
        (Number.isNaN(right) ? Number.MAX_SAFE_INTEGER : right) || byName(a, b);
    };
    if (ui.channelSort === 'az') return list.sort(byName);
    if (ui.channelSort === 'za') return list.sort((a, b) => byName(b, a));
    if (ui.channelSort === 'number') return list.sort(byNumber);
    return list; // 'default': playlist order
  }

  /** Keeps the sidebar sort chips' gold state honest. */
  function updateCategorySortControls() {
    if (!els.catSort) return;
    for (const button of els.catSort.querySelectorAll('.cat-sort-btn')) {
      button.setAttribute('aria-pressed', String(button.dataset.sort === ui.categorySort));
    }
  }

  /** Keeps the channel page's sort chips and back button honest. */
  function updateChannelSortControls() {
    if (!els.channelSort) return;
    for (const button of els.channelSort.querySelectorAll('.cat-sort-btn')) {
      button.setAttribute('aria-pressed', String(button.dataset.chsort === ui.channelSort));
    }
    const onCategoryPage = Boolean(ui.category);
    if (els.categoryPageTools) els.categoryPageTools.hidden = !onCategoryPage;
  }

  let programmeIndex = new Map();
  // The scrapers' live-game feeds, grouped by sport (Live Events tab) and
  // indexed by URL (LIVE labels, server fallback).
  let liveSections = [];
  let liveIndex = new Map();
  // Multi-server playback: the ordered server list of the open player.
  let playQueue = [];
  let playQueueIndex = 0;
  // The 1.0.8 side player: true while the picture is tucked into the corner
  // and the browser is up. The stream itself keeps playing either way.
  let playerMini = false;
  // Recently watched + Favorites, persisted per machine (personal.js logic).
  const personal = window.PremiumPersonal;
  let recentKeys = personal.load(window.localStorage, personal.RECENTS_KEY);
  let favoriteKeys = personal.load(window.localStorage, personal.FAVORITES_KEY);
  // 1.1.0 dead-feed memory: a channel whose every server failed is hidden
  // from the browser for seven days (health.js), with a Settings restore.
  const health = window.PremiumHealth;
  let deadFeeds = health ? health.load(window.localStorage) : new Set();
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
    liveSections = window.PremiumLive.buildSections(channels, ui.schedule || {});
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

  /** Every published channel the browser is allowed to show right now. */
  function liveChannels() {
    const channels = snapshot.library.channels || [];
    return health ? health.filterChannels(channels, deadFeeds) : channels;
  }

  function renderCategories() {
    const groups = sortedGroups();
    const total = liveChannels().length;
    els.categories.textContent = '';
    updateCategorySortControls();

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
    const all = liveChannels();
    if (ui.category === RECENT_CATEGORY) return personal.resolve(recentKeys, all);
    if (ui.category === FAVORITE_CATEGORY) return personal.resolve(favoriteKeys, all);
    const channels = all;
    const query = ui.query.trim().toLowerCase();
    const filtered = channels.filter((channel) => {
      if (ui.category && channel.group !== ui.category) return false;
      if (!query) return true;
      return (
        channel.name.toLowerCase().includes(query) ||
        channel.group.toLowerCase().includes(query) ||
        (channel.country || '').toLowerCase().includes(query)
      );
    });
    return sortedChannels(filtered);
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
    updateChannelSortControls();
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

  /**
   * A team's drawn badge: the team's two colours and its initials, from the
   * name alone — the same badge on every launch, nothing to load in.
   */
  function teamBadge(name) {
    const span = document.createElement('span');
    span.className = 'team-crest';
    const [start, end] = window.PremiumLive.crestColorsFor(name);
    span.style.background = `linear-gradient(135deg, ${start}, ${end})`;
    span.textContent = window.PremiumLive.initialsFor(name);
    // Official crest when the repository has one for this team; the drawn
    // badge shows while it loads and forever when it does not.
    const logo = window.PremiumLive.teamLogoUrl(ui.sportsDoc, name);
    if (logo) {
      const img = document.createElement('img');
      img.className = 'team-crest-img';
      img.alt = '';
      img.addEventListener('error', () => img.remove(), { once: true });
      api.logoUrl(logo).then((resolved) => {
        if (img.isConnected) img.src = resolved;
      }).catch(() => img.remove());
      span.append(img);
    }
    return span;
  }

  /** The live-or-not pill: red while a feed answers, grey once none does. */
  function livePill(status) {
    const pill = document.createElement('span');
    pill.className = `now-pill${status === 'silent' ? ' silent' : status === 'checking' ? ' checking' : status === 'notlive' ? ' upcoming' : ''}`;
    pill.textContent = status === 'silent' ? 'NO SIGNAL'
      : status === 'checking' ? 'CHECKING'
      : status === 'notlive' ? 'Not live yet'
      : 'LIVE';
    return pill;
  }

  function eventCard(event) {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'event-card';
    const servers = event.servers.length > 1
      ? `${event.servers.length} streams · switchable in the player`
      : '1 stream';
    card.innerHTML = '<div class="event-head"></div>' +
      '<span class="event-teams"></span>' +
      `<span class="event-sport">${window.PremiumIcons.svgForGroup(event.sport, 'ph-icon event-icon')}</span>` +
      '<span class="event-servers"></span>';
    const status = window.PremiumLive.eventStatus(
      ui.liveStatus.get(event.key), event.kickoffMs, Date.now(),
    );
    card.querySelector('.event-head').append(livePill(status));
    card.querySelector('.event-sport').insertAdjacentText('beforeend', event.sport);
    if (status === 'notlive') {
      const kickoff = document.createElement('span');
      kickoff.className = 'event-kickoff';
      kickoff.dataset.kickoff = String(event.kickoffMs);
      kickoff.textContent = `Starts in ${window.PremiumLive.countdownText(
        Math.max(0, ((event.kickoffMs || 0) - Date.now()) / 1000),
      )} · ${window.PremiumLive.kickoffLabel(event.kickoffMs)}`;
      card.querySelector('.event-head').append(kickoff);
    }

    // The matchup as two badge-and-name rows, the way a score bug reads.
    const teams = window.PremiumLive.teamsOf(event.title);
    const teamsHost = card.querySelector('.event-teams');
    if (teams) {
      for (const team of teams) {
        const row = document.createElement('span');
        row.className = 'event-team';
        row.append(teamBadge(team));
        const name = document.createElement('span');
        name.className = 'event-team-name';
        name.textContent = team;
        row.append(name);
        teamsHost.append(row);
      }
    } else {
      // Not a two-team matchup (a fight card, for instance): the full title.
      const title = document.createElement('span');
      title.className = 'event-title';
      title.textContent = event.title;
      teamsHost.append(title);
    }
    card.querySelector('.event-servers').textContent = servers;
    card.addEventListener('click', () => openPlayer(event.servers[0], event.servers));
    return card;
  }

  /** One game finished its check: repaint soon, not once per answer. */
  let liveRenderQueued = false;
  function scheduleLiveRender() {
    if (liveRenderQueued) return;
    liveRenderQueued = true;
    window.requestAnimationFrame(() => {
      liveRenderQueued = false;
      if (ui.tab === 'live') renderLive();
    });
  }

  /**
   * Asks every game's feeds whether anything still answers, six at a time.
   * Opening the tab checks the games it has no answer for; the tab's refresh
   * button re-checks all of them and pulls the newest playlist.
   */
  let liveProbeToken = 0;
  async function probeLiveGames(force = false) {
    const events = liveSections.flatMap((section) => section.events);
    if (!events.length || typeof api.probeStream !== 'function') return;
    const token = ++liveProbeToken;
    let pending = 0;
    for (const event of events) {
      if (force || !ui.liveStatus.has(event.key) || ui.liveStatus.get(event.key) === 'checking') {
        ui.liveStatus.set(event.key, 'checking');
        pending += 1;
      }
    }
    if (!pending) return;
    els.liveSubtitle.setAttribute('data-probing', 'true');
    scheduleLiveRender();

    const queue = events.filter((event) => ui.liveStatus.get(event.key) === 'checking');
    async function worker() {
      while (queue.length && token === liveProbeToken) {
        const event = queue.shift();
        let live = false;
        for (const server of event.servers) {
          if (await api.probeStream(server.url)) {
            live = true;
            break;
          }
        }
        if (token !== liveProbeToken) return;
        ui.liveStatus.set(event.key, live ? 'live' : 'silent');
        scheduleLiveRender();
      }
    }
    await Promise.all(Array.from({ length: Math.min(6, queue.length) }, worker));
    if (token === liveProbeToken) els.liveSubtitle.removeAttribute('data-probing');
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
    const statuses = [...ui.liveStatus.values()];
    const answering = statuses.filter((status) => status === 'live').length;
    const decided = statuses.filter((status) => status !== 'checking').length;
    const probing = els.liveSubtitle.getAttribute('data-probing') === 'true';
    if (games) {
      els.liveSubtitle.textContent = probing
        ? `Checking which games are still on air… (${games} games, ${feeds} streams)`
        : decided > 0
          ? `${games} games across ${feeds} streams · ${answering} of ${decided} checked are live · Refresh live games re-checks every feed`
          : `${games} games across ${feeds} streams · grouped by sport · a game with more than one stream can be switched in the player and falls back by itself`;
    } else {
      els.liveSubtitle.textContent =
        'Games the repository\u2019s scrapers have on air right now, grouped by sport.';
    }

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
    const update = updateState || appInfo.updates || {};
    const source = snapshot.state.source;
    const current = update.currentVersion || appInfo.version || '';
    const latest = update.latestStableVersion || '';
    const available = update.availableVersion || '';
    const ready = Boolean(update.downloadedVersion && update.downloadedVersion === available);
    const updateBusy = Boolean(update.checking || update.downloading);
    const refreshing = refreshPending || info.inProgress || snapshot.state.phase === 'loading' ||
      snapshot.library.guideLoading;
    const guideCount = meta.guide_channels || new Set(programmeIndex.keys()).size;
    const status = diagnoseStatusLine(info, update, refreshing);

    const sourceBadge =
      source === 'cache'
        ? '<span class="badge ok">Downloaded copy</span>'
        : source === 'bundled'
          ? '<span class="badge">Bundled in the app</span>'
          : '<span class="badge bad">Unavailable</span>';

    const downloadLabel = update.downloading
      ? `Downloading… ${Math.max(0, Number(update.progressPercent) || 0)}%`
      : ready
        ? 'Open installer'
        : 'Download update';

    els.settingsBody.innerHTML = `
      <div class="panel settings-hero">
        <div class="settings-version">
          <div>
            <p class="eyebrow">PREMIUMTV</p>
            <h2>Version ${escapeHtml(current || appInfo.version || 'unknown')}</h2>
          </div>
          <span class="badge ${meta.library_scope === 'all' ? 'warn' : 'ok'}">${
            meta.library_scope === 'all' ? 'GLOBAL LIBRARY' : 'STABLE · USA'
          }</span>
        </div>
        <div class="settings-stats">
          <div><strong>${escapeHtml(String((snapshot.library.channels || []).length))}</strong><span>channels</span></div>
          <div><strong>${escapeHtml(String((snapshot.library.groups || []).length))}</strong><span>categories</span></div>
          <div><strong>${escapeHtml(String(guideCount))}</strong><span>with guide</span></div>
          <div><strong>${escapeHtml(meta.version || 'unknown')}</strong><span>library build</span></div>
        </div>
        <p class="muted">Built ${escapeHtml(meta.generated_utc || 'unknown')} · ${sourceBadge}</p>
        <div class="actions">
          <button class="btn btn-primary" id="force-refresh" ${refreshing ? 'disabled' : ''}>${
            refreshing ? 'Refreshing…' : 'Force refresh'
          }</button>
          <button class="btn" id="check-update" ${updateBusy ? 'disabled' : ''}>${
            update.checking ? 'Checking…' : 'Check for update'
          }</button>
          <button class="btn" id="check-bugs" ${bugCheckRunning ? 'disabled' : ''}>${
            bugCheckRunning ? 'Checking for bugs…' : 'Check for bugs'
          }</button>
          ${available ? `<button class="btn btn-primary" id="download-update" ${updateBusy ? 'disabled' : ''}>${
            escapeHtml(downloadLabel)
          }</button>` : ''}
        </div>
        <p class="settings-status ${update.error ? 'bad' : ''}">${escapeHtml(status)}</p>
      </div>

      ${bugReport ? renderBugReport(bugReport) : ''}

      <div class="panel">
        <h2>App updates</h2>
        <dl class="meta compact">
          <dt>Installed</dt><dd>${escapeHtml(current)}</dd>
          <dt>Newest stable</dt><dd>${escapeHtml(latest || 'not checked yet')}</dd>
          <dt>Last check</dt><dd>${formatStamp(update.lastCheckedAtMillis)}</dd>
          <dt>Installer</dt><dd>${escapeHtml(
            update.installerSize ? formatMegabytes(update.installerSize) : 'not downloaded',
          )}${ready && update.installerPath ? ` · ${escapeHtml(update.installerPath)}` : ''}</dd>
        </dl>
        <p class="muted">Only a published stable release above ${escapeHtml(current)} is offered. The daily
          check sends GitHub the previous ETag; the installer downloads only when you press the button,
          is checked against the release's SHA-256 file and is reused rather than downloaded again.</p>
      </div>

      <div class="panel">
        <h2>Refresh &amp; files</h2>
        <dl class="meta compact">
          <dt>Last attempt</dt><dd>${formatStamp(info.lastAttemptAt)}${info.lastTrigger ? ` · ${escapeHtml(info.lastTrigger)}` : ''}</dd>
          <dt>Last success</dt><dd>${formatStamp(info.lastSuccessAt)}</dd>
          <dt>Last result</dt><dd>${escapeHtml(info.lastMessage || 'No refresh has been attempted in this install yet.')}</dd>
          <dt>Next automatic check</dt><dd>${formatStamp(info.nextAutomaticAt)} <span class="muted">${escapeHtml(
            relativeFromNow(info.nextAutomaticAt),
          )}</span></dd>
        </dl>
        <div class="actions">
          <button class="btn" id="check-now" ${refreshing ? 'disabled' : ''}>Check for changes</button>
          <button class="btn btn-danger" id="reset-bundled" ${refreshing ? 'disabled' : ''}>Reset to bundled copy</button>
          <button class="btn" id="restore-hidden" ${deadFeeds.size ? '' : 'disabled'}>${
            deadFeeds.size ? `Restore ${deadFeeds.size} hidden channel${deadFeeds.size === 1 ? '' : 's'}` : 'No hidden channels'
          }</button>
        </div>
        <p class="muted">Channels the player watched fail on every server are hidden for seven days so
          they cannot be opened again by mistake. Restore them to try again — a dead link may have come back.</p>
      </div>

      <details class="panel">
        <summary><h2>Details</h2></summary>
        <dl class="meta">
          <dt>Library scope</dt><dd>${escapeHtml(meta.library_scope || 'usa')}${Array.isArray(meta.preview_features) && meta.preview_features.length ? ` · preview: ${escapeHtml(meta.preview_features.join(', '))}` : ''}</dd>
          <dt>Guide listings</dt><dd>${escapeHtml(String(meta.programme_count || (snapshot.library.programmes || []).length))} for ${escapeHtml(String(guideCount))} channels</dd>
          <dt>Guide window</dt><dd>${meta.window_start ? `${formatClock(meta.window_start)} – ${formatClock(meta.window_end)}` : 'unknown'}</dd>
          <dt>Playlist source</dt><dd>${escapeHtml(meta.playlist || '')}</dd>
          <dt>Guide source</dt><dd>${escapeHtml(meta.guide || '')}</dd>
          <dt>Refresh URL (playlist)</dt><dd>${escapeHtml(meta.playlist_url || '')}</dd>
          <dt>Refresh URL (guide)</dt><dd>${escapeHtml(meta.guide_url || '')}</dd>
          <dt>Check times</dt><dd>${escapeHtml((appInfo.checkTimes || []).join(', '))}</dd>
        </dl>
        <p class="muted">Refreshes follow the repository's publishing jobs in ${escapeHtml(
          appInfo.repositoryTimeZone || 'America/New_York',
        )}, ${escapeHtml(String(appInfo.publishingGraceMinutes || 45))} minutes after each slot. Unchanged
          playlist and guide files use ETag / Last-Modified, so they cost two small 304 responses.</p>
      </details>

      <details class="panel">
        <summary><h2>About this build</h2></summary>
        <dl class="meta">
          <dt>PremiumTV</dt><dd>${escapeHtml(appInfo.version || '')}</dd>
          <dt>Electron</dt><dd>${escapeHtml(appInfo.electron || '')}</dd>
          <dt>Chromium</dt><dd>${escapeHtml(appInfo.chromium || '')}</dd>
          <dt>Platform</dt><dd>${escapeHtml(appInfo.platform || '')} (${escapeHtml(appInfo.arch || '')})</dd>
          <dt>App data</dt><dd>${escapeHtml(appInfo.userData || '')}</dd>
          <dt>Bundled data</dt><dd>${escapeHtml(appInfo.bundleDir || '')}</dd>
        </dl>
        <p class="muted">This app is ad-hoc signed and not notarized by Apple. On first launch, right-click it
          in Applications and choose Open. A channel that will not play is almost always a dead upstream link.</p>
      </details>
    `;

    renderActivity();
    const bind = (id, event, handler) => {
      const element = document.getElementById(id);
      if (element) element.addEventListener(event, handler);
    };
    bind('force-refresh', 'click', () => runRefresh(true, 'force-refresh'));
    bind('check-now', 'click', () => runRefresh(false, 'check-now'));
    bind('reset-bundled', 'click', resetToBundled);
    bind('restore-hidden', 'click', () => {
      deadFeeds = health ? health.clear(window.localStorage) : new Set();
      renderCategories();
      renderChannels();
      renderSettings();
    });
    bind('check-update', 'click', async (event) => {
      event.currentTarget.disabled = true;
      await api.checkForUpdate(true);
      updateState = await api.updateStatus();
      renderSettings();
    });
    bind('download-update', 'click', async (event) => {
      event.currentTarget.disabled = true;
      const state = updateState || appInfo.updates || {};
      if (state.downloadedVersion && state.downloadedVersion === state.availableVersion) {
        await api.installUpdate();
      } else {
        await api.downloadUpdate();
      }
      updateState = await api.updateStatus();
      renderSettings();
    });
    bind('check-bugs', 'click', () => runBugCheck());
  }

  // ------------------------------------------------------------- bug check
  //
  // The renderer already has the loaded library, the refresh result and the
  // update state. The main process adds environment facts (bundle present,
  // data directory writable) through one read-only IPC call. Nothing here
  // changes data, so a bug check can never make a working install worse.

  let bugReport = null;
  let bugCheckRunning = false;

  function diagnoseStatusLine(info, update, refreshing) {
    if (refreshing) return 'Refreshing the channel list and guide…';
    if (update && update.error) return `Update check failed: ${update.error}`;
    if (bugCheckRunning) return 'Checking the library for bugs…';
    if (bugReport) {
      if (bugReport.fail) return `${bugReport.fail} bug${bugReport.fail === 1 ? '' : 's'} found — see the report below.`;
      if (bugReport.warn) return `No blocking bugs · ${bugReport.warn} warning${bugReport.warn === 1 ? '' : 's'}.`;
      return `All ${bugReport.checks.length} checks passed.`;
    }
    if (info.lastMessage) return info.lastMessage;
    if (update && update.message) return update.message;
    return 'Everything is ready.';
  }

  async function runBugCheck() {
    if (bugCheckRunning) return;
    bugCheckRunning = true;
    if (ui.tab === 'settings') renderSettings();
    let environment = null;
    try {
      environment = typeof api.diagnostics === 'function' ? await api.diagnostics() : null;
    } catch (error) {
      environment = { error: error && error.message ? error.message : String(error) };
    }
    bugReport = buildBugReport(environment);
    bugCheckRunning = false;
    if (ui.tab === 'settings') renderSettings();
  }

  function buildBugReport(environment) {
    const library = snapshot.library || {};
    const meta = library.meta || {};
    const info = snapshot.info || {};
    const update = updateState || appInfo.updates || {};
    const channels = Array.isArray(library.channels) ? library.channels : [];
    const programmes = Array.isArray(library.programmes) ? library.programmes : [];
    const checks = [];
    const add = (label, status, detail) => checks.push({ label, status, detail });

    const blank = channels.filter((c) => !c || !c.name || !c.url).length;
    const badScheme = channels.filter((c) => c && c.url && !/^https?:\/\//i.test(c.url)).length;
    const seen = new Set();
    let duplicates = 0;
    for (const channel of channels) {
      if (!channel || !channel.url) continue;
      if (seen.has(channel.url)) duplicates += 1;
      seen.add(channel.url);
    }
    add(
      'Channel list',
      channels.length === 0 || blank || badScheme ? 'fail' : duplicates ? 'warn' : 'ok',
      channels.length === 0
        ? 'No channels were loaded.'
        : blank
          ? `${blank} channel(s) have no name or stream URL.`
          : badScheme
            ? `${badScheme} channel(s) have an unusable stream URL.`
            : duplicates
              ? `${duplicates} duplicate stream URL(s).`
              : `${channels.length} channels, every entry playable in format.`,
    );

    const groups = Array.isArray(library.groups) ? library.groups : [];
    const groupNames = new Set(groups.map((g) => g && g.name));
    const ungrouped = channels.filter((c) => c && c.group && !groupNames.has(c.group)).length;
    add(
      'Categories',
      groups.length === 0 ? 'fail' : ungrouped ? 'warn' : 'ok',
      groups.length === 0
        ? 'No categories were loaded.'
        : ungrouped
          ? `${ungrouped} channel(s) name a category that is not in the sidebar.`
          : `${groups.length} categories, every channel grouped.`,
    );

    add(
      'TV guide',
      library.guideError ? 'warn' : programmes.length === 0 ? 'fail' : 'ok',
      library.guideError
        ? `Guide unavailable: ${library.guideError}`
        : library.guideLoading
          ? 'The guide is still loading; channels remain usable.'
          : programmes.length === 0
            ? 'No programme listings parsed.'
            : `${programmes.length} listings across ${meta.guide_channels || new Set(programmes.map((p) => p.c)).size} channels.`,
    );

    const sourceProblems = [];
    if (!String(meta.playlist_url || '').startsWith('https://')) sourceProblems.push('playlist URL');
    if (!String(meta.guide_url || '').startsWith('https://')) sourceProblems.push('guide URL');
    if (!meta.version) sourceProblems.push('bundle version');
    add(
      'Data bundle',
      sourceProblems.length ? 'fail' : 'ok',
      sourceProblems.length
        ? `Missing or unsafe ${sourceProblems.join(', ')}.`
        : `Built ${meta.generated_utc || 'unknown'} · scope ${meta.library_scope || 'usa'}.`,
    );

    const refreshFailed = info.lastAttemptAt && Number(info.lastSuccessAt || 0) < Number(info.lastAttemptAt);
    add(
      'Refresh pipeline',
      refreshFailed ? 'warn' : 'ok',
      info.inProgress
        ? 'A refresh is running now.'
        : refreshFailed
          ? (info.lastMessage || 'The last refresh did not finish.')
          : info.lastTrigger
            ? 'Last success and last attempt agree.'
            : 'No refresh yet; the bundled copy is in use.',
    );

    add(
      'App updates',
      update.error ? 'fail' : 'ok',
      update.error
        ? update.error
        : update.availableVersion
          ? `PremiumTV ${update.availableVersion} is ready in App updates.`
          : update.latestStableVersion
            ? `Newest stable ${update.latestStableVersion}; this build is current.`
            : 'Not checked yet; press Check for update.',
    );

    const installed = String(update.currentVersion || appInfo.version || '');
    // Display V name for patch builds: 1.0.8.1 -> 1.0.8 V1
    const patchDisplay = (() => {
      const p = String(installed).split('.');
      if (p.length === 4 && p[3] !== '0' && Number.isFinite(Number(p[3]))) return `${p[0]}.${p[1]}.${p[2]} V${p[3]}`;
      return installed;
    })();
    add(
      'Version',
      installed && meta.version ? 'ok' : 'warn',
      `Installed ${installed || 'unknown'}${patchDisplay !== installed ? ` (${patchDisplay})` : ''} · library built for ${meta.version || 'unknown'} · V patches order by fourth number.`,
    );

    // 1.0.8 V1 Patch: patch chain integrity — each V must raise the fourth number.
    if (/^\d+\.\d+\.\d+\.\d+$/.test(installed)) {
      const parts = String(installed).split('.').map(Number);
      const patchOk = parts.length === 4 && parts[3] >= 1 && parts[3] <= 9999;
      add(
        'Patch chain',
        patchOk ? 'ok' : 'warn',
        patchOk ? `Patch V${parts[3]} of ${parts[0]}.${parts[1]}.${parts[2]} — chain intact, next V is V${parts[3] + 1}.` : `Patch version ${installed} has an unexpected format.`,
      );
    }

    // Stream hygiene: spaces in URLs and malformed logos are common breakage on TVs.
    const spacedUrls = channels.filter((c) => c && c.url && String(c.url).includes(' ')).length;
    const logoProblems = channels.filter((c) => c && c.logo && !/^https?:\/\//i.test(c.logo)).length;
    add(
      'Stream hygiene',
      spacedUrls ? 'warn' : logoProblems ? 'warn' : 'ok',
      spacedUrls ? `${spacedUrls} stream URL(s) contain spaces — they may fail on some players.` : logoProblems ? `${logoProblems} logo URL(s) look malformed.` : 'All stream and logo URLs are clean.',
    );

    // Guide freshness: how old is the advertised window start?
    const windowStart = Number(meta.window_start || meta.windowStart || 0);
    if (library.guideError) {
      add('Guide freshness', 'warn', `Guide error hides freshness: ${library.guideError}`);
    } else if (!windowStart) {
      add('Guide freshness', 'warn', 'Guide window not reported — freshness unknown.');
    } else {
      const ageDays = (Date.now() / 1000 - windowStart) / 86400;
      const text = ageDays > 14 ? `Guide window is ${ageDays.toFixed(1)} days old — a refresh may be overdue.` : ageDays > 7 ? `Guide window is ${ageDays.toFixed(1)} days old.` : `Guide window is ${ageDays.toFixed(1)} days old — fresh.`;
      add('Guide freshness', ageDays > 7 ? 'warn' : 'ok', text);
    }

    // Library health: empty categories and oversized groups stress TV hardware.
    const emptyGroups = groups.filter((g) => !g || Number(g.count) === 0).length;
    const hugeGroup = groups.reduce((m, g) => Math.max(m, Number(g && g.count) || 0), 0);
    add(
      'Library health',
      emptyGroups ? 'warn' : hugeGroup > 5000 ? 'warn' : 'ok',
      emptyGroups ? `${emptyGroups} categories report 0 channels — shelf may be stale.` : hugeGroup > 5000 ? `Largest category holds ${hugeGroup} channels — UI paging is active, but verify on low-memory devices.` : `No empty categories; largest holds ${hugeGroup} channels.`,
    );

    if (environment) {
      const ok = environment.bundleOk !== false && environment.userDataWritable !== false;
      add(
        'Files & storage',
        environment.error || !ok ? 'warn' : 'ok',
        environment.error
          ? environment.error
          : `Bundle ${environment.bundleOk ? 'present' : 'missing'} · data folder ${
            environment.userDataWritable ? 'writable' : 'not writable'
          }.`,
      );
    }

    const fail = checks.filter((c) => c.status === 'fail').length;
    const warn = checks.filter((c) => c.status === 'warn').length;
    return { checks, fail, warn, ok: checks.filter((c) => c.status === 'ok').length };
  }

  function renderBugReport(report) {
    const accent = report.fail ? 'bad' : report.warn ? 'warn' : 'ok';
    const title = report.fail
      ? `${report.fail} bug${report.fail === 1 ? '' : 's'} found`
      : report.warn
        ? `No blocking bugs · ${report.warn} warning${report.warn === 1 ? '' : 's'}`
        : `All ${report.checks.length} checks passed`;
    const icon = { ok: '✓', warn: '!', fail: '×' };
    return `
      <div class="panel bug-report">
        <div class="bug-head">
          <h2>Check for bugs</h2>
          <span class="badge ${accent}">${escapeHtml(title)}</span>
        </div>
        <ul class="bug-list">
          ${report.checks.map((check) => `
            <li class="bug-${check.status}">
              <span class="bug-mark">${icon[check.status]}</span>
              <strong>${escapeHtml(check.label)}</strong>
              <span>${escapeHtml(check.detail)}</span>
            </li>`).join('')}
        </ul>
        <p class="muted">Offline, read-only check of the loaded library, refresh state and update
          configuration. Press it again after a refresh to confirm a fix.</p>
      </div>`;
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
    // The sidebar's sort row belongs with the category list.
    if (els.catSort) els.catSort.style.display = categories ? '' : 'none';
    els.search.placeholder = tab === 'guide'
      ? (cableGuideEnabled() ? 'Search channel or show' : 'Search the guide')
      : tab === 'live'
        ? 'Search live games'
        : tab === 'movies'
          ? 'Browse movies & shows'
          : 'Search channels';
    render();
    // Opening the Live Events tab checks the games it has no answer for yet;
    // the refresh button re-asks every game on demand.
    if (ui.tab === 'live') probeLiveGames(false);
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
    else if (ui.tab === 'movies') renderMovies();
    else renderSettings();
  }

  // ------------------------------------------------ 1.1.2 Movies & Shows
  //
  // The 1.1.1 tab was a coming-soon page. This one renders the on-demand test
  // catalogue: public-domain films and classic TV episodes resolved by
  // scripts/vod_catalog.py (plus the repository's own synthetic test card),
  // shipped in the bundle and played through the same side player as a
  // channel. An item is one finite stream, so it has no guide listings and no
  // backup servers - the player simply opens it.

  const VOD_POSITIONS_KEY = 'premiumtv.vod.positions.v1';

  function loadVodPositions() {
    try {
      const raw = JSON.parse(window.localStorage.getItem(VOD_POSITIONS_KEY) || '{}');
      return raw && typeof raw === 'object' ? raw : {};
    } catch (error) {
      return {};
    }
  }

  function saveVodPosition(id, seconds, duration) {
    if (!id || !Number.isFinite(seconds)) return;
    try {
      const store = loadVodPositions();
      if (Number.isFinite(duration) && duration > 20 && seconds >= duration - 12) {
        delete store[id];
      } else if (seconds >= 5) {
        store[id] = Math.floor(seconds);
      } else {
        return;
      }
      window.localStorage.setItem(VOD_POSITIONS_KEY, JSON.stringify(store));
    } catch (error) {
      /* storage unavailable */
    }
  }

  function formatMediaClock(totalSeconds) {
    if (!Number.isFinite(totalSeconds) || totalSeconds < 0) return '0:00';
    const whole = Math.floor(totalSeconds);
    const hrs = Math.floor(whole / 3600);
    const mins = Math.floor((whole % 3600) / 60);
    const secs = whole % 60;
    const pad = (n) => String(n).padStart(2, '0');
    return hrs > 0 ? `${hrs}:${pad(mins)}:${pad(secs)}` : `${mins}:${pad(secs)}`;
  }

  function vodLabel(item) {
    if (item.kind === 'movie') return 'FILM';
    if (item.season > 0 && item.episode > 0) return `S${item.season} E${item.episode}`;
    if (item.season > 0) return `S${item.season}`;
    return 'EPISODE';
  }

  function vodDetail(item) {
    return [
      item.year > 0 ? String(item.year) : '',
      item.genre || '',
      item.runtime_seconds > 0 ? `${Math.round(item.runtime_seconds / 60)} min` : '',
    ].filter(Boolean).join(' · ');
  }

  /** The player's input: the same shape a channel has, minus the live bits. */
  function vodChannel(item, streamUrl = item.stream) {
    return {
      id: item.id,
      name: item.kind === 'movie' ? item.title : `${item.show || item.title} · ${vodLabel(item)}`,
      url: streamUrl,
      logo: item.poster || '',
      group: item.kind === 'movie' ? 'Movies' : 'TV Shows',
      country: 'US',
      vod: true,
      vodSummary: item.summary || '',
      vodDetail: vodDetail(item),
    };
  }

  function vodServers(item) {
    const urls = Array.isArray(item.streams) && item.streams.length
      ? item.streams.filter(Boolean)
      : [item.stream];
    const unique = [...new Set(urls)];
    return unique.map((url) => vodChannel(item, url));
  }

  function watchVod(item) {
    const servers = vodServers(item);
    openPlayer(servers[0], servers);
  }

  function renderMovies() {
    if (!els.moviesGrid) return;
    const items = Array.isArray(ui.vodItems) ? ui.vodItems : [];
    const byKind = ui.vodFilter === 'all' ? items : items.filter((item) => item.kind === ui.vodFilter);

    const genres = [...new Set(byKind.map((item) => item.genre).filter(Boolean))].sort();
    if (ui.vodGenre !== 'all' && !genres.includes(ui.vodGenre)) {
      ui.vodGenre = 'all';
    }
    if (els.moviesGenres) {
      if (genres.length > 1) {
        els.moviesGenres.hidden = false;
        const chips = ['all', ...genres].map((genre) => {
          const label = genre === 'all' ? 'All genres' : genre;
          const active = ui.vodGenre === genre;
          return `<button class="vod-genre-chip" type="button" data-vod-genre="${escapeHtml(genre)}" aria-pressed="${active}">${escapeHtml(label)}</button>`;
        });
        els.moviesGenres.innerHTML = chips.join('');
        for (const btn of els.moviesGenres.querySelectorAll('[data-vod-genre]')) {
          btn.addEventListener('click', () => {
            ui.vodGenre = btn.dataset.vodGenre || 'all';
            renderMovies();
          });
        }
      } else {
        els.moviesGenres.innerHTML = '';
        els.moviesGenres.hidden = true;
      }
    }

    const needle = (ui.vodQuery || '').trim().toLowerCase();
    const shown = byKind.filter((item) => {
      if (ui.vodGenre !== 'all' && item.genre !== ui.vodGenre) return false;
      if (!needle) return true;
      const hay = `${item.title || ''} ${item.show || ''} ${item.genre || ''} ${item.summary || ''} ${item.year || ''}`.toLowerCase();
      return hay.includes(needle);
    });

    if (els.moviesSubtitle) {
      els.moviesSubtitle.textContent = items.length
        ? `${items.length} on demand · films, classic TV and a test card · plays in the side player`
        : 'Films, classic TV episodes and a test card, on demand.';
    }
    for (const chip of document.querySelectorAll('#movies-filters .vod-chip')) {
      chip.setAttribute('aria-pressed', String(chip.dataset.vodFilter === ui.vodFilter));
    }
    const positions = loadVodPositions();
    els.moviesGrid.innerHTML = shown.map((item) => {
      const kind = item.kind === 'movie' ? 'movie' : 'episode';
      const summary = item.summary ? `<p class="vod-summary">${escapeHtml(item.summary)}</p>` : '';
      const detail = vodDetail(item);
      const savedSec = Number(positions[item.id] || 0);
      const resumeBadge = savedSec >= 5
        ? `<span class="vod-resume">Continue · ${escapeHtml(formatMediaClock(savedSec))}</span>`
        : '';
      return `
        <button class="vod-card" data-vod-id="${escapeHtml(item.id)}" data-vod-kind="${kind}" aria-label="Play ${escapeHtml(item.title)}">
          <span class="vod-poster">
            <img src="${escapeHtml(item.poster || '')}" alt="" loading="lazy" />
            <span class="vod-play">▶</span>
            <span class="vod-label">${escapeHtml(vodLabel(item))}</span>
            ${resumeBadge}
          </span>
          <span class="vod-body">
            <span class="vod-title">${escapeHtml(item.title)}</span>
            ${detail ? `<span class="vod-detail">${escapeHtml(detail)}</span>` : ''}
            ${summary}
          </span>
        </button>`;
    }).join('');
    for (const card of els.moviesGrid.querySelectorAll('[data-vod-id]')) {
      card.addEventListener('click', () => {
        const item = shown.find((candidate) => candidate.id === card.dataset.vodId);
        if (item) watchVod(item);
      });
    }
    if (els.moviesEmpty) {
      els.moviesEmpty.hidden = shown.length > 0;
      els.moviesEmpty.textContent = items.length
        ? 'No titles match this filter.'
        : 'No on-demand catalogue in this build. Run scripts/vod_catalog.py and rebuild the bundle.';
    }
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
        button.textContent = force ? 'Force refresh' : 'Check for changes';
      }
      render();
      renderActivity();
      // A refresh swaps games in and out of the playlist; whatever the Live
      // Events tab has no answer for yet gets checked right away.
      if (ui.tab === 'live') probeLiveGames(false);
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
    if (channel.vod) {
      els.playerNow.textContent = channel.vodDetail || 'On demand';
      els.playerNext.textContent = '';
      els.playerDetail.textContent = channel.vodSummary || channel.group;
      renderServerBadge();
      return;
    }
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

  let audioSilentHopUsed = false;
  let vodResumeAppliedForId = '';
  let lastVodSaveAt = 0;
  let seekingDrag = false;

  function isFiniteVodPlayback() {
    const channel = currentChannel();
    const dur = els.video ? els.video.duration : NaN;
    return Boolean((channel && channel.vod) || (Number.isFinite(dur) && dur > 0 && dur < 86400));
  }

  function syncTransportChrome() {
    const video = els.video;
    if (!video) return;
    const seekable = isFiniteVodPlayback();
    if (els.playerToggle) {
      const paused = Boolean(video.paused);
      els.playerToggle.textContent = paused ? '▶' : '❚❚';
      els.playerToggle.setAttribute('aria-label', paused ? 'Play' : 'Pause playback');
    }
    if (els.playerBack10) els.playerBack10.hidden = !seekable;
    if (els.playerFwd10) els.playerFwd10.hidden = !seekable;
    if (els.playerSeek) els.playerSeek.hidden = !seekable;
    if (els.playerTime) els.playerTime.hidden = !seekable;
    if (els.playerLivePill) els.playerLivePill.hidden = seekable;
    if (seekable) {
      const cur = Number.isFinite(video.currentTime) ? video.currentTime : 0;
      const dur = Number.isFinite(video.duration) && video.duration > 0 ? video.duration : 0;
      if (els.playerTime) {
        els.playerTime.textContent = dur > 0
          ? `${formatMediaClock(cur)} / ${formatMediaClock(dur)}`
          : formatMediaClock(cur);
      }
      if (els.playerSeek && !seekingDrag && dur > 0) {
        els.playerSeek.value = String(Math.round((cur / dur) * 1000));
      }
    }
    const muted = window.PremiumPlayer.isMuted ? window.PremiumPlayer.isMuted() : Boolean(video.muted);
    const volume = window.PremiumPlayer.getVolume ? window.PremiumPlayer.getVolume() : (video.volume ?? 1);
    if (els.playerMute) {
      els.playerMute.textContent = muted || volume === 0 ? '🔇' : '🔊';
      els.playerMute.setAttribute('aria-label', muted ? 'Unmute audio' : 'Mute audio');
    }
    if (els.playerVolume) {
      els.playerVolume.value = String(Math.round((muted ? 0 : volume) * 100));
    }
  }

  if (typeof window.PremiumPlayer.onAudioState === 'function') {
    window.PremiumPlayer.onAudioState((audioState) => {
      syncTransportChrome();
      const tracks = Array.isArray(audioState.tracks) ? audioState.tracks : [];
      if (els.playerAudioTrack) {
        if (tracks.length > 1) {
          const activeLabel = audioState.activeTrack ? audioState.activeTrack.label : 'Audio';
          els.playerAudioTrack.textContent = `🔊 ${activeLabel} (${tracks.length})`;
          els.playerAudioTrack.hidden = false;
        } else {
          els.playerAudioTrack.hidden = true;
        }
      }
      if (audioState.switchedTrack) {
        els.statusText.textContent = `Switched audio track to ${audioState.switchedTrack}`;
        if (els.playerAudioBadge) {
          els.playerAudioBadge.textContent = `🔊 ${audioState.switchedTrack}`;
          els.playerAudioBadge.hidden = false;
        }
      } else if (audioState.silent && !els.player.hidden) {
        const channel = currentChannel();
        if (channel && !channel.vod && playQueue.length > 1 && !audioSilentHopUsed) {
          audioSilentHopUsed = true;
          playQueueIndex = (playQueueIndex + 1) % playQueue.length;
          els.statusText.textContent =
            `No audio decoded on previous feed — trying server ${playQueueIndex + 1} of ${playQueue.length}…`;
          playCurrentServer().catch(() => {});
          return;
        }
        if (els.playerAudioBadge) {
          els.playerAudioBadge.textContent = '🔇 No audio track decoded on this feed';
          els.playerAudioBadge.hidden = false;
        }
        els.statusText.textContent = playQueue.length > 1
          ? 'No audio track decoded on this feed — try Server ▶ for another feed.'
          : 'No audio track decoded on this stream.';
      } else if (!audioState.silent && els.playerAudioBadge) {
        els.playerAudioBadge.hidden = true;
      }
    });
  }

  async function openPlayer(channel, servers) {
    noteWatched(channel);
    const list = Array.isArray(servers) && servers.length
      ? servers
      : window.PremiumLive.serversFor(channel, snapshot.library.channels || []);
    playQueue = list;
    playQueueIndex = Math.max(0, list.findIndex((item) => item.url === channel.url));
    audioSilentHopUsed = false;
    vodResumeAppliedForId = '';
    if (els.playerAudioBadge) els.playerAudioBadge.hidden = true;
    els.player.hidden = false;
    // 1.1.2: a channel (or an on-demand item) opens in the side player; one
    // click on the picture grows it to the full window.
    playerMini = true;
    updatePlayerMode();
    describeChannel(playQueue[playQueueIndex] || channel);
    syncTransportChrome();
    await playCurrentServer(channel.name);
  }

  /**
   * The side player (1.0.8): the same player element rendered as a small
   * corner card (#player.mini) so the stream never restarts while the viewer
   * browses. Clicking the corner picture — or the button, once it says
   * "⤢ Big screen" — grows it back to the full window.
   */
  function minimizePlayer() {
    if (els.player.hidden) return;
    playerMini = true;
    updatePlayerMode();
  }

  function expandPlayer() {
    playerMini = false;
    updatePlayerMode();
  }

  function updatePlayerMode() {
    els.player.classList.toggle('mini', playerMini);
    if (els.playerMinimize) {
      els.playerMinimize.textContent = playerMini ? '⤢ Big screen' : '⧉ Side player';
      els.playerMinimize.setAttribute(
        'aria-label',
        playerMini ? 'Grow the side player back to the big screen' : 'Tuck the player into the side of the window',
      );
    }
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
    // Every feed failed: remember the feed so the browser stops offering this
    // dead channel, and redraw the list behind the player.
    const dead = playQueue[playQueueIndex];
    if (health && dead && dead.url) {
      deadFeeds = health.record(window.localStorage, dead.url);
      renderCategories();
      if (ui.tab === 'channels') renderChannels();
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
    const closing = currentChannel();
    if (closing && closing.vod && els.video) {
      saveVodPosition(closing.id, els.video.currentTime, els.video.duration);
      if (ui.tab === 'movies') renderMovies();
    }
    window.PremiumPlayer.stop();
    els.player.hidden = true;
    if (els.playerAudioBadge) els.playerAudioBadge.hidden = true;
    playerMini = false;
    els.player.classList.remove('mini');
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

  // 1.0.8 sorting: the sidebar chips order the category list; the chips on a
  // category page order that page's channels.
  if (els.catSort) {
    els.catSort.addEventListener('click', (event) => {
      const button = event.target.closest('.cat-sort-btn');
      if (!button) return;
      ui.categorySort = button.dataset.sort;
      renderCategories();
    });
  }
  if (els.channelSort) {
    els.channelSort.addEventListener('click', (event) => {
      const button = event.target.closest('.cat-sort-btn');
      if (!button) return;
      ui.channelSort = button.dataset.chsort;
      renderChannels();
    });
  }
  if (els.catBack) els.catBack.addEventListener('click', () => selectCategory(null));
  if (els.moviesFilters) {
    els.moviesFilters.addEventListener('click', (event) => {
      const button = event.target.closest('[data-vod-filter]');
      if (!button) return;
      ui.vodFilter = button.dataset.vodFilter;
      renderMovies();
    });
  }
  if (els.moviesSearch) {
    els.moviesSearch.addEventListener('input', () => {
      ui.vodQuery = els.moviesSearch.value;
      renderMovies();
    });
  }
  if (els.liveRefresh) {
    els.liveRefresh.addEventListener('click', () => {
      // The tab's own refresh: the newest playlist (ended games drop out,
      // new games appear) plus a fresh live check of every game on the card.
      runRefresh(true);
      probeLiveGames(true);
    });
  }

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
  // The side player toggle: tuck on the big screen, grow in the corner.
  if (els.playerMinimize) {
    els.playerMinimize.addEventListener('click', () => {
      if (playerMini) expandPlayer();
      else minimizePlayer();
    });
  }
  // Clicking the corner picture grows the side player back to the big screen.
  if (window.PremiumPlayer.element) {
    window.PremiumPlayer.element.addEventListener('click', () => {
      if (playerMini && !els.player.hidden) expandPlayer();
    });
  }
  if (els.playerPrevServer) els.playerPrevServer.addEventListener('click', () => switchServer(-1));
  if (els.playerNextServer) els.playerNextServer.addEventListener('click', () => switchServer(1));
  if (els.playerFavorite) els.playerFavorite.addEventListener('click', toggleFavorite);
  els.playerRetry.addEventListener('click', () => window.PremiumPlayer.retry());

  if (els.playerControls) {
    els.playerControls.addEventListener('click', (event) => event.stopPropagation());
  }
  if (els.playerToggle) {
    els.playerToggle.addEventListener('click', () => {
      if (!els.video) return;
      if (els.video.paused) els.video.play().catch(() => {});
      else els.video.pause();
      syncTransportChrome();
    });
  }
  if (els.playerBack10) {
    els.playerBack10.addEventListener('click', () => {
      if (!els.video || !isFiniteVodPlayback()) return;
      els.video.currentTime = Math.max(0, (els.video.currentTime || 0) - 10);
      syncTransportChrome();
    });
  }
  if (els.playerFwd10) {
    els.playerFwd10.addEventListener('click', () => {
      if (!els.video || !isFiniteVodPlayback()) return;
      const dur = Number.isFinite(els.video.duration) ? els.video.duration : Infinity;
      els.video.currentTime = Math.min(dur, (els.video.currentTime || 0) + 10);
      syncTransportChrome();
    });
  }
  if (els.playerSeek) {
    els.playerSeek.addEventListener('mousedown', () => { seekingDrag = true; });
    els.playerSeek.addEventListener('mouseup', () => { seekingDrag = false; });
    els.playerSeek.addEventListener('input', () => {
      if (!els.video || !Number.isFinite(els.video.duration) || els.video.duration <= 0) return;
      const ratio = Number(els.playerSeek.value) / 1000;
      els.video.currentTime = ratio * els.video.duration;
      syncTransportChrome();
    });
  }
  if (els.playerMute) {
    els.playerMute.addEventListener('click', () => {
      if (typeof window.PremiumPlayer.toggleMute === 'function') {
        window.PremiumPlayer.toggleMute();
      } else if (els.video) {
        els.video.muted = !els.video.muted;
      }
      syncTransportChrome();
    });
  }
  if (els.playerVolume) {
    els.playerVolume.addEventListener('input', () => {
      const vol = Number(els.playerVolume.value) / 100;
      if (typeof window.PremiumPlayer.setVolume === 'function') {
        window.PremiumPlayer.setVolume(vol);
      } else if (els.video) {
        els.video.volume = vol;
        els.video.muted = vol === 0;
      }
      syncTransportChrome();
    });
  }
  if (els.playerAudioTrack) {
    els.playerAudioTrack.addEventListener('click', () => {
      if (typeof window.PremiumPlayer.cycleAudioTrack === 'function') {
        window.PremiumPlayer.cycleAudioTrack();
      }
      syncTransportChrome();
    });
  }
  if (els.video && typeof els.video.addEventListener === 'function') {
    for (const evt of ['play', 'pause', 'durationchange', 'volumechange']) {
      els.video.addEventListener(evt, syncTransportChrome);
    }
    els.video.addEventListener('loadedmetadata', () => {
      const channel = currentChannel();
      if (channel && channel.vod && vodResumeAppliedForId !== channel.id) {
        vodResumeAppliedForId = channel.id;
        const saved = Number(loadVodPositions()[channel.id] || 0);
        if (saved >= 5 && Number.isFinite(els.video.duration) && saved < els.video.duration - 12) {
          els.video.currentTime = saved;
          els.statusText.textContent = `Resumed ${channel.name} at ${formatMediaClock(saved)}`;
        }
      }
      syncTransportChrome();
    });
    els.video.addEventListener('timeupdate', () => {
      syncTransportChrome();
      const channel = currentChannel();
      if (channel && channel.vod && Date.now() - lastVodSaveAt >= 5000) {
        lastVodSaveAt = Date.now();
        saveVodPosition(channel.id, els.video.currentTime, els.video.duration);
      }
    });
    els.video.addEventListener('ended', () => {
      const channel = currentChannel();
      if (channel && channel.vod) {
        saveVodPosition(channel.id, els.video.duration, els.video.duration);
        if (ui.tab === 'movies') renderMovies();
      }
      syncTransportChrome();
    });
  }

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
    const blocked = notice.level === 'blocked';
    els.updateNotice.classList.toggle('ended', ended || blocked);
    els.updateNoticeEyebrow.textContent = blocked
      ? 'BUILD RETIRED'
      : ended
        ? 'SUPPORT HAS ENDED'
        : 'PREMIUMTV UPDATE';
    els.updateNoticeTitle.textContent = notice.title || 'A newer PremiumTV is available';
    els.updateNoticeMessage.textContent = notice.message || '';
    els.updateNoticeSurpriseWrap.hidden = !notice.surprise;
    const surpriseLabel = els.updateNoticeSurpriseWrap.querySelector('.notice-surprise-label');
    if (surpriseLabel) surpriseLabel.textContent = blocked ? 'WHAT REPLACES IT' : 'THE SURPRISE';
    els.updateNoticeSurprise.textContent = notice.surprise || '';

    const current = state.currentVersion || (appInfo && appInfo.version) || '';
    const newest = state.latestStableVersion || state.availableVersion || '';
    els.updateNoticeVersions.textContent = newest
      ? `Installed ${current} · newest on GitHub ${newest}`
      : `Installed ${current}`;
    els.updateNoticeUrl.textContent = notice.releasesUrl || '';
    els.updateNoticeAction.textContent = notice.actionLabel || 'Update now';
    els.updateNoticeDismiss.textContent = notice.dismissLabel || 'Remind me next time';
    els.updateNoticeFoot.textContent = blocked
      ? 'This retired preview is blocked from download. Install the current stable ' +
        'release; it replaces this build and keeps updating itself.'
      : ended
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
      const blocked = updateState && updateState.notice && updateState.notice.level === 'blocked';
      const releasesUrl = updateState && updateState.notice && updateState.notice.releasesUrl;
      if (blocked && releasesUrl) {
        // Stranded builds (retired preview, or 1.0.8.1's frozen alias) would
        // see Settings say “up to date”. Open the download page directly
        // so one press gets the installer without a second white lie.
        await dismissUpdateNotice();
        try {
          await api.openExternal(releasesUrl);
        } catch (error) {
          // Fall through to Settings if the shell cannot open a browser.
        }
        return;
      }
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
      // On the big screen Esc tucks the picture into the side player and
      // hands the window back to the browser; in the corner it stops.
      if (playerMini) closePlayer();
      else minimizePlayer();
      return;
    }
    if (event.key === ' ' && !els.player.hidden && event.target === document.body) {
      event.preventDefault();
      const video = window.PremiumPlayer.element;
      if (video.paused) video.play();
      else video.pause();
    }
    if ((event.key === 'm' || event.key === 'M') && !els.player.hidden
        && !['INPUT', 'TEXTAREA'].includes(document.activeElement?.tagName || '')) {
      event.preventDefault();
      if (typeof window.PremiumPlayer.toggleMute === 'function') window.PremiumPlayer.toggleMute();
      syncTransportChrome();
      return;
    }
    if (event.key === '/' && document.activeElement !== els.search
        && document.activeElement !== els.moviesSearch) {
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
    const meta = (snapshot.library && snapshot.library.meta) || {};
    // 1.1.1: the bundle ships two documents - "team_logos" ({ schema, source,
    // logos: { teamKey: url } }) and "live_schedule" ({ schema, games: [{ key,
    // kickoff_utc }] }). Flatten them into the maps the renderer looks up by
    // team key and matchup key, and do it before the derived indexes are
    // rebuilt so the first paint already has the crests and countdowns.
    const logoDoc = meta.team_logos || meta['team-logos'] || {};
    ui.teamLogos = logoDoc.logos || logoDoc;
    const scheduleDoc = meta.live_schedule || meta['live-schedule'] || {};
    ui.schedule = {};
    for (const game of scheduleDoc.games || []) {
      const kickoff = game && game.kickoff_utc ? Date.parse(game.kickoff_utc) : NaN;
      if (game && game.key && Number.isFinite(kickoff)) ui.schedule[game.key] = kickoff / 1000;
    }
    ui.sportsDoc = { team_logos: ui.teamLogos };
    // 1.1.2: the on-demand catalogue rides beside the crests in the bundle.
    const vodDoc = meta.vod_catalog || meta['vod-catalog'] || {};
    ui.vodItems = Array.isArray(vodDoc.items) ? vodDoc.items.filter((item) =>
      item && item.id && item.title && item.stream) : [];
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

  api.onProgress((progress) => {
    const pct = progress && typeof progress.percent === 'number' ? progress.percent : 68;
    setSplashProgress(pct, progress && progress.message ? progress.message : 'Loading channels & guide…');
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

  function setSplashProgress(percent, message) {
    const clamped = Math.max(8, Math.min(100, Math.round(Number(percent) || 12)));
    if (els.splashBarFill) els.splashBarFill.style.width = `${clamped}%`;
    if (els.splashBar) els.splashBar.setAttribute('aria-valuenow', String(clamped));
    if (message && els.splashStatus) els.splashStatus.textContent = message;
  }

  /** Fade the launch splash out; the app underneath is already painted. */
  function hideSplash() {
    if (!els.splash || els.splash.classList.contains('done')) return;
    setSplashProgress(100, 'Ready');
    els.splash.classList.add('done');
    els.splash.setAttribute('aria-hidden', 'true');
  }

  async function boot() {
    setSplashProgress(18, 'Starting PremiumTV…');
    appInfo = await api.getAppInfo();
    setSplashProgress(46, 'Reading your channel library…');
    updateState = appInfo.updates || null;
    renderUpdateNotice();
    const brandTag = document.getElementById('brand-tag');
    if (brandTag && appInfo.version) {
      const p = String(appInfo.version).split('.');
      const display = p.length === 4 && p[3] !== '0' ? `${p[0]}.${p[1]}.${p[2]} V${p[3]}` : appInfo.version;
      brandTag.textContent = display;
    }
    // The splash names the build the viewer is waiting on, the same way the
    // sidebar plaque and Settings do. 1.0.8 V1 Patch shows the V plaque.
    if (els.splashVersion && appInfo.version) {
      const p = String(appInfo.version).split('.');
      const display = p.length === 4 && p[3] !== '0' ? `${p[0]}.${p[1]}.${p[2]} V${p[3]} Patch` : appInfo.version;
      els.splashVersion.textContent = `Version ${display}`;
      const plaque = document.getElementById('splash-plaque');
      if (plaque) {
        if (p.length === 4 && p[3] !== '0') {
          plaque.textContent = `Patched · V${p[3]} · ${display}`;
          plaque.hidden = false;
        } else {
          plaque.hidden = true;
        }
      }
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

    // Second-accurate "Not live yet" countdowns on the Live Events tab.
    // The ticker itself runs constantly, but it only touches the DOM while
    // the tab is open, so it costs nothing elsewhere.
    let liveCountdownTimer = null;
    function ensureLiveCountdownClock() {
      if (liveCountdownTimer) return;
      liveCountdownTimer = window.setInterval(updateLiveCountdowns, 1000);
      updateLiveCountdowns();
    }
    function updateLiveCountdowns() {
      const now = Date.now();
      let flipped = false;
      for (const node of els.liveList.querySelectorAll('[data-kickoff]')) {
        const kickoff = Number(node.dataset.kickoff);
        if (kickoff > now) {
          node.textContent = `Starts in ${window.PremiumLive.countdownText(
            Math.max(0, ((kickoff - now) / 1000) | 0),
          )} · ${window.PremiumLive.kickoffLabel(kickoff)}`;
        } else if (node.dataset.flipped !== 'true') {
          node.dataset.flipped = 'true';
          node.textContent = 'Kickoff time';
          flipped = true;
        }
      }
      if (flipped) renderLive();
    }
    ensureLiveCountdownClock();
  }

  boot().catch((error) => {
    hideSplash();
    els.statusText.textContent = `Startup failed: ${error.message}`;
    snapshot.state = { phase: 'error', message: `Startup failed: ${error.message}. Quit and reopen PremiumTV to retry.` };
    renderActivity();
  });
})();
