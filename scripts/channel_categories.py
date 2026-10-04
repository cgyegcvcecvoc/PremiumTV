#!/usr/bin/env python3
"""Canonical channel categories and deterministic playlist ordering.

Upstream playlists carry hundreds of different ``group-title`` values - "General",
"Undefined", "Tv \u2022 Series \U0001f4fa", "Italy \U0001f1ee\U0001f1f9", "VOD Italy", "Sports \U0001f30d" -
so a player shows a long, inconsistent list and the same kind of channel is
scattered over several groups. This module collapses every channel into one of a
small, fixed set of categories and orders the result the same way on every run:

    TV            general / basic TV, catch-all live channels
    Local TV      local broadcast stations (kept separate: see epg_build.py)
    Cartoons      cartoons, animation, kids and family channels
    Sports        all sports, motorsport, hunting/fishing and outdoor sport
    News          news, business news and legislative channels
    Movies        films, cinema and movie FAST channels
    Series        drama, telenovelas and series channels
    Documentary   documentary, history, nature, science and true crime
    Entertainment comedy, reality, talk and general entertainment
    Music         music and music-video channels
    Lifestyle     food, travel, home, health, fashion and outdoor lifestyle
    Religious     religious channels
    Education     education, learning and culture
    Shopping      shopping and teleshopping
    Weather       weather channels
    Other         nothing else fits

Within a category the order is: US channels first, then UK, Canada, Australia,
Ireland and New Zealand, then every other country alphabetically, with channels
from unknown countries ("International") last. Inside one country the channels
are ordered by display name, with the different feeds of the same channel next
to each other and the highest quality first. This is the ordering every
published playlist uses, and the same ``sort_key`` is reused by the deep link
checker and the re-sort/verify tools, so a playlist can never be in a different
order than the report that describes it.

Pure standard library and no imports from the scraper, so it can be reused by
the scraper, the link checker, the re-sort tool and the tests without cycles.
"""
from __future__ import annotations

import re
import unicodedata

# --------------------------------------------------------------------------- #
# Categories
# --------------------------------------------------------------------------- #
# The order here is the order the categories appear in every playlist.
CATEGORY_ORDER: tuple[str, ...] = (
    "TV",
    "Local TV",
    "Cartoons",
    "Sports",
    "News",
    "Movies",
    "Series",
    "Documentary",
    "Entertainment",
    "Music",
    "Lifestyle",
    "Religious",
    "Education",
    "Shopping",
    "Weather",
    "Other",
)
CATEGORY_RANK: dict[str, int] = {name: index for index, name in enumerate(CATEGORY_ORDER)}
DEFAULT_CATEGORY = "TV"
OTHER_CATEGORY = "Other"

# Country display order inside every category. The repository's audience is
# primarily US/English-language, so those markets lead; everything else follows
# alphabetically by country name.
COUNTRY_PRIORITY: dict[str, int] = {
    "usa": 0, "united states": 0, "us": 0, "america": 0,
    "uk": 1, "gb": 1, "united kingdom": 1, "great britain": 1,
    "canada": 2, "ca": 2,
    "australia": 3, "au": 3,
    "ireland": 4, "ie": 4,
    "new zealand": 5, "nz": 5,
}
NON_COUNTRY_BUCKETS = {"", "international", "other", "unknown", "global", "world", "undefined"}
UNRANKED_COUNTRY_RANK = 10
LAST_COUNTRY_RANK = 90


def country_rank(country: str) -> tuple[int, str]:
    """Sort order for a country: known markets first, unknown/"International" last."""
    key = re.sub(r"[^a-z ]", "", (country or "").strip().lower()).strip()
    if key in NON_COUNTRY_BUCKETS:
        return (LAST_COUNTRY_RANK, "")
    if key in COUNTRY_PRIORITY:
        return (COUNTRY_PRIORITY[key], key)
    return (UNRANKED_COUNTRY_RANK, key)


