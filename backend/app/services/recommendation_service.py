from sqlalchemy.orm import Session

from app.database.models import Problem


def get_problem_by_code(db: Session, code: str) -> Problem | None:
    return db.query(Problem).filter(Problem.code == code).first()


def build_troubleshooting_steps(problem: Problem) -> list[dict]:
    steps = []
    for step in problem.troubleshooting_steps:
        steps.append({
            "step": step.step_number,
            "title": step.title,
            "description": step.description,
            "warning": step.warning,
            "is_advanced": bool(step.is_advanced),
        })
    return steps
