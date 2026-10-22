(function () {
  "use strict";
  var drawer = document.getElementById("side-drawer");
  var overlay = document.getElementById("drawer-overlay");
  var openBtn = document.getElementById("drawer-open");
  var closeBtn = document.getElementById("drawer-close");
  if (!drawer || !overlay || !openBtn) return;

  function setOpen(open) {
    drawer.classList.toggle("open", open);
    overlay.classList.toggle("open", open);
    drawer.setAttribute("aria-hidden", open ? "false" : "true");
    openBtn.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.classList.toggle("drawer-locked", open);
    if (open && closeBtn) closeBtn.focus();
  }

  openBtn.addEventListener("click", function () { setOpen(true); });
  if (closeBtn) closeBtn.addEventListener("click", function () { setOpen(false); });
  overlay.addEventListener("click", function () { setOpen(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
})();
