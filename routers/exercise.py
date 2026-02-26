from fastapi import APIRouter, Depends, HTTPException
from models.exercise_test_case import ExerciseTestCase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from db.session import get_db
from models.exercise import Exercise
from schemas.exercise import ExerciseCreate, ExerciseRead

from schemas.exercise_test_case import ExerciseTestCaseCreate, ExerciseTestCaseRead

from dependencies.auth import require_admin

router = APIRouter(prefix="/exercises", tags=["Exercises"])

@router.get("/{exercise_id}/test-cases", response_model=list[ExerciseTestCaseRead])
async def list_exercise_test_cases(
    exercise_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id)
    )
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    result = await db.execute(
        select(ExerciseTestCase).where(
            ExerciseTestCase.exercise_id == exercise_id
        )
    )

    return result.scalars().all()

@router.post("/", response_model=ExerciseRead)
async def create_exercise(
    payload: ExerciseCreate,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin)
):
    exercise = Exercise(**payload.model_dump())

    db.add(exercise)
    await db.commit()
    await db.refresh(exercise)

    return exercise


@router.get("/", response_model=list[ExerciseRead])
async def list_exercises(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Exercise))
    return result.scalars().all()


@router.get("/{exercise_id}", response_model=ExerciseRead)
async def get_exercise(
    exercise_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Exercise).where(Exercise.id == exercise_id)
    )

    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(404, "Exercise not found")

    return exercise

@router.delete("/{exercise_id}", status_code=204)
async def delete_exercise(
    exercise_id: UUID,
    db: AsyncSession = Depends(get_db),
    admin = Depends(require_admin)
):
    result = await db.execute(select(Exercise).where(Exercise.id == exercise_id))
    exercise = result.scalar_one_or_none()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    await db.delete(exercise)
    await db.commit()
    return None  

