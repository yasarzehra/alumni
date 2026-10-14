-- Migration: 007_create_events_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by INTEGER NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    event_date TIMESTAMP NOT NULL,
    location VARCHAR(255) NOT NULL,
    capacity INTEGER DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
);

-- Direction: DOWN
-- DROP TABLE IF EXISTS events;
