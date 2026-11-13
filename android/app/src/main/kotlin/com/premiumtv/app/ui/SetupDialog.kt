package com.premiumtv.app.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.height
import androidx.compose.material3.AlertDialog
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

/** A single local viewer identity; existing favorites and history stay in place. */
@Composable
internal fun SetupDialog(onComplete: (String) -> Unit) {
    var name by rememberSaveable { mutableStateOf("") }
    AlertDialog(
        onDismissRequest = { onComplete("Viewer") },
        title = { Text("Welcome to PremiumTV") },
        text = {
            Column {
                Text("Choose a category, then pick a channel. Favorites and recently watched stay on this device.")
                Spacer(Modifier.height(16.dp))
                OutlinedTextField(
                    value = name,
                    onValueChange = { name = it.take(40) },
                    label = { Text("Viewer name (optional)") },
                    singleLine = true,
                )
                Spacer(Modifier.height(8.dp))
                Text("This is a local setup. Multiple profiles and cloud sync are not available yet.")
            }
        },
        confirmButton = { TextButton(onClick = { onComplete(name.trim().ifEmpty { "Viewer" }) }) { Text("Start watching") } },
        dismissButton = { TextButton(onClick = { onComplete("Viewer") }) { Text("Skip") } },
    )
}
