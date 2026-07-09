# Kategori detay sayfalarını (SEO için ayrı ayrı) üretir.
# Kategori eklemek/değiştirmek için: aşağıdaki MACHINES / SPARE_PARTS listesini VE js/i18n.js içindeki
# CATEGORIES / SPARE_PARTS_CATEGORIES listesini birlikte güncelleyin (iki yerde de aynı bilgi tutuluyor).
import os

SITE_NAME = "GND İş Makineleri"
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

# (slug, ad, kısa açıklama (kart), uzun açıklama (SEO sayfası), icon key)
MACHINES = [
    ("mini-ekskavator", "Mini Ekskavatör", "Dar alan ve hafif hafriyat işleri için kompakt ekskavatörler.",
     "Mini ekskavatörler, dar sokak aralarında, bahçe düzenlemesinde, bina içi yıkım ve küçük çaplı hafriyat işlerinde manevra kabiliyeti sağlar. GND İş Makineleri olarak sıfır ve 2. el mini ekskavatör tedarikinde geniş üretici ağımızla size en uygun teklifi sunuyoruz.", "excavator"),
    ("orta-ekskavator", "Orta Seviye Ekskavatör", "Genel hafriyat ve inşaat işleri için orta sınıf ekskavatörler.",
     "Orta seviye ekskavatörler, konut ve ticari inşaat projelerinde, altyapı çalışmalarında ve genel hafriyat işlerinde en çok tercih edilen makine sınıfıdır. Sıfır ve 2. el seçeneklerle, ihtiyacınıza uygun tonaj ve modeli sizin için buluyoruz.", "excavator"),
    ("agir-tonaj-ekskavator", "Ağır Tonaj Ekskavatör", "Maden ve büyük ölçekli hafriyat için ağır tonajlı ekskavatörler.",
     "Ağır tonajlı ekskavatörler; maden ocakları, büyük ölçekli hafriyat sahaları ve taş ocağı operasyonları için yüksek kazı kapasitesi sunar. Global tedarik ağımız sayesinde ağır tonaj sınıfında sıfır ve 2. el makineler için rekabetçi teklifler hazırlıyoruz.", "excavator"),
    ("loader", "Loaderlar", "Lastikli yükleyiciler, her ölçekte yükleme işi için.",
     "Lastikli yükleyiciler (loader), malzeme yükleme, taşıma ve istifleme operasyonlarında saha verimliliğini artırır. GND İş Makineleri, farklı kapasite ve marka seçenekleriyle sıfır ve 2. el loader tedariki sağlar.", "loader"),
    ("bekoloader", "Bekoloaderler", "Kazı ve yükleme işini tek makinede birleştiren bekoloaderler.",
     "Bekoloaderler, kazı ve yükleme fonksiyonlarını tek bir makinede birleştirerek küçük ve orta ölçekli şantiyelerde çok yönlü kullanım sağlar. İhtiyacınıza uygun bekoloader modelini üretici ağımızdan bulup teklif hazırlıyoruz.", "backhoe-loader"),
    ("manlift", "Manliftler", "Yüksekte çalışma platformları, bakım ve montaj işleri için.",
     "Manliftler (yüksekte çalışma platformları), bakım, montaj, elektrik ve boya işlerinde güvenli ve verimli erişim sağlar. GND İş Makineleri olarak makaslı ve eklemli manlift seçenekleri için teklif sunuyoruz.", "manlift"),
    ("telehandler", "Telehandlerlar", "Teleskopik kollu yükleyiciler, yüksek ve uzak noktalara taşıma için.",
     "Telehandlerlar, teleskopik kolları sayesinde yüksek ve uzak noktalara malzeme taşımada esneklik sağlar; inşaat, tarım ve depo operasyonlarında tercih edilir. Sıfır ve 2. el telehandler tedariki için bize ulaşın.", "telehandler"),
    ("silindir", "Silindirler", "Zemin ve asfalt sıkıştırma işleri için silindirler.",
     "Silindirler, yol yapımı, zemin ve asfalt sıkıştırma işlerinde vazgeçilmez makinelerdir. GND İş Makineleri, tek ve çift tamburlu silindir seçenekleriyle projelerinize uygun tedarik sağlar.", "roller"),
    ("finiser", "Finişerler", "Asfalt serimi için finişer makineleri.",
     "Finişerler, asfalt serim kalitesini ve hızını doğrudan etkileyen kritik yol yapım makineleridir. Üretici ağımız üzerinden sıfır ve 2. el finişer tedariki konusunda size destek oluyoruz.", "finisher"),
    ("greyder", "Greyderler", "Zemin tesviyesi ve yol yapımı için greyderler.",
     "Greyderler, zemin tesviyesi, yol yapımı ve bakımında hassas düzeltme sağlayan makinelerdir. GND İş Makineleri, greyder tedarikinde global üretici ağımızla rekabetçi teklifler sunar.", "grader"),
    ("dozer", "Dozerler", "Ağır zemin çalışmaları için güçlü dozer seçenekleri.",
     "Dozerler, ağır zemin itme, tesviye ve hafriyat hazırlığı işlerinde yüksek güç ve verim sağlar. Sıfır ve 2. el dozer seçenekleri için GND İş Makineleri'nden teklif alabilirsiniz.", "dozer"),
    ("skid-steer-loader", "Skid Steer Loaderlar", "Dar alanlarda manevra kabiliyeti yüksek kompakt yükleyiciler.",
     "Skid steer loaderlar, dar ve engebeli alanlarda yüksek manevra kabiliyeti sunan kompakt yükleyicilerdir; peyzaj, iç mekan ve küçük şantiye işlerinde tercih edilir. Uygun modeli sizin için buluyoruz.", "skid-steer"),
]

