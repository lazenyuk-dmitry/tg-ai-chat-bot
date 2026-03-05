# 🤖 TG AiChat Bot

Асинхронный Telegram-бот на aiogram 3, просто отправляет запрос в API сервиса AI для генерации ответа.
Ипользует Gemini и PostgreSQL для хранения истории сообщений.

Cсылка на работающий бот [AiChat Bot](https://t.me/ai_chat_xbot)

Весь процесс установки зависимостей и запуска в docker для production выполняется одной командой.
Для проекта выбран Gemini (gemini-2.5-flash) так как он предоставляет бесплатный тариф.
Gemini вроде бы умеет сохранять контекст самомтоятельно, но в рамках тестового проекта контекст храниться в PostgreSQL (последние 10 сообщений).
Пример работающего бота развернут на бесплатном инстансе Oracle Cloud Free Tier.

Проект построен по принципам:

- Clean Architecture
- Разделение зон ответственности
- Dependency Injection
- Async-first подход
- Alembic миграции

---

## 🚀 Стек технологий

- Python 3.12+
- Docker
- aiogram 3
- SQLAlchemy 2 (async)
- PostgreSQL
- Alembic
- genai
- pip

---

## 📁 Структура проекта

```
tg-chatgpt-bot/
│
├── alembic/           # миграции
│   ├── versions/
│   └── env.py
|
├── app/
│   ├── bot/                # роутеры, хендлеры, telegram-логика
│   ├── services/           # бизнес-логика (ChatGPT, работа с сообщениями)
│   ├── db/
│   │   ├── models/         # ORM модели
│   │   ├── session.py      # создание AsyncSession
│   │   └── base.py         # Base metadata
│   ├── config.py           # Pydantic settings
│   └── main.py             # точка входа
│
├── alembic.ini
├── .gitignore
├── .env.example
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements-dev.txt    # зависимости для разработки
├── requirements.txt        # остальные зависимости
└── README.md
```

---

## ⚙️ Подготовка и настройка

1️⃣ Клонировать проект:

```bash
git clone https://github.com/yourname/tg-chatgpt-bot.git
cd tg-chatgpt-bot
```

2️⃣ Создай .env файл (можно копировать и переименовать .env.example -> .env) в корне проекта:

```bash
cp .env.example .env
```

```ini
BOT_TOKEN=XXX
AI_API_KEY=XXX
DB_USER=admin
DB_PASSWORD=admin
DB_NAME=tg-ai-bot
DB_HOST="localhost" # для разработки "localhost" для прода db
DB_PORT=5432
HEALTH_PORT=8000
```

---

## 🐳 Запуск в Docker (production)

```bash
docker compose up -d
```

---

## 🛠️ Локальный запуск (development)

1️⃣ Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

2️⃣ Установить зависимости

```bash
pip install -r requirements-dev.txt
```

3️⃣ Поднять сервис базы данных в docker если нужно

```bash
docker compose up db -d
```

4️⃣ Если нужно применить мограции

```bash
alembic upgrade head
```

5️⃣ Запустить бота

- Запуск со слежением за изменениями:

```bash
watchmedo auto-restart --patterns="*.py;*.env" --recursive -- python -m app.main
```

- или просто запуск приложения (при изменение файлов нужно перезапустить вручную):

```bash
python -m app.main
```
