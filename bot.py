import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import gspread

TOKEN = os.getenv("BOT_TOKEN", "").strip()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CREDENTIALS_JSON = os.getenv("CREDENTIALS_JSON")

# Проверка наличия необходимых переменных окружения
if not TOKEN or not SPREADSHEET_ID or not CREDENTIALS_JSON:
    raise ValueError("Отсутствуют переменные окружения BOT_TOKEN, SPREADSHEET_ID или CREDENTIALS_JSON")

# Создаём файл с учётными данными
with open("credentials.json", "w") as creds_file:
    creds_file.write(CREDENTIALS_JSON)

# Авторизация с использованием Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Создаём объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Бот работает!")

# Обработчик отчётов
@dp.message()
async def handle_message(message: Message):
    text = message.text
    lines = text.split("\n")
    report_data = {}

    for line in lines:
        parts = line.split(":")
        if len(parts) == 2:
            key, value = parts[0].strip(), parts[1].strip()
            report_data[key] = value

    if "Актив" in report_data:
        row = [message.from_user.full_name, report_data.get("Актив", ""), report_data.get("Новых номеров", "")]
        sheet.append_row(row)
        await message.reply("Отчёт записан ✅")
    else:
        await message.reply("Ошибка в формате отчёта ❌")

# Запуск бота
async def main():
    await dp.start_polling()

if name == "__main__":
    asyncio.run(main())
    
