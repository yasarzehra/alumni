"""
ApiUserController - RESTful API Controller
Handles JSON API requests and returns HTTP status codes and JSON payloads.
"""
from typing import Dict, Any, Tuple
from models.user import User


class ApiUserController:
    """
    REST API Controller for User resources.
    Translates HTTP actions into User model operations and returns (status_code, json_dict).
    """

    @staticmethod
    def index() -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/users
        [R]ead: Returns a list of all users.
        """
        users = User.find_all()
        return 200, {
            "success": True,
            "count": len(users),
            "data": users
        }

    @staticmethod
    def show(user_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/users/{id}
        [R]ead: Returns a single user by ID.
        """
        user = User.find_by_id(user_id)
        if not user:
            return 404, {
                "error": "NotFound",
                "message": f"{user_id} ID'li kullanıcı bulunamadı"
            }
        return 200, {
            "success": True,
            "data": user
        }

    @staticmethod
    def store(data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        POST /api/users
        [C]reate: Creates a new user record from JSON payload.
        """
        if not data or not data.get("name") or not data.get("email"):
            return 400, {
                "error": "BadRequest",
                "message": "name ve email alanları zorunludur"
            }

        try:
            new_user = User.create(data)
            return 201, {
                "success": True,
                "message": "Kullanıcı başarıyla oluşturuldu",
                "data": new_user
            }
        except ValueError as e:
            err_msg = str(e)
            status_code = 409 if "already registered" in err_msg or "already in use" in err_msg else 400
            err_type = "Conflict" if status_code == 409 else "BadRequest"
            return status_code, {
                "error": err_type,
                "message": err_msg
            }

    @staticmethod
    def update(user_id: int, data: Dict[str, Any], partial: bool = False) -> Tuple[int, Dict[str, Any]]:
        """
        PUT /api/users/{id} (partial=False) or PATCH /api/users/{id} (partial=True)
        [U]pdate: Updates user information.
        """
        if not User.find_by_id(user_id):
            return 404, {
                "error": "NotFound",
                "message": f"{user_id} ID'li kullanıcı bulunamadı"
            }

        if not data:
            return 400, {
                "error": "BadRequest",
                "message": "Güncellenecek en az bir alan gönderilmelidir"
            }

        if not partial and (not data.get("name") or not data.get("email")):
            return 400, {
                "error": "BadRequest",
                "message": "PUT isteğinde name ve email alanları zorunludur"
            }

        try:
            updated_user = User.update(user_id, data, partial=partial)
            action_desc = "kısmen güncellendi" if partial else "güncellendi"
            return 200, {
                "success": True,
                "message": f"Kullanıcı başarıyla {action_desc}",
                "data": updated_user
            }
        except ValueError as e:
            err_msg = str(e)
            status_code = 409 if "already in use" in err_msg else 400
            err_type = "Conflict" if status_code == 409 else "BadRequest"
            return status_code, {
                "error": err_type,
                "message": err_msg
            }

    @staticmethod
    def destroy(user_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        DELETE /api/users/{id}
        [D]elete: Removes a user by ID.
        """
        deleted = User.delete(user_id)
        if not deleted:
            return 404, {
                "error": "NotFound",
                "message": f"{user_id} ID'li kullanıcı bulunamadı"
            }
        return 200, {
            "success": True,
            "message": f"{user_id} ID'li kullanıcı başarıyla silindi"
        }
