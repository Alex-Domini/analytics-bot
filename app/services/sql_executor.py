from sqlalchemy import select, func, distinct

from app.db.session import AsyncSessionLocal
from app.models import Video, VideoSnapshot
from app.llm.schemas import AnalyticsRequest


class SQLExecutor:
    async def execute(self, request: AnalyticsRequest) -> int:
        async with AsyncSessionLocal() as session:
            # 1. Сколько всего видео
            if request.metric == "total_videos":
                result = await session.execute(select(func.count()).select_from(Video))
                return result.scalar_one()

            # 2. Сколько видео у креатора в диапазоне дат
            if request.metric == "creator_videos_in_range":
                if (
                    request.date_from is None
                    or request.date_to is None
                    or request.creator_id is None
                ):
                    raise ValueError("creator_id, date_from and date_to are required")

                utc_date = func.date(func.timezone("UTC", Video.video_created_at))

                result = await session.execute(
                    select(func.count())
                    .select_from(Video)
                    .where(
                        Video.creator_id == request.creator_id,
                        utc_date >= request.date_from,
                        utc_date <= request.date_to,
                    )
                )
                return result.scalar_one()

            # 3. Видео с просмотрами больше N
            if request.metric == "videos_with_views_threshold":
                if request.views_threshold is None:
                    raise ValueError("views_threshold is required")

                stmt = (
                    select(func.count())
                    .select_from(Video)
                    .where(Video.views_count > request.views_threshold)
                )

                if request.creator_id:
                    stmt = stmt.where(Video.creator_id == request.creator_id)

                result = await session.execute(stmt)
                return result.scalar_one()

            # 4. Суммарный прирост просмотров за день
            if request.metric == "views_growth_for_day":
                result = await session.execute(
                    select(
                        func.coalesce(func.sum(VideoSnapshot.delta_views_count), 0)
                    ).where(func.date(VideoSnapshot.created_at) == request.target_date)
                )
                return result.scalar_one()

            # 5. Сколько разных видео получали новые просмотры за день
            if request.metric == "distinct_videos_with_new_views_for_day":
                result = await session.execute(
                    select(func.count(distinct(VideoSnapshot.video_id))).where(
                        func.date(VideoSnapshot.created_at) == request.target_date,
                        VideoSnapshot.delta_views_count > 0,
                    )
                )
                return result.scalar_one()

            # 6. Сколько снапшотов имеют отрицательный прирост просмотров
            if request.metric == "negative_views_snapshots":
                result = await session.execute(
                    select(func.count())
                    .select_from(VideoSnapshot)
                    .where(VideoSnapshot.delta_views_count < 0)
                )
                return result.scalar_one()

            # 7 Суммарное количество просмотров набрали все видео, опубликованные в определенную дату?
            if request.metric == "videos_views_sum_in_range":
                utc_date = func.date(func.timezone("UTC", Video.video_created_at))
                result = await session.execute(
                    select(func.coalesce(func.sum(Video.views_count), 0)).where(
                        utc_date >= request.date_from, utc_date <= request.date_to
                    )
                )
                return result.scalar_one()
            raise ValueError("Неизвестная метрика")
