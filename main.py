import os
import chainlit as cl
from dotenv import load_dotenv
from agents.routing_agent import routing_agent
from agents.weather_agent import weather_agent, Deps
from agents.chat_agent import chat_agent
from httpx import AsyncClient

load_dotenv()

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
        print("🔁 進入天氣判斷流程")
        print("🌐 使用者輸入：", user_input)

        async with AsyncClient(verify=False) as client:
            deps = Deps(
                client=client,
                weather_api_key=os.getenv("WEATHER_API_KEY"),
                geo_api_key=os.getenv("GEO_API_KEY")
            )
            print("🧠 呼叫 weather agent...")
            try:
                result = await weather_agent.run(user_input, deps=deps)
                print("✅ 天氣結果：", result.output)
            except Exception as e:
                print("❌ weather_agent 發生錯誤：", e)
                await cl.Message(content="抱歉，查詢天氣時發生錯誤。請稍後再試。").send()
                return

        await cl.Message(content=result.output).send()
    else:
        result = await chat_agent.run(user_input)
        await cl.Message(content=result.output).send()
