"""
ApiJobController - RESTful API Controller
Handles JSON API requests for Job Postings / Career resources and returns HTTP status codes with JSON responses.
Supports direct endpoints as well as nested relational operations.
"""
from typing import Dict, Any, Tuple, Optional
from models.job_posting import JobPosting
from models.user import User


class ApiJobController:
    """
    REST API Controller for JobPosting resources.
    Translates HTTP actions into JobPosting model operations and returns (status_code, json_dict).
    """

    @staticmethod
    def index(query_params: Optional[Dict[str, Any]] = None) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/jobs or /api/job-postings
        [R]ead: Returns all job postings in JSON format with optional query filters.
        """
        items = JobPosting.find_all(filters=query_params)
        return 200, {
            "success": True,
            "count": len(items),
            "data": items
        }

    @staticmethod
    def show(job_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/jobs/{id}
        [R]ead: Returns a single job posting by ID.
        """
        item = JobPosting.find_by_id(job_id)
        if not item:
            return 404, {
                "error": "NotFound",
                "message": f"{job_id} ID'li iş ilanı bulunamadı"
            }
        return 200, {
            "success": True,
            "data": item
        }

    @staticmethod
    def store(data: Dict[str, Any]) -> Tuple[int, Dict[str, Any]]:
        """
        POST /api/jobs
        [C]reate: Creates a new job posting from JSON payload.
        """
        if not data or not data.get("title") or not data.get("company_name") or not data.get("description"):
            return 400, {
                "error": "BadRequest",
                "message": "title, company_name ve description alanları zorunludur"
            }

        try:
            item = JobPosting.create(data)
            return 201, {
                "success": True,
                "message": "İş ilanı başarıyla oluşturuldu",
                "data": item
            }
        except ValueError as e:
            return 400, {
                "error": "BadRequest",
                "message": str(e)
            }

    @staticmethod
    def update(job_id: int, data: Dict[str, Any], partial: bool = False) -> Tuple[int, Dict[str, Any]]:
        """
        PUT/PATCH /api/jobs/{id}
        [U]pdate: Updates job posting information.
        """
        if not JobPosting.find_by_id(job_id):
            return 404, {
                "error": "NotFound",
                "message": f"{job_id} ID'li iş ilanı bulunamadı"
            }

        if not data:
            return 400, {
                "error": "BadRequest",
                "message": "Güncellenecek en az bir alan gönderilmelidir"
            }

        if not partial and (not data.get("title") or not data.get("company_name") or not data.get("description")):
            return 400, {
                "error": "BadRequest",
                "message": "PUT isteğinde title, company_name ve description alanları zorunludur"
            }

        try:
            item = JobPosting.update(job_id, data, partial=partial)
            action_desc = "kısmen güncellendi" if partial else "güncellendi"
            return 200, {
                "success": True,
                "message": f"İş ilanı başarıyla {action_desc}",
                "data": item
            }
        except ValueError as e:
            return 400, {
                "error": "BadRequest",
                "message": str(e)
            }

    @staticmethod
    def destroy(job_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        DELETE /api/jobs/{id}
        [D]elete: Removes a job posting by ID.
        """
        deleted = JobPosting.delete(job_id)
        if not deleted:
            return 404, {
                "error": "NotFound",
                "message": f"{job_id} ID'li iş ilanı bulunamadı"
            }
        return 200, {
            "success": True,
            "message": f"{job_id} ID'li iş ilanı başarıyla silindi"
        }

    # =========================================================================
    # Nested Relational Action
    # =========================================================================

    @staticmethod
    def author(job_id: int) -> Tuple[int, Dict[str, Any]]:
        """
        GET /api/jobs/{id}/author
        [Nested Relation]: Returns the author user profile who published this job.
        """
        author = JobPosting.get_author(job_id)
        if not author:
            return 404, {
                "error": "NotFound",
                "message": f"{job_id} ID'li ilanın yayıncısı bulunamadı veya anonim"
            }
        return 200, {
            "success": True,
            "data": author
        }
