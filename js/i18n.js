const WHATSAPP_NUMBER = "905550708034";

const TRANSLATIONS = {
  tr: {
    nav_home: "Ana Sayfa",
    nav_categories: "Makineler",
    nav_spareparts: "Yedek Parça",
    nav_about: "Hakkımızda",
    nav_contact: "İletişim",
    get_quote: "Teklif Al",
    live_support: "Canlı Destek",
    hero_title: "Ağır İş Makinesi Dünyasında Güvenilir Ortağınız",
    hero_subtitle: "Hafriyat, madencilik ve inşaat sektörü için geniş makine kategorileri. İhtiyacınızı söyleyin, size özel teklifi WhatsApp üzerinden anında iletelim.",
    hero_cta: "Makineleri İncele",
    categories_title: "Makine Kategorilerimiz",
    categories_subtitle: "Her kategori için detaylı teklif almak üzere doğrudan WhatsApp üzerinden bize ulaşın.",
    condition_new: "Sıfır",
    condition_used: "2. El",
    spareparts_title: "Yedek Parça",
    spareparts_subtitle: "Filtre, mekanik, hidrolik grupları ve ataşmanlar için bize ulaşın.",
    about_title: "Hakkımızda",
    about_p1: "GND İş Makineleri olarak, hafriyat ve madencilik sektörüne global ölçekte ağır iş makinesi tedariki, kiralama ve satış sonrası destek sunuyoruz.",
    about_p2: "Geniş üretici ağımız sayesinde ihtiyacınıza en uygun makineyi bulup, rekabetçi bir teklifle sizinle buluşturuyoruz.",
    stat_categories: "Makine Kategorisi",
    stat_reach: "Tedarik Ağı",
    stat_support: "WhatsApp Destek",
    vision_title: "Vizyonumuz",
    vision_text: "Ağır iş makineleri sektöründe, güvenilirlik ve global erişimi bir araya getiren öncü bir tedarik markası olmak.",
    mission_title: "Misyonumuz",
    mission_text: "Müşterilerimizin ihtiyacını doğru anlayıp, geniş üretici ağımızla en uygun makine ve yedek parça çözümünü hızlı ve şeffaf şekilde sunmak.",
    history_title: "Yolculuğumuz",
    history_subtitle: "Kuruluşumuzdan bugüne büyüme hikayemiz.",
    history_step1_title: "Kuruluş",
    history_step1_text: "GND İş Makineleri'nin temelleri atıldı.",
    history_step2_title: "Büyüme",
    history_step2_text: "Üretici ağımızı ve makine kategorilerimizi genişlettik.",
    history_step3_title: "Bugün",
    history_step3_text: "Global ölçekte hafriyat ve madencilik sektörüne hizmet veriyoruz.",
    category_search_placeholder: "Kategori ara...",
    category_no_results: "Aramanızla eşleşen kategori bulunamadı.",
    contact_title: "Bize Ulaşın",
    contact_subtitle: "İhtiyacınızı iletin, size en kısa sürede dönüş yapalım.",
    contact_cta: "WhatsApp'tan Teklif Al",
    footer_note: "Bu site içeriği yer tutucu görsellerle hazırlanmıştır.",
    quote_intro: "Merhaba, ",
    quote_middle: " için teklif almak istiyorum.",
    quote_generic: "Merhaba, GND İş Makineleri hakkında bilgi almak istiyorum."
  },
  en: {
    nav_home: "Home",
    nav_categories: "Machines",
    nav_spareparts: "Spare Parts",
    nav_about: "About Us",
    nav_contact: "Contact",
    get_quote: "Get a Quote",
    live_support: "Live Support",
    hero_title: "Your Trusted Partner in Heavy Equipment",
    hero_subtitle: "Wide range of machine categories for earthmoving, mining and construction. Tell us what you need, we'll send your custom quote straight to WhatsApp.",
    hero_cta: "Browse Machines",
    categories_title: "Our Machine Categories",
    categories_subtitle: "Reach us directly on WhatsApp for a detailed quote on any category.",
    condition_new: "New",
    condition_used: "Used",
    spareparts_title: "Spare Parts",
    spareparts_subtitle: "Reach out for filters, mechanical, hydraulic groups and attachments.",
    about_title: "About Us",
    about_p1: "GND İş Makineleri supplies, rents, and supports heavy equipment for the earthmoving and mining sector on a global scale.",
    about_p2: "Through our wide manufacturer network, we match you with the right machine and a competitive offer.",
    stat_categories: "Machine Categories",
    stat_reach: "Supply Network",
    stat_support: "WhatsApp Support",
    vision_title: "Our Vision",
    vision_text: "To be a leading supply brand in the heavy equipment industry, combining reliability with global reach.",
    mission_title: "Our Mission",
    mission_text: "To understand our customers' needs precisely and deliver the right machine and spare part solution quickly and transparently through our wide manufacturer network.",
    history_title: "Our Journey",
    history_subtitle: "Our growth story from founding to today.",
    history_step1_title: "Founding",
    history_step1_text: "The foundations of GND İş Makineleri were laid.",
    history_step2_title: "Growth",
    history_step2_text: "We expanded our manufacturer network and machine categories.",
    history_step3_title: "Today",
    history_step3_text: "We serve the earthmoving and mining sector on a global scale.",
    category_search_placeholder: "Search categories...",
    category_no_results: "No categories match your search.",
    contact_title: "Get in Touch",
    contact_subtitle: "Tell us what you need and we'll get back to you shortly.",
    contact_cta: "Get a Quote on WhatsApp",
    footer_note: "This site currently uses placeholder content and images.",
    quote_intro: "Hi, I'd like a quote for ",
    quote_middle: ".",
    quote_generic: "Hi, I'd like more information about GND İş Makineleri."
  }
};

