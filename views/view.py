"""
View Layer - MVC Architecture
Handles presentation and HTML rendering for Web Controllers.
Redesigned with high-trust Istanbul University Dark Theme, Alumni Directory Grid, and profile views.
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
        [R]ead: Renders the Alumni Directory Grid view with action triggers.
        Route: GET /users -> UserController.index()
        """
        alert_html = cls._render_alert(success, error)

        cards = ""
        if users:
            for u in users:
                u_id = u.get('id')
                u_name = html.escape(str(u.get('name') or 'İsimsiz Üye'))
                u_email = html.escape(str(u.get('email') or ''))
                u_created = html.escape(str(u.get('createdAt') or '-')[:10])

                # Get initials for avatar
                name_parts = u_name.split()
                initials = "".join([p[0].upper() for p in name_parts[:2] if p]) if name_parts else "İÜ"

                cards += f"""
                <div class="item-card">
                    <div>
                        <!-- Top Bar: Avatar & Identification -->
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 16px;">
                            <div style="display: flex; align-items: center; gap: 14px;">
                                <div class="avatar-box" style="font-family: 'Cinzel', serif; font-weight: 800; font-size: 1.1rem; color: #d4af37;">
                                    {initials}
                                </div>
                                <div>
                                    <h3 style="font-size: 1.15rem; font-weight: 700; color: #ffffff; line-height: 1.3;">
                                        <a href="/users/{u_id}" style="color: #ffffff; text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='#d4af37'" onmouseout="this.style.color='#ffffff'">
                                            {u_name}
                                        </a>
                                    </h3>
                                    <div style="display: flex; align-items: center; gap: 6px; margin-top: 3px;">
                                        <span class="badge badge-green" style="font-size: 0.72rem; padding: 2px 8px;">✓ Doğrulanmış Mezun</span>
                                    </div>
                                </div>
                            </div>
                            <span class="mono" style="font-weight: 700; color: var(--text-muted); font-size: 0.85rem;">#{u_id}</span>
                        </div>

                        <!-- Email & Info Chips -->
                        <div style="background: #090e1a; padding: 12px 14px; border-radius: 10px; border: 1px solid var(--dark-border); margin-bottom: 18px;">
                            <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">E-Posta & İletişim</div>
                            <div class="mono" style="font-size: 0.88rem; color: #cbd5e1; word-break: break-all; margin-top: 2px;">
                                {u_email}
                            </div>
                        </div>

                        <!-- Registration Meta -->
                        <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 18px;">
                            <span>Kayıt Tarihi:</span>
                            <span class="mono" style="color: #94a3b8; font-weight: 600;">{u_created}</span>
                        </div>
                    </div>

                    <div>
                        <!-- Relational Quick Links -->
                        <div style="display: flex; gap: 8px; margin-bottom: 12px; padding-top: 12px; border-top: 1px solid var(--dark-border);">
                            <a href="/users/{u_id}/jobs" class="filter-chip" style="flex: 1; justify-content: center; font-size: 0.78rem;">
                                💼 İlanları
                            </a>
                            <a href="/users/{u_id}/applications" class="filter-chip" style="flex: 1; justify-content: center; font-size: 0.78rem;">
                                📝 Başvuruları
                            </a>
                        </div>

                        <!-- Card Actions -->
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <a href="/users/{u_id}" class="btn btn-sm btn-ghost" style="flex: 1; justify-content: center;" title="Profili Görüntüle">👤 Profil</a>
                            <a href="/users/{u_id}/edit" class="btn btn-sm btn-gold" style="flex: 1; justify-content: center;" title="Profili Düzenle">✏️ Düzenle</a>
                            <form action="/users/{u_id}/delete" method="POST" style="display: inline-block;" onsubmit="return confirm('Kullanıcı #{u_id} ({u_name}) silinsin mi?');">
                                <button type="submit" class="btn btn-sm btn-danger" title="Kullanıcıyı Sil" style="padding: 6px 10px;">🗑️</button>
                            </form>
                        </div>
                    </div>
                </div>
                """
        else:
            cards = """
            <div style="grid-column: 1 / -1; padding: 60px 24px; text-align: center; background: var(--dark-card); border: 1px solid var(--dark-border); border-radius: 18px;">
                <div style="font-size: 3rem; margin-bottom: 12px;">👥</div>
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 8px;">Kayıtlı Mezun Bulunamadı</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 480px; margin: 0 auto 20px;">
                    İlk mezun veya öğrenci kaydını ekleyerek İstanbul Üniversitesi ağına dahil edin.
                </p>
                <a href="/users/create" class="btn btn-burgundy">+ Yeni Mezun Ekle</a>
            </div>
            """

        content = f"""
        <!-- İstatistik ve Durum Şeridi -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 28px;">
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: var(--iu-gold-light);">{count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Kayıtlı İÜ Mezunu & Üyesi</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: var(--success);">Aktif</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Veritabanı Durumu (SQLite)</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: #60a5fa;">RBAC</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Yetkilendirme Seviyesi</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: #c084fc;">%100</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Doğrulanmış İÜ Profili</div>
            </div>
        </div>

        <!-- Filtre ve Hızlı İşlemler Çubuğu -->
        <div class="filter-bar">
            <div class="filter-group">
                <span class="filter-chip active">Tüm Mezunlar ({count})</span>
                <span class="filter-chip">⚖️ Hukuk</span>
                <span class="filter-chip">🩺 Tıp</span>
                <span class="filter-chip">📈 İktisat</span>
                <span class="filter-chip">💻 Bilişim</span>
            </div>
            <div style="display: flex; gap: 8px;">
                <a href="/api/users" class="btn btn-sm btn-ghost" title="REST API JSON">⚡ API JSON</a>
                <a href="/users/create" class="btn btn-sm btn-burgundy">+ Yeni Mezun Ekle</a>
            </div>
        </div>

        <!-- Mezunlar Izgarası (Bento Grid) -->
        <div class="item-grid">
            {cards}
        </div>

        <!-- Hızlı Üye Ekleme Kartı (In-Page Quick Create) -->
        <div class="card" style="margin-top: 36px; position: relative;">
            <div style="margin-bottom: 20px;">
                <span class="badge badge-burgundy" style="margin-bottom: 8px;">Hızlı İşlem</span>
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.3rem; color: #ffffff;">Anında Mezun Kaydı Oluştur</h3>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 2px;">
                    Formu doldurarak veritabanına doğrudan yeni bir mezun veya öğrenci profili tanımlayın.
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
                <button type="submit" class="btn btn-burgundy" style="height: 48px; padding: 0 24px;">+ Mezunu Kaydet</button>
            </form>
        </div>
        """

        return Layout.render(
            title="Mezun & Öğrenci Rehberi",
            active_nav="users",
            content=content,
            subtitle="İstanbul Üniversitesi mezun ve akademisyen ağının doğrulanmış üyeleri.",
            actions='<a href="/users/create" class="btn btn-burgundy">+ Yeni Kullanıcı Ekle</a>',
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
        <div class="card" style="max-width: 660px; margin: 0 auto; position: relative;">
            <div style="margin-bottom: 26px; border-bottom: 1px solid var(--dark-border); padding-bottom: 18px;">
                <span class="badge badge-burgundy" style="margin-bottom: 10px;">Yeni Üyelik Formu</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff;">Mezun Kaydı Oluşturun</h2>
                <p style="font-size: 0.92rem; color: var(--text-muted); margin-top: 4px;">
                    Platforma dahil edilecek mezun veya öğrencinin iletişim bilgilerini sisteme kaydedin.
                </p>
            </div>

            <form action="/users" method="POST">
                <div class="form-group">
                    <label class="form-label" for="name">Ad Soyad *</label>
                    <input type="text" id="name" name="name" class="form-control" placeholder="Örn: Selin Yılmaz" required autofocus>
                </div>
                <div class="form-group">
                    <label class="form-label" for="email">Kurumsal / Kişisel E-Posta *</label>
                    <input type="email" id="email" name="email" class="form-control" placeholder="Örn: selin.yilmaz@alumni.istanbul.edu.tr" required>
                </div>
                <div style="display: flex; gap: 12px; margin-top: 30px;">
                    <button type="submit" class="btn btn-burgundy" style="flex: 1; justify-content: center; font-size: 1rem; padding: 12px;">+ Kullanıcıyı Kaydet</button>
                    <a href="/users" class="btn btn-ghost" style="padding: 12px 20px;">İptal / Listeye Dön</a>
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

        name_parts = u_name.split()
        initials = "".join([p[0].upper() for p in name_parts[:2] if p]) if name_parts else "İÜ"

        content = f"""
        <div class="card" style="max-width: 760px; margin: 0 auto; position: relative;">
            
            <!-- Profil Üst Başlığı -->
            <div style="display: flex; align-items: center; gap: 22px; margin-bottom: 28px; padding-bottom: 24px; border-bottom: 1px solid var(--dark-border); flex-wrap: wrap;">
                <div style="width: 80px; height: 80px; border-radius: 20px; background: linear-gradient(135deg, var(--iu-burgundy), #4c0519); border: 2px solid #d4af37; display: flex; align-items: center; justify-content: center; font-family: 'Cinzel', serif; font-size: 1.8rem; font-weight: 800; color: #ffffff; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);">
                    {initials}
                </div>
                <div style="flex: 1;">
                    <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                        <h2 style="font-family: 'Cinzel', serif; font-size: 1.8rem; color: #ffffff;">{u_name}</h2>
                        <span class="badge badge-green">✓ Doğrulanmış Mezun</span>
                    </div>
                    <p style="color: #d4af37; font-size: 0.95rem; font-weight: 600; margin-top: 4px;">
                        İstanbul Üniversitesi Mezunlar & Kariyer Ağı Üyesi
                    </p>
                </div>
            </div>

            <!-- Bilgi Izgarası (Bento) -->
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 18px; margin-bottom: 28px;">
                <div style="background: #090e1a; padding: 18px; border-radius: 14px; border: 1px solid var(--dark-border);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">Üye / Mezun Numarası</div>
                    <div class="mono" style="font-size: 1.3rem; color: #d4af37; font-weight: 800; margin-top: 4px;">#{u_id}</div>
                </div>
                <div style="background: #090e1a; padding: 18px; border-radius: 14px; border: 1px solid var(--dark-border);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">Resmi İletişim E-Postası</div>
                    <div class="mono" style="font-size: 0.95rem; color: #ffffff; margin-top: 4px; word-break: break-all;">{u_email}</div>
                </div>
                <div style="background: #090e1a; padding: 18px; border-radius: 14px; border: 1px solid var(--dark-border);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">Ağa Katılım Tarihi</div>
                    <div class="mono" style="font-size: 0.92rem; color: var(--text-muted); margin-top: 4px;">{u_created}</div>
                </div>
                <div style="background: #090e1a; padding: 18px; border-radius: 14px; border: 1px solid var(--dark-border);">
                    <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700; letter-spacing: 0.5px;">Son Güncelleme</div>
                    <div class="mono" style="font-size: 0.92rem; color: var(--text-muted); margin-top: 4px;">{u_updated}</div>
                </div>
            </div>

            <!-- İlişkisel Bağlantılar (User's Jobs & Applications) -->
            <div style="display: flex; gap: 14px; margin-bottom: 28px; flex-wrap: wrap;">
                <a href="/users/{u_id}/jobs" class="btn btn-ghost" style="flex: 1; justify-content: center; padding: 12px;">
                    💼 Bu Mezunun İlanları &rarr;
                </a>
                <a href="/users/{u_id}/applications" class="btn btn-ghost" style="flex: 1; justify-content: center; padding: 12px;">
                    📝 Aday Başvuruları &rarr;
                </a>
            </div>

            <!-- Aksiyon Butonları -->
            <div style="display: flex; justify-content: space-between; align-items: center; padding-top: 22px; border-top: 1px solid var(--dark-border); flex-wrap: wrap; gap: 14px;">
                <div style="display: flex; gap: 10px;">
                    <a href="/users/{u_id}/edit" class="btn btn-gold">✏️ Profili Düzenle</a>
                    <form action="/users/{u_id}/delete" method="POST" style="display: inline;" onsubmit="return confirm('Kullanıcı #{u_id} ({u_name}) silinecektir. Emin misiniz?');">
                        <button type="submit" class="btn btn-danger">🗑️ Üyeyi Sil</button>
                    </form>
                </div>
                <div style="display: flex; gap: 10px;">
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
        <div class="card" style="max-width: 660px; margin: 0 auto; position: relative;">
            <div style="margin-bottom: 26px; border-bottom: 1px solid var(--dark-border); padding-bottom: 18px;">
                <span class="badge badge-gold" style="margin-bottom: 10px;">Profili Düzenle</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff;">#{u_id} — Bilgileri Güncelleyin</h2>
                <p style="font-size: 0.92rem; color: var(--text-muted); margin-top: 4px;">
                    Mezunun ad ve kurumsal iletişim bilgilerini güncelleyin.
                </p>
            </div>

            <form action="/users/{u_id}" method="POST">
                <div class="form-group">
                    <label class="form-label" for="name">Ad Soyad *</label>
                    <input type="text" id="name" name="name" class="form-control" value="{u_name}" required autofocus>
                </div>
                <div class="form-group">
                    <label class="form-label" for="email">E-Posta Adresi *</label>
                    <input type="email" id="email" name="email" class="form-control" value="{u_email}" required>
                </div>
                <div style="display: flex; gap: 12px; margin-top: 30px;">
                    <button type="submit" class="btn btn-gold" style="flex: 1; justify-content: center; font-size: 1rem; padding: 12px;">💾 Değişiklikleri Kaydet</button>
                    <a href="/users/{u_id}" class="btn btn-ghost" style="padding: 12px 20px;">İptal</a>
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
    def render_register(cls, departments: List[Dict[str, Any]], error: Optional[str] = None, form_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Registration View: Renders standalone self-registration page for Students and Alumni.
        Route: GET /register -> AuthController.register_form()
        """
        alert_html = cls._render_alert(error=error)
        fd = form_data or {}

        selected_role = str(fd.get("role") or "alumni").lower()
        if selected_role not in ("student", "alumni"):
            selected_role = "alumni"

        first_name = html.escape(str(fd.get("first_name") or ""))
        last_name = html.escape(str(fd.get("last_name") or ""))
        email = html.escape(str(fd.get("email") or ""))
        phone = html.escape(str(fd.get("phone") or ""))
        linkedin_url = html.escape(str(fd.get("linkedin_url") or ""))
        bio = html.escape(str(fd.get("bio") or ""))
        selected_dept = str(fd.get("department_id") or "")

        # Student fields
        student_number = html.escape(str(fd.get("student_number") or ""))
        current_semester = html.escape(str(fd.get("current_semester") or "1"))

        # Alumni fields
        graduation_year = html.escape(str(fd.get("graduation_year") or "2024"))
        current_company = html.escape(str(fd.get("current_company") or ""))
        current_title = html.escape(str(fd.get("current_title") or ""))
        industry = html.escape(str(fd.get("industry") or ""))
        is_mentor_checked = "checked" if str(fd.get("is_mentor_available") or "").lower() in ("1", "true", "on", "yes") else ""

        dept_options = ""
        for d in departments:
            d_id = str(d.get("id"))
            d_label = html.escape(f"{d.get('faculty_name')} — {d.get('department_name')} ({d.get('code')})")
            sel = " selected" if d_id == selected_dept else ""
            dept_options += f'<option value="{d_id}"{sel}>{d_label}</option>\n'

        student_display = "block" if selected_role == "student" else "none"
        alumni_display = "block" if selected_role == "alumni" else "none"
        student_checked = "checked" if selected_role == "student" else ""
        alumni_checked = "checked" if selected_role == "alumni" else ""

        content = f"""
        <div class="card" style="max-width: 780px; margin: 0 auto; position: relative;">
            <div style="margin-bottom: 26px; border-bottom: 1px solid var(--dark-border); padding-bottom: 18px;">
                <span class="badge badge-burgundy" style="margin-bottom: 10px;">İÜ Mezun & Öğrenci Ağı</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.75rem; color: #ffffff;">Platforma Kayıt Olun</h2>
                <p style="font-size: 0.94rem; color: var(--text-muted); margin-top: 4px;">
                    İstanbul Üniversitesi kariyer fırsatlarına, mentorluk ağına ve mezun topluluğuna katılmak için hesabınızı oluşturun.
                </p>
            </div>

            <form action="/register" method="POST" id="registerForm">
                <!-- Rol Seçimi -->
                <div class="form-group">
                    <label class="form-label">Üyelik Rolünüz *</label>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
                        <label style="display: flex; align-items: center; gap: 12px; padding: 14px 16px; background: #090e1a; border: 1px solid var(--dark-border); border-radius: 12px; cursor: pointer;">
                            <input type="radio" name="role" value="alumni" {alumni_checked} onchange="toggleRoleFields('alumni')" style="accent-color: #881337; width: 18px; height: 18px;">
                            <div>
                                <div style="font-weight: 700; color: #ffffff;">🏛️ Mezun (Alumni)</div>
                                <div style="font-size: 0.78rem; color: var(--text-muted);">İlan yayınlayabilir ve mentorluk yapabilirsiniz</div>
                            </div>
                        </label>
                        <label style="display: flex; align-items: center; gap: 12px; padding: 14px 16px; background: #090e1a; border: 1px solid var(--dark-border); border-radius: 12px; cursor: pointer;">
                            <input type="radio" name="role" value="student" {student_checked} onchange="toggleRoleFields('student')" style="accent-color: #881337; width: 18px; height: 18px;">
                            <div>
                                <div style="font-weight: 700; color: #ffffff;">🎓 Öğrenci (Student)</div>
                                <div style="font-size: 0.78rem; color: var(--text-muted);">Staj/iş ilanlarına ve mentorluğa başvurabilirsiniz</div>
                            </div>
                        </label>
                    </div>
                </div>

                <!-- Ad & Soyad -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                        <label class="form-label" for="first_name">Ad *</label>
                        <input type="text" id="first_name" name="first_name" class="form-control" value="{first_name}" placeholder="Örn: Zehra" required autofocus>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="last_name">Soyad *</label>
                        <input type="text" id="last_name" name="last_name" class="form-control" value="{last_name}" placeholder="Örn: Yaşar" required>
                    </div>
                </div>

                <!-- E-posta & Telefon -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                        <label class="form-label" for="email">E-Posta Adresi *</label>
                        <input type="email" id="email" name="email" class="form-control" value="{email}" placeholder="ornek@istanbul.edu.tr" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="phone">Telefon (Opsiyonel)</label>
                        <input type="tel" id="phone" name="phone" class="form-control" value="{phone}" placeholder="+90 555 000 00 00">
                    </div>
                </div>

                <!-- Şifre & Şifre Tekrarı -->
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                        <label class="form-label" for="password">Şifre (En az 6 karakter) *</label>
                        <input type="password" id="password" name="password" class="form-control" minlength="6" placeholder="••••••" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="password_confirm">Şifre Tekrarı *</label>
                        <input type="password" id="password_confirm" name="password_confirm" class="form-control" minlength="6" placeholder="••••••" required>
                    </div>
                </div>

                <!-- Bölüm Seçimi -->
                <div class="form-group">
                    <label class="form-label" for="department_id">Fakülte & Bölüm *</label>
                    <select id="department_id" name="department_id" class="form-control" required>
                        {dept_options}
                    </select>
                </div>

                <!-- Öğrenciye Özel Alanlar -->
                <div id="student-fields" style="display: {student_display}; background: rgba(9, 14, 26, 0.7); padding: 18px; border-radius: 14px; border: 1px solid var(--dark-border); margin-bottom: 20px;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #d4af37; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;">
                        🎓 Öğrenci Akademik Bilgileri
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div class="form-group" style="margin-bottom: 0;">
                            <label class="form-label" for="student_number">Öğrenci Numarası *</label>
                            <input type="text" id="student_number" name="student_number" class="form-control" value="{student_number}" placeholder="Örn: 1306200045">
                        </div>
                        <div class="form-group" style="margin-bottom: 0;">
                            <label class="form-label" for="current_semester">Mevcut Dönem (1-12)</label>
                            <input type="number" id="current_semester" name="current_semester" class="form-control" min="1" max="12" value="{current_semester}">
                        </div>
                    </div>
                </div>

                <!-- Mezuna Özel Alanlar -->
                <div id="alumni-fields" style="display: {alumni_display}; background: rgba(9, 14, 26, 0.7); padding: 18px; border-radius: 14px; border: 1px solid var(--dark-border); margin-bottom: 20px;">
                    <div style="font-size: 0.85rem; font-weight: 700; color: #d4af37; margin-bottom: 12px; text-transform: uppercase; letter-spacing: 0.5px;">
                        🏛️ Mezuniyet & Kariyer Bilgileri
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div class="form-group">
                            <label class="form-label" for="graduation_year">Mezuniyet Yılı *</label>
                            <input type="number" id="graduation_year" name="graduation_year" class="form-control" min="1950" max="2030" value="{graduation_year}">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="industry">Sektör (Opsiyonel)</label>
                            <input type="text" id="industry" name="industry" class="form-control" value="{industry}" placeholder="Örn: Yazılım, Finans, Hukuk">
                        </div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                        <div class="form-group">
                            <label class="form-label" for="current_company">Mevcut Kurum / Şirket</label>
                            <input type="text" id="current_company" name="current_company" class="form-control" value="{current_company}" placeholder="Örn: Aselsan / İstanbul Üniversitesi">
                        </div>
                        <div class="form-group">
                            <label class="form-label" for="current_title">Pozisyon / Unvan</label>
                            <input type="text" id="current_title" name="current_title" class="form-control" value="{current_title}" placeholder="Örn: Kıdemli Yazılım Mühendisi">
                        </div>
                    </div>
                    <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; color: #e2e8f0; font-size: 0.9rem;">
                        <input type="checkbox" name="is_mentor_available" value="1" {is_mentor_checked} style="accent-color: #881337; width: 17px; height: 17px;">
                        <span>Öğrencilere gönüllü kariyer mentorluğu yapmak istiyorum</span>
                    </label>
                </div>

                <!-- LinkedIn & Kısa Özgeçmiş -->
                <div class="form-group">
                    <label class="form-label" for="linkedin_url">LinkedIn Profili (Opsiyonel)</label>
                    <input type="url" id="linkedin_url" name="linkedin_url" class="form-control" value="{linkedin_url}" placeholder="https://www.linkedin.com/in/kullanici">
                </div>
                <div class="form-group">
                    <label class="form-label" for="bio">Kısa Biyografi / İlgi Alanları (Opsiyonel)</label>
                    <textarea id="bio" name="bio" class="form-control" rows="3" placeholder="Kendinizden ve mesleki hedeflerinizden kısaca bahsedin...">{bio}</textarea>
                </div>

                <div style="display: flex; gap: 12px; margin-top: 28px;">
                    <button type="submit" class="btn btn-burgundy" style="flex: 1; justify-content: center; font-size: 1rem; padding: 13px;">✓ Kaydı Tamamla</button>
                    <a href="/users" class="btn btn-ghost" style="padding: 13px 22px;">Vazgeç</a>
                </div>
            </form>
        </div>

        <script>
            function toggleRoleFields(role) {{
                const studentBox = document.getElementById('student-fields');
                const alumniBox = document.getElementById('alumni-fields');
                const studentNumInput = document.getElementById('student_number');
                const gradYearInput = document.getElementById('graduation_year');
                if (role === 'student') {{
                    studentBox.style.display = 'block';
                    alumniBox.style.display = 'none';
                    if (studentNumInput) studentNumInput.required = true;
                    if (gradYearInput) gradYearInput.required = false;
                }} else {{
                    studentBox.style.display = 'none';
                    alumniBox.style.display = 'block';
                    if (studentNumInput) studentNumInput.required = false;
                    if (gradYearInput) gradYearInput.required = true;
                }}
            }}
            document.addEventListener('DOMContentLoaded', function() {{
                toggleRoleFields('{selected_role}');
            }});
        </script>
        """

        return Layout.render(
            title="Kayıt Ol — Mezun & Öğrenci Ağı",
            active_nav="users",
            content=content,
            subtitle="İstanbul Üniversitesi resmi mezun ve öğrenci ağına yeni üyelik kaydı.",
            actions='<a href="/users" class="btn btn-ghost">&larr; Mezun Rehberine Dön</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_login(cls, error: Optional[str] = None, success: Optional[str] = None, email: str = "") -> str:
        """
        Login View: Renders standalone sign-in page for Alumni, Students, Coordinators, and Admins.
        Route: GET /login -> AuthController.login_form()
        """
        alert_html = cls._render_alert(success=success, error=error)
        email_val = html.escape(str(email or ""))

        content = f"""
        <div class="card" style="max-width: 500px; margin: 24px auto; position: relative;">
            <div style="margin-bottom: 26px; border-bottom: 1px solid var(--dark-border); padding-bottom: 18px; text-align: center;">
                <div style="font-size: 2.2rem; margin-bottom: 8px;">🏛️</div>
                <span class="badge badge-burgundy" style="margin-bottom: 10px;">İÜ Mezun & Öğrenci Oturumu</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.7rem; color: #ffffff;">Giriş Yapın</h2>
                <p style="font-size: 0.92rem; color: var(--text-muted); margin-top: 4px;">
                    Kayıtlı e-posta adresiniz ve şifrenizle platforma erişin.
                </p>
            </div>

            <form action="/login" method="POST">
                <div class="form-group">
                    <label class="form-label" for="email">E-Posta Adresi *</label>
                    <input type="email" id="email" name="email" class="form-control" value="{email_val}" placeholder="ornek@istanbul.edu.tr" required autofocus>
                </div>

                <div class="form-group">
                    <label class="form-label" for="password">Şifre *</label>
                    <input type="password" id="password" name="password" class="form-control" placeholder="••••••" required>
                </div>

                <div style="display: flex; flex-direction: column; gap: 12px; margin-top: 26px;">
                    <button type="submit" class="btn btn-burgundy" style="width: 100%; justify-content: center; font-size: 1rem; padding: 13px;">🔐 Giriş Yap</button>
                </div>
            </form>

            <div style="margin-top: 24px; padding-top: 18px; border-top: 1px solid var(--dark-border); text-align: center; font-size: 0.9rem; color: var(--text-muted);">
                Henüz hesabınız yok mu?
                <a href="/register" style="color: #d4af37; font-weight: 700; text-decoration: none; margin-left: 4px;">📝 Hemen Kayıt Olun &rarr;</a>
            </div>
        </div>
        """

        return Layout.render(
            title="Giriş Yap — İÜ Mezun Ağı",
            active_nav="home",
            content=content,
            subtitle="İstanbul Üniversitesi Mezun Bilgi & Kariyer Ağı üye girişi.",
            actions='<a href="/register" class="btn btn-ghost">📝 Kayıt Ol</a>',
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
