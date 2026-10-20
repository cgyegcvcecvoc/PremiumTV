package com.premiumtv.app

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.premiumtv.app.data.LoadState
import com.premiumtv.app.data.RefreshTrigger
import com.premiumtv.app.update.AppUpdateManager
import com.premiumtv.app.update.Diagnostics
import com.premiumtv.app.update.DiagnosticsReport
import com.premiumtv.app.BuildConfig
import com.premiumtv.app.ui.LiveFeedStatus
import com.premiumtv.app.ui.feedAnswers
import com.premiumtv.app.ui.groupLiveEvents
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.joinAll
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class TvViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = (application as PremiumTvApplication).repository
    private val updateManager: AppUpdateManager =
        (application as PremiumTvApplication).updateManager
    private var forceRefreshJob: Job? = null
    private var updateJob: Job? = null
    private var diagnosticsJob: Job? = null

    val state = repository.state
    val status = repository.status
    val refreshInfo = repository.refreshInfo

    /** App updates: newest stable release, download progress, installer state. */
    val updateInfo = updateManager.state

    /** The last Settings → Check for bugs result; null until it has been run. */
    private val _diagnostics = MutableStateFlow<DiagnosticsReport?>(null)
    val diagnostics = _diagnostics.asStateFlow()

    private val _diagnosticsRunning = MutableStateFlow(false)
    val diagnosticsRunning = _diagnosticsRunning.asStateFlow()

    // ---------------------------------------------------------- live events
    //
    // The 1.0.8 Live Events revamp: the tab's refresh button (and opening the
    // tab) asks every game's feeds whether anything still answers, so the tab
    // can show LIVE or NO SIGNAL per game instead of trusting a snapshot.
    // Statuses are keyed by the game's stable key, so a refresh that swaps
    // games leaves the surviving games' answers in place.

    private val _liveFeedStatus = MutableStateFlow<Map<String, LiveFeedStatus>>(emptyMap())
    val liveFeedStatus = _liveFeedStatus.asStateFlow()

    private val _liveProbeRunning = MutableStateFlow(false)
    val liveProbeRunning = _liveProbeRunning.asStateFlow()

    private var liveProbeJob: Job? = null

    /** Live Events → Refresh live games: newest playlist, then a feed check. */
    fun refreshLiveEvents() {
        forceRefresh()
        probeLiveEvents()
    }

    /** Asks every live game's feeds (six games at a time) whether anything answers. */
    fun probeLiveEvents() {
        if (liveProbeJob?.isActive == true) return
        val library = (state.value as? LoadState.Ready)?.library ?: return
        liveProbeJob = viewModelScope.launch {
            _liveProbeRunning.value = true
            try {
                val sections = groupLiveEvents(library.channels)
                val started = LinkedHashMap<String, LiveFeedStatus>()
                for (section in sections) {
                    for (event in section.events) started[event.key] = LiveFeedStatus.Checking
                }
                if (started.isEmpty()) return@launch
                _liveFeedStatus.value = started
                // Six games in parallel, chunk by chunk: fast enough for a
                // full card on a remote press, gentle enough for the
                // scrapers' edges.
                val games = sections.flatMap { it.events }
                coroutineScope {
                    games.chunked(PROBE_CONCURRENCY).forEach { chunk ->
                        val jobs = chunk.map { event ->
                            launch {
                                val answers = event.servers.any { feedAnswers(it) }
                                _liveFeedStatus.value = _liveFeedStatus.value +
                                    (event.key to if (answers) LiveFeedStatus.Answering else LiveFeedStatus.Silent)
                            }
                        }
                        jobs.joinAll()
                    }
                }
            } finally {
                _liveProbeRunning.value = false
            }
        }
    }

    private companion object {
        const val PROBE_CONCURRENCY = 6
    }

    init {
        load()
        // Once a day at most; the manager sends its ETag and does no download.
        updateJob = viewModelScope.launch { updateManager.checkIfDue() }
    }

    fun load() {
        viewModelScope.launch { repository.load() }
    }

    /** Settings action: bypass validators and fetch both playlist and guide. */
    fun forceRefresh() {
        if (forceRefreshJob?.isActive == true || refreshInfo.value.inProgress) return
        forceRefreshJob = viewModelScope.launch {
            repository.refresh(RefreshTrigger.Manual)
        }
    }

    fun resetToBundled() {
        if (refreshInfo.value.inProgress) return
        viewModelScope.launch { repository.resetToBundled() }
    }

    /** Settings → Check for updates. Always asks GitHub, at most one at a time. */
    fun checkForUpdates() {
        if (updateInfo.value.busy) return
        if (updateJob?.isActive == true) return
        updateJob = viewModelScope.launch { updateManager.check(force = true) }
    }

    /** Settings → Download update. An installer for this version is reused. */
    fun downloadUpdate() {
        if (updateInfo.value.busy || updateJob?.isActive == true) return
        updateJob = viewModelScope.launch { updateManager.download() }
    }

    /** Settings → Install update. Opens Android's package installer. */
    fun installUpdate() {
        updateManager.installDownloaded()
    }

    /**
     * Settings → Check for bugs. Offline and read-only: inspects the loaded
     * library, the refresh pipeline and the update state, then reports every
     * finding with a pass/warning/problem level.
     */
    fun runDiagnostics() {
        if (diagnosticsJob?.isActive == true) return
        diagnosticsJob = viewModelScope.launch {
            _diagnosticsRunning.value = true
            try {
                val library = (state.value as? LoadState.Ready)?.library
                if (library == null) {
                    _diagnostics.value = null
                    return@launch
                }
                _diagnostics.value = withContext(Dispatchers.Default) {
                    Diagnostics.run(
                        library = library,
                        refresh = refreshInfo.value,
                        update = updateInfo.value,
                        installedVersion = BuildConfig.VERSION_NAME,
                    )
                }
            } finally {
                _diagnosticsRunning.value = false
            }
        }
    }

    /**
     * The startup popup's "Remind me next time" (and the remote's Back key).
     *
     * The dismissal lives in memory only, so the notice is back on the next
     * launch: an out-of-date build cannot be silenced for good by one press.
     */
    fun dismissUpdateNotice() {
        updateManager.dismissNotice()
    }
}
