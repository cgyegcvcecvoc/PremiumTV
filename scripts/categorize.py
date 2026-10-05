#!/usr/bin/env python3
"""
One category system for every published playlist.

The daily scraper inherits whatever ``group-title`` the public indexes happen to
publish, which is why the player playlists ended up with 1647 "General",
872 "Undefined", 162 "TV" and a long tail of emoji-decorated one-offs - and why
NFL Network sat in "TV" instead of Sports.

This module replaces that with a single, ordered taxonomy:

    1. Sports
    2. Lifestyle
    3. Fox Channels
    4. CBS
    5. NBC
    6. NBC Sports Channels
    7. Cartoons
    8. PBS
    9. Game Shows

Every one of them is followed by its own "<category> Backups" group, so a
channel that stops playing has somewhere to fail over to and the player keeps
the two apart. Cartoons, PBS and Game Shows are categories of their own, as
requested; everything else in the library keeps a tidy, normalised group and is
listed *after* the nine curated ones instead of being thrown away.

Order is part of the contract: ``CURATED_CATEGORIES`` is the order the groups
appear in the file, not a set. Change the list and the playlist order changes
with it - no other file needs to be touched.

Usage:

    python scripts/categorize.py --audit playlists/PremiumTV.m3u
    python scripts/categorize.py --audit playlists/PremiumTV.m3u --show 40

    import categorize
    categorize.assign_categories(channels)      # set group-title on each channel
    ordered = categorize.build_main_order(channels)   # primary + backup groups
"""
from __future__ import annotations

import argparse
import collections
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --------------------------------------------------------------------------- #
# The taxonomy
# --------------------------------------------------------------------------- #
# The order of this list is the order of the groups in every published playlist.
CURATED_CATEGORIES: tuple[str, ...] = (
    "Sports",
    "Lifestyle",
    "Fox Channels",
    "CBS",
    "NBC",
    "NBC Sports Channels",
    "Cartoons",
    "PBS",
    "Game Shows",
)

BACKUP_SUFFIX = " Backups"
OTHER = "Other"

# Groups the upstream indexes use as a dumping ground. They carry no
# information, so they never survive normalisation - the channel is classified
# by what it actually is instead.
GENERIC_GROUPS = {
    "general", "undefined", "tv", "other", "misc", "miscellaneous", "unknown",
    "channels", "all", "n/a", "none", "default", "various", "diversos", "diverse",
    "varios", "variados", "outros", "otros", "autres", "sonstiges", "buy me a coffee",
    "donate", "support us", "",
}

# A compound group such as "Culture Education" or "Documentary News" is folded
# onto its first meaningful token, so the listing keeps a handful of stable
# labels instead of one group per upstream spelling.
CANONICAL_TOKENS = {
    "movies": "Movies", "movie": "Movies", "films": "Movies", "film": "Movies",
    "cinema": "Movies", "vod": "Movies", "classics": "Movies", "classicos": "Movies",
    "western": "Movies", "terror": "Movies", "horror": "Movies", "thriller": "Movies",
    "news": "News", "music": "Music", "kids": "Kids", "documentary": "Documentary",
    "documentaries": "Documentary", "religious": "Religious", "education": "Education",
    "culture": "Culture", "business": "Business", "entertainment": "Entertainment",
    "sports": "Sports", "sport": "Sports", "series": "Series", "novelas": "Series",
    "telenovelas": "Series", "comedy": "Comedy", "family": "Family",
    "classic": "Classic TV", "weather": "Weather", "legislative": "Legislative",
    "shopping": "Shopping", "shop": "Shopping", "anime": "Anime", "cartoons": "Cartoons",
    "animation": "Cartoons", "lifestyle": "Lifestyle", "travel": "Lifestyle",
    "science": "Documentary", "public": "Public TV", "local": "Local TV",
    "general": "", "tv": "", "and": "", "the": "",
}

# Country-named groups ("Italy", "Greece", "日本 Japan") are regional, not
# genres. The repository already publishes one playlist per country, so inside
# the main playlist they are folded into a single International group.
INTERNATIONAL = "International"

