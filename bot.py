import openai
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

# Инициализация API ключей
openai.api_key = os.getenv("OPENAI_API_KEY")
API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Функция для общения с AI
async def chat_with_ai(message_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message_text},
            ],
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"Ошибка при взаимодействии с AI: {e}")
        return "Произошла ошибка при взаимодействии с ИИ."

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, использующий нейросети от OpenAI. Задавай мне вопросы, и я постараюсь ответить.")

# Обработка текстовых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    user_message = message.text.strip()
    ai_response = await chat_with_ai(user_message)
    await message.reply(f"Ответ от ИИ:\n{ai_response}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
