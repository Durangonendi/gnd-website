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
    if (mode === "login") {
      title.textContent = "Giriş Yap";
      submitBtn.textContent = "Giriş Yap";
      toggle.textContent = "Hesabın yok mu? Kayıt ol";
    } else {
      title.textContent = "Kayıt Ol";
      submitBtn.textContent = "Kayıt Ol";
      toggle.textContent = "Zaten hesabın var mı? Giriş yap";
    }
  }

  document.addEventListener("DOMContentLoaded", async function () {
    var existing = await window.gndAuth.getUser();
    if (existing) {
      window.location.href = "hesabim.html";
      return;
    }

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
          var res2 = await window.gndAuth.signUp(email, password);
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
