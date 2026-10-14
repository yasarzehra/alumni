"""
View Layer - MVC Architecture
Handles presentation and HTML rendering for Web Controllers.
Separates UI presentation from business logic (Model) and orchestration (Controller).
"""
import os
from typing import Dict, Any, Optional, List


class View:
    """
    Presentation Layer (View)
    Renders clean, modern, responsive HTML templates for web clients.
    Implements all CRUD views: Index, Create, Show, Edit.
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
    def render_users_index(cls, users: List[Dict[str, Any]], count: int, error: Optional[str] = None, success: Optional[str] = None) -> str:
        """
        [R]ead: Renders the User Listing (R) view with action buttons for Edit (U) and Delete (D).
        Route: GET /users -> UserController.index()
        """
        alert_html = cls._render_alert(success, error)

        # Table rows for Listing (R)
        rows = ""
        if users:
            for u in users:
                updated_at_str = f"<br><small style='color:#94a3b8;'>Güncellendi: {u.get('updatedAt')}</small>" if u.get('updatedAt') else ""
                rows += f"""
                <tr>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;"><strong>#{u.get('id')}</strong></td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; font-weight: 600; color: #1e293b;">{u.get('name')}</td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;"><code>{u.get('email')}</code></td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; font-size: 0.85rem; color: #64748b;">
                        {u.get('createdAt', '-')}{updated_at_str}
                    </td>
                    <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; text-align: right; white-space: nowrap;">
                        <a href="/users/{u.get('id')}" style="padding: 6px 12px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-size: 0.82rem; font-weight: 500; margin-right: 4px; display: inline-block;">Görüntüle (R)</a>
                        <a href="/users/{u.get('id')}/edit" style="padding: 6px 12px; background: #f59e0b; color: white; text-decoration: none; border-radius: 6px; font-size: 0.82rem; font-weight: 500; margin-right: 4px; display: inline-block;">Düzenle (U)</a>
                        <form action="/users/{u.get('id')}/delete" method="POST" style="display: inline-block; margin: 0;" onsubmit="return confirm('Kullanıcı #{u.get('id')} silinsin mi?');">
                            <button type="submit" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-size: 0.82rem; font-weight: 500; cursor: pointer;">Sil (D)</button>
                        </form>
                    </td>
                </tr>
                """
        else:
            rows = """
            <tr>
                <td colspan="5" style="padding: 36px; text-align: center; color: #64748b;">
                    Henüz kayıtlı kullanıcı bulunmamaktadır.
                </td>
            </tr>
            """

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kullanıcı Yönetimi (MVC CRUD) - Alumni</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: #f1f5f9;
            color: #0f172a;
            padding: 40px 20px;
            line-height: 1.5;
        }}
        .wrapper {{ max-width: 1040px; margin: 0 auto; }}
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
        .actions-top {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; }}
        .badge {{
            padding: 6px 12px;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .badge-blue {{ background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }}
        .badge-green {{ background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }}
        .btn-create-top {{
            padding: 8px 18px;
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
            grid-template-columns: 1fr 1fr auto;
            gap: 16px;
            align-items: flex-end;
        }}
        @media (max-width: 768px) {{
            .form-grid {{ grid-template-columns: 1fr; }}
        }}
        .form-group {{ display: flex; flex-direction: column; gap: 6px; }}
        label {{ font-size: 0.85rem; font-weight: 600; color: #334155; }}
        input[type="text"], input[type="email"] {{
            padding: 10px 14px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            transition: border-color 0.2s, box-shadow 0.2s;
        }}
        input:focus {{
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

        <!-- 1. [R]ead: User List Table -->
        <div class="card">
            <div class="header">
                <div>
                    <h1>Kullanıcı Yönetimi (CRUD Web View)</h1>
                    <p style="color: #64748b; font-size: 0.95rem; margin-top: 4px;">
                        Model: <code>User</code> &bull; Controller: <code>UserController</code> &bull; View: <code>View.render_users_index</code>
                    </p>
                </div>
                <div class="actions-top">
                    <span class="badge badge-green">{count} Kullanıcı</span>
                    <a href="/users/create" class="btn-create-top">+ Yeni Kullanıcı Sayfası (C)</a>
                </div>
            </div>

            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Ad Soyad</th>
                        <th>E-posta</th>
                        <th>Kayıt / Güncelleme</th>
                        <th style="text-align: right;">CRUD İşlemleri</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>

        <!-- 2. [C]reate: Quick In-Page User Creation Form -->
        <div class="card" style="border-left: 4px solid #2563eb;">
            <div class="header" style="border-bottom: none; margin-bottom: 16px; padding-bottom: 0;">
                <div>
                    <h2 style="font-size: 1.25rem; color: #0f172a;">Hızlı Kullanıcı Ekle [Create (C)]</h2>
                    <p style="color: #64748b; font-size: 0.85rem; margin-top: 2px;">
                        Route: <code>POST /users</code> &rarr; Controller: <code>UserController.store()</code>
                    </p>
                </div>
                <span class="badge badge-blue">Route: POST /users</span>
            </div>

            <form action="/users" method="POST">
                <div class="form-grid">
                    <div class="form-group">
                        <label for="name">Ad Soyad</label>
                        <input type="text" id="name" name="name" placeholder="Örn: Mehmet Öz" required>
                    </div>
                    <div class="form-group">
                        <label for="email">E-posta Adresi</label>
                        <input type="email" id="email" name="email" placeholder="Örn: mehmet@example.com" required>
                    </div>
                    <div>
                        <button type="submit" class="btn-submit">+ Kullanıcı Ekle</button>
                    </div>
                </div>
            </form>
        </div>

        <!-- Navigation Bar -->
        <div class="nav-links">
            <a href="/" class="nav-link">&larr; Ana Sayfa</a>
            <a href="/about" class="nav-link">About Sayfası</a>
            <a href="/users/create" class="nav-link">Ayrı Form: /users/create</a>
            <a href="/api/users" class="nav-link">REST API (JSON: /api/users)</a>
            <a href="/api/swagger" class="nav-link" style="background: #e0e7ff; color: #4338ca;">Swagger UI Dokümantasyon</a>
        </div>
    </div>
</body>
</html>"""

    @classmethod
    def render_users_create(cls, error: Optional[str] = None) -> str:
        """
        [C]reate Form View: Displays standalone user creation page.
        Route: GET /users/create -> UserController.create()
        """
        alert_html = cls._render_alert(error=error)
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Yeni Kullanıcı Oluştur (Create View) - Alumni</title>
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
            max-width: 540px;
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
        input[type="text"], input[type="email"] {{
            padding: 12px 14px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s;
        }}
        input:focus {{
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
        <span class="badge">GET /users/create &rarr; UserController.create</span>
        <h1>Yeni Kullanıcı Oluştur [Create (C)]</h1>
        <p class="subtitle">Kullanıcı bilgilerini girerek MVC Model katmanına yeni kayıt ekleyin.</p>

        <form action="/users" method="POST">
            <div class="form-group">
                <label for="name">Ad Soyad</label>
                <input type="text" id="name" name="name" placeholder="Örn: Selin Yılmaz" required autofocus>
            </div>
            <div class="form-group">
                <label for="email">E-posta Adresi</label>
                <input type="email" id="email" name="email" placeholder="Örn: selin@example.com" required>
            </div>
            <div class="actions">
                <button type="submit" class="btn btn-primary">+ Kullanıcıyı Kaydet</button>
                <a href="/users" class="btn btn-sec">İptal</a>
            </div>
        </form>
    </div>
</body>
</html>"""

    @classmethod
    def render_users_show(cls, user: Dict[str, Any], success: Optional[str] = None, error: Optional[str] = None) -> str:
        """
        [R]ead Detail View: Displays single user profile with Update (U) and Delete (D) triggers.
        Route: GET /users/{id} -> UserController.show(id)
        """
        alert_html = cls._render_alert(success, error)
        updated_box = f"<div class='field'><div class='label'>Son Güncelleme</div><div class='val' style='font-size:0.95rem; color:#64748b;'>{user.get('updatedAt')}</div></div>" if user.get('updatedAt') else ""

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kullanıcı #{user.get('id')} Profili - Alumni</title>
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
            max-width: 560px;
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
        .field {{ margin-bottom: 16px; }}
        .label {{ font-size: 0.8rem; text-transform: uppercase; color: #64748b; font-weight: 600; letter-spacing: 0.05em; }}
        .val {{ font-size: 1.15rem; color: #0f172a; margin-top: 4px; }}
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
        .btn-primary {{ background: #2563eb; color: white; }}
        .btn-warning {{ background: #f59e0b; color: white; }}
        .btn-danger {{ background: #ef4444; color: white; }}
        .btn-sec {{ background: #f1f5f9; color: #334155; }}
    </style>
</head>
<body>
    <div class="card">
        {alert_html}
        <span class="badge">GET /users/{user.get('id')} &rarr; UserController.show</span>
        <h1 style="font-size: 1.5rem; margin-bottom: 20px;">Kullanıcı Detay Profili [Show (R)]</h1>
        <div class="field">
            <div class="label">Kullanıcı ID</div>
            <div class="val"><strong>#{user.get('id')}</strong></div>
        </div>
        <div class="field">
            <div class="label">Ad Soyad</div>
            <div class="val">{user.get('name')}</div>
        </div>
        <div class="field">
            <div class="label">E-Posta</div>
            <div class="val"><code>{user.get('email')}</code></div>
        </div>
        <div class="field">
            <div class="label">Kayıt Tarihi</div>
            <div class="val" style="font-size: 0.95rem; color: #64748b;">{user.get('createdAt', '-')}</div>
        </div>
        {updated_box}

        <div class="actions">
            <a href="/users/{user.get('id')}/edit" class="btn btn-warning">Düzenle (U)</a>
            <form action="/users/{user.get('id')}/delete" method="POST" style="display:inline;" onsubmit="return confirm('Kullanıcı #{user.get('id')} silinecektir. Onaylıyor musunuz?');">
                <button type="submit" class="btn btn-danger">Sil (D)</button>
            </form>
            <a href="/users" class="btn btn-sec">&larr; Listeye Dön</a>
            <a href="/api/users/{user.get('id')}" class="btn btn-sec">API JSON</a>
        </div>
    </div>
</body>
</html>"""

    @classmethod
    def render_users_edit(cls, user: Dict[str, Any], error: Optional[str] = None) -> str:
        """
        [U]pdate Form View: Displays edit form pre-filled with existing user details.
        Route: GET /users/{id}/edit -> UserController.edit(id)
        """
        alert_html = cls._render_alert(error=error)
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kullanıcı #{user.get('id')} Düzenle (Edit View) - Alumni</title>
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
            max-width: 540px;
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
        input[type="text"], input[type="email"] {{
            padding: 12px 14px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.95rem;
            outline: none;
            transition: all 0.2s;
        }}
        input:focus {{
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
        <span class="badge">GET /users/{user.get('id')}/edit &rarr; UserController.edit</span>
        <h1>Kullanıcıyı Düzenle [Edit (U)]</h1>
        <p class="subtitle">Kullanıcı #{user.get('id')} bilgilerini güncelleyin.</p>

        <!-- Submits to POST /users/{id} for web browser form update -->
        <form action="/users/{user.get('id')}" method="POST">
            <div class="form-group">
                <label for="name">Ad Soyad</label>
                <input type="text" id="name" name="name" value="{user.get('name')}" required autofocus>
            </div>
            <div class="form-group">
                <label for="email">E-posta Adresi</label>
                <input type="email" id="email" name="email" value="{user.get('email')}" required>
            </div>
            <div class="actions">
                <button type="submit" class="btn btn-warning">Değişiklikleri Kaydet (U)</button>
                <a href="/users/{user.get('id')}" class="btn btn-sec">İptal</a>
            </div>
        </form>
    </div>
</body>
</html>"""

    @classmethod
    def render_error_404(cls, message: str = "Aranan kayıt bulunamadı.") -> str:
        """Renders 404 Not Found view."""
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>404 - Bulunamadı</title>
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
        <a href="/users">&larr; Kullanıcı Listesine Dön</a>
    </div>
</body>
</html>"""
