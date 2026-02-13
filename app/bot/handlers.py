from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from app.utils.logger import logger

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    logger.info(f"User {message.from_user.id} sent /start")
    await message.answer(
        "Привет! 👋\n\n"
        "Я AI-бот. Отправь мне сообщение, и я сгенерирую ответ.\n\n"
        "Нажми /help для справки."
    )


@router.message(Command("help"))
async def help_handler(message: Message):
    logger.info(f"User {message.from_user.id} sent /help")
    await message.answer(
        "Доступные команды:\n"
        "/start — сбросить контекст\n"
        "/help — показать справку\n\n"
        "Просто отправь текст для общения с AI."
    )


@router.message()
async def echo_handler(message: Message):
    logger.info(f"Received text from {message.from_user.id}: {message.text}")
    await message.answer("Сейчас будет ответ от AI... (позже подключим OpenAI)")
