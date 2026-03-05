from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from app.bot.middleware.typing import TypingMiddleware
from app.services.dialog_service import DialogService

from app.config import settings
from app.bot.handlers import router, ai_router
from app.utils.logger import logger


class BotService():
    def __init__(self, dialog_service: DialogService):
        self.bot = Bot(
            token=settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        self.dialog_service=dialog_service

        self.dp = Dispatcher()
        self.dp.include_router(router)
        self.dp.include_router(ai_router)
        ai_router.message.middleware(TypingMiddleware())


    async def start(self) -> None:
        logger.info("Starting Telegram AI Bot...")

        try:
            logger.info("Polling started")
            await self.dp.start_polling(self.bot, dialog_service=self.dialog_service)
        except Exception:
            logger.exception("Bot stopped unexpectedly!")
        finally:
            await self.stop()

    async def stop(self):
        await self.bot.session.close()
        logger.info("Bot stopped")

    async def is_healthy(self):
        try:
            await self.bot.get_me()
            return True
        except Exception:
            return False
