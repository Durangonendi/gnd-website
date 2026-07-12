(function () {
  var stored = localStorage.getItem('gnd-site-lang');
  var lang = stored === 'tr' ? 'tr' : 'en';

  function apply(l) {
    document.documentElement.lang = l;
    document.querySelectorAll('[data-tr]').forEach(function (el) {
      if (el.dataset.en === undefined) el.dataset.en = el.innerHTML;
      el.innerHTML = l === 'tr' ? el.dataset.tr : el.dataset.en;
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
