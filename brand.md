# 🏛️ İstanbul Üniversitesi Mezun Bilgi Sistemi (İÜ Mezun Ağı) — Kurumsal Marka & Tasarım Rehberi

Bu belge, **İstanbul Üniversitesi (İÜ) Mezun ve Kariyer Ağı Platformu** için kurumsal kimlik, tarihi marka değerleri, resmi renk paleti (Bordo & Altın Sarısı), tipografi ve modern UI/UX tasarım standartlarını belirler.

---

## 📌 1. Marka Kimliği & Misyon (1453'ten Günümüze)

İstanbul Üniversitesi, Türkiye'nin en köklü ve öncü yükseköğretim kurumudur. Bu platform; 1453'ten bu yana yetişen yüzbinlerce mezun ile geleceğin liderleri olan mevcut öğrencileri, akademik kadroyu ve iş dünyasını birbirine bağlar.

### Temel Marka Değerleri:
* **Tarihi Köklülük & Prestij:** Beyazıt Tarihi Kapısı, kurumsal asalet ve akademik liyakat.
* **Nesiller Arası Köprü:** Kıdemli mezunlar ile üniversiteye yeni adım atan öğrencilerin mentorluk ve staj dayanışması.
* **Modern Teknolojik Güç:** Tarihi mirası en yeni nesil web standartları, REST API ve kesintisiz mimariyle buluşturma.
* **Aidiyet & Gurur:** *"Dünyanın En Köklü Üniversitelerinden Birinin Mezunuyum"* gururunu yaşatma.

---

## 🎨 2. Resmi Kurumsal Renk Sistemi

Tasarım sistemi, İstanbul Üniversitesi'nin asırlık resmi renkleri olan **Bordo (İÜ Bordo)** ve **Altın Sarısı / Varak Sarısı (İÜ Altın)** etrafında şekillendirilmiştir. Arka plan ve kartlarda ise modern koyu lacivert/derin gece tonları ile altın yansımalar harmanlanmıştır.

### Ana Kurumsal Renkler (Primary Palette)
| Görünüm | Renk Adı | Hex Kodu | Kullanım Alanı ve Anlamı |
| :---: | :--- | :--- | :--- |
| 🍷 | **İÜ Bordo (Imperial Burgundy)** | `#7f1d1d` / `#991b1b` / `#881337` | Üniversitenin resmi kurumsal rengi, ana marka vurguları, birincil butonlar (`btn-burgundy`). |
| 🌿 | **Akademik Zümrüt Yeşili (Botanical Seal Green)** | `#065f46` / `#047857` | Logo ve mühür zemininde asırlık Beyazıt çınarlarını, köklü gelişimi ve canlılığı simgeler. |
| 👑 | **İÜ Altın Sarısı (Heritage Gold)** | `#f59e0b` / `#d97706` | Başarı, mezuniyet diploması simgesi, rozetler, yıldızlar ve altın detaylar. |
| ✨ | **Parlak Varak & Güneş Sarısı (Solar Gold Glow)** | `#fbbf24` / `#fef08a` | Logo çerçevesi, mühür parıltısı, aktif sekme vurgusu ve manşet degradeleri. |
| 🏛️ | **Derin Gece / Beyazıt Mavisi** | `#080c16` / `#111827` | Sayfa ve kart zeminleri; kurumsal ağırlığı ve modernliği pekiştirir. |

### Semantik Durum Renkleri
| Görünüm | Durum | Hex Kodu | Kullanım Alanı |
| :---: | :--- | :--- | :--- |
| 🟢 | **Başarı (Success)** | `#10b981` | Aktif mezun kaydı, onaylanmış iş başvurusu, 200/201 yanıtları. |
| 🟡 | **Beklemede (Warning)** | `#f59e0b` | İncelenmeyi bekleyen başvurular, taslak ilanlar. |
| 🔴 | **Hata / Uyarı (Danger)** | `#dc2626` | 404/500 hata koruyucuları (Guardians), silme ve ret işlemleri. |
| ⚪ | **Ana Metin (Pure Light)** | `#f8fafc` | Okunabilirliği yüksek birincil başlıklar ve metinler. |
| 🔘 | **İkincil Metin (Muted Slate)** | `#94a3b8` | Fakülte adları, mezuniyet yılları ve alt bilgiler. |

