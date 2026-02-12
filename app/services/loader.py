from datetime import datetime
from sqlalchemy import insert
from app.db.session import AsyncSessionLocal
from app.models import Video, VideoSnapshot


async def load_videos(data: list[dict]):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            video_rows = []
            snapshot_rows = []

            seen_ids = set()

            for video in data:
                if video["id"] in seen_ids:
                    continue

                seen_ids.add(video["id"])

                video_rows.append(
                    {
                        "id": video["id"],
                        "creator_id": video["creator_id"],
                        "video_created_at": datetime.fromisoformat(
                            video["video_created_at"]
                        ),
                        "views_count": video["views_count"],
                        "likes_count": video["likes_count"],
                        "comments_count": video["comments_count"],
                        "reports_count": video["reports_count"],
                        "created_at": datetime.fromisoformat(video["created_at"]),
                        "updated_at": datetime.fromisoformat(video["updated_at"]),
                    }
                )

                for snapshot in video["snapshots"]:
                    snapshot_rows.append(
                        {
                            "id": snapshot["id"],
                            "video_id": video["id"],
                            "views_count": snapshot["views_count"],
                            "likes_count": snapshot["likes_count"],
                            "comments_count": snapshot["comments_count"],
                            "reports_count": snapshot["reports_count"],
                            "delta_views_count": snapshot["delta_views_count"],
                            "delta_likes_count": snapshot["delta_likes_count"],
                            "delta_comments_count": snapshot["delta_comments_count"],
                            "delta_reports_count": snapshot["delta_reports_count"],
                            "created_at": datetime.fromisoformat(
                                snapshot["created_at"]
                            ),
                            "updated_at": datetime.fromisoformat(
                                snapshot["updated_at"]
                            ),
                        }
                    )
            await session.execute(insert(Video), video_rows)
            await session.execute(insert(VideoSnapshot), snapshot_rows)