# Last-resort fallback: a channel nobody can classify by name still carries a
# country in its tvg-id ("KosTV.gr@SD"), so it lands in a world region instead
# of one giant "Other" bucket.
COUNTRY_REGION: dict[str, str] = {
    "ad": "Europe", "ae": "Asia", "af": "Asia", "ag": "North America", "al": "Europe",
    "am": "Asia", "ao": "Africa", "ar": "South America", "at": "Europe", "au": "Oceania",
    "aw": "North America", "az": "Asia", "ba": "Europe", "bb": "North America", "bd": "Asia",
    "be": "Europe", "bf": "Africa", "bg": "Europe", "bh": "Asia", "bi": "Africa",
    "bj": "Africa", "bm": "North America", "bn": "Asia", "bo": "South America",
    "bq": "North America", "br": "South America", "bs": "North America", "bt": "Asia",
    "bw": "Africa", "by": "Europe", "bz": "North America", "ca": "North America",
    "cd": "Africa", "cf": "Africa", "cg": "Africa", "ch": "Europe", "ci": "Africa",
    "cl": "South America", "cm": "Africa", "cn": "Asia", "co": "South America",
    "cr": "North America", "cu": "North America", "cv": "Africa", "cw": "North America",
    "cy": "Asia", "cz": "Europe", "de": "Europe", "dj": "Africa", "dk": "Europe",
    "dm": "North America", "do": "North America", "dz": "Africa", "ec": "South America",
    "ee": "Europe", "eg": "Africa", "er": "Africa", "es": "Europe", "et": "Africa",
    "fi": "Europe", "fj": "Oceania", "fo": "Europe", "fr": "Europe", "ga": "Africa",
    "gb": "Europe", "gd": "North America", "ge": "Asia", "gf": "South America", "gh": "Africa",
    "gi": "Europe", "gl": "North America", "gm": "Africa", "gn": "Africa",
    "gp": "North America", "gq": "Africa", "gr": "Europe", "gt": "North America",
    "gu": "Oceania", "gw": "Africa", "gy": "South America", "hk": "Asia",
    "hn": "North America", "hr": "Europe", "ht": "North America", "hu": "Europe", "id": "Asia",
    "ie": "Europe", "il": "Asia", "in": "Asia", "iq": "Asia", "ir": "Asia", "is": "Europe",
    "it": "Europe", "jm": "North America", "jo": "Asia", "jp": "Asia", "ke": "Africa",
    "kg": "Asia", "kh": "Asia", "kn": "North America", "kp": "Asia", "kr": "Asia",
    "kw": "Asia", "ky": "North America", "kz": "Asia", "la": "Asia", "lb": "Asia",
    "lc": "North America", "li": "Europe", "lk": "Asia", "lr": "Africa", "ls": "Africa",
    "lt": "Europe", "lu": "Europe", "lv": "Europe", "ly": "Africa", "ma": "Africa",
    "mc": "Europe", "md": "Europe", "me": "Europe", "mg": "Africa", "mk": "Europe",
    "ml": "Africa", "mm": "Asia", "mn": "Asia", "mo": "Asia", "mq": "North America",
    "mr": "Africa", "mt": "Europe", "mu": "Africa", "mv": "Asia", "mw": "Africa",
    "mx": "North America", "my": "Asia", "mz": "Africa", "na": "Africa", "ne": "Africa",
    "ng": "Africa", "ni": "North America", "nl": "Europe", "no": "Europe", "np": "Asia",
    "nz": "Oceania", "om": "Asia", "pa": "North America", "pe": "South America",
    "pf": "Oceania", "pg": "Oceania", "ph": "Asia", "pk": "Asia", "pl": "Europe",
    "pr": "North America", "ps": "Asia", "pt": "Europe", "py": "South America", "qa": "Asia",
    "re": "Africa", "ro": "Europe", "rs": "Europe", "ru": "Europe", "rw": "Africa",
    "sa": "Asia", "sd": "Africa", "se": "Europe", "sg": "Asia", "si": "Europe", "sk": "Europe",
    "sl": "Africa", "sm": "Europe", "sn": "Africa", "so": "Africa", "sr": "South America",
    "ss": "Africa", "sv": "North America", "sy": "Asia", "sz": "Africa", "td": "Africa",
    "tg": "Africa", "th": "Asia", "tj": "Asia", "tm": "Asia", "tn": "Africa", "tr": "Asia",
    "tt": "North America", "tw": "Asia", "tz": "Africa", "ua": "Europe", "ug": "Africa",
    "us": "North America", "uy": "South America", "uz": "Asia", "vc": "North America",
    "ve": "South America", "vg": "North America", "vi": "North America", "vn": "Asia",
    "vu": "Oceania", "ws": "Oceania", "xk": "Europe", "ye": "Asia", "za": "Africa",
    "zm": "Africa", "zw": "Africa"
}
COUNTRY_REGION.update({"us": "United States", "gb": "UK", "uk": "UK",
                       "ca": "Canada", "au": "Australia", "in": "India"})

# Explicit group-title cleanups for groups that do carry information but are
# spelled inconsistently upstream ("VOD Italy", "Films 📽️", "Tv • Series 📺"...).
GROUP_SYNONYMS = {
    "vod": "Movies",
    "vod italy": "Movies",
    "vod movies": "Movies",
    "vod movies (en)": "Movies",
    "films": "Movies",
    "films • terror & sci-fi": "Movies",
    "films • clássicos & western": "Movies",
    "movies;series": "Movies",
    "series": "Series",
    "tv • series": "Series",
    "doc & history": "Documentary",
    "documentaries": "Documentary",
    "crime files": "Documentary",
    "music • stingray": "Music",
    "animation": "Cartoons",
    "anime": "Anime",
    "news;general": "News",
    "general;news": "News",
    "kids": "Kids",
    "kids 🧒🌎": "Kids",
    "tv • reality": "Lifestyle",
    "tv • lifestyles & travel": "Lifestyle",
    "shop": "Shopping",
    "legislative": "Legislative",
    "live events": "Sports",
    "local": "Local TV",
    "education": "Education",
    "culture": "Culture",
    "religious": "Religious",
    "business": "Business",
    "entertainment": "Entertainment",
    "documentary": "Documentary",
    "comedy": "Comedy",
    "classic": "Classic TV",
    "classic tv": "Classic TV",
    "family": "Family",
    "travel": "Lifestyle",
    "cooking": "Lifestyle",
    "outdoor": "Lifestyle",
}

# --------------------------------------------------------------------------- #
# Matching helpers
# --------------------------------------------------------------------------- #
def norm_text(value: str) -> str:
    """Lowercase, strip accents and punctuation: 'NFL Network (720p)' -> 'nfl network 720p'."""
    text = (value or "").lower()
    text = re.sub(r"[à-ɏ]", lambda m: _strip_accents(m.group()), text)
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _strip_accents(chunk: str) -> str:
    import unicodedata
    decomposed = unicodedata.normalize("NFKD", chunk)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def norm_key(value: str) -> str:
    """Squeezed comparison key: 'MeTV Toons' -> 'metvtoons'."""
    return re.sub(r"[^a-z0-9]+", "", norm_text(value))


