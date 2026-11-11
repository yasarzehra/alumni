"""
404 Guardian Middleware
Intercepts unmatched routes and 404 conditions, providing clear diagnostics and reasons.
Distinguishes between:
- Method not allowed (e.g. route exists for GET but request was POST)
- Unregistered route / path typo with suggested alternative endpoints
- Web HTML vs REST API JSON content negotiation
"""
from typing import Dict, Any, List, Optional
import json


class NotFoundGuardianMiddleware:
    """
    Guardian middleware protecting against unhandled 404s by enriching error responses
    with root-cause explanations and path suggestions.
    """

    KNOWN_API_PREFIXES = [
        "/api/users",
        "/api/jobs",
        "/api/job-postings",
        "/api/applications",
        "/api/announcements",
        "/api/swagger",
        "/api/health"
    ]

    KNOWN_WEB_ROUTES = [
        "/",
        "/users",
        "/jobs",
        "/applications",
        "/announcements",
        "/about",
        "/ok"
    ]

    @classmethod
    def diagnose_reason(cls, method: str, path: str, router=None) -> Dict[str, Any]:
        """
        Analyzes the incoming method and path to determine the exact reason for the 404 error.
        """
        clean_path = path.split("?")[0].rstrip("/")
        if not clean_path:
            clean_path = "/"

        # Check if the route exists under other HTTP methods
        allowed_methods = []
        if router and hasattr(router, 'routes'):
            for route in router.routes:
                # Test route matching by swapping method
                for test_m in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
                    if test_m != method.upper() and route.match(test_m, clean_path) is not None:
                        if test_m not in allowed_methods:
                            allowed_methods.append(test_m)

        if allowed_methods:
            return {
                "error": "MethodNotAllowed",
                "reason": f"'{clean_path}' rotası {method.upper()} metodunu desteklemiyor.",
                "allowed_methods": allowed_methods,
                "suggestion": f"Bu rota için şu metotları kullanabilirsiniz: {', '.join(allowed_methods)}"
            }

        # Check for near matches or common prefixes
        suggestions = []
        is_api = clean_path.startswith("/api/")
        reference_list = cls.KNOWN_API_PREFIXES if is_api else cls.KNOWN_WEB_ROUTES

        for ref in reference_list:
            if clean_path.startswith(ref) or ref.startswith(clean_path[:8]):
                suggestions.append(ref)

        if not suggestions:
            suggestions = ["/api/swagger", "/api/users", "/api/jobs", "/api/applications"] if is_api else ["/", "/jobs", "/users"]

        return {
            "error": "NotFound",
            "reason": f"'{clean_path}' adresi sunucu rotalarında bulunamadı.",
            "requested_method": method.upper(),
            "requested_path": clean_path,
            "suggestions": suggestions
        }

    @classmethod
    def handle(cls, method: str, path: str, router=None) -> tuple[int, str, str]:
        """
        Returns (status_code, content_type, response_body_str).
        Auto-negotiates response format (JSON for /api/ routes, HTML for web).
        """
        diagnosis = cls.diagnose_reason(method, path, router)
        status_code = 405 if diagnosis.get("error") == "MethodNotAllowed" else 404
        is_api = path.startswith("/api/")

        if is_api:
            content_type = "application/json"
            response_payload = {
                "success": False,
                "status": status_code,
                "error": diagnosis.get("error", "NotFound"),
                "reason": diagnosis.get("reason"),
                "path": diagnosis.get("requested_path", path),
                "method": method.upper(),
                "details": {
                    "suggestion": diagnosis.get("suggestion") or diagnosis.get("suggestions")
                }
            }
            body = json.dumps(response_payload, ensure_ascii=False, indent=2)
        else:
            content_type = "text/html"
            suggestions_html = "".join([f"<li><a href='{s}'>{s}</a></li>" for s in diagnosis.get("suggestions", [])])
            body = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <title>404 Sayfa Bulunamadı - Guardian</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; text-align: center; }}
        .card {{ max-width: 600px; margin: 50px auto; background: #1e293b; border-radius: 12px; padding: 32px; box-shadow: 0 8px 24px rgba(0,0,0,0.4); text-align: left; }}
        h1 {{ color: #ef4444; margin-top: 0; }}
        .badge {{ display: inline-block; background: #334155; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-family: monospace; }}
        .reason {{ color: #cbd5e1; margin: 16px 0; font-size: 1.1em; line-height: 1.5; }}
        ul {{ list-style: none; padding: 0; margin-top: 12px; }}
        li {{ margin-bottom: 8px; }}
        a {{ color: #38bdf8; text-decoration: none; font-family: monospace; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🛡️ 404 Not Found (Guardian)</h1>
        <p><span class="badge">{method.upper()}</span> <span class="badge">{path}</span></p>
        <p class="reason"><strong>Sebep:</strong> {diagnosis.get('reason')}</p>
        <hr style="border: 0; border-top: 1px solid #334155; margin: 20px 0;">
        <p><strong>Önerilen Uç Noktalar:</strong></p>
        <ul>
            {suggestions_html}
        </ul>
        <p style="margin-top: 24px;"><a href="/">← Ana Sayfaya Dön</a></p>
    </div>
</body>
</html>"""

        return status_code, content_type, body
