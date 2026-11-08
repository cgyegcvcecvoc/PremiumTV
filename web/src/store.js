/* Browser storage is optional: private mode and blocked storage must not
 * prevent watching TV. Pure policies are exported for the offline tests. */
(function (root) {
  "use strict";
  const memory = new Map();
  let persistent = true;
  const storage = {
    getItem(key) {
      try {
        return root.localStorage.getItem(key);
      } catch (_) {
        persistent = false;
        return memory.get(key) || null;
      }
    },
    setItem(key, value) {
      memory.set(key, String(value));
      try {
        root.localStorage.setItem(key, String(value));
      } catch (_) {
        persistent = false;
      }
    },
    removeItem(key) {
      memory.delete(key);
      try {
        root.localStorage.removeItem(key);
      } catch (_) {
        persistent = false;
      }
    },
  };
  try {
    root.localStorage.setItem("premiumtv.web.probe", "1");
    root.localStorage.removeItem("premiumtv.web.probe");
  } catch (_) {
    persistent = false;
  }
  const KEYS = {
    favorites: "premiumtv.favorites.v1",
    recent: "premiumtv.recents.v1",
    positions: "premiumtv.vod.positions.v1",
    sleep: "premiumtv.web.sleep.v1",
    prefs: "premiumtv.web.prefs.v1",
    audio: "premiumtv.audio.v1",
  };
  function read(key, fallback) {
    try {
      const value = JSON.parse(storage.getItem(key));
      return value == null ? fallback : value;
    } catch (_) {
      return fallback;
    }
  }
  function write(key, value) {
    storage.setItem(key, JSON.stringify(value));
  }
  function normalize(query) {
    return String(query || "")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .toLowerCase()
      .trim();
  }
  function matches(channel, query) {
    const text = normalize(
      [
        channel.name,
        channel.group,
        channel.country,
        channel.chno,
        channel.id,
      ].join(" "),
    );
    return normalize(query)
      .split(/\s+/)
      .filter(Boolean)
      .every((word) => text.includes(word));
  }
  function sortChannels(channels, order) {
    const result = channels.slice();
    const name = (a, b) =>
      String(a.name).localeCompare(String(b.name), undefined, {
        numeric: true,
        sensitivity: "base",
      });
    if (order === "az") result.sort(name);
    if (order === "za") result.sort((a, b) => name(b, a));
    if (order === "number")
      result.sort(
        (a, b) =>
          (parseInt(a.chno, 10) || Number.MAX_SAFE_INTEGER) -
            (parseInt(b.chno, 10) || Number.MAX_SAFE_INTEGER) || name(a, b),
      );
    return result;
  }
  function sortGroups(groups, order) {
    const result = groups.slice();
    const name = (a, b) =>
      a.name.localeCompare(b.name, undefined, { sensitivity: "base" });
    if (order === "az") result.sort(name);
    if (order === "za") result.sort((a, b) => name(b, a));
    if (order === "big" || order === "number")
      result.sort((a, b) => b.count - a.count || name(a, b));
    return result;
  }
  function positions() {
    const value = read(KEYS.positions, {});
    return value && typeof value === "object" && !Array.isArray(value)
      ? value
      : {};
  }
  function resumeAt(store, duration) {
    const at = Number(store);
    return Number.isFinite(at) &&
      at >= 5 &&
      (!Number.isFinite(duration) || at < duration - 12)
      ? at
      : 0;
  }
  function savePosition(id, seconds, duration) {
    if (!id || !Number.isFinite(seconds)) return;
    const value = positions();
    if (Number.isFinite(duration) && duration > 20 && seconds >= duration - 12)
      delete value[id];
    else if (seconds >= 5) value[id] = Math.floor(seconds);
    else return;
    write(KEYS.positions, value);
  }
  function sleepRemaining(end, now) {
    return Math.max(0, (Number(end) || 0) - now);
  }
  function sleepLabel(ms) {
    if (ms <= 0) return "Off";
    const min = Math.ceil(ms / 60000);
    return min < 60
      ? `${min} min`
      : `${Math.floor(min / 60)} hr${min % 60 ? ` ${min % 60} min` : ""}`;
  }
  function validateLibrary(meta, channels, groups) {
    if (
      !meta ||
      meta.platform !== "web" ||
      !/^[a-f0-9]{16}$/.test(meta.build_id)
    )
      throw new Error("This is not a valid PremiumTV web library.");
    if (
      !Array.isArray(channels) ||
      !channels.length ||
      !Array.isArray(groups) ||
      !groups.length
    )
      throw new Error("The library is empty or incomplete.");
    if (
      channels.some(
        (c) =>
          !c ||
          typeof c.name !== "string" ||
          !c.name ||
          typeof c.url !== "string" ||
          !/^https?:\/\//i.test(c.url) ||
          typeof c.group !== "string",
      )
    )
      throw new Error("The channel list contains an invalid entry.");
    if (
      groups.some(
        (g) => !g || typeof g.name !== "string" || !Number.isFinite(g.count),
      )
    )
      throw new Error("The category list is invalid.");
    return true;
  }
  const api = {
    KEYS,
    storage,
    read,
    write,
    normalize,
    matches,
    sortChannels,
    sortGroups,
    positions,
    resumeAt,
    savePosition,
    sleepRemaining,
    sleepLabel,
    validateLibrary,
    get persistent() {
      return persistent;
    },
  };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  root.PremiumStore = api;
})(typeof window !== "undefined" ? window : globalThis);
