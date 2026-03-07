FROM python:3.12-slim

ENV APP_HOME=/home/appuser/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m appuser

WORKDIR $APP_HOME
RUN chown -R appuser:appuser $APP_HOME

# копируем зависимости
COPY --chown=appuser:appuser requirements.txt .
COPY --chown=appuser:appuser alembic.ini .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# копируем весь проект
COPY --chown=appuser:appuser . .

USER appuser

# запускаем миграции и бот
CMD ["sh", "-c", "alembic upgrade head && python -m app.main"]
