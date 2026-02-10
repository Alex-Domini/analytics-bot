from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.videosnapshot import VideoSnapshot

from app.db.base import Base
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Video(Base):
    __tablename__ = "videos"


id: Mapped[int] = mapped_column(primary_key=True)
creator_id: Mapped[int]
video_created_at: Mapped[DateTime]

views_count: Mapped[int]
likes_count: Mapped[int]
comments_count: Mapped[int]
reports_count: Mapped[int]

created_at: Mapped[DateTime] = mapped_column(server_default=func.now())
updated_at: Mapped[DateTime] = mapped_column(
    server_default=func.now(), onupdate=func.now()
)

snapshots: Mapped[list["VideoSnapshot"]] = relationship(
    "VideoSnapshot", back_populates="videos", cascade="all, delete-orphan"
)