# --------------------------------------------------------------------------- #
# Aliases: upstream group names -> canonical category
# --------------------------------------------------------------------------- #
# First the group tokens that map to something specific. A group like
# "Local;USA" or "Animation;Kids" is split on ; / | and each token is looked up,
# so a compound group still lands in the right category.
GROUP_ALIASES: dict[str, str] = {
    # local stations (the word "local" is also used by epg_build.py)
    "local": "Local TV",
    "local tv": "Local TV",
    "local channels": "Local TV",
    "locals": "Local TV",
    "regional": "Local TV",
    # cartoons / kids
    "kids": "Cartoons",
    "kid": "Cartoons",
    "children": "Cartoons",
    "cartoon": "Cartoons",
    "cartoons": "Cartoons",
    "animation": "Cartoons",
    "animated": "Cartoons",
    "anime": "Cartoons",
    "junior": "Cartoons",
    "family": "Cartoons",
    "kids tv": "Cartoons",
    # sports
    "sport": "Sports",
    "sports": "Sports",
    "sport tv": "Sports",
    "live sports": "Sports",
    "sports news": "Sports",
    "motorsport": "Sports",
    "motor sport": "Sports",
    "hunt and fishing": "Sports",
    "hunting and fishing": "Sports",
    "outdoor sports": "Sports",
    # news
    "news": "News",
    "noticias": "News",
    "business": "News",
    "business news": "News",
    "finance": "News",
    "legislative": "News",
    "politics": "News",
    "weather": "Weather",
    "meteo": "Weather",
    # movies / series
    "movies": "Movies",
    "movie": "Movies",
    "films": "Movies",
    "film": "Movies",
    "cinema": "Movies",
    "cine": "Movies",
    "vod": "Movies",
    "vod movies": "Movies",
    "movie zone": "Movies",
    "series": "Series",
    "tv series": "Series",
    "drama": "Series",
    "dramas": "Series",
    "novelas": "Series",
    "telenovelas": "Series",
    "soap": "Series",
    # documentary
    "documentary": "Documentary",
    "documentaries": "Documentary",
    "documentary history": "Documentary",
    "docs": "Documentary",
    "history": "Documentary",
    "nature": "Documentary",
    "animals": "Documentary",
    "animals and nature": "Documentary",
    "science": "Documentary",
    "culture": "Documentary",
    "discovery": "Documentary",
    "crime": "Documentary",
    "true crime": "Documentary",
    "investigation": "Documentary",
    "doc and history": "Documentary",
    # entertainment
    "entertainment": "Entertainment",
    "comedy": "Entertainment",
    "reality": "Entertainment",
    "talk": "Entertainment",
    "game shows": "Entertainment",
    "classic": "TV",
    "classic tv": "TV",
    "priority": "TV",
    "live events": "TV",
    # music
    "music": "Music",
    "music videos": "Music",
    "radio": "Music",
    "concerts": "Music",
    # lifestyle
    "lifestyle": "Lifestyle",
    "lifestyles": "Lifestyle",
    "lifestyles and travel": "Lifestyle",
    "travel": "Lifestyle",
    "cooking": "Lifestyle",
    "food": "Lifestyle",
    "home": "Lifestyle",
    "garden": "Lifestyle",
    "health": "Lifestyle",
    "fashion": "Lifestyle",
    "beauty": "Lifestyle",
    "outdoor": "Lifestyle",
    "shop": "Shopping",
    "shopping": "Shopping",
    "teleshopping": "Shopping",
    "religious": "Religious",
    "religion": "Religious",
    "education": "Education",
    "educational": "Education",
    "learning": "Education",
    "university": "Education",
    # general / catch-all groups
    "tv": "TV",
    "general": "TV",
    "general tv": "TV",
    "basic": "TV",
    "basic tv": "TV",
    "entertainment tv": "TV",
    "undefined": "TV",
    "other": "TV",
    "misc": "TV",
    "mixed": "TV",
    "variety": "TV",
    "channel": "TV",
    "channels": "TV",
    "24 7": "TV",
    "live": "TV",
    "digital tv": "TV",
    "online tv": "TV",
    "dltv": "TV",
    "global tv": "TV",
    "iptv": "TV",
}

