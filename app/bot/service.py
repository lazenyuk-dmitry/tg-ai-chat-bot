from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from app.bot.middleware.typing import TypingMiddleware

from app.config import settings
from app.bot.handlers import router
from app.utils.logger import logger
from app.db.session import init_db


class BotService():
    def __init__(self):
        self.bot = Bot(
            token=settings.bot_token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )

        self.dp = Dispatcher()
        self.dp.include_router(router)
        self.dp.message.middleware(TypingMiddleware())

    async def start(self):
        logger.info("Starting Telegram AI Bot...")

        try:
            logger.info("Polling started")
            await init_db() # TODO: вынести в отдельную функцию, чтобы не инициализировать БД при каждом перезапуске бота
            await self.dp.start_polling(self.bot)
        except Exception:
            logger.exception("Bot stopped unexpectedly!")
        finally:
            await self.stop()

    async def stop(self):
        await self.bot.session.close()
        logger.info("Bot stopped")
