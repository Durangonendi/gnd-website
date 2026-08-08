# Generates English-first SEO landing pages per machine/spare-part category.
# To add/change a category: update MACHINES / SPARE_PARTS below AND the matching
# entry in js/i18n.js (CATEGORIES / SPARE_PARTS_CATEGORIES) — both keep the same data.
#
# Language handling on these pages: the server-rendered default is always English
# (SEO-safe — matches what a crawler with no localStorage sees). Visible text carries
# a `data-tr="..."` twin; js/detail-lang.js swaps to Turkish at runtime ONLY if the
# visitor already has "tr" explicitly stored in localStorage (gnd-site-lang), i.e. they
# picked it via the lang-select on this site before. First-time visitors with no stored
# preference keep seeing English, same as today.
import os

SITE_NAME = "GND Machinery"
BASE_URL = "https://gndmachinery.com"
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
    "trade": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.5 6 3.5 9s-1 6.5-3.5 9c-2.5-2.5-3.5-6-3.5-9s1-6.5 3.5-9z"/></svg>',
}

# (title, text, title_tr, text_tr)
BENEFITS = [
    ("Global manufacturer network", "Access to new and used equipment sourced from trusted producers worldwide.",
     "Küresel üretici ağı", "Dünya çapında güvenilir üreticilerden sıfır ve ikinci el ekipmana erişim."),
    ("New and used options", "Flexible sourcing matched to your budget, timeline, and specification.",
     "Sıfır ve ikinci el seçenekler", "Bütçenize, zaman çizelgenize ve spesifikasyonunuza uygun esnek tedarik."),
    ("Fast quotation", "Get pricing and availability directly on WhatsApp, without a sign-up form.",
     "Hızlı teklif", "Kayıt formu olmadan doğrudan WhatsApp üzerinden fiyat ve stok bilgisi alın."),
    ("Genuine parts support", "Backed by our own spare parts and after-sales network.",
     "Orijinal parça desteği", "Kendi yedek parça ve satış sonrası ağımızla desteklenir."),
]

MACHINE_LINKS = [("filters", "Filters", "Filtreler"), ("hydraulic-parts", "Hydraulic Parts", "Hidrolik Gruplar"), ("attachments", "Attachments", "Ataşmanlar")]
PARTS_LINKS = [("excavator", "Excavators", "Ekskavatörler"), ("wheel-loader", "Wheel Loaders", "Loaderlar"), ("bulldozer", "Bulldozers", "Dozerler")]
SERVICE_LINKS = [("excavator", "Excavators", "Ekskavatörler"), ("wheel-loader", "Wheel Loaders", "Loaderlar"), ("attachments", "Attachments", "Ataşmanlar")]


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;")


# (slug, name, meta description, intro, icon key, image filename, specs, tr)
# specs = (typical_spec_range, common_applications)
# tr = (name_tr, intro_tr, (spec_range_tr, applications_tr), desc_tr)
MACHINES = [
    ("mini-excavator", "Mini Excavators",
     "New and used mini excavators for sale from GND Machinery. Global supplier of compact excavators for construction, landscaping and utility work.",
     "Mini excavators combine compact size with genuine digging power, making them the preferred choice for landscaping, utility work, demolition in tight spaces and urban construction sites. GND Machinery sources new and used mini excavators from a wide international manufacturer network, matching each buyer with the right size, reach and operating weight for their project.",
     "excavator", "mini-ekskavator.jpg",
     ("Operating weight 0.8–6 t &middot; Engine power 10–50 HP",
      "Landscaping, utility trenching, small demolition, indoor and basement work, tight urban sites"),
     ("Mini Ekskavatörler",
      "Mini ekskavatörler, kompakt boyutları ile gerçek kazı gücünü bir araya getirir; peyzaj işleri, altyapı çalışmaları, dar alanlarda yıkım ve şehir içi inşaat sahaları için tercih edilir. GND Machinery, geniş uluslararası üretici ağı üzerinden sıfır ve ikinci el mini ekskavatör tedarik ederek her alıcıyı projesine uygun boyut, erişim mesafesi ve çalışma ağırlığıyla eşleştirir.",
      ("Çalışma ağırlığı 0,8–6 ton · Motor gücü 10–50 HP",
       "Peyzaj işleri, altyapı hendek kazısı, küçük ölçekli yıkım, bodrum ve iç mekan çalışmaları, dar şehir içi sahalar"),
      "Dar alan ve hafif hafriyat işleri için kompakt ekskavatörler.")),
    ("excavator", "Excavators",
     "Buy new or used excavators from GND Machinery, a global heavy equipment supplier. Crawler excavators for construction, earthmoving and infrastructure projects.",
     "Excavators are the backbone of any earthmoving operation, and GND Machinery supplies mid-size crawler excavators for construction, road building and general earthmoving work. Through our global manufacturer network, we source both new and used excavators matched to your tonnage, reach and site requirements.",
     "excavator", "orta-ekskavator.jpg",
     ("Operating weight 13–25 t &middot; Engine power 90–150 HP",
      "General earthmoving, foundation work, road construction, utility installation"),
     ("Ekskavatörler",
      "Ekskavatörler her hafriyat operasyonunun temelini oluşturur; GND Machinery inşaat, yol yapımı ve genel hafriyat işleri için orta sınıf paletli ekskavatörler tedarik eder. Küresel üretici ağımız sayesinde tonaj, erişim mesafesi ve saha gereksinimlerinize uygun sıfır ve ikinci el ekskavatörler buluyoruz.",
      ("Çalışma ağırlığı 13–25 ton · Motor gücü 90–150 HP",
       "Genel hafriyat, temel çalışmaları, yol yapımı, altyapı tesisatı"),
      "Genel hafriyat ve inşaat işleri için orta sınıf ekskavatörler.")),
    ("mining-excavator", "Mining & Heavy-Duty Excavators",
     "Heavy-duty and mining excavators for sale. GND Machinery supplies large-tonnage excavators for quarries, mines and large-scale earthmoving projects worldwide.",
     "Mining and heavy-duty excavators deliver the digging capacity required for quarries, open-pit mines and large-scale earthmoving projects. GND Machinery's global supply network sources new and used heavy-tonnage excavators, offering competitive quotations for buyers in the mining and quarrying sector.",
     "excavator", "agir-tonaj-ekskavator.jpg",
     ("Operating weight 30–120+ t &middot; Engine power 200–700+ HP",
      "Open-pit mining, quarrying, overburden removal, large-scale earthmoving"),
     ("Madencilik ve Ağır Tonaj Ekskavatörler",
      "Madencilik ve ağır tonaj ekskavatörler; taş ocakları, açık maden sahaları ve büyük ölçekli hafriyat projeleri için gereken kazı kapasitesini sağlar. GND Machinery'nin küresel tedarik ağı, madencilik ve taş ocağı sektöründeki alıcılar için sıfır ve ikinci el ağır tonajlı ekskavatörler bularak rekabetçi teklifler sunar.",
      ("Çalışma ağırlığı 30–120+ ton · Motor gücü 200–700+ HP",
       "Açık maden işletmeciliği, taş ocakçılığı, örtü tabakası kaldırma, büyük ölçekli hafriyat"),
      "Maden ve büyük ölçekli hafriyat için ağır tonajlı ekskavatörler.")),
    ("wheel-loader", "Wheel Loaders",
     "New and used wheel loaders for sale from GND Machinery. Global supplier of loading equipment for construction, quarrying and material handling.",
     "Wheel loaders are essential for loading, carrying and stockpiling material on any construction or quarry site. GND Machinery supplies new and used wheel loaders in a range of capacities, sourced through our international manufacturer network to match your operation's throughput needs.",
     "loader", "loader.jpg",
     ("Operating weight 5–25 t &middot; Engine power 100–300 HP",
      "Material loading, stockpiling, quarry face loading, snow removal"),
     ("Lastikli Yükleyiciler",
      "Lastikli yükleyiciler, her inşaat veya taş ocağı sahasında yükleme, taşıma ve stoklama için vazgeçilmezdir. GND Machinery, uluslararası üretici ağı üzerinden farklı kapasitelerde sıfır ve ikinci el lastikli yükleyiciler tedarik ederek operasyonunuzun verim ihtiyacına uygun çözümler sunar.",
      ("Çalışma ağırlığı 5–25 ton · Motor gücü 100–300 HP",
       "Malzeme yükleme, stoklama, taş ocağı yüzü yükleme, kar temizleme"),
      "Lastikli yükleyiciler, her ölçekte yükleme işi için.")),
    ("backhoe-loader", "Backhoe Loaders",
     "Backhoe loaders for sale, new and used. GND Machinery supplies versatile backhoe loaders combining excavation and loading in a single machine.",
     "Backhoe loaders combine excavation and loading in a single versatile machine, ideal for small to mid-size construction sites. GND Machinery sources new and used backhoe loaders from trusted manufacturers worldwide, offering flexible supply options for contractors and rental fleets.",
     "backhoe-loader", "bekoloader.jpg",
     ("Operating weight 7–9 t &middot; Engine power 80–110 HP",
      "Small-to-mid excavation, utility work, municipal projects, material handling"),
     ("Bekoloaderler",
      "Bekoloaderler, kazı ve yükleme işlevlerini tek bir çok yönlü makinede birleştirir; küçük ve orta ölçekli inşaat sahaları için idealdir. GND Machinery, dünya çapında güvenilir üreticilerden sıfır ve ikinci el bekoloaderler tedarik ederek yükleniciler ve kiralama filoları için esnek tedarik seçenekleri sunar.",
      ("Çalışma ağırlığı 7–9 ton · Motor gücü 80–110 HP",
       "Küçük ve orta ölçekli kazı, altyapı işleri, belediye projeleri, malzeme taşıma"),
      "Kazı ve yükleme işini tek makinede birleştiren bekoloaderler.")),
    ("boom-lift", "Boom Lifts & Man Lifts",
     "Boom lifts and man lifts for sale. GND Machinery supplies aerial work platforms for maintenance, installation and construction access work.",
     "Boom lifts and man lifts provide safe, efficient access for maintenance, installation and construction work at height. GND Machinery supplies articulating and telescopic boom lifts through its global equipment network, sourced new or used to fit your project's reach and budget.",
     "manlift", "manlift.jpg",
     ("Working height 12–45 m",
      "Maintenance, installation, facade work, warehouse and steel-structure access"),
     ("Platform ve Manliftler",
      "Platform ve manliftler, yükseklikte yapılan bakım, montaj ve inşaat çalışmaları için güvenli ve verimli erişim sağlar. GND Machinery, küresel ekipman ağı üzerinden eklemli ve teleskopik platformları sıfır veya ikinci el olarak, projenizin erişim mesafesine ve bütçesine uygun şekilde tedarik eder.",
      ("Çalışma yüksekliği 12–45 m",
       "Bakım, montaj, cephe çalışmaları, depo ve çelik yapı erişimi"),
      "Yüksekte çalışma platformları, bakım ve montaj işleri için.")),
    ("telehandler", "Telehandlers",
     "Telehandlers for sale, new and used telescopic handlers from GND Machinery, a global heavy equipment supplier for construction and agriculture.",
     "Telehandlers extend the reach of a standard forklift, moving materials to high and hard-to-reach points on construction sites, warehouses and farms. GND Machinery supplies new and used telehandlers sourced through its international manufacturer network.",
     "telehandler", "telehandler.jpg",
     ("Lift height 6–17 m &middot; Lift capacity 2.5–5 t",
      "Construction material handling, agriculture, warehouse logistics"),
     ("Telehandlerlar",
      "Telehandlerlar, standart bir forkliftin erişim mesafesini uzatarak inşaat sahalarında, depolarda ve tarım alanlarında malzemeyi yüksek ve zor ulaşılan noktalara taşır. GND Machinery, uluslararası üretici ağı üzerinden sıfır ve ikinci el telehandlerlar tedarik eder.",
      ("Kaldırma yüksekliği 6–17 m · Kaldırma kapasitesi 2,5–5 ton",
       "İnşaat malzeme taşıma, tarım, depo lojistiği"),
      "Teleskopik kollu yükleyiciler, yüksek ve uzak noktalara taşıma için.")),
    ("road-roller", "Road Rollers & Compactors",
     "Road rollers and compactors for sale. GND Machinery supplies single and double-drum rollers for road construction and ground compaction projects.",
     "Road rollers and compactors are essential for road construction, ground preparation and asphalt compaction. GND Machinery supplies single and double-drum rollers, sourced new or used to match the compaction requirements of your project.",
     "roller", "silindir.jpg",
     ("Operating weight 1–20 t",
      "Subgrade compaction, asphalt finishing, trench and ground compaction"),
     ("Silindirler ve Kompaktörler",
      "Silindirler ve kompaktörler; yol yapımı, zemin hazırlığı ve asfalt sıkıştırma çalışmaları için vazgeçilmezdir. GND Machinery, projenizin sıkıştırma gereksinimlerine uygun tek ve çift tamburlu silindirleri sıfır veya ikinci el olarak tedarik eder.",
      ("Çalışma ağırlığı 1–20 ton",
       "Zemin sıkıştırma, asfalt serme sonrası sıkıştırma, hendek ve zemin sıkıştırma"),
      "Zemin ve asfalt sıkıştırma işleri için silindirler.")),
    ("asphalt-paver", "Asphalt Pavers (Finishers)",
     "Asphalt pavers and finishers for sale from GND Machinery, a global supplier of road construction equipment for paving contractors.",
     "Asphalt pavers, also known as finishers, determine the speed and quality of any road paving project. GND Machinery supplies new and used asphalt pavers through its global manufacturer network, matched to your paving width and output requirements.",
     "finisher", "finiser.jpg",
     ("Paving width 2–10 m &middot; Engine power 60–130 HP",
      "Road paving, parking lots, airport runways"),
     ("Asfalt Finişerleri",
      "Finişer olarak da bilinen asfalt serici makineler, herhangi bir yol yapım projesinin hızını ve kalitesini belirler. GND Machinery, küresel üretici ağı üzerinden serim genişliği ve kapasite gereksinimlerinize uygun sıfır ve ikinci el asfalt finişerleri tedarik eder.",
      ("Serim genişliği 2–10 m · Motor gücü 60–130 HP",
       "Yol serimi, otopark yapımı, havalimanı pisti çalışmaları"),
      "Asfalt serimi için finişer makineleri.")),
    ("motor-grader", "Motor Graders",
     "Motor graders for sale, new and used grading equipment from GND Machinery, a global supplier for road construction and site leveling.",
     "Motor graders deliver the precision grading needed for road construction, site leveling and maintenance work. GND Machinery sources new and used motor graders from a global manufacturer network, supporting contractors and infrastructure projects worldwide.",
     "grader", "greyder.jpg",
     ("Engine power 100–280 HP &middot; Blade width 3–4.3 m",
      "Road grading, site leveling, slope and maintenance work"),
     ("Greyderler",
      "Greyderler, yol yapımı, saha tesviyesi ve bakım çalışmaları için gereken hassas tesviyeyi sağlar. GND Machinery, dünya çapındaki yükleniciler ve altyapı projeleri için küresel üretici ağından sıfır ve ikinci el greyderler tedarik eder.",
      ("Motor gücü 100–280 HP · Bıçak genişliği 3–4,3 m",
       "Yol tesviyesi, saha düzleştirme, eğim ve bakım çalışmaları"),
      "Zemin tesviyesi ve yol yapımı için greyderler.")),
    ("bulldozer", "Bulldozers",
     "Bulldozers for sale, new and used dozers from GND Machinery, a global heavy equipment supplier for earthmoving and site preparation.",
     "Bulldozers provide the pushing power needed for site preparation, grading and heavy earthmoving work. GND Machinery supplies new and used bulldozers sourced through its international manufacturer network, matched to your project's horsepower and blade requirements.",
     "dozer", "dozer.jpg",
     ("Engine power 70–450+ HP",
      "Site clearing, grading, material pushing, rough terrain leveling"),
     ("Dozerler",
      "Dozerler, saha hazırlığı, tesviye ve ağır hafriyat çalışmaları için gereken itme gücünü sağlar. GND Machinery, projenizin beygir gücü ve bıçak gereksinimlerine uygun sıfır ve ikinci el dozerleri uluslararası üretici ağı üzerinden tedarik eder.",
      ("Motor gücü 70–450+ HP",
       "Saha temizleme, tesviye, malzeme itme, arazi düzleştirme"),
      "Ağır zemin çalışmaları için güçlü dozer seçenekleri.")),
    ("skid-steer-loader", "Skid Steer Loaders",
     "Skid steer loaders for sale, compact and versatile loaders from GND Machinery, a global supplier for landscaping, demolition and tight-access sites.",
     "Skid steer loaders bring compact power and tight-radius maneuverability to landscaping, demolition and confined job sites. GND Machinery supplies new and used skid steer loaders through its global equipment network, matched to your attachment and lift capacity needs.",
     "skid-steer", "skid-steer-loader.jpg",
     ("Operating weight 1.4–3.5 t &middot; Engine power 45–100 HP",
      "Landscaping, demolition, tight-access material handling"),
     ("Skid Steer Loaderlar",
      "Skid steer loaderlar, peyzaj işleri, yıkım ve dar alanlı iş sahalarına kompakt güç ve dar dönüş yarıçapıyla manevra kabiliyeti kazandırır. GND Machinery, ataşman ve kaldırma kapasitesi ihtiyacınıza uygun sıfır ve ikinci el skid steer loaderları küresel ekipman ağı üzerinden tedarik eder.",
      ("Çalışma ağırlığı 1,4–3,5 ton · Motor gücü 45–100 HP",
       "Peyzaj işleri, yıkım, dar alanda malzeme taşıma"),
      "Dar alanlarda manevra kabiliyeti yüksek kompakt yükleyiciler.")),
]

