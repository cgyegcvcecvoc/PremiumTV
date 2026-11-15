package com.premiumtv.app.data

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.LocationManager
import org.json.JSONObject
import kotlin.math.asin
import kotlin.math.cos
import kotlin.math.min
import kotlin.math.radians
import kotlin.math.sin
import kotlin.math.sqrt

/** One local station as published in playlists/local-channels.json (schema 2). */
data class LocalStation(
    val callsign: String,
    val network: String,
    val name: String,
    val city: String,
    val channelId: String,
    val url: String,
    val backupUrls: List<String> = emptyList(),
) {
    val label: String
        get() {
            val call = callsign.ifBlank { name.substringBefore(" (").trim() }
            return if (network.isBlank()) call else "$call · $network"
        }
}

/** A market is the unit a viewer is local to: a city with the stations it carries. */
data class LocalMarket(
    val id: String,
    val city: String,
    val state: String,
    val stateName: String,
    val latitude: Double,
    val longitude: Double,
    val stations: List<LocalStation>,
) {
    val label: String get() = "$city, $state"
}

/**
 * The viewer's answer to "where are you watching from?".
 *
 * A location fix only narrows a market (the document carries one point per
 * market and one per ZIP prefix); a ZIP is translated through the published
 * prefix table, and a state, city or country can be typed when location is
 * declined. Nothing is uploaded and nothing leaves the device.
 */
data class LocalSelection(
    val country: String = "US",
    val state: String = "",
    val zip: String = "",
    val city: String = "",
    val source: String = "",
) {
    val hasSelection: Boolean
        get() = country.isNotBlank() && (state.isNotBlank() || zip.isNotBlank() || city.isNotBlank())

    fun label(): String = when {
        city.isNotBlank() && state.isNotBlank() -> "$city, $state"
        zip.length >= 3 -> "ZIP $zip"
        state.isNotBlank() -> state
        country.isNotBlank() && country != "US" -> country
        else -> "Not set"
    }

    companion object {
        const val SOURCE_LOCATION = "location"
        const val SOURCE_ZIP = "zip"
        const val SOURCE_STATE = "state"
        const val SOURCE_CITY = "city"
        const val SOURCE_COUNTRY = "country"
    }
}

/** The parsed local-channel directory bundled with the app. */
class LocalDirectory internal constructor(val document: JSONObject) {

    private val markets: List<LocalMarket> = buildList {
        val array = document.optJSONArray("markets") ?: return@buildList
        for (index in 0 until array.length()) {
            val item = array.optJSONObject(index) ?: continue
            val stations = buildList {
                val stationArray = item.optJSONArray("stations") ?: return@buildList
                for (stationIndex in 0 until stationArray.length()) {
                    val station = stationArray.optJSONObject(stationIndex) ?: continue
                    add(
                        LocalStation(
                            callsign = station.optString("callsign"),
                            network = station.optString("network"),
                            name = station.optString("name"),
                            city = station.optString("city"),
                            channelId = station.optString("channel_id"),
                            url = station.optString("url"),
                            backupUrls = station.optJSONArray("backup_urls")?.let { backups ->
                                (0 until backups.length()).map { backups.optString(it) }
                            }.orEmpty(),
                        )
                    )
                }
            }
            if (stations.isEmpty()) continue
            add(
                LocalMarket(
                    id = item.optString("id"),
                    city = item.optString("city"),
                    state = item.optString("state").uppercase(),
                    stateName = item.optString("state_name", item.optString("state")),
                    latitude = item.optDouble("latitude", Double.NaN),
                    longitude = item.optDouble("longitude", Double.NaN),
                    stations = stations,
                )
            )
        }
    }

    private val zipPrefixes: Map<String, Triple<String, String, Pair<Double, Double>>> = buildMap {
        val array = document.optJSONArray("zip_prefixes") ?: return@buildMap
        for (index in 0 until array.length()) {
            val item = array.optJSONObject(index) ?: continue
            val prefix = item.optString("prefix")
            if (prefix.isBlank()) continue
            val point = item.optDouble("latitude", Double.NaN) to item.optDouble("longitude", Double.NaN)
            put(prefix, Triple(item.optString("state").uppercase(), item.optString("market"), point))
        }
    }

    private val zipRanges: List<Triple<String, String, String>> = buildList {
        val ranges = document.optJSONArray("zip_ranges") ?: return@buildList
        for (index in 0 until ranges.length()) {
            val range = ranges.optJSONArray(index) ?: continue
            if (range.length() < 3) continue
            add(Triple(range.optString(0), range.optString(1), range.optString(2)))
        }
    }

