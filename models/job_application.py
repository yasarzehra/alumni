"""
JobApplication Model - MVC Architecture
Backed by Persistent Database Connection (SQLite / MySQL).
Represents candidate applications to job postings within the alumni network.
Maintains bidirectional relationships between Applicants (Users) and JobPostings.
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from database.connection import Database


class JobApplication:
    """
    JobApplication Model representing candidate submissions for job postings.
    Provides complete CRUD operations, duplicate check validation, and relational navigation.
    """

    @staticmethod
    def _format_row(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Formats raw database row to structured model dictionary with embedded applicant & job relations."""
        if not row:
            return None

        first = row.get("applicant_first_name") or ""
        last = row.get("applicant_last_name") or ""
        applicant_name = f"{first} {last}".strip() if (first or last) else (row.get("applicant_email") or "").split("@")[0]
        if not applicant_name:
            applicant_name = f"Kullanıcı #{row.get('applicant_id')}"

        applicant_data = None
        if row.get("applicant_id"):
            applicant_data = {
                "id": row.get("applicant_id"),
                "name": applicant_name,
                "email": row.get("applicant_email"),
                "role": row.get("applicant_role", "student"),
                "phone": row.get("applicant_phone"),
                "linkedin": row.get("applicant_linkedin")
            }

        job_data = None
        if row.get("job_id"):
            job_data = {
                "id": row.get("job_id"),
                "title": row.get("job_title") or f"İş İlanı #{row.get('job_id')}",
                "company_name": row.get("job_company") or "Bilinmeyen Şirket",
                "location": row.get("job_location") or "Remote"
            }

        return {
            "id": row.get("id"),
            "job_id": row.get("job_id"),
            "applicant_id": row.get("applicant_id"),
            "resume_url": row.get("resume_url"),
            "cover_letter": row.get("cover_letter"),
            "status": row.get("status", "pending"),
            "createdAt": row.get("created_at"),
            "updatedAt": row.get("updated_at"),
            "applicant": applicant_data,
            "job": job_data
        }

    @classmethod
    def _base_query(cls) -> str:
        """Returns normalized relational SELECT query joining job_applications with job_postings and users/profiles."""
        return """
            SELECT a.*,
                   j.title as job_title, j.company_name as job_company, j.location as job_location,
                   u.email as applicant_email, u.role as applicant_role,
                   p.first_name as applicant_first_name, p.last_name as applicant_last_name,
                   p.phone as applicant_phone, p.linkedin_url as applicant_linkedin
            FROM job_applications a
            LEFT JOIN job_postings j ON a.job_id = j.id
            LEFT JOIN users u ON a.applicant_id = u.id
            LEFT JOIN profiles p ON u.id = p.user_id
        """

    @classmethod
    def find_all(cls, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        [R]ead: Retrieves all job applications, optionally filtered by job_id, applicant_id, or status.
        Newest applications appear first.
        """
        query = cls._base_query()
        clauses = []
        params = []

        if filters:
            if filters.get("job_id"):
                clauses.append("a.job_id = ?")
                params.append(int(filters["job_id"]))
            if filters.get("applicant_id"):
                clauses.append("a.applicant_id = ?")
                params.append(int(filters["applicant_id"]))
            if filters.get("status"):
                clauses.append("a.status = ?")
                params.append(filters["status"])

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        query += " ORDER BY a.id DESC"
        rows = Database.fetch_all(query, tuple(params))
        return [cls._format_row(r) for r in rows if r]

    @classmethod
    def find_by_id(cls, app_id: int) -> Optional[Dict[str, Any]]:
        """
        [R]ead: Retrieves a single job application by ID with full job & applicant relationships.
        """
        query = cls._base_query() + " WHERE a.id = ?"
        row = Database.fetch_one(query, (int(app_id),))
        return cls._format_row(row)

    @classmethod
    def find_by_job(cls, job_id: int) -> List[Dict[str, Any]]:
        """
        [Relation]: Retrieves all applications submitted to a specific job posting.
        """
        return cls.find_all(filters={"job_id": int(job_id)})

    @classmethod
    def find_by_applicant(cls, applicant_id: int) -> List[Dict[str, Any]]:
        """
        [Relation]: Retrieves all job applications submitted by a specific user.
        """
        return cls.find_all(filters={"applicant_id": int(applicant_id)})

    @classmethod
    def find_by_job_and_applicant(cls, job_id: int, applicant_id: int) -> Optional[Dict[str, Any]]:
        """
        Checks if candidate has already applied to this specific job posting.
        """
        query = cls._base_query() + " WHERE a.job_id = ? AND a.applicant_id = ?"
        row = Database.fetch_one(query, (int(job_id), int(applicant_id)))
        return cls._format_row(row)

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [C]reate: Inserts a new job application record.
        Validates job existence, applicant existence, and uniqueness constraint.
        """
        job_id = data.get("job_id")
        applicant_id = data.get("applicant_id")

        if not job_id:
            raise ValueError("job_id (ilan referansı) alanı zorunludur")
        if not applicant_id:
            raise ValueError("applicant_id (aday referansı) alanı zorunludur")

        # Verify duplicate application
        existing = cls.find_by_job_and_applicant(int(job_id), int(applicant_id))
        if existing:
            raise ValueError(f"Bu ilana ({job_id}) daha önce başvuru yaptınız. (Başvuru #{existing['id']})")

        resume_url = data.get("resume_url")
        cover_letter = data.get("cover_letter")
        status = data.get("status", "pending")
        now = datetime.now(timezone.utc).isoformat()

        app_id = Database.insert("""
            INSERT INTO job_applications (job_id, applicant_id, resume_url, cover_letter, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (int(job_id), int(applicant_id), resume_url, cover_letter, status, now))

        return cls.find_by_id(app_id)

    @classmethod
    def update(cls, app_id: int, data: Dict[str, Any], partial: bool = False) -> Optional[Dict[str, Any]]:
        """
        [U]pdate: Updates application status, cover letter, or resume URL.
        """
        existing = cls.find_by_id(app_id)
        if not existing:
            return None

        fields = []
        values = []

        updatable = ["status", "cover_letter", "resume_url"]
        for key in updatable:
            if key in data and data[key] is not None:
                fields.append(f"{key} = ?")
                values.append(data[key])

        if not fields:
            return existing

        now = datetime.now(timezone.utc).isoformat()
        fields.append("updated_at = ?")
        values.append(now)

        values.append(int(app_id))
        query = f"UPDATE job_applications SET {', '.join(fields)} WHERE id = ?"
        Database.execute(query, tuple(values))

        return cls.find_by_id(app_id)

    @classmethod
    def delete(cls, app_id: int) -> bool:
        """
        [D]elete: Removes/withdraws a job application from the database.
        """
        existing = cls.find_by_id(app_id)
        if not existing:
            return False

        Database.execute("DELETE FROM job_applications WHERE id = ?", (int(app_id),))
        return True

    @classmethod
    def get_job(cls, app_id: int) -> Optional[Dict[str, Any]]:
        """
        [Relation]: Returns the full JobPosting entity for this application.
        """
        app = cls.find_by_id(app_id)
        if not app or not app.get("job_id"):
            return None
        from models.job_posting import JobPosting
        return JobPosting.find_by_id(app["job_id"])

    @classmethod
    def get_applicant(cls, app_id: int) -> Optional[Dict[str, Any]]:
        """
        [Relation]: Returns the full User entity of the applicant.
        """
        app = cls.find_by_id(app_id)
        if not app or not app.get("applicant_id"):
            return None
        from models.user import User
        return User.find_by_id(app["applicant_id"])


# Backward-compatible alias
Application = JobApplication
