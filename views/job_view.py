"""
JobView - HTML View Layer for Job Postings
Renders responsive web views for career opportunities, employment board, and relational author listings.
Now completely unified with Istanbul University Tri-Font & Dark Institutional Theme via Layout.
"""
from typing import List, Dict, Any, Optional
import html
from views.layout import Layout


class JobView:
    """Renders HTML presentation for Job Posting resources."""

    @staticmethod
    def render_index(jobs: List[Dict[str, Any]], count: int, error: Optional[str] = None, success: Optional[str] = None, filter_user: Optional[Dict[str, Any]] = None) -> str:
        alert_html = ""
        if error:
            alert_html += f'<div class="alert alert-danger"><span>⚠</span><span>{html.escape(error)}</span></div>'
        if success:
            alert_html += f'<div class="alert alert-success"><span>✓</span><span>{html.escape(success)}</span></div>'

        subtitle = "İstanbul Üniversitesi mezunlarının çalıştığı ve yönettiği kurumlardan kariyer fırsatları."
        if filter_user:
            subtitle = f"<strong>{html.escape(filter_user.get('name', 'Kullanıcı'))}</strong> tarafından yayınlanan iş & staj ilanları."

        # Stats calculation
        full_time_cnt = sum(1 for j in jobs if j.get('employment_type') == 'full_time')
        intern_cnt = sum(1 for j in jobs if j.get('employment_type') == 'internship')

        rows_html = ""
        for j in jobs:
            j_id = j.get('id')
            title = html.escape(str(j.get('title') or 'Pozisyon Belirtilmedi'))
            company = html.escape(str(j.get('company_name') or 'Kurum Belirtilmedi'))
            location = html.escape(str(j.get('location') or 'İstanbul (Hibrit)'))
            emp_type = j.get('employment_type', 'full_time')
            
            # Badge selection
            if emp_type == 'internship':
                badge_cls = 'badge-gold'
                emp_label = '🎓 Staj'
            elif emp_type == 'full_time':
                badge_cls = 'badge-green'
                emp_label = '💼 Tam Zamanlı'
            elif emp_type == 'part_time':
                badge_cls = 'badge-blue'
                emp_label = '⏱️ Yarı Zamanlı'
            else:
                badge_cls = 'badge-purple'
                emp_label = '📝 Proje Bazlı'

            author_info = j.get("author") or {}
            author_name = html.escape(str(author_info.get("name") or "İÜ Mezunu"))
            author_id = j.get("alumni_id")

            rows_html += f"""
            <tr>
                <td class="mono" style="font-weight: 700; color: var(--iu-gold-light);">#{j_id}</td>
                <td>
                    <a href="/jobs/{j_id}" style="color: #ffffff; text-decoration: none; font-weight: 700; font-size: 1rem; display: block;">
                        {title}
                    </a>
                    <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 3px;">
                        🏢 <strong style="color: #e2e8f0;">{company}</strong> &bull; 📍 {location}
                    </div>
                </td>
                <td>
                    <span class="badge {badge_cls}">{emp_label}</span>
                </td>
                <td>
                    <a href="/users/{author_id}" style="color: var(--iu-gold-light); text-decoration: none; font-weight: 600; font-size: 0.9rem;">
                        👤 {author_name}
                    </a>
                    <div style="font-size: 0.78rem; color: var(--text-muted);">Doğrulanmış İÜ Mezunu</div>
                </td>
                <td style="text-align: right; white-space: nowrap;">
                    <a href="/jobs/{j_id}" class="btn btn-sm btn-ghost" title="İlan Detayı">👁️ Detay</a>
                    <a href="/jobs/{j_id}/apply" class="btn btn-sm btn-burgundy" style="margin-left: 4px;" title="İlana Başvur">📝 Başvur</a>
                    <form action="/jobs/{j_id}/delete" method="POST" style="display: inline-block; margin-left: 4px;" onsubmit="return confirm('İş ilanı #{j_id} ({title}) silinsin mi?');">
                        <button type="submit" class="btn btn-sm btn-danger" title="İlanı Sil">🗑️</button>
                    </form>
                </td>
            </tr>
            """

        if not jobs:
            rows_html = '<tr><td colspan="5" style="padding:40px; text-align:center; color:var(--text-muted);">Henüz yayınlanmış bir iş veya staj ilanı bulunmamaktadır.</td></tr>'

        content = f"""
        <!-- İstatistik Şeridi -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 16px; margin-bottom: 24px;">
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: var(--iu-gold-light);">{count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Aktif Kariyer & Staj İlanı</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: var(--success);">{full_time_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Tam Zamanlı İstihdam</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center;">
                <div class="mono" style="font-size: 2rem; font-weight: 800; color: #fbbf24);">{intern_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted);">Öğrenci Staj İlanı</div>
            </div>
        </div>

        <!-- İlanlar Tablosu -->
        <div class="card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; flex-wrap: wrap; gap: 12px;">
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.3rem; color: #ffffff;">Güncel Kariyer Fırsatları</h2>
                <div style="display: flex; gap: 8px;">
                    <a href="/api/jobs" class="btn btn-sm btn-ghost" title="REST API JSON">⚡ JSON API</a>
                    <a href="/jobs/create" class="btn btn-sm btn-burgundy">+ Yeni İlan Ekle</a>
                </div>
            </div>

            <div class="table-responsive">
                <table>
                    <thead>
                        <tr>
                            <th style="width: 70px;">ID</th>
                            <th>Pozisyon & Şirket</th>
                            <th>Çalışma Türü</th>
                            <th>Yayınlayan Mezun</th>
                            <th style="text-align: right; width: 220px;">İşlemler</th>
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
            title="Kariyer & Staj İlanları",
            active_nav="jobs",
            content=content,
            subtitle=subtitle,
            actions='<a href="/jobs/create" class="btn btn-burgundy">+ Yeni İlan Yayınla</a>',
            alert_html=alert_html
        )

    @staticmethod
    def render_show(job: Dict[str, Any]) -> str:
        j_id = job.get('id')
        title = html.escape(str(job.get('title') or 'Pozisyon'))
        company = html.escape(str(job.get('company_name') or 'Şirket'))
        location = html.escape(str(job.get('location') or 'İstanbul'))
        emp_type = job.get('employment_type', 'full_time')
        description = html.escape(str(job.get('description') or ''))
        requirements = html.escape(str(job.get('requirements') or ''))
        salary = html.escape(str(job.get('salary_range') or ''))
        app_url = html.escape(str(job.get('application_url') or ''))

        author = job.get("author") or {}
        author_name = html.escape(str(author.get("name") or "İÜ Mezunu"))
        author_id = job.get("alumni_id")

        req_section = f"""
        <div style="margin-top: 24px; padding-top: 20px; border-top: 1px solid var(--dark-border);">
            <h3 style="font-family: 'Cinzel', serif; font-size: 1.15rem; color: #ffffff; margin-bottom: 8px;">Aranan Nitelikler & Yetkinlikler</h3>
            <p style="color: #cbd5e1; line-height: 1.6; white-space: pre-line;">{requirements}</p>
        </div>
        """ if requirements else ""

        salary_section = f"""
        <div style="background: #090e1a; padding: 14px 18px; border-radius: 12px; border: 1px solid var(--dark-border); margin-top: 20px;">
            <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Maaş / Yan Haklar</div>
            <div class="mono" style="font-size: 1.1rem; color: var(--iu-gold-light); font-weight: 700; margin-top: 2px;">{salary}</div>
        </div>
        """ if salary else ""

        apply_btn = f"""
        <a href="{app_url}" target="_blank" class="btn btn-gold" style="font-size: 1rem; padding: 12px 24px;">
            Şirket Sitesinden Başvur &rarr;
        </a>
        """ if app_url else ""

        content = f"""
        <div class="card" style="max-width: 820px; margin: 0 auto; border-top: 4px solid var(--iu-burgundy);">
            <!-- İlan Üst Başlığı -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; padding-bottom: 20px; border-bottom: 1px solid var(--dark-border); flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 6px;">
                        <span class="mono" style="color: var(--iu-gold-light); font-weight: 700;">#{j_id}</span>
                        <span class="badge badge-burgundy">{html.escape(emp_type.replace('_', ' ').title())}</span>
                    </div>
                    <h2 style="font-family: 'Cinzel', serif; font-size: 1.8rem; color: #ffffff;">{title}</h2>
                    <div style="font-size: 1.05rem; color: var(--iu-gold-light); font-weight: 600; margin-top: 4px;">
                        🏢 {company} &bull; 📍 {location}
                    </div>
                </div>
                <div style="display: flex; gap: 10px;">
                    <a href="/jobs/{j_id}/apply" class="btn btn-burgundy">📝 Platformdan Başvur</a>
                    {apply_btn}
                </div>
            </div>

            <!-- Yayınlayan Mezun Kartı -->
            <div style="background: #090e1a; padding: 16px 20px; border-radius: 12px; border: 1px solid var(--dark-border); margin-bottom: 24px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="font-size: 1.6rem;">🎓</span>
                    <div>
                        <div style="font-size: 0.78rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">İlanı Yayınlayan Mezun</div>
                        <a href="/users/{author_id}" style="color: #ffffff; font-weight: 700; text-decoration: none;">{author_name}</a>
                    </div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <a href="/users/{author_id}/jobs" class="btn btn-sm btn-ghost">Tüm İlanları</a>
                    <a href="/jobs/{j_id}/applications" class="btn btn-sm btn-ghost">Aday Başvuruları ({j_id})</a>
                </div>
            </div>

            <!-- İş Tanımı -->
            <div>
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.15rem; color: #ffffff; margin-bottom: 8px;">Pozisyon Tanımı & Görevler</h3>
                <p style="color: #cbd5e1; line-height: 1.7; white-space: pre-line; font-size: 1rem;">{description}</p>
            </div>

            {req_section}
            {salary_section}

            <!-- Alt Aksiyonlar -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 32px; padding-top: 20px; border-top: 1px solid var(--dark-border); flex-wrap: wrap; gap: 12px;">
                <div style="display: flex; gap: 8px;">
                    <a href="/jobs/{j_id}/edit" class="btn btn-gold">✏️ İlanı Düzenle</a>
                    <form action="/jobs/{j_id}/delete" method="POST" style="display: inline;" onsubmit="return confirm('Bu ilan silinecektir. Emin misiniz?');">
                        <button type="submit" class="btn btn-danger">🗑️ İlanı Kaldır</button>
                    </form>
                </div>
                <div style="display: flex; gap: 8px;">
                    <a href="/api/jobs/{j_id}" class="btn btn-ghost">⚡ API JSON</a>
                    <a href="/jobs" class="btn btn-ghost">&larr; İlan Listesine Dön</a>
                </div>
            </div>
        </div>
        """

        return Layout.render(
            title=f"{title} — {company}",
            active_nav="jobs",
            content=content,
            subtitle="İstanbul Üniversitesi Mezun Kariyer Portalı İş Detayı.",
            actions='<a href="/jobs" class="btn btn-ghost">&larr; Tüm İlanlara Dön</a>'
        )

    @staticmethod
    def render_create() -> str:
        content = """
        <div class="card" style="max-width: 680px; margin: 0 auto; border-top: 4px solid var(--iu-burgundy);">
            <div style="margin-bottom: 24px;">
                <span class="badge badge-burgundy" style="margin-bottom: 10px;">Yeni Kariyer & Staj İlanı</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.5rem; color: #ffffff;">İlan Bilgilerini Tanımlayın</h2>
                <p style="font-size: 0.9rem; color: var(--text-muted); margin-top: 4px;">
                    İstanbul Üniversitesi mezunlarına ve öğrencilerine ulaşacak kariyer fırsatını yayınlayın.
                </p>
            </div>

            <form action="/jobs" method="POST">
                <div class="form-group">
                    <label class="form-label" for="title">Pozisyon / Unvan *</label>
                    <input type="text" id="title" name="title" class="form-control" placeholder="Örn: Kıdemli Yazılım Mühendisi / Hukuk Stajyeri" required autofocus>
                </div>

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
                    <div class="form-group">
                        <label class="form-label" for="company_name">Şirket / Kurum Adı *</label>
                        <input type="text" id="company_name" name="company_name" class="form-control" placeholder="Örn: Garanti BBVA / TÜBİTAK" required>
                    </div>
                    <div class="form-group">
                        <label class="form-label" for="location">Lokasyon</label>
                        <input type="text" id="location" name="location" class="form-control" placeholder="Örn: İstanbul (Hibrit / Maslak)">
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label" for="employment_type">İstihdam Türü</label>
                    <select id="employment_type" name="employment_type" class="form-control">
                        <option value="full_time">Tam Zamanlı (Full-Time)</option>
                        <option value="part_time">Yarı Zamanlı (Part-Time)</option>
                        <option value="internship">Staj (Öğrenci / Yeni Mezun)</option>
                        <option value="contract">Sözleşmeli / Proje Bazlı</option>
                    </select>
                </div>

                <div class="form-group">
                    <label class="form-label" for="description">İş Tanımı & Sorumluluklar *</label>
                    <textarea id="description" name="description" class="form-control" rows="5" placeholder="Pozisyonun kapsamı, ekip yapısı ve beklentiler..." required></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label" for="requirements">Aranan Nitelikler (Opsiyonel)</label>
                    <textarea id="requirements" name="requirements" class="form-control" rows="3" placeholder="Gerekli deneyim, yabancı dil, mezuniyet fakültesi..."></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label" for="application_url">Harici Başvuru URL'si (Opsiyonel)</label>
                    <input type="url" id="application_url" name="application_url" class="form-control" placeholder="https://careers.company.com/apply/123">
                </div>

                <div style="display: flex; gap: 12px; margin-top: 28px;">
                    <button type="submit" class="btn btn-burgundy" style="flex: 1;">🚀 İlanı Yayınla</button>
                    <a href="/jobs" class="btn btn-ghost">İptal</a>
                </div>
            </form>
        </div>
        """

        return Layout.render(
            title="Yeni İlan Yayınla",
            active_nav="jobs",
            content=content,
            subtitle="İÜ Mezun ve Öğrenci Kariyer Ağına yeni iş/staj ilanı ekleyin.",
            actions='<a href="/jobs" class="btn btn-ghost">&larr; İlan Listesine Dön</a>'
        )

    @staticmethod
    def render_error_404(msg: str) -> str:
        content = f"""
        <div class="card" style="max-width: 520px; margin: 40px auto; text-align: center; border-top: 4px solid var(--danger);">
            <div class="mono" style="font-size: 4rem; font-weight: 800; color: var(--danger); line-height: 1;">404</div>
            <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff; margin: 16px 0 10px;">İş İlanı Bulunamadı</h2>
            <p style="color: var(--text-muted); margin-bottom: 24px;">{html.escape(msg)}</p>
            <a href="/jobs" class="btn btn-burgundy">&larr; Tüm İlanlara Dön</a>
        </div>
        """
        return Layout.render(
            title="İlan Bulunamadı",
            active_nav="jobs",
            content=content
        )