# Group tokens that mean "unknown": fall through to the channel-name rules and
# finally to TV. Country/region group names land here too.
AMBIGUOUS_GROUPS = {
    "international", "global", "world", "arab world", "latin america", "europe",
    "asia", "africa", "north america", "south america", "caribbean", "middle east",
    "free tv", "public", "regional tv", "undefined tv", "hdtv", "hd", "sd", "fhd",
    "4k", "8k", "1080p", "720p", "480p", "vip", "premium", "backup", "test",
}

# --------------------------------------------------------------------------- #
# Channel-name keywords (used when the group is generic or missing)
# --------------------------------------------------------------------------- #
# (category, compiled regex) in priority order. Sports before news so
# "Sky Sports News" is a sports channel; weather before news for the same reason.
NAME_RULES: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (category, re.compile(pattern))
    for category, pattern in (
        ("Weather", r"weather|meteo|forecast|wetter"),
        ("Cartoons", (
            r"cartoon|toon(?:s)?\b|anime|animasi|animation|kids?\b|junior|juniors|"
            r"baby ?(?:tv|first)|boomerang|nick(?:elodeon|toons?|jr)|disney|"
            r"pokemon|pogo\b|chutti|duck ?tv|happy kids|tv ?okids|bambini|"
            r"teennick|cartoonito|kika\b|gulli|minika|baby ?tv|me ?tv ?toons|"
            r"family ?(?:tv|channel)|familia|familie|antena ?3|shorts ?tv|"
            r"yakari|piwi|nicktoons"
        )),
        ("Sports", (
            r"\bsport|espn|eurosport|dazn|bein|sky ?sport|fox ?sport|nba\b|nfl\b|"
            r"mlb\b|nhl\b|ufc\b|wwe\b|motogp|formula ?1|\bf1\b|nascar|indycar|"
            r"cricket|football|soccer|golf|tennis|boxing|fight|wrestling|olympic|"
            r"arena ?sport|willow|stadium|match ?(?:tv|day|centre|center)|"
            r"supersport|sportklub|sportv|premier ?sport|tsn\b|sportsnet|"
            r"olympiad|liga|bundesliga|premier ?league|la ?liga|serie ?a\b|"
            r"copa|champions ?(?:tv|league)|motorvision|speed ?tv|bike|surf|"
            r"fishing|hunting|outdoor ?channel|nfl ?network|golf ?channel"
        )),
        ("News", (
            r"\bnews|noticias|noticiero|actual(?:ite|ité)s?|nachrichten|"
            r"cnn\b|msnbc|fox ?news|sky ?news|bbc ?news|abc ?news|nbc ?news|"
            r"cbs ?news|euronews|france ?24|al ?jazeera|bloomberg|cnbc|"
            r"france ?info|dw\b|trt ?(?:world|haber)|ntv\b|haber|i24|wion|"
            r"newsmax|oann|gb ?news|ndtv|aaj ?tak|republic ?(?:tv|bharat)|"
            r"press ?tv|journal|tv5 ?monde|rai ?news|tgcom|rainews"
        )),
        ("Movies", (
            r"movie|movies|cinema|cinemax|\bfilms?\b|film4|hbo\b|starz|showtime|"
            r"tcm\b|tnt ?(?:film|movies)|sony ?movie|sky ?cinema|canal ?\+ ?cinema|"
            r"cine ?(?:max|polis|canal|latino|premier)|megacine|tcm ?cine|"
            r"paradise ?(?:tv|cinema)|action ?movies|horror|thriller|western|"
            r"moviesphere|filmrise|runtime|pluto ?tv ?movies"
        )),
        ("Series", (
            r"\bseries|telenovela|novelas?|soap ?(?:tv|opera)|drama|k-drama|"
            r"turca ?(?:tv|drama)|series ?tv"
        )),
        ("Documentary", (
            r"discovery|documentar|documental|\bdocs?\b|national ?geographic|"
            r"nat ?geo|animal ?planet|histoire|history|\bhistory\b|"
            r"investigation ?(?:discovery|id)|true ?crime|crime ?\+|crime ?&|"
            r"science|smithsonian|\bnat ?geo ?wild|wild\b|nature|voyage|"
            r"planet ?(?:earth|wild)|curiosity|timeline|pbs ?(?:america|nature)"
        )),
        ("Music", (
            r"\bmusic|\bmtv\b|vevo|vh1|\bmuch\b|trace ?(?:tv|urban)|stingray|"
            r"deluxe ?music|now ?(?:80s|90s|rock)|clubland|hits ?(?:tv)?|"
            r"kerrang|box ?(?:music|hits)|radio|4music|the ?box|magic ?tv|"
            r"music ?choice|mcm\b|nrj ?hits|c ?star|clubbing ?tv|remeber"
        )),
        ("Religious", (
            r"\bgod\b|jesus|christ|bible|gospel|church|catholic|christian|"
            r"islam|quran|koran|hindu|sikh|buddh|sat ?7|ewtn|daystar|\btbn\b|"
            r"hope ?(?:channel|tv)|faith|preach|salvation|religious|islamic|"
            r"makkah|madinah|iqraa|risala|mecca"
        )),
        ("Shopping", r"\bshop|qvc\b|\bhsn\b|telemarket|teleshop|home ?shopping|juwelo|"
                     r"gem ?(?:shopping|tv)|the ?store|teleshopping"),
        ("Education", r"education|educational|\blearn|school|university|academy|"
                      r"khan ?academy|\bted\b|classroom|curso|tutorial"),
        ("Lifestyle", (
            r"\bfood|kitchen|cooking|recipe|gourmet|\btravel|traveling|"
            r"home ?(?:tv|garden|improvement)|garden|\bhgtv\b|diy\b|fashion|"
            r"beauty|style|\bhealth|fit(?:ness)?\b|yoga|wellness|"
            r"auto ?(?:motor|show)|\bcars?\b|motor ?(?:trend|vision)|"
            r"\bmen'?s\b|\bwomen'?s\b|wedding|pet ?(?:tv)?|countryfile"
        )),
        ("Entertainment", (
            r"entertainment|comedy|reality|game ?show|talk ?(?:show|tv)|gossip|"
            r"\btlc\b|bravo|e! ?(?:tv)?|tru ?tv|comet ?tv|buzzr|conan|"
            r"just ?for ?laughs|fail ?army|people ?are ?awesome|tmz|inside ?edition"
        )),
    )
)

