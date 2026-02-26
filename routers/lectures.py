from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from db.session import get_db
from models.lecture import Lecture
from schemas.lecture import LectureCreate, LectureRead

router = APIRouter(prefix="/lectures", tags=["Lectures"])

@router.post("/", response_model=LectureRead)
async def create_lecture(
    payload: LectureCreate,
    db: AsyncSession = Depends(get_db),
):
    lecture = Lecture(**payload.model_dump())

    db.add(lecture)
    await db.commit()
    await db.refresh(lecture)

    return lecture


@router.get("/", response_model=list[LectureRead])
async def list_lectures(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Lecture))
    return result.scalars().all()


@router.get("/{lecture_id}", response_model=LectureRead)
async def get_lecture(
    lecture_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Lecture).where(Lecture.id == lecture_id)
    )

    lecture = result.scalar_one_or_none()

    if not lecture:
        raise HTTPException(404, "Lecture not found")

    return lecture

@router.delete("/{lecture_id}", status_code=204)
async def delete_lecture(
    lecture_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Lecture).where(Lecture.id == lecture_id))
    lecture = result.scalar_one_or_none()

    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")

    await db.delete(lecture)
    await db.commit()
    return None