# (slug, name, meta description, intro, icon key, image filename, sourcing, tr)
# sourcing = (domestic_text, imported_text, oem_text)
# tr = (name_tr, intro_tr, (domestic_tr, imported_tr, oem_tr), desc_tr)
SPARE_PARTS = [
    ("filters", "Heavy Equipment Filters",
     "OEM and aftermarket filters for heavy equipment. GND Machinery supplies oil, fuel, air and hydraulic filters for construction and mining machinery.",
     "Genuine and aftermarket filtration keeps heavy equipment running at peak performance. GND Machinery supplies oil, fuel, air, hydraulic and cabin filters for excavators, loaders and other construction and mining machinery.",
     "filter", "filtre-gruplari.jpg",
     ("Locally manufactured filters offering fast delivery and lower cost for routine maintenance.",
      "Internationally sourced filters from established brands for buyers with a preferred standard.",
      "Original equipment manufacturer filters matched exactly to your machine's model, for warranty-sensitive use."),
     ("Filtre Grupları",
      "Orijinal ve muadil filtrasyon çözümleri, ağır iş makinelerinin en yüksek performansta çalışmasını sağlar. GND Machinery, ekskavatör, yükleyici ve diğer inşaat/madencilik makineleri için yağ, yakıt, hava, hidrolik ve kabin filtreleri tedarik eder.",
      ("Rutin bakım için hızlı teslimat ve düşük maliyet sunan yerli üretim filtreler.",
       "Belirli bir standardı tercih eden alıcılar için köklü markalardan ithal edilen filtreler.",
       "Garanti kapsamındaki kullanım için makinenizin modeliyle birebir uyumlu orijinal ekipman üreticisi (OEM) filtreleri."),
      "Yağ, yakıt, hava ve hidrolik filtreleri.")),
    ("mechanical-parts", "Mechanical Parts & Components",
     "Mechanical parts for heavy equipment: engines, transmissions, undercarriage and drive components supplied globally by GND Machinery.",
     "From engine and transmission components to undercarriage and drive axle groups, GND Machinery supplies mechanical parts for heavy equipment, backed by a global sourcing network and technical support.",
     "mechanical", "mekanik-gruplar.jpg",
     ("Locally produced components for common wear items such as seals, gaskets and basic mechanical parts.",
      "Internationally sourced mechanical components for models without a ready local equivalent.",
      "Manufacturer-original parts for engine, transmission and drivetrain components requiring exact specification."),
     ("Mekanik Parçalar ve Bileşenler",
      "Motor ve şanzıman bileşenlerinden şasi altı ve tahrik grubu parçalarına kadar, GND Machinery ağır iş makineleri için mekanik parçaları küresel bir tedarik ağı ve teknik destekle sunar.",
      ("Conta, keçe ve temel mekanik parçalar gibi yaygın aşınan bileşenler için yerli üretim seçenekler.",
       "Yerli muadili bulunmayan modeller için uluslararası kaynaklardan tedarik edilen mekanik bileşenler.",
       "Tam spesifikasyon gerektiren motor, şanzıman ve tahrik grubu bileşenleri için üretici orijinali parçalar."),
      "Motor ve şanzıman gibi mekanik parça grupları.")),
    ("hydraulic-parts", "Hydraulic Parts & Components",
     "Hydraulic parts for heavy equipment: pumps, valves, cylinders and motors supplied globally by GND Machinery for construction and mining machinery.",
     "Hydraulic pumps, control valves, cylinders and motors are critical to the performance of any heavy equipment fleet. GND Machinery supplies hydraulic components for excavators, loaders and other construction machinery through its global parts network.",
     "hydraulic", "hidrolik-gruplar.jpg",
     ("Locally manufactured hydraulic components for standard repair and maintenance needs.",
      "Internationally sourced hydraulic pumps, valves and cylinders across a wider brand and model range.",
      "Manufacturer-original hydraulic components for precision-critical applications."),
     ("Hidrolik Parçalar ve Bileşenler",
      "Hidrolik pompalar, kontrol valfleri, silindirler ve motorlar, herhangi bir ağır iş makinesi filosunun performansı için kritik öneme sahiptir. GND Machinery, ekskavatör, yükleyici ve diğer inşaat makineleri için hidrolik bileşenleri küresel parça ağı üzerinden tedarik eder.",
      ("Standart onarım ve bakım ihtiyaçları için yerli üretim hidrolik bileşenler.",
       "Daha geniş marka ve model yelpazesi için uluslararası kaynaklardan tedarik edilen hidrolik pompa, valf ve silindirler.",
       "Hassasiyet gerektiren uygulamalar için üretici orijinali hidrolik bileşenler."),
      "Hidrolik pompa, silindir ve valf grupları.")),
    ("attachments", "Attachments & Implements",
     "Heavy equipment attachments for sale: buckets, breakers, grapples and implements supplied globally by GND Machinery.",
     "The right attachment turns a single machine into a multi-purpose tool. GND Machinery supplies buckets, hydraulic breakers, grapples and other attachments for excavators, loaders and skid steers worldwide.",
     "attachment", "atasmanlar.jpg",
     ("Locally manufactured buckets and general attachments, a cost-effective choice for standard jobs.",
      "Internationally sourced specialty attachments such as grapples and breakers for specific working conditions.",
      "Manufacturer-original attachments engineered for exact compatibility with your machine."),
     ("Ataşmanlar ve Ekipmanlar",
      "Doğru ataşman, tek bir makineyi çok amaçlı bir araca dönüştürür. GND Machinery, dünya çapında ekskavatör, yükleyici ve skid steer loaderlar için kova, hidrolik kırıcı, grapple ve diğer ataşmanları tedarik eder.",
      ("Standart işler için maliyet avantajlı, yerli üretim kova ve genel ataşmanlar.",
       "Özel çalışma koşulları için grapple ve kırıcı gibi uluslararası kaynaklı özel ataşmanlar.",
       "Makinenizle tam uyumluluk için mühendislik detayına uygun üretici orijinali ataşmanlar."),
      "Kova, kırıcı ve diğer ekipman ataşmanları.")),
]

# (slug, name, meta description, intro, icon key, image filename, help_areas, tr)
# help_areas = (sourcing_text, customs_text, logistics_text)
# tr = (name_tr, intro_tr, (sourcing_tr, customs_tr, logistics_tr), desc_tr)
SERVICES = [
    ("import-export-consultancy", "Import & Export Consultancy",
     "Heavy equipment import and export consultancy from GND Machinery — reference-backed sourcing, customs guidance and logistics support for international buyers and sellers.",
     "Buying or selling heavy equipment across borders involves sourcing verification, customs documentation, logistics and market knowledge that most buyers don't have in-house. GND Machinery draws on its own international trade network and track record to guide clients through the import and export process, from finding a reliable counterpart to coordinating shipment.",
     "trade", None,
     ("Connecting buyers and sellers with vetted counterparts through our reference network, built on real transaction history rather than cold listings.",
      "General guidance on the customs documentation and process involved in cross-border equipment transactions — not a substitute for formal customs/legal advice.",
      "Coordinating freight and logistics for cross-border heavy equipment shipments, from origin to destination."),
     ("İthalat & İhracat Danışmanlığı",
      "Ağır iş makinesi alım satımında sınır ötesi işlemler; tedarik doğrulaması, gümrük evrakları, lojistik ve çoğu alıcının kurum içinde sahip olmadığı bir pazar bilgisi gerektirir. GND Machinery, kendi uluslararası ticaret ağını ve geçmiş iş tecrübesini kullanarak müşterilerine güvenilir bir muhatap bulmaktan sevkiyatın koordinasyonuna kadar ithalat ve ihracat sürecinde rehberlik eder.",
      ("Soğuk ilanlar yerine gerçek işlem geçmişine dayanan referans ağımız üzerinden alıcı ve satıcıları doğrulanmış muhataplarla buluşturuyoruz.",
       "Sınır ötesi makine işlemlerinde gerekli gümrük evrakları ve süreci hakkında genel yönlendirme — resmi gümrük/hukuk danışmanlığının yerini tutmaz.",
       "Sınır ötesi ağır iş makinesi sevkiyatları için çıkış noktasından varış noktasına kadar navlun ve lojistik koordinasyonu."),
      "Referans temelli tedarik, gümrük rehberliği ve lojistik desteği.")),
]

