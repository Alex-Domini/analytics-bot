import re

from dateparser.search import search_dates
from .base import BaseLLMService
from .schemas import AnalyticsRequest


class FakeLLMService(BaseLLMService):
    async def parse(self, text: str) -> AnalyticsRequest:
        text = text.lower()

        # --- извлечение чисел ---
        numbers = re.findall(r"\d[\d\s]*", text)
        numbers = [int(n.replace(" ", "")) for n in numbers]

        # --- извлечение дат ---
        dates = search_dates(text, languages=["ru"])
        parsed_dates = [d[1].date() for d in dates] if dates else []

        uuid_match = re.findall(r"[0-9a-fA-F]{32,36}", text)
        # ======================================================
        # 1. ВСЕГО ВИДЕО
        # ======================================================
        if "видео" in text and (
            "всего" in text
            or "общее" in text
            or "в системе" in text
            or "в базе" in text
        ):
            return AnalyticsRequest(metric="total_videos")

        # ======================================================
        # 2. ВИДЕО С ПРОСМОТРАМИ БОЛЬШЕ N
        # ======================================================
        if "просмотр" in text and "больше" in text and numbers:
            return AnalyticsRequest(
                metric="videos_with_views_threshold", views_threshold=numbers[0]
            )

        # ======================================================
        # 3. СКОЛЬКО ВИДЕО У КРЕАТОРА
        # ======================================================
        if "креатор" in text or "creator" in text or "автор" in text:
            creator_id = None
            if uuid_match:
                creator_id = uuid_match[0]
            elif numbers:
                creator_id = str(numbers[0])

            if creator_id is None:
                raise ValueError("Не удалось определить creator_id")
            return AnalyticsRequest(
                metric="creator_total_videos", creator_id=creator_id
            )

        # ======================================================
        # 4. ПРИРОСТ ПРОСМОТРОВ ЗА ДЕНЬ
        # ======================================================
        if ("вырос" in text or "прирост" in text or "прибав" in text) and parsed_dates:
            return AnalyticsRequest(
                metric="views_growth_for_day", target_date=parsed_dates[0]
            )

        # ======================================================
        # 5. РАЗНЫЕ ВИДЕО С НОВЫМИ ПРОСМОТРАМИ
        # ======================================================
        if (
            ("разных" in text or "разные" in text)
            and "просмотр" in text
            and parsed_dates
        ):
            return AnalyticsRequest(
                metric="distinct_videos_with_new_views_for_day",
                target_date=parsed_dates[0],
            )
        # ======================================================
        # 6. ВИДЕО КРЕАТОРА В ДИАПАЗОНЕ
        # ======================================================
        creator_match = re.search(r"id\s*(\d+)", text)

        if creator_match and len(parsed_dates) >= 2:
            return AnalyticsRequest(
                metric="creator_videos_in_range",
                creator_id=str(creator_match.group(1)),
                date_from=parsed_dates[0],
                date_to=parsed_dates[1],
            )

        raise ValueError("Не удалось распознать запрос")
