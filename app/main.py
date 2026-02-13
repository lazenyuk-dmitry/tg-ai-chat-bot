import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.bot.handlers import router
from app.utils.logger import logger


async def main():
    logger.info("Starting Telegram AI Bot...")
    
    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher()
    dp.include_router(router)

    try:
        logger.info("Polling started")
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Bot stopped unexpectedly!")
    finally:
        await bot.session.close()
        logger.info("Bot stopped")


if __name__ == "__main__":
    asyncio.run(main())
