"""
Announcement Factory
Generates realistic Announcements across diverse categories.
Persists to both in-memory Announcement Model and SQLite database.
"""
import random
from typing import Dict, Any, Optional
from database.factories.base_factory import BaseFactory
from models.announcement import Announcement


class AnnouncementFactory(BaseFactory):
    """Factory for Announcement entities."""

    TEMPLATES = [
        {
            "category": "Etkinlik",
            "title": "{year} Güz Dönemi Mezunlar Networking Kokteyli",
            "content": "Geleneksel mezunlar networking buluşmamız bu dönem teknoloji ve girişimcilik temasıyla gerçekleştirilecektir. Katılım için kayıt gereklidir.",
            "author": "Alumni Koordinatörlüğü"
        },
        {
            "category": "Kariyer",
            "title": "{company} Mezunlarımıza Özel Yazılım ve Staj İlanları",
            "content": "{company} bünyesinde açılan Junior ve Senior pozisyonlar için alumni platformu üyelerine öncelikli başvuru imkanı sunulmaktadır.",
            "author": "Kariyer Merkezi"
        },
        {
            "category": "Akademik",
            "title": "Büyük Veri & Yapay Zeka Sertifika Programı Başvuruları",
            "content": "Üniversitemiz Sürekli Eğitim Merkezi iş birliğiyle mezunlarımıza %40 indirimli yapay zeka uzmanlık sertifika programı başlatılmıştır.",
            "author": "Mühendislik Dekanlığı"
        },
        {
            "category": "Genel",
            "title": "Alumni Mentorluk Ağı 2026-2027 Dönemi Kayıtları",
            "content": "Öğrencilere kariyer yolculuklarında rehberlik etmek isteyen gönüllü mezun mentorlarımızın başvuruları sistem üzerinden alınmaktadır.",
            "author": "Rektörlük Alumni Ofisi"
        },
        {
            "category": "Etkinlik",
            "title": "Yıllık Alumni Hackathon & İnovasyon Yarışması",
            "content": "48 saatlik maratonda mezun ve mevcut öğrencilerimiz karma takımlar kurarak sürdürülebilirlik çözümleri geliştirecektir. Ödül havuzu 150.000 TL.",
            "author": "Girişimcilik Kulübü"
        },
        {
            "category": "Kariyer",
            "title": "Teknoloji Sektöründe Yurt Dışı Kariyer Deneyimleri Paneli",
            "content": "Avrupa ve Amerika'da çalışan mezunlarımız vize, iş arama ve remote çalışma süreçlerindeki tecrübelerini paylaşacaktır.",
            "author": "Uluslararası İlişkiler Ofisi"
        }
    ]

    @classmethod
    def definition(cls) -> Dict[str, Any]:
        template = random.choice(cls.TEMPLATES)
        company = cls.random_company()
        year = random.choice([2026, 2027])
        title = template["title"].format(company=company, year=year)
        content = template["content"].format(company=company, year=year)

        return {
            "title": title,
            "content": content,
            "category": template["category"],
            "author": template["author"],
            "status": "Aktif"
        }

    @classmethod
    def create(cls, db_conn=None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Creates announcement in in-memory Announcement model and optionally in database."""
        data = cls.make(overrides)

        # 1. Persist to in-memory model repository
        created_item = Announcement.create(data)

        # 2. Persist to SQLite DB if connection provided
        if db_conn:
            cursor = db_conn.cursor()
            cursor.execute("""
                INSERT INTO announcements (title, content, category, author_name, status)
                VALUES (?, ?, ?, ?, ?)
            """, (data["title"], data["content"], data["category"], data["author"], data["status"]))
            db_conn.commit()
            created_item["db_id"] = cursor.lastrowid

        return created_item
