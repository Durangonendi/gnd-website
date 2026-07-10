# Generates English-first SEO landing pages per machine/spare-part category.
# To add/change a category: update MACHINES / SPARE_PARTS below AND the matching
# entry in js/i18n.js (CATEGORIES / SPARE_PARTS_CATEGORIES) — both keep the same data.
import os

SITE_NAME = "GND Machinery"
BASE_URL = "https://gnd-website-five.vercel.app"
WHATSAPP_NUMBER = "905550708034"

ICONS = {
    "excavator": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 20h9M14 20h7M6 20V9l6-3 4 2-3 5M6 9l4 2M13 13l4 2 3-4"/><circle cx="8" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/></svg>',
    "loader": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 17h2l2-6h6l2 6h6M9 11V6h4l2 5"/><circle cx="7" cy="19" r="1.6"/><circle cx="18" cy="19" r="1.6"/></svg>',
    "backhoe-loader": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 17h2l2-6h6l2 6h4M8 11V6h4l1.5 4M16 17l4-3 2 1-2 4h-4"/><circle cx="6" cy="19" r="1.5"/><circle cx="16" cy="19" r="1.5"/></svg>',
    "manlift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 21V11l10-6v9L6 21z"/><rect x="4" y="19" width="6" height="3"/><circle cx="16" cy="21" r="1.4"/></svg>',
    "telehandler": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 20h4l14-9M20 11l1 2-3 2M6 20v-4h4v4"/><circle cx="6" cy="20" r="1.4"/><circle cx="14" cy="20" r="1.4"/></svg>',
    "roller": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="6" cy="16" r="4"/><path d="M10 16h5a3 3 0 0 0 3-3V9h-4"/></svg>',
    "finisher": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 10h13l4 4v3H3z"/><circle cx="7" cy="19" r="1.5"/><circle cx="16" cy="19" r="1.5"/></svg>',
    "grader": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 19h18M6 19l2-5h8l2 5M9 14V8l3-2 3 2v6"/></svg>',
    "dozer": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 19h3l2-3h9l3 3h3M6 16V9h10v7M4 19v-2h16v2"/></svg>',
    "skid-steer": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 18V11h9l3 3h2v4H4z"/><circle cx="7" cy="20" r="1.4"/><circle cx="16" cy="20" r="1.4"/></svg>',
    "filter": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 4h16l-4 8v6l-4 2v-8L4 4z"/></svg>',
    "mechanical": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14.7 6.3a4 4 0 0 1-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 1 5.4-5.4L15 12l-3-3 2.7-2.7z"/></svg>',
    "hydraulic": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="9" width="12" height="6" rx="1"/><path d="M16 11h4v2h-4M6 9V6h4v3"/></svg>',
    "attachment": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 15l5-5 3 3-5 5-3-3zM11 10l4-4 6 6-4 4M9 17l-4 4"/></svg>',
}

BENEFITS = [
    ("Global manufacturer network", "Access to new and used equipment sourced from trusted producers worldwide."),
    ("New and used options", "Flexible sourcing matched to your budget, timeline, and specification."),
    ("Fast quotation", "Get pricing and availability directly on WhatsApp, without a sign-up form."),
    ("Genuine parts support", "Backed by our own spare parts and after-sales network."),
]

MACHINE_LINKS = [("filters", "Filters"), ("hydraulic-parts", "Hydraulic Parts"), ("attachments", "Attachments")]
PARTS_LINKS = [("excavator", "Excavators"), ("wheel-loader", "Wheel Loaders"), ("bulldozer", "Bulldozers")]

