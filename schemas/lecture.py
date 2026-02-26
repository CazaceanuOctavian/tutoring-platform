# schemas/lecture.py

from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class LectureBase(BaseModel):
    title: str
    content: str
    section: str
    order_index: int

class LectureCreate(LectureBase):
    course_id: UUID

class LectureRead(LectureBase):
    id: UUID
    course_id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)