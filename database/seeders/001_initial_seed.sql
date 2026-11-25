-- Seeder: 001_initial_seed.sql
-- Seeds departments, default users, and initial announcements

INSERT OR IGNORE INTO departments (faculty_name, department_name, code) VALUES
('Mühendislik Fakültesi', 'Bilgisayar Mühendisliği', 'CENG'),
('Mühendislik Fakültesi', 'Elektrik-Elektronik Mühendisliği', 'EEE'),
('Mühendislik Fakültesi', 'Endüstri Mühendisliği', 'IE'),
('İşletme Fakültesi', 'Yönetim Bilişim Sistemleri', 'MIS'),
('İşletme Fakültesi', 'İşletme', 'BUS'),
('Bilgisayar ve Bilişim Teknolojileri Fakültesi', 'Bilgisayar Bilimleri', 'CS'),
('Bilgisayar ve Bilişim Teknolojileri Fakültesi', 'Yapay Zeka ve Veri Mühendisliği', 'AIDE'),
('Bilgisayar ve Bilişim Teknolojileri Fakültesi', 'Siber Güvenlik Mühendisliği', 'CYBER'),
('Hukuk Fakültesi', 'Hukuk', 'LAW'),
('İstanbul Tıp Fakültesi', 'Tıp', 'MED'),
('Diş Hekimliği Fakültesi', 'Diş Hekimliği', 'DENT'),
('Eczacılık Fakültesi', 'Eczacılık', 'PHARM'),
('İktisat Fakültesi', 'İktisat', 'ECON'),
('İktisat Fakültesi', 'Ekonometri', 'ECM'),
('İktisat Fakültesi', 'Maliye', 'FIN'),
('İktisat Fakültesi', 'Çalışma Ekonomisi ve Endüstri İlişkileri', 'CEKO'),
('Siyasal Bilgiler Fakültesi', 'Siyaset Bilimi ve Uluslararası İlişkiler', 'PSIR'),
('Siyasal Bilgiler Fakültesi', 'Siyaset Bilimi ve Kamu Yönetimi', 'PUBA'),
('Siyasal Bilgiler Fakültesi', 'İşletme (Siyasal)', 'SBF-BUS'),
('Edebiyat Fakültesi', 'Psikoloji', 'PSY'),
('Edebiyat Fakültesi', 'Türk Dili ve Edebiyatı', 'TLL'),
('Edebiyat Fakültesi', 'Tarih', 'HIST'),
('Edebiyat Fakültesi', 'İngiliz Dili ve Edebiyatı', 'ELL'),
('Edebiyat Fakültesi', 'Sosyoloji', 'SOC'),
('Fen Fakültesi', 'Matematik', 'MATH'),
('Fen Fakültesi', 'Fizik', 'PHYS'),
('Fen Fakültesi', 'Moleküler Biyoloji ve Genetik', 'MBG'),
('İletişim Fakültesi', 'Gazetecilik', 'JOUR'),
('İletişim Fakültesi', 'Halkla İlişkiler ve Tanıtım', 'PR'),
('İletişim Fakültesi', 'Radyo, Televizyon ve Sinema', 'RTS'),
('Mimarlık Fakültesi', 'Mimarlık', 'ARCH');

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
