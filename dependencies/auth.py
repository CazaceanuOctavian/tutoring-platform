from fastapi import Request, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.student import Student
from db.session import get_db
from core.security import decode_token

from fastapi import HTTPException, status


async def get_current_student(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    payload = decode_token(token)

    if payload["type"] != "access":
        raise HTTPException(status_code=401, detail="Invalid token")

    student_id = payload["sub"]

    result = await db.execute(
        select(Student).where(Student.id == student_id)
    )
    student = result.scalar_one_or_none()

    if not student:
        raise HTTPException(status_code=401, detail="User not found")

    return student

async def require_admin(current_student = Depends(get_current_student)):
    if current_student.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_student