# --------------------------------------------------------------------------- #
# Name cleanup and ordering helpers
# --------------------------------------------------------------------------- #
QUALITY_TOKENS: dict[str, int] = {
    "2160p": 6, "4k": 6, "uhd": 6,
    "1440p": 5, "2k": 5,
    "1080p": 4, "1080i": 4, "fhd": 4, "full hd": 4,
    "720p": 3, "hd": 3,
    "576p": 2, "540p": 2,
    "480p": 1, "360p": 1, "240p": 1, "sd": 1,
}
# Parenthesised/bracketed markers that describe the feed rather than the
# channel: they are used for ordering but hidden from the sort key so every
# feed of a channel sits together.
FEED_MARKER_RE = re.compile(
    r"[\(\[\{]\s*(?:"
    r"2160p|1440p|1080[pi]|720p|576p|540p|480p|360p|240p|4k|8k|uhd|fhd|full ?hd|hd|sd|"
    r"alt|alternative|alt ?feed|backup|back ?up|mirror|test|temp|temporary|"
    r"feed ?\d*|link ?\d*|source ?\d*|server ?\d*|option ?\d*|stream ?\d*|"
    r"multiplex|mux|redundant|unstable|stable|not ?24 ?7|24 ?7"
    r")\s*[\)\]\}]",
    re.IGNORECASE,
)
BARE_FEED_MARKER_RE = re.compile(
    r"(?:^|[\s\-–|])(?:backup|mirror|alt(?:ernative)?|\(?\d{3,4}p\)?|fhd|uhd|4k|"
    r"1080[pi]|720p|480p|576p|540p|sd|hd)(?=$|[\s\-–|])",
    re.IGNORECASE,
)
MULTISPACE_RE = re.compile(r"\s{2,}")
NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
COUNTRY_SUFFIX_RE = re.compile(r"\b(?:us|usa|uk|gb|ca|au|ie|nz|(?:[a-z]{2}))\s*$", re.IGNORECASE)


