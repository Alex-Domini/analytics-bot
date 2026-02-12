from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio

from app.core.config import settings
from app.services.sql_executor import count_all_videos

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


# @dp.message()
# async def handle_message(message: Message):
#     await message.answer("Бот работает")


@dp.message()
async def handle_message(message: Message):
    text_msg = (message.text or "").strip().lower()

    if "сколько всего видео" in text_msg:
        value = await count_all_videos()
        await message.answer(str(value))
        return
    await message.answer("Пока понимаю только: 'Сколько всего видео есть в системе?'")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
