"""
AnnouncementController - Web Controller
Handles web browser requests for Announcements, interacting with Model and View layer.
Supports complete management interface operations:
- [R] Listing:  index()
- [C] Create:   create() (form), store() (action)
- [R] Show:     show(id) (detail)
- [U] Edit:     edit(id) (form), update(id, data) (action)
- [D] Delete:   destroy(id) (action)
"""
from typing import Dict, Any, Optional
from models.announcement import Announcement
from views.announcement_view import AnnouncementView


class AnnouncementController:
    """
    Web Controller for Announcement resources.
    Follows MVC: Orchestrates between Announcement model and AnnouncementView presentation.
    """

    @staticmethod
    def index(error: Optional[str] = None, success: Optional[str] = None) -> str:
        """
        [R]ead: Get all announcements for the management interface.
        Route: GET /announcements
        """
        announcements = Announcement.find_all()
        return AnnouncementView.render_index(
            announcements=announcements,
            count=len(announcements),
            error=error,
            success=success
        )

    @staticmethod
    def show(announcement_id: int, success: Optional[str] = None, error: Optional[str] = None) -> str:
        """
        [R]ead: Display single announcement detail page.
        Route: GET /announcements/{id}
        """
        item = Announcement.find_by_id(announcement_id)
        if not item:
            return AnnouncementView.render_error_404(f"{announcement_id} ID'li duyuru bulunamadı.")
        return AnnouncementView.render_show(item, success=success, error=error)

    @staticmethod
    def create(error: Optional[str] = None) -> str:
        """
        [C]reate: Render standalone announcement creation form.
        Route: GET /announcements/create
        """
        return AnnouncementView.render_create(error=error)

    @staticmethod
    def store(data: Dict[str, Any]) -> str:
        """
        [C]reate: Process web form submission to create an announcement.
        Route: POST /announcements
        """
        try:
            item = Announcement.create(data)
            announcements = Announcement.find_all()
            return AnnouncementView.render_index(
                announcements=announcements,
                count=len(announcements),
                success=f"Duyuru '{item['title']}' (#{item['id']}) başarıyla yayınlandı!"
            )
        except ValueError as e:
            announcements = Announcement.find_all()
            return AnnouncementView.render_index(
                announcements=announcements,
                count=len(announcements),
                error=f"Duyuru eklenemedi: {str(e)}"
            )

    @staticmethod
    def edit(announcement_id: int, error: Optional[str] = None) -> str:
        """
        [U]pdate: Render the edit form pre-filled with announcement data.
        Route: GET /announcements/{id}/edit
        """
        item = Announcement.find_by_id(announcement_id)
        if not item:
            return AnnouncementView.render_error_404(f"{announcement_id} ID'li duyuru bulunamadı.")
        return AnnouncementView.render_edit(item, error=error)

    @staticmethod
    def update(announcement_id: int, data: Dict[str, Any], partial: bool = False) -> str:
        """
        [U]pdate: Process announcement update from web form.
        Route: POST /announcements/{id} or PUT/PATCH /announcements/{id}
        """
        try:
            item = Announcement.update(announcement_id, data, partial=partial)
            if not item:
                return AnnouncementView.render_error_404(f"{announcement_id} ID'li duyuru bulunamadı.")
            return AnnouncementView.render_show(
                item,
                success=f"Duyuru #{announcement_id} başarıyla güncellendi!"
            )
        except ValueError as e:
            item = Announcement.find_by_id(announcement_id)
            if item:
                return AnnouncementView.render_edit(item, error=f"Güncelleme hatası: {str(e)}")
            return AnnouncementView.render_error_404(f"Güncelleme hatası: {str(e)}")

    @staticmethod
    def destroy(announcement_id: int) -> str:
        """
        [D]elete: Remove announcement and return to management interface.
        Route: POST /announcements/{id}/delete or DELETE /announcements/{id}
        """
        deleted = Announcement.delete(announcement_id)
        announcements = Announcement.find_all()
        if not deleted:
            return AnnouncementView.render_index(
                announcements=announcements,
                count=len(announcements),
                error=f"{announcement_id} ID'li duyuru bulunamadı veya silinemedi."
            )
        return AnnouncementView.render_index(
            announcements=announcements,
            count=len(announcements),
            success=f"#{announcement_id} ID'li duyuru başarıyla silindi."
        )
