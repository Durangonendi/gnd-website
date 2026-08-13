(function () {
  "use strict";

  var currentTuru = "satis";
  var allListings = [];
  var currentFilter = "all";

  var TXT = {
    baslikSatis: { tr: "Makine / Parça Adı", en: "Machine / Part Name" },
    baslikAlim: { tr: "Aradığınız Makine / Parça", en: "Machine / Part You're Looking For" },
    fiyatSatis: { tr: "Fiyat Beklentisi", en: "Expected Price" },
    fiyatAlim: { tr: "Bütçeniz", en: "Your Budget" },
    badgeSatis: { tr: "Satış", en: "Sell" },
    badgeAlim: { tr: "Alım Talebi", en: "Buy Request" },
    waBtn: { tr: "WhatsApp'tan Sor →", en: "Ask on WhatsApp →" },
    noListings: { tr: "Şu an bu kategoride yayında bir talep yok.", en: "There are no published requests in this category right now." },
    loadError: { tr: "Talepler yüklenemedi: ", en: "Could not load requests: " },
  };

  function getLang() {
    return localStorage.getItem("gnd-site-lang") === "tr" ? "tr" : "en";
  }

  function t(key) {
    return TXT[key][getLang()];
  }

  function escapeHtml(s) {
    var d = document.createElement("div");
    d.textContent = s || "";
    return d.innerHTML;
  }

  function setTuru(turu) {
    currentTuru = turu;
    document.querySelectorAll('[data-turu]').forEach(function (btn) {
      btn.classList.toggle("active", btn.dataset.turu === turu);
    });
    document.getElementById("pazarTuru").value = turu;
    var durumWrap = document.getElementById("pazarDurumWrap");
    var baslikLabel = document.getElementById("pazarBaslikLabel");
    var fiyatLabel = document.getElementById("pazarFiyatLabel");
    if (turu === "satis") {
      durumWrap.style.display = "";
      baslikLabel.textContent = t("baslikSatis");
      fiyatLabel.textContent = t("fiyatSatis");
    } else {
      durumWrap.style.display = "none";
      baslikLabel.textContent = t("baslikAlim");
      fiyatLabel.textContent = t("fiyatAlim");
    }
  }

  function renderListings() {
    var listEl = document.getElementById("pazarList");
    var filtered = currentFilter === "all" ? allListings : allListings.filter(function (r) { return r.islem_turu === currentFilter; });
    if (filtered.length === 0) {
      listEl.innerHTML = "<p>" + t("noListings") + "</p>";
      return;
    }
    listEl.innerHTML = filtered.map(function (r) {
      var badge = r.islem_turu === "satis" ? t("badgeSatis") : t("badgeAlim");
      return (
        '<div class="category-card">' +
        "<h3>" + escapeHtml(r.baslik) + "</h3>" +
        '<p><strong>' + badge + '</strong>' + (r.durum_bilgisi ? " · " + escapeHtml(r.durum_bilgisi) : "") + "</p>" +
        (r.fiyat ? "<p>" + escapeHtml(r.fiyat) + "</p>" : "") +
        (r.aciklama ? "<p>" + escapeHtml(r.aciklama) + "</p>" : "") +
        '<a class="btn btn-primary" style="width:100%;margin-top:8px" target="_blank" rel="noopener" href="https://wa.me/905550708034?text=' +
        encodeURIComponent("Merhaba, \"" + r.baslik + "\" ilanı/talebi hakkında bilgi almak istiyorum.") +
        '">' + t("waBtn") + "</a>" +
        "</div>"
      );
    }).join("");
  }

  async function loadListings() {
    var { data, error } = await window.gndSupabase
      .from("market_requests")
      .select("*")
      .eq("onay_durumu", "yayinda")
      .order("created_at", { ascending: false });
    if (error) {
      document.getElementById("pazarList").textContent = t("loadError") + error.message;
      return;
    }
    allListings = data || [];
    renderListings();
  }

  document.addEventListener("DOMContentLoaded", async function () {
    document.querySelectorAll('[data-turu]').forEach(function (btn) {
      btn.addEventListener("click", function () { setTuru(btn.dataset.turu); });
    });
    document.querySelectorAll('[data-filter]').forEach(function (btn) {
      btn.addEventListener("click", function () {
        currentFilter = btn.dataset.filter;
        document.querySelectorAll('[data-filter]').forEach(function (b) { b.classList.toggle("active", b === btn); });
        renderListings();
      });
    });

    var langSelect = document.getElementById("lang-select");
    if (langSelect) {
      langSelect.addEventListener("change", function () {
        setTuru(currentTuru);
        renderListings();
      });
    }

    var user = await window.gndAuth.getUser();
    if (user) {
      document.getElementById("pazarForm").style.display = "";
      document.getElementById("pazarLoginPrompt").style.display = "none";
      var meta = user.user_metadata || {};
      if (meta.ad_soyad) document.getElementById("pazarAdSoyad").value = meta.ad_soyad;
      if (meta.telefon) document.getElementById("pazarTelefon").value = meta.telefon;
    } else {
      document.getElementById("pazarForm").style.display = "none";
      document.getElementById("pazarLoginPrompt").style.display = "";
    }

    var form = document.getElementById("pazarForm");
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      var msgEl = document.getElementById("pazarMsg");
      var currentUser = await window.gndAuth.getUser();
      if (!currentUser) {
        msgEl.textContent = getLang() === "tr" ? "Oturumunuz sona ermiş, lütfen tekrar giriş yapın." : "Your session has expired, please log in again.";
        return;
      }
      var payload = {
        user_id: currentUser.id,
        islem_turu: currentTuru,
        ad_soyad: document.getElementById("pazarAdSoyad").value.trim(),
        telefon: document.getElementById("pazarTelefon").value.trim(),
        baslik: document.getElementById("pazarBaslik").value.trim(),
        durum_bilgisi: currentTuru === "satis" ? document.getElementById("pazarDurum").value : null,
        fiyat: document.getElementById("pazarFiyat").value.trim() || null,
        aciklama: document.getElementById("pazarAciklama").value.trim() || null,
      };
      msgEl.textContent = getLang() === "tr" ? "Gönderiliyor..." : "Submitting...";
      var { error } = await window.gndSupabase.from("market_requests").insert(payload);
      if (error) {
        msgEl.textContent = (getLang() === "tr" ? "Bir hata oluştu: " : "An error occurred: ") + error.message;
        return;
      }
      msgEl.textContent = getLang() === "tr"
        ? "Talebiniz alındı. İncelendikten sonra onaylanırsa yayına alınacaktır."
        : "Your request has been received. It will be published once reviewed and approved.";
      if (typeof gtag === "function") {
        gtag("event", "generate_lead", { lead_source: "makine_pazari", page_path: window.location.pathname });
      }
      form.reset();
      setTuru("satis");
    });

    setTuru("satis");
    loadListings();
  });
})();
