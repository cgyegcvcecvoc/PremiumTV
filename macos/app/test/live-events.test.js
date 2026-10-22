'use strict';

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const renderer = path.join(__dirname, '..', 'src', 'renderer');

function loadLive() {
  const window = {};
  vm.runInNewContext(
    fs.readFileSync(path.join(renderer, 'live-events.js'), 'utf8'),
    { window },
  );
  return window.PremiumLive;
}

function loadIcons() {
  const window = {};
  vm.runInNewContext(
    fs.readFileSync(path.join(renderer, 'category-icons.js'), 'utf8'),
    { window },
  );
  return window.PremiumIcons;
}

function channel(id, name, url, group = 'Sports') {
  return { id, name, url, group, country: 'US', logo: '', chno: '' };
}

test('the scrapers event names parse into sport and matchup', () => {
  const live = loadLive();
  const event = live.parseLiveEvent(channel(
    'Football.Dummy.us',
    '[American Football] Ball State Cardinals vs. Bowling Green Falcons | English (STRMCNTR)',
    'https://edge.example/1.m3u8',
  ));
  assert.equal(event.sport, 'American Football');
  assert.equal(event.title, 'Ball State Cardinals vs. Bowling Green Falcons');
});

test('the soccer placeholder id wins over the "[Football]" tag', () => {
  const live = loadLive();
  const event = live.parseLiveEvent(channel(
    'Soccer.Dummy.us', '[Football] AS Roma vs. Genoa | English (STRMCNTR)', 'https://s/2',
  ));
  assert.equal(event.sport, 'Soccer');
  assert.equal(event.title, 'AS Roma vs. Genoa');
});

test('college, hockey, league and mma tags land in their own sections', () => {
  const live = loadLive();
  assert.equal(
    live.parseLiveEvent(channel('NCAA.Sports.Dummy.us', '[NCAAF] Ohio vs. Michigan | English', 'u')).sport,
    'College Football',
  );
  assert.equal(
    live.parseLiveEvent(channel('NHL.Hockey.Dummy.us', '[NHL Hockey] Bruins vs. Rangers', 'u')).sport,
    'NHL Hockey',
  );
  assert.equal(live.parseLiveEvent(channel('doms9.example_17', '[Liga MX] America vs. Chivas', 'u')).sport, 'Soccer');
  assert.equal(live.parseLiveEvent(channel('doms9.example_18', '[UFC] A vs. B', 'u')).sport, 'UFC / MMA');
});

test('ordinary channels and shows without a matchup are not events', () => {
  const live = loadLive();
  assert.equal(live.parseLiveEvent(channel('news.us', 'NBC News Now', 'u')), null);
  assert.equal(live.parseLiveEvent(channel('Sports.Dummy.us', '[Sports] Pregame Show', 'u')), null);
  assert.equal(live.parseLiveEvent(channel('movies.us', 'Casino (1995)', 'u', 'Movies')), null);
});

test('games group into sport sections with their servers', () => {
  const live = loadLive();
  const sections = live.buildSections([
    channel('Football.Dummy.us', '[American Football] A Cats vs. B Dogs | English (STRMCNTR)', 'https://e/1'),
    channel('Soccer.Dummy.us', '[Football] Roma vs. Genoa | English (STRMCNTR)', 'https://e/2'),
    channel('Soccer.Dummy.us', '[Football] Roma vs. Genoa | Spanish (STRMCNTR)', 'https://e/3'),
    channel('news.us', 'Local News', 'https://e/4', 'News'),
  ]);
  assert.deepEqual([...sections.map((section) => section.sport)], ['Soccer', 'American Football']);
  const soccer = sections[0].events[0];
  assert.equal(soccer.title, 'Roma vs. Genoa');
  assert.deepEqual([...soccer.servers.map((server) => server.url)], ['https://e/2', 'https://e/3']);
});

test('every feed of a game falls back to its siblings, and backups to each other', () => {
  const live = loadLive();
  const english = channel('Soccer.Dummy.us', '[Football] Roma vs. Genoa | English (STRMCNTR)', 'https://e/2');
  const spanish = channel('Soccer.Dummy.us', '[Football] Roma vs. Genoa | Spanish (STRMCNTR)', 'https://e/3');
  const all = [english, spanish, channel('news.us', 'News', 'https://e/4', 'News')];
  assert.deepEqual([...live.serversFor(english, all).map((s) => s.url)], ['https://e/2', 'https://e/3']);
  assert.deepEqual([...live.serversFor(spanish, all).map((s) => s.url)], ['https://e/3', 'https://e/2']);

  const main = channel('Jokes.us@SD', 'Just for Laughs Gags (1080p)', 'https://j/1', 'Comedy');
  const backup = channel('Jokes.us@SD', 'Just for Laughs Gags (Backup 1)', 'https://j/2', 'Comedy Backups');
  const sameIdOtherShow = channel('Jokes.us@SD', 'Comedy Block (720p)', 'https://j/3', 'Comedy');
  const mixed = [main, backup, sameIdOtherShow];
  assert.deepEqual([...live.serversFor(main, mixed).map((s) => s.url)], ['https://j/1', 'https://j/2']);
  // Sharing an id is not enough: another show on the id stays out.
  assert.deepEqual([...live.serversFor(sameIdOtherShow, mixed).map((s) => s.url)], ['https://j/3']);
});

