from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    complaint_id = Column(Integer, ForeignKey("complaints.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=True)
    confidence = Column(Float, nullable=False, default=0.0)
    priority = Column(String(20), nullable=False, default="MEDIUM")
    model_version = Column(String(30), nullable=False, default="v1.0.0")
    is_low_confidence = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    complaint = relationship("Complaint", back_populates="diagnoses")
    problem = relationship("Problem", back_populates="diagnoses")
    feedback = relationship("DiagnosisFeedback", back_populates="diagnosis", uselist=False)
    service_records = relationship("ServiceRecord", back_populates="diagnosis")