# (slug, name, name_tr, meta_desc, meta_desc_tr, intro, intro_tr, calc_type, form_html, approximate)
# form_html: the literal <div class="calc-field">...</div> block(s) for this calculator's inputs.
# approximate: True if results use general industry averages rather than exact geometry (shows an extra disclaimer).
CALCULATORS = [
    ("hafriyat-dolgu-hesaplama", "Excavation &amp; Fill Volume Calculator", "Hafriyat / Dolgu Hesaplama",
     "Free excavation and fill volume calculator for construction projects. Enter length, width and depth to get bank and loose (swelled) volume in cubic meters.",
     "Hafriyat ve dolgu hacmi hesaplama aracı. Uzunluk, genişlik ve derinlik girin; yerinde ve gevşeme sonrası (kazılmış) hacmi m³ olarak görün.",
     "Enter your excavation dimensions to calculate the in-place (bank) volume and the loose volume after excavation, accounting for soil swell.",
     "Kazı ölçülerinizi girin, yerinde (bank) hacmi ve zeminin gevşeme payı ile kazıldıktan sonraki hacmi hesaplayın.",
     "hafriyat",
     """<div class="calc-field"><label data-tr="Uzunluk (m)">Length (m)</label><input type="number" id="uzunluk" value="10" min="0" step="0.1"></div>
      <div class="calc-field"><label data-tr="Genişlik (m)">Width (m)</label><input type="number" id="genislik" value="5" min="0" step="0.1"></div>
      <div class="calc-field"><label data-tr="Derinlik (m)">Depth (m)</label><input type="number" id="derinlik" value="1.5" min="0" step="0.1"></div>
      <div class="calc-field"><label data-tr="Şişme Faktörü (%)">Swell Factor (%)</label><input type="number" id="sisme" value="25" min="0" step="1"></div>""",
     False),
    ("beton-hesaplama", "Concrete Volume Calculator", "Beton Hesaplama",
     "Free concrete volume calculator. Enter length, width and thickness to get the required concrete volume in cubic meters, with a waste margin included.",
     "Beton hacmi hesaplama aracı. Uzunluk, genişlik ve kalınlık girin; gerekli beton hacmini m³ olarak, fire payıyla birlikte görün.",
     "Enter your slab or foundation dimensions to calculate how much concrete you'll need, including a standard waste margin.",
     "Döşeme veya temel ölçülerinizi girin, standart fire payı dahil ne kadar beton gerektiğini hesaplayın.",
     "beton",
     """<div class="calc-field"><label data-tr="Uzunluk (m)">Length (m)</label><input type="number" id="uzunluk" value="10" min="0" step="0.1"></div>
      <div class="calc-field"><label data-tr="Genişlik (m)">Width (m)</label><input type="number" id="genislik" value="5" min="0" step="0.1"></div>
      <div class="calc-field"><label data-tr="Kalınlık (cm)">Thickness (cm)</label><input type="number" id="kalinlik" value="15" min="0" step="1"></div>""",
     False),
    ("malzeme-tasima-hesaplama", "Material Hauling Calculator", "Malzeme Taşıma Hesaplama",
     "Free material hauling calculator. Enter total material volume and vehicle capacity to find out how many trips you'll need.",
     "Malzeme taşıma hesaplama aracı. Toplam malzeme hacmini ve araç kapasitesini girin, kaç sefer gerektiğini görün.",
     "Enter the total material volume and your vehicle's capacity to calculate the number of trips required.",
     "Toplam malzeme hacmini ve aracınızın kapasitesini girin, gereken sefer sayısını hesaplayın.",
     "tasima",
     """<div class="calc-field"><label data-tr="Toplam Malzeme Hacmi (m³)">Total Material Volume (m³)</label><input type="number" id="toplamHacim" value="50" min="0" step="0.1"></div>
      <div class="calc-field"><label data-tr="Araç Kapasitesi (m³)">Vehicle Capacity (m³)</label><input type="number" id="kapasite" value="10" min="0.1" step="0.1"></div>""",
     False),
    ("ekipman-secim-rehberi", "Equipment Selection Guide", "Ekipman Seçim Rehberi",
     "Free equipment selection guide. Answer one question about your job type to get a recommended excavator class for your project.",
     "Ekipman seçim rehberi. İşinizin türünü seçin, projeniz için önerilen ekskavatör sınıfını görün.",
     "Not sure which excavator class fits your project? Select your job type below for a general recommendation.",
     "Projeniz için hangi ekskavatör sınıfının uygun olduğundan emin değil misiniz? İş türünüzü seçin, genel bir öneri alın.",
     "ekipman",
     """<div class="calc-field"><label data-tr="İş Türü">Job Type</label>
      <select id="isTuru">
        <option value="dar" data-tr="Dar alan / peyzaj / iç mekan">Tight space / landscaping / indoor</option>
        <option value="genel" selected data-tr="Genel hafriyat / inşaat">General earthmoving / construction</option>
        <option value="buyuk" data-tr="Büyük ölçekli / maden">Large-scale / mining</option>
      </select></div>""",
     True),
    ("yakit-maliyeti-hesaplama", "Fuel Cost Calculator", "Yakıt Maliyeti Hesaplama",
     "Free fuel cost calculator for heavy equipment. Estimate fuel consumption and cost based on machine type, working hours and fuel price.",
     "Ağır iş makinesi yakıt maliyeti hesaplama aracı. Makine tipi, çalışma saati ve yakıt fiyatına göre tahmini yakıt tüketimi ve maliyeti.",
     "Estimate fuel consumption and cost using general industry averages for each machine class.",
     "Her makine sınıfı için genel sektör ortalamalarını kullanarak tahmini yakıt tüketimi ve maliyeti hesaplayın.",
     "yakit",
     """<div class="calc-field"><label data-tr="Makine Tipi">Machine Type</label>
      <select id="makineTipi">
        <option value="mini" data-tr="Mini Ekskavatör (~8 L/saat)">Mini Excavator (~8 L/hr)</option>
        <option value="orta" selected data-tr="Orta Sınıf Ekskavatör (~15 L/saat)">Mid-size Excavator (~15 L/hr)</option>
        <option value="agir" data-tr="Ağır Tonaj Ekskavatör (~25 L/saat)">Heavy-duty Excavator (~25 L/hr)</option>
      </select></div>
      <div class="calc-field"><label data-tr="Günlük Çalışma Saati">Daily Working Hours</label><input type="number" id="calismaSaati" value="8" min="0" step="0.5"></div>
      <div class="calc-field"><label data-tr="Gün Sayısı">Number of Days</label><input type="number" id="gunSayisi" value="5" min="1" step="1"></div>
      <div class="calc-field"><label data-tr="Yakıt Fiyatı (TL/litre)">Fuel Price (TRY/liter)</label><input type="number" id="yakitFiyati" value="45" min="0" step="0.5"></div>""",
     True),
    ("kazi-suresi-hesaplama", "Excavation Time Estimator", "Kazı Süresi Tahmini",
     "Free excavation time estimator. Enter total volume and machine type to estimate how many hours or days the job will take.",
     "Kazı süresi tahmin aracı. Toplam hacim ve makine tipini girin, işin kaç saat/gün süreceğini tahmin edin.",
     "Estimate how long an excavation job will take, based on total volume and general production rates per machine class.",
     "Toplam hacme ve makine sınıfına göre genel üretim hızlarını kullanarak işin ne kadar süreceğini tahmin edin.",
     "sure",
     """<div class="calc-field"><label data-tr="Toplam Hacim (m³)">Total Volume (m³)</label><input type="number" id="toplamHacim2" value="200" min="0" step="1"></div>
      <div class="calc-field"><label data-tr="Makine Tipi">Machine Type</label>
      <select id="makineTipi2">
        <option value="mini" data-tr="Mini Ekskavatör (~8 m³/saat)">Mini Excavator (~8 m³/hr)</option>
        <option value="orta" selected data-tr="Orta Sınıf Ekskavatör (~20 m³/saat)">Mid-size Excavator (~20 m³/hr)</option>
        <option value="agir" data-tr="Ağır Tonaj Ekskavatör (~40 m³/saat)">Heavy-duty Excavator (~40 m³/hr)</option>
      </select></div>""",
     True),
    ("ithalat-maliyet-hesaplama", "Import Cost Estimator", "İthalat Maliyet Hesaplayıcı",
     "Free heavy equipment import cost estimator for Turkey. Enter FOB price, freight, customs duty and VAT rate to estimate total landed cost.",
     "Ağır iş makinesi ithalat maliyeti hesaplama aracı. FOB fiyat, navlun, gümrük vergisi ve KDV oranını girin; tahmini toplam maliyeti görün.",
     "Enter your machine's FOB price and your own freight quote to estimate total landed cost in Turkish Lira. Duty rate depends on the machine's GTİP/HS code — confirm the exact rate with a customs broker before finalizing a purchase.",
     "Makinenizin FOB fiyatını ve kendi navlun teklifinizi girin, Türk Lirası cinsinden tahmini toplam maliyeti görün. Gümrük vergisi oranı makinenin GTİP koduna göre değişir — kesin oran için satın almadan önce bir gümrük müşavirine danışın.",
     "ithalat",
     """<div class="calc-field"><label data-tr="Makine Fiyatı - FOB (USD)">Machine Price - FOB (USD)</label><input type="number" id="fobFiyat" value="50000" min="0" step="100"></div>
      <div class="calc-field"><label data-tr="Navlun / Nakliye Teklifi (USD)">Freight Quote (USD)</label><input type="number" id="navlun" value="8000" min="0" step="100"></div>
      <div class="calc-field"><label data-tr="Gümrük Vergisi Oranı (%)">Customs Duty Rate (%)</label><input type="number" id="gumrukOrani" value="0" min="0" step="0.5"></div>
      <div class="calc-field"><label data-tr="KDV Oranı (%)">VAT Rate (%)</label><input type="number" id="kdvOrani" value="20" min="0" step="0.5"></div>
      <div class="calc-field"><label data-tr="Güncel USD/TL Kuru">Current USD/TRY Rate</label><input type="number" id="usdKur" value="34" min="0" step="0.01"></div>""",
     True),
    ("atasman-secim-rehberi", "Attachment Selection Guide", "Ataşman Seçim Rehberi",
     "Free excavator attachment selection guide. Select your machine's weight class and job type to get a recommended attachment.",
     "Ekskavatör ataşman seçim rehberi. Makinenizin ağırlık sınıfını ve yapacağınız işi seçin, önerilen ataşmanı görün.",
     "Not sure which attachment fits your machine and job? Select your excavator's weight class and the work you'll do for a general recommendation.",
     "Makinenize ve işinize hangi ataşmanın uygun olduğundan emin değil misiniz? Ekskavatörünüzün ağırlık sınıfını ve yapacağınız işi seçin, genel bir öneri alın.",
     "atasman",
     """<div class="calc-field"><label data-tr="Makine Ağırlık Sınıfı">Machine Weight Class</label>
      <select id="agirlikSinifi">
        <option value="mini" data-tr="Mini Ekskavatör (0,8–6 ton)">Mini Excavator (0.8–6 t)</option>
        <option value="orta" selected data-tr="Orta Sınıf Ekskavatör (13–25 ton)">Mid-size Excavator (13–25 t)</option>
        <option value="agir" data-tr="Ağır Tonaj Ekskavatör (30+ ton)">Heavy-duty Excavator (30+ t)</option>
      </select></div>
      <div class="calc-field"><label data-tr="Yapılacak İş">Job Type</label>
      <select id="isTuruAtasman">
        <option value="kazi" selected data-tr="Genel Kazı / Hafriyat">General Digging / Earthmoving</option>
        <option value="kirma" data-tr="Beton / Asfalt Kırma, Yıkım">Concrete / Asphalt Breaking, Demolition</option>
        <option value="delme" data-tr="Delme / Kazık Sondajı">Drilling / Pile Boring</option>
        <option value="hurda" data-tr="Hurda / Metal Ayırma">Scrap / Metal Sorting</option>
        <option value="tasima" data-tr="Malzeme Taşıma / İstifleme">Material Handling / Stacking</option>
        <option value="sikistirma" data-tr="Zemin Sıkıştırma">Soil Compaction</option>
      </select></div>""",
     True),
]

HEADER = """<header class="site-header">
  <div class="header-inner">
    <a href="{root}index.html" class="logo"><img src="{root}assets/logo-header.png" width="160" height="160" alt="GND Machinery" /></a>
    <nav class="main-nav">
      <a href="{root}index.html#home" data-tr="Ana Sayfa">Home</a>
      <a href="{root}index.html#categories" data-tr="Makineler">Machines</a>
      <a href="{root}index.html#spareparts" data-tr="Yedek Parça">Spare Parts</a>
      <a href="{root}index.html#areas" data-tr="Hizmetler">Services</a>
      <a href="{root}index.html#calculators" data-tr="Hesaplama Araçları">Calculators</a>
      <a href="{root}blog/index.html" data-tr="Blog">Blog</a>
      <a href="{root}kurumsal.html" data-tr="Hakkımızda">About</a>
      <a href="{root}index.html#contact" data-tr="İletişim">Contact</a>
    </nav>
    <div class="header-actions">
      <span id="auth-nav-slot" class="auth-nav-slot"></span>
      <select id="lang-select" class="lang-select" aria-label="Language">
        <option value="en">EN</option>
        <option value="tr">TR</option>
      </select>
      <a class="btn btn-primary header-cta" href="https://wa.me/{wa}?text={wa_generic}" target="_blank" rel="noopener">
        <span data-tr="Teklif Al">Get a Quote</span>
      </a>
    </div>
  </div>
</header>"""

FOOTER = """<footer class="site-footer">
  <div class="section-inner footer-inner">
    <div>© 2026 GND Machinery — GND İş Makineleri Sanayi ve Ticaret A.Ş.</div>
    <div class="footer-note" data-tr="Ağır iş makinesi ve yedek parça küresel tedarikçisi.">Global supplier of heavy equipment and spare parts.</div>
  </div>
</footer>

<a href="https://wa.me/{wa}?text={wa_generic}" class="floating-whatsapp" target="_blank" rel="noopener" aria-label="WhatsApp">
  <svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.5 15.2L2 22l4.9-1.5A10 10 0 1 0 12 2zm0 18.2a8.15 8.15 0 0 1-4.2-1.15l-.3-.18-3.1.95.95-3-.2-.32A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.25-.13-1.45-.72-1.68-.8-.22-.08-.39-.13-.55.13-.16.25-.63.8-.78.97-.14.16-.28.18-.53.06-.25-.13-1.06-.39-2.02-1.25-.75-.67-1.25-1.5-1.4-1.75-.14-.25-.02-.39.11-.51.11-.11.25-.28.37-.42.13-.14.17-.25.25-.4.08-.16.04-.3-.02-.42-.06-.13-.55-1.34-.76-1.83-.2-.48-.4-.42-.55-.42h-.47c-.16 0-.42.06-.64.3-.22.25-.85.83-.85 2.03s.87 2.36 1 2.52c.12.16 1.7 2.6 4.13 3.64.58.25 1.03.4 1.38.5.58.19 1.11.16 1.53.1.47-.07 1.45-.6 1.65-1.17.2-.58.2-1.07.14-1.17-.06-.1-.22-.16-.47-.28z"/></svg>
  <span data-tr="Canlı Destek">Live Support</span>
</a>"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title data-tr="{title_tr}">{name} | {title_suffix} — {site_name}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="{root}css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="{root}js/analytics.js"></script>
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
    <h1 data-tr="{name_tr}">{name}</h1>
    <p data-tr="{intro_tr}">{intro}</p>
    <a href="https://wa.me/{wa}?text={wa_quote}" data-href-tr="https://wa.me/{wa}?text={wa_quote_tr}" class="btn btn-primary btn-lg" target="_blank" rel="noopener" data-tr="Teklif Al →">Get a Quote →</a>
  </div>
</section>

{supply_section}

{info_section}

<section class="categories-section spareparts-section">
  <div class="section-inner">
    <h2 data-tr="Neden GND Machinery Üzerinden Tedarik?">Why Source Through GND Machinery</h2>
    <div class="category-grid">
      {benefits}
    </div>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <h2 data-tr="İlgili Ekipman Kategorileri">Related Equipment Categories</h2>
    <div class="category-grid">
      {siblings}
    </div>
    <p class="back-link">{cross_links} &nbsp;|&nbsp; <a href="{root}index.html" data-tr="← Anasayfaya dön">← Back to home</a></p>
  </div>
</section>

{footer}

<script src="{root}js/detail-lang.js"></script>
<script src="{root}js/lib/supabase.min.js"></script>
<script src="{root}js/auth.js"></script>
<script src="{root}js/advisor-widget.js"></script>
</body>
</html>
"""

SUPPLY_SECTION = """<section class="categories-section">
  <div class="section-inner">
    <h2 data-tr="Sıfır ve İkinci El {name_tr} Tedariği">New &amp; Used {name} Supply</h2>
    <div class="vm-grid">
      <div class="vm-card">
        <h3 data-tr="Sıfır {name_tr}">New {name}</h3>
        <p data-tr="Üretici ortaklarımızdan doğrudan temin edilen, talep üzerine tam spesifikasyon ve teslimat süresi bilgisi sağlanan fabrika çıkışı sıfır üniteler.">Factory-new units sourced directly from our manufacturer partners, with full specification and delivery lead time provided on request.</p>
      </div>
      <div class="vm-card">
        <h3 data-tr="İkinci El {name_tr}">Used {name}</h3>
        <p data-tr="Global ağımızdan temin edilen, çalışma saatlerinize ve bütçenize uygun, incelemesi yapılmış ikinci el üniteler.">Inspected used units offering lower upfront cost, sourced from our global network and matched to your working hours and budget.</p>
      </div>
    </div>
  </div>
</section>"""

SIBLING_CARD_PHOTO = """<div class="category-card">
        <div class="category-photo-wrap"><img class="category-photo" src="{root}assets/categories/{image}" alt="{name} supplied by GND Machinery" data-alt-tr="{name_tr} — GND İş Makineleri" loading="lazy"></div>
        <h3><a href="{href}" data-tr="{name_tr}">{name}</a></h3>
        <p data-tr="{desc_tr}">{desc}</p>
      </div>"""

SIBLING_CARD_ICON = """<div class="category-card">
        <div class="category-icon">{icon}</div>
        <h3><a href="{href}" data-tr="{name_tr}">{name}</a></h3>
        <p data-tr="{desc_tr}">{desc}</p>
      </div>"""

BENEFIT_CARD = """<div class="category-card">
        <h3 data-tr="{title_tr}">{title}</h3>
        <p data-tr="{text_tr}">{text}</p>
      </div>"""


def wa_link_text(text):
    from urllib.parse import quote
    return quote(text)


MACHINE_INFO_SECTION = """<section class="categories-section">
  <div class="section-inner">
    <h2 data-tr="Performans ve Kullanım Alanı Genel Bakışı">Performance &amp; Application Overview</h2>
    <div class="vm-grid">
      <div class="vm-card">
        <h3 data-tr="Tipik Teknik Özellikler">Typical Specifications</h3>
        <p data-tr="{spec_range_tr}">{spec_range}</p>
      </div>
      <div class="vm-card">
        <h3 data-tr="Yaygın Kullanım Alanları">Common Applications</h3>
        <p data-tr="{applications_tr}">{applications}</p>
      </div>
    </div>
    <p class="section-sub" style="margin-top:16px" data-tr="Kesin fiyat; marka, model yılı, çalışma saati ve konfigürasyona göre değişir. Bütçenize uygun fiyat-performans karşılaştırması için WhatsApp'tan bize ulaşın — başlamak için tam teknik döküman gerekmiyor.">Exact pricing depends on brand, model year, working hours and configuration. For a price-performance comparison matched to your budget, message us on WhatsApp — no full spec sheet needed to get started.</p>
    <a href="https://wa.me/{wa}?text={wa_info}" data-href-tr="https://wa.me/{wa}?text={wa_info_tr}" class="btn btn-primary" target="_blank" rel="noopener" data-tr="WhatsApp'tan Fiyat Sorun →">Ask About Pricing on WhatsApp →</a>
  </div>
</section>"""