// Basit tekrar kullanılabilir ikonlar (stroke tabanlı, tek renk SVG)
const ICONS = {
  excavator: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 20h9M14 20h7M6 20V9l6-3 4 2-3 5M6 9l4 2M13 13l4 2 3-4"/><circle cx="8" cy="20" r="1.4"/><circle cx="17" cy="20" r="1.4"/></svg>`,
  loader: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 17h2l2-6h6l2 6h6M9 11V6h4l2 5"/><circle cx="7" cy="19" r="1.6"/><circle cx="18" cy="19" r="1.6"/></svg>`,
  "backhoe-loader": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 17h2l2-6h6l2 6h4M8 11V6h4l1.5 4M16 17l4-3 2 1-2 4h-4"/><circle cx="6" cy="19" r="1.5"/><circle cx="16" cy="19" r="1.5"/></svg>`,
  manlift: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 21V11l10-6v9L6 21z"/><rect x="4" y="19" width="6" height="3"/><circle cx="16" cy="21" r="1.4"/></svg>`,
  telehandler: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 20h4l14-9M20 11l1 2-3 2M6 20v-4h4v4"/><circle cx="6" cy="20" r="1.4"/><circle cx="14" cy="20" r="1.4"/></svg>`,
  roller: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="6" cy="16" r="4"/><path d="M10 16h5a3 3 0 0 0 3-3V9h-4"/></svg>`,
  finisher: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 10h13l4 4v3H3z"/><circle cx="7" cy="19" r="1.5"/><circle cx="16" cy="19" r="1.5"/></svg>`,
  grader: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 19h18M6 19l2-5h8l2 5M9 14V8l3-2 3 2v6"/></svg>`,
  dozer: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M2 19h3l2-3h9l3 3h3M6 16V9h10v7M4 19v-2h16v2"/></svg>`,
  "skid-steer": `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 18V11h9l3 3h2v4H4z"/><circle cx="7" cy="20" r="1.4"/><circle cx="16" cy="20" r="1.4"/></svg>`,
  filter: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 4h16l-4 8v6l-4 2v-8L4 4z"/></svg>`,
  mechanical: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14.7 6.3a4 4 0 0 1-5.4 5.4L4 17l3 3 5.3-5.3a4 4 0 0 1 5.4-5.4L15 12l-3-3 2.7-2.7z"/></svg>`,
  hydraulic: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="9" width="12" height="6" rx="1"/><path d="M16 11h4v2h-4M6 9V6h4v3"/></svg>`,
  attachment: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 15l5-5 3 3-5 5-3-3zM11 10l4-4 6 6-4 4M9 17l-4 4"/></svg>`
};

