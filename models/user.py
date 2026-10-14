"""
User Model - MVC Architecture
Encapsulates in-memory CRUD operations for User entities without requiring a database connection.
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any


class User:
    """
    User Model representing the User entity.
    Maintains an in-memory repository with full CRUD operations.
    """
    _db: List[Dict[str, Any]] = []
    _current_id: int = 1

    def __init__(self, name: str, email: str, id: Optional[int] = None, **extra_fields):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = extra_fields.get("createdAt") or datetime.now(timezone.utc).isoformat()
        self.updated_at = extra_fields.get("updatedAt")
        self.extra_fields = extra_fields

    def to_dict(self) -> Dict[str, Any]:
        """Convert the User model instance to a dictionary representation."""
        data = {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "createdAt": self.created_at,
        }
        if self.updated_at:
            data["updatedAt"] = self.updated_at
        for k, v in self.extra_fields.items():
            if k not in data:
                data[k] = v
        return data

    # =========================================================================
    # CRUD Operations (In-Memory, No Database Connection Required)
    # =========================================================================

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [C]reate: Adds a new user to the in-memory repository.
        Validates required fields and checks for unique email constraints.
        """
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            raise ValueError("name and email fields are required")

        if cls.find_by_email(email):
            raise ValueError(f"Email '{email}' is already registered")

        user_id = cls._current_id
        cls._current_id += 1

        now = datetime.now(timezone.utc).isoformat()
        user_record = {
            "id": user_id,
            "name": name,
            "email": email,
            "createdAt": now,
        }

        # Store any additional fields (e.g. password, role)
        for key, val in data.items():
            if key not in user_record:
                user_record[key] = val

        cls._db.append(user_record)
        return dict(user_record)

    @classmethod
    def find_all(cls) -> List[Dict[str, Any]]:
        """
        [R]ead: Retrieves all users stored in memory.
        """
        return [dict(u) for u in cls._db]

    @classmethod
    def find_by_id(cls, user_id: int) -> Optional[Dict[str, Any]]:
        """
        [R]ead: Retrieves a single user record by its unique identifier.
        """
        user = next((u for u in cls._db if u["id"] == user_id), None)
        return dict(user) if user else None

    @classmethod
    def find_by_email(cls, email: str) -> Optional[Dict[str, Any]]:
        """
        [R]ead: Retrieves a user record by email (case-insensitive).
        """
        user = next((u for u in cls._db if u.get("email", "").lower() == email.lower()), None)
        return dict(user) if user else None

    @classmethod
    def update(cls, user_id: int, data: Dict[str, Any], partial: bool = False) -> Optional[Dict[str, Any]]:
        """
        [U]pdate: Updates an existing user record.
        - partial=False: Full update (PUT style, requires name and email).
        - partial=True: Partial update (PATCH style, updates only provided fields).
        """
        user = next((u for u in cls._db if u["id"] == user_id), None)
        if not user:
            return None

        # Check for unique email conflict
        if "email" in data:
            new_email = data["email"]
            if new_email.lower() != user["email"].lower():
                conflict = cls.find_by_email(new_email)
                if conflict and conflict["id"] != user_id:
                    raise ValueError(f"Email '{new_email}' is already in use by another user")

        if not partial:
            # Full update (PUT)
            name = data.get("name")
            email = data.get("email")
            if not name or not email:
                raise ValueError("name and email fields are required for a full update")
            user["name"] = name
            user["email"] = email
        else:
            # Partial update (PATCH)
            if "name" in data:
                user["name"] = data["name"]
            if "email" in data:
                user["email"] = data["email"]

        # Update any other custom fields provided
        for key, val in data.items():
            if key not in ("id", "createdAt"):
                user[key] = val

        user["updatedAt"] = datetime.now(timezone.utc).isoformat()
        return dict(user)

    @classmethod
    def delete(cls, user_id: int) -> bool:
        """
        [D]elete: Removes a user from the in-memory repository by ID.
        Returns True if deleted, False if user does not exist.
        """
        initial_count = len(cls._db)
        cls._db = [u for u in cls._db if u["id"] != user_id]
        return len(cls._db) < initial_count

    @classmethod
    def clear(cls):
        """Helper method to reset the in-memory database (useful for testing)."""
        cls._db = []
        cls._current_id = 1
