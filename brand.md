# 🎓 Alumni Network Platform — Brand & Design Identity Guide

This document defines the brand values, design language, color palette, typography, visual voice, and UI guidelines for the **Alumni Management & Networking Platform**.

---

## 📌 1. Brand Mission & Core Identity

The **Alumni Network Platform** empowers students and university graduates by providing a transparent, verified, and community-driven bridge between academic roots and industry excellence.

### Core Brand Attributes:
* **Academic Integrity:** Grounded in credibility, verified records, and university prestige.
* **Modern Velocity:** Clean, fast, modern, and developer-friendly UX/UI.
* **Empowering Community:** Promoting mutual growth through mentorship, career postings, and reunion networks.
* **Reliability & Security:** Robust data isolation, persistent containerized volumes, and resilient error guardians.

---

## 🎨 2. Visual Color System

The design system uses a dark-first modern palette inspired by premium developer portals and high-impact SaaS tools, accented with vibrant educational blues and energetic cyans.

### Primary Palette
| Swatch | Color Name | Hex Code | Purpose & Semantic Usage |
| :---: | :--- | :--- | :--- |
| 🔵 | **Primary Blue** | `#2563eb` | Main brand identity, primary call-to-action buttons, active navigation states. |
| 🔷 | **Primary Hover** | `#1d4ed8` | Interactive button hover and pressed states. |
| 💠 | **Accent Cyan** | `#0ea5e9` | Gradients, badges, links, and highlights. |
| 🔮 | **Accent Purple** | `#c084fc` | Gradient endpoints for hero text accents and premium cards. |

### Semantic Status Colors
| Swatch | Status | Hex Code | Semantic Usage |
| :---: | :--- | :--- | :--- |
| 🟢 | **Success** | `#10b981` | Successful submissions, active status, 200/201 responses. |
| 🟡 | **Warning** | `#f59e0b` | Pending reviews, draft postings, caution alerts. |
| 🔴 | **Danger / Error** | `#ef4444` | 400/404/500 Guardian error badges, deletions, rejected records. |
| ⚪ | **Text Main** | `#f8fafc` | Primary titles, body headings, active text. |
| 🔘 | **Text Muted** | `#94a3b8` | Subtitles, labels, timestamps, table metadata. |

### Surface & Background Tokens
| Token | Hex Code | Description |
| :--- | :--- | :--- |
| `var(--bg-body)` | `#0b1120` | Root background with subtle ambient radial glow. |
| `var(--dark-card)` | `#1e293b` | Elevation cards, module containers, modal sheets. |
| `var(--dark-border)` | `#334155` | Subtle container borders and divider lines. |
| `var(--card-hover)` | `#475569` | Interactive card border highlight on mouse-over. |

---

## 🔤 3. Typography & Font Pairing

The platform leverages modern, high-legibility web typography with clear geometric hierarchy:

1. **Display & Headings:** `Plus Jakarta Sans`
   * Weights: `700 (Bold)`, `800 (Extra Bold)`
   * Usage: Hero headlines, module card titles, section headers.
2. **Body Prose & Interface:** `Plus Jakarta Sans` / System Sans-Serif (`-apple-system`, `BlinkMacSystemFont`)
   * Weights: `400 (Regular)`, `500 (Medium)`, `600 (Semi-Bold)`
   * Usage: Body copy, navigation links, form inputs, button labels.
3. **Monospace & Code Metrics:** `JetBrains Mono` / System Monospace
   * Weights: `400 (Regular)`, `600 (Semi-Bold)`
   * Usage: Live terminal logs, API endpoints (`GET /api/users`), JSON schemas, status codes.

---

## 📐 4. UI Components & Layout Guidelines

* **Corner Radius:**
  * Action Buttons & Badges: `10px` / `9999px (Pill)`
  * Information Cards & Modules: `16px` – `20px`
* **Card Elevation & Depth:**
  * Subtle `1px solid #334155` border with `backdrop-filter: blur(12px)`.
  * Deep atmospheric shadows: `0 16px 32px rgba(0, 0, 0, 0.4)`.
* **Motion & Interactivity:**
  * Hover translation: `transform: translateY(-2px)` on buttons, `-6px` on feature cards.
  * Cubic-bezier easing: `all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`.

---

## 🏷️ 5. Logo & Brand Mark

* **Emblem:** Graduation Cap (`🎓`) set against a rounded gradient badge (`#2563eb` to `#0ea5e9`).
* **Wordmark:** **Alumni Network** (Geometric bold styling).
* **Tagline:** *"Üniversite Geleceğini Mezunlarınla İnşa Et" (Build the University Future with Your Alumni).*

---

## 🔗 6. Related Resources & Links

* 🏠 **Main Documentation:** [README.md](README.md)
* 🗄️ **Data & Domain Architecture:** [ddd.md](ddd.md)
* 🚀 **Interactive Prototype Homepage:** [`index.html`](index.html)
* 🛡️ **Error Guardians:** [`404.html`](404.html) &bull; [`middlewares/`](middlewares/)
