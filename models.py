from __future__ import annotations
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    pw_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    scores: Mapped[list["Score"]] = relationship(back_populates='user')


class Score(Base):
    __tablename__ = 'scores'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False, index=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    scale: Mapped[str] = mapped_column(String(50), nullable=False)
    scale_key: Mapped[str] = mapped_column(String(5), nullable=False)
    bpm: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    user: Mapped["User"] = relationship(back_populates='scores')

    



