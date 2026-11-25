"""
SessionMiddleware - Signed Cookie Session Management
Provides HMAC-SHA256 signed session tokens and thread-local current_user context
for Web and API requests without external dependencies.
"""
import base64
import hashlib
import hmac
import json
import os
import threading
import time
from http.cookies import SimpleCookie
from typing import Any, Dict, Optional

_SECRET_KEY = os.environ.get("IU_SESSION_SECRET", "iu-alumni-1453-beyazit-session-secret-key").encode("utf-8")
_SESSION_COOKIE_NAME = "iu_session"
_SESSION_TTL_SECONDS = 86400  # 24 hours

_request_ctx = threading.local()


class SessionManager:
    """Handles creation, verification, and request-scoped storage of user sessions."""

    @staticmethod
    def create_token(user: Dict[str, Any]) -> str:
        payload = {
            "id": user.get("id"),
            "email": user.get("email"),
            "name": user.get("name"),
            "role": user.get("role", "alumni"),
            "exp": int(time.time()) + _SESSION_TTL_SECONDS,
        }
        raw_json = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
        b64_payload = base64.urlsafe_b64encode(raw_json).decode("ascii").rstrip("=")
        sig = hmac.new(_SECRET_KEY, b64_payload.encode("ascii"), hashlib.sha256).hexdigest()
        return f"{b64_payload}.{sig}"

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        if not token or "." not in token:
            return None
        try:
            b64_payload, sig = token.split(".", 1)
            expected_sig = hmac.new(_SECRET_KEY, b64_payload.encode("ascii"), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(sig, expected_sig):
                return None
            padding = "=" * (-len(b64_payload) % 4)
            raw_json = base64.urlsafe_b64decode(b64_payload + padding).decode("utf-8")
            payload = json.loads(raw_json)
            if int(payload.get("exp", 0)) < int(time.time()):
                return None
            return payload
        except Exception:
            return None

    @classmethod
    def get_session_from_headers(cls, headers: Any) -> Optional[Dict[str, Any]]:
        cookie_header = headers.get("Cookie") if headers else None
        if not cookie_header:
            return None
        cookie = SimpleCookie()
        try:
            cookie.load(cookie_header)
        except Exception:
            return None
        morsel = cookie.get(_SESSION_COOKIE_NAME)
        if not morsel:
            return None
        return cls.verify_token(morsel.value)

    @staticmethod
    def make_set_cookie_header(token: str) -> str:
        return f"{_SESSION_COOKIE_NAME}={token}; HttpOnly; Path=/; SameSite=Lax; Max-Age={_SESSION_TTL_SECONDS}"

    @staticmethod
    def make_clear_cookie_header() -> str:
        return f"{_SESSION_COOKIE_NAME}=; HttpOnly; Path=/; SameSite=Lax; Max-Age=0"

    @staticmethod
    def set_current_user(user: Optional[Dict[str, Any]]) -> None:
        _request_ctx.user = user

    @staticmethod
    def get_current_user() -> Optional[Dict[str, Any]]:
        return getattr(_request_ctx, "user", None)
