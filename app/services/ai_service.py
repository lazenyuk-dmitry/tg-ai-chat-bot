from openai import OpenAI
from app.config import settings
from app.utils.logger import logger
from google.genai import Client, types


class AIService:
    def __init__(self):
        self.client = Client(api_key=settings.openai_api_key).aio

    async def generate_response(self, messages: list[dict]) -> str:
        """
        messages: список словарей вида:
        [
            {"role": "system", "content": "Ты помощник"},
            {"role": "user", "content": "Привет"}
        ]
        """
        print(messages)
        try:
            # logger.info(f"Sending request to OpenAI: {messages[-1]['parts'][0].text[:50]}...")
            response = await self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction="Ты — дружелюбный ИИ-помощник. Отвечай на языке пользователя. Будь лаконичен.",
                    max_output_tokens=1000,
                    temperature=0.7,
                ),
            )
            answer = response.text
            logger.info(f"Received response from OpenAI: {answer[:50]}...")
            return answer
        except Exception as e:
            logger.exception("OpenAI API error")
            return "Извини, произошла ошибка при генерации ответа."
        finally:
            if hasattr(self, "typing_task"):
                self.typing_task.cancel()
