"""
Announcement View Layer - MVC Architecture
Renders rich, responsive management interface and HTML templates for Announcements.
"""
from typing import Dict, Any, Optional, List


class AnnouncementView:
    """
    Presentation layer for Announcement resources.
    Provides complete management interface (CRUD) for web clients.
    """

    @classmethod
    def _render_alert(cls, success: Optional[str] = None, error: Optional[str] = None) -> str:
        """Helper to render flash messages."""
        if success:
            return f"""
            <div style="background: #ecfdf5; border: 1px solid #a7f3d0; color: #065f46; padding: 14px 18px; border-radius: 10px; margin-bottom: 24px; display: flex; align-items: center; gap: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <span style="font-size: 1.25rem; font-weight: bold;">✓</span>
                <span style="font-size: 0.95rem; font-weight: 500;">{success}</span>
            </div>
            """
        elif error:
            return f"""
            <div style="background: #fef2f2; border: 1px solid #fecaca; color: #991b1b; padding: 14px 18px; border-radius: 10px; margin-bottom: 24px; display: flex; align-items: center; gap: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">
                <span style="font-size: 1.25rem; font-weight: bold;">⚠</span>
                <span style="font-size: 0.95rem; font-weight: 500;">{error}</span>
            </div>
            """
        return ""

    @classmethod
    def _category_badge(cls, category: str) -> str:
        cat_lower = category.lower()
        if "etkinlik" in cat_lower:
            return f"<span style='background:#fdf4ff; color:#9333ea; border:1px solid #f0abfc; padding:4px 10px; border-radius:9999px; font-size:0.78rem; font-weight:600;'>{category}</span>"
        elif "kariyer" in cat_lower or "staj" in cat_lower:
            return f"<span style='background:#eff6ff; color:#2563eb; border:1px solid #bfdbfe; padding:4px 10px; border-radius:9999px; font-size:0.78rem; font-weight:600;'>{category}</span>"
        elif "akademik" in cat_lower:
            return f"<span style='background:#ecfdf5; color:#059669; border:1px solid #a7f3d0; padding:4px 10px; border-radius:9999px; font-size:0.78rem; font-weight:600;'>{category}</span>"
        return f"<span style='background:#f1f5f9; color:#475569; border:1px solid #cbd5e1; padding:4px 10px; border-radius:9999px; font-size:0.78rem; font-weight:600;'>{category}</span>"

    @classmethod
    def render_index(cls, announcements: List[Dict[str, Any]], count: int, error: Optional[str] = None, success: Optional[str] = None) -> str:
        """
        Management Interface: Lists announcements with statistics, quick create form, and action triggers.
        Route: GET /announcements -> AnnouncementController.index()
        """
        alert_html = cls._render_alert(success, error)

        # Statistics
        active_count = sum(1 for a in announcements if a.get("status") == "Aktif")
        categories_count = len(set(a.get("category", "Genel") for a in announcements))

        # Rows
        rows = ""
        if announcements:
            for a in announcements:
                badge = cls._category_badge(a.get("category", "Genel"))
                preview_content = (a.get("content", "")[:90] + "...") if len(a.get("content", "")) > 90 else a.get("content", "")
                rows += f"""
                <tr>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;"><strong>#{a.get('id')}</strong></td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;">
                        <a href="/announcements/{a.get('id')}" style="color: #0f172a; text-decoration: none; font-weight: 600; font-size: 0.95rem;">{a.get('title')}</a>
                        <div style="font-size: 0.82rem; color: #64748b; margin-top: 3px;">{preview_content}</div>
                    </td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;">{badge}</td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; font-size: 0.85rem; color: #334155;">{a.get('author', '-')}</td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; font-size: 0.82rem; color: #64748b; white-space: nowrap;">
                        {a.get('createdAt', '-')[:10]}
                    </td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; text-align: right; white-space: nowrap;">
                        <a href="/announcements/{a.get('id')}" style="padding: 6px 12px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-size: 0.82rem; font-weight: 500; margin-right: 4px; display: inline-block;">Görüntüle</a>
                        <a href="/announcements/{a.get('id')}/edit" style="padding: 6px 12px; background: #f59e0b; color: white; text-decoration: none; border-radius: 6px; font-size: 0.82rem; font-weight: 500; margin-right: 4px; display: inline-block;">Düzenle</a>
                        <form action="/announcements/{a.get('id')}/delete" method="POST" style="display: inline-block; margin: 0;" onsubmit="return confirm('Duyuru #{a.get('id')} silinsin mi?');">
                            <button type="submit" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 500; cursor: pointer;">Sil</button>
                        </form>
                    </td>
                </tr>
                """
        else:
            rows = """
            <tr>
                <td colspan="6" style="padding: 36px; text-align: center; color: #64748b;">
                    Henüz kayıtlı duyuru bulunmamaktadır. Aşağıdaki formu kullanarak ilk duyuruyu yayınlayabilirsiniz.
                </td>
            </tr>
            """

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Duyuru Yönetim Paneli - Alumni MVC</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f1f5f9;
            color: #0f172a;
            padding: 40px 20px;
            line-height: 1.5;
        }}
        .wrapper {{ max-width: 1100px; margin: 0 auto; }}
        .card {{
            background: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
            padding: 32px;
            border: 1px solid #e2e8f0;
            margin-bottom: 28px;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #f1f5f9;
            padding-bottom: 20px;
            margin-bottom: 24px;
            flex-wrap: wrap;
            gap: 16px;
        }}
        h1 {{ font-size: 1.65rem; color: #0f172a; font-weight: 700; }}
        
        /* Stats Dashboard */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            margin-bottom: 28px;
        }}
        .stat-card {{
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.03);
        }}
        .stat-label {{ font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 600; letter-spacing: 0.05em; }}
        .stat-val {{ font-size: 1.8rem; font-weight: 700; color: #0f172a; margin-top: 6px; }}
        
        .btn-create-top {{
            padding: 9px 20px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: background 0.2s;
        }}
        .btn-create-top:hover {{ background: #1d4ed8; }}
        
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        th {{
            background: #f8fafc;
            padding: 12px 14px;
            font-size: 0.8rem;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 2px solid #e2e8f0;
        }}
        
        .form-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr;
            gap: 16px;
            margin-bottom: 16px;
        }}
        @media (max-width: 768px) {{
            .form-grid {{ grid-template-columns: 1fr; }}
        }}
        .form-group {{ display: flex; flex-direction: column; gap: 6px; margin-bottom: 14px; }}
        label {{ font-size: 0.85rem; font-weight: 600; color: #334155; }}
        input[type="text"], select, textarea {{
            padding: 10px 14px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            font-family: inherit;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}
        input:focus, select:focus, textarea:focus {{
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}
        .btn-submit {{
            padding: 11px 24px;
            background: #2563eb;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s;
        }}
        .btn-submit:hover {{ background: #1d4ed8; }}
        
        .nav-links {{ display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }}
        .nav-link {{
            padding: 8px 16px;
            background: #f1f5f9;
            color: #334155;
            text-decoration: none;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.2s;
        }}
        .nav-link:hover {{ background: #e2e8f0; color: #0f172a; }}
    </style>
</head>
<body>
    <div class="wrapper">
        {alert_html}

        <!-- Statistics Dashboard -->
        <div class="stats-grid">
            <div class="stat-card" style="border-left: 4px solid #2563eb;">
                <div class="stat-label">Toplam Duyuru</div>
                <div class="stat-val">{count}</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid #10b981;">
                <div class="stat-label">Aktif Yayınlar</div>
                <div class="stat-val">{active_count}</div>
            </div>
            <div class="stat-card" style="border-left: 4px solid #8b5cf6;">
                <div class="stat-label">Kategori Çeşidi</div>
                <div class="stat-val">{categories_count}</div>
            </div>
        </div>

        <!-- 1. Announcements Table -->
        <div class="card">
            <div class="header">
                <div>
                    <h1>Duyuru Yönetim Paneli (Announcement Management Interface)</h1>
                    <p style="color: #64748b; font-size: 0.95rem; margin-top: 4px;">
                        Model: <code>Announcement</code> &bull; Controller: <code>AnnouncementController</code> &bull; View: <code>AnnouncementView.render_index</code>
                    </p>
                </div>
                <div>
                    <a href="/announcements/create" class="btn-create-top">+ Yeni Duyuru Ekle (C)</a>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Başlık & Özet</th>
                        <th>Kategori</th>
                        <th>Yayınlayan</th>
                        <th>Tarih</th>
                        <th style="text-align: right;">Yönetim</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>

        <!-- 2. Quick Create Form -->
        <div class="card" style="border-left: 4px solid #2563eb;">
            <div class="header" style="border-bottom: none; margin-bottom: 16px; padding-bottom: 0;">
                <div>
                    <h2 style="font-size: 1.25rem; color: #0f172a;">Hızlı Duyuru Ekle (Create Announcement)</h2>
                    <p style="color: #64748b; font-size: 0.85rem; margin-top: 2px;">
                        Route: <code>POST /announcements</code> &rarr; Controller: <code>AnnouncementController.store()</code>
                    </p>
                </div>
            </div>

            <form action="/announcements" method="POST">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="title">Duyuru Başlığı</label>
                        <input type="text" id="title" name="title" placeholder="Örn: 2026 Girişimcilik Zirvesi" required>
                    </div>
                    <div class="form-group">
                        <label for="category">Kategori</label>
                        <select id="category" name="category">
                            <option value="Genel">Genel</option>
                            <option value="Etkinlik">Etkinlik</option>
                            <option value="Kariyer">Kariyer / Staj</option>
                            <option value="Akademik">Akademik</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="author">Yayınlayan Birim</label>
                        <input type="text" id="author" name="author" placeholder="Alumni Koordinatörlüğü" value="Alumni Koordinatörlüğü">
                    </div>
                </div>
                <div class="form-group">
                    <label for="content">Duyuru Detayı ve Açıklama</label>
                    <textarea id="content" name="content" rows="3" placeholder="Duyuru metnini buraya yazınız..." required></textarea>
                </div>
                <button type="submit" class="btn-submit">+ Duyuruyu Yayınla (Create)</button>
            </form>
        </div>

        <!-- Navigation Bar -->
        <div class="nav-links">
            <a href="/" class="nav-link">&larr; Ana Sayfa</a>
            <a href="/users" class="nav-link">Kullanıcı Yönetimi (/users)</a>
            <a href="/announcements/create" class="nav-link">Ayrı Form: /announcements/create</a>
            <a href="/api/announcements" class="nav-link">REST API (JSON: /api/announcements)</a>
            <a href="/api/swagger" class="nav-link" style="background: #e0e7ff; color: #4338ca;">Swagger UI Dokümantasyon</a>
        </div>
    </div>
</body>
</html>"""

    @classmethod
    def render_create(cls, error: Optional[str] = None) -> str:
        """
        [C]reate Form View: Standalone announcement creation page.
        Route: GET /announcements/create -> AnnouncementController.create()
        """
        alert_html = cls._render_alert(error=error)
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yeni Duyuru Yayınla - Alumni MVC</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f1f5f9;
            color: #0f172a;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .card {{
            max-width: 640px;
            width: 100%;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
            padding: 36px;
            border: 1px solid #e2e8f0;
        }}
        .badge {{
            background: #eff6ff;
            color: #2563eb;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 16px;
        }}
        h1 {{ font-size: 1.6rem; margin-bottom: 8px; color: #0f172a; }}
        p.subtitle {{ color: #64748b; font-size: 0.9rem; margin-bottom: 24px; }}
        .form-group {{ margin-bottom: 18px; display: flex; flex-direction: column; gap: 6px; }}
        label {{ font-size: 0.85rem; font-weight: 600; color: #334155; }}
        input[type="text"], select, textarea {{
            padding: 12px 14px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            font-family: inherit;
            transition: all 0.2s;
        }}
        input:focus, select:focus, textarea:focus {{
            border-color: #2563eb;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}
        .actions {{ margin-top: 28px; display: flex; gap: 12px; }}
        .btn {{
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
            border: none;
        }}
        .btn-primary {{ background: #2563eb; color: white; flex: 1; }}
        .btn-primary:hover {{ background: #1d4ed8; }}
        .btn-sec {{ background: #f1f5f9; color: #334155; }}
        .btn-sec:hover {{ background: #e2e8f0; }}
    </style>
</head>
<body>
    <div class="card">
        {alert_html}
        <span class="badge">GET /announcements/create &rarr; AnnouncementController.create</span>
        <h1>Yeni Duyuru Oluştur [Create (C)]</h1>
        <p class="subtitle">Platform üyeleri ve mezunlar için yeni bir bilgilendirme duyurusu yayınlayın.</p>

        <form action="/announcements" method="POST">
            <div class="form-group">
                <label for="title">Duyuru Başlığı</label>
                <input type="text" id="title" name="title" placeholder="Örn: Yıllık Mezunlar Networking Kokteyli" required autofocus>
            </div>
            <div class="form-group">
                <label for="category">Kategori</label>
                <select id="category" name="category">
                    <option value="Genel">Genel</option>
                    <option value="Etkinlik">Etkinlik</option>
                    <option value="Kariyer">Kariyer</option>
                    <option value="Akademik">Akademik</option>
                </select>
            </div>
            <div class="form-group">
                <label for="author">Yayınlayan Birim / Yazar</label>
                <input type="text" id="author" name="author" value="Alumni Koordinatörlüğü" required>
            </div>
            <div class="form-group">
                <label for="content">Duyuru İçeriği</label>
                <textarea id="content" name="content" rows="5" placeholder="Duyurunun tüm detaylarını buraya giriniz..." required></textarea>
            </div>
            <div class="actions">
                <button type="submit" class="btn btn-primary">+ Duyuruyu Yayınla</button>
                <a href="/announcements" class="btn btn-sec">İptal</a>
            </div>
        </form>
    </div>
</body>
</html>"""

    @classmethod
    def render_show(cls, announcement: Dict[str, Any], success: Optional[str] = None, error: Optional[str] = None) -> str:
        """
        [R]ead Detail View: Displays single announcement with full content and management actions.
        Route: GET /announcements/{id} -> AnnouncementController.show(id)
        """
        alert_html = cls._render_alert(success, error)
        badge = cls._category_badge(announcement.get("category", "Genel"))
        updated_box = f"<div class='field'><div class='label'>Son Güncelleme</div><div class='val' style='font-size:0.95rem; color:#64748b;'>{announcement.get('updatedAt')}</div></div>" if announcement.get('updatedAt') else ""

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{announcement.get('title')} - Alumni Duyurular</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f1f5f9;
            color: #0f172a;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .card {{
            max-width: 680px;
            width: 100%;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
            padding: 36px;
            border: 1px solid #e2e8f0;
        }}
        .badge-route {{
            background: #eff6ff;
            color: #2563eb;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 16px;
        }}
        .field {{ margin-bottom: 18px; }}
        .label {{ font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 600; letter-spacing: 0.05em; }}
        .val {{ font-size: 1.15rem; color: #0f172a; margin-top: 4px; }}
        .content-box {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            padding: 20px;
            font-size: 1.05rem;
            color: #1e293b;
            line-height: 1.7;
            margin-top: 6px;
            white-space: pre-wrap;
        }}
        .actions {{ margin-top: 32px; display: flex; gap: 10px; flex-wrap: wrap; }}
        .btn {{
            padding: 10px 18px;
            border-radius: 8px;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            display: inline-block;
            border: none;
            cursor: pointer;
        }}
        .btn-warning {{ background: #f59e0b; color: white; }}
        .btn-danger {{ background: #ef4444; color: white; }}
        .btn-sec {{ background: #f1f5f9; color: #334155; }}
    </style>
</head>
<body>
    <div class="card">
        {alert_html}
        <span class="badge-route">GET /announcements/{announcement.get('id')} &rarr; AnnouncementController.show</span>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; gap:12px; flex-wrap:wrap;">
            <h1 style="font-size: 1.6rem; color: #0f172a;">{announcement.get('title')}</h1>
            <div>{badge}</div>
        </div>

        <div style="display:flex; gap:24px; margin-bottom:20px; font-size:0.9rem; color:#64748b; flex-wrap:wrap;">
            <div><strong>Yayınlayan:</strong> {announcement.get('author', '-')}</div>
            <div><strong>Tarih:</strong> {announcement.get('createdAt', '-')[:10]}</div>
            <div><strong>Durum:</strong> {announcement.get('status', 'Aktif')}</div>
        </div>

        <div class="field">
            <div class="label">Duyuru İçeriği</div>
            <div class="content-box">{announcement.get('content')}</div>
        </div>
        {updated_box}

        <div class="actions">
            <a href="/announcements/{announcement.get('id')}/edit" class="btn btn-warning">Düzenle (U)</a>
            <form action="/announcements/{announcement.get('id')}/delete" method="POST" style="display:inline;" onsubmit="return confirm('Duyuru #{announcement.get('id')} silinecektir. Emin misiniz?');">
                <button type="submit" class="btn btn-danger">Sil (D)</button>
            </form>
            <a href="/announcements" class="btn btn-sec">&larr; Duyuru Listesi</a>
            <a href="/api/announcements/{announcement.get('id')}" class="btn btn-sec">API JSON</a>
        </div>
    </div>
</body>
</html>"""

    @classmethod
    def render_edit(cls, announcement: Dict[str, Any], error: Optional[str] = None) -> str:
        """
        [U]pdate Form View: Displays edit form pre-filled with announcement details.
        Route: GET /announcements/{id}/edit -> AnnouncementController.edit(id)
        """
        alert_html = cls._render_alert(error=error)
        cat = announcement.get("category", "Genel")
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Duyuru #{announcement.get('id')} Düzenle - Alumni MVC</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background: #f1f5f9;
            color: #0f172a;
            padding: 40px 20px;
            display: flex;
            justify-content: center;
        }}
        .card {{
            max-width: 640px;
            width: 100%;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
            padding: 36px;
            border: 1px solid #e2e8f0;
        }}
        .badge {{
            background: #fef3c7;
            color: #b45309;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 16px;
        }}
        h1 {{ font-size: 1.6rem; margin-bottom: 8px; color: #0f172a; }}
        p.subtitle {{ color: #64748b; font-size: 0.9rem; margin-bottom: 24px; }}
        .form-group {{ margin-bottom: 18px; display: flex; flex-direction: column; gap: 6px; }}
        label {{ font-size: 0.85rem; font-weight: 600; color: #334155; }}
        input[type="text"], select, textarea {{
            padding: 12px 14px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            font-family: inherit;
            transition: all 0.2s;
        }}
        input:focus, select:focus, textarea:focus {{
            border-color: #f59e0b;
            box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.15);
        }}
        .actions {{ margin-top: 28px; display: flex; gap: 12px; }}
        .btn {{
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
            border: none;
        }}
        .btn-warning {{ background: #f59e0b; color: white; flex: 1; }}
        .btn-warning:hover {{ background: #d97706; }}
        .btn-sec {{ background: #f1f5f9; color: #334155; }}
        .btn-sec:hover {{ background: #e2e8f0; }}
    </style>
</head>
<body>
    <div class="card">
        {alert_html}
        <span class="badge">GET /announcements/{announcement.get('id')}/edit &rarr; AnnouncementController.edit</span>
        <h1>Duyuruyu Düzenle [Edit (U)]</h1>
        <p class="subtitle">Duyuru #{announcement.get('id')} bilgilerini güncelleyin.</p>

        <form action="/announcements/{announcement.get('id')}" method="POST">
            <div class="form-group">
                <label for="title">Duyuru Başlığı</label>
                <input type="text" id="title" name="title" value="{announcement.get('title')}" required autofocus>
            </div>
            <div class="form-group">
                <label for="category">Kategori</label>
                <select id="category" name="category">
                    <option value="Genel" {'selected' if cat == 'Genel' else ''}>Genel</option>
                    <option value="Etkinlik" {'selected' if cat == 'Etkinlik' else ''}>Etkinlik</option>
                    <option value="Kariyer" {'selected' if cat == 'Kariyer' else ''}>Kariyer</option>
                    <option value="Akademik" {'selected' if cat == 'Akademik' else ''}>Akademik</option>
                </select>
            </div>
            <div class="form-group">
                <label for="author">Yayınlayan Birim</label>
                <input type="text" id="author" name="author" value="{announcement.get('author', 'Alumni Koordinatörlüğü')}" required>
            </div>
            <div class="form-group">
                <label for="content">Duyuru İçeriği</label>
                <textarea id="content" name="content" rows="6" required>{announcement.get('content')}</textarea>
            </div>
            <div class="actions">
                <button type="submit" class="btn btn-warning">Değişiklikleri Kaydet (U)</button>
                <a href="/announcements/{announcement.get('id')}" class="btn btn-sec">İptal</a>
            </div>
        </form>
    </div>
</body>
</html>"""

    @classmethod
    def render_error_404(cls, message: str = "Aranan duyuru bulunamadı.") -> str:
        """Renders 404 Not Found view for Announcements."""
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>404 - Duyuru Bulunamadı</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #1e293b; padding: 40px 20px; display: flex; justify-content: center; }}
        .card {{ max-width: 480px; width: 100%; background: white; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.06); padding: 32px; border: 1px solid #fee2e2; text-align: center; }}
        h1 {{ color: #dc2626; font-size: 1.8rem; margin-bottom: 12px; }}
        p {{ color: #64748b; margin-bottom: 24px; }}
        a {{ display: inline-block; padding: 10px 20px; background: #2563eb; color: white; text-decoration: none; border-radius: 8px; font-weight: 500; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>404 Not Found</h1>
        <p>{message}</p>
        <a href="/announcements">&larr; Duyuru Listesine Dön</a>
    </div>
</body>
</html>"""
