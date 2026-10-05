import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("LAPTOPCARE_SECRET_KEY", "test-secret")

from app.database.database import Base, engine, SessionLocal
from app.database.models import Category, Problem, TroubleshootingStep
from app.database.seed_data import CATEGORIES, PROBLEMS
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(Category).count() == 0:
        name_to_category = {}
        for cat in CATEGORIES:
            c = Category(name=cat["name"], description=cat["description"])
            db.add(c)
            db.flush()
            name_to_category[cat["name"]] = c
        for p in PROBLEMS:
            problem = Problem(
                category_id=name_to_category[p["category"]].id,
                code=p["code"],
                name=p["name"],
                description=p["description"],
                severity=p["severity"],
                estimated_time_min=p["time"][0],
                estimated_time_max=p["time"][1],
                possible_causes="|".join(p["causes"]),
            )
            db.add(problem)
            db.flush()
            for i, (title, desc, warning, is_advanced) in enumerate(p["steps"], start=1):
                db.add(TroubleshootingStep(
                    problem_id=problem.id, step_number=i, title=title,
                    description=desc, warning=warning, is_advanced=1 if is_advanced else 0,
                ))
        db.commit()
    db.close()
    yield


@pytest.fixture
def client():
    return TestClient(app)
