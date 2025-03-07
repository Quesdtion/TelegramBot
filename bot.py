import os
import logging
import gspread
from aiogram import Bot, Dispatcher, types
from google.oauth2.service_account import Credentials
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import matplotlib.pyplot as plt
import io

logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения
TOKEN = os.getenv("BOT_TOKEN", "")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "")
credentials_json = os.getenv("CREDENTIALS_JSON", "")

# Проверка переменных
if not TOKEN or not SPREADSHEET_ID or not credentials_json:
    raise ValueError("Ошибка: отсутствуют необходимые переменные окружения!")

logging.info("✅ Переменные окружения загружены")

# Подключаемся к Google Sheets API
credentials_dict = json.loads(credentials_json)
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID)
logging.info("✅ Подключение к Google Sheets успешно!")

# Подключаем Telegram-бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
logging.info("✅ Бот успешно запущен!")

# Обработчики команд
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer("Добро пожаловать! Используйте кнопки ниже.")

async def main():
    logging.info("✅ Запуск бота...")
    await dp.start_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
