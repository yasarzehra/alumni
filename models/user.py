"""
User Model - MVC Architecture
Backed by Persistent Database Connection (SQLite / MySQL).
Replaces ephemeral in-memory storage with ACID-compliant relational persistence.
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
import hashlib
import hmac
import re
import secrets
from database.connection import Database


class User:
    """
    User Model representing the User entity and its Profile relationship.
    Directly connected to the persistent database.
    """

    @staticmethod
    def _format_row(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Formats raw database row to match model attributes."""
        if not row:
            return None
        first = row.get("first_name") or ""
        last = row.get("last_name") or ""
        name = f"{first} {last}".strip() if (first or last) else row.get("email", "").split("@")[0]

        data = {
            "id": row.get("id"),
            "name": name,
            "first_name": first,
            "last_name": last,
            "email": row.get("email"),
            "role": row.get("role", "alumni"),
            "status": row.get("status", "active"),
            "createdAt": row.get("created_at"),
            "updatedAt": row.get("updated_at"),
            "phone": row.get("phone"),
            "bio": row.get("bio"),
            "linkedin_url": row.get("linkedin_url"),
            "company": row.get("current_company"),
            "title": row.get("current_title"),
            "graduation_year": row.get("graduation_year")
        }
        return data

    @classmethod
    def find_all(cls) -> List[Dict[str, Any]]:
        """
        [R]ead: Retrieves all users stored in the database.
        """
        query = """
            SELECT u.id, u.email, u.role, u.status, u.created_at, u.updated_at,
                   p.first_name, p.last_name, p.phone, p.bio, p.linkedin_url,
                   a.current_company, a.current_title, a.graduation_year
            FROM users u
            LEFT JOIN profiles p ON u.id = p.user_id
            LEFT JOIN alumni_details a ON p.id = a.profile_id
            ORDER BY u.id ASC
        """
        rows = Database.fetch_all(query)
        return [cls._format_row(r) for r in rows if r]

    @classmethod
    def find_by_id(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """
        [R]ead: Retrieves a single user record by ID.
        """
        query = """
            SELECT u.id, u.email, u.role, u.status, u.created_at, u.updated_at,
                   p.first_name, p.last_name, p.phone, p.bio, p.linkedin_url,
                   a.current_company, a.current_title, a.graduation_year
            FROM users u
            LEFT JOIN profiles p ON u.id = p.user_id
            LEFT JOIN alumni_details a ON p.id = a.profile_id
            WHERE u.id = ?
        """
        row = Database.fetch_one(query, (user_id,))
        return cls._format_row(row)

    @classmethod
    def find_by_email(cls, email: str) -> Optional[Dict[str, Any]]:
        """
        [R]ead: Retrieves a user record by email.
        """
        query = """
            SELECT u.id, u.email, u.role, u.status, u.created_at, u.updated_at,
                   p.first_name, p.last_name, p.phone, p.bio, p.linkedin_url,
                   a.current_company, a.current_title, a.graduation_year
            FROM users u
            LEFT JOIN profiles p ON u.id = p.user_id
            LEFT JOIN alumni_details a ON p.id = a.profile_id
            WHERE LOWER(u.email) = LOWER(?)
        """
        row = Database.fetch_one(query, (email.strip(),))
        return cls._format_row(row)

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [C]reate: Inserts a new user record into the database.
        Validates required fields and checks for unique email constraint.
        """
        name = data.get("name") or f"{data.get('first_name', '')} {data.get('last_name', '')}".strip()
        email = data.get("email")

        if not name or not str(name).strip():
            raise ValueError("name (ad soyad) alanı zorunludur")
        if not email or not str(email).strip():
            raise ValueError("email alanı zorunludur")

        email_clean = str(email).strip().lower()
        if cls.find_by_email(email_clean):
            raise ValueError(f"Email '{email}' is already registered")

        # Split name into first and last name
        name_parts = str(name).strip().split(maxsplit=1)
        first_name = data.get("first_name") or name_parts[0]
        last_name = data.get("last_name") or (name_parts[1] if len(name_parts) > 1 else "")

        role = data.get("role", "alumni")
        status = data.get("status", "active")
        pwd_hash = data.get("password_hash") or "$2b$12$e88e9763f943ec1834f992a4b51e0f24500486803e8bc534e5767af9ea65f6ce"
        now = datetime.now(timezone.utc).isoformat()

        # Insert user
        user_id = Database.insert("""
            INSERT INTO users (email, password_hash, role, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (email_clean, pwd_hash, role, status, now))

        # Insert profile
        Database.insert("""
            INSERT INTO profiles (user_id, first_name, last_name, phone, bio, linkedin_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, first_name, last_name, data.get("phone"), data.get("bio"), data.get("linkedin_url")))

        return cls.find_by_id(user_id)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a plaintext password with PBKDF2-HMAC-SHA256 and a random salt."""
        salt = secrets.token_hex(16)
        iterations = 260000
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations)
        return f"pbkdf2_sha256${iterations}${salt}${dk.hex()}"

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """Verifies a plaintext password against a stored PBKDF2-HMAC-SHA256 hash."""
        try:
            algo, iter_str, salt, expected_hex = stored_hash.split("$", 3)
            if algo != "pbkdf2_sha256":
                return False
            dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), int(iter_str))
            return hmac.compare_digest(dk.hex(), expected_hex)
        except Exception:
            return False

    @staticmethod
    def get_departments() -> List[Dict[str, Any]]:
        """Returns all seeded academic departments for registration forms."""
        return Database.fetch_all(
            "SELECT id, faculty_name, department_name, code FROM departments ORDER BY faculty_name, department_name"
        )

    @classmethod
    def register(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full user registration workflow: validates credentials, role, and subtype details
        (student_details or alumni_details), hashes password, and persists across 3NF tables.
        """
        first_name = str(data.get("first_name") or "").strip()
        last_name = str(data.get("last_name") or "").strip()
        if not first_name or not last_name:
            raise ValueError("Ad ve Soyad alanları zorunludur.")

        email_raw = str(data.get("email") or "").strip().lower()
        if not email_raw or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email_raw):
            raise ValueError("Geçerli bir e-posta adresi giriniz.")
        if cls.find_by_email(email_raw):
            raise ValueError(f"'{email_raw}' e-posta adresi sistemde zaten kayıtlı.")

        password = str(data.get("password") or "")
        password_confirm = data.get("password_confirm")
        if len(password) < 6:
            raise ValueError("Şifre en az 6 karakter uzunluğunda olmalıdır.")
        if password_confirm is not None and password != str(password_confirm):
            raise ValueError("Girilen şifreler birbiriyle eşleşmiyor.")

        role = str(data.get("role") or "student").strip().lower()
        if role not in ("student", "alumni"):
            raise ValueError("Kayıt rolü yalnızca 'student' (Öğrenci) veya 'alumni' (Mezun) olabilir.")

        dept_raw = data.get("department_id")
        try:
            department_id = int(dept_raw) if dept_raw else 1
        except (TypeError, ValueError):
            raise ValueError("Geçerli bir bölüm seçiniz.")

        dept_exists = Database.fetch_one("SELECT id FROM departments WHERE id = ?", (department_id,))
        if not dept_exists:
            raise ValueError("Seçilen bölüm veritabanında bulunamadı.")

        # Validate subtype fields before any DB insert
        student_number = ""
        current_semester = 1
        graduation_year = 2024
        if role == "student":
            student_number = str(data.get("student_number") or "").strip()
            if not student_number:
                raise ValueError("Öğrenci kaydı için Öğrenci Numarası zorunludur.")
            existing_student = Database.fetch_one(
                "SELECT id FROM student_details WHERE student_number = ?", (student_number,)
            )
            if existing_student:
                raise ValueError(f"'{student_number}' öğrenci numarası zaten kayıtlı.")
            try:
                current_semester = int(data.get("current_semester") or 1)
            except (TypeError, ValueError):
                current_semester = 1
            current_semester = max(1, min(12, current_semester))
        else:
            try:
                graduation_year = int(data.get("graduation_year") or 0)
            except (TypeError, ValueError):
                raise ValueError("Mezuniyet yılı geçerli bir sayı olmalıdır.")
            if graduation_year < 1950 or graduation_year > 2030:
                raise ValueError("Mezuniyet yılı 1950 ile 2030 arasında olmalıdır.")

        pwd_hash = cls.hash_password(password)
        now = datetime.now(timezone.utc).isoformat()
        phone = str(data.get("phone") or "").strip() or None
        bio = str(data.get("bio") or "").strip() or None
        linkedin_url = str(data.get("linkedin_url") or "").strip() or None

        user_id = Database.insert("""
            INSERT INTO users (email, password_hash, role, status, created_at)
            VALUES (?, ?, ?, 'active', ?)
        """, (email_raw, pwd_hash, role, now))

        profile_id = Database.insert("""
            INSERT INTO profiles (user_id, first_name, last_name, phone, bio, linkedin_url)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, first_name, last_name, phone, bio, linkedin_url))

        if role == "student":
            Database.insert("""
                INSERT INTO student_details (profile_id, department_id, student_number, current_semester)
                VALUES (?, ?, ?, ?)
            """, (profile_id, department_id, student_number, current_semester))
        else:
            current_company = str(data.get("current_company") or "").strip() or None
            current_title = str(data.get("current_title") or "").strip() or None
            industry = str(data.get("industry") or "").strip() or None
            mentor_val = data.get("is_mentor_available")
            is_mentor = 1 if str(mentor_val).lower() in ("1", "true", "on", "yes") else 0
            Database.insert("""
                INSERT INTO alumni_details (
                    profile_id, department_id, graduation_year,
                    current_company, current_title, industry, is_mentor_available
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (profile_id, department_id, graduation_year, current_company, current_title, industry, is_mentor))

        return cls.find_by_id(user_id)

    @classmethod
    def update(cls, user_id: int, data: Dict[str, Any], partial: bool = False) -> Optional[Dict[str, Any]]:
        """
        [U]pdate: Updates existing user record in the database.
        """
        existing = cls.find_by_id(user_id)
        if not existing:
            return None

        # Check email uniqueness
        if "email" in data and str(data["email"]).strip():
            new_email = str(data["email"]).strip().lower()
            if new_email != existing["email"].lower():
                conflict = cls.find_by_email(new_email)
                if conflict and conflict["id"] != user_id:
                    raise ValueError(f"Email '{new_email}' is already in use by another user")
                Database.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

        if not partial and (not data.get("name") or not data.get("email")):
            raise ValueError("PUT isteğinde name ve email alanları zorunludur")

        # Update name in profiles
        if "name" in data and str(data["name"]).strip():
            parts = str(data["name"]).strip().split(maxsplit=1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ""
            Database.execute("""
                UPDATE profiles SET first_name = ?, last_name = ? WHERE user_id = ?
            """, (first_name, last_name, user_id))

        now = datetime.now(timezone.utc).isoformat()
        Database.execute("UPDATE users SET updated_at = ? WHERE id = ?", (now, user_id))

        return cls.find_by_id(user_id)

    @classmethod
    def delete(cls, user_id: int) -> bool:
        """
        [D]elete: Removes user record from database (cascades to profile).
        """
        existing = cls.find_by_id(user_id)
        if not existing:
            return False
        Database.execute("DELETE FROM users WHERE id = ?", (user_id,))
        return True

    # =========================================================================
    # Relational Navigation Methods
    # =========================================================================

    @classmethod
    def get_job_postings(cls, user_id: int) -> List[Dict[str, Any]]:
        """
        [Relation (1:N)]: Returns all job postings published by this user.
        """
        from models.job_posting import JobPosting
        return JobPosting.find_by_alumni(user_id)

    @classmethod
    def get_announcements(cls, user_id: int) -> List[Dict[str, Any]]:
        """
        [Relation (1:N)]: Returns all announcements published by this user.
        """
        query = "SELECT * FROM announcements WHERE author_id = ? ORDER BY id DESC"
        rows = Database.fetch_all(query, (int(user_id),))
        from models.announcement import Announcement
        return [Announcement._format_row(r) for r in rows if r]

    @classmethod
    def get_profile(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """
        [Relation (1:1)]: Returns the extended profile and academic/career details.
        """
        query = """
            SELECT p.*, a.graduation_year, a.current_company, a.current_title, a.industry, a.is_mentor_available,
                   d.department_name, d.faculty_name
            FROM profiles p
            LEFT JOIN alumni_details a ON p.id = a.profile_id
            LEFT JOIN departments d ON a.department_id = d.id
            WHERE p.user_id = ?
        """
        return Database.fetch_one(query, (int(user_id),))

    @classmethod
    def get_applications(cls, user_id: int) -> List[Dict[str, Any]]:
        """
        [Relation (1:N)]: Returns all job applications submitted by this user.
        """
        from models.job_application import JobApplication
        return JobApplication.find_by_applicant(user_id)
