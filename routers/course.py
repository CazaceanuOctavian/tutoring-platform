from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from db.session import get_db
from schemas.course import CourseCreate, CourseRead

from models.course import Course
from models.lecture import Lecture
from models.exercise import Exercise
from schemas.course import CourseCreate, CourseRead
from schemas.lecture import LectureCreate, LectureRead
from schemas.exercise import ExerciseCreate, ExerciseRead

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/{course_id}/lectures", response_model=list[LectureRead])
async def get_course_lectures(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(404, "Course not found")

    result = await db.execute(
        select(Lecture)
        .where(Lecture.course_id == course_id)
        .order_by(Lecture.order_index)
    )

    return result.scalars().all()

@router.get(
    "/{course_id}/sections/{section_number}/lectures",
    response_model=list[LectureRead],
)
async def get_lectures_by_section(
    course_id: UUID,
    section: str,
    db: AsyncSession = Depends(get_db),
):
    course_result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    course = course_result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    result = await db.execute(
        select(Lecture)
        .where(
            Lecture.course_id == course_id,
            Lecture.section == section,
        )
        .order_by(Lecture.order_index)
    )

    lectures = result.scalars().all()

    return lectures


@router.get("/{course_id}/exercises", response_model=list[ExerciseRead])
async def get_course_exercises(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    # check course exists
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(404, "Course not found")

    result = await db.execute(
        select(Exercise)
        .where(Exercise.course_id == course_id)
        .order_by(Exercise.order_index)
    )

    return result.scalars().all()


@router.get(
    "/{course_id}/sections/{section}/exercises",
    response_model=list[ExerciseRead],
)
async def get_exercises_by_section(
    course_id: UUID,
    section: str,  
    db: AsyncSession = Depends(get_db),
):
    course_result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    course = course_result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    result = await db.execute(
        select(Exercise)
        .where(
            Exercise.course_id == course_id,
            Exercise.section == section,  
        )
        .order_by(Exercise.order_index)
    )

    exercises = result.scalars().all()
    return exercises


@router.post("/", response_model=CourseRead)
async def create_course(
    payload: CourseCreate,
    db: AsyncSession = Depends(get_db),
):
    course = Course(**payload.model_dump())

    db.add(course)
    await db.commit()
    await db.refresh(course)

    return course


@router.get("/", response_model=list[CourseRead])
async def list_courses(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Course))
    return result.scalars().all()


@router.get("/{course_id}", response_model=CourseRead)
async def get_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(404, "Course not found")

    return course


@router.delete("/{course_id}")
async def delete_course(
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )

    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(404, "Course not found")

    await db.delete(course)
    await db.commit()

    return {"detail": "Deleted"}
