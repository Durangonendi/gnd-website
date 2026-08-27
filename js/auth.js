(function () {
  "use strict";

  var SUPABASE_URL = "https://ffqjotevmozjidhhjsqy.supabase.co";
  var SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmcWpvdGV2bW96amlkaGhqc3F5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2NzgwMzYsImV4cCI6MjA5ODI1NDAzNn0.tQ1SjyCnmSKqwrpQRQ177DR88XREG7QCwZ74gkAgCXs";

  var client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
  window.gndSupabase = client;

  // --- Faz 7: Marketplace event tracking (GND OS funnel'ı için) ---
  // Ziyaretçiyi anonim bir id ile takip eder, UTM parametrelerini yakalar,
  // ve website_visit / registration / listing_created / request_created
  // olaylarını marketplace_events tablosuna yazar. Kişisel veri içermez.
  function getVisitorRef() {
    try {
      var ref = localStorage.getItem("gnd_visitor_ref");
      if (!ref) {
        ref = (window.crypto && crypto.randomUUID) ? crypto.randomUUID() : "v_" + Date.now() + "_" + Math.random().toString(36).slice(2);
        localStorage.setItem("gnd_visitor_ref", ref);
      }
      return ref;
    } catch (e) { return null; }
  }

  function getUtm() {
    try {
      var params = new URLSearchParams(window.location.search);
      var fromUrl = {
        utm_source: params.get("utm_source"),
        utm_medium: params.get("utm_medium"),
        utm_campaign: params.get("utm_campaign"),
        utm_content: params.get("utm_content"),
      };
      if (fromUrl.utm_source || fromUrl.utm_medium || fromUrl.utm_campaign) {
        sessionStorage.setItem("gnd_utm", JSON.stringify(fromUrl));
        return fromUrl;
      }
      var stored = sessionStorage.getItem("gnd_utm");
      return stored ? JSON.parse(stored) : { utm_source: null, utm_medium: null, utm_campaign: null, utm_content: null };
    } catch (e) { return { utm_source: null, utm_medium: null, utm_campaign: null, utm_content: null }; }
  }

  window.gndTrack = function (eventType, extra) {
    try {
      var utm = getUtm();
      client.from("marketplace_events").insert({
        visitor_ref: getVisitorRef(),
        utm_source: utm.utm_source,
        utm_medium: utm.utm_medium,
        utm_campaign: utm.utm_campaign,
        utm_content: utm.utm_content,
        event_type: eventType,
        metadata: extra || null,
      }).then(function () {}, function () {});
    } catch (e) { /* takip hatası sitenin çalışmasını engellemez */ }
  };

  (function trackVisitOnce() {
    try {
      if (sessionStorage.getItem("gnd_visit_tracked")) return;
      sessionStorage.setItem("gnd_visit_tracked", "1");
      window.gndTrack("website_visit", { page: window.location.pathname });
    } catch (e) {}
  })();

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

    var navToggle = document.querySelector(".nav-toggle");
    var header = document.querySelector(".site-header");
    if (navToggle && header) {
      navToggle.addEventListener("click", function () {
        header.classList.toggle("nav-open");
      });
    }
    document.querySelectorAll(".nav-dropdown-toggle").forEach(function (toggle) {
      toggle.addEventListener("click", function (e) {
        e.preventDefault();
        toggle.closest(".nav-dropdown").classList.toggle("dd-open");
      });
    });
  });
})();
