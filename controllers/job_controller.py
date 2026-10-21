"""
JobController - Web Controller
Handles web browser requests for Job Postings, interacting with Model and View layers.
Supports Direct and Nested CRUD operations.
"""
from typing import Dict, Any, Optional
from models.job_posting import JobPosting
from models.user import User
from views.job_view import JobView


class JobController:
    """Web Controller for Job Posting resources."""

    @staticmethod
    def index(error: Optional[str] = None, success: Optional[str] = None, filter_user_id: Optional[int] = None) -> str:
        """
        [R]ead: Get all job postings for the web interface.
        Direct: GET /jobs
        Nested: GET /users/{user_id}/jobs
        """
        filters = {}
        filter_user = None
        if filter_user_id:
            filters["alumni_id"] = filter_user_id
            filter_user = User.find_by_id(filter_user_id)

        jobs = JobPosting.find_all(filters=filters if filters else None)
        return JobView.render_index(
            jobs=jobs,
            count=len(jobs),
            error=error,
            success=success,
            filter_user=filter_user
        )

    @staticmethod
    def show(job_id: int) -> str:
        """
        [R]ead: Display single job posting detail page.
        Direct: GET /jobs/{id}
        """
        job = JobPosting.find_by_id(job_id)
        if not job:
            return JobView.render_error_404(f"{job_id} ID'li iş ilanı bulunamadı.")
        return JobView.render_show(job)

    @staticmethod
    def create() -> str:
        """
        [C]reate: Render job posting creation form.
        Direct: GET /jobs/create
        """
        return JobView.render_create()

    @staticmethod
    def store(data: Dict[str, Any]) -> str:
        """
        [C]reate: Process web form submission to create a job posting.
        Direct: POST /jobs
        """
        try:
            new_job = JobPosting.create(data)
            return JobController.index(success=f"'{new_job['title']}' ilanı başarıyla yayınlandı!")
        except Exception as e:
            return JobController.index(error=f"Hata: {str(e)}")

    @staticmethod
    def update(job_id: int, data: Dict[str, Any], partial: bool = False) -> str:
        """
        [U]pdate: Process update submission for a job posting.
        Direct: POST /jobs/{id}
        """
        try:
            JobPosting.update(job_id, data, partial=partial)
            return JobController.index(success=f"İlan #{job_id} başarıyla güncellendi!")
        except Exception as e:
            return JobController.index(error=f"Güncelleme hatası: {str(e)}")

    @staticmethod
    def destroy(job_id: int) -> str:
        """
        [D]elete: Process deletion of a job posting.
        Direct: POST /jobs/{id}/delete
        """
        success = JobPosting.delete(job_id)
        if success:
            return JobController.index(success=f"İlan #{job_id} başarıyla silindi.")
        return JobController.index(error=f"İlan #{job_id} silinemedi.")
