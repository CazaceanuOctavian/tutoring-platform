from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from db.session import get_db
from models.course import Course
from schemas.course import CourseCreate, CourseRead

router = APIRouter(prefix="/courses", tags=["Courses"])


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
