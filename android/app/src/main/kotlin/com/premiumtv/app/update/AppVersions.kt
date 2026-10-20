package com.premiumtv.app.update

/**
 * Version comparison for the in-app updater.
 *
 * Versions are `MAJOR.MINOR.PATCH` or `MAJOR.MINOR.PATCH.HOTFIX`.  The fourth
 * component is for small fixes to a stable line (`1.0.6.1`), so an installed
 * 1.0.6 can be offered 1.0.6.1 without waiting for 1.0.7.  A missing component
 * counts as zero, and only the numeric parts decide whether a release is an
 * update, so a debug APK's `-debug` suffix cannot change the answer.
 *
 * 1.0.8 V1 Patch establishes the V series: 1.0.8 V1 = 1.0.8.1 (alias 1.0.9),
 * V2 = 1.0.8.2 (alias 1.0.10) ... the same compatibility-alias rule as 1.0.7,
 * with the V name shown in Settings so future Vs order predictably.
 */
object AppVersions {

    /**
     * Releases that exist only so an updater which cannot read a four-part
     * version (1.0.4-1.0.6) can reach the canonical build.  They carry the
     * same app code; an install already running the canonical build ignores
     * them instead of downloading the same APK again.
     */
    private val COMPATIBILITY_ALIASES = mapOf(
        "1.0.7" to "1.0.6.1",
        "1.0.9" to "1.0.8.1",
        "1.0.10" to "1.0.8.2",
        "1.0.11" to "1.0.8.3",
        "1.0.12" to "1.0.8.4",
        "1.0.13" to "1.0.8.5",
    )

    /** Human-facing V display: 1.0.8.1 -> 1.0.8 V1, 1.0.8 stays 1.0.8. */
    fun display(version: String): String? {
        val normalized = normalize(version) ?: return null
        val parts = normalized.split(".")
        return if (parts.size == 4) "${parts[0]}.${parts[1]}.${parts[2]} V${parts[3]}" else normalized
    }

    /** Next V patch after a base: patch("1.0.8", 1) -> "1.0.8.1". */
    fun patch(base: String, v: Int): String? {
        val n = normalize(base) ?: return null
        if (n.split(".").size != 3 || v < 1 || v > 9999) return null
        return "$n.$v"
    }

    /** The version a compatibility alias stands for, or the version itself. */
    fun canonical(version: String): String? {
        val normalized = normalize(version) ?: return null
        return COMPATIBILITY_ALIASES[normalized] ?: normalized
    }

    /**
     * True when [candidate] is a registered alias of the build [current] runs.
     *
     * The canonical version itself is not an alias, even though [canonical]
     * maps it to itself: only 1.0.7 stands for 1.0.6.1, never the other way.
     */
    fun isCompatibilityAlias(candidate: String, current: String): Boolean {
        val normalized = normalize(candidate) ?: return false
        val canonicalCandidate = COMPATIBILITY_ALIASES[normalized] ?: return false
        return canonicalCandidate == canonical(current)
    }

    /** Returns up to four numeric parts, or null for foreign text. */
    fun parse(version: String): List<Int>? {
        val clean = version.trim()
            .removePrefix("v")
            .substringBefore('-')
            .substringBefore('+')
        if (clean.isBlank()) return null
        val parts = clean.split('.')
        if (parts.size !in 3..4) return null
        val numbers = parts.map { part ->
            if (part.isEmpty() || part.any { !it.isDigit() }) return null
            part.toIntOrNull() ?: return null
        }
        return numbers + List(4 - numbers.size) { 0 }
    }

    /** Normalised "1.0.6" / "1.0.6.1" form, or null when it is unreadable. */
    fun normalize(version: String): String? {
        val values = parse(version) ?: return null
        val last = values.indexOfLast { it != 0 }
        if (last < 2) return values.take(3).joinToString(".")
        return values.take(last + 1).joinToString(".")
    }

    /** True only when [candidate] is strictly above [current]. */
    fun isNewer(candidate: String, current: String): Boolean {
        val left = parse(candidate) ?: return false
        val right = parse(current) ?: return false
        for (index in 0 until 4) {
            if (left[index] != right[index]) return left[index] > right[index]
        }
        return false
    }
}
