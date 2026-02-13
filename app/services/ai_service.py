from openai import OpenAI
from app.config import settings
from app.utils.logger import logger


class AIService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def generate_response(self, messages: list[dict]) -> str:
        """
        messages: список словарей вида:
        [
            {"role": "system", "content": "Ты помощник"},
            {"role": "user", "content": "Привет"}
        ]
        """
        try:
            logger.info(f"Sending request to OpenAI: {messages[-1]['content']}")
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
            )
            answer = response.choices[0].message.content
            logger.info(f"Received response from OpenAI: {answer[:50]}...")
            return answer
        except Exception as e:
            logger.exception("OpenAI API error")
            return "Извини, произошла ошибка при генерации ответа."