# ``normalize_group`` compares a cleaned group against GENERIC_GROUPS through
# norm_key, which squeezes spaces out ("Buy Me a Coffee" -> "buymeacoffee"). The
# set is squeezed the same way, otherwise a dumping ground written with spaces
# ("buy me a coffee", "donate", "buy me a coffee") never matches and gets published.
GENERIC_GROUP_KEYS = frozenset(norm_key(item) for item in GENERIC_GROUPS)


def _compile(fragments) -> re.Pattern:
    """Build one case-insensitive regex from fragments with safe word edges."""
    return re.compile(r"(?<![a-z0-9])(?:" + "|".join(fragments) + r")(?![a-z0-9])", re.IGNORECASE)


def _words(text: str) -> str:
    """Normalised text padded with spaces so ^/$ anchors behave like word edges."""
    return f" {norm_text(text)} "


# --------------------------------------------------------------------------- #
# Category vocabularies
# --------------------------------------------------------------------------- #
SPORTS = _compile([
    # US leagues / networks
    r"nfl", r"nba", r"wnba", r"mlb", r"nhl", r"mls", r"nfl network", r"nfl redzone",
    r"nfl red zone", r"nfl network hd", r"ncaa", r"ncaaf", r"ncaab", r"college football",
    r"college basketball", r"college sports", r"espn", r"espn2", r"espn3", r"espnu",
    r"espnews", r"espn plus", r"espn deportes", r"sec network", r"acc network",
    r"longhorn network", r"fox sports", r"fs1", r"fs2", r"fox soccer plus", r"fox deportes",
    r"big ten network", r"btn", r"cbs sports", r"cbs sports network", r"cbssports",
    r"stadium", r"stadium sports", r"bein", r"bein sports", r"bein max", r"dazn",
    r"eurosport", r"sky sports", r"sky sport", r"bt sport", r"tnt sports", r"tnt sport",
    r"premier sports", r"supersport(?:s)?", r"super sport", r"sportklub", r"arena sport",
    r"sport tv", r"sportsnet", r"tsn", r"rds", r"movistar deportes", r"tyc sports",
    r"dsports", r"directv sports", r"espn brasil", r"sportv", r"premiere fc", r"star sports",
    r"sony ten", r"sony six", r"willow", r"hotstar", r"tapmad", r"ptv sports", r"ary sports",
    r"geo super", r"azam sports", r"z sports", r"w-sport", r"fight sports", r"fight network",
    r"fight\+", r"fite",
    # Competitions
    r"fifa", r"uefa", r"champions league", r"europa league", r"premier league", r"la liga",
    r"serie a", r"bundesliga", r"ligue 1", r"eredivisie", r"super lig", r"liga mx",
    r"copa libertadores", r"copa america", r"world cup", r"nrl", r"afl", r"cfl", r"xfl",
    r"usfl", r"ipl", r"big bash", r"super bowl",
    # Combat / motors / endurance
    r"ufc", r"bellator", r"mma", r"pfl", r"one championship", r"wwe", r"aew",
    r"impact wrestling", r"ring of honor", r"roh", r"nxt", r"boxing", r"boxeo",
    r"kickboxing", r"muay thai", r"sumo", r"wrestling", r"lucha libre", r"glory",
    r"nascar", r"indycar", r"indy car", r"formula 1", r"f1", r"formula e", r"motogp",
    r"moto gp", r"motocross", r"supercross", r"speedway", r"world superbike", r"wsbk",
    r"rally tv", r"world rally", r"wrc", r"dakar", r"cycling", r"velo", r"tour de france",
    r"giro d'?italia", r"vuelta", r"triathlon", r"marathon",
    # Racquet / team / field sports
    r"tennis", r"atp", r"wta", r"grand slam", r"wimbledon", r"roland garros", r"golf",
    r"pga", r"lpga", r"ryder cup", r"cricket", r"kabaddi", r"badminton", r"table tennis",
    r"ping pong", r"hockey", r"football", r"futbol", r"futebol", r"soccer", r"baseball",
    r"beisbol", r"basketball", r"basquet", r"volleyball", r"voleibol", r"handball",
    r"balonmano", r"water polo", r"rugby", r"netball", r"lacrosse", r"field hockey",
    r"esports", r"e-sports", r"olympic(?:s)?", r"paralympic(?:s)?", r"pan american games",
    r"commonwealth games", r"horse racing", r"racing", r"turf", r"hipica", r"hipismo",
    r"polo", r"rodeo", r"bull riding", r"pbr", r"darts", r"snooker", r"billiards",
    r"surfing", r"surf", r"wsl", r"skiing", r"ski", r"snowboard(?:ing)?", r"biathlon",
    r"bobsleigh", r"luge", r"skeleton", r"figure skating", r"speed skating", r"curling",
    r"athletics", r"athletic", r"swimming", r"diving", r"gymnastics", r"rowing",
    r"sailing", r"equestrian", r"judo", r"karate", r"taekwondo", r"fencing",
    r"weightlifting", r"archery", r"shooting", r"climbing", r"skateboarding", r"bmx",
    r"体育", r"спорт",
    # Generic sport words (kept last: they only fire when nothing specific did)
    r"sports?", r"deportes", r"deportivos", r"esportes?", r"sporting", r"atletico",
])

NBC_SPORTS = _compile([
    r"nbc ?sports?", r"nbcsn", r"nbc sports network", r"nbc sports philadelphia",
    r"nbc sports boston", r"nbc sports bay area", r"nbc sports chicago",
    r"nbc sports washington", r"nbc sports northwest", r"nbc sports california",
    r"nbc sports philadelphia", r"golf channel", r"golf pass", r"olympic channel",
    r"peacock sports", r"telemundo deportes",
])

