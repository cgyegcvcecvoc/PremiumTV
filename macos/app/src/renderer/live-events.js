'use strict';

/**
 * Live games and multi-server playback.
 *
 * The repository's scrapers publish game streams as ordinary playlist
 * entries named "[Sport] Team A vs. Team B | English (SOURCE)". They share
 * placeholder EPG ids ("Football.Dummy.us"), so everything the app can tell
 * a viewer about them lives in the name itself: the sport, the matchup and -
 * when the same game is published more than once - extra servers to fall
 * back to when one feed dies mid-game.
 *
 * Kept in its own file (like player.js) so the parsing and the server
 * grouping can be unit tested in a VM without the rest of the renderer.
 */

window.PremiumLive = (function () {
  const BRACKET_TAG = /^\[([^\]]{2,48})]\s*(.*)$/;
  const VERSUS = /\s+vs\.?\s+/i;
  const TRAILER = /\s*\|.*$/;
  const SOURCE_SUFFIX = /\s*\((?:STRMCNTR|[A-Z0-9]{3,14})\)\s*$/;
  const PARENS = /\([^)]*\)/;

  const SPORT_LABELS = {
    soccer: 'Soccer',
    football: 'American Football',
    'american football': 'American Football',
    nfl: 'American Football',
    ncaaf: 'College Football',
    'college football': 'College Football',
    nhl: 'NHL Hockey',
    'nhl hockey': 'NHL Hockey',
    hockey: 'Hockey',
    basketball: 'Basketball',
    nba: 'NBA Basketball',
    'ncaa basketball': 'College Basketball',
    mlb: 'MLB Baseball',
    baseball: 'Baseball',
    ufc: 'UFC / MMA',
    mma: 'UFC / MMA',
    boxing: 'Boxing',
    wrestling: 'Wrestling',
    golf: 'Golf',
    tennis: 'Tennis',
    f1: 'Formula 1',
    nascar: 'NASCAR',
    cricket: 'Cricket',
    rugby: 'Rugby',
    sports: 'Sports',
  };

  // Football-league tags the scrapers use for soccer competitions.
  const SOCCER_LEAGUES = new Set([
    'liga mx', 'ligamx', 'laliga', 'la liga', 'premier league', 'epl', 'mls',
    'bundesliga', 'serie a', 'ligue 1', 'liga profesional', 'liga 1',
    'champions league', 'europa league', 'copa', 'eredivisie', 'primeira liga',
    'saudi pro league', 'world cup', 'euros',
  ]);

  // Section order on the Live Events tab; unlisted sports sort after these.
  const SPORT_ORDER = [
    'Soccer', 'American Football', 'College Football', 'NHL Hockey', 'Hockey',
    'Basketball', 'NBA Basketball', 'College Basketball', 'MLB Baseball',
    'Baseball', 'UFC / MMA', 'Boxing',
  ];

  function normKey(value) {
    return String(value || '').toLowerCase().replace(/[^a-z0-9]+/g, '');
  }

  /**
   * The sport one event entry belongs to, or null when the name is not an
   * event. The placeholder ids the event feeds share ("Soccer.Dummy.us") are
   * the strongest hint; the bracket tag decides everywhere else.
   */
  function sportOfEvent(channel) {
    const id = channel.id || '';
    let fromId = null;
    // Only the scrapers' placeholder ids are trustworthy hints; a real
    // channel id that merely starts with "soccer" says nothing.
    if (id.toLowerCase().includes('.dummy.')) {
      const prefix = normKey(id.split('.Dummy')[0].split('.')[0]);
      fromId = {
        soccer: 'Soccer',
        football: 'American Football',
        nhlhockey: 'NHL Hockey',
        ncaasports: 'College Football',
        ncaa: 'College Football',
      }[prefix] || null;
    }
    const match = BRACKET_TAG.exec(channel.name || '');
    if (!match) return null;
    const tag = match[1].trim();
    const tagKey = normKey(tag);
    let fromTag = SPORT_LABELS[tagKey] || null;
    if (!fromTag && SOCCER_LEAGUES.has(tag.toLowerCase().trim())) fromTag = 'Soccer';
    if (fromId) {
      // The id knows the discipline; the tag may only name the league -
      // except "[Football]", which the scrapers also use for soccer games.
      if (!fromTag || (fromTag === 'American Football' && fromId === 'Soccer')) return fromId;
      return fromTag;
    }
    return fromTag || tag;
  }

  /** One parsed game: { sport, title, key } or null. */
  function parseLiveEvent(channel) {
    const sport = sportOfEvent(channel);
    if (!sport) return null;
    const match = BRACKET_TAG.exec(channel.name || '');
    let title = (match ? match[2] : '').replace(TRAILER, '').trim();
    title = title.replace(SOURCE_SUFFIX, '').trim();
    const parts = title.split(VERSUS);
    if (parts.length < 2) return null;
    const home = parts[0].trim();
    const away = parts.slice(1).join(' vs. ').trim();
    if (!home || !away) return null;
    return {
      sport,
      title: `${home} vs. ${away}`,
      key: `${normKey(sport)}|${normKey(home)}|${normKey(away)}`,
    };
  }

  /**
   * Every game in the playlist, grouped into sport sections, each game with
   * all of its streams as servers (playlist order kept, URLs deduplicated).
   * Returns [{ sport, events: [{ sport, title, key, servers: [channel] }] }].
   */
  function buildSections(channels) {
    const events = new Map();
    for (const channel of channels || []) {
      const parsed = parseLiveEvent(channel);
      if (!parsed) continue;
      let event = events.get(parsed.key);
      if (!event) {
        event = { sport: parsed.sport, title: parsed.title, key: parsed.key, servers: [] };
        events.set(parsed.key, event);
      }
      if (!event.servers.some((server) => server.url === channel.url)) {
        event.servers.push(channel);
      }
    }
    if (!events.size) return [];
    const bySport = new Map();
    for (const event of events.values()) {
      const list = bySport.get(event.sport) || [];
      list.push(event);
      bySport.set(event.sport, list);
    }
    const sections = [];
    for (const [sport, list] of bySport) {
      list.sort((a, b) => a.title.localeCompare(b.title));
      sections.push({ sport, events: list });
    }
    sections.sort((a, b) => {
      const ia = SPORT_ORDER.indexOf(a.sport);
      const ib = SPORT_ORDER.indexOf(b.sport);
      const ra = ia < 0 ? SPORT_ORDER.length : ia;
      const rb = ib < 0 ? SPORT_ORDER.length : ib;
      return ra - rb || a.sport.localeCompare(b.sport);
    });
    return sections;
  }

  /** Maps every event feed's URL to its game, for the LIVE labels. */
  function indexByChannel(channels) {
    const index = new Map();
    for (const section of buildSections(channels)) {
      for (const event of section.events) {
        for (const server of event.servers) index.set(server.url, event);
      }
    }
    return index;
  }

  /** "Pluto TV Kids (Spain) (720p)" -> "pluto tv kids": the name backups share. */
  function baseDisplayName(name) {
    let text = String(name || '');
    let previous;
    do {
      previous = text;
      text = text.replace(PARENS, ' ');
    } while (text !== previous);
    return text.replace(/\s{2,}/g, ' ').trim().toLowerCase();
  }

  /**
   * The playable server list for a channel: the game's other feeds when it
   * is an event, otherwise the channel's backup feeds (same EPG id, same base
   * name), with the selected feed first.
   */
  function serversFor(channel, channels) {
    const event = indexByChannel(channels).get(channel.url);
    let pool;
    if (event) {
      pool = event.servers;
    } else {
      const base = baseDisplayName(channel.name);
      pool = [channel].concat((channels || []).filter((other) => (
        other.url !== channel.url &&
        other.id && other.id === channel.id &&
        baseDisplayName(other.name) === base
      )));
    }
    const ordered = [channel];
    for (const candidate of pool) {
      if (candidate.url !== channel.url && !ordered.some((item) => item.url === candidate.url)) {
        ordered.push(candidate);
      }
    }
    return ordered;
  }

  return {
    sportOfEvent,
    parseLiveEvent,
    buildSections,
    indexByChannel,
    serversFor,
    baseDisplayName,
  };
})();
