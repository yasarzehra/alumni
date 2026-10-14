"""
User Factory
Generates realistic User, Profile, and academic/career attributes.
Can persist to both in-memory User Model and SQLite database.
"""
import random
from typing import Dict, Any, Optional
from database.factories.base_factory import BaseFactory
from models.user import User


class UserFactory(BaseFactory):
    """Factory for User entities."""

    ROLES = ["student", "alumni", "alumni", "alumni", "coordinator"]
    STATUSES = ["active", "active", "active", "pending"]

    @classmethod
    def definition(cls) -> Dict[str, Any]:
        first = cls.random_first_name()
        last = cls.random_last_name()
        role = random.choice(cls.ROLES)
        return {
            "first_name": first,
            "last_name": last,
            "name": f"{first} {last}",
            "email": cls.random_email(first, last),
            "password_hash": "$2b$12$e88e9763f943ec1834f992a4b51e0f24500486803e8bc534e5767af9ea65f6ce",
            "role": role,
            "status": random.choice(cls.STATUSES),
            "phone": f"+90 5{random.randint(30, 59)} {random.randint(100, 999)} {random.randint(10, 99)} {random.randint(10, 99)}",
            "company": cls.random_company(),
            "title": cls.random_title(),
            "graduation_year": random.randint(2012, 2025) if role == "alumni" else None,
            "bio": f"{first} {last}, alumni platformu aktif üyesidir. Kariyer ve teknoloji alanlarında mentorluk sağlamaktadır.",
            "linkedin_url": f"https://linkedin.com/in/{first.lower()}-{last.lower()}-{random.randint(100, 999)}"
        }

    @classmethod
    def create(cls, db_conn=None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Creates user in in-memory User model and optionally in database."""
        data = cls.make(overrides)

        # 1. Persist to in-memory model repository
        created_user = User.create({
            "name": data["name"],
            "email": data["email"],
            "role": data.get("role", "alumni"),
            "status": data.get("status", "active"),
            "company": data.get("company"),
            "title": data.get("title"),
        })

        # 2. Persist to SQLite DB if connection provided
        if db_conn:
            cursor = db_conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO users (email, password_hash, role, status)
                VALUES (?, ?, ?, ?)
            """, (data["email"], data["password_hash"], data["role"], data["status"]))
            user_id = cursor.lastrowid
            if user_id:
                cursor.execute("""
                    INSERT OR IGNORE INTO profiles (user_id, first_name, last_name, phone, bio, linkedin_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, data["first_name"], data["last_name"], data.get("phone"), data.get("bio"), data.get("linkedin_url")))
                profile_id = cursor.lastrowid

                if data.get("role") == "alumni":
                    cursor.execute("""
                        INSERT OR IGNORE INTO alumni_details (profile_id, department_id, graduation_year, current_company, current_title, industry, is_mentor_available)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (profile_id, random.randint(1, 3), data.get("graduation_year", 2020), data.get("company"), data.get("title"), "Teknoloji", 1))
                db_conn.commit()
                created_user["db_id"] = user_id

        return created_user