test('the live index maps every feed to its game', () => {
  const live = loadLive();
  const a = channel('Soccer.Dummy.us', '[Football] Roma vs. Genoa | English (STRMCNTR)', 'https://e/2');
  const b = channel('Soccer.Dummy.us', '[Football] Roma vs. Genoa | Spanish (STRMCNTR)', 'https://e/3');
  const index = live.indexByChannel([a, b, channel('news.us', 'News', 'https://e/4', 'News')]);
  assert.equal(index.size, 2);
  assert.equal(index.get('https://e/2').title, 'Roma vs. Genoa');
  assert.equal(index.get('https://e/4'), undefined);
});

test('categories get their own placeholder picture and the rest get the TV set', () => {
  const icons = loadIcons();
  assert.equal(icons.keyForGroup('Sports'), 'ball');
  assert.equal(icons.keyForGroup('Sports Backups'), 'ball');
  assert.equal(icons.keyForGroup('NHL Hockey'), 'ball');
  assert.equal(icons.keyForGroup('Comedy'), 'smile');
  assert.equal(icons.keyForGroup('News'), 'news');
  assert.equal(icons.keyForGroup('Kids'), 'balloon');
  assert.equal(icons.keyForGroup('Cartoons'), 'balloon');
  assert.equal(icons.keyForGroup('Music'), 'music');
  assert.equal(icons.keyForGroup('Movies'), 'movie');
  assert.equal(icons.keyForGroup('Weather'), 'weather');
  assert.equal(icons.keyForGroup('Documentary'), 'book');
  assert.equal(icons.keyForGroup('Business'), 'chart');
  assert.equal(icons.keyForGroup('Tv Celebrities'), 'star');
  assert.equal(icons.keyForGroup('Religious'), 'cross');
  assert.equal(icons.keyForGroup('Legislative'), 'law');
  assert.equal(icons.keyForGroup('Lifestyle'), 'heart');
  assert.equal(icons.keyForGroup('International'), 'globe');
  assert.equal(icons.keyForGroup('Other'), 'tv');
  assert.equal(icons.keyForGroup('Classic TV'), 'tv');

  const svg = icons.svgForGroup('Sports');
  assert.match(svg, /^<svg class="ph-icon" viewBox="0 0 24 24"/);
  assert.match(svg, /<\/svg>$/);
  // A hostile group name cannot inject markup: only the class is interpolated
  // and it comes from the app, never from the playlist.
  assert.doesNotMatch(icons.svgForGroup('<img src=x onerror=alert(1)>'), /<img/);
});

test('1.0.8: a matchup splits into its two teams for the badges', () => {
  const live = loadLive();
  // teamsOf runs in the module's VM realm, so copy the array out before
  // comparing it with a same-realm literal.
  assert.deepEqual([...live.teamsOf('Ball State Cardinals vs. Bowling Green Falcons')], [
    'Ball State Cardinals',
    'Bowling Green Falcons',
  ]);
  assert.deepEqual([...live.teamsOf('Roma vs Genoa')], ['Roma', 'Genoa']);
  assert.equal(live.teamsOf('Pregame Show'), null);
  assert.equal(live.teamsOf(''), null);
});

test('1.0.8: badges take two initials and stable colours from the name', () => {
  const live = loadLive();
  assert.equal(live.initialsFor('Ball State Cardinals'), 'BS');
  assert.equal(live.initialsFor('Arsenal'), 'AR');
  assert.equal(live.initialsFor('AS Roma'), 'AR');
  assert.equal(live.initialsFor('   '), '?');
  // Same team, same colours — every launch, no network involved.
  assert.deepEqual([...live.crestColorsFor('Boston Bruins')], [...live.crestColorsFor('Boston Bruins')]);
  assert.notDeepEqual(live.crestColorsFor('Boston Bruins'), live.crestColorsFor('Montreal Canadiens'));
  const [start, end] = live.crestColorsFor('Boston Bruins');
  assert.match(start, /^hsl\(\d+, 58%, 44%\)$/);
  assert.match(end, /^hsl\(\d+, 52%, 28%\)$/);
  const hue = live.teamHue('Boston');
  assert.ok(hue >= 0 && hue < 360, `hue in range, got ${hue}`);
  assert.equal(live.teamHue('Boston'), live.teamHue('Boston'));
});

