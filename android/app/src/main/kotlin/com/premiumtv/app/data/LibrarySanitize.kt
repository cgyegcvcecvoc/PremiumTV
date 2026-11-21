package com.premiumtv.app.data

/**
 * Row identity for the lists the UI renders in a Lazy grid or column (1.1.17).
 *
 * Compose's lazy layouts key their rows, and a lazy layout with two identical
 * keys throws `IllegalArgumentException` during measure - it does not skip the
 * duplicate row. The browser keys a channel card by `id|url`, the category rail
 * by group name, the Movies & Shows grid by catalogue id; that is honest
 * identity, but it only works while the data really is unique.
 *
 * The bundled data is unique (build_bundle.py writes it that way), yet a
 * *refreshed* library is whatever the upstream playlist says: the downloader
 * parses it directly, and nothing stopped a duplicated `#EXTINF` block, a
 * repeated `groups.jsonl` line, or a catalogue document that lists one id
 * twice from reaching the browser and stopping the app on the next tab switch.
 * The app's own bug check already reports duplicate URLs as a warning, so the
 * possibility is not hypothetical.
 *
 * These are the pure fixes: de-duplicate at the data boundary, where the row
 * count is still small enough to matter, and let every UI key stay meaningful.
 * A library that was already unique is returned as the same instance, so the
 * common path allocates nothing.
 */

/** Drops a second channel row with the same EPG id and stream URL. */
internal fun dedupeChannels(channels: List<Channel>): List<Channel> {
    if (channels.size < 2) return channels
    val seen = HashSet<String>(channels.size * 2)
    val out = ArrayList<Channel>(channels.size)
    for (channel in channels) {
        // \u0000 cannot occur in either field, so the pair cannot collide.
        if (seen.add(channel.id + "\u0000" + channel.url)) out.add(channel)
    }
    return if (out.size == channels.size) channels else out
}

/** Drops a second category row with the same name, keeping the first. */
internal fun dedupeGroups(groups: List<CategoryGroup>): List<CategoryGroup> {
    if (groups.size < 2) return groups
    val seen = HashSet<String>(groups.size * 2)
    val out = ArrayList<CategoryGroup>(groups.size)
    for (group in groups) {
        if (seen.add(group.name)) out.add(group)
    }
    return if (out.size == groups.size) groups else out
}

/** The key a channel card uses; unique once [dedupeChannels] has run. */
internal fun channelRowKey(channel: Channel): String = "${channel.id}|${channel.url}"
