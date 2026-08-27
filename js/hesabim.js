(function () {
  "use strict";

  function fmtDate(iso) {
    var d = new Date(iso);
    return d.toLocaleDateString("tr-TR") + " " + d.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" });
  }

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  var KATEGORI_LABEL = { makine: "Makine", atasman: "Ataşman", parca: "Yedek Parça" };
  function badgeFor(status) {
    if (status === "yayinda") return '<span class="admin-badge live">Yayında</span>';
    if (status === "reddedildi") return '<span class="admin-badge rejected">Reddedildi</span>';
    return '<span class="admin-badge pending">İnceleniyor</span>';
  }

  function altKategoriOptions(kategori) {
    if (kategori === "makine" && typeof CATEGORIES !== "undefined") return CATEGORIES;
    if (kategori === "parca" && typeof SPARE_PARTS_CATEGORIES !== "undefined") {
      return SPARE_PARTS_CATEGORIES.filter(function (c) { return c.id !== "attachments"; });
    }
    return [];
  }

  function updateDzAltKategori(kategori, selectedId) {
    var selectEl = document.getElementById("dzAltKategori");
    var wrapEl = document.getElementById("dzAltKategoriWrap");
    var options = altKategoriOptions(kategori);
    if (!options.length) {
      wrapEl.style.display = "none";
      selectEl.innerHTML = "";
      return;
    }
    selectEl.innerHTML = options.map(function (c) {
      return '<option value="' + c.id + '">' + esc(c.name.tr) + "</option>";
    }).join("");
    if (selectedId) selectEl.value = selectedId;
    wrapEl.style.display = "";
  }

  var ilanlarim = [];
  var dzExistingPhotos = [];
  var dzNewFiles = [];
  var currentUser = null;

  function renderIlanlarim() {
    var listEl = document.getElementById("ilanlarimList");
    if (ilanlarim.length === 0) {
      listEl.innerHTML = '<p>Henüz bir ilanınız yok. <a href="pazar.html">İlan ver →</a></p>';
      return;
    }
    listEl.innerHTML = ilanlarim.map(function (r) {
      var typeLabel = r.islem_turu === "satis" ? "Satış" : "Alım Talebi";
      var kategoriLabel = KATEGORI_LABEL[r.kategori] ? " · " + KATEGORI_LABEL[r.kategori] : "";
      var photos = r.foto_urls && r.foto_urls.length ? r.foto_urls : [];
      var photoHtml = photos.length
        ? '<div style="display:flex;gap:6px;flex-wrap:wrap;margin:8px 0">' +
          photos.slice(0, 4).map(function (p) { return '<img src="' + esc(p) + '" style="width:56px;height:56px;object-fit:cover;border-radius:8px">'; }).join("") +
          "</div>"
        : "";
      return (
        '<div class="admin-card">' +
        '<div class="admin-card-top"><strong>' + esc(r.baslik) + "</strong>" + badgeFor(r.onay_durumu) + "</div>" +
        '<div class="admin-row">' + typeLabel + kategoriLabel + (r.durum_bilgisi ? " · " + esc(r.durum_bilgisi) : "") + (r.fiyat ? " · " + esc(r.fiyat) : "") + "</div>" +
        photoHtml +
        '<div class="admin-row" style="color:var(--text-muted,#888)">' + fmtDate(r.created_at) + "</div>" +
        '<div class="admin-actions"><button type="button" class="admin-btn-undo" data-edit-id="' + r.id + '">Düzenle</button></div>' +
        "</div>"
      );
    }).join("");
  }

  async function loadIlanlarim() {
    var { data, error } = await window.gndSupabase
      .from("market_requests")
      .select("*")
      .eq("user_id", currentUser.id)
      .order("created_at", { ascending: false });
    var listEl = document.getElementById("ilanlarimList");
    if (error) {
      listEl.innerHTML = "<p>Yüklenemedi: " + esc(error.message) + "</p>";
      return;
    }
    ilanlarim = data || [];
    renderIlanlarim();
  }

  function setDzTuru(turu) {
    document.getElementById("dzTuru").value = turu;
    document.querySelectorAll("[data-dzturu]").forEach(function (b) { b.classList.toggle("active", b.dataset.dzturu === turu); });
    document.getElementById("dzDurumWrap").style.display = turu === "satis" ? "" : "none";
  }

  function renderDzExistingPhotos() {
    var wrap = document.getElementById("dzFotoMevcut");
    if (dzExistingPhotos.length === 0) {
      wrap.innerHTML = "<p class=\"calc-note\" style=\"margin:0\">Fotoğraf yok.</p>";
      return;
    }
    wrap.innerHTML = dzExistingPhotos.map(function (url, i) {
      return (
        '<div style="position:relative;display:inline-block">' +
        '<img src="' + esc(url) + '" style="width:72px;height:72px;object-fit:cover;border-radius:8px;border:1px solid var(--border)">' +
        '<button type="button" data-remove-photo="' + i + '" style="position:absolute;top:-6px;right:-6px;width:20px;height:20px;border-radius:50%;background:#ef4444;color:#fff;border:none;cursor:pointer;font-size:12px;line-height:1">×</button>' +
        "</div>"
      );
    }).join("");
  }

  function renderDzNewPreview() {
    var wrap = document.getElementById("dzFotoYeniPreview");
    wrap.innerHTML = "";
    dzNewFiles.forEach(function (file) {
      var img = document.createElement("img");
      img.src = URL.createObjectURL(file);
      wrap.appendChild(img);
    });
  }

  function openEditModal(id) {
    var r = ilanlarim.find(function (x) { return String(x.id) === String(id); });
    if (!r) return;
    document.getElementById("dzId").value = r.id;
    setDzTuru(r.islem_turu || "satis");
    document.getElementById("dzBaslik").value = r.baslik || "";
    document.getElementById("dzKategori").value = r.kategori || "makine";
    updateDzAltKategori(r.kategori || "makine", r.alt_kategori || "");
    document.getElementById("dzDurum").value = r.durum_bilgisi || "Sıfır";
    document.getElementById("dzModelYili").value = r.model_yili || "";
    document.getElementById("dzMotorSaati").value = r.motor_saati || "";
    document.getElementById("dzTonaj").value = r.tonaj || "";
    document.getElementById("dzYakit").value = r.yakit_tipi || "";
    document.getElementById("dzFiyat").value = r.fiyat || "";
    document.getElementById("dzAciklama").value = r.aciklama || "";
    dzExistingPhotos = (r.foto_urls || []).slice();
    dzNewFiles = [];
    document.getElementById("dzFotoYeni").value = "";
    document.getElementById("dzMsg").textContent = "";
    renderDzExistingPhotos();
    renderDzNewPreview();
    document.getElementById("ilanDuzenleOverlay").classList.add("is-open");
  }

  function closeEditModal() {
    document.getElementById("ilanDuzenleOverlay").classList.remove("is-open");
  }

  async function uploadNewPhotos() {
    var urls = [];
    for (var i = 0; i < dzNewFiles.length; i++) {
      var file = dzNewFiles[i];
      var ext = (file.name.split(".").pop() || "jpg").toLowerCase().replace(/[^a-z0-9]/g, "") || "jpg";
      var path = currentUser.id + "/" + Date.now() + "-edit-" + i + "." + ext;
      var { error } = await window.gndSupabase.storage.from("market-photos").upload(path, file, { cacheControl: "3600", upsert: false });
      if (error) throw error;
      var { data } = window.gndSupabase.storage.from("market-photos").getPublicUrl(path);
      urls.push(data.publicUrl);
    }
    return urls;
  }

  document.addEventListener("DOMContentLoaded", async function () {
    currentUser = await window.gndAuth.getUser();
    if (!currentUser) {
      window.location.href = "giris.html";
      return;
    }
    var meta = currentUser.user_metadata || {};
    var parts = [meta.ad_soyad, currentUser.email, meta.telefon].filter(Boolean);
    document.getElementById("hesabimEmail").textContent = parts.join(" · ");

    var listEl = document.getElementById("hesabimList");
    var { data, error } = await window.gndSupabase
      .from("website_quote_requests")
      .select("*")
      .order("created_at", { ascending: false });

    if (error) {
      listEl.textContent = "Talepler yüklenemedi: " + error.message;
    } else if (!data || data.length === 0) {
      listEl.innerHTML = '<p>Henüz bir teklif talebin yok. <a href="teklif-al.html">Yeni talep oluştur →</a></p>';
    } else {
      var rows = data.map(function (r) {
        return (
          "<tr>" +
          "<td>" + fmtDate(r.created_at) + "</td>" +
          "<td>" + (r.kategori || "-") + "</td>" +
          "<td>" + (r.adet || 1) + "</td>" +
          "<td>" + (r.notlar || "-") + "</td>" +
          "</tr>"
        );
      }).join("");
      listEl.innerHTML =
        '<table class="compare-table"><thead><tr><th>Tarih</th><th>Makine</th><th>Adet</th><th>Notlar</th></tr></thead><tbody>' +
        rows + "</tbody></table>";
    }

    loadIlanlarim();

    document.querySelectorAll("[data-dzturu]").forEach(function (btn) {
      btn.addEventListener("click", function () { setDzTuru(btn.dataset.dzturu); });
    });

    document.getElementById("dzKategori").addEventListener("change", function () {
      updateDzAltKategori(this.value, "");
    });

    document.getElementById("ilanlarimList").addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-edit-id]");
      if (!btn) return;
      openEditModal(btn.dataset.editId);
    });

    document.getElementById("ilanDuzenleClose").addEventListener("click", closeEditModal);
    document.getElementById("ilanDuzenleOverlay").addEventListener("click", function (e) {
      if (e.target.id === "ilanDuzenleOverlay") closeEditModal();
    });

    document.getElementById("dzFotoMevcut").addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-remove-photo]");
      if (!btn) return;
      dzExistingPhotos.splice(Number(btn.dataset.removePhoto), 1);
      renderDzExistingPhotos();
    });

    document.getElementById("dzFotoYeni").addEventListener("change", function () {
      var files = Array.prototype.slice.call(this.files || []);
      var remaining = 10 - dzExistingPhotos.length;
      var msgEl = document.getElementById("dzMsg");
      if (files.length > remaining) {
        msgEl.textContent = "En fazla " + remaining + " yeni fotoğraf daha ekleyebilirsiniz, fazlası alınmadı.";
        files = files.slice(0, Math.max(0, remaining));
      } else {
        msgEl.textContent = "";
      }
      dzNewFiles = files;
      renderDzNewPreview();
    });

    document.getElementById("ilanDuzenleForm").addEventListener("submit", async function (e) {
      e.preventDefault();
      var msgEl = document.getElementById("dzMsg");
      var submitBtn = this.querySelector('button[type="submit"]');
      submitBtn.disabled = true;

      var newUrls = [];
      if (dzNewFiles.length) {
        msgEl.textContent = "Fotoğraflar yükleniyor...";
        try {
          newUrls = await uploadNewPhotos();
        } catch (err) {
          msgEl.textContent = "Fotoğraf yükleme hatası: " + err.message;
          submitBtn.disabled = false;
          return;
        }
      }

      var finalPhotos = dzExistingPhotos.concat(newUrls);
      var payload = {
        islem_turu: document.getElementById("dzTuru").value,
        kategori: document.getElementById("dzKategori").value,
        alt_kategori: document.getElementById("dzAltKategori").value || null,
        baslik: document.getElementById("dzBaslik").value.trim(),
        durum_bilgisi: document.getElementById("dzTuru").value === "satis" ? document.getElementById("dzDurum").value : null,
        model_yili: document.getElementById("dzModelYili").value.trim() || null,
        motor_saati: document.getElementById("dzMotorSaati").value.trim() || null,
        tonaj: document.getElementById("dzTonaj").value.trim() || null,
        yakit_tipi: document.getElementById("dzYakit").value || null,
        fiyat: document.getElementById("dzFiyat").value.trim() || null,
        aciklama: document.getElementById("dzAciklama").value.trim() || null,
        foto_urls: finalPhotos.length ? finalPhotos : null,
        onay_durumu: "beklemede",
      };

      msgEl.textContent = "Kaydediliyor...";
      var id = document.getElementById("dzId").value;
      var { error } = await window.gndSupabase.from("market_requests").update(payload).eq("id", id);
      if (error && /alt_kategori/i.test(error.message || "")) {
        delete payload.alt_kategori;
        ({ error } = await window.gndSupabase.from("market_requests").update(payload).eq("id", id));
      }
      submitBtn.disabled = false;
      if (error) {
        msgEl.textContent = "Hata: " + error.message;
        return;
      }
      msgEl.textContent = "Kaydedildi, tekrar onaya gönderildi.";
      closeEditModal();
      loadIlanlarim();
    });
  });
})();
