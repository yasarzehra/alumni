"""
AuthMiddleware - Authentication & Role-Based Access Control (RBAC) Middleware
Validates session cookies (iu_session) and Bearer tokens (Authorization: Bearer <token>),
populates request-scoped current_user context, and enforces RBAC policies across Web routes
and authenticated API requests.
"""
import html
import re
from typing import Any, Dict, List, Optional, Tuple
from middlewares.session_middleware import SessionManager


class AuthMiddleware:
    """
    Centralized authentication and RBAC authorization middleware.
    Aligned with ddd.md Section 5 (student, alumni, coordinator, admin).
    """

    # Web routes that require an active session and specific roles
    # Tuple: (HTTP_METHOD, regex_pattern, allowed_roles_or_None_for_any_logged_in, allow_self_user_id)
    PROTECTED_WEB_RULES: List[Tuple[str, str, Optional[Tuple[str, ...]], bool]] = [
        # Job postings creation, editing, deletion -> alumni, coordinator, admin
        ("GET", r"^/jobs/create/?$", ("alumni", "coordinator", "admin"), False),
        ("GET", r"^/job-postings/create/?$", ("alumni", "coordinator", "admin"), False),
        ("POST", r"^/jobs/?$", ("alumni", "coordinator", "admin"), False),
        ("POST", r"^/job-postings/?$", ("alumni", "coordinator", "admin"), False),
        ("GET", r"^/jobs/\d+/edit/?$", ("alumni", "coordinator", "admin"), False),
        ("POST", r"^/jobs/\d+(/delete)?/?$", ("alumni", "coordinator", "admin"), False),
        ("POST", r"^/job-postings/\d+(/delete)?/?$", ("alumni", "coordinator", "admin"), False),

        # Job application submission -> student, alumni, admin
        ("GET", r"^/jobs/\d+/apply/?$", ("student", "alumni", "admin"), False),
        ("POST", r"^/jobs/\d+/apply/?$", ("student", "alumni", "admin"), False),

        # Announcements management -> coordinator, admin
        ("GET", r"^/announcements/create/?$", ("coordinator", "admin"), False),
        ("POST", r"^/announcements/?$", ("coordinator", "admin"), False),
        ("GET", r"^/announcements/\d+/edit/?$", ("coordinator", "admin"), False),
        ("POST", r"^/announcements/\d+(/delete)?/?$", ("coordinator", "admin"), False),

        # User management -> admin (or self for profile edit/update)
        ("GET", r"^/users/create/?$", ("admin",), False),
        ("POST", r"^/users/?$", ("admin",), False),
        ("GET", r"^/users/(\d+)/edit/?$", ("admin",), True),
        ("POST", r"^/users/(\d+)/?$", ("admin",), True),
        ("POST", r"^/users/\d+/delete/?$", ("admin",), False),

        # Applications deletion -> any authenticated user
        ("POST", r"^/applications/\d+/delete/?$", None, False),
    ]

    # Authenticated API RBAC rules (enforced when an authenticated token/cookie is present,
    # or for endpoints that strictly require auth like /api/me)
    STRICT_AUTH_API_PREFIXES = ("/api/me",)

    API_RBAC_RULES: List[Tuple[str, str, Tuple[str, ...]]] = [
        ("POST", r"^/api/jobs/?$", ("alumni", "coordinator", "admin")),
        ("POST", r"^/api/job-postings/?$", ("alumni", "coordinator", "admin")),
        ("PUT", r"^/api/jobs/\d+/?$", ("alumni", "coordinator", "admin")),
        ("PATCH", r"^/api/jobs/\d+/?$", ("alumni", "coordinator", "admin")),
        ("DELETE", r"^/api/jobs/\d+/?$", ("alumni", "coordinator", "admin")),
        ("POST", r"^/api/announcements/?$", ("coordinator", "admin")),
        ("PUT", r"^/api/announcements/\d+/?$", ("coordinator", "admin")),
        ("PATCH", r"^/api/announcements/\d+/?$", ("coordinator", "admin")),
        ("DELETE", r"^/api/announcements/\d+/?$", ("coordinator", "admin")),
    ]

    @classmethod
    def extract_user(cls, headers: Any) -> Optional[Dict[str, Any]]:
        """
        Resolves the authenticated user from either:
        1. Authorization: Bearer <token> header
        2. Signed iu_session cookie
        """
        if headers:
            auth_header = headers.get("Authorization") or headers.get("authorization") or ""
            if auth_header.startswith("Bearer "):
                token = auth_header[7:].strip()
                user = SessionManager.verify_token(token)
                if user:
                    return user
        return SessionManager.get_session_from_headers(headers)

    @staticmethod
    def render_forbidden_html(required_roles: Optional[Tuple[str, ...]], user_role: str) -> str:
        """Renders a styled 403 Forbidden page using the unified Layout."""
        from views.layout import Layout

        roles_str = ", ".join(required_roles) if required_roles else "Yetkili Kullanıcı"
        content = f"""
        <div class="card" style="max-width: 580px; margin: 40px auto; text-align: center; border-top: 4px solid var(--danger);">
            <div class="mono" style="font-size: 3.8rem; font-weight: 800; color: var(--danger); line-height: 1;">403</div>
            <h2 style="font-family: 'Cinzel', serif; font-size: 1.6rem; color: #ffffff; margin: 16px 0 10px;">
                Yetkisiz Erişim (Forbidden)
            </h2>
            <p style="color: var(--text-muted); margin-bottom: 18px;">
                Bu işlemi gerçekleştirmek için gerekli role sahip değilsiniz.
            </p>
            <div style="background: #090e1a; padding: 14px 18px; border-radius: 12px; border: 1px solid var(--dark-border); margin-bottom: 24px; font-size: 0.9rem;">
                <div><strong style="color: #94a3b8;">Mevcut Rolünüz:</strong> <span class="mono" style="color: #fbbf24;">{html.escape(user_role)}</span></div>
                <div style="margin-top: 4px;"><strong style="color: #94a3b8;">Gerekli Rol(ler):</strong> <span class="mono" style="color: #34d399;">{html.escape(roles_str)}</span></div>
            </div>
            <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
                <a href="/" class="btn btn-burgundy">🏛️ Ana Sayfaya Dön</a>
                <a href="javascript:history.back()" class="btn btn-ghost">↩ Geri Dön</a>
            </div>
        </div>
        """
        return Layout.render(
            title="403 — Erişim Engellendi",
            active_nav="home",
            content=content
        )

    @classmethod
    def check_request(cls, method: str, path: str, headers: Any) -> Optional[Dict[str, Any]]:
        """
        Evaluates authentication & RBAC for an incoming HTTP request.
        Sets SessionManager.set_current_user(user) for downstream controllers/views.

        Returns:
            - None if the request is allowed to proceed.
            - A response dict (redirect / html / json with status) if blocked (401/302/403).
        """
        clean_path = path.split("?")[0]
        method_upper = method.upper()
        user = cls.extract_user(headers)
        SessionManager.set_current_user(user)

        # 1. Strict API routes (e.g., /api/me)
        if any(clean_path.startswith(prefix) for prefix in cls.STRICT_AUTH_API_PREFIXES):
            if not user:
                return {
                    "status": 401,
                    "json": {"error": "Unauthorized", "message": "Bu endpoint için geçerli bir oturum veya Bearer token gereklidir."}
                }

        # 2. API RBAC enforcement when caller provides an authenticated session/token
        if clean_path.startswith("/api/"):
            if user:
                user_role = str(user.get("role") or "student").lower()
                for rule_method, pattern, allowed_roles in cls.API_RBAC_RULES:
                    if method_upper == rule_method and re.match(pattern, clean_path):
                        if user_role not in allowed_roles:
                            return {
                                "status": 403,
                                "json": {
                                    "error": "Forbidden",
                                    "message": f"'{user_role}' rolü bu işlem için yetkili değil. Gerekli roller: {', '.join(allowed_roles)}"
                                }
                            }
            return None

        # 3. Protected Web UI routes
        for rule_method, pattern, allowed_roles, allow_self in cls.PROTECTED_WEB_RULES:
            if method_upper == rule_method:
                match = re.match(pattern, clean_path)
                if match:
                    if not user:
                        return {"redirect": "/login"}
                    user_role = str(user.get("role") or "student").lower()
                    is_self = False
                    if allow_self and match.groups():
                        try:
                            is_self = int(match.group(1)) == int(user.get("id"))
                        except (TypeError, ValueError):
                            is_self = False

                    if allowed_roles is not None and (user_role not in allowed_roles) and not is_self:
                        return {
                            "status": 403,
                            "html": cls.render_forbidden_html(allowed_roles, user_role)
                        }
                    return None

        return None
