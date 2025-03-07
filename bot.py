import os
import json
import gspread
import logging
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from google.oauth2.service_account import Credentials
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import matplotlib.pyplot as plt
import io

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения
TOKEN = os.getenv("BOT_TOKEN", "").strip()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID", "").strip()
credentials_json = os.getenv("CREDENTIALS_JSON", "").strip()

# Проверяем, загружены ли переменные
if not TOKEN or not SPREADSHEET_ID or not credentials_json:
    raise ValueError("Ошибка: отсутствуют необходимые переменные окружения!")

logging.info("✅ Переменные окружения загружены")

# Подключаемся к Google Sheets API
try:
    credentials_dict = json.loads(credentials_json)
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(credentials_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    logging.info("✅ Подключение к Google Sheets успешно!")
except Exception as e:
    logging.error(f"Ошибка при подключении к Google Sheets: {e}")
    raise

# Подключаем Telegram-бота
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

# Настраиваем планировщик
scheduler = AsyncIOScheduler()

async def send_reminder():
    chat_id = 123456789  # Укажи реальный chat_id или загрузи его из базы
    try:
        await bot.send_message(chat_id, "Не забывайте отправить отчет! 📝")
    except Exception as e:
        logging.error(f"Ошибка при отправке напоминания: {e}")

scheduler.add_job(send_reminder, 'cron', hour=18, minute=30, day_of_week='mon-fri')

# Генерация графика
def generate_report_chart(data):
    if not data:
        return None  # Если данных нет, не создаём график

    categories = list(data.keys())
    values = list(data.values())

    fig, ax = plt.subplots()
    ax.bar(categories, values)
    ax.set_xlabel("Категории")
    ax.set_ylabel("Значения")
    ax.set_title("Статистика по отчетам")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    return buf

# Обработчики команд
@router.message(commands=['start'])
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать! Используйте кнопки ниже.", reply_markup=create_keyboard())

@router.message(lambda message: message.text == "Отправить отчет")
async def handle_report(message: Message):
    await message.answer("Отправьте отчет в формате: \nНОМЕРА: 10\nПЕРЕВОДЫ: 5")

@router.message(lambda message: message.text == "Просмотр статистики")
async def show_statistics(message: Message):
    user_name = message.from_user.username

    if user_name not in user_to_row:
        await message.reply("Ошибка: Вы не настроены для записи отчёта ❌")
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

    await message.answer(statistics)

    chart_image = generate_report_chart(report_data)
    if chart_image:
        await bot.send_photo(message.chat.id, chart_image)
    else:
        await message.answer("Нет данных для построения графика.")

# Запуск бота
async def main():
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if name == "__main__":
    asyncio.run(main())
