# import os
# from openai import AsyncOpenAI
# from app.llm.base import BaseLLMService


# class OpenAILLMService(BaseLLMService):
#     def __init__(self):
#         self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

#     async def generate_sql(self, text: str) -> str | None:
#         response = await self.client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[
#                 {"role": "system", "content": "Ты генерируешь только SQL запрос."},
#                 {"role": "user", "content": text},
#             ],
#         )
#         return response.choices[0].message.content
