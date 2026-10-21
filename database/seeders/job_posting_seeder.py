"""
JobPostingSeeder - Dedicated Seeder for Job Postings Table
Seeds the database with realistic tech career opportunities and internships.
"""
import sys
import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)

from database.factories.job_posting_factory import JobPostingFactory

DEFAULT_DB_FILE = os.path.join(BASE_DIR, "database", "alumni.sqlite")


class JobPostingSeeder:
    """Seeder dedicated to populating job_postings."""

    @classmethod
    def run(cls, count: int = 8, db_conn=None):
        should_close = False
        if not db_conn:
            db_conn = sqlite3.connect(DEFAULT_DB_FILE)
            should_close = True

        print(f"\n[JOB SEEDER] Generating {count} realistic Job Postings via JobPostingFactory...")
        jobs = JobPostingFactory.create_batch(count=count, db_conn=db_conn)
        for j in jobs:
            print(f"  [+] #{j['id']} [{j['experience_level'].upper()}] {j['title']} @ {j['company_name']} ({j['location']}) - {j['salary_range']}")

        print(f"[SUCCESS] {len(jobs)} Job Postings seeded successfully!\n")

        if should_close:
            db_conn.close()


if __name__ == "__main__":
    count = 8
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        count = int(sys.argv[1])
    JobPostingSeeder.run(count=count)