# (slug, name, meta description, intro, icon key, image filename)
MACHINES = [
    ("mini-excavator", "Mini Excavators",
     "New and used mini excavators for sale from GND Machinery. Global supplier of compact excavators for construction, landscaping and utility work.",
     "Mini excavators combine compact size with genuine digging power, making them the preferred choice for landscaping, utility work, demolition in tight spaces and urban construction sites. GND Machinery sources new and used mini excavators from a wide international manufacturer network, matching each buyer with the right size, reach and operating weight for their project.",
     "excavator", "mini-ekskavator.jpg"),
    ("excavator", "Excavators",
     "Buy new or used excavators from GND Machinery, a global heavy equipment supplier. Crawler excavators for construction, earthmoving and infrastructure projects.",
     "Excavators are the backbone of any earthmoving operation, and GND Machinery supplies mid-size crawler excavators for construction, road building and general earthmoving work. Through our global manufacturer network, we source both new and used excavators matched to your tonnage, reach and site requirements.",
     "excavator", "orta-ekskavator.jpg"),
    ("mining-excavator", "Mining & Heavy-Duty Excavators",
     "Heavy-duty and mining excavators for sale. GND Machinery supplies large-tonnage excavators for quarries, mines and large-scale earthmoving projects worldwide.",
     "Mining and heavy-duty excavators deliver the digging capacity required for quarries, open-pit mines and large-scale earthmoving projects. GND Machinery's global supply network sources new and used heavy-tonnage excavators, offering competitive quotations for buyers in the mining and quarrying sector.",
     "excavator", "agir-tonaj-ekskavator.jpg"),
    ("wheel-loader", "Wheel Loaders",
     "New and used wheel loaders for sale from GND Machinery. Global supplier of loading equipment for construction, quarrying and material handling.",
     "Wheel loaders are essential for loading, carrying and stockpiling material on any construction or quarry site. GND Machinery supplies new and used wheel loaders in a range of capacities, sourced through our international manufacturer network to match your operation's throughput needs.",
     "loader", "loader.jpg"),
    ("backhoe-loader", "Backhoe Loaders",
     "Backhoe loaders for sale, new and used. GND Machinery supplies versatile backhoe loaders combining excavation and loading in a single machine.",
     "Backhoe loaders combine excavation and loading in a single versatile machine, ideal for small to mid-size construction sites. GND Machinery sources new and used backhoe loaders from trusted manufacturers worldwide, offering flexible supply options for contractors and rental fleets.",
     "backhoe-loader", "bekoloader.jpg"),
    ("boom-lift", "Boom Lifts & Man Lifts",
     "Boom lifts and man lifts for sale. GND Machinery supplies aerial work platforms for maintenance, installation and construction access work.",
     "Boom lifts and man lifts provide safe, efficient access for maintenance, installation and construction work at height. GND Machinery supplies articulating and telescopic boom lifts through its global equipment network, sourced new or used to fit your project's reach and budget.",
     "manlift", "manlift.jpg"),
    ("telehandler", "Telehandlers",
     "Telehandlers for sale, new and used telescopic handlers from GND Machinery, a global heavy equipment supplier for construction and agriculture.",
     "Telehandlers extend the reach of a standard forklift, moving materials to high and hard-to-reach points on construction sites, warehouses and farms. GND Machinery supplies new and used telehandlers sourced through its international manufacturer network.",
     "telehandler", "telehandler.jpg"),
    ("road-roller", "Road Rollers & Compactors",
     "Road rollers and compactors for sale. GND Machinery supplies single and double-drum rollers for road construction and ground compaction projects.",
     "Road rollers and compactors are essential for road construction, ground preparation and asphalt compaction. GND Machinery supplies single and double-drum rollers, sourced new or used to match the compaction requirements of your project.",
     "roller", "silindir.jpg"),
    ("asphalt-paver", "Asphalt Pavers (Finishers)",
     "Asphalt pavers and finishers for sale from GND Machinery, a global supplier of road construction equipment for paving contractors.",
     "Asphalt pavers, also known as finishers, determine the speed and quality of any road paving project. GND Machinery supplies new and used asphalt pavers through its global manufacturer network, matched to your paving width and output requirements.",
     "finisher", "finiser.jpg"),
    ("motor-grader", "Motor Graders",
     "Motor graders for sale, new and used grading equipment from GND Machinery, a global supplier for road construction and site leveling.",
     "Motor graders deliver the precision grading needed for road construction, site leveling and maintenance work. GND Machinery sources new and used motor graders from a global manufacturer network, supporting contractors and infrastructure projects worldwide.",
     "grader", "greyder.jpg"),
    ("bulldozer", "Bulldozers",
     "Bulldozers for sale, new and used dozers from GND Machinery, a global heavy equipment supplier for earthmoving and site preparation.",
     "Bulldozers provide the pushing power needed for site preparation, grading and heavy earthmoving work. GND Machinery supplies new and used bulldozers sourced through its international manufacturer network, matched to your project's horsepower and blade requirements.",
     "dozer", "dozer.jpg"),
    ("skid-steer-loader", "Skid Steer Loaders",
     "Skid steer loaders for sale, compact and versatile loaders from GND Machinery, a global supplier for landscaping, demolition and tight-access sites.",
     "Skid steer loaders bring compact power and tight-radius maneuverability to landscaping, demolition and confined job sites. GND Machinery supplies new and used skid steer loaders through its global equipment network, matched to your attachment and lift capacity needs.",
     "skid-steer", "skid-steer-loader.jpg"),
]

