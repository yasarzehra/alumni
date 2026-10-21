"""
JobView - HTML View Layer for Job Postings
Renders responsive web views for career opportunities, employment board, and relational author listings.
"""
from typing import List, Dict, Any, Optional
import html


class JobView:
    """Renders HTML presentation for Job Posting resources."""

    @staticmethod
    def render_index(jobs: List[Dict[str, Any]], count: int, error: Optional[str] = None, success: Optional[str] = None, filter_user: Optional[Dict[str, Any]] = None) -> str:
        alert_html = ""
        if error:
            alert_html += f'<div style="background:#fee2e2;color:#991b1b;padding:14px;border-radius:8px;margin-bottom:20px;">{html.escape(error)}</div>'
        if success:
            alert_html += f'<div style="background:#dcfce7;color:#166534;padding:14px;border-radius:8px;margin-bottom:20px;">{html.escape(success)}</div>'

        subtitle = "Kariyer ve Staj Fırsatları Yönetim Paneli"
        if filter_user:
            subtitle = f"<strong>{html.escape(filter_user['name'])}</strong> kullanıcısına ait iş ilanları"

        rows_html = ""
        for j in jobs:
            author_info = j.get("author") or {}
            author_name = author_info.get("name") or "Alumni Üyesi"
            emp_badge = "#2563eb" if j.get("employment_type") == "full_time" else "#059669"
            
            rows_html += f"""
            <tr>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;"><strong>#{j['id']}</strong></td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;">
                    <a href="/jobs/{j['id']}" style="color: #0f172a; text-decoration: none; font-weight: 600; font-size: 1rem;">
                        {html.escape(j['title'])}
                    </a>
                    <div style="font-size: 0.85rem; color: #64748b; margin-top: 2px;">
                        🏢 {html.escape(j['company_name'])} &bull; 📍 {html.escape(j.get('location') or 'Remote')}
                    </div>
                </td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;">
                    <span style="background: #eff6ff; color: {emp_badge}; padding: 4px 10px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600;">
                        {html.escape(j.get('employment_type', 'full_time').replace('_', ' ').title())}
                    </span>
                </td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;">
                    <a href="/users/{j.get('alumni_id')}" style="color: #4338ca; text-decoration: none; font-size: 0.9rem; font-weight: 500;">
                        👤 {html.escape(author_name)}
                    </a>
                </td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; text-align: right; white-space: nowrap;">
                    <a href="/jobs/{j['id']}" style="padding: 6px 12px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; font-size: 0.82rem; margin-right: 4px; display: inline-block;">Görüntüle</a>
                    <a href="/jobs/{j['id']}/edit" style="padding: 6px 12px; background: #f59e0b; color: white; text-decoration: none; border-radius: 6px; font-size: 0.82rem; margin-right: 4px; display: inline-block;">Düzenle</a>
                    <form action="/jobs/{j['id']}/delete" method="POST" style="display: inline-block; margin: 0;" onsubmit="return confirm('İş ilanı #{j['id']} silinsin mi?');">
                        <button type="submit" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-size: 0.82rem; cursor: pointer;">Sil</button>
                    </form>
                </td>
            </tr>
            """

        if not jobs:
            rows_html = '<tr><td colspan="5" style="padding:30px; text-align:center; color:#94a3b8;">Henüz kayıtlı iş ilanı bulunmamaktadır.</td></tr>'

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kariyer & İş İlanları - Alumni Platform</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #0f172a; padding: 40px 20px; }}
        .wrapper {{ max-width: 1080px; margin: 0 auto; }}
        .card {{ background: #ffffff; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); padding: 32px; border: 1px solid #e2e8f0; margin-bottom: 28px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 20px; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        .btn {{ padding: 8px 16px; border-radius: 8px; font-weight: 600; text-decoration: none; display: inline-block; }}
        .btn-primary {{ background: #2563eb; color: white; }}
        .badge {{ padding: 6px 12px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="wrapper">
        {alert_html}
        <div class="card">
            <div class="header">
                <div>
                    <h1 style="font-size: 1.6rem; color: #0f172a;">💼 İş & Staj İlanları (Job Board)</h1>
                    <p style="color: #64748b; font-size: 0.95rem; margin-top: 4px;">{subtitle}</p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span class="badge" style="background:#f0fdf4; color:#166534; border:1px solid #bbf7d0;">● DB: Connected (job_postings)</span>
                    <span class="badge" style="background:#eff6ff; color:#1d4ed8;">{count} İlan</span>
                    <a href="/jobs/create" class="btn btn-primary">+ Yeni İlan Ekle (C)</a>
                </div>
            </div>

            <table>
                <thead>
                    <tr style="background: #f8fafc; color: #64748b; font-size: 0.85rem; text-transform: uppercase;">
                        <th style="padding: 12px 14px;">ID</th>
                        <th style="padding: 12px 14px;">Pozisyon / Şirket</th>
                        <th style="padding: 12px 14px;">Çalışma Türü</th>
                        <th style="padding: 12px 14px;">Yayınlayan Mezun (Relation)</th>
                        <th style="padding: 12px 14px; text-align: right;">İşlemler</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
            <a href="/" style="color: #64748b; text-decoration: none; font-size: 0.9rem;">&larr; Ana Sayfa</a>
            <a href="/users" style="color: #2563eb; text-decoration: none; font-size: 0.9rem;">Kullanıcılar (/users)</a>
            <a href="/announcements" style="color: #2563eb; text-decoration: none; font-size: 0.9rem;">Duyurular (/announcements)</a>
            <a href="/api/jobs" style="color: #2563eb; text-decoration: none; font-size: 0.9rem;">REST API (/api/jobs)</a>
            <a href="/api/swagger" style="color: #4338ca; text-decoration: none; font-size: 0.9rem;">Swagger UI</a>
        </div>
    </div>
</body>
</html>
"""

    @staticmethod
    def render_show(job: Dict[str, Any]) -> str:
        author = job.get("author") or {}
        author_name = author.get("name") or "Alumni Üyesi"
        author_id = job.get("alumni_id")

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{html.escape(job['title'])} - Detay</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #0f172a; padding: 40px 20px; }}
        .card {{ max-width: 800px; margin: 0 auto; background: white; padding: 32px; border-radius: 16px; border: 1px solid #e2e8f0; }}
        .meta {{ margin-bottom: 24px; color: #64748b; font-size: 0.95rem; }}
        .btn {{ padding: 8px 16px; border-radius: 8px; text-decoration: none; font-weight: 600; display: inline-block; }}
    </style>
</head>
<body>
    <div class="card">
        <a href="/jobs" style="color: #2563eb; text-decoration: none;">&larr; Tüm İlanlara Dön</a>
        <h1 style="font-size: 1.8rem; margin: 16px 0 8px 0;">{html.escape(job['title'])}</h1>
        <div class="meta">
            🏢 <strong>{html.escape(job['company_name'])}</strong> &bull; 📍 {html.escape(job.get('location') or 'Remote')} &bull; 💼 {html.escape(job.get('employment_type', 'full_time'))}
        </div>
        <div style="background: #f1f5f9; padding: 14px; border-radius: 8px; margin-bottom: 24px;">
            👤 <strong>Yayınlayan Mezun:</strong> <a href="/users/{author_id}" style="color: #2563eb;">{html.escape(author_name)}</a>
            &bull; <a href="/users/{author_id}/jobs" style="color: #4338ca;">(Bu kullanıcının diğer ilanları)</a>
        </div>
        <h3 style="margin-bottom: 8px;">İş Tanımı & Sorumluluklar</h3>
        <p style="line-height: 1.6; margin-bottom: 24px; color: #334155;">{html.escape(job.get('description', ''))}</p>
        
        {f'<div style="margin-bottom:20px;"><strong>Aranan Nitelikler:</strong><p style="color:#475569;margin-top:4px;">{html.escape(job["requirements"])}</p></div>' if job.get("requirements") else ''}
        {f'<div style="margin-bottom:20px;"><strong>Maaş Aralığı:</strong> {html.escape(job["salary_range"])}</div>' if job.get("salary_range") else ''}
        {f'<div style="margin-bottom:24px;"><a href="{html.escape(job["application_url"])}" target="_blank" class="btn" style="background:#2563eb;color:white;">Başvuru Yap &rarr;</a></div>' if job.get("application_url") else ''}
        
        <div style="border-top: 1px solid #f1f5f9; padding-top: 16px; display: flex; gap: 10px;">
            <a href="/jobs/{job['id']}/edit" class="btn" style="background: #f59e0b; color: white;">Düzenle (U)</a>
            <a href="/jobs" class="btn" style="background: #e2e8f0; color: #334155;">Geri</a>
        </div>
    </div>
</body>
</html>
"""

    @staticmethod
    def render_create() -> str:
        return """<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Yeni İş İlanı Ekle</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; padding: 40px 20px; }
        .card { max-width: 650px; margin: 0 auto; background: white; padding: 32px; border-radius: 16px; border: 1px solid #e2e8f0; }
        .form-group { margin-bottom: 16px; }
        label { display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.9rem; }
        input, select, textarea { width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; }
        .btn-submit { background: #2563eb; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }
    </style>
</head>
<body>
    <div class="card">
        <a href="/jobs" style="color: #2563eb; text-decoration: none;">&larr; İlan Listesi</a>
        <h1 style="font-size: 1.5rem; margin: 16px 0 20px 0;">+ Yeni İş İlanı Ekle [Create (C)]</h1>
        <form action="/jobs" method="POST">
            <div class="form-group">
                <label for="title">İş / Pozisyon Başlığı *</label>
                <input type="text" id="title" name="title" placeholder="Örn: Senior Frontend Developer" required>
            </div>
            <div class="form-group">
                <label for="company_name">Şirket Adı *</label>
                <input type="text" id="company_name" name="company_name" placeholder="Örn: Trendyol" required>
            </div>
            <div class="form-group">
                <label for="location">Lokasyon</label>
                <input type="text" id="location" name="location" placeholder="Örn: İstanbul (Hybrid / Remote)">
            </div>
            <div class="form-group">
                <label for="employment_type">İstihdam Türü</label>
                <select id="employment_type" name="employment_type">
                    <option value="full_time">Tam Zamanlı (Full Time)</option>
                    <option value="part_time">Yarı Zamanlı (Part Time)</option>
                    <option value="internship">Staj (Internship)</option>
                    <option value="contract">Sözleşmeli / Proje Bazlı</option>
                </select>
            </div>
            <div class="form-group">
                <label for="description">İş Tanımı *</label>
                <textarea id="description" name="description" rows="4" placeholder="Görev ve sorumluluklar..." required></textarea>
            </div>
            <div class="form-group">
                <label for="application_url">Başvuru Linki</label>
                <input type="url" id="application_url" name="application_url" placeholder="https://careers.company.com/apply">
            </div>
            <button type="submit" class="btn-submit">+ İlanı Yayınla</button>
        </form>
    </div>
</body>
</html>
"""

    @staticmethod
    def render_error_404(msg: str) -> str:
        return f"""<!DOCTYPE html><html><body style="font-family:sans-serif;text-align:center;padding:50px;">
        <h2>404 - Sayfa Bulunamadı</h2><p>{html.escape(msg)}</p><a href="/jobs">İlan Listesine Dön</a></body></html>"""