test('team keys collapse spelling variants and merge reversed matchups', () => {
  const live = loadLive();
  // "F.C. København" and "FC Copenhagen" are the same club.
  assert.equal(live.teamKey('F.C. København'), live.teamKey('FC Copenhagen'));
  // "Stade Rennais" and "Rennes" are the same club.
  assert.equal(live.teamKey('Stade Rennais'), live.teamKey('Rennes'));
  // Reversed matchups key identically.
  const a = live.parseLiveEvent({
    id: 'Soccer.Dummy.us', name: '[UEFA Conference League] A vs. B (FAWA)', url: 'u/1',
  });
  const b = live.parseLiveEvent({
    id: 'Soccer.Dummy.us', name: '[UEFA Conference League] B vs. A (FAWA)', url: 'u/2',
  });
  assert.equal(a.key, b.key);
  // Feed-copy numbers are stripped from the identity.
  const c = live.parseLiveEvent({
    id: 'Soccer.Dummy.us', name: '[UEFA Conference League] C vs. D 2 (FAWA)', url: 'u/3',
  });
  const d = live.parseLiveEvent({
    id: 'Soccer.Dummy.us', name: '[UEFA Conference League] C vs. D (FAWA)', url: 'u/4',
  });
  assert.equal(c.key, d.key);
});

test('source markers are stripped from team names', () => {
  const live = loadLive();
  assert.equal(live.cleanTeam('Ferencváros vs Torreense (DAMITV) (Backup 1)'), 'Ferencváros vs Torreense');
  assert.equal(live.cleanTeam('Union St.-Gilloise vs. Hapoel Be\'er (DAMITV)'), 'Union St.-Gilloise vs. Hapoel Be\'er');
});

test('buildSections attaches scheduled kickoffs and deduplicates feeds', () => {
  const live = loadLive();
  const schedule = {
    'uefachampionsleague|arsenal|chelsea': 1_792_646_000, // a future kickoff on 2026-10-22
  };
  const sections = live.buildSections([
    { id: 'e/1', name: '[UEFA Champions League] Arsenal vs. Chelsea', url: 'https://e/1', group: 'Sports' },
    { id: 'e/2', name: '[UEFA Champions League] Chelsea vs. Arsenal', url: 'https://e/2', group: 'Sports' },
    { id: 'e/3', name: '[UEFA Champions League] Arsenal vs. Chelsea 2', url: 'https://e/3', group: 'Sports' },
  ], schedule);
  assert.equal(sections.length, 1);
  assert.equal(sections[0].events.length, 1);
  const event = sections[0].events[0];
  assert.equal(event.title, 'Arsenal vs. Chelsea');
  assert.deepEqual([...event.servers.map((s) => s.url)], ['https://e/1', 'https://e/2', 'https://e/3']);
  assert.equal(event.kickoffMs, 1_792_646_000 * 1000);
});

test('eventStatus reports not-live-yet before kickoff', () => {
  const live = loadLive();
  const now = 1_792_640_000; // before kickoff
  assert.equal(live.eventStatus('live', null, now), 'live');
  assert.equal(live.eventStatus('checking', 1_792_700_000, now), 'checking');
  assert.equal(live.eventStatus(null, 1_792_700_000, now), 'notlive');
  assert.equal(live.eventStatus('silent', 1_792_700_000, now), 'notlive');
  assert.equal(live.eventStatus('silent', 1_792_600_000, now), 'silent');
  assert.equal(live.eventStatus('checking', null, now), 'checking');
});

test('countdownText formats seconds remaining', () => {
  const live = loadLive();
  assert.equal(live.countdownText(45), '00:45');
  assert.equal(live.countdownText(90), '01:30');
  assert.equal(live.countdownText(3700), '1:01:40');
  assert.equal(live.countdownText(90061), '1d 1:01:01');
});

test('kickoffLabel renders local kickoff time', () => {
  const live = loadLive();
  const label = live.kickoffLabel(1_792_702_800); // 2026-10-22T21:00:00Z
  assert.ok(/^\d{1,2}:\d{2}( AM| PM)$/.test(label), `unexpected label: ${label}`);
});

test('teamLogoUrl reads bundled crest URLs', () => {
  const live = loadLive();
  const doc = { team_logos: { chelsea: 'https://example.org/chelsea.svg' } };
  assert.equal(live.teamLogoUrl(doc, 'Chelsea'), 'https://example.org/chelsea.svg');
  assert.equal(live.teamLogoUrl(doc, 'Nobody'), null);
  assert.equal(live.teamLogoUrl(null, 'Chelsea'), null);
});