    private val countries: List<Pair<String, String>> = buildList {
        val list = document.optJSONArray("countries") ?: return@buildList
        for (index in 0 until list.length()) {
            val item = list.optJSONObject(index) ?: continue
            add(item.optString("code") to item.optString("name"))
        }
    }

    val stateCodes: List<String> = buildList {
        val states = document.optJSONArray("states") ?: return@buildList
        for (index in 0 until states.length()) {
            states.optJSONObject(index)?.optString("code")?.takeIf { it.isNotBlank() }?.let { add(it) }
        }
    }

    /** Every market city, for the dialog's "or pick a city" list. */
    val cityNames: List<Pair<String, String>> = markets
        .map { it.city to it.state }
        .distinct()
        .sortedWith(compareBy({ it.second }, { it.first.lowercase() }))

    val marketCount: Int get() = markets.size
    val stationCount: Int get() = markets.sumOf { it.stations.size }

    fun countryName(code: String): String =
        countries.firstOrNull { it.first.equals(code, ignoreCase = true) }?.second ?: code

    fun hasCountry(code: String): Boolean =
        countries.any { it.first.equals(code, ignoreCase = true) }

    /** The state a ZIP belongs to, from the per-prefix table first. */
    fun stateForZip(zip: String): String? {
        val digits = zip.filter { it.isDigit() }
        if (digits.length < 3) return null
        val prefix = digits.take(3)
        zipPrefixes[prefix]?.let { (state, _) -> if (state.isNotBlank()) return state }
        return zipRanges.firstOrNull { range -> prefix >= range.first && prefix <= range.second }?.third
    }

    /** The market a ZIP belongs to, or null when the prefix has none published. */
    fun marketForZip(zip: String): LocalMarket? {
        val digits = zip.filter { it.isDigit() }
        if (digits.length < 3) return null
        val prefix = digits.take(3)
        val id = zipPrefixes[prefix]?.second.orEmpty()
        if (id.isNotBlank()) markets.firstOrNull { it.id == id }?.let { return it }
        val point = zipPrefixes[prefix]?.third
        if (point != null && !point.first.isNaN()) {
            return nearestMarket(point.first, point.second, stateForZip(zip))
        }
        return null
    }

    /** The nearest published market to a coarse fix, optionally inside a state. */
    fun nearestMarket(latitude: Double, longitude: Double, state: String? = null): LocalMarket? {
        val wanted = state?.uppercase().orEmpty()
        var best: LocalMarket? = null
        var bestDistance = Double.MAX_VALUE
        for (market in markets) {
            if (market.latitude.isNaN() || market.longitude.isNaN()) continue
            if (wanted.isNotBlank() && market.state != wanted) continue
            val km = distanceKm(latitude, longitude, market.latitude, market.longitude)
            if (km < bestDistance) {
                bestDistance = km
                best = market
            }
        }
        return best
    }

    /**
     * The markets a selection points at.
     *
     * Resolving a ZIP resolves a *market* when the prefix has one; a state
     * alone returns every market PremiumTV publishes there, and a city narrows
     * that list.
     */
    fun marketsFor(selection: LocalSelection): List<LocalMarket> {
        if (selection.country.isNotBlank() && !hasCountry(selection.country)) return emptyList()
        val wantedState = selection.state.ifBlank { stateForZip(selection.zip).orEmpty() }.uppercase()
        val zipMarket = selection.zip.takeIf { it.isNotBlank() }?.let { marketForZip(it) }
        if (zipMarket != null && selection.city.isBlank()) return listOf(zipMarket)
        val wantedCity = selection.city.trim().lowercase()
        return markets.filter { market ->
            (wantedState.isBlank() || market.state == wantedState) &&
                (wantedCity.isBlank() || market.city.lowercase() == wantedCity) &&
                (zipMarket == null || market.id == zipMarket.id || wantedCity.isNotBlank())
        }.ifEmpty {
            if (wantedCity.isBlank() && zipMarket != null) listOf(zipMarket) else emptyList()
        }
    }

    /** All stations in the given markets, in market order. */
    fun stationsFor(selection: LocalSelection): List<LocalStation> =
        marketsFor(selection).flatMap { market -> market.stations }

    /**
     * The loaded channels that belong to the selected market(s).
     *
     * Identity is the published EPG id first (WGAL's ``NBC.us@WGAL`` is stable
     * across backup feeds) and the stream URL second, for stations published
     * without an id.
     */
    fun channelsFor(channels: List<Channel>, selection: LocalSelection): List<Channel> {
        val stations = stationsFor(selection)
        if (stations.isEmpty()) return emptyList()
        val byId = HashMap<String, Channel>()
        val byUrl = HashMap<String, Channel>()
        for (channel in channels) {
            if (channel.id.isNotBlank()) byId.putIfAbsent(channel.id, channel)
            byUrl.putIfAbsent(channel.url, channel)
        }
        val out = LinkedHashMap<String, Channel>()
        for (station in stations) {
            val channel = byId[station.channelId] ?: byUrl[station.url]
                ?: station.backupUrls.firstNotNullOfOrNull { byUrl[it] }
            if (channel != null) out.putIfAbsent(channel.url, channel)
        }
        return out.values.sortedWith(compareBy({ it.group.lowercase() }, { it.name.lowercase() }))
    }

