package com.premiumtv.app.update

/**
 * Version comparison for the in-app updater.
 *
 * The installed app can be a stable build (1.0.4) or a preview (1.1.1), and
 * debug APKs carry a "-debug" suffix in `versionName`.  Only the numeric
 * MAJOR.MINOR.PATCH part decides whether a release is an update, so a preview
 * is never offered a stable build below it and a stable build is never offered
 * an older release because two strings happened to sort differently.
 */
object AppVersions {

    /** Returns the numeric MAJOR.MINOR.PATCH parts, or null for foreign text. */
    fun parse(version: String): List<Int>? {
        val clean = version.trim()
            .removePrefix("v")
            .substringBefore('-')
            .substringBefore('+')
        if (clean.isBlank()) return null
        val parts = clean.split('.')
        if (parts.size != 3) return null
        val numbers = parts.map { part ->
            if (part.isEmpty() || part.any { !it.isDigit() }) return null
            part.toIntOrNull() ?: return null
        }
        return numbers
    }

    /** Normalised "1.0.4" form, or the input unchanged when it is unreadable. */
    fun normalize(version: String): String? {
        val parts = parse(version) ?: return null
        return parts.joinToString(".")
    }

    /** True only when [candidate] is strictly above [current]. */
    fun isNewer(candidate: String, current: String): Boolean {
        val left = parse(candidate) ?: return false
        val right = parse(current) ?: return false
        for (index in 0 until 3) {
            if (left[index] != right[index]) return left[index] > right[index]
        }
        return false
    }
}