NBC_FAMILY = _compile([
    r"nbc", r"msnbc", r"cnbc", r"bravo", r"usa network", r"syfy", r"oxygen",
    r"telemundo", r"universo", r"nbclx", r"nbc news now", r"cozi tv", r"cozi",
    r"dateline", r"nbc american crimetimes", r"e!",
])

CBS_FAMILY = _compile([
    r"cbs", r"cbsn", r"cbs news", r"cbs reality", r"cbs justice", r"cbs drama",
    r"cbs action", r"cbs europa", r"paramount network", r"paramount plus",
])

FOX_FAMILY = _compile([
    r"fox", r"fox news", r"fox business", r"fox weather", r"fox soul", r"fox local",
    r"fox life", r"fox crime", r"fox comedy", r"fox movies", r"fox family",
    r"fox kids", r"fox action movies", r"mynetworktv", r"my network tv", r"movies!",
])

LIFESTYLE = _compile([
    r"hgtv", r"food network", r"cooking channel", r"tlc", r"travel channel",
    r"discovery life", r"destination america", r"magnolia network", r"magnolia",
    r"hallmark", r"lifetime", r"lmn", r"own", r"oprah", r"we tv", r"home & garden",
    r"home and garden", r"home", r"garden(?:ing)?", r"decor", r"interior", r"design",
    r"renovation", r"property", r"real estate", r"fashion", r"style", r"beauty",
    r"cosmetics", r"health", r"wellness", r"fitness", r"yoga", r"pilates", r"cooking",
    r"cook", r"kitchen", r"recipes", r"food", r"chef", r"grill", r"bbq", r"baking",
    r"wine", r"spirits", r"cocktails", r"travel", r"tourism", r"trip", r"holiday",
    r"adventure", r"outdoor(?:s)?", r"hunt(?:ing)?", r"fish(?:ing)?", r"camping",
    r"hiking", r"boating", r"rv", r"caravan", r"automotive", r"auto", r"cars",
    r"motor(?:cycle)?s?", r"bikes", r"pets", r"parenting", r"wedding", r"bridal",
    r"babies", r"craft(?:ing)?", r"diy", r"hobby", r"collectibles", r"antiques",
    r"auction", r"shopping", r"shop", r"qvc", r"hsn", r"jewel(?:ry)?",
    r"lifestyle", r"life style", r"reality", r"sportsman", r" Pursuit",
])

CARTOONS = _compile([
    r"cartoons?", r"toons?", r"boomerang", r"adult swim", r"toonami", r"cartoonito",
    r"animation", r"animated", r"animaniacs", r"looney tunes", r"anime",
    # Brands whose name does not contain a cartoon word edge ("nickTOONS").
    r"nick ?toons?", r"tom and jerry", r"scooby", r"spongebob", r"pokemon", r"ben 10",
    r"disney junior", r"disney jr", r"dreamworks channel",
])

PBS_CALLSIGNS = (
    "wvia", "witf", "wqed", "whyy", "wpsu", "wnet", "wgbh", "weta", "wedu", "wgte",
    "kqed", "kpbs", "koce", "ketc", "klru", "kcts", "wfyi", "wnit", "wnpt", "wmht",
    "wmfe", "wu ft", "wfsu", "wpbt", "wlrn", "wxel", "wusf", "wgcu", "wjct", "wvpt",
    "wbra", "whro", "wcte", "wljt", "wkno", "wkar", "wcmu", "wfwa", "wnin", "wtiu",
    "wyin", "wvut", "wsec", "wsiu", "will", "wtvp", "wqpt", "wmec", "wusi", "wqln",
    "wskg", "wxxi", "wmht", "wliw", "wliw21", "njmouth", "nj tv", "mpt", "mpbn",
    "iptv", "alabama public television", "wisconsin public television", "pioneer pbs",
    "twin cities pbs", "milwaukee pbs", "detroit public tv", "houston pbs",
)

PBS = _compile([r"pbs", r"public television", r"public tv", r"public broadcasting"] +
               [re.escape(call) for call in PBS_CALLSIGNS])

GAME_SHOWS = _compile([
    r"game shows?", r"game show network", r"gsn", r"buzzr", r"jeopardy",
    r"wheel of fortune", r"family feud", r"price is right", r"millionaire",
    r"deal or no deal", r"match game", r"cash cab", r"the chase", r"pyramid",
    r"quiz(?:zes)?", r"trivia", r"wheel of fortune", r"concentration",
])

