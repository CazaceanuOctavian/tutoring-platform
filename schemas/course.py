from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class CourseCreate(BaseModel):
    title: str
    description: str | None = None


class CourseRead(BaseModel):
    id: UUID
    title: str
    description: str | None
    created_at: datetime

    class Config:
        from_attributes = True
