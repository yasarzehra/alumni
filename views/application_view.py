"""
ApplicationView - HTML View Layer for Job Applications
Renders responsive web views for candidate submissions, recruiter review boards, and application forms.
Now completely unified with Istanbul University Tri-Font & Dark Institutional Theme via Layout.
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

        subtitle = "Öğrenci ve mezunların kariyer ilanlarına yaptıkları başvuruların merkezi takip paneli."
        if filter_title:
            subtitle = html.escape(filter_title)

        accepted_cnt = sum(1 for a in applications if a.get('status') == 'accepted')
        pending_cnt = sum(1 for a in applications if a.get('status') in ['pending', None])

        rows_html = ""
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
            created_at = html.escape(str(app.get('createdAt') or '-')[:19])

            rows_html += f"""
            <tr>
                <td class="mono" style="font-weight: 700; color: var(--iu-gold-light);">#{app_id}</td>
                <td>
                    <a href="/jobs/{job_id}" style="color: #ffffff; text-decoration: none; font-weight: 700; font-size: 0.98rem; display: block;">
                        {job_title}
                    </a>
                    <div style="font-size: 0.82rem; color: var(--text-muted); margin-top: 2px;">🏢 {company_name}</div>
                </td>
                <td>
                    <a href="/users/{applicant_id}" style="color: var(--iu-gold-light); text-decoration: none; font-weight: 600; font-size: 0.92rem; display: block;">
                        👤 {applicant_name}
                    </a>
                    <div class="mono" style="font-size: 0.78rem; color: var(--text-muted);">{applicant_email}</div>
                </td>
                <td>
                    {st_badge}
                </td>
                <td class="mono" style="font-size: 0.85rem; color: var(--text-muted); white-space: nowrap;">
                    {created_at}
                </td>
                <td style="text-align: right; white-space: nowrap;">
                    <form action="/applications/{app_id}/delete" method="POST" style="display: inline-block;" onsubmit="return confirm('Başvuru #{app_id} geri çekilsin / silinsin mi?');">
                        <button type="submit" class="btn btn-sm btn-danger" title="Başvuruyu Geri Çek">🗑️ Geri Çek</button>
                    </form>
                </td>
            </tr>
            """

        if not applications:
            rows_html = '<tr><td colspan="6" style="padding:40px; text-align:center; color:var(--text-muted);">Henüz kayıtlı başvuru bulunmamaktadır.</td></tr>'

        content = f"""
        <!-- İstatistik Şeridi -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: var(--iu-gold-light);">{count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Toplam Aday Başvurusu</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: #fbbf24;">{pending_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">İnceleme Bekleyen</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: var(--success);">{accepted_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Kabul Edilen Adaylar</div>
            </div>
        </div>

        <!-- Başvurular Tablosu -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; flex-wrap: wrap; gap: 12px;">
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.3rem; color: #ffffff;">Başvuru Listesi</h2>
                <div style="display: flex; gap: 8px;">
                    <a href="/api/applications" class="btn btn-sm btn-ghost" title="REST API JSON">⚡ JSON API</a>
                    <a href="/jobs" class="btn btn-sm btn-burgundy">Kariyer İlanlarına Göz At</a>
                </div>
            </div>

            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 70px;">ID</th>
                            <th>Başvurulan Pozisyon</th>
                            <th>Aday Mezun / Öğrenci</th>
                            <th>Durum</th>
                            <th>Başvuru Tarihi</th>
                            <th style="text-align: right; width: 140px;">İşlemler</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows_html}
                    </tbody>
                </table>
            </div>
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
        <div class="card" style="max-width: 680px; margin: 0 auto; border-top: 4px solid var(--iu-burgundy);">
            <!-- Pozisyon Özeti -->
            <div style="background: #090e1a; padding: 20px; border-radius: 14px; border: 1px solid var(--dark-border); margin-bottom: 24px;">
                <span class="badge badge-gold" style="margin-bottom: 8px;">Kariyer Başvurusu</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.5rem; color: #ffffff; margin-bottom: 4px;">{job_title}</h2>
                <div style="font-size: 0.95rem; color: var(--iu-gold-light); font-weight: 600;">🏢 {company}</div>
            </div>

            <form action="/jobs/{job_id}/apply" method="POST">
                <input type="hidden" name="applicant_id" value="{applicant_id}">

                <div class="form-group">
                    <label class="form-label" for="resume_url">Özgeçmiş (CV) / LinkedIn / Portfolyo URL *</label>
                    <input type="url" id="resume_url" name="resume_url" class="form-control" placeholder="https://linkedin.com/in/... veya https://drive.google.com/..." required autofocus>
                    <small style="color: var(--text-muted); font-size: 0.8rem; margin-top: 4px; display: block;">
                        İşverenin inceleyebileceği güncel profil veya özgeçmiş bağlantınızı girin.
                    </small>
                </div>

                <div class="form-group">
                    <label class="form-label" for="cover_letter">Ön Yazı & Motivasyon Mektubu (Opsiyonel)</label>
                    <textarea id="cover_letter" name="cover_letter" class="form-control" rows="5" placeholder="Pozisyona uygunluğunuzu, İÜ mezuniyet / öğrenim durumunuzu ve motivasyonunuzu belirten kısa bir not..."></textarea>
                </div>

                <div style="display: flex; gap: 12px; margin-top: 28px;">
                    <button type="submit" class="btn btn-burgundy" style="flex: 1;">🚀 Başvuruyu Tamamla</button>
                    <a href="/jobs/{job_id}" class="btn btn-ghost">İptal</a>
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
