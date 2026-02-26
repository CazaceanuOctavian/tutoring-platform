from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.student import Student
from db.session import get_db
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(
    email: str,
    password: str,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Student).where(Student.email == email))
    student = result.scalar_one_or_none()

    if not student or not verify_password(password, student.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(str(student.id), student.role)
    refresh_token = create_refresh_token(str(student.id))

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,        # True in production (HTTPS)
        samesite="lax",
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return {"message": "Logged in"}

@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Missing refresh token")

    payload = decode_token(refresh_token)

    if payload["type"] != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    student_id = payload["sub"]
    role = payload['role']

    new_access = create_access_token(student_id, role)

    response.set_cookie(
        key="access_token",
        value=new_access,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return {"message": "Token refreshed"}

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out"}