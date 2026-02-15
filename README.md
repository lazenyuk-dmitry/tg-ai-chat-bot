# 🤖 TG AiChat Bot

Асинхронный Telegram-бот на aiogram 3, использующий OpenAI API и PostgreSQL для хранения истории сообщений.

Проект построен по принципам:

- Clean Architecture
- Разделение зон ответственности
- Dependency Injection
- Async-first подход
- Alembic миграции

---

## 🚀 Стек технологий

- Python 3.12+
- aiogram 3
- SQLAlchemy 2 (async)
- PostgreSQL
- Alembic
- OpenAI API
- pip

---

## 📁 Структура проекта

```
tg-chatgpt-bot/
│
├── app/
│   ├── bot/            # роутеры, хендлеры, telegram-логика
│   ├── services/       # бизнес-логика (ChatGPT, работа с сообщениями)
│   ├── db/
│   │   ├── models.py   # ORM модели
│   │   ├── session.py  # создание AsyncSession
│   │   └── base.py     # Base metadata
│   ├── config.py       # Pydantic settings
│   └── main.py         # точка входа
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── alembic.ini
├── pyproject.toml
├── .env
└── README.md
```

---

## ⚙️ Установка

1️⃣ Клонировать проект:

```bash
git clone https://github.com/yourname/tg-chatgpt-bot.git
cd tg-chatgpt-bot
```

2️⃣ Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

3️⃣ Установить зависимости

```bash
pip install -r requirements.txt
```

---

## 🔐 Настройка окружения

Создай .env файл:

```ini
BOT_TOKEN=your_telegram_token
OPENAI_API_KEY=your_openai_key
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/tg_chatbot
```

---

## 🐳 Docker

```bash
docker compose ud -d
```

---

## 🧱 Миграции

Применить миграции

```bash
alembic upgrade head
```

## ▶️ Запуск бота

```bash
python -m app.main
```
