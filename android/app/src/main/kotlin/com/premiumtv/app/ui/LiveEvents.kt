package com.premiumtv.app.ui

import com.premiumtv.app.data.Channel

/*
 * Live games and multi-server playback, kept free of Compose so the parsing
 * and the server grouping can be unit tested on the JVM (the same pattern
 * GuideModel uses for the cable grid).
 *
 * The repository's scrapers publish game streams as ordinary playlist
 * entries named "[Sport] Team A vs. Team B | English (SOURCE)". They share
 * placeholder EPG ids ("Football.Dummy.us"), so everything the app can tell
 * a viewer about them lives in the name itself: the sport, the matchup and -
 * when the same game is published more than once - extra servers to fall
 * back to when one feed dies mid-game.
 */

/** One live game: the matchup, its sport label, and every stream carrying it. */
internal data class LiveEvent(
    val sport: String,
    val title: String,
    val servers: List<Channel>,
)

/** One sport heading of the Live Events screen and the games under it. */
internal data class LiveEventSection(
    val sport: String,
    val events: List<LiveEvent>,
)

private val BRACKET_TAG = Regex("""^\[([^\]]{2,48})]\s*(.*)$""")
private val VERSUS = Regex("""\s+vs\.?\s+""", RegexOption.IGNORE_CASE)
private val TRAILER = Regex("""\s*\|.*$""")
private val SOURCE_SUFFIX = Regex("""\s*\((?:STRMCNTR|[A-Z0-9]{3,14})\)\s*$""")
private val NON_ALNUM = Regex("""[^a-z0-9]+""")
private val PARENS = Regex("""\([^)]*\)""")

/** Canonical section labels, keyed by the playlist's own bracket tag. */
private val SPORT_LABELS = mapOf(
    "soccer" to "Soccer",
    "football" to "American Football",
    "american football" to "American Football",
    "nfl" to "American Football",
    "ncaaf" to "College Football",
    "college football" to "College Football",
    "nhl" to "NHL Hockey",
    "nhl hockey" to "NHL Hockey",
    "hockey" to "Hockey",
    "basketball" to "Basketball",
    "nba" to "NBA Basketball",
    "ncaa basketball" to "College Basketball",
    "mlb" to "MLB Baseball",
    "baseball" to "Baseball",
    "ufc" to "UFC / MMA",
    "mma" to "UFC / MMA",
    "boxing" to "Boxing",
    "wrestling" to "Wrestling",
    "golf" to "Golf",
    "tennis" to "Tennis",
    "f1" to "Formula 1",
    "nascar" to "NASCAR",
    "cricket" to "Cricket",
    "rugby" to "Rugby",
    "sports" to "Sports",
)

/** Football-league tags the scrapers use for soccer competitions. */
private val SOCCER_LEAGUES = setOf(
    "liga mx", "ligamx", "laliga", "la liga", "premier league", "epl", "mls",
    "bundesliga", "serie a", "ligue 1", "liga profesional", "liga 1",
    "champions league", "europa league", "copa", "eredivisie", "primeira liga",
    "saudi pro league", "world cup", "euros",
)

/** Section order on the Live Events screen; unlisted sports sort after these. */
private val SPORT_ORDER = listOf(
    "Soccer",
    "American Football",
    "College Football",
    "NHL Hockey",
    "Hockey",
    "Basketball",
    "NBA Basketball",
    "College Basketball",
    "MLB Baseball",
    "Baseball",
    "UFC / MMA",
    "Boxing",
)

private fun normKey(value: String): String =
    NON_ALNUM.replace(value.lowercase(), "").trim()

/**
 * The sport one event entry belongs to, or null when the name is not an
 * event. The placeholder ids the event feeds share ("Soccer.Dummy.us") are
 * the strongest hint; the bracket tag decides everywhere else.
 */
internal fun sportOfEvent(channel: Channel): String? {
    // Only the scrapers' placeholder ids are trustworthy hints ("Soccer.Dummy.us");
    // a real channel id that merely starts with "soccer" says nothing.
    val idPrefix = if (channel.id.contains(".Dummy.", ignoreCase = true)) {
        normKey(channel.id.substringBefore(".Dummy").substringBefore('.'))
    } else {
        ""
    }
    val fromId = when (idPrefix) {
        "soccer" -> "Soccer"
        "football" -> "American Football"
        "nhlhockey" -> "NHL Hockey"
        "ncaasports", "ncaa" -> "College Football"
        else -> null
    }
    val tag = BRACKET_TAG.find(channel.name)?.groupValues?.get(1)?.trim().orEmpty()
    if (tag.isEmpty()) return null
    val tagKey = normKey(tag)
    val fromTag = SPORT_LABELS[tagKey]
        ?: if (SOCCER_LEAGUES.contains(tag.lowercase().trim())) "Soccer" else null
    if (fromId != null) {
        // The id knows the discipline; the tag may only name the league.
        return if (fromTag == null || fromTag == "American Football" && fromId == "Soccer") fromId else fromTag
    }
    return fromTag ?: tag.trim()
}

