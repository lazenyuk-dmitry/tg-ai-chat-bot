import asyncio
from app.bot.service import BotService


async def main():
    bot_service = BotService()
    await bot_service.start()


if __name__ == "__main__":
    asyncio.run(main())
