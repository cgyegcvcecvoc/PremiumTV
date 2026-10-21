package com.premiumtv.app.update

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/** The version policy behind the in-app updater, including the 1.0.7 alias. */
class AppVersionsTest {

    @Test
    fun `four part versions sort above their three part parent`() {
        assertTrue(AppVersions.isNewer("1.0.6.1", "1.0.6"))
        assertFalse(AppVersions.isNewer("1.0.6", "1.0.6.1"))
        assertTrue(AppVersions.isNewer("1.1.0", "1.0.6.1"))
        assertFalse(AppVersions.isNewer("1.0.6.1", "1.1.0"))
    }

    @Test
    fun `normalize keeps only the parts that carry information`() {
        assertEquals("1.0.6.1", AppVersions.normalize("v1.0.6.1-debug"))
        assertEquals("1.0.6", AppVersions.normalize("1.0.6.0"))
    }

    @Test
    fun `the compatibility alias stands for the canonical build`() {
        assertEquals("1.0.6.1", AppVersions.canonical("1.0.7"))
        assertEquals("1.0.6.1", AppVersions.canonical("1.0.6.1"))
        assertTrue(AppVersions.isCompatibilityAlias("1.0.7", "1.0.6.1"))
        assertFalse(AppVersions.isCompatibilityAlias("1.0.7", "1.0.6"))
        assertFalse(AppVersions.isCompatibilityAlias("1.0.6.1", "1.0.6.1"))
    }

    @Test
    fun `1_0_9 is a real release and the V series is retired`() {
        // 1.0.9 briefly existed as the alias of 1.0.8.1 (the only V patch);
        // as a real release it must resolve to itself and read as newer
        // than 1.0.8.1, or the crash fix could never be offered.
        assertEquals("1.0.9", AppVersions.canonical("1.0.9"))
        assertEquals("1.0.10", AppVersions.canonical("1.0.10"))
        assertFalse(AppVersions.isCompatibilityAlias("1.0.9", "1.0.8.1"))
        assertFalse(AppVersions.isCompatibilityAlias("1.0.10", "1.0.8.2"))
        assertFalse(AppVersions.isCompatibilityAlias("1.0.8.1", "1.0.8.1"))
        assertTrue(AppVersions.isNewer("1.0.9", "1.0.8.1"))
        assertTrue(AppVersions.isNewer("1.0.8.1", "1.0.8"))
        // The historical names still resolve for old tags and screens.
        assertEquals("1.0.8 V1", AppVersions.display("1.0.8.1"))
        assertEquals("1.0.9", AppVersions.display("1.0.9"))
        assertEquals("1.0.8.1", AppVersions.patch("1.0.8", 1))
    }
}
