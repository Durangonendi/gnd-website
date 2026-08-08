(function () {
  "use strict";

  var currentTuru = "satis";
  var allListings = [];
  var currentFilter = "all";

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
      baslikLabel.textContent = "Makine / Parça Adı";
      fiyatLabel.textContent = "Fiyat Beklentisi";
    } else {
      durumWrap.style.display = "none";
      baslikLabel.textContent = "Aradığınız Makine / Parça";
      fiyatLabel.textContent = "Bütçeniz";
    }
  }

  function renderListings() {
    var listEl = document.getElementById("pazarList");
    var filtered = currentFilter === "all" ? allListings : allListings.filter(function (r) { return r.islem_turu === currentFilter; });
    if (filtered.length === 0) {
      listEl.innerHTML = "<p>Şu an bu kategoride yayında bir talep yok.</p>";
      return;
    }
    listEl.innerHTML = filtered.map(function (r) {
      var badge = r.islem_turu === "satis" ? "Satış" : "Alım Talebi";
      return (
        '<div class="category-card">' +
        "<h3>" + escapeHtml(r.baslik) + "</h3>" +
        '<p><strong>' + badge + '</strong>' + (r.durum_bilgisi ? " · " + escapeHtml(r.durum_bilgisi) : "") + "</p>" +
        (r.fiyat ? "<p>" + escapeHtml(r.fiyat) + "</p>" : "") +
        (r.aciklama ? "<p>" + escapeHtml(r.aciklama) + "</p>" : "") +
        '<a class="btn btn-primary" style="width:100%;margin-top:8px" target="_blank" rel="noopener" href="https://wa.me/905550708034?text=' +
        encodeURIComponent("Merhaba, \"" + r.baslik + "\" ilanı/talebi hakkında bilgi almak istiyorum.") +
        '">WhatsApp\'tan Sor →</a>' +
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
      document.getElementById("pazarList").textContent = "Talepler yüklenemedi: " + error.message;
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

    var user = await window.gndAuth.getUser();
    if (user) {
      document.getElementById("pazarForm").style.display = "";
      var meta = user.user_metadata || {};
      if (meta.ad_soyad) document.getElementById("pazarAdSoyad").value = meta.ad_soyad;
      if (meta.telefon) document.getElementById("pazarTelefon").value = meta.telefon;
    } else {
      document.getElementById("pazarLoginPrompt").style.display = "";
    }

    var form = document.getElementById("pazarForm");
    form.addEventListener("submit", async function (e) {
      e.preventDefault();
      var msgEl = document.getElementById("pazarMsg");
      var currentUser = await window.gndAuth.getUser();
      if (!currentUser) {
        msgEl.textContent = "Oturumunuz sona ermiş, lütfen tekrar giriş yapın.";
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
      msgEl.textContent = "Gönderiliyor...";
      var { error } = await window.gndSupabase.from("market_requests").insert(payload);
      if (error) {
        msgEl.textContent = "Bir hata oluştu: " + error.message;
        return;
      }
      msgEl.textContent = "Talebiniz alındı. İncelendikten sonra onaylanırsa yayına alınacaktır.";
      form.reset();
      setTuru("satis");
    });

    loadListings();
  });
})();
