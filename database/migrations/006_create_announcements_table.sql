-- Migration: 006_create_announcements_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NULL,
    author_name VARCHAR(150) NOT NULL DEFAULT 'Alumni Koordinatörlüğü',
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    category VARCHAR(64) NOT NULL DEFAULT 'Genel',
    status VARCHAR(32) NOT NULL DEFAULT 'Aktif',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL
);
CREATE INDEX IF NOT EXISTS idx_announcements_status_cat ON announcements(status, category);

-- Direction: DOWN
-- DROP TABLE IF EXISTS announcements;
