import os
import logging
import json
import gspread
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from oauth2client.service_account import ServiceAccountCredentials

# Получаем токен из переменных окружения (или вставьте ваш токен напрямую)
TOKEN = os.getenv("BOT_TOKEN", "ВАШ_BOT_TOKEN").strip()

# Подключаем Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Открываем таблицу по ID
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "ВАШ_ID_ТАБЛИЦЫ")
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Настроим логирование
logging.basicConfig(level=logging.INFO)

# Создаём объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer("Привет! Бот работает!")

# Функция для обработки отчётов
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

# Запуск основного цикла
if name == "__main__":
    asyncio.run(main())
