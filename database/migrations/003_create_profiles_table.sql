-- Migration: 003_create_profiles_table
-- Direction: UP
CREATE TABLE IF NOT EXISTS profiles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(32) NULL,
    avatar_url VARCHAR(512) NULL,
    bio TEXT NULL,
    linkedin_url VARCHAR(512) NULL,
    updated_at TIMESTAMP NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Direction: DOWN
-- DROP TABLE IF EXISTS profiles;
