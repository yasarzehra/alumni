-- Migration: 005_create_student_details_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS student_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    student_number VARCHAR(32) NOT NULL UNIQUE,
    current_semester INTEGER DEFAULT 1,
    gpa REAL NULL,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
);

-- Direction: DOWN
-- DROP TABLE IF EXISTS student_details;
