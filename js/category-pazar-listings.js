(function () {
  "use strict";

  var TXT = {
    heading: { tr: "Şu An Satıştaki İlanlar", en: "Current Listings" },
    empty: { tr: "Şu an bu kategoride yayında bir ilan yok. WhatsApp üzerinden bize ulaşabilirsiniz.", en: "There are no published listings in this category right now. Feel free to reach us on WhatsApp." },
    cta: { tr: "İlan Detayını Gör →", en: "View Listing →" },
    loading: { tr: "Yükleniyor...", en: "Loading..." },
  };

  function getLang() {
    var stored = localStorage.getItem("gnd-site-lang");
    return stored === "tr" ? "tr" : "en";
  }

  function t(key) {
    return TXT[key][getLang()];
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s || "";
    return d.innerHTML;
  }

  var cachedListings = null;

  function render(container, kategori) {
    var lang = getLang();
    if (!cachedListings || !cachedListings.length) {
      container.innerHTML = '<p class="section-sub">' + t("empty") + "</p>";
      return;
    }
    container.innerHTML =
      '<h2 style="margin-bottom:16px">' + t("heading") + "</h2>" +
      '<div class="category-grid">' +
      cachedListings.map(function (r) {
        var photos = r.foto_urls && r.foto_urls.length ? r.foto_urls : [];
        var imgHtml = photos.length
          ? '<div class="category-photo-wrap"><img class="category-photo" src="' + escapeHtml(photos[0]) + '" loading="lazy"></div>'
          : "";
        var specBits = [r.model_yili, r.motor_saati, r.tonaj, r.yakit_tipi].filter(Boolean).map(escapeHtml);
        var specLine = specBits.length ? "<p>" + specBits.join(" · ") + "</p>" : "";
        return (
          '<div class="category-card">' +
          imgHtml +
          "<h3>" + escapeHtml(r.baslik) + "</h3>" +
          "<p>" + (r.durum_bilgisi ? escapeHtml(r.durum_bilgisi) : "") + "</p>" +
          specLine +
          (r.fiyat ? "<p><strong>" + escapeHtml(r.fiyat) + "</strong></p>" : "") +
          '<a class="category-quote-btn" href="../pazar.html?id=' + encodeURIComponent(r.id) + '">' + t("cta") + "</a>" +
          "</div>"
        );
      }).join("") +
      "</div>";
  }

  document.addEventListener("DOMContentLoaded", async function () {
    var container = document.getElementById("categoryPazarListings");
    if (!container) return;
    var kategori = container.dataset.kategori;
    var altKategori = container.dataset.altKategori || null;
    if (!kategori || !window.gndSupabase) return;

    container.innerHTML = '<p class="section-sub">' + t("loading") + "</p>";

    var query = window.gndSupabase
      .from("market_requests")
      .select("*")
      .eq("onay_durumu", "yayinda")
      .eq("kategori", kategori)
      .eq("islem_turu", "satis")
      .order("created_at", { ascending: false })
      .limit(12);
    if (altKategori) query = query.eq("alt_kategori", altKategori);

    var { data, error } = await query;
    if (error) {
      container.innerHTML = "";
      return;
    }
    cachedListings = data || [];
    render(container, kategori);

    var sel = document.getElementById("lang-select");
    if (sel) {
      sel.addEventListener("change", function () { render(container, kategori); });
    }
  });
})();
