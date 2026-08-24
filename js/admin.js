(function () {
  "use strict";

  var ADMIN_EMAILS = ["kuralsz_drn3444@hotmail.com"];

  function esc(s) {
    var d = document.createElement("div");
    d.textContent = s == null ? "" : String(s);
    return d.innerHTML;
  }

  function fmtDate(iso) {
    var d = new Date(iso);
    return d.toLocaleDateString("tr-TR") + " " + d.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" });
  }

  var KATEGORI_LABEL = { makine: "Makine", atasman: "Ataşman", parca: "Yedek Parça" };

  function badgeFor(status) {
    if (status === "yayinda") return '<span class="admin-badge live">Yayında</span>';
    if (status === "reddedildi") return '<span class="admin-badge rejected">Reddedildi</span>';
    return '<span class="admin-badge pending">Bekliyor</span>';
  }

  var pazarData = [];
  var pazarFilter = "bekleyen";

  function renderPazar() {
    var listEl = document.getElementById("pazarList");
    var filtered = pazarData.filter(function (r) {
      if (pazarFilter === "all") return true;
      if (pazarFilter === "yayinda") return r.onay_durumu === "yayinda";
      return r.onay_durumu !== "yayinda" && r.onay_durumu !== "reddedildi";
    });
    if (filtered.length === 0) {
      listEl.innerHTML = "<p>Bu filtrede talep yok.</p>";
      return;
    }
    listEl.innerHTML = filtered.map(function (r) {
      var typeLabel = r.islem_turu === "satis" ? "Satış" : "Alım Talebi";
      var isPending = r.onay_durumu !== "yayinda" && r.onay_durumu !== "reddedildi";
      var actions = "";
      if (isPending) {
        actions =
          '<div class="admin-actions">' +
          '<button class="admin-btn-approve" data-action="approve" data-id="' + r.id + '">Onayla</button>' +
          '<button class="admin-btn-reject" data-action="reject" data-id="' + r.id + '">Reddet</button>' +
          "</div>";
      } else {
        actions =
          '<div class="admin-actions">' +
          '<button class="admin-btn-undo" data-action="pending" data-id="' + r.id + '">Bekleyene Al</button>' +
          "</div>";
      }
      var photos = r.foto_urls && r.foto_urls.length ? r.foto_urls : [];
      var photoHtml = photos.length
        ? '<div style="display:flex;gap:6px;flex-wrap:wrap;margin:8px 0">' +
          photos.map(function (p) { return '<img src="' + esc(p) + '" style="width:64px;height:64px;object-fit:cover;border-radius:8px">'; }).join("") +
          "</div>"
        : "";
      var kategoriLabel = KATEGORI_LABEL[r.kategori] ? " · " + KATEGORI_LABEL[r.kategori] : "";
      return (
        '<div class="admin-card">' +
        '<div class="admin-card-top"><strong>' + esc(r.baslik) + "</strong>" + badgeFor(r.onay_durumu) + "</div>" +
        '<div class="admin-row">' + typeLabel + kategoriLabel + (r.durum_bilgisi ? " · " + esc(r.durum_bilgisi) : "") + (r.fiyat ? " · " + esc(r.fiyat) : "") + "</div>" +
        '<div class="admin-row"><b>Kişi:</b> ' + esc(r.ad_soyad) + " · <b>Tel:</b> " + esc(r.telefon) + "</div>" +
        (r.aciklama ? '<div class="admin-row">' + esc(r.aciklama) + "</div>" : "") +
        photoHtml +
        '<div class="admin-row" style="color:var(--text-muted,#888)">' + fmtDate(r.created_at) + "</div>" +
        actions +
        "</div>"
      );
    }).join("");
  }

  async function loadPazar() {
    var { data, error } = await window.gndSupabase
      .from("market_requests")
      .select("*")
      .order("created_at", { ascending: false });
    var listEl = document.getElementById("pazarList");
    if (error) {
      listEl.innerHTML = "<p>Yüklenemedi: " + esc(error.message) + "</p>";
      return;
    }
    pazarData = data || [];
    renderPazar();
  }

  async function setStatus(id, status) {
    var { error } = await window.gndSupabase.from("market_requests").update({ onay_durumu: status }).eq("id", id);
    if (error) {
      alert("Hata: " + error.message);
      return;
    }
    loadPazar();
  }

  async function loadTeklif() {
    var listEl = document.getElementById("teklifList");
    var { data, error } = await window.gndSupabase
      .from("website_quote_requests")
      .select("*")
      .order("created_at", { ascending: false });
    if (error) {
      listEl.innerHTML = "<p>Yüklenemedi: " + esc(error.message) + "</p>";
      return;
    }
    if (!data || data.length === 0) {
      listEl.innerHTML = "<p>Henüz teklif talebi yok.</p>";
      return;
    }
    listEl.innerHTML = data.map(function (r) {
      return (
        '<div class="admin-card">' +
        '<div class="admin-card-top"><strong>' + esc(r.kategori || "-") + "</strong></div>" +
        '<div class="admin-row"><b>Kişi:</b> ' + esc(r.ad_soyad) + (r.firma ? " (" + esc(r.firma) + ")" : "") + "</div>" +
        '<div class="admin-row"><b>İletişim:</b> ' + esc(r.iletisim) + "</div>" +
        '<div class="admin-row"><b>Adet:</b> ' + esc(r.adet || 1) + "</div>" +
        (r.notlar ? '<div class="admin-row">' + esc(r.notlar) + "</div>" : "") +
        '<div class="admin-row" style="color:var(--text-muted,#888)">' + fmtDate(r.created_at) + "</div>" +
        "</div>"
      );
    }).join("");
  }

  document.addEventListener("DOMContentLoaded", async function () {
    var user = await window.gndAuth.getUser();
    var who = document.getElementById("adminWho");
    var gate = document.getElementById("adminGate");
    var content = document.getElementById("adminContent");

    if (!user || ADMIN_EMAILS.indexOf((user.email || "").toLowerCase()) === -1) {
      who.textContent = user ? "Bu hesabın yönetici yetkisi yok." : "Giriş yapmanız gerekiyor.";
      gate.style.display = "";
      return;
    }

    who.textContent = user.email;
    content.style.display = "";
    loadPazar();
    loadTeklif();

    document.querySelectorAll(".admin-tabs")[0].addEventListener("click", function (e) {
      var btn = e.target.closest(".admin-tab-btn[data-tab]");
      if (!btn) return;
      document.querySelectorAll(".admin-tabs")[0].querySelectorAll(".admin-tab-btn").forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      var tab = btn.dataset.tab;
      document.getElementById("tabPazar").style.display = tab === "pazar" ? "" : "none";
      document.getElementById("tabTeklif").style.display = tab === "teklif" ? "" : "none";
    });

    document.querySelectorAll(".admin-tabs")[1].addEventListener("click", function (e) {
      var btn = e.target.closest(".admin-tab-btn[data-filter]");
      if (!btn) return;
      document.querySelectorAll(".admin-tabs")[1].querySelectorAll(".admin-tab-btn").forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      pazarFilter = btn.dataset.filter;
      renderPazar();
    });

    document.getElementById("pazarList").addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-action]");
      if (!btn) return;
      var id = btn.dataset.id;
      var action = btn.dataset.action;
      if (action === "approve") setStatus(id, "yayinda");
      else if (action === "reject") setStatus(id, "reddedildi");
      else if (action === "pending") setStatus(id, "beklemede");
    });
  });
})();
