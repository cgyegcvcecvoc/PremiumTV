package com.premiumtv.app.ui

import com.premiumtv.app.data.Channel
import java.text.SimpleDateFormat
import java.util.Locale
import java.util.TimeZone

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
 *
 * build_live_schedule.py publishes "playlists/live-schedule.json" (bundled
 * with the app data by build_bundle.py), mapping each matchup's stable key
 * to a kickoff instant (epoch seconds). Games whose kickoff is still in the
 * future show "Not live yet" with a countdown; games past kickoff with no
 * answering feed show "NO SIGNAL".
 */

/** One live game: the matchup, its sport label, and every stream carrying it. */
internal data class LiveEvent(
    val sport: String,
    val title: String,
    /** Stable identity of the matchup, shared by all of its servers. */
    val key: String,
    val servers: List<Channel>,
    /** Kickoff instant in epoch seconds, when the schedule knows it. */
    val kickoffUtc: Long? = null,
)

/** Parse "2026-10-22T16:45:00Z" to epoch seconds, or null when it cannot be parsed. */
internal fun parseKickoff(value: String?): Long? {
    if (value.isNullOrBlank()) return null
    return try {
        SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US).apply {
            timeZone = TimeZone.getTimeZone("UTC")
        }.parse(value)?.time?.let { it / 1000L }
    } catch (_: Exception) {
        null
    }
}

/** One sport heading of the Live Events screen and the games under it. */
internal data class LiveEventSection(
    val sport: String,
    val events: List<LiveEvent>,
)

private val BRACKET_TAG = Regex("""^\[([^\]]{2,48})]\s*(.*)$""")
private val VERSUS = Regex("""\s+vs\.?\s+""", RegexOption.IGNORE_CASE)
private val TRAILER = Regex("""\s*\|.*$""")
/** Source/backup markers the scrapers append to team names, removed wherever they appear. */
private val MARKERS = Regex("""\s*\((?:STRMCNTR|[A-Z0-9]{3,14}|[Bb]ackup(?:\s+\d{1,2})?|iSTRMEAST|FAWA)\)""")
private val FEED_COPY = Regex("""\s+\d{1,2}$""")
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
 * Team-name variants the scrapers use for the same club, normalized through
 * [normKey]. Applied before keying so "FC Lugano" vs "Lugano" or
 * "Crvena Zvezda vs F.C. København" vs "F.C. København vs Red Star Belgrade"
 * merge into a single game card instead of two.
 */
private val TEAM_ALIASES = mapOf(
    "fckbenhavn" to "fccopenhagen",
    "fclugano" to "lugano",
    "hapoelbeer" to "hapoelbeersheva",
    "mjallbyaif" to "mjallby",
    "royaleunionsg" to "unionstgilloise",
    "univcraiova" to "csucraiova",
    "interdescaldes" to "interescaldes",
    "staderennais" to "rennes",
    "fcnordsjaelland" to "nordsjaelland",
    "skbrann" to "brann",
    "rigafc" to "riga",
)

/** Norm key for one team, alias-collapsed so spelling variants match. */
internal fun teamKey(name: String): String =
    TEAM_ALIASES[normKey(name)] ?: normKey(name)

/** One team name with source/backup markers and feed-copy numbers stripped. */
private fun cleanTeam(name: String): String {
    var text = MARKERS.replace(name, " ").trim()
    text = TRAILER.replace(text, "").trim()
    text = FEED_COPY.replace(text, "").trim()
    return text.replace(Regex("""\s{2,}"""), " ").trim()
}

/** The sport one event entry belongs to, or null when the name is not an event. */
internal fun sportOfEvent(channel: Channel): String? {
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
        return if (fromTag == null || fromTag == "American Football" && fromId == "Soccer") fromId else fromTag
    }
    return fromTag ?: tag.trim()
}

/** One parsed game, or null when the channel name is not an event entry. */
internal data class ParsedEvent(val sport: String, val title: String, val key: String)

internal fun parseLiveEvent(channel: Channel): ParsedEvent? {
    val sport = sportOfEvent(channel) ?: return null
    val title = cleanTeam(
        BRACKET_TAG.find(channel.name)?.groupValues?.get(2).orEmpty()
    )
    val parts = VERSUS.split(title)
    if (parts.size < 2) return null
    val home = parts[0].trim()
    val away = parts.drop(1).joinToString(" vs. ").trim()
    if (home.isEmpty() || away.isEmpty()) return null
    val clean = "$home vs. $away"
    val teams = listOf(teamKey(home), teamKey(away)).sorted()
    return ParsedEvent(sport, clean, "${normKey(sport)}|${teams.first}|${teams.second}")
}

/** True when this channel is one of the scraper's live-game entries. */
internal fun isLiveEventChannel(channel: Channel): Boolean = parseLiveEvent(channel) != null

/**
 * Splits a matchup title into its two team names, in playlist order.
 *
 * "Arsenal vs. Chelsea" -> ("Arsenal", "Chelsea"). Returns null when the
 * title is not a two-team matchup (a boxing or UFC card, for instance, keeps
 * its full title on the card instead of team badges).
 */
internal fun teamsOf(title: String): Pair<String, String>? {
    val parts = VERSUS.split(title)
    if (parts.size < 2) return null
    val first = parts[0].trim()
    val second = parts.drop(1).joinToString(" vs. ").trim()
    if (first.isEmpty() || second.isEmpty()) return null
    return first to second
}

/**
 * Every game in the playlist, grouped into sport sections and with each
 * game's duplicate feeds collected as its server list (playlist order kept,
 * identical URLs deduplicated). Games whose keys appear in [schedule] are
 * annotated with their kickoff instant.
 */
internal fun groupLiveEvents(
    channels: List<Channel>,
    schedule: Map<String, Long> = emptyMap(),
): List<LiveEventSection> {
    val events = LinkedHashMap<String, LiveEvent>()
    val servers = LinkedHashMap<String, MutableList<Channel>>()
    for (channel in channels) {
        val parsed = parseLiveEvent(channel) ?: continue
        val existing = events[parsed.key]
        if (existing == null) {
            events[parsed.key] = LiveEvent(
                parsed.sport, parsed.title, parsed.key, emptyList(),
                schedule[parsed.key],
            )
            servers[parsed.key] = mutableListOf(channel)
        } else {
            val list = servers.getValue(parsed.key)
            if (list.none { it.url == channel.url }) list.add(channel)
        }
    }
    if (events.isEmpty()) return emptyList()
    val assembled = events.map { (key, event) ->
        event.copy(servers = servers.getValue(key).toList(), kickoffUtc = schedule[key])
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

/** How many seconds until [kickoffUtc], or null when it is in the past or unknown. */
internal fun secondsUntilKickoff(kickoffUtc: Long?, nowEpochSeconds: Long): Long? =
    kickoffUtc?.let { it - nowEpochSeconds }?.takeIf { it > 0 }
