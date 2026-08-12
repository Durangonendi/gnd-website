(function () {
  var KEY = "gnd-fraud-notice-seen-v1";
  var overlay = document.getElementById("fraud-notice-overlay");
  if (!overlay) return;
  if (!localStorage.getItem(KEY)) {
    overlay.classList.add("is-visible");
  }
  var closeBtn = document.getElementById("fraud-notice-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", function () {
      localStorage.setItem(KEY, "1");
      overlay.classList.remove("is-visible");
    });
  }
})();
