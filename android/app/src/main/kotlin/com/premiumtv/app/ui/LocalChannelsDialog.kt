package com.premiumtv.app.ui

import android.Manifest
import android.content.Intent
import android.net.Uri
import android.provider.Settings
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.rememberCoroutineScope
import androidx.lifecycle.Lifecycle
import androidx.lifecycle.LifecycleEventObserver
import androidx.lifecycle.compose.LocalLifecycleOwner
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.KeyboardCapitalization
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.launch
import com.premiumtv.app.data.LocalChannelSettings
import com.premiumtv.app.data.LocalDirectory
import com.premiumtv.app.data.LocalMarket
import com.premiumtv.app.data.LocalSelection
import com.premiumtv.app.data.awaitCoordinates
import com.premiumtv.app.data.enabledLocationProviders
import com.premiumtv.app.data.hasLocationPermission
import com.premiumtv.app.data.marketIsNear

/**
 * Asks where the viewer watches from (1.1.7, refined in 1.1.11).
 *
 * The order is deliberate, because each answer is more private than the last:
 *
 *  1. "Use my location" - an approximate fix, matched to the nearest *market*
 *     PremiumTV publishes (WGAL's Lancaster, not the whole state). 1.1.18 made
 *     that ask real: both location permissions are requested in one dialog, a
 *     fix is *requested* instead of read from a cache that is empty on a fresh
 *     grant, a device with no location service says so, a refusal Android
 *     remembers offers the app's permission screen, and a market farther than
 *     [com.premiumtv.app.data.LOCAL_MARKET_NEAR_KM] is offered rather than
 *     saved.
 *  2. Declined, unavailable, or no station near the fix: a **ZIP code**, which
 *     resolves to a market through the bundled ZIP prefix table.
 *  3. No ZIP at hand: a **state** or a **city** - either one lists the
 *     published markets there.
 *  4. Outside the United States: the **country** picker says what exists, and
 *     the answer is honest that local stations are US-only so far.
 *
 * Nothing is uploaded; the answer is stored on this device and only filters
 * the published station list. A market we do not carry is reported as such
 * rather than filled with invented channels.
 */
