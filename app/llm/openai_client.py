import json
from openai import AsyncOpenAI

from app.llm.base import BaseLLMService
from .schemas import AnalyticsRequest
from app.core.config import settings


class OpenAILLMService(BaseLLMService):
    def __init__(self):
        api_key = settings.OPENAI_API_KEY
        if not api_key or api_key == "your_key_here":
            raise ValueError("OPENAI_API_KEY not set")

        self.client = AsyncOpenAI(api_key=api_key)

    async def parse(self, text: str) -> AnalyticsRequest:
        system_prompt = """
        Ты аналитический ассистент.
        Верни строго JSON без пояснений.

        Возможные метрики:
        - total_videos
        - creator_videos_in_range
        - videos_with_views_threshold
        - views_growth_for_day
        - distinct_videos_with_new_views_for_day

        Формат ответа:
        {
          "metric": "...",
          "creator_id": int | null,
          "date_from": "YYYY-MM-DD" | null,
          "date_to": "YYYY-MM-DD" | null,
          "target_date": "YYYY-MM-DD" | null,
          "views_threshold": int | null
        }

        Никакого текста. Только JSON.
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text},
                ],
                temperature=0,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content

            assert content is not None
            data = json.loads(content)
            return AnalyticsRequest(**data)
        except Exception as e:
            print(f"OpenAI Error: {e}")
            raise ValueError(f"Не удалось распознать запрос: {e}")
