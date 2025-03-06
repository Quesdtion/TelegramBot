import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = os.getenv("BOT_TOKEN", "").strip()

# Создаём объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Бот работает!")

async def main():
    # Запускаем поллинг, передавая бота в Dispatcher
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())  # Запускаем бота
