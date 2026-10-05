from typing import Optional

from pydantic import BaseModel, Field


class ComplaintCreate(BaseModel):
    complaint: str = Field(..., min_length=3, max_length=2000)


class GuidedAnswer(BaseModel):
    question_id: str
    answer: str  # "yes" | "no" | "not_sure"


class GuidedDiagnosisRequest(BaseModel):
    complaint: Optional[str] = None
    answers: list[GuidedAnswer] = []
