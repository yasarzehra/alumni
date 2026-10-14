"""
Announcement Model - MVC Architecture
Backed by Persistent Database Connection (SQLite / MySQL).
Replaces ephemeral in-memory storage with ACID-compliant relational persistence.
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from database.connection import Database


class Announcement:
    """
    Announcement Model representing institutional, event, and career announcements.
    Directly connected to the persistent database.
    """

    @staticmethod
    def _format_row(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not row:
            return None
        return {
            "id": row.get("id"),
            "title": row.get("title"),
            "content": row.get("content"),
            "category": row.get("category", "Genel"),
            "author": row.get("author_name") or row.get("author") or "Alumni Koordinatörlüğü",
            "status": row.get("status", "Aktif"),
            "createdAt": row.get("created_at"),
            "updatedAt": row.get("updated_at")
        }

    @classmethod
    def find_all(cls) -> List[Dict[str, Any]]:
        """
        [R]ead: Retrieves all announcements from the database (newest first).
        """
        query = "SELECT * FROM announcements ORDER BY id DESC"
        rows = Database.fetch_all(query)
        return [cls._format_row(r) for r in rows if r]

    @classmethod
    def find_by_id(cls, announcement_id: int) -> Optional[Dict[str, Any]]:
        """
        [R]ead: Retrieves a single announcement record by ID from the database.
        """
        query = "SELECT * FROM announcements WHERE id = ?"
        row = Database.fetch_one(query, (announcement_id,))
        return cls._format_row(row)

    @classmethod
    def create(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        [C]reate: Inserts a new announcement record into the database.
        """
        title = data.get("title")
        content = data.get("content")

        if not title or not str(title).strip():
            raise ValueError("title (başlık) alanı zorunludur")
        if not content or not str(content).strip():
            raise ValueError("content (içerik) alanı zorunludur")

        category = data.get("category", "Genel")
        author = data.get("author") or data.get("author_name") or "Alumni Koordinatörlüğü"
        status = data.get("status", "Aktif")
        now = datetime.now(timezone.utc).isoformat()

        announcement_id = Database.insert("""
            INSERT INTO announcements (title, content, category, author_name, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(title).strip(), str(content).strip(), str(category).strip(), str(author).strip(), str(status).strip(), now))

        return cls.find_by_id(announcement_id)

    @classmethod
    def update(cls, announcement_id: int, data: Dict[str, Any], partial: bool = False) -> Optional[Dict[str, Any]]:
        """
        [U]pdate: Updates an existing announcement record in the database.
        """
        existing = cls.find_by_id(announcement_id)
        if not existing:
            return None

        if not partial:
            if not data.get("title") or not str(data.get("title")).strip():
                raise ValueError("PUT isteğinde title (başlık) zorunludur")
            if not data.get("content") or not str(data.get("content")).strip():
                raise ValueError("PUT isteğinde content (içerik) zorunludur")

        title = str(data.get("title", existing["title"])).strip()
        content = str(data.get("content", existing["content"])).strip()
        category = str(data.get("category", existing["category"])).strip()
        author = str(data.get("author", existing["author"])).strip()
        status = str(data.get("status", existing["status"])).strip()
        now = datetime.now(timezone.utc).isoformat()

        Database.execute("""
            UPDATE announcements
            SET title = ?, content = ?, category = ?, author_name = ?, status = ?, updated_at = ?
            WHERE id = ?
        """, (title, content, category, author, status, now, announcement_id))

        return cls.find_by_id(announcement_id)

    @classmethod
    def delete(cls, announcement_id: int) -> bool:
        """
        [D]elete: Removes an announcement record from the database.
        """
        existing = cls.find_by_id(announcement_id)
        if not existing:
            return False
        Database.execute("DELETE FROM announcements WHERE id = ?", (announcement_id,))
        return True
