from uuid import UUID
from pydantic import BaseModel


class ExerciseTestCaseCreate(BaseModel):
    exercise_id: UUID
    input_data: str
    expected_output: str
    is_hidden: bool = True


class ExerciseTestCaseRead(BaseModel):
    id: UUID
    exercise_id: UUID
    input_data: str
    expected_output: str
    is_hidden: bool

    class Config:
        from_attributes = True