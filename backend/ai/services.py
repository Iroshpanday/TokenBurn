import os
from openai import OpenAI, RateLimitError

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

class AIService:

    @staticmethod
    def generate_response(message: str):
        try:
            response = client.chat.completions.create(
                model="nex-agi/nex-n2.5-pro:free",
                messages=[{"role": "user", "content": message}],
            )

            return {
                "success": True,
                "response": response.choices[0].message.content,
            }

        except RateLimitError:
            return {
                "success": False,
                "error": "Provider is busy. Please try again in a few seconds.",
            }