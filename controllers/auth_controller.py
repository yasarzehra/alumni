"""
AuthController - Handles user registration workflows for Web and REST API.
"""
from typing import Dict, Any, Optional, Tuple
from models.user import User
from views.view import View


class AuthController:
    """Controller for user registration endpoints."""

    @staticmethod
    def register_form(error: Optional[str] = None, form_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Renders the registration form page.
        Route: GET /register
        """
        departments = User.get_departments()
        return View.render_register(departments=departments, error=error, form_data=form_data)

    @staticmethod
    def register_submit(data: Dict[str, Any]) -> str:
        """
        Processes web registration form submission.
        Route: POST /register
        """
        try:
            user = User.register(data)
            return View.render_users_show(
                user,
                success=f"Hoş geldiniz {user['name']}! Kaydınız başarıyla oluşturuldu."
            )
        except ValueError as e:
            departments = User.get_departments()
            return View.render_register(
                departments=departments,
                error=str(e),
                form_data=data
            )

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
