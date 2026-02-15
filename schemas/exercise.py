from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ExerciseCreate(BaseModel):
    course_id: UUID                  
    title: str                        
    description: str | None = None    
    starter_code: str | None = None   
    order_index: int | None = None    

class ExerciseRead(BaseModel):
    id: UUID
    course_id: UUID
    title: str
    description: str | None
    starter_code: str | None
    order_index: int | None
    created_at: datetime

    class Config:
        from_attributes = True  
