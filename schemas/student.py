from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class StudentRead(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
