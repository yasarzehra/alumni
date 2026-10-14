-- Migration: 004_create_alumni_details_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS alumni_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    graduation_year INTEGER NOT NULL,
    current_company VARCHAR(191) NULL,
    current_title VARCHAR(191) NULL,
    industry VARCHAR(100) NULL,
    is_mentor_available BOOLEAN DEFAULT 0,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
);
CREATE INDEX IF NOT EXISTS idx_alumni_dept_year ON alumni_details(department_id, graduation_year);

-- Direction: DOWN
-- DROP TABLE IF EXISTS alumni_details;
