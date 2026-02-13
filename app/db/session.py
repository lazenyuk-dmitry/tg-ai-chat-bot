from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.utils.logger import logger
from app.db.base import Base

engine = create_async_engine(settings.database_url, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def test_connection():
    async with async_session() as session:
        try:
            result = await session.execute(text("SELECT 1"))
            logger.info("DB connected success!")
        except Exception as e:
            logger.exception("DB connection failed!")
            raise


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
