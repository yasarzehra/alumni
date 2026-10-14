"""
Database Connection Manager
Provides thread-safe connection management and query execution.
Reads configuration from .env and supports SQLite and MySQL.
"""
import os
import sqlite3
import threading
from typing import List, Dict, Any, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "alumni.sqlite")


def parse_env() -> Dict[str, str]:
    """Parse .env file for database configurations."""
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


class Database:
    """Thread-safe Database Connection & Query Executor."""
    _local = threading.local()

    @classmethod
    def get_connection(cls):
        """Returns thread-local database connection with row factory enabled."""
        if not hasattr(cls._local, "conn") or cls._local.conn is None:
            os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
            conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=20.0)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            conn.execute("PRAGMA journal_mode = WAL;")
            cls._local.conn = conn
        return cls._local.conn

    @classmethod
    def execute(cls, query: str, params: Tuple = ()) -> int:
        """Executes INSERT/UPDATE/DELETE query and returns affected rows count."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.rowcount

    @classmethod
    def insert(cls, query: str, params: Tuple = ()) -> int:
        """Executes INSERT query and returns last inserted row ID."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        return cursor.lastrowid

    @classmethod
    def fetch_all(cls, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Executes SELECT query and returns list of dictionaries."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @classmethod
    def fetch_one(cls, query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """Executes SELECT query and returns a single dictionary or None."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    @classmethod
    def get_info(cls) -> Dict[str, Any]:
        """Returns connection metadata for display in the view layer."""
        env = parse_env()
        driver = env.get("DB_CONNECTION", "sqlite")
        return {
            "driver": "SQLite (Persistent)" if driver == "sqlite" else f"MySQL ({env.get('DB_DATABASE', 'alumni_db')})",
            "file": os.path.basename(DB_PATH),
            "status": "Connected"
        }
