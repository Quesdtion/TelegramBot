import os
import json
import gspread
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from google.oauth2.service_account import Credentials

# Читаем JSON-ключ из переменной окружения
credentials_json = os.getenv("CREDENTIALS_JSON")

if not credentials_json:
    raise ValueError("Отсутствует CREDENTIALS_JSON в переменных окружения")

# Преобразуем строку JSON в словарь
credentials_dict = json.loads(credentials_json)

# Подключаем Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
client = gspread.authorize(creds)

# Открываем таблицу
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
sheet = client.open_by_key(SPREADSHEET_ID).sheet1

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Подключаем Telegram-бота
TOKEN = os.getenv("BOT_TOKEN")
print(f"Токен: {TOKEN}")bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик сообщений с отчётами
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
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
