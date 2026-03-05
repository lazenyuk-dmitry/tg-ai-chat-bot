import asyncio
from app.bot.service import BotService
from app.health.health_server import HealthServer
from app.db.service import DatabaseService
from app.services.ai_service import AIService
from app.services.dialog_service import DialogService
from app.db.repositories.message_repo import MessageRepo

async def main():
    db_service = DatabaseService()
    message_repo = MessageRepo(db_service.async_session)
    ai_service = AIService()
    dialog_service = DialogService(message_repo = message_repo, ai_service = ai_service)

    bot_service = BotService(dialog_service)
    health_server = HealthServer(bot_service, db_service)

    await health_server.start()
    await bot_service.start()

if __name__ == "__main__":
    asyncio.run(main())
