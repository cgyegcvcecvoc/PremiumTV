package com.premiumtv.app.ui

import android.Manifest
import android.content.pm.PackageManager
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
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
import com.premiumtv.app.data.LocalChannelSettings
import com.premiumtv.app.data.LocalDirectory
import com.premiumtv.app.data.LocalSelection
import com.premiumtv.app.data.lastKnownCoordinates

/**
 * Asks where the viewer watches from (1.1.7, refined in 1.1.11).
 *
 * The order is deliberate, because each answer is more private than the last:
 *
 *  1. "Use my location" - an approximate fix, matched to the nearest *market*
 *     PremiumTV publishes (WGAL's Lancaster, not the whole state).
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
    var zip by rememberSaveable { mutableStateOf(initial.zip) }
    var state by rememberSaveable { mutableStateOf(initial.state) }
    var city by rememberSaveable { mutableStateOf(initial.city) }
    var country by rememberSaveable { mutableStateOf(initial.country.ifBlank { "US" }) }
    var source by rememberSaveable { mutableStateOf(initial.source) }
    var message by remember { mutableStateOf("") }
    var locating by remember { mutableStateOf(false) }
    var showEverything by rememberSaveable { mutableStateOf(false) }

    fun selection(): LocalSelection = LocalSelection(
        country = country.trim().uppercase().ifBlank { "US" },
        state = state.trim().uppercase(),
        zip = zip.filter { it.isDigit() },
        city = city.trim(),
        source = source,
    )

    fun applyFix(latitude: Double, longitude: Double) {
        locating = false
        val market = directory?.nearestMarket(latitude, longitude)
        if (market == null) {
            message = "No local stations are published near that fix. Enter a ZIP code instead."
            source = ""
            return
        }
        state = market.state
        city = if (directory.marketsFor(LocalSelection(state = market.state)).size > 1 && showEverything) "" else market.city
        zip = ""
        source = LocalSelection.SOURCE_LOCATION
        message = "Location set to ${market.label}. Pick another ZIP or state any time."
    }

    val permission = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (!granted) {
            locating = false
            source = ""
            message = "Location was declined - that is fine. Enter a ZIP code, state or city instead."
            return@rememberLauncherForActivityResult
        }
        val fix = context.lastKnownCoordinates()
        if (fix == null) {
            locating = false
            message = "No location fix is available on this device. Enter a ZIP code or state instead."
        } else {
            applyFix(fix.first, fix.second)
        }
    }

    fun useLocation() {
        locating = true
        message = ""
        val granted = context.checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) ==
            PackageManager.PERMISSION_GRANTED
        if (granted) {
            val fix = context.lastKnownCoordinates()
            if (fix == null) {
                locating = false
                message = "No location fix is available. Enter a ZIP code or state instead."
            } else {
                applyFix(fix.first, fix.second)
            }
        } else {
            permission.launch(Manifest.permission.ACCESS_COARSE_LOCATION)
        }
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
                    "PremiumTV asks your device for an approximate location once, to find the local " +
                        "stations for your area - stations like WGAL in Lancaster. Declining is fine: a " +
                        "ZIP code, a state or a city works just as well. Nothing leaves this device."
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
                Spacer(Modifier.height(6.dp))
                OutlinedTextField(
                    value = zip,
                    onValueChange = { value ->
                        zip = value.filter { it.isDigit() }.take(5)
                        source = if (zip.isNotBlank()) LocalSelection.SOURCE_ZIP else source
                        message = ""
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
                        "ZIP $zip resolves to $zipState" + (directory?.marketForZip(current.zip)?.let { " · ${it.label}" } ?: "")
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
