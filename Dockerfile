# Используем официальный образ Python версии 3.9
FROM python:3.9-slim

# Устанавливаем переменную окружения для отключения буферизации вывода
ENV PYTHONUNBUFFERED=1

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем необходимые системные зависимости
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем Python-зависимости
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt


# Копируем все файлы проекта в рабочую директорию
COPY . .

# Указываем команду для запуска приложения
CMD ["python", "bot.py"]
