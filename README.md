# Alumni Management & Networking Platform

An enterprise-grade, containerized web application built to connect, track, and empower university alumni, current students, and faculty administration.

---

## 📌 1. Project Overview & Mission

The **Alumni Platform** bridges the communication and professional gap between university graduates and ongoing students. Over time, universities struggle to track where alumni build their careers, while current students lack direct mentorship pathways.

This platform solves this by offering a centralized directory, career tracking, verification pipelines, and event networking—designed from the ground up for high reliability, modular scalability, and modern web standards.

### Key Capabilities
- **Verified Alumni Profiles:** Comprehensive user profiles recording graduation year, faculty, department, current enterprise, LinkedIn integration, and industry domain.
- **Student-to-Alumni Mentorship Network:** Direct communication and appointment channels enabling undergraduates to seek career guidance.
- **Job & Internship Board:** Exclusive job openings posted directly by alumni companies for university talent.
- **Event & Reunion Management:** Registration, ticketing, and scheduling for faculty webinars, conferences, and reunions.
- **Role-Based Access Control (RBAC):** Distinct authentication flows and permission sets for Students, Verified Alumni, Department Coordinators, and System Administrators.

---

## 🛠️ 2. Architectural Choices & Technical Decisions

### Backend: PHP
- **Why Chosen:**
  - **Native Web Foundation:** PHP is engineered explicitly for the web request-response lifecycle, eliminating heavy runtime overhead for standard API and server-rendered workflows.
  - **Ecosystem & Speed to Delivery:** Robust package ecosystem (via Composer) provides production-ready libraries for authentication, ORM/DB abstraction, and routing without rebuilding boilerplate.
  - **Maintainability & Typing:** Modern PHP (8.x+) introduces strict typing, attributes, union types, and JIT compilation, drastically elevating type-safety and developer ergonomics.
- **Weakness / Architectural Trade-off:**
  - **Concurrency Limitations:** PHP operates on a shared-nothing, single-threaded execution model per request. Running long-polling, background workers, or real-time WebSockets requires external event loops (e.g., Swoole, RoadRunner) or task queues (Redis/Worker).
  - **Design Hygiene:** Its forgiving legacy syntax makes codebases vulnerable to spaghetti patterns if strict architectural patterns (such as MVC/clean architecture) are not rigorously enforced.

### Database: MySQL
- **Why Chosen:**
  - **Relational Integrity (ACID):** Alumni, departments, graduation cohorts, mentorship requests, and security logs are inherently relational. MySQL provides strict foreign key constraints and transactional integrity.
  - **Native Synergy with PHP:** PDO and MySQL drivers offer mature, zero-configuration connection pooling and query optimization.
  - **Reliable Indexing:** B-Tree and Composite indexing ensure microsecond lookup times for complex filters (e.g., filtering alumni by `faculty_id`, `graduation_year`, and `city`).
- **Weakness / Architectural Trade-off:**
  - **Analytical Query Overhead:** Lacks the rich out-of-the-box analytical indexing, window function flexibility, and specialized JSON operations available in PostgreSQL.
  - **Scaling Bottlenecks:** Horizontal scaling (sharding) is non-trivial compared to NoSQL alternatives and requires third-party orchestration tools at massive scale.

### AI Assistant: Antigravity
- **Role in Engineering:**
  - Generating boilerplates for MVC routing controllers and database migrations.
  - Assisting in automated unit/integration test generation.
  - Refactoring raw SQL into parameterized, injection-safe prepared statements.
  - Maintaining up-to-date API and deployment documentation.

---

## 🗄️ 3. Proposed Database Schema (Core Tables)

```text
users (id, email, password_hash, role, status, created_at)
  └── profiles (id, user_id, first_name, last_name, bio, avatar_url)
        ├── alumni_details (id, profile_id, graduation_year, department_id, current_company, title)
        └── student_details (id, profile_id, student_number, current_semester)

departments (id, faculty_name, department_name)
events (id, title, description, event_date, location, created_by)
event_attendees (id, event_id, user_id, rsvp_status)
job_posts (id, alumni_id, title, company_name, description, application_url, created_at)
mentorship_requests (id, student_id, alumni_id, message, status, updated_at)
alumni/
├── docker/                 # Nginx, PHP-FPM, MySQL service definitions
├── public/                 # Front controller (index.php) and static assets
│   └── index.php           # Global application entry point
├── src/
│   ├── Config/             # Environment, Database, and App configurations
│   ├── Controllers/        # HTTP Request handlers (Auth, Profile, Admin)
│   ├── Models/             # Database access layers & Business Logic
│   └── Views/              # UI templates / JSON API serializers
├── docker-compose.yml      # Multi-container orchestration specification
├── Dockerfile              # PHP runtime build recipe
├── README.md               # Architecture documentation
└── AGENTS.md               # AI tooling guidelines and prompt engineering specs
# 1. Clone repository
git clone https://github.com/yasarzehra/alumni.git
cd alumni

# 2. Spin up containers (PHP-FPM, Web Server, MySQL)
docker compose up --build
