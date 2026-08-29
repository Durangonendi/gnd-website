(function () {
  "use strict";

  var mode = "login"; // or "signup"

  var TXT = {
    loginTitle: { tr: "Giriş Yap", en: "Log In" },
    signupTitle: { tr: "Kayıt Ol", en: "Sign Up" },
    loginToggle: { tr: "Hesabın yok mu? Kayıt ol", en: "Don't have an account? Sign up" },
    signupToggle: { tr: "Zaten hesabın var mı? Giriş yap", en: "Already have an account? Log in" },
    missingFields: { tr: "Lütfen ad soyad ve telefon numaranı da girin.", en: "Please also enter your full name and phone number." },
    signupSuccess: { tr: "Kayıt oluşturuldu. E-postana gelen onay linkine tıkladıktan sonra giriş yapabilirsin.", en: "Account created. You can log in after clicking the confirmation link sent to your email." },
    genericError: { tr: "Bir hata oluştu, tekrar deneyin.", en: "Something went wrong, please try again." },
  };

  function getLang() {
    return localStorage.getItem("gnd-site-lang") === "tr" ? "tr" : "en";
  }

  function showMessage(textOrKey, isError) {
    var el = document.getElementById("authMessage");
    if (TXT[textOrKey]) {
      el.textContent = TXT[textOrKey][getLang()];
      el.dataset.msgKey = textOrKey;
    } else {
      el.textContent = textOrKey;
      delete el.dataset.msgKey;
    }
    el.style.display = "block";
    el.style.color = isError ? "#c0392b" : "inherit";
  }

  function applyMode() {
    var lang = getLang();
    var title = document.getElementById("authPageTitle");
    var submitBtn = document.getElementById("authSubmitBtn");
    var toggle = document.getElementById("authToggleMode");
    var adSoyadField = document.getElementById("authAdSoyadField");
    var telefonField = document.getElementById("authTelefonField");
    var adSoyadInput = document.getElementById("authAdSoyad");
    var telefonInput = document.getElementById("authTelefon");
    if (mode === "login") {
      title.textContent = TXT.loginTitle[lang];
      submitBtn.textContent = TXT.loginTitle[lang];
      toggle.textContent = TXT.loginToggle[lang];
      adSoyadField.style.display = "none";
      telefonField.style.display = "none";
      adSoyadInput.required = false;
      telefonInput.required = false;
    } else {
      title.textContent = TXT.signupTitle[lang];
      submitBtn.textContent = TXT.signupTitle[lang];
      toggle.textContent = TXT.signupToggle[lang];
      adSoyadField.style.display = "";
      telefonField.style.display = "";
      adSoyadInput.required = true;
      telefonInput.required = true;
    }
    var msgEl = document.getElementById("authMessage");
    if (msgEl.dataset.msgKey) msgEl.textContent = TXT[msgEl.dataset.msgKey][lang];
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
            showMessage("missingFields", true);
            submitBtn.disabled = false;
            return;
          }
          var res2 = await window.gndAuth.signUp(email, password, { ad_soyad: adSoyad, telefon: telefon });
          if (res2.error) throw res2.error;
          if (typeof window.gndTrack === "function") window.gndTrack("registration", { email: email, ad_soyad: adSoyad, telefon: telefon });
          if (res2.data && res2.data.session) {
            window.location.href = "hesabim.html";
          } else {
            showMessage("signupSuccess", false);
          }
        }
      } catch (err) {
        showMessage(err.message || TXT.genericError[getLang()], true);
      } finally {
        submitBtn.disabled = false;
      }
    });

    var langSelect = document.getElementById("lang-select");
    if (langSelect) {
      langSelect.addEventListener("change", applyMode);
    }
  });
})();
