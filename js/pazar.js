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
    factAltKategori: { tr: "Alt Kategori", en: "Subcategory" },
    factTarih: { tr: "İlan Tarihi", en: "Listed On" },
    factIletisim: { tr: "GND Machinery Üzerinden İletişime Geçin", en: "Contact via GND Machinery" },
    shareBtn: { tr: "Bağlantıyı Kopyala", en: "Copy Link" },
    shareCopied: { tr: "Bağlantı kopyalandı!", en: "Link copied!" },
    shareLabel: { tr: "İlanı Paylaş", en: "Share This Listing" },
    factModelYili: { tr: "Model Yılı", en: "Model Year" },
    factMotorSaati: { tr: "Motor Saati", en: "Working Hours" },
    factTonaj: { tr: "Tonaj", en: "Tonnage" },
    factYakit: { tr: "Yakıt Tipi", en: "Fuel Type" },
    aciklamaGoster: { tr: "Açıklamayı Göster", en: "Show Description" },
  };

  var KATEGORI_LABEL_KEY = { makine: "kategoriMakine", atasman: "kategoriAtasman", parca: "kategoriParca" };

  var ICON_WHATSAPP = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M17.5 14.4c-.3-.1-1.6-.8-1.9-.9-.2-.1-.4-.1-.6.1-.2.3-.7.9-.8 1-.2.2-.3.2-.5.1-.3-.1-1.2-.4-2.2-1.3-.8-.7-1.4-1.6-1.5-1.9-.2-.3 0-.4.1-.6.1-.1.3-.3.4-.5.1-.1.2-.3.3-.4.1-.2 0-.4 0-.5C11.5 9.4 11 8.2 10.8 7.7c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s1 2.5 1.1 2.7c.1.2 1.9 3 4.7 4.1.7.3 1.2.4 1.6.6.7.2 1.3.2 1.8.1.5-.1 1.6-.7 1.9-1.3.2-.6.2-1.2.2-1.3-.1-.2-.3-.2-.5-.3z"/><path d="M12 2C6.5 2 2 6.5 2 12c0 1.9.5 3.6 1.5 5.2L2 22l4.9-1.3C8.4 21.5 10.1 22 12 22c5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.7 0-3.3-.5-4.7-1.3l-.3-.2-3.5.9.9-3.4-.2-.3C3.4 14.5 3 13.3 3 12c0-4.9 4.1-9 9-9s9 4.1 9 9-4.1 9-9 9z"/></svg>';
  var ICON_FACEBOOK = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><path d="M13.5 21v-8h2.7l.4-3.1h-3.1V8c0-.9.2-1.5 1.5-1.5h1.6V3.7C15.9 3.5 15 3.5 13.9 3.5c-2.4 0-4 1.5-4 4.1v2.3H7.2V13h2.7v8h3.6z"/></svg>';
  var ICON_LINK = '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2"><path d="M10 13a5 5 0 007.1 0l2-2a5 5 0 00-7-7l-1.2 1.1"/><path d="M14 11a5 5 0 00-7.1 0l-2 2a5 5 0 007 7l1.1-1.1"/></svg>';
  var ICON_MORE = '<svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor"><circle cx="6" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="18" cy="12" r="2"/></svg>';

  function altKategoriOptions(kategori) {
    if (kategori === "makine" && typeof CATEGORIES !== "undefined") return CATEGORIES;
    if (kategori === "parca" && typeof SPARE_PARTS_CATEGORIES !== "undefined") {
      return SPARE_PARTS_CATEGORIES.filter(function (c) { return c.id !== "attachments"; });
    }
    return [];
  }

  function altKategoriLabel(kategori, altId) {
    var list = altKategoriOptions(kategori);
    var found = list.find(function (c) { return c.id === altId; });
    return found ? found.name[getLang()] : "";
  }

  function updateAltKategoriSelect(selectEl, wrapEl, kategori, selectedId) {
    var options = altKategoriOptions(kategori);
    if (!options.length) {
      wrapEl.style.display = "none";
      selectEl.innerHTML = "";
      return;
    }
    var lang = getLang();
    selectEl.innerHTML = options.map(function (c) {
      return '<option value="' + c.id + '">' + escapeHtml(c.name[lang]) + "</option>";
    }).join("");
    if (selectedId) selectEl.value = selectedId;
    wrapEl.style.display = "";
  }

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
    if (imgMatch) aciklama = aciklama.slice(imgMatch[0].length);
    var langMatch = aciklama.match(/^\[TR\]([\s\S]*?)\[EN\]([\s\S]*)$/);
    if (langMatch) return (getLang() === "tr" ? langMatch[1] : langMatch[2]).trim();
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
      var specBits = [r.model_yili, r.motor_saati, r.tonaj, r.yakit_tipi].filter(Boolean).map(escapeHtml);
      var specLine = specBits.length ? "<p>" + specBits.join(" · ") + "</p>" : "";
      return (
        '<div class="category-card pazar-clickable" data-id="' + r.id + '">' +
        imgHtml +
        "<h3>" + escapeHtml(r.baslik) + kategoriHtml + "</h3>" +
        '<p><strong>' + badge + '</strong>' + (r.durum_bilgisi ? " · " + escapeHtml(r.durum_bilgisi) : "") + "</p>" +
        specLine +
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

  function splitAciklamaFacts(aciklama) {
    var lines = (aciklama || "").split(/\r?\n/);
    var pairs = [];
    var freeLines = [];
    var lineRe = /^\s*([\wÇĞİÖŞÜçğıöşü][\wÇĞİÖŞÜçğıöşü .()/-]{1,28}?)\s*[:：]\s*(.+?)\s*$/;
    lines.forEach(function (line) {
      var m = line.match(lineRe);
      if (m && m[2]) {
        pairs.push([m[1], m[2]]);
      } else if (line.trim()) {
        freeLines.push(line);
      }
    });
    return { pairs: pairs, freeText: freeLines.join("\n") };
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
    if (r.alt_kategori) {
      var altLabel = altKategoriLabel(r.kategori, r.alt_kategori);
      if (altLabel) facts.push([t("factAltKategori"), escapeHtml(altLabel)]);
    }
    if (r.model_yili) facts.push([t("factModelYili"), escapeHtml(r.model_yili)]);
    if (r.motor_saati) facts.push([t("factMotorSaati"), escapeHtml(r.motor_saati)]);
    if (r.tonaj) facts.push([t("factTonaj"), escapeHtml(r.tonaj)]);
    if (r.yakit_tipi) facts.push([t("factYakit"), escapeHtml(r.yakit_tipi)]);
    facts.push([t("factTarih"), fmtTarih(r.created_at)]);

    var split = splitAciklamaFacts(aciklama);
    split.pairs.forEach(function (p) {
      facts.push([escapeHtml(p[0]), escapeHtml(p[1])]);
    });
    aciklama = split.freeText;

    var factRows = facts.map(function (f) {
      return '<div class="pazar-fact-row"><span class="pazar-fact-label">' + f[0] + "</span><span class=\"pazar-fact-value\">" + f[1] + "</span></div>";
    }).join("");

    var infoPanel =
      "<h2 style=\"margin:0 0 4px\">" + escapeHtml(r.baslik) + kategoriHtml + "</h2>" +
      (r.fiyat ? '<div class="pazar-detay-fiyat">' + escapeHtml(r.fiyat) + "</div>" : "") +
      '<div class="pazar-fact-table">' + factRows + "</div>" +
      (aciklama
        ? '<details class="pazar-detay-aciklama-details"><summary>' + t("aciklamaGoster") + '</summary><p class="pazar-detay-aciklama">' + escapeHtml(aciklama) + "</p></details>"
        : "") +
      '<div class="pazar-detay-contact-box">' +
      '<div class="pazar-detay-contact-title">' + t("factIletisim") + "</div>" +
      '<a class="btn btn-primary pazar-detay-wa-btn" target="_blank" rel="noopener" href="' + waHref + '">' + t("waBtn") + "</a>" +
      '<div class="pazar-share-label">' + t("shareLabel") + "</div>" +
      '<div class="pazar-share-row">' +
      '<a class="pazar-share-icon" id="pazarShareWa" target="_blank" rel="noopener" aria-label="WhatsApp" title="WhatsApp">' + ICON_WHATSAPP + "</a>" +
      '<a class="pazar-share-icon" id="pazarShareFb" target="_blank" rel="noopener" aria-label="Facebook" title="Facebook">' + ICON_FACEBOOK + "</a>" +
      '<button type="button" class="pazar-share-icon" id="pazarDetayShareBtn" aria-label="' + t("shareBtn") + '" title="' + t("shareBtn") + '">' + ICON_LINK + "</button>" +
      '<button type="button" class="pazar-share-icon" id="pazarNativeShareBtn" style="display:none" aria-label="' + t("shareBtn") + '" title="' + t("shareBtn") + '">' + ICON_MORE + "</button>" +
      "</div>" +
      '<span class="pazar-detay-share-msg" id="pazarDetayShareMsg"></span>' +
      "</div>";

    var body =
      '<div class="pazar-detay-grid">' +
      '<div class="pazar-detay-media">' + mainImg + thumbs + "</div>" +
      '<div class="pazar-detay-info">' + infoPanel + "</div>" +
      "</div>";

    document.getElementById("pazarDetayBody").innerHTML = body;
    document.getElementById("pazarDetayOverlay").classList.add("is-open");

    var shareUrl = location.origin + location.pathname + "?id=" + encodeURIComponent(r.id);
    history.replaceState(null, "", shareUrl);
    var shareBtn = document.getElementById("pazarDetayShareBtn");
    if (shareBtn) {
      shareBtn.addEventListener("click", function () {
        var msgEl = document.getElementById("pazarDetayShareMsg");
        var done = function () { if (msgEl) msgEl.textContent = t("shareCopied"); };
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(shareUrl).then(done).catch(function () { window.prompt(t("shareBtn"), shareUrl); });
        } else {
          window.prompt(t("shareBtn"), shareUrl);
        }
      });
    }

    var shareText = getLang() === "tr" ? "\"" + r.baslik + "\" ilanına göz atın:" : "Check out this listing: \"" + r.baslik + "\"";
    var waShare = document.getElementById("pazarShareWa");
    if (waShare) waShare.href = "https://api.whatsapp.com/send?text=" + encodeURIComponent(shareText + " " + shareUrl);
    var fbShare = document.getElementById("pazarShareFb");
    if (fbShare) fbShare.href = "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(shareUrl);
    var nativeShareBtn = document.getElementById("pazarNativeShareBtn");
    if (nativeShareBtn && navigator.share) {
      nativeShareBtn.style.display = "";
      nativeShareBtn.addEventListener("click", function () {
        navigator.share({ title: r.baslik, text: shareText, url: shareUrl }).catch(function () {});
      });
    }

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
    if (new URLSearchParams(location.search).get("id")) {
      history.replaceState(null, "", location.pathname);
    }
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
    var sharedId = new URLSearchParams(location.search).get("id");
    if (sharedId) openDetay(sharedId);
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

    var pazarKategoriSelect = document.getElementById("pazarKategori");
    var pazarAltKategoriSelect = document.getElementById("pazarAltKategori");
    var pazarAltKategoriWrap = document.getElementById("pazarAltKategoriWrap");
    pazarKategoriSelect.addEventListener("change", function () {
      updateAltKategoriSelect(pazarAltKategoriSelect, pazarAltKategoriWrap, pazarKategoriSelect.value);
    });
    updateAltKategoriSelect(pazarAltKategoriSelect, pazarAltKategoriWrap, pazarKategoriSelect.value);
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
        alt_kategori: document.getElementById("pazarAltKategori").value || null,
        ad_soyad: document.getElementById("pazarAdSoyad").value.trim(),
        telefon: document.getElementById("pazarTelefon").value.trim(),
        baslik: document.getElementById("pazarBaslik").value.trim(),
        durum_bilgisi: currentTuru === "satis" ? document.getElementById("pazarDurum").value : null,
        model_yili: document.getElementById("pazarModelYili").value.trim() || null,
        motor_saati: document.getElementById("pazarMotorSaati").value.trim() || null,
        tonaj: document.getElementById("pazarTonaj").value.trim() || null,
        yakit_tipi: document.getElementById("pazarYakit").value || null,
        fiyat: document.getElementById("pazarFiyat").value.trim() || null,
        aciklama: document.getElementById("pazarAciklama").value.trim() || null,
        foto_urls: fotoUrls.length ? fotoUrls : null,
      };
      msgEl.textContent = getLang() === "tr" ? "Gönderiliyor..." : "Submitting...";
      var { error } = await window.gndSupabase.from("market_requests").insert(payload);
      if (error && /alt_kategori/i.test(error.message || "")) {
        delete payload.alt_kategori;
        ({ error } = await window.gndSupabase.from("market_requests").insert(payload));
      }
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
      if (typeof window.gndTrack === "function") {
        window.gndTrack(currentTuru === "satis" ? "listing_created" : "request_created", { kategori: payload.kategori });
      }
      form.reset();
      selectedFiles = [];
      document.getElementById("pazarFotoPreview").innerHTML = "";
      setTuru("satis");
      updateAltKategoriSelect(pazarAltKategoriSelect, pazarAltKategoriWrap, pazarKategoriSelect.value);
    });

    var VIDEO_TAB_IDS = { satis: "Zbkf3q_7Vp0", alim: "nRf3YRmgQT4", foto: "g2JkOwoNPsw" };
    document.querySelectorAll('[data-video-tab]').forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll('[data-video-tab]').forEach(function (b) { b.classList.toggle("active", b === btn); });
        var frame = document.getElementById("pazarHelpVideo");
        if (frame) frame.src = "https://www.youtube-nocookie.com/embed/" + VIDEO_TAB_IDS[btn.dataset.videoTab];
      });
    });

    setTuru("satis");
    loadListings();
  });
})();
