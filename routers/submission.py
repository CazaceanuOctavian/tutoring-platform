from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID

from db.session import get_db
from models.submission import Submission
from schemas.submission import SubmissionCreate, SubmissionRead

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post("/", response_model=SubmissionRead)
async def create_submission(
    payload: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
):
    submission = Submission(
        **payload.model_dump(),
        status="pending",
    )

    db.add(submission)
    await db.commit()
    await db.refresh(submission)

    return submission


@router.get("/", response_model=list[SubmissionRead])
async def list_submissions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Submission))
    return result.scalars().all()


@router.get("/{submission_id}", response_model=SubmissionRead)
async def get_submission(
    submission_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Submission).where(Submission.id == submission_id)
    )

    submission = result.scalar_one_or_none()

    if not submission:
        raise HTTPException(404, "Submission not found")

    return submission
