"""
AuthController - Handles user registration, login, and logout workflows for Web and REST API.
"""
from typing import Dict, Any, Optional, Tuple
from models.user import User
from views.view import View
from middlewares.session_middleware import SessionManager


class AuthController:
    """Controller for authentication and registration endpoints."""

    @staticmethod
    def register_form(error: Optional[str] = None, form_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Renders the registration form page.
        Route: GET /register
        """
        departments = User.get_departments()
        return View.render_register(departments=departments, error=error, form_data=form_data)

    @staticmethod
    def register_submit(data: Dict[str, Any]) -> Any:
        """
        Processes web registration form submission and signs the new user in.
        Route: POST /register
        """
        try:
            user = User.register(data)
            token = SessionManager.create_token(user)
            SessionManager.set_current_user(user)
            html_body = View.render_users_show(
                user,
                success=f"Hoş geldiniz {user['name']}! Kaydınız başarıyla oluşturuldu ve oturumunuz açıldı."
            )
            return {
                "html": html_body,
                "cookies": [SessionManager.make_set_cookie_header(token)]
            }
        except ValueError as e:
            departments = User.get_departments()
            return View.render_register(
                departments=departments,
                error=str(e),
                form_data=data
            )

    @staticmethod
    def login_form(error: Optional[str] = None, success: Optional[str] = None, email: str = "") -> str:
        """
        Renders the login form page.
        Route: GET /login
        """
        return View.render_login(error=error, success=success, email=email)

    @staticmethod
    def login_submit(data: Dict[str, Any]) -> Any:
        """
        Authenticates user credentials, sets signed session cookie, and redirects to profile.
        Route: POST /login
        """
        email = str(data.get("email") or "").strip()
        password = str(data.get("password") or "")
        try:
            user = User.authenticate(email, password)
            token = SessionManager.create_token(user)
            SessionManager.set_current_user(user)
            return {
                "redirect": f"/users/{user['id']}",
                "cookies": [SessionManager.make_set_cookie_header(token)]
            }
        except ValueError as e:
            return View.render_login(error=str(e), email=email)

    @staticmethod
    def logout() -> Dict[str, Any]:
        """
        Clears the signed session cookie and redirects to login page.
        Route: GET /logout, POST /logout
        """
        SessionManager.set_current_user(None)
        return {
            "redirect": "/login",
            "cookies": [SessionManager.make_clear_cookie_header()]
        }

    @staticmethod
    def api_register(data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        REST API endpoint for user registration.
        Route: POST /api/register
        """
        try:
            user = User.register(data)
            return 201, {
                "message": "Kayıt başarıyla tamamlandı.",
                "user": user
            }
        except ValueError as e:
            return 400, {
                "error": "ValidationError",
                "message": str(e)
            }

    @staticmethod
    def api_login(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        REST API endpoint for login. Sets session cookie and returns user + token.
        Route: POST /api/login
        """
        try:
            user = User.authenticate(data.get("email", ""), data.get("password", ""))
            token = SessionManager.create_token(user)
            return {
                "status": 200,
                "json": {
                    "message": "Giriş başarılı.",
                    "user": user,
                    "token": token
                },
                "cookies": [SessionManager.make_set_cookie_header(token)]
            }
        except ValueError as e:
            return {
                "status": 401,
                "json": {
                    "error": "Unauthorized",
                    "message": str(e)
                }
            }

    @staticmethod
    def api_logout() -> Dict[str, Any]:
        """
        REST API endpoint for logout. Clears session cookie.
        Route: POST /api/logout
        """
        return {
            "status": 200,
            "json": {"message": "Çıkış yapıldı."},
            "cookies": [SessionManager.make_clear_cookie_header()]
        }

    @staticmethod
    def api_me() -> Tuple[int, Dict[str, Any]]:
        """
        Returns the currently authenticated session user.
        Route: GET /api/me
        """
        session_user = SessionManager.get_current_user()
        if not session_user:
            return 401, {"error": "Unauthorized", "message": "Aktif oturum bulunamadı."}
        full_user = User.find_by_id(session_user["id"])
        return 200, {"user": full_user or session_user}