SPARE_PARTS = [
    ("filtre-gruplari", "Filtre Grupları", "Yağ, yakıt, hava ve hidrolik filtreleri.",
     "İş makinelerinizin performansını korumak için yağ, yakıt, hava ve hidrolik filtre gruplarını orijinal ve muadil seçeneklerle tedarik ediyoruz.", "filter"),
    ("mekanik-gruplar", "Mekanik Gruplar", "Motor ve şanzıman gibi mekanik parça grupları.",
     "Motor, şanzıman ve diğer mekanik parça gruplarında güvenilir tedarik ve teknik destek sağlıyoruz.", "mechanical"),
    ("hidrolik-gruplar", "Hidrolik Gruplar", "Hidrolik pompa, silindir ve valf grupları.",
     "Hidrolik pompa, silindir ve valf grupları başta olmak üzere iş makinesi hidrolik sistem parçalarını tedarik ediyoruz.", "hydraulic"),
    ("atasmanlar", "Ataşmanlar", "Kova, kırıcı ve diğer ekipman ataşmanları.",
     "Kova, kırıcı ve makinenize özel diğer ekipman ataşmanlarını ihtiyacınıza göre tedarik ediyoruz.", "attachment"),
]

HEADER = """<header class="site-header">
  <div class="header-inner">
    <a href="{root}index.html" class="logo"><img src="{root}assets/logo-original.png" alt="GND İş Makineleri" /></a>
    <nav class="main-nav">
      <a href="{root}index.html#home">Ana Sayfa</a>
      <a href="{root}index.html#categories">Makineler</a>
      <a href="{root}index.html#spareparts">Yedek Parça</a>
      <a href="{root}index.html#about">Hakkımızda</a>
      <a href="{root}index.html#contact">İletişim</a>
    </nav>
    <div class="header-actions">
      <a class="btn btn-primary header-cta" href="https://wa.me/{wa}?text={wa_generic}" target="_blank" rel="noopener">
        <span>Teklif Al</span>
      </a>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="section-inner footer-inner">
    <div>© 2026 GND İş Makineleri</div>
    <div class="footer-note">GND İş Makineleri Sanayi ve Ticaret A.Ş.</div>
  </div>
</footer>

<a href="https://wa.me/{wa}?text={wa_generic}" class="floating-whatsapp" target="_blank" rel="noopener" aria-label="WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.5A10 10 0 1 0 12 2zm0 18.2a8.15 8.15 0 0 1-4.2-1.15l-.3-.18-3.1.95.95-3-.2-.32A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.25-.13-1.45-.72-1.68-.8-.22-.08-.39-.13-.55.13-.16.25-.63.8-.78.97-.14.16-.28.18-.53.06-.25-.13-1.06-.39-2.02-1.25-.75-.67-1.25-1.5-1.4-1.75-.14-.25-.02-.39.11-.51.11-.11.25-.28.37-.42.13-.14.17-.25.25-.4.08-.16.04-.3-.02-.42-.06-.13-.55-1.34-.76-1.83-.2-.48-.4-.42-.55-.42h-.47c-.16 0-.42.06-.64.3-.22.25-.85.83-.85 2.03s.87 2.36 1 2.52c.12.16 1.7 2.6 4.13 3.64.58.25 1.03.4 1.38.5.58.19 1.11.16 1.53.1.47-.07 1.45-.6 1.65-1.17.2-.58.2-1.07.14-1.17-.06-.1-.22-.16-.47-.28z"/></svg>
  <span>Canlı Destek</span>
</a>"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} | {site_name}</title>
<meta name="description" content="{long_desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="{root}css/style.css">
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <div class="category-detail-icon">{icon}</div>
    <h1>{name}</h1>
    <p>{long_desc}</p>
    <a href="https://wa.me/{wa}?text={wa_quote}" class="btn btn-primary btn-lg" target="_blank" rel="noopener">Teklif Al →</a>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <h2>Diğer {group_title}</h2>
    <div class="category-grid">
      {siblings}
    </div>
    <p style="margin-top:28px"><a href="{root}index.html">← Ana sayfaya dön</a></p>
  </div>
</section>

{footer}

</body>
</html>
"""

