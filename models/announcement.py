"""
Announcement Model - MVC Architecture
Encapsulates in-memory CRUD operations for Announcement entities without requiring a database connection.
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any


class Announcement:
    """
    Announcement Model representing institutional, event, and career announcements.
    Maintains an in-memory repository with full CRUD operations.
    """
    _db: List[Dict[str, Any]] = []
    _current_id: int = 1

    def __init__(self, title: str, content: str, category: str = "Genel", author: str = "Alumni Koordinatörlüğü", id: Optional[int] = None, **extra_fields):
        self.id = id
        self.title = title
        self.content = content
        self.category = category
        self.author = author
        self.status = extra_fields.get("status", "Aktif")
        self.created_at = extra_fields.get("createdAt") or datetime.now(timezone.utc).isoformat()
        self.updated_at = extra_fields.get("updatedAt")
        self.extra_fields = extra_fields

    def to_dict(self) -> Dict[str, Any]:
        """Convert Announcement model instance to dictionary representation."""
        data = {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "author": self.author,
            "status": self.status,
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
        [C]reate: Adds a new announcement to the in-memory repository.
        Validates required fields (title, content).
        """
        title = data.get("title")
        content = data.get("content")

        if not title or not str(title).strip():
            raise ValueError("title (başlık) alanı zorunludur")
        if not content or not str(content).strip():
            raise ValueError("content (içerik) alanı zorunludur")

        announcement_id = cls._current_id
        cls._current_id += 1

        now = datetime.now(timezone.utc).isoformat()
        announcement_record = {
            "id": announcement_id,
            "title": str(title).strip(),
            "content": str(content).strip(),
            "category": data.get("category", "Genel").strip() if data.get("category") else "Genel",
            "author": data.get("author", "Alumni Koordinatörlüğü").strip() if data.get("author") else "Alumni Koordinatörlüğü",
            "status": data.get("status", "Aktif"),
            "createdAt": now,
        }

        # Store any additional fields
        for key, val in data.items():
            if key not in announcement_record:
                announcement_record[key] = val

        cls._db.append(announcement_record)
        return dict(announcement_record)

    @classmethod
    def find_all(cls) -> List[Dict[str, Any]]:
        """
        [R]ead: Retrieves all announcements stored in memory (newest first).
        """
        return [dict(a) for a in reversed(cls._db)]

    @classmethod
    def find_by_id(cls, announcement_id: int) -> Optional[Dict[str, Any]]:
        """
        [R]ead: Retrieves a single announcement record by ID.
        """
        item = next((a for a in cls._db if a["id"] == announcement_id), None)
        return dict(item) if item else None

    @classmethod
    def update(cls, announcement_id: int, data: Dict[str, Any], partial: bool = False) -> Optional[Dict[str, Any]]:
        """
        [U]pdate: Updates an existing announcement record.
        - partial=False: Full update (PUT style, title and content required).
        - partial=True: Partial update (PATCH style, updates only provided fields).
        """
        item = next((a for a in cls._db if a["id"] == announcement_id), None)
        if not item:
            return None

        if not partial:
            if not data.get("title") or not str(data.get("title")).strip():
                raise ValueError("PUT isteğinde title (başlık) zorunludur")
            if not data.get("content") or not str(data.get("content")).strip():
                raise ValueError("PUT isteğinde content (içerik) zorunludur")

        # Update allowed fields
        if "title" in data and str(data["title"]).strip():
            item["title"] = str(data["title"]).strip()
        if "content" in data and str(data["content"]).strip():
            item["content"] = str(data["content"]).strip()
        if "category" in data and str(data["category"]).strip():
            item["category"] = str(data["category"]).strip()
        if "author" in data and str(data["author"]).strip():
            item["author"] = str(data["author"]).strip()
        if "status" in data and str(data["status"]).strip():
            item["status"] = str(data["status"]).strip()

        # Update extra fields
        for key, val in data.items():
            if key not in ["id", "createdAt", "updatedAt", "title", "content", "category", "author", "status"]:
                item[key] = val

        item["updatedAt"] = datetime.now(timezone.utc).isoformat()
        return dict(item)

    @classmethod
    def delete(cls, announcement_id: int) -> bool:
        """
        [D]elete: Removes an announcement by its ID.
        Returns True if deleted, False if not found.
        """
        for i, a in enumerate(cls._db):
            if a["id"] == announcement_id:
                cls._db.pop(i)
                return True
        return False

    @classmethod
    def clear_all(cls):
        """Reset repository (useful for tests)."""
        cls._db.clear()
        cls._current_id = 1

    @classmethod
    def seed_defaults(cls):
        """Seed sample announcements if repository is empty."""
        if not cls._db:
            cls.create({
                "title": "2026 Geleneksel Mezunlar Buluşması & Gala",
                "content": "Bu yıl 15. kez düzenlenecek olan Mezunlar Buluşması 25 Ekim 2026 tarihinde ana kampüste gerçekleşecektir. Tüm mezunlarımız ve aileleri davetlidir.",
                "category": "Etkinlik",
                "author": "Rektörlük Alumni Ofisi",
                "status": "Aktif"
            })
            cls.create({
                "title": "Alumni - Öğrenci Mentorluk Başvuruları Başladı",
                "content": "Sektör deneyimi olan mezunlarımız ile kariyerine yön vermek isteyen son sınıf öğrencilerimizi buluşturan 2026-2027 Mentorluk Programı kayıtları açılmıştır.",
                "category": "Kariyer",
                "author": "Kariyer Merkezi",
                "status": "Aktif"
            })
            cls.create({
                "title": "Teknoloji Girişimciliği Webinarı & Panel",
                "content": "Silikon Vadisi ve Avrupa'da girişim kurmuş mezunlarımızın katılacağı panel 18 Kasım Çarşamba 19:00'da online olarak yapılacaktır.",
                "category": "Akademik",
                "author": "Girişimcilik Kulübü",
                "status": "Aktif"
            })
