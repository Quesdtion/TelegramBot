import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import re

# Вставьте ваш API ключ OpenAI
openai.api_key = "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"

# Вставьте ваш ключ Telegram бота
API_TOKEN = '7671376837:AAGgp6Vyz2o-IcviYljQz409QQZq-3V5ztI'

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Функция для проверки, является ли сообщение отчетом
def check_report_format(report):
    pattern = r"""
    Актив:\s*(\d+)\n
    Новых\s*номеров:\s*(\d+)\s*-\s*(\d+)\n
    Кол-во\s*вбросов:\s*(\d+)\n
    Кол-во\s*предложек:\s*(\d+)\n
    Кол-во\s*согласий:\s*(\d+)\n
    Кол-во\s*отказов:\s*(\d+)\n
    Кол-во\s*Обраток:\s*(\d+)\n
    Кол-во\s*лидов:\s*(\d+)\n
    Кол-во\s*депов:\s*(\d+)
    """
    match = re.match(pattern, report, re.VERBOSE)
    return match is not None

# Функция для общения с AI
async def chat_with_ai(message_text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # или другой доступный модель
            messages=[ 
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message_text},
            ],
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Ошибка при взаимодействии с AI: {e}")
        return "Произошла ошибка при взаимодействии с ИИ."

# Обработка команд
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот, готов к работе!")

# Обработка всех текстовых сообщений
@dp.message_handler()
async def handle_message(message: types.Message):
    user_message = message.text.strip()

    # Проверяем, является ли сообщение отчетом
    if check_report_format(user_message):
        ai_response = await chat_with_ai(user_message)
        await message.reply(f"Ответ на отчет от ИИ:\n{ai_response}")
    else:
        # Бот общается с пользователем, если это не отчет
        ai_response = await chat_with_ai(user_message)
        await message.reply(f"Ответ от ИИ:\n{ai_response}")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
