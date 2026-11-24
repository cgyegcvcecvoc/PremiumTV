package com.premiumtv.app.data

import android.Manifest
import android.content.Context
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import android.os.Bundle
import android.os.Looper
import org.json.JSONObject
import java.text.Normalizer
import kotlinx.coroutines.suspendCancellableCoroutine
import kotlinx.coroutines.withTimeoutOrNull
import kotlin.coroutines.resume
import kotlin.math.PI
import kotlin.math.asin
import kotlin.math.cos
import kotlin.math.min
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

    /**
     * The market a ZIP belongs to, or null when no published market is inside
     * [LOCAL_MARKET_NEAR_KM] of the ZIP's area (1.1.21). The distance rule the
     * GPS path already applies applies here too: a Wilkes-Barre ZIP is not
     * Philadelphia just because Philadelphia is the nearest market in the state.
     */
    fun marketForZip(zip: String): LocalMarket? {
        val digits = zip.filter { it.isDigit() }
        if (digits.length < 3) return null
        val prefix = digits.take(3)
        val id = zipPrefixes[prefix]?.second.orEmpty()
        if (id.isNotBlank()) markets.firstOrNull { it.id == id }?.let { return it }
        val point = zipPrefixes[prefix]?.third
        if (point != null && !point.first.isNaN()) {
            val hit = nearestMarketWithDistance(point.first, point.second, stateForZip(zip))
            return hit?.takeIf { marketIsNear(it.second) }?.first
        }
        return null
    }

    /** The nearest published market to a coarse fix, optionally inside a state. */
    fun nearestMarket(latitude: Double, longitude: Double, state: String? = null): LocalMarket? =
        nearestMarketWithDistance(latitude, longitude, state)?.first

    /**
     * The nearest published market to a fix, with how far away it is in
     * kilometres, or null when no market has a position.
     *
     * The distance is not decoration. [LOCAL_MARKET_NEAR_KM] explains why.
     */
    fun nearestMarketWithDistance(
        latitude: Double,
        longitude: Double,
        state: String? = null,
    ): Pair<LocalMarket, Double>? {
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
        return best?.let { it to bestDistance }
    }

    /**
     * Every published market within [maxKm] of a fix, nearest first, each with
     * its distance in kilometres (1.1.19).
     *
     * "Your area" is rarely one market. The published list splits several
     * metros into entries a short drive apart - Dallas, Fort Worth and Garland;
     * Newark, Paterson and New York City; Oakland, San Francisco and San Jose -
     * so a fix inside one of those clusters is inside several markets at once.
     * The nearest is the answer the apps save; the rest are handed to the dialog
     * as alternatives, because a viewer on the far side of the cluster receives
     * the other market's stations. Empty means nothing is published within the
     * radius, which is a different sentence than "the nearest is 150 km away".
     */
    fun nearbyMarketsWithDistance(
        latitude: Double,
        longitude: Double,
        state: String? = null,
        maxKm: Double = LOCAL_MARKET_NEAR_KM,
    ): List<Pair<LocalMarket, Double>> {
        val wanted = state?.uppercase().orEmpty()
        return markets
            .filter { market ->
                !market.latitude.isNaN() && !market.longitude.isNaN() &&
                    (wanted.isBlank() || market.state == wanted)
            }
            .map { market -> market to distanceKm(latitude, longitude, market.latitude, market.longitude) }
            .filter { (_, km) -> km <= maxKm }
            .sortedBy { (_, km) -> km }
    }

    /** The state a fix falls in, for the "nothing published near you" sentence. */
    fun stateForLocation(latitude: Double, longitude: Double): String? =
        nearestMarket(latitude, longitude)?.state

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
        // A ZIP with no published market near it is an honest "none", not every
        // market in its state (1.1.21).
        if (selection.zip.length >= 3 && zipMarket == null && selection.city.isBlank()) return emptyList()
        val wantedCity = normalizePlace(selection.city)
        return markets.filter { market ->
            (wantedState.isBlank() || market.state == wantedState) &&
                (wantedCity.isBlank() || normalizePlace(market.city) == wantedCity) &&
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

    /** Great-circle distance in kilometres; `kotlin.math` has no `radians`. */
    private fun distanceKm(lat1: Double, lon1: Double, lat2: Double, lon2: Double): Double {
        val radius = 6371.0
        val phi1 = toRadians(lat1)
        val phi2 = toRadians(lat2)
        val dPhi = phi2 - phi1
        val dLambda = toRadians(lon2 - lon1)
        val a = sin(dPhi / 2) * sin(dPhi / 2) + cos(phi1) * cos(phi2) * sin(dLambda / 2) * sin(dLambda / 2)
        return 2 * radius * asin(min(1.0, sqrt(a)))
    }

    private fun toRadians(degrees: Double): Double = degrees * PI / 180.0
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
 * How far a fix may be from a published market and still be called the
 * viewer's area (1.1.18).
 *
 * PremiumTV publishes local stations for around a hundred markets, so the
 * nearest one to any point on the map always exists - and for a viewer in a
 * market nobody has published (Wilkes-Barre, Scranton, Lancaster before its
 * feed came back) "nearest" meant being told their area was Philadelphia,
 * 150 km away. A fix inside this radius is treated as local; beyond it the
 * market is offered as an option instead of saved as the answer. The same
 * limit is in the macOS/Linux renderer (`NEAREST_MARKET_MAX_KM`) and the web
 * edition, so one rule decides it on every screen.
 */
const val LOCAL_MARKET_NEAR_KM = 120.0

/** True when a published market is close enough to a fix to be called local. */
fun marketIsNear(distanceKm: Double): Boolean =
    distanceKm.isFinite() && distanceKm <= LOCAL_MARKET_NEAR_KM

/**
 * The one spelling a place is matched by (1.1.19).
 *
 * A viewer types the city they know - "Wilkes Barre", "Wilkes-Barre",
 * "Saint Paul", "St. Paul" - and the directory holds exactly one of those
 * spellings. Folding accents, punctuation and repeated spaces to a single
 * canonical form, and reading "Saint" as "St", makes the city field match the
 * place instead of the typist. Pure text, so it is unit-testable on the JVM.
 */
fun normalizePlace(name: String): String {
    val folded = Normalizer.normalize(name.trim(), Normalizer.Form.NFD)
        .replace(Regex("\\p{Mn}+"), "")
        .lowercase()
        .replace(Regex("[^a-z0-9]+"), " ")
        .trim()
    return folded.replace(Regex("^saint\\s+"), "st ")
}

/** The permission "Use my location" needs; either precision is enough. */
fun Context.hasLocationPermission(): Boolean =
    checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED ||
        checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED

/**
 * The location providers this device has *and* the viewer has switched on.
 *
 * Empty on most TV boxes and sticks, which is a fact the dialog must say out
 * loud instead of hanging on a request no hardware will answer.
 */
fun Context.enabledLocationProviders(): List<String> {
    val manager = getSystemService(Context.LOCATION_SERVICE) as? LocationManager ?: return emptyList()
    return try {
        manager.allProviders.filter { manager.isProviderEnabled(it) }
    } catch (error: Exception) {
        emptyList()
    }
}

/** A cached fix plus its age in milliseconds, or null when there is none. */
fun Context.lastKnownCoordinatesWithAge(): Triple<Double, Double, Long>? {
    if (!hasLocationPermission()) return null
    val manager = getSystemService(Context.LOCATION_SERVICE) as? LocationManager ?: return null
    for (provider in listOf(
        LocationManager.NETWORK_PROVIDER,
        LocationManager.GPS_PROVIDER,
        LocationManager.PASSIVE_PROVIDER,
    )) {
        val location = try {
            manager.getLastKnownLocation(provider)
        } catch (error: SecurityException) {
            null
        } catch (error: IllegalArgumentException) {
            null
        } ?: continue
        if (!location.latitude.isFinite() || !location.longitude.isFinite()) continue
        // `Location.getTime()` is wall-clock, so it can read as the future on a
        // device whose clock jumped. An unset (0) or future timestamp is treated
        // as ancient, which costs one fresh request; believing it would reuse
        // yesterday's city as if it were now.
        val now = System.currentTimeMillis()
        val age = if (location.time <= 0L || location.time > now) Long.MAX_VALUE else now - location.time
        return Triple(location.latitude, location.longitude, age)
    }
    return null
}

/**
 * A coarse last-known fix, when the viewer allowed location.
 *
 * Returns null when the permission is missing or no provider has a cached fix,
 * so the dialog can fall back to asking for a ZIP instead of blocking.
 */
fun Context.lastKnownCoordinates(): Pair<Double, Double>? =
    lastKnownCoordinatesWithAge()?.let { it.first to it.second }

/**
 * One fix, asked for rather than remembered (1.1.18).
 *
 * [lastKnownCoordinates] reads a cache, and a cache is empty on a device that
 * has never located itself - which is every TV box and plenty of phones. Since
 * 1.1.7 the dialog read it immediately after the grant, so a viewer who said
 * yes was told "No location fix is available on this device" and the feature
 * looked like it had never asked. This waits for a real update from the enabled
 * providers, keeps any fix that is already recent (no second GPS wake for
 * nothing), and falls back to the cache when the deadline passes.
 *
 * Coarse only, on purpose: [LOCAL_MARKET_NEAR_KM] is a market radius, so
 * ACCESS_FINE_LOCATION buys nothing here and the dialog says so.
 */
suspend fun Context.awaitCoordinates(timeoutMs: Long = 8_000L): Pair<Double, Double>? {
    if (!hasLocationPermission()) return null
    val manager = getSystemService(Context.LOCATION_SERVICE) as? LocationManager ?: return null
    val cached = lastKnownCoordinatesWithAge()
    if (cached != null && cached.third <= FRESH_FIX_MS) return cached.first to cached.second
    val providers = enabledLocationProviders()
    if (providers.isEmpty()) return cached?.let { it.first to it.second }
    val fix = try {
        withTimeoutOrNull(timeoutMs) {
            suspendCancellableCoroutine<Pair<Double, Double>?> { continuation ->
                var listener: LocationListener? = null
                fun stop() {
                    val active = listener ?: return
                    providers.forEach { runCatching { manager.removeUpdates(active) } }
                }
                listener = object : LocationListener {
                    override fun onLocationChanged(location: Location) {
                        if (!location.latitude.isFinite() || !location.longitude.isFinite()) return
                        stop()
                        if (continuation.isActive) {
                            continuation.resume(location.latitude to location.longitude)
                        }
                    }

                    override fun onProviderEnabled(provider: String) = Unit
                    override fun onProviderDisabled(provider: String) = Unit
                    @Suppress("DEPRECATION")
                    override fun onStatusChanged(provider: String, status: Int, extras: Bundle?) = Unit
                }
                val watched = providers.filter { provider ->
                    try {
                        manager.requestLocationUpdates(provider, 1_000L, 0f, listener!!, Looper.getMainLooper())
                        true
                    } catch (error: SecurityException) {
                        false
                    } catch (error: IllegalArgumentException) {
                        false
                    }
                }
                if (watched.isEmpty()) {
                    stop()
                    if (continuation.isActive) {
                        continuation.resume(cached?.let { it.first to it.second })
                    }
                }
                continuation.invokeOnCancellation { stop() }
            }
        }
    } catch (error: Exception) {
        null
    }
    return fix ?: cached?.let { it.first to it.second }
}

/** A fix this old is worth reusing; [awaitCoordinates] does not re-ask. */
private const val FRESH_FIX_MS = 10 * 60 * 1000L

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
