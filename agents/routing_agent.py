from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os

routing_model = OpenAIModel(
    "google/gemini-2.0-flash-lite-001",
    provider=OpenAIProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
)

routing_agent = Agent(
    model=routing_model,
    system_prompt=(
        "你是一個任務分類助手。\n"
        "如果以下句子是在詢問天氣，請回覆 'weather'。\n"
        "否則回覆 'chat'。"
    )
)
