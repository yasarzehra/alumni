"""
User Model - MVC Architecture
Backed by Persistent Database Connection (SQLite / MySQL).
Replaces ephemeral in-memory storage with ACID-compliant relational persistence.
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
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
