from abc import ABC, abstractmethod
from .schemas import AnalyticsRequest


class BaseLLMService(ABC):
    @abstractmethod
    async def parse(self, user_message: str) -> AnalyticsRequest:
        """
        Должен вернуть структуру вида:

        {
            "metric": "total_videos",
            "creator_id": None,
            "date_from": None,
            "date_to": None,
            "threshold": None
        }
        """
        pass
