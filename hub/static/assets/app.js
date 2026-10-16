/* PremiumTV Download Hub front-end */
(function () {
  "use strict";

  var $ = function (s, el) { return (el || document).querySelector(s); };

  function fmtSize(b) {
    if (b == null) return "";
    if (b >= 1 << 30) return (b / (1 << 30)).toFixed(2) + " GB";
    if (b >= 1 << 20) return (b / (1 << 20)).toFixed(1) + " MB";
    if (b >= 1 << 10) return Math.round(b / 1024) + " KB";
    return b + " B";
  }
  function fmtNum(n) { return n == null ? "—" : n.toLocaleString("en-US"); }
  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  /* ---- copy to clipboard with toast ---- */
  var toastTimer;
  function toast(msg) {
    var t = $("#toast");
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.classList.remove("show"); }, 1800);
  }
  function copy(text) {
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = text;
      ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); toast("Copied!"); }
      catch (e) { toast("Copy failed — long-press the link instead"); }
      document.body.removeChild(ta);
    }
    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(function () { toast("Copied!"); }, fallback);
    } else fallback();
  }
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-copy]");
    if (el) { e.preventDefault(); copy(el.getAttribute("data-copy")); }
  });

  /* ---- mobile nav ---- */
  $("#nav-toggle").addEventListener("click", function () { $("#nav").classList.toggle("open"); });
  $("#nav").addEventListener("click", function () { $("#nav").classList.remove("open"); });

  /* ---- render helpers ---- */
  function copyBtn(url, label) {
    return '<button class="chip-btn" data-copy="' + esc(url) + '">' + (label || "Copy URL") + "</button>";
  }
  function dlBtn(href, label, primary) {
    return '<a class="chip-btn' + (primary ? " primary" : "") + '" href="' + esc(href) + '" download>' + (label || "⬇ Download") + "</a>";
  }

  function plCard(p) {
    var meta = [];
    if (p.channels) meta.push(fmtNum(p.channels) + " channels");
    meta.push(fmtSize(p.size));
    return (
      '<div class="pl-card">' +
      "<h4>" + esc(p.label) + "</h4>" +
      '<div class="pl-meta">' + meta.join(" · ") + " · <code>" + esc(p.name) + "</code></div>" +
      '<p class="pl-desc">' + esc(p.desc || "") + "</p>" +
      '<div class="pl-actions">' + dlBtn(p.dl + "?dl=1", "⬇ Download", true) +
      (p.raw ? copyBtn(p.raw) : "") + "</div></div>"
    );
  }

  fetch("data.json").then(function (r) { return r.json(); }).then(function (D) {
    /* ---- hero stats ---- */
    $("#stat-channels").textContent = fmtNum(D.stats.working);
    $("#stat-countries").textContent = fmtNum(D.stats.countries);
    $("#stat-links").textContent = fmtNum(D.stats.unique);
    $("#hero-meta").textContent =
      "Library last re-checked " + D.stats.updated_local + " (" + D.stats.run_label + "). Hub data built " + D.generated_utc + ".";
    $("#footer-updated").textContent = " Library updated " + D.stats.updated + ".";
    $("#about-stats").innerHTML =
      "Right now: <strong>" + fmtNum(D.stats.working) + " working channels</strong> out of " +
      fmtNum(D.stats.unique) + " unique links checked, split across <strong>" + fmtNum(D.stats.countries) +
      " countries</strong> and " + fmtNum(D.stats.categories) + "+ category playlists, with XMLTV guide data for most of the lineup.";

    /* ---- apps: featured cards ---- */
    var stableApk = null, previewApk = null;
    D.android.forEach(function (a) {
      if (!stableApk && a.channel === "Stable") stableApk = a;
      if (!previewApk && a.channel === "Preview") previewApk = a;
    });
    // prefer the published stable (1.0.2) as the headline stable
    D.android.forEach(function (a) { if (a.version === "1.0.2") stableApk = a; });

    var macStable = D.macos[0], macPreview = D.macos[1];
    var appCards = "";

    if (stableApk) {
      appCards +=
        '<div class="app-card featured"><span class="badge stable">Stable</span>' +
        "<h3>Android TV · Fire TV</h3>" +
        '<p class="app-kind">APK · v' + esc(stableApk.version) + " · " + fmtSize(stableApk.size) + "</p>" +
        '<p class="app-desc">' + esc(stableApk.desc) + " Served directly from this hub.</p>" +
        '<div class="app-actions"><div class="dl-row"><span class="fname">' + esc(stableApk.name) + "</span>" +
        '<a class="dl" href="' + esc(stableApk.dl) + '" download>⬇ APK</a></div>' +
        '<div class="dl-row"><span class="fname">Direct link for the Downloader app</span>' +
        '<a class="dl alt2" href="#" data-copy="' + esc(location.origin + stableApk.dl) + '">Copy link</a></div></div></div>';
    }
    if (macStable) {
      var dmg = macStable.assets[0], dmgIntel = macStable.assets[2];
      appCards +=
        '<div class="app-card"><span class="badge stable">Stable</span>' +
        "<h3>macOS</h3>" +
        '<p class="app-kind">DMG / PKG · v' + esc(macStable.version) + " · ~135 MB</p>" +
        '<p class="app-desc">' + esc(macStable.desc) + "</p>" +
        '<div class="app-actions">' +
        '<div class="dl-row"><span class="fname">Apple Silicon (M-series)</span><a class="dl" href="' + esc(dmg.url) + '">⬇ DMG</a></div>' +
        '<div class="dl-row"><span class="fname">Intel Macs</span><a class="dl" href="' + esc(dmgIntel.url) + '">⬇ DMG</a></div>' +
        "</div></div>";
    }
    if (previewApk) {
      appCards +=
        '<div class="app-card"><span class="badge preview">Preview</span>' +
        "<h3>Preview — cable-style guide</h3>" +
        '<p class="app-kind">Android APK v' + esc(previewApk.version) + " · " + fmtSize(previewApk.size) +
        (macPreview ? " · also for macOS below" : "") + "</p>" +
        '<p class="app-desc">' + esc(previewApk.desc) + "</p>" +
        '<div class="app-actions"><div class="dl-row"><span class="fname">' + esc(previewApk.name) + "</span>" +
        '<a class="dl" href="' + esc(previewApk.dl) + '" download>⬇ APK</a></div>' +
        (macPreview ? '<div class="dl-row"><span class="fname">macOS preview (Apple Silicon)</span><a class="dl alt2" href="' +
          esc(macPreview.assets[0].url) + '">⬇ DMG</a></div>' : "") +
        "</div></div>";
    }
    $("#app-grid").innerHTML = appCards;

    /* ---- apps: full APK table ---- */
    $("#apk-table tbody").innerHTML = D.android.map(function (a) {
      return "<tr><td><strong>v" + esc(a.version) + "</strong></td><td>" + esc(a.channel) + "</td><td>" +
        fmtSize(a.size) + '</td><td><span class="hash">' + a.sha256 + "</span></td><td>" +
        '<a class="chip-btn primary" href="' + esc(a.dl) + '" download>⬇ APK</a></td></tr>';
    }).join("");

    /* ---- apps: all mac installers ---- */
    $("#mac-list").innerHTML = D.macos.map(function (m) {
      return "<h4 style='margin:10px 0 8px'>PremiumTV " + esc(m.version) + " — " + esc(m.channel) + "</h4>" +
        m.assets.map(function (a) {
          return '<div class="dl-row" style="margin-bottom:8px"><span class="fname">' + esc(a.label) +
            ' <span class="meta">(' + esc(a.name) + ')</span></span><a class="dl" href="' + esc(a.url) + '">⬇ Download</a></div>';
        }).join("");
    }).join("");

    /* ---- featured playlists & bundles ---- */
    $("#featured-grid").innerHTML = D.featured.map(plCard).join("");
    $("#bundle-grid").innerHTML = D.bundles.map(function (b) {
      return '<div class="pl-card"><h4>' + esc(b.label) + "</h4>" +
        '<div class="pl-meta">' + b.files + " files · " + fmtSize(b.size) + " zipped</div>" +
        '<p class="pl-desc">' + esc(b.desc) + "</p>" +
        '<div class="pl-actions">' + dlBtn(b.dl, "⬇ Download zip", true) + "</div></div>";
    }).join("");

    /* ---- category chips ---- */
    function renderCats(which) {
      var list = D.categories[which] || [];
      $("#cat-list").innerHTML = list.map(function (c) {
        return '<span class="chip">' + esc(c.label) +
          ' <span class="n">' + fmtNum(c.channels) + "</span>" +
          ' <a href="' + esc(c.dl + "?dl=1") + '" download>⬇</a>' +
          (c.raw ? ' <a href="#" data-copy="' + esc(c.raw) + '" title="Copy playlist URL">🔗</a>' : "") +
          "</span>";
      }).join("");
    }
    renderCats("published");
    document.querySelectorAll("#cat-tabs .tab").forEach(function (t) {
      t.addEventListener("click", function () {
        document.querySelectorAll("#cat-tabs .tab").forEach(function (x) { x.classList.remove("active"); });
        t.classList.add("active");
        renderCats(t.getAttribute("data-cat"));
      });
    });

    /* ---- countries ---- */
    var grid = $("#country-grid");
    function countryCard(c) {
      return '<div class="country-card" data-name="' + esc(c.label.toLowerCase()) + '">' +
        '<div class="cname">' + esc(c.label) + "</div>" +
        '<div class="cmeta">' + fmtNum(c.channels) + " channels · " + fmtSize(c.size) + "</div>" +
        '<div class="pl-actions">' +
        dlBtn(c.dl + "?dl=1", "⬇ M3U", true) +
        (c.raw ? copyBtn(c.raw, "Copy URL") : "") +
        (c.epg ? '<a class="chip-btn" href="' + esc(c.epg + "?dl=1") + '" download title="XMLTV guide (' + fmtSize(c.epg_size) + ')">Guide</a>' : "") +
        "</div></div>";
    }
    function renderCountries(q) {
      var qq = (q || "").trim().toLowerCase();
      var aliases = { uk: "united kingdom", us: "usa", uae: "united arab emirates" };
      if (aliases[qq]) qq = aliases[qq];
      var list = D.countries.filter(function (c) {
        return !qq || c.label.toLowerCase().indexOf(qq) !== -1;
      });
      // Put the big ones first when not searching
      if (!qq) {
        var pin = ["USA", "United Kingdom", "Canada", "India", "China", "Germany", "France", "Spain", "Mexico", "Brazil", "Australia", "Italy"];
        list = list.slice().sort(function (a, b) {
          var ia = pin.indexOf(a.label), ib = pin.indexOf(b.label);
          ia = ia === -1 ? 99 : ia; ib = ib === -1 ? 99 : ib;
          return ia - ib || a.label.localeCompare(b.label);
        });
      }
      grid.innerHTML = list.length
        ? list.map(countryCard).join("")
        : '<div class="country-empty">No playlist for that search — try the "Everything" playlist above, or the International playlist.</div>';
    }
    renderCountries("");
    $("#country-search").addEventListener("input", function (e) { renderCountries(e.target.value); });

    /* ---- EPG ---- */
    $("#epg-grid").innerHTML = D.epg.map(function (g) {
      return '<div class="pl-card"><h4>' + esc(g.label) + "</h4>" +
        '<div class="pl-meta">' + fmtSize(g.size) + " · <code>" + esc(g.name) + "</code></div>" +
        '<p class="pl-desc">XMLTV format — paste into any player that asks for an EPG URL, or download the file.</p>' +
        '<div class="pl-actions">' + dlBtn(g.dl + "?dl=1", "⬇ Download", true) + copyBtn(g.raw) + "</div></div>";
    }).join("");
  }).catch(function (err) {
    $("#hero-meta").textContent = "Could not load library data (" + err + "). Try refreshing.";
  });
})();
