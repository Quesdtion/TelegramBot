import os
import json
import gspread
import logging
import sys
import asyncio
import io
import matplotlib.pyplot as plt
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from google.oauth2.service_account import Credentials
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Настраиваем логирование для Railway
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Загружаем переменные окружения
TOKEN = os.getenv("BOT_TOKEN", "").strip()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "").strip()
CREDENTIALS_JSON = os.getenv("CREDENTIALS_JSON", "").strip()

# Проверяем, загружены ли переменные
if not TOKEN or not SPREADSHEET_ID or not CREDENTIALS_JSON:
    raise ValueError("❌ Ошибка: отсутствуют необходимые переменные окружения!")

logging.info("✅ Переменные окружения загружены")

# Подключение к Google Sheets
try:
    credentials_dict = json.loads(CREDENTIALS_JSON)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    logging.info("✅ Подключение к Google Sheets успешно!")
except Exception as e:
    logging.error(f"❌ Ошибка при подключении к Google Sheets: {e}")
    raise

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# Словари пользователей и категорий
user_to_row = {'question': 2}  # Пример
user_to_categories = {'question': ["НОМЕРА", "ПЕРЕВОДЫ", "ДИАЛОГИ", "ВБРОС"]}

# Клавиатуры
def create_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Отправить отчет"))
    keyboard.add(KeyboardButton("Просмотр статистики"))
    return keyboard

# Планировщик задач (напоминание)
scheduler = AsyncIOScheduler()

async def send_reminder():
    chat_id = 123456789  # Укажи свой chat_id
    await bot.send_message(chat_id=chat_id, text="🔔 Не забывайте отправить отчет!")

scheduler.add_job(send_reminder, 'cron', hour=18, minute=30, day_of_week='mon-fri')

async def start_scheduler():
    if not scheduler.running:
        scheduler.start()

# Генерация графика
def generate_report_chart(data):
    categories = list(data.keys())
    values = list(data.values())
    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_xlabel("Категории")
    ax.set_ylabel("Значения")
    ax.set_title("📊 Статистика по отчетам")
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

# Обработчики команд
@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("👋 Добро пожаловать! Используйте кнопки ниже.", reply_markup=create_keyboard())

@router.message(lambda message: message.text == "Отправить отчет")
async def handle_report(message: Message):
    await message.answer("📄 Отправьте отчет в формате:\n\nНОМЕРА: 10\nПЕРЕВОДЫ: 5")

@router.message(lambda message: message.text == "Просмотр статистики")
async def show_statistics(message: Message):
    user_name = message.from_user.username

    if user_name not in user_to_row:
        await message.reply("❌ Ошибка: Вы не настроены для записи отчёта")
        return

    row_number = user_to_row[user_name]
    worksheet = sheet.worksheet("Март")
    header = worksheet.row_values(1)
    statistics = "📊 Статистика:\n"
    report_data = {}

    for category in user_to_categories.get(user_name, []):
        if category in header:
            col = header.index(category) + 1
            value = worksheet.cell(row_number, col).value or "0"
            statistics += f"{category}: {value}\n"
            report_data[category] = int(value) if value.isdigit() else 0

    chart_image = generate_report_chart(report_data)
    await message.answer(statistics)
    await bot.send_photo(message.chat.id, chart_image)

# Запуск бота
async def main():
    await start_scheduler()
await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
    
