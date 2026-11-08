package com.premiumtv.app.ui

import android.view.KeyEvent
import com.premiumtv.app.data.Channel
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Assert.assertSame
import org.junit.Test

/** Direct channel-number entry for Android TV remotes. */
class ChannelNumberTunerTest {

    private fun channel(name: String, number: String) = Channel(
        id = "id.$name",
        name = name,
        logo = "",
        group = "Group",
        country = "US",
        chno = number,
        url = "https://stream/$name",
        userAgent = "",
        referrer = "",
        origin = "",
    )

    @Test
    fun `all Android number keys map to their digits`() {
        val keys = listOf(
            KeyEvent.KEYCODE_0,
            KeyEvent.KEYCODE_1,
            KeyEvent.KEYCODE_2,
            KeyEvent.KEYCODE_3,
            KeyEvent.KEYCODE_4,
            KeyEvent.KEYCODE_5,
            KeyEvent.KEYCODE_6,
            KeyEvent.KEYCODE_7,
            KeyEvent.KEYCODE_8,
            KeyEvent.KEYCODE_9,
        )
        val numpadKeys = listOf(
            KeyEvent.KEYCODE_NUMPAD_0,
            KeyEvent.KEYCODE_NUMPAD_1,
            KeyEvent.KEYCODE_NUMPAD_2,
            KeyEvent.KEYCODE_NUMPAD_3,
            KeyEvent.KEYCODE_NUMPAD_4,
            KeyEvent.KEYCODE_NUMPAD_5,
            KeyEvent.KEYCODE_NUMPAD_6,
            KeyEvent.KEYCODE_NUMPAD_7,
            KeyEvent.KEYCODE_NUMPAD_8,
            KeyEvent.KEYCODE_NUMPAD_9,
        )
        keys.forEachIndexed { digit, key ->
            val expected = ('0'.code + digit).toChar()
            assertEquals(expected, channelNumberCharacterForKey(key))
            assertEquals(expected, channelNumberCharacterForKey(numpadKeys[digit]))
        }
        assertEquals('.', channelNumberCharacterForKey(KeyEvent.KEYCODE_PERIOD))
        assertEquals('.', channelNumberCharacterForKey(KeyEvent.KEYCODE_NUMPAD_DOT))
        assertNull(channelNumberCharacterForKey(KeyEvent.KEYCODE_DPAD_UP))
    }

    @Test
    fun `number lookup ignores surrounding whitespace and leading zeroes`() {
        val seven = channel("Seven", "7")
        assertSame(seven, findChannelByNumber(listOf(seven), " 007 "))
    }

    @Test
    fun `decimal subchannels normalize leading and trailing zeroes`() {
        val subchannel = channel("Subchannel", "24.20")
        assertSame(subchannel, findChannelByNumber(listOf(subchannel), "024.200"))
    }

    @Test
    fun `first playlist entry wins when channel numbers are duplicated`() {
        val first = channel("First", "18")
        val second = channel("Second", "018.0")
        assertSame(first, findChannelByNumber(listOf(first, second), "18.00"))
    }

    @Test
    fun `blank missing and non numeric numbers never tune`() {
        val channels = listOf(channel("No number", ""), channel("Text id", "CS055"))
        assertNull(findChannelByNumber(channels, ""))
        assertNull(findChannelByNumber(channels, "8"))
        assertNull(findChannelByNumber(channels, "7.1"))
        assertNull(findChannelByNumber(channels, "7e1"))
    }
}
