from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class ServiceRecord(Base):
    __tablename__ = "service_records"

    id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=False)
    customer_name = Column(String(120), nullable=False)
    device_model = Column(String(120), nullable=True)
    actual_diagnosis = Column(String(120), nullable=True)
    service_performed = Column(Text, nullable=True)
    status = Column(String(30), default="IN_PROGRESS")  # IN_PROGRESS | COMPLETED | CANCELLED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    diagnosis = relationship("Diagnosis", back_populates="service_records")
