from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
import os

chat_model = OpenAIModel(
    "google/gemini-2.0-flash-lite-001",
    provider=OpenAIProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
)

chat_agent = Agent(
    model=chat_model,
    system_prompt="你是一個善解人意、風趣、溫柔的聊天助手，永遠用繁體中文回應。"
)
