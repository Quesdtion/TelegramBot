# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаем и активируем виртуальную среду
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем файлы приложения
COPY . /app
WORKDIR /app

# Обновляем pip и устанавливаем зависимости с использованием кэша
RUN --mount=type=cache,id=pip-cache-${BUILD_ID},target=/root/.cache/pip pip install --upgrade pip \
    && pip install -r requirements.txt

# Запускаем приложение
CMD ["python", "main.py"]