# Brand groups for the long tail (after the curated categories, alphabetically
# ordered by size at write time). These keep the library browsable instead of
# dumping thousands of channels into "Other".
BRAND_GROUPS: list[tuple[str, re.Pattern]] = [
    ("Kids", _compile([
        r"nickelodeon", r"nick(?!elodeon)", r"nick jr", r"nick jr\.", r"disney channel",
        r"disney junior", r"disney xd", r"disneyjr", r"baby ?tv", r"babyfirst",
        r"cbeebies", r"cbbc", r"milkshake!", r"kidoodle", r"kids", r"kidz", r"children",
        r"junior", r"teen", r"teen nick", r"teennick", r"nickjr",
    ])),
    ("Movies", _compile([
        r"movies?", r"cinema", r"films?", r"vod", r"box office", r"hollywood",
        r"bollywood", r"nollywood", r"terror", r"thriller", r"horror", r"premiere(?:s)?",
        r"classics?", r"warner tv", r"axn", r"studio universal", r"tcm", r"amc",
        r"showtime", r"hbo", r"starz", r"cinemax", r"epix", r"flix", r"movieplex",
    ])),
    ("Music", _compile([
        r"music", r"mtv(?![a-z])", r"vh1", r"vevo", r"stingray", r"radio", r"karaoke",
        r"jazz", r"country music", r"hip hop", r"rock", r"charts", r"hits", r"tracy",
        r"club mtv", r"mtv live", r"cmt", r"much music",
    ])),
    ("Documentary", _compile([
        r"documentary", r"documentaries", r"discovery", r"history", r"national geographic",
        r"nat geo", r"animal planet", r"science", r"crime", r"investigation", r"wild(?:life)?",
        r"nature", r"smithsonian", r"curiosity", r"war", r"military",
    ])),
    ("Religious", _compile([
        r"church", r"gospel", r"faith", r"christian", r"catholic", r"islam(?:ic)?",
        r"muslim", r"quran", r"koran", r"hindu", r"buddhist", r"jewish", r"spiritual",
        r"prayer", r"bible", r"tbn", r"daystar", r"ewtn", r"religious", r"ministry",
        r"praise", r"worship", r"jesus", r"god tv", r"trinity", r"sikh", r"zoe tv",
    ])),
    ("Education", _compile([
        r"education(?:al)?", r"learning", r"school", r"university", r"lecture",
        r"academic", r"knowledge", r"teach(?:ing)?",
    ])),
    ("Business", _compile([
        r"business", r"bloomberg", r"finance", r"financial", r"markets?", r"trading",
        r"economy", r"forbes", r"invest(?:ing)?",
    ])),
    ("News", _compile([
        r"news", r"cnn", r"bbc", r"sky news", r"al ?jazeera", r"euronews", r"france 24",
        r"dw news", r"rt news", r"ndtv", r"times now", r"zee news", r"aaj tak",
        r"news18", r"news nation", r"newsnation", r"newsmax", r"oann", r"i24",
        r"trt world", r"nhk world", r"press(?:tv)?", r"journal", r"headlines", r"breaking",
    ])),
    ("Entertainment", _compile([
        r"entertainment", r"series", r"sitcom", r"comedy", r"drama", r"variety",
        r"talk show", r"celebrity", r"gossip", r"e! (?:news|entertainment)", r"reality",
        r"general entertainment", r"tv shows?",
    ])),
]

# --------------------------------------------------------------------------- #
# Cross-source group voting
# --------------------------------------------------------------------------- #
# Most channels are published by several indexes at once. When this playlist's
# own index tagged it "General" but three others tagged it "Music", the majority
# wins. The votes are learned from the corpus (playlists/PremiumTV_all.m3u, the
# source caches) by build_group_votes() and installed with set_group_votes().
_GROUP_VOTES: dict[str, collections.Counter] = {}


def set_group_votes(votes: dict[str, collections.Counter] | None) -> None:
    """Install (or clear) the learned group votes used as a fallback."""
    global _GROUP_VOTES
    _GROUP_VOTES = votes or {}


def build_group_votes(channels: list) -> dict[str, collections.Counter]:
    """Learn what each channel is from every index that publishes it."""
    votes: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for channel in channels:
        attrs = channel.attrs if hasattr(channel, "attrs") else {}
        group = normalize_group(str(attrs.get("group-title", "") or ""))
        if not group:
            continue
        key = norm_key(clean_display_name(_get(channel, "name")))
        if key:
            votes[key][group] += 1
    return votes


def lookup_group_vote(name: str) -> str:
    """The most common non-generic label other indexes gave this channel."""
    key = norm_key(clean_display_name(name))
    counter = _GROUP_VOTES.get(key)
    if not counter:
        return ""
    label, count = counter.most_common(1)[0]
    return label if count else ""


# Quality/duplication markers stripped from a name to recognise that two entries
# are the same channel, and to give the entry one clean display name.
_NOISE_PARENS = re.compile(
    r"\s*\((?:"
    r"2160p|1440p|1080p|720p|576p|480p|360p|240p|4k|uhd|fhd|hd|sd|hdtv|hevc|h264|h265|"
    r"auto|mobile|high|low|mid|best|main|"
    r"(?:alt|alternate|backup|mirror|feed|link|stream|source|server|cdn)\s*\d*|"
    r"\d{3,4}p"
    r")\)\s*", re.IGNORECASE)
# Status markers the upstream indexes put in square brackets. They say nothing
# about which channel this is, and they stop "NFL Network [Not 24/7]" from
# matching "NFL Network" in the guide.
_NOISE_BRACKETS = re.compile(
    r"\s*\[(?:not\s*24/?7|geo[- ]?blocked|offline|down|dead|new|hd|sd)\]\s*",
    re.IGNORECASE)

_RESOLUTION_SCORE = (
    ("2160", 5), ("4k", 5), ("uhd", 5), ("1440", 4), ("1080", 3), ("720", 2),
    ("576", 1), ("480", 1), ("360", 0), ("240", 0),
)


# --------------------------------------------------------------------------- #
# Group normalisation
# --------------------------------------------------------------------------- #
def clean_group(raw: str) -> str:
    """Strip emoji/decoration from a group-title and collapse separators."""
    text = (raw or "").replace("​", " ").replace("﻿", " ")
    text = re.sub(r"[\U0001F000-\U0001FAFF☀-➿←-⇿️︎]", "", text)
    text = re.sub(r"[\u0300-\u036f]", "", text)
    text = text.replace("•", " ").replace("|", " ").replace("/", " ").replace(";", " ")
    text = re.sub(r"\s+", " ", text).strip(" -–—_:;,.·&")
    return text


_COUNTRY_NAMES: set[str] | None = None


