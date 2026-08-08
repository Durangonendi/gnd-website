(function () {
  var stored = localStorage.getItem('gnd-site-lang');
  var lang = stored === 'tr' ? 'tr' : 'en';

  function apply(l) {
    document.documentElement.lang = l;
    document.querySelectorAll('[data-tr]').forEach(function (el) {
      if (el.dataset.en === undefined) el.dataset.en = el.innerHTML;
      el.innerHTML = l === 'tr' ? el.dataset.tr : el.dataset.en;
    });
    document.querySelectorAll('[data-href-tr]').forEach(function (el) {
      if (el.dataset.hrefEn === undefined) el.dataset.hrefEn = el.getAttribute('href');
      el.setAttribute('href', l === 'tr' ? el.dataset.hrefTr : el.dataset.hrefEn);
    });
    document.querySelectorAll('[data-alt-tr]').forEach(function (el) {
      if (el.dataset.altEn === undefined) el.dataset.altEn = el.getAttribute('alt');
      el.setAttribute('alt', l === 'tr' ? el.dataset.altTr : el.dataset.altEn);
    });
    document.querySelectorAll('[data-tr-placeholder]').forEach(function (el) {
      if (el.dataset.placeholderEn === undefined) el.dataset.placeholderEn = el.getAttribute('placeholder');
      el.setAttribute('placeholder', l === 'tr' ? el.dataset.trPlaceholder : el.dataset.placeholderEn);
    });
    var sel = document.getElementById('lang-select');
    if (sel) sel.value = l;
  }

  apply(lang);

  var sel = document.getElementById('lang-select');
  if (sel) {
    sel.addEventListener('change', function (e) {
      localStorage.setItem('gnd-site-lang', e.target.value);
      apply(e.target.value);
    });
  }
})();