SPARE_PARTS = [
    ("filters", "Heavy Equipment Filters",
     "OEM and aftermarket filters for heavy equipment. GND Machinery supplies oil, fuel, air and hydraulic filters for construction and mining machinery.",
     "Genuine and aftermarket filtration keeps heavy equipment running at peak performance. GND Machinery supplies oil, fuel, air, hydraulic and cabin filters for excavators, loaders and other construction and mining machinery.",
     "filter", "filtre-gruplari.jpg"),
    ("mechanical-parts", "Mechanical Parts & Components",
     "Mechanical parts for heavy equipment: engines, transmissions, undercarriage and drive components supplied globally by GND Machinery.",
     "From engine and transmission components to undercarriage and drive axle groups, GND Machinery supplies mechanical parts for heavy equipment, backed by a global sourcing network and technical support.",
     "mechanical", "mekanik-gruplar.jpg"),
    ("hydraulic-parts", "Hydraulic Parts & Components",
     "Hydraulic parts for heavy equipment: pumps, valves, cylinders and motors supplied globally by GND Machinery for construction and mining machinery.",
     "Hydraulic pumps, control valves, cylinders and motors are critical to the performance of any heavy equipment fleet. GND Machinery supplies hydraulic components for excavators, loaders and other construction machinery through its global parts network.",
     "hydraulic", "hidrolik-gruplar.jpg"),
    ("attachments", "Attachments & Implements",
     "Heavy equipment attachments for sale: buckets, breakers, grapples and implements supplied globally by GND Machinery.",
     "The right attachment turns a single machine into a multi-purpose tool. GND Machinery supplies buckets, hydraulic breakers, grapples and other attachments for excavators, loaders and skid steers worldwide.",
     "attachment", "atasmanlar.jpg"),
]

HEADER = """<header class="site-header">
  <div class="header-inner">
    <a href="{root}index.html" class="logo"><img src="{root}assets/logo-header.png" width="160" height="160" alt="GND Machinery" /></a>
    <nav class="main-nav">
      <a href="{root}index.html#home">Home</a>
      <a href="{root}index.html#categories">Machines</a>
      <a href="{root}index.html#spareparts">Spare Parts</a>
      <a href="{root}index.html#about">About</a>
      <a href="{root}index.html#contact">Contact</a>
    </nav>
    <div class="header-actions">
      <a class="btn btn-primary header-cta" href="https://wa.me/{wa}?text={wa_generic}" target="_blank" rel="noopener">
        <span>Get a Quote</span>
      </a>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="section-inner footer-inner">
    <div>© 2026 GND Machinery — GND İş Makineleri Sanayi ve Ticaret A.Ş.</div>
    <div class="footer-note">Global supplier of heavy equipment and spare parts.</div>
  </div>
</footer>

<a href="https://wa.me/{wa}?text={wa_generic}" class="floating-whatsapp" target="_blank" rel="noopener" aria-label="WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.5A10 10 0 1 0 12 2zm0 18.2a8.15 8.15 0 0 1-4.2-1.15l-.3-.18-3.1.95.95-3-.2-.32A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.25-.13-1.45-.72-1.68-.8-.22-.08-.39-.13-.55.13-.16.25-.63.8-.78.97-.14.16-.28.18-.53.06-.25-.13-1.06-.39-2.02-1.25-.75-.67-1.25-1.5-1.4-1.75-.14-.25-.02-.39.11-.51.11-.11.25-.28.37-.42.13-.14.17-.25.25-.4.08-.16.04-.3-.02-.42-.06-.13-.55-1.34-.76-1.83-.2-.48-.4-.42-.55-.42h-.47c-.16 0-.42.06-.64.3-.22.25-.85.83-.85 2.03s.87 2.36 1 2.52c.12.16 1.7 2.6 4.13 3.64.58.25 1.03.4 1.38.5.58.19 1.11.16 1.53.1.47-.07 1.45-.6 1.65-1.17.2-.58.2-1.07.14-1.17-.06-.1-.22-.16-.47-.28z"/></svg>
  <span>Live Support</span>
</a>"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} | New &amp; Used Supplier — {site_name}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="{root}css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{base_url}/"}},
    {{"@type": "ListItem", "position": 2, "name": "{group_title}", "item": "{base_url}/#categories"}},
    {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "{canonical}"}}
  ]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "{name}",
  "description": "{meta_desc}",
  "provider": {{"@type": "Organization", "name": "GND İş Makineleri Sanayi ve Ticaret A.Ş.", "url": "{base_url}/"}},
  "areaServed": "Worldwide",
  "url": "{canonical}",
  "inLanguage": "en"
}}
</script>
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    {media}
    <h1>{name}</h1>
    <p>{intro}</p>
    <a href="https://wa.me/{wa}?text={wa_quote}" class="btn btn-primary btn-lg" target="_blank" rel="noopener">Get a Quote →</a>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <h2>New &amp; Used {name} Supply</h2>
    <div class="vm-grid">
      <div class="vm-card">
        <h3>New {name}</h3>
        <p>Factory-new units sourced directly from our manufacturer partners, with full specification and delivery lead time provided on request.</p>
      </div>
      <div class="vm-card">
        <h3>Used {name}</h3>
        <p>Inspected used units offering lower upfront cost, sourced from our global network and matched to your working hours and budget.</p>
      </div>
    </div>
  </div>
</section>

<section class="categories-section spareparts-section">
  <div class="section-inner">
    <h2>Why Source Through GND Machinery</h2>
    <div class="category-grid">
      {benefits}
    </div>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <h2>Related Equipment Categories</h2>
    <div class="category-grid">
      {siblings}
    </div>
    <p class="back-link">{cross_links} &nbsp;|&nbsp; <a href="{root}index.html">← Back to home</a></p>
  </div>
</section>

{footer}

</body>
</html>
"""

