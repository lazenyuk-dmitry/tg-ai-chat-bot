from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.utils.chat_action import ChatActionSender

class TypingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        async with ChatActionSender.typing(bot=event.bot, chat_id=event.chat.id, interval=4.0):
            return await handler(event, data)
