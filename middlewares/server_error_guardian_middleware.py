"""
5xx Guardian Middleware
Catches unexpected server exceptions and system errors (500 Internal Server Error, 502/503),
generates unique incident tracking IDs, logs clean stack traces, and formats user-friendly,
safe error payloads for both REST API and Web HTML clients.
"""
import uuid
import traceback
import os
from datetime import datetime, timezone
from typing import Tuple, Dict, Any
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS_DIR = os.path.join(BASE_DIR, "logs")
ERROR_LOG_PATH = os.path.join(LOGS_DIR, "error.log")


class ServerErrorGuardianMiddleware:
    """
    Guardian middleware intercepting uncaught exceptions, preventing server crashes,
    masking internal infrastructure leaks, assigning unique incident correlation IDs,
    and persisting error details to logs/error.log.
    """

    @classmethod
    def write_error_log(cls, incident_id: str, error_type: str, error_message: str, method: str, path: str, tb_str: str):
        """Appends formatted error incident details to logs/error.log."""
        try:
            os.makedirs(LOGS_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entry = (
                f"[{timestamp}] [INCIDENT {incident_id}] {method.upper()} {path}\n"
                f"Type: {error_type}\n"
                f"Message: {error_message}\n"
                f"Traceback:\n{tb_str}\n"
                f"{'-'*70}\n"
            )
            with open(ERROR_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as log_err:
            print(f"[5xx GUARDIAN] Failed to write to {ERROR_LOG_PATH}: {log_err}", flush=True)

    @classmethod
    def handle(cls, exc: Exception, method: str, path: str) -> Tuple[int, str, str]:
        """
        Handles an exception and returns (status_code, content_type, response_body_str).
        Auto-negotiates JSON for /api/ routes and an HTML error page for web requests.
        """
        incident_id = f"ERR-{uuid.uuid4().hex[:8].upper()}"
        error_type = exc.__class__.__name__
        error_message = str(exc) or "Beklenmeyen bir sunucu hatası meydana geldi."
        timestamp = datetime.now(timezone.utc).isoformat()
        tb_str = traceback.format_exc()
        is_api = path.startswith("/api/")

        # Write to logs/error.log file
        cls.write_error_log(incident_id, error_type, error_message, method, path, tb_str)

        # Log diagnostic traceback to server console with incident tracking
        print(f"\n[5xx GUARDIAN] Incident: {incident_id} | Type: {error_type} | Route: {method.upper()} {path}", flush=True)
        print(tb_str, flush=True)

        if is_api:
            content_type = "application/json"
            payload: Dict[str, Any] = {
                "success": False,
                "status": 500,
                "error": "InternalServerError",
                "incident_id": incident_id,
                "type": error_type,
                "message": error_message,
                "path": path,
                "method": method.upper(),
                "timestamp": timestamp,
                "suggestion": "İstek parametrelerinizi kontrol edip tekrar deneyin veya incident_id ile sistem yöneticisine başvurun."
            }
            body = json.dumps(payload, ensure_ascii=False, indent=2)
        else:
            content_type = "text/html"
            body = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="utf-8">
    <title>500 Sunucu Hatası - 5xx Guardian</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #0f172a; color: #f8fafc; padding: 40px; text-align: center; }}
        .card {{ max-width: 640px; margin: 50px auto; background: #1e293b; border-radius: 12px; padding: 32px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); text-align: left; }}
        h1 {{ color: #f87171; margin-top: 0; }}
        .badge {{ display: inline-block; background: #334155; padding: 4px 10px; border-radius: 6px; font-weight: bold; font-family: monospace; }}
        .incident {{ background: #450a0a; color: #fecaca; padding: 10px 14px; border-radius: 8px; border: 1px solid #7f1d1d; font-family: monospace; font-size: 0.95em; margin: 16px 0; }}
        .reason {{ color: #cbd5e1; margin: 16px 0; font-size: 1.05em; line-height: 1.5; }}
        a {{ color: #38bdf8; text-decoration: none; font-weight: 500; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>🛡️ 500 Sunucu Hatası (5xx Guardian)</h1>
        <p><span class="badge">{method.upper()}</span> <span class="badge">{path}</span></p>
        <div class="incident">
            <strong>Olay Takip Kodu (Incident ID):</strong> {incident_id}<br>
            <strong>Hata Türü:</strong> {error_type}
        </div>
        <p class="reason"><strong>Hata Detayı:</strong> {error_message}</p>
        <hr style="border: 0; border-top: 1px solid #334155; margin: 20px 0;">
        <p style="color: #94a3b8; font-size: 0.9em;">Bu hata sistem koruması tarafından güvenli şekilde izole edilmiştir. Lütfen daha sonra tekrar deneyiniz.</p>
        <p style="margin-top: 24px;"><a href="/">← Ana Sayfaya Dön</a></p>
    </div>
</body>
</html>"""

        return 500, content_type, body
