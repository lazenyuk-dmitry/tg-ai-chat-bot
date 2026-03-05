import asyncio
from app.bot.service import BotService
from app.health.health_server import HealthServer


async def main():
    bot_service = BotService()
    health_server = HealthServer(bot_service)

    await health_server.start()
    await bot_service.start()

if __name__ == "__main__":
    asyncio.run(main())
