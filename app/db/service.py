from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import text
from app.config import settings

class DatabaseService:
    def __init__(self):
        self.engine = create_async_engine(settings.database_url, echo=settings.db_echo)
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def is_healthy(self) -> bool:
        try:
            async with self.async_session() as session:
                await session.execute(text("SELECT 1"))
                return True
        except Exception:
            return False

    async def close(self):
        await self.engine.dispose()
