import re
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Ваш токен бота Telegram
API_TOKEN = 'YOUR_API_TOKEN'

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Подключение к Google Sheets с использованием учетных данных
def connect_to_google_sheets(credentials_file):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)
    client = gspread.authorize(creds)
    return client

# Функция для извлечения данных из отчета
def extract_data_from_report(report):
    report_data = {}
    lines = report.split('\n')
    for line in lines:
        match = re.match(r"([А-Яа-я\s]+):\s*(\d+\s*-\s*\d+|\d+)", line)
        if match:
            key = match.group(1).strip()
            value = match.group(2)
            if '-' in value:
                value = value.split(' - ')  # Разделяем значения по " - "
            report_data[key] = value
    return report_data

# Функция для записи данных в Google Sheets
def write_data_to_sheet(client, sheet_name, data, current_date):
    sheet = client.open("Название вашего документа").worksheet(sheet_name)

    # Найдем строку для текущей даты
    date_cell = sheet.find(current_date)

    if date_cell:
        start_row = date_cell.row  # Получаем номер строки для текущей даты

        # Сопоставление извлеченных данных с ячейками в таблице
        cell_mapping = {
            'Актив': 'A',
            'Новых номеров': 'B',
            'Кол-во вбросов': 'C',
            'Кол-во предложек': 'D',
            'Кол-во согласий': 'E',
            'Кол-во отказов': 'F',
            'Кол-во Обраток': 'G',
            'Кол-во лидов': 'H',
            'Кол-во депов': 'I',
        }

        # Записываем данные в таблицу, начиная с строки для текущей даты
        for i, (key, value) in enumerate(data.items()):
            if key in cell_mapping:
                column = cell_mapping[key]
                cell = f"{column}{start_row + i}"
                if isinstance(value, list):
                    sheet.update(cell, f"{value[0]} - {value[1]}")
                else:
                    sheet.update(cell, value)

# Обработчик сообщений
@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_report(message: types.Message):
    # Пример отчета, который бот должен обработать
    report = message.text

    # Проверим, содержит ли сообщение отчет
    if re.match(r".*Актив:.*Новых номеров:.*Кол-во вбросов:.*", report):  # Паттерн для простого отчета
        # Получаем текущую дату
        current_date = datetime.now().strftime("%d.%m")
        
        # Подключаемся к Google Sheets
        client = connect_to_google_sheets('path_to_your_credentials_file.json')

        # Извлекаем данные из отчета
        extracted_data = extract_data_from_report(report)

        # Записываем данные в таблицу на лист "март" для текущей даты
        write_data_to_sheet(client, "март", extracted_data, current_date)

        # Отправляем подтверждение пользователю
        await message.reply("Отчет успешно принят и записан в таблицу.")
    else:
        # Если это не отчет, отправляем пользователю сообщение
        await message.reply("Это не отчет. Пожалуйста, отправьте правильный отчет.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
