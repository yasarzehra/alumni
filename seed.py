#!/usr/bin/env python3
"""
Alumni Platform - Database Seed CLI Runner
Runs Model Factories to populate the database with realistic test datasets.

Usage:
    python seed.py
    python seed.py --users 20 --announcements 10
"""
import sys
import os
import argparse
import sqlite3

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from database.seeders.database_seeder import DatabaseSeeder

DB_PATH = os.path.join(BASE_DIR, "database", "alumni.sqlite")


def main():
    parser = argparse.ArgumentParser(description="Alumni Database Seeder with Model Factories")
    parser.add_argument("--users", type=int, default=12, help="Number of random users to generate (default: 12)")
    parser.add_argument("--announcements", type=int, default=6, help="Number of random announcements to generate (default: 6)")
    parser.add_argument("--events", type=int, default=4, help="Number of random events to generate (default: 4)")
    parser.add_argument("--jobs", type=int, default=5, help="Number of random job postings to generate (default: 5)")
    parser.add_argument("--only-jobs", action="store_true", help="Seed only job postings table without modifying other tables")
    args = parser.parse_args()

    conn = None
    if os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)

    if args.only_jobs:
        from database.seeders.job_posting_seeder import JobPostingSeeder
        JobPostingSeeder.run(count=args.jobs, db_conn=conn)
    else:
        DatabaseSeeder.run(
            db_conn=conn,
            user_count=args.users,
            announcement_count=args.announcements,
            event_count=args.events,
            job_count=args.jobs
        )

    if conn:
        conn.close()


if __name__ == "__main__":
    main()
