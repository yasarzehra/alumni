"""
Event & JobPost Factories
Generates realistic Events and Job Postings for alumni ecosystem.
"""
import random
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional
from database.factories.base_factory import BaseFactory


class EventFactory(BaseFactory):
    """Factory for Event entities."""

    EVENT_TITLES = [
        "2026 Geleneksel Mezunlar Galası",
        "Kariyer ve Yetenek Zirvesi",
        "Teknoloji Liderleri Paneli",
        "Girişimcilik ve Yatırımcı Buluşması",
        "Alumni Basketbol Turnuvası & Barbekü",
        "Yapay Zeka ve Gelecek Çalıştayı"
    ]

    @classmethod
    def definition(cls) -> Dict[str, Any]:
        title = random.choice(cls.EVENT_TITLES)
        days_ahead = random.randint(5, 60)
        event_time = datetime.now(timezone.utc) + timedelta(days=days_ahead)

        return {
            "title": title,
            "description": f"{title} ana kampüs kültür merkezinde gerçekleştirilecektir. Tüm mezunlarımız davetlidir.",
            "event_date": event_time.isoformat(),
            "location": f"Ana Kampüs, {cls.random_city()}",
            "capacity": random.choice([50, 100, 250, 500])
        }

    @classmethod
    def create(cls, db_conn=None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = cls.make(overrides)
        if db_conn:
            cursor = db_conn.cursor()
            cursor.execute("""
                INSERT INTO events (title, description, event_date, location, capacity)
                VALUES (?, ?, ?, ?, ?)
            """, (data["title"], data["description"], data["event_date"], data["location"], data["capacity"]))
            db_conn.commit()
            data["id"] = cursor.lastrowid
        return data


class JobPostFactory(BaseFactory):
    """Factory for JobPost entities."""

    @classmethod
    def definition(cls) -> Dict[str, Any]:
        company = cls.random_company()
        title = cls.random_title()
        return {
            "title": title,
            "company_name": company,
            "location": f"{cls.random_city()} (Hybrid / Remote)",
            "employment_type": random.choice(["full_time", "full_time", "internship", "part_time"]),
            "description": f"{company} ekibimizde {title} olarak aramıza katılacak mezun takım arkadaşları arıyoruz. Modern teknolojiler ve esnek çalışma imkanı.",
            "application_url": f"https://careers.{company.lower().replace(' ', '')}.com/apply"
        }

    @classmethod
    def create(cls, db_conn=None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = cls.make(overrides)
        if db_conn:
            cursor = db_conn.cursor()
            cursor.execute("""
                INSERT INTO job_posts (alumni_id, title, company_name, location, employment_type, description, application_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (1, data["title"], data["company_name"], data["location"], data["employment_type"], data["description"], data["application_url"]))
            db_conn.commit()
            data["id"] = cursor.lastrowid
        return data