PARTS_INFO_SECTION = """<section class="categories-section">
  <div class="section-inner">
    <h2 data-tr="Tedarik Seçenekleri">Sourcing Options</h2>
    <div class="category-grid">
      <div class="category-card"><h3 data-tr="Yerli Üretim">Domestic Production</h3><p data-tr="{domestic_tr}">{domestic}</p></div>
      <div class="category-card"><h3 data-tr="İthal Ürünler">Imported Products</h3><p data-tr="{imported_tr}">{imported}</p></div>
      <div class="category-card"><h3 data-tr="OEM İthal">OEM Imported</h3><p data-tr="{oem_tr}">{oem}</p></div>
    </div>
    <p class="section-sub" style="margin-top:16px" data-tr="Doğru seçenek; makinenizin markasına, modeline ve parçanın operasyonunuz için ne kadar kritik olduğuna bağlıdır. Size özel bir öneri için makine bilgilerinizle WhatsApp'tan bize ulaşın.">The right option depends on your machine's brand, model and how critical the part is to your operation. Message us on WhatsApp with your machine details for a tailored recommendation.</p>
    <a href="https://wa.me/{wa}?text={wa_info}" data-href-tr="https://wa.me/{wa}?text={wa_info_tr}" class="btn btn-primary" target="_blank" rel="noopener" data-tr="WhatsApp'tan Tedarik Sorun →">Ask About Sourcing on WhatsApp →</a>
  </div>
</section>"""

SERVICE_INFO_SECTION = """<section class="categories-section">
  <div class="section-inner">
    <h2 data-tr="Nasıl Yardımcı Oluyoruz">What We Help With</h2>
    <div class="category-grid">
      <div class="category-card"><h3 data-tr="Tedarik ve Doğrulama">Sourcing &amp; Verification</h3><p data-tr="{sourcing_tr}">{sourcing}</p></div>
      <div class="category-card"><h3 data-tr="Gümrük ve Evrak Rehberliği">Customs &amp; Documentation Guidance</h3><p data-tr="{customs_tr}">{customs}</p></div>
      <div class="category-card"><h3 data-tr="Lojistik Koordinasyonu">Logistics Coordination</h3><p data-tr="{logistics_tr}">{logistics}</p></div>
    </div>
    <p class="section-sub" style="margin-top:16px" data-tr="Her ülke ve işlemin kendine has gereksinimleri vardır. Sizin ithalat veya ihracat durumunuza özel rehberlik için doğrudan WhatsApp'tan bize ulaşın.">Every country and transaction has its own requirements. For guidance specific to your import or export case, message us directly on WhatsApp.</p>
    <a href="https://wa.me/{wa}?text={wa_info}" data-href-tr="https://wa.me/{wa}?text={wa_info_tr}" class="btn btn-primary" target="_blank" rel="noopener" data-tr="WhatsApp'tan Durumunuzu Sorun →">Ask About Your Case on WhatsApp →</a>
  </div>
</section>"""


def build_pages(items, out_dir, group_title, url_prefix, root, cross_link_target_prefix, cross_links_list, kind):
    os.makedirs(out_dir, exist_ok=True)
    wa_generic = wa_link_text("Hi, I'd like more information about GND Machinery.")
    header = HEADER.format(root=root, wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    benefits_html = "\n      ".join(
        BENEFIT_CARD.format(title=t, text=x, title_tr=esc(tt), text_tr=esc(tx))
        for t, x, tt, tx in BENEFITS
    )
    cross_links_html = " &middot; ".join(
        f'<a href="{root}{cross_link_target_prefix}/{s}.html" data-tr="{esc(n_tr)}">{n}</a>' for s, n, n_tr in cross_links_list
    )

    for slug, name, meta_desc, intro, icon_key, image, extra, tr in items:
        name_tr, intro_tr, extra_tr, desc_tr = tr

        sibling_parts = []
        for s, n, m, d, k, img, ex, tri in items:
            if s == slug:
                continue
            n_tr, _, _, d_tr = tri
            if img:
                sibling_parts.append(SIBLING_CARD_PHOTO.format(root=root, image=img, href=f"{s}.html", name=n, desc=m, name_tr=esc(n_tr), desc_tr=esc(d_tr)))
            else:
                sibling_parts.append(SIBLING_CARD_ICON.format(icon=ICONS[k], href=f"{s}.html", name=n, desc=m, name_tr=esc(n_tr), desc_tr=esc(d_tr)))
        siblings_html = "\n      ".join(sibling_parts)

        wa_quote = wa_link_text(f"Hi, I'd like a quote for {name}.")
        wa_quote_tr = wa_link_text(f"Merhaba, {name_tr} için teklif almak istiyorum.")
        wa_info = wa_link_text(f"Hi, I have a question about {name}.")
        wa_info_tr = wa_link_text(f"Merhaba, {name_tr} hakkında bir sorum var.")
        if image:
            media = f'<div class="category-detail-photo"><img src="{root}assets/categories/{image}" alt="{name} for sale — GND Machinery" data-alt-tr="{esc(name_tr)} — GND İş Makineleri" loading="lazy"></div>'
        else:
            media = f'<div class="category-detail-icon">{ICONS[icon_key]}</div>'

        if kind == "machine":
            spec_range, applications = extra
            spec_range_tr, applications_tr = extra_tr
            info_section = MACHINE_INFO_SECTION.format(spec_range=spec_range, applications=applications, spec_range_tr=esc(spec_range_tr), applications_tr=esc(applications_tr), wa=WHATSAPP_NUMBER, wa_info=wa_info, wa_info_tr=wa_info_tr)
            title_suffix = "New & Used Supplier"
            title_suffix_tr = "Sıfır ve İkinci El Tedarikçisi"
            supply_section = SUPPLY_SECTION.format(name=name, name_tr=esc(name_tr))
        elif kind == "service":
            sourcing, customs, logistics = extra
            sourcing_tr, customs_tr, logistics_tr = extra_tr
            info_section = SERVICE_INFO_SECTION.format(sourcing=sourcing, customs=customs, logistics=logistics, sourcing_tr=esc(sourcing_tr), customs_tr=esc(customs_tr), logistics_tr=esc(logistics_tr), wa=WHATSAPP_NUMBER, wa_info=wa_info, wa_info_tr=wa_info_tr)
            title_suffix = "Consultancy Services"
            title_suffix_tr = "Danışmanlık Hizmetleri"
            supply_section = ""
        else:
            domestic, imported, oem = extra
            domestic_tr, imported_tr, oem_tr = extra_tr
            info_section = PARTS_INFO_SECTION.format(domestic=domestic, imported=imported, oem=oem, domestic_tr=esc(domestic_tr), imported_tr=esc(imported_tr), oem_tr=esc(oem_tr), wa=WHATSAPP_NUMBER, wa_info=wa_info, wa_info_tr=wa_info_tr)
            title_suffix = "New & Used Supplier"
            title_suffix_tr = "Sıfır ve İkinci El Tedarikçisi"
            supply_section = SUPPLY_SECTION.format(name=name, name_tr=esc(name_tr))

        title_tr = esc(f"{name_tr} | {title_suffix_tr} — {SITE_NAME}")
        page = PAGE_TEMPLATE.format(
            name=name, site_name=SITE_NAME, meta_desc=meta_desc, intro=intro,
            canonical=f"{BASE_URL}/{url_prefix}/{slug}.html", base_url=BASE_URL,
            root=root, header=header, media=media, benefits=benefits_html,
            wa=WHATSAPP_NUMBER, wa_quote=wa_quote, wa_quote_tr=wa_quote_tr, cross_links=cross_links_html,
            group_title=group_title, siblings=siblings_html, footer=footer,
            info_section=info_section, title_suffix=title_suffix, supply_section=supply_section,
            name_tr=esc(name_tr), intro_tr=esc(intro_tr), title_tr=title_tr,
        )
        with open(os.path.join(out_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  wrote {out_dir}/{slug}.html")


CALC_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} — {site_name}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="../css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="../js/analytics.js"></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Home", "item": "{base_url}/"}},
    {{"@type": "ListItem", "position": 2, "name": "Calculators", "item": "{base_url}/#calculators"}},
    {{"@type": "ListItem", "position": 3, "name": "{name}", "item": "{canonical}"}}
  ]
}}
</script>
</head>
<body data-calc="{calc_type}">

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <h1 data-tr="{name_tr}">{name}</h1>
    <p data-tr="{intro_tr}">{intro}</p>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <div class="calc-panel">
      {form_html}
      <button id="calcBtn" class="btn btn-primary" style="width:100%" data-tr="Hesapla">Calculate</button>
      <div id="calcResult" class="calc-result"></div>
      {approx_note}
      <div class="calc-cta">
        <a href="https://wa.me/{wa}?text={wa_info}" class="btn btn-primary" style="width:100%" target="_blank" rel="noopener" data-tr="Kesin Bilgi İçin WhatsApp'tan Sorun →">Ask on WhatsApp for Exact Info →</a>
      </div>
    </div>
  </div>
</section>

<section class="categories-section spareparts-section">
  <div class="section-inner">
    <h2 data-tr="Diğer Hesaplama Araçları">Other Calculators</h2>
    <div class="category-grid">
      {siblings}
    </div>
    <p class="back-link"><a href="{root}index.html" data-tr="← Anasayfaya dön">← Back to home</a></p>
  </div>
</section>

{footer}

