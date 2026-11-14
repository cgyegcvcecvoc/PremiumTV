package com.premiumtv.app.data

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.LocationManager
import com.premiumtv.app.data.Channel
import org.json.JSONObject

/** One local station as published in playlists/local-channels.json. */
data class LocalStation(
    val callsign: String,
    val network: String,
    val name: String,
    val channelId: String,
    val url: String,
    val backupUrls: List<String> = emptyList(),
)

data class LocalMarket(
    val city: String,
    val state: String,
    val stateName: String,
    val stations: List<LocalStation>,
)

/**
 * The viewer's answer to "where are you watching from?".
 *
 * A location fix only narrows the state (the document has one centroid per
 * state); a ZIP is translated through the USPS prefix ranges, and a state or
 * country can be typed directly when location is declined. Nothing is uploaded.
 */
data class LocalSelection(
    val country: String = "US",
    val state: String = "",
    val zip: String = "",
    val city: String = "",
) {
    val hasSelection: Boolean get() = country.isNotBlank() && (state.isNotBlank() || zip.isNotBlank() || city.isNotBlank())

    fun label(): String = when {
        city.isNotBlank() && state.isNotBlank() -> "$city, $state"
        state.isNotBlank() -> state
        zip.isNotBlank() -> "ZIP $zip"
        country.isNotBlank() && country != "US" -> country
        else -> "Not set"
    }
}

/** The parsed local-channel directory bundled with the app. */
class LocalDirectory internal constructor(val document: JSONObject) {

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

    fun countryName(code: String): String =
        countries.firstOrNull { it.first.equals(code, ignoreCase = true) }?.second ?: code

    /** USPS prefix range lookup: the ZIP's first three digits decide the state. */
    fun stateForZip(zip: String): String? {
        val digits = zip.filter { it.isDigit() }
        if (digits.length < 3) return null
        val prefix = digits.take(3)
        return zipRanges.firstOrNull { range ->
            prefix >= range.first && prefix <= range.second
        }?.third
    }

    /** The nearest state that has a published station, from a coarse fix. */
    fun stateForLocation(latitude: Double, longitude: Double): String? {
        val states = document.optJSONArray("states") ?: return null
        var best: String? = null
        var bestDistance = Double.MAX_VALUE
        for (index in 0 until states.length()) {
            val state = states.optJSONObject(index) ?: continue
            val lat = state.optDouble("latitude", Double.NaN)
            val lon = state.optDouble("longitude", Double.NaN)
            if (lat.isNaN() || lon.isNaN()) continue
            val distance = (lat - latitude) * (lat - latitude) + (lon - longitude) * (lon - longitude)
            if (distance < bestDistance) {
                bestDistance = distance
                best = state.optString("code")
            }
        }
        return best
    }

    /** Every market in the selected state (or one city when the viewer named it). */
    fun marketsFor(selection: LocalSelection): List<LocalMarket> {
        val states = document.optJSONArray("states") ?: return emptyList()
        val wantedState = selection.state.ifBlank { stateForZip(selection.zip).orEmpty() }.uppercase()
        if (wantedState.isBlank()) return emptyList()
        val wantedCity = selection.city.trim().lowercase()
        val out = ArrayList<LocalMarket>()
        for (index in 0 until states.length()) {
            val state = states.optJSONObject(index) ?: continue
            val code = state.optString("code").uppercase()
            if (code != wantedState) continue
            val markets = state.optJSONArray("markets") ?: continue
            for (marketIndex in 0 until markets.length()) {
                val market = markets.optJSONObject(marketIndex) ?: continue
                val city = market.optString("city")
                if (wantedCity.isNotBlank() && !city.lowercase().contains(wantedCity)) continue
                val stations = ArrayList<LocalStation>()
                val stationArray = market.optJSONArray("stations") ?: continue
                for (stationIndex in 0 until stationArray.length()) {
                    val station = stationArray.optJSONObject(stationIndex) ?: continue
                    stations.add(
                        LocalStation(
                            callsign = station.optString("callsign"),
                            network = station.optString("network"),
                            name = station.optString("name"),
                            channelId = station.optString("channel_id"),
                            url = station.optString("url"),
                            backupUrls = station.optJSONArray("backup_urls")?.let { backups ->
                                (0 until backups.length()).map { backups.optString(it) }
                            }.orEmpty(),
                        )
                    )
                }
                if (stations.isNotEmpty()) {
                    out.add(LocalMarket(city, code, state.optString("name", code), stations))
                }
            }
        }
        return out
    }

    /**
     * The loaded channels that belong to the selected market(s).
     *
     * Identity is the published EPG id first (WGAL's ``NBC.us@WGAL`` is stable
     * across backup feeds) and the stream URL second, for stations published
     * without an id.
     */
    fun channelsFor(channels: List<Channel>, selection: LocalSelection): List<Channel> {
        val markets = marketsFor(selection)
        if (markets.isEmpty()) return emptyList()
        val byId = HashMap<String, Channel>()
        val byUrl = HashMap<String, Channel>()
        for (channel in channels) {
            if (channel.id.isNotBlank()) byId.putIfAbsent(channel.id, channel)
            byUrl.putIfAbsent(channel.url, channel)
        }
        val out = LinkedHashMap<String, Channel>()
        for (market in markets) {
            for (station in market.stations) {
                val channel = byId[station.channelId] ?: byUrl[station.url]
                    ?: station.backupUrls.firstNotNullOfOrNull { byUrl[it] }
                if (channel != null) out.putIfAbsent(channel.url, channel)
            }
        }
        return out.values.sortedWith(compareBy({ it.group.lowercase() }, { it.name.lowercase() }))
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
    )

    fun save(selection: LocalSelection) {
        prefs.edit()
            .putString("country", selection.country.uppercase())
            .putString("state", selection.state.uppercase())
            .putString("zip", selection.zip)
            .putString("city", selection.city)
            .apply()
    }

    fun clear() {
        prefs.edit().clear().apply()
    }
}
