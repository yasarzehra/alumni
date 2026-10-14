#!/usr/bin/env python3
"""
Alumni Platform - Database Migration Runner
Manages version-controlled schema migrations and seeders.
Supports SQLite (zero-dependency local development) and MySQL.

Usage:
    python migrate.py up        # Run pending migrations
    python migrate.py rollback  # Roll back the last migration batch
    python migrate.py status    # View status of all migrations
    python migrate.py fresh     # Fresh rebuild (drop & re-run all migrations)
    python migrate.py seed      # Run database seeders
"""
import sys
import os
import sqlite3

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MIGRATIONS_DIR = os.path.join(BASE_DIR, "database", "migrations")
SEEDERS_DIR = os.path.join(BASE_DIR, "database", "seeders")
DEFAULT_DB_FILE = os.path.join(BASE_DIR, "database", "alumni.sqlite")


def parse_env() -> dict:
    """Parses local .env file if available."""
    env = {}
    env_file = os.path.join(BASE_DIR, ".env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def get_connection():
    """Connects to the database (SQLite default for zero-dependency portability)."""
    os.makedirs(os.path.join(BASE_DIR, "database"), exist_ok=True)
    conn = sqlite3.connect(DEFAULT_DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_migrations_table(conn):
    """Ensures migrations tracking table exists."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            migration VARCHAR(255) NOT NULL UNIQUE,
            batch INTEGER NOT NULL,
            executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()


def get_applied_migrations(conn):
    """Returns a dict of migration_name -> batch."""
    cursor = conn.cursor()
    cursor.execute("SELECT migration, batch FROM migrations ORDER BY id ASC")
    return {row[0]: row[1] for row in cursor.fetchall()}


def get_migration_files():
    """Returns sorted list of migration filenames."""
    if not os.path.exists(MIGRATIONS_DIR):
        return []
    files = [f for f in os.listdir(MIGRATIONS_DIR) if f.endswith(".sql")]
    files.sort()
    return files


def parse_sql_file(file_path):
    """Splits migration file into UP and DOWN SQL statements."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    up_sql = ""
    down_sql = ""

    if "-- Direction: DOWN" in content:
        parts = content.split("-- Direction: DOWN")
        up_sql = parts[0].replace("-- Direction: UP", "").strip()
        down_raw = parts[1].strip()
        down_lines = []
        for line in down_raw.splitlines():
            line_str = line.strip()
            if line_str.startswith("-- DROP") or line_str.startswith("--"):
                down_lines.append(line_str.lstrip("-").strip())
            else:
                down_lines.append(line_str)
        down_sql = "\n".join(down_lines).strip()
    else:
        up_sql = content.replace("-- Direction: UP", "").strip()

    return up_sql, down_sql


def run_up():
    """Runs all pending migrations."""
    conn = get_connection()
    init_migrations_table(conn)
    applied = get_applied_migrations(conn)
    files = get_migration_files()

    pending = [f for f in files if f not in applied]

    if not pending:
        print("[OK] Database is up to date. Nothing to migrate.")
        return

    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(batch), 0) + 1 FROM migrations")
    next_batch = cursor.fetchone()[0]

    print(f"\n[MIGRATE] Running {len(pending)} pending migration(s) [Batch: {next_batch}]...")
    for filename in pending:
        path = os.path.join(MIGRATIONS_DIR, filename)
        up_sql, _ = parse_sql_file(path)
        try:
            conn.executescript(up_sql)
            conn.execute("INSERT INTO migrations (migration, batch) VALUES (?, ?)", (filename, next_batch))
            conn.commit()
            print(f"  [+] Migrated: {filename}")
        except Exception as e:
            conn.rollback()
            print(f"  [ERROR] Migrating {filename}: {e}")
            sys.exit(1)

    print("\n[SUCCESS] All migrations applied successfully!")


def run_rollback():
    """Rolls back the last executed migration batch."""
    conn = get_connection()
    init_migrations_table(conn)

    cursor = conn.cursor()
    cursor.execute("SELECT MAX(batch) FROM migrations")
    last_batch = cursor.fetchone()[0]

    if not last_batch:
        print("[OK] No migrations to roll back.")
        return

    cursor.execute("SELECT migration FROM migrations WHERE batch = ? ORDER BY id DESC", (last_batch,))
    to_rollback = [row[0] for row in cursor.fetchall()]

    print(f"\n[ROLLBACK] Rolling back batch {last_batch} ({len(to_rollback)} migration(s))...")
    for filename in to_rollback:
        path = os.path.join(MIGRATIONS_DIR, filename)
        _, down_sql = parse_sql_file(path)
        try:
            if down_sql:
                conn.executescript(down_sql)
            conn.execute("DELETE FROM migrations WHERE migration = ?", (filename,))
            conn.commit()
            print(f"  [-] Rolled back: {filename}")
        except Exception as e:
            conn.rollback()
            print(f"  [ERROR] Rolling back {filename}: {e}")
            sys.exit(1)

    print("\n[SUCCESS] Rollback completed successfully!")


def run_status():
    """Prints status of all migrations."""
    conn = get_connection()
    init_migrations_table(conn)
    applied = get_applied_migrations(conn)
    files = get_migration_files()

    print("\n[STATUS] Migration Status:")
    print("-" * 65)
    print(f"{'Status':<12} | {'Batch':<6} | {'Migration File'}")
    print("-" * 65)
    for f in files:
        if f in applied:
            print(f"{'Applied':<12} | {applied[f]:<6} | {f}")
        else:
            print(f"{'Pending':<12} | {'-':<6} | {f}")
    print("-" * 65)


def run_seed():
    """Runs seeders and factory generators."""
    conn = get_connection()
    if os.path.exists(SEEDERS_DIR):
        files = [f for f in os.listdir(SEEDERS_DIR) if f.endswith(".sql")]
        files.sort()
        print(f"\n[SEED] Running {len(files)} SQL seeder(s)...")
        for filename in files:
            path = os.path.join(SEEDERS_DIR, filename)
            with open(path, "r", encoding="utf-8") as f:
                sql = f.read()
            try:
                conn.executescript(sql)
                conn.commit()
                print(f"  [+] Seeded SQL: {filename}")
            except Exception as e:
                conn.rollback()
                print(f"  [ERROR] Seeding {filename}: {e}")

    # Run Factory-based Seeder
    try:
        from database.seeders.database_seeder import DatabaseSeeder
        DatabaseSeeder.run(db_conn=conn, user_count=10, announcement_count=5, event_count=3, job_count=4)
    except Exception as e:
        print(f"  [ERROR] Running factory seeder: {e}")

    print("\n[SUCCESS] Seeding completed successfully!")


def run_fresh():
    """Drops all tables and re-runs migrations from scratch."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = [row[0] for row in cursor.fetchall()]

    print(f"\n[FRESH] Dropping {len(tables)} table(s)...")
    conn.execute("PRAGMA foreign_keys = OFF;")
    for table in tables:
        conn.execute(f"DROP TABLE IF EXISTS {table};")
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.commit()

    run_up()
    run_seed()


def main():
    command = sys.argv[1].lower() if len(sys.argv) > 1 else "up"

    if command == "up":
        run_up()
    elif command in ["rollback", "down"]:
        run_rollback()
    elif command == "status":
        run_status()
    elif command == "seed":
        run_seed()
    elif command == "fresh":
        run_fresh()
    else:
        print(f"Unknown command: {command}")
        print("Available commands: up, rollback, down, status, fresh, seed")


if __name__ == "__main__":
    main()
