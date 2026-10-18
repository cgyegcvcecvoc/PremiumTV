package com.premiumtv.app.ui

import org.junit.Assert.assertEquals
import org.junit.Test

/** Which placeholder picture each category gets, on the plain JVM. */
class ChannelLogoTest {

    @Test fun categoriesGetTheirOwnPicture() {
        assertEquals("ball", iconKeyForGroup("Sports"))
        assertEquals("ball", iconKeyForGroup("Sports Backups"))
        assertEquals("ball", iconKeyForGroup("NBC Sports Channels"))
        assertEquals("ball", iconKeyForGroup("NHL Hockey"))
        assertEquals("ball", iconKeyForGroup("Soccer"))
        assertEquals("smile", iconKeyForGroup("Comedy"))
        assertEquals("smile", iconKeyForGroup("Comedy Backups"))
        assertEquals("news", iconKeyForGroup("News"))
        assertEquals("balloon", iconKeyForGroup("Kids"))
        assertEquals("balloon", iconKeyForGroup("Cartoons"))
        assertEquals("music", iconKeyForGroup("Music"))
        assertEquals("movie", iconKeyForGroup("Movies"))
        assertEquals("weather", iconKeyForGroup("Weather"))
        assertEquals("book", iconKeyForGroup("Documentary"))
        assertEquals("book", iconKeyForGroup("Education"))
        assertEquals("chart", iconKeyForGroup("Business"))
        assertEquals("star", iconKeyForGroup("Entertainment"))
        assertEquals("star", iconKeyForGroup("Tv Celebrities"))
        assertEquals("star", iconKeyForGroup("Game Shows"))
        assertEquals("cross", iconKeyForGroup("Religious"))
        assertEquals("law", iconKeyForGroup("Legislative"))
        assertEquals("heart", iconKeyForGroup("Lifestyle"))
        assertEquals("heart", iconKeyForGroup("Family"))
        assertEquals("globe", iconKeyForGroup("International"))
        assertEquals("globe", iconKeyForGroup("Global TV"))
    }

    @Test fun everythingElseGetsTheTelevisionSet() {
        assertEquals("tv", iconKeyForGroup("Other"))
        assertEquals("tv", iconKeyForGroup("Classic TV"))
        assertEquals("tv", iconKeyForGroup("CBS"))
        assertEquals("tv", iconKeyForGroup(""))
    }
}
