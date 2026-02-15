FROM python:3.12-slim

# отключаем .pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# системные зависимости (для asyncpg и psycopg)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# копируем зависимости
COPY requirements.txt ./
COPY alembic.ini ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# копируем весь проект
COPY . .

# запускаем миграции и бот
CMD ["sh", "-c", "alembic upgrade head && python -m app.main"]
