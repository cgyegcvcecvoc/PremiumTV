package com.premiumtv.app

import android.app.Application
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.viewModelScope
import com.premiumtv.app.data.TvRepository
import kotlinx.coroutines.launch

class TvViewModel(application: Application) : AndroidViewModel(application) {

    private val repository = TvRepository(application)

    val state = repository.state
    val status = repository.status

    init {
        load()
    }

    fun load() {
        viewModelScope.launch { repository.load() }
    }

    fun refresh() {
        viewModelScope.launch { repository.refresh() }
    }

    fun resetToBundled() {
        viewModelScope.launch { repository.resetToBundled() }
    }
}
