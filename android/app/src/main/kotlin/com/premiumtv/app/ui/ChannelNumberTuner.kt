package com.premiumtv.app.ui

import android.view.KeyEvent
import com.premiumtv.app.data.Channel

/** Pause after the last digit before auto-tuning, so multi-digit numbers can be entered. */
internal const val CHANNEL_NUMBER_ENTRY_DELAY_MS = 900L
internal const val CHANNEL_NUMBER_MAX_DIGITS = 6

/** The Android remote's number or decimal key to a character; null for any other key. */
internal fun channelNumberCharacterForKey(keyCode: Int): Char? = when (keyCode) {
    KeyEvent.KEYCODE_0, KeyEvent.KEYCODE_NUMPAD_0 -> '0'
    KeyEvent.KEYCODE_1, KeyEvent.KEYCODE_NUMPAD_1 -> '1'
    KeyEvent.KEYCODE_2, KeyEvent.KEYCODE_NUMPAD_2 -> '2'
    KeyEvent.KEYCODE_3, KeyEvent.KEYCODE_NUMPAD_3 -> '3'
    KeyEvent.KEYCODE_4, KeyEvent.KEYCODE_NUMPAD_4 -> '4'
    KeyEvent.KEYCODE_5, KeyEvent.KEYCODE_NUMPAD_5 -> '5'
    KeyEvent.KEYCODE_6, KeyEvent.KEYCODE_NUMPAD_6 -> '6'
    KeyEvent.KEYCODE_7, KeyEvent.KEYCODE_NUMPAD_7 -> '7'
    KeyEvent.KEYCODE_8, KeyEvent.KEYCODE_NUMPAD_8 -> '8'
    KeyEvent.KEYCODE_9, KeyEvent.KEYCODE_NUMPAD_9 -> '9'
    KeyEvent.KEYCODE_PERIOD, KeyEvent.KEYCODE_NUMPAD_DOT -> '.'
    else -> null
}

private val channelNumberPattern = Regex("\\d+(?:\\.\\d+)?")

private fun normalizedChannelNumber(value: String): String? {
    val candidate = value.trim()
    if (!channelNumberPattern.matches(candidate)) return null
    return candidate.toBigDecimalOrNull()?.stripTrailingZeros()?.toPlainString()
}

/**
 * Finds the first published channel for a numeric `tvg-chno` value, including
 * decimal subchannels.
 *
 * Leading and trailing zeroes are ignored; blank and non-numeric channel
 * numbers are not candidates. Playlist order resolves duplicates consistently
 * with the library the viewer is already browsing.
 */
internal fun findChannelByNumber(channels: List<Channel>, entered: String): Channel? {
    val number = normalizedChannelNumber(entered) ?: return null
    return channels.firstOrNull { channel ->
        normalizedChannelNumber(channel.chno) == number
    }
}
