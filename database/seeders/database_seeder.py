"""
DatabaseSeeder - Master Seeder
Coordinates all model factories to populate a rich, realistic test environment.
Populates both SQLite persistent database and in-memory repositories.
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from database.factories.user_factory import UserFactory
from database.factories.announcement_factory import AnnouncementFactory
from database.factories.event_factory import EventFactory
from database.factories.job_posting_factory import JobPostingFactory, JobPostFactory
from models.user import User
from models.announcement import Announcement


class DatabaseSeeder:
    """Master Database Seeder."""

    @classmethod
    def run(cls, db_conn=None, user_count: int = 12, announcement_count: int = 6, event_count: int = 4, job_count: int = 5):
        """Executes seeding workflow using factories."""
        print("\n========================================================")
        print("SEEDING ALUMNI PLATFORM DATABASE WITH FACTORIES")
        print("========================================================")

        cursor = db_conn.cursor() if db_conn else None

        # 1. Seed Core Admin & Demo Accounts
        print("\n[1/5] Checking and Seeding Core Accounts...")
        admin_exists = False
        if cursor:
            cursor.execute("SELECT id FROM users WHERE email = 'zehra@example.com'")
            admin_exists = bool(cursor.fetchone())
        else:
            admin_exists = bool(User.find_by_email("zehra@example.com"))

        if not admin_exists:
            admin = UserFactory.create(db_conn, {
                "first_name": "Zehra",
                "last_name": "Yaşar",
                "name": "Zehra Yaşar",
                "email": "zehra@example.com",
                "role": "admin",
                "status": "active",
                "company": "Alumni Platform",
                "title": "Lead Platform Architect"
            })
            print(f"  [+] Admin seeded: {admin['name']} <{admin['email']}>")
        else:
            print("  [*] Admin already exists: Zehra Yaşar <zehra@example.com>")

        demo_exists = False
        if cursor:
            cursor.execute("SELECT id FROM users WHERE email = 'alican@example.com'")
            demo_exists = bool(cursor.fetchone())
        else:
            demo_exists = bool(User.find_by_email("alican@example.com"))

        if not demo_exists:
            demo_alumni = UserFactory.create(db_conn, {
                "first_name": "Ali",
                "last_name": "Can",
                "name": "Ali Can",
                "email": "alican@example.com",
                "role": "alumni",
                "status": "active",
                "company": "Trendyol",
                "title": "Senior Backend Engineer",
                "graduation_year": 2019
            })
            print(f"  [+] Demo Alumni seeded: {demo_alumni['name']} <{demo_alumni['email']}>")
        else:
            print("  [*] Demo Alumni already exists: Ali Can <alican@example.com>")

        # 2. Generate Users via UserFactory
        print(f"\n[2/5] Generating {user_count} Users via UserFactory...")
        users = UserFactory.create_batch(count=user_count, db_conn=db_conn)
        for u in users[:4]:
            print(f"  [+] User created: {u['name']} ({u.get('role', 'user')}) <{u['email']}>")
        if len(users) > 4:
            print(f"  ... ve {len(users) - 4} kullanıcı daha başarıyla üretildi.")

        # 3. Generate Announcements via AnnouncementFactory
        print(f"\n[3/5] Generating {announcement_count} Announcements via AnnouncementFactory...")
        announcements = AnnouncementFactory.create_batch(count=announcement_count, db_conn=db_conn)
        for a in announcements[:3]:
            print(f"  [+] Announcement created: [{a.get('category')}] {a.get('title')}")
        if len(announcements) > 3:
            print(f"  ... ve {len(announcements) - 3} duyuru daha başarıyla üretildi.")

        # 4. Generate Events via EventFactory
        print(f"\n[4/5] Generating {event_count} Events via EventFactory...")
        events = EventFactory.create_batch(count=event_count, db_conn=db_conn)
        for e in events:
            print(f"  [+] Event created: {e['title']} ({e['location']})")

        # 5. Generate Job Postings via JobPostingFactory
        print(f"\n[5/5] Generating {job_count} Job Postings via JobPostingFactory...")
        jobs = JobPostingFactory.create_batch(count=job_count, db_conn=db_conn)
        for j in jobs:
            level = j.get('experience_level', 'mid').upper()
            salary = j.get('salary_range') or 'Maaş Belirtilmedi'
            print(f"  [+] Job created: [{level}] {j['title']} @ {j['company_name']} ({salary})")

        print("\n========================================================")
        print("[SUCCESS] DATABASE SEEDING COMPLETED SUCCESSFULLY!")
        print("========================================================\n")