def country_names() -> set[str]:
    """Country names known to the scraper, as squeezed comparison keys."""
    global _COUNTRY_NAMES
    if _COUNTRY_NAMES is None:
        names = set()
        try:
            import scraper
            names.update(scraper.COUNTRY_CODE_MAP.values())
        except Exception:  # noqa: BLE001 - the audit must work without the scraper
            pass
        names.update({
            "USA", "US", "UK", "United States", "United States of America", "International",
            "Columbia", "Turkyie", "Türkiye", "Korea", "South Korea", "North Korea",
            "Czech Republic", "Ivory Coast", "Cape Verde", "Latin America", "Arab World",
            "Caribbean",
        })
        _COUNTRY_NAMES = {norm_key(name) for name in names if name}
    return _COUNTRY_NAMES


def region_labels() -> set[str]:
    """Group names this module generates for a world region."""
    return set(COUNTRY_REGION.values()) | {INTERNATIONAL}


def is_country_group(cleaned: str) -> bool:
    """True when a group-title is really a region ("Italy", "日本 Japan").

    A region this module assigned ("United States", "Europe") is left alone:
    folding it into International would call American channels international.
    """
    whole = norm_key(cleaned)
    if whole in {norm_key(label) for label in region_labels()}:
        return False
    keys = country_names()
    if whole in keys:
        return True
    tokens = [norm_key(token) for token in cleaned.split()]
    return bool(tokens) and all(token in keys for token in tokens)


def normalize_group(raw: str) -> str:
    """Normalise an inherited group-title, or '' when it carries no information."""
    cleaned = clean_group(raw)
    if not cleaned:
        return ""
    key = norm_key(cleaned)
    if key in GENERIC_GROUP_KEYS:
        return ""
    if is_country_group(cleaned):
        return INTERNATIONAL
    lowered = cleaned.lower()
    if lowered in GROUP_SYNONYMS:
        return GROUP_SYNONYMS[lowered]
    if key in GROUP_SYNONYMS:
        return GROUP_SYNONYMS[key]

    # "Tv • Series 📺" -> "Series", "Music • Stingray" -> "Music",
    # "Culture Education" -> "Culture", "Terror & Sci-Fi" -> "Movies".
    tokens = [token for token in cleaned.split() if token]
    for token in tokens:
        mapped = CANONICAL_TOKENS.get(norm_key(token))
        if mapped:
            return mapped
    return cleaned


# --------------------------------------------------------------------------- #
# Classification
# --------------------------------------------------------------------------- #
_COUNTRY_CODES: dict[str, str] | None = None


def country_code_map() -> dict[str, str]:
    """Country name -> ISO code, built from the scraper's own table."""
    global _COUNTRY_CODES
    if _COUNTRY_CODES is None:
        codes: dict[str, str] = {}
        try:
            import scraper
            for code, name in scraper.COUNTRY_CODE_MAP.items():
                codes.setdefault(norm_key(name), code)
        except Exception:  # noqa: BLE001
            pass
        _COUNTRY_CODES = codes
    return _COUNTRY_CODES


def country_code(tvg_id: str = "", country: str = "") -> str:
    """Two-letter country code for a channel ('KosTV.gr@SD' -> 'gr')."""
    text = (country or "").strip()
    if len(text) == 2 and text.isalpha():
        return text.lower()
    match = re.search(r"\.([a-z]{2})(?:@|$)", (tvg_id or "").strip(), re.IGNORECASE)
    if match:
        return match.group(1).lower()
    if text:
        key = norm_key(text)
        if key in ("international", "unknown", "world", "global", "various"):
            return ""
        return country_code_map().get(key, "")
    return ""


def region_for(tvg_id: str = "", country: str = "") -> str:
    """World region for a channel, used when nothing else identifies its genre."""
    return COUNTRY_REGION.get(country_code(tvg_id, country), "")


def classify(name: str, group: str = "", tvg_id: str = "", url: str = "",
             country: str = "") -> str:
    """Return the category for one channel.

    The channel name decides first - that is what puts NFL Network in Sports
    instead of the "TV" bucket the index shipped it in. The inherited group is
    only consulted when the name is not recognisable.
    """
    name_text = _words(name)
    id_text = _words(tvg_id.replace(".", " ").replace("@", " "))

    # 1. Curated categories, most specific first.
    if PBS.search(name_text) or (tvg_id and PBS.search(id_text)):
        return "PBS"
    if GAME_SHOWS.search(name_text):
        return "Game Shows"
    if CARTOONS.search(name_text):
        return "Cartoons"
    if NBC_SPORTS.search(name_text):
        return "NBC Sports Channels"
    if SPORTS.search(name_text) or (tvg_id and SPORTS.search(id_text)):
        return "Sports"
    if LIFESTYLE.search(name_text):
        return "Lifestyle"
    if NBC_FAMILY.search(name_text):
        return "NBC"
    if CBS_FAMILY.search(name_text):
        return "CBS"
    if FOX_FAMILY.search(name_text):
        return "Fox Channels"

    # 2. Recognisable brands in the long tail.
    for label, pattern in BRAND_GROUPS:
        if pattern.search(name_text):
            return label

    # 3. The inherited group can still be a curated one ("Sports 🌍",
    #    "Animation;Kids") even when the channel name is not recognisable.
    group_text = _words(group)
    if group_text.strip():
        if PBS.search(group_text):
            return "PBS"
        if GAME_SHOWS.search(group_text):
            return "Game Shows"
        if CARTOONS.search(group_text):
            return "Cartoons"
        if NBC_SPORTS.search(group_text):
            return "NBC Sports Channels"
        if SPORTS.search(group_text):
            return "Sports"
        if LIFESTYLE.search(group_text):
            return "Lifestyle"

    # 4. The inherited group, when it says something else useful.
    normalized = normalize_group(group)
    if normalized:
        return normalized

    # 5. What the other indexes that publish this channel call it.
    vote = lookup_group_vote(name)
    if vote:
        return vote

    # 6. Nothing identified it: fall back to where in the world it broadcasts,
    #    which beats one enormous "Other" bucket in a player.
    return region_for(tvg_id, country) or OTHER


