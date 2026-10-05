from typing import Optional

from pydantic import BaseModel


class TroubleshootingStepOut(BaseModel):
    step: int
    title: str
    description: str
    warning: Optional[str] = None
    is_advanced: bool = False


class FollowUpQuestion(BaseModel):
    id: str
    question: str
    options: list[str] = ["Yes", "No", "Not sure"]


class DiagnosisResult(BaseModel):
    problem: Optional[str]
    category: Optional[str]
    confidence: float
    is_low_confidence: bool


class DiagnosisResponse(BaseModel):
    diagnosis_id: Optional[int] = None
    diagnosis: DiagnosisResult
    priority: str
    estimated_time: str
    possible_causes: list[str] = []
    reasoning: list[str] = []
    troubleshooting_steps: list[TroubleshootingStepOut] = []
    safety_warning: Optional[str] = None
    follow_up_questions: list[FollowUpQuestion] = []
    top_predictions: dict[str, float] = {}


class FeedbackCreate(BaseModel):
    is_correct: bool
    actual_problem: Optional[str] = None
    feedback_note: Optional[str] = None
