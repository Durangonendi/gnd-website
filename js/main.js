const STORAGE_KEY = "gnd-site-lang";
let currentCondition = "new"; // "new" | "used"
let searchTerm = "";
let currentGroup = "all";

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
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (dict[key]) el.placeholder = dict[key];
  });
  document.documentElement.lang = lang;

  const hw = document.getElementById("header-whatsapp-btn");
  if (hw) hw.href = buildWhatsAppLink(dict.quote_generic);
  const cw = document.getElementById("contact-whatsapp-btn");
  if (cw) cw.href = buildWhatsAppLink(dict.quote_generic);
}

function conditionLabel(lang) {
  return currentCondition === "new" ? TRANSLATIONS[lang].condition_new : TRANSLATIONS[lang].condition_used;
}

function renderCategoryGrid(gridId, list, lang, includeCondition) {
  const grid = document.getElementById(gridId);
  if (!grid) return;
  grid.innerHTML = "";
  list.forEach((cat) => {
    const card = document.createElement("div");
    card.className = "category-card";
    const label = includeCondition ? `${conditionLabel(lang)} ${cat.name[lang]}` : cat.name[lang];
    const message = TRANSLATIONS[lang].quote_intro + label + TRANSLATIONS[lang].quote_middle;
    const titleHtml = cat.page ? `<a href="${cat.page}">${cat.name[lang]}</a>` : cat.name[lang];
    const mediaHtml = cat.image
      ? `<div class="category-photo-wrap"><img class="category-photo" src="${cat.image}" alt="${cat.name[lang]}" loading="lazy"></div>`
      : `<div class="category-icon">${cat.icon}</div>`;
    card.innerHTML = `
      ${mediaHtml}
      <h3>${titleHtml}</h3>
      <p>${cat.desc[lang]}</p>
      <a class="category-quote-btn" href="${buildWhatsAppLink(message)}" target="_blank" rel="noopener">
        ${TRANSLATIONS[lang].get_quote} →
      </a>
    `;
    grid.appendChild(card);
  });
}

function filteredCategories(lang) {
  const term = searchTerm.trim().toLocaleLowerCase("tr");
  return CATEGORIES.filter((cat) => {
    const matchesTerm = !term || cat.name[lang].toLocaleLowerCase("tr").includes(term);
    const matchesGroup = currentGroup === "all" || cat.group === currentGroup;
    return matchesTerm && matchesGroup;
  });
}

function renderGroupFilter(lang) {
  const wrap = document.getElementById("group-filter");
  if (!wrap) return;
  wrap.innerHTML = "";
  CATEGORY_GROUPS.forEach((g) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "group-filter-btn" + (g.id === currentGroup ? " active" : "");
    btn.textContent = g.label[lang];
    btn.addEventListener("click", () => {
      currentGroup = g.id;
      renderGroupFilter(lang);
      renderMachines(lang);
    });
    wrap.appendChild(btn);
  });
}

function renderMachines(lang) {
  const list = filteredCategories(lang);
  renderCategoryGrid("category-grid", list, lang, true);
  const cg = document.getElementById("category-grid");
  if (cg) cg.style.display = list.length ? "grid" : "none";
  const nr = document.getElementById("category-no-results");
  if (nr) nr.style.display = list.length ? "none" : "block";
}

function renderAll(lang) {
  renderGroupFilter(lang);
  renderMachines(lang);
  renderCategoryGrid("spareparts-grid", SPARE_PARTS_CATEGORIES, lang, false);
}

function setLang(lang) {
  localStorage.setItem(STORAGE_KEY, lang);
  applyTranslations(lang);
  renderAll(lang);
  const ls = document.getElementById("lang-select");
  if (ls) ls.value = lang;
}

function setCondition(condition) {
  currentCondition = condition;
  document.querySelectorAll(".condition-toggle button").forEach((btn) => {
    btn.classList.toggle("active", btn.dataset.condition === condition);
  });
  renderMachines(getLang());
}

document.addEventListener("DOMContentLoaded", () => {
  const fy = document.getElementById("footer-year");
  if (fy) fy.textContent = new Date().getFullYear();
  const sc = document.getElementById("stat-category-count");
  if (sc) sc.textContent = CATEGORIES.length + "+";
  const initialLang = getLang();
  setLang(initialLang);

  const langSel = document.getElementById("lang-select");
  if (langSel) langSel.addEventListener("change", (e) => {
    setLang(e.target.value);
  });

  document.querySelectorAll(".condition-toggle button").forEach((btn) => {
    btn.addEventListener("click", () => setCondition(btn.dataset.condition));
  });

  const csi = document.getElementById("category-search-input");
  if (csi) csi.addEventListener("input", (e) => {
    searchTerm = e.target.value;
    renderMachines(getLang());
  });
});
