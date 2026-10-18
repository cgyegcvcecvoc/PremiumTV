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
