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

## 🗄️ 3. Data Design & Database Schema

> 📖 **Full Specification:** For complete Entity-Relationship Diagrams (ERD), full data dictionary, column types, indexing heuristics, and 3NF normalization analysis, see the dedicated **[Data Design Documentation (ddd.md)](ddd.md)**.

### Core Relational Schema Overview

```text
users (id, email, password_hash, role, status, created_at)
  ├── profiles (id, user_id, first_name, last_name, bio, avatar_url)
  │     ├── alumni_details (id, profile_id, graduation_year, department_id, current_company, title)
  │     └── student_details (id, profile_id, student_number, current_semester)
  ├── announcements (id, author_id, title, content, category, status, created_at)
  ├── events (id, title, description, event_date, location, created_by)
  │     └── event_attendees (id, event_id, user_id, rsvp_status)
  ├── job_posts (id, alumni_id, title, company_name, description, application_url, created_at)
  └── mentorship_requests (id, student_id, alumni_id, message, status, updated_at)

departments (id, faculty_name, department_name, code)
```

The data layer is engineered to transition from in-memory prototypes to production-grade persistent MySQL/PostgreSQL storage backed by named Docker volumes (solving the transient data loss demonstrated in *The Forgetting Test*). For detailed table constraints and Mermaid ERD visualizer, refer to **[ddd.md](ddd.md)**.

---

## 🏛️ 4. MVC Architecture Overview

The Alumni platform follows the **Model-View-Controller (MVC)** architectural pattern to maintain strict separation of concerns, high maintainability, testability, and clean code organization.

```text
       HTTP Request
Client -------------> [Router / Front Controller] (public/index.php or server.py)
                              |
                              v
                       [ Controller ] <---- Input validation, routing & orchestration
                         /          \
                        /            \
                       v              v
                  [ Model ]        [ View ]
             (Data & DB Queries)  (HTML Templates / JSON Serializers)
                       \              /
                        \            /
                         v          v
                       HTTP Response (JSON / HTML)
Client <----------------------'
```

### Core Components & Responsibilities

| Component | Responsibility | Project Implementation |
| :--- | :--- | :--- |
| **Model** (`M`) | Encapsulates business logic, data rules, entity representations, and database access layers. Ensures data validation and transactional consistency. | `User.php`, `Profile.php`, `JobPost.php`, `Event.php` (In-memory: `users_db`) |
| **View** (`V`) | Manages the presentation layer. Formats and renders output for end users, serving either responsive HTML pages or standardized JSON API responses. | `index.html`, `about.html`, `JsonResponse.php`, Swagger UI template |
| **Controller** (`C`) | Acts as the orchestrator. Receives HTTP requests (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), validates input, calls Model methods, and returns Views. | `UserController.php`, `AuthController.php`, `SimpleHandler` in `server.py` |

---

## 📂 5. Directory, Folder & File Structure

