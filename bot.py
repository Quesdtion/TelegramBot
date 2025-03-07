import logging
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# Токен вашего бота
API_TOKEN = '7671376837:AAGgp6Vyz2o-IcviYljQz409QQZq-3V5ztI'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

def check_report_format(report):
    # Обновленное регулярное выражение для соответствия отчету
    pattern = r"""
    Актив:\s*(\d+)\s*\n
    Новых\s*номеров:\s*(\d+)\s*-\s*(\d+)\s*\n
    Кол-во\s*вбросов:\s*(\d+)\s*\n
    Кол-во\s*предложек:\s*(\d+)\s*\n
    Кол-во\s*согласий:\s*(\d+)\s*\n
    Кол-во\s*отказов:\s*(\d+)\s*\n
    Кол-во\s*Обраток:\s*(\d+)\s*\n
    Кол-во\s*лидов:\s*(\d+)\s*\n
    Кол-во\s*депов:\s*(\d+)
    """
    # Проверка с использованием многострочного шаблона
    match = re.match(pattern, report, re.VERBOSE)
    if match:
        return True
    return False

def extract_data_from_report(report):
    report_data = {}

    # Убираем лишние пробелы и символы из текста отчета
    report = re.sub(r'\s+', ' ', report)  # Заменяем все множественные пробелы на один
    report = re.sub(r'\n+', ' ', report)  # Заменяем все новые строки на пробелы

    # Обновленное регулярное выражение для извлечения данных
    pattern = r"""
    Актив:\s*(\d+)\s*
    Новых\s*номеров:\s*(\d+)\s*-\s*(\d+)\s*
    Кол-во\s*вбросов:\s*(\d+)\s*
    Кол-во\s*предложек:\s*(\d+)\s*
    Кол-во\s*согласий:\s*(\d+)\s*
    Кол-во\s*отказов:\s*(\d+)\s*
    Кол-во\s*Обраток:\s*(\d+)\s*
    Кол-во\s*лидов:\s*(\d+)\s*
    Кол-во\s*депов:\s*(\d+)
    """
    
    # Ищем совпадение с шаблоном
    match = re.match(pattern, report, re.VERBOSE)
    if match:
        # Сохраняем данные в словарь
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

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправьте отчет, и я помогу вам с ним.")

@dp.message_handler(content_types=['text'])
async def handle_report(message: types.Message):
    report = message.text.strip()

    # Проверяем, подходит ли отчет
    if check_report_format(report):
        extracted_data = extract_data_from_report(report)
        response = "Отчет принят!\nИзвлеченные данные:\n"
        
        # Формируем ответ с извлеченными данными
        for key, value in extracted_data.items():
            response += f"{key}: {value}\n"
        
        await message.reply(response)
    else:
        await message.reply("Это не отчет. Пожалуйста, отправьте правильный отчет.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
