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
    "請根據使用者輸入內容，判斷這是不是一個關於天氣查詢的問題。\n"
    "如果是，請只回覆：weather\n"
    "如果不是，請只回覆：chat\n"
    "不要加入任何其他字元、標點、emoji 或解釋說明。只回覆其中一個詞即可。"
)
    )

