(function () {
  "use strict";

  var mode = "login"; // or "signup"

  function showMessage(text, isError) {
    var el = document.getElementById("authMessage");
    el.textContent = text;
    el.style.display = "block";
    el.style.color = isError ? "#c0392b" : "inherit";
  }

  function applyMode() {
    var title = document.getElementById("authPageTitle");
    var submitBtn = document.getElementById("authSubmitBtn");
    var toggle = document.getElementById("authToggleMode");
    var adSoyadField = document.getElementById("authAdSoyadField");
    var telefonField = document.getElementById("authTelefonField");
    var adSoyadInput = document.getElementById("authAdSoyad");
    var telefonInput = document.getElementById("authTelefon");
    if (mode === "login") {
      title.textContent = "Giriş Yap";
      submitBtn.textContent = "Giriş Yap";
      toggle.textContent = "Hesabın yok mu? Kayıt ol";
      adSoyadField.style.display = "none";
      telefonField.style.display = "none";
      adSoyadInput.required = false;
      telefonInput.required = false;
    } else {
      title.textContent = "Kayıt Ol";
      submitBtn.textContent = "Kayıt Ol";
      toggle.textContent = "Zaten hesabın var mı? Giriş yap";
      adSoyadField.style.display = "";
      telefonField.style.display = "";
      adSoyadInput.required = true;
      telefonInput.required = true;
    }
  }

  document.addEventListener("DOMContentLoaded", async function () {
    var existing = await window.gndAuth.getUser();
    if (existing) {
      window.location.href = "hesabim.html";
      return;
    }

    applyMode();
    document.getElementById("authToggleMode").addEventListener("click", function (e) {
      e.preventDefault();
      mode = mode === "login" ? "signup" : "login";
      applyMode();
    });

    document.getElementById("authForm").addEventListener("submit", async function (e) {
      e.preventDefault();
      var email = document.getElementById("authEmail").value.trim();
      var password = document.getElementById("authPassword").value;
      var submitBtn = document.getElementById("authSubmitBtn");
      submitBtn.disabled = true;

      try {
        if (mode === "login") {
          var res = await window.gndAuth.signIn(email, password);
          if (res.error) throw res.error;
          window.location.href = "hesabim.html";
        } else {
          var adSoyad = document.getElementById("authAdSoyad").value.trim();
          var telefon = document.getElementById("authTelefon").value.trim();
          if (!adSoyad || !telefon) {
            showMessage("Lütfen ad soyad ve telefon numaranı da girin.", true);
            submitBtn.disabled = false;
            return;
          }
          var res2 = await window.gndAuth.signUp(email, password, { ad_soyad: adSoyad, telefon: telefon });
          if (res2.error) throw res2.error;
          if (res2.data && res2.data.session) {
            window.location.href = "hesabim.html";
          } else {
            showMessage("Kayıt oluşturuldu. E-postana gelen onay linkine tıkladıktan sonra giriş yapabilirsin.", false);
          }
        }
      } catch (err) {
        showMessage(err.message || "Bir hata oluştu, tekrar deneyin.", true);
      } finally {
        submitBtn.disabled = false;
      }
    });
  });
})();
