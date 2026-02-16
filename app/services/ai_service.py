from typing import Iterator
from google.genai import Client, types
from app.db.models.message import Message, RoleEnum
from app.config import settings
from app.utils.logger import logger


class AIService:
    def __init__(self):
        self.client = Client(api_key=settings.ai_api_key).aio

    async def generate_response(self, message: str, history: Iterator[Message]) -> str:
        """
        Подготавливает список сообщений для генерации ответа.
        [
            {"role": "user", "parts": ["Привет", "Как дела?"]},
            {"role": "model", "parts": ["Привет! У меня все хорошо, спасибо! Чем могу помочь?"]},
                ...
        ]
        """
        try:
            messages_list = [
                {
                    "role": msg.role.value,
                    "content": msg.content,
                }
                for msg in history
            ]
            messages_list.append({
                "role": RoleEnum.USER.value,
                "content": message,
            })

            contents = [
                types.Content(
                    role=msg["role"],
                    parts=[types.Part.from_text(text=msg["content"])]
                )
                for msg in messages_list
            ]

            logger.info("Sending request to AI: %s...", message[:50])
            response = await self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction="Ты — дружелюбный ИИ-помощник. Будь вежлевым.",
                    max_output_tokens=1000,
                    temperature=0.7,
                ),
            )
            answer = response.text
            logger.info("Received response from AI: %s...", answer[:50])
            return answer
        except Exception:
            logger.exception("AI API error")
            return "Извини, произошла ошибка при генерации ответа."
