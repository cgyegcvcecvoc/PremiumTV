package com.premiumtv.app

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.premiumtv.app.data.RefreshTrigger
import com.premiumtv.app.update.AppUpdateManager
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch

class TvViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = (application as PremiumTvApplication).repository
    private val updateManager: AppUpdateManager =
        (application as PremiumTvApplication).updateManager
    private var forceRefreshJob: Job? = null
    private var updateJob: Job? = null

    val state = repository.state
    val status = repository.status
    val refreshInfo = repository.refreshInfo

    /** App updates: newest stable release, download progress, installer state. */
    val updateInfo = updateManager.state

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
}
