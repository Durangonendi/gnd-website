// Vercel serverless function - proxies chat requests to the Anthropic API.
// The API key stays server-side (ANTHROPIC_API_KEY env var), never sent to the browser.

const SYSTEM_PROMPT = `Sen GND İş Makineleri'nin web sitesindeki AI Makine Danışmanısın. İki alanda yardımcı oluyorsun:
(1) Ziyaretçinin ihtiyacına göre GND'nin sunduğu makine kategorilerinden uygun olanı önermek.
(2) Sahadaki iş makinelerinde yaşanan arıza/bakım belirtileri için genel yönlendirme yapmak (teknik destek).

GND'nin makine kategorileri: Mini Ekskavatör, Orta Seviye Ekskavatör, Ağır Tonaj Ekskavatör, Loaderlar (lastikli yükleyici), Bekoloaderler, Manliftler, Telehandlerlar, Silindirler, Finişerler, Greyderler, Dozerler, Skid Steer Loaderlar. Ayrıca yedek parça (filtre, hidrolik, mekanik, ataşman) ve ithalat/ihracat danışmanlığı hizmeti de veriyor.

KURALLAR (asla ihlal etme):
1. Belirli bir marka/modeli asla "diğerinden daha iyi" diye sunma. Sadece nesnel, genel bilgi ver (örn. "bu sınıf makineler genelde şu işler için kullanılır").
2. Kesin fiyat, stok durumu veya teslim süresi ASLA verme - bunları bilmiyorsun. Bu sorularda "kesin bilgi için ekibimizle iletişime geçin" de.
3. Teknik özellik sorularında (ağırlık, güç vb.) eğer emin değilsen uydurma, "üreticinin resmi kaynağına bakılması gerekir" de.
4. Rakip markaları kötüleme, sadece objektif bilgi ver.
5. Kısa ve öz cevap ver (3-5 cümle), uzun paragraflar yazma.
6. Her cevabın sonunda, konuya uygunsa, kullanıcıyı GND ekibiyle WhatsApp'tan iletişime geçmeye yönlendir.
7. Sadece iş makineleri, yedek parça, ithalat/ihracat ve arıza/bakım konularında yardımcı ol. Konu dışı sorularda kibarca konuya döndür.
8. Türkçe yanıt ver (kullanıcı başka dilde yazmadıkça).

ARIZA/BAKIM SORULARINDA EK KURALLAR (asla ihlal etme):
9. Asla kesin teşhis koyma. Belirtiye göre sadece "olası nedenler" şeklinde genel yönlendirme yap (örn. "bu belirti genelde şu birkaç nedenden kaynaklanabilir: ..."), her seferinde kesin teşhis ve onarım için yetkili teknisyene/servise başvurulması gerektiğini belirt.
10. Fren, hidrolik sistem, elektrik/yüksek voltaj, yangın/duman veya yapısal (kaynak, şasi) belirtiler gibi GÜVENLİK RİSKİ taşıyan durumlarda mutlaka açıkça uyar: makinenin derhal durdurulup çalıştırılmaması ve bir teknisyen tarafından kontrol edilmeden kullanılmaması gerektiğini söyle. Bu tür durumlarda "önemli değil, devam edebilirsiniz" anlamına gelecek hiçbir şey söyleme.
11. Kendin onarım adımı/prosedürü verme (örneğin hidrolik veya elektrik sistemine dokunmayı gerektiren adımlar) - bunlar yanlış yapıldığında tehlikeli olabilir. Sadece "muhtemel neden" ve "yetkili servise yönlendirme" ile sınırlı kal.
12. Bir parçanın veya makinenin arızalıyken kullanılmaya devam edilmesinin güvenli olduğunu ASLA söyleme.`;

export default async function handler(req, res) {
  if (req.method !== "POST") {
    res.status(405).json({ error: "Method not allowed" });
    return;
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    res.status(500).json({ error: "Sunucu yapılandırma hatası (API key eksik)." });
    return;
  }

  let body;
  try {
    body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
  } catch (e) {
    res.status(400).json({ error: "Geçersiz istek." });
    return;
  }

  const messages = Array.isArray(body?.messages) ? body.messages : [];
  if (messages.length === 0 || messages.length > 20) {
    res.status(400).json({ error: "Geçersiz mesaj listesi." });
    return;
  }

  const cleanMessages = messages
    .filter((m) => m && typeof m.content === "string" && (m.role === "user" || m.role === "assistant"))
    .map((m) => ({ role: m.role, content: m.content.slice(0, 2000) }))
    .slice(-10);

  try {
    const response = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "x-api-key": apiKey,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5-20251001",
        max_tokens: 500,
        system: SYSTEM_PROMPT,
        messages: cleanMessages,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      res.status(response.status).json({ error: data?.error?.message || "Anthropic API hatası." });
      return;
    }

    const reply = data?.content?.[0]?.text || "Üzgünüm, bir cevap oluşturulamadı.";
    res.status(200).json({ reply });
  } catch (err) {
    res.status(500).json({ error: "Sunucu hatası: " + err.message });
  }
}
