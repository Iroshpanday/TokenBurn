import os
import time

from openai import OpenAI

from .models import AIRequest

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

MODEL_NAME = "nvidia/nemotron-3.5-lightning:free"

# USD per 1M tokens
MODEL_PRICING = {
    "nvidia/nemotron-3.5-lightning:free": {"input": 0.0, "output": 0.0},
}


class AIService:

    @staticmethod
    def calculate_cost(model, input_tokens, output_tokens):
        pricing = MODEL_PRICING.get(model, {"input": 0.0, "output": 0.0})
        return (
            input_tokens * pricing["input"] + output_tokens * pricing["output"]
        ) / 1_000_000

    @staticmethod
    def generate_response(message, project, organization_id):
        start = time.time()

        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": message}],
            )

            latency_ms = (time.time() - start) * 1000
            answer = response.choices[0].message.content
            input_tokens = response.usage.prompt_tokens
            output_tokens = response.usage.completion_tokens

            AIRequest.objects.create(
                organization_id=organization_id,
                project=project,
                prompt=message,
                response=answer,
                model_name=MODEL_NAME,
                status="success",
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost=AIService.calculate_cost(MODEL_NAME, input_tokens, output_tokens),
                latency_ms=latency_ms,
            )

            return {"success": True, "response": answer}

        except Exception as e:
            latency_ms = (time.time() - start) * 1000

            AIRequest.objects.create(
                organization_id=organization_id,
                project=project,
                prompt=message,
                model_name=MODEL_NAME,
                status="failed",
                error_message=str(e),
                latency_ms=latency_ms,
            )

            return {"success": False, "error": str(e)}
