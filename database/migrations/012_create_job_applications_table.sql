-- Migration: 012_create_job_applications_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS job_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER NOT NULL,
    applicant_id INTEGER NOT NULL,
    resume_url VARCHAR(512) NULL,
    cover_letter TEXT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (job_id) REFERENCES job_postings(id) ON DELETE CASCADE,
    FOREIGN KEY (applicant_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (job_id, applicant_id)
);

CREATE INDEX IF NOT EXISTS idx_job_applications_job ON job_applications (job_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_applicant ON job_applications (applicant_id);
CREATE INDEX IF NOT EXISTS idx_job_applications_status_date ON job_applications (status, created_at DESC);

CREATE VIEW IF NOT EXISTS applications AS SELECT * FROM job_applications;

-- Direction: DOWN
DROP VIEW IF EXISTS applications;
DROP TABLE IF EXISTS job_applications;
