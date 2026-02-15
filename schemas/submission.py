from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class SubmissionCreate(BaseModel):
    student_id: UUID
    exercise_id: UUID
    code_submitted: str


class SubmissionRead(BaseModel):
    id: UUID
    student_id: UUID
    exercise_id: UUID
    status: str | None
    score: int | None
    submitted_at: datetime

    class Config:
        from_attributes = True
