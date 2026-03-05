from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from app.services.dialog_service import DialogService

router = Router()
ai_router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, dialog_service: DialogService, **kwargs):
    await dialog_service.start_handler(message, **kwargs)

@router.message(Command("help"))
async def help_handler(message: Message, dialog_service: DialogService, **kwargs):
    await dialog_service.help_handler(message, **kwargs)

@ai_router.message()
async def message_handler(message: Message, dialog_service: DialogService, **kwargs):
    await dialog_service.message_handler(message, **kwargs)