def clean_display_name(name: str) -> str:
    """One stable display name for a channel: drop the quality/duplicate tags."""
    text = (name or "").strip()
    previous = None
    while previous != text:
        previous = text
        text = _NOISE_PARENS.sub(" ", text)
        text = _NOISE_BRACKETS.sub(" ", text).strip()
    text = re.sub(r"\s{2,}", " ", text)
    return text or (name or "").strip()


def quality_score(name: str) -> int:
    """Higher is better: used to pick which duplicate becomes the main link."""
    lowered = (name or "").lower()
    score = 0
    for token, value in _RESOLUTION_SCORE:
        if token in lowered:
            score = max(score, value)
    if "hd" in lowered:
        score += 1
    if re.search(r"\b(alt|backup|mirror|feed ?\d|link ?\d)\b", lowered):
        score -= 2
    return score


def channel_key(name: str, country: str = "") -> str:
    """Identity of a channel across duplicate links."""
    return f"{norm_key(clean_display_name(name))}|{(country or '').strip().upper()}"


def backup_group(category: str) -> str:
    """The companion group holding the spare links for a category."""
    return f"{category}{BACKUP_SUFFIX}"


def is_backup_group(category: str) -> bool:
    return category.endswith(BACKUP_SUFFIX)


def base_category(category: str) -> str:
    return category[: -len(BACKUP_SUFFIX)] if is_backup_group(category) else category


def is_canonical_group(raw: str) -> bool:
    """True when ``raw`` is a label this module itself would write.

    Used by the offline tools (``rebuild_playlists.py``, ``resort_playlists.py``,
    ``verify_playlists.py``) to tell "already published in the taxonomy" from
    "still carrying an upstream dumping ground". ``General``, ``Undefined``,
    ``Tv • Series 📺`` and ``Italy 🇮🇹`` are not canonical; ``Sports``,
    ``Sports Backups``, ``United States`` and ``Other`` are.

    The test runs on the base of the label, because ``normalize_group`` folds a
    compound group onto its first recognised token (``"Kids Backups"`` would
    normalise to ``"Kids"``) - the `` Backups`` half is this module's own doing,
    so it is taken apart before the label is judged.
    """
    group = (raw or "").strip()
    if not group:
        return False
    base = base_category(group)
    if is_backup_group(group) and backup_group(base) != group:
        return False  # "Sports Backups Extra" is not a group this module writes
    if base in CURATED_CATEGORIES or base in {OTHER, INTERNATIONAL}:
        return True
    if base in region_labels():
        return True
    return normalize_group(base) == base


def needs_normalization(raw: str) -> bool:
    """True when a group-title has to be re-classified before it is published."""
    return not is_canonical_group(raw)


# --------------------------------------------------------------------------- #
# Applying the taxonomy to channels
# --------------------------------------------------------------------------- #
def _get(channel, attr: str) -> str:
    value = getattr(channel, attr, None)
    return value if isinstance(value, str) else ""


def category_of(channel) -> str:
    """The taxonomy category already assigned to a channel ('' when not yet set)."""
    value = getattr(channel, "category", "")
    return value if isinstance(value, str) and value else ""


def assign_categories(channels: list) -> None:
    """Set ``group-title`` on every channel in place, using the taxonomy.

    The result is remembered on the channel as ``.category`` so a second pass
    (the backup split, a re-order) cannot re-interpret an assigned category as
    if it were the raw group the upstream index shipped.
    """
    for channel in channels:
        name = _get(channel, "name")
        group = (channel.attrs.get("group-title", "") if hasattr(channel, "attrs") else "") or ""
        tvg_id = (channel.attrs.get("tvg-id", "") if hasattr(channel, "attrs") else "") or ""
        channel.category = classify(name, group, tvg_id,
                                    _get(channel, "url"), country_of(channel))
        channel.attrs["group-title"] = channel.category


def country_of(channel) -> str:
    """Best-effort country for a channel (used only to keep feeds apart)."""
    if hasattr(channel, "country"):
        try:
            return (channel.country or "").strip()
        except Exception:  # noqa: BLE001 - resolve_country can fail on odd metadata
            pass
    if hasattr(channel, "attrs"):
        return (channel.attrs.get("tvg-country", "") or "").strip()
    return ""


def split_primary_backups(channels: list, max_backups: int = 0) -> tuple[list, list]:
    """Split channels into (primary links, backup links).

    Channels that are the same station - same cleaned name and country - keep
    one entry in the main category; the spare links move to the matching
    "<category> Backups" group instead of cluttering the listing.
    """
    groups: dict[str, list] = collections.defaultdict(list)
    for channel in channels:
        groups[channel_key(_get(channel, "name"), country_of(channel))].append(channel)

    primary: list = []
    backups: list = []
    for members in groups.values():
        members = sorted(members, key=lambda ch: (-quality_score(_get(ch, "name")), _get(ch, "name")))
        main = members[0]
        main_category = category_of(main) or classify(
            _get(main, "name"), main.attrs.get("group-title", ""),
            main.attrs.get("tvg-id", ""), _get(main, "url"), country_of(main))
        main.category = main_category
        main.attrs["group-title"] = main_category
        primary.append(main)
        spares = members[1:]
        if max_backups:
            spares = spares[:max_backups]
        display = clean_display_name(_get(main, "name"))
        for index, spare in enumerate(spares, 1):
            spare.name = f"{display} (Backup {index})"
            spare.category = backup_group(main_category)
            spare.attrs["group-title"] = spare.category
            spare.attrs["tvg-id"] = main.attrs.get("tvg-id", spare.attrs.get("tvg-id", ""))
            spare.attrs["tvg-logo"] = main.attrs.get("tvg-logo", spare.attrs.get("tvg-logo", ""))
            backups.append(spare)
    return primary, backups