def strip_accents(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value or "")
    return "".join(ch for ch in decomposed if not unicodedata.combining(ch))


def quality_rank(*values: str) -> int:
    """Highest resolution marker found in the given strings (0 when unknown)."""
    best = 0
    for value in values:
        if not value:
            continue
        text = strip_accents(str(value)).lower()
        for token, rank in QUALITY_TOKENS.items():
            if re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", text):
                best = max(best, rank)
        match = re.search(r"(?<!\d)(\d{3,4})p(?![a-z0-9])", text)
        if match:
            height = int(match.group(1))
            best = max(best, 5 if height >= 1440 else 4 if height >= 1080 else
                       3 if height >= 720 else 2 if height >= 540 else 1)
    return best


def display_name(name: str) -> str:
    """Clean a channel name without changing what it identifies.

    Only feed/quality markers are removed ("CNN (1080p)" -> "CNN"), plus
    duplicated whitespace. Region, feed and language labels ("(US East)",
    "(Brazil)", "en Español") are kept - they are part of the channel identity.
    """
    text = (name or "").replace("\u00a0", " ").strip()
    text = MULTISPACE_RE.sub(" ", text)
    cleaned = FEED_MARKER_RE.sub(" ", text)
    cleaned = MULTISPACE_RE.sub(" ", cleaned).strip(" -–|,").strip()
    return cleaned or text or "Unnamed channel"


def sort_name(name: str) -> str:
    """Case/accent-insensitive sort key with feed markers and duplicates removed."""
    text = display_name(name)
    text = FEED_MARKER_RE.sub(" ", text)
    text = BARE_FEED_MARKER_RE.sub(" ", text)
    text = strip_accents(text).lower()
    text = NON_ALNUM_RE.sub("", text)
    return text or strip_accents(name or "").lower()


def group_tokens(group: str) -> list[str]:
    """Split a group title into lowercase tokens ("Local;USA" -> local, usa)."""
    text = strip_accents(group or "").lower()
    text = re.sub(r"[^\w\s;&/|+-]", " ", text)
    tokens: list[str] = []
    for chunk in re.split(r"[;&/|]+", text):
        token = MULTISPACE_RE.sub(" ", chunk).strip(" -_+")
        if token:
            tokens.append(token)
    return tokens or [""]


def keyword_category(text: str) -> str | None:
    """First category whose name keyword matches, or None."""
    haystack = strip_accents(text or "").lower()
    if not haystack:
        return None
    for category, pattern in NAME_RULES:
        if pattern.search(haystack):
            return category
    return None


def canonical_group(name: str, group: str = "", tvg_id: str = "", country: str = "") -> str:
    """Map any upstream group/name combination to one canonical category."""
    raw_group = (group or "").strip()
    tokens = group_tokens(raw_group)

    # 1. A specific upstream group wins outright.
    for token in tokens:
        mapped = GROUP_ALIASES.get(token)
        if mapped and mapped != "TV":
            return mapped

    # 2. The channel name is more reliable than a generic/country group.
    name_hint = keyword_category(f"{name} {tvg_id}")
    if name_hint:
        return name_hint

    # 3. Any specific group token (including compound groups like "Films + Series").
    for token in tokens:
        mapped = GROUP_ALIASES.get(token)
        if mapped:
            return mapped
        if token in AMBIGUOUS_GROUPS:
            continue
        # Unknown groups are usually a country/region ("Italy", "Arab World") or a
        # brand; try the group words as keywords, then fall through.
        hint = keyword_category(token)
        if hint:
            return hint

    # 4. Country group with no genre information: keep it as general TV.
    if raw_group and raw_group.lower() not in AMBIGUOUS_GROUPS:
        return DEFAULT_CATEGORY
    return DEFAULT_CATEGORY


