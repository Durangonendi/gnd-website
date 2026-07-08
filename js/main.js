const STORAGE_KEY = "gnd-site-lang";
let currentCondition = "new"; // "new" | "used"

function buildWhatsAppLink(message) {
  const encoded = encodeURIComponent(message);
  return `https://wa.me/${WHATSAPP_NUMBER}?text=${encoded}`;
}

function getLang() {
  return localStorage.getItem(STORAGE_KEY) || "tr";
}

function applyTranslations(lang) {
  const dict = TRANSLATIONS[lang];
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) el.textContent = dict[key];
  });
  document.documentElement.lang = lang;

  document.getElementById("header-whatsapp-btn").href = buildWhatsAppLink(dict.quote_generic);
  document.getElementById("contact-whatsapp-btn").href = buildWhatsAppLink(dict.quote_generic);
  document.getElementById("floating-whatsapp-btn").href = buildWhatsAppLink(dict.quote_generic);
}

function conditionLabel(lang) {
  return currentCondition === "new" ? TRANSLATIONS[lang].condition_new : TRANSLATIONS[lang].condition_used;
}

function renderCategoryGrid(gridId, list, lang, includeCondition) {
  const grid = document.getElementById(gridId);
  grid.innerHTML = "";
  list.forEach((cat) => {
    const card = document.createElement("div");
    card.className = "category-card";
    const label = includeCondition ? `${conditionLabel(lang)} ${cat.name[lang]}` : cat.name[lang];
    const message = TRANSLATIONS[lang].quote_intro + label + TRANSLATIONS[lang].quote_middle;
    card.innerHTML = `
      <div class="category-icon">${cat.icon}</div>
      <h3>${cat.name[lang]}</h3>
      <p>${cat.desc[lang]}</p>
      <a class="category-quote-btn" href="${buildWhatsAppLink(message)}" target="_blank" rel="noopener">
        ${TRANSLATIONS[lang].get_quote} →
      </a>
    `;
    grid.appendChild(card);
  });
}

function renderAll(lang) {
  renderCategoryGrid("category-grid", CATEGORIES, lang, true);
  renderCategoryGrid("spareparts-grid", SPARE_PARTS_CATEGORIES, lang, false);
}

function setLang(lang) {
  localStorage.setItem(STORAGE_KEY, lang);
  applyTranslations(lang);
  renderAll(lang);
  document.getElementById("lang-select").value = lang;
}

function setCondition(condition) {
  currentCondition = condition;
  document.querySelectorAll(".condition-toggle button").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.condition === condition);
  });
  renderCategoryGrid("category-grid", CATEGORIES, getLang(), true);
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("footer-year").textContent = new Date().getFullYear();
  document.getElementById("stat-category-count").textContent = CATEGORIES.length + "+";
  const initialLang = getLang();
  setLang(initialLang);

  document.getElementById("lang-select").addEventListener("change", (e) => {
    setLang(e.target.value);
  });

  document.querySelectorAll(".condition-toggle button").forEach((btn) => {
    btn.addEventListener("click", () => setCondition(btn.dataset.condition));
  });
});
