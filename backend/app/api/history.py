from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Diagnosis, ServiceRecord
from app.schemas.history import HistoryItem, ServiceRecordCreate, ServiceRecordOut

router = APIRouter(tags=["history"])


@router.get("/history", response_model=list[HistoryItem])
def get_history(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    diagnoses = (
        db.query(Diagnosis)
        .order_by(Diagnosis.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        HistoryItem(
            diagnosis_id=d.id,
            complaint_text=d.complaint.complaint_text if d.complaint else "",
            problem_name=d.problem.name if d.problem else None,
            confidence=d.confidence,
            priority=d.priority,
            created_at=d.created_at,
        )
        for d in diagnoses
    ]


@router.post("/service-records", response_model=ServiceRecordOut)
def create_service_record(payload: ServiceRecordCreate, db: Session = Depends(get_db)):
    diagnosis = db.query(Diagnosis).filter(Diagnosis.id == payload.diagnosis_id).first()
    if not diagnosis:
        raise HTTPException(status_code=404, detail="Diagnosis not found")

    record = ServiceRecord(**payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/service-records", response_model=list[ServiceRecordOut])
def list_service_records(db: Session = Depends(get_db)):
    return db.query(ServiceRecord).order_by(ServiceRecord.created_at.desc()).all()
