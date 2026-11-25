"""
Layout - Shared Base Template for Web Views
Provides a unified Istanbul University visual theme, responsive layout,
navigation bar with active states, typography (Cinzel, Plus Jakarta Sans, JetBrains Mono),
and dark-first institutional styling.
"""
from typing import Optional


class Layout:
    @staticmethod
    def render(title: str, active_nav: str, content: str, subtitle: Optional[str] = None, actions: Optional[str] = None, alert_html: Optional[str] = None) -> str:
        """
        Wraps view content inside the unified institutional Istanbul University layout.
        
        :param title: Page title (H1 and <title>)
        :param active_nav: One of 'home', 'jobs', 'users', 'applications', 'announcements', 'about'
        :param content: Inner page HTML
        :param subtitle: Optional description below page title
        :param actions: Optional header action buttons (e.g. "Yeni İlan Ekle")
        :param alert_html: Optional alert message banner
        """
        nav_items = [
            ("home", "/", "Ana Sayfa"),
            ("jobs", "/jobs", "İş & Staj İlanları"),
            ("users", "/users", "Mezun Rehberi"),
            ("applications", "/applications", "Başvuru Paneli"),
            ("announcements", "/announcements", "Duyurular"),
            ("about", "/about", "Tarihçe & Hakkımızda"),
        ]

        nav_links_html = ""
        for key, href, label in nav_items:
            active_cls = " active" if active_nav == key else ""
            nav_links_html += f'<li><a href="{href}" class="nav-link{active_cls}">{label}</a></li>\n'

        from typing import Optional
        import html as _html
        from middlewares.session_middleware import SessionManager

        current_user = SessionManager.get_current_user()
        if current_user:
            cu_id = current_user.get("id")
            cu_name = _html.escape(str(current_user.get("name") or current_user.get("email") or "Üye"))
            auth_actions_html = f'''
                <a href="/users/{cu_id}" class="btn btn-ghost" title="Profilim">👤 {cu_name}</a>
                <a href="/logout" class="btn btn-ghost" title="Oturumu Kapat">🚪 Çıkış</a>
            '''
        else:
            auth_actions_html = '''
                <a href="/login" class="btn btn-ghost" title="Giriş Yap">🔐 Giriş Yap</a>
                <a href="/register" class="btn btn-ghost" title="Üyelik Kaydı">📝 Kayıt Ol</a>
            '''

        actions_html = actions if actions else ""
        subtitle_html = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ""
        alert_section = alert_html if alert_html else ""

        return f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — İstanbul Üniversitesi Mezun Platformu</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --iu-burgundy: #881337;
            --iu-burgundy-hover: #9f1239;
            --iu-burgundy-dark: #4c0519;
            --iu-gold: #c59b27;
            --iu-gold-light: #d4af37;
            --iu-gold-glow: rgba(0, 0, 0, 0.25);
            --bg-body: #0d1525;
            --dark-card: #0f172a;
            --dark-card-hover: #162036;
            --dark-border: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --success: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            min-height: 100vh;
            line-height: 1.6;
            background-image: 
                radial-gradient(circle at 10% 15%, rgba(136, 19, 55, 0.18) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(197, 155, 39, 0.10) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(15, 23, 42, 0.7) 0%, transparent 100%);
            display: flex;
            flex-direction: column;
        }}

        /* Navigation Bar */
        nav {{
            position: sticky;
            top: 0;
            z-index: 100;
            backdrop-filter: blur(16px);
            background: rgba(8, 12, 22, 0.92);
            border-bottom: 1px solid rgba(31, 41, 61, 0.8);
            padding: 14px 24px;
        }}

        .nav-container {{
            max-width: 1240px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 14px;
            text-decoration: none;
            color: #ffffff;
        }}

        .brand-seal {{
            width: 44px;
            height: 44px;
            background: linear-gradient(145deg, #064e3b 0%, #022c22 100%);
            border: 1.5px solid #d4af37;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.35rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35);
            transition: all 0.2s ease;
        }}

        .brand-seal:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
        }}

        .brand-text {{
            display: flex;
            flex-direction: column;
        }}

        .brand-title {{
            font-family: 'Cinzel', serif;
            font-weight: 800;
            font-size: 1.15rem;
            letter-spacing: 0.5px;
            color: #ffffff;
            line-height: 1.2;
        }}

        .brand-sub {{
            font-size: 0.74rem;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            color: #d4af37;
            font-weight: 700;
            margin-top: 2px;
        }}

        .brand-meta {{
            font-size: 0.68rem;
            color: #94a3b8;
            font-weight: 500;
            letter-spacing: 0.2px;
            margin-top: 1px;
        }}

        .nav-links {{
            display: flex;
            align-items: center;
            gap: 22px;
            list-style: none;
        }}

        .nav-link {{
            color: var(--text-muted);
            text-decoration: none;
            font-weight: 600;
            font-size: 0.92rem;
            transition: color 0.2s ease;
        }}

        .nav-link:hover, .nav-link.active {{
            color: var(--iu-gold-light);
        }}

        .nav-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}

        /* Buttons */
        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 18px;
            border-radius: 10px;
            font-weight: 600;
            font-size: 0.9rem;
            text-decoration: none;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
            border: none;
        }}

        .btn-sm {{
            padding: 6px 12px;
            font-size: 0.82rem;
            border-radius: 8px;
        }}

        .btn-burgundy {{
            background: linear-gradient(135deg, var(--iu-burgundy), #9f1239);
            color: #ffffff;
            border: 1px solid rgba(212, 175, 55, 0.35);
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .btn-burgundy:hover {{
            background: linear-gradient(135deg, #9f1239, #be123c);
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 4px 14px rgba(136, 19, 55, 0.4);
        }}

        /* Rafine İlan Butonu */
        .btn-nav-cta {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 9px 18px;
            border-radius: 9px;
            background: linear-gradient(135deg, #881337 0%, #6b0c2a 100%);
            color: #ffffff;
            font-weight: 600;
            font-size: 0.88rem;
            letter-spacing: 0.2px;
            text-decoration: none;
            border: 1px solid rgba(212, 175, 55, 0.45);
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            cursor: pointer;
        }}

        .btn-nav-cta:hover {{
            background: linear-gradient(135deg, #9f1239 0%, #7a0e30 100%);
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 4px 14px rgba(136, 19, 55, 0.45);
            color: #ffffff;
        }}

        .btn-nav-cta .btn-arrow-chip {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 20px;
            height: 20px;
            border-radius: 5px;
            background: rgba(212, 175, 55, 0.15);
            color: #d4af37;
            font-size: 0.8rem;
            transition: transform 0.2s ease;
        }}

        .btn-nav-cta:hover .btn-arrow-chip {{
            transform: translateX(3px);
            background: rgba(212, 175, 55, 0.25);
            color: #ffffff;
        }}

        .btn-gold {{
            background: linear-gradient(135deg, #c59b27, #a17c18);
            color: #ffffff;
            border: 1px solid rgba(212, 175, 55, 0.45);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .btn-gold:hover {{
            background: linear-gradient(135deg, #d4af37, #b88f20);
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.55), 0 4px 14px rgba(0, 0, 0, 0.3);
        }}

        .btn-ghost {{
            background: rgba(255, 255, 255, 0.04);
            color: #f8fafc;
            border: 1px solid var(--dark-border);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .btn-ghost:hover {{
            background: rgba(255, 255, 255, 0.08);
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.5);
            color: #ffffff;
        }}

        .btn-danger {{
            background: rgba(239, 68, 68, 0.15);
            color: #fca5a5;
            border: 1px solid rgba(239, 68, 68, 0.4);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .btn-danger:hover {{
            background: #ef4444;
            color: #ffffff;
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 22px rgba(239, 68, 68, 0.35);
        }}

        /* Page Layout */
        .page-wrapper {{
            max-width: 1240px;
            width: 100%;
            margin: 36px auto 70px;
            padding: 0 24px;
            flex: 1;
        }}

        .page-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 28px;
            flex-wrap: wrap;
            gap: 18px;
            border-bottom: 1px solid var(--dark-border);
            padding-bottom: 20px;
        }}

        .page-title {{
            font-family: 'Cinzel', serif;
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: 0.5px;
            color: #ffffff;
        }}

        .page-subtitle {{
            color: var(--text-muted);
            font-size: 0.98rem;
            margin-top: 6px;
        }}

        /* Card */
        .card {{
            background: var(--dark-card);
            border: 1px solid var(--dark-border);
            border-radius: 18px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .card-hover:hover {{
            transform: translateY(-4px);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6);
            background: var(--dark-card-hover);
        }}

        /* Modern Filter Bar & Search */
        .filter-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            margin-bottom: 24px;
            flex-wrap: wrap;
        }}

        .filter-group {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}

        .filter-chip {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 7px 14px;
            border-radius: 9999px;
            font-size: 0.82rem;
            font-weight: 600;
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid var(--dark-border);
            color: #94a3b8;
            text-decoration: none;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            cursor: pointer;
        }}

        .filter-chip:hover, .filter-chip.active {{
            background: rgba(136, 19, 55, 0.25);
            color: #ffffff;
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.5);
        }}

        /* Bento Grid & Modern Item Cards */
        .item-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 22px;
            margin-bottom: 30px;
        }}

        .item-card {{
            background: var(--dark-card);
            border: 1px solid var(--dark-border);
            border-radius: 18px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.35);
        }}

        .item-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--iu-burgundy), var(--iu-gold));
            opacity: 0.3;
            transition: opacity 0.25s ease;
        }}

        .item-card:hover {{
            transform: translateY(-4px) scale(1.01);
            box-shadow: 0 16px 36px rgba(0, 0, 0, 0.6);
            background: var(--dark-card-hover);
        }}

        .item-card:hover::before {{
            opacity: 1;
        }}

        .avatar-box {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(136, 19, 55, 0.3) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid rgba(212, 175, 55, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            flex-shrink: 0;
        }}

        /* Table */
        .table-responsive {{
            overflow-x: auto;
            border-radius: 14px;
            border: 1px solid var(--dark-border);
            background: rgba(13, 19, 34, 0.85);
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
        }}

        th {{
            background: #090e1a;
            color: var(--iu-gold-light);
            font-family: 'Cinzel', serif;
            font-size: 0.82rem;
            font-weight: 700;
            letter-spacing: 0.8px;
            text-transform: uppercase;
            padding: 14px 18px;
            border-bottom: 1px solid var(--dark-border);
        }}

        td {{
            padding: 14px 18px;
            border-bottom: 1px solid rgba(31, 41, 61, 0.6);
            color: #e2e8f0;
            font-size: 0.92rem;
            vertical-align: middle;
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover td {{
            background: rgba(255, 255, 255, 0.02);
        }}

        /* Badges */
        .badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 9999px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.3px;
        }}

        .badge-gold {{
            background: rgba(217, 119, 6, 0.2);
            color: #fbbf24;
            border: 1px solid rgba(217, 119, 6, 0.4);
        }}

        .badge-burgundy {{
            background: rgba(136, 19, 55, 0.25);
            color: #fda4af;
            border: 1px solid rgba(136, 19, 55, 0.5);
        }}

        .badge-green {{
            background: rgba(16, 185, 129, 0.15);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.35);
        }}

        .badge-blue {{
            background: rgba(59, 130, 246, 0.15);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.35);
        }}

        .badge-purple {{
            background: rgba(147, 51, 234, 0.15);
            color: #c084fc;
            border: 1px solid rgba(147, 51, 234, 0.35);
        }}

        .mono {{
            font-family: 'JetBrains Mono', monospace;
        }}

        /* Forms */
        .form-group {{
            margin-bottom: 20px;
        }}

        .form-label {{
            display: block;
            font-size: 0.88rem;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--text-main);
        }}

        .form-control {{
            width: 100%;
            background: #090e1a;
            border: 1px solid var(--dark-border);
            border-radius: 10px;
            padding: 12px 14px;
            color: #ffffff;
            font-family: inherit;
            font-size: 0.95rem;
            transition: all 0.2s ease;
        }}

        .form-control:focus {{
            outline: none;
            border-color: rgba(136, 19, 55, 0.6);
            box-shadow: 0 0 0 3px rgba(136, 19, 55, 0.15);
        }}

        textarea.form-control {{
            min-height: 120px;
            resize: vertical;
        }}

        /* Alerts */
        .alert {{
            padding: 14px 18px;
            border-radius: 12px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.95rem;
            font-weight: 500;
        }}

        .alert-success {{
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.4);
            color: #a7f3d0;
        }}

        .alert-danger {{
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.4);
            color: #fecaca;
        }}

        /* Footer */
        footer {{
            border-top: 1px solid var(--dark-border);
            padding: 44px 24px;
            background: #050811;
            text-align: center;
            color: var(--text-muted);
            font-size: 0.9rem;
            margin-top: auto;
        }}

        .footer-seal {{
            font-size: 2rem;
            margin-bottom: 12px;
        }}

        .footer-links {{
            display: flex;
            justify-content: center;
            gap: 22px;
            margin: 18px 0;
            flex-wrap: wrap;
        }}

        .footer-links a {{
            color: var(--text-muted);
            text-decoration: none;
            transition: color 0.2s ease;
        }}

        .footer-links a:hover {{
            color: var(--iu-gold-light);
        }}

        @media (max-width: 820px) {{
            .nav-links {{ display: none; }}
            .page-title {{ font-size: 1.8rem; }}
        }}
    </style>
