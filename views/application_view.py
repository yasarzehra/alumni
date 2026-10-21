"""
ApplicationView - HTML View Layer for Job Applications
Renders responsive web views for candidate submissions, recruiter review boards, and application forms.
"""
from typing import List, Dict, Any, Optional
import html


class ApplicationView:
    """Renders HTML presentation for Job Application resources."""

    @staticmethod
    def render_index(applications: List[Dict[str, Any]], count: int, error: Optional[str] = None, success: Optional[str] = None, filter_title: Optional[str] = None) -> str:
        alert_html = ""
        if error:
            alert_html += f'<div style="background:#fee2e2;color:#991b1b;padding:14px;border-radius:8px;margin-bottom:20px;">{html.escape(error)}</div>'
        if success:
            alert_html += f'<div style="background:#dcfce7;color:#166534;padding:14px;border-radius:8px;margin-bottom:20px;">{html.escape(success)}</div>'

        subtitle = "Tüm Aday Başvuruları ve İnceleme Paneli"
        if filter_title:
            subtitle = html.escape(filter_title)

        status_colors = {
            "pending": "#eab308",
            "reviewed": "#3b82f6",
            "shortlisted": "#8b5cf6",
            "accepted": "#22c55e",
            "rejected": "#ef4444"
        }

        rows_html = ""
        for app in applications:
            applicant = app.get("applicant") or {}
            job = app.get("job") or {}
            st = app.get("status", "pending")
            st_color = status_colors.get(st, "#64748b")

            rows_html += f"""
            <tr>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;"><strong>#{app['id']}</strong></td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;">
                    <a href="/jobs/{app.get('job_id')}" style="color: #0f172a; text-decoration: none; font-weight: 600;">
                        {html.escape(job.get('title') or 'İş İlanı')}
                    </a>
                    <div style="font-size: 0.85rem; color: #64748b;">🏢 {html.escape(job.get('company_name') or '')}</div>
                </td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;">
                    <a href="/users/{app.get('applicant_id')}" style="color: #2563eb; text-decoration: none; font-weight: 500;">
                        👤 {html.escape(applicant.get('name') or 'Aday')}
                    </a>
                    <div style="font-size: 0.85rem; color: #64748b;">✉️ {html.escape(applicant.get('email') or '')}</div>
                </td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0;">
                    <span style="background: #f8fafc; color: {st_color}; border: 1px solid {st_color}; padding: 4px 10px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; text-transform: capitalize;">
                        ● {html.escape(st)}
                    </span>
                </td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; font-size: 0.85rem; color: #64748b;">
                    {html.escape(str(app.get('createdAt') or '')[:19])}
                </td>
                <td style="padding: 14px; border-bottom: 1px solid #e2e8f0; text-align: right; white-space: nowrap;">
                    <form action="/applications/{app['id']}/delete" method="POST" style="display: inline-block; margin: 0;" onsubmit="return confirm('Başvuru #{app['id']} silinsin mi?');">
                        <button type="submit" style="padding: 6px 12px; background: #ef4444; color: white; border: none; border-radius: 6px; font-size: 0.82rem; cursor: pointer;">Geri Çek / Sil</button>
                    </form>
                </td>
            </tr>
            """

        if not applications:
            rows_html = '<tr><td colspan="6" style="padding:30px; text-align:center; color:#94a3b8;">Henüz kayıtlı başvuru bulunmamaktadır.</td></tr>'

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>İş Başvuruları - Alumni Platform</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; color: #0f172a; padding: 40px 20px; }}
        .wrapper {{ max-width: 1080px; margin: 0 auto; }}
        .card {{ background: #ffffff; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.05); padding: 32px; border: 1px solid #e2e8f0; margin-bottom: 28px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 20px; margin-bottom: 24px; flex-wrap: wrap; gap: 16px; }}
        table {{ width: 100%; border-collapse: collapse; text-align: left; }}
        .badge {{ padding: 6px 12px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="wrapper">
        {alert_html}
        <div class="card">
            <div class="header">
                <div>
                    <h1 style="font-size: 1.6rem; color: #0f172a;">📋 İş Başvuruları (Applications)</h1>
                    <p style="color: #64748b; font-size: 0.95rem; margin-top: 4px;">{subtitle}</p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <span class="badge" style="background:#f0fdf4; color:#166534; border:1px solid #bbf7d0;">● DB: Connected (job_applications)</span>
                    <span class="badge" style="background:#eff6ff; color:#1d4ed8;">{count} Başvuru</span>
                </div>
            </div>

            <table>
                <thead>
                    <tr style="background: #f8fafc; color: #64748b; font-size: 0.85rem; text-transform: uppercase;">
                        <th style="padding: 12px 14px;">ID</th>
                        <th style="padding: 12px 14px;">Başvurulan Pozisyon (Rel)</th>
                        <th style="padding: 12px 14px;">Aday Bilgisi (Rel)</th>
                        <th style="padding: 12px 14px;">Durum</th>
                        <th style="padding: 12px 14px;">Başvuru Tarihi</th>
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
            <a href="/jobs" style="color: #2563eb; text-decoration: none; font-size: 0.9rem;">İş İlanları (/jobs)</a>
            <a href="/users" style="color: #2563eb; text-decoration: none; font-size: 0.9rem;">Kullanıcılar (/users)</a>
            <a href="/api/applications" style="color: #2563eb; text-decoration: none; font-size: 0.9rem;">REST API (/api/applications)</a>
            <a href="/api/swagger" style="color: #4338ca; text-decoration: none; font-size: 0.9rem;">Swagger UI</a>
        </div>
    </div>
</body>
</html>
"""

    @staticmethod
    def render_apply_form(job: Dict[str, Any], applicant_id: int = 1) -> str:
        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{html.escape(job['title'])} - Başvuru Yap</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8fafc; padding: 40px 20px; }}
        .card {{ max-width: 600px; margin: 0 auto; background: white; padding: 32px; border-radius: 16px; border: 1px solid #e2e8f0; }}
        .form-group {{ margin-bottom: 16px; }}
        label {{ display: block; font-weight: 600; margin-bottom: 6px; font-size: 0.9rem; }}
        input, textarea {{ width: 100%; padding: 10px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 0.95rem; }}
        .btn-submit {{ background: #2563eb; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="card">
        <a href="/jobs/{job['id']}" style="color: #2563eb; text-decoration: none;">&larr; İlan Detayına Dön</a>
        <h1 style="font-size: 1.5rem; margin: 16px 0 6px 0;">Başvuru Yap: {html.escape(job['title'])}</h1>
        <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 24px;">🏢 {html.escape(job['company_name'])}</p>

        <form action="/jobs/{job['id']}/apply" method="POST">
            <input type="hidden" name="applicant_id" value="{applicant_id}">
            <div class="form-group">
                <label for="resume_url">Özgeçmiş (CV) / LinkedIn / Portfolyo Linki</label>
                <input type="url" id="resume_url" name="resume_url" placeholder="https://linkedin.com/in/... veya CV linki">
            </div>
            <div class="form-group">
                <label for="cover_letter">Ön Yazı / Motivasyon Mektubu</label>
                <textarea id="cover_letter" name="cover_letter" rows="4" placeholder="Neden bu pozisyon için uygun olduğunuzu açıklayın..."></textarea>
            </div>
            <button type="submit" class="btn-submit">🚀 Başvuruyu Gönder</button>
        </form>
    </div>
</body>
</html>
"""
