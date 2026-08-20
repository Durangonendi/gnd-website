(function () {
  "use strict";

  var messages = [];
  var isOpen = false;
  var isSending = false;

  var WELCOME_TEXT =
    "Merhaba! Ben GND'nin AI Makine Danışmanıyım. Sana uygun makineyi önerebilir, ayrıca makinende yaşadığın arıza/bakım belirtileri için genel yönlendirme yapabilirim. Nasıl yardımcı olabilirim?";

  function el(tag, attrs, children) {
    var e = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        if (k === "class") e.className = attrs[k];
        else if (k === "text") e.textContent = attrs[k];
        else e.setAttribute(k, attrs[k]);
      });
    }
    (children || []).forEach(function (c) {
      e.appendChild(c);
    });
    return e;
  }

  function scrollToBottom(box) {
    box.scrollTop = box.scrollHeight;
  }

  function addBubble(box, role, text) {
    var bubble = el("div", { class: "advisor-bubble advisor-bubble-" + role, text: text });
    box.appendChild(bubble);
    scrollToBottom(box);
    return bubble;
  }

  async function sendMessage(box, form, input, text) {
    if (isSending) return;
    isSending = true;
    messages.push({ role: "user", content: text });
    addBubble(box, "user", text);

    var typing = addBubble(box, "assistant", "Yazıyor...");
    typing.classList.add("advisor-bubble-typing");

    try {
      var res = await fetch("/api/advisor", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ messages: messages }),
      });
      var data = await res.json();
      typing.remove();
      if (!res.ok) {
        addBubble(box, "assistant", "Bir sorun oluştu: " + (data.error || "bilinmeyen hata") + ". Lütfen WhatsApp'tan bize ulaş.");
      } else {
        messages.push({ role: "assistant", content: data.reply });
        addBubble(box, "assistant", data.reply);
      }
    } catch (err) {
      typing.remove();
      addBubble(box, "assistant", "Bağlantı hatası oldu. Lütfen WhatsApp'tan bize ulaş.");
    } finally {
      isSending = false;
    }
  }

  function buildWidget() {
    var lang = localStorage.getItem("gnd-site-lang") === "en" ? "en" : "tr";
    var isTR = lang === "tr";

    var fabLabel = isTR ? "Canlı Destek" : "Live Support";
    var fab = el("button", { class: "support-fab", type: "button", "aria-label": fabLabel }, [
      el("span", { text: "💬" }),
      el("span", { text: fabLabel }),
    ]);

    var waText = isTR
      ? "Merhaba, GND İş Makineleri hakkında bilgi almak istiyorum."
      : "Hi, I'd like more information about GND İş Makineleri.";
    var waLink = "https://wa.me/905550708034?text=" + encodeURIComponent(waText);

    var menu = el("div", { class: "support-menu" });
    var aiOption = el("button", { class: "support-menu-item", type: "button" }, [
      el("span", { class: "support-menu-icon", text: "🤖" }),
      el("span", { text: isTR ? "AI Danışman" : "AI Advisor" }),
    ]);
    var waOption = el("a", { class: "support-menu-item", href: waLink, target: "_blank", rel: "noopener" }, [
      el("span", { class: "support-menu-icon", text: "💬" }),
      el("span", { text: "WhatsApp" }),
    ]);
    menu.appendChild(aiOption);
    menu.appendChild(waOption);

    var menuOpen = false;
    function setMenuOpen(open) {
      menuOpen = open;
      menu.classList.toggle("open", open);
    }
    fab.addEventListener("click", function () {
      setMenuOpen(!menuOpen);
    });
    aiOption.addEventListener("click", function () {
      setMenuOpen(false);
      isOpen = true;
      panel.classList.add("open");
      input.focus();
    });
    waOption.addEventListener("click", function () {
      setMenuOpen(false);
    });
    document.addEventListener("click", function (e) {
      if (menuOpen && !menu.contains(e.target) && !fab.contains(e.target)) {
        setMenuOpen(false);
      }
    });

    var panel = el("div", { class: "advisor-panel" });
    var header = el("div", { class: "advisor-panel-header" }, [
      el("span", { text: "AI Makine Danışmanı" }),
      el("button", { class: "advisor-close-btn", type: "button", "aria-label": "Kapat", text: "✕" }),
    ]);
    var box = el("div", { class: "advisor-messages" });
    var form = el("form", { class: "advisor-form" });
    var input = el("input", { type: "text", placeholder: "Mesajını yaz...", class: "advisor-input" });
    var sendBtn = el("button", { type: "submit", class: "advisor-send-btn", text: "Gönder" });
    form.appendChild(input);
    form.appendChild(sendBtn);

    panel.appendChild(header);
    panel.appendChild(box);
    panel.appendChild(form);

    addBubble(box, "assistant", WELCOME_TEXT);
    var disclaimer = el("div", {
      class: "advisor-disclaimer",
      text: "Bu bir yapay zeka asistanıdır, verdiği bilgiler genel yönlendirme amaçlıdır. Kesin fiyat ve teknik detay için GND ekibiyle iletişime geçin.",
    });
    box.appendChild(disclaimer);

    header.querySelector(".advisor-close-btn").addEventListener("click", function () {
      isOpen = false;
      panel.classList.remove("open");
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var text = input.value.trim();
      if (!text) return;
      input.value = "";
      sendMessage(box, form, input, text);
    });

    document.body.appendChild(fab);
    document.body.appendChild(menu);
    document.body.appendChild(panel);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildWidget);
  } else {
    buildWidget();
  }
})();
