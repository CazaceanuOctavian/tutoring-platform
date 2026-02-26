# routers/exercise_test_cases.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from db.session import get_db
from models.exercise import Exercise
from models.exercise_test_case import ExerciseTestCase
from schemas.exercise_test_case import (
    ExerciseTestCaseCreate,
    ExerciseTestCaseRead,
)

router = APIRouter(prefix="/exercise-test-cases", tags=["Exercise Test Cases"])


@router.post("/", response_model=ExerciseTestCaseRead)
async def create_test_case(
    payload: ExerciseTestCaseCreate,
    db: AsyncSession = Depends(get_db),
):
    
    result = await db.execute(
        select(Exercise).where(Exercise.id == payload.exercise_id)
    )
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    test_case = ExerciseTestCase(**payload.model_dump())

    db.add(test_case)
    await db.commit()
    await db.refresh(test_case)

    return test_case


@router.delete("/{test_case_id}", status_code=204)
async def delete_test_case(
    test_case_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(ExerciseTestCase).where(ExerciseTestCase.id == test_case_id)
    )
    test_case = result.scalar_one_or_none()

    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")

    await db.delete(test_case)
    await db.commit()

    return None  