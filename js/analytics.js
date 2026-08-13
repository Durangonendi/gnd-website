window.dataLayer = window.dataLayer || [];
function gtag() {
  dataLayer.push(arguments);
}
gtag("js", new Date());
gtag("config", "G-37LSLM4SE6");

document.addEventListener("click", function (e) {
  var link = e.target.closest('a[href*="wa.me"]');
  if (!link) return;
  gtag("event", "generate_lead", {
    lead_source: "whatsapp",
    page_path: window.location.pathname,
  });
});