<script src="{root}js/detail-lang.js"></script>
<script src="{root}js/calculators.js"></script>
<script src="{root}js/lib/supabase.min.js"></script>
<script src="{root}js/auth.js"></script>
<script src="{root}js/advisor-widget.js"></script>
</body>
</html>
"""

CALC_APPROX_NOTE = '<p class="calc-note" data-tr="Bu sonuçlar genel sektör ortalamalarına dayanır, yaklaşıktır. Projenize özel kesin bilgi için bize ulaşın.">These results are based on general industry averages and are approximate. Contact us for exact figures specific to your project.</p>'

CALC_SIBLING_CARD = """<div class="category-card">
        <h3><a href="{href}" data-tr="{name_tr}">{name}</a></h3>
        <p data-tr="{desc_tr}">{desc}</p>
      </div>"""


def build_calculator_pages(root_dir):
    out_dir = os.path.join(root_dir, "hesaplama-araclari")
    os.makedirs(out_dir, exist_ok=True)
    wa_generic = wa_link_text("Hi, I'd like more information about GND Machinery.")
    header = HEADER.format(root="../", wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)

    for slug, name, name_tr, meta_desc, meta_desc_tr, intro, intro_tr, calc_type, form_html, approximate in CALCULATORS:
        sibling_parts = []
        for s, n, n_tr, m, m_tr, *_ in CALCULATORS:
            if s == slug:
                continue
            sibling_parts.append(CALC_SIBLING_CARD.format(href=f"{s}.html", name=n, desc=m, name_tr=esc(n_tr), desc_tr=esc(m_tr)))
        siblings_html = "\n      ".join(sibling_parts)

        wa_info = wa_link_text(f"Hi, I have a question about {name}.")
        approx_note = CALC_APPROX_NOTE if approximate else ""

        page = CALC_PAGE_TEMPLATE.format(
            name=name, site_name=SITE_NAME, meta_desc=meta_desc, intro=intro,
            canonical=f"{BASE_URL}/hesaplama-araclari/{slug}.html", base_url=BASE_URL,
            root="../", header=header, footer=footer, calc_type=calc_type,
            form_html=form_html, approx_note=approx_note, siblings=siblings_html,
            wa=WHATSAPP_NUMBER, wa_info=wa_info, name_tr=esc(name_tr), intro_tr=esc(intro_tr),
        )
        with open(os.path.join(out_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  wrote hesaplama-araclari/{slug}.html")


# (slug, title_tr, meta_desc_tr, machine_a, machine_b, spec_rows, sources)
# spec_rows: list of (label_tr, value_a, value_b) — only fields verified from official
# manufacturer documents go here, never estimated/guessed values.
# sources: list of (label, url) to the official documents the numbers came from.
COMPARISONS = [
    ("cat-320-vs-komatsu-pc200",
     "CAT 320 vs Komatsu PC200-8 Karşılaştırma — Teknik Özellikler",
     "CAT 320 ve Komatsu PC200-8 ekskavatörlerin resmi üretici verilerine dayanan teknik özellik karşılaştırması: çalışma ağırlığı, motor gücü, kova kapasitesi, kazı derinliği.",
     "CAT 320", "Komatsu PC200-8",
     [
         ("Çalışma Ağırlığı", "22.500 kg", "20.010 kg"),
         ("Motor Gücü", "121 kW (162 HP)", "110 kW (148 HP) @ 2000 rpm"),
         ("Kova Kapasitesi", "1,19 m³", "0,50–1,20 m³"),
         ("Maksimum Kazı Derinliği", "6,72 m", "6,62 m"),
         ("Maksimum Yatay Erişim", "9,86 m", "9,70 m"),
         ("Emisyon Standardı", "Tier 4 Final / EU Stage IV", "Üreticiye danışın"),
     ],
     [
         ("Caterpillar resmi teknik özellik dokümanı", "https://www.petersoncat.com/sites/cat/files/products/documents/1455901915-33586.pdf"),
         ("Komatsu resmi satış broşürü (PC200/PC200LC-8)", "http://www.komatsu.pe/images/pdf-construccion/excavadora/PC200200LC-8SALESBROCHUREAESS688-012006EV-2.pdf"),
     ]),
    ("jcb-3cx-vs-cat-428",
     "JCB 3CX vs CAT 428 Karşılaştırma — Kepçe-Loader Teknik Özellikler",
     "JCB 3CX ve CAT 428 kepçe-loader (beko loader) modellerinin resmi üretici verilerine dayanan teknik özellik karşılaştırması: çalışma ağırlığı, motor gücü, kazı derinliği, kepçe kapasitesi.",
     "JCB 3CX", "CAT 428",
     [
         ("Çalışma Ağırlığı", "7.370–8.070 kg", "≈11.000 kg (11 ton)"),
         ("Motor Gücü", "68,5 kW (92 HP)", "74 kW (99 HP)"),
         ("Kazı Derinliği", "5,46 m", "Üreticiye danışın"),
         ("Ön Kepçe Kapasitesi", "1,1 m³", "Üreticiye danışın"),
     ],
     [
         ("JCB 3CX resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.companywrench.com/PDF/JCB_3CX_SPECS.pdf"),
         ("Caterpillar 428 resmi ürün sayfası", "https://www.cat.com/en_US/products/new/equipment/backhoe-loaders/side-shift-backhoe-loaders/102200.html"),
     ]),
    ("cat-d6-vs-komatsu-d65",
     "CAT D6 vs Komatsu D65EX-16 Karşılaştırma — Dozer Teknik Özellikler",
     "CAT D6 ve Komatsu D65EX-16 dozerlerin resmi üretici verilerine dayanan teknik özellik karşılaştırması: çalışma ağırlığı, motor gücü, bıçak kapasitesi.",
     "CAT D6", "Komatsu D65EX-16",
     [
         ("Çalışma Ağırlığı", "≈23.010 kg (50.733 lb)", "20.500–22.900 kg"),
         ("Motor Gücü", "257 kW (345 HP) — C9.3 ACERT", "155 kW (207 HP)"),
         ("Bıçak Kapasitesi", "Üreticiye danışın", "3,55–5,61 m³"),
     ],
     [
         ("Caterpillar D6/D6 XE resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.hawthornecat.com/wp-content/uploads/2021/03/Technical-Specs-D6-and-D6-XE-Dozers.pdf"),
         ("Komatsu D65EX/WX/PX-16 resmi broşürü", "https://www.komatsu.eu/Assets/GetBrochureByProductName.aspx?id=D65EX/WX/PX-16&langID=en"),
     ]),
    ("cat-950gc-vs-komatsu-wa380",
     "CAT 950 GC vs Komatsu WA380-8 Karşılaştırma — Lastikli Yükleyici Teknik Özellikler",
     "CAT 950 GC ve Komatsu WA380-8 lastikli yükleyicilerin resmi üretici verilerine dayanan teknik özellik karşılaştırması: çalışma ağırlığı, motor gücü, kova kapasitesi, emisyon standardı.",
     "CAT 950 GC", "Komatsu WA380-8",
     [
         ("Çalışma Ağırlığı", "19.069 kg", "18.155–19.765 kg"),
         ("Motor Gücü", "180 kW (241 HP)", "143 kW (192 HP) @ 2100 rpm"),
         ("Kova Kapasitesi", "Üreticiye danışın", "3,2–6,5 m³"),
         ("Emisyon Standardı", "Tier 4 Final / EU Stage V–IV", "EU Stage IV"),
     ],
     [
         ("Caterpillar 950 GC resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.teknoxgroup.com/fileadmin/user_upload/950GC.pdf"),
         ("Komatsu WA380-8 resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.ridgwayrentals.com/wp-content/uploads/2021/02/Komatsu-WA380-8-wheel-loader-spec-sheet.pdf"),
     ]),
    ("hidromek-220lc-vs-cat-320",
     "Hidromek HMK 220 LC vs CAT 320 Karşılaştırma — Ekskavatör Teknik Özellikler",
     "Yerli üretici Hidromek'in HMK 220 LC modeli ile küresel lider Caterpillar'ın 320 modelinin teknik özellik karşılaştırması: çalışma ağırlığı, motor gücü, kova kapasitesi, kazı derinliği.",
     "Hidromek HMK 220 LC", "CAT 320",
     [
         ("Çalışma Ağırlığı", "23.350 kg", "22.500 kg"),
         ("Motor Gücü", "119 kW (162 HP) — Isuzu", "121 kW (162 HP)"),
         ("Kova Kapasitesi", "1,0 m³", "1,19 m³"),
         ("Maksimum Kazı Derinliği", "6,67 m", "6,72 m"),
         ("Maksimum Yatay Erişim", "10,05 m", "9,86 m"),
     ],
     [
         ("Hidromek HMK 220 LC teknik verisi (lectura-specs.com — üretici verilerini derleyen bağımsız kaynak; Hidromek'in kendi sitesine bu oturumda erişilemedi)", "https://www.lectura-specs.com/en/model/construction-machinery/crawler-excavators-hidromek/hmk-220-lc-11682240"),
         ("Caterpillar resmi teknik özellik dokümanı", "https://www.petersoncat.com/sites/cat/files/products/documents/1455901915-33586.pdf"),
     ]),
    ("cat-236d3-vs-bobcat-s650",
     "CAT 236D3 vs Bobcat S650 Karşılaştırma — Skid Steer Loader Teknik Özellikler",
     "CAT 236D3 ve Bobcat S650 skid steer loader (kompakt kaydırmalı yükleyici) modellerinin resmi üretici verilerine dayanan teknik özellik karşılaştırması: çalışma ağırlığı, motor gücü, kaldırma kapasitesi.",
     "CAT 236D3", "Bobcat S650",
     [
         ("Çalışma Ağırlığı", "2.979 kg", "3.777 kg"),
         ("Motor Gücü", "49,1 kW (65,8 HP) — Cat C2.2", "54,6 kW (73 HP) — Kubota V3307"),
         ("Kaldırma Kapasitesi (ROC)", "820 kg", "1.282 kg"),
     ],
     [
         ("Caterpillar 236D3 resmi teknik özellikleri (bayi kaynaklı)", "https://www.petersoncat.com/products/new/skid-steer-loaders/236d3"),
         ("Bobcat S650 resmi ürün sayfası", "https://www.bobcat.com/mea/en/loaders/skid-steer-loaders/models/s650/specs-options"),
     ]),
    ("jlg-600aj-vs-genie-s60j",
     "JLG 600AJ vs Genie S-60 J Karşılaştırma — Manlift (Boom Lift) Teknik Özellikler",
     "JLG 600AJ ve Genie S-60 J eklemli platform (boom lift/manlift) modellerinin resmi üretici verilerine dayanan teknik özellik karşılaştırması: platform yüksekliği, yatay erişim, kapasite.",
     "JLG 600AJ", "Genie S-60 J",
     [
         ("Platform Yüksekliği", "18,47 m", "Üreticiye danışın"),
         ("Maksimum Çalışma Yüksekliği", "Üreticiye danışın", "20,50 m"),
         ("Yatay Erişim", "12,10 m", "12,30 m"),
         ("Platform Kapasitesi", "227 kg", "300 kg"),
         ("Makine Ağırlığı", "10.292 kg", "7.550 kg"),
         ("Motor Gücü", "62 kW (84 HP) dual-fuel / 36,4 kW (49 HP) dizel", "18 kW (24 HP)"),
     ],
     [
         ("JLG 600AJ resmi teknik özellik dokümanı", "https://s3-us-west-1.amazonaws.com/acropolis-wp-content-uploads/jlg-600AJ-Spec-Sheet.pdf"),
         ("Genie S-60 J resmi ürün sayfası", "https://www.genielift.com/en/aerial-lifts/telescopic-boom-lifts/s60j"),
     ]),
    ("cat-140gc-vs-komatsu-gd655",
     "CAT 140 GC vs Komatsu GD655-6 Karşılaştırma — Greyder Teknik Özellikler",
     "CAT 140 GC ve Komatsu GD655-6 motor greyderlerin resmi üretici verilerine dayanan teknik özellik karşılaştırması: çalışma ağırlığı, motor gücü, bıçak genişliği.",
     "CAT 140 GC", "Komatsu GD655-6",
     [
         ("Çalışma Ağırlığı", "18.700 kg", "16.940 kg (kazıyıcısız) / 18.900 kg (kazıyıcılı)"),
         ("Motor Gücü", "131 kW (176 HP) — Cat C7.1", "163 kW (218 HP) net"),
         ("Bıçak (Moldboard) Genişliği", "3,7 m (standart)", "4,27 m"),
     ],
     [
         ("Caterpillar 140 GC resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.avesco-cat.com/fileadmin/unsorted/140_GC_SPECS.pdf"),
         ("Komatsu GD655-6 resmi broşürü", "https://www.komatsu.com/content/dam/komatsu/sales-and-marketing-documents/brochures/motor-graders/gd655-6/en-gd655-6br01-0722-v8.pdf"),
     ]),
    ("cat-cs56b-vs-bomag-bw213",
     "CAT CS56B vs Bomag BW213 D-5 Karşılaştırma — Silindir Teknik Özellikler",
     "CAT CS56B ve Bomag BW213 D-5 tek tamburlu silindirlerin resmi üretici verilerine dayanan teknik özellik karşılaştırması: çalışma ağırlığı, motor gücü, tambur genişliği.",
     "CAT CS56B", "Bomag BW213 D-5",
     [
         ("Çalışma Ağırlığı (kabinli)", "11.500 kg", "12.600 kg"),
         ("Motor Gücü", "117 kW (157 HP) — Cat C4.4 ACERT", "95 kW (127 HP)"),
         ("Tambur Genişliği", "2.134 mm", "2.130 mm"),
     ],
     [
         ("Caterpillar CS56B resmi ürün sayfası (bayi kaynaklı)", "https://www.petersoncat.com/products/new/vibratory-soil-compactors/cs56b"),
         ("Bomag BW 213 D-5 resmi ürün sayfası", "https://www.bomag.com/ww-en/machinery/categories/single-drum-rollers-soil-compactors/single-drum-rollers/bw-213-d-5-58615/"),
     ]),
]

# (slug, name, meta_desc_tr, intro_tr, specs=[(label,value)], source=(label,url), compare_slug, gnd_category_slug)
# Same sourcing rule as COMPARISONS: every value here must trace to an official
# manufacturer document. compare_slug/gnd_category_slug are used for cross-links.
MACHINE_SPECS = [
    ("cat-320-teknik-ozellikler", "CAT 320",
     "CAT 320 ekskavatörün resmi Caterpillar teknik özellikleri: çalışma ağırlığı, motor gücü, kova kapasitesi, kazı derinliği ve erişim mesafesi.",
     "Caterpillar 320, orta sınıf paletli ekskavatör segmentinin en çok tercih edilen modellerinden biridir. Aşağıdaki veriler doğrudan Caterpillar'ın resmi teknik özellik dokümanından alınmıştır.",
     [("Çalışma Ağırlığı", "22.500 kg"), ("Motor", "Cat C4.4 ACERT"), ("Motor Gücü", "121 kW (162 HP)"),
      ("Emisyon Standardı", "Tier 4 Final / EU Stage IV"), ("Kova Kapasitesi", "1,19 m³"),
      ("Maksimum Kazı Derinliği", "6,72 m"), ("Maksimum Yatay Erişim", "9,86 m")],
     ("Caterpillar resmi teknik özellik dokümanı", "https://www.petersoncat.com/sites/cat/files/products/documents/1455901915-33586.pdf"),
     "cat-320-vs-komatsu-pc200", "excavator"),
    ("komatsu-pc200-8-teknik-ozellikler", "Komatsu PC200-8",
     "Komatsu PC200-8 ekskavatörün resmi Komatsu teknik özellikleri: çalışma ağırlığı, motor gücü, kova kapasitesi, kazı derinliği ve erişim mesafesi.",
     "Komatsu PC200-8, dünya genelinde en yaygın kullanılan orta sınıf ekskavatörlerden biridir. Aşağıdaki veriler doğrudan Komatsu'nun resmi satış broşüründen alınmıştır.",
     [("Çalışma Ağırlığı", "20.010 kg"), ("Motor Gücü", "110 kW (148 HP) @ 2000 rpm"),
      ("Kova Kapasitesi", "0,50–1,20 m³"), ("Maksimum Kazı Derinliği", "6,62 m"),
      ("Maksimum Yatay Erişim", "9,70 m"), ("Palet Genişliği", "600 mm")],
     ("Komatsu resmi satış broşürü (PC200/PC200LC-8)", "http://www.komatsu.pe/images/pdf-construccion/excavadora/PC200200LC-8SALESBROCHUREAESS688-012006EV-2.pdf"),
     "cat-320-vs-komatsu-pc200", "excavator"),
    ("jcb-3cx-teknik-ozellikler", "JCB 3CX",
     "JCB 3CX kepçe-loader'ın resmi JCB teknik özellikleri: çalışma ağırlığı, motor gücü, kazı derinliği, ön kepçe kapasitesi.",
     "JCB 3CX, Türkiye'de kepçe-loader (beko loader) segmentinin en çok tercih edilen modelidir. Aşağıdaki veriler doğrudan JCB'nin resmi teknik özellik dokümanından alınmıştır.",
     [("Çalışma Ağırlığı", "7.370–8.070 kg"), ("Motor Gücü", "55–81 kW (74–109 HP), tipik 68,5 kW (92 HP)"),
      ("Kazı Derinliği", "5,46 m (varyanta göre 4,00–6,14 m)"), ("Ön Kepçe Kapasitesi", "1,1 m³")],
     ("JCB 3CX resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.companywrench.com/PDF/JCB_3CX_SPECS.pdf"),
     "jcb-3cx-vs-cat-428", "backhoe-loader"),
    ("cat-428-teknik-ozellikler", "CAT 428",
     "CAT 428 kepçe-loader'ın resmi Caterpillar teknik özellikleri: çalışma ağırlığı ve motor gücü.",
     "Caterpillar 428, kepçe-loader segmentinde CAT'in güncel nesil modelidir. Aşağıdaki veriler doğrudan Caterpillar'ın resmi ürün sayfasından alınmıştır.",
     [("Çalışma Ağırlığı", "≈11.000 kg (11 ton)"), ("Motor", "Cat 3054C, 4,4L turbo"), ("Motor Gücü", "74 kW (99 HP)")],
     ("Caterpillar 428 resmi ürün sayfası", "https://www.cat.com/en_US/products/new/equipment/backhoe-loaders/side-shift-backhoe-loaders/102200.html"),
     "jcb-3cx-vs-cat-428", "backhoe-loader"),
    ("cat-d6-teknik-ozellikler", "CAT D6",
     "CAT D6 dozerin resmi Caterpillar teknik özellikleri: çalışma ağırlığı ve motor gücü.",
     "Caterpillar D6, orta-ağır sınıf paletli dozer segmentinin öncü modellerindendir. Aşağıdaki veriler doğrudan Caterpillar'ın resmi teknik özellik dokümanından alınmıştır.",
     [("Çalışma Ağırlığı", "≈23.010 kg (50.733 lb)"), ("Motor", "Cat C9.3 ACERT"), ("Motor Gücü", "257 kW (345 HP)")],
     ("Caterpillar D6/D6 XE resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.hawthornecat.com/wp-content/uploads/2021/03/Technical-Specs-D6-and-D6-XE-Dozers.pdf"),
     "cat-d6-vs-komatsu-d65", "bulldozer"),
    ("komatsu-d65-teknik-ozellikler", "Komatsu D65EX-16",
     "Komatsu D65EX-16 dozerin resmi Komatsu teknik özellikleri: çalışma ağırlığı, motor gücü, bıçak kapasitesi.",
     "Komatsu D65EX-16, orta-ağır sınıf paletli dozer segmentinde CAT D6'nın doğrudan rakibidir. Aşağıdaki veriler doğrudan Komatsu'nun resmi broşüründen alınmıştır.",
     [("Çalışma Ağırlığı", "20.500–22.900 kg"), ("Motor Gücü", "155 kW (207 HP)"), ("Bıçak Kapasitesi", "3,55–5,61 m³")],
     ("Komatsu D65EX/WX/PX-16 resmi broşürü", "https://www.komatsu.eu/Assets/GetBrochureByProductName.aspx?id=D65EX/WX/PX-16&langID=en"),
     "cat-d6-vs-komatsu-d65", "bulldozer"),
    ("cat-950gc-teknik-ozellikler", "CAT 950 GC",
     "CAT 950 GC lastikli yükleyicinin resmi Caterpillar teknik özellikleri: çalışma ağırlığı, motor gücü, emisyon standardı.",
     "Caterpillar 950 GC, orta sınıf lastikli yükleyici segmentinde CAT'in güncel nesil modelidir. Aşağıdaki veriler doğrudan Caterpillar'ın resmi teknik özellik dokümanından alınmıştır.",
     [("Çalışma Ağırlığı", "19.069 kg"), ("Motor Gücü", "180 kW (241 HP)"), ("Emisyon Standardı", "Tier 4 Final / EU Stage V–IV")],
     ("Caterpillar 950 GC resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.teknoxgroup.com/fileadmin/user_upload/950GC.pdf"),
     "cat-950gc-vs-komatsu-wa380", "wheel-loader"),
    ("komatsu-wa380-8-teknik-ozellikler", "Komatsu WA380-8",
     "Komatsu WA380-8 lastikli yükleyicinin resmi Komatsu teknik özellikleri: çalışma ağırlığı, motor gücü, kova kapasitesi, emisyon standardı.",
     "Komatsu WA380-8, orta sınıf lastikli yükleyici segmentinde CAT 950 GC'nin doğrudan rakibidir. Aşağıdaki veriler doğrudan Komatsu'nun resmi teknik özellik dokümanından alınmıştır.",
     [("Çalışma Ağırlığı", "18.155–19.765 kg"), ("Motor Gücü", "143 kW (192 HP) @ 2100 rpm"), ("Kova Kapasitesi", "3,2–6,5 m³"), ("Emisyon Standardı", "EU Stage IV")],
     ("Komatsu WA380-8 resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.ridgwayrentals.com/wp-content/uploads/2021/02/Komatsu-WA380-8-wheel-loader-spec-sheet.pdf"),
     "cat-950gc-vs-komatsu-wa380", "wheel-loader"),
    ("hidromek-220lc-teknik-ozellikler", "Hidromek HMK 220 LC",
     "Hidromek HMK 220 LC ekskavatörün teknik özellikleri: çalışma ağırlığı, motor gücü, kova kapasitesi, kazı derinliği.",
     "Hidromek HMK 220 LC, Türkiye'nin küresel ölçekte üretim yapan iş makinesi üreticisi Hidromek'in orta-ağır sınıf paletli ekskavatörüdür. Aşağıdaki veriler bağımsız bir teknik veri kaynağından derlenmiştir.",
     [("Çalışma Ağırlığı", "23.350 kg"), ("Motor Gücü", "119 kW (162 HP) — Isuzu"), ("Kova Kapasitesi", "1,0 m³"), ("Maksimum Kazı Derinliği", "6,67 m"), ("Maksimum Yatay Erişim", "10,05 m")],
     ("Hidromek HMK 220 LC teknik verisi (lectura-specs.com)", "https://www.lectura-specs.com/en/model/construction-machinery/crawler-excavators-hidromek/hmk-220-lc-11682240"),
     "hidromek-220lc-vs-cat-320", "excavator"),
    ("cat-236d3-teknik-ozellikler", "CAT 236D3",
     "CAT 236D3 skid steer loader'ın resmi Caterpillar teknik özellikleri: çalışma ağırlığı, motor gücü, kaldırma kapasitesi.",
     "Caterpillar 236D3, kompakt kaydırmalı yükleyici (skid steer loader) segmentinde CAT'in güncel nesil modelidir. Aşağıdaki veriler doğrudan Caterpillar'ın resmi bayi kaynaklı sayfasından alınmıştır.",
     [("Çalışma Ağırlığı", "2.979 kg"), ("Motor", "Cat C2.2 turbo"), ("Motor Gücü", "49,1 kW (65,8 HP)"), ("Kaldırma Kapasitesi (ROC)", "820 kg")],
     ("Caterpillar 236D3 resmi teknik özellikleri (bayi kaynaklı)", "https://www.petersoncat.com/products/new/skid-steer-loaders/236d3"),
     "cat-236d3-vs-bobcat-s650", "skid-steer-loader"),
    ("bobcat-s650-teknik-ozellikler", "Bobcat S650",
     "Bobcat S650 skid steer loader'ın resmi Bobcat teknik özellikleri: çalışma ağırlığı, motor gücü, kaldırma kapasitesi.",
     "Bobcat S650, kompakt kaydırmalı yükleyici segmentinin dünya genelinde en tanınan markalarından Bobcat'in orta sınıf modelidir. Aşağıdaki veriler doğrudan Bobcat'in resmi ürün sayfasından alınmıştır.",
     [("Çalışma Ağırlığı", "3.777 kg"), ("Motor", "Kubota V3307-DI-TE3"), ("Motor Gücü", "54,6 kW (73 HP)"), ("Kaldırma Kapasitesi (ROC)", "1.282 kg")],
     ("Bobcat S650 resmi ürün sayfası", "https://www.bobcat.com/mea/en/loaders/skid-steer-loaders/models/s650/specs-options"),
     "cat-236d3-vs-bobcat-s650", "skid-steer-loader"),
    ("jlg-600aj-teknik-ozellikler", "JLG 600AJ",
     "JLG 600AJ eklemli platformun (boom lift) resmi JLG teknik özellikleri: platform yüksekliği, yatay erişim, kapasite.",
     "JLG 600AJ, yükseğe erişim platformu (manlift/boom lift) segmentinde dünya genelinde en yaygın kullanılan modellerden biridir. Aşağıdaki veriler doğrudan JLG'nin resmi teknik özellik dokümanından alınmıştır.",
     [("Platform Yüksekliği", "18,47 m"), ("Yatay Erişim", "12,10 m"), ("Platform Kapasitesi", "227 kg"), ("Makine Ağırlığı", "10.292 kg"), ("Motor Gücü", "62 kW (84 HP) dual-fuel / 36,4 kW (49 HP) dizel")],
     ("JLG 600AJ resmi teknik özellik dokümanı", "https://s3-us-west-1.amazonaws.com/acropolis-wp-content-uploads/jlg-600AJ-Spec-Sheet.pdf"),
     "jlg-600aj-vs-genie-s60j", "boom-lift"),
    ("genie-s60j-teknik-ozellikler", "Genie S-60 J",
     "Genie S-60 J eklemli platformun (boom lift) resmi Genie teknik özellikleri: çalışma yüksekliği, yatay erişim, kapasite.",
     "Genie S-60 J, yükseğe erişim platformu segmentinde JLG ile birlikte dünyanın en tanınan iki markasından biridir. Aşağıdaki veriler doğrudan Genie'nin resmi ürün sayfasından alınmıştır.",
     [("Maksimum Çalışma Yüksekliği", "20,50 m"), ("Yatay Erişim", "12,30 m"), ("Platform Kapasitesi", "300 kg"), ("Makine Ağırlığı", "7.550 kg"), ("Motor Gücü", "18 kW (24 HP)")],
     ("Genie S-60 J resmi ürün sayfası", "https://www.genielift.com/en/aerial-lifts/telescopic-boom-lifts/s60j"),
     "jlg-600aj-vs-genie-s60j", "boom-lift"),
    ("cat-140gc-teknik-ozellikler", "CAT 140 GC",
     "CAT 140 GC motor greyderin resmi Caterpillar teknik özellikleri: çalışma ağırlığı, motor gücü, bıçak genişliği.",
     "Caterpillar 140 GC, motor greyder segmentinde CAT'in güncel nesil modelidir. Aşağıdaki veriler doğrudan Caterpillar'ın resmi teknik özellik dokümanından alınmıştır.",
     [("Çalışma Ağırlığı", "18.700 kg"), ("Motor", "Cat C7.1"), ("Motor Gücü", "131 kW (176 HP)"), ("Bıçak (Moldboard) Genişliği", "3,7 m (standart)")],
     ("Caterpillar 140 GC resmi teknik özellik dokümanı (bayi kaynaklı)", "https://www.avesco-cat.com/fileadmin/unsorted/140_GC_SPECS.pdf"),
     "cat-140gc-vs-komatsu-gd655", "motor-grader"),
    ("komatsu-gd655-6-teknik-ozellikler", "Komatsu GD655-6",
     "Komatsu GD655-6 motor greyderin resmi Komatsu teknik özellikleri: çalışma ağırlığı, motor gücü, bıçak genişliği.",
     "Komatsu GD655-6, motor greyder segmentinde CAT 140 GC'nin doğrudan rakibidir. Aşağıdaki veriler doğrudan Komatsu'nun resmi broşüründen alınmıştır.",
     [("Çalışma Ağırlığı", "16.940 kg (kazıyıcısız) / 18.900 kg (kazıyıcılı)"), ("Motor Gücü Net", "163 kW (218 HP)"), ("Motor Gücü Gross", "165 kW (221 HP)"), ("Bıçak (Moldboard) Genişliği", "4,27 m")],
     ("Komatsu GD655-6 resmi broşürü", "https://www.komatsu.com/content/dam/komatsu/sales-and-marketing-documents/brochures/motor-graders/gd655-6/en-gd655-6br01-0722-v8.pdf"),
     "cat-140gc-vs-komatsu-gd655", "motor-grader"),
    ("cat-cs56b-teknik-ozellikler", "CAT CS56B",
     "CAT CS56B tek tamburlu silindirin resmi Caterpillar teknik özellikleri: çalışma ağırlığı, motor gücü, tambur genişliği.",
     "Caterpillar CS56B, zemin sıkıştırma (silindir) segmentinde CAT'in güncel nesil modelidir. Aşağıdaki veriler doğrudan Caterpillar'ın resmi bayi kaynaklı sayfasından alınmıştır.",
     [("Çalışma Ağırlığı (kabinli)", "11.500 kg"), ("Motor", "Cat C4.4 ACERT"), ("Motor Gücü", "117 kW (157 HP)"), ("Tambur Genişliği", "2.134 mm")],
     ("Caterpillar CS56B resmi ürün sayfası (bayi kaynaklı)", "https://www.petersoncat.com/products/new/vibratory-soil-compactors/cs56b"),
     "cat-cs56b-vs-bomag-bw213", "road-roller"),
    ("bomag-bw213-d5-teknik-ozellikler", "Bomag BW213 D-5",
     "Bomag BW213 D-5 tek tamburlu silindirin resmi Bomag teknik özellikleri: çalışma ağırlığı, motor gücü, tambur genişliği.",
     "Bomag BW213 D-5, zemin sıkıştırma segmentinde CAT CS56B'nin doğrudan rakibidir. Aşağıdaki veriler doğrudan Bomag'ın resmi ürün sayfasından alınmıştır.",
     [("Çalışma Ağırlığı", "12.600 kg"), ("Motor Gücü", "95 kW (127 HP)"), ("Tambur Genişliği", "2.130 mm"), ("Emisyon Standardı", "Stage IV / Tier 4f")],
     ("Bomag BW 213 D-5 resmi ürün sayfası", "https://www.bomag.com/ww-en/machinery/categories/single-drum-rollers-soil-compactors/single-drum-rollers/bw-213-d-5-58615/"),
     "cat-cs56b-vs-bomag-bw213", "road-roller"),
]

MACHINE_SPEC_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} Teknik Özellikler — {site_name}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="js/analytics.js"></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "{base_url}/"}},
    {{"@type": "ListItem", "position": 2, "name": "{name} Teknik Özellikler", "item": "{canonical}"}}
  ]
}}
</script>
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <h1>{name} Teknik Özellikler</h1>
    <p>{intro}</p>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <div class="calc-panel" style="overflow-x:auto">
      <table class="compare-table">
        <tbody>
          {rows}
        </tbody>
      </table>
      <p class="calc-note">Kaynak: <a href="{source_url}" target="_blank" rel="noopener">{source_label}</a></p>
      <div class="calc-cta">
        <a href="https://wa.me/{wa}?text={wa_text}" class="btn btn-primary" style="width:100%" target="_blank" rel="noopener">Bu Model İçin Teklif Al →</a>
      </div>
    </div>

    <div class="calc-panel" style="margin-top:24px">
      <h3 style="margin-top:0">İlgili Sayfalar</h3>
      <ul>
        <li><a href="{compare_href}">{compare_label}</a></li>
        <li><a href="makineler/{category_slug}.html">{category_label}</a></li>
      </ul>
    </div>
  </div>
</section>

{footer}

<script src="js/lib/supabase.min.js"></script>
<script src="js/auth.js"></script>
<script src="js/advisor-widget.js"></script>
</body>
</html>
"""


