import openai
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import logging

# Ваш API-ключ OpenAI
openai.api_key = "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"

# Создаём объект бота и диспетчера
API_TOKEN = '7671376837:AAGgp6Vyz2o-IcviYljQz409QQZq-3V5ztI'  # Замените на ваш токен
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Функция для общения с ИИ
async def chat_with_ai(report):
    try:
        # Новый API-метод для общения с ChatGPT
        response = openai.completions.create(
            model="gpt-3.5-turbo",  # или другой доступный модель
            messages=[ 
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": report},
            ],
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        print(f"Ошибка при взаимодействии с AI: {e}")
        return "Произошла ошибка при взаимодействии с ИИ."

# Регулярное выражение для отчета
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
    if match:
        return True
    return False

# Извлечение данных из отчета
def extract_data_from_report(report):
    report_data = {}
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
    if match:
        report_data = {
            'Актив': match.group(1),
            'Новых номеров': f"{match.group(2)} - {match.group(3)}",
            'Кол-во вбросов': match.group(4),
            'Кол-во предложек': match.group(5),
            'Кол-во согласий': match.group(6),
            'Кол-во отказов': match.group(7),
            'Кол-во Обраток': match.group(8),
            'Кол-во лидов': match.group(9),
            'Кол-во депов': match.group(10),
        }
    
    return report_data

# Хэндлер для получения сообщений
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне отчет, и я помогу обработать его или передам ИИ для ответа.")

# Хэндлер для обработки отчетов
@dp.message_handler()
async def handle_report(message: types.Message):
    report = message.text.strip()

    if check_report_format(report):
        # Если это отчет, извлекаем данные
        extracted_data = extract_data_from_report(report)
        response = "Данные из отчета:\n"
        for key, value in extracted_data.items():
            response += f"{key}: {value}\n"
        await message.reply(response)

        # Дополнительный ответ от ИИ
        ai_response = await chat_with_ai(report)
        await message.reply(f"Ответ от ИИ:\n{ai_response}")
    else:
        # Если это не отчет
        await message.reply("Это не отчет. Пожалуйста, отправьте правильный отчет.")

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