</head>
<body>

    <nav>
        <div class="nav-container">
            <a href="/" class="brand">
                <div class="brand-seal">🏛️</div>
                <div class="brand-text">
                    <span class="brand-title">İstanbul Üniversitesi</span>
                    <span class="brand-sub">Mezun Bilgi & Kariyer Ağı</span>
                    <span class="brand-meta">Rektörlük Mezunlar Koordinatörlüğü • Kuruluş 1453</span>
                </div>
            </a>
            <ul class="nav-links">
                {nav_links_html}
            </ul>
            <div class="nav-actions">
                {auth_actions_html}
                <a href="/api/swagger" class="btn btn-ghost" title="OpenAPI / Swagger">⚡ API Docs</a>
                <a href="/jobs/create" class="btn btn-burgundy">+ İlan Ver</a>
            </div>
        </div>
    </nav>

    <div class="page-wrapper">
        <header class="page-header">
            <div>
                <h1 class="page-title">{title}</h1>
                {subtitle_html}
            </div>
            {f'<div>{actions_html}</div>' if actions_html else ''}
        </header>

        {alert_section}

        {content}
    </div>

    <footer>
        <div class="footer-seal">🏛️</div>
        <p style="font-family: 'Cinzel', serif; font-weight: 700; color: #ffffff; font-size: 1.05rem; margin-bottom: 6px; letter-spacing: 0.5px;">
            İstanbul Üniversitesi Mezunlar Koordinatörlüğü
        </p>
        <p style="color: var(--iu-gold-light); font-size: 0.85rem; margin-bottom: 16px;">
            Beyazıt Yerleşkesi, 34452 Fatih / İstanbul
        </p>
        <div class="footer-links">
            <a href="/">Ana Sayfa</a>
            <a href="/jobs">İş İlanları</a>
            <a href="/users">Mezun Rehberi</a>
            <a href="/applications">Başvurular</a>
            <a href="/announcements">Duyurular</a>
            <a href="/about">Hakkımızda</a>
            <a href="/api/swagger">API Swagger</a>
        </div>
        <p>&copy; 1453 - 2026 İstanbul Üniversitesi. Tüm hakları saklıdır.</p>
    </footer>

</body>
</html>"""
