from typing import Optional

from pydantic import BaseModel


class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True


class TroubleshootingStepOut(BaseModel):
    step_number: int
    title: str
    description: str
    warning: Optional[str] = None

    class Config:
        from_attributes = True


class ProblemOut(BaseModel):
    id: int
    code: str
    name: str
    description: Optional[str] = None
    severity: str
    estimated_time_min: int
    estimated_time_max: int
    category: Optional[CategoryOut] = None
    troubleshooting_steps: list[TroubleshootingStepOut] = []

    class Config:
        from_attributes = True


class ProblemSummary(BaseModel):
    id: int
    code: str
    name: str
    severity: str

    class Config:
        from_attributes = True
