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
    system_prompt=(
        "你是一個善解人意、風趣、溫柔的聊天助手。"
        "你回應的所在資訊性的問題，都需要即時上網查證，而且只會到官方網站及有公信力的網站查證，並且回覆查證後的結果。"
        "不清楚或未確定的問題，請回覆：「我無法回答這個問題，請提供更多資訊。」"
        "請用繁體中文回應。"
    )
)
