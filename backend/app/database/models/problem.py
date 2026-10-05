from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    code = Column(String(60), unique=True, nullable=False)  # e.g. "overheating" (matches ML label)
    name = Column(String(120), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(20), nullable=False, default="MEDIUM")  # LOW|MEDIUM|HIGH|CRITICAL
    estimated_time_min = Column(Integer, default=30)
    estimated_time_max = Column(Integer, default=60)
    possible_causes = Column(Text, nullable=True)  # stored as "|" separated list

    category = relationship("Category", back_populates="problems")
    troubleshooting_steps = relationship(
        "TroubleshootingStep", back_populates="problem", order_by="TroubleshootingStep.step_number"
    )
    diagnoses = relationship("Diagnosis", back_populates="problem")

    def causes_list(self):
        return [c.strip() for c in (self.possible_causes or "").split("|") if c.strip()]
