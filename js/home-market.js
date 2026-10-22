(function () {
  "use strict";

  var grid = document.getElementById("mkt-grid");
  if (!grid) return;
  var status = document.getElementById("mkt-status");
  var search = document.getElementById("mkt-search");
  var filters = document.getElementById("mkt-filters");
  var all = [];
  var filter = "all";
  var failed = false;

  function getLang() {
    var stored = localStorage.getItem("gnd-site-lang");
    return stored === "tr" || stored === "en" ? stored : (document.documentElement.lang === "en" ? "en" : "tr");
  }
  function tr(key) {
    var d = (typeof TRANSLATIONS !== "undefined" && TRANSLATIONS[getLang()]) || {};
    return d[key] || "";
  }
  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }
  function photoOf(r) {
    if (r.foto_urls && r.foto_urls.length) return r.foto_urls[0];
    var m = (r.aciklama || "").match(/^\[img:([^\]]+)\]/);
    return m ? m[1] : "";
  }

  function render() {
    var q = search ? search.value.trim().toLocaleLowerCase("tr") : "";
    var list = all.filter(function (r) {
      if (filter !== "all" && r.kategori !== filter) return false;
      if (!q) return true;
      var hay = [r.baslik, r.marka, r.model, r.alt_kategori, r.durum_bilgisi, r.model_yili, r.tonaj].join(" ").toLocaleLowerCase("tr");
      return hay.indexOf(q) !== -1;
    });
    grid.innerHTML = list.map(function (r) {
      var img = photoOf(r);
      var wanted = r.islem_turu !== "satis";
      var bits = [r.model_yili, r.motor_saati, r.tonaj, r.yakit_tipi].filter(Boolean).map(esc).join(" · ");
      return '<a class="mkt-card" href="pazar.html?id=' + encodeURIComponent(r.id) + '">' +
        '<div class="mkt-photo">' + (img ? '<img src="' + esc(img) + '" alt="' + esc(r.baslik) + '" loading="lazy">' : '<span class="mkt-nophoto">GND</span>') +
        (wanted ? '<span class="mkt-badge">' + esc(tr("mkt_badge_wanted")) + "</span>" : "") + "</div>" +
        '<div class="mkt-body"><h3>' + esc(r.baslik) + "</h3>" +
        (bits ? "<p>" + bits + "</p>" : "") +
        (r.fiyat ? '<p class="mkt-price">' + esc(r.fiyat) + "</p>" : "") + "</div></a>";
    }).join("");
    if (status) {
      status.hidden = false;
      if (failed) status.textContent = tr("mkt_error");
      else if (!list.length) status.textContent = tr("mkt_empty");
      else status.hidden = true;
    }
  }

  if (filters) {
    filters.addEventListener("click", function (e) {
      var b = e.target.closest("[data-f]");
      if (!b) return;
      filter = b.getAttribute("data-f");
      filters.querySelectorAll(".mkt-chip").forEach(function (c) { c.classList.toggle("active", c === b); });
      render();
    });
  }
  if (search) search.addEventListener("input", render);
  var sel = document.getElementById("lang-select");
  if (sel) sel.addEventListener("change", function () { setTimeout(render, 0); });

  document.addEventListener("DOMContentLoaded", async function () {
    if (!window.gndSupabase) { failed = true; render(); return; }
    var res = await window.gndSupabase.from("market_requests").select("*")
      .eq("onay_durumu", "yayinda").order("created_at", { ascending: false }).limit(60);
    if (res.error) failed = true; else all = res.data || [];
    render();
  });
})();
