(function () {
  "use strict";

  function fmtDate(iso) {
    var d = new Date(iso);
    return d.toLocaleDateString("tr-TR") + " " + d.toLocaleTimeString("tr-TR", { hour: "2-digit", minute: "2-digit" });
  }

  document.addEventListener("DOMContentLoaded", async function () {
    var user = await window.gndAuth.getUser();
    if (!user) {
      window.location.href = "giris.html";
      return;
    }
    var meta = user.user_metadata || {};
    var parts = [meta.ad_soyad, user.email, meta.telefon].filter(Boolean);
    document.getElementById("hesabimEmail").textContent = parts.join(" · ");

    var listEl = document.getElementById("hesabimList");
    var { data, error } = await window.gndSupabase
      .from("website_quote_requests")
      .select("*")
      .order("created_at", { ascending: false });

    if (error) {
      listEl.textContent = "Talepler yüklenemedi: " + error.message;
      return;
    }
    if (!data || data.length === 0) {
      listEl.innerHTML = '<p>Henüz bir teklif talebin yok. <a href="teklif-al.html">Yeni talep oluştur →</a></p>';
      return;
    }

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
      rows +
      "</tbody></table>";
  });
})();
