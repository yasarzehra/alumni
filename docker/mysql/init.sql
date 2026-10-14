-- Alumni Platform Database Initialization Script
-- Conforms to Data Design Documentation (ddd.md)

CREATE DATABASE IF NOT EXISTS alumni_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE alumni_db;

-- 1. Departments
CREATE TABLE IF NOT EXISTS departments (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    faculty_name VARCHAR(150) NOT NULL,
    department_name VARCHAR(150) NOT NULL,
    code VARCHAR(32) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Users (Authentication & Identity)
CREATE TABLE IF NOT EXISTS users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('student', 'alumni', 'coordinator', 'admin') NOT NULL DEFAULT 'student',
    status ENUM('active', 'pending', 'suspended') NOT NULL DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_role_status (role, status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 3. Profiles (Personal details)
CREATE TABLE IF NOT EXISTS profiles (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL UNIQUE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(32) NULL,
    avatar_url VARCHAR(512) NULL,
    bio TEXT NULL,
    linkedin_url VARCHAR(512) NULL,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_profiles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Alumni Details
CREATE TABLE IF NOT EXISTS alumni_details (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    profile_id BIGINT UNSIGNED NOT NULL UNIQUE,
    department_id BIGINT UNSIGNED NOT NULL,
    graduation_year SMALLINT UNSIGNED NOT NULL,
    current_company VARCHAR(191) NULL,
    current_title VARCHAR(191) NULL,
    industry VARCHAR(100) NULL,
    is_mentor_available BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_alumni_profile FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    CONSTRAINT fk_alumni_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT,
    INDEX idx_alumni_search (department_id, graduation_year, industry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 5. Student Details
CREATE TABLE IF NOT EXISTS student_details (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    profile_id BIGINT UNSIGNED NOT NULL UNIQUE,
    department_id BIGINT UNSIGNED NOT NULL,
    student_number VARCHAR(32) NOT NULL UNIQUE,
    current_semester TINYINT UNSIGNED DEFAULT 1,
    gpa DECIMAL(3, 2) NULL,
    CONSTRAINT fk_students_profile FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE,
    CONSTRAINT fk_students_department FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 6. Announcements (Matching Model & Views)
CREATE TABLE IF NOT EXISTS announcements (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    author_id BIGINT UNSIGNED NULL,
    author_name VARCHAR(150) NOT NULL DEFAULT 'Alumni Koordinatörlüğü',
    title VARCHAR(255) NOT NULL,
    content LONGTEXT NOT NULL,
    category ENUM('Genel', 'Etkinlik', 'Kariyer', 'Akademik') NOT NULL DEFAULT 'Genel',
    status ENUM('Aktif', 'Taslak', 'Arsiv') NOT NULL DEFAULT 'Aktif',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_announcements_author FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_announcements_cat_date (status, category, created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 7. Events
CREATE TABLE IF NOT EXISTS events (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    created_by BIGINT UNSIGNED NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT NULL,
    event_date DATETIME NOT NULL,
    location VARCHAR(255) NOT NULL,
    capacity INT UNSIGNED DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_events_creator FOREIGN KEY (created_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 8. Event Attendees
CREATE TABLE IF NOT EXISTS event_attendees (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    event_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    rsvp_status ENUM('attending', 'declined', 'waitlist') NOT NULL DEFAULT 'attending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY uq_event_user (event_id, user_id),
    CONSTRAINT fk_attendees_event FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    CONSTRAINT fk_attendees_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 9. Job Posts
CREATE TABLE IF NOT EXISTS job_posts (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    alumni_id BIGINT UNSIGNED NOT NULL,
    title VARCHAR(255) NOT NULL,
    company_name VARCHAR(191) NOT NULL,
    location VARCHAR(191) NULL,
    employment_type ENUM('full_time', 'part_time', 'internship', 'contract') NOT NULL DEFAULT 'full_time',
    description TEXT NOT NULL,
    application_url VARCHAR(512) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_jobs_alumni FOREIGN KEY (alumni_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 10. Mentorship Requests
CREATE TABLE IF NOT EXISTS mentorship_requests (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    student_id BIGINT UNSIGNED NOT NULL,
    alumni_id BIGINT UNSIGNED NOT NULL,
    message TEXT NOT NULL,
    status ENUM('pending', 'accepted', 'rejected', 'completed') NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_mentorship_student FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    CONSTRAINT fk_mentorship_alumni FOREIGN KEY (alumni_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Initial Seed Data
INSERT INTO departments (faculty_name, department_name, code) VALUES
('Mühendislik Fakültesi', 'Bilgisayar Mühendisliği', 'CENG'),
('Mühendislik Fakültesi', 'Elektrik-Elektronik Mühendisliği', 'EEE'),
('İşletme Fakültesi', 'Yönetim Bilişim Sistemleri', 'MIS')
ON DUPLICATE KEY UPDATE code = code;

INSERT INTO announcements (title, content, category, author_name, status) VALUES
('2026 Geleneksel Mezunlar Buluşması & Gala', 'Bu yıl 15. kez düzenlenecek olan Mezunlar Buluşması ana kampüste gerçekleşecektir.', 'Etkinlik', 'Alumni Ofisi', 'Aktif'),
('Alumni - Öğrenci Mentorluk Başvuruları Başladı', 'Mezunlarımız ile son sınıf öğrencilerimizi buluşturan mentorluk programı açıldı.', 'Kariyer', 'Kariyer Merkezi', 'Aktif'),
('Teknoloji Girişimciliği Webinarı & Panel', 'Girişim kurmuş mezunlarımızın katılacağı online panel 18 Kasım günü yapılacaktır.', 'Akademik', 'Girişimcilik Kulübü', 'Aktif');
