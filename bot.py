import os
import json
import gspread
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from google.oauth2.service_account import Credentials

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения
TOKEN = os.getenv("BOT_TOKEN", "").strip()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "").strip()
credentials_json = os.getenv("CREDENTIALS_JSON", "").strip()

# Проверяем, загружены ли переменные
if not TOKEN:
    raise ValueError("Ошибка: отсутствует BOT_TOKEN в переменных окружения!")
if not SPREADSHEET_ID:
    raise ValueError("Ошибка: отсутствует SPREADSHEET_ID в переменных окружения!")
if not credentials_json:
    raise ValueError("Ошибка: отсутствует CREDENTIALS_JSON в переменных окружения!")

logging.info(f"✅ Токен загружен: {repr(TOKEN)}")
logging.info(f"✅ ID таблицы загружен: {SPREADSHEET_ID}")

# Подключаемся к Google Sheets API
try:
    credentials_dict = json.loads(credentials_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).sheet1
    logging.info("✅ Подключение к Google Sheets успешно!")
except Exception as e:
    logging.error(f"Ошибка при подключении к Google Sheets: {e}")
    raise

# Подключаем Telegram-бота
try:
    bot = Bot(token=TOKEN)
    dp = Dispatcher()
    logging.info("✅ Бот успешно запущен!")
except Exception as e:
    logging.error(f"Ошибка при запуске бота: {e}")
    raise

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
