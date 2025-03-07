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
    # Проверка с использованием многострочного шаблона
    match = re.match(pattern, report, re.VERBOSE)
    if match:
        return True
    return False

def extract_data_from_report(report):
    report_data = {}
    
    # Обновленное регулярное выражение для извлечения данных
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

async def process_report(message: types.Message):
    report = message.text

    # Проверяем, подходит ли отчет
    if check_report_format(report):
        # Если отчет принят, извлекаем данные
        extracted_data = extract_data_from_report(report)
        # Отправляем извлеченные данные в ответ пользователю
        await message.answer(f"Отчет принят! Вот извлеченные данные:\n{extracted_data}", parse_mode=ParseMode.MARKDOWN)
    else:
        # Если формат отчета некорректный
        await message.answer("Это не отчет. Пожалуйста, отправьте правильный отчет.")

# Хэндлер для текстовых сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    # Вызовем функцию для обработки отчета
    await process_report(message)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
