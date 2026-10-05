from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class TroubleshootingStep(Base):
    __tablename__ = "troubleshooting_steps"

    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    step_number = Column(Integer, nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    warning = Column(Text, nullable=True)
    is_advanced = Column(Integer, default=0)  # 0 = "Start Here", 1 = "Advanced Troubleshooting"

    problem = relationship("Problem", back_populates="troubleshooting_steps")
