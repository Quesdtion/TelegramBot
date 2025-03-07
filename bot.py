# bot.py

from aiogram import Bot, Dispatcher, types
import openai_api  # Импортируем созданный файл

API_TOKEN = 'YOUR_BOT_API_TOKEN'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь отчет для обработки.")

@dp.message_handler(lambda message: True)
async def handle_report(message: types.Message):
    report = message.text
    ai_response = await openai_api.chat_with_ai(report)  # Используем функцию из openai_api.py
    await message.reply(ai_response)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp)
