-- Seeder: 001_initial_seed.sql
-- Seeds departments, default users, and initial announcements

INSERT INTO departments (faculty_name, department_name, code) VALUES
('Mühendislik Fakültesi', 'Bilgisayar Mühendisliği', 'CENG'),
('Mühendislik Fakültesi', 'Elektrik-Elektronik Mühendisliği', 'EEE'),
('İşletme Fakültesi', 'Yönetim Bilişim Sistemleri', 'MIS');

INSERT INTO users (email, password_hash, role, status) VALUES
('zehra@example.com', '$2b$12$e88e9763f943ec1834f992a4b51e0f24500486803e8bc534e5767af9ea65f6ce', 'admin', 'active'),
('alican@example.com', '$2b$12$e88e9763f943ec1834f992a4b51e0f24500486803e8bc534e5767af9ea65f6ce', 'alumni', 'active');

INSERT INTO profiles (user_id, first_name, last_name, bio) VALUES
(1, 'Zehra', 'Yaşar', 'Alumni Platform Administrator & Lead Developer'),
(2, 'Ali', 'Can', 'Senior Software Engineer & Mentor');

INSERT INTO announcements (title, content, category, author_name, status) VALUES
('2026 Geleneksel Mezunlar Buluşması & Gala', 'Bu yıl 15. kez düzenlenecek olan Mezunlar Buluşması ana kampüste gerçekleşecektir.', 'Etkinlik', 'Alumni Ofisi', 'Aktif'),
('Alumni - Öğrenci Mentorluk Başvuruları Başladı', 'Mezunlarımız ile son sınıf öğrencilerimizi buluşturan mentorluk programı açıldı.', 'Kariyer', 'Kariyer Merkezi', 'Aktif'),
('Teknoloji Girişimciliği Webinarı & Panel', 'Girişim kurmuş mezunlarımızın katılacağı online panel 18 Kasım günü yapılacaktır.', 'Akademik', 'Girişimcilik Kulübü', 'Aktif');