def build_machine_spec_pages(root_dir):
    wa_generic = wa_link_text("Hi, I'd like more information about GND Machinery.")
    header = HEADER.format(root="", wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    compare_titles = {slug: title for slug, title, *_ in COMPARISONS}
    category_names = {slug: tr[0] for slug, name, meta, intro, icon, img, specs, tr in MACHINES}

    for slug, name, meta_desc, intro, specs, source, compare_slug, category_slug in MACHINE_SPECS:
        rows_html = "\n          ".join(
            f"<tr><td>{esc(label)}</td><td>{esc(value)}</td></tr>" for label, value in specs
        )
        wa_text = wa_link_text(f"Hi, I'd like a quote for a {name}.")
        page = MACHINE_SPEC_PAGE_TEMPLATE.format(
            name=name, site_name=SITE_NAME, meta_desc=meta_desc,
            canonical=f"{BASE_URL}/{slug}.html", base_url=BASE_URL,
            header=header, footer=footer, intro=intro, rows=rows_html,
            source_url=source[1], source_label=esc(source[0]),
            wa=WHATSAPP_NUMBER, wa_text=wa_text,
            compare_href=f"{compare_slug}.html", compare_label=esc(f"{compare_titles[compare_slug]}"),
            category_slug=category_slug, category_label=esc(f"{category_names[category_slug]} kategorisine göz atın"),
        )
        with open(os.path.join(root_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  wrote {slug}.html")


COMPARISON_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {site_name}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="js/analytics.js"></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": "{base_url}/"}},
    {{"@type": "ListItem", "position": 2, "name": "{title}", "item": "{canonical}"}}
  ]
}}
</script>
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <h1>{title}</h1>
    <p>Aşağıdaki veriler her iki üreticinin de kendi resmi teknik dokümanlarından alınmıştır. Amacımız size bir tercih dayatmak değil, karar vermeniz için doğru ve kaynaklı bilgi sunmaktır.</p>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <div class="calc-panel" style="overflow-x:auto">
      <table class="compare-table">
        <thead>
          <tr><th>Özellik</th><th>{machine_a}</th><th>{machine_b}</th></tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
      <p class="calc-note">Bu tablo bir üstünlük/aşağılık değerlendirmesi değildir — sadece resmi verilerin yan yana karşılaştırmasıdır. Hangi makinenin sizin işinize uygun olduğu; kullanım yoğunluğu, bütçe ve servis ağı gibi faktörlere göre değişir.</p>
      <div class="calc-cta">
        <a href="https://wa.me/{wa}?text={wa_text}" class="btn btn-primary" style="width:100%" target="_blank" rel="noopener">Detaylı Teknik Değerlendirme ve Teklif İçin WhatsApp →</a>
      </div>
    </div>

    <div class="calc-panel" style="margin-top:24px">
      <h3 style="margin-top:0">Kaynaklar</h3>
      <ul>
        {sources}
      </ul>
    </div>

    {detail_links_block}
  </div>
</section>

{footer}