SIBLING_CARD = """<div class="category-card">
        <div class="category-icon">{icon}</div>
        <h3><a href="{href}">{name}</a></h3>
        <p>{desc}</p>
      </div>"""


def wa_link_text(text):
    from urllib.parse import quote
    return quote(text)


def build_pages(items, out_dir, group_title, url_prefix):
    os.makedirs(out_dir, exist_ok=True)
    root = "../"
    wa_generic = wa_link_text("Merhaba, GND İş Makineleri hakkında bilgi almak istiyorum.")
    header = HEADER.format(root=root, wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)

    for slug, name, short_desc, long_desc, icon_key in items:
        siblings_html = "\n      ".join(
            SIBLING_CARD.format(icon=ICONS[k], href=f"{s}.html", name=n, desc=d)
            for s, n, d, _, k in items if s != slug
        )
        wa_quote = wa_link_text(f"Merhaba, {name} için teklif almak istiyorum.")
        page = PAGE_TEMPLATE.format(
            name=name, site_name=SITE_NAME, long_desc=long_desc,
            canonical=f"{BASE_URL}/{url_prefix}/{slug}.html",
            root=root, header=header, icon=ICONS[icon_key],
            wa=WHATSAPP_NUMBER, wa_quote=wa_quote,
            group_title=group_title, siblings=siblings_html, footer=footer
        )
        with open(os.path.join(out_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  wrote {out_dir}/{slug}.html")


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))
    print("Makine sayfaları:")
    build_pages(MACHINES, os.path.join(root_dir, "makineler"), "Makineler", "makineler")
    print("Yedek parça sayfaları:")
    build_pages(SPARE_PARTS, os.path.join(root_dir, "yedek-parca"), "Yedek Parça Kategorileri", "yedek-parca")
    print("Tamamlandı.")
