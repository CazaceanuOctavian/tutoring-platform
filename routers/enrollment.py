from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from db.session import get_db
from models.enrollment import Enrollment
from models.student import Student
from models.course import Course

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])


@router.post("/")
async def enroll_student(
    student_id: UUID,
    course_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    # check student
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(404, "Student not found")

    # check course
    result = await db.execute(
        select(Course).where(Course.id == course_id)
    )
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(404, "Course not found")

    enrollment = Enrollment(
        student_id=student_id,
        course_id=course_id,
    )

    db.add(enrollment)
    await db.commit()

    return {"detail": "Student enrolled"}
