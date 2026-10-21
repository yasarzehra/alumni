-- Migration: 011_create_job_postings_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS job_postings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    alumni_id INTEGER NOT NULL,
    title VARCHAR(255) NOT NULL,
    company_name VARCHAR(191) NOT NULL,
    location VARCHAR(191) NULL,
    employment_type VARCHAR(64) NOT NULL DEFAULT 'full_time',
    experience_level VARCHAR(32) NOT NULL DEFAULT 'entry',
    description TEXT NOT NULL,
    requirements TEXT NULL,
    salary_range VARCHAR(100) NULL,
    application_url VARCHAR(512) NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'active',
    expires_at DATETIME NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (alumni_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_job_postings_alumni ON job_postings (alumni_id);
CREATE INDEX IF NOT EXISTS idx_job_postings_status_date ON job_postings (status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_job_postings_type_location ON job_postings (employment_type, location);

-- Populate from existing job_posts if available
INSERT OR IGNORE INTO job_postings (id, alumni_id, title, company_name, location, employment_type, description, application_url, created_at)
SELECT id, alumni_id, title, company_name, location, employment_type, description, application_url, created_at FROM job_posts;

-- Direction: DOWN
DROP TABLE IF EXISTS job_postings;
