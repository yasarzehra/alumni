"""
ApplicationView - HTML View Layer for Job Applications
Renders responsive web views for candidate submissions, recruiter review boards, and application forms.
Redesigned with high-trust Istanbul University Dark Theme, Candidate Bento Cards, and status filters.
"""
from typing import List, Dict, Any, Optional
import html
from views.layout import Layout


class ApplicationView:
    """Renders HTML presentation for Job Application resources."""

    @staticmethod
    def _status_badge(status: str) -> str:
        st = (status or "pending").lower()
        if st == "accepted":
            return '<span class="badge badge-green">✓ Kabul Edildi</span>'
        elif st == "shortlisted":
            return '<span class="badge badge-purple">★ Kısa Liste</span>'
        elif st == "reviewed":
            return '<span class="badge badge-blue">● İncelendi</span>'
        elif st == "rejected":
            return '<span class="badge" style="background:rgba(239,68,68,0.15);color:#fca5a5;border:1px solid rgba(239,68,68,0.35);">✕ Reddedildi</span>'
        return '<span class="badge badge-gold">⏳ İnceleniyor</span>'

    @staticmethod
    def render_index(applications: List[Dict[str, Any]], count: int, error: Optional[str] = None, success: Optional[str] = None, filter_title: Optional[str] = None) -> str:
        alert_html = ""
        if error:
            alert_html += f'<div class="alert alert-danger"><span>⚠</span><span>{html.escape(error)}</span></div>'
        if success:
            alert_html += f'<div class="alert alert-success"><span>✓</span><span>{html.escape(success)}</span></div>'

        subtitle = "Öğrenci ve mezunların kariyer ilanlarına yaptıkları başvuruların merkezi takip ve değerlendirme paneli."
        if filter_title:
            subtitle = html.escape(filter_title)

        accepted_cnt = sum(1 for a in applications if a.get('status') == 'accepted')
        pending_cnt = sum(1 for a in applications if a.get('status') in ['pending', None])
        shortlisted_cnt = sum(1 for a in applications if a.get('status') == 'shortlisted')

        cards_html = ""
        for app in applications:
            app_id = app.get('id')
            applicant = app.get("applicant") or {}
            applicant_name = html.escape(str(applicant.get("name") or "İÜ Öğrencisi / Mezunu"))
            applicant_email = html.escape(str(applicant.get("email") or ""))
            applicant_id = app.get('applicant_id')

            job = app.get("job") or {}
            job_title = html.escape(str(job.get('title') or 'Kariyer Pozisyonu'))
            company_name = html.escape(str(job.get('company_name') or 'Kurum'))
            job_id = app.get('job_id')

            st_badge = ApplicationView._status_badge(app.get("status", "pending"))
            created_at = html.escape(str(app.get('createdAt') or '-')[:10])

            # Initials for applicant
            name_parts = applicant_name.split()
            initials = "".join([p[0].upper() for p in name_parts[:2] if p]) if name_parts else "İÜ"

            cards_html += f"""
            <div class="item-card">
                <div>
                    <!-- Top Bar: Applicant Info & Status -->
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 14px;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div class="avatar-box" style="font-family: 'Cinzel', serif; font-weight: 800; font-size: 1rem; color: #d4af37;">
                                {initials}
                            </div>
                            <div>
                                <h3 style="font-size: 1.05rem; font-weight: 700; color: #ffffff; line-height: 1.3;">
                                    <a href="/users/{applicant_id}" style="color: #ffffff; text-decoration: none; transition: color 0.2s;" onmouseover="this.style.color='#d4af37'" onmouseout="this.style.color='#ffffff'">
                                        {applicant_name}
                                    </a>
                                </h3>
                                <div class="mono" style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">
                                    {applicant_email}
                                </div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span class="mono" style="font-size: 0.8rem; color: var(--text-muted); font-weight: 700;">#{app_id}</span>
                            <div style="margin-top: 4px;">{st_badge}</div>
                        </div>
                    </div>

                    <!-- Target Job Info -->
                    <div style="background: #090e1a; padding: 14px 16px; border-radius: 12px; border: 1px solid var(--dark-border); margin-bottom: 16px;">
                        <div style="font-size: 0.75rem; text-transform: uppercase; color: #d4af37; font-weight: 700; letter-spacing: 0.5px;">Başvurulan Pozisyon</div>
                        <a href="/jobs/{job_id}" style="color: #ffffff; font-weight: 700; font-size: 1.02rem; text-decoration: none; display: block; margin-top: 2px;" onmouseover="this.style.color='#d4af37'" onmouseout="this.style.color='#ffffff'">
                            {job_title}
                        </a>
                        <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 3px;">
                            🏢 {company_name}
                        </div>
                    </div>

                    <!-- Date Meta -->
                    <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem; color: var(--text-muted); margin-bottom: 16px;">
                        <span>Başvuru Tarihi:</span>
                        <span class="mono" style="color: #cbd5e1; font-weight: 600;">{created_at}</span>
                    </div>
                </div>

                <div>
                    <!-- Action Triggers -->
                    <div style="display: flex; gap: 8px; align-items: center; padding-top: 14px; border-top: 1px solid var(--dark-border);">
                        <a href="/jobs/{job_id}" class="btn btn-sm btn-ghost" style="flex: 1; justify-content: center;" title="İlanı Görüntüle">💼 İlan</a>
                        <a href="/users/{applicant_id}" class="btn btn-sm btn-ghost" style="flex: 1; justify-content: center;" title="Aday Profili">👤 Aday</a>
                        <form action="/applications/{app_id}/delete" method="POST" style="display: inline-block;" onsubmit="return confirm('Başvuru #{app_id} silinsin / geri çekilsin mi?');">
                            <button type="submit" class="btn btn-sm btn-danger" title="Başvuruyu Geri Çek" style="padding: 6px 12px;">🗑️ Geri Çek</button>
                        </form>
                    </div>
                </div>
            </div>
            """

        if not applications:
            cards_html = """
            <div style="grid-column: 1 / -1; padding: 60px 24px; text-align: center; background: var(--dark-card); border: 1px solid var(--dark-border); border-radius: 18px;">
                <div style="font-size: 3rem; margin-bottom: 12px;">📝</div>
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 8px;">Henüz Başvuru Bulunmuyor</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 480px; margin: 0 auto 20px;">
                    Aktif kariyer ve staj ilanlarını inceleyerek ilk başvurunuzu gerçekleştirebilirsiniz.
                </p>
                <a href="/jobs" class="btn btn-burgundy">💼 İlanları Keşfet</a>
            </div>
            """

        content = f"""
        <!-- İstatistik Şeridi (Bento) -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 28px;">
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: var(--iu-gold-light);">{count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Toplam Aday Başvurusu</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: #fbbf24;">{pending_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">İnceleme Bekleyen</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: var(--success);">{accepted_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Kabul Edilen Adaylar</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: #c084fc;">{shortlisted_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Kısa Liste Adayları</div>
            </div>
        </div>

        <!-- Filtre ve Hızlı İşlem Çubuğu -->
        <div class="filter-bar">
            <div class="filter-group">
                <span class="filter-chip active">Tüm Başvurular ({count})</span>
                <span class="filter-chip">⏳ İnceleniyor ({pending_cnt})</span>
                <span class="filter-chip">✓ Kabul Edildi ({accepted_cnt})</span>
                <span class="filter-chip">★ Kısa Liste ({shortlisted_cnt})</span>
            </div>
            <div style="display: flex; gap: 8px;">
                <a href="/api/applications" class="btn btn-sm btn-ghost" title="REST API JSON">⚡ API JSON</a>
                <a href="/jobs" class="btn btn-sm btn-burgundy">Kariyer İlanlarına Göz At</a>
            </div>
        </div>

        <!-- Başvuru Kartları Izgarası (Bento Grid) -->
        <div class="item-grid">
            {cards_html}
        </div>
        """

        return Layout.render(
            title="Başvuru & Takip Paneli",
            active_nav="applications",
            content=content,
            subtitle=subtitle,
            actions='<a href="/jobs" class="btn btn-burgundy">💼 İlanları Keşfet</a>',
            alert_html=alert_html
        )

    @staticmethod
    def render_apply_form(job: Dict[str, Any], applicant_id: int = 1) -> str:
        job_id = job.get('id')
        job_title = html.escape(str(job.get('title') or 'Pozisyon'))
        company = html.escape(str(job.get('company_name') or 'Kurum'))

        content = f"""
        <div class="card" style="max-width: 720px; margin: 0 auto; position: relative;">
            
            <!-- Pozisyon Özeti -->
            <div style="background: #090e1a; padding: 22px; border-radius: 14px; border: 1px solid var(--dark-border); margin-bottom: 26px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                    <span class="badge badge-gold">Kariyer Başvurusu</span>
                    <span class="mono" style="color: var(--text-muted); font-size: 0.85rem;">İlan #{job_id}</span>
                </div>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff; margin-bottom: 4px;">{job_title}</h2>
                <div style="font-size: 1rem; color: #d4af37; font-weight: 600;">🏢 {company}</div>
            </div>

            <form action="/jobs/{job_id}/apply" method="POST">
                <input type="hidden" name="applicant_id" value="{applicant_id}">

                <div class="form-group">
                    <label class="form-label" for="resume_url">Özgeçmiş (CV) / LinkedIn / Portfolyo URL *</label>
                    <input type="url" id="resume_url" name="resume_url" class="form-control" placeholder="https://linkedin.com/in/... veya https://drive.google.com/..." required autofocus>
                    <small style="color: var(--text-muted); font-size: 0.82rem; margin-top: 6px; display: block;">
                        İşverenin inceleyebileceği güncel profil, portfolyo veya özgeçmiş bağlantınızı girin.
                    </small>
                </div>

                <div class="form-group">
                    <label class="form-label" for="cover_letter">Ön Yazı & Motivasyon Mektubu (Opsiyonel)</label>
                    <textarea id="cover_letter" name="cover_letter" class="form-control" rows="5" placeholder="Pozisyona uygunluğunuzu, İÜ mezuniyet / öğrenim durumunuzu ve motivasyonunuzu belirten kısa bir açıklama..."></textarea>
                </div>

                <div style="display: flex; gap: 12px; margin-top: 30px;">
                    <button type="submit" class="btn btn-burgundy" style="flex: 1; justify-content: center; font-size: 1rem; padding: 12px;">🚀 Başvuruyu Tamamla</button>
                    <a href="/jobs/{job_id}" class="btn btn-ghost" style="padding: 12px 20px;">İptal</a>
                </div>
            </form>
        </div>
        """

        return Layout.render(
            title=f"Başvuru Yap — {job_title}",
            active_nav="applications",
            content=content,
            subtitle=f"{company} bünyesindeki açık pozisyona resmi başvuru gönderimi.",
            actions=f'<a href="/jobs/{job_id}" class="btn btn-ghost">&larr; İlan Detayına Dön</a>'
        )
