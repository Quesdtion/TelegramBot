import logging
import json
import gspread
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from oauth2client.service_account import ServiceAccountCredentials

# Получаем токен бота из переменных окружения
import os

TOKEN = os.getenv("BOT_TOKEN")
print(f"TOKEN: '{TOKEN}'")  # Выведет токен в логи Railway

if not TOKEN or " " in TOKEN:
    raise ValueError("Ошибка: Токен пустой или содержит пробелы!")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CREDENTIALS_JSON = os.getenv("CREDENTIALS_JSON")
CREDENTIALS_PATH = "credentials.json"

if not TOKEN or not SPREADSHEET_ID or not CREDENTIALS_JSON:
    raise ValueError("Отсутствуют переменные окружения BOT_TOKEN, SPREADSHEET_ID или CREDENTIALS_JSON")

# Создаём credentials.json из переменной окружения
with open(CREDENTIALS_PATH, "w") as creds_file:
    creds_file.write(CREDENTIALS_JSON)

# Подключаем Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_PATH, scope)
client = gspread.authorize(creds)

# Открываем таблицу
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Функция для обработки отчётов
@dp.message_handler()
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

if __name__ == "__main__":
    asyncio.run(main())
