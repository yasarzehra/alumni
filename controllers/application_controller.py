"""
ApplicationController - Web Controller
Handles web browser requests for Job Applications, interacting with Model and View layers.
Supports Direct listing and Nested application flows (/jobs/{id}/apply, /users/{id}/applications).
"""
from typing import Dict, Any, Optional
from models.job_application import JobApplication
from models.job_posting import JobPosting
from models.user import User
from views.application_view import ApplicationView


class ApplicationController:
    """Web Controller for Job Application resources."""

    @staticmethod
    def index(error: Optional[str] = None, success: Optional[str] = None, filter_job_id: Optional[int] = None, filter_user_id: Optional[int] = None) -> str:
        """
        [R]ead: Get all applications.
        Direct: GET /applications
        Nested (Job): GET /jobs/{job_id}/applications
        Nested (User): GET /users/{user_id}/applications
        """
        filters = {}
        filter_title = None

        if filter_job_id:
            filters["job_id"] = filter_job_id
            job = JobPosting.find_by_id(filter_job_id)
            if job:
                filter_title = f"'{job['title']}' ilanına gelen başvurular"
        elif filter_user_id:
            filters["applicant_id"] = filter_user_id
            user = User.find_by_id(filter_user_id)
            if user:
                filter_title = f"'{user['name']}' tarafından yapılan başvurular"

        apps = JobApplication.find_all(filters=filters if filters else None)
        return ApplicationView.render_index(
            applications=apps,
            count=len(apps),
            error=error,
            success=success,
            filter_title=filter_title
        )

    @staticmethod
    def apply_form(job_id: int) -> str:
        """
        [C]reate Form: Render candidate application form for a specific job.
        Nested: GET /jobs/{id}/apply
        """
        job = JobPosting.find_by_id(job_id)
        if not job:
            return "İş ilanı bulunamadı"
        return ApplicationView.render_apply_form(job=job)

    @staticmethod
    def submit_application(job_id: int, data: Dict[str, Any]) -> str:
        """
        [C]reate Action: Submit candidate application for a specific job.
        Nested: POST /jobs/{id}/apply
        """
        data["job_id"] = int(job_id)
        if not data.get("applicant_id"):
            # Default to first available user
            first_user = User.find_all()
            data["applicant_id"] = first_user[0]["id"] if first_user else 1

        try:
            new_app = JobApplication.create(data)
            return ApplicationController.index(success=f"Başvurunuz başarıyla kaydedildi! (Başvuru #{new_app['id']})")
        except Exception as e:
            return ApplicationController.index(error=f"Başvuru hatası: {str(e)}")

    @staticmethod
    def destroy(app_id: int) -> str:
        """
        [D]elete: Withdraw/remove an application.
        Direct: POST /applications/{id}/delete
        """
        success = JobApplication.delete(app_id)
        if success:
            return ApplicationController.index(success=f"Başvuru #{app_id} başarıyla silindi.")
        return ApplicationController.index(error=f"Başvuru #{app_id} silinemedi.")
