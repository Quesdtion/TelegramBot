# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем зависимости для работы с Google Sheets
RUN pip install --no-cache-dir gspread google-auth aiogram matplotlib apscheduler

# Копируем все файлы проекта в контейнер
COPY . /app

# Переходим в директорию с кодом
WORKDIR /app

# Устанавливаем все зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем переменную окружения
ENV PYTHONUNBUFFERED 1

# Запускаем бота
CMD ["python", "bot.py"]
