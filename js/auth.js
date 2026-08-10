(function () {
  "use strict";

  var SUPABASE_URL = "https://ffqjotevmozjidhhjsqy.supabase.co";
  var SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmcWpvdGV2bW96amlkaGhqc3F5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2NzgwMzYsImV4cCI6MjA5ODI1NDAzNn0.tQ1SjyCnmSKqwrpQRQ177DR88XREG7QCwZ74gkAgCXs";

  var client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  window.gndSupabase = client;

  window.gndAuth = {
    signUp: function (email, password, metadata) {
      var redirectTo = window.location.origin + window.location.pathname.replace(/[^/]*$/, "") + "giris.html";
      return client.auth.signUp({
        email: email,
        password: password,
        options: { data: metadata || {}, emailRedirectTo: redirectTo },
      });
    },
    signIn: function (email, password) {
      return client.auth.signInWithPassword({ email: email, password: password });
    },
    signOut: function () {
      return client.auth.signOut();
    },
    getUser: async function () {
      var res = await client.auth.getSession();
      return res.data && res.data.session ? res.data.session.user : null;
    },
  };

  function siteRoot() {
    // pages under /makineler/, /yedek-parca/, /hizmetler/, /hesaplama-araclari/ are one level deep
    var deep = /\/(makineler|yedek-parca|hizmetler|hesaplama-araclari|blog)\//.test(window.location.pathname);
    return deep ? "../" : "";
  }

  function getLang() {
    return localStorage.getItem("gnd-site-lang") === "tr" ? "tr" : "en";
  }

  var AUTH_TXT = {
    account: { tr: "Hesabım", en: "My Account" },
    logout: { tr: "Çıkış", en: "Log Out" },
    login: { tr: "Giriş Yap", en: "Log In" },
  };

  async function renderAuthNav() {
    var slot = document.getElementById("auth-nav-slot");
    if (!slot) return;
    var root = siteRoot();
    var lang = getLang();
    var user = await window.gndAuth.getUser();
    if (user) {
      var displayName = (user.user_metadata && user.user_metadata.ad_soyad) || user.email || AUTH_TXT.account[lang];
      slot.innerHTML =
        '<a href="' + root + 'hesabim.html" class="auth-link">' + displayName + "</a>" +
        '<a href="#" id="auth-logout-link" class="auth-link">' + AUTH_TXT.logout[lang] + "</a>";
      var logoutLink = document.getElementById("auth-logout-link");
      if (logoutLink) {
        logoutLink.addEventListener("click", async function (e) {
          e.preventDefault();
          await window.gndAuth.signOut();
          window.location.href = root + "index.html";
        });
      }
    } else {
      slot.innerHTML = '<a href="' + root + 'giris.html" class="auth-link">' + AUTH_TXT.login[lang] + "</a>";
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    renderAuthNav();
    var langSelect = document.getElementById("lang-select");
    if (langSelect) {
      langSelect.addEventListener("change", function () {
        setTimeout(renderAuthNav, 0);
      });
    }
  });
})();
