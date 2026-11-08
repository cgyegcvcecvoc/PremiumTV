/* PremiumTV Web. Platform-independent UI; the same personal, event, health and
 * category policies as the native renderer are copied unchanged at build time. */
(function () {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const store = window.PremiumStore,
    personal = window.PremiumPersonal,
    health = window.PremiumHealth;
  const live = window.PremiumLive,
    icons = window.PremiumIcons,
    player = window.PremiumPlayer;
  const P = personal,
    S = store;
  const state = {
    tab: "channels",
    category: "",
    shelf: "",
    query: "",
    sort: "published",
    channelSort: "published",
    limit: 60,
    guideLimit: 40,
    guideLayout: "list",
    guideCategory: "",
    guideQuery: "",
    movieQuery: "",
    kind: "all",
    genre: "All",
    refreshing: false,
  };
  let library = {
    meta: {},
    channels: [],
    groups: [],
    programmes: [],
    guideLoading: false,
    guideError: "",
  };
  let movies = [],
    events = [],
    eventIndex = new Map(),
    programmeIndex = new Map();
  let favorites = P.load(S.storage, P.FAVORITES_KEY),
    recents = P.load(S.storage, P.RECENTS_KEY);
  let dead = health.load(S.storage),
    queue = [],
    serverIndex = 0,
    current = null,
    playerSerial = 0;
  let expanded = false,
    lastProgressSave = 0,
    sleepDeadline = Number(S.read(S.KEYS.sleep, 0)) || 0;
  let lastRefresh = 0,
    lastRefreshMessage = "Using the published web library.",
    bugReport = null,
    installPrompt = null;
  let toastTimer,
    searchTimer,
    guidePromise = null,
    renderToken = 0;
  const collator = new Intl.Collator(undefined, {
    numeric: true,
    sensitivity: "base",
  });
  const esc = (value) =>
    String(value == null ? "" : value).replace(
      /[&<>"']/g,
      (c) =>
        ({
          "&": "&amp;",
          "<": "&lt;",
          ">": "&gt;",
          '"': "&quot;",
          "'": "&#39;",
        })[c],
    );
  const clock = (seconds) =>
    new Date(seconds * 1000).toLocaleTimeString([], {
      hour: "numeric",
      minute: "2-digit",
    });
  const number = (value) => Number(value || 0).toLocaleString();
  const mediaClock = (value) => {
    if (!Number.isFinite(value) || value < 0) return "0:00";
    const s = Math.floor(value);
    return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;
  };
  const icon = (name, cls) => {
    const node = document.createElement("span");
    node.innerHTML = icons.svgForGroup(name, cls || "ph-icon");
    return node.firstElementChild.outerHTML;
  };
  function initializeIcons() {
    const paths = {
      settings:
        '<path d="M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM9 3h6l.7 3 2.8 1.5 2.5 2v5l-2.5 2-2.8 1.5-.7 3H9l-.7-3-2.8-1.5-2.5-2v-5l2.5-2L8.3 6z"/>',
      search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
      clock: '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
      info: '<circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7v1"/>',
    };
    document.querySelectorAll("[data-icon]").forEach((el) => {
      const name = el.dataset.icon;
      el.innerHTML = paths[name]
        ? `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${paths[name]}</svg>`
        : icons.svgForGroup(name);
    });
  }
  function toast(message) {
    clearTimeout(toastTimer);
    $("toast").textContent = message;
    $("toast").hidden = false;
    toastTimer = setTimeout(() => {
      $("toast").hidden = true;
    }, 4500);
  }
  function progress(percent, label) {
    $("library-progress").setAttribute("aria-valuenow", String(percent));
    $("library-progress").firstElementChild.style.width = percent + "%";
    $("connection-status").textContent = label;
  }
  async function json(path, force) {
    const response = await fetch(path, {
      cache: force ? "no-store" : "default",
      credentials: "same-origin",
    });
    if (!response.ok)
      throw new Error(`Library request failed (${response.status})`);
    return response.json();
  }
  async function loadLibrary(force) {
    if (state.refreshing) return;
    state.refreshing = true;
    renderSettings();
    try {
      const meta = await json("data/meta.json", force);
      const version = "?v=" + encodeURIComponent(meta.build_id || "");
      const [channels, groups] = await Promise.all([
        json("data/channels.json" + version, force),
        json("data/groups.json" + version, force),
      ]);
      S.validateLibrary(meta, channels, groups);
      // Publish the pair together only after both pass validation.
      library = {
        meta,
        channels,
        groups,
        programmes: [],
        guideLoading: false,
        guideError: "",
      };
      programmeIndex = new Map();
      guidePromise = null;
      bugReport = null;
      recents = P.resolve(recents, channels).map(P.keyFor);
      rebuildEvents();
      renderCategories();
      renderGuideControls();
      $("channels-subtitle").textContent =
        `${number(channels.length)} channel feeds · ${groups.length} categories · Your favorites, guide and classics, without an install.`;
      $("footer-version").textContent = "· " + meta.web_version;
      progress(100, navigator.onLine ? "Library ready" : "Offline library");
      $("library-progress").hidden = true;
      lastRefresh = Date.now();
      lastRefreshMessage = `Web library loaded: ${number(channels.length)} feeds, ${groups.length} categories.`;
      if (force) toast("Library refreshed. Your favorites are kept.");
      // Noncritical shelves are independent: one unavailable extra must not
      // strand the channel browser behind a loading screen.
      const build = meta.build_id;
      json("data/vod.json?v=" + build, force)
        .then((doc) => {
          if (library.meta.build_id !== build) return;
          movies = Array.isArray(doc.items) ? doc.items : [];
          renderMovieFilters();
          if (state.tab === "movies") renderMovies();
        })
        .catch(() => {
          if (library.meta.build_id === build) {
            movies = [];
            if (state.tab === "movies") renderMovies();
          }
        });
      ensureGuide().catch(() => {});
    } catch (error) {
      lastRefreshMessage =
        error.message + " The previous usable library is kept.";
      $("connection-status").textContent = library.channels.length
        ? "Using cached library"
        : "Library unavailable";
      $("library-progress").hidden = true;
      if (!library.channels.length) {
        $("channels-subtitle").textContent = "The library could not load.";
        $("channel-grid").innerHTML =
          `<div class="empty-state"><h2>Let’s try that again.</h2><p>${esc(error.message)} Check your connection, or use the basic directory below.</p><button class="button primary" data-retry-library>Retry library</button> <a class="button quiet" href="directory.html">Channel directory</a></div>`;
      }
      if (force) toast(lastRefreshMessage);
    } finally {
      state.refreshing = false;
      renderSettings();
      if (current) renderPlayerMeta();
    }
  }
  function scheduleMap(doc) {
    const map = {};
    ((doc && doc.games) || []).forEach((game) => {
      const seconds = Date.parse(game.kickoff_utc || "") / 1000;
      if (game.key && Number.isFinite(seconds)) map[game.key] = seconds;
    });
    return map;
  }
  function rebuildEvents() {
    // Event extras are lazy; until they arrive, grouping works without them.
    const schedule = scheduleMap(library.meta.live_schedule);
    const sections = live.buildSections(library.channels, schedule);
    events = sections.flatMap((section) => section.events);
    eventIndex = new Map();
    sections.forEach((section) =>
      section.events.forEach((event) =>
        event.servers.forEach((server) => eventIndex.set(server.url, event)),
      ),
    );
    $("live-subtitle").textContent =
      `${events.length} matchups · ${sections.length} sports · ${events.reduce((n, e) => n + e.servers.length, 0)} listed feeds`;
    $("live-empty").hidden = events.length > 0;
    if (state.tab === "live") renderLive();
    json("data/events.json?v=" + library.meta.build_id)
      .then((doc) => {
        library.meta.live_schedule = doc.live_schedule;
        library.meta.team_logos = doc.team_logos;
        const mapped = scheduleMap(doc.live_schedule);
        const sections = live.buildSections(library.channels, mapped);
        events = sections.flatMap((s) => s.events);
        eventIndex = new Map();
        sections.forEach((s) =>
          s.events.forEach((e) =>
            e.servers.forEach((c) => eventIndex.set(c.url, e)),
          ),
        );
        if (state.tab === "live") renderLive();
      })
      .catch(() => {});
  }
  async function ensureGuide(force) {
    if (guidePromise && !force) return guidePromise;
    if (!library.meta.build_id) return;
    const build = library.meta.build_id;
    library.guideLoading = true;
    library.guideError = "";
    if (state.tab === "guide") renderGuide();
    guidePromise = json("data/epg.json?v=" + build, force)
      .then((rows) => {
        if (library.meta.build_id !== build) return;
        if (!Array.isArray(rows))
          throw new Error("The guide is not a valid programme list.");
        library.programmes = rows;
        programmeIndex = new Map();
        rows.forEach((p) => {
          if (!programmeIndex.has(p.c)) programmeIndex.set(p.c, []);
          programmeIndex.get(p.c).push(p);
        });
        library.guideLoading = false;
        if (state.tab === "guide") renderGuide();
        if (state.tab === "channels" && state.category) renderChannels();
        if (current) renderPlayerMeta();
      })
      .catch((error) => {
        if (library.meta.build_id !== build) return;
        library.guideLoading = false;
        library.guideError =
          "Listings are unavailable. Channels and playback are still usable.";
        if (state.tab === "guide") renderGuide();
        guidePromise = null;
      });
    return guidePromise;
  }
  function listings(channel) {
    return programmeIndex.get(channel.id) || [];
  }
  function onNow(channel, at) {
    const rows = listings(channel);
    return rows.find((p) => p.s <= at && p.e > at) || null;
  }
  function nextShow(channel, at) {
    return listings(channel).find((p) => p.s > at) || null;
  }
  function available() {
    return health.filterChannels(library.channels, dead);
  }
  function setTab(tab, updateHash) {
    if (!["channels", "live", "movies", "guide", "settings"].includes(tab))
      tab = "channels";
    state.tab = tab;
    document.querySelectorAll(".view").forEach((el) => {
      el.hidden = el.id !== "view-" + tab;
    });
    document.querySelectorAll("[data-tab]").forEach((el) => {
      const selected = el.dataset.tab === tab;
      el.setAttribute("aria-selected", String(selected));
      el.tabIndex = selected ? 0 : -1;
    });
    document
      .querySelectorAll("[data-shelf]")
      .forEach((el) =>
        el.classList.toggle(
          "active",
          tab === "channels" && el.dataset.shelf === state.shelf,
        ),
      );
    if (tab === "channels") renderChannels();
    if (tab === "live") renderLive();
    if (tab === "movies") renderMovies();
    if (tab === "guide") {
      ensureGuide();
      renderGuide();
    }
    if (tab === "settings") renderSettings();
    if (updateHash !== false) {
      try {
        history.replaceState(null, "", "#" + tab);
      } catch (_) {}
    }
  }
  function renderCategories() {
    renderChannels();
  }
  function channelMarkup(channel) {
    const key = P.keyFor(channel),
      favorite = P.isFavorite(favorites, key),
      now = onNow(channel, Date.now() / 1000);
    const logo = /^https:\/\//i.test(channel.logo || "") ? channel.logo : "";
    const quality = (channel.name.match(/\((\d{3,4}p)\)/) || [])[1] || "";
    return `<article class="channel-card${current && current.url === channel.url ? " playing" : ""}"><button class="channel-open" data-channel="${esc(key)}" aria-label="Watch ${esc(channel.name)}"><div class="channel-logo">${icon(channel.group)}${logo ? `<img src="${esc(logo)}" alt="" loading="lazy" referrerpolicy="no-referrer">` : ""}${quality ? `<span class="quality">${esc(quality)}</span>` : ""}</div><div class="channel-card-text"><h3>${esc(channel.name)}</h3><p>${esc(now ? now.t : channel.group || "Live channel")}</p></div></button><button class="favorite-button" data-favorite="${esc(key)}" aria-label="${favorite ? "Remove" : "Add"} ${esc(channel.name)} ${favorite ? "from" : "to"} favorites" aria-pressed="${favorite}">${favorite ? "★" : "☆"}</button></article>`;
  }
  function renderChannels() {
    const token = ++renderToken;
    let channels = available(),
      groups = library.groups;
    if (state.shelf)
      channels = P.resolve(
        state.shelf === "favorites" ? favorites : recents,
        channels,
      );
    if (state.category)
      channels = channels.filter((c) => c.group === state.category);
    if (state.query)
      channels = channels.filter((c) => S.matches(c, state.query));
    const browsing = !state.category && !state.shelf && !state.query;
    $("channels-heading").textContent =
      state.shelf === "favorites"
        ? "The channels you come back to."
        : state.shelf === "recent"
          ? "Pick up where you left off."
          : state.category || "Find your next watch.";
    $("channel-section-title").textContent = browsing
      ? "Browse by category"
      : state.shelf === "recent"
        ? "Recently watched"
        : "Channels";
    $("category-context").hidden = !state.category;
    $("category-count").textContent =
      `${channels.length} feeds in this category`;
    $("channel-result-count").textContent = browsing
      ? `${groups.length} categories`
      : `${number(channels.length)} feeds`;
    $("channel-sort").value = browsing ? state.sort : state.channelSort;
    $("channel-sort").querySelector("[value=big]").disabled = !browsing;
    $("channel-sort").querySelector("[value=number]").disabled = browsing;
    $("channel-empty").hidden = browsing
      ? groups.length > 0
      : channels.length > 0;
    $("channel-more").hidden = browsing || channels.length <= state.limit;
    $("channel-grid").setAttribute("aria-busy", "false");
    if (browsing) {
      $("channel-grid").innerHTML = S.sortGroups(groups, state.sort)
        .map(
          (group) =>
            `<button class="category-card" data-category="${esc(group.name)}"><span class="category-art">${icon(group.name)}</span><span><h3>${esc(group.name.replace(/_/g, " "))}</h3><p>${number(group.count)} channels</p></span><span class="category-arrow" aria-hidden="true">›</span></button>`,
        )
        .join("");
    } else {
      const ordered =
        state.shelf === "recent" && state.channelSort === "published"
          ? channels
          : S.sortChannels(
              channels,
              state.channelSort === "big" ? "published" : state.channelSort,
            );
      $("channel-grid").innerHTML = ordered
        .slice(0, state.limit)
        .map(channelMarkup)
        .join("");
      if (channels.length > state.limit)
        $("channel-more").textContent =
          `Load more · ${channels.length - state.limit} remaining`;
    }
    $("favorite-count").textContent = favorites.length;
    document
      .querySelectorAll("[data-shelf]")
      .forEach((el) =>
        el.classList.toggle(
          "active",
          state.tab === "channels" && el.dataset.shelf === state.shelf,
        ),
      );
  }
  function chooseCategory(name) {
    state.category = name;
    state.shelf = "";
    state.query = "";
    state.channelSort = "published";
    state.limit = 60;
    $("channel-search").value = "";
    setTab("channels");
    window.scrollTo(0, 0);
  }
  function chooseShelf(shelf) {
    state.shelf = shelf;
    state.category = "";
    state.query = "";
    state.limit = 60;
    $("channel-search").value = "";
    setTab("channels");
    window.scrollTo(0, 0);
  }
  function renderLive() {
    const schedule = scheduleMap(library.meta.live_schedule);
    const sections = live.buildSections(available(), schedule);
    $("live-empty").hidden = sections.length > 0;
    $("live-grid").innerHTML = sections
      .map(
        (section) =>
          `<section class="event-section"><h2>${esc(section.sport)} <span class="muted small">· ${section.events.length}</span></h2><div class="event-grid">${section.events
            .map((event) => {
              const upcoming = event.kickoffMs > Date.now();
              const teams = live.teamsOf(event.title) || [event.title, ""];
              const crest = (name) => {
                const colors = live.crestColorsFor(name);
                const logoDoc = library.meta.team_logos || {};
                const logo = live.teamLogoUrl(
                  { team_logos: logoDoc.logos || logoDoc },
                  name,
                );
                return `<span class="team-crest" style="background:linear-gradient(145deg,${colors[0]},${colors[1]})">${esc(live.initialsFor(name))}${logo && /^https:\/\//.test(logo) ? `<img class="team-crest-img" src="${esc(logo)}" alt="" loading="lazy" referrerpolicy="no-referrer">` : ""}</span>`;
              };
              return `<article class="event-card"><div class="event-status${upcoming ? " upcoming" : ""}">${upcoming ? "UPCOMING" : "LISTED FEED · NOT PRE-CHECKED"}</div><div class="event-teams"><div class="team">${crest(teams[0])}<strong>${esc(teams[0])}</strong></div><span class="versus">VS</span><div class="team">${crest(teams[1])}<strong>${esc(teams[1])}</strong></div></div><p class="event-kickoff" data-kickoff="${event.kickoffMs || ""}">${event.kickoffMs ? esc((upcoming ? "Starts in " + live.countdownText((event.kickoffMs - Date.now()) / 1000) + " · " : "Listed kickoff ") + new Date(event.kickoffMs).toLocaleString([], { month: "short", day: "numeric", hour: "numeric", minute: "2-digit" })) : "Kickoff time not listed"} · ${event.servers.length} server${event.servers.length === 1 ? "" : "s"}</p><button class="button" data-event="${esc(event.key)}">▶ Try this matchup</button></article>`;
            })
            .join("")}</div></section>`,
      )
      .join("");
  }
  function movieDetail(item) {
    return [
      item.year || "",
      item.genre,
      item.runtime_seconds
        ? Math.round(item.runtime_seconds / 60) + " min"
        : "",
    ]
      .filter(Boolean)
      .join(" · ");
  }
  function movieLabel(item) {
    return item.kind === "movie"
      ? "FILM"
      : item.season
        ? `S${item.season}${item.episode ? " E" + item.episode : ""}`
        : "EPISODE";
  }
  function renderMovieFilters() {
    const genres = [
      "All",
      ...new Set(movies.map((m) => m.genre).filter(Boolean)),
    ];
    $("movie-genres").innerHTML = genres
      .map(
        (genre) =>
          `<button data-genre="${esc(genre)}" aria-pressed="${genre === state.genre}">${esc(genre)}</button>`,
      )
      .join("");
  }
  function renderMovies() {
    const query = S.normalize(state.movieQuery);
    const items = movies.filter(
      (m) =>
        (state.kind === "all" || m.kind === state.kind) &&
        (state.genre === "All" || m.genre === state.genre) &&
        S.normalize([m.title, m.show, m.genre, m.summary].join(" ")).includes(
          query,
        ),
    );
    $("movies-subtitle").textContent =
      `${movies.length} on-demand titles · Public-domain classics · Resume on this browser`;
    $("movie-empty").hidden = items.length > 0;
    $("movie-grid").innerHTML = items
      .map((item) => {
        const at = S.resumeAt(S.positions()[item.id], item.runtime_seconds);
        return `<article class="movie-card"><button class="movie-poster" data-movie="${esc(item.id)}" aria-label="${at ? "Resume" : "Play"} ${esc(item.title)}">${icon("movie")}${/^https:\/\//.test(item.poster || "") || item.test_card ? `<img src="${esc(item.poster)}" alt="" loading="lazy" referrerpolicy="no-referrer">` : ""}<span class="movie-kind">${esc(movieLabel(item))}</span></button><h3>${esc(item.title)}</h3><p>${esc(movieDetail(item))}</p>${at ? `<div class="resume-track" aria-label="Resume at ${mediaClock(at)}"><span style="width:${Math.min(100, (at / item.runtime_seconds) * 100)}%"></span></div><p class="small muted">Resume at ${mediaClock(at)}</p>` : ""}</article>`;
      })
      .join("");
    $("movie-kind")
      .querySelectorAll("button")
      .forEach((b) =>
        b.setAttribute("aria-pressed", String(b.dataset.kind === state.kind)),
      );
    $("movie-genres")
      .querySelectorAll("button")
      .forEach((b) =>
        b.setAttribute("aria-pressed", String(b.dataset.genre === state.genre)),
      );
  }
  function renderGuideControls() {
    $("guide-category").innerHTML =
      '<option value="">All categories</option>' +
      library.groups
        .map((g) => `<option value="${esc(g.name)}">${esc(g.name)}</option>`)
        .join("");
  }
  function renderGuide() {
    const at = Date.now() / 1000,
      query = S.normalize(state.guideQuery);
    const channels = available().filter(
      (c) =>
        (!state.guideCategory || c.group === state.guideCategory) &&
        (!query || S.normalize(c.name).includes(query)) &&
        listings(c).some((p) => p.e > at),
    );
    $("guide-subtitle").textContent = library.guideLoading
      ? "Loading the guide in the background…"
      : `${number(library.programmes.length)} listings · ${programmeIndex.size} channels with guide data · Times in your local timezone`;
    $("guide-notice").hidden = !library.guideError && !library.guideLoading;
    $("guide-notice").textContent =
      library.guideError ||
      "Loading real programme listings. You can keep browsing channels.";
    $("guide-empty").hidden = channels.length > 0 || library.guideLoading;
    $("guide-more").hidden = channels.length <= state.guideLimit;
    document
      .querySelectorAll("[data-guide-layout]")
      .forEach((b) =>
        b.setAttribute(
          "aria-pressed",
          String(b.dataset.guideLayout === state.guideLayout),
        ),
      );
    const visible = channels.slice(0, state.guideLimit);
    if (state.guideLayout === "list") {
      $("guide-grid").className = "guide-list";
      $("guide-grid").innerHTML = visible
        .map((channel) => {
          const now = onNow(channel, at),
            next = nextShow(channel, at);
          const pct = now
            ? Math.max(0, Math.min(100, ((at - now.s) / (now.e - now.s)) * 100))
            : 0;
          return `<article class="guide-channel"><div class="guide-logo">${icon(channel.group)}${/^https:\/\//.test(channel.logo || "") ? `<img src="${esc(channel.logo)}" alt="" loading="lazy" referrerpolicy="no-referrer">` : ""}</div><div class="guide-content"><h3>${esc(channel.name)}</h3><p>${esc(now ? now.t : "No current listing")}</p>${now ? `<div class="guide-progress"><span style="width:${pct}%"></span></div>` : ""}<p class="guide-next">${next ? "Next · " + clock(next.s) + " · " + esc(next.t) : "Nothing next listed"}</p></div><span class="guide-time">${now ? clock(now.s) + " – " + clock(now.e) : ""}</span><button class="button quiet small" data-channel="${esc(P.keyFor(channel))}" aria-label="Watch ${esc(channel.name)}">▶ Watch</button></article>`;
        })
        .join("");
    } else {
      const start = Math.floor(at / 1800) * 1800,
        end = start + 6 * 3600,
        width = 900;
      const hours = Array.from(
        { length: 12 },
        (_, i) =>
          `<span style="left:${i * 75}px">${clock(start + i * 1800)}</span>`,
      ).join("");
      $("guide-grid").className = "timeline-scroll";
      $("guide-grid").innerHTML =
        `<div class="timeline-inner"><div class="timeline-header"><div class="timeline-label">Channel / local time</div><div class="timeline-hours">${hours}</div></div>${visible
          .map(
            (channel) =>
              `<div class="timeline-row"><div class="timeline-label">${esc(channel.name)}</div><div class="timeline-track">${listings(
                channel,
              )
                .filter((p) => p.e > start && p.s < end)
                .map(
                  (p) =>
                    `<button class="timeline-program" style="left:${Math.max(0, ((p.s - start) / (end - start)) * width)}px;width:${Math.max(8, ((Math.min(p.e, end) - Math.max(p.s, start)) / (end - start)) * width - 3)}px" data-channel="${esc(P.keyFor(channel))}" title="${esc(p.t + " · " + clock(p.s))}"><strong>${esc(p.t)}</strong><span>${clock(p.s)} · ${Math.round((p.e - p.s) / 60)} min</span></button>`,
                )
                .join("")}</div></div>`,
          )
          .join(
            "",
          )}<div class="timeline-now" style="left:${180 + ((at - start) / (end - start)) * width}px;top:40px"></div></div>`;
    }
  }
  function renderSettings() {
    if (!document.getElementById("settings-body")) return;
    const meta = library.meta;
    $("settings-body").innerHTML =
      `<div class="panel"><div class="settings-version"><div><p class="eyebrow">INDEPENDENT WEB EDITION</p><h2>PremiumTV Web ${esc(meta.web_version || "0.1.0")}</h2></div><span class="outline-badge" style="display:inline">${esc((meta.library_scope || "usa").toUpperCase())} LIBRARY</span></div><div class="settings-stats"><div><strong>${number(library.channels.length)}</strong><span>channel feeds</span></div><div><strong>${library.groups.length}</strong><span>categories</span></div><div><strong>${programmeIndex.size || meta.guide_channels || "—"}</strong><span>channels with guide</span></div><div><strong>${movies.length || (meta.vod_catalog && meta.vod_catalog.items.length) || "—"}</strong><span>films &amp; episodes</span></div></div><p>Library built ${esc(meta.generated_utc || "unknown")} · Library data ${esc(meta.version || "")}<br>${esc(lastRefreshMessage)}</p><div class="button-row"><button id="force-refresh" class="button primary" ${state.refreshing ? "disabled" : ""}>${state.refreshing ? "Refreshing…" : "Refresh library"}</button><button id="check-bugs" class="button">Check for bugs</button><button id="settings-install" class="button quiet">Add to home screen</button></div><p class="small muted" style="margin-top:15px;margin-bottom:0">The web edition updates when its site is deployed. It never downloads APKs, DMGs or native-app updates.</p></div>
      ${bugReport ? `<div class="panel"><h2>${bugReport.fail ? bugReport.fail + " blocking issues" : "No blocking issues"} · ${bugReport.warn} browser warnings</h2><ul class="bug-list">${bugReport.checks.map((c) => `<li><span class="${c.status}">${c.status === "ok" ? "✓" : c.status === "warn" ? "!" : "×"}</span><strong>${esc(c.label)}</strong><span>${esc(c.detail)}</span></li>`).join("")}</ul><p class="small muted">Read-only library and browser checks. Stream availability is verified only by opening a feed.</p></div>` : ""}
      <div class="panel"><h2>Playback &amp; personal library</h2><div class="settings-row"><div><strong>Sleep timer</strong><p id="sleep-description">${sleepDeadline > Date.now() ? "Stops playback in " + S.sleepLabel(S.sleepRemaining(sleepDeadline, Date.now())) : "Stop playback after 30, 60 or 90 minutes."}</p></div><select id="sleep-timer" aria-label="Sleep timer"><option value="0">Off</option><option value="30">30 minutes</option><option value="60">1 hour</option><option value="90">1 hour 30 minutes</option></select></div><div class="settings-row"><div><strong>Hidden channels</strong><p>Feeds that fail on every server are hidden on this browser for seven days.</p></div><button id="restore-hidden" class="button quiet" ${dead.size ? "" : "disabled"}>Restore ${dead.size} hidden</button></div><div class="settings-row"><div><strong>Favorites &amp; history</strong><p>${favorites.length} favorites · ${recents.length} recently watched. Stored only in this browser.</p></div><button id="clear-personal" class="button quiet danger">Clear personal data</button></div></div>
      <div class="panel"><h2>Made for the browser</h2><p>No installation required. iPhone and iPad use native HLS playback; Chrome, Edge and Firefox use Media Source Extensions when available. Films use native MP4 playback.</p><div class="info-strip"><span>${icon("info")}</span><p>Some provider feeds need custom headers, block cross-origin requests, use HTTP, or carry AC-3/DTS audio your browser cannot decode. The native apps can handle more of these cases. The web player tries backups and explains failures instead of bypassing browser security.</p></div><div class="button-row"><a class="button quiet" href="data/PremiumTV.m3u" download>Download M3U</a><a class="button quiet" href="../#apps">Get the native apps ↗</a><button id="reload-app" class="button quiet">Reload web app</button></div></div>
      <details class="panel"><summary>Library sources &amp; privacy</summary><dl class="settings-meta"><dt>Playlist</dt><dd>${esc(meta.playlist || "playlists/live/USA.m3u")}</dd><dt>Guide</dt><dd>${esc(meta.guide || "EPG/USA.xml")}</dd><dt>Web build</dt><dd>${esc(meta.build_id || "loading")}</dd><dt>Last library load</dt><dd>${lastRefresh ? esc(new Date(lastRefresh).toLocaleString()) : "Not loaded"}</dd><dt>Storage</dt><dd>${S.persistent ? "Available on this browser" : "Session only — browser storage is blocked"}</dd><dt>Account / analytics</dt><dd>None. No sign-in, tracking, or uploaded viewing history.</dd><dt>Third-party requests</dt><dd>Channel logos, stream providers and Internet Archive receive normal network requests when you browse or play. No viewing data is sent to PremiumTV.</dd></dl><p>The offline cache contains the public app and library, not live video. Clear personal data above to reset favorites, history and resume positions.</p></details>`;
    $("force-refresh").onclick = () => loadLibrary(true);
    $("check-bugs").onclick = () => {
      bugReport = window.PremiumDiagnostics.check(
        library,
        {
          nativeHls: player.nativeHls(),
          mse: Boolean(window.MediaSource),
          storage: S.persistent,
          serviceWorker: "serviceWorker" in navigator && window.isSecureContext,
          online: navigator.onLine,
        },
        Date.now(),
      );
      renderSettings();
    };
    $("settings-install").onclick = installApp;
    $("restore-hidden").onclick = () => {
      dead = health.clear(S.storage);
      renderChannels();
      renderSettings();
      toast("Hidden channels restored.");
    };
    $("clear-personal").onclick = () => {
      if (
        !window.confirm(
          "Clear favorites, recently watched, resume positions and hidden-channel history on this browser?",
        )
      )
        return;
      favorites = [];
      recents = [];
      dead = new Set();
      [P.FAVORITES_KEY, P.RECENTS_KEY, S.KEYS.positions, health.KEY].forEach(
        (k) => S.storage.removeItem(k),
      );
      renderChannels();
      renderMovies();
      renderSettings();
      toast("Personal data cleared.");
    };
    $("sleep-timer").onchange = (event) => {
      const minutes = Number(event.target.value);
      sleepDeadline = minutes ? Date.now() + minutes * 60000 : 0;
      S.write(S.KEYS.sleep, sleepDeadline);
      renderSettings();
      toast(
        minutes
          ? `Sleep timer set for ${minutes} minutes.`
          : "Sleep timer off.",
      );
    };
    $("reload-app").onclick = async () => {
      if (
        current &&
        !confirm("Reload the web app and stop the current stream?")
      )
        return;
      player.stop();
      if ("caches" in window) {
        try {
          const keys = await caches.keys();
          await Promise.all(
            keys
              .filter((k) => k.startsWith("premiumtv-web-"))
              .map((k) => caches.delete(k)),
          );
        } catch (_) {}
      }
      location.reload();
    };
  }
  function serversFor(channel) {
    const event = eventIndex.get(channel.url);
    if (event)
      return [channel].concat(
        event.servers.filter((c) => c.url !== channel.url),
      );
    // Build the backup index once rather than re-group all events per server hop.
    if (!serversFor.index || serversFor.source !== library.channels) {
      serversFor.source = library.channels;
      serversFor.index = new Map();
      library.channels.forEach((c) => {
        const key = c.id + "|" + live.baseDisplayName(c.name);
        if (!serversFor.index.has(key)) serversFor.index.set(key, []);
        serversFor.index.get(key).push(c);
      });
    }
    const pool = serversFor.index.get(
      channel.id + "|" + live.baseDisplayName(channel.name),
    ) || [channel];
    return [channel].concat(pool.filter((c) => c.id && c.url !== channel.url));
  }
  function openPlayer(channel, servers) {
    if (!channel) return;
    current = channel;
    queue = (servers || serversFor(channel)).filter(
      (c, i, list) => list.findIndex((x) => x.url === c.url) === i,
    );
    serverIndex = 0;
    $("player").hidden = false;
    $("player-error").hidden = true;
    document.body.classList.add("has-mini-player");
    if (!expanded) minimizePlayer();
    if (!channel.vod) {
      recents = P.recordRecent(recents, P.keyFor(channel));
      P.save(S.storage, P.RECENTS_KEY, recents);
    }
    renderPlayerMeta();
    playServer();
    renderChannels();
  }
  function playServer() {
    if (!queue.length) return;
    const source = queue[serverIndex];
    current = source;
    playerSerial++;
    lastProgressSave = 0;
    $("player-error").hidden = true;
    $("player-loading").hidden = false;
    renderPlayerMeta();
    const restricted = source.ua || source.referrer || source.origin;
    $("player-browser-note").hidden =
      !restricted && !source.url.startsWith("http:");
    $("player-browser-note").textContent = restricted
      ? "This feed requests custom headers that browsers cannot send. It may require the native app."
      : "HTTP feed: your browser may block it on this secure page.";
    player.play(source.url, source.url, source, {
      onFatal: () => advanceServer(true),
      onState: (info) => {
        if (info.started && current && !current.vod && dead.has(current.url)) {
          dead = health.clear(S.storage);
          renderChannels();
        }
        if (info.silent) {
          toast("No decodable audio detected. Trying the next server…");
          advanceServer(true);
        }
        if (info.ended && current && current.vod) {
          const value = S.positions();
          delete value[current.id];
          S.write(S.KEYS.positions, value);
        }
        syncTransport(info);
      },
      onProgress: (seconds, duration) => {
        if (current && current.vod && Date.now() - lastProgressSave > 4000) {
          S.savePosition(current.id, seconds, duration);
          lastProgressSave = Date.now();
        }
        syncTransport();
      },
    });
  }
  function advanceServer(auto) {
    if (!queue.length) return;
    if (auto && serverIndex + 1 >= queue.length) {
      if (!current.vod) {
        queue.forEach((c) => {
          dead = health.record(S.storage, c.url);
        });
        renderChannels();
      }
      player.fail(
        "Every listed server failed in this browser. The provider may be offline or block browser playback. Try again later, restore hidden channels in Settings, or use the native app.",
      );
      toast(
        current.vod
          ? "No movie server could play."
          : "All servers failed. Channel hidden for seven days; restore it in Settings.",
      );
      return;
    }
    serverIndex = P.nextServerIndex(serverIndex, queue.length, 1);
    if (auto) toast(`Trying server ${serverIndex + 1} of ${queue.length}…`);
    playServer();
  }
  function renderPlayerMeta() {
    if (!current) return;
    $("player-name").textContent = current.name;
    $("player-detail").textContent = current.vod
      ? current.vodDetail || "On demand"
      : [current.group, current.country].filter(Boolean).join(" · ");
    $("player-server").textContent =
      `Server ${serverIndex + 1} / ${queue.length}`;
    $("player-prev").disabled =
      $("player-next").disabled =
      $("player-next-error").disabled =
        queue.length < 2;
    $("player-original").href = /^https?:\/\//i.test(current.url)
      ? current.url
      : "#";
    $("player-favorite").hidden = Boolean(current.vod);
    const fav = P.isFavorite(favorites, P.keyFor(current));
    $("player-favorite").textContent = fav ? "★" : "☆";
    $("player-favorite").setAttribute("aria-pressed", String(fav));
    $("player-favorite").setAttribute(
      "aria-label",
      fav ? "Remove from favorites" : "Add to favorites",
    );
    const now = onNow(current, Date.now() / 1000),
      next = nextShow(current, Date.now() / 1000);
    $("player-now").textContent = current.vod
      ? current.vodSummary || ""
      : now
        ? "Now · " + now.t
        : "Live channel · No current listing";
    $("player-next").textContent = next
      ? "Next · " + clock(next.s) + " · " + next.t
      : "";
    $("player-mode-label").textContent = current.vod
      ? "ON DEMAND"
      : "LIVE TV · WEB PLAYER";
  }
  function syncTransport(info) {
    if (!current) return;
    const video = player.element,
      finite = Boolean(
        current.vod && Number.isFinite(video.duration) && video.duration > 0,
      );
    document.querySelectorAll(".transport-vod").forEach((el) => {
      el.hidden = !finite;
    });
    document.querySelectorAll(".transport-live").forEach((el) => {
      el.hidden = finite;
    });
    $("player-toggle").textContent = video.paused ? "▶" : "❚❚";
    $("player-toggle").setAttribute(
      "aria-label",
      video.paused ? "Play" : "Pause",
    );
    $("player-mute").textContent = video.muted ? "🔇" : "🔊";
    $("player-mute").setAttribute(
      "aria-label",
      video.muted ? "Unmute" : "Mute",
    );
    if (document.activeElement !== $("player-volume"))
      $("player-volume").value = Math.round(video.volume * 100);
    if (finite) {
      if (document.activeElement !== $("player-seek"))
        $("player-seek").value =
          Math.round((video.currentTime / video.duration) * 1000) || 0;
      $("player-time").textContent =
        mediaClock(video.currentTime) + " / " + mediaClock(video.duration);
    }
    const tracks = player.audioTracks();
    $("player-audio").hidden = tracks.length < 2;
    const signature = tracks.map((t) => t.label + t.selected).join("|");
    if ($("player-audio").dataset.signature !== signature) {
      $("player-audio").innerHTML = tracks
        .map(
          (t) =>
            `<option value="${t.index}"${t.selected ? " selected" : ""}>${esc(t.label)}</option>`,
        )
        .join("");
      $("player-audio").dataset.signature = signature;
    }
    $("player-pip").hidden = !(
      document.pictureInPictureEnabled || video.webkitSupportsPresentationMode
    );
  }
  function minimizePlayer() {
    expanded = false;
    $("player").className = "player mini";
    document.body.classList.remove("player-expanded");
    $("player-minimize").textContent = "Expand player";
    $("player-expand-picture").hidden = true;
  }
  function expandPlayer() {
    expanded = true;
    $("player").className = "player expanded";
    document.body.classList.add("player-expanded");
    $("player-minimize").textContent = "Browse while watching";
    $("player-expand-picture").hidden = false;
    $("player-minimize").focus({ preventScroll: true });
  }
  function saveCurrentProgress() {
    if (current && current.vod)
      S.savePosition(
        current.id,
        player.element.currentTime,
        player.element.duration,
      );
  }
  function closePlayer() {
    saveCurrentProgress();
    playerSerial++;
    player.stop();
    $("player").hidden = true;
    current = null;
    queue = [];
    expanded = false;
    document.body.classList.remove("player-expanded", "has-mini-player");
    if (document.fullscreenElement) document.exitFullscreen().catch(() => {});
    renderChannels();
    if (state.tab === "movies") renderMovies();
  }
  async function fullscreen() {
    const video = player.element;
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if ($("player").requestFullscreen)
        await $("player").requestFullscreen();
      else if (video.webkitEnterFullscreen) video.webkitEnterFullscreen();
      else {
        expandPlayer();
        toast(
          "Full-screen layout enabled. Native full screen is not available in this browser.",
        );
      }
    } catch (_) {
      expandPlayer();
      toast("Using the full-window player.");
    }
  }
  function toggleFavorite(key) {
    if (!key) return;
    favorites = P.toggleFavorite(favorites, key);
    P.save(S.storage, P.FAVORITES_KEY, favorites);
    renderChannels();
    renderPlayerMeta();
  }
  function watchKey(key) {
    const channel = library.channels.find((c) => P.keyFor(c) === key);
    if (channel) openPlayer(channel);
  }
  function watchMovie(id) {
    const item = movies.find((m) => m.id === id);
    if (!item) return;
    const urls = [
      ...new Set(
        (item.streams && item.streams.length
          ? item.streams
          : [item.stream]
        ).filter(Boolean),
      ),
    ];
    const resume = S.resumeAt(S.positions()[id], item.runtime_seconds);
    const servers = urls.map((url) => ({
      id: item.id,
      name:
        item.kind === "episode"
          ? `${item.show || item.title} · ${movieLabel(item)}`
          : item.title,
      url,
      group: item.kind === "movie" ? "Movies" : "TV Shows",
      country: "US",
      logo: item.poster,
      vod: true,
      vodDetail: movieDetail(item),
      vodSummary: item.summary,
      resume,
    }));
    if (servers.length) openPlayer(servers[0], servers);
  }
  async function installApp() {
    if (installPrompt) {
      try {
        await installPrompt.prompt();
        await installPrompt.userChoice;
        installPrompt = null;
        $("install-button").hidden = true;
      } catch (_) {}
    } else if ($("install-dialog").showModal) $("install-dialog").showModal();
    else toast("Use your browser menu → Add to Home Screen.");
  }
  function connectionChanged() {
    $("offline-banner").hidden = navigator.onLine;
    $("connection-status").textContent = navigator.onLine
      ? "Library ready"
      : "Offline library";
    if (!navigator.onLine && current)
      toast("Connection lost. Cached browsing is still available.");
  }
  function checkSleep() {
    if (sleepDeadline && Date.now() >= sleepDeadline) {
      sleepDeadline = 0;
      S.write(S.KEYS.sleep, 0);
      if (current) closePlayer();
      if (state.tab === "settings") renderSettings();
      toast("Sleep timer finished. Playback stopped.");
    } else if (
      state.tab === "settings" &&
      $("sleep-description") &&
      sleepDeadline
    )
      $("sleep-description").textContent =
        "Stops playback in " +
        S.sleepLabel(S.sleepRemaining(sleepDeadline, Date.now()));
  }

  initializeIcons();
  document.addEventListener("click", (event) => {
    const button = event.target.closest("button, a");
    if (!button) return;
    if (button.dataset.tab) setTab(button.dataset.tab);
    if (button.dataset.go) setTab(button.dataset.go);
    if (button.dataset.category) chooseCategory(button.dataset.category);
    if (button.dataset.shelf) chooseShelf(button.dataset.shelf);
    if (button.dataset.channel) watchKey(button.dataset.channel);
    if (button.dataset.favorite) toggleFavorite(button.dataset.favorite);
    if (button.dataset.event) {
      const item = events.find((e) => e.key === button.dataset.event);
      if (item) openPlayer(item.servers[0], item.servers);
    }
    if (button.dataset.movie) watchMovie(button.dataset.movie);
    if (button.dataset.kind) {
      state.kind = button.dataset.kind;
      renderMovies();
    }
    if (button.dataset.genre) {
      state.genre = button.dataset.genre;
      renderMovies();
    }
    if (button.dataset.guideLayout) {
      state.guideLayout = button.dataset.guideLayout;
      renderGuide();
    }
    if (button.hasAttribute("data-retry-library")) loadLibrary(true);
    if (button.hasAttribute("data-close-dialog")) $("install-dialog").close();
  });
  // Replace remote logo failures with the existing category artwork, not a
  // broken-image glyph. Capture handles image errors without inline handlers.
  document.addEventListener(
    "error",
    (event) => {
      if (event.target.tagName === "IMG") event.target.hidden = true;
    },
    true,
  );
  $("channel-search").addEventListener("input", (event) => {
    clearTimeout(searchTimer);
    const value = event.target.value;
    searchTimer = setTimeout(() => {
      state.query = value;
      state.shelf = "";
      state.category = "";
      state.limit = 60;
      renderChannels();
    }, 150);
  });
  $("channel-sort").onchange = (event) => {
    if (!state.category && !state.shelf && !state.query)
      state.sort = event.target.value;
    else state.channelSort = event.target.value;
    renderChannels();
  };
  $("category-back").onclick = () => chooseCategory("");
  $("clear-search").onclick = () => {
    state.query = "";
    state.shelf = "";
    state.category = "";
    $("channel-search").value = "";
    renderChannels();
  };
  $("channel-more").onclick = () => {
    state.limit += 60;
    renderChannels();
  };
  $("guide-more").onclick = () => {
    state.guideLimit += 40;
    renderGuide();
  };
  $("guide-search").oninput = (event) => {
    state.guideQuery = event.target.value;
    state.guideLimit = 40;
    renderGuide();
  };
  $("guide-category").onchange = (event) => {
    state.guideCategory = event.target.value;
    state.guideLimit = 40;
    renderGuide();
  };
  $("movie-search").oninput = (event) => {
    state.movieQuery = event.target.value;
    renderMovies();
  };
  $("clear-movies").onclick = () => {
    state.movieQuery = "";
    state.kind = "all";
    state.genre = "All";
    $("movie-search").value = "";
    renderMovies();
  };
  $("refresh-events").onclick = () => loadLibrary(true);
  $("player-close").onclick = closePlayer;
  $("player-toggle").onclick = () => player.toggle();
  $("gesture-play").onclick = () => player.resumeGesture();
  $("player-mute").onclick = () => player.mute();
  $("player-volume").oninput = (event) =>
    player.volume(Number(event.target.value) / 100);
  $("player-seek").oninput = (event) => {
    if (Number.isFinite(player.element.duration))
      player.seek(
        (Number(event.target.value) / 1000) * player.element.duration,
      );
  };
  $("player-back").onclick = () => player.skip(-10);
  $("player-forward").onclick = () => player.skip(10);
  $("player-live").onclick = () => player.goLive();
  $("player-prev").onclick = () => {
    saveCurrentProgress();
    serverIndex = P.nextServerIndex(serverIndex, queue.length, -1);
    playServer();
  };
  $("player-next").onclick = $("player-next-error").onclick = () =>
    advanceServer(false);
  $("player-retry").onclick = () => {
    $("player-error").hidden = true;
    playServer();
  };
  $("player-favorite").onclick = () => toggleFavorite(P.keyFor(current));
  $("player-minimize").onclick = () =>
    expanded ? minimizePlayer() : expandPlayer();
  $("player-expand-picture").onclick = () =>
    player.element.paused ? player.toggle() : minimizePlayer();
  $("player-fullscreen").onclick = fullscreen;
  $("player-audio").onchange = (event) =>
    player.setAudio(Number(event.target.value));
  $("player-pip").onclick = async () => {
    try {
      if (document.pictureInPictureElement)
        await document.exitPictureInPicture();
      else if (player.element.requestPictureInPicture)
        await player.element.requestPictureInPicture();
      else if (player.element.webkitSetPresentationMode)
        player.element.webkitSetPresentationMode("picture-in-picture");
    } catch (_) {
      toast("Picture in picture is not available for this feed.");
    }
  };
  $("player-airplay").onclick = () => {
    try {
      player.element.webkitShowPlaybackTargetPicker();
    } catch (_) {
      toast("AirPlay is not available on this device.");
    }
  };
  player.element.addEventListener(
    "webkitplaybacktargetavailabilitychanged",
    (event) => {
      $("player-airplay").hidden = event.availability !== "available";
    },
  );
  $("install-button").onclick = installApp;
  window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    installPrompt = event;
    $("install-button").hidden = false;
  });
  window.addEventListener("appinstalled", () => {
    $("install-button").hidden = true;
    toast("PremiumTV added to your device.");
  });
  document
    .querySelector(".nav-primary")
    .addEventListener("keydown", (event) => {
      if (
        ![
          "ArrowRight",
          "ArrowLeft",
          "ArrowDown",
          "ArrowUp",
          "Home",
          "End",
        ].includes(event.key)
      )
        return;
      const tabs = Array.from(document.querySelectorAll("[data-tab]"));
      const index = tabs.indexOf(document.activeElement);
      if (index < 0) return;
      event.preventDefault();
      const next =
        event.key === "Home"
          ? 0
          : event.key === "End"
            ? tabs.length - 1
            : (index +
                (event.key === "ArrowRight" || event.key === "ArrowDown"
                  ? 1
                  : -1) +
                tabs.length) %
              tabs.length;
      setTab(tabs[next].dataset.tab);
      tabs[next].focus();
    });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && current && !$("install-dialog").open) {
      if (expanded) minimizePlayer();
      else closePlayer();
      return;
    }
    if (
      /INPUT|SELECT|TEXTAREA|BUTTON/.test(event.target.tagName) ||
      event.target.isContentEditable ||
      event.ctrlKey ||
      event.metaKey ||
      event.altKey
    )
      return;
    if (event.key === "/") {
      event.preventDefault();
      setTab("channels");
      $("channel-search").focus();
    }
    if (current && event.code === "Space") {
      event.preventDefault();
      player.toggle();
    }
    if (current && event.key.toLowerCase() === "m") player.mute();
    if (current && event.key.toLowerCase() === "f") fullscreen();
  });
  window.addEventListener("online", connectionChanged);
  window.addEventListener("offline", connectionChanged);
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) {
      checkSleep();
      connectionChanged();
    }
  });
  window.addEventListener("pagehide", () => {
    saveCurrentProgress();
    closePlayer();
  });
  window.addEventListener("hashchange", () =>
    setTab(location.hash.slice(1), false),
  );
  const sleepInterval = setInterval(checkSleep, 1000);
  const eventInterval = setInterval(() => {
    if (!document.hidden && state.tab === "live") {
      document.querySelectorAll("[data-kickoff]").forEach((el) => {
        const at = Number(el.dataset.kickoff);
        if (!at) return;
        const remaining = at - Date.now();
        if (remaining <= 0) {
          renderLive();
          return;
        }
        el.textContent =
          "Starts in " +
          live.countdownText(remaining / 1000) +
          " · " +
          new Date(at).toLocaleString([], {
            month: "short",
            day: "numeric",
            hour: "numeric",
            minute: "2-digit",
          });
      });
    }
  }, 1000);
  const guideInterval = setInterval(() => {
    if (!document.hidden && !current && state.tab === "guide") renderGuide();
  }, 60000);
  window.addEventListener("beforeunload", () => {
    clearInterval(sleepInterval);
    clearInterval(guideInterval);
    clearInterval(eventInterval);
  });
  if ("serviceWorker" in navigator && window.isSecureContext)
    navigator.serviceWorker.register("sw.js").catch(() => {});
  setTab(location.hash.slice(1) || "channels", false);
  connectionChanged();
  checkSleep();
  renderSettings();
  loadLibrary(false);
})();