SIBLING_CARD_PHOTO = """<div class="category-card">
        <div class="category-photo-wrap"><img class="category-photo" src="{root}assets/categories/{image}" alt="{name} supplied by GND Machinery" loading="lazy"></div>
        <h3><a href="{href}">{name}</a></h3>
        <p>{desc}</p>
      </div>"""

SIBLING_CARD_ICON = """<div class="category-card">
        <div class="category-icon">{icon}</div>
        <h3><a href="{href}">{name}</a></h3>
        <p>{desc}</p>
      </div>"""

BENEFIT_CARD = """<div class="category-card">
        <h3>{title}</h3>
        <p>{text}</p>
      </div>"""


def wa_link_text(text):
    from urllib.parse import quote
    return quote(text)


def build_pages(items, out_dir, group_title, url_prefix, root, cross_link_target_prefix, cross_links_list):
    os.makedirs(out_dir, exist_ok=True)
    wa_generic = wa_link_text("Hi, I'd like more information about GND Machinery.")
    header = HEADER.format(root=root, wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    benefits_html = "\n      ".join(BENEFIT_CARD.format(title=t, text=x) for t, x in BENEFITS)
    cross_links_html = " &middot; ".join(f'<a href="{root}{cross_link_target_prefix}/{s}.html">{n}</a>' for s, n in cross_links_list)

    for slug, name, meta_desc, intro, icon_key, image in items:
        sibling_parts = []
        for s, n, m, d, k, img in items:
            if s == slug:
                continue
            if img:
                sibling_parts.append(SIBLING_CARD_PHOTO.format(root=root, image=img, href=f"{s}.html", name=n, desc=m))
            else:
                sibling_parts.append(SIBLING_CARD_ICON.format(icon=ICONS[k], href=f"{s}.html", name=n, desc=m))
        siblings_html = "\n      ".join(sibling_parts)

        wa_quote = wa_link_text(f"Hi, I'd like a quote for {name}.")
        if image:
            media = f'<div class="category-detail-photo"><img src="{root}assets/categories/{image}" alt="{name} for sale — GND Machinery" loading="lazy"></div>'
        else:
            media = f'<div class="category-detail-icon">{ICONS[icon_key]}</div>'
        page = PAGE_TEMPLATE.format(
            name=name, site_name=SITE_NAME, meta_desc=meta_desc, intro=intro,
            canonical=f"{BASE_URL}/{url_prefix}/{slug}.html", base_url=BASE_URL,
            root=root, header=header, media=media, benefits=benefits_html,
            wa=WHATSAPP_NUMBER, wa_quote=wa_quote, cross_links=cross_links_html,
            group_title=group_title, siblings=siblings_html, footer=footer
        )
        with open(os.path.join(out_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  wrote {out_dir}/{slug}.html")


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print("Machine pages:")
    build_pages(MACHINES, os.path.join(root_dir, "makineler"), "Machines", "makineler", "../", "yedek-parca", MACHINE_LINKS)
    print("Spare parts pages:")
    build_pages(SPARE_PARTS, os.path.join(root_dir, "yedek-parca"), "Spare Parts", "yedek-parca", "../", "makineler", PARTS_LINKS)

    urls = [(f"{BASE_URL}/", "weekly", "1.0")]
    for slug, *_ in MACHINES:
        urls.append((f"{BASE_URL}/makineler/{slug}.html", "monthly", "0.8"))
    for slug, *_ in SPARE_PARTS:
        urls.append((f"{BASE_URL}/yedek-parca/{slug}.html", "monthly", "0.7"))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, freq, pri in urls:
        sitemap.append(f"<url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    sitemap.append("</urlset>")
    with open(os.path.join(root_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap) + "\n")
    print(f"sitemap.xml updated ({len(urls)} URLs).")
    print("Done.")