<script src="js/lib/supabase.min.js"></script>
<script src="js/auth.js"></script>
<script src="js/advisor-widget.js"></script>
</body>
</html>
"""

COMPARISON_DETAIL_LINKS_BLOCK = """<div class="calc-panel" style="margin-top:24px">
      <h3 style="margin-top:0">Tekil Teknik Özellik Sayfaları</h3>
      <ul>
        {links}
      </ul>
    </div>"""


def build_comparison_pages(root_dir):
    out_dir = root_dir
    wa_generic = wa_link_text("Hi, I'd like more information about GND Machinery.")
    header = HEADER.format(root="", wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    spec_slug_by_name = {name: slug for slug, name, *_ in MACHINE_SPECS}

    for slug, title, meta_desc, machine_a, machine_b, spec_rows, sources in COMPARISONS:
        rows_html = "\n          ".join(
            f"<tr><td>{esc(label)}</td><td>{esc(a)}</td><td>{esc(b)}</td></tr>"
            for label, a, b in spec_rows
        )
        sources_html = "\n        ".join(
            f'<li><a href="{url}" target="_blank" rel="noopener">{esc(label)}</a></li>'
            for label, url in sources
        )
        wa_text = wa_link_text(f"Hi, I have a question about {machine_a} vs {machine_b}.")

        detail_links = [
            (name, spec_slug_by_name[name]) for name in (machine_a, machine_b) if name in spec_slug_by_name
        ]
        detail_links_block = ""
        if detail_links:
            links_html = "\n        ".join(
                f'<li><a href="{s}.html">{esc(n)} Teknik Özellikler</a></li>' for n, s in detail_links
            )
            detail_links_block = COMPARISON_DETAIL_LINKS_BLOCK.format(links=links_html)

        page = COMPARISON_PAGE_TEMPLATE.format(
            title=title, site_name=SITE_NAME, meta_desc=meta_desc,
            canonical=f"{BASE_URL}/{slug}.html", base_url=BASE_URL,
            header=header, footer=footer, machine_a=machine_a, machine_b=machine_b,
            rows=rows_html, sources=sources_html, wa=WHATSAPP_NUMBER, wa_text=wa_text,
            detail_links_block=detail_links_block,
        )
        with open(os.path.join(out_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  wrote {slug}.html")


TEKLIF_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Teklif Talebi Oluştur — {site_name}</title>
<meta name="description" content="İhtiyacınız olan makineyi seçin, saniyeler içinde kendi teklif talep özetinizi PDF olarak indirin veya WhatsApp'tan gönderin.">
<link rel="canonical" href="{base_url}/teklif-al.html">
<link rel="stylesheet" href="css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="js/analytics.js"></script>
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <h1>Teklif Talebi Oluştur</h1>
    <p>Bilgilerinizi girin, kendi teklif talep özetinizi anında PDF olarak indirin ya da WhatsApp'tan gönderin.</p>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <div class="calc-panel">
      <form id="teklifForm">
        <div class="calc-field"><label>Ad Soyad</label><input type="text" id="adSoyad" required></div>
        <div class="calc-field"><label>Firma (opsiyonel)</label><input type="text" id="firma"></div>
        <div class="calc-field"><label>Telefon veya E-posta</label><input type="text" id="iletisim" required></div>
        <div class="calc-field"><label>Makine Kategorisi</label>
          <select id="kategori">
            {machine_options}
          </select>
        </div>
        <div class="calc-field"><label>Adet</label><input type="number" id="adet" value="1" min="1" step="1"></div>
        <div class="calc-field"><label>Ek Notlar (opsiyonel)</label><textarea id="notlar" rows="3"></textarea></div>
        <button type="submit" class="btn btn-primary" style="width:100%">PDF Talep Özeti Oluştur</button>
      </form>
      <p class="calc-note">Bu araç otomatik bir talep özeti PDF'i oluşturur, kesin fiyat teklifi değildir. Ekibimiz size dönüş yapacaktır.</p>
      <div id="waSendBox" style="display:none" class="calc-cta">
        <a id="waSendLink" class="btn btn-primary" style="width:100%" target="_blank" rel="noopener">Aynı Talebi WhatsApp'tan da Gönder →</a>
      </div>
    </div>
  </div>
</section>

{footer}

<script src="js/lib/jspdf.umd.min.js"></script>
<script src="js/lib/notosans-font-data.js"></script>
<script src="js/logo-base64.js"></script>
<script src="js/lib/supabase.min.js"></script>
<script src="js/auth.js"></script>
<script src="js/advisor-widget.js"></script>
<script src="js/teklif.js"></script>
</body>
</html>
"""


