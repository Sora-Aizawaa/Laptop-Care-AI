from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Diagnosis, DiagnosisFeedback
from app.schemas.complaint import GuidedDiagnosisRequest
from app.schemas.diagnosis import DiagnosisResponse, FeedbackCreate
from app.services.diagnosis_service import diagnose

router = APIRouter(prefix="/diagnosis", tags=["diagnosis"])


@router.post("", response_model=DiagnosisResponse)
def create_diagnosis(payload: GuidedDiagnosisRequest, db: Session = Depends(get_db)):
    if not payload.complaint and not payload.answers:
        raise HTTPException(status_code=400, detail="Please describe what is happening with your laptop.")
    result = diagnose(db, complaint_text=payload.complaint or "", answers=payload.answers)
    return result


@router.get("/{diagnosis_id}", response_model=DiagnosisResponse)
def get_diagnosis(diagnosis_id: int, db: Session = Depends(get_db)):
    d = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Diagnosis not found")

    from app.services import recommendation_service, rule_engine
    from app.services.explanation_service import build_reasoning

    problem = d.problem
    steps = recommendation_service.build_troubleshooting_steps(problem) if problem else []
    return {
        "diagnosis_id": d.id,
        "diagnosis": {
            "problem": problem.name if problem else None,
            "category": problem.category.name if problem and problem.category else None,
            "confidence": d.confidence,
            "is_low_confidence": bool(d.is_low_confidence),
        },
        "priority": d.priority,
        "estimated_time": rule_engine.estimate_time_label(problem.estimated_time_min, problem.estimated_time_max) if problem else "N/A",
        "possible_causes": problem.causes_list() if problem else [],
        "reasoning": build_reasoning(problem.code, d.complaint.complaint_text) if problem else [],
        "troubleshooting_steps": steps,
        "safety_warning": rule_engine.get_safety_warning(problem.code, d.priority) if problem else None,
        "follow_up_questions": [],
        "top_predictions": {},
    }


@router.post("/{diagnosis_id}/feedback")
def submit_feedback(diagnosis_id: int, payload: FeedbackCreate, db: Session = Depends(get_db)):
    d = db.query(Diagnosis).filter(Diagnosis.id == diagnosis_id).first()
    if not d:
        raise HTTPException(status_code=404, detail="Diagnosis not found")

    existing = db.query(DiagnosisFeedback).filter(DiagnosisFeedback.diagnosis_id == diagnosis_id).first()
    if existing:
        existing.is_correct = payload.is_correct
        existing.actual_problem = payload.actual_problem
        existing.feedback_note = payload.feedback_note
    else:
        feedback = DiagnosisFeedback(
            diagnosis_id=diagnosis_id,
            is_correct=payload.is_correct,
            actual_problem=payload.actual_problem,
            feedback_note=payload.feedback_note,
        )
        db.add(feedback)
    db.commit()
    return {"message": "Feedback recorded. Thank you — this helps improve future diagnoses."}
