from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class HistoryItem(BaseModel):
    diagnosis_id: int
    complaint_text: str
    problem_name: Optional[str] = None
    confidence: float
    priority: str
    created_at: datetime

    class Config:
        from_attributes = True


class ServiceRecordCreate(BaseModel):
    diagnosis_id: int
    customer_name: str
    device_model: Optional[str] = None
    actual_diagnosis: Optional[str] = None
    service_performed: Optional[str] = None
    status: str = "IN_PROGRESS"


class ServiceRecordOut(BaseModel):
    id: int
    diagnosis_id: int
    customer_name: str
    device_model: Optional[str] = None
    actual_diagnosis: Optional[str] = None
    service_performed: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_diagnoses: int
    resolved: int
    high_priority: int
    ai_accuracy: Optional[float]
    most_common_problems: list[dict]
