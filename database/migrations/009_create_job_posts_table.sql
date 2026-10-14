-- Migration: 009_create_job_posts_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS job_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumni_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    company_name VARCHAR(191) NOT NULL,
    location VARCHAR(191) NULL,
    employment_type VARCHAR(64) NOT NULL DEFAULT 'full_time',
    description TEXT NOT NULL,
    application_url VARCHAR(512) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alumni_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Direction: DOWN
-- DROP TABLE IF EXISTS job_posts;
