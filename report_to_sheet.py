import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime

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
    # Открываем таблицу по имени
    sheet = client.open("Название вашего документа").worksheet(sheet_name)

    # Найдем строку для текущей даты
    date_cell = sheet.find(current_date)  # Ищем ячейку с текущей датой в таблице

    if date_cell:
        start_row = date_cell.row  # Получаем номер строки, где находится дата

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

        # Записываем данные в таблицу, начиная с строки, которая соответствует текущей дате
        for i, (key, value) in enumerate(data.items()):
            if key in cell_mapping:
                column = cell_mapping[key]
                cell = f"{column}{start_row + i}"
                if isinstance(value, list):
                    # Если значение это список (например, для "Новых номеров")
                    sheet.update(cell, f"{value[0]} - {value[1]}")
                else:
                    sheet.update(cell, value)

# Пример отчета
report = """Актив: 10
Новых номеров: 2 - 0
Кол-во вбросов: 3
Кол-во предложек: 1
Кол-во согласий: 0
Кол-во отказов: 0
Кол-во Обраток: 1
Кол-во лидов: 1
Кол-во депов: 0
"""

# Получаем текущую дату в формате "ДД.ММ"
current_date = datetime.now().strftime("%d.%m")

# Подключаемся к Google Sheets
client = connect_to_google_sheets('path_to_your_credentials_file.json')

# Извлекаем данные из отчета
extracted_data = extract_data_from_report(report)

# Записываем данные в таблицу на лист "март" для текущей даты
write_data_to_sheet(client, "март", extracted_data, current_date)

print("Данные успешно записаны в таблицу.")

