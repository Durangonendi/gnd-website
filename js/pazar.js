(function () {
  "use strict";

  var currentTuru = "satis";
  var allListings = [];
  var currentFilter = "all";
  var currentKategori = "all";
  var currentDurum = "all";
  var selectedFiles = [];

  var TXT = {
    baslikSatis: { tr: "Makine / Ataşman / Parça Adı", en: "Machine / Attachment / Part Name" },
    baslikAlim: { tr: "Aradığınız Makine / Ataşman / Parça", en: "Machine / Attachment / Part You're Looking For" },
    fiyatSatis: { tr: "Fiyat Beklentisi", en: "Expected Price" },
    fiyatAlim: { tr: "Bütçeniz", en: "Your Budget" },
    badgeSatis: { tr: "Satış", en: "Sell" },
    badgeAlim: { tr: "Alım Talebi", en: "Buy Request" },
    kategoriMakine: { tr: "Makine", en: "Machine" },
    kategoriAtasman: { tr: "Ataşman", en: "Attachment" },
    kategoriParca: { tr: "Yedek Parça", en: "Spare Part" },
    waBtn: { tr: "WhatsApp'tan Sor →", en: "Ask on WhatsApp →" },
    noListings: { tr: "Şu an bu kategoride yayında bir talep yok.", en: "There are no published requests in this category right now." },
    loadError: { tr: "Talepler yüklenemedi: ", en: "Could not load requests: " },
    maxFotoWarn: { tr: "En fazla 10 fotoğraf seçebilirsiniz, ilk 10 tanesi alındı.", en: "You can select up to 10 photos, only the first 10 were kept." },
    uploading: { tr: "Fotoğraflar yükleniyor...", en: "Uploading photos..." },
    factKod: { tr: "İlan Kodu", en: "Listing Code" },
    factTuru: { tr: "İlan Türü", en: "Listing Type" },
    factDurum: { tr: "Durumu", en: "Condition" },
    factTarih: { tr: "İlan Tarihi", en: "Listed On" },
    factIletisim: { tr: "GND Machinery Üzerinden İletişime Geçin", en: "Contact via GND Machinery" },
  };

  var KATEGORI_LABEL_KEY = { makine: "kategoriMakine", atasman: "kategoriAtasman", parca: "kategoriParca" };

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

  function getListingPhotos(r) {
    if (r.foto_urls && r.foto_urls.length) return r.foto_urls;
    var aciklama = r.aciklama || "";
    var imgMatch = aciklama.match(/^\[img:([^\]]+)\]\s*/);
    if (imgMatch) return [imgMatch[1]];
    return [];
  }

  function getListingDescription(r) {
    var aciklama = r.aciklama || "";
    var imgMatch = aciklama.match(/^\[img:([^\]]+)\]\s*/);
    if (imgMatch) return aciklama.slice(imgMatch[0].length);
    return aciklama;
  }

  function renderListings() {
    var listEl = document.getElementById("pazarList");
    var filtered = allListings.filter(function (r) {
      if (currentFilter !== "all" && r.islem_turu !== currentFilter) return false;
      if (currentKategori !== "all" && r.kategori !== currentKategori) return false;
      if (currentDurum !== "all" && r.durum_bilgisi !== currentDurum) return false;
      return true;
    });
    if (filtered.length === 0) {
      listEl.innerHTML = "<p>" + t("noListings") + "</p>";
      return;
    }
    listEl.innerHTML = filtered.map(function (r) {
      var badge = r.islem_turu === "satis" ? t("badgeSatis") : t("badgeAlim");
      var photos = getListingPhotos(r);
      var aciklama = getListingDescription(r);
      var imgHtml = photos.length
        ? '<div class="category-photo-wrap"><img class="category-photo" src="' + escapeHtml(photos[0]) + '" loading="lazy"></div>'
        : "";
      var kategoriHtml = r.kategori && KATEGORI_LABEL_KEY[r.kategori]
        ? '<span class="pazar-kategori-badge">' + t(KATEGORI_LABEL_KEY[r.kategori]) + "</span>"
        : "";
      return (
        '<div class="category-card pazar-clickable" data-id="' + r.id + '">' +
        imgHtml +
        "<h3>" + escapeHtml(r.baslik) + kategoriHtml + "</h3>" +
        '<p><strong>' + badge + '</strong>' + (r.durum_bilgisi ? " · " + escapeHtml(r.durum_bilgisi) : "") + "</p>" +
        (r.fiyat ? "<p>" + escapeHtml(r.fiyat) + "</p>" : "") +
        (aciklama ? "<p>" + escapeHtml(aciklama.slice(0, 120)) + (aciklama.length > 120 ? "…" : "") + "</p>" : "") +
        '<a class="btn btn-primary" style="width:100%;margin-top:8px" target="_blank" rel="noopener" href="https://wa.me/905550708034?text=' +
        encodeURIComponent("Merhaba, \"" + r.baslik + "\" ilanı/talebi hakkında bilgi almak istiyorum.") +
        '" onclick="event.stopPropagation()">' + t("waBtn") + "</a>" +
        "</div>"
      );
    }).join("");
  }

  function fmtTarih(iso) {
    if (!iso) return "-";
    var d = new Date(iso);
    return d.toLocaleDateString(getLang() === "tr" ? "tr-TR" : "en-GB", { day: "2-digit", month: "short", year: "numeric" });
  }

  function ilanKodu(r) {
    var prefix = r.kategori === "makine" ? "MK" : r.kategori === "atasman" ? "AT" : r.kategori === "parca" ? "YP" : "GN";
    return prefix + "-" + String(r.id).slice(0, 6).toUpperCase();
  }

  function openDetay(id) {
    var r = allListings.find(function (x) { return String(x.id) === String(id); });
    if (!r) return;
    var badge = r.islem_turu === "satis" ? t("badgeSatis") : t("badgeAlim");
    var photos = getListingPhotos(r);
    var aciklama = getListingDescription(r);
    var kategoriHtml = r.kategori && KATEGORI_LABEL_KEY[r.kategori]
      ? '<span class="pazar-kategori-badge">' + t(KATEGORI_LABEL_KEY[r.kategori]) + "</span>"
      : "";
    var waHref = "https://wa.me/905550708034?text=" +
      encodeURIComponent("Merhaba, \"" + r.baslik + "\" ilanı/talebi hakkında bilgi almak istiyorum.");

    var mainImg = photos.length
      ? '<img class="pazar-detay-gallery-main" id="pazarDetayMain" src="' + escapeHtml(photos[0]) + '">'
      : '<div class="pazar-detay-gallery-main pazar-detay-noimg"><span>' + escapeHtml(r.baslik) + "</span></div>";
    var thumbs = photos.length > 1
      ? '<div class="pazar-detay-gallery">' + photos.map(function (p) {
          return '<img src="' + escapeHtml(p) + '" data-full="' + escapeHtml(p) + '">';
        }).join("") + "</div>"
      : "";

    var facts = [
      [t("factKod"), ilanKodu(r)],
      [t("factTuru"), badge],
    ];
    if (r.durum_bilgisi) facts.push([t("factDurum"), escapeHtml(r.durum_bilgisi)]);
    facts.push([t("factTarih"), fmtTarih(r.created_at)]);

    var factRows = facts.map(function (f) {
      return '<div class="pazar-fact-row"><span class="pazar-fact-label">' + f[0] + "</span><span class=\"pazar-fact-value\">" + f[1] + "</span></div>";
    }).join("");

    var infoPanel =
      "<h2 style=\"margin:0 0 4px\">" + escapeHtml(r.baslik) + kategoriHtml + "</h2>" +
      (r.fiyat ? '<div class="pazar-detay-fiyat">' + escapeHtml(r.fiyat) + "</div>" : "") +
      '<div class="pazar-fact-table">' + factRows + "</div>" +
      (aciklama ? '<p class="pazar-detay-aciklama">' + escapeHtml(aciklama) + "</p>" : "") +
      '<div class="pazar-detay-contact-box">' +
      '<div class="pazar-detay-contact-title">' + t("factIletisim") + "</div>" +
      '<a class="btn btn-primary pazar-detay-wa-btn" target="_blank" rel="noopener" href="' + waHref + '">' + t("waBtn") + "</a>" +
      "</div>";

    var body =
      '<div class="pazar-detay-grid">' +
      '<div class="pazar-detay-media">' + mainImg + thumbs + "</div>" +
      '<div class="pazar-detay-info">' + infoPanel + "</div>" +
      "</div>";

    document.getElementById("pazarDetayBody").innerHTML = body;
    document.getElementById("pazarDetayOverlay").classList.add("is-open");

    var gallery = document.querySelector(".pazar-detay-gallery");
    if (gallery) {
      gallery.addEventListener("click", function (e) {
        var img = e.target.closest("img[data-full]");
        if (!img) return;
        var mainEl = document.getElementById("pazarDetayMain");
        if (mainEl) mainEl.src = img.dataset.full;
      });
    }
  }

  function closeDetay() {
    document.getElementById("pazarDetayOverlay").classList.remove("is-open");
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

  function renderFotoPreview() {
    var wrap = document.getElementById("pazarFotoPreview");
    wrap.innerHTML = "";
    selectedFiles.forEach(function (file) {
      var img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      wrap.appendChild(img);
    });
  }

  async function uploadPhotos(userId) {
    var urls = [];
    for (var i = 0; i < selectedFiles.length; i++) {
      var file = selectedFiles[i];
      var ext = (file.name.split(".").pop() || "jpg").toLowerCase().replace(/[^a-z0-9]/g, "") || "jpg";
      var path = userId + "/" + Date.now() + "-" + i + "." + ext;
      var { error } = await window.gndSupabase.storage.from("market-photos").upload(path, file, {
        cacheControl: "3600",
        upsert: false,
      });
      if (error) throw error;
      var { data } = window.gndSupabase.storage.from("market-photos").getPublicUrl(path);
      urls.push(data.publicUrl);
    }
    return urls;
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
    document.querySelectorAll('[data-kategori]').forEach(function (btn) {
      btn.addEventListener("click", function () {
        currentKategori = btn.dataset.kategori;
        document.querySelectorAll('[data-kategori]').forEach(function (b) { b.classList.toggle("active", b === btn); });
        renderListings();
      });
    });
    document.querySelectorAll('[data-durum]').forEach(function (btn) {
      btn.addEventListener("click", function () {
        currentDurum = btn.dataset.durum;
        document.querySelectorAll('[data-durum]').forEach(function (b) { b.classList.toggle("active", b === btn); });
        renderListings();
      });
    });

    document.getElementById("pazarList").addEventListener("click", function (e) {
      var card = e.target.closest(".pazar-clickable");
      if (!card) return;
      openDetay(card.dataset.id);
    });
    document.getElementById("pazarDetayClose").addEventListener("click", closeDetay);
    document.getElementById("pazarDetayOverlay").addEventListener("click", function (e) {
      if (e.target.id === "pazarDetayOverlay") closeDetay();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeDetay();
    });

    var fotoInput = document.getElementById("pazarFoto");
    fotoInput.addEventListener("change", function () {
      var files = Array.prototype.slice.call(fotoInput.files || []);
      var msgEl = document.getElementById("pazarMsg");
      if (files.length > 10) {
        msgEl.textContent = t("maxFotoWarn");
        files = files.slice(0, 10);
      } else {
        msgEl.textContent = "";
      }
      selectedFiles = files;
      renderFotoPreview();
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

      var submitBtn = form.querySelector('button[type="submit"]');
      submitBtn.disabled = true;

      var fotoUrls = [];
      if (selectedFiles.length) {
        msgEl.textContent = t("uploading");
        try {
          fotoUrls = await uploadPhotos(currentUser.id);
        } catch (err) {
          msgEl.textContent = (getLang() === "tr" ? "Fotoğraf yükleme hatası: " : "Photo upload error: ") + err.message;
          submitBtn.disabled = false;
          return;
        }
      }

      var payload = {
        user_id: currentUser.id,
        islem_turu: currentTuru,
        kategori: document.getElementById("pazarKategori").value,
        ad_soyad: document.getElementById("pazarAdSoyad").value.trim(),
        telefon: document.getElementById("pazarTelefon").value.trim(),
        baslik: document.getElementById("pazarBaslik").value.trim(),
        durum_bilgisi: currentTuru === "satis" ? document.getElementById("pazarDurum").value : null,
        fiyat: document.getElementById("pazarFiyat").value.trim() || null,
        aciklama: document.getElementById("pazarAciklama").value.trim() || null,
        foto_urls: fotoUrls.length ? fotoUrls : null,
      };
      msgEl.textContent = getLang() === "tr" ? "Gönderiliyor..." : "Submitting...";
      var { error } = await window.gndSupabase.from("market_requests").insert(payload);
      submitBtn.disabled = false;
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
      selectedFiles = [];
      document.getElementById("pazarFotoPreview").innerHTML = "";
      setTuru("satis");
    });

    setTuru("satis");
    loadListings();
  });
})();
