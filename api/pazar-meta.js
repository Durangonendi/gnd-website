// Vercel serverless function - serves pazar.html but with per-listing
// Open Graph / Twitter meta tags injected server-side, so link previews on
// WhatsApp/Facebook/etc and search engine crawlers see the actual listing
// title/description/photo instead of the generic page shell.

import fs from "fs";
import path from "path";

const SUPABASE_URL = "https://ffqjotevmozjidhhjsqy.supabase.co";
const SUPABASE_ANON_KEY =
  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZmcWpvdGV2bW96amlkaGhqc3F5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI2NzgwMzYsImV4cCI6MjA5ODI1NDAzNn0.tQ1SjyCnmSKqwrpQRQ177DR88XREG7QCwZ74gkAgCXs";

const FALLBACK_IMAGE = "https://gndmachinery.com/assets/logo-header.png";

function escapeAttr(s) {
  return String(s || "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function cleanDescription(raw) {
  let text = raw || "";
  text = text.replace(/^\[img:[^\]]+\]\s*/, "");
  const langMatch = text.match(/^\[TR\]([\s\S]*?)\[EN\]([\s\S]*)$/);
  if (langMatch) text = langMatch[1];
  text = text.replace(/\n+/g, " · ").trim();
  return text.length > 200 ? text.slice(0, 200).trim() + "…" : text;
}

async function fetchListing(id) {
  const url =
    SUPABASE_URL +
    "/rest/v1/market_requests?id=eq." +
    encodeURIComponent(id) +
    "&onay_durumu=eq.yayinda&select=id,baslik,aciklama,foto_urls,fiyat,durum_bilgisi";
  const res = await fetch(url, {
    headers: { apikey: SUPABASE_ANON_KEY, Authorization: "Bearer " + SUPABASE_ANON_KEY },
  });
  if (!res.ok) return null;
  const rows = await res.json();
  return Array.isArray(rows) && rows.length ? rows[0] : null;
}

export default async function handler(req, res) {
  const id = typeof req.query.id === "string" ? req.query.id : null;
  const filePath = path.join(process.cwd(), "pazar.html");
  let html = fs.readFileSync(filePath, "utf8");

  let ogTitle = "Makine Pazarı — GND Machinery";
  let ogDescription =
    "İş makinesi, ataşman veya yedek parça alım/satım ilanlarını görüntüleyin veya ücretsiz ilan verin.";
  let ogImage = FALLBACK_IMAGE;
  const pageUrl = "https://gndmachinery.com/pazar.html" + (id ? "?id=" + encodeURIComponent(id) : "");

  if (id) {
    try {
      const listing = await fetchListing(id);
      if (listing) {
        ogTitle = listing.baslik + " — GND Machinery";
        const desc = cleanDescription(listing.aciklama);
        ogDescription = [listing.durum_bilgisi, listing.fiyat, desc].filter(Boolean).join(" · ") || ogDescription;
        if (listing.foto_urls && listing.foto_urls.length) ogImage = listing.foto_urls[0];
      }
    } catch (e) {
      // fall through to generic tags on any error
    }
  }

  const metaTags =
    '<meta property="og:type" content="website">\n' +
    '<meta property="og:url" content="' + escapeAttr(pageUrl) + '">\n' +
    '<meta property="og:title" content="' + escapeAttr(ogTitle) + '">\n' +
    '<meta property="og:description" content="' + escapeAttr(ogDescription) + '">\n' +
    '<meta property="og:image" content="' + escapeAttr(ogImage) + '">\n' +
    '<meta name="twitter:card" content="summary_large_image">\n' +
    '<meta name="twitter:title" content="' + escapeAttr(ogTitle) + '">\n' +
    '<meta name="twitter:description" content="' + escapeAttr(ogDescription) + '">\n' +
    '<meta name="twitter:image" content="' + escapeAttr(ogImage) + '">\n';

  html = html.replace(
    /<meta name="description"[^>]*>/,
    '<meta name="description" content="' + escapeAttr(ogDescription) + '">\n' + metaTags
  );
  html = html.replace(/<title[^>]*>[^<]*<\/title>/, "<title>" + escapeAttr(ogTitle) + "</title>");

  res.setHeader("Content-Type", "text/html; charset=utf-8");
  res.setHeader("Cache-Control", "public, max-age=60, s-maxage=300, stale-while-revalidate=600");
  res.status(200).send(html);
}