// Makine kategorileri — "Sıfır / 2. El" seçimi arayüzde ayrı bir anahtar (toggle) ile yönetiliyor.
const CATEGORIES = [
  {
    id: "mini-excavator",
    name: { tr: "Mini Ekskavatör", en: "Mini Excavator" },
    desc: { tr: "Dar alan ve hafif hafriyat işleri için kompakt ekskavatörler.", en: "Compact excavators for tight spaces and light earthmoving." },
    icon: ICONS.excavator
  },
  {
    id: "mid-excavator",
    name: { tr: "Orta Seviye Ekskavatör", en: "Mid-Range Excavator" },
    desc: { tr: "Genel hafriyat ve inşaat işleri için orta sınıf ekskavatörler.", en: "Mid-class excavators for general earthmoving and construction." },
    icon: ICONS.excavator
  },
  {
    id: "heavy-excavator",
    name: { tr: "Ağır Tonaj Ekskavatör", en: "Heavy-Duty Excavator" },
    desc: { tr: "Maden ve büyük ölçekli hafriyat için ağır tonajlı ekskavatörler.", en: "Heavy-tonnage excavators for mining and large-scale earthmoving." },
    icon: ICONS.excavator
  },
  {
    id: "loader",
    name: { tr: "Loaderlar", en: "Loaders" },
    desc: { tr: "Lastikli yükleyiciler, her ölçekte yükleme işi için.", en: "Wheel loaders for loading jobs of any scale." },
    icon: ICONS.loader
  },
  {
    id: "backhoe-loader",
    name: { tr: "Bekoloaderler", en: "Backhoe Loaders" },
    desc: { tr: "Kazı ve yükleme işini tek makinede birleştiren bekoloaderler.", en: "Backhoe loaders combining digging and loading in one machine." },
    icon: ICONS["backhoe-loader"]
  },
  {
    id: "manlift",
    name: { tr: "Manliftler", en: "Man Lifts" },
    desc: { tr: "Yüksekte çalışma platformları, bakım ve montaj işleri için.", en: "Aerial work platforms for maintenance and installation work." },
    icon: ICONS.manlift
  },
  {
    id: "telehandler",
    name: { tr: "Telehandlerlar", en: "Telehandlers" },
    desc: { tr: "Teleskopik kollu yükleyiciler, yüksek ve uzak noktalara taşıma için.", en: "Telescopic handlers for reaching high and far load points." },
    icon: ICONS.telehandler
  },
  {
    id: "roller",
    name: { tr: "Silindirler", en: "Rollers" },
    desc: { tr: "Zemin ve asfalt sıkıştırma işleri için silindirler.", en: "Rollers for ground and asphalt compaction." },
    icon: ICONS.roller
  },
  {
    id: "finisher",
    name: { tr: "Finişerler", en: "Asphalt Finishers" },
    desc: { tr: "Asfalt serimi için finişer makineleri.", en: "Paver finishers for asphalt laying." },
    icon: ICONS.finisher
  },
  {
    id: "grader",
    name: { tr: "Greyderler", en: "Graders" },
    desc: { tr: "Zemin tesviyesi ve yol yapımı için greyderler.", en: "Graders for ground leveling and road construction." },
    icon: ICONS.grader
  },
  {
    id: "dozer",
    name: { tr: "Dozerler", en: "Bulldozers" },
    desc: { tr: "Ağır zemin çalışmaları için güçlü dozer seçenekleri.", en: "Powerful dozers for heavy grading work." },
    icon: ICONS.dozer
  },
  {
    id: "skid-steer",
    name: { tr: "Skid Steer Loaderlar", en: "Skid Steer Loaders" },
    desc: { tr: "Dar alanlarda manevra kabiliyeti yüksek kompakt yükleyiciler.", en: "Compact loaders with high maneuverability in tight spaces." },
    icon: ICONS["skid-steer"]
  }
];

// Yedek parça kategorileri (durum/koşul ayrımı yok)
const SPARE_PARTS_CATEGORIES = [
  {
    id: "filter-groups",
    name: { tr: "Filtre Grupları", en: "Filter Groups" },
    desc: { tr: "Yağ, yakıt, hava ve hidrolik filtreleri.", en: "Oil, fuel, air and hydraulic filters." },
    icon: ICONS.filter
  },
  {
    id: "mechanical-groups",
    name: { tr: "Mekanik Gruplar", en: "Mechanical Groups" },
    desc: { tr: "Motor ve şanzıman gibi mekanik parça grupları.", en: "Mechanical part groups such as engine and transmission." },
    icon: ICONS.mechanical
  },
  {
    id: "hydraulic-groups",
    name: { tr: "Hidrolik Gruplar", en: "Hydraulic Groups" },
    desc: { tr: "Hidrolik pompa, silindir ve valf grupları.", en: "Hydraulic pump, cylinder and valve groups." },
    icon: ICONS.hydraulic
  },
  {
    id: "attachments",
    name: { tr: "Ataşmanlar", en: "Attachments" },
    desc: { tr: "Kova, kırıcı ve diğer ekipman ataşmanları.", en: "Buckets, breakers and other equipment attachments." },
    icon: ICONS.attachment
  }
];
