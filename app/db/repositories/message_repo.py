from typing import Iterator
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models.message import Message, RoleEnum
from app.utils.logger import logger


class MessageRepo:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def add_message(self, user_id: int, role: RoleEnum, content: str) -> None:
        async with self.async_session() as session:
            msg = Message(user_id=user_id, role=role, content=content)
            session.add(msg)
            await session.commit()
            logger.debug("Saved message for user %s: %s...", user_id, content[:30])


    async def reset_history(self, user_id: int) -> None:
        async with self.async_session() as session:
            stmt = delete(Message).where(Message.user_id == user_id)
            await session.execute(stmt)
            await session.commit()
            logger.info("History reset for user %s", user_id)

    async def get_history(self, user_id: int, limit: int = 10) -> Iterator[Message]:
        async with self.async_session() as session:
            result = await session.execute(
                select(Message)
                .where(Message.user_id == user_id)
                .order_by(Message.id.desc())
                .limit(limit)
            )
            return reversed(result.scalars().all())
