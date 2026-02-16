from aiogram import Router
from aiogram.filters import CommandStart, Command
from app.services.ai_service import AIService
from app.services.dialog_service import DialogService
from app.db.repositories.message_repo import MessageRepo
from app.db.session import async_session

router = Router()
ai_router = Router()
message_repo = MessageRepo(async_session)
ai_service = AIService()
dialog_service = DialogService(message_repo = message_repo, ai_service = ai_service)

router.message(CommandStart())(dialog_service.start_handler)
router.message(Command("help"))(dialog_service.help_handler)
ai_router.message()(dialog_service.message_handler)
