from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from passlib.hash import bcrypt

from db.session import get_db
from models.student import Student
from schemas.student import StudentCreate, StudentRead

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", response_model=StudentRead)
async def create_student(
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db),
):
    student = Student(
        name=payload.name,
        email=payload.email,
        password_hash=bcrypt.hash(payload.password),
    )

    db.add(student)
    await db.commit()
    await db.refresh(student)

    return student


@router.get("/", response_model=list[StudentRead])
async def list_students(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Student))
    return result.scalars().all()


@router.get("/{student_id}", response_model=StudentRead)
async def get_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(404, "Student not found")

    return student


@router.delete("/{student_id}")
async def delete_student(
    student_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )

    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(404, "Student not found")

    await db.delete(student)
    await db.commit()

    return {"detail": "Deleted"}
