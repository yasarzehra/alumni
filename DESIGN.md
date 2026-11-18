# DESIGN.md — İstanbul Üniversitesi Mezun Bilgi Sistemi (İÜ Alumni) Design System

> **Style Standard:** [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) & [Refero Design Styles](https://styles.refero.design/)  
> **Brand Persona:** Academic Heritage (1453), High-Trust Alumni Network, Modern Developer & Product Craft  
> **Target Theme:** Dark-first Academic Elegance with Historic Burgundy & Heritage Gold

---

## 1. Visual Atmosphere & Philosophy

The interface merges the as-yet-unsurpassed **1453 heritage of Istanbul University** (historical Beyazıt Gate, Romanesque/Ottoman archival authority) with **modern high-velocity SaaS ergonomics** (Linear, Vercel, Stripe).

- **Tone & Mood:** Authoritative, prestigious, trustworthy, academic, modern, precise.
- **Contrast & Geometry:** Deep midnight backgrounds (`#080c16`), sharp yet rounded cards (`14px` - `18px`), paired with imperial burgundy gradients and warm gold leaf hairlines.
- **Lighting Model:** Ambient radial glows resembling ceremonial academy lighting (`rgba(136, 19, 55, 0.22)` and `rgba(217, 119, 6, 0.16)`).

---

## 2. Design Tokens

### 2.1. Color Roles & Palette

#### Brand & Accent Colors
```css
--iu-burgundy-dark:   #4c0519; /* Deepest Imperial Burgundy */
--iu-burgundy:        #881337; /* Official IU Burgundy (Base Brand) */
--iu-burgundy-hover:  #9f1239; /* Interactive Hover State */
--iu-burgundy-light:  #f43f5e; /* Rose / Active Indicator */

--iu-gold-dark:       #b45309; /* Deep Antique Bronze */
--iu-gold:            #d97706; /* Official IU Heritage Gold */
--iu-gold-light:      #fbbf24; /* Gilded Highlights & Badges */
--iu-gold-subtle:     #fef08a; /* Soft Cream Gold for Accented Prose */
--iu-gold-glow:       rgba(245, 158, 11, 0.25);
```

#### Neutral & Canvas Colors (Dark-First Foundation)
```css
--canvas-bg:          #080c16; /* Beyazıt Midnight (Root Background) */
--canvas-subtle:      #0d1322; /* Secondary sections & navigation */
--surface-card:       #111827; /* Elevated card surface */
--surface-card-hover: #152033; /* Hovered card elevation */
--surface-sunken:     #040711; /* Code editor, terminal & inputs */

--border-subtle:      #1f293d; /* Default structural hairlines */
--border-strong:      #334155; /* Interactive borders & focus states */
--border-gold-accent: rgba(217, 119, 6, 0.45); /* Highlighted feature bounds */
```

#### Typography Colors
```css
--text-primary:       #f8fafc; /* High-contrast white for titles & primary values */
--text-secondary:     #94a3b8; /* Muted slate for body, descriptions & labels */
--text-tertiary:      #64748b; /* Captions, disabled text, footnotes */
--text-gold-accent:   #fbbf24; /* Featured highlights & active links */
```

#### Semantic & Guardian Status Tokens
```css
--status-success:     #10b981; /* 200 OK, Active Job, Verified Alumni */
--status-warning:     #f59e0b; /* Pending review, expiring post */
--status-danger:      #ef4444; /* 404 / 500 Guardian, Rejected, Deleted */
--status-info:        #0ea5e9; /* System notices, OpenAPI link */
```

---

### 2.2. Typography Hierarchy

| Style Role | Font Family | Size | Weight | Line Height | Tracking |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Display 1 (Hero)** | `'Plus Jakarta Sans', sans-serif` | `3.4rem (54px)` | `800 (ExtraBold)` | `1.15` | `-1.2px` |
| **Heading 1 (H1)** | `'Plus Jakarta Sans', sans-serif` | `2.4rem (38px)` | `800` | `1.2` | `-0.8px` |
| **Heading 2 (H2)** | `'Plus Jakarta Sans', sans-serif` | `1.8rem (28px)` | `700 (Bold)` | `1.3` | `-0.4px` |
| **Heading 3 (H3)** | `'Plus Jakarta Sans', sans-serif` | `1.3rem (20px)` | `700` | `1.4` | `-0.2px` |
| **Body Large** | `'Plus Jakarta Sans', sans-serif` | `1.15rem (18px)`| `400 / 500` | `1.6` | `0` |
| **Body Default** | `'Plus Jakarta Sans', sans-serif` | `0.95rem (15px)`| `400 (Regular)` | `1.6` | `0` |
| **Body Strong** | `'Plus Jakarta Sans', sans-serif` | `0.95rem (15px)`| `600 (SemiBold)`| `1.5` | `0` |
| **Caption / Label** | `'Plus Jakarta Sans', sans-serif` | `0.82rem (13px)`| `600 / 700` | `1.4` | `+0.6px (Upper)` |
| **Code / Metrics** | `'JetBrains Mono', monospace` | `0.85rem (13.5px)`| `500 / 600` | `1.5` | `0` |

---

### 2.3. Spacing, Geometry & Radii Scale

```css
--radius-sm:   6px;   /* Micro badges & tags */
--radius-md:   10px;  /* Buttons, text inputs, dropdowns */
--radius-lg:   16px;  /* Cards, modals, feature modules */
--radius-xl:   20px;  /* Hero containers, large dialogs */
--radius-full: 9999px;/* Pill buttons, avatar seals, status dots */

--space-1:     4px;
--space-2:     8px;
--space-3:     12px;
--space-4:     16px;
--space-6:     24px;
--space-8:     32px;
--space-12:    48px;
--space-16:    64px;
--space-20:    80px;
```

---

## 3. UI Patterns & Component Guidelines

### 3.1. Navigation & Institutional Top Bar
* **Top Institutional Strip:** Height `32px`, gradient `#4c0519` to `#881337` to `#b45309`, text `0.78rem` uppercase letter-spaced `+0.8px` showcasing *"🏛️ İstanbul Üniversitesi • Kuruluş 1453"*.
* **Main Sticky Header:** Glassmorphic background `rgba(8, 12, 22, 0.88)` with `backdrop-filter: blur(16px)` and border-bottom `1px solid rgba(31, 41, 61, 0.8)`.
* **Brand Seal:** `44x44px` squircle with `border: 2px solid var(--iu-gold-light)` and subtle glow.

### 3.2. Action Buttons (Refero Standard)
* **Primary (İÜ Burgundy):**
  ```css
  background: linear-gradient(135deg, var(--iu-burgundy), #9f1239);
  color: #ffffff;
  border: 1px solid rgba(251, 191, 36, 0.35);
  box-shadow: 0 4px 16px rgba(136, 19, 55, 0.35);
  ```
  *Hover:* Elevates `-2px`, background shifts to `#be123c`, border glows to `--iu-gold-light`.
* **Secondary (Heritage Gold):**
  ```css
  background: linear-gradient(135deg, #d97706, #b45309);
  color: #ffffff;
  box-shadow: 0 4px 14px var(--iu-gold-glow);
  ```
* **Tertiary Ghost:**
  ```css
  background: rgba(255, 255, 255, 0.04);
  color: #f8fafc;
  border: 1px solid var(--border-subtle);
  ```
  *Hover:* Border highlights in `var(--iu-gold)`, text colors to `var(--iu-gold-light)`.

### 3.3. Bento & Module Cards
* **Dimensions & Padding:** `padding: 30px 24px`, border-radius `18px`, solid border `1px solid var(--border-subtle)`.
* **Top Accent Hairline:** Absolute `top: 0`, height `4px`, gradient `linear-gradient(90deg, var(--iu-burgundy), var(--iu-gold))`, initially opacity `0`, transitions to `1` on hover.
* **Elevation:** `box-shadow: 0 16px 32px rgba(0, 0, 0, 0.45)` upon hover accompanied by `-6px` smooth vertical translation.

### 3.4. Academic Faculty Pills & Badges
* Rounded pill badges (`border-radius: 9999px`) with individual emoji faculty iconography:
  - ⚖️ Hukuk Fakültesi
  - 🩺 İstanbul Tıp Fakültesi (Çapa)
  - 📈 İktisat Fakültesi
  - 🏛️ Siyasal Bilgiler Fakültesi
  - 💻 Bilgisayar & Bilişim
* Default background `#1f293d`, subtle border `#334155`. On hover, border turns `--iu-gold`, text shifts to `--iu-gold-light`.

### 3.5. Terminal & Observability Card (Developer Experience)
* Deep inset canvas `#040711` with simulated macOS window dots (`#ef4444`, `#f59e0b`, `#10b981`).
* Method badges color-coded:
  - `GET` $\rightarrow$ Gold (`#fbbf24`)
  - `POST` $\rightarrow$ Rose/Burgundy (`#f43f5e`)
  - Status `200/201` $\rightarrow$ Mint Emerald (`#34d399`)

---

## 4. Error State & Guardian Guidelines

### 404 Not Found Guardian Pattern
* **Visual Anchor:** Oversized gradient glitch code `404` (`#fbbf24` to `#f43f5e`).
* **Shield Badge:** *"🏛️ İÜ 404 GUARDIAN"*.
* **Diagnostic Box:** Mono-spaced requested path container `#080c16` displaying `{{REQUESTED_PATH}}`.
* **Quick Navigation:** Grid of fallback destination pills (`/jobs`, `/users`, `/applications`, `/announcements`).

### 5xx Server Error Guardian Pattern
* **Incident Correlation:** Generates unique `ERR-XXXXXXXX` incident token.
* **Safety Isolation:** Masks server secrets and internal SQL paths while persisting full tracebacks into `logs/error.log`.

---

## 5. Rules for AI Coding Agents

When prompting an AI agent to generate new views, components, or endpoints for this repository:

1. **Always adhere to the Dark-first Foundation:** Never introduce raw pure-white (`#ffffff`) background canvases for full views; use `--canvas-bg` (`#080c16`) and `--surface-card` (`#111827`).
2. **Strict Color Primaries:** Always use Istanbul University Burgundy (`#881337`) for dominant actions and Gold (`#d97706` / `#fbbf24`) for secondary highlights and ratings.
3. **Typography Pairing:** Ensure headlines use `Plus Jakarta Sans` with tight negative tracking (`-0.5px` to `-1.2px`), and machine endpoints/numbers use `JetBrains Mono`.
4. **Refero Component Density:** Maintain generous spacing (`padding: 24px` on cards) and tactile hover translations (`transform: translateY(-2px)`).
5. **No Broken Links:** Web links must connect to valid internal MVC routes (`/jobs`, `/users`, `/applications`, `/announcements`, `/api/swagger`).
