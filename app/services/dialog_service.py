
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.db.models.message import RoleEnum
from app.services.ai_service import AIService
from app.db.repositories.message_repo import MessageRepo
from app.utils.logger import logger

class DialogService:
    def __init__(self, message_repo: MessageRepo, ai_service: AIService):
        self.message_repo = message_repo
        self.ai_service = ai_service

    async def start_handler(self, message: Message, state: FSMContext, **_) -> None:
        logger.info("User %s sent /start", message.from_user.id)
        await state.clear()
        await self.message_repo.reset_history(message.from_user.id)
        await message.answer(
            "Привет! 👋\n\n"
            "Я AI-бот. Отправь мне сообщение, и я сгенерирую ответ.\n\n"
            "Нажми /help для справки."
        )

    async def help_handler(self, message: Message, **_) -> None:
        logger.info("User %s sent /help", message.from_user.id)
        await message.answer(
            "Доступные команды:\n"
            "/start — сбросить контекст\n"
            "/help — показать справку\n\n"
            "Просто отправь текст для общения с AI."
        )

    async def message_handler(self, message: Message, **_) -> None:
        logger.info("Received text from %s: %s", message.from_user.id, message.text)

        user_id = message.from_user.id
        user_text = message.text

        # Берем историю
        history = await self.message_repo.get_history(user_id)

        # Генерируем ответ
        answer = await self.ai_service.generate_response(user_text, history)

        # Сохраняем сообщение пользователя
        await self.message_repo.add_message(user_id, RoleEnum.USER.value, user_text)

        # Сохраняем ответ AI
        await self.message_repo.add_message(user_id, RoleEnum.MODEL.value, answer)

        # Отправляем ответ пользователю
        await message.answer(answer)