/** One parsed game, or null when the channel name is not an event entry. */
internal data class ParsedEvent(val sport: String, val title: String, val key: String)

internal fun parseLiveEvent(channel: Channel): ParsedEvent? {
    val sport = sportOfEvent(channel) ?: return null
    val rest = BRACKET_TAG.find(channel.name)?.groupValues?.get(2).orEmpty()
    var title = TRAILER.replace(rest, "").trim()
    title = SOURCE_SUFFIX.replace(title, "").trim()
    val parts = VERSUS.split(title)
    if (parts.size < 2) return null
    val home = parts[0].trim()
    val away = parts.drop(1).joinToString(" vs. ").trim()
    if (home.isEmpty() || away.isEmpty()) return null
    val clean = "$home vs. $away"
    return ParsedEvent(sport, clean, "${normKey(sport)}|${normKey(home)}|${normKey(away)}")
}

/** True when this channel is one of the scraper's live-game entries. */
internal fun isLiveEventChannel(channel: Channel): Boolean = parseLiveEvent(channel) != null

/**
 * Every game in the playlist, grouped into sport sections and with each
 * game's duplicate feeds collected as its server list (playlist order kept,
 * identical URLs deduplicated).
 */
internal fun groupLiveEvents(channels: List<Channel>): List<LiveEventSection> {
    val events = LinkedHashMap<String, LiveEvent>()
    val servers = LinkedHashMap<String, MutableList<Channel>>()
    for (channel in channels) {
        val parsed = parseLiveEvent(channel) ?: continue
        val existing = events[parsed.key]
        if (existing == null) {
            events[parsed.key] = LiveEvent(parsed.sport, parsed.title, emptyList())
            servers[parsed.key] = mutableListOf(channel)
        } else {
            val list = servers.getValue(parsed.key)
            if (list.none { it.url == channel.url }) list.add(channel)
        }
    }
    if (events.isEmpty()) return emptyList()
    val assembled = events.map { (key, event) ->
        event.copy(servers = servers.getValue(key).toList())
    }
    return assembled
        .groupBy { it.sport }
        .map { (sport, list) -> sport to list.sortedBy { it.title.lowercase() } }
        .sortedWith(
            compareBy(
                { (sport, _) ->
                    val index = SPORT_ORDER.indexOf(sport)
                    if (index < 0) SPORT_ORDER.size else index
                },
                { (sport, _) -> sport.lowercase() },
            ),
        )
        .map { (sport, list) -> LiveEventSection(sport, list) }
}

/** Maps every event feed's URL to its game, for the "LIVE" labels. */
internal fun liveEventIndex(channels: List<Channel>): Map<String, LiveEvent> {
    val out = HashMap<String, LiveEvent>()
    for (section in groupLiveEvents(channels)) {
        for (event in section.events) {
            for (server in event.servers) out[server.url] = event
        }
    }
    return out
}

/**
 * The playable server list for a channel: the game's other feeds when it is
 * an event, otherwise the channel's backup feeds (same EPG id, same base
 * name - "Pluto TV Kids (Backup 1)" is the same channel as "Pluto TV Kids"),
 * with the selected feed moved to the front.
 */
internal fun serversFor(channel: Channel, channels: List<Channel>): List<Channel> {
    val event = liveEventIndex(channels)[channel.url]
    val pool = if (event != null) {
        event.servers
    } else {
        val base = baseDisplayName(channel.name)
        channels.filter {
            it.id == channel.id && it.id.isNotBlank() &&
                baseDisplayName(it.name) == base && it.url != channel.url
        }.let { backups -> listOf(channel) + backups }
    }
    val ordered = ArrayList<Channel>(pool.size)
    ordered.add(channel)
    for (candidate in pool) {
        if (candidate.url != channel.url && ordered.none { it.url == candidate.url }) {
            ordered.add(candidate)
        }
    }
    return ordered
}

/** "Pluto TV Kids (Spain) (720p)" -> "Pluto TV Kids": the name backups share. */
internal fun baseDisplayName(name: String): String {
    var text = name
    var previous: String
    do {
        previous = text
        text = PARENS.replace(text, " ")
    } while (text != previous)
    return text.replace(Regex("""\s{2,}"""), " ").trim().lowercase()
}
