from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.videosnapshot import VideoSnapshot

from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Video(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column()
    video_created_at: Mapped[datetime] = mapped_column(DateTime)

    views_count: Mapped[int] = mapped_column()
    likes_count: Mapped[int] = mapped_column()
    comments_count: Mapped[int] = mapped_column()
    reports_count: Mapped[int] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    snapshots: Mapped[list["VideoSnapshot"]] = relationship(
        "VideoSnapshot", back_populates="videos", cascade="all, delete-orphan"
    )
