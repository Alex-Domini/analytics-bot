from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.video import Video

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class VideoSnapshot(Base):
    __tablename__ = "video_snapshots"


id: Mapped[int] = mapped_column(primary_key=True)
views_count: Mapped[int]
likes_count: Mapped[int]
comments_count: Mapped[int]
reports_count: Mapped[int]

delta_views_count: Mapped[int]
delta_likes_count: Mapped[int]
delta_comments_count: Mapped[int]
delta_reports_count: Mapped[int]

create_at: Mapped[DateTime]
update_at: Mapped[DateTime]

video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"))

video: Mapped["Video"] = relationship(back_populates="snapshots")
