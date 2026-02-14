import asyncio
from app.db.session import async_session
from app.db.models import Message, RoleEnum
from sqlalchemy.future import select
from app.utils.logger import logger
from aiogram.enums import ChatAction
from google.genai import types

class DialogService:
    def __init__(self):
        pass

    async def add_message(self, user_id: int, role: str, content: str):
        async with async_session() as session:
            msg = Message(user_id=user_id, role=role, content=content)
            session.add(msg)
            await session.commit()
            logger.debug(f"Saved message for user {user_id}: {content[:30]}...")

    async def get_history(self, user_id: int, limit: int = 10):
        async with async_session() as session:
            result = await session.execute(
                select(Message)
                .where(Message.user_id == user_id)
                .order_by(Message.id.desc())
                .limit(limit)
            )
            messages = result.scalars().all()
            # возвращаем в порядке от старых к новым
            return [
                types.Content(
                    role='user',
                    parts=[types.Part.from_text(text=msg.content)]
                )
                for msg in reversed(messages)
            ]

    async def reset_history(self, user_id: int):
        async with async_session() as session:
            await session.execute(
                f"DELETE FROM messages WHERE user_id = {user_id}"
            )
            await session.commit()
            logger.info(f"History reset for user {user_id}")
