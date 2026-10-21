"""
ApiApplicationController - RESTful API Controller
Handles JSON API requests for Job Applications and candidate submissions.
Supports direct endpoints as well as nested relational operations under Jobs and Users.
"""
from typing import Dict, Any, Tuple, Optional
from models.job_application import JobApplication
from models.job_posting import JobPosting
from models.user import User


class ApiApplicationController:
    """
    REST API Controller for JobApplication resources.
    Translates HTTP actions into JobApplication model operations and returns (status_code, json_dict).
    """

    # =========================================================================
    # 1. Direct Routes (/api/applications)
    # =========================================================================

    @staticmethod
    def index(filters: Optional[Dict[str, Any]] = None) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/applications
        [R]ead: Returns all applications in JSON format with optional query filters.
        """
        items = JobApplication.find_all(filters=filters)
        return 200, {
            "success": True,
            "count": len(items),
            "data": items
        }

    @staticmethod
    def show(app_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/applications/{id}
        [R]ead: Returns a single application by ID with full applicant and job information.
        """
        item = JobApplication.find_by_id(app_id)
        if not item:
            return 404, {
                "error": "NotFound",
                "message": f"{app_id} ID'li başvuru bulunamadı"
            }
        return 200, {
            "success": True,
            "data": item
        }

    @staticmethod
    def store(data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        POST /api/applications
        [C]reate: Submits a new job application from JSON payload.
        """
        if not data or not data.get("job_id") or not data.get("applicant_id"):
            return 400, {
                "error": "BadRequest",
                "message": "job_id ve applicant_id alanları zorunludur"
            }

        try:
            item = JobApplication.create(data)
            return 201, {
                "success": True,
                "message": "Başvuru başarıyla alındı",
                "data": item
            }
        except ValueError as e:
            return 400, {
                "error": "BadRequest",
                "message": str(e)
            }

    @staticmethod
    def update(app_id: int, data: Dict[str, Any], partial: bool = False) -> Tuple[int, Dict[str, Any]]:
        """
        PUT/PATCH /api/applications/{id}
        [U]pdate: Updates application status, cover letter, or resume URL.
        """
        if not JobApplication.find_by_id(app_id):
            return 404, {
                "error": "NotFound",
                "message": f"{app_id} ID'li başvuru bulunamadı"
            }

        if not data:
            return 400, {
                "error": "BadRequest",
                "message": "Güncellenecek alan gönderilmelidir"
            }

        try:
            item = JobApplication.update(app_id, data, partial=partial)
            return 200, {
                "success": True,
                "message": "Başvuru başarıyla güncellendi",
                "data": item
            }
        except ValueError as e:
            return 400, {
                "error": "BadRequest",
                "message": str(e)
            }

    @staticmethod
    def destroy(app_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        DELETE /api/applications/{id}
        [D]elete: Withdraws/deletes a job application.
        """
        deleted = JobApplication.delete(app_id)
        if not deleted:
            return 404, {
                "error": "NotFound",
                "message": f"{app_id} ID'li başvuru bulunamadı"
            }
        return 200, {
            "success": True,
            "message": f"{app_id} ID'li başvuru başarıyla silindi"
        }

    # =========================================================================
    # 2. Nested Relational Actions
    # =========================================================================

    @staticmethod
    def by_job(job_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/jobs/{job_id}/applications
        [Nested Relation]: Returns all applications submitted to a specific job.
        """
        job = JobPosting.find_by_id(job_id)
        if not job:
            return 404, {
                "error": "NotFound",
                "message": f"{job_id} ID'li iş ilanı bulunamadı"
            }
        apps = JobApplication.find_by_job(job_id)
        return 200, {
            "success": True,
            "job_id": job_id,
            "job_title": job["title"],
            "count": len(apps),
            "data": apps
        }

    @staticmethod
    def store_for_job(job_id: int, data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        POST /api/jobs/{job_id}/applications
        [Nested Relation]: Submits an application directly scoped to a job.
        """
        job = JobPosting.find_by_id(job_id)
        if not job:
            return 404, {
                "error": "NotFound",
                "message": f"{job_id} ID'li iş ilanı bulunamadı"
            }
        data["job_id"] = job_id
        return ApiApplicationController.store(data)

    @staticmethod
    def by_user(user_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/users/{user_id}/applications
        [Nested Relation]: Returns all job applications submitted by a specific user.
        """
        user = User.find_by_id(user_id)
        if not user:
            return 404, {
                "error": "NotFound",
                "message": f"{user_id} ID'li kullanıcı bulunamadı"
            }
        apps = User.get_applications(user_id)
        return 200, {
            "success": True,
            "user_id": user_id,
            "user_name": user["name"],
            "count": len(apps),
            "data": apps
        }

    @staticmethod
    def get_job_rel(app_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/applications/{id}/job
        [Nested Relation]: Returns the job details for this application.
        """
        job = JobApplication.get_job(app_id)
        if not job:
            return 404, {"error": "NotFound", "message": f"{app_id} ID'li başvurunun ilanı bulunamadı"}
        return 200, {"success": True, "data": job}

    @staticmethod
    def get_applicant_rel(app_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/applications/{id}/applicant
        [Nested Relation]: Returns the candidate profile for this application.
        """
        applicant = JobApplication.get_applicant(app_id)
        if not applicant:
            return 404, {"error": "NotFound", "message": f"{app_id} ID'li başvurunun adayı bulunamadı"}
        return 200, {"success": True, "data": applicant}
