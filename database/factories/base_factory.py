"""
Base Factory - Data Generator Pattern
Provides lightweight, dependency-free mock data generation for testing and database seeding.
"""
import random
import string
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional


class BaseFactory:
    """
    Abstract Base Factory.
    Subclasses define default attribute definitions and persist models/records.
    """

    FIRST_NAMES = [
        "Zehra", "Ahmet", "Mehmet", "Selin", "Can", "Emre", "Burak", "Ayşe", 
        "Elif", "Deniz", "Ece", "Kerem", "Murat", "Gizem", "Onur", "Berk", 
        "Cem", "Derya", "Banu", "Tolga", "Oğuz", "Zeynep", "Mert", "Yasemin"
    ]

    LAST_NAMES = [
        "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım", 
        "Öztürk", "Aydın", "Özdemir", "Arslan", "Doğan", "Kılıç", "Aslan", 
        "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek", "Polat", "Erdoğan"
    ]

    COMPANIES = [
        "Google", "Microsoft", "Trendyol", "Getir", "Amazon", "Siemens",
        "Aselsan", "Baykar", "Garanti BBVA", "Turkcell", "Hepsiburada",
        "Peak Games", "Insider", "Vodafone", "Beko", "Yemeksepeti"
    ]

    TITLES = [
        "Software Engineer", "Backend Developer", "Frontend Developer",
        "Fullstack Engineer", "DevOps Engineer", "Data Scientist",
        "Product Manager", "Machine Learning Specialist", "QA Automation Engineer",
        "Cloud Solutions Architect", "Engineering Manager", "CTO"
    ]

    CITIES = [
        "İstanbul", "Ankara", "İzmir", "Bursa", "Antalya", "Londra",
        "Berlin", "Amsterdam", "San Francisco", "Zürih"
    ]

    @classmethod
    def random_first_name(cls) -> str:
        return random.choice(cls.FIRST_NAMES)

    @classmethod
    def random_last_name(cls) -> str:
        return random.choice(cls.LAST_NAMES)

    @classmethod
    def random_name(cls) -> str:
        return f"{cls.random_first_name()} {cls.random_last_name()}"

    @classmethod
    def random_email(cls, first: str = "", last: str = "") -> str:
        first = (first or cls.random_first_name()).lower()
        last = (last or cls.random_last_name()).lower()
        # Clean non-ascii
        table = str.maketrans("çğıöşü", "cgiosu")
        first = first.translate(table)
        last = last.translate(table)
        rand_num = random.randint(10, 9999)
        domains = ["alumni.edu.tr", "gmail.com", "outlook.com", "example.com"]
        return f"{first}.{last}{rand_num}@{random.choice(domains)}"

    @classmethod
    def random_company(cls) -> str:
        return random.choice(cls.COMPANIES)

    @classmethod
    def random_title(cls) -> str:
        return random.choice(cls.TITLES)

    @classmethod
    def random_city(cls) -> str:
        return random.choice(cls.CITIES)

    @classmethod
    def random_date(cls, days_back: int = 180) -> str:
        delta = timedelta(days=random.randint(0, days_back), seconds=random.randint(0, 86400))
        past = datetime.now(timezone.utc) - delta
        return past.isoformat()

    @classmethod
    def definition(cls) -> Dict[str, Any]:
        """Subclasses must implement default mock attributes."""
        raise NotImplementedError

    @classmethod
    def make(cls, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Creates a mock dictionary instance without persisting."""
        data = cls.definition()
        if overrides:
            data.update(overrides)
        return data

    @classmethod
    def create(cls, db_conn=None, overrides: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Creates and persists an entity."""
        raise NotImplementedError

    @classmethod
    def create_batch(cls, count: int = 5, db_conn=None, overrides: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Creates multiple records."""
        results = []
        for _ in range(count):
            results.append(cls.create(db_conn=db_conn, overrides=overrides))
        return results
