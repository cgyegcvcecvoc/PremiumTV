package com.premiumtv.app

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.premiumtv.app.data.RefreshTrigger
import kotlinx.coroutines.Job
import kotlinx.coroutines.launch

class TvViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = (application as PremiumTvApplication).repository
    private var forceRefreshJob: Job? = null

    val state = repository.state
    val status = repository.status
    val refreshInfo = repository.refreshInfo

    init {
        load()
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
}
