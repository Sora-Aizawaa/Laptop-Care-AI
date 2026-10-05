"""
Seed the database with categories, problems, and troubleshooting steps.

Usage:
    python -m app.database.seed
"""
from app.database.database import Base, SessionLocal, engine
from app.database.models import Category, Problem, TroubleshootingStep
from app.database.seed_data import CATEGORIES, PROBLEMS


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Category).count() > 0:
            print("Database already seeded, skipping. (Delete laptopcare.db to reseed.)")
            return

        name_to_category = {}
        for cat in CATEGORIES:
            category = Category(name=cat["name"], description=cat["description"])
            db.add(category)
            db.flush()
            name_to_category[cat["name"]] = category

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
                step = TroubleshootingStep(
                    problem_id=problem.id,
                    step_number=i,
                    title=title,
                    description=desc,
                    warning=warning,
                    is_advanced=1 if is_advanced else 0,
                )
                db.add(step)

        db.commit()
        print(f"Seeded {len(CATEGORIES)} categories and {len(PROBLEMS)} problems.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
