"""
JobPostingFactory - Model Factory
Generates realistic career opportunities, job postings, and internship offerings
for the alumni ecosystem with rich industry attributes (experience level, requirements, salaries).
"""
import random
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from database.factories.base_factory import BaseFactory


class JobPostingFactory(BaseFactory):
    """Factory for JobPosting entities."""

    TECH_TITLES = [
        ("Senior Backend Engineer", "senior", "full_time", "130.000 - 180.000 TL", "Python, FastAPI, PostgreSQL, Docker, Redis, Kubernetes"),
        ("Full Stack Developer", "mid", "full_time", "95.000 - 140.000 TL", "TypeScript, React, Node.js, PostgreSQL, Docker"),
        ("Data Scientist & AI Specialist", "mid", "full_time", "110.000 - 160.000 TL", "Python, PyTorch, SQL, Pandas, Scikit-Learn, MLOps"),
        ("Cloud & DevOps Architect", "lead", "full_time", "160.000 - 220.000 TL", "AWS, Terraform, Kubernetes, CI/CD, Linux, Prometheus"),
        ("Frontend Engineer (React/Next.js)", "mid", "full_time", "90.000 - 130.000 TL", "React, Next.js, TailwindCSS, Redux Toolkit, REST"),
        ("Yazılım Mühendisliği Stajyeri", "entry", "internship", "35.000 - 45.000 TL", "Python / Go temelleri, Veri Yapıları, Git, Meraklı ve Öğrenmeye Açık"),
        ("Cyber Security Analyst", "senior", "full_time", "125.000 - 175.000 TL", "Network Security, SIEM, Penetration Testing, OWASP"),
        ("Mobile Developer (Flutter / iOS)", "mid", "full_time", "100.000 - 145.000 TL", "Flutter, Dart, Swift, REST APIs, App Store Deployment"),
        ("Ürün Yöneticisi (Product Manager)", "senior", "full_time", "140.000 - 190.000 TL", "Agile/Scrum, Jira, Ürün Analitiği, A/B Testing, İletişim")
    ]

    COMPANIES = [
        "Google", "Trendyol", "Peak Games", "Getir", "Baykar Teknoloji",
        "Aselsan", "Insider", "Turkcell", "Vodafone", "Microsoft", "Havelsan"
    ]

    LOCATIONS = [
        "İstanbul (Hybrid)", "İstanbul (Levent Ofis)", "Ankara (ODTÜ Teknokent)",
        "İzmir (Urla Bilişim Vadisi)", "Remote (Türkiye Geneli)", "Amsterdam (Hybrid / Remote)",
        "Berlin (Tamamen Uzaktan)"
    ]

    @classmethod
    def definition(cls) -> Dict[str, Any]:
        job_template = random.choice(cls.TECH_TITLES)
        company = random.choice(cls.COMPANIES)
        title, level, emp_type, salary, reqs = job_template
        location = random.choice(cls.LOCATIONS)

        company_slug = company.lower().replace(" ", "").replace("teknoloji", "")

        return {
            "title": title,
            "company_name": company,
            "location": location,
            "employment_type": emp_type,
            "experience_level": level,
            "description": f"{company} ekibimizde {title} olarak çalışacak mezun ve yetenekli takım arkadaşları arıyoruz. Hızlı büyüyen dinamik ekibimizde modern teknolojiler ve esnek çalışma kültürü sunuyoruz.",
            "requirements": reqs,
            "salary_range": salary,
            "application_url": f"https://careers.{company_slug}.com/apply",
            "status": "active"
        }

    @classmethod
    def create(cls, db_conn=None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        data = cls.make(overrides)
        if db_conn:
            cursor = db_conn.cursor()

            # Assign to an existing alumni/user if not explicitly specified
            alumni_id = data.get("alumni_id")
            if not alumni_id:
                try:
                    cursor.execute("SELECT id FROM users ORDER BY RANDOM() LIMIT 1")
                    row = cursor.fetchone()
                    alumni_id = row[0] if row else 1
                except Exception:
                    alumni_id = 1
            data["alumni_id"] = alumni_id

            now = datetime.now(timezone.utc).isoformat()
            cursor.execute("""
                INSERT INTO job_postings (
                    alumni_id, title, company_name, location, employment_type,
                    experience_level, description, requirements, salary_range,
                    application_url, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["alumni_id"], data["title"], data["company_name"], data["location"],
                data["employment_type"], data["experience_level"], data["description"],
                data["requirements"], data["salary_range"], data["application_url"],
                data["status"], now
            ))

            job_id = cursor.lastrowid
            data["id"] = job_id

            # Keep legacy job_posts synchronized
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO job_posts (id, alumni_id, title, company_name, location, employment_type, description, application_url, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (job_id, data["alumni_id"], data["title"], data["company_name"], data["location"], data["employment_type"], data["description"], data["application_url"], now))
            except Exception:
                pass

            db_conn.commit()

        return data


# Backward compatible alias
JobPostFactory = JobPostingFactory
