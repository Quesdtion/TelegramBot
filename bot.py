import logging
import openai
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Установите ваш API ключ для OpenAI
openai.api_key = "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"

# Инициализация бота
API_TOKEN = '7671376837:AAGgp6Vyz2o-IcviYljQz409QQZq-3V5ztI'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Функция для общения с ИИ
async def chat_with_ai(report):
    try:
        # Новый API-метод для общения с ChatGPT
        response = openai.ChatCompletion.create(
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

# Функция для проверки формата отчета
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

# Функция для извлечения данных из отчета
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

# Обработчик сообщений
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправьте отчет, и я помогу его обработать.")

@dp.message_handler()
async def handle_report(message: types.Message):
    report = message.text.strip()

    # Проверяем, соответствует ли сообщение отчету
    if check_report_format(report):
        await message.reply("Отчет принят! Обрабатываю...")

        # Извлекаем данные из отчета
        extracted_data = extract_data_from_report(report)
        print(extracted_data)

        # Отправляем отчет в OpenAI для анализа
        ai_response = await chat_with_ai(report)

        # Отправляем ответ от ИИ
        await message.reply(f"Ответ ИИ:\n{ai_response}")

    else:
        await message.reply("Это не отчет. Пожалуйста, отправьте правильный отчет.")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
