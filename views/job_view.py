"""
JobView - HTML View Layer for Job Postings
Renders responsive web views for career opportunities, employment board, and relational author listings.
Redesigned with high-trust Istanbul University Dark Theme, Bento Job Cards, and interactive filters.
"""
from typing import List, Dict, Any, Optional
import html
from views.layout import Layout


class JobView:
    """Renders modern HTML presentation for Job Posting resources."""

    @staticmethod
    def render_index(jobs: List[Dict[str, Any]], count: int, error: Optional[str] = None, success: Optional[str] = None, filter_user: Optional[Dict[str, Any]] = None) -> str:
        alert_html = ""
        if error:
            alert_html += f'<div class="alert alert-danger"><span>⚠</span><span>{html.escape(error)}</span></div>'
        if success:
            alert_html += f'<div class="alert alert-success"><span>✓</span><span>{html.escape(success)}</span></div>'

        subtitle = "İstanbul Üniversitesi mezunlarının çalıştığı ve yönettiği seçkin kurumlardan kariyer & staj fırsatları."
        if filter_user:
            subtitle = f"<strong>{html.escape(filter_user.get('name', 'Kullanıcı'))}</strong> tarafından yayınlanan iş & staj ilanları."

        # Statistics
        full_time_cnt = sum(1 for j in jobs if j.get('employment_type') == 'full_time')
        intern_cnt = sum(1 for j in jobs if j.get('employment_type') == 'internship')
        part_time_cnt = sum(1 for j in jobs if j.get('employment_type') == 'part_time')

        # Generate modern bento job cards
        cards_html = ""
        for j in jobs:
            j_id = j.get('id')
            title = html.escape(str(j.get('title') or 'Pozisyon Belirtilmedi'))
            company = html.escape(str(j.get('company_name') or 'Kurum Belirtilmedi'))
            location = html.escape(str(j.get('location') or 'İstanbul (Hibrit)'))
            emp_type = j.get('employment_type', 'full_time')
            raw_desc = str(j.get('description') or '')
            preview_desc = html.escape((raw_desc[:120] + "...") if len(raw_desc) > 120 else raw_desc)
            salary = html.escape(str(j.get('salary_range') or ''))

            # Badge selection
            if emp_type == 'internship':
                badge_cls = 'badge-gold'
                emp_label = '🎓 Staj Programı'
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

            salary_chip = f'<span style="font-size: 0.78rem; color: #d4af37; font-family: monospace; font-weight: 700; background: rgba(212, 175, 55, 0.12); padding: 3px 8px; border-radius: 6px;">💵 {salary}</span>' if salary else ''

            cards_html += f"""
            <div class="item-card">
                <div>
                    <!-- Header: Company & Badges -->
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; margin-bottom: 14px;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <div class="avatar-box">🏢</div>
                            <div>
                                <div style="font-size: 0.82rem; font-weight: 700; color: #d4af37; text-transform: uppercase; letter-spacing: 0.5px;">{company}</div>
                                <div style="font-size: 0.8rem; color: var(--text-muted); display: flex; align-items: center; gap: 4px; margin-top: 2px;">
                                    <span>📍</span> <span>{location}</span>
                                </div>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <span class="mono" style="font-size: 0.8rem; color: var(--text-muted); font-weight: 700;">#{j_id}</span>
                            <div style="margin-top: 4px;"><span class="badge {badge_cls}">{emp_label}</span></div>
                        </div>
                    </div>

                    <!-- Job Title -->
                    <h3 style="margin-bottom: 10px; font-size: 1.15rem; line-height: 1.4;">
                        <a href="/jobs/{j_id}" style="color: #ffffff; text-decoration: none; font-weight: 700; transition: color 0.2s;" onmouseover="this.style.color='#d4af37'" onmouseout="this.style.color='#ffffff'">
                            {title}
                        </a>
                    </h3>

                    <!-- Description Preview -->
                    <p style="font-size: 0.88rem; color: #cbd5e1; line-height: 1.5; margin-bottom: 16px;">
                        {preview_desc}
                    </p>

                    <!-- Tags & Salary -->
                    <div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 18px;">
                        {salary_chip}
                        <span style="font-size: 0.78rem; color: #94a3b8; background: #090e1a; padding: 3px 8px; border-radius: 6px; border: 1px solid var(--dark-border);">
                            🏛️ Mezun İlanı
                        </span>
                    </div>
                </div>

                <div>
                    <!-- Author Information -->
                    <div style="display: flex; align-items: center; justify-content: space-between; padding-top: 14px; border-top: 1px solid var(--dark-border); margin-bottom: 14px;">
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span style="font-size: 1rem;">🎓</span>
                            <div>
                                <a href="/users/{author_id}" style="color: #f1f5f9; text-decoration: none; font-weight: 600; font-size: 0.85rem;" onmouseover="this.style.color='#d4af37'" onmouseout="this.style.color='#f1f5f9'">
                                    {author_name}
                                </a>
                                <div style="font-size: 0.72rem; color: var(--text-muted);">Doğrulanmış İÜ Mezunu</div>
                            </div>
                        </div>
                        <a href="/jobs/{j_id}/applications" class="filter-chip" style="font-size: 0.75rem; padding: 4px 10px;">
                            Adaylar
                        </a>
                    </div>

                    <!-- Card Actions -->
                    <div style="display: flex; gap: 8px; align-items: center;">
                        <a href="/jobs/{j_id}" class="btn btn-sm btn-ghost" style="flex: 1; justify-content: center;" title="İlan Detayı">👁️ Detay</a>
                        <a href="/jobs/{j_id}/apply" class="btn btn-sm btn-burgundy" style="flex: 1.2; justify-content: center;" title="İlana Başvur">📝 Başvur</a>
                        <form action="/jobs/{j_id}/delete" method="POST" style="display: inline-block;" onsubmit="return confirm('İş ilanı #{j_id} ({title}) silinsin mi?');">
                            <button type="submit" class="btn btn-sm btn-danger" title="İlanı Sil" style="padding: 6px 10px;">🗑️</button>
                        </form>
                    </div>
                </div>
            </div>
            """

        if not jobs:
            cards_html = """
            <div style="grid-column: 1 / -1; padding: 60px 24px; text-align: center; background: var(--dark-card); border: 1px solid var(--dark-border); border-radius: 18px;">
                <div style="font-size: 3rem; margin-bottom: 12px;">💼</div>
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 8px;">Henüz İlan Yayınlanmadı</h3>
                <p style="color: var(--text-muted); font-size: 0.95rem; max-width: 480px; margin: 0 auto 20px;">
                    İlk kariyer veya staj ilanını açarak İstanbul Üniversitesi öğrencileri ve mezunlarıyla buluşun.
                </p>
                <a href="/jobs/create" class="btn btn-burgundy">+ İlk İlanı Yayınla</a>
            </div>
            """

        content = f"""
        <!-- İstatistik Şeridi (Bento) -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 28px;">
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: var(--iu-gold-light);">{count}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Aktif Kariyer & Staj İlanı</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: var(--success);">{full_time_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Tam Zamanlı İstihdam</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: #fbbf24;">{intern_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Öğrenci Staj İlanı</div>
            </div>
            <div class="card" style="padding: 20px; text-align: center; margin-bottom: 0;">
                <div class="mono" style="font-size: 2.2rem; font-weight: 800; color: #60a5fa;">{part_time_cnt}</div>
                <div style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">Yarı Zamanlı / Proje</div>
            </div>
        </div>

        <!-- Filtre ve Hızlı İşlem Çubuğu -->
        <div class="filter-bar">
            <div class="filter-group">
                <span class="filter-chip active">Tüm İlanlar ({count})</span>
                <span class="filter-chip">💼 Tam Zamanlı ({full_time_cnt})</span>
                <span class="filter-chip">🎓 Staj ({intern_cnt})</span>
                <span class="filter-chip">⏱️ Yarı Zamanlı ({part_time_cnt})</span>
            </div>
            <div style="display: flex; gap: 8px;">
                <a href="/api/jobs" class="btn btn-sm btn-ghost" title="REST API JSON">⚡ API JSON</a>
                <a href="/jobs/create" class="btn btn-sm btn-burgundy">+ Yeni İlan Ekle</a>
            </div>
        </div>

        <!-- İlan Kartları Izgarası (Bento Grid) -->
        <div class="item-grid">
            {cards_html}
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
        <div style="margin-top: 28px; padding-top: 22px; border-top: 1px solid var(--dark-border);">
            <h3 style="font-family: 'Cinzel', serif; font-size: 1.2rem; color: #ffffff; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                <span>📋</span> Aranan Nitelikler & Yetkinlikler
            </h3>
            <div style="color: #cbd5e1; line-height: 1.7; white-space: pre-line; background: #090e1a; padding: 20px; border-radius: 12px; border: 1px solid var(--dark-border);">
                {requirements}
            </div>
        </div>
        """ if requirements else ""

        salary_section = f"""
        <div style="background: rgba(212, 175, 55, 0.08); padding: 14px 20px; border-radius: 12px; border: 1px solid rgba(212, 175, 55, 0.25); margin-top: 20px; display: flex; align-items: center; justify-content: space-between;">
            <div>
                <div style="font-size: 0.78rem; text-transform: uppercase; color: #d4af37; font-weight: 700;">Tahmini Ücret / Yan Haklar</div>
                <div class="mono" style="font-size: 1.15rem; color: #ffffff; font-weight: 700; margin-top: 2px;">{salary}</div>
            </div>
            <span style="font-size: 1.6rem;">💼</span>
        </div>
        """ if salary else ""

        apply_external = f"""
        <a href="{app_url}" target="_blank" class="btn btn-gold" style="font-size: 0.95rem;">
            Kurum Sitesinden Başvur &rarr;
        </a>
        """ if app_url else ""

        content = f"""
        <div class="card" style="max-width: 860px; margin: 0 auto; position: relative;">
            
            <!-- İlan Üst Başlığı -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px; padding-bottom: 22px; border-bottom: 1px solid var(--dark-border); flex-wrap: wrap; gap: 16px;">
                <div>
                    <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
                        <span class="mono" style="color: #d4af37; font-weight: 800; font-size: 0.95rem;">#{j_id}</span>
                        <span class="badge badge-burgundy">{html.escape(emp_type.replace('_', ' ').title())}</span>
                        <span class="badge badge-green">✓ Açık Pozisyon</span>
                    </div>
                    <h2 style="font-family: 'Cinzel', serif; font-size: 2rem; color: #ffffff; letter-spacing: 0.5px;">{title}</h2>
                    <div style="font-size: 1.05rem; color: #d4af37; font-weight: 600; margin-top: 6px; display: flex; align-items: center; gap: 6px;">
                        <span>🏢</span> <strong>{company}</strong> &bull; <span>📍</span> <span>{location}</span>
                    </div>
                </div>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <a href="/jobs/{j_id}/apply" class="btn btn-burgundy" style="font-size: 1rem; padding: 12px 24px;">📝 Platformdan Başvur</a>
                    {apply_external}
                </div>
            </div>

            <!-- Yayınlayan Mezun & İlan Bilgi Şeridi -->
            <div style="background: #090e1a; padding: 18px 22px; border-radius: 14px; border: 1px solid var(--dark-border); margin-bottom: 26px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 14px;">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div class="avatar-box" style="width: 44px; height: 44px; font-size: 1.2rem;">🎓</div>
                    <div>
                        <div style="font-size: 0.76rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">İlanı Yayınlayan Mezun</div>
                        <a href="/users/{author_id}" style="color: #ffffff; font-weight: 700; text-decoration: none; font-size: 1rem;" onmouseover="this.style.color='#d4af37'" onmouseout="this.style.color='#ffffff'">
                            {author_name}
                        </a>
                        <span style="font-size: 0.75rem; color: #34d399; margin-left: 6px;">● Doğrulanmış Profil</span>
                    </div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <a href="/users/{author_id}/jobs" class="filter-chip">Mezunun Diğer İlanları</a>
                    <a href="/jobs/{j_id}/applications" class="filter-chip">Gelen Başvurular ({j_id})</a>
                </div>
            </div>

            <!-- Pozisyon Açıklaması -->
            <div>
                <h3 style="font-family: 'Cinzel', serif; font-size: 1.2rem; color: #ffffff; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;">
                    <span>📌</span> Pozisyon Tanımı & Görevler
                </h3>
                <div style="color: #cbd5e1; line-height: 1.8; white-space: pre-line; font-size: 1.02rem;">
                    {description}
                </div>
            </div>

            {req_section}
            {salary_section}

            <!-- Alt Aksiyon Çubuğu -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 36px; padding-top: 24px; border-top: 1px solid var(--dark-border); flex-wrap: wrap; gap: 14px;">
                <div style="display: flex; gap: 10px;">
                    <a href="/jobs/{j_id}/edit" class="btn btn-gold">✏️ İlanı Düzenle</a>
                    <form action="/jobs/{j_id}/delete" method="POST" style="display: inline;" onsubmit="return confirm('Bu ilan silinecektir. Emin misiniz?');">
                        <button type="submit" class="btn btn-danger">🗑️ İlanı Kaldır</button>
                    </form>
                </div>
                <div style="display: flex; gap: 10px;">
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
        <div class="card" style="max-width: 720px; margin: 0 auto; position: relative;">
            <div style="margin-bottom: 26px; border-bottom: 1px solid var(--dark-border); padding-bottom: 18px;">
                <span class="badge badge-burgundy" style="margin-bottom: 10px;">Kariyer Formu</span>
                <h2 style="font-family: 'Cinzel', serif; font-size: 1.7rem; color: #ffffff;">Yeni İlan Yayınlayın</h2>
                <p style="font-size: 0.92rem; color: var(--text-muted); margin-top: 4px;">
                    İstanbul Üniversitesi mezunlarına ve öğrencilerine ulaşacak kariyer veya staj fırsatını tanımlayın.
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
                        <option value="full_time">💼 Tam Zamanlı (Full-Time)</option>
                        <option value="part_time">⏱️ Yarı Zamanlı (Part-Time)</option>
                        <option value="internship">🎓 Staj (Öğrenci / Yeni Mezun)</option>
                        <option value="contract">📝 Sözleşmeli / Proje Bazlı</option>
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

                <div style="display: flex; gap: 12px; margin-top: 30px;">
                    <button type="submit" class="btn btn-burgundy" style="flex: 1; justify-content: center; font-size: 1rem; padding: 12px;">🚀 İlanı Yayınla</button>
                    <a href="/jobs" class="btn btn-ghost" style="padding: 12px 20px;">İptal</a>
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
