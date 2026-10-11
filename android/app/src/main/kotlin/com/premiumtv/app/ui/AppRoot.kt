package com.premiumtv.app.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.viewmodel.compose.viewModel
import com.premiumtv.app.TvViewModel
import com.premiumtv.app.data.Channel
import com.premiumtv.app.data.LoadState
import kotlinx.coroutines.delay

@Composable
fun AppRoot(viewModel: TvViewModel = viewModel()) {
    val state by viewModel.state.collectAsState()
    val status by viewModel.status.collectAsState()
    val refreshInfo by viewModel.refreshInfo.collectAsState()

    // The guide's "now" has to move on its own; the listings are keyed to real
    // clock times, so a static value would leave yesterday's show on screen.
    var now by remember { mutableStateOf(System.currentTimeMillis() / 1000L) }
    LaunchedEffect(Unit) {
        while (true) {
            delay(60_000L)
            now = System.currentTimeMillis() / 1000L
        }
    }

    var playing by remember { mutableStateOf<Channel?>(null) }

    when (val current = state) {
        LoadState.Loading -> LoadingScreen(
            title = "Loading channels…",
            detail = "Getting your TV library ready.",
        )

        is LoadState.Error -> LoadErrorScreen(
            message = current.message,
            onRetry = { viewModel.load() },
        )

        is LoadState.Ready -> {
            val channel = playing
            if (channel != null) {
                PlayerScreen(
                    channel = channel,
                    programmes = current.library.programmes[channel.id].orEmpty(),
                    now = now,
                    onClose = { playing = null },
                )
            } else {
                HomeScreen(
                    library = current.library,
                    now = now,
                    status = status,
                    refreshInfo = refreshInfo,
                    onSelect = { playing = it },
                    onForceRefresh = { viewModel.forceRefresh() },
                    onReset = { viewModel.resetToBundled() },
                )
            }
        }
    }
}
