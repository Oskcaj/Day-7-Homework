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
    "你是一個有10年經驗的專業任務分類助手。\n"
    "請根據使用者輸入內容，判斷這是不是一個關於天氣的查詢。\n\n"
    "如果是查詢天氣，請只需要回覆：weather\n\n"
    "如果不是或聊天，請只需要回覆：chat\n"
    "以上的任何回覆，請不要加入任何其他字元、標點、emoji 或解釋說明。只回覆其中一個單詞即可。"
    )
)

