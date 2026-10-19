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
}
