(function () {
  "use strict";

  function buildWhatsAppText(data) {
    var lines = [
      "Merhaba, bir teklif talebim var:",
      "Ad Soyad: " + data.adSoyad,
      data.firma ? "Firma: " + data.firma : null,
      "İletişim: " + data.iletisim,
      "Makine Kategorisi: " + data.kategori,
      "Adet: " + data.adet,
      data.notlar ? "Notlar: " + data.notlar : null,
    ].filter(Boolean);
    return lines.join("\n");
  }

  function generatePdf(data, logoDataUrl) {
    var jsPDF = window.jspdf.jsPDF;
    var doc = new jsPDF({ unit: "mm", format: "a4" });

    if (window.GND_ROBOTO_REGULAR && window.GND_ROBOTO_BOLD) {
      doc.addFileToVFS("Roboto-Regular.ttf", window.GND_ROBOTO_REGULAR);
      doc.addFont("Roboto-Regular.ttf", "Roboto", "normal");
      doc.addFileToVFS("Roboto-Bold.ttf", window.GND_ROBOTO_BOLD);
      doc.addFont("Roboto-Bold.ttf", "Roboto", "bold");
      doc.setFont("Roboto", "normal");
    }

    var pageW = doc.internal.pageSize.getWidth();
    var y = 20;

    if (logoDataUrl) {
      doc.addImage(logoDataUrl, "PNG", 15, y, 28, 28);
    }
    doc.setFont("Roboto", "bold");
    doc.setFontSize(18);
    doc.setTextColor(20, 20, 20);
    doc.text("GND İş Makineleri", 50, y + 10);
    doc.setFont("Roboto", "normal");
    doc.setFontSize(11);
    doc.setTextColor(120, 120, 120);
    doc.text("Teklif Talebi", 50, y + 18);
    y += 40;

    doc.setDrawColor(200, 170, 100);
    doc.setLineWidth(0.5);
    doc.line(15, y, pageW - 15, y);
    y += 10;

    doc.setFontSize(10);
    doc.setTextColor(90, 90, 90);
    doc.text("Tarih: " + new Date().toLocaleDateString("tr-TR"), 15, y);
    y += 12;

    var rows = [
      ["Ad Soyad", data.adSoyad],
      ["Firma", data.firma || "-"],
      ["İletişim", data.iletisim],
      ["Makine Kategorisi", data.kategori],
      ["Adet", String(data.adet)],
    ];
    doc.setFontSize(12);
    rows.forEach(function (r) {
      doc.setTextColor(150, 120, 40);
      doc.text(r[0] + ":", 15, y);
      doc.setTextColor(20, 20, 20);
      doc.text(String(r[1]), 70, y);
      y += 9;
    });

    if (data.notlar) {
      y += 3;
      doc.setTextColor(150, 120, 40);
      doc.text("Notlar:", 15, y);
      y += 7;
      doc.setTextColor(20, 20, 20);
      var split = doc.splitTextToSize(data.notlar, pageW - 30);
      doc.text(split, 15, y);
      y += split.length * 6;
    }

    y += 10;
    doc.setDrawColor(220, 220, 220);
    doc.line(15, y, pageW - 15, y);
    y += 8;
    doc.setFontSize(9);
    doc.setTextColor(130, 130, 130);
    doc.text(
      "Bu belge otomatik olarak oluşturulmuş bir talep özetidir, kesin fiyat teklifi değildir.",
      15, y
    );
    y += 5;
    doc.text("Kesin fiyat ve stok bilgisi için ekibimiz sizinle iletişime geçecektir.", 15, y);
    y += 8;
    doc.text("WhatsApp: +90 555 070 80 34   ·   gnd-website-five.vercel.app", 15, y);

    doc.save("GND_Teklif_Talebi_" + data.adSoyad.replace(/\s+/g, "_") + ".pdf");
  }

  function onSubmit(e) {
    e.preventDefault();
    var data = {
      adSoyad: document.getElementById("adSoyad").value.trim(),
      firma: document.getElementById("firma").value.trim(),
      iletisim: document.getElementById("iletisim").value.trim(),
      kategori: document.getElementById("kategori").selectedOptions[0].text,
      adet: document.getElementById("adet").value || 1,
      notlar: document.getElementById("notlar").value.trim(),
    };
    if (!data.adSoyad || !data.iletisim) {
      alert("Lütfen ad soyad ve iletişim bilgisi girin.");
      return;
    }

    generatePdf(data, window.GND_LOGO_DATAURL || null);

    var waText = encodeURIComponent(buildWhatsAppText(data));
    var waLink = document.getElementById("waSendLink");
    waLink.href = "https://wa.me/905550708034?text=" + waText;
    document.getElementById("waSendBox").style.display = "block";
  }

  var form = document.getElementById("teklifForm");
  if (form) form.addEventListener("submit", onSubmit);
})();