def build_main_order(channels: list, max_backups: int = 0) -> list:
    """Full curated ordering: category -> backups -> next category, long tail last."""
    assign_categories(channels)
    primary, backups = split_primary_backups(channels, max_backups=max_backups)
    ordered = order_channels(primary + backups)
    return ordered


def category_counts(channels: list) -> collections.Counter:
    counts: collections.Counter = collections.Counter()
    for channel in channels:
        counts[channel.attrs.get("group-title", OTHER)] += 1
    return counts


def order_categories(counts: collections.Counter) -> list[str]:
    """Group order for a playlist: curated (each with its backups), then the rest."""
    curated = {category: index for index, category in enumerate(CURATED_CATEGORIES)}
    order: list[str] = []

    def push(category: str) -> None:
        order.append(category)
        backup = backup_group(category)
        if counts.get(backup):
            order.append(backup)

    for category in CURATED_CATEGORIES:
        if counts.get(category) or counts.get(backup_group(category)):
            push(category)

    tail = [
        category for category in counts
        if category not in curated and not is_backup_group(category) and category != OTHER
    ]
    for category in sorted(tail, key=lambda item: (-counts[item], item.lower())):
        push(category)

    if counts.get(OTHER) or counts.get(backup_group(OTHER)):
        push(OTHER)
    return order


def order_key_for(channels: list):
    """The published order as a key function for ``channels`` and its siblings.

    ``order_channels`` is the contract every playlist is written in: the groups
    of *this* set in ``order_categories`` order (curated categories first, each
    followed by its own Backups group, then the long tail by size, ``Other``
    last), then the channel name, then the URL. Exposing the key separately lets
    a caller keep a second list in step with the channels - the block lists of
    ``link_check.py`` and ``resort_playlists.py`` are exactly that - without
    inventing a second, subtly different order.
    """
    counts = category_counts(channels)
    order = order_categories(counts)
    rank = {category: index for index, category in enumerate(order)}

    def key(channel) -> tuple:
        attrs = getattr(channel, "attrs", None)
        # Exactly the value category_counts() keys on, so every group present in
        # the playlist has a rank in order_categories() and nothing sorts adrift.
        group = attrs.get("group-title", OTHER) if isinstance(attrs, dict) else OTHER
        return (rank.get(group, len(rank)),
                norm_text(_get(channel, "name")),
                _get(channel, "url"))

    return key


def order_channels(channels: list) -> list:
    """Sort channels into the published group order, then by name within a group."""
    return sorted(channels, key=order_key_for(channels))


def sort_key(channel):
    """Drop-in replacement for ``scraper.sort_key`` that honours the taxonomy."""
    category = channel.attrs.get("group-title", OTHER) if hasattr(channel, "attrs") else OTHER
    base = base_category(category)
    if base in CURATED_CATEGORIES:
        rank = (0, CURATED_CATEGORIES.index(base))
    elif base == OTHER:
        rank = (2, 0)
    else:
        rank = (1, 0)
    return (rank, is_backup_group(category), norm_text(_get(channel, "name")), _get(channel, "url"))


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _load(paths: list[str]) -> list:
    import scraper
    channels: list = []
    for raw in paths:
        path = Path(raw)
        if not path.is_file():
            print(f"missing playlist: {path}", file=sys.stderr)
            continue
        parsed, _ = scraper.parse_m3u(path.read_text(encoding="utf-8", errors="replace"),
                                      path.stem)
        channels.extend(parsed)
    return channels


DEFAULT_CORPUS = ("playlists/PremiumTV_all.m3u", "playlists/sources/*.m3u")


def load_corpus(patterns=DEFAULT_CORPUS) -> dict:
    """Learn group votes from every index the repository keeps a copy of."""
    import glob
    corpus: list = []
    for pattern in patterns:
        for match in sorted(glob.glob(pattern)):
            corpus.extend(_load([match]))
    votes = build_group_votes(corpus)
    set_group_votes(votes)
    return votes


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit playlist categories.")
    parser.add_argument("playlists", nargs="*", default=["playlists/PremiumTV.m3u"],
                        help="M3U files to audit (default: playlists/PremiumTV.m3u)")
    parser.add_argument("--show", type=int, default=25,
                        help="how many groups to print (0 for all)")
    parser.add_argument("--sample", type=int, default=0,
                        help="print N example channels per group")
    parser.add_argument("--no-corpus", action="store_true",
                        help="do not learn categories from the local corpus")
    args = parser.parse_args(argv)

    channels = _load(args.playlists)
    if not channels:
        print("no channels found", file=sys.stderr)
        return 1
    if not args.no_corpus:
        load_corpus()

    ordered = build_main_order(channels)
    counts = category_counts(ordered)
    order = order_categories(counts)
    print(f"{len(channels)} entries -> {len(ordered)} published "
          f"({sum(counts[c] for c in counts if is_backup_group(c))} backups)")
    print(f"groups in published order ({len(order)}):\n")
    shown = order if not args.show else order[: args.show]
    for index, category in enumerate(shown, 1):
        print(f"{index:>3}. {category:<28} {counts[category]:>6}")
        if args.sample:
            for channel in ordered:
                if channel.attrs.get("group-title") == category:
                    print(f"       - {channel.name}")
                    args.sample -= 1
                    if args.sample <= 0:
                        break
    if args.show and len(order) > args.show:
        print(f"... and {len(order) - args.show} more groups")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
