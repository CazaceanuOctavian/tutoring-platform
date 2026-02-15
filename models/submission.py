import uuid
from datetime import datetime
from sqlalchemy import Text, DateTime, ForeignKey, String, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("students.id", ondelete="CASCADE")
    )

    exercise_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("exercises.id", ondelete="CASCADE")
    )

    code_submitted: Mapped[str] = mapped_column(Text, nullable=False)

    status: Mapped[str | None] = mapped_column(String(50))  # pending/passed/failed
    score: Mapped[int | None] = mapped_column(Integer)

    submitted_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    student = relationship("Student", back_populates="submissions")
    exercise = relationship("Exercise", back_populates="submissions")

    results = relationship(
        "SubmissionResult",
        back_populates="submission",
        cascade="all, delete-orphan"
    )
