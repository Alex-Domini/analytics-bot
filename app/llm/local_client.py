from app.llm.base import BaseLLMService


class LocalLLMService(BaseLLMService):
    async def generate_sql(self, text: str) -> str:
        raise NotImplementedError("Локальная модель пока не подключена")
