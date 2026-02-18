from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.video import Video

from datetime import datetime
from sqlalchemy import String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    views_count: Mapped[int] = mapped_column()
    likes_count: Mapped[int] = mapped_column()
    comments_count: Mapped[int] = mapped_column()
    reports_count: Mapped[int] = mapped_column()

    delta_views_count: Mapped[int] = mapped_column()
    delta_likes_count: Mapped[int] = mapped_column()
    delta_comments_count: Mapped[int] = mapped_column()
    delta_reports_count: Mapped[int] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    video_id: Mapped[str] = mapped_column(ForeignKey("videos.id", ondelete="CASCADE"))

    video: Mapped["Video"] = relationship(back_populates="snapshots")
