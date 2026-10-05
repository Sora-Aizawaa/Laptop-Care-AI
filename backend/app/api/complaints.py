from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Complaint

router = APIRouter(prefix="/complaints", tags=["complaints"])


@router.get("")
def list_complaints(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    complaints = (
        db.query(Complaint)
        .order_by(Complaint.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return [
        {"id": c.id, "complaint_text": c.complaint_text, "created_at": c.created_at}
        for c in complaints
    ]
