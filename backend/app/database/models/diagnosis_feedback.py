from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class DiagnosisFeedback(Base):
    __tablename__ = "diagnosis_feedback"

    id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), unique=True, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    actual_problem = Column(String(120), nullable=True)
    feedback_note = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    diagnosis = relationship("Diagnosis", back_populates="feedback")
