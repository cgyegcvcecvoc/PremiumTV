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
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
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
