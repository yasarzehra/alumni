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
| 🍷 | **İÜ Bordo (Imperial Burgundy)** | `#7f1d1d` / `#991b1b` | Üniversitenin resmi kurumsal rengi, ana marka vurguları, birincil butonlar ve logolar. |
| 👑 | **İÜ Altın Sarısı (Heritage Gold)** | `#f59e0b` / `#d97706` | Başarı, mezuniyet diploması simgesi, rozetler, yıldızlar ve altın detaylar. |
| ✨ | **Parlak Altın (Gold Glow)** | `#fbbf24` | Buton hover efektleri, gradient geçişleri ve dikkat çekici metinler. |
| 🏛️ | **Derin Gece / Beyazıt Mavisi** | `#0f172a` | Sayfa ve kart zeminleri; kurumsal ağırlığı ve modernliği pekiştirir. |

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
    --iu-gold-light: #fbbf24;        /* Parlak Varak Sarısı */
    --iu-gold-glow: rgba(245, 158, 11, 0.25);
    --bg-body: #090d16;              /* Beyazıt Gece Mavisi Zemin */
    --card-surface: #131c2e;         /* Yüzey Kartı */
    --card-border: #1e293b;          /* Kart Çerçevesi */
    --border-accent: #b45309;        /* Altın Çerçeve Vurgusu */
}
```

---

## 🔤 3. Tipografi Standartları

1. **Başlıklar & Manşetler:** `Plus Jakarta Sans` / `Cinzel` (Klasik zarafet için)
   * Kalınlık: `700 (Bold)`, `800 (Extra Bold)`
   * Kullanım: "İstanbul Üniversitesi Mezunlar Ağı", bölüm başlıkları, fakülte isimleri.
2. **Gövde Metinleri & Arayüz:** `Plus Jakarta Sans`
   * Kalınlık: `400 (Regular)`, `500 (Medium)`, `600 (Semi-Bold)`
   * Kullanım: Profil açıklamaları, iş ilanı detayları, duyuru metinleri.
3. **Kod & Metrik Göstergeleri:** `JetBrains Mono`
   * Kullanım: Öğrenci / Mezun ID numaraları, REST API rotaları, terminal logları.

---

## 🏛️ 4. Arayüz ve Görsel Dil (UI/UX)

* **Tarihi Beyazıt Kapısı Motifi:** Kartların ve kahraman (hero) alanlarının arka planında İstanbul Üniversitesi'nin simgesi olan tarihi kapı ve meşale silüeti.
* **Fakülte Rozetleri:** Hukuk, Tıp, İktisat, İletişim, Edebiyat, Fen, Mühendislik gibi fakültelere özel renkli mikro etiketler.
* **Köşe Yuvarlaklığı & Gölge:** Kurumsal ciddiyeti modernizmle birleştiren `12px` - `16px` kart eğriliği ve altın ışıltılı derin gölgeler.

---

## 🏷️ 5. Logo & Slogan

* **Sembol:** İstanbul Üniversitesi Meşalesi & Tarihi Taç Motifi (`🏛️` / `🎓`) + Altın ve Bordo Çerçeve.
* **Kurumsal İsim:** **İstanbul Üniversitesi Mezun Bilgi ve Kariyer Ağı** (*IU Alumni*).
* **Resmi Slogan:** *"1453'ten Geleceğe: Mezunlarımızın Işığında Birlikte İleriye."*

---

## 🔗 6. İlgili Belgeler ve Bağlantılar

* 🏠 **Genel Proje Özeti:** [README.md](README.md)
* 🗄️ **Veritabanı ve İlişki Modeli (ERD):** [ddd.md](ddd.md)
* 💻 **Ana Sayfa:** [`index.html`](index.html)
* 🛡️ **Hata Koruyucuları (Guardians):** [`404.html`](404.html) &bull; [`middlewares/`](middlewares/)
