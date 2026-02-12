from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
import asyncio

from app.core.config import settings

bot = Bot(
    token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()


@dp.message()
async def handle_message(message: Message):
    await message.answer("Бот работает")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
