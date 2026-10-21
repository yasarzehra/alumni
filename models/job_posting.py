"""
JobPosting Model - MVC Architecture
Backed by Persistent Database Connection (SQLite / MySQL).
Represents career, employment, and internship opportunities in the alumni ecosystem.
Supports complete relational mappings with User / Alumni entities.
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from database.connection import Database


class JobPosting:
    """
    JobPosting Model representing career opportunities posted by alumni and recruiters.
    Provides complete CRUD operations, relational joins with User/Profile, and filtering.
    """

    @staticmethod
    def _format_row(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Formats raw database row to structured model dictionary with embedded author relation."""
        if not row:
            return None

        first = row.get("poster_first_name") or ""
        last = row.get("poster_last_name") or ""
        author_name = f"{first} {last}".strip() if (first or last) else (row.get("poster_email") or "").split("@")[0]
        if not author_name:
            author_name = "Alumni Üyesi"

        author_data = None
        if row.get("alumni_id"):
            author_data = {
                "id": row.get("alumni_id"),
                "name": author_name,
                "email": row.get("poster_email"),
                "role": row.get("poster_role", "alumni"),
                "company": row.get("poster_company") or row.get("company_name")
            }

        return {
            "id": row.get("id"),
            "alumni_id": row.get("alumni_id"),
            "title": row.get("title"),
            "company_name": row.get("company_name"),
            "location": row.get("location") or "Belirtilmemiş (Remote / Hybrid)",
            "employment_type": row.get("employment_type", "full_time"),
            "experience_level": row.get("experience_level", "entry"),
            "description": row.get("description"),
            "requirements": row.get("requirements"),
            "salary_range": row.get("salary_range"),
            "application_url": row.get("application_url"),
            "status": row.get("status", "active"),
            "expires_at": row.get("expires_at"),
            "createdAt": row.get("created_at"),
            "updatedAt": row.get("updated_at"),
            "author": author_data
        }

    @classmethod
    def _base_query(cls) -> str:
        """Returns normalized relational SELECT query joining job_postings with users and profiles."""
        return """
            SELECT j.*,
                   u.email as poster_email, u.role as poster_role,
                   p.first_name as poster_first_name, p.last_name as poster_last_name,
                   a.current_company as poster_company
            FROM job_postings j
            LEFT JOIN users u ON j.alumni_id = u.id
            LEFT JOIN profiles p ON u.id = p.user_id
            LEFT JOIN alumni_details a ON p.id = a.profile_id
        """

    @classmethod
    def find_all(cls, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        [R]ead: Retrieves job postings with optional filtering by status, type, or search term.
        Newest postings appear first.
        """
        query = cls._base_query()
        clauses = []
        params = []

        if filters:
            if filters.get("status"):
                clauses.append("j.status = ?")
                params.append(filters["status"])
            if filters.get("employment_type"):
                clauses.append("j.employment_type = ?")
                params.append(filters["employment_type"])
            if filters.get("alumni_id"):
                clauses.append("j.alumni_id = ?")
                params.append(int(filters["alumni_id"]))
            if filters.get("search"):
                term = f"%{filters['search']}%"
                clauses.append("(j.title LIKE ? OR j.company_name LIKE ? OR j.location LIKE ?)")
                params.extend([term, term, term])

        if clauses:
            query += " WHERE " + " AND ".join(clauses)

        query += " ORDER BY j.id DESC"
        rows = Database.fetch_all(query, tuple(params))
        return [cls._format_row(r) for r in rows if r]

    @classmethod
    def find_by_id(cls, job_id: int) -> Optional[Dict[str, Any]]:
        """
        [R]ead: Retrieves a single job posting by ID with author relationship populated.
        """
        query = cls._base_query() + " WHERE j.id = ?"
        row = Database.fetch_one(query, (int(job_id),))
        return cls._format_row(row)

    @classmethod
    def find_by_alumni(cls, alumni_id: int) -> List[Dict[str, Any]]:
        """
        [Relation]: Retrieves all job postings published by a specific alumni/user ID.
        """
        return cls.find_all(filters={"alumni_id": int(alumni_id)})

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [C]reate: Inserts a new job posting record into the database.
        Validates required fields: title, company_name, description.
        """
        title = data.get("title")
        company_name = data.get("company_name")
        description = data.get("description")
        alumni_id = data.get("alumni_id")

        if not title or not str(title).strip():
            raise ValueError("title (iş başlığı) alanı zorunludur")
        if not company_name or not str(company_name).strip():
            raise ValueError("company_name (şirket adı) alanı zorunludur")
        if not description or not str(description).strip():
            raise ValueError("description (iş tanımı) alanı zorunludur")

        # Fallback to the first available user if alumni_id is not explicitly provided
        if not alumni_id:
            first_user = Database.fetch_one("SELECT id FROM users LIMIT 1")
            alumni_id = first_user["id"] if first_user else 1

        location = data.get("location") or "Belirtilmemiş"
        employment_type = data.get("employment_type", "full_time")
        experience_level = data.get("experience_level", "entry")
        requirements = data.get("requirements")
        salary_range = data.get("salary_range")
        application_url = data.get("application_url")
        status = data.get("status", "active")
        expires_at = data.get("expires_at")
        now = datetime.now(timezone.utc).isoformat()

        job_id = Database.insert("""
            INSERT INTO job_postings (
                alumni_id, title, company_name, location, employment_type,
                experience_level, description, requirements, salary_range,
                application_url, status, expires_at, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            int(alumni_id), str(title).strip(), str(company_name).strip(),
            str(location).strip(), employment_type, experience_level,
            str(description).strip(), requirements, salary_range,
            application_url, status, expires_at, now
        ))

        # Also maintain compatibility with legacy job_posts table if it exists
        try:
            Database.insert("""
                INSERT OR IGNORE INTO job_posts (id, alumni_id, title, company_name, location, employment_type, description, application_url, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (job_id, int(alumni_id), str(title).strip(), str(company_name).strip(), str(location).strip(), employment_type, str(description).strip(), application_url, now))
        except Exception:
            pass

        return cls.find_by_id(job_id)

    @classmethod
    def update(cls, job_id: int, data: Dict[str, Any], partial: bool = False) -> Optional[Dict[str, Any]]:
        """
        [U]pdate: Updates an existing job posting record.
        """
        existing = cls.find_by_id(job_id)
        if not existing:
            return None

        if not partial and (not data.get("title") or not data.get("company_name") or not data.get("description")):
            raise ValueError("PUT isteğinde title, company_name ve description alanları zorunludur")

        fields = []
        values = []

        updatable = [
            "title", "company_name", "location", "employment_type",
            "experience_level", "description", "requirements",
            "salary_range", "application_url", "status", "expires_at"
        ]

        for key in updatable:
            if key in data and data[key] is not None:
                fields.append(f"{key} = ?")
                values.append(data[key])

        if not fields:
            return existing

        now = datetime.now(timezone.utc).isoformat()
        fields.append("updated_at = ?")
        values.append(now)

        values.append(int(job_id))
        query = f"UPDATE job_postings SET {', '.join(fields)} WHERE id = ?"
        Database.execute(query, tuple(values))

        # Mirror update to legacy job_posts table if applicable
        try:
            legacy_fields = [f for f in fields if f.split()[0] in ["title", "company_name", "location", "employment_type", "description", "application_url"]]
            if legacy_fields:
                leg_values = [data[f.split()[0]] for f in legacy_fields]
                leg_values.append(int(job_id))
                Database.execute(f"UPDATE job_posts SET {', '.join(legacy_fields)} WHERE id = ?", tuple(leg_values))
        except Exception:
            pass

        return cls.find_by_id(job_id)

    @classmethod
    def delete(cls, job_id: int) -> bool:
        """
        [D]elete: Removes job posting from persistent database.
        """
        existing = cls.find_by_id(job_id)
        if not existing:
            return False

        Database.execute("DELETE FROM job_postings WHERE id = ?", (int(job_id),))
        try:
            Database.execute("DELETE FROM job_posts WHERE id = ?", (int(job_id),))
        except Exception:
            pass
        return True

    @classmethod
    def get_author(cls, job_id: int) -> Optional[Dict[str, Any]]:
        """
        [Relation]: Returns the full User record of the author who published this job posting.
        """
        job = cls.find_by_id(job_id)
        if not job or not job.get("alumni_id"):
            return None
        # Delayed import to avoid circular dependency
        from models.user import User
        return User.find_by_id(job["alumni_id"])


# Backward-compatible alias
JobPost = JobPosting
