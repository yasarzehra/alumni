"""
View Layer - MVC Architecture
Handles presentation and HTML rendering for Web Controllers.
Now fully unified with the Istanbul University Tri-Font & Dark Institutional Theme via Layout.
"""
import html
from typing import Dict, Any, Optional, List
from views.layout import Layout


class View:
    """
    Presentation Layer (View)
    Renders clean, modern, responsive HTML templates for web clients.
    Implements all User CRUD views: Index, Create, Show, Edit.
    """

    @classmethod
    def _render_alert(cls, success: Optional[str] = None, error: Optional[str] = None) -> str:
        """Helper to render flash messages."""
        if success:
            return f"""
            <div class="alert alert-success">
                <span style="font-size: 1.25rem; font-weight: bold;">✓</span>
                <span>{html.escape(success)}</span>
            </div>
            """
        elif error:
            return f"""
            <div class="alert alert-danger">
                <span style="font-size: 1.25rem; font-weight: bold;">⚠</span>
                <span>{html.escape(error)}</span>
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

        rows = ""
        if users:
            for u in users:
                u_id = u.get('id')
                u_name = html.escape(str(u.get('name') or 'İsimsiz Üye'))
                u_email = html.escape(str(u.get('email') or ''))
                u_created = html.escape(str(u.get('createdAt') or '-'))
                updated_at_str = f"<br><small style='color:var(--text-muted); font-size:0.75rem;'>Güncelleme: {html.escape(str(u.get('updatedAt')))}</small>" if u.get('updatedAt') else ""
                
                rows += f"""
                <tr>
                    <td class="mono" style="font-weight: 700; color: var(--iu-gold-light);">#{u_id}</td>
                    <td>
                        <div style="font-weight: 700; color: #ffffff; font-size: 0.98rem;">{u_name}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">İstanbul Üniversitesi Mezunu / Öğrencisi</div>
                    </td>
                    <td><code class="mono" style="color: #cbd5e1; background: #080c16; padding: 4px 8px; border-radius: 6px; border: 1px solid var(--dark-border);">{u_email}</code></td>
                    <td class="mono" style="font-size: 0.85rem; color: var(--text-muted);">
                        {u_created}{updated_at_str}
                    </td>
                    <td style="text-align: right; white-space: nowrap;">
                        <a href="/users/{u_id}" class="btn btn-sm btn-ghost" title="Profili Görüntüle">👤 Detay</a>
                        <a href="/users/{u_id}/edit" class="btn btn-sm btn-gold" style="margin-left: 4px;" title="Profili Düzenle">✏️ Düzenle</a>
                        <form action="/users/{u_id}/delete" method="POST" style="display: inline-block; margin-left: 4px;" onsubmit="return confirm('Kullanıcı #{u_id} ({u_name}) silinsin mi?');">
                            <button type="submit" class="btn btn-sm btn-danger" title="Kullanıcıyı Sil">🗑️ Sil</button>
                        </form>
                    </td>
                </tr>
                """
        else:
            rows = """
            <tr>
                <td colspan="5" style="padding: 40px; text-align: center; color: var(--text-muted);">
                    Henüz kayıtlı İÜ mezunu veya kullanıcısı bulunmamaktadır.
                </td>
            </tr>
            """

        content = f"""
        <!-- İstatistik ve Hızlı İşlemler Kartı -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: var(--iu-gold-light);">{count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Kayıtlı İÜ Mezunu & Üyesi</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: var(--success);">Aktif</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Veritabanı Durumu (SQLite)</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: #60a5fa;">RBAC</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Yetkilendirme Seviyesi</div>
            </div>
        </div>

        <!-- Mezunlar Listesi Tablosu -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; flex-wrap: wrap; gap: 12px;">
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.3rem; color: #ffffff;">Doğrulanmış Üye Listesi</h2>
                <div style="display: flex; gap: 8px;">
                    <a href="/api/users" class="btn btn-sm btn-ghost" title="REST API JSON Çıktısı">⚡ JSON API</a>
                    <a href="/users/create" class="btn btn-sm btn-burgundy">+ Yeni Mezun Ekle</a>
                </div>
            </div>

            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 70px;">ID</th>
                            <th>Ad Soyad & Ünvan</th>
                            <th>E-Posta</th>
                            <th>Kayıt Tarihi</th>
                            <th style="text-align: right; width: 220px;">İşlemler</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Hızlı Üye Ekleme Kartı (In-Page Quick Create) -->
        <div class="card" style="border-left: 4px solid var(--iu-burgundy);">
            <div style="margin-bottom: 18px;">
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.2rem; color: #ffffff;">Hızlı Mezun Kaydı [Create (C)]</h3>
                <p style="font-size: 0.88rem; color: var(--text-muted);">
                    Formu doldurarak veritabanına anında yeni bir öğrenci veya mezun profili ekleyin.
                </p>
            </div>

            <form action="/users" method="POST" style="display: grid; grid-template-columns: 1fr 1fr auto; gap: 16px; align-items: flex-end;">
                <div class="form-group" style="margin-bottom: 0;">
                    <label class="form-label" for="name">Ad Soyad</label>
                    <input type="text" id="name" name="name" class="form-control" placeholder="Örn: Dr. Ali Yılmaz" required>
                </div>
                <div class="form-group" style="margin-bottom: 0;">
                    <label class="form-label" for="email">E-Posta Adresi</label>
                    <input type="email" id="email" name="email" class="form-control" placeholder="Örn: ali.yilmaz@istanbul.edu.tr" required>
                </div>
                <button type="submit" class="btn btn-burgundy" style="height: 46px;">+ Mezunu Kaydet</button>
            </form>
        </div>
        """

        return Layout.render(
            title="Mezun & Öğrenci Rehberi",
            active_nav="users",
            content=content,
            subtitle="İstanbul Üniversitesi mezun ve akademisyen ağının doğrulanmış üyeleri.",
            actions='<a href="/users/create" class="btn btn-burgundy">+ Yeni Kullanıcı Sayfası</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_users_create(cls, error: Optional[str] = None) -> str:
        """
        [C]reate Form View: Displays standalone user creation page.
        Route: GET /users/create -> UserController.create()
        """
        alert_html = cls._render_alert(error=error)

        content = f"""
        <div class="card" style="max-width: 620px; margin: 0 auto; border-top: 4px solid var(--iu-burgundy);">
            <div style="margin-bottom: 24px;">
                <span class="badge badge-burgundy" style="margin-bottom: 10px;">Yeni Mezun / Kullanıcı Formu</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.5rem; color: #ffffff;">Üyelik Bilgileri</h2>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 4px;">
                    Platforma dahil edilecek mezun veya öğrencinin iletişim bilgilerini tanımlayın.
                </p>
            </div>

            <form action="/users" method="POST">
                <div class="form-group">
                    <label class="form-label" for="name">Ad Soyad</label>
                    <input type="text" id="name" name="name" class="form-control" placeholder="Örn: Selin Yılmaz" required autofocus>
                </div>
                <div class="form-group">
                    <label class="form-label" for="email">Kurumsal / Kişisel E-Posta</label>
                    <input type="email" id="email" name="email" class="form-control" placeholder="Örn: selin.yilmaz@alumni.istanbul.edu.tr" required>
                </div>
                <div style="display: flex; gap: 12px; margin-top: 28px;">
                    <button type="submit" class="btn btn-burgundy" style="flex: 1;">+ Kullanıcıyı Kaydet</button>
                    <a href="/users" class="btn btn-ghost">İptal / Listeye Dön</a>
                </div>
            </form>
        </div>
        """

        return Layout.render(
            title="Yeni Mezun / Kullanıcı Kaydı",
            active_nav="users",
            content=content,
            subtitle="İstanbul Üniversitesi Mezun Platformu veri tabanına yeni üye tanımlayın.",
            actions='<a href="/users" class="btn btn-ghost">&larr; Üye Listesine Dön</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_users_show(cls, user: Dict[str, Any], success: Optional[str] = None, error: Optional[str] = None) -> str:
        """
        [R]ead Detail View: Displays single user profile with Update (U) and Delete (D) triggers.
        Route: GET /users/{id} -> UserController.show(id)
        """
        alert_html = cls._render_alert(success, error)
        u_id = user.get('id')
        u_name = html.escape(str(user.get('name') or 'İsimsiz'))
        u_email = html.escape(str(user.get('email') or ''))
        u_created = html.escape(str(user.get('createdAt') or '-'))
        u_updated = html.escape(str(user.get('updatedAt') or 'Henüz güncellenmedi'))

        content = f"""
        <div class="card" style="max-width: 720px; margin: 0 auto; border-top: 4px solid var(--iu-gold);">
            <!-- Profil Üst Başlığı -->
            <div style="display: flex; align-items: center; gap: 20px; margin-bottom: 28px; padding-bottom: 20px; border-bottom: 1px solid var(--dark-border);">
                <div style="width: 72px; height: 72px; border-radius: 20px; background: linear-gradient(135deg, var(--iu-burgundy), #4c0519); border: 2px solid var(--iu-gold-light); display: flex; align-items: center; justify-content: center; font-size: 2.2rem; box-shadow: 0 6px 18px var(--iu-gold-glow);">
                    🎓
                </div>
                <div>
                    <div style="display: flex; align-items: center; gap: 10px;">
                        <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff;">{u_name}</h2>
                        <span class="badge badge-green">Doğrulanmış Üye</span>
                    </div>
                    <p style="color: var(--iu-gold-light); font-size: 0.9rem; font-weight: 600;">İstanbul Üniversitesi Mezunlar Ağı</p>
                </div>
            </div>

            <!-- Bilgi Izgarası -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 28px;">
                <div style="background: #090e1a; padding: 16px; border-radius: 12px; border: 1px solid var(--dark-border);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">Mezun ID</div>
                    <div class="mono" style="font-size: 1.2rem; color: var(--iu-gold-light); font-weight: 700; margin-top: 4px;">#{u_id}</div>
                </div>
                <div style="background: #090e1a; padding: 16px; border-radius: 12px; border: 1px solid var(--dark-border);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">E-Posta Adresi</div>
                    <div class="mono" style="font-size: 0.95rem; color: #ffffff; margin-top: 4px; word-break: break-all;">{u_email}</div>
                </div>
                <div style="background: #090e1a; padding: 16px; border-radius: 12px; border: 1px solid var(--dark-border);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">Kayıt Zamanı</div>
                    <div class="mono" style="font-size: 0.9rem; color: var(--text-muted); margin-top: 4px;">{u_created}</div>
                </div>
                <div style="background: #090e1a; padding: 16px; border-radius: 12px; border: 1px solid var(--dark-border);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">Son Güncelleme</div>
                    <div class="mono" style="font-size: 0.9rem; color: var(--text-muted); margin-top: 4px;">{u_updated}</div>
                </div>
            </div>

            <!-- İlişkisel Bağlantılar (User's Jobs & Applications) -->
            <div style="display: flex; gap: 12px; margin-bottom: 28px; flex-wrap: wrap;">
                <a href="/users/{u_id}/jobs" class="btn btn-ghost" style="flex: 1; justify-content: center;">
                    💼 Bu Mezunun İlanları &rarr;
                </a>
                <a href="/users/{u_id}/applications" class="btn btn-ghost" style="flex: 1; justify-content: center;">
                    📝 Başvuruları &rarr;
                </a>
            </div>

            <!-- Aksiyon Butonları -->
            <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 20px; border-top: 1px solid var(--dark-border); flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; gap: 8px;">
                    <a href="/users/{u_id}/edit" class="btn btn-gold">✏️ Profili Düzenle</a>
                    <form action="/users/{u_id}/delete" method="POST" style="display: inline;" onsubmit="return confirm('Kullanıcı #{u_id} ({u_name}) silinecektir. Emin misiniz?');">
                        <button type="submit" class="btn btn-danger">🗑️ Üyeyi Sil</button>
                    </form>
                </div>
                <div style="display: flex; gap: 8px;">
                    <a href="/api/users/{u_id}" class="btn btn-ghost">⚡ API JSON</a>
                    <a href="/users" class="btn btn-ghost">&larr; Rehbere Dön</a>
                </div>
            </div>
        </div>
        """

        return Layout.render(
            title=f"Mezun Profili — {u_name}",
            active_nav="users",
            content=content,
            subtitle=f"İstanbul Üniversitesi #{u_id} numaralı üye ayrıntıları.",
            actions='<a href="/users" class="btn btn-ghost">&larr; Listeye Dön</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_users_edit(cls, user: Dict[str, Any], error: Optional[str] = None) -> str:
        """
        [U]pdate Form View: Displays edit form pre-filled with existing user details.
        Route: GET /users/{id}/edit -> UserController.edit(id)
        """
        alert_html = cls._render_alert(error=error)
        u_id = user.get('id')
        u_name = html.escape(str(user.get('name') or ''))
        u_email = html.escape(str(user.get('email') or ''))

        content = f"""
        <div class="card" style="max-width: 620px; margin: 0 auto; border-top: 4px solid var(--iu-gold);">
            <div style="margin-bottom: 24px;">
                <span class="badge badge-gold" style="margin-bottom: 10px;">Profili Düzenle [Update (U)]</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.5rem; color: #ffffff;">#{u_id} — Bilgileri Güncelle</h2>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 4px;">
                    Kullanıcının ad ve iletişim bilgilerini güncelleyin.
                </p>
            </div>

            <form action="/users/{u_id}" method="POST">
                <div class="form-group">
                    <label class="form-label" for="name">Ad Soyad</label>
                    <input type="text" id="name" name="name" class="form-control" value="{u_name}" required autofocus>
                </div>
                <div class="form-group">
                    <label class="form-label" for="email">E-Posta Adresi</label>
                    <input type="email" id="email" name="email" class="form-control" value="{u_email}" required>
                </div>
                <div style="display: flex; gap: 12px; margin-top: 28px;">
                    <button type="submit" class="btn btn-gold" style="flex: 1;">💾 Değişiklikleri Kaydet</button>
                    <a href="/users/{u_id}" class="btn btn-ghost">İptal</a>
                </div>
            </form>
        </div>
        """

        return Layout.render(
            title=f"Kullanıcı #{u_id} Düzenle",
            active_nav="users",
            content=content,
            subtitle="Kayıtlı üye verilerini düzenleme formu.",
            actions=f'<a href="/users/{u_id}" class="btn btn-ghost">&larr; Profile Dön</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_error_404(cls, message: str = "Aranan kayıt bulunamadı.") -> str:
        """Renders 404 Not Found view."""
        content = f"""
        <div class="card" style="max-width: 520px; margin: 40px auto; text-align: center; border-top: 4px solid var(--danger);">
            <div class="mono" style="font-size: 4rem; font-weight: 800; color: var(--danger); line-height: 1;">404</div>
            <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff; margin: 16px 0 10px;">Kayıt Bulunamadı</h2>
            <p style="color: var(--text-muted); margin-bottom: 24px;">{html.escape(message)}</p>
            <a href="/users" class="btn btn-burgundy">&larr; Kullanıcı Listesine Dön</a>
        </div>
        """
        return Layout.render(
            title="Kayıt Bulunamadı",
            active_nav="users",
            content=content
        )
