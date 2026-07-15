// Hesaplama araçları — ortak hesaplama mantığı, tüm hesaplayıcı sayfalarında kullanılır.
// Her sayfa <body data-calc="..."> ile hangi hesaplamayı çalıştıracağını belirtir.
(function () {
  "use strict";

  function num(id) {
    return Number(document.getElementById(id).value) || 0;
  }

  function fmt(n) {
    return n.toLocaleString("tr-TR", { maximumFractionDigits: 2 });
  }

  function showResult(html) {
    var box = document.getElementById("calcResult");
    box.innerHTML = html;
    box.classList.add("show");
  }

  var CALCS = {
    hafriyat: function () {
      var L = num("uzunluk"), W = num("genislik"), D = num("derinlik"), swell = num("sisme");
      var bank = L * W * D;
      var loose = bank * (1 + swell / 100);
      showResult(
        '<div class="calc-result-value">' + fmt(bank) + " m³</div>" +
        "<div>Yerinde (bank) hacim. Kazıldıktan sonra gevşeme payıyla taşınacak hacim: <strong>" + fmt(loose) + " m³</strong></div>"
      );
    },
    beton: function () {
      var L = num("uzunluk"), W = num("genislik"), T = num("kalinlik");
      var vol = L * W * (T / 100);
      var withWaste = vol * 1.08;
      showResult(
        '<div class="calc-result-value">' + fmt(vol) + " m³</div>" +
        "<div>Gerekli beton hacmi. %8 fire payıyla sipariş önerisi: <strong>" + fmt(withWaste) + " m³</strong></div>"
      );
    },
    tasima: function () {
      var total = num("toplamHacim"), cap = num("kapasite");
      if (cap <= 0) {
        showResult('<div class="calc-result-value">—</div><div>Araç kapasitesini girin.</div>');
        return;
      }
      var trips = Math.ceil(total / cap);
      showResult(
        '<div class="calc-result-value">' + trips + " sefer</div>" +
        "<div>" + fmt(total) + " m³ malzeme, " + fmt(cap) + " m³ kapasiteli araçla taşınırsa.</div>"
      );
    },
    ekipman: function () {
      var tip = document.getElementById("isTuru").value;
      var map = {
        dar: { name: "Mini Ekskavatör", range: "0,8–6 ton", href: "../makineler/mini-excavator.html" },
        genel: { name: "Ekskavatör", range: "13–25 ton", href: "../makineler/excavator.html" },
        buyuk: { name: "Madencilik / Ağır Tonaj Ekskavatör", range: "30–120+ ton", href: "../makineler/mining-excavator.html" },
      };
      var r = map[tip];
      showResult(
        '<div class="calc-result-value">' + r.name + "</div>" +
        "<div>Tipik çalışma ağırlığı: " + r.range + ". <a href=\"" + r.href + "\">Bu kategoriye göz atın →</a></div>"
      );
    },
    yakit: function () {
      var tip = document.getElementById("makineTipi").value;
      var saat = num("calismaSaati"), gun = num("gunSayisi"), fiyat = num("yakitFiyati");
      var rates = { mini: 8, orta: 15, agir: 25 };
      var rate = rates[tip];
      var totalL = rate * saat * gun;
      var totalCost = totalL * fiyat;
      showResult(
        '<div class="calc-result-value">' + fmt(totalL) + " litre</div>" +
        "<div>Tahmini toplam yakıt maliyeti: <strong>" + fmt(totalCost) + " TL</strong></div>"
      );
    },
    sure: function () {
      var vol = num("toplamHacim2");
      var tip = document.getElementById("makineTipi2").value;
      var rates = { mini: 8, orta: 20, agir: 40 };
      var rate = rates[tip];
      var hours = vol / rate;
      var days = hours / 8;
      showResult(
        '<div class="calc-result-value">' + fmt(hours) + " saat</div>" +
        "<div>Yaklaşık <strong>" + fmt(days) + " iş günü</strong> (günde 8 saat çalışmayla).</div>"
      );
    },
  };

  var type = document.body.getAttribute("data-calc");
  var btn = document.getElementById("calcBtn");
  if (btn && CALCS[type]) {
    btn.addEventListener("click", CALCS[type]);
  }
})();
