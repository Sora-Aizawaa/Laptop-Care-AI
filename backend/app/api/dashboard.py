from sqlalchemy import func
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Diagnosis, DiagnosisFeedback, Problem, ServiceRecord
from app.schemas.history import DashboardStats

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/statistics", response_model=DashboardStats)
def get_statistics(db: Session = Depends(get_db)):
    total_diagnoses = db.query(Diagnosis).count()
    resolved = db.query(ServiceRecord).filter(ServiceRecord.status == "COMPLETED").count()
    high_priority = db.query(Diagnosis).filter(Diagnosis.priority.in_(["HIGH", "CRITICAL"])).count()

    feedback_total = db.query(DiagnosisFeedback).count()
    feedback_correct = db.query(DiagnosisFeedback).filter(DiagnosisFeedback.is_correct.is_(True)).count()
    ai_accuracy = round((feedback_correct / feedback_total) * 100, 1) if feedback_total > 0 else None

    rows = (
        db.query(Problem.name, func.count(Diagnosis.id).label("count"))
        .join(Diagnosis, Diagnosis.problem_id == Problem.id)
        .group_by(Problem.name)
        .order_by(func.count(Diagnosis.id).desc())
        .limit(6)
        .all()
    )
    total_for_pct = sum(r.count for r in rows) or 1
    most_common = [
        {"name": r.name, "count": r.count, "percentage": round(r.count / total_for_pct * 100, 1)}
        for r in rows
    ]

    return DashboardStats(
        total_diagnoses=total_diagnoses,
        resolved=resolved,
        high_priority=high_priority,
        ai_accuracy=ai_accuracy,
        most_common_problems=most_common,
    )
