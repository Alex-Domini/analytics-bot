import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.core.config import settings
from app.services.sql_executor import SQLExecutor
from app.llm.fake_client import FakeLLMService

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

llm_service = FakeLLMService()
sql_executor = SQLExecutor()


@dp.message()
async def handle_message(message: Message):
    try:
        if not message.text:
            await message.answer("Отправьте текстовый запрос")
            return

        request = await llm_service.parse(message.text)
        result = await sql_executor.execute(request)
        await message.answer(str(result))
    except ValueError as e:
        await message.answer(str(e))

    except Exception as e:
        print(f"Unexpected error: {e}")
        await message.answer("Внутренняя ошибка сервера")


async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
