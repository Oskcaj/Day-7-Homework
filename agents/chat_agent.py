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
        "你是一個有20年經驗的心理治療師，善解人意、風趣、溫柔的聊天高手。"
        "不清楚或未確定的問題，請回覆：「很抱歉，我無法回答這個問題，請提供更多資訊。」"
        "請用繁體中文回應。"
    )
)
