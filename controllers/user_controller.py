"""
UserController - Web Controller
Handles web browser requests, interacts with User Model, and coordinates with View Layer.
Provides complete CRUD operations:
- [C]reate: create() -> View (form), store(data) -> Model + View
- [R]ead:   index() -> Model + View (list), show(id) -> Model + View (detail)
- [U]pdate: edit(id) -> View (form), update(id, data) -> Model + View
- [D]elete: destroy(id) -> Model + View
"""
from typing import Dict, Any, Optional
from models.user import User
from views.view import View


class UserController:
    """
    Web Controller for User resources.
    Follows MVC: Interacts with Model (User) and presents via View Layer (View).
    """

    # =========================================================================
    # [R]ead: Listing & Detail Views
    # =========================================================================

    @staticmethod
    def index(error: Optional[str] = None, success: Optional[str] = None) -> str:
        """
        [R]ead: Get all users for the web view.
        Route: GET /users
        """
        users = User.find_all()
        return View.render_users_index(
            users=users,
            count=len(users),
            error=error,
            success=success
        )

    @staticmethod
    def show(user_id: int, success: Optional[str] = None, error: Optional[str] = None) -> str:
        """
        [R]ead: Display a single user profile page.
        Route: GET /users/{id}
        """
        user = User.find_by_id(user_id)
        if not user:
            return View.render_error_404(f"{user_id} ID'li kullanıcı bulunamadı.")
        return View.render_users_show(user, success=success, error=error)

    # =========================================================================
    # [C]reate: Create Form & Storage
    # =========================================================================

    @staticmethod
    def create(error: Optional[str] = None) -> str:
        """
        [C]reate: Render the user creation form.
        Route: GET /users/create
        """
        return View.render_users_create(error=error)

    @staticmethod
    def store(data: Dict[str, Any]) -> str:
        """
        [C]reate: Process web form submission to create a user.
        Route: POST /users
        """
        try:
            user = User.create(data)
            users = User.find_all()
            return View.render_users_index(
                users=users,
                count=len(users),
                success=f"Kullanıcı '{user['name']}' (#{user['id']}) başarıyla eklendi!"
            )
        except ValueError as e:
            # If submitted from /users/create form, re-render form with error;
            # otherwise re-render index with error
            users = User.find_all()
            return View.render_users_index(
                users=users,
                count=len(users),
                error=f"Kullanıcı eklenemedi: {str(e)}"
            )

    # =========================================================================
    # [U]pdate: Edit Form & Processing
    # =========================================================================

    @staticmethod
    def edit(user_id: int, error: Optional[str] = None) -> str:
        """
        [U]pdate: Render the edit form pre-filled with user data.
        Route: GET /users/{id}/edit
        """
        user = User.find_by_id(user_id)
        if not user:
            return View.render_error_404(f"{user_id} ID'li kullanıcı bulunamadı.")
        return View.render_users_edit(user, error=error)

    @staticmethod
    def update(user_id: int, data: Dict[str, Any], partial: bool = False) -> str:
        """
        [U]pdate: Process user updates from web edit form.
        Route: POST /users/{id} or PUT/PATCH /users/{id}
        """
        try:
            user = User.update(user_id, data, partial=partial)
            if not user:
                return View.render_error_404(f"{user_id} ID'li kullanıcı bulunamadı.")
            return View.render_users_show(
                user=user,
                success=f"Kullanıcı #{user_id} bilgileri başarıyla güncellendi!"
            )
        except ValueError as e:
            user = User.find_by_id(user_id)
            if user:
                return View.render_users_edit(user=user, error=f"Güncelleme hatası: {str(e)}")
            return View.render_error_404(f"Güncelleme hatası: {str(e)}")

    # =========================================================================
    # [D]elete: Remove User
    # =========================================================================

    @staticmethod
    def destroy(user_id: int) -> str:
        """
        [D]elete: Remove user and return updated user list view.
        Route: POST /users/{id}/delete or DELETE /users/{id}
        """
        deleted = User.delete(user_id)
        users = User.find_all()
        if not deleted:
            return View.render_users_index(
                users=users,
                count=len(users),
                error=f"{user_id} ID'li kullanıcı bulunamadı veya silinemedi."
            )
        return View.render_users_index(
            users=users,
            count=len(users),
            success=f"#{user_id} ID'li kullanıcı başarıyla silindi."
        )
