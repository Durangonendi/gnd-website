// Vercel serverless function - dynamic sitemap of published Makine Pazarı listings.
// Served at /sitemap-pazar.xml (see vercel.json rewrite) so every approved listing
// is discoverable by search engines without hand-editing sitemap.xml.

const SUPABASE_URL = "https://ffqjotevmozjidhhjsqy.supabase.co";
const SUPABASE_ANON_KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmcWpvdGV2bW96amlkaGhqc3F5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2NzgwMzYsImV4cCI6MjA5ODI1NDAzNn0.tQ1SjyCnmSKqwrpQRQ177DR88XREG7QCwZ74gkAgCXs";

function xmlEscape(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export default async function handler(req, res) {
  let rows = [];
  try {
    const url =
      SUPABASE_URL +
      "/rest/v1/market_requests?onay_durumu=eq.yayinda&select=id,created_at&order=created_at.desc&limit=5000";
    const r = await fetch(url, {
      headers: { apikey: SUPABASE_ANON_KEY, Authorization: "Bearer " + SUPABASE_ANON_KEY },
    });
    if (r.ok) rows = await r.json();
  } catch (e) {
    rows = [];
  }

  const urls = (Array.isArray(rows) ? rows : [])
    .filter((x) => x && x.id)
    .map((x) => {
      const last = x.created_at ? new Date(x.created_at).toISOString().slice(0, 10) : null;
      return (
        "<url><loc>https://gndmachinery.com/pazar.html?id=" +
        xmlEscape(encodeURIComponent(x.id)) +
        "</loc>" +
        (last ? "<lastmod>" + last + "</lastmod>" : "") +
        "<changefreq>weekly</changefreq><priority>0.6</priority></url>"
      );
    })
    .join("\n");

  const xml =
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    urls +
    "\n</urlset>\n";

  res.setHeader("Content-Type", "application/xml; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=300, s-maxage=900, stale-while-revalidate=3600");
  res.status(200).send(xml);
}
