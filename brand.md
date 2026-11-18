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

### Ana Kurumsal Renkler (Primary Palette - Yüksek Güven & Akademik Prestij)
| Görünüm | Renk Adı | Hex Kodu | Kullanım Alanı ve Anlamı |
| :---: | :--- | :--- | :--- |
| 🍷 | **İÜ Bordo (Imperial Burgundy)** | `#7f1d1d` / `#881337` | Üniversitenin resmi kurumsal rengi, ana marka vurguları, birincil butonlar (`btn-burgundy`). |
| 🌿 | **Mat Akademik Zümrüt (Botanical Seal Green)** | `#064e3b` / `#022c22` | Logo ve mühür zemininde asırlık Beyazıt çınarlarını, köklü gelişimi ve ağırbaşlılığı simgeler. |
| 👑 | **Antik İÜ Altını (Antique Prestige Gold)** | `#c59b27` / `#d4af37` | Yüksek güven veren mat altın varak, rozetler, mühür kenarlığı ve akademik detaylar (neon ışıltılardan arındırılmış). |
| 🏛️ | **Derin Gece / Beyazıt Mavisi** | `#080c16` / `#111827` | Sayfa ve kart zeminleri; kurumsal ağırlığı ve modernliği pekiştirir. |
| 🔘 | **Kurumsal Bilgi Grisi (Institutional Meta)** | `#94a3b8` / `#64748b` | Rektörlük ve koordinatörlük alt bilgileri, tarihler ve yardımcı metinler. |

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
    --iu-gold: #c59b27;              /* İÜ Ağırbaşlı Altın */
    --iu-gold-light: #d4af37;        /* Antik İpek Altın Varak */
    --iu-gold-glow: rgba(212, 175, 55, 0.20); /* Bahis sitesi parıltısından uzak mat ışıltı */
    --logo-green-start: #064e3b;     /* Mühür Derin Zümrüt Başlangıç */
    --logo-green-end: #022c22;       /* Mühür Koyu Botanik Bitiş */
    --logo-gold-border: #d4af37;     /* Mühür 1.5px Antik Altın Çerçeve */
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

## 🏛️ 4. Arayüz ve Görsel Dil (UI/UX - Yüksek Güven & Saygınlık)

* **Kurumsal Meta Hiyerarşisi (`.brand-meta`):**
  Önceki versiyonlarda en tepede yer alan ve bahis/kampanya sitelerini andıran bağımsız üst bant (`.iu-top-strip`) tamamen kaldırılarak arayüz sadeleştirilmiştir. Bunun yerine kurumsal aidiyet:
  - **`🏛️ İstanbul Üniversitesi`** (`.brand-title`, `Cinzel`, 1.15rem, beyaz)
  - **`MEZUN BİLGİ & KARİYER AĞI`** (`.brand-sub`, antik altın `#d4af37`, 0.74rem)
  - **`Rektörlük Mezunlar Koordinatörlüğü • Kuruluş 1453`** (`.brand-meta`, kurumsal gri `#94a3b8`, 0.68rem, zarif ve okunaklı)
  olarak logonun hemen yanındaki marka bloğunda tek ve yüksek güvenli bir hiyerarşide konumlandırılmıştır.
* **Açık Mimari Beyazıt Kitabesi (Ağırbaşlı / Mat Stil):**  
  Ana manşetin (`H1`) üzerinde yer alan tarihi miras ifadesi, yapay baloncuk veya neon ışık animasyonlarından arındırılarak Beyazıt Tarihi Kapısı'nın taş frizlerine uygun **açık çizgisel mimari kitabe** olarak yerleştirilir:
  - Üst hat: İki yana zarifçe süzülen ince çizgiler (`inscription-hairline`), merkezde asil antik altın ile yazılmış **`1453`** yılı.
  - Alt hat: İki yanında `⚜️` motifleri ve `Cinzel` inscriptional serif yazı karakteriyle:  
    **`⚜️ Beyazıt'ın Asırlık Bilgi Işığı • Geleceğe Kök Salan Miras ⚜️`**
  - Güven Veren Doku: Yanıp sönen casino beacon ışıkları veya göz yoran neon sarı degradeler yerine mat antik altın ve gümüşi beyaz tipografi hakimdir.
* **Rafine Aksiyon Butonu — `İlanları İncele` (`.btn-nav-cta`):**  
  Platform genelinde pasif ve jenerik ifadeler yerine, kurumsal bordoyu antik altın yansımalar ve mikro-etkileşimlerle taçlandıran özel buton mimarisi kullanılır:
  - Zemin: `linear-gradient(135deg, #881337 0%, #700d2b 55%, #4c0519 100%)`
  - Çerçeve: `1px solid rgba(212, 175, 55, 0.45)`
  - Ok Çipi (`.btn-arrow-chip`): Butonun sağında ayrı bir yarı saydam altın kare içinde yer alan ve hover durumunda sağa doğru süzülen `→` oku.
  - Doğrudan Başvuru: **`💼 Mezun İlanlarına Göz At`** / **`📝 Platformdan Başvur`**
  - Üye Keşfi: **`👥 Mezunlarımızı Keşfet`**
* **Fakülte Rozetleri:** Hukuk, Tıp, İktisat, İletişim, Edebiyat, Fen, Mühendislik gibi fakültelere özel mikro etiketler.
* **Köşe Yuvarlaklığı & Gölge:** Kurumsal ciddiyeti modernizmle birleştiren `12px` - `18px` kart eğriliği ve doğal derin gölgeler.

---

## 🏷️ 5. Logo & Mühür (Mat Yeşil & Antik Altın Sistemi)

* **Marka Mührü (Brand Seal):**  
  Üniversitenin tarihi Beyazıt kapısı meşale ve köklülüğünü yansıtmak üzere **Mat Zümrüt Yeşili zemin (`linear-gradient(145deg, #064e3b 0%, #022c22 100%)`)** üzerine **1.5px Antik Altın (`#d4af37`)** çerçeve ile donatılmıştır. Bahis sitesi izlenimi veren aşırı neon haleler kaldırılmış, doğal derin gölge (`box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35)`) ile akademiye yaraşır bir ağırlık verilmiştir.
* **Sembol:** İstanbul Üniversitesi Meşalesi & Tarihi Taç Motifi (`🏛️` / `🎓`).
* **Kurumsal İsim:** **İstanbul Üniversitesi Mezun Bilgi ve Kariyer Ağı** (*IU Alumni*).
* **Resmi Slogan:** *"1453'ten Geleceğe: Mezunlarımızın Işığında Birlikte İleriye."*

---

## 🔗 6. İlgili Belgeler ve Bağlantılar

* 🏠 **Genel Proje Özeti:** [README.md](README.md)
* 🗄️ **Veritabanı ve İlişki Modeli (ERD):** [ddd.md](ddd.md)
* 💻 **Ana Sayfa:** [`index.html`](index.html)
* 🛡️ **Hata Koruyucuları (Guardians):** [`404.html`](404.html) &bull; [`middlewares/`](middlewares/)
