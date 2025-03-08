# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем все файлы в контейнер
COPY . /app/

# Обновляем pip и устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем бота
RUN apt-get update && apt-get install -y git
CMD ["python", "bot.py"]

