FROM python:3.12-slim

# Установка системных зависимостей для psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    musl-dev \
    libpq-dev \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=DjREST.settings

WORKDIR /app

# Копируем файл зависимостей и устанавливаем пакеты (для кэширования слоя)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем оставшийся код
COPY . .

# Запуск через Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "DjREST.wsgi:application"]
