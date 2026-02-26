from models.student import Student
from models.course import Course
from models.enrollment import Enrollment
from models.lecture import Lecture
from models.exercise import Exercise
from models.submission import Submission
from models.exercise_test_case import ExerciseTestCase
from models.submission_result import SubmissionResult  

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from db.session import engine
from models.base import Base

# Import routers
from routers import (
    student,
    course,
    enrollment,
    submission,
    exercise,
    lectures, 
    exercise_test_case,
    auth
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables (DEV ONLY)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Tutoring Platform API",
        version="1.0.0",
        description="Backend API for tutoring platform",
        lifespan=lifespan,
    )

    # ---------------------------
    # CORS (adjust for production)
    # ---------------------------
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # change in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ---------------------------
    # Include Routers
    # ---------------------------
    app.include_router(student.router)
    app.include_router(course.router)
    app.include_router(enrollment.router)
    app.include_router(submission.router)
    app.include_router(exercise.router)
    app.include_router(exercise_test_case.router)
    app.include_router(lectures.router)
    app.include_router(auth.router)

    # ---------------------------
    # Health Check
    # ---------------------------
    @app.get("/health", tags=["Health"])
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()
