"""
Announcement View Layer - MVC Architecture
Renders rich, responsive management interface and HTML templates for Announcements.
Redesigned with high-trust Istanbul University Dark Theme, Magazine News Cards, and Category Filters.
"""
from typing import Dict, Any, Optional, List
import html
from views.layout import Layout


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
    def _category_badge(cls, category: str) -> str:
        cat_lower = (category or "").lower()
        if "etkinlik" in cat_lower:
            return f'<span class="badge badge-purple">🎉 {html.escape(category)}</span>'
        elif "kariyer" in cat_lower or "staj" in cat_lower:
            return f'<span class="badge badge-green">💼 {html.escape(category)}</span>'
        elif "akademik" in cat_lower:
            return f'<span class="badge badge-gold">🎓 {html.escape(category)}</span>'
        return f'<span class="badge badge-blue">📢 {html.escape(category)}</span>'

    @classmethod
    def render_index(cls, announcements: List[Dict[str, Any]], count: int, error: Optional[str] = None, success: Optional[str] = None) -> str:
        """
        Management Interface: Lists announcements with statistics, magazine grid, and action triggers.
        Route: GET /announcements -> AnnouncementController.index()
        """
        alert_html = cls._render_alert(success, error)

        # Statistics
        active_count = sum(1 for a in announcements if a.get("status") == "Aktif")
        categories_count = len(set(a.get("category", "Genel") for a in announcements))

        cards = ""
        if announcements:
            for a in announcements:
                a_id = a.get('id')
                title = html.escape(str(a.get('title') or 'Başlıksız Duyuru'))
                raw_content = str(a.get('content') or '')
                preview_content = html.escape((raw_content[:140] + "...") if len(raw_content) > 140 else raw_content)
                badge = cls._category_badge(a.get("category", "Genel"))
                author = html.escape(str(a.get('author') or 'Koordinatörlük'))
                created_date = html.escape(str(a.get('createdAt') or '-')[:10])

                cards += f"""
                <div class="item-card">
                    <div>
                        <!-- Card Header: Category & Date -->
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
                            <div>{badge}</div>
                            <div style="display: flex; align-items: center; gap: 8px;">
                                <span class="mono" style="font-size: 0.8rem; color: var(--text-muted);">{created_date}</span>
                                <span class="mono" style="font-size: 0.82rem; color: #d4af37; font-weight: 700;">#{a_id}</span>
                            </div>
                        </div>

                        <!-- Announcement Headline -->
                        <h3 style="font-size: 1.2rem; font-weight: 700; color: #ffffff; line-height: 1.4; margin-bottom: 10px;">
                            <a href="/announcements/{a_id}" style="color: #ffffff; text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='#d4af37'" onmouseout="this.style.color='#ffffff'">
                                {title}
                            </a>
                        </h3>

                        <!-- Excerpt -->
                        <p style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6; margin-bottom: 18px;">
                            {preview_content}
                        </p>
                    </div>

                    <div>
                        <!-- Author / Unit -->
                        <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 12px; border-top: 1px solid var(--dark-border); margin-bottom: 14px; font-size: 0.82rem; color: var(--text-muted);">
                            <span style="display: flex; align-items: center; gap: 6px;">
                                <span>🏛️</span> <span style="color: #e2e8f0; font-weight: 500;">{author}</span>
                            </span>
                            <span class="badge badge-green" style="font-size: 0.72rem; padding: 2px 8px;">Aktif</span>
                        </div>

                        <!-- Action Triggers -->
                        <div style="display: flex; gap: 8px; align-items: center;">
                            <a href="/announcements/{a_id}" class="btn btn-sm btn-ghost" style="flex: 1; justify-content: center;" title="Duyuruyu Oku">👁️ Oku</a>
                            <a href="/announcements/{a_id}/edit" class="btn btn-sm btn-gold" style="flex: 1; justify-content: center;" title="Düzenle">✏️ Düzenle</a>
                            <form action="/announcements/{a_id}/delete" method="POST" style="display: inline-block;" onsubmit="return confirm('Duyuru #{a_id} ({title}) silinsin mi?');">
                                <button type="submit" class="btn btn-sm btn-danger" title="Duyuruyu Sil" style="padding: 6px 10px;">🗑️</button>
                            </form>
                        </div>
                    </div>
                </div>
                """
        else:
            cards = """
            <div style="grid-column: 1 / -1; padding: 60px 24px; text-align: center; background: var(--dark-card); border: 1px solid var(--dark-border); border-radius: 18px;">
                <div style="font-size: 3rem; margin-bottom: 12px;">📢</div>
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 8px;">Henüz Duyuru Bulunmuyor</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 480px; margin: 0 auto 20px;">
                    İlk kurumsal haberi veya etkinlik duyurusunu yayınlayarak mezun topluluğuna iletin.
                </p>
                <a href="/announcements/create" class="btn btn-burgundy">+ İlk Duyuruyu Yayınla</a>
            </div>
            """

        content = f"""
        <!-- İstatistik Şeridi (Bento) -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 28px;">
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: var(--iu-gold-light);">{count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Toplam Duyuru & Etkinlik</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: var(--success);">{active_count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Aktif / Yayında</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: #c084fc;">{categories_count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Farklı Kategori</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: #60a5fa;">Canlı</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Rektörlük Bilgi Akışı</div>
            </div>
        </div>

        <!-- Filtre ve Hızlı İşlem Çubuğu -->
        <div class="filter-bar">
            <div class="filter-group">
                <span class="filter-chip active">Tüm Duyurular ({count})</span>
                <span class="filter-chip">🎉 Etkinlik & Zirve</span>
                <span class="filter-chip">💼 Kariyer & Staj</span>
                <span class="filter-chip">🎓 Akademik</span>
                <span class="filter-chip">📢 Genel</span>
            </div>
            <div style="display: flex; gap: 8px;">
                <a href="/api/announcements" class="btn btn-sm btn-ghost" title="REST API JSON">⚡ API JSON</a>
                <a href="/announcements/create" class="btn btn-sm btn-burgundy">+ Yeni Duyuru Ekle</a>
            </div>
        </div>

        <!-- Duyurular Izgarası (Bento Grid) -->
        <div class="item-grid">
            {cards}
        </div>

        <!-- Hızlı Duyuru Yayınlama Kartı (Quick Create) -->
        <div class="card" style="margin-top: 36px; position: relative;">
            <div style="margin-bottom: 20px;">
                <span class="badge badge-burgundy" style="margin-bottom: 8px;">Hızlı Yayın</span>
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.3rem; color: #ffffff;">Hızlı Duyuru Bildirimi Oluştur</h3>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 2px;">
                    Üniversite mezunlarına ve öğrencilerine anında duyuru ve etkinlik bildirimi iletin.
                </p>
            </div>

            <form action="/announcements" method="POST">
                <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 16px; margin-bottom: 16px;">
                    <div class="form-group" style="margin-bottom: 0;">
                        <label class="form-label" for="title">Duyuru Başlığı</label>
                        <input type="text" id="title" name="title" class="form-control" placeholder="Örn: 2026 Mezunlar Zirvesi & Kokteyli" required>
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label class="form-label" for="category">Kategori</label>
                        <select id="category" name="category" class="form-control">
                            <option value="Genel">📢 Genel</option>
                            <option value="Etkinlik">🎉 Etkinlik</option>
                            <option value="Kariyer">💼 Kariyer / Staj</option>
                            <option value="Akademik">🎓 Akademik</option>
                        </select>
                    </div>
                    <div class="form-group" style="margin-bottom: 0;">
                        <label class="form-label" for="author">Yayınlayan Birim</label>
                        <input type="text" id="author" name="author" class="form-control" value="İÜ Mezunlar Koordinatörlüğü">
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="content">Duyuru Metni & Detayları</label>
                    <textarea id="content" name="content" class="form-control" rows="3" placeholder="Duyuru metnini ve etkinlik detaylarını giriniz..." required></textarea>
                </div>

                <button type="submit" class="btn btn-burgundy" style="padding: 12px 24px; font-size: 0.95rem;">📢 Duyuruyu Yayınla</button>
            </form>
        </div>
        """

        return Layout.render(
            title="Duyurular & Etkinlikler",
            active_nav="announcements",
            content=content,
            subtitle="İstanbul Üniversitesi Rektörlüğü ve Fakültelerinden resmi duyuru ve etkinlik akışı.",
            actions='<a href="/announcements/create" class="btn btn-burgundy">+ Yeni Duyuru Ekle</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_create(cls, error: Optional[str] = None) -> str:
        """
        [C]reate Form View: Standalone announcement creation page.
        Route: GET /announcements/create -> AnnouncementController.create()
        """
        alert_html = cls._render_alert(error=error)

        content = f"""
        <div class="card" style="max-width: 720px; margin: 0 auto; position: relative;">
            <div style="margin-bottom: 26px; border-bottom: 1px solid var(--dark-border); padding-bottom: 18px;">
                <span class="badge badge-burgundy" style="margin-bottom: 10px;">Yeni Duyuru Formu</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff;">Duyuru & Haber Yayınlayın</h2>
                <p style="font-size: 0.92rem; color: var(--text-muted); margin-top: 4px;">
                    Platform üyeleri ve mezunlar için yeni bir haber veya etkinlik akışı tanımlayın.
                </p>
            </div>

            <form action="/announcements" method="POST">
                <div class="form-group">
                    <label class="form-label" for="title">Duyuru Başlığı *</label>
                    <input type="text" id="title" name="title" class="form-control" placeholder="Örn: 2026 Yıllık Mezunlar Networking Zirvesi" required autofocus>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                        <label class="form-label" for="category">Kategori</label>
                        <select id="category" name="category" class="form-control">
                            <option value="Genel">📢 Genel Bilgilendirme</option>
                            <option value="Etkinlik">🎉 Etkinlik & Buluşma</option>
                            <option value="Kariyer">💼 Kariyer & Staj</option>
                            <option value="Akademik">🎓 Akademik Seminer</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="author">Yayınlayan Birim *</label>
                        <input type="text" id="author" name="author" class="form-control" value="Rektörlük Mezunlar Koordinatörlüğü" required>
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="content">Duyuru İçeriği *</label>
                    <textarea id="content" name="content" class="form-control" rows="6" placeholder="Duyurunun tam metnini ve program akışını yazınız..." required></textarea>
                </div>

                <div style="display: flex; gap: 12px; margin-top: 30px;">
                    <button type="submit" class="btn btn-burgundy" style="flex: 1; justify-content: center; font-size: 1rem; padding: 12px;">📢 Duyuruyu Yayınla</button>
                    <a href="/announcements" class="btn btn-ghost" style="padding: 12px 20px;">İptal</a>
                </div>
            </form>
        </div>
        """

        return Layout.render(
            title="Yeni Duyuru Oluştur",
            active_nav="announcements",
            content=content,
            subtitle="İÜ Mezun Platformunda yeni bir haber veya duyuru yayınlama formu.",
            actions='<a href="/announcements" class="btn btn-ghost">&larr; Duyuru Listesine Dön</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_show(cls, announcement: Dict[str, Any], success: Optional[str] = None, error: Optional[str] = None) -> str:
        """
        [R]ead Detail View: Displays single announcement with full content and management actions.
        Route: GET /announcements/{id} -> AnnouncementController.show(id)
        """
        alert_html = cls._render_alert(success, error)
        a_id = announcement.get('id')
        title = html.escape(str(announcement.get('title') or 'Duyuru'))
        content_text = html.escape(str(announcement.get('content') or ''))
        badge = cls._category_badge(announcement.get("category", "Genel"))
        author = html.escape(str(announcement.get('author') or 'İÜ Rektörlüğü'))
        created_date = html.escape(str(announcement.get('createdAt') or '-')[:19])
        status = html.escape(str(announcement.get('status', 'Aktif')))
        updated_box = f"<div style='font-size:0.82rem; color:var(--text-muted); margin-top:10px; background:#090e1a; padding:8px 14px; border-radius:8px;'>Son Güncelleme: {html.escape(str(announcement.get('updatedAt')))}</div>" if announcement.get('updatedAt') else ""

        content = f"""
        <div class="card" style="max-width: 860px; margin: 0 auto; position: relative;">
            
            <!-- Duyuru Üst Başlığı -->
            <div style="margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--dark-border);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 12px; flex-wrap: wrap;">
                    <span class="mono" style="color: #d4af37; font-weight: 800; font-size: 0.95rem;">#{a_id}</span>
                    {badge}
                    <span class="badge badge-green">✓ {status}</span>
                </div>
                <h2 style="font-family: 'Cinzel', serif; font-size: 2.1rem; color: #ffffff; letter-spacing: 0.5px; line-height: 1.3;">
                    {title}
                </h2>
            </div>

            <!-- Meta Bilgiler Şeridi -->
            <div style="display: flex; gap: 24px; margin-bottom: 28px; font-size: 0.92rem; color: var(--text-muted); flex-wrap: wrap; background: #090e1a; padding: 16px 20px; border-radius: 14px; border: 1px solid var(--dark-border);">
                <div>🏛️ <strong style="color: #ffffff;">Yayınlayan Birim:</strong> {author}</div>
                <div>📅 <strong style="color: #ffffff;">Yayın Tarihi:</strong> <span class="mono" style="color: #cbd5e1;">{created_date}</span></div>
            </div>

            <!-- Duyuru İçeriği -->
            <div style="font-size: 1.05rem; line-height: 1.85; color: #cbd5e1; white-space: pre-wrap; margin-bottom: 32px; background: rgba(9, 14, 26, 0.5); padding: 24px; border-radius: 14px; border: 1px solid var(--dark-border);">
                {content_text}
            </div>

            {updated_box}

            <!-- Alt Aksiyonlar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 24px; border-top: 1px solid var(--dark-border); flex-wrap: wrap; gap: 14px;">
                <div style="display: flex; gap: 10px;">
                    <a href="/announcements/{a_id}/edit" class="btn btn-gold">✏️ Duyuruyu Düzenle</a>
                    <form action="/announcements/{a_id}/delete" method="POST" style="display: inline;" onsubmit="return confirm('Duyuru #{a_id} silinecektir. Emin misiniz?');">
                        <button type="submit" class="btn btn-danger">🗑️ Duyuruyu Sil</button>
                    </form>
                </div>
                <div style="display: flex; gap: 10px;">
                    <a href="/api/announcements/{a_id}" class="btn btn-ghost">⚡ API JSON</a>
                    <a href="/announcements" class="btn btn-ghost">&larr; Tüm Duyurulara Dön</a>
                </div>
            </div>
        </div>
        """

        return Layout.render(
            title=title,
            active_nav="announcements",
            content=content,
            subtitle="İstanbul Üniversitesi Mezunlar Portalı Duyuru ve Haber Metni.",
            actions='<a href="/announcements" class="btn btn-ghost">&larr; Tüm Duyurulara Dön</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_edit(cls, announcement: Dict[str, Any], error: Optional[str] = None) -> str:
        """
        [U]pdate Form View: Displays edit form pre-filled with announcement details.
        Route: GET /announcements/{id}/edit -> AnnouncementController.edit(id)
        """
        alert_html = cls._render_alert(error=error)
        a_id = announcement.get('id')
        title = html.escape(str(announcement.get('title') or ''))
        cat = announcement.get("category", "Genel")
        author = html.escape(str(announcement.get('author') or 'İÜ Mezunlar Koordinatörlüğü'))
        content_text = html.escape(str(announcement.get('content') or ''))

        content = f"""
        <div class="card" style="max-width: 720px; margin: 0 auto; position: relative;">
            <div style="margin-bottom: 26px; border-bottom: 1px solid var(--dark-border); padding-bottom: 18px;">
                <span class="badge badge-gold" style="margin-bottom: 10px;">Duyuruyu Düzenle</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff;">#{a_id} — Bilgileri Güncelleyin</h2>
                <p style="font-size: 0.92rem; color: var(--text-muted); margin-top: 4px;">
                    Duyuru başlığını, kategorisini veya içeriğini güncelleyin.
                </p>
            </div>

            <form action="/announcements/{a_id}" method="POST">
                <div class="form-group">
                    <label class="form-label" for="title">Duyuru Başlığı *</label>
                    <input type="text" id="title" name="title" class="form-control" value="{title}" required autofocus>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                        <label class="form-label" for="category">Kategori</label>
                        <select id="category" name="category" class="form-control">
                            <option value="Genel" {'selected' if cat == 'Genel' else ''}>📢 Genel</option>
                            <option value="Etkinlik" {'selected' if cat == 'Etkinlik' else ''}>🎉 Etkinlik</option>
                            <option value="Kariyer" {'selected' if cat == 'Kariyer' else ''}>💼 Kariyer</option>
                            <option value="Akademik" {'selected' if cat == 'Akademik' else ''}>🎓 Akademik</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="author">Yayınlayan Birim *</label>
                        <input type="text" id="author" name="author" class="form-control" value="{author}" required>
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="content">Duyuru İçeriği *</label>
                    <textarea id="content" name="content" class="form-control" rows="6" required>{content_text}</textarea>
                </div>

                <div style="display: flex; gap: 12px; margin-top: 30px;">
                    <button type="submit" class="btn btn-gold" style="flex: 1; justify-content: center; font-size: 1rem; padding: 12px;">💾 Değişiklikleri Kaydet</button>
                    <a href="/announcements/{a_id}" class="btn btn-ghost" style="padding: 12px 20px;">İptal</a>
                </div>
            </form>
        </div>
        """

        return Layout.render(
            title=f"Duyuru #{a_id} Düzenle",
            active_nav="announcements",
            content=content,
            subtitle="Mevcut duyuru bilgilerini güncelleme formu.",
            actions=f'<a href="/announcements/{a_id}" class="btn btn-ghost">&larr; Duyuruya Dön</a>',
            alert_html=alert_html
        )

    @classmethod
    def render_error_404(cls, message: str = "Aranan duyuru bulunamadı.") -> str:
        """Renders 404 Not Found view for Announcements."""
        content = f"""
        <div class="card" style="max-width: 520px; margin: 40px auto; text-align: center; border-top: 4px solid var(--danger);">
            <div class="mono" style="font-size: 4rem; font-weight: 800; color: var(--danger); line-height: 1;">404</div>
            <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff; margin: 16px 0 10px;">Duyuru Bulunamadı</h2>
            <p style="color: var(--text-muted); margin-bottom: 24px;">{html.escape(message)}</p>
            <a href="/announcements" class="btn btn-burgundy">&larr; Duyuru Listesine Dön</a>
        </div>
        """
        return Layout.render(
            title="Duyuru Bulunamadı",
            active_nav="announcements",
            content=content
        )
