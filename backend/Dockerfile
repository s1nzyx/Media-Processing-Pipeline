FROM python:3.14-slim

WORKDIR /app

# Установка системных зависимостей (нужных для Pillow, ffmpeg и т.д.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Порт по умолчанию
EXPOSE 8000