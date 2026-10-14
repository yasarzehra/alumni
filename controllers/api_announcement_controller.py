"""
ApiAnnouncementController - RESTful API Controller
Handles JSON API requests for Announcement resources and returns HTTP status codes with JSON responses.
"""
from typing import Dict, Any, Tuple
from models.announcement import Announcement


class ApiAnnouncementController:
    """
    REST API Controller for Announcement resources.
    Translates HTTP actions into Announcement model operations and returns (status_code, json_dict).
    """

    @staticmethod
    def index() -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/announcements
        [R]ead: Returns all announcements in JSON format.
        """
        items = Announcement.find_all()
        return 200, {
            "success": True,
            "count": len(items),
            "data": items
        }

    @staticmethod
    def show(announcement_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/announcements/{id}
        [R]ead: Returns a single announcement by ID.
        """
        item = Announcement.find_by_id(announcement_id)
        if not item:
            return 404, {
                "error": "NotFound",
                "message": f"{announcement_id} ID'li duyuru bulunamadı"
            }
        return 200, {
            "success": True,
            "data": item
        }

    @staticmethod
    def store(data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        POST /api/announcements
        [C]reate: Creates a new announcement from JSON payload.
        """
        if not data or not data.get("title") or not data.get("content"):
            return 400, {
                "error": "BadRequest",
                "message": "title (başlık) ve content (içerik) alanları zorunludur"
            }

        try:
            item = Announcement.create(data)
            return 201, {
                "success": True,
                "message": "Duyuru başarıyla oluşturuldu",
                "data": item
            }
        except ValueError as e:
            return 400, {
                "error": "BadRequest",
                "message": str(e)
            }

    @staticmethod
    def update(announcement_id: int, data: Dict[str, Any], partial: bool = False) -> Tuple[int, Dict[str, Any]]:
        """
        PUT/PATCH /api/announcements/{id}
        [U]pdate: Updates announcement information.
        """
        if not Announcement.find_by_id(announcement_id):
            return 404, {
                "error": "NotFound",
                "message": f"{announcement_id} ID'li duyuru bulunamadı"
            }

        if not data:
            return 400, {
                "error": "BadRequest",
                "message": "Güncellenecek en az bir alan gönderilmelidir"
            }

        if not partial and (not data.get("title") or not data.get("content")):
            return 400, {
                "error": "BadRequest",
                "message": "PUT isteğinde title ve content alanları zorunludur"
            }

        try:
            item = Announcement.update(announcement_id, data, partial=partial)
            action_desc = "kısmen güncellendi" if partial else "güncellendi"
            return 200, {
                "success": True,
                "message": f"Duyuru başarıyla {action_desc}",
                "data": item
            }
        except ValueError as e:
            return 400, {
                "error": "BadRequest",
                "message": str(e)
            }

    @staticmethod
    def destroy(announcement_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        DELETE /api/announcements/{id}
        [D]elete: Removes an announcement by ID.
        """
        deleted = Announcement.delete(announcement_id)
        if not deleted:
            return 404, {
                "error": "NotFound",
                "message": f"{announcement_id} ID'li duyuru bulunamadı"
            }
        return 200, {
            "success": True,
            "message": f"{announcement_id} ID'li duyuru başarıyla silindi"
        }
