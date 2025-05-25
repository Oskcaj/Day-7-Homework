# main.py
import os
import chainlit as cl
from dotenv import load_dotenv
from agents.routing_agent import routing_agent
from agents.weather_agent import weather_agent, Deps
from agents.chat_agent import chat_agent
from httpx import AsyncClient
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

async def translate(text: str, direction: str, translator: Agent) -> str:
    """將文字進行中英文互譯。

    Args:
        text: 原始文字。
        direction: "zh2en" 表示中翻英，"en2zh" 表示英翻中。
        translator: 用來翻譯的 Agent。

    Returns:
        翻譯後的文字。
    """
    prompt = f"請將以下內容翻譯為{'英文' if direction == 'zh2en' else '繁體中文'}：{text}"
    result = await translator.run(prompt)
    return result.output.strip()

# 用 Gemini 建立翻譯模型（可重複使用）
translate_model = OpenAIModel(
    "google/gemini-2.0-flash-lite-001",
    provider=OpenAIProvider(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
)

translate_agent = Agent(
    model=translate_model,
    system_prompt="你是一個翻譯助理，請精確翻譯輸入文字，不要加入解釋。"
)

@cl.on_message
async def on_message(message: cl.Message):
    """處理使用者訊息，根據任務分派到對應的 Agent。

    Args:
        message: 使用者輸入的 Chainlit 訊息物件。
    """
    user_input = message.content
    route = await routing_agent.run(user_input)
    task_type = route.output.strip().lower()

    if "weather" in task_type:
        # 中文翻譯成英文給 weather agent
        translated_input = await translate(user_input, "zh2en", translate_agent)
        async with AsyncClient(verify=False) as client:
            deps = Deps(
                client=client,
                weather_api_key=os.getenv("WEATHER_API_KEY"),
                geo_api_key=os.getenv("GEO_API_KEY")
            )
            result = await weather_agent.run(translated_input, deps=deps)
        # 將英文結果翻回中文
        translated_output = await translate(result.output, "en2zh", translate_agent)
        await cl.Message(content=translated_output).send()
    else:
        result = await chat_agent.run(user_input)
        await cl.Message(content=result.output).send()
        
    if "weather" in task_type:
        print("🔁 進入天氣判斷流程")
        translated_input = await translate(user_input, "zh2en", translate_agent)
        print("🌐 翻譯為英文：", translated_input)

        async with AsyncClient(verify=False) as client:
            deps = Deps(
                client=client,
                weather_api_key=os.getenv("WEATHER_API_KEY"),
                geo_api_key=os.getenv("GEO_API_KEY")
            )
            print("🧠 呼叫 weather agent...")
            try:
                result = await weather_agent.run(translated_input, deps=deps)
                print("✅ 天氣結果：", result.output)
            except Exception as e:
                print("❌ weather_agent 發生錯誤：", e)
                await cl.Message(content="抱歉，查詢天氣時發生錯誤。").send()
                return

        translated_output = await translate(result.output, "en2zh", translate_agent)
        print("🌏 翻譯為中文：", translated_output)
        await cl.Message(content=translated_output).send()
