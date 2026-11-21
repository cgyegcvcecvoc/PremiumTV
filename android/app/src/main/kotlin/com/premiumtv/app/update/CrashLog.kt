package com.premiumtv.app.update

import java.io.File
import java.util.Date

/** One recorded fatal error, as written by the last-chance handler. */
data class RecordedCrash(
    /** When the crash happened, exactly as the handler recorded it. */
    val recordedAt: String,
    /** The thread that died, for example "main". */
    val thread: String,
    /** "java.lang.NullPointerException: message", the line to quote in a report. */
    val summary: String,
    /** The recorded stack frames, innermost first. */
    val frames: List<String>,
    /** The file's full text, so a viewer can read every recorded frame. */
    val text: String,
)

/**
 * The device-local record of the last fatal error.
 *
 * 1.1.12 started writing this file from a default uncaught-exception handler,
 * but nothing ever read it: the file lives in the app's private storage, so a
 * viewer could not reach it and a report could only say "it crashed". This
 * turns the same record into something Settings can show, quote and clear.
 *
 * It never leaves the device. There is no upload, no identifier and no
 * third-party service: the text is shown in the app and the viewer decides
 * whether to send it.
 */
object CrashLog {

    const val FILE_NAME = "last-crash.txt"

    /** The handler records at most this many frames; Settings shows the same. */
    const val MAX_FRAMES = 24

    fun file(dir: File): File = File(dir, FILE_NAME)

    /** Writes the record. Never throws: a dying process must reach the OS. */
    fun write(dir: File, thread: Thread, throwable: Throwable, now: Date = Date()): Boolean = try {
        file(dir).writeText(format(now, thread.name, throwable))
        true
    } catch (_: Throwable) {
        false
    }

    /** The record's text, in the one shape [parse] understands. */
    fun format(now: Date, threadName: String, throwable: Throwable): String = buildString {
        append("time=").append(now.toString()).append('\n')
        append("thread=").append(threadName).append('\n')
        append(throwable.javaClass.name).append(": ")
        append(throwable.message ?: "(no message)").append('\n')
        throwable.stackTrace.take(MAX_FRAMES).forEach { append("  at ").append(it).append('\n') }
    }

    /** The last recorded crash, or null when there is none (or it is unreadable). */
    fun read(dir: File): RecordedCrash? {
        val text = try {
            file(dir).readText()
        } catch (_: Throwable) {
            return null
        }
        return parse(text)
    }

    /** Deletes the record so an old crash stops being reported. */
    fun clear(dir: File): Boolean = try {
        !file(dir).exists() || file(dir).delete()
    } catch (_: Throwable) {
        false
    }

    /**
     * Parses the handler's own format. Kept tolerant on purpose: the file is
     * written by a process that is already dying, so a truncated record still
     * yields whatever was saved instead of nothing at all.
     */
    fun parse(text: String?): RecordedCrash? {
        val lines = text?.lines()?.filter { it.isNotBlank() } ?: return null
        if (lines.isEmpty()) return null
        val recordedAt = lines.firstOrNull { it.startsWith("time=") }
            ?.removePrefix("time=")?.trim().orEmpty()
        val thread = lines.firstOrNull { it.startsWith("thread=") }
            ?.removePrefix("thread=")?.trim().orEmpty()
        val frames = lines.filter { it.trimStart().startsWith("at ") }
            .map { it.trim() }
        val summary = lines.firstOrNull { line ->
            !line.startsWith("time=") && !line.startsWith("thread=") &&
                !line.trimStart().startsWith("at ")
        }?.trim()
        if (summary.isNullOrBlank() && frames.isEmpty()) return null
        return RecordedCrash(
            recordedAt = recordedAt,
            thread = thread,
            summary = summary ?: "The app stopped unexpectedly",
            frames = frames.take(MAX_FRAMES),
            text = text,
        )
    }

    /** The one-line shape Settings shows next to the record. */
    fun describe(crash: RecordedCrash): String = buildString {
        append(crash.summary)
        crash.frames.firstOrNull()?.let { append(" · ").append(it) }
        if (crash.recordedAt.isNotBlank()) append(" · ").append(crash.recordedAt)
    }.let { it.replace(Regex("\\s+"), " ").trim() }.let {
        if (it.length <= 220) it else it.take(217) + "…"
    }

}