@Composable
internal fun LocalChannelsDialog(
    directory: LocalDirectory?,
    initial: LocalSelection,
    onSave: (LocalSelection) -> Unit,
    onDismiss: () -> Unit,
    onDecline: (() -> Unit)? = null,
) {
    val context = LocalContext.current
    val scope = rememberCoroutineScope()
    var zip by rememberSaveable { mutableStateOf(initial.zip) }
    var state by rememberSaveable { mutableStateOf(initial.state) }
    var city by rememberSaveable { mutableStateOf(initial.city) }
    var country by rememberSaveable { mutableStateOf(initial.country.ifBlank { "US" }) }
    var source by rememberSaveable { mutableStateOf(initial.source) }
    var message by remember { mutableStateOf("") }
    var locating by remember { mutableStateOf(false) }
    var showEverything by rememberSaveable { mutableStateOf(false) }
    // 1.1.18: the two things the old dialog could not tell apart. `needsSettings`
    // means Android will not ask again (a remembered refusal), so the only way
    // back is the system's own screen; `noProvider` means there is no location
    // service to ask at all, which is normal on a TV box. `saveable` because a
    // permission prompt can take the activity with it, and the answer must
    // still be read when the viewer comes back.
    var needsSettings by rememberSaveable { mutableStateOf(false) }
    var noProvider by rememberSaveable { mutableStateOf(false) }
    var awaitingPermission by rememberSaveable { mutableStateOf(false) }
    var farMarket by remember { mutableStateOf<LocalMarket?>(null) }
    // 1.1.19: the other markets a fix found inside the radius. Several metros
    // are published as a cluster of markets a short drive apart (Dallas / Fort
    // Worth / Garland), so a fix can be inside more than one; the nearest is
    // saved and these are offered as the alternatives.
    var nearby by remember { mutableStateOf<List<Pair<LocalMarket, Double>>>(emptyList()) }

    fun selection(): LocalSelection = LocalSelection(
        country = country.trim().uppercase().ifBlank { "US" },
        state = state.trim().uppercase(),
        zip = zip.filter { it.isDigit() },
        city = city.trim(),
        source = source,
    )

    fun applyFix(latitude: Double, longitude: Double) {
        locating = false
        val known = directory
        if (known == null) {
            message = "No local stations are published near that fix. Enter a ZIP code instead."
            source = ""
            return
        }
        // 1.1.19: the area is every market inside the radius, nearest first.
        // 1.1.18: "nearest" is not "yours". Wilkes-Barre, Scranton and Lancaster
        // all sit closer to a published market than to nothing, and until that
        // release the app saved that far market as the viewer's area — the
        // reason the feature looked broken to the people it was meant to help.
        val area = known.nearbyMarketsWithDistance(latitude, longitude)
        if (area.isEmpty()) {
            val far = known.nearestMarketWithDistance(latitude, longitude)
            if (far == null) {
                message = "No local stations are published near that fix. Enter a ZIP code instead."
                source = ""
                return
            }
            val miles = (far.second * 0.621371).toInt()
            farMarket = far.first
            nearby = emptyList()
            source = ""
            message = "Nothing is published for your spot yet — the nearest stations PremiumTV " +
                "carries are in ${far.first.label}, about $miles miles away. Enter a ZIP code or a " +
                "state, or use that market."
            return
        }
        val (market, km) = area.first()
        val miles = (km * 0.621371).toInt()
        farMarket = null
        nearby = area.drop(1)
        state = market.state
        city = if (known.marketsFor(LocalSelection(state = market.state)).size > 1 && showEverything) "" else market.city
        zip = ""
        source = LocalSelection.SOURCE_LOCATION
        message = if (nearby.isNotEmpty()) {
            "Location set to ${market.label}, about $miles miles away. Also nearby: " +
                nearby.joinToString(", ") { (option, distance) ->
                    "${option.label} (${(distance * 0.621371).toInt()} mi)"
                } + " — pick one below if that is the area you receive."
        } else {
            "Location set to ${market.label}, about $miles miles away. Pick another ZIP or state any time."
        }
    }

    /** Switch to another market the same fix found inside the radius. */
    fun useNearbyMarket(option: LocalMarket, km: Double) {
        farMarket = null
        nearby = nearby.filterNot { (market, _) -> market.id == option.id }
        state = option.state
        city = option.city
        zip = ""
        source = LocalSelection.SOURCE_LOCATION
        message = "Location set to ${option.label}, about ${(km * 0.621371).toInt()} miles away."
    }

    /**
     * Read a fix now.
     *
     * The grant and this read are separate steps on purpose: the last-known
     * cache that 1.1.17 answered from is empty right after a first grant, so
     * the dialog asks the enabled providers for one update and waits for it.
     */
    fun requestFix() {
        if (!context.hasLocationPermission()) return
        locating = true
        message = "Waiting for a fix from this device…"
        scope.launch {
            val fix = context.awaitCoordinates()
            locating = false
            if (fix == null) {
                source = ""
                message = "This device did not answer with a fix in time. A ZIP code, state or " +
                    "city works just as well."
            } else {
                applyFix(fix.first, fix.second)
            }
        }
    }

    val permission = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { result ->
        awaitingPermission = false
        val granted = result[Manifest.permission.ACCESS_COARSE_LOCATION] == true ||
            result[Manifest.permission.ACCESS_FINE_LOCATION] == true
        if (!granted) {
            locating = false
            source = ""
            // Two different refusals, and only one of them is the viewer's
            // answer. Android stops showing the prompt once "Don't ask again"
            // is on (or after the second refusal on most builds), which is the
            // state 1.1.17 reported as "declined" forever.
            val activity = context as? android.app.Activity
            val canAskAgain = activity != null &&
                activity.shouldShowRequestPermissionRationale(Manifest.permission.ACCESS_COARSE_LOCATION)
            needsSettings = !canAskAgain
            message = if (canAskAgain) {
                "Location was declined - that is fine. Enter a ZIP code, state or city instead."
            } else {
                "Location is switched off for PremiumTV in the system settings, so this app cannot be " +
                    "asked again. Enter a ZIP code, state or city - or open the settings and allow it."
            }
            return@rememberLauncherForActivityResult
        }
        requestFix()
    }

    // A permission prompt can outlive this dialog: Android may recreate the
    // activity behind it, and the launcher's callback is gone with the old
    // composition. Resuming with a request still owed reads the answer from the
    // system instead of leaving "Locating…" on screen forever.
    val lifecycleOwner = LocalLifecycleOwner.current
    DisposableEffect(lifecycleOwner) {
        val observer = LifecycleEventObserver { _, event ->
            if (event == Lifecycle.Event.ON_RESUME && awaitingPermission) {
                awaitingPermission = false
                if (context.hasLocationPermission()) requestFix()
            }
        }
        lifecycleOwner.lifecycle.addObserver(observer)
        onDispose { lifecycleOwner.lifecycle.removeObserver(observer) }
    }

    fun useLocation() {
        locating = true
        message = ""
        needsSettings = false
        farMarket = null
        noProvider = context.enabledLocationProviders().isEmpty()
        if (noProvider) {
            // Asking for a permission that no hardware can use would leave the
            // viewer staring at a prompt and then at nothing, which is how this
            // button came to look dead on TV boxes. Say what is missing instead.
            locating = false
            message = "This device has no location service to ask — usual for a TV box or a stick. " +
                "A ZIP code, state or city finds the same stations."
            return
        }
        if (context.hasLocationPermission()) {
            requestFix()
        } else {
            awaitingPermission = true
            // Both rough and precise are in one request: a single-permission ask
            // for the rough one is what Android 12+ answers with the
            // "Precise/Approximate" sheet, and a request for a permission this
            // manifest does not list is answered "denied" with no dialog at all.
            permission.launch(
                arrayOf(
                    Manifest.permission.ACCESS_COARSE_LOCATION,
                    Manifest.permission.ACCESS_FINE_LOCATION,
                ),
            )
        }
    }

    fun openLocationSettings() {
        val opened = runCatching {
            context.startActivity(
                Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS)
                    .addFlags(Intent.FLAG_ACTIVITY_NEW_TASK),
            )
        }.isSuccess
        if (!opened) {
            message = "This device has no location settings screen. Enter a ZIP code, state or city instead."
        }
    }

    fun openAppPermissionSettings() {
        val opened = runCatching {
            context.startActivity(
                Intent(
                    Settings.ACTION_APPLICATION_DETAILS_SETTINGS,
                    Uri.fromParts("package", context.packageName, null),
                ).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK),
            )
        }.isSuccess
        message = if (opened) {
            "Opened PremiumTV's app settings. Choose Permissions → Location → Allow, then press " +
                "\"Use my location\" again."
        } else {
            "Android would not open the settings screen. Allow location for PremiumTV in the system " +
                "settings, then press the button again."
        }
    }

    /** Accept the far market the fix found, when the viewer wants it anyway. */
    fun useFarMarket() {
        val market = farMarket ?: return
        farMarket = null
        state = market.state
        city = market.city
        zip = ""
        source = LocalSelection.SOURCE_LOCATION
        message = "Using ${market.label}, the nearest market PremiumTV publishes. A ZIP or state " +
            "replaces it any time."
    }

    val current = selection()
    val zipState = directory?.stateForZip(current.zip).orEmpty()
    val resolvedState = current.state.ifBlank { zipState }
    val resolved = current.copy(state = resolvedState)
    val markets = remember(directory, resolved.country, resolved.state, resolved.zip, resolved.city, showEverything) {
        when {
            directory == null -> emptyList()
            showEverything && resolved.city.isBlank() && resolved.zip.isBlank() ->
                directory.marketsFor(LocalSelection(country = resolved.country, state = resolved.state))
            else -> directory.marketsFor(resolved)
        }
    }
    val stationCount = markets.sumOf { it.stations.size }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text(if (initial.hasSelection) "Local channels" else "Where do you watch from?") },
        text = {
            Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                Text(
                    "PremiumTV asks your device once whether it may use an approximate location, to " +
                        "find the local stations for your area - stations like WGAL in Lancaster. Only " +
                        "the rough position is used, never an address, and nothing leaves this device. " +
                        "Declining is fine: a ZIP code, a state or a city works just as well."
                )
                Spacer(Modifier.height(14.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    TextButton(onClick = { useLocation() }, enabled = !locating) {
                        Text(if (locating) "Locating…" else "Use my location")
                    }
                    TextButton(
                        onClick = {
                            locating = false
                            source = ""
                            message = "No problem - enter a ZIP code, state or city below."
                        },
                        enabled = !locating,
                    ) { Text("No thanks") }
                }
                if (locating || needsSettings || noProvider || farMarket != null) {
                    Spacer(Modifier.height(4.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                        if (needsSettings) {
                            TextButton(onClick = { openAppPermissionSettings() }) {
                                Text("Allow in app settings")
                            }
                        }
                        if (noProvider) {
                            TextButton(onClick = { openLocationSettings() }) {
                                Text("Location settings")
                            }
                        }
                        if (farMarket != null) {
                            TextButton(onClick = { useFarMarket() }) {
                                Text("Use ${farMarket?.city} anyway")
                            }
                        }
                    }
                }
                // 1.1.19: a fix inside a published cluster (Dallas / Fort Worth /
                // Garland) is inside several markets; the nearest is saved and the
                // rest are one tap away, because the viewer may receive either.
                // Hidden once the answer is edited by hand: the alternatives
                // belong to the fix, not to a ZIP or a typed state.
                if (nearby.isNotEmpty() && source == LocalSelection.SOURCE_LOCATION) {
                    Spacer(Modifier.height(6.dp))
                    Text("Also nearby:", style = MaterialTheme.typography.labelSmall)
                    nearby.forEach { (option, km) ->
                        TextButton(onClick = { useNearbyMarket(option, km) }) {
                            Text("${option.label} · ${(km * 0.621371).toInt()} mi")
                        }
                    }
                }
                Spacer(Modifier.height(6.dp))
                OutlinedTextField(
                    value = zip,
                    onValueChange = { value ->
                        zip = value.filter { it.isDigit() }.take(5)
                        source = if (zip.isNotBlank()) LocalSelection.SOURCE_ZIP else source
                        message = ""
                        farMarket = null
                    },
                    label = { Text("ZIP code") },
                    placeholder = { Text("17603") },
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(
                        keyboardType = KeyboardType.Number,
                        imeAction = ImeAction.Next,
                    ),
                    modifier = Modifier.fillMaxWidth(),
                )
                val zipHint = when {
                    current.zip.length in 1..2 -> "A ZIP code needs five digits."
                    current.zip.length >= 3 && zipState.isNotBlank() ->
                        directory?.marketForZip(current.zip)?.let { "ZIP $zip resolves to ${it.label}" }
                            ?: "ZIP $zip is in $zipState, but no published station is within 120 km of it - not your area.",
                    current.zip.length >= 3 -> "That ZIP is not in the published table - check it, or use a state."
                    else -> null
                }
                if (zipHint != null) {
                    Spacer(Modifier.height(4.dp))
                    Text(zipHint, style = MaterialTheme.typography.labelSmall)
                }
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = state,
                        onValueChange = { value ->
                            state = value.filter { it.isLetter() }.take(2).uppercase()
                            source = if (state.isNotBlank()) LocalSelection.SOURCE_STATE else source
                            message = ""
                        },
                        label = { Text("State") },
                        placeholder = { Text("PA") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(
                            capitalization = KeyboardCapitalization.Characters,
                            imeAction = ImeAction.Next,
                        ),
                        modifier = Modifier.weight(1f),
                    )
                    OutlinedTextField(
                        value = country,
                        onValueChange = { value ->
                            country = value.filter { it.isLetter() }.take(2).uppercase()
                            message = ""
                        },
                        label = { Text("Country") },
                        singleLine = true,
                        keyboardOptions = KeyboardOptions(
                            capitalization = KeyboardCapitalization.Characters,
                            imeAction = ImeAction.Next,
                        ),
                        modifier = Modifier.weight(1f),
                    )
                }
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = city,
                    onValueChange = { value ->
                        city = value.take(40)
                        source = if (city.isNotBlank()) LocalSelection.SOURCE_CITY else source
                        message = ""
                    },
                    label = { Text("City (optional)") },
                    placeholder = { Text("Lancaster") },
                    singleLine = true,
                    keyboardOptions = KeyboardOptions(imeAction = ImeAction.Done),
                    modifier = Modifier.fillMaxWidth(),
                )
                if (directory != null && directory.stateCodes.isNotEmpty()) {
                    Spacer(Modifier.height(6.dp))
                    val covered = directory.stateCodes.joinToString(" ")
                    Text(
                        "Published local stations are in: $covered",
                        style = MaterialTheme.typography.labelSmall,
                    )
                }
                Spacer(Modifier.height(10.dp))
                val summary = when {
                    directory == null -> "Local-channel data is not bundled in this build."
                    current.country.isNotBlank() && !directory.hasCountry(current.country) ->
                        "Local stations are published for the United States only so far - " +
                            "choose US, or browse the national lineup."
                    resolvedState.isBlank() && current.zip.isBlank() -> "Enter a ZIP code, state or city to see your local stations."
                    stationCount == 0 -> directory.summary(resolved)
                    else -> "$stationCount local station${if (stationCount == 1) "" else "s"} in " +
                        markets.joinToString(", ") { it.label } + "."
                }
                Text(summary, style = MaterialTheme.typography.bodySmall)
                if (message.isNotBlank()) {
                    Spacer(Modifier.height(6.dp))
                    Text(message, style = MaterialTheme.typography.labelSmall)
                }
                if (markets.size > 1 && !showEverything) {
                    Spacer(Modifier.height(4.dp))
                    TextButton(onClick = { showEverything = true }) {
                        Text("Show all ${markets.size} markets in $resolvedState")
                    }
                }
            }
        },
        confirmButton = {
            TextButton(
                onClick = {
                    val answer = current.copy(state = resolvedState)
                    onSave(answer.copy(source = answer.source.ifBlank {
                        when {
                            answer.zip.isNotBlank() -> LocalSelection.SOURCE_ZIP
                            answer.city.isNotBlank() -> LocalSelection.SOURCE_CITY
                            answer.state.isNotBlank() -> LocalSelection.SOURCE_STATE
                            else -> LocalSelection.SOURCE_COUNTRY
                        }
                    }))
                },
                enabled = directory != null,
            ) { Text(if (initial.hasSelection) "Save" else "Save and show local channels") }
        },
        dismissButton = {
            Row {
                TextButton(onClick = {
                    zip = ""
                    state = ""
                    city = ""
                    country = "US"
                    source = ""
                    message = ""
                }) { Text("Clear") }
                TextButton(onClick = { onDecline?.invoke() ?: onDismiss() }) {
                    Text(if (initial.hasSelection) "Not now" else "Skip for now")
                }
            }
        },
    )
}
