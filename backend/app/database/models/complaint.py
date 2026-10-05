from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Complaint(Base):
    __tablename__ = "complaints"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    complaint_text = Column(Text, nullable=False)
    answers_json = Column(Text, nullable=True)  # guided-mode Q&A stored as JSON string
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    diagnoses = relationship("Diagnosis", back_populates="complaint")
