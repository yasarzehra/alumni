-- Migration: 001_create_departments_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_name VARCHAR(150) NOT NULL,
    department_name VARCHAR(150) NOT NULL,
    code VARCHAR(32) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Direction: DOWN
-- DROP TABLE IF EXISTS departments;
