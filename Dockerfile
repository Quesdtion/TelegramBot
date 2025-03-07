# Убедитесь, что используем правильный базовый образ
FROM python:3.9-slim

# Устанавливаем необходимые зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev

# Копируем requirements.txt в контейнер
COPY requirements.txt /app/requirements.txt

# Устанавливаем виртуальное окружение и зависимости
RUN --mount=type=cache,id=s/222d00e6-0bde-4d48-b06c-40ddd02c66c7-/root/cache/pip,target=/root/.cache/pip \
    python -m venv --copies /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --no-cache-dir -r /app/requirements.txt

# Копируем весь проект в контейнер
COPY . /app

# Устанавливаем рабочую директорию
WORKDIR /app

# Указываем команду для запуска контейнера
CMD ["python", "bot.py"]