def build_teklif_page(root_dir):
    wa_generic = wa_link_text("Hi, I'd like more information about GND Machinery.")
    header = HEADER.format(root="", wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    options = "\n            ".join(
        f'<option value="{slug}">{name_tr}</option>' for slug, name, *_rest, tr in MACHINES
        for name_tr in [tr[0]]
    )
    page = TEKLIF_PAGE_TEMPLATE.format(
        site_name=SITE_NAME, base_url=BASE_URL, header=header, footer=footer,
        machine_options=options,
    )
    with open(os.path.join(root_dir, "teklif-al.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print("wrote teklif-al.html")


GIRIS_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Giriş Yap / Kayıt Ol — {site_name}</title>
<meta name="description" content="GND Machinery müşteri hesabınıza giriş yapın veya yeni hesap oluşturun.">
<link rel="canonical" href="{base_url}/giris.html">
<link rel="stylesheet" href="css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="js/analytics.js"></script>
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <h1 id="authPageTitle">Giriş Yap</h1>
    <p>Hesabınla önceki teklif taleplerini görebilirsin.</p>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <div class="calc-panel">
      <form id="authForm">
        <div class="calc-field" id="authAdSoyadField" style="display:none"><label>Ad Soyad</label><input type="text" id="authAdSoyad"></div>
        <div class="calc-field" id="authTelefonField" style="display:none"><label>Telefon</label><input type="text" id="authTelefon" placeholder="05XX XXX XX XX"></div>
        <div class="calc-field"><label>E-posta</label><input type="email" id="authEmail" required></div>
        <div class="calc-field"><label>Şifre</label><input type="password" id="authPassword" required minlength="6"></div>
        <button type="submit" class="btn btn-primary" style="width:100%" id="authSubmitBtn">Giriş Yap</button>
      </form>
      <p id="authMessage" class="calc-note" style="display:none"></p>
      <p class="calc-note" style="margin-top:16px">
        <a href="#" id="authToggleMode">Hesabın yok mu? Kayıt ol</a>
      </p>
    </div>
  </div>
</section>

{footer}

<script src="js/lib/supabase.min.js"></script>
<script src="js/auth.js"></script>
<script src="js/advisor-widget.js"></script>
<script src="js/auth-page.js"></script>
</body>
</html>
"""

HESABIM_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hesabım — {site_name}</title>
<meta name="description" content="GND Machinery hesabınız ve önceki teklif talepleriniz.">
<link rel="canonical" href="{base_url}/hesabim.html">
<link rel="stylesheet" href="css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="js/analytics.js"></script>
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <h1>Hesabım</h1>
    <p id="hesabimEmail">Yükleniyor...</p>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <div class="calc-panel" style="max-width:760px">
      <h3 style="margin-top:0">Teklif Taleplerim</h3>
      <div id="hesabimList">Yükleniyor...</div>
    </div>
  </div>
</section>

{footer}

<script src="js/lib/supabase.min.js"></script>
<script src="js/auth.js"></script>
<script src="js/advisor-widget.js"></script>
<script src="js/hesabim.js"></script>
</body>
</html>
"""


def build_auth_pages(root_dir):
    wa_generic = wa_link_text("Hi, I'd like more information about GND Machinery.")
    header = HEADER.format(root="", wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)

    with open(os.path.join(root_dir, "giris.html"), "w", encoding="utf-8") as f:
        f.write(GIRIS_PAGE_TEMPLATE.format(site_name=SITE_NAME, base_url=BASE_URL, header=header, footer=footer))
    print("wrote giris.html")


# (slug, title, meta_desc, date, intro, sections=[(heading, [paragraphs])], sources=[(label, url)])
# Same sourcing rule as COMPARISONS/MACHINE_SPECS: facts and figures must trace to a
# real source (government body, official industry association, professional/legal
# source, or manufacturer/dealer documentation) — never estimated or invented.
BLOG_POSTS = [
    ("is-makinesi-operator-guvenligi-sik-yapilan-hatalar",
     "İş Makinesi Operatöründe En Sık Yapılan 3 Güvenlik Hatası",
     "Türkiye'de inşaat sektöründeki iş kazası rakamları ve iş makinesi operasyonlarında en sık yapılan 3 güvenlik hatası.",
     "2026-08-08",
     "İnşaat sektörü, Türkiye'de ölümlü iş kazalarının önemli bir bölümünün yaşandığı alanlardan biri. Bu yazıda güncel rakamları ve sahada en sık karşılaşılan 3 güvenlik hatasını ele alıyoruz.",
     [
         ("Rakamlarla Durum",
          ["Çalışma ve Sosyal Güvenlik Bakanlığı'na bağlı Güvenli İnşaat platformunun yayınladığı verilere göre 2024 yılında inşaat sektöründe 86.736 iş kazası meydana geldi, 552 çalışan hayatını kaybetti. Sektörün yüz bin çalışanda ölüm oranı (mortalite hızı) 27,7 olarak hesaplandı.",
           "İnşaat sektörü, Türkiye'deki ölümlü iş kazalarının yaklaşık üçte birinin yaşandığı bir alan. Bu tablo, iş makinesi operasyonlarında güvenliğin neden bir tercih değil, zorunluluk olduğunu açıkça gösteriyor."]),
         ("1. Sertifikasız veya Yetersiz Eğitimli Operatör",
          ["İş makinesi kullanımı, sadece makineyi hareket ettirebilmek değil; sahadaki diğer çalışanları, çevredeki yapıları ve makinenin kendisini de gözeten bir sorumluluktur. Sertifikasız ya da yetersiz eğitimli bir operatörün saha koşullarını doğru okuyamaması, kazaların en sık rastlanan nedenlerinden biri."]),
         ("2. Aksatılan Periyodik Bakım",
          ["Bakımı aksatılan bir makinede fren, hidrolik sistem veya görüş açısını etkileyen ekipmanlar zamanla güvenlik risk taşımaya başlar. Düzenli bakım, sadece makinenin ömrünü değil, sahadaki güvenliği de doğrudan etkiler."]),
         ("3. Sahada İş Güvenliği Tedbirlerinin İhmali",
          ["Baret, uyarı sinyalizasyonu, güvenlik mesafesi gibi temel tedbirlerin atlanması, kaza riskini artırmanın yanında; bir kaza yaşandığında işveren ve saha yöneticisi için hukuki sorumluluk doğurabiliyor."]),
     ],
     [("Güvenli İnşaat (ÇSGB) — 2024 Yılı SGK İş Kazası İstatistikleri", "https://guvenliinsaat.csgb.gov.tr/haberler/2024-yili-sgk-is-kazasi-istatistikleri-yayinlandi/")]),

    ("is-makinesinde-yakit-tasarrufu-operator-aliskanliklari",
     "İş Makinesinde Yakıt Tasarrufu: Operatör Alışkanlıkları Neden Motor Teknolojisinden Daha Önemli?",
     "İş makinesinde yakıt tüketimini en çok etkileyen faktör operatör alışkanlıkları. Ani hızlanma, rölanti ve doğru vites kullanımı ile yakıt tasarrufu nasıl sağlanır?",
     "2026-08-08",
     "Bir makinenin teknik olarak ne kadar verimli ve modern olduğu önemli, ama sürüş alışkanlıkları bilinçsizse bu verimlilik kağıt üzerinde kalır. Yakıt tüketimini en çok etkileyen faktör, çoğu zaman motor teknolojisinden çok operatörün kullanım alışkanlıklarıdır.",
     [
         ("Ani Hızlanma ve Sert Kullanım",
          ["Ani hızlanmalar, sert frenlemeler ve gereksiz gazlama, yakıt tüketimini belirgin şekilde artıran faktörler arasında yer alıyor. Yumuşak ve öngörülü kullanım, aynı işi daha az yakıtla tamamlamayı mümkün kılıyor."]),
         ("Gereksiz Rölanti Süresi",
          ["Boşta çalışan motor, iş yapmadan yakıt tüketmeye devam eder. Sahada makinenin gerçekten ihtiyaç duyulmadığı sürelerde rölantide bekletilmesi, uzun vadede ciddi bir yakıt kaybına dönüşebilir."]),
         ("Doğru Vites ve Mod Kullanımı",
          ["Yanlış vites seçimi motor devrini gereksiz yükseltip yakıt tüketimini artırabilir. Modern makinelerdeki 'Eco' modu, operatörün agresif gaz kullanımını dahi filtreleyerek motora yalnızca o an gereken optimum yakıtı gönderecek şekilde tasarlanmıştır — ama bu mod da doğru kullanılmadığında beklenen tasarrufu sağlamaz."]),
         ("Sonuç: Eğitim, Teknolojiden Önce Gelir",
          ["Doğru kullanım alışkanlıkları kazandırmak amacıyla verilecek operatör eğitimi, tek başına önemli ölçüde yakıt tasarrufu sağlayabilir — üstelik hiçbir ek donanım yatırımı gerektirmeden."]),
     ],
     [("PetrolTTS — Yakıt Tüketimi Nasıl Azaltılır? Filo Perspektifi ile Pratik Yöntemler", "https://petroltts.com.tr/yakit-tuketimi-nasil-azaltilir-filo-perspektifi-ile-pratik-yontemler/")]),

    ("sahte-yedek-parca-nasil-anlasilir",
     "Sahte Yedek Parçayı Bu 5 Yöntemle Tespit Edin",
     "İş makinesi yedek parçasında sahtecilik riskine karşı hologram, seri numarası, karekod ve fiyat kontrolü ile orijinal parça nasıl anlaşılır?",
     "2026-08-08",
     "İş makinesi yedek parçasında sahtecilik, hem makinenin ömrünü kısaltıyor hem de beklenmedik arızalara yol açabiliyor. İşte orijinal parçayı sahtesinden ayırmak için kontrol edebileceğiniz 5 nokta.",
     [
         ("1. Hologram ve Güvenlik Etiketleri",
          ["Orijinal parça ambalajlarında genellikle taklit edilmesi zor hologram etiketleri bulunur. Bu etiketler ışık altında renk değiştirir veya üç boyutlu bir görüntü verir — düz, tek renkli bir etiket şüphe uyandırmalı."]),
         ("2. Seri Numarası Doğrulama",
          ["Üretilen parçalar genellikle firmanın veritabanına kayıtlı bir seri numarasıyla işaretlenir. Üreticinin web sitesinde bir doğrulama paneli varsa, seri numarasını buradan sorgulamak mümkün."]),
         ("3. Karekod / QR Kod Kontrolü",
          ["Ambalajdaki karekodu mobil uygulamayla okutarak ürünün orijinalliğini üretici veritabanından anlık olarak sorgulayabilirsiniz."]),
         ("4. Ambalaj ve İşçilik Kalitesi",
          ["Yazım hataları, soluk renkler, özensiz yapıştırılmış etiketler ve kalitesiz baskı sahtecilik işareti olabilir. Parçanın kendisinde de ağırlık farkı, yüzey işlemi ve boya kalitesi dikkatle incelenmeli."]),
         ("5. Fiyat ve Satıcı Kontrolü",
          ["Piyasa ortalamasının belirgin şekilde altındaki teklifler çoğu zaman bir tuzak. Satıcının iletişim bilgilerini, fiziksel adresini ve referanslarını doğrulamak, sahte parça riskini büyük ölçüde azaltır."]),
     ],
     [("AloParça — Sahte Yedek Parça Nasıl Anlaşılır?", "https://aloparca.com/blog-detay/sahte-yedek-parca-nasil-anlasilir")]),

    ("yatirim-tesvik-belgesi-is-makinesi-ithalati-vergi-avantajlari",
     "İş Makinesi İthalatında Yatırım Teşvik Belgesi İle Vergi Avantajları",
     "Yatırım Teşvik Belgesi kapsamında iş makinesi ithalatında gümrük vergisi muafiyeti ve KDV istisnası nasıl işliyor?",
     "2026-08-08",
     "Yatırım Teşvik Belgesi, iş makinesi ithal eden işletmeler için önemli bir maliyet avantajı sunuyor. İşte belgenin sağladığı iki temel destek unsuru.",
     [
         ("Gümrük Vergisi Muafiyeti",
          ["Teşvik belgesi kapsamındaki yatırım malı makine ve teçhizatın ithalatı, yürürlükteki İthalat Rejimi Kararı gereğince ödenmesi gereken gümrük vergisinden muaf tutuluyor. Muafiyetin uygulanabilmesi için ithal edilecek malın 'makine ve teçhizat' niteliği taşıması gerekiyor."]),
         ("KDV İstisnası",
          ["Yatırım Teşvik Belgesi sahibi yatırımcı, yurt içi ve yurt dışından yapacağı makine-teçhizat alımlarında KDV ödemiyor. Gümrük vergisi muafiyeti ve KDV istisnası birbirinden bağımsız iki destek unsuru olup, aynı belge kapsamında bir arada uygulanabiliyor."]),
         ("Önemli: Tutarlar Her Yıl Güncelleniyor",
          ["Teşvik mevzuatındaki asgari yatırım tutarları ve destek üst sınırları her yıl yeniden değerleme oranına göre güncelleniyor. Bu nedenle bir önceki yıla ait rakamları doğrudan kullanmak yerine, başvuru anındaki güncel tutarları Sanayi ve Teknoloji Bakanlığı kaynaklarından ya da mali müşavirinizden teyit etmeniz gerekiyor."]),
     ],
     [("Sun & Sun International — İthal Makine Alımlarında Gümrük Vergisi Muafiyeti Nasıl Kullanılır?", "https://www.sunandsun.com.tr/ithal-makine-alimlarinda-gumruk-vergisi-muafiyeti-nasil-kullanilir/"),
      ("Yatırım Destek ve Tanıtım Ajansı (T.C. Cumhurbaşkanlığı) — Yatırımlarda Devlet Yardımları Hakkında Karar", "https://www.yatirimadestek.gov.tr/pdf/assets/upload/dosyalar/karar-yatirim_tesvik_uygulamalari.pdf")]),

    ("is-makinesi-kiralama-sozlesmesi-dikkat-edilmesi-gerekenler",
     "İş Makinesi Kiralama Sözleşmesinde Dikkat Edilmesi Gereken 5 Madde",
     "İş makinesi kiralarken sözleşmede mutlaka bulunması gereken teslim tutanağı, sorumluluk ve cezai şart maddeleri.",
     "2026-08-08",
     "İş makinesi kiralama, doğru sözleşme olmadan hem kiracı hem kiraya veren için risk taşıyor. İşte imzalamadan önce kontrol etmeniz gereken 5 madde.",
     [
         ("1. Teslim Tutanağı ve Makine Özellikleri",
          ["Kiralanan makinenin teknik özellikleri tek tek yazılmalı, hangi durumda (çalışma saati, hasar, aşınma) teslim edildiği fotoğraflarla birlikte tutanağa geçirilmelidir. Bu, sözleşme sonunda yaşanabilecek anlaşmazlıkların önüne geçer."]),
         ("2. Sözleşmenin Temel Maddeleri",
          ["Teslim ve iade tarihi, ödeme şekli ve bedeli, tarafların sorumlulukları ve makinenin teslim adresi sözleşmede açıkça yer almalıdır."]),
         ("3. Sorumluluk ve Sigorta",
          ["Makinenin yetkisiz, eğitimsiz veya belgesiz personel tarafından ya da amacı dışında kullanılmasından doğabilecek zararlardan genellikle kiracı sorumlu tutulur. Bu sorumluluğun sözleşmede net şekilde tanımlanması önemlidir."]),
         ("4. Operatörlü Kiralamada Ek Şartlar",
          ["Makine operatörlü kiralanıyorsa, operatörün sigortalı olduğu ve iş sağlığı-güvenliği ile makine kullanımı konusunda gerekli eğitimleri aldığı sözleşmede teyit edilmelidir."]),
         ("5. Cezai Şart",
          ["Makinenin sözleşme süresinden önce erken iadesi ya da sözleşme ihlali durumunda uygulanacak cezai şart, kiraya verenin olası zararını karşılamak için sözleşmeye eklenmelidir."]),
     ],
     [("AKKOR Hukuk Bürosu — İş Makinası Kiralama Sözleşmesi", "https://akkor.av.tr/makaleler/is-makinasi-kiralama-sozlesmesi")]),

    ("makine-kirilmasi-sigortasi-kapsam",
     "Makine Kırılması Sigortası Neleri Kapsar, Neleri Kapsamaz?",
     "İş makinesi için makine kırılması sigortasının kapsadığı ve kapsam dışı bıraktığı riskler nelerdir?",
     "2026-08-08",
     "Makine kırılması sigortası, iş makinenizi beklenmedik teknik arızalara karşı korur — ama her riski kapsamaz. İmza atmadan önce kapsamı doğru anlamak önemli.",
     [
         ("Kapsam İçinde Olanlar",
          ["Türkiye Sigorta Birliği'nin genel şartlarına göre makine kırılması sigortası; işletme kazaları, kusurlu model/imalat/montaj/malzeme, yağlama kusurları, elektrik enerjisinin kısa devre veya voltaj yükselmesinden kaynaklanan hasarları, ayrıca ani ve aşırı ısınma-soğumadan oluşan su çekiçlemesi (su darbesi) hasarlarını kapsar."]),
         ("Kapsam Dışında Kalanlar",
          ["Yangın, yangın nedeniyle yapılan söndürme/kurtarma faaliyetleri, deprem, sel-su baskını ile hırsızlık veya hırsızlığa teşebbüsten kaynaklanan zararlar makine kırılması sigortasının kapsamı dışındadır — bu riskler için ayrı bir teminat gerekir."]),
         ("İş Makineleri İçin Geniş Kasko Seçeneği",
          ["Ekskavatör, dozer, loader, vinç, forklift gibi hareketli iş makineleri için; yangın, deprem, sel, toprak çökmesi, kaya düşmesi, çarpma, çarpışma, devrilme ve talep halinde hırsızlığı da kapsayan daha geniş bir kasko teminatı ayrıca sağlanabilir."]),
         ("Poliçeyi İmzalamadan Önce",
          ["Kapsam maddeleri poliçeden poliçeye farklılık gösterebilir. Genel şartları ve varsa istisnaları sigorta şirketinizle birebir teyit etmeniz, ilerideki bir hasar talebinde sürpriz yaşamamanızı sağlar."]),
     ],
     [("Türkiye Sigorta Birliği — Makina Kırılması Sigortası Genel Şartları", "https://www.tsb.org.tr/content/Legislations/Makina_K%C4%B1r%C4%B1lmas%C4%B1_Sigortas%C4%B1_Genel_Sartlar%C4%B1.pdf")]),
]

BLOG_POST_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — {site_name}</title>
<meta name="description" content="{meta_desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="../css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="../js/analytics.js"></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "{title}",
  "description": "{meta_desc}",
  "datePublished": "{date}",
  "author": {{"@type": "Organization", "name": "GND İş Makineleri Sanayi ve Ticaret A.Ş."}},
  "publisher": {{"@type": "Organization", "name": "GND İş Makineleri Sanayi ve Ticaret A.Ş."}},
  "mainEntityOfPage": "{canonical}"
}}
</script>
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <h1>{title}</h1>
    <p>{intro}</p>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <div class="calc-panel blog-post-body">
      {content}
    </div>

    <div class="calc-panel" style="margin-top:24px">
      <h3 style="margin-top:0">Kaynaklar</h3>
      <ul>
        {sources}
      </ul>
    </div>

    <div class="calc-panel" style="margin-top:24px">
      <p class="calc-note">İhtiyacınıza uygun makine veya yedek parça tedariki için doğrudan bize ulaşın.</p>
      <a href="https://wa.me/{wa}?text={wa_text}" class="btn btn-primary" style="width:100%" target="_blank" rel="noopener">WhatsApp'tan Bize Ulaşın →</a>
    </div>

    <p class="back-link"><a href="index.html">← Tüm Yazılar</a></p>
  </div>
</section>

{footer}

<script src="../js/lib/supabase.min.js"></script>
<script src="../js/auth.js"></script>
<script src="../js/advisor-widget.js"></script>
</body>
</html>
"""

BLOG_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Blog — {site_name}</title>
<meta name="description" content="İş makinesi sahipliği, tedariki, ithalatı ve bakımı hakkında güncel ve kaynaklı yazılar.">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="../css/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-37LSLM4SE6"></script>
<script src="../js/analytics.js"></script>
</head>
<body>

{header}

<section class="hero category-hero">
  <div class="hero-inner">
    <h1>Blog</h1>
    <p>İş makinesi sahipliği, tedariki, ithalatı ve bakımı hakkında güncel ve kaynaklı yazılar.</p>
  </div>
</section>

<section class="categories-section">
  <div class="section-inner">
    <div class="category-grid">
      {cards}
    </div>
  </div>
</section>

{footer}

<script src="../js/lib/supabase.min.js"></script>
<script src="../js/auth.js"></script>
<script src="../js/advisor-widget.js"></script>
</body>
</html>
"""

BLOG_CARD = """<div class="category-card">
        <h3><a href="{slug}.html">{title}</a></h3>
        <p>{meta_desc}</p>
      </div>"""


def build_blog_pages(root_dir):
    out_dir = os.path.join(root_dir, "blog")
    os.makedirs(out_dir, exist_ok=True)
    wa_generic = wa_link_text("Hi, I'd like more information about GND Machinery.")
    header = HEADER.format(root="../", wa=WHATSAPP_NUMBER, wa_generic=wa_generic)
    footer = FOOTER.format(wa=WHATSAPP_NUMBER, wa_generic=wa_generic)

    for slug, title, meta_desc, date, intro, sections, sources in BLOG_POSTS:
        content_parts = []
        for heading, paragraphs in sections:
            content_parts.append(f"<h2>{esc(heading)}</h2>")
            for p in paragraphs:
                content_parts.append(f"<p>{esc(p)}</p>")
        content_html = "\n      ".join(content_parts)
        sources_html = "\n        ".join(
            f'<li><a href="{url}" target="_blank" rel="noopener">{esc(label)}</a></li>' for label, url in sources
        )
        wa_text = wa_link_text(f"Hi, I have a question after reading '{title}'.")

        page = BLOG_POST_TEMPLATE.format(
            title=esc(title), site_name=SITE_NAME, meta_desc=esc(meta_desc),
            canonical=f"{BASE_URL}/blog/{slug}.html", date=date, intro=esc(intro),
            header=header, footer=footer, content=content_html, sources=sources_html,
            wa=WHATSAPP_NUMBER, wa_text=wa_text,
        )
        with open(os.path.join(out_dir, f"{slug}.html"), "w", encoding="utf-8") as f:
            f.write(page)
        print(f"  wrote blog/{slug}.html")

    cards_html = "\n      ".join(
        BLOG_CARD.format(slug=slug, title=esc(title), meta_desc=esc(meta_desc))
        for slug, title, meta_desc, *_ in BLOG_POSTS
    )
    index_page = BLOG_INDEX_TEMPLATE.format(
        site_name=SITE_NAME, canonical=f"{BASE_URL}/blog/index.html",
        header=header, footer=footer, cards=cards_html,
    )
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_page)
    print("  wrote blog/index.html")

    with open(os.path.join(root_dir, "hesabim.html"), "w", encoding="utf-8") as f:
        f.write(HESABIM_PAGE_TEMPLATE.format(site_name=SITE_NAME, base_url=BASE_URL, header=header, footer=footer))
    print("wrote hesabim.html")


DETAIL_LANG_JS = """(function () {
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
"""


if __name__ == "__main__":
    root_dir = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(root_dir, "js", "detail-lang.js"), "w", encoding="utf-8") as f:
        f.write(DETAIL_LANG_JS)
    print("Wrote js/detail-lang.js")

    print("Machine pages:")
    build_pages(MACHINES, os.path.join(root_dir, "makineler"), "Machines", "makineler", "../", "yedek-parca", MACHINE_LINKS, kind="machine")
    print("Spare parts pages:")
    build_pages(SPARE_PARTS, os.path.join(root_dir, "yedek-parca"), "Spare Parts", "yedek-parca", "../", "makineler", PARTS_LINKS, kind="parts")
    print("Service pages:")
    build_pages(SERVICES, os.path.join(root_dir, "hizmetler"), "Services", "hizmetler", "../", "makineler", SERVICE_LINKS, kind="service")
    print("Calculator pages:")
    build_calculator_pages(root_dir)
    build_teklif_page(root_dir)
    build_auth_pages(root_dir)
    print("Comparison pages:")
    build_comparison_pages(root_dir)
    print("Machine spec pages:")
    build_machine_spec_pages(root_dir)
    print("Blog pages:")
    build_blog_pages(root_dir)

    urls = [(f"{BASE_URL}/", "weekly", "1.0"), (f"{BASE_URL}/kurumsal.html", "monthly", "0.6"), (f"{BASE_URL}/blog/index.html", "weekly", "0.7"), (f"{BASE_URL}/teklif-al.html", "monthly", "0.8"), (f"{BASE_URL}/giris.html", "yearly", "0.3")]
    for slug, *_ in BLOG_POSTS:
        urls.append((f"{BASE_URL}/blog/{slug}.html", "monthly", "0.6"))
    for slug, *_ in COMPARISONS:
        urls.append((f"{BASE_URL}/{slug}.html", "monthly", "0.7"))
    for slug, *_ in MACHINE_SPECS:
        urls.append((f"{BASE_URL}/{slug}.html", "monthly", "0.7"))
    for slug, *_ in MACHINES:
        urls.append((f"{BASE_URL}/makineler/{slug}.html", "monthly", "0.8"))
    for slug, *_ in SPARE_PARTS:
        urls.append((f"{BASE_URL}/yedek-parca/{slug}.html", "monthly", "0.7"))
    for slug, *_ in SERVICES:
        urls.append((f"{BASE_URL}/hizmetler/{slug}.html", "monthly", "0.7"))
    for slug, *_ in CALCULATORS:
        urls.append((f"{BASE_URL}/hesaplama-araclari/{slug}.html", "monthly", "0.7"))
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, freq, pri in urls:
        sitemap.append(f"<url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{pri}</priority></url>")
    sitemap.append("</urlset>")
    with open(os.path.join(root_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap) + "\n")
    print(f"sitemap.xml updated ({len(urls)} URLs).")
    print("Done.")