### Zemin ve Yüzey Belirteçleri (CSS Tokens)
```css
:root {
    --iu-burgundy: #881337;          /* İÜ Bordo */
    --iu-burgundy-hover: #9f1239;    /* İÜ Bordo Hover */
    --iu-gold: #d97706;              /* İÜ Kurumsal Altın */
    --iu-gold-light: #fbbf24;        /* Parlak Varak & Güneş Sarısı */
    --iu-gold-glow: rgba(245, 158, 11, 0.28);
    --logo-green-start: #065f46;     /* Mühür Zümrüt Yeşili Başlangıç */
    --logo-green-end: #047857;       /* Mühür Zümrüt Yeşili Bitiş */
    --logo-yellow-border: #fbbf24;   /* Mühür Altın Sarısı Çerçeve */
    --bg-body: #080c16;              /* Beyazıt Gece Mavisi Zemin */
    --card-surface: #111827;         /* Yüzey Kartı */
    --card-border: #1f293d;          /* Kart Çerçevesi */
}
```

---

## 🔤 3. Tipografi Standartları

1. **Başlıklar & Manşetler:** `Cinzel` (Anıtsal Latin ve Beyazıt kitabe zarafeti için)
   * Kalınlık: `700 (Bold)`, `800 (Extra Bold)`
   * Kullanım: "İstanbul Üniversitesi Mezunlar Ağı", bölüm başlıkları, kurumsal üst bant, kitabe metinleri.
2. **Gövde Metinleri & Arayüz:** `Plus Jakarta Sans`
   * Kalınlık: `400 (Regular)`, `500 (Medium)`, `600 (Semi-Bold)`, `700 (Bold)`
   * Kullanım: Profil açıklamaları, iş ilanı detayları, buton etiketleri (`İlanları İncele →`), navigasyon.
3. **Kod & Metrik Göstergeleri:** `JetBrains Mono`
   * Kullanım: Öğrenci / Mezun ID numaraları (`#1453`), REST API rotaları, terminal logları.

---

## 🏛️ 4. Arayüz ve Görsel Dil (UI/UX)

* **Tarihi Beyazıt Kitabesi & Canlı İlim Işığı (Heritage Crest):**  
  Ana manşetin üzerinde yer alan "1453'ten Geleceğe: Beyazıt'ın Asırlık Bilgi Işığı" ifadesi; klasik düz bir hap rozet yerine, iki kademeli mimari kitabe olarak sunulur:
  - Sol blok: Zümrüt yeşili zemin üzerine parlayan altın çerçeveli `[ 1453 ]` mühür tag'i ve canlı nabız gibi atan altın-zümrüt `heritage-beacon` ışığı.
  - Sağ blok: İki yanında `⚜️` altın zambak/defne motifleri, `Cinzel` inscriptional serif yazı stili ve yatay altın-zümrüt degradeli cam yüzey.
* **Aksiyon Butonları (Call to Action - CTA):**  
  Platform genelinde pasif ve jenerik ifadeler yerine eyleme dönük kurumsal standartlar kullanılır:
  - Birincil İnceleme: **`İlanları İncele →`** (eski: *Fırsatları İncele*)
  - Doğrudan Başvuru: **`💼 Mezun İlanlarına Göz At`** / **`📝 Platformdan Başvur`**
  - Üye Keşfi: **`👥 Mezunlarımızı Keşfet`**
* **Fakülte Rozetleri:** Hukuk, Tıp, İktisat, İletişim, Edebiyat, Fen, Mühendislik gibi fakültelere özel mikro etiketler.
* **Köşe Yuvarlaklığı & Gölge:** Kurumsal ciddiyeti modernizmle birleştiren `12px` - `18px` kart eğriliği ve altın ışıltılı derin gölgeler.

---

## 🏷️ 5. Logo & Mühür (Yeşil & Sarı / Altın Sistemi)

* **Marka Mührü (Brand Seal):**  
  Üniversitenin tarihi Beyazıt kapısı meşale ve köklülüğünü yansıtmak üzere **Zümrüt Yeşili zemin (`#065f46` $\rightarrow$ `#047857`)** üzerine **Parlak Varak Sarısı (`#fbbf24`)** 2px çerçeve ile donatılmıştır. Çevresinde güneş sarısı ve zümrüt ışığı yayar (`box-shadow: 0 4px 18px rgba(251, 191, 36, 0.35)`).
* **Sembol:** İstanbul Üniversitesi Meşalesi & Tarihi Taç Motifi (`🏛️` / `🎓`).
* **Kurumsal İsim:** **İstanbul Üniversitesi Mezun Bilgi ve Kariyer Ağı** (*IU Alumni*).
* **Resmi Slogan:** *"1453'ten Geleceğe: Mezunlarımızın Işığında Birlikte İleriye."*

---

## 🔗 6. İlgili Belgeler ve Bağlantılar

* 🏠 **Genel Proje Özeti:** [README.md](README.md)
* 🗄️ **Veritabanı ve İlişki Modeli (ERD):** [ddd.md](ddd.md)
* 💻 **Ana Sayfa:** [`index.html`](index.html)
* 🛡️ **Hata Koruyucuları (Guardians):** [`404.html`](404.html) &bull; [`middlewares/`](middlewares/)
