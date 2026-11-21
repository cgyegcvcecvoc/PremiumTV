package com.premiumtv.app.update

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.rules.TemporaryFolder
import java.util.Date

/**
 * 1.1.14 "crash diagnostics": the record the last-chance handler writes has to
 * be readable again, or Settings still has nothing to show and a crash can only
 * be reported as "it crashed".
 */
class CrashLogTest {

    @get:Rule
    val folder = TemporaryFolder()

    @Test
    fun `a written crash round-trips with its message and frames`() {
        val throwable = IllegalStateException("player released")
        assertTrue(CrashLog.write(folder.root, Thread.currentThread(), throwable))

        val crash = CrashLog.read(folder.root)
        assertNotNull(crash)
        crash!!
        assertEquals("java.lang.IllegalStateException: player released", crash.summary)
        assertTrue(crash.frames.isNotEmpty())
        assertTrue(crash.frames.first().contains("CrashLogTest"))
        assertTrue(crash.recordedAt.isNotBlank())
    }

    @Test
    fun `the recorded thread is kept for the report`() {
        val throwable = RuntimeException("boom")
        CrashLog.write(folder.root, Thread.currentThread(), throwable)
        assertEquals(Thread.currentThread().name, CrashLog.read(folder.root)?.thread)
    }

    @Test
    fun `no record reads as no crash`() {
        assertNull(CrashLog.read(folder.root))
    }

    @Test
    fun `an empty or truncated record never becomes a blank crash`() {
        assertNull(CrashLog.parse(""))
        assertNull(CrashLog.parse(null))
        val truncated = "time=Fri Nov 20\nthread=main\njava.lang.OutOfMemoryError: no message\n"
        val parsed = CrashLog.parse(truncated)
        assertNotNull(parsed)
        assertEquals("java.lang.OutOfMemoryError: no message", parsed!!.summary)
    }

    @Test
    fun `clearing removes the record so an old crash stops showing`() {
        CrashLog.write(folder.root, Thread.currentThread(), RuntimeException("once"))
        assertNotNull(CrashLog.read(folder.root))

        assertTrue(CrashLog.clear(folder.root))
        assertNull(CrashLog.read(folder.root))
        assertFalse(CrashLog.file(folder.root).exists())
        // Clearing again is harmless.
        assertTrue(CrashLog.clear(folder.root))
    }

    @Test
    fun `the described line names the error and the first frame`() {
        val crash = CrashLog.parse(
            CrashLog.format(Date(), "main", IllegalArgumentException("bad feed")),
        )!!
        val line = CrashLog.describe(crash)
        assertTrue(line.startsWith("java.lang.IllegalArgumentException: bad feed"))
        assertTrue(line.length <= 220)
    }
}
