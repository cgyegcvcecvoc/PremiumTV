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
import androidx.compose.ui.unit.dp
import com.premiumtv.app.data.LocalChannelSettings
import com.premiumtv.app.data.LocalDirectory
import com.premiumtv.app.data.LocalSelection
import com.premiumtv.app.data.lastKnownCoordinates

/**
 * Asks where the viewer watches from (1.1.7).
 *
 * PremiumTV cannot know a market from geolocation on a TV stick, and it must
 * never make location mandatory: "Use my location" is the first offer, and
 * declining it leaves a ZIP, a state or a country to type. The answer is
 * stored on this device only and is used to filter the published local
 * stations - a market we do not carry shows that honestly instead of inventing
 * channels.
 */
@Composable
internal fun LocalChannelsDialog(
    directory: LocalDirectory?,
    initial: LocalSelection,
    onSave: (LocalSelection) -> Unit,
    onDismiss: () -> Unit,
) {
    val context = LocalContext.current
    var zip by rememberSaveable { mutableStateOf(initial.zip) }
    var state by rememberSaveable { mutableStateOf(initial.state) }
    var city by rememberSaveable { mutableStateOf(initial.city) }
    var country by rememberSaveable { mutableStateOf(initial.country.ifBlank { "US" }) }
    var message by remember { mutableStateOf("") }
    var locating by remember { mutableStateOf(false) }

    fun selection(): LocalSelection = LocalSelection(
        country = country.trim().uppercase().ifBlank { "US" },
        state = state.trim().uppercase(),
        zip = zip.filter { it.isDigit() },
        city = city.trim(),
    )

    fun applyFix(latitude: Double, longitude: Double) {
        locating = false
        val found = directory?.stateForLocation(latitude, longitude)
        if (found.isNullOrBlank()) {
            message = "No local stations are published near you yet. Enter a ZIP or state."
        } else {
            state = found
            zip = ""
            message = "Location set to ${directory?.countryName(country) ?: "your area"} · $found"
        }
    }

    val permission = rememberLauncherForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { granted ->
        if (!granted) {
            locating = false
            message = "Location was declined. Enter a ZIP, state or country instead."
            return@rememberLauncherForActivityResult
        }
        val fix = context.lastKnownCoordinates()
        if (fix == null) {
            locating = false
            message = "No location fix is available on this device. Enter a ZIP or state instead."
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
                message = "No location fix is available. Enter a ZIP or state instead."
            } else {
                applyFix(fix.first, fix.second)
            }
        } else {
            permission.launch(Manifest.permission.ACCESS_COARSE_LOCATION)
        }
    }

    val current = selection()
    val resolvedState = current.state.ifBlank { directory?.stateForZip(current.zip).orEmpty() }
    val markets = remember(directory, current.country, resolvedState, current.city) {
        if (directory == null) emptyList() else directory.marketsFor(current.copy(state = resolvedState))
    }
    val stationCount = markets.sumOf { it.stations.size }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Local channels") },
        text = {
            Column(modifier = Modifier.verticalScroll(rememberScrollState())) {
                Text(
                    "Find local stations like WGAL for where you watch. PremiumTV asks your " +
                        "device for an approximate location once; declining is fine — a ZIP, " +
                        "state or country works just as well. Nothing leaves this device."
                )
                Spacer(Modifier.height(14.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(10.dp)) {
                    TextButton(onClick = { useLocation() }, enabled = !locating) {
                        Text(if (locating) "Locating…" else "Use my location")
                    }
                }
                Spacer(Modifier.height(6.dp))
                OutlinedTextField(
                    value = zip,
                    onValueChange = { value -> zip = value.filter { it.isDigit() }.take(5) },
                    label = { Text("ZIP code (optional)") },
                    singleLine = true,
                )
                Spacer(Modifier.height(8.dp))
                Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    OutlinedTextField(
                        value = state,
                        onValueChange = { value -> state = value.filter { it.isLetter() }.take(2).uppercase() },
                        label = { Text("State") },
                        singleLine = true,
                        modifier = Modifier.weight(1f),
                    )
                    OutlinedTextField(
                        value = country,
                        onValueChange = { value -> country = value.filter { it.isLetter() }.take(2).uppercase() },
                        label = { Text("Country") },
                        singleLine = true,
                        modifier = Modifier.weight(1f),
                    )
                }
                Spacer(Modifier.height(8.dp))
                OutlinedTextField(
                    value = city,
                    onValueChange = { value -> city = value.take(40) },
                    label = { Text("City (optional)") },
                    singleLine = true,
                )
                Spacer(Modifier.height(10.dp))
                val summary = when {
                    directory == null -> "Local-channel data is not bundled in this build."
                    current.country != "US" -> "Local stations are published for the United States only so far."
                    resolvedState.isBlank() -> "Enter a ZIP or state to see your local stations."
                    stationCount == 0 -> "No local stations are published for ${if (current.city.isBlank()) resolvedState else "${current.city}, $resolvedState"} yet."
                    else -> "$stationCount local station${if (stationCount == 1) "" else "s"} in " +
                        markets.joinToString(", ") { it.city } + "."
                }
                Text(summary, style = androidx.compose.material3.MaterialTheme.typography.bodySmall)
                if (message.isNotBlank()) {
                    Spacer(Modifier.height(6.dp))
                    Text(message, style = androidx.compose.material3.MaterialTheme.typography.labelSmall)
                }
            }
        },
        confirmButton = {
            TextButton(
                onClick = { onSave(current.copy(state = resolvedState)) },
                enabled = directory != null,
            ) { Text("Save") }
        },
        dismissButton = {
            Row {
                TextButton(onClick = { zip = ""; state = ""; city = ""; country = "US" }) { Text("Clear") }
                TextButton(onClick = onDismiss) { Text("Not now") }
            }
        },
    )
}