```text
alumni/
├── docker/                             # Multi-container service definitions
│   ├── nginx/
│   │   └── default.conf                # Nginx reverse proxy & virtual host configuration
│   ├── php/
│   │   └── local.ini                   # PHP runtime configuration overrides
│   └── mysql/
│       └── init.sql                    # Database initialization scripts and seed schemas
├── public/                             # Public web root (directly exposed to web server)
│   ├── index.php                       # Front controller & single application entry point
│   ├── css/                            # Global stylesheets and design tokens
│   ├── js/                             # Client-side JavaScript interactions
│   └── assets/                         # Static media assets (logos, icons, illustrations)
├── src/                                # Core application source code (MVC structure)
│   ├── Config/                         # Configuration and environment loaders
│   │   ├── Database.php                # Database connection manager (PDO with connection pooling)
│   │   └── App.php                     # Application settings and environment variables
│   ├── Controllers/                    # HTTP Request Handlers (Controller Layer)
│   │   ├── BaseController.php          # Shared controller abstractions (JSON response, status codes)
│   │   ├── AuthController.php          # Login, registration, token issuance, logout
│   │   ├── UserController.php          # User profile management and CRUD operations
│   │   ├── JobController.php           # Job & internship postings
│   │   └── EventController.php         # Event creation, RSVPs, and attendee listing
│   ├── Models/                         # Business Logic & Database Layer (Model Layer)
│   │   ├── BaseModel.php               # Base model with shared query builders and CRUD helpers
│   │   ├── User.php                    # User identity, authentication, and role checking
│   │   ├── Profile.php                 # Extended profile, alumni details, student data
│   │   ├── JobPost.php                 # Job vacancies and application relationships
│   │   └── Event.php                   # Event scheduling and attendee mappings
│   ├── Views/                          # Presentation Layer (View Layer)
│   │   ├── layouts/                    # Shared layout templates (header, footer, navigation)
│   │   │   ├── main.php                # Main HTML layout wrapper
│   │   │   └── auth.php                # Authentication pages layout
│   │   ├── pages/                      # Specific view templates
│   │   │   ├── home.php                # Landing page view
│   │   │   ├── about.php               # About platform view
│   │   │   ├── users/                  # User directory and profile detail views
│   │   │   └── jobs/                   # Job board views
│   │   └── responses/                  # API response serializers (JSON payload formatters)
│   │       └── JsonResponse.php        # Standardized JSON response envelope
│   ├── Routes/                         # Routing definitions and dispatchers
│   │   ├── api.php                     # RESTful API route declarations (/api/*)
│   │   └── web.php                     # Web browser route declarations (/, /about, etc.)
│   └── Middleware/                     # Request lifecycle filters
│       ├── AuthMiddleware.php          # Authentication verification (session / JWT)
│       ├── RoleMiddleware.php          # Role-based access control (RBAC) guard
│       └── CorsMiddleware.php          # Cross-Origin Resource Sharing headers
├── index.html                          # Prototype landing page (Temporary Main Page)
├── about.html                          # Prototype about page (Temporary About Page)
├── server.py                           # Python development HTTP server (interactive demo)
├── main.py                             # Python in-memory RESTful CRUD API & Swagger server
├── docker-compose.yml                  # Multi-container orchestration (PHP-FPM, Nginx, MySQL)
├── Dockerfile                          # Application runtime container recipe
├── .gitignore                          # Git file exclusion rules
├── ddd.md                              # Data Design Documentation (ERD, Schema, Indexing)
└── README.md                           # Project documentation & architectural blueprints
```

### Detailed Breakdown of Directories & Roles

1. **`public/` (Web Document Root)**
   - The only directory exposed to the public internet by the web server (Nginx/Apache).
   - Houses the **Front Controller** (`index.php`), which intercepts all incoming requests, bootstraps the environment, applies middleware, and routes to appropriate controllers.

2. **`src/Controllers/` (Controller Layer)**
   - Acts as the orchestrator of application workflows.
   - Extracts payload data from requests (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`), validates input, calls Model methods, and formats outgoing responses.

3. **`src/Models/` (Model Layer)**
   - Encapsulates database tables, relationships, and business integrity rules.
   - Interacts with MySQL through PDO prepared statements to guard against SQL injection, managing operations across `users`, `profiles`, `events`, and `job_posts`.

4. **`src/Views/` (View Layer)**
   - Strictly reserved for rendering presentation logic.
   - Separates HTML templates for web visitors from standardized JSON API responses consumed by mobile clients, Postman, or third-party integrations.

5. **`src/Config/` & `src/Middleware/` (Infrastructure & Security)**
   - Houses database connection pools, environment configurations, and security filters (JWT verification, RBAC permissions, and CORS).

6. **`docker/` (Containerization Environment)**
   - Defines reproducible isolated runtimes for PHP-FPM, Nginx, and MySQL, ensuring zero configuration discrepancies between development and production.

---

## 🚀 6. Quick Start & Running the Project

### Option A: Local Python Prototype Server (Current Development Server)
```bash
# Run the threaded HTTP server (port 80 / 8000 fallback)
python server.py

# Available Endpoints:
# - GET    /                  -> Main landing page (index.html)
# - GET    /about             -> About page (about.html)
# - GET    /hello             -> Plaintext "hello world!"
# - GET    /hello/{name}      -> Plaintext "hello, {name}"
# - GET    /sum/{n1}/{n2}     -> Sum calculation
# - GET    /api/health        -> JSON health status
# - GET    /api/swagger       -> Interactive Swagger UI documentation
# - GET    /api/users         -> List all users (JSON)
# - POST   /api/users         -> Create new user (JSON)
# - GET    /api/users/{id}    -> Fetch single user (JSON)
# - PUT    /api/users/{id}    -> Update full user (JSON)
# - PATCH  /api/users/{id}    -> Partially update user (JSON)
# - DELETE /api/users/{id}    -> Remove user (JSON)
```

### Option B: Docker Containerized Stack (Production Deployment)
```bash
# 1. Clone repository
git clone https://github.com/yasarzehra/alumni.git
cd alumni

# 2. Spin up containers (PHP-FPM, Nginx, MySQL)
docker compose up --build
```
