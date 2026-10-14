-- Migration: 010_create_mentorship_requests_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS mentorship_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    alumni_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (alumni_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Direction: DOWN
-- DROP TABLE IF EXISTS mentorship_requests;