    /**
     * A short, honest sentence about what the selection resolves to.
     *
     * A state with no carried affiliate says so instead of quietly showing
     * nothing; a market we carry lists itself.
     */
    fun summary(selection: LocalSelection): String {
        if (selection.country.isNotBlank() && !hasCountry(selection.country)) {
            return "Local stations are published for ${countries.joinToString(", ") { it.second }} so far."
        }
        if (stateForZip(selection.zip) == null && selection.zip.length >= 3 && selection.state.isBlank()) {
            return "That ZIP is not in the published US ZIP table. Check it, or enter a state instead."
        }
        val resolved = marketsFor(selection)
        if (resolved.isEmpty()) {
            val state = selection.state.ifBlank { stateForZip(selection.zip).orEmpty() }
            return when {
                selection.city.isNotBlank() ->
                    "No local station is published in ${selection.city}, ${state.ifBlank { "your area" }} yet."
                state.isNotBlank() -> "No local stations are published in $state yet."
                else -> "Enter a ZIP, state or city to see your local stations."
            }
        }
        val stations = resolved.sumOf { it.stations.size }
        val places = resolved.joinToString(", ") { it.label }
        return "$stations local station${if (stations == 1) "" else "s"} in $places."
    }

    private fun distanceKm(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Double {
        val radius = 6371.0
        val phi1 = radians(lat1)
        val phi2 = radians(lat2)
        val dPhi = phi2 - phi1
        val dLambda = radians(lon2 - lon1)
        val a = sin(dPhi / 2) * sin(dPhi / 2) + cos(phi1) * cos(phi2) * sin(dLambda / 2) * sin(dLambda / 2)
        return 2 * radius * asin(min(1.0, sqrt(a)))
    }
}

object LocalChannels {
    fun parse(text: String): LocalDirectory = LocalDirectory(JSONObject(text))
}

/** Reads the local-channel directory bundled beside the channel list. */
fun Context.readLocalChannelDirectory(): LocalDirectory? = try {
    assets.open("bundle/local-channels.json").bufferedReader().use { LocalChannels.parse(it.readText()) }
} catch (error: Exception) {
    null
}

/**
 * A coarse last-known fix, when the viewer allowed location.
 *
 * Returns null when the permission is missing or no provider has a cached fix,
 * so the dialog can fall back to asking for a ZIP instead of blocking.
 */
fun Context.lastKnownCoordinates(): Pair<Double, Double>? {
    if (checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED &&
        checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
    ) {
        return null
    }
    val manager = getSystemService(Context.LOCATION_SERVICE) as? LocationManager ?: return null
    for (provider in listOf(LocationManager.NETWORK_PROVIDER, LocationManager.GPS_PROVIDER, LocationManager.PASSIVE_PROVIDER)) {
        val location = try {
            manager.getLastKnownLocation(provider)
        } catch (error: SecurityException) {
            null
        } catch (error: IllegalArgumentException) {
            null
        }
        if (location != null) return location.latitude to location.longitude
    }
    return null
}

/** Remembers the viewer's local-channel answer on this device only. */
class LocalChannelSettings(context: Context) {
    private val prefs = context.getSharedPreferences("premiumtv_local", Context.MODE_PRIVATE)

    fun selection(): LocalSelection = LocalSelection(
        country = prefs.getString("country", "US") ?: "US",
        state = prefs.getString("state", "") ?: "",
        zip = prefs.getString("zip", "") ?: "",
        city = prefs.getString("city", "") ?: "",
        source = prefs.getString("source", "") ?: "",
    )

    fun save(selection: LocalSelection) {
        prefs.edit()
            .putString("country", selection.country.uppercase())
            .putString("state", selection.state.uppercase())
            .putString("zip", selection.zip)
            .putString("city", selection.city)
            .putString("source", selection.source)
            .apply()
    }

    /** True until the viewer has answered or explicitly declined the question. */
    fun asked(): Boolean = prefs.getBoolean("asked", false)

    fun markAsked() {
        prefs.edit().putBoolean("asked", true).apply()
    }

    fun clear() {
        prefs.edit().clear().apply()
    }
}
