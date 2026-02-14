from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from app.utils.logger import logger
from app.services.ai_service import AIService
from app.services.dialog_service import DialogService

router = Router()
ai_router = Router()
ai_service = AIService()
dialog_service = DialogService()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} sent /start")
    await state.clear()
    await dialog_service.reset_history(message.from_user.id)
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


@ai_router.message()
async def echo_handler(message: Message):
    logger.info(f"Received text from {message.from_user.id}: {message.text}")

    user_id = message.from_user.id
    text = message.text

    # Сохраняем сообщение пользователя
    await dialog_service.add_message(user_id, "user", text)

    # Берем историю
    history = await dialog_service.get_history(user_id)

    # Добавляем системное сообщение (опционально)
    # if not any(msg['role'] == "system" for msg in history):
    #     history.insert(0, {"role": "system", "content": "Ты помощник, отвечай дружелюбно."})

    # Генерируем ответ
    answer = await ai_service.generate_response(history)

    # Сохраняем ответ AI
    await dialog_service.add_message(user_id, "model", answer)

    # Отправляем пользователю
    await message.answer(answer)
