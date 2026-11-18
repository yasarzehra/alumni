# DESIGN.md — İstanbul Üniversitesi Mezun Bilgi Sistemi (İÜ Alumni)

> **Design Style Synthesis & References:**
> 1. [MasterClass Design System (Refero #4367b4cd)](https://styles.refero.design/style/4367b4cd-b002-4719-a418-cbce020f0d33) — *Cinematic Dark Media, Obsidian & Carbon Surfaces, Warm Gold Accents, Sohne Structural Rigor.*
> 2. [Syllabus Design System (Refero #b78edcaa)](https://styles.refero.design/style/b78edcaa-6754-41d7-ac00-0119b41ad88a) — *High-Trust Academic SaaS, Ink Violet/Deep Burgundy Contrast, Warm Butter/Gold Badging, Roobert Editorial Balance.*
> 3. [Genway Design System (Refero #a81607e2)](https://styles.refero.design/style/a81607e2-254f-4f53-b357-68c39c9cfc03) — *Atmospheric Gradient Washes, Geist Tech-Precision, Strict Monochromatic Discipline with Single-Hue Dominance.*
> 4. [VoltAgent/awesome-design-md Specification](https://github.com/VoltAgent/awesome-design-md) — *Machine-readable token schemas, component-level constraints, and strict negative rules for AI coding agents.*

---

## 🏛️ 1. Visual Atmosphere & Aesthetic Synthesis

The interface achieves **"Historic Academic Monumentality fused with Modern Product Craft"**:

* **From MasterClass:** The immersive dark stage background (`Carbon #080c16` & `Obsidian #111827`) that lets community talent, faculty badges, and career opportunities command total focus, using gold accents strictly for conversion and prestige.
* **From Syllabus:** The scholarly editorial dignity, refined typography hierarchy (academic badges, curriculum-style module grouping), and high-contrast pill metadata tags.
* **From Genway:** Atmospheric gradient glows (instead of flat harsh boxes), clean Geist/Plus Jakarta sans spacing, and a strict rule of single-hue dominance (Istanbul University Burgundy carries all weight; Gold serves as the singular heritage accent).

---

## 🎨 2. Design Tokens & Color System

### 2.1. Color Roles & Palette (İÜ Heritage & Refero Synthesis)

```css
:root {
  /* =========================================================================
     1. PRIMARY BRAND ROLES (Derived from Syllabus Ink & İÜ Official Burgundy)
     ========================================================================= */
  --color-brand-deep:      #4c0519; /* Deep Imperial Burgundy (Headers, Active Nav) */
  --color-brand-base:      #881337; /* Canonical İÜ Burgundy (CTAs, Key Buttons) */
  --color-brand-hover:     #9f1239; /* High-velocity hover state */
  --color-brand-active:    #be123c; /* Pressed button feedback */
  --color-brand-glow:      rgba(136, 19, 55, 0.35);

  /* =========================================================================
     2. HERITAGE ACCENTS (High-Trust Academic Palette, Zero Neon / Casino Glow)
     ========================================================================= */
  --color-accent-antique:  #b45309; /* Deep Antique Bronze (Border highlights) */
  --color-accent-gold:     #c59b27; /* Dignified Heritage Gold */
  --color-accent-light:    #d4af37; /* Matte Antique Silk Gold (Badges, Active Links) */
  --color-accent-butter:   #fef3c7; /* Soft Cream Gold for Tag Fills & Callouts */
  --color-accent-glow:     rgba(212, 175, 55, 0.20); /* Subdued institutional aura */

  /* =========================================================================
     2.1. BOTANICAL SEAL GREEN & GOLD (Brand Logo & Heritage Seal)
     ========================================================================= */
  --logo-green-deep:       #064e3b; /* Deep Matte Emerald Base */
  --logo-green-vibrant:    #022c22; /* Deep Botanical Green Shade */
  --logo-gold-border:      #d4af37; /* 1.5px Antique Gold Rim */
  --logo-seal-shadow:      rgba(0, 0, 0, 0.35); /* Serene institutional shadow (no neon halos) */

  /* =========================================================================
     3. CANVASES & SURFACES (MasterClass Obsidian & Carbon Dark-Stage Architecture)
     ========================================================================= */
  --canvas-bg:             #080c16; /* Beyazıt Midnight (Root HTML background) */
  --canvas-surface:        #111827; /* Obsidian Card Layer 1 */
  --canvas-elevated:       #1a2438; /* Elevated Modal & Dropdown Layer 2 */
  --canvas-sunken:         #040711; /* Terminal, Code Blocks & Inset Search */

  /* =========================================================================
     4. BORDERS & HAIRLINES (Genway Micro-Precision)
     ========================================================================= */
  --border-subtle:         #1f293d; /* 1px container separations */
  --border-strong:         #334155; /* Interactive form inputs & pills */
  --border-gold:           rgba(217, 119, 6, 0.45); /* Highlighted feature bounds */

  /* =========================================================================
     5. TYPOGRAPHY TEXT COLORS
     ========================================================================= */
  --text-primary:          #f8fafc; /* High-contrast white for headings */
  --text-secondary:        #94a3b8; /* Muted slate for body descriptions */
  --text-tertiary:         #64748b; /* Captions, timestamps, disabled items */
  --text-accent:           #fbbf24; /* Gold links and highlighted spans */

  /* =========================================================================
     6. STATUS & GUARDIAN ROLES
     ========================================================================= */
  --status-success:        #10b981; /* Verified alumni, 200 OK, active job */
  --status-warning:        #f59e0b; /* Pending submission, expiring posting */
  --status-danger:         #ef4444; /* 404 / 500 Guardian error, deletion */
}
```

---

## 🔤 3. Typography & Hierarchy (Tri-Font Architecture)

Instead of relying on a single repetitive font, the platform adopts a curated **Tri-Font Architecture** reflecting historic university prestige, modern interface ergonomics, and engineering precision:

1. **Editorial & Monumental Serif:** `'Cinzel', serif`  
   *Inspiration: Roman inscriptional monumentality, the historic Beyazıt Archway (1453), diplomas, faculty heraldry.*
2. **Interface & Product Sans:** `'Plus Jakarta Sans', sans-serif`  
   *Inspiration: Refero modern SaaS standards, legible micro-copy, dense form fields, crisp button labels.*
3. **Observability & Data Mono:** `'JetBrains Mono', monospace`  
   *Inspiration: Developer APIs, live metrics, terminal logs, matriculation student/alumni IDs.*

| Role | Font Family | Size | Weight | Line Height | Tracking | Purpose & Semantic Usage |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Hero Display (H1)** | `'Cinzel', serif` | `3.4rem (54px)` | `700 / 800` | `1.18` | `-0.5px` | "İstanbul Üniversitesi Mezunlar Ağı", Tarihi Kapı Manşeti |
| **Section Title (H2)**| `'Cinzel', serif` | `2.2rem (35px)` | `700 (Bold)` | `1.25` | `+0.2px` | "Platform Hizmetleri", "Fakültelerimiz" |
| **Module Title (H3)** | `'Plus Jakarta Sans', sans-serif` | `1.3rem (20px)` | `700` | `1.4` | `-0.2px` | Bento kart başlıkları (Kariyer, Rehber, Duyurular) |
| **Lead Subtitle** | `'Plus Jakarta Sans', sans-serif` | `1.18rem (19px)`| `400 / 500` | `1.6` | `0` | Hero açıklama paragrafı |
| **Body Regular** | `'Plus Jakarta Sans', sans-serif` | `0.95rem (15px)`| `400 / 500` | `1.6` | `0` | İlan detayları, kullanıcı biyografileri, tablo satırları |
| **Badges & Labels**| `'Plus Jakarta Sans', sans-serif` | `0.80rem (12.8px)`| `700` | `1.4` | `+1.0px (Caps)`| Fakülte etiketleri, "1453'ten Geleceğe" kurumsal şerit |
| **Code & Metrics** | `'JetBrains Mono', monospace` | `0.90rem (14px)` | `600 / 700` | `1.5` | `0` | "1453", "13+ Mezun", live terminal log satırları |

---

## 📐 4. Spacing, Geometry & Radii Tokens

Following **Refero's modular component scale**:
```css
--radius-badge:    9999px; /* Pill tags, faculty chips, status indicators */
--radius-sm:       6px;    /* Tooltips, input fields */
--radius-md:       10px;   /* Standard action buttons, dropdowns */
--radius-lg:       18px;   /* Feature cards, module tiles */
--radius-xl:       24px;   /* Hero containers, large dialogs */

--shadow-sm:       0 2px 8px rgba(0, 0, 0, 0.2);
--shadow-card:     0 8px 24px rgba(0, 0, 0, 0.4);
--shadow-card-hover: 0 16px 36px rgba(0, 0, 0, 0.55), 0 0 20px rgba(136, 19, 55, 0.25);
```

---

## 🧩 5. UI Patterns & Component Specifications

### 5.1. Institutional Brand Architecture & Navigation
* **Top Header Strip Eliminated:** The isolated `.iu-top-strip` bar was removed to eliminate header fragmentation and avoid the neon promotional banner look common in betting sites.
* **Integrated Institutional Brand Meta (`.brand-meta`):**
  - Brand Header: `İstanbul Üniversitesi` (`.brand-title`, `Cinzel`, 1.15rem, `#ffffff`).
  - Brand Sub: `MEZUN BİLGİ & KARİYER AĞI` (`.brand-sub`, `#d4af37`, 0.74rem).
  - Brand Meta: `Rektörlük Mezunlar Koordinatörlüğü • Kuruluş 1453` (`.brand-meta`, `#94a3b8`, 0.68rem) placed neatly right under the brand sub within `.brand-text`.
* **Sticky Glass Navbar:** Background `rgba(8, 12, 22, 0.92)` with `backdrop-filter: blur(16px)` positioned flush at `top: 0`.
* **Brand Seal (Botanical Green & Antique Gold System):** 44x44px rounded squircle, background `linear-gradient(145deg, #064e3b 0%, #022c22 100%)`, border `1.5px solid #d4af37`, housing the Beyazıt emblem (`🏛️`), with calm shadow `box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35)` (zero neon blur).
* **Navbar Primary CTA:** Direct action link **`İlanları İncele →`** with antique gold border.

### 5.2. Action Buttons (MasterClass & Genway Synthesis)
* **Refined Primary CTA — `İlanları İncele` (`.btn-nav-cta`):**
  - Background: `linear-gradient(135deg, #9f1239 0%, #881337 55%, #58061d 100%)`
  - Border: `1px solid rgba(251, 191, 36, 0.55)` with internal glow `inset 0 1px 0 rgba(255, 255, 255, 0.2)`
  - Shadow: `0 4px 16px rgba(136, 19, 55, 0.45)`
  - Interactive Arrow Chip (`.btn-arrow-chip`): Translucent gold housing for `→` with `translateX(3px)` translation on hover.
  - Phrasing: **`İlanları İncele →`**, **`💼 Mezun İlanlarına Göz At`**, **`+ İlan Ver`**.
* **Secondary CTA (Heritage Gold):**
  - Background: `linear-gradient(135deg, #d97706, #b45309)`
  - Color: `#ffffff`, Shadow: `0 4px 14px var(--color-accent-glow)`
* **Ghost Action Button:**
  - Background: `rgba(255, 255, 255, 0.04)`, border: `1px solid #1f293d`
  - Hover: Border `#d97706`, color `#fbbf24`.

### 5.3. Bento Feature Cards (Refero Style)
* Background: `#111827`, border: `1px solid #1f293d`, radius: `18px`, padding: `30px 24px`.
* **Dynamic Hover Line:** A 4px line at the top border: `linear-gradient(90deg, #881337, #d97706)` with opacity transitioning from `0` to `1` on hover.
* **Translation:** `-6px` smooth vertical transform with `box-shadow: var(--shadow-card-hover)`.

### 5.4. Academic Faculty Pills (Syllabus Pattern)
* Border radius: `9999px`, background: `#1f293d`, border: `1px solid #334155`.
* Typography: `0.88rem`, weight: `500`.
* Faculty tags include emoji markers:
  - `⚖️ Hukuk Fakültesi`
  - `🩺 İstanbul Tıp Fakültesi (Çapa)`
  - `📈 İktisat Fakültesi`
  - `🏛️ Siyasal Bilgiler Fakültesi`
  - `💻 Bilgisayar & Bilişim Fakültesi`

### 5.5. Observability Terminal Card (Genway Tech Pattern)
* Background: `#040711`, inset border `#1e293b`.
* Three window dots: `#ef4444`, `#f59e0b`, `#10b981`.
* Method color syntax:
  - `GET` $\rightarrow$ Gold (`#fbbf24`)
  - `POST` $\rightarrow$ Rose/Burgundy (`#f43f5e`)
  - `STATUS 200/201` $\rightarrow$ Mint Emerald (`#34d399`)

### 5.6. Beyazıt Archway Open Inscription (Açık Mimari Kitabe — Baloncuksuz & Yüksek Güven)
* Flat, open-air architectural inscriptional header (no enclosed rounded bubble, pill or balloon):
  - **Top Hairline Bar:** Two flanking antique gold hairlines (`inscription-hairline`) tapering to transparent on the sides.
  - **1453 Center Marker:** Solid dignified antique gold inscriptional date (`#d4af37`) with `letter-spacing: 3px`, free from flashing casino beacon animations.
  - **Monumental Inscription:** "BEYAZIT'IN ASIRLIK BİLGİ IŞIĞI • GELECEĞE KÖK SALAN MİRAS" in `Cinzel` serif with flanking `⚜️` fleur-de-lis ornaments.
  - **Tapered Gold Ground Line:** A 140px centered accent beam (`inscription-bottom-bar`) connecting down to the H1 display title.

---

## 🛡️ 6. Error Guardians & Resilience States

* **404 Not Found Guardian (`404.html`):**
  - Shield badge: `🏛️ İÜ 404 GUARDIAN` in burgundy pill.
  - Large glitch headline `404` (`#fbbf24` to `#f43f5e` gradient).
  - Terminal-style path container `#080c16` displaying `{{REQUESTED_PATH}}`.
  - Fallback navigation pills (`/jobs`, `/users`, `/applications`, `/announcements`).
* **5xx Server Error Guardian:**
  - Automated correlation ID generation (`ERR-XXXXXXXX`).
  - Strict isolation: Secrets and raw paths masked from users while full diagnostic traces persist to `logs/error.log`.

---

## 🤖 7. Strict Directives for AI Coding Agents

When generating new pages, components, controllers, or templates in this repository, AI agents must strictly follow these rules:

1. **Dark-first Canvas Obligation:** Never render pure white (`#ffffff`) background canvases. Always use `--canvas-bg` (`#080c16`) and `--canvas-surface` (`#111827`).
2. **Single-Hue Brand Dominance:** Istanbul University Burgundy (`#881337`) is the primary driver of all high-impact actions. Heritage Gold (`#d97706` / `#fbbf24`) is strictly reserved for prestige accents, ratings, and secondary buttons. Never introduce random third-party blues, purples, or greens as primary buttons.
3. **Typography Discipline:** Use `Plus Jakarta Sans` with negative letter-spacing for headlines (`-0.5px` to `-1.2px`), and `JetBrains Mono` for IDs, status codes, and API routes.
4. **Refero Micro-Interactions:** Always provide hover elevations (`transform: translateY(-2px)`) and subtle border color shifts on interactive cards.
5. **Route Integrity:** Every anchor link must resolve to a valid MVC route (`/jobs`, `/users`, `/applications`, `/announcements`, `/api/swagger`).