def channel_category(channel) -> str:
    """Canonical category for a Channel-like object (name/attrs)."""
    attrs = getattr(channel, "attrs", {}) or {}
    return canonical_group(
        getattr(channel, "name", "") or "",
        attrs.get("group-title", "") or "",
        attrs.get("tvg-id", "") or "",
        attrs.get("tvg-country", "") or "",
    )


def channel_sort_key(channel) -> tuple:
    """Deterministic playlist order: category, country, name, quality, source, url."""
    attrs = getattr(channel, "attrs", {}) or {}
    name = getattr(channel, "name", "") or ""
    country = getattr(channel, "country", "") or attrs.get("tvg-country", "") or ""
    category = channel_category(channel)
    rank, country_key = country_rank(country)
    return (
        CATEGORY_RANK.get(category, CATEGORY_RANK[DEFAULT_CATEGORY]),
        rank,
        country_key,
        sort_name(name),
        -quality_rank(name, attrs.get("tvg-id", ""), getattr(channel, "url", "")),
        getattr(channel, "source", "") or "",
        getattr(channel, "url", "") or "",
    )


def apply_categories(channels: list) -> dict:
    """Rewrite every channel's ``group-title`` to its canonical category and sort.

    Returns ``{category: count}`` in category order. The caller decides which
    playlists this applies to: published player playlists are categorised,
    normalized source caches keep their upstream metadata untouched.
    """
    counts: dict[str, int] = {}
    for channel in channels:
        category = channel_category(channel)
        if category != (channel.attrs.get("group-title") or ""):
            channel.attrs["group-title"] = category
        counts[category] = counts.get(category, 0) + 1
    channels.sort(key=channel_sort_key)
    return {name: counts[name] for name in CATEGORY_ORDER if name in counts}


def category_counts(channels: list) -> dict:
    counts: dict[str, int] = {}
    for channel in channels:
        category = channel_category(channel)
        counts[category] = counts.get(category, 0) + 1
    return {name: counts[name] for name in CATEGORY_ORDER if name in counts}


def feed_key(channel) -> tuple:
    """Identity of 'the same channel' for feed capping: id first, else name+country."""
    attrs = getattr(channel, "attrs", {}) or {}
    tvg_id = (attrs.get("tvg-id") or "").strip().lower()
    country = (getattr(channel, "country", "") or "").strip().lower()
    if tvg_id:
        return ("id", tvg_id, country)
    return ("name", sort_name(getattr(channel, "name", "") or ""), country)


def cap_feeds(channels: list, limit: int = 3) -> list:
    """Keep at most ``limit`` feeds per channel, best quality first.

    ``limit <= 0`` keeps every stream. The input is expected to already be
    sorted; surviving feeds of a channel stay in place.
    """
    if limit <= 0:
        return list(channels)
    kept: list = []
    seen: dict[tuple, int] = {}
    for channel in channels:
        key = feed_key(channel)
        used = seen.get(key, 0)
        if used >= limit:
            continue
        seen[key] = used + 1
        kept.append(channel)
    return kept


def summarize(channels: list) -> dict:
    """Report helper: category counts plus the countries inside each category."""
    summary: dict[str, dict] = {}
    for channel in channels:
        category = channel_category(channel)
        bucket = summary.setdefault(category, {"count": 0, "countries": {}})
        bucket["count"] += 1
        country = getattr(channel, "country", "") or "International"
        bucket["countries"][country] = bucket["countries"].get(country, 0) + 1
    ordered: dict[str, dict] = {}
    for name in CATEGORY_ORDER:
        if name not in summary:
            continue
        item = summary[name]
        item["countries"] = dict(sorted(item["countries"].items(),
                                        key=lambda pair: (-pair[1], pair[0].lower()))[:12])
        ordered[name] = item
    return ordered
