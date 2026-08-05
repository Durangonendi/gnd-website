(function () {
  "use strict";

  var SUPABASE_URL = "https://ffqjotevmozjidhhjsqy.supabase.co";
  var SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmcWpvdGV2bW96amlkaGhqc3F5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2NzgwMzYsImV4cCI6MjA5ODI1NDAzNn0.tQ1SjyCnmSKqwrpQRQ177DR88XREG7QCwZ74gkAgCXs";

  var client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  window.gndSupabase = client;

  window.gndAuth = {
    signUp: function (email, password) {
      return client.auth.signUp({ email: email, password: password });
    },
    signIn: function (email, password) {
      return client.auth.signInWithPassword({ email: email, password: password });
    },
    signOut: function () {
      return client.auth.signOut();
    },
    getUser: async function () {
      var res = await client.auth.getUser();
      return res.data ? res.data.user : null;
    },
  };

  function siteRoot() {
    // pages under /makineler/, /yedek-parca/, /hizmetler/, /hesaplama-araclari/ are one level deep
    var deep = /\/(makineler|yedek-parca|hizmetler|hesaplama-araclari)\//.test(window.location.pathname);
    return deep ? "../" : "";
  }

  async function renderAuthNav() {
    var slot = document.getElementById("auth-nav-slot");
    if (!slot) return;
    var root = siteRoot();
    var user = await window.gndAuth.getUser();
    if (user) {
      slot.innerHTML =
        '<a href="' + root + 'hesabim.html" class="auth-link">' + (user.email || "Hesabım") + "</a>" +
        '<a href="#" id="auth-logout-link" class="auth-link">Çıkış</a>';
      var logoutLink = document.getElementById("auth-logout-link");
      if (logoutLink) {
        logoutLink.addEventListener("click", async function (e) {
          e.preventDefault();
          await window.gndAuth.signOut();
          window.location.href = root + "index.html";
        });
      }
    } else {
      slot.innerHTML = '<a href="' + root + 'giris.html" class="auth-link">Giriş Yap</a>';
    }
  }

  document.addEventListener("DOMContentLoaded", renderAuthNav);
})